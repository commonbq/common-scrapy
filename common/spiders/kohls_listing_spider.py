from __future__ import annotations

import json
from urllib.parse import quote, urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.kohls_categories import KOHLS_CATEGORIES


class KohlsListingSpider(BaseListingSpider):
    """Extract Kohl's listings from its web catalog JSON endpoint."""

    name = "kohls_listing"
    allowed_domains = ["kohls.com", "www.kohls.com", "127.0.0.1"]

    categories = KOHLS_CATEGORIES

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image_url",
            "price", "regular_price", "sale_price", "currency", "rating",
            "reviews_count", "source", "category_url", "page", "raw",
            "timestamp",
        ]
    }

    page_size = 120

    def start_requests(self):
        url = self.url or self._build_api_url(1)
        yield scrapy.Request(url, callback=self.parse, headers=self._headers(), meta={"category": self.category, "page": 1})

    def parse(self, response: scrapy.http.Response):
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Kohl's catalog API returned non-JSON at {response.url}") from exc

        products = payload.get("payload", {}).get("products")
        if not isinstance(products, list) or not products:
            raise RuntimeError(f"No Kohl's catalog API products found at {response.url}")

        category = response.meta.get("category")
        page = int(response.meta.get("page", 1))
        for product in products:
            prices = product.get("prices") or [{}]
            price_data = prices[0] if isinstance(prices, list) and prices else {}
            regular = self._number((price_data.get("regularPrice") or {}).get("minPrice"))
            sale = self._number((price_data.get("salePrice") or {}).get("minPrice"))
            product_url = product.get("productDetailsUrl") or product.get("url")
            if product_url and product_url.startswith("/"):
                product_url = f"https://www.kohls.com{product_url}"
            yield {
                "category": category,
                "item_id": product.get("productId") or product.get("id"),
                "title": product.get("productTitle") or product.get("title"),
                "brand": product.get("brand") or product.get("brandName"),
                "url": product_url,
                "image_url": product.get("imageUrl") or product.get("imageURL"),
                "price": sale if sale is not None else regular,
                "regular_price": regular,
                "sale_price": sale,
                "currency": price_data.get("currencyCode") or "USD",
                "rating": self._number(product.get("averageRating")),
                "reviews_count": product.get("reviews") or product.get("reviewCount"),
                "source": "kohls_web_catalog_api",
                "category_url": self._category_entry().get("url"),
                "page": page,
                "raw": product,
                "timestamp": self.job_timestamp,
            }

        total = payload.get("payload", {}).get("totalProducts") or payload.get("payload", {}).get("totalResults")
        has_next = total is None or page * self.page_size < int(total)
        if has_next and page < self.max_pages and not self.url:
            next_page = page + 1
            yield scrapy.Request(self._build_api_url(next_page), callback=self.parse, headers=self._headers(), meta={"category": category, "page": next_page})

    def _category_entry(self):
        entry = self.category_entry(self.category)
        if entry is None:
            raise ValueError(f"Unknown Kohl's category {self.category!r}")
        return entry

    def _build_api_url(self, page: int) -> str:
        entry = self._category_entry()
        offset = (page - 1) * self.page_size
        params = {
            "limit": self.page_size, "offset": offset, "storeNum": 977,
            "isDefaultStore": "true", "includeStoreOnlyProducts": "true",
            "isLTL": "true", "channel": "web",
        }
        return f"https://www.kohls.com/web/catalog/{quote(entry['cn'], safe=':') }?{urlencode(params)}"

    def _headers(self):
        return {
            "accept": "application/json", "channel": "web",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
            "referer": self._category_entry()["url"],
        }

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None
