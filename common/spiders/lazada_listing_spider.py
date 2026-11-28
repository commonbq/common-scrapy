"""Lazada Thailand product listings from its first-party catalog XHR response."""

from __future__ import annotations

from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.lazada_categories import LAZADA_CATEGORIES


class LazadaListingSpider(BaseListingSpider):
    name = "lazada_listing"
    allowed_domains = ["lazada.co.th"]
    categories = LAZADA_CATEGORIES
    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "url", "price", "original_price", "currency",
            "image_url", "brand", "seller", "category", "category_url", "page",
            "position", "source", "source_url", "timestamp",
        ],
    }

    API_URL = "https://www.lazada.co.th/catalog/"

    async def start(self):
        entry = self.category_entry(self.category) if self.category else None
        if not self.category and not self.url and not self.category_url:
            raise ValueError("Choose a category, URL, or category_url")
        target = self.url or self.category_url or entry["url"]
        query = entry.get("query", self.category) if entry else self.category
        if not query:
            raise ValueError("Lazada catalog API requires a category query")
        yield scrapy.Request(
            self._api_url(query, 1), callback=self.parse,
            headers={
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": target,
                "Accept-Language": "th-TH,th;q=0.9,en;q=0.8",
            },
            meta={"category": self.category, "category_url": target, "query": query, "page": 1},
        )

    @classmethod
    def _api_url(cls, query: str, page: int) -> str:
        return f"{cls.API_URL}?{urlencode({'ajax': 'true', 'q': query, 'page': page})}"

    def parse(self, response):
        payload = response.json()
        mods = payload.get("mods") or {}
        products = mods.get("listItems")
        if not isinstance(products, list) or not products:
            raise RuntimeError(f"Lazada catalog API returned no listItems for {response.url}")
        info = payload.get("mainInfo") or {}
        page = int(info.get("page") or response.meta["page"])
        for position, product in enumerate(products, 1):
            item_id = product.get("itemId") or product.get("nid")
            if not item_id:
                continue
            thumbs = product.get("thumbs") or []
            path = next((thumb.get("itemUrl") for thumb in thumbs if thumb.get("itemUrl")), None)
            yield {
                "item_id": str(item_id),
                "title": product.get("name"),
                "url": response.urljoin(path or f"/products/pdp-i{item_id}.html"),
                "price": product.get("price"),
                "original_price": product.get("originalPrice"),
                "currency": "THB",
                "image_url": product.get("image"),
                "brand": product.get("brandName"),
                "seller": product.get("sellerName"),
                "category": response.meta["category"],
                "category_url": response.meta["category_url"],
                "page": page,
                "position": position,
                "source": "lazada_catalog_xhr_api",
                "source_url": response.url,
            }
        if page < self.max_pages and not info.get("noMorePages"):
            next_page = page + 1
            yield scrapy.Request(
                self._api_url(response.meta["query"], next_page),
                callback=self.parse,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": response.meta["category_url"],
                    "Accept-Language": "th-TH,th;q=0.9,en;q=0.8",
                },
                meta={**response.meta, "page": next_page},
            )
