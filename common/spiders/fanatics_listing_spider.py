from __future__ import annotations

"""Fanatics product listings parsed from the page's ``__platform_data__`` hydration."""

import json
import re
from typing import Any
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.fanatics_categories import FANATICS_CATEGORIES


class FanaticsListingSpider(BaseListingSpider):
    name = "fanatics_listing"
    allowed_domains = ["fanatics.com"]
    categories = FANATICS_CATEGORIES
    PLATFORM_RE = re.compile(r'__platform_data__\s*=\s*', re.I)
    custom_settings = {"DOWNLOAD_DELAY": 1, "FEED_EXPORT_FIELDS": [
        "category", "item_id", "title", "url", "brand", "image_url", "price",
        "list_price", "currency", "position", "page", "category_url", "source", "raw", "timestamp",
    ]}

    def start_requests(self):
        url = self.resolve_target_url()
        yield scrapy.Request(url, callback=self.parse_listing, meta={"category": self.category or "custom", "category_url": url, "page": 1})

    @staticmethod
    def _platform_data(html: str) -> dict[str, Any]:
        match = FanaticsListingSpider.PLATFORM_RE.search(html)
        if not match:
            raise ValueError("Fanatics response did not contain __platform_data__ hydration")
        start = html.find("{", match.end())
        if start < 0:
            raise ValueError("Fanatics __platform_data__ was not a JSON object")
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(html[start:])
        return data

    @staticmethod
    def _money(value):
        if isinstance(value, dict):
            return value.get("amount") or value.get("value") or value.get("formatted")
        return value

    def parse_listing(self, response):
        data = self._platform_data(response.text)
        browse = data.get("browse-data") or data.get("browseData") or {}
        products = browse.get("products") or []
        if isinstance(products, dict):
            products = products.get("items") or products.get("results") or []
        for position, product in enumerate(products, 1):
            price = product.get("price") or {}
            money = lambda entry: (entry or {}).get("money") or {}
            regular_money = money(price.get("regular"))
            sale_money = money(price.get("discountPrice"))
            image_obj = ((product.get("imageSelector") or {}).get("defaultImage") or {}).get("image") or {}
            image = image_obj.get("src")
            item_id = str(product.get("id") or product.get("productId") or product.get("product_id") or "")
            product_url = product.get("url") or product.get("productUrl")
            yield {
                "category": response.meta["category"], "item_id": item_id or None,
                "title": product.get("title") or product.get("name"),
                "url": urljoin("https://www.fanatics.com", product_url) if product_url else None,
                "brand": (product.get("brandResource") or {}).get("value"),
                "image_url": urljoin("https://fanatics.frgimages.com/", image) if image else None,
                "price": sale_money.get("userCurrencyValue") or regular_money.get("userCurrencyValue"),
                "list_price": regular_money.get("userCurrencyValue"),
                "currency": sale_money.get("userCC") or regular_money.get("userCC"),
                "page": response.meta["page"], "category_url": response.meta["category_url"],
                "source": "fanatics_platform_data", "raw": product, "timestamp": self.get_timestamp(),
                "position": position,
            }
        if response.meta["page"] >= self.max_pages:
            return
        pagination = browse.get("paginationLinks") or []
        next_link = next((entry.get("url") for entry in pagination if entry.get("rel") == "next"), None)
        if next_link:
            next_url = urljoin(response.url, next_link)
            yield response.follow(next_url, callback=self.parse_listing, meta={**response.meta, "page": response.meta["page"] + 1})
