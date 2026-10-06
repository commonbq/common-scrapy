from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.harborfreight_categories import HARBORFREIGHT_CATEGORIES
from common.spiders.retail_bootstrap_utils import extract_apollo_state


class HarborfreightListingSpider(BaseListingSpider):
    """Harbor Freight PLP products from server-rendered Apollo hydration only."""

    name = "harborfreight_listing"
    allowed_domains = ["harborfreight.com", "www.harborfreight.com"]
    categories = HARBORFREIGHT_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "item_id", "sku", "title",
            "brand", "url", "image_url", "price", "regular_price", "currency",
            "page", "position", "total_count", "total_pages", "timestamp",
            "source", "raw",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError("Provide category, category_url, or url")
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        selected = next((e for e in self.categories if e["url"] == target), {})
        yield self._request(target, 1, selected)

    def _request(self, base_url: str, page: int, selected: dict[str, Any]):
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta={"page": page, "base_url": base_url,
                  "category": self.category or selected.get("category") or "custom",
                  "department": selected.get("department"),
                  "subcategory": selected.get("subcategory")},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query) if k != "p"]
        query.append(("p", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Harbor Freight returned HTTP {response.status}: {response.url}")
        state = extract_apollo_state(response.text)
        if not state:
            lower = response.text.lower()
            if any(marker in lower for marker in ("captcha", "pardon the interruption", "failed to get successful response")):
                raise RuntimeError(f"Harbor Freight returned a bot/proxy challenge: {response.url}")
            raise RuntimeError(f"Harbor Freight Apollo hydration is missing or malformed: {response.url}")
        result = self._products_result(state, int(response.meta["page"]))
        refs = result.get("items")
        if not isinstance(refs, list) or not refs:
            raise RuntimeError(f"Harbor Freight hydration has no product references: {response.url}")
        page_info = result.get("page_info") or {}
        total_count = self._integer(result.get("total_count"))
        total_pages = self._integer(page_info.get("total_pages")) or 1
        emitted = 0
        for position, ref in enumerate(refs, 1):
            key = ref.get("__ref") if isinstance(ref, dict) else None
            entity = state.get(key) if key else None
            if not isinstance(entity, dict):
                continue
            sku = str(entity.get("sku") or entity.get("id") or "").strip()
            if not sku or sku in self._seen:
                continue
            self._seen.add(sku)
            emitted += 1
            yield self._item(entity, response, position, total_count, total_pages)
        page = int(response.meta["page"])
        if emitted and page < min(self.max_pages, total_pages):
            yield self._request(response.meta["base_url"], page + 1, response.meta)

    @staticmethod
    def _products_result(state: dict[str, Any], expected_page: int) -> dict[str, Any]:
        root = state.get("ROOT_QUERY")
        if not isinstance(root, dict):
            raise RuntimeError("Harbor Freight Apollo hydration has no ROOT_QUERY")
        candidates = [(key, value) for key, value in root.items()
                      if key.startswith("products(") and isinstance(value, dict)]
        if not candidates:
            raise RuntimeError("Harbor Freight Apollo hydration has no products query")
        for key, value in candidates:
            if f'"currentPage":{expected_page}' in key:
                return value
        return candidates[0][1]

    def _item(self, entity, response, position, total_count, total_pages):
        minimum = ((entity.get("price_range") or {}).get("minimum_price") or {})
        final = minimum.get("final_price") or {}
        regular = minimum.get("regular_price") or {}
        image = entity.get("small_image") or {}
        canonical = entity.get("canonical_url")
        return {
            "category": response.meta.get("category"), "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"), "item_id": str(entity.get("id") or entity.get("sku")),
            "sku": str(entity.get("sku")) if entity.get("sku") is not None else None,
            "title": entity.get("name"), "brand": entity.get("Brand") or entity.get("brand"),
            "url": urljoin("https://www.harborfreight.com/", canonical) if canonical else None,
            "image_url": image.get("url") if isinstance(image, dict) else None,
            "price": self._number(final.get("value")), "regular_price": self._number(regular.get("value")),
            "currency": final.get("currency") or regular.get("currency") or "USD",
            "page": int(response.meta["page"]), "position": position, "total_count": total_count,
            "total_pages": total_pages, "timestamp": self.get_timestamp(),
            "source": "harborfreight_apollo_bootstrap", "raw": entity,
        }

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
