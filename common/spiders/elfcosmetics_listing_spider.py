from __future__ import annotations

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class ElfcosmeticsListingSpider(BaseListingSpider):
    name = "elfcosmetics_listing"
    allowed_domains = ["elfcosmetics.com", "www.elfcosmetics.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "variant_id",
            "title",
            "url",
            "price",
            "compare_at_price",
            "currency",
            "brand",
            "available_for_sale",
            "rating",
            "reviews_count",
            "image_url",
            "images",
            "selected_options",
            "swatches",
            "category",
            "category_url",
            "page",
            "source",
            "source_url",
            "raw",
            "timestamp",
        ],
    }

    categories = [
        {"category": "makeup", "url": "https://www.elfcosmetics.com/collections/all-makeup"},
        {"category": "face", "url": "https://www.elfcosmetics.com/collections/face"},
        {"category": "eyes", "url": "https://www.elfcosmetics.com/collections/eyes"},
        {"category": "lips", "url": "https://www.elfcosmetics.com/collections/lips"},
        {"category": "skin-care", "url": "https://www.elfcosmetics.com/collections/skin-care"},
        {"category": "hair", "url": "https://www.elfcosmetics.com/collections/hair"},
        {"category": "brushes", "url": "https://www.elfcosmetics.com/collections/brushes"},
        {"category": "best-sellers", "url": "https://www.elfcosmetics.com/collections/best-sellers"},
        {"category": "whats-new", "url": "https://www.elfcosmetics.com/collections/whats-new"},
    ]

    def start_requests(self):
        target = self.resolve_target_url()
        yield scrapy.Request(
            self._with_page(target, 1),
            callback=self.parse,
            meta={"page": 1, "origin": target},
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        listing = self._extract_listing(response.text)
        products = listing.get("products") or []

        for product in products:
            if not isinstance(product, dict) or product.get("type") != "product":
                continue
            yield self._product_item(product, response, page)

        if not products:
            self.logger.warning("e.l.f. bootstrap parser returned 0 items (status=%s)", response.status)

        pagination = listing.get("pagination") or {}
        if page < min(self.max_pages, int(pagination.get("totalPages") or page)):
            yield scrapy.Request(
                self._with_page(response.meta.get("origin") or response.url, page + 1),
                callback=self.parse,
                meta={"page": page + 1, "origin": response.meta.get("origin")},
            )

    def _product_item(self, product: dict, response: scrapy.http.Response, page: int) -> dict:
        price = product.get("price") or {}
        compare_at_price = product.get("compareAtPrice") or {}
        images = product.get("images") or []
        options = product.get("selectedOptions") or []
        handle = product.get("handle")
        query = urlencode(
            {
                option["name"]: option["value"]
                for option in options
                if isinstance(option, dict) and option.get("name") and option.get("value")
            }
        )
        url = response.urljoin(f"/products/{handle}")
        if query:
            url = f"{url}?{query}"

        return {
            "item_id": product.get("id"),
            "variant_id": product.get("variationId"),
            "title": product.get("title"),
            "url": url,
            "price": self._number(price.get("amount")),
            "compare_at_price": self._number(compare_at_price.get("amount")),
            "currency": price.get("currencyCode"),
            "brand": "e.l.f. Cosmetics",
            "available_for_sale": product.get("availableForSale"),
            "rating": None,
            "reviews_count": None,
            "image_url": images[0].get("url") if images else None,
            "images": images,
            "selected_options": options,
            "swatches": product.get("swatches") or [],
            "category": self.category,
            "category_url": response.meta.get("origin"),
            "page": page,
            "source": "elfcosmetics_hydrogen_bootstrap",
            "source_url": response.url,
            "raw": product,
        }

    @classmethod
    def _extract_listing(cls, html: str) -> dict:
        match = re.search(
            r'streamController\.enqueue\(("(?:\\.|[^"\\])*")\)',
            html or "",
            re.DOTALL,
        )
        if not match:
            return {}

        try:
            stream_payload = json.loads(match.group(1))
            flattened = json.loads(stream_payload)
        except (TypeError, ValueError, json.JSONDecodeError):
            return {}
        if not isinstance(flattened, list):
            return {}

        root = cls._decode_flattened(flattened)
        loader_data = root.get("loaderData") if isinstance(root, dict) else None
        if not isinstance(loader_data, dict):
            return {}
        for route_data in loader_data.values():
            if isinstance(route_data, dict) and isinstance(route_data.get("products"), list):
                return route_data
        return {}

    @staticmethod
    def _decode_flattened(flattened: list):
        cache: dict[int, object] = {}
        resolving: set[int] = set()

        def resolve(reference):
            if not isinstance(reference, int) or isinstance(reference, bool):
                return decode(reference)
            if reference < 0 or reference >= len(flattened):
                return None
            if reference in cache:
                return cache[reference]
            if reference in resolving:
                return None
            resolving.add(reference)
            value = decode(flattened[reference])
            resolving.remove(reference)
            cache[reference] = value
            return value

        def decode(value):
            if isinstance(value, list):
                return [resolve(entry) for entry in value]
            if isinstance(value, dict):
                decoded = {}
                for key_reference, entry in value.items():
                    if key_reference.startswith("_") and key_reference[1:].isdigit():
                        key = resolve(int(key_reference[1:]))
                    else:
                        key = key_reference
                    if isinstance(key, str):
                        decoded[key] = resolve(entry)
                return decoded
            return value

        return resolve(0)

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        query = parse_qs(parts.query)
        if page > 1:
            query["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(query, doseq=True)))
