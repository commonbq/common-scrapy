from __future__ import annotations

"""Dell US listings from the Product Stack bootstrap state."""

import html
import json
import re
from typing import Any, Iterable
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.dell_categories import DELL_CATEGORIES


class DellListingSpider(BaseListingSpider):
    name = "dell_listing"
    allowed_domains = ["dell.com", "www.dell.com"]
    categories = DELL_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "offer_id", "title", "url", "image",
            "price", "regular_price", "savings", "currency", "rating",
            "reviews_count", "badges", "page", "position", "total_count",
            "source", "source_url", "raw", "timestamp",
        ],
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield scrapy.Request(
            self.resolve_target_url(), headers=self.headers, callback=self.parse_bootstrap,
            meta={"category": self.category}, dont_filter=True,
        )

    @staticmethod
    def _script_value(text: str, name: str) -> str | None:
        match = re.search(rf"(?:window\.)?{re.escape(name)}\s*=\s*['\"]([^'\"]+)", text)
        return match.group(1) if match else None

    @staticmethod
    def _request_model(response) -> dict[str, Any]:
        raw = response.css("#hdnRequestPaginationData::attr(value)").get()
        if raw is None:
            raw = response.css("#hdnRequestPaginationData::text").get()
        if not raw:
            raise RuntimeError(f"Dell page has no pagination request model: {response.url}")
        try:
            model = json.loads(html.unescape(raw))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Dell pagination request model is malformed: {response.url}") from exc
        if not isinstance(model, dict):
            raise RuntimeError("Dell pagination request model is not an object")
        return model

    def parse_bootstrap(self, response):
        if response.status != 200:
            raise RuntimeError(f"Dell listing returned HTTP {response.status}: {response.url}")
        raw = response.css("#ps-wrapper::attr(data-product-detail-info)").get()
        if not raw:
            raise RuntimeError(f"Dell page has no Product Stack bootstrap: {response.url}")
        try:
            products = json.loads(html.unescape(raw))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Dell Product Stack bootstrap is malformed: {response.url}") from exc
        if not isinstance(products, dict) or not products:
            raise RuntimeError(f"Dell Product Stack bootstrap is empty: {response.url}")
        total = self._number(self._script_value(response.text, "TotalItem"))
        for position, (key, detail) in enumerate(products.items(), 1):
            if not isinstance(detail, dict):
                continue
            item_id = str(detail.get("productId") or key)
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(detail, item_id, key, response.meta["category"],
                             response.url, 1, position, total)

    @staticmethod
    def _number(value):
        if value in (None, ""):
            return None
        cleaned = re.sub(r"[^0-9.-]", "", str(value))
        if not cleaned:
            return None
        number = float(cleaned)
        return int(number) if number.is_integer() else number

    @staticmethod
    def _detail(tile) -> dict[str, Any]:
        raw = tile.attrib.get("data-product-detail")
        if not raw:
            return {}
        try:
            data = json.loads(html.unescape(raw))
        except json.JSONDecodeError:
            return {}
        if isinstance(data, list) and data:
            entry = data[0]
            return entry.get("Value", entry) if isinstance(entry, dict) else {}
        return data if isinstance(data, dict) else {}

    def _item(self, detail, item_id, offer_id, category, source_url, page, position, total):
        title = detail.get("title")
        return {
            "category": category, "item_id": item_id, "offer_id": offer_id,
            "title": title.strip() if isinstance(title, str) else title,
            "url": urljoin("https://www.dell.com", detail.get("pdUrl") or ""),
            "image": detail.get("image"), "price": self._number(detail.get("dellPrice")),
            "regular_price": self._number(detail.get("marketPrice") or detail.get("regularPrice") or detail.get("listPrice")),
            "savings": self._number(detail.get("savings") or detail.get("saveAmount")),
            "currency": "USD", "rating": self._number(detail.get("rating")),
            "reviews_count": self._number(detail.get("reviewCount") or detail.get("reviewsCount")),
            "badges": detail.get("badges") or {}, "page": page, "position": position,
            "total_count": total, "source": "dell_product_stack_bootstrap",
            "source_url": source_url, "raw": detail, "timestamp": self.get_timestamp(),
        }
