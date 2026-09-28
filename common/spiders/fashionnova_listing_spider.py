from __future__ import annotations

"""Fashion Nova listings from the server-rendered CollectionPage JSON-LD."""

import json
from collections.abc import Iterable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


FASHIONNOVA_CATEGORIES = {
    "new": {"all": "https://www.fashionnova.com/collections/new"},
    "women": {"all": "https://www.fashionnova.com/collections/women"},
    "novadeals": {"all": "https://www.fashionnova.com/collections/womens-novadeals"},
    "halloween": {"all": "https://www.fashionnova.com/collections/halloween"},
    "jeans": {"all": "https://www.fashionnova.com/collections/jeans"},
    "dresses": {
        "all": "https://www.fashionnova.com/collections/dresses",
        "going-out": "https://www.fashionnova.com/collections/club-dresses",
        "birthday": "https://www.fashionnova.com/collections/birthday-dresses",
        "office": "https://www.fashionnova.com/collections/wear-to-work-dresses",
        "cocktail": "https://www.fashionnova.com/collections/cocktail-dresses",
        "fall": "https://www.fashionnova.com/collections/fall-dresses",
        "formal": "https://www.fashionnova.com/collections/formal-shop",
        "luxe": "https://www.fashionnova.com/collections/womens-nova-luxe-dresses",
        "deals": "https://www.fashionnova.com/collections/everyday-dresses",
    },
    "matching-sets": {"all": "https://www.fashionnova.com/collections/matching-sets"},
    "tops": {"all": "https://www.fashionnova.com/collections/all-tops"},
    "graphic-tops": {"all": "https://www.fashionnova.com/collections/graphic-tops"},
    "jackets-and-sweaters": {"all": "https://www.fashionnova.com/collections/jackets"},
    "shoes": {"all": "https://www.fashionnova.com/collections/shoes"},
    "formal": {"all": "https://www.fashionnova.com/collections/formal-shop"},
    "jumpsuits": {"all": "https://www.fashionnova.com/collections/rompers-and-jumpsuits"},
    "bottoms": {"all": "https://www.fashionnova.com/collections/bottoms"},
    "lingerie-and-sleep": {"all": "https://www.fashionnova.com/collections/lingerie"},
    "accessories": {"all": "https://www.fashionnova.com/collections/accessories"},
    "sale": {"all": "https://www.fashionnova.com/collections/sale"},
    "nova-luxe": {"all": "https://www.fashionnova.com/collections/luxe"},
}


class FashionnovaListingSpider(BaseListingSpider):
    name = "fashionnova_listing"
    allowed_domains = ["fashionnova.com", "www.fashionnova.com"]
    categories = FASHIONNOVA_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "brand",
            "description",
            "price",
            "price_max",
            "currency",
            "availability",
            "url",
            "image_url",
            "product_category",
            "category",
            "subcategory",
            "page",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def start_requests(self) -> Iterable[scrapy.Request]:
        if self.url or self.category_url:
            url = self.url or self.category_url
            yield self._request(url, self.category or "custom", "custom", 1)
            return

        if self.category not in self.categories:
            available = ", ".join(self.available_categories())
            raise ValueError(
                f"Unknown category '{self.category}'. Available categories: {available}"
            )
        for subcategory, url in self.categories[self.category].items():
            yield self._request(url, self.category, subcategory, 1)

    def _request(self, url: str, category: str, subcategory: str, page: int):
        return scrapy.Request(
            self._with_page(url, page),
            callback=self.parse,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                ),
            },
            meta={
                "category": category,
                "subcategory": subcategory,
                "page": page,
                "listing_url": url,
                "handle_httpstatus_all": True,
            },
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        collection = self._collection_json_ld(response)
        if response.status != 200 or not collection:
            self.logger.error(
                "Fashion Nova listing has no CollectionPage JSON-LD: status=%s url=%s",
                response.status,
                response.url,
            )
            return

        entries = collection.get("mainEntity", {}).get("itemListElement") or []
        for entry in entries:
            product = entry.get("item") or {}
            item_id = product.get("sku") or product.get("url")
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            offers = product.get("offers") or {}
            images = product.get("image") or []
            brand = product.get("brand") or {}
            yield {
                "item_id": item_id,
                "title": product.get("name"),
                "brand": brand.get("name") if isinstance(brand, dict) else brand,
                "description": (product.get("description") or "").strip() or None,
                "price": self._number(offers.get("lowPrice")),
                "price_max": self._number(offers.get("highPrice")),
                "currency": offers.get("priceCurrency"),
                "availability": (offers.get("availability") or "").rsplit("/", 1)[-1] or None,
                "url": product.get("url"),
                "image_url": images[0] if isinstance(images, list) and images else images or None,
                "product_category": product.get("category"),
                "category": response.meta["category"],
                "subcategory": response.meta["subcategory"],
                "page": page,
                "source": "fashionnova_collection_json_ld",
                "raw": product,
            }

        if entries and page < self.max_pages:
            yield self._request(
                response.meta["listing_url"],
                response.meta["category"],
                response.meta["subcategory"],
                page + 1,
            )

    @staticmethod
    def _collection_json_ld(response: scrapy.http.Response) -> dict | None:
        for raw in response.css('script[type="application/ld+json"]::text').getall():
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            candidates = data if isinstance(data, list) else [data]
            for candidate in candidates:
                if isinstance(candidate, dict) and candidate.get("@type") == "CollectionPage":
                    return candidate
        return None

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
        else:
            query.pop("page", None)
        return urlunparse(parts._replace(query=urlencode(query, doseq=True)))
