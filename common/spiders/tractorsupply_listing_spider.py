from __future__ import annotations

"""Tractor Supply listings from PDP ``__NEXT_DATA__`` bootstrap state.

The catalog-search endpoint cannot currently be used through the configured
proxy because it strips the required ``channel`` header.  This spider uses one
direction only: official product sitemaps discover PDPs and each PDP's Next.js
bootstrap state supplies the structured product record.  There is no HTML-card
or JSON-LD fallback.
"""

import json
from typing import Any

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.tractorsupply_categories import TRACTORSUPPLY_CATEGORIES


class TractorsupplyListingSpider(BaseListingSpider):
    name = "tractorsupply_listing"
    allowed_domains = ["tractorsupply.com", "www.tractorsupply.com"]
    categories = TRACTORSUPPLY_CATEGORIES
    require_category_arg = False
    PAGE_SIZE = 24

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "category_name", "item_id", "sku",
            "title", "brand", "url", "image_url", "price", "list_price",
            "currency", "availability", "rating", "reviews_count",
            "primary_category", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def start_requests(self):
        targets = self.categories
        if self.category or self.category_url or self.url:
            target = self.resolve_target_url()
            targets = [row for row in self.categories if row["url"] == target]
        for entry in targets:
            yield scrapy.Request(entry["url"], callback=self.parse_sitemap, meta={"entry": entry})

    def parse_sitemap(self, response):
        if response.status != 200:
            raise RuntimeError(f"Tractor Supply sitemap returned HTTP {response.status}: {response.url}")
        urls = response.xpath("//*[local-name()='url']/*[local-name()='loc']/text()").getall()
        requested_limit = int(getattr(self, "max_items", 0) or 0)
        limit = requested_limit or self.PAGE_SIZE * self.max_pages
        for position, url in enumerate(urls[:limit], 1):
            yield scrapy.Request(
                url.strip(), callback=self.parse_product,
                meta={"entry": response.meta["entry"], "position": position},
            )

    def parse_product(self, response):
        if response.status != 200:
            raise RuntimeError(f"Tractor Supply PDP returned HTTP {response.status}: {response.url}")
        encoded = response.css("script#__NEXT_DATA__::text").get()
        if not encoded:
            self.logger.warning("Skipping PDP without __NEXT_DATA__: %s", response.url)
            return
        payload = json.loads(encoded)
        details = self._nested(payload, "props", "pageProps", "pageProps", "pdpData", "productDetails") or {}
        views = self._nested(details, "productDetailsById", "catalogEntryView") or []
        if not views:
            self.logger.warning("Skipping PDP without catalogEntryView: %s", response.url)
            return
        product = views[0]
        attributes = self._attributes(product)
        seo_views = details.get("decodeSEOCatalogEntryView") or []
        seo = seo_views[0] if seo_views else {}
        pricing = product.get("itemPricing") or {}
        breadcrumb = self._nested(details, "breadcrumb", "breadCrumbTrailEntryView") or []
        entry = response.meta["entry"]
        image_key = product.get("xf_thumbnail") or product.get("thumbnail")
        if isinstance(image_key, str) and image_key.startswith("/wcsstore/"):
            image_key = image_key.rsplit("/", 1)[-1]
        item_id = product.get("uniqueID") or seo.get("catentry_id")
        yield {
            "category": entry["category"], "department": entry["department"],
            "category_name": entry["name"], "item_id": str(item_id or ""),
            "sku": product.get("partNumber") or seo.get("partNumber_ntk"),
            "title": product.get("name") or seo.get("name"),
            "brand": product.get("manufacturer") or attributes.get("Brand") or seo.get("mfName"),
            "url": response.url,
            "image_url": f"https://media.tractorsupply.com/is/image/TractorSupplyCompany/{image_key}?$470$" if image_key else None,
            "price": self._number(pricing.get("minOfferPrice") or pricing.get("pickupPrice")),
            "list_price": self._number(pricing.get("listPriceMin") or pricing.get("maxListPrice")),
            "currency": "USD",
            "availability": self._nested(details, "inventoryAvailabilityData", "inventoryStatus") or attributes.get("_AvailabilityStatusOnly"),
            "rating": self._number(attributes.get("_BazaarVoiceReviewRating")),
            "reviews_count": self._int(attributes.get("_BazaarVoiceReviewCount")),
            "primary_category": breadcrumb[-1].get("label") if breadcrumb else None,
            "source_url": response.url, "source": "tractorsupply_next_data",
            "raw": product,
        }

    @staticmethod
    def _nested(value: Any, *keys: str):
        for key in keys:
            if not isinstance(value, dict):
                return None
            value = value.get(key)
        return value

    @staticmethod
    def _attributes(product):
        result = {}
        for attribute in product.get("attributes") or []:
            values = attribute.get("values") or []
            if values:
                result[attribute.get("identifier")] = values[0].get("value") or values[0].get("identifier")
        return result

    @staticmethod
    def _number(value):
        try:
            return float(str(value).replace("$", "").replace(",", ""))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
