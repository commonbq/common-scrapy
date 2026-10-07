from __future__ import annotations

import json
import math
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.movoto_categories import MOVOTO_CATEGORIES


class MovotoListingSpider(BaseListingSpider):
    """Movoto properties from the server-rendered Nuxt hydration state."""

    name = "movoto_listing"
    allowed_domains = ["movoto.com", "www.movoto.com", "localhost", "127.0.0.1"]
    categories = MOVOTO_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "url", "address", "price", "price_raw", "beds",
            "baths", "sqft", "lot_size", "property_type", "year_built", "hoa_fee",
            "status", "mls_number", "mls_db", "listing_agent", "office", "office_phone",
            "open_houses", "latitude", "longitude", "city", "state", "county", "zip",
            "neighborhood", "photo", "photo_count", "days_on_movoto", "list_date",
            "total_count", "category", "page", "position", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name|all>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        if self.category and self.category != "all" and self.category not in self.available_categories():
            raise ValueError(f"Unknown category '{self.category}'. Available categories: {', '.join(self.available_categories())}")
        self._seen_ids: set[str] = set()
        self._first_ids: dict[str, str] = {}

    def start_requests(self):
        self._seen_ids.clear()
        self._first_ids.clear()
        targets = self.categories if self.category == "all" else [{
            "category": self.category or "custom", "url": self.resolve_target_url()
        }]
        for target in targets:
            yield scrapy.Request(target["url"], callback=self.parse, headers=self._headers(), meta={
                "category": target["category"], "page": 1, "base_url": target["url"]
            })

    def parse(self, response):
        self._validate_response(response)
        state = self._extract_state(response)
        page_data = state.get("pageData") if isinstance(state, dict) else None
        listings = page_data.get("listings") if isinstance(page_data, dict) else None
        if not isinstance(listings, list) or not listings:
            raise RuntimeError(f"Movoto bootstrap has no listings at {response.url}")

        page = int(response.meta.get("page", 1))
        category = str(response.meta.get("category", "custom"))
        first_id = str(listings[0].get("propertyId") or listings[0].get("id") or "")
        if page > 1 and self._first_ids.get(category) == first_id:
            self.logger.warning("Stopping on repeated Movoto page at %s", response.url)
            return
        self._first_ids[category] = first_id

        total = self._integer(page_data.get("totalCount"))
        for position, listing in enumerate(listings, start=1):
            if not isinstance(listing, dict):
                continue
            item_id = str(listing.get("propertyId") or listing.get("id") or "")
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            yield self._item(listing, response, page, position, total)

        last_page = math.ceil(total / len(listings)) if total and listings else page
        if page < min(self.max_pages, last_page) and len(listings) >= 50:
            yield response.follow(
                self._page_url(response.meta["base_url"], page + 1), callback=self.parse,
                headers=self._headers(), meta={**response.meta, "page": page + 1},
            )

    def _item(self, listing, response, page, position, total):
        geo = listing.get("geo") if isinstance(listing.get("geo"), dict) else {}
        address = geo.get("formatAddress")
        price = self._number(listing.get("listPrice"))
        return {
            "item_id": str(listing.get("propertyId") or listing.get("id")),
            "title": address,
            "url": urljoin("https://www.movoto.com/", listing.get("path") or ""),
            "address": address,
            "price": price,
            "price_raw": listing.get("listPrice"),
            "beds": self._number(listing.get("bed")),
            "baths": self._number(listing.get("bath")),
            "sqft": self._number(listing.get("sqftTotal")),
            "lot_size": self._number(listing.get("lotSize")),
            "property_type": listing.get("propertyTypeDisplayName") or listing.get("propertyType"),
            "year_built": self._integer(listing.get("yearBuilt")),
            "hoa_fee": self._number(listing.get("hoafee")),
            "status": listing.get("status") or listing.get("houseRealStatus"),
            "mls_number": listing.get("mlsNumber"),
            "mls_db": listing.get("mlsDbNumber"),
            "listing_agent": listing.get("listingAgent"),
            "office": listing.get("officeListName"),
            "office_phone": listing.get("officeListPhone"),
            "open_houses": listing.get("openHouses") if isinstance(listing.get("openHouses"), list) else [],
            "latitude": geo.get("lat"), "longitude": geo.get("lng"),
            "city": geo.get("city"), "state": geo.get("state"), "county": geo.get("county"),
            "zip": geo.get("zipcode") or listing.get("zipCode"),
            "neighborhood": geo.get("neighborhoodName") or geo.get("neighborhoodN"),
            "photo": listing.get("tnImgPath"), "photo_count": self._integer(listing.get("photoCount")),
            "days_on_movoto": self._integer(listing.get("daysOnMovoto")), "list_date": listing.get("listDate"),
            "total_count": total, "category": response.meta.get("category"), "page": page,
            "position": position, "source": "movoto_initial_state", "raw": listing,
            "timestamp": self.job_timestamp.isoformat(),
        }

    @staticmethod
    def _extract_state(response):
        raw = response.css("script#__INITIAL_STATE__::text").get()
        try:
            value = json.loads(raw) if raw else None
        except (TypeError, ValueError):
            return {}
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _page_url(base_url, page):
        parts = urlsplit(base_url)
        path = parts.path.rstrip("/") + f"/p-{page}/"
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

    @staticmethod
    def _validate_response(response):
        body = response.text or ""
        lowered = body.lower()
        markers = ("failed to get successful response", "px-captcha", "captcha challenge")
        if response.status != 200:
            raise RuntimeError(f"Movoto listing returned HTTP {response.status}: {response.url}")
        if len(response.body) < 5000 or any(marker in lowered for marker in markers):
            raise RuntimeError(f"Movoto listing returned a challenge or proxy-error payload at {response.url}")

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

    @staticmethod
    def _headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
