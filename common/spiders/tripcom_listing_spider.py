from __future__ import annotations

"""Trip.com hotels from server-provided template component bootstrap props."""

import hashlib
import html
import json
import re
from typing import Iterable

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.tripcom_categories import TRIPCOM_CATEGORIES


class TripcomListingSpider(BaseListingSpider):
    name = "tripcom_listing"
    allowed_domains = ["trip.com", "us.trip.com"]
    categories = TRIPCOM_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": ["category", "item_id", "hotel_id", "title", "price", "currency",
                               "price_unit", "city", "city_id", "position", "source_url", "source",
                               "raw", "timestamp"],
    }
    headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "accept-language": "en-US,en;q=0.9",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36"}

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield scrapy.Request(self.resolve_target_url(), callback=self.parse, headers=self.headers,
                             meta={"proxy": self.settings.get("PROXY")})

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Trip.com returned HTTP {response.status}: {response.url}")
        lowered = response.text[:10000].lower()
        if len(response.body) < 5000 or "failed to get successful response" in lowered or "captcha" in lowered:
            raise RuntimeError(f"Trip.com challenge/proxy response at {response.url}")
        payloads = response.xpath('//div[@data-type="template-comp" and @data-name="City"]/@data-jsondata').getall()
        if len(payloads) != 1:
            raise RuntimeError(f"Trip.com expected one City bootstrap component at {response.url}; found {len(payloads)}")
        try:
            state = json.loads(html.unescape(payloads[0]))
        except (TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Trip.com City bootstrap is invalid at {response.url}") from exc
        hotels = state.get("hotels")
        if not isinstance(hotels, list) or not hotels:
            raise RuntimeError(f"Trip.com City bootstrap contains no hotels at {response.url}")
        category, city_id = self.category or "custom", state.get("cityId")
        for position, hotel in enumerate(hotels, start=1):
            if not isinstance(hotel, dict) or not hotel.get("hotelName"):
                continue
            title = hotel["hotelName"].strip()
            item_id = hashlib.sha1(f"{city_id}:{title}".encode()).hexdigest()[:20]
            price, currency = self._price(hotel.get("price"))
            yield {"category": category, "item_id": item_id, "hotel_id": None, "title": title,
                   "price": price, "currency": currency, "price_unit": hotel.get("priceUnit") or None,
                   "city": state.get("cityName"), "city_id": city_id, "position": position,
                   "source_url": response.url, "source": "tripcom_city_component_bootstrap",
                   "raw": hotel, "timestamp": self.job_timestamp}

    @staticmethod
    def _price(value):
        match = re.search(r"([\$€£¥])\s*([\d,.]+)", str(value or "").strip())
        if not match:
            return None, None
        currencies = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "CNY"}
        number = float(match.group(2).replace(",", ""))
        return (int(number) if number.is_integer() else number), currencies[match.group(1)]
