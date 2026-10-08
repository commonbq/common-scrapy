from __future__ import annotations

"""Blick Art Materials listing spider (issue #227).

Blick is a Next.js storefront. The category page server-renders the first 30
products into ``__NEXT_DATA__``, but the storefront's own pager never emits
links -- the page-number buttons are JavaScript. Every page after the first is
fetched from a first-party JSON API.

This spider uses exactly ONE product-data direction -- the first-party
product-search API:

    GET https://api.dickblick.com/product-search/api/v1.0/collections/alias/{entryId}
        ?pageNumber=N&pageSize=30&includeFacets=false
    Header: X-blick-portal: blick

The category landing page is requested for exactly one purpose: to read
``props.pageProps.entryId`` from ``__NEXT_DATA__``, the opaque collection id
the API is keyed by. Products are never parsed out of the HTML -- API
``pageNumber=0`` returns the same 30 records the HTML embeds, so page 1 is
fetched from the API too and there is exactly one item source.

There is **no HTML / JSON-LD fallback**. If the API stops answering, the spider
raises rather than silently yielding fewer items.

API paging is **zero-based**: ``pageNumber=0`` is the first page and
``pageNumber=1`` is the second. The stop condition is ``totalPages``, plus a
``pageNumber * pageSize >= totalCount`` backstop and a max_pages cap.

Taxonomy lives in ``blick_categories.py``: 899 crawlable category URLs under 17
departments, captured from the ``/categories/`` hydration.

Flow:
    category (or all categories)
        -> GET /categories/<...>/ (read entryId only)
        -> GET api.dickblick.com/.../alias/{entryId} (pageNumber=0..max_pages-1)
        -> emit one item per product, deduped on itemId
"""

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.blick_categories import BLICK_SITE_BASE, crawlable_categories

API_BASE = "https://api.dickblick.com/product-search/api/v1.0/collections/alias"
PAGE_SIZE = 30

# The API rejects requests without this portal header; it is a static literal in
# the storefront bundle, not a credential.
PORTAL_HEADER = {"X-blick-portal": "blick"}

# Bot-wall / error interstitials. Only the head of the document is scanned: a
# real category page is ~370 KB of markup and product JSON whose feature-flag
# blob contains strings like "ff-checkout-captcha-enabled", so a whole-body
# substring scan produces false positives. Walls and error pages serve a short
# document, so the challenge text always lands in the first few KB.
CHALLENGE_HEAD_BYTES = 8192

# Wording varies by vendor and casing, so match case-insensitively.
CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "are you a human",
    "verify you are human",
    "just a moment",
    "checking your browser",
    "enable javascript and cookies",
    "attention required",
    "too many requests",
    "request unsuccessful",
    "site unavailable",
)

# Only meaningful for the API leg: any markup at all means a wall, since that
# endpoint otherwise answers with JSON. The category page is real HTML, so it
# cannot be checked this way.
JSON_MARKERS = CHALLENGE_MARKERS + ("<html", "<!doctype")


