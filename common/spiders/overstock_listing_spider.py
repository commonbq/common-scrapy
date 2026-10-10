from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.overstock_categories import OVERSTOCK_CATEGORIES


_FLIGHT_CHUNK_RE = re.compile(
    r'self\.__next_f\.push\(\[\s*1\s*,\s*("(?:[^"\\]|\\.)*")\s*\]\)', re.DOTALL
)
_CHALLENGE_MARKERS = (
    "access denied", "are you a human", "captcha", "request unsuccessful",
    "proxy authentication required",
)

class OverstockListingSpider(BaseListingSpider):
    """Overstock listings from the server-rendered Next.js RSC hydration."""

    name = "overstock_listing"
    allowed_domains = ["overstock.com", "www.overstock.com", "localhost", "127.0.0.1"]

    categories = OVERSTOCK_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "category_id", "category_name",
            "item_id", "sku", "option_id", "title", "url", "image_url", "price",
            "currency", "discount", "rating", "reviews_count", "is_spa", "page",
            "position", "hits_per_page", "total_pages", "sort_order", "search_filter",
            "grs_filter", "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target_url = self.resolve_target_url()
        target = self.category_entry(self.category) or {
            "group": None,
            "category": self.category or self._slug_from_url(target_url),
            "subcategory": None,
            "url": target_url,
        }
        yield scrapy.Request(
            target_url, callback=self.parse, headers=self._html_headers(),
            meta={"target": target, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        self._reject_challenge(response)
        page = int(response.meta.get("page", 1))
        target = response.meta["target"]
        payload = self._flight_payload(response.text)
        tracking = self._view_item_list(payload)
        ecommerce = tracking.get("ecommerce")
        if not isinstance(ecommerce, dict):
            raise RuntimeError(f"Overstock RSC viewItemList at {response.url} has no ecommerce object")
        products = ecommerce.get("items")
        if not isinstance(products, list) or not products:
            if page > 1:
                return
            raise RuntimeError(f"Overstock RSC ecommerce payload at {response.url} has no products")

        pagination = self._pagination(payload)
        urls = self._product_urls(payload)
        for index, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("product_id") or "").strip()
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            product_index = self._integer(product.get("index"))
            yield {
                "category": target["category"],
                "department": target.get("department"),
                "subcategory": target.get("subcategory"),
                "category_id": ecommerce.get("item_list_id"),
                "category_name": ecommerce.get("item_list_name"),
                "item_id": item_id,
                "sku": self._string(product.get("item_id")),
                "option_id": product.get("option_id"),
                "title": product.get("item_name"),
                "url": urls.get(item_id),
                "image_url": product.get("image_url"),
                "price": self._number(product.get("price")),
                "currency": "USD" if product.get("price") is not None else None,
                "discount": self._number(product.get("discount")),
                "rating": self._number(product.get("product_rating")),
                "reviews_count": self._integer(product.get("product_num_reviews")),
                "is_spa": product.get("is_spa"),
                "page": self._integer(ecommerce.get("page_number")) or page,
                "position": product_index + 1 if product_index is not None else index,
                "hits_per_page": pagination.get("hitsPerPage"),
                "total_pages": pagination.get("totalPages"),
                "sort_order": ecommerce.get("sort_order"),
                "search_filter": ecommerce.get("search_filter"),
                "grs_filter": ecommerce.get("grs_filter"),
                "source_url": response.url,
                "source": "overstock_nextjs_rsc_view_item_list",
                "raw": dict(product),
                "timestamp": self.get_timestamp().isoformat(),
            }

        if page >= self.max_pages:
            return
        next_url = pagination.get("nextPageUrl")
        total_pages = self._integer(pagination.get("totalPages"))
        if not next_url or (total_pages is not None and page >= total_pages):
            return
        yield scrapy.Request(
            str(next_url), callback=self.parse, headers=self._html_headers(),
            meta={**response.meta, "page": page + 1},
        )

    @classmethod
    def _flight_payload(cls, document: str) -> str:
        chunks = _FLIGHT_CHUNK_RE.findall(document or "")
        if not chunks:
            raise RuntimeError("No self.__next_f RSC hydration chunks in the Overstock response")
        return "".join(json.loads(chunk) for chunk in chunks)

    @classmethod
    def _view_item_list(cls, payload: str) -> dict[str, Any]:
        marker = '"viewItemList":'
        start = payload.find(marker)
        if start < 0:
            raise RuntimeError("Overstock RSC hydration has no viewItemList bootstrap data")
        try:
            value, _ = json.JSONDecoder().raw_decode(payload, start + len(marker))
        except ValueError as exc:
            raise RuntimeError("Overstock viewItemList bootstrap data is malformed") from exc
        if not isinstance(value, dict):
            raise RuntimeError("Overstock viewItemList bootstrap data is not an object")
        return value

    @classmethod
    def _pagination(cls, payload: str) -> dict[str, Any]:
        marker = '"hitsPerPage":'
        start = payload.find(marker)
        if start < 0:
            return {}
        object_start = payload.rfind("{", 0, start)
        try:
            value, _ = json.JSONDecoder().raw_decode(payload, object_start)
        except ValueError:
            return {}
        return value if isinstance(value, dict) else {}

    @classmethod
    def _product_urls(cls, payload: str) -> dict[str, str]:
        urls: dict[str, str] = {}
        for line in payload.splitlines():
            if '"data-testid":"product-' not in line:
                continue
            try:
                node = json.loads(line.split(":", 1)[-1])
            except (TypeError, ValueError):
                continue
            cls._collect_product_urls(node, urls)
        return urls

    @classmethod
    def _collect_product_urls(cls, node: Any, urls: dict[str, str]) -> None:
        if isinstance(node, list):
            if len(node) >= 4 and node[0] == "$" and node[1] == "article":
                item_id = str(node[2] or "")
                href = cls._find_href(node[3])
                if item_id and href:
                    urls[item_id] = cls._canonical_url(href)
            for child in node:
                cls._collect_product_urls(child, urls)
        elif isinstance(node, dict):
            for child in node.values():
                cls._collect_product_urls(child, urls)

    @classmethod
    def _find_href(cls, node: Any) -> str | None:
        if isinstance(node, dict):
            href = node.get("href")
            if isinstance(href, str) and "/product.html" in href:
                return href
            for child in node.values():
                found = cls._find_href(child)
                if found:
                    return found
        elif isinstance(node, list):
            for child in node:
                found = cls._find_href(child)
                if found:
                    return found
        return None

    @staticmethod
    def _canonical_url(url: str) -> str:
        parts = urlsplit(url)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

    def _reject_challenge(self, response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(f"Overstock returned HTTP {response.status} for {response.url}")
        head = response.text[:5000].lower()
        marker = next((value for value in _CHALLENGE_MARKERS if value in head), None)
        if marker:
            raise RuntimeError(f"Overstock returned a challenge body at {response.url} (matched {marker!r})")

    @staticmethod
    def _slug_from_url(url: str) -> str:
        return urlsplit(url).path.rstrip("/").split("/")[-1] or "overstock"

    @staticmethod
    def _html_headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _string(value: Any) -> str | None:
        return str(value) if value is not None else None

    @staticmethod
    def _number(value: Any) -> float | int | None:
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            parsed = float(str(value).replace(",", "").replace("$", ""))
            return int(parsed) if parsed.is_integer() else parsed
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value: Any) -> int | None:
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None
