from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.tesco_categories import TESCO_CATEGORIES


class TescoListingSpider(BaseListingSpider):
    """Tesco listings from the page's normalized Apollo product cache."""

    name = "tesco_listing"
    allowed_domains = ["tesco.com", "www.tesco.com"]
    categories = TESCO_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "url", "price", "unit_price",
            "currency", "image_url", "brand", "department", "aisle",
            "availability", "in_stock", "page", "position", "total_count",
            "source_url", "source", "raw",
        ],
    }

    async def start(self):
        target = self.url or self.category_url
        category = self.category or "custom"
        if not target and self.category:
            entry = self.category_entry(self.category)
            if not entry:
                raise ValueError(f"Unknown Tesco category: {self.category}")
            target, category = entry["url"], entry["category"]
        if not target:
            entry = next(self.iter_categories())
            target, category = entry["url"], entry["category"]
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers={"Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-GB,en;q=0.9"},
            meta={"category": category, "page": 1, "seen": set()},
        )

    @staticmethod
    def _apollo_cache(response) -> dict[str, Any]:
        for script in response.css('script[type="application/discover+json"]::text').getall():
            try:
                payload = json.loads(script)
            except json.JSONDecodeError:
                continue
            cache = payload.get("mfe-orchestrator", {}).get("props", {}).get("apolloCache")
            if isinstance(cache, dict) and "ROOT_QUERY" in cache:
                return cache
        raise ValueError("Tesco page did not contain the normalized Apollo cache")

    @staticmethod
    def _listing(cache: dict[str, Any], page: int) -> dict[str, Any]:
        for value in cache.get("ROOT_QUERY", {}).values():
            if (isinstance(value, dict) and value.get("__typename") == "ProductListType"
                    and isinstance(value.get("results"), list)
                    and value.get("info", {}).get("page") == page):
                return value
        raise ValueError(f"Tesco Apollo cache has no product listing for page {page}")

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Tesco listing returned HTTP {response.status}: {response.url}")
        page = int(response.meta["page"])
        category = response.meta["category"]
        cache = self._apollo_cache(response)
        listing = self._listing(cache, page)
        info = listing.get("info", {})
        products = []
        for result in listing["results"]:
            ref = result.get("node", {}).get("__ref") if isinstance(result, dict) else None
            product = cache.get(ref) if isinstance(ref, str) else None
            if isinstance(product, dict) and product.get("id"):
                products.append(product)
        if not products:
            raise RuntimeError(f"Tesco Apollo listing at {response.url} had no product records")

        seen = response.meta["seen"]
        for position, product in enumerate(products, 1):
            item_id = str(product.get("id"))
            if item_id in seen:
                continue
            seen.add(item_id)
            price = product.get("price") or {}
            image = product.get("media", {}).get("defaultImage", {}).get("url") or product.get("defaultImageUrl")
            status = product.get("status")
            yield {
                "category": category,
                "item_id": item_id,
                "title": product.get("title"),
                "url": urljoin("https://www.tesco.com", f"/shop/en-GB/products/{item_id}"),
                "price": price.get("actual"),
                "unit_price": price.get("unitPrice"),
                "currency": "GBP",
                "image_url": image,
                "brand": product.get("brandName"),
                "department": product.get("departmentName"),
                "aisle": product.get("aisleName"),
                "availability": status,
                "in_stock": status == "AvailableForSale",
                "page": page,
                "position": position,
                "total_count": info.get("total"),
                "source_url": response.url,
                "source": "apollo-bootstrap",
                "raw": product,
            }

        if page >= self.max_pages or len(seen) >= (info.get("total") or 0):
            return
        next_page = page + 1
        link = response.css(f'a[aria-label="page: {next_page}"]::attr(href)').get()
        if not link:
            return
        # Preserve Tesco's observed page/sort/count query contract from its link.
        yield response.follow(
            link,
            callback=self.parse,
            meta={"category": category, "page": next_page, "seen": seen},
            headers={"Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-GB,en;q=0.9"},
        )
