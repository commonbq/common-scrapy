from __future__ import annotations

"""Hilton hotels from destination-page Next.js bootstrap state only."""

import json
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.hilton_categories import HILTON_CATEGORIES


class HiltonListingSpider(BaseListingSpider):
    name = "hilton_listing"
    allowed_domains = ["hilton.com", "www.hilton.com"]
    categories = HILTON_CATEGORIES
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "url", "brand_code", "address",
            "city", "state", "state_name", "postal_code", "country", "latitude",
            "longitude", "price", "price_fmt", "currency", "rate_plan", "distance",
            "distance_fmt", "amenities", "is_open", "open_date", "phone", "photo",
            "position", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen = set()

    def start_requests(self):
        yield scrapy.Request(
            self.resolve_target_url(), callback=self.parse, headers=self.headers,
            meta={"proxy": self.settings.get("PROXY")}, dont_filter=True,
        )

    @staticmethod
    def _hotels(text, url="response"):
        lowered = text[:200000].lower()
        if any(marker in lowered for marker in ("captcha", "access denied", "proxy error", "scrapeops error")):
            raise RuntimeError(f"Hilton challenge or proxy error at {url}")
        raw = scrapy.Selector(text=text).css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Hilton response has no __NEXT_DATA__ at {url}")
        try:
            hotels = json.loads(raw)["props"]["pageProps"]["pageData"]["hotelSummaryOptions"]["hotels"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Invalid Hilton hydration at {url}: {exc}") from exc
        if not isinstance(hotels, list):
            raise RuntimeError(f"Hilton hydration has no hotel list at {url}")
        return hotels

    @staticmethod
    def _photo(hotel):
        ratios = ((hotel.get("images") or {}).get("master") or {}).get("ratios") or []
        preferred = next(
            (image for image in ratios if (image.get("size") or image.get("ratio")) == "threeByTwo"),
            None,
        )
        image = preferred or next((image for image in ratios if image.get("url")), {})
        return image.get("url")

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Hilton returned HTTP {response.status}: {response.url}")
        for position, hotel in enumerate(self._hotels(response.text, response.url), 1):
            item_id = str(hotel.get("ctyhocn") or "").strip()
            if not item_id or item_id in self.seen:
                continue
            self.seen.add(item_id)
            address = hotel.get("address") or {}
            localization = hotel.get("localization") or {}
            coordinates = localization.get("coordinate") or {}
            lowest = ((hotel.get("leadRate") or {}).get("lowest") or {})
            display = hotel.get("display") or {}
            contact = hotel.get("contactInfo") or {}
            home_url = (hotel.get("facilityOverview") or {}).get("homeUrlTemplate") or ""
            yield {
                "category": self.category, "item_id": item_id, "title": hotel.get("name"),
                "url": urljoin("https://www.hilton.com", home_url), "brand_code": hotel.get("brandCode"),
                "address": address.get("addressFmt"), "city": address.get("city"),
                "state": address.get("state"), "state_name": address.get("stateName"),
                "postal_code": address.get("postalCode"), "country": address.get("country"),
                "latitude": coordinates.get("latitude"), "longitude": coordinates.get("longitude"),
                "price": lowest.get("rateAmount"), "price_fmt": lowest.get("rateAmountFmt"),
                "currency": localization.get("currencyCode"),
                "rate_plan": (lowest.get("ratePlan") or {}).get("ratePlanName"),
                "distance": hotel.get("distance"), "distance_fmt": hotel.get("distanceFmt"),
                "amenities": hotel.get("amenityIds") or [], "is_open": display.get("open"),
                "open_date": display.get("openDate"), "phone": contact.get("phoneNumber"),
                "photo": self._photo(hotel), "position": position,
                "source": "hilton_next_data", "raw": hotel, "timestamp": self.job_timestamp,
            }
