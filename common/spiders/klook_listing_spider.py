from __future__ import annotations

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.klook_categories import KLOOK_CATEGORIES


class KlookListingSpider(BaseListingSpider):
    """Klook activities from the destination page's declared first-party XHR."""

    name = "klook_listing"
    allowed_domains = ["www.klook.com"]
    categories = KLOOK_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "vertical_type", "title", "activity_category",
            "city", "url", "image_url", "price", "price_text", "currency",
            "market_price", "market_price_text", "rating", "reviews_text",
            "booked_text", "sold_out", "availability", "position", "total_count",
            "has_more", "more_url", "listing_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    def start_requests(self):
        self._seen_ids.clear()
        yield scrapy.Request(
            self.resolve_target_url(), callback=self.parse_destination,
            headers={"Accept-Language": "en-US,en;q=0.9"},
            meta={"category": self.category or "custom"},
        )

    def parse_destination(self, response):
        if response.status != 200 or self._challenge(response.text):
            raise RuntimeError(f"Klook destination returned a blocked HTTP {response.status}: {response.url}")
        state = self._state(response.text)
        sections = (((state.get("data") or [{}])[0].get("pageData") or {})
                    .get("page", {}).get("body", {}).get("sections", []))
        candidates = []
        for section in sections:
            if not isinstance(section, dict):
                continue
            candidates.extend((section, (section.get("body") or {}).get("content")))
        section = next((s for s in candidates if isinstance(s, dict) and s.get("data_type") == "ttd_acts"), None)
        if not section or not section.get("src"):
            raise RuntimeError(f"Klook hydration has no ttd_acts XHR source: {response.url}")
        yield scrapy.Request(
            urljoin(response.url, section["src"]), callback=self.parse_activities,
            headers={"Accept": "application/json", "Referer": response.url},
            meta={"category": response.meta["category"], "listing_url": response.url},
            dont_filter=True,
        )

    def parse_activities(self, response):
        if response.status != 200:
            raise RuntimeError(f"Klook activity API returned HTTP {response.status}: {response.url}")
        try:
            payload = json.loads(response.text)
        except ValueError as error:
            raise RuntimeError(f"Klook activity API returned non-JSON: {response.url}") from error
        result = payload.get("result") if isinstance(payload, dict) else None
        items = result.get("items") if isinstance(result, dict) else None
        if payload.get("success") is not True or not isinstance(items, list):
            raise RuntimeError(f"Klook activity API contract changed: {response.url}")
        total = result.get("total")
        has_more = bool(result.get("has_more"))
        more_url = result.get("corner_button_deep_link")
        for position, wrapper in enumerate(items, 1):
            data = wrapper.get("data", wrapper) if isinstance(wrapper, dict) else {}
            item_id = str(data.get("vertical_id") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            price_text = (data.get("price") or {}).get("selling_price")
            market_text = (data.get("price") or {}).get("market_price")
            price, currency = self._money(price_text)
            market_price, _ = self._money(market_text)
            review = data.get("review_obj") or {}
            sold_out = bool(data.get("sold_out"))
            yield {
                "category": response.meta.get("category"), "item_id": item_id,
                "vertical_type": data.get("vertical_type"), "title": data.get("title"),
                "activity_category": data.get("category"), "city": data.get("city_name"),
                "url": data.get("deep_link"), "image_url": data.get("cover_url"),
                "price": price, "price_text": price_text, "currency": currency,
                "market_price": market_price, "market_price_text": market_text,
                "rating": self._number(review.get("star")), "reviews_text": review.get("count"),
                "booked_text": review.get("booked"), "sold_out": sold_out,
                "availability": "sold_out" if sold_out else "available", "position": position,
                "total_count": total, "has_more": has_more, "more_url": more_url,
                "listing_url": response.meta.get("listing_url"), "source": "klook_destination_api",
                "raw": data, "timestamp": self.get_timestamp(),
            }

    @staticmethod
    def _state(body: str) -> dict:
        match = re.search(r"window\.__KLOOK__\s*=\s*", body)
        if not match:
            raise RuntimeError("Klook destination hydration is missing")
        try:
            value, _ = json.JSONDecoder().raw_decode(body, match.end())
        except ValueError as error:
            raise RuntimeError("Klook destination hydration is malformed") from error
        if not isinstance(value, dict):
            raise RuntimeError("Klook destination hydration is not an object")
        return value

    @staticmethod
    def _challenge(body: str) -> bool:
        sample = body[:100000].lower()
        return "cf-chl-" in sample or "access denied" in sample or "just a moment" in sample

    @staticmethod
    def _money(text):
        if not text:
            return None, None
        match = re.search(r"([^\d\s.,]+)\s*([\d,.]+)", str(text))
        if not match:
            return None, None
        symbol = match.group(1).strip()
        currency = {"$": "USD", "US$": "USD", "HK$": "HKD", "S$": "SGD", "€": "EUR", "£": "GBP", "¥": "JPY"}.get(symbol, symbol)
        return float(match.group(2).replace(",", "")), currency

    @staticmethod
    def _number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
