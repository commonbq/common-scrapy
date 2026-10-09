from __future__ import annotations

"""Argos listings from the server-rendered Next.js bootstrap state."""

import json
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.argos_categories import ARGOS_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


class ArgosListingSpider(BaseListingSpider):
    name = "argos_listing"
    allowed_domains = ["argos.co.uk", "www.argos.co.uk"]
    categories = ARGOS_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image", "price",
            "was_price", "currency", "rating", "reviews_count", "deliverable",
            "reservable", "free_delivery", "clearance", "has_variations",
            "special_offer", "badges", "in_stock", "page", "position",
            "total_count", "source_url", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url: str, page: int):
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta={"category": self.category or "custom", "page": page, "base_url": base_url},
        )

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Argos listing returned HTTP {response.status}: {response.url}")
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Argos response has no __NEXT_DATA__ hydration: {response.url}")
        try:
            page_props = json.loads(raw)["props"]["pageProps"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Argos __NEXT_DATA__ hydration is malformed: {response.url}") from exc
        products = page_props.get("productData")
        metadata = page_props.get("productMetadata") or {}
        if not isinstance(products, list):
            raise RuntimeError(f"Argos hydration has no pageProps.productData list: {response.url}")

        page = self._integer(metadata.get("currentPage")) or int(response.meta.get("page", 1))
        total = self._integer(metadata.get("numberOfResults"))
        new_ids = 0
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            attributes = product.get("attributes") or {}
            item_id = str(attributes.get("productId") or product.get("id") or "").strip()
            if not item_id or not attributes.get("name") or item_id in self._seen:
                continue
            self._seen.add(item_id)
            new_ids += 1
            yield self._item(product, attributes, response, page, position, total)

        total_pages = self._integer(metadata.get("totalPages"))
        if page < self.max_pages and new_ids and (total_pages is None or page < total_pages):
            yield self._request(response.meta["base_url"], page + 1)

    def _item(self, product, attributes, response, page, position, total):
        item_id = str(attributes.get("productId") or product.get("id"))
        badge = attributes.get("badge") or {}
        badges = [value for values in badge.values() if isinstance(values, list) for value in values]
        image = attributes.get("image") or attributes.get("imageUrl") or attributes.get("primaryImage")
        if isinstance(image, dict):
            image = image.get("url") or image.get("src")
        if not image:
            image = f"https://media.4rgos.it/s/Argos/{item_id}_R_SET"
        deliverable = self._boolean(attributes.get("deliverable"))
        reservable = self._boolean(attributes.get("reservable"))
        return {
            "category": response.meta.get("category"),
            "item_id": item_id,
            "title": attributes.get("name"),
            "brand": attributes.get("brand"),
            "url": urljoin("https://www.argos.co.uk/", attributes.get("url") or f"product/{item_id}"),
            "image": image,
            "price": self._number(attributes.get("price")),
            "was_price": self._positive_number(attributes.get("wasPrice")),
            "currency": "GBP",
            "rating": self._number(attributes.get("avgRating")),
            "reviews_count": self._integer(attributes.get("reviewsCount")),
            "deliverable": deliverable,
            "reservable": reservable,
            "free_delivery": self._boolean(attributes.get("freeDelivery")),
            "clearance": self._boolean(attributes.get("clearance")),
            "has_variations": self._boolean(attributes.get("hasVariations")),
            "special_offer": attributes.get("specialOfferText") or None,
            "badges": badges,
            "in_stock": bool(deliverable or reservable),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": "argos_next_data_bootstrap",
            "raw": product,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        path = parts.path.rstrip("/")
        marker = "/opt/page:"
        if marker in path:
            path = path.split(marker, 1)[0]
        if page > 1:
            path += f"/opt/page:{page}"
        return urlunsplit((parts.scheme, parts.netloc, path + "/", parts.query, ""))

    @staticmethod
    def _number(value):
        if value is None or isinstance(value, bool):
            return None
        try:
            return float(str(value).replace(",", "").replace("£", ""))
        except ValueError:
            return None

    @classmethod
    def _positive_number(cls, value):
        number = cls._number(value)
        return number if number and number > 0 else None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _boolean(value):
        return value if isinstance(value, bool) else None
