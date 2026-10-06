from __future__ import annotations

"""Viator destination activities from the authoritative preload state."""

import json
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.viator_categories import VIATOR_CATEGORIES


class ViatorListingSpider(BaseListingSpider):
    """Extract the bounded ``pageModel.topActivities`` destination shelf."""

    name = "viator_listing"
    allowed_domains = ["viator.com", "www.viator.com"]
    categories = VIATOR_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "description", "url", "image_url",
            "image_srcset", "activity_category", "location", "price",
            "original_price", "discount_amount", "is_discounted", "currency",
            "currency_symbol", "rating", "reviews_count", "languages", "duration",
            "free_cancellation", "private_tour", "badges", "latitude", "longitude",
            "listing_url", "source", "timestamp", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    def start_requests(self):
        self._seen_ids.clear()
        yield scrapy.Request(
            self.resolve_target_url(),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category},
        )

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Viator returned HTTP {response.status}: {response.url}")
        products = self._top_activities(response)
        if not products:
            raise RuntimeError(f"Viator preload has no topActivities records: {response.url}")

        for product in products:
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("code") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            price = product.get("price") or {}
            retail = price.get("retailPrice") or {}
            discounted = price.get("discountedPrice") or {}
            discount = price.get("discountAmount") or {}
            effective = discounted or retail
            rating = product.get("rating") or {}
            behaviours = product.get("behaviours") or {}
            geo = product.get("geolocation") or {}
            images = product.get("images") or product.get("image") or []
            yield {
                "category": response.meta.get("category"),
                "item_id": item_id,
                "title": product.get("title"),
                "description": product.get("description") or product.get("shortDescription"),
                "url": urljoin("https://www.viator.com", product.get("url") or ""),
                "image_url": self._image_url(images),
                "image_srcset": self._image_srcset(images),
                "activity_category": product.get("category"),
                "location": product.get("location"),
                "price": effective.get("amount"),
                "original_price": retail.get("amount"),
                "discount_amount": discount.get("amount"),
                "is_discounted": bool(price.get("isDiscounted")),
                "currency": effective.get("currencyCode") or retail.get("currencyCode"),
                "currency_symbol": effective.get("currencySymbol") or retail.get("currencySymbol"),
                "rating": rating.get("exactScore", rating.get("score")),
                "reviews_count": rating.get("reviewCount"),
                "languages": product.get("languages") or [],
                "duration": self._duration(product.get("displayDuration")),
                "free_cancellation": behaviours.get("hasFreeCancellation"),
                "private_tour": behaviours.get("isPrivateTour", product.get("isPrivateTour")),
                "badges": product.get("badges") or [],
                "latitude": geo.get("latitude"),
                "longitude": geo.get("longitude"),
                "listing_url": response.url,
                "source": "viator_preloaded_top_activities",
                "timestamp": self.get_timestamp(),
                "raw": product,
            }

    @staticmethod
    def _top_activities(response) -> list:
        candidates = response.css('script[type="mime/invalid"]::text').getall()
        marked = [text for text in candidates if "__PRELOADED_DATA__" in text]
        if not marked:
            raise RuntimeError("Viator __PRELOADED_DATA__ mime/invalid script is absent")
        for text in marked:
            try:
                payload = json.loads(text)
            except (TypeError, ValueError) as error:
                raise RuntimeError("Viator __PRELOADED_DATA__ script is malformed JSON") from error
            preload = payload.get("__PRELOADED_DATA__") if isinstance(payload, dict) else None
            activities = ((preload or {}).get("pageModel") or {}).get("topActivities")
            if isinstance(activities, list):
                return activities
        raise RuntimeError("Viator preload is missing pageModel.topActivities")

    @staticmethod
    def _duration(value):
        duration = value.get("duration") if isinstance(value, dict) else None
        if not isinstance(duration, dict):
            return None
        parts = [f"{duration[key]} {label}" for key, label in
                 (("days", "days"), ("hours", "hours"), ("minutes", "minutes"))
                 if duration.get(key)]
        return " ".join(parts) or None

    @classmethod
    def _image_url(cls, value):
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return value.get("url") or value.get("src") or value.get("imageUrl")
        if isinstance(value, list) and value:
            return cls._image_url(value[0])
        return None

    @staticmethod
    def _image_srcset(value):
        image = value[0] if isinstance(value, list) and value else value
        return image.get("srcset") or image.get("srcSet") if isinstance(image, dict) else None

    @staticmethod
    def _headers():
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        }
