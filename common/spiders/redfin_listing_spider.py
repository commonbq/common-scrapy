from __future__ import annotations

"""Redfin listings from the first-party Stingray GIS API."""

import json
import re
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.redfin_categories import REDFIN_CATEGORIES


STATE_MARKER = "root.__reactServerState.InitialContext ="


class RedfinListingSpider(BaseListingSpider):
    name = "redfin_listing"
    allowed_domains = ["redfin.com", "www.redfin.com"]
    categories = REDFIN_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "listing_id", "mls_id", "title", "url",
            "image_url", "price", "currency", "beds", "baths", "sqft",
            "price_per_sqft", "city", "state", "zip", "property_type",
            "status", "latitude", "longitude", "year_built", "photo_count",
            "days_on_market", "time_on_redfin", "is_hot", "is_new_construction",
            "page", "position", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError("Provide category, category_url, or url")
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        self._seen.clear()
        url = self.resolve_target_url()
        meta = {"category": self.category or "custom", "page": 1, "listing_url": url}
        proxy = self.settings.get("PROXY")
        if proxy:
            meta["proxy"] = proxy
        yield scrapy.Request(url, headers=self.headers, meta=meta, callback=self.parse)

    def parse(self, response):
        self._validate_response(response, "category")
        state = self._initial_context(response.text)
        api_url, payload = self._cached_gis(state)
        yield from self._emit(payload, response.meta, response)
        if self.max_pages > 1 and self._homes(payload):
            yield self._api_request(api_url, response.meta, page=2, page_size=len(self._homes(payload)))

    def parse_api(self, response):
        self._validate_response(response, "GIS API")
        payload = self._decode_gis(response.text)
        homes = self._homes(payload)
        if not homes:
            return
        before = len(self._seen)
        yield from self._emit(payload, response.meta, response)
        page = int(response.meta["page"])
        if page < self.max_pages and len(self._seen) > before:
            yield self._api_request(response.meta["api_url"], response.meta, page=page + 1, page_size=len(homes))

    def _api_request(self, api_url, meta, *, page, page_size):
        parts = urlsplit(urljoin("https://www.redfin.com", api_url))
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query.update(page_number=str(page), start=str((page - 1) * page_size))
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))
        request_meta = {"category": meta["category"], "listing_url": meta["listing_url"], "page": page, "api_url": api_url}
        if meta.get("proxy"):
            request_meta["proxy"] = meta["proxy"]
        return scrapy.Request(url, callback=self.parse_api, headers={**self.headers, "accept": "application/json", "referer": meta["listing_url"]}, meta=request_meta, dont_filter=True)

    @classmethod
    def _initial_context(cls, text):
        pos = text.find(STATE_MARKER)
        if pos < 0:
            raise RuntimeError("Redfin React InitialContext hydration is missing")
        start = text.find("{", pos + len(STATE_MARKER))
        try:
            return json.JSONDecoder().raw_decode(text[start:])[0]
        except (ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError("Redfin InitialContext hydration is malformed") from exc

    @classmethod
    def _cached_gis(cls, state):
        for key, value in cls._walk(state):
            candidates = [key] if isinstance(key, str) else []
            if isinstance(value, dict):
                candidates += [value.get(k) for k in ("url", "requestUrl", "href")]
            api_url = next((v for v in candidates if isinstance(v, str) and "/stingray/api/gis?" in v), None)
            if not api_url:
                continue
            for candidate in cls._values(value):
                try:
                    decoded = cls._decode_gis(candidate) if isinstance(candidate, str) else candidate
                except (ValueError, TypeError):
                    continue
                if cls._homes(decoded):
                    return api_url, decoded
        raise RuntimeError("Redfin hydration contains no cached Stingray GIS response")

    @staticmethod
    def _walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                yield key, child
                yield from RedfinListingSpider._walk(child)
        elif isinstance(value, list):
            for child in value:
                yield None, child
                yield from RedfinListingSpider._walk(child)

    @staticmethod
    def _values(value):
        yield value
        if isinstance(value, dict):
            for child in value.values():
                yield from RedfinListingSpider._values(child)
        elif isinstance(value, list):
            for child in value:
                yield from RedfinListingSpider._values(child)

    @staticmethod
    def _decode_gis(text):
        if not isinstance(text, str):
            return text
        text = text.strip()
        if text.startswith("{}&&"):
            text = text[4:]
        return json.loads(text)

    @staticmethod
    def _homes(payload):
        if not isinstance(payload, dict) or payload.get("resultCode", 0) != 0:
            return []
        homes = (payload.get("payload") or {}).get("homes")
        return homes if isinstance(homes, list) else []

    def _emit(self, payload, meta, response):
        for position, home in enumerate(self._homes(payload), 1):
            item_id = str(home.get("propertyId") or "")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            value = lambda key: (home.get(key) or {}).get("value") if isinstance(home.get(key), dict) else home.get(key)
            address = value("streetLine") or value("address") or ""
            title = ", ".join(str(x) for x in (address, home.get("city"), home.get("state"), home.get("zip")) if x)
            yield {
                "category": meta["category"], "item_id": item_id, "listing_id": home.get("listingId"),
                "mls_id": value("mlsId"), "title": title, "url": urljoin("https://www.redfin.com", home.get("url") or ""),
                "image_url": home.get("photoUrl") or home.get("urlPhoto"), "price": value("price"), "currency": "USD",
                "beds": value("beds"), "baths": value("baths"), "sqft": value("sqFt"), "price_per_sqft": value("pricePerSqFt"),
                "city": home.get("city"), "state": home.get("state"), "zip": home.get("zip"),
                "property_type": value("propertyType"), "status": home.get("mlsStatus"),
                "latitude": home.get("latLong", {}).get("latitude") if isinstance(home.get("latLong"), dict) else home.get("latitude"),
                "longitude": home.get("latLong", {}).get("longitude") if isinstance(home.get("latLong"), dict) else home.get("longitude"),
                "year_built": value("yearBuilt"), "photo_count": home.get("numPictures"), "days_on_market": value("dom"),
                "time_on_redfin": home.get("timeOnRedfin"), "is_hot": home.get("isHot"),
                "is_new_construction": home.get("isNewConstruction"), "page": meta["page"], "position": position,
                "source": "redfin_stingray_api", "raw": home,
                "timestamp": self.job_timestamp,
            }

    @staticmethod
    def _validate_response(response, label):
        head = response.text[:5000].lower()
        if response.status != 200:
            raise RuntimeError(f"Redfin {label} returned HTTP {response.status}")
        if any(marker in head for marker in ("captcha", "access denied", "px-captcha")):
            raise RuntimeError(f"Redfin {label} returned an anti-bot challenge")
