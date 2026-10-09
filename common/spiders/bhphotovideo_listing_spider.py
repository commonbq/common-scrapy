from __future__ import annotations

import html
import json
import re
from math import ceil
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.bhphotovideo_categories import BH_PHOTO_CATEGORIES


class BhphotovideoListingSpider(BaseListingSpider):
    """B&H listings sourced only from the server-rendered MobX hydration."""

    name = "bhphotovideo_listing"
    allowed_domains = ["bhphotovideo.com", "www.bhphotovideo.com"]
    categories = BH_PHOTO_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "category_id", "category_path", "category_url",
            "product_id", "sku", "manufacturer_sku", "title", "brand", "url",
            "image_url", "price", "original_price", "currency", "rating",
            "reviews_count", "stock", "in_stock", "page", "position", "total_count",
            "items_per_page", "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        target = self.resolve_target_url()
        selected = next((row for row in self.iter_categories() if row["url"] == target), {})
        yield scrapy.Request(target, callback=self.parse, meta={
            "page": 1,
            "category": self.category or selected.get("category") or "custom",
            "department": selected.get("department"),
            "category_url": target,
        })

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"B&H listing returned HTTP {response.status}: {response.url}")
        data = self._listing_data(response)
        products = self._products(data)
        if not products:
            raise RuntimeError(f"B&H hydration returned no products: {response.url}")

        page = self._integer(data.get("pageNumber")) or int(response.meta["page"])
        total = self._integer(data.get("count"))
        per_page = self._integer(data.get("itemsPerPage")) or len(products)
        main = data.get("mainCategory") if isinstance(data.get("mainCategory"), dict) else {}
        fresh = 0
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            key = self._mapping(product.get("itemKey"))
            core = self._mapping(product.get("core"))
            item_id = str(key.get("skuNo") or core.get("itemCode") or "")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            fresh += 1
            yield self._item(product, main, response, page, position, total, per_page)

        last_page = ceil(total / per_page) if total and per_page else page
        if fresh and page < self.max_pages and page < last_page:
            base = re.sub(r"/pn/\d+/?$", "", response.meta["category_url"].rstrip("/"))
            yield scrapy.Request(
                f"{base}/pn/{page + 1}", callback=self.parse,
                meta={**response.meta, "page": page + 1}, dont_filter=True,
            )

    @staticmethod
    def _listing_data(response):
        raw = response.css("div.bh-preloaded-data::attr(data-data)").get()
        if not raw:
            raise RuntimeError(f"B&H preloaded hydration is missing: {response.url}")
        try:
            state = json.loads(html.unescape(raw))
            data = state["ListingStore"]["state"]["response"]["data"]
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(f"Invalid B&H ListingStore hydration: {response.url}") from exc
        if not isinstance(data, dict):
            raise RuntimeError(f"Invalid B&H listing data: {response.url}")
        return data

    @staticmethod
    def _products(data):
        for key in ("items", "products", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return value
        return []

    def _item(self, product, main, response, page, position, total, per_page):
        key = self._mapping(product.get("itemKey"))
        core = self._mapping(product.get("core"))
        price = self._mapping(product.get("priceInfo"))
        stock_info = self._mapping(product.get("stockInfo"))
        reviews = self._mapping(product.get("reviewsStats"))
        image = self._mapping(self._mapping(product.get("mainImage")).get("listing"))
        category_info = self._mapping(product.get("categoryInfo"))
        path = category_info.get("primaryCategoryPath")
        if not isinstance(path, list):
            path = main.get("categoryPath") if isinstance(main.get("categoryPath"), list) else []
        stock = stock_info.get("statusMessage") or stock_info.get("status")
        return {
            "category": response.meta["category"], "department": response.meta.get("department"),
            "category_id": main.get("id"), "category_path": " > ".join(str(x.get("name")) for x in path if isinstance(x, dict) and x.get("name")),
            "category_url": response.meta["category_url"], "product_id": key.get("skuNo"),
            "sku": core.get("itemCode"), "manufacturer_sku": core.get("manufacturerCatalogNumber"),
            "title": core.get("shortDescription"), "brand": core.get("brandName"),
            "url": urljoin(response.url, core.get("detailsUrl") or ""),
            "image_url": image.get("url"), "price": price.get("price"),
            "original_price": price.get("strikethroughPrice"), "currency": "USD",
            "rating": reviews.get("reviewRating"), "reviews_count": reviews.get("reviewCount"),
            "stock": stock, "in_stock": price.get("addToCartButton") not in {None, "NOT_AVAILABLE", "SOLD_OUT"},
            "page": page, "position": position, "total_count": total, "items_per_page": per_page,
            "source_url": response.url, "source": "bootstrap", "raw": product,
            "timestamp": self.job_timestamp,
        }

    @staticmethod
    def _integer(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _mapping(value):
        return value if isinstance(value, dict) else {}
