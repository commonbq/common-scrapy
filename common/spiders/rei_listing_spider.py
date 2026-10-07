from __future__ import annotations

"""REI listings from the server-rendered ``#initial-props`` bootstrap."""

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.rei_categories import REI_CATEGORIES


class ReiListingSpider(BaseListingSpider):
    name = "rei_listing"
    allowed_domains = ["rei.com", "www.rei.com"]
    categories = REI_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image_url",
            "price", "min_price", "max_price", "original_price", "currency",
            "on_sale", "partial_clearance", "clearance", "available", "rating",
            "reviews_count", "page", "position", "total_count", "source_url",
            "source", "raw", "timestamp",
        ],
    }

    _bootstrap = re.compile(
        r'<script[^>]+id=["\']initial-props["\'][^>]*>', re.I
    )
    _challenge_markers = (
        "access denied", "akamai", "captcha", "reference #", "bot manager",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        yield scrapy.Request(
            self.resolve_target_url(),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category or "custom", "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"REI returned HTTP {response.status}: {response.url}")
        lowered = response.text[:200000].lower()
        if any(marker in lowered for marker in self._challenge_markers):
            raise RuntimeError(f"REI challenge page returned at {response.url}")

        state = self._initial_props(response.text, response.url)
        search = self._search_results(state, response.url)
        products = search.get("results")
        if not isinstance(products, list):
            raise RuntimeError(f"REI hydration has no searchResults.results at {response.url}")
        if not products:
            raise RuntimeError(f"REI hydration returned zero products at {response.url}")

        page = int(response.meta.get("page", 1))
        query = search.get("query") if isinstance(search.get("query"), dict) else {}
        total = self._integer(query.get("totalResults"))
        emitted = 0
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("prodId") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(product, response, page, position, total)

        if page >= self.max_pages:
            return
        pagination = search.get("pagination")
        pagination = pagination if isinstance(pagination, dict) else {}
        next_page = pagination.get("nextPage")
        next_page = next_page if isinstance(next_page, dict) else {}
        query_string = next_page.get("queryString")
        if not emitted or not isinstance(query_string, str) or not query_string:
            return
        yield scrapy.Request(
            urljoin(response.url, query_string), callback=self.parse,
            headers=self._headers(),
            meta={**response.meta, "page": page + 1}, dont_filter=True,
        )

    def _item(self, product, response, page, position, total):
        display = product.get("displayPrice")
        display = display if isinstance(display, dict) else {}
        price = self._number(display.get("min"))
        maximum = self._number(display.get("max"))
        regular = self._number(product.get("regularPrice"))
        on_sale = bool(product.get("sale") or product.get("partialClearance") or product.get("clearance"))
        return {
            "category": response.meta.get("category"),
            "item_id": str(product.get("prodId")),
            "title": self._text(product.get("title")),
            "brand": self._text(product.get("brand")),
            "url": urljoin(response.url, str(product.get("link") or "")) or None,
            "image_url": self._text(product.get("thumbnailImageLink")),
            "price": price if price is not None else regular,
            "min_price": price,
            "max_price": maximum,
            "original_price": regular if on_sale else None,
            "currency": "USD",
            "on_sale": on_sale,
            "partial_clearance": bool(product.get("partialClearance")),
            "clearance": bool(product.get("clearance")),
            "available": bool(product.get("available")),
            "rating": self._number(product.get("rating")),
            "reviews_count": self._integer(product.get("reviewCount")),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": "rei_initial_props_bootstrap",
            "raw": product,
            "timestamp": self.job_timestamp,
        }

    def _initial_props(self, document: str, url: str) -> dict:
        match = self._bootstrap.search(document or "")
        if not match:
            raise RuntimeError(f"No REI #initial-props bootstrap found at {url}")
        try:
            payload, _ = json.JSONDecoder().raw_decode(document, match.end())
        except ValueError as exc:
            raise RuntimeError(f"Malformed REI #initial-props bootstrap at {url}") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"REI #initial-props is not an object at {url}")
        return payload

    @staticmethod
    def _search_results(state: dict, url: str) -> dict:
        try:
            search = state["ProductSearch"]["products"]["searchResults"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError(f"REI bootstrap has no ProductSearch results at {url}") from exc
        if not isinstance(search, dict):
            raise RuntimeError(f"REI searchResults is not an object at {url}")
        return search

    @staticmethod
    def _headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _text(value):
        return str(value).strip() if value is not None and str(value).strip() else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and value != "" else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and value != "" else None
        except (TypeError, ValueError):
            return None
