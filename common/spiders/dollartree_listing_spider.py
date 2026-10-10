from __future__ import annotations

from typing import Any
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.dollartree_categories import DOLLARTREE_CATEGORIES


class DollartreeListingSpider(BaseListingSpider):
    """Dollar Tree products from the first-party OCC guided-search API only."""

    name = "dollartree_listing"
    allowed_domains = ["dollartree.com", "www.dollartree.com"]
    categories = DOLLARTREE_CATEGORIES
    require_category_arg = False
    page_size = 24

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "RETRY_HTTP_CODES": [403, 408, 429, 500, 502, 503, 504],
        "RETRY_TIMES": 3,
        "FEED_EXPORT_FIELDS": [
            "category", "dimension_id", "item_id", "sku", "title", "brand",
            "url", "image_url", "description", "product_category", "price",
            "min_price", "max_price", "case_price", "currency", "availability",
            "in_stock", "minimum_quantity", "case_pack_size", "average_rating",
            "reviews_count", "page", "position", "total_count", "timestamp",
            "source", "raw",
        ],
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "X-CCProfileType": "storefrontUI",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        yield self._api_request(self._selected_category(), page=1, offset=0)

    def _selected_category(self) -> dict[str, str]:
        if self.category:
            selected = self.category_entry(self.category)
            if selected is None:
                available = ", ".join(self.available_categories())
                raise ValueError(
                    f"Unknown category '{self.category}'. Available categories: {available}"
                )
            return selected
        if self.category_url or self.url:
            target = self.category_url or self.url
            selected = next(
                (entry for entry in self.iter_categories() if entry["url"] == target), None
            )
            if selected is None:
                raise ValueError(
                    "Custom URLs are unsupported because the OCC dimension_id is required"
                )
            return selected
        return next(iter(self.iter_categories()))

    def _api_request(self, selected: dict[str, str], page: int, offset: int):
        query = urlencode(
            {"N": selected["dimension_id"], "Nrpp": self.page_size, "No": offset}
        )
        return scrapy.Request(
            f"https://www.dollartree.com/ccstoreui/v1/search?{query}",
            callback=self.parse_api,
            headers=self.headers,
            meta={
                "category": selected["category"],
                "dimension_id": selected["dimension_id"],
                "page": page,
            },
            dont_filter=True,
        )

    def parse_api(self, response):
        if response.status != 200:
            raise RuntimeError(
                f"Dollar Tree API returned HTTP {response.status}: {response.url}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Dollar Tree API returned invalid JSON: {response.url}"
            ) from exc
        results = payload.get("resultsList")
        if not isinstance(results, dict):
            raise RuntimeError(
                f"Dollar Tree API response has no resultsList: {response.url}"
            )
        records = results.get("records")
        if not isinstance(records, list):
            raise RuntimeError(
                f"Dollar Tree API response has no records list: {response.url}"
            )

        page = int(response.meta["page"])
        for position, record in enumerate(records, 1):
            attrs = self._attributes(record)
            item_id = self._first(attrs, "product.id", "product.repositoryId")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(attrs, response, position, results)

        total = self._integer(results.get("totalNumRecs")) or 0
        per_page = self._integer(results.get("recsPerPage")) or self.page_size
        offset = page * per_page
        if records and page < self.max_pages and offset < total:
            selected = {
                "category": response.meta["category"],
                "dimension_id": response.meta["dimension_id"],
            }
            yield self._api_request(selected, page + 1, offset)

    @staticmethod
    def _attributes(record: Any) -> dict[str, Any]:
        if not isinstance(record, dict):
            return {}
        grouped = record.get("attributes")
        merged = dict(grouped) if isinstance(grouped, dict) else {}
        variants = record.get("records")
        if not isinstance(variants, list) or not variants:
            return merged
        attrs = variants[0].get("attributes") if isinstance(variants[0], dict) else None
        if isinstance(attrs, dict):
            merged.update(attrs)
        return merged

    @staticmethod
    def _first(attrs: dict[str, Any], *keys: str):
        for key in keys:
            value = attrs.get(key)
            if isinstance(value, list) and value:
                return value[0]
            if value not in (None, ""):
                return value
        return None

    def _item(self, attrs, response, position, results):
        route = self._first(attrs, "product.route")
        image = self._first(
            attrs, "product.primaryFullImageURL", "product.primaryLargeImageURL"
        )
        availability = self._first(attrs, "sku.availabilityStatus")
        return {
            "category": response.meta["category"],
            "dimension_id": response.meta["dimension_id"],
            "item_id": str(self._first(attrs, "product.id", "product.repositoryId")),
            "sku": self._first(attrs, "sku.repositoryId"),
            "title": self._first(
                attrs, "product.displayName", "product.primaryImageAltText"
            ),
            "brand": self._first(attrs, "product.brand"),
            "url": urljoin("https://www.dollartree.com", route) if route else None,
            "image_url": urljoin("https://www.dollartree.com", image) if image else None,
            "description": self._first(
                attrs, "product.longDescription", "product.description"
            ),
            "product_category": self._first(
                attrs, "product.category", "parentCategory.displayName"
            ),
            "price": self._number(
                self._first(attrs, "sku.activePrice", "product.x_unitPriceNumeric")
            ),
            "min_price": self._number(self._first(attrs, "sku.minActivePrice")),
            "max_price": self._number(self._first(attrs, "sku.maxActivePrice")),
            "case_price": self._number(self._first(attrs, "product.casePrice")),
            "currency": "USD",
            "availability": availability,
            "in_stock": availability == "INSTOCK",
            "minimum_quantity": self._integer(
                self._first(attrs, "product.minimumQuantity")
            ),
            "case_pack_size": self._integer(
                self._first(attrs, "DollarProductType.casePackSize")
            ),
            "average_rating": self._number(
                self._first(attrs, "DollarProductType.averageRating")
            ),
            "reviews_count": self._integer(
                self._first(attrs, "DollarProductType.numberOfReviews")
            ),
            "page": int(response.meta["page"]),
            "position": position,
            "total_count": self._integer(results.get("totalNumRecs")),
            "timestamp": self.get_timestamp(),
            "source": "dollartree_occ_guided_search_api",
            "raw": attrs,
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
            return int(float(value)) if value is not None else None
        except (TypeError, ValueError):
            return None
