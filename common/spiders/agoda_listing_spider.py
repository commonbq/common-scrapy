from __future__ import annotations

import json
import re
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.agoda_categories import AGODA_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


GEO_API = "https://www.agoda.com/api/cronos/geo/accommodations/"
GEO_PARAMS_MARKER = re.compile(r"geoPageParams\s*=\s*JSON\.parse\s*\(")


class AgodaListingSpider(BaseListingSpider):
    """Agoda curated destination hotels from the first-party Cronos API."""

    name = "agoda_listing"
    allowed_domains = ["agoda.com", "www.agoda.com"]
    categories = [
        {"category": name, "url": url} for name, url in AGODA_CATEGORIES.items()
    ]
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "translated_name", "url",
            "image_url", "image_caption", "review_score", "review_score_text",
            "reviews_count", "star_rating", "review_snippet", "reviewer_name",
            "reviewer_country", "price", "currency", "page_type_id",
            "object_id", "accommodation_type_id", "source_url", "source", "raw",
            "timestamp",
        ],
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        yield scrapy.Request(
            target, headers=self.headers, callback=self.parse_config,
            meta={"category": self.category or "custom"}, dont_filter=True,
        )

    def parse_config(self, response):
        self._validate_response(response, "destination")
        config = self.extract_geo_params(response.text)
        required = ("pageTypeId", "objectId", "accommodationTypeId")
        if any(config.get(key) is None for key in required):
            raise RuntimeError("Agoda geoPageParams is missing required API identifiers")
        params = {
            "pageTypeId": config["pageTypeId"],
            "objectId": config["objectId"],
            "accommodationType": config["accommodationTypeId"],
            "accommodationFeaturesType": 1,
        }
        meta = {
            "category": response.meta["category"], "source_url": response.url,
            "page_type_id": config["pageTypeId"], "object_id": config["objectId"],
            "accommodation_type_id": config["accommodationTypeId"],
        }
        yield scrapy.Request(
            f"{GEO_API}?{urlencode(params)}", headers={"Accept": "application/json", "Referer": response.url},
            callback=self.parse, meta=meta, dont_filter=True,
        )

    @staticmethod
    def extract_geo_params(text: str) -> dict:
        marker = GEO_PARAMS_MARKER.search(text or "")
        if not marker:
            raise RuntimeError("Agoda destination response has no geoPageParams hydration")
        decoder = json.JSONDecoder()
        try:
            encoded, end = decoder.raw_decode(text, marker.end())
        except (TypeError, ValueError) as exc:
            raise RuntimeError("Agoda geoPageParams JavaScript string is malformed") from exc
        if not isinstance(encoded, str) or not text[end:].lstrip().startswith(")"):
            raise RuntimeError("Agoda geoPageParams JSON.parse argument is malformed")
        try:
            config = json.loads(encoded)
        except (TypeError, ValueError) as exc:
            raise RuntimeError("Agoda geoPageParams JSON is malformed") from exc
        if not isinstance(config, dict):
            raise RuntimeError("Agoda geoPageParams is not an object")
        return config

    def parse(self, response):
        self._validate_response(response, "Cronos API")
        try:
            payload = json.loads(response.text)
        except (TypeError, ValueError) as exc:
            raise RuntimeError("Agoda Cronos API returned malformed JSON") from exc
        cards = payload.get("hotelcards") if isinstance(payload, dict) else None
        if not isinstance(cards, list):
            raise RuntimeError("Agoda Cronos API response has no hotelcards array")
        if not cards:
            raise RuntimeError("Agoda Cronos API returned an empty hotelcards array")
        for card in cards:
            if not isinstance(card, dict):
                continue
            item_id = str(card.get("hotelId") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(card, response, item_id)

    @staticmethod
    def _validate_response(response, leg: str):
        if response.status != 200:
            raise RuntimeError(f"Agoda {leg} returned HTTP {response.status}: {response.url}")
        body = response.text or ""
        lowered = body[:5000].lower()
        if not body.strip() or any(token in lowered for token in (
            "pardon the interruption", "captcha", "failed to get successful response", "access denied",
        )):
            raise RuntimeError(f"Agoda {leg} returned a challenge or proxy-error response")

    @staticmethod
    def _number(value):
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    def _item(self, card: dict, response, item_id: str):
        price = card.get("price") or card.get("displayPrice") or card.get("roomPrice")
        currency = card.get("currency") or card.get("currencyCode")
        return {
            "category": response.meta["category"], "item_id": item_id,
            "title": card.get("name"), "translated_name": card.get("translatedName"),
            "url": urljoin("https://www.agoda.com/", card.get("hotelUrl") or ""),
            "image_url": urljoin("https:", card.get("imgUrl") or ""),
            "image_caption": card.get("imgCaption"), "review_score": self._number(card.get("reviewScore")),
            "review_score_text": card.get("reviewScoreText"), "reviews_count": card.get("numberOfReviews"),
            "star_rating": self._number(card.get("starRating")),
            "review_snippet": card.get("moreReviewSnippet") or card.get("reviewSnippet"),
            "reviewer_name": card.get("customerName"), "reviewer_country": card.get("customerCountry"),
            "price": self._number(price), "currency": currency,
            "page_type_id": response.meta["page_type_id"], "object_id": response.meta["object_id"],
            "accommodation_type_id": response.meta["accommodation_type_id"],
            "source_url": response.meta["source_url"], "source": "agoda_cronos_geo_api", "raw": card,
            "timestamp": self.get_timestamp(),
        }

