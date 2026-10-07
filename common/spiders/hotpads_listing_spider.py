from __future__ import annotations

"""HotPads rentals from the server-rendered Next.js RSC bootstrap only."""

import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.hotpads_categories import HOTPADS_CATEGORIES


class HotPadsListingSpider(BaseListingSpider):
    name = "hotpads_listing"
    allowed_domains = ["hotpads.com", "www.hotpads.com"]
    categories = HOTPADS_CATEGORIES
    require_category_arg = False
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "marker_id", "title", "url", "address", "street",
            "city", "state", "postal_code", "beds", "baths", "sqft",
            "price_low", "price_high", "price_currency", "availability",
            "photo", "units_available", "property_type", "badges", "phone",
            "tags", "latitude", "longitude", "total_count", "total_pages",
            "area_id", "category", "page", "position", "source", "raw",
            "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }
    _flight_re = re.compile(r"self\.__next_f\.push\(\[1,(.*)\]\)", re.DOTALL)
    _marker = '"initialListingsData":'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen: set[str] = set()

    def start_requests(self):
        if self.url or self.category_url or self.category:
            category = self.category or "custom"
            yield self._request(self.resolve_target_url(), category, 1)
            return
        for entry in self.categories:
            yield self._request(entry["url"], entry["category"], 1)

    def _request(self, base_url: str, category: str, page: int):
        settings = getattr(self, "settings", {})
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta={"proxy": settings.get("PROXY"), "base_url": base_url,
                  "category": category, "page": page},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        path = re.sub(r"/page/\d+$", "", parts.path.rstrip("/"))
        if page > 1:
            path += f"/page/{page}"
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

    @classmethod
    def _bootstrap(cls, text: str, url: str = "response") -> dict:
        lowered = text.lower()
        challenges = ("failed to get successful response", "pardon the interruption",
                      "px-captcha", "captcha")
        if len(text.encode()) < 5000 or any(value in lowered for value in challenges):
            raise RuntimeError(f"HotPads challenge/proxy response at {url}")
        selector = scrapy.Selector(text=text)
        decoder = json.JSONDecoder()
        for script in selector.css("script::text").getall():
            match = cls._flight_re.fullmatch(script.strip())
            if not match:
                continue
            try:
                flight = json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
            offset = flight.find(cls._marker)
            if offset < 0:
                continue
            try:
                state, _ = decoder.raw_decode(flight[offset + len(cls._marker):])
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Invalid HotPads RSC bootstrap at {url}: {exc}") from exc
            if isinstance(state, dict):
                return state
        raise RuntimeError(f"HotPads response has no initialListingsData RSC bootstrap at {url}")

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"HotPads returned HTTP {response.status}: {response.url}")
        state = self._bootstrap(response.text, response.url)
        listings = state.get("listings") or {}
        buildings = listings.get("buildings")
        if not isinstance(buildings, list):
            raise RuntimeError(f"HotPads bootstrap has no buildings at {response.url}")
        page = int(response.meta["page"])
        params = state.get("initialParams") or {}
        area = params.get("area") or {}
        total_pages = state.get("totalPages")
        new_count = 0
        for position, building in enumerate(buildings, 1):
            records = building.get("listings") or []
            if not records:
                continue
            record = records[0]
            item_id = str(building.get("lotIdEncoded") or record.get("lotIdEncoded") or "").strip()
            if not item_id or item_id in self.seen:
                continue
            self.seen.add(item_id)
            new_count += 1
            summary = record.get("summary") or {}
            address = record.get("address") or {}
            photos = record.get("photos") or {}
            hero = photos.get("heroId")
            photo = None
            if hero and photos.get("baseUrl"):
                photo = f"{photos['baseUrl']}{hero}{(photos.get('formats') or {}).get('medium', '')}"
            price = summary.get("price") or {}
            beds = summary.get("beds") or {}
            baths = summary.get("baths") or {}
            sqft = summary.get("sqft") or {}
            geo = building.get("geo") or {}
            yield {
                "item_id": item_id, "marker_id": item_id,
                "title": record.get("title") or record.get("name"),
                "url": urljoin("https://hotpads.com", record.get("uriMalone") or building.get("uri") or ""),
                "address": address, "street": address.get("street"),
                "city": address.get("city") or area.get("city"),
                "state": address.get("state") or area.get("state"),
                "postal_code": address.get("zip"), "beds": beds, "baths": baths,
                "sqft": sqft, "price_low": price.get("min"),
                "price_high": price.get("max"), "price_currency": "USD",
                "availability": "active" if "active" in (record.get("tags") or []) else None,
                "photo": photo, "units_available": record.get("unitCount"),
                "property_type": record.get("propertyType"),
                "badges": [badge.get("text") for badge in record.get("displayTags") or [] if badge.get("text")],
                "phone": record.get("contactPhone"), "tags": record.get("tags") or [],
                "latitude": geo.get("lat"), "longitude": geo.get("lon"),
                "total_count": listings.get("numUnits"), "total_pages": total_pages,
                "area_id": area.get("areaId") or params.get("areaId"),
                "category": response.meta["category"], "page": page,
                "position": position, "source": "hotpads_rsc_bootstrap",
                "raw": record, "timestamp": self.job_timestamp,
            }
        if page < self.max_pages and buildings and new_count and (not total_pages or page < int(total_pages)):
            yield self._request(response.meta["base_url"], response.meta["category"], page + 1)
