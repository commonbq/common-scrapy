from __future__ import annotations

"""Trulia sale listings from the server-rendered Next.js search state."""

import json
import re
from urllib.parse import quote, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.trulia_categories import TRULIA_CATEGORIES

_NEXT_DATA_RE = re.compile(r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>', re.S)
_PAGE_RE = re.compile(r'href=["\']([^"\']*/(\d+)_p/[^"\']*)["\']')


class TruliaListingSpider(BaseListingSpider):
    name = "trulia_listing"
    allowed_domains = ["trulia.com", "www.trulia.com"]
    categories = [{"category": key, "url": url} for key, url in TRULIA_CATEGORIES.items()]
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1.0,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "url", "price", "currency",
            "beds", "baths", "sqft", "property_type", "latitude", "longitude",
            "image_url", "provider", "listing_status", "total_count", "page",
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
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, url: str, page: int):
        return scrapy.Request(url, callback=self.parse, headers=self.headers, meta={
            "page": page, "category": self.category or "custom", "proxy": self._proxy(),
        }, dont_filter=True)

    def _proxy(self):
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not isinstance(proxy, str) or not proxy or "scrapeops" not in proxy.lower():
            return proxy or None
        parts = urlsplit(proxy)
        if not parts.hostname or parts.password is None:
            return proxy
        username = parts.username or ""
        options = username.split(".")
        if "residential=true" not in options:
            options.append("residential=true")
        if "bypass=5" not in options:
            options.append("bypass=5")
        host = f"{'.'.join(options)}:{quote(parts.password, safe='')}@{parts.hostname}"
        if parts.port:
            host += f":{parts.port}"
        return urlunsplit((parts.scheme, host, parts.path, parts.query, parts.fragment))

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Trulia returned HTTP {response.status}: {response.url}")
        text = response.text
        if "scrapeops" in text[:1000].lower() and "error" in text[:1000].lower():
            raise RuntimeError("ScrapeOps failure response received for Trulia")
        if any(token in text.lower() for token in ("captcha", "access denied", "challenge-platform")):
            raise RuntimeError("Trulia challenge page received")
        match = _NEXT_DATA_RE.search(text)
        if not match:
            raise RuntimeError("Trulia response has no __NEXT_DATA__ hydration")
        try:
            state = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise RuntimeError("Trulia __NEXT_DATA__ is malformed") from exc
        search = state.get("props", {}).get("searchData")
        if not isinstance(search, dict):
            raise RuntimeError("Trulia hydration has no props.searchData")
        homes = search.get("homes")
        if not isinstance(homes, list):
            raise RuntimeError("Trulia hydration searchData.homes is not a list")
        page = int(response.meta.get("page", 1))
        category = response.meta.get("category", "custom")
        for position, home in enumerate(homes, 1):
            if not isinstance(home, dict):
                continue
            typed_id = str(home.get("typedHomeId") or "")
            item_id = typed_id.removesuffix("_ZPID")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            location = home.get("location") or {}
            coordinates = location.get("coordinates") or {}
            price = home.get("price") or {}
            tracking = {
                row.get("key"): row.get("value")
                for row in home.get("tracking", [])
                if isinstance(row, dict) and row.get("key")
            }
            floor = home.get("floorSpace") or {}
            formatted_sqft = floor.get("formattedDimension") or ""
            sqft_match = re.search(r"[\d,]+", formatted_sqft)
            media = home.get("media") or {}
            hero = media.get("heroImage") or {}
            image = hero.get("url") or {}
            provider = home.get("provider") or home.get("brokerage") or {}
            yield {
                "category": category, "item_id": item_id,
                "title": location.get("fullLocation"), "url": urljoin(response.url, home.get("url") or ""),
                "price": price.get("price") or price.get("min"), "currency": price.get("currencyCode"),
                "beds": (home.get("bedrooms") or {}).get("value"),
                "baths": (home.get("bathrooms") or {}).get("value"),
                "sqft": floor.get("value") or (int(sqft_match.group().replace(",", "")) if sqft_match else None),
                "property_type": (home.get("propertyType") or {}).get("value") or tracking.get("propertyType"),
                "latitude": coordinates.get("latitude"), "longitude": coordinates.get("longitude"),
                "image_url": image.get("medium") or image.get("large") or image.get("small"),
                "provider": provider.get("name") if isinstance(provider, dict) else provider,
                "listing_status": home.get("listingStatus") or home.get("status") or tracking.get("listingStatus"),
                "total_count": search.get("totalHomes"), "page": page, "position": position,
                "source": "trulia_next_data", "raw": home,
                "timestamp": self.job_timestamp,
            }
        if not homes or page >= self.max_pages:
            return
        candidates = [(int(number), urljoin(response.url, href)) for href, number in _PAGE_RE.findall(text)]
        next_url = next((url for number, url in candidates if number == page + 1), None)
        if next_url and next_url != response.url:
            yield self._request(next_url, page + 1)
