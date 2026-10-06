from __future__ import annotations

"""Rent.com listings from server-rendered Next.js hydration only."""

import json
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.rent_categories import RENT_CATEGORIES


class RentListingSpider(BaseListingSpider):
    name = "rent_listing"
    allowed_domains = ["rent.com", "www.rent.com"]
    categories = RENT_CATEGORIES
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "url", "property_type", "address",
            "city", "state", "state_abbr", "postal_code", "latitude", "longitude",
            "price", "price_min", "price_max", "beds_min", "beds_max", "baths",
            "square_feet_min", "square_feet_max", "availability", "verified",
            "rating_percent", "rating_count", "amenities", "image_ids", "phone",
            "website", "management_company", "listing_tier", "page", "position",
            "total_count", "source", "raw", "timestamp",
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
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url, page):
        settings = getattr(self, "settings", {})
        url = base_url.rstrip("/") if page == 1 else f"{base_url.rstrip('/')}/page-{page}"
        return scrapy.Request(
            url, callback=self.parse, headers=self.headers, dont_filter=True,
            meta={"proxy": settings.get("PROXY"), "page": page, "base_url": base_url},
        )

    @staticmethod
    def _search_state(text, url="response"):
        selector = scrapy.Selector(text=text)
        raw = selector.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Rent.com response has no __NEXT_DATA__ at {url}")
        try:
            return json.loads(raw)["props"]["pageProps"]["pageData"]["location"]["listingSearch"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Invalid Rent.com hydration at {url}: {exc}") from exc

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Rent.com returned HTTP {response.status}: {response.url}")
        search = self._search_state(response.text, response.url)
        listings = search.get("listings")
        if not isinstance(listings, list):
            raise RuntimeError(f"Rent.com hydration has no listings at {response.url}")
        page = int(response.meta["page"])
        total = search.get("total")
        new_count = 0
        for position, listing in enumerate(listings, 1):
            item_id = str(listing.get("id") or "").strip()
            if not item_id or item_id in self.seen:
                continue
            self.seen.add(item_id)
            new_count += 1
            location = listing.get("location") or {}
            price_range = listing.get("priceRange") or {}
            bed_range = listing.get("bedRange") or {}
            plans = listing.get("floorPlans") or []
            baths = sorted({plan.get("bathCount") for plan in plans if plan.get("bathCount") is not None})
            sqft = [plan.get("sqFtRange") or {} for plan in plans]
            management = listing.get("propertyManagementCompany") or {}
            yield {
                "category": self.category, "item_id": item_id, "title": listing.get("name"),
                "url": urljoin("https://www.rent.com", listing.get("urlPathname") or ""),
                "property_type": listing.get("propertyType"), "address": listing.get("addressFull"),
                "city": location.get("city"), "state": location.get("state"),
                "state_abbr": location.get("stateAbbr"), "postal_code": location.get("zip"),
                "latitude": location.get("lat"), "longitude": location.get("lng"),
                "price": listing.get("priceText"), "price_min": price_range.get("min"),
                "price_max": price_range.get("max"), "beds_min": bed_range.get("min"),
                "beds_max": bed_range.get("max"), "baths": baths,
                "square_feet_min": min((r.get("min") for r in sqft if r.get("min") is not None), default=None),
                "square_feet_max": max((r.get("max") for r in sqft if r.get("max") is not None), default=None),
                "availability": listing.get("availabilityStatus"), "verified": listing.get("verified"),
                "rating_percent": listing.get("ratingPercent"), "rating_count": listing.get("ratingCount"),
                "amenities": listing.get("amenitiesHighlighted") or [],
                "image_ids": [photo.get("id") for photo in listing.get("optimizedPhotos") or [] if photo.get("id")],
                "phone": listing.get("phoneDesktopText"), "website": listing.get("website"),
                "management_company": management.get("name"), "listing_tier": listing.get("listingTier"),
                "page": page, "position": position, "total_count": total,
                "source": "rent_next_data", "raw": listing, "timestamp": self.job_timestamp,
            }
        if page < self.max_pages and listings and new_count == len(listings):
            yield self._request(response.meta["base_url"], page + 1)
