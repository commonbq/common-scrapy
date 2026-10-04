from __future__ import annotations

"""PetSmart listing spider (issue #162).

PetSmart's PLPs are Next.js App Router pages (RSC flight stream, no
``__NEXT_DATA__``), and the storefront itself never talks to Algolia's public
hosts: ``NEXT_PUBLIC_ALGOLIA_HOST_URL`` is built into the storefront bundle as
``www.petsmart.com/api/search``, i.e. Algolia is proxied through PetSmart's own
first-party endpoint with an empty application id / api key.

This spider therefore uses exactly one data direction -- that first-party search
API, called the same way the storefront calls it:

    POST https://www.petsmart.com/api/search/1/indexes/r-US_products_best-sellers/query
    {"params": "query=&hitsPerPage=100&page=0&filters=isSKUAvailable: true AND ... &
                custom_category_names:\"Dog > Food\"&attributesToRetrieve=id,objectID,..."}

Advantages over the SSR-hydration route (no HTML parsing, no JSON-LD zip):

* no browser execution and no 1.8 MB HTML per page;
* the identical taxonomy the storefront filters on, so listing order matches
  what a shopper sees;
* one request per 100 SKUs (``attributesToRetrieve`` keeps the response at
  ~450 KB instead of ~1.9 MB);
* three storefront sort replicas are addressable: ``r-US_products_best-sellers``
  (default), ``r-US_products_top-rated``, ``r-US_products_new-arrivals``;
* product URLs, which the Algolia hits do not carry, are rebuilt from the
  canonical PDP route (``/<category-slug>/<name-slug>-<masterProductID>.html``).

There is no HTML fallback: if the API stops answering with hits the spider fails
loudly instead of degrading into a challenge page.

Flow:
    category (or every bundled category)
        -> POST /api/search/1/indexes/<index>/query (page=N, hitsPerPage=N)
        -> emit one item per hit
        -> repeat until max_pages, nbPages, or the 1000-hit replica cap

Usage:
    common-scrapy crawl petsmart_listing -a category=dog/food/dry-food -a max_pages=2
    common-scrapy crawl petsmart_listing -a category=dog/food -a sort=top-rated
    common-scrapy crawl petsmart_listing -a category_url=https://www.petsmart.com/cat/toys/
"""

import json
import time
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote, urlsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.petsmart_categories import (
    PETSMART_CATEGORIES,
    PETSMART_DEPARTMENTS,
    _segment_slug,
    category_slug,
)

SITE_BASE = "https://www.petsmart.com"
SEARCH_API = f"{SITE_BASE}/api/search/1/indexes"

# Storefront sort replicas. `best-sellers` is the default PLP ordering.
SORT_INDEXES = {
    "best-sellers": "r-US_products_best-sellers",
    "new-arrivals": "r-US_products_new-arrivals",
    "top-rated": "r-US_products_top-rated",
}
DEFAULT_SORT = "best-sellers"
DEFAULT_HITS_PER_PAGE = 100

# Every attribute the exported item reads. Asking the index for exactly these
# keeps a 100-hit page at ~450 KB (the untrimmed payload is ~1.9 MB because each
# hit carries a full HTML `long_description`).
RETRIEVED_ATTRIBUTES = (
    "id",
    "objectID",
    "sku",
    "masterProductID",
    "name",
    "brand",
    "price",
    "priceData",
    "images",
    "alternateImages",
    "upc",
    "upcList",
    "bvAverageRating",
    "bvReviewCount",
    "isSKUAvailable",
    "isInStockInStore",
    "isSubscriptionEnabled",
    "customScheduledDeliveryEligible",
    "short_description",
    "manufacturerName",
    "manufacturerSku",
    "primary_category_id",
    "primary_category_name",
    "custom_category_names",
    "assigned_category_paths",
    "variationData",
    "variations",
    "flavorList",
    "kibbleSizes",
    "foodForms",
    "eligiblePromotions",
    "package",
    "dimensionsAndWeight",
    "size",
    "customCaseQuantity",
    "totalCupsPerPackage",
    "series",
    "productAvailabilityLocations",
    "shoppingOptions-isBopisEligible",
    "shoppingOptions-isInStorePickUp",
    "onlineFrom",
    "onlineTo",
    "conversionRate",
    "lastModifiedMillis",
)

