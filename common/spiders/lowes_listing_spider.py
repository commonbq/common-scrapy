from __future__ import annotations

"""Lowe's listings extracted only from server-rendered bootstrap state."""

from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.lowes_categories import LOWES_CATEGORIES
from common.spiders.retail_bootstrap_utils import extract_items_from_unknown_state, extract_preloaded_state


class LowesListingSpider(BaseListingSpider):
    name = "lowes_listing"
    allowed_domains = ["lowes.com", "www.lowes.com"]
    categories = LOWES_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "brand", "url", "image_url", "price",
            "original_price", "currency", "rating", "reviews_count",
            "availability", "category", "page", "position", "source", "raw",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError("Provide category, category_url, or url")
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, url: str, page: int) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(url, page), headers=self.headers, callback=self.parse,
            meta={"proxy": self._proxy(), "page": page}, dont_filter=True,
        )

    def _proxy(self) -> str | None:
        proxy = self.settings.get("PROXY")
        if not proxy or "scrapeops" not in proxy.lower():
            return proxy
        parts = urlsplit(proxy)
        if not parts.hostname or parts.password is None:
            return proxy
        username = parts.username or ""
        for option in ("residential=true", "bypass=5"):
            if option not in username:
                username += f".{option}"
        return urlunsplit((parts.scheme, f"{username}:{parts.password}@{parts.hostname}:{parts.port}", parts.path, parts.query, parts.fragment))

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query) if k != "page"]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Lowe's returned HTTP {response.status}: {response.url}")
        lower = response.text[:300000].lower()
        if any(marker in lower for marker in ("access denied", "captcha", "pardon the interruption", "failed to get successful response")):
            raise RuntimeError(f"Lowe's returned a challenge/proxy page: {response.url}")
        state = extract_preloaded_state(response.text)
        if not state:
            raise RuntimeError(f"Lowe's response has no __PRELOADED_STATE__: {response.url}")
        records = extract_items_from_unknown_state(state, "lowes_preloaded_state")
        if not records:
            records = self._product_records(state)
        if not records:
            raise RuntimeError(f"Lowe's __PRELOADED_STATE__ has no products (keys={sorted(state)}): {response.url}")
        page = int(response.meta.get("page", 1))
        emitted = 0
        for position, record in enumerate(records, 1):
            item_id = str(record.get("item_id") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            record.update(
                item_id=item_id,
                url=urljoin(response.url, record.get("url") or ""),
                category=self.category or "custom",
                page=page,
                position=position,
                source="lowes_preloaded_state",
            )
            emitted += 1
            yield record
        if emitted and page < self.max_pages:
            yield self._request(response.url, page + 1)

    @classmethod
    def _product_records(cls, node: Any) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        if isinstance(node, list):
            for value in node:
                found.extend(cls._product_records(value))
            return found
        if not isinstance(node, dict):
            return found
        item_id = node.get("productId") or node.get("itemId") or node.get("omniItemId")
        title = node.get("productName") or node.get("title") or node.get("description")
        if item_id and isinstance(title, str):
            price_node = node.get("price") or node.get("pricing") or node.get("priceInfo") or {}
            if not isinstance(price_node, dict):
                price_node = {"value": price_node}
            found.append({
                "item_id": item_id,
                "title": title,
                "brand": node.get("brand") or node.get("brandName"),
                "url": node.get("productUrl") or node.get("url"),
                "image_url": node.get("imageUrl") or node.get("image"),
                "price": price_node.get("value") or price_node.get("currentPrice") or price_node.get("sellingPrice") or node.get("priceValue"),
                "original_price": price_node.get("originalPrice") or price_node.get("wasPrice"),
                "currency": price_node.get("currency") or "USD",
                "rating": node.get("rating") or node.get("averageRating"),
                "reviews_count": node.get("reviewCount") or node.get("reviewsCount"),
                "availability": node.get("availability") or node.get("inventoryStatus"),
                "raw": node,
            })
            return found
        for value in node.values():
            found.extend(cls._product_records(value))
        return found
