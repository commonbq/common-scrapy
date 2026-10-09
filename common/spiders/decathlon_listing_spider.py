from __future__ import annotations

from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.decathlon_categories import DECATHLON_CATEGORIES


class DecathlonListingSpider(BaseListingSpider):
    """Decathlon products from Shopify's first-party collection JSON API."""

    name = "decathlon_listing"
    allowed_domains = ["decathlon.com", "www.decathlon.com"]
    categories = DECATHLON_CATEGORIES
    require_category_arg = False
    page_size = 250

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "RETRY_HTTP_CODES": [403, 408, 429, 500, 502, 503, 504],
        "RETRY_TIMES": 3,
        "FEED_EXPORT_FIELDS": [
            "category",
            "item_id",
            "handle",
            "variant_id",
            "sku",
            "title",
            "vendor",
            "product_type",
            "url",
            "image_url",
            "description",
            "price",
            "compare_at_price",
            "currency",
            "in_stock",
            "available_variant_count",
            "tags",
            "published_at",
            "page",
            "position",
            "source_url",
            "source",
            "timestamp",
            "raw",
        ],
    }
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        has_target = self.category or self.category_url or self.url
        listing_url = (
            self.resolve_target_url() if has_target else next(iter(self.iter_categories()))["url"]
        )
        yield self._api_request(listing_url, page=1)

    def _api_request(self, listing_url: str, *, page: int):
        path = urlparse(listing_url).path.rstrip("/")
        api_url = (
            f"https://www.decathlon.com{path}/products.json"
            f"?limit={self.page_size}&page={page}"
        )
        return scrapy.Request(
            api_url,
            callback=self.parse_api,
            headers=self.headers,
            meta={
                "category": self.category or path.rsplit("/", 1)[-1],
                "listing_url": listing_url,
                "page": page,
            },
            dont_filter=True,
        )

    def parse_api(self, response):
        if response.status != 200:
            raise RuntimeError(
                f"Decathlon Shopify API returned HTTP {response.status}: {response.url}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Decathlon Shopify API returned invalid JSON: {response.url}"
            ) from exc
        products = payload.get("products")
        if not isinstance(products, list):
            raise RuntimeError(
                f"Decathlon Shopify API response has no products list: {response.url}"
            )

        page = int(response.meta["page"])
        category = response.meta["category"]
        for position, product in enumerate(products, 1):
            item_id = str(product.get("id") or "")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(product, response, category, page, position)

        if products and len(products) >= self.page_size and page < self.max_pages:
            yield self._api_request(response.meta["listing_url"], page=page + 1)

    def _item(self, product, response, category, page, position):
        variants = product.get("variants") or []
        available = [variant for variant in variants if variant.get("available")]
        selected = available[0] if available else (variants[0] if variants else {})
        images = product.get("images") or []
        image = product.get("image") or (images[0] if images else {})
        handle = product.get("handle")
        return {
            "category": category,
            "item_id": str(product.get("id")),
            "handle": handle,
            "variant_id": str(selected.get("id")) if selected.get("id") else None,
            "sku": selected.get("sku"),
            "title": product.get("title"),
            "vendor": product.get("vendor"),
            "product_type": product.get("product_type"),
            "url": f"https://www.decathlon.com/products/{handle}" if handle else None,
            "image_url": image.get("src") if isinstance(image, dict) else None,
            "description": product.get("body_html"),
            "price": self._number(selected.get("price")),
            "compare_at_price": self._number(selected.get("compare_at_price")),
            "currency": "USD",
            "in_stock": bool(available),
            "available_variant_count": len(available),
            "tags": product.get("tags") or [],
            "published_at": product.get("published_at"),
            "page": page,
            "position": position,
            "source_url": response.url,
            "source": "decathlon_shopify_collection_api",
            "timestamp": self.get_timestamp().isoformat(),
            "raw": product,
        }

    @staticmethod
    def _number(value):
        if value in (None, ""):
            return None
        try:
            return float(Decimal(str(value)))
        except (InvalidOperation, TypeError, ValueError):
            return None
