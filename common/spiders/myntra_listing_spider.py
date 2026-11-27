from __future__ import annotations

"""Myntra India listings from the server-rendered ``window.__myx`` state."""

import json
import re
from typing import Any
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.myntra_categories import MYNTRA_CATEGORIES

SITE = "https://www.myntra.com/"
STATE_RE = re.compile(r"window\.__myx\s*=\s*", re.S)


class MyntraListingSpider(BaseListingSpider):
    """Extract Myntra products from the initial server-rendered search state only."""

    name = "myntra_listing"
    allowed_domains = ["myntra.com", "www.myntra.com"]
    categories = MYNTRA_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_name", "item_id", "style_id", "title", "brand",
            "url", "image", "price", "original_price", "currency", "sizes",
            "availability", "inventory", "page", "position", "total_count",
            "has_next_page", "source_url", "source", "raw",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-IN,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            self.category = "topwear"
        self._seen: set[str] = set()

    async def start(self):
        target = self.resolve_target_url()
        entry = next((row for row in self.iter_categories() if row["url"] == target), {})
        yield scrapy.Request(
            target,
            headers=self.headers,
            callback=self.parse,
            errback=self._request_failed,
            meta={"category": self.category or entry.get("category"),
                  "category_name": entry.get("name"), "page": 1},
        )

    def _request_failed(self, failure):
        raise RuntimeError(f"Myntra listing request failed: {failure.getErrorMessage()}")

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Myntra listing returned HTTP {response.status}: {response.url}")
        state = self._extract_state(response.text, response.url)
        try:
            search = state["searchData"]
            results = search["results"]
            products = results["products"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError(f"Myntra __myx state has no searchData.results.products at {response.url}") from exc
        if not isinstance(products, list) or not products:
            raise RuntimeError(f"Myntra __myx state contains no listing products at {response.url}")
        total = self._int(results.get("totalCount") or results.get("totalResults"))
        has_next = bool(results.get("hasNextPage"))
        category_name = (
            results.get("title")
            or response.meta.get("category_name")
            or self._text(response.css("title::text").get())
        )
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            item_id = self._text(product.get("productId") or product.get("styleId"))
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            sizes = product.get("sizes")
            inventory_info = product.get("inventoryInfo")
            available = None
            if isinstance(inventory_info, list):
                available = any(
                    isinstance(row, dict) and row.get("available") is True
                    for row in inventory_info
                )
            path = product.get("landingPageUrl")
            image = product.get("searchImage")
            if isinstance(image, str) and image.startswith("http://"):
                image = "https://" + image[7:]
            yield {
                "category": response.meta.get("category"),
                "category_name": category_name,
                "item_id": item_id,
                "style_id": self._text(product.get("styleId") or product.get("productId")),
                "title": self._text(product.get("productName")),
                "brand": self._text(product.get("brand")),
                "url": urljoin(SITE, path) if path else None,
                "image": image,
                "price": self._money(product.get("price")),
                "original_price": self._money(product.get("mrp")),
                "currency": "INR",
                "sizes": sizes,
                "availability": available,
                "inventory": inventory_info,
                "page": 1,
                "position": position,
                "total_count": total,
                "has_next_page": has_next,
                "source_url": response.url,
                "source": "myntra_myx_bootstrap",
                "raw": product,
            }

    @classmethod
    def _extract_state(cls, text: str, url: str) -> dict[str, Any]:
        match = STATE_RE.search(text or "")
        if not match:
            raise RuntimeError(f"Myntra response has no window.__myx bootstrap at {url}")
        try:
            state, _ = json.JSONDecoder().raw_decode(text, match.end())
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid Myntra __myx bootstrap JSON at {url}: {exc}") from exc
        if not isinstance(state, dict):
            raise RuntimeError(f"Myntra __myx bootstrap is not an object at {url}")
        return state

    @staticmethod
    def _text(value: Any) -> str | None:
        if value is None:
            return None
        text = re.sub(r"\s+", " ", str(value)).strip()
        return text or None

    @classmethod
    def _money(cls, value: Any) -> float | None:
        if isinstance(value, dict):
            value = value.get("value") or value.get("amount")
        if value is None:
            return None
        try:
            return float(re.sub(r"[^\d.]", "", str(value)))
        except ValueError:
            return None

    @staticmethod
    def _int(value: Any) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
