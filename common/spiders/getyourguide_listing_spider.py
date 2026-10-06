from __future__ import annotations

"""GetYourGuide destination listings from server-rendered SDUI hydration."""

import json
from collections.abc import Iterator
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.getyourguide_categories import GETYOURGUIDE_CATEGORIES


class GetYourGuideListingSpider(BaseListingSpider):
    """Extract the bounded activity shelf from ``window.__INITIAL_STATE__``."""

    name = "getyourguide_listing"
    allowed_domains = ["getyourguide.com", "www.getyourguide.com"]
    categories = GETYOURGUIDE_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "tour_id", "title", "description", "url",
            "image_url", "image_urls", "activity_type", "starting_price",
            "base_price", "currency", "currency_symbol", "price_category",
            "price_category_label", "rating", "reviews_count", "attributes",
            "availability_message", "next_available_at", "page_url", "page",
            "source", "raw",
        ],
    }

    def start_requests(self):
        yield scrapy.Request(
            self.resolve_target_url(),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category, "page": 1, "proxy": self._proxy},
        )

    @property
    def _proxy(self):
        return self.settings.get("PROXY") if "PROXY" in self.settings else None

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"GetYourGuide returned HTTP {response.status} for {response.url}")

        state = self._extract_initial_state(response.text)
        sdui = state.get("sdui")
        if not isinstance(sdui, (dict, list)):
            raise RuntimeError(f"GetYourGuide initial state has no SDUI contract at {response.url}")

        products = self._extract_products(sdui)
        if not products:
            raise RuntimeError(f"No GetYourGuide SDUI products found at {response.url}")

        for product in products:
            price = product.get("price") or {}
            reviews = product.get("review_statistics") or {}
            availability = product.get("availability") or {}
            images = self._image_urls(product)
            yield {
                "category": response.meta.get("category"),
                "item_id": product["id"],
                "tour_id": product.get("tour_id"),
                "title": product.get("title"),
                "description": product.get("activity_abstract"),
                "url": self._canonical_url(response.url, product.get("url")),
                "image_url": images[0] if images else None,
                "image_urls": images,
                "activity_type": product.get("activity_type") or product.get("category"),
                "starting_price": price.get("starting_price"),
                "base_price": price.get("base_price"),
                "currency": price.get("currency"),
                "currency_symbol": price.get("currency_symbol"),
                "price_category": price.get("price_category"),
                "price_category_label": price.get("price_category_label"),
                "rating": reviews.get("rating"),
                "reviews_count": reviews.get("quantity"),
                "attributes": product.get("attributes") or [],
                "availability_message": availability.get("message"),
                "next_available_at": availability.get("next_available_date_time"),
                "page_url": response.url,
                "page": 1,
                "source": "getyourguide_initial_state_sdui",
                "raw": product,
            }

    @staticmethod
    def _extract_initial_state(html: str) -> dict:
        marker = "window.__INITIAL_STATE__"
        marker_index = html.find(marker)
        if marker_index < 0:
            raise RuntimeError("GetYourGuide window.__INITIAL_STATE__ assignment is absent")
        assignment = html.find("=", marker_index + len(marker))
        start = html.find("{", assignment + 1) if assignment >= 0 else -1
        if start < 0:
            raise RuntimeError("GetYourGuide window.__INITIAL_STATE__ assignment is malformed")
        try:
            state, _ = json.JSONDecoder().raw_decode(html[start:])
        except json.JSONDecodeError as exc:
            raise RuntimeError("GetYourGuide window.__INITIAL_STATE__ is invalid JSON") from exc
        if not isinstance(state, dict):
            raise RuntimeError("GetYourGuide window.__INITIAL_STATE__ is not an object")
        return state

    @classmethod
    def _extract_products(cls, value) -> list[dict]:
        products = []
        seen = set()
        for node in cls._walk(value):
            if not cls._is_product(node):
                continue
            item_id = node["id"]
            if item_id in seen:
                continue
            seen.add(item_id)
            products.append(node)
        return products

    @classmethod
    def _walk(cls, value) -> Iterator[dict]:
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from cls._walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from cls._walk(child)

    @staticmethod
    def _is_product(value: dict) -> bool:
        required = ("id", "title", "activity_abstract", "url", "price", "review_statistics")
        return all(key in value for key in required) and isinstance(value.get("price"), dict)

    @staticmethod
    def _canonical_url(page_url: str, product_url) -> str | None:
        if not product_url:
            return None
        parts = urlsplit(urljoin(page_url, str(product_url)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

    @staticmethod
    def _image_urls(product: dict) -> list[str]:
        urls = []
        for photo in product.get("photos") or []:
            if not isinstance(photo, dict):
                continue
            for image in photo.get("urls") or []:
                url = image.get("url") if isinstance(image, dict) else None
                if url and url not in urls:
                    urls.append(url)
        return urls

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        }