# An HTML body where the JSON search envelope was expected means a bot wall, a
# geo-block or an edge error page -- never a product payload.
CHALLENGE_MARKERS = (
    "access denied",
    "are you a human",
    "captcha",
    "pardon the interruption",
    "request unsuccessful",
    "site unavailable",
)


class PetsmartListingSpider(BaseListingSpider):
    name = "petsmart_listing"
    allowed_domains = ["petsmart.com", "www.petsmart.com", "localhost", "127.0.0.1"]
    require_category_arg = False

    categories = PETSMART_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category",
            "department",
            "subcategory",
            "category_name",
            "category_url",
            "category_item_count",
            "sort",
            "index",
            "item_id",
            "master_product_id",
            "title",
            "brand",
            "url",
            "image_url",
            "alternate_image_count",
            "price",
            "list_price",
            "strikethrough_price",
            "price_display",
            "price_display_type",
            "discount_percent",
            "currency",
            "rating",
            "reviews_count",
            "upc",
            "manufacturer",
            "manufacturer_sku",
            "primary_category",
            "primary_category_id",
            "available",
            "in_stock_in_store",
            "bopis_eligible",
            "in_store_pickup_eligible",
            "autoship_eligible",
            "scheduled_delivery_eligible",
            "flavors",
            "sizes",
            "variation_types",
            "food_forms",
            "kibble_sizes",
            "series",
            "package_weight",
            "case_quantity",
            "promotions",
            "online_from",
            "online_to",
            "page",
            "position",
            "total_count",
            "total_pages",
            "source_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort = str(kwargs.get("sort") or DEFAULT_SORT).strip().lower()
        if self.sort not in SORT_INDEXES:
            raise ValueError(
                f"Unknown sort '{self.sort}'. Available sorts: {', '.join(sorted(SORT_INDEXES))}"
            )
        self.index = SORT_INDEXES[self.sort]
        self.hits_per_page = self._clamp(int(kwargs.get("hits_per_page") or DEFAULT_HITS_PER_PAGE), 1, 1000)
        # `-a available_only=0` drops the storefront's availability window so
        # out-of-stock / not-yet-online SKUs are crawled too.
        available_only = kwargs.get("available_only", True)
        self.available_only = available_only in (True, 1, "1", "true", "True")
        self._seen_items: set[str] = set()
        # Resolve (and validate) targets eagerly so a bad -a argument fails at
        # construction instead of after the crawler is already scheduled.
        self._targets: list[dict[str, Any]] = self._target_categories()
        # Injectable clock so the availability window is deterministic in tests.
        self._now_ms: int | None = kwargs.get("now_ms")

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_items.clear()
        for entry in self._targets:
            yield self._search_request(entry, page=0)

    def _target_categories(self) -> list[dict[str, Any]]:
        target = self.resolve_target_url() if (self.url or self.category_url or self.category) else None
        if target is None:
            return list(self.categories)
        for entry in self.categories:
            if entry["url"] == target or entry["category"] == self.category:
                return [entry]
        # A PLP URL that is in the inventory only through an override, or a
        # hand-typed path: match on the slug of the incoming URL.
        slug = self._url_slug(target)
        for entry in self.categories:
            if entry["category"] == slug:
                return [entry]
        raise ValueError(
            f"Unknown category '{self.category or target}'. petsmart_listing filters the "
            "first-party search API, so the target must be one of the bundled inventory "
            f"entries ({len(self.categories)} paths / 7 departments). Example: "
            "-a category=dog/food/dry-food or -a category_url=https://www.petsmart.com/cat/toys/"
        )

    def _search_request(self, entry: dict[str, Any], *, page: int):
        return scrapy.Request(
            f"{SEARCH_API}/{self.index}/query",
            method="POST",
            body=json.dumps({"params": self._params(entry, page=page)}),
            headers=self._api_headers(),
            callback=self.parse_search,
            dont_filter=True,
            meta={"entry": entry, "page": page},
        )

    def _params(self, entry: dict[str, Any], *, page: int) -> str:
        """Build the ``params`` payload exactly the way the storefront does."""
        params = [
            ("query", ""),
            ("hitsPerPage", str(self.hits_per_page)),
            ("page", str(page)),
        ]
        filters = self._filters(entry)
        if filters:
            params.append(("filters", filters))
        params.append(("attributesToRetrieve", ",".join(RETRIEVED_ATTRIBUTES)))
        return "&".join(f"{key}={quote(str(value), safe='')}" for key, value in params)

    def _filters(self, entry: dict[str, Any]) -> str:
        """Mirror the storefront PLP filter: availability window + category path."""
        clauses = []
        if self.available_only:
            now_ms = self._now_ms or int(time.time() * 1000)
            clauses.append("isSKUAvailable: true")
            clauses.append(f"onlineFrom < {now_ms}")
            clauses.append(f"onlineTo > {now_ms}")
        clauses.append(f'custom_category_names:"{entry["name"]}"')
        return " AND ".join(clauses)

    def _api_headers(self) -> dict[str, str]:
        # The storefront sends empty Algolia credentials: the proxy host resolves
        # the application, and only the caller tag is meaningful.
        return {
            "content-type": "application/json",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
            "x-algolia-application-id": "",
            "x-algolia-api-key": "",
            "x-petm-algolia-caller": "web_desktop",
        }

    # ------------------------------------------------------------------ parse

    def parse_search(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        entry = response.meta["entry"]
        payload = self._json_payload(response)

        hits = payload.get("hits")
        if not isinstance(hits, list):
            raise RuntimeError(
                f"petsmart search API returned no hits list for '{entry['name']}' "
                f"(index={self.index}, page={page}): {response.url}"
            )
        total_count = self._integer(payload.get("nbHits"))
        total_pages = self._integer(payload.get("nbPages"))
        positions = 0
        for hit in hits:
            if not isinstance(hit, dict):
                continue
            positions += 1
            item_id = str(hit.get("objectID") or hit.get("sku") or hit.get("id") or "") or None
            if not item_id or item_id in self._seen_items:
                continue
            self._seen_items.add(item_id)
            yield self._item(
                hit,
                entry=entry,
                page=page,
                position=positions,
                total_count=total_count,
                total_pages=total_pages,
            )

        if not hits:
            return
        if total_pages is not None and page + 1 >= total_pages:
            self.logger.info(
                "petsmart %r exhausted: %s hits over %s pages in %s",
                entry["name"], total_count, total_pages, self.index,
            )
            return
        if page + 1 >= self.max_pages:
            return
        yield self._search_request(entry, page=page + 1)

    def _item(
        self,
        hit: dict[str, Any],
        *,
        entry: dict[str, Any],
        page: int,
        position: int,
        total_count: int | None,
        total_pages: int | None,
    ) -> dict[str, Any]:
        price = hit.get("price") if isinstance(hit.get("price"), dict) else {}
        price_data = hit.get("priceData") if isinstance(hit.get("priceData"), dict) else {}
        formatted = price.get("formatted") if isinstance(price.get("formatted"), dict) else {}
        sale_range = price_data.get("saleRange") if isinstance(price_data.get("saleRange"), list) else []
        list_range = price_data.get("listRange") if isinstance(price_data.get("listRange"), list) else []

        current = self._number(price_data.get("current"))
        if current is None and price.get("displayType") == "range" and sale_range:
            # Range pricing: the card advertises "from $x" while `number` is the
            # most expensive variant of the family.
            current = self._number(sale_range[0])
        if current is None:
            current = self._number(price.get("number"))
        list_price = self._number(price_data.get("list_price")) or self._number(price_data.get("list"))
        discount_percent = None
        if current is not None and list_price and list_price > current:
            discount_percent = round((list_price - current) / list_price * 100, 2)

        images = hit.get("images") if isinstance(hit.get("images"), dict) else {}
        alternate_images = hit.get("alternateImages") if isinstance(hit.get("alternateImages"), list) else []
        upc_list = hit.get("upcList") if isinstance(hit.get("upcList"), list) else []
        variation_data = hit.get("variationData") if isinstance(hit.get("variationData"), list) else []
        variations = hit.get("variations") if isinstance(hit.get("variations"), list) else []
        flavor_list = hit.get("flavorList") if isinstance(hit.get("flavorList"), list) else []
        promotions = hit.get("eligiblePromotions") if isinstance(hit.get("eligiblePromotions"), list) else []
        package = hit.get("package") if isinstance(hit.get("package"), dict) else {}
        size = hit.get("size") if isinstance(hit.get("size"), dict) else {}

        return {
            "category": entry.get("category"),
            "department": entry.get("department"),
            "subcategory": entry.get("subcategory"),
            "category_name": entry.get("name"),
            "category_url": entry.get("url"),
            "category_item_count": entry.get("item_count"),
            "sort": self.sort,
            "index": self.index,
            "item_id": str(hit.get("objectID") or hit.get("sku") or hit.get("id") or "") or None,
            "master_product_id": self._integer(hit.get("masterProductID")),
            "title": hit.get("name"),
            "brand": hit.get("brand"),
            "url": self._product_url(hit),
            "image_url": images.get("large") or images.get("small"),
            "alternate_image_count": len(alternate_images) or None,
            "price": current,
            "list_price": list_price,
            "strikethrough_price": self._number(price.get("strikethrough-number")),
            "price_display": formatted.get("primary"),
            "price_display_type": price.get("displayType"),
            "discount_percent": discount_percent,
            "currency": "USD",
            "rating": self._number(hit.get("bvAverageRating")),
            "reviews_count": self._integer(hit.get("bvReviewCount")),
            "upc": hit.get("upc") or (upc_list[0] if upc_list else None),
            "manufacturer": hit.get("manufacturerName"),
            "manufacturer_sku": hit.get("manufacturerSku"),
            "primary_category": hit.get("primary_category_name"),
            "primary_category_id": hit.get("primary_category_id"),
            "available": bool(hit.get("isSKUAvailable")),
            "in_stock_in_store": bool(hit.get("isInStockInStore")),
            "bopis_eligible": hit.get("shoppingOptions-isBopisEligible"),
            "in_store_pickup_eligible": hit.get("shoppingOptions-isInStorePickUp"),
            "autoship_eligible": bool(hit.get("isSubscriptionEnabled")),
            "scheduled_delivery_eligible": bool(hit.get("customScheduledDeliveryEligible")),
            "flavors": ", ".join(str(value) for value in flavor_list if value) or None,
            "sizes": self._join(
                entry_value.get("value")
                for entry_value in variation_data
                if isinstance(entry_value, dict) and str(entry_value.get("type", "")).lower() == "size"
            ),
            "variation_types": ", ".join(str(value) for value in variations if value) or None,
            "food_forms": self._join(hit.get("foodForms")),
            "kibble_sizes": self._join(hit.get("kibbleSizes")),
            "series": ", ".join(str(value) for value in (hit.get("series") or []) if value) or None,
            "package_weight": size.get("solidSize") or self._package_weight(package),
            "case_quantity": self._integer(hit.get("customCaseQuantity")),
            "promotions": self._promotions(promotions),
            "online_from": self._iso_date(hit.get("onlineFrom")),
            "online_to": self._iso_date(hit.get("onlineTo")),
            "page": page + 1,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": f"{SEARCH_API}/{self.index}/query",
            "source": "petsmart_first_party_search_api",
            "raw": hit,
        }

    # ---------------------------------------------------------------- helpers

    def _product_url(self, hit: dict[str, Any]) -> str | None:
        """Rebuild the canonical PDP route.

        Hits carry no URL, but the storefront PDP path is fully determined by
        the product's category path, its name slug and the master product id
        (the JSON-LD `offers.url` on the PLP uses exactly this shape).
        """
        master_id = self._integer(hit.get("masterProductID"))
        name = hit.get("name")
        if not master_id or not isinstance(name, str) or not name.strip():
            return None
        path = self._category_path(hit)
        slug = self._slug(name)
        return f"{SITE_BASE}/{path}/{slug}-{master_id}.html" if path else f"{SITE_BASE}/{slug}-{master_id}.html"

    def _category_path(self, hit: dict[str, Any]) -> str | None:
        """Pick the browse-department path of a hit and return its URL slug."""
        candidates: list[str] = []
        assigned = hit.get("assigned_category_paths")
        if isinstance(assigned, list):
            candidates.extend(path for path in assigned if isinstance(path, str))
        names = hit.get("custom_category_names")
        if isinstance(names, list):
            candidates.extend(name for name in names if isinstance(name, str))
        for path in candidates:
            parts = path.split(" > ")
            if parts[0] in PETSMART_DEPARTMENTS:
                return category_slug(path)
        return None

    @staticmethod
    def _slug(value: str, limit: int = 120) -> str:
        # Same rule as the category route slugs, truncated like the storefront
        # PDP slugs so the rebuilt URL is canonical more often than not.
        return _segment_slug(value)[:limit].strip("-")

    @staticmethod
    def _url_slug(url: str) -> str:
        return urlsplit(url).path.strip("/").lower()

    def _json_payload(self, response: scrapy.http.Response) -> dict[str, Any]:
        if response.status != 200:
            raise RuntimeError(f"petsmart search API returned HTTP {response.status}: {response.url}")
        body = response.text.strip()
        if not body.startswith("{"):
            lowered = body[:2000].lower()
            for marker in CHALLENGE_MARKERS:
                if marker in lowered:
                    raise RuntimeError(f"petsmart search API served a challenge page: {response.url}")
            raise RuntimeError(f"petsmart search API returned a non-JSON body: {response.url}")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"petsmart search API returned invalid JSON: {response.url}") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"petsmart search API returned a non-object JSON body: {response.url}")
        message = payload.get("message")
        if message and not payload.get("hits"):
            raise RuntimeError(f"petsmart search API error ({response.url}): {message}")
        return payload

    @staticmethod
    def _promotions(promotions: list[Any], limit: int = 3) -> str | None:
        texts: list[str] = []
        for promotion in promotions:
            if not isinstance(promotion, dict):
                continue
            text = str(promotion.get("promoText") or "").strip()
            if text and text not in texts:
                texts.append(text)
            if len(texts) >= limit:
                break
        return "; ".join(texts) or None

    @staticmethod
    def _package_weight(package: dict[str, Any]) -> str | None:
        weight = package.get("weight")
        return f"{weight} lb" if isinstance(weight, (int, float)) and weight else None

    @staticmethod
    def _join(values: Any) -> str | None:
        if not isinstance(values, (list, tuple)):
            return None
        seen: list[str] = []
        for value in values:
            if isinstance(value, dict):
                continue
            text = str(value).strip() if value is not None else ""
            if text and text not in seen:
                seen.append(text)
        return ", ".join(seen) or None

    @staticmethod
    def _iso_date(value: Any) -> str | None:
        millis = PetsmartListingSpider._integer(value)
        if not millis:
            return None
        return datetime.fromtimestamp(millis / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

    @staticmethod
    def _integer(value: Any) -> int | None:
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, (int, float)):
            return int(value)
        try:
            return int(str(value).strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _number(value: Any) -> float | None:
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(str(value).strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clamp(value: int, low: int, high: int) -> int:
        return max(low, min(high, value))
