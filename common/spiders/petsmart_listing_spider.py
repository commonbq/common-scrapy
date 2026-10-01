from __future__ import annotations

import html
import json
import re
from urllib.parse import urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.petsmart_categories import PETSMART_CATEGORIES

PRODUCT_URL_TEMPLATE = "https://www.petsmart.com/-{master_product_id}.html"


class PetsmartListingSpider(BaseListingSpider):
    """PetSmart listings from the inline Algolia InstantSearch hydration state."""

    name = "petsmart_listing"
    allowed_domains = ["petsmart.com", "www.petsmart.com", "localhost", "127.0.0.1"]
    categories = PETSMART_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "master_product_id", "sku", "upc",
            "title", "brand", "manufacturer", "url", "image_url", "price",
            "list_price", "currency", "availability", "in_stock_in_store",
            "is_subscription_enabled", "rating", "reviews_count", "category_path",
            "primary_category", "pet_type", "page", "position", "total_count",
            "source_url", "source", "raw",
        ],
    }

    # `window[Symbol.for("InstantSearchInitialResults")] = {...}` is emitted
    # un-escaped into a plain inline <script>, unlike the RSC stream, so the
    # payload can be JSON-decoded straight out of the response body.
    _assignment = re.compile(
        r'window\[Symbol\.for\("InstantSearchInitialResults"\)\]\s*=\s*', re.DOTALL
    )
    # Algolia caps pagination at 1000 hits regardless of the reported nbHits.
    MAX_TRAVERSABLE_HITS = 1000
    CHALLENGE_MARKERS = (
        "Access Denied",
        "akamai reference",
        "You don't have permission to access",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            errback=self.handle_error,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
            },
            meta={
                "category": self.category or "custom",
                "department": selected.get("department"),
                "page": 1,
            },
            dont_filter=True,
        )

    def handle_error(self, failure):
        raise RuntimeError(f"PetSmart listing request failed: {failure.value}")

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"PetSmart listing returned HTTP {response.status}: {response.url}")
        if any(marker in response.text[:20000] for marker in self.CHALLENGE_MARKERS):
            raise RuntimeError(f"PetSmart served an anti-bot challenge page at {response.url}")

        result = self._extract_result(response.text)
        if result is None:
            raise RuntimeError(
                f"No Algolia InstantSearch hydration state found at {response.url}"
            )

        hits = result.get("hits")
        if not isinstance(hits, list):
            raise RuntimeError(f"PetSmart hydration state has no hits list at {response.url}")

        page = int(response.meta.get("page", 1))
        total_count = self._integer(result.get("nbHits"))
        total_pages = self._integer(result.get("nbPages")) or 1
        hits_per_page = self._integer(result.get("hitsPerPage")) or len(hits) or 1

        for position, hit in enumerate(hits, start=1):
            if not isinstance(hit, dict):
                continue
            item_id = str(hit.get("objectID") or hit.get("id") or "") or None
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(hit, response, page, position, total_count)

        next_page = page + 1
        if page >= min(total_pages, self.max_pages) or not hits:
            return
        if len(self._seen_products) >= min(
            total_count or self.MAX_TRAVERSABLE_HITS, self.MAX_TRAVERSABLE_HITS
        ):
            return
        if next_page * hits_per_page > self.MAX_TRAVERSABLE_HITS:
            return

        yield scrapy.Request(
            self._page_url(response.url, next_page),
            callback=self.parse,
            errback=self.handle_error,
            headers=dict(response.request.headers),
            meta={**response.meta, "page": next_page},
            dont_filter=True,
        )

    def _item(self, hit: dict, response, page: int, position: int, total_count: int | None) -> dict:
        master_product_id = self._integer(hit.get("masterProductID"))
        images = hit.get("images") if isinstance(hit.get("images"), dict) else {}
        price_data = hit.get("priceData") if isinstance(hit.get("priceData"), dict) else {}
        price = self._price(hit, price_data)
        list_price = self._number(price_data.get("list"))
        category_path = self._string_list(hit.get("assigned_category_paths"))
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "item_id": str(hit.get("objectID") or hit.get("id") or ""),
            "master_product_id": master_product_id,
            "sku": self._string(hit.get("sku") or hit.get("id")),
            "upc": self._string(hit.get("upc")),
            "title": html.unescape(self._string(hit.get("name"))),
            "brand": html.unescape(self._string(hit.get("brand"))),
            "manufacturer": html.unescape(self._string(hit.get("manufacturerName"))),
            "url": PRODUCT_URL_TEMPLATE.format(master_product_id=master_product_id)
            if master_product_id
            else None,
            "image_url": self._string(images.get("large") or images.get("small")),
            "price": price,
            "list_price": list_price,
            "currency": "USD" if price is not None or list_price is not None else None,
            "availability": "in_stock" if hit.get("isSKUAvailable") else "out_of_stock",
            "in_stock_in_store": hit.get("isInStockInStore"),
            "is_subscription_enabled": hit.get("isSubscriptionEnabled"),
            "rating": self._number(hit.get("bvAverageRating")),
            "reviews_count": self._integer(hit.get("bvReviewCount")),
            "category_path": category_path[0] if category_path else None,
            "primary_category": self._string(hit.get("primary_category_name")),
            "pet_type": self._string_list(hit.get("customPet")),
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "petsmart_instantsearch_algolia",
            "raw": hit,
        }

    @classmethod
    def _extract_result(cls, document: str) -> dict | None:
        """Return the single `results` entry from the InstantSearch hydration state."""
        match = cls._assignment.search(document or "")
        if not match:
            return None
        try:
            state, _ = json.JSONDecoder().raw_decode(document, match.end())
        except (TypeError, ValueError):
            return None
        if not isinstance(state, dict):
            return None
        for payload in state.values():
            if not isinstance(payload, dict):
                continue
            results = payload.get("results")
            if isinstance(results, list) and results and isinstance(results[0], dict):
                return results[0]
        return None

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        """Build the server-rendered `?page=N` pagination URL (N is 1-based)."""
        parts = urlparse(url)
        query = dict(part.split("=", 1) for part in parts.query.split("&") if "=" in part)
        query["page"] = str(page)
        return urlunparse(parts._replace(query=urlencode(query)))

    @classmethod
    def _price(cls, hit: dict, price_data: dict) -> float | None:
        """Resolve the buyable price, using the low end for range-priced SKUs."""
        price = hit.get("price") if isinstance(hit.get("price"), dict) else {}
        for candidate in (
            price_data.get("current"),
            (price_data.get("saleRange") or [None])[0],
            (price_data.get("listRange") or [None])[0],
            price.get("number"),
        ):
            number = cls._number(candidate)
            if number is not None:
                return number
        return None

    @staticmethod
    def _string_list(value) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, str) and item]

    @staticmethod
    def _string(value):
        return str(value) if value is not None and value != "" else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None