class BlickListingSpider(BaseListingSpider):
    name = "blick_listing"
    allowed_domains = ["dickblick.com", "www.dickblick.com", "api.dickblick.com"]
    require_category_arg = False

    categories = [
        {
            "category": row["category"],
            "name": row["name"],
            "url": row["url"],
            "path": row["path"],
            "depth": row["depth"],
        }
        for row in crawlable_categories()
    ]

    PAGE_SIZE = PAGE_SIZE

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "department",
            "category_name",
            "category_path",
            "category_url",
            "collection_id",
            "item_id",
            "entry_id",
            "sku_id",
            "title",
            "brand",
            "url",
            "image_url",
            "image_alt",
            "short_description",
            "price",
            "price_max",
            "list_price",
            "sale_price",
            "currency",
            "savings_text",
            "is_sale",
            "is_best_price",
            "rating",
            "reviews_count",
            "sku_count",
            "in_stock",
            "is_new",
            "is_overstock",
            "is_clearance",
            "is_coupon_eligible",
            "page",
            "position",
            "total_count",
            "total_pages",
            "source_url",
            "source",
            "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_items: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_items.clear()
        for entry in self._target_categories():
            yield self._entry_id_request(entry)

    def _target_categories(self) -> list[dict[str, Any]]:
        if not (self.url or self.category_url or self.category):
            return list(self.categories)
        target_url = self.url or self.category_url
        for entry in self.categories:
            if self.category and entry["category"] == self.category:
                return [entry]
            # Exact match: substring matching would let a department URL such as
            # /categories/painting/ swallow every one of its children.
            if target_url and entry["url"] == target_url:
                return [entry]
        target = self.category or target_url
        available = ", ".join(self.available_categories()[:20])
        raise ValueError(
            f"Unknown category '{target}'. Use -a category=<department>/<leaf> or "
            f"-a category_url=https://www.dickblick.com/categories/... "
            f"Available categories (first 20): {available}"
        )

    def _entry_id_request(self, entry: dict[str, Any]):
        return scrapy.Request(
            entry["url"],
            callback=self.parse_entry_id,
            headers={"Accept": "text/html,application/xhtml+xml"},
            meta={"entry": entry},
            dont_filter=True,
        )

    def _api_request(self, entry: dict[str, Any], collection_id: str, *, page: int):
        url = f"{API_BASE}/{collection_id}?" + urlencode(
            {
                "pageNumber": page,
                "pageSize": self.PAGE_SIZE,
                # Facets are only needed when a facet UI is being rendered; they
                # roughly double the payload and pagination never needs them.
                "includeFacets": "false",
            }
        )
        return scrapy.Request(
            url,
            callback=self.parse_api_page,
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": BLICK_SITE_BASE,
                "Referer": entry["url"],
                **PORTAL_HEADER,
            },
            meta={"entry": entry, "collection_id": collection_id, "page": page},
            dont_filter=True,
        )

    # ------------------------------------------------------------------ parse

    def parse_entry_id(self, response: scrapy.http.Response):
        entry = response.meta["entry"]
        collection_id = self._extract_entry_id(response)
        yield self._api_request(entry, collection_id, page=0)

    def parse_api_page(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        entry = response.meta["entry"]
        collection_id = response.meta["collection_id"]
        payload = self._json_payload(response)

        items = payload.get("items")
        if not isinstance(items, list):
            raise RuntimeError(
                f"Blick product-search API returned no items list at {response.url}: "
                f"keys={sorted(payload)[:12]}"
            )

        total = self._integer(payload.get("totalCount"))
        total_pages = self._integer(payload.get("totalPages"))

        for position, product in enumerate(items, start=1):
            if not isinstance(product, dict):
                continue
            item = self._item(
                product, response, entry, collection_id, page, position, total, total_pages
            )
            if item is not None:
                yield item

        if page + 1 >= self.max_pages or not items:
            return
        # totalPages is authoritative; the count arithmetic is a backstop for
        # payloads where totalPages is absent.
        if total_pages is not None and page + 1 >= total_pages:
            return
        if total_pages is None and total is not None and (page + 1) * self.PAGE_SIZE >= total:
            return
        yield self._api_request(entry, collection_id, page=page + 1)

    def _extract_entry_id(self, response: scrapy.http.Response) -> str:
        """Read the API collection id out of the Next.js hydration state.

        The page is fetched only for this value -- products come from the API.
        """
        if response.status != 200:
            raise RuntimeError(
                f"Blick category page returned HTTP {response.status}: {response.url}"
            )
        body = response.text or ""
        head = body[:CHALLENGE_HEAD_BYTES].lower()
        if any(marker in head for marker in CHALLENGE_MARKERS):
            raise RuntimeError(
                f"Blick category page returned a bot-challenge/error body at {response.url}; "
                "refusing to resolve a collection id from it."
            )
        match = re.search(
            r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>', body, re.S
        )
        if not match:
            raise RuntimeError(
                f"No __NEXT_DATA__ hydration state found on the Blick category page {response.url}; "
                "the collection id can only be resolved from the Next.js payload."
            )
        try:
            payload = json.loads(match.group(1))
        except ValueError as exc:
            raise RuntimeError(
                f"Blick category page shipped malformed __NEXT_DATA__ at {response.url}"
            ) from exc

        page_props = (payload.get("props") or {}).get("pageProps") or {}
        collection_id = page_props.get("entryId")
        if not collection_id:
            raise RuntimeError(
                f"Blick category page {response.url} has no props.pageProps.entryId "
                f"(contentType={page_props.get('contentType')!r}); "
                f"pageProps keys={sorted(page_props)}"
            )
        return str(collection_id)

    def _json_payload(self, response: scrapy.http.Response) -> dict[str, Any]:
        if response.status != 200:
            raise RuntimeError(
                f"Blick product-search API returned HTTP {response.status}: {response.url}"
            )
        body = response.text or ""
        if any(marker in body.lower() for marker in JSON_MARKERS):
            raise RuntimeError(
                f"Blick product-search API returned a bot-challenge/error body at {response.url}"
            )
        try:
            payload = json.loads(body)
        except ValueError as exc:
            raise RuntimeError(
                f"Blick product-search API returned non-JSON at {response.url}: {body[:200]!r}"
            ) from exc
        if not isinstance(payload, dict):
            raise RuntimeError(
                f"Blick product-search API returned a non-object payload at {response.url}"
            )
        # The API answers 200 with a bare string when the alias is unknown, which
        # happens for department landing pages that have no product collection.
        return payload

    # ------------------------------------------------------------------- item

    def _item(
        self,
        product: dict,
        response,
        entry: dict,
        collection_id: str,
        page: int,
        position: int,
        total: int | None,
        total_pages: int | None,
    ):
        entry_id = self._text(product.get("entryId"))
        item_id = self._text(product.get("itemId")) or entry_id
        if not item_id or item_id in self._seen_items:
            return None
        self._seen_items.add(item_id)

        title = self._text(product.get("name"))
        pricing = product.get("pricing")
        pricing = pricing if isinstance(pricing, dict) else {}
        availability = product.get("availability")
        availability = availability if isinstance(availability, dict) else {}

        price_min = self._number(pricing.get("priceMin"))
        price_max = self._number(pricing.get("priceMax"))
        msrp = self._number(pricing.get("skuMsrp"))
        list_price = msrp or (price_max if price_max != price_min else None)
        is_sale = bool(pricing.get("isSkuOnSale"))

        department, _, category_name = (entry.get("path") or "").partition(" > ")

        return {
            "category": entry["category"],
            "department": department or None,
            "category_name": category_name or entry.get("name"),
            "category_path": entry.get("path"),
            "category_url": entry.get("url"),
            "collection_id": collection_id,
            "item_id": item_id,
            "entry_id": entry_id,
            "sku_id": self._text(product.get("itemId")),
            "title": title,
            "brand": self._text(product.get("brand")),
            "url": self._absolute_url(product.get("url")),
            "image_url": self._absolute_url(product.get("featuredImageUrl")),
            "image_alt": title,
            "short_description": self._text(product.get("shortDescription")),
            "price": price_min,
            "price_max": price_max,
            "list_price": list_price,
            "sale_price": price_min if is_sale else None,
            "currency": "USD",
            "savings_text": self._text(pricing.get("savingStory")),
            "is_sale": is_sale,
            "is_best_price": self._bool(pricing.get("isBestPrice")),
            "rating": self._number(product.get("rating")),
            "reviews_count": self._integer(product.get("ratingCount")),
            "sku_count": self._integer(product.get("skuCount")),
            # The search payload has no explicit stock flag; a product that is
            # listed at all is orderable, so availability is expressed through
            # the clearance/overstock flags the payload does carry.
            "in_stock": None if availability == {} else True,
            "is_new": self._bool(product.get("isNew")),
            "is_overstock": self._bool(product.get("isOverstock")),
            "is_clearance": self._bool(availability.get("isOnClearance")),
            "is_coupon_eligible": self._bool(product.get("isCouponEligible")),
            "page": page,
            "position": position,
            "total_count": total,
            "total_pages": total_pages,
            "source_url": response.url,
            "source": "blick_product_search_api",
            "raw": product,
        }

    @staticmethod
    def _absolute_url(value):
        if not value:
            return None
        value = str(value).strip()
        if not value:
            return None
        if value.startswith("//"):
            return f"https:{value}"
        return urljoin(f"{BLICK_SITE_BASE}/", value)

    # ------------------------------------------------------------------ utils

    @staticmethod
    def _text(value):
        if value is None:
            return None
        if isinstance(value, (list, tuple)):
            value = value[0] if value else None
            if value is None:
                return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in ("true", "yes", "1"):
                return True
            if lowered in ("false", "no", "0"):
                return False
        return None

    @staticmethod
    def _number(value):
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, str):
            value = value.strip().replace("$", "").replace(",", "")
            if not value:
                return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        if isinstance(value, bool) or value is None:
            return None
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None
