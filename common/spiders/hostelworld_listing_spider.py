from __future__ import annotations

import json
from urllib.parse import urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.hostelworld_categories import (
    HOSTELWORLD_CATEGORIES,
    HOSTELWORLD_CATEGORY_LIST,
    HOSTELWORLD_CITY_IDS,
)


class HostelworldListingSpider(BaseListingSpider):
    """Hostelworld properties from the first-party city-properties API."""

    name = "hostelworld_listing"
    allowed_domains = ["prod.apigee.hostelworld.com"]
    categories = HOSTELWORLD_CATEGORY_LIST
    require_category_arg = False
    api_key = "TKM51SUbyeCZl8soGScBLR9lYQdjCvTR8cIN4vfqpG6oExKT"
    api_base = "https://prod.apigee.hostelworld.com/legacy-staticpages-service/city/hostel"

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        # Apigee rejects the repository proxy's rewritten Accept headers.
        "PROXY": None,
        "FEED_EXPORT_FIELDS": [
            "item_id", "url", "name", "address", "city", "country", "continent",
            "rating", "reviews", "min_price", "price_shared", "price_private",
            "currency", "lat", "lng", "photo", "distance_km", "badges",
            "property_type", "has_availability", "category", "page", "position",
            "total_count", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name|all>, category_url=<known city URL>, or url=<known city URL>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        if self.category and self.category != "all" and self.category not in HOSTELWORLD_CITY_IDS:
            raise ValueError(f"Unknown category '{self.category}'. Available categories: {', '.join(self.available_categories())}")
        self._seen_ids: set[str] = set()
        self._first_ids: dict[str, str] = {}

    def start_requests(self):
        self._seen_ids.clear()
        self._first_ids.clear()
        if self.category == "all":
            targets = [(slug, city_id) for slug, city_id in HOSTELWORLD_CITY_IDS.items()]
        else:
            slug = self.category or self._slug_for_url(self.url or self.category_url or "")
            if slug not in HOSTELWORLD_CITY_IDS:
                raise ValueError("Custom URL must match one of the 20 configured Hostelworld city URLs")
            targets = [(slug, HOSTELWORLD_CITY_IDS[slug])]
        for slug, city_id in targets:
            yield self._api_request(slug, city_id, 1)

    def parse(self, response):
        page = int(response.meta["page"])
        category = response.meta["category"]
        data = self._response_data(response)
        if data is None:
            return
        properties = data.get("properties")
        if not isinstance(properties, list) or not properties:
            self.logger.warning("Hostelworld API returned no properties for %s page %s", category, page)
            return

        first_id = str(properties[0].get("id") or "") if isinstance(properties[0], dict) else ""
        if page > 1 and self._first_ids.get(category) == first_id:
            self.logger.warning("Stopping on repeated Hostelworld API page for %s", category)
            return
        self._first_ids[category] = first_id

        for position, prop in enumerate(properties, start=1):
            if not isinstance(prop, dict):
                continue
            item_id = str(prop.get("id") or "")
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            yield self._item(prop, data, response, position)

        number_of_pages = self._integer(data.get("numberOfPages")) or page
        if page < min(self.max_pages, number_of_pages) and len(properties) >= 30:
            yield self._api_request(category, response.meta["city_id"], page + 1)

    def _api_request(self, category, city_id, page):
        url = (
            f"{self.api_base}/{city_id}/properties/?limit=30&page={page}&featured=0"
            "&origin=spapi&priorityPropertyType=hostel&currency=USD"
        )
        return scrapy.Request(
            url, callback=self.parse, headers={
                "api-key": self.api_key, "Accept": "application/json", "Accept-Language": "en",
            }, meta={"category": category, "city_id": city_id, "page": page, "dont_proxy": True},
        )

    def _response_data(self, response):
        lowered = (response.text or "").lower()
        challenge = ("unacceptable value set to the 'accept' header", "px-captcha", "perimeterx", "captcha")
        if response.status != 200 or any(marker in lowered for marker in challenge):
            self.logger.warning("Hostelworld API challenge/error (HTTP %s) at %s", response.status, response.url)
            return None
        try:
            payload = json.loads(response.text)
        except (TypeError, ValueError):
            self.logger.warning("Hostelworld API returned invalid JSON at %s", response.url)
            return None
        if not isinstance(payload, dict) or payload.get("success") is not True or not isinstance(payload.get("data"), dict):
            self.logger.warning("Hostelworld API returned an unsuccessful payload at %s", response.url)
            return None
        return payload["data"]

    def _item(self, prop, data, response, position):
        shared = prop.get("sharedMinPrice") if isinstance(prop.get("sharedMinPrice"), dict) else {}
        private = prop.get("privateMinPrice") if isinstance(prop.get("privateMinPrice"), dict) else {}
        geo = prop.get("geoCoordinates") if isinstance(prop.get("geoCoordinates"), dict) else {}
        image = prop.get("image") if isinstance(prop.get("image"), dict) else {}
        photo = image.get("medium") or image.get("large") or image.get("small")
        if photo and not str(photo).startswith(("http://", "https://")):
            photo = "https://" + str(photo).lstrip("/")
        badges = prop.get("badges") if isinstance(prop.get("badges"), list) else []
        item_id = str(prop["id"])
        slug = prop.get("urlFriendlyName") or item_id
        return {
            "item_id": item_id,
            "url": f"https://www.hostelworld.com/hostels/p/{item_id}/{slug}/",
            "name": prop.get("name"), "address": prop.get("address"),
            "city": prop.get("city") or data.get("name"),
            "country": prop.get("country") or data.get("country"),
            "continent": prop.get("continent") or data.get("continent"),
            "rating": self._number(prop.get("avgRating")), "reviews": self._integer(prop.get("numberReviews")),
            "min_price": self._number(shared.get("value")), "price_shared": self._number(shared.get("value")),
            "price_private": self._number(private.get("value")),
            "currency": shared.get("currency") or private.get("currency"),
            "lat": self._number(geo.get("latitude")), "lng": self._number(geo.get("longitude")),
            "photo": photo, "distance_km": self._number(prop.get("cityCenterDistance")),
            "badges": [badge.get("badgeName") for badge in badges if isinstance(badge, dict) and badge.get("badgeName")],
            "property_type": prop.get("type"), "has_availability": prop.get("hasAvailability"),
            "category": response.meta["category"], "page": response.meta["page"], "position": position,
            "total_count": self._integer(data.get("totalPropertiesCount")),
            "source": "hostelworld_city_properties_api", "raw": prop,
            "timestamp": self.job_timestamp.isoformat(),
        }

    @staticmethod
    def _slug_for_url(url):
        path = urlparse(url).path.rstrip("/")
        slug = path.rsplit("/", 1)[-1]
        return slug if HOSTELWORLD_CATEGORIES.get(slug) else None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _number(value):
        try:
            result = float(value) if value is not None and not isinstance(value, bool) else None
            return int(result) if result is not None and result.is_integer() else result
        except (TypeError, ValueError):
            return None
