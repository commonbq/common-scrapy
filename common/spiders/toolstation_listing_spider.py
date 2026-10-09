from __future__ import annotations

"""Toolstation UK listings from the storefront's first-party CRS search API."""

import json
import math
import re
import uuid
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.toolstation_categories import TOOLSTATION_CATEGORIES


class ToolstationListingSpider(BaseListingSpider):
    name = "toolstation_listing"
    allowed_domains = ["toolstation.com", "www.toolstation.com"]
    categories = TOOLSTATION_CATEGORIES
    page_size = 48
    api_url = "https://www.toolstation.com/api/search/crs"

    api_fields = [
        "pid", "slug", "numberofreviews", "title", "brand", "sale_price",
        "promotion", "thumb_image", "url", "priceRange", "description",
        "formattedPrices", "prices", "ts_reviews", "assettr", "name_type",
        "name_qty", "variations", "price", "samedaydelivery",
        "quantitymaximum", "quantityminimum", "quantitylabel", "channel",
        "group_title", "sku_count", "sku_group_price_range",
        "sku_group_price_range_ex_vat", "campaign",
    ]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_name", "category_id", "department",
            "category_url", "item_id", "title", "group_title", "brand", "url",
            "image_url", "additional_images", "price", "original_price",
            "net_price", "unit_price", "currency", "rating", "reviews_count",
            "availability", "in_stock", "product_type", "quantity_label",
            "variations_count", "promotion", "page", "position", "total_count",
            "items_per_page", "total_pages", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("category", "kitchen-cabinets")
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()
        target = self.resolve_target_url()
        self._category_record = next(
            (row for row in self.categories if row["url"] == target), {}
        )
        match = re.search(r"/c(\d+)(?:[/?]|$)", target)
        if not match:
            raise ValueError(f"Toolstation category URL has no c<id>: {target}")
        self.category_id = f"c{match.group(1)}"
        self.category_url = target

    def start_requests(self):
        yield self._api_request(1)

    def _api_request(self, page: int):
        params = {
            "q": self.category_id,
            "fl": ",".join(self.api_fields),
            "rows": self.page_size,
            "start": (page - 1) * self.page_size,
            "url": self.category_url,
            "ref_url": "",
            "search_type": "category",
            "groupby": "variant_group",
            "request_id": str(uuid.uuid4()),
            "domain_key": "toolstation",
            "view_id": "gb",
            "request_type": "search",
            "stats_field": "price,channel",
            "f.category.facet.prefix": "/root,Home/",
        }
        return scrapy.Request(
            f"{self.api_url}?{urlencode(params)}",
            callback=self.parse,
            headers={"accept": "application/json, text/plain, */*", "referer": self.category_url},
            meta={"page": page},
        )

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Toolstation CRS API returned HTTP {response.status}: {response.url}")
        try:
            payload = json.loads(response.text)
        except (TypeError, ValueError) as exc:
            raise RuntimeError("Toolstation CRS API returned malformed JSON") from exc
        result = payload.get("response") if isinstance(payload, dict) else None
        products = result.get("docs") if isinstance(result, dict) else None
        if not isinstance(products, list) or not products:
            raise RuntimeError("Toolstation CRS API response has no product docs")

        page = int(response.meta.get("page", 1))
        total = self._integer(result.get("numFound")) or len(products)
        per_page = self.page_size
        total_pages = max(1, math.ceil(total / per_page))
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("pid") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            prices = self._json_mapping(product.get("prices"))
            channel = self._integer(product.get("channel"))
            yield {
                "category": self.category,
                "category_name": self._category_record.get("name"),
                "category_id": self.category_id,
                "department": self._category_record.get("department"),
                "category_url": self.category_url,
                "item_id": item_id,
                "title": product.get("title"),
                "group_title": product.get("group_title"),
                "brand": product.get("brand"),
                "url": product.get("url") or f"https://www.toolstation.com/{product.get('slug', 'product')}/p{item_id}",
                "image_url": product.get("thumb_image"),
                "additional_images": product.get("additional_images") or [],
                "price": self._number(prices.get("gross") if prices else product.get("sale_price") or product.get("price")),
                "original_price": self._number(prices.get("was")),
                "net_price": self._number(prices.get("net")),
                "unit_price": self._number(prices.get("priceperunit")),
                "currency": "GBP",
                "rating": self._number(product.get("ts_reviews")),
                "reviews_count": self._integer(product.get("numberofreviews")),
                "availability": self._availability(channel),
                "in_stock": channel in {0, 1, 2, 3, 4},
                "product_type": product.get("name_type"),
                "quantity_label": product.get("name_qty") or product.get("quantitylabel"),
                "variations_count": self._integer(
                    product.get("variations")
                    if product.get("variations") is not None
                    else product.get("sku_count")
                ),
                "promotion": product.get("promotion") or product.get("campaign"),
                "page": page,
                "position": (page - 1) * per_page + position,
                "total_count": total,
                "items_per_page": per_page,
                "total_pages": total_pages,
                "source_url": response.url,
                "source": "toolstation_bloomreach_crs_api",
                "raw": product,
                "timestamp": self.get_timestamp(),
            }

        if page < min(total_pages, self.max_pages):
            yield self._api_request(page + 1)

    @staticmethod
    def _json_mapping(value):
        if isinstance(value, dict):
            return value
        try:
            parsed = json.loads(value or "{}")
        except (TypeError, ValueError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    @staticmethod
    def _number(value):
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _availability(channel):
        return {0: "delivery_and_collection", 1: "delivery", 2: "collection", 3: "direct_ship", 4: "next_day_collection"}.get(channel, "unknown")
