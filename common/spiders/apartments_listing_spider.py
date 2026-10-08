from __future__ import annotations

"""Apartments.com rental inventory from ``window.aptsState`` only.

The server-rendered bootstrap contains the complete map inventory rather than
only the 40 rendered placards.  Product rows are therefore read exclusively
from ``aptsState.as.p``; HTML cards and JSON-LD are deliberately not parsed.
"""

import json
import re

import scrapy

from common.spiders.apartments_categories import APARTMENTS_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


class ApartmentsListingSpider(BaseListingSpider):
    name = "apartments_listing"
    allowed_domains = ["apartments.com", "www.apartments.com", "localhost", "127.0.0.1"]
    categories = APARTMENTS_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "latitude", "longitude", "listing_type_code",
            "feature_flags", "rent_min", "rent_max", "currency", "multi_unit",
            "related_listing_ids", "market_display", "city", "state", "county",
            "country_code", "market_name", "dma", "geography_id", "geography_type",
            "geography_vector_id", "total_available", "total_capped", "nearby_count",
            "page", "total_pages", "next_url", "position", "source_url", "source",
            "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    _assignment = re.compile(r"window\.aptsState\s*=\s*", re.DOTALL)
    _challenge_markers = (
        "failed to get successful response",
        "you have consumed all your api credits",
        "pardon the interruption",
        "px-captcha",
        "access denied",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen: set[str] = set()

    def start_requests(self):
        if self.url or self.category_url or self.category:
            yield self._request(self.resolve_target_url(), self.category or "custom", 1)
            return
        for entry in self.categories:
            yield self._request(entry["url"], entry["category"], 1)

    def _request(self, url: str, category: str, page: int):
        settings = getattr(self, "settings", {})
        return scrapy.Request(
            url,
            callback=self.parse,
            headers=self.headers,
            meta={"proxy": settings.get("PROXY"), "category": category, "page": page},
            dont_filter=True,
        )

    @classmethod
    def _bootstrap(cls, document: str, url: str = "response") -> dict:
        lowered = document.lower()
        if any(marker in lowered for marker in cls._challenge_markers):
            raise RuntimeError(f"Apartments.com challenge/proxy response at {url}")
        match = cls._assignment.search(document)
        if not match:
            raise RuntimeError(f"Apartments.com response has no window.aptsState bootstrap at {url}")
        try:
            state, _ = json.JSONDecoder().raw_decode(document, match.end())
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid Apartments.com aptsState bootstrap at {url}: {exc}") from exc
        inventory = state.get("as", {}).get("p") if isinstance(state, dict) else None
        if not isinstance(inventory, list):
            raise RuntimeError(f"Apartments.com aptsState has no as.p inventory at {url}")
        return state

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Apartments.com returned HTTP {response.status}: {response.url}")
        state = self._bootstrap(response.text, response.url)
        search = state["as"]
        inventory = search["p"]
        paging = search.get("pg") or {}
        geography = (search.get("ic") or {}).get("g") or {}
        address = geography.get("a") or {}
        page = self._integer(paging.get("page")) or self._integer(response.meta.get("page")) or 1
        total_pages = self._integer(paging.get("totalPages"))
        new_count = 0

        for position, record in enumerate(inventory, 1):
            if not isinstance(record, dict):
                continue
            item_id = str(record.get("k") or "").strip()
            if not item_id or item_id in self.seen:
                continue
            self.seen.add(item_id)
            new_count += 1
            related = [
                str(row.get("k")) for row in (record.get("sl") or [])
                if isinstance(row, dict) and row.get("k")
            ]
            yield {
                "category": response.meta.get("category"),
                "item_id": item_id,
                "latitude": record.get("lat"),
                "longitude": record.get("lng"),
                "listing_type_code": record.get("t"),
                "feature_flags": record.get("f"),
                "rent_min": record.get("nr"),
                "rent_max": record.get("xr"),
                "currency": "USD" if record.get("nr") is not None or record.get("xr") is not None else None,
                "multi_unit": bool(record.get("mu")) if record.get("mu") is not None else None,
                "related_listing_ids": related,
                "market_display": geography.get("d"),
                "city": address.get("ci"),
                "state": address.get("st"),
                "county": address.get("co"),
                "country_code": address.get("cc"),
                "market_name": address.get("mn"),
                "dma": address.get("dma"),
                "geography_id": geography.get("id"),
                "geography_type": geography.get("t"),
                "geography_vector_id": geography.get("v"),
                "total_available": search.get("ac"),
                "total_capped": search.get("lc"),
                "nearby_count": search.get("nc"),
                "page": page,
                "total_pages": total_pages,
                "next_url": paging.get("nextUrl"),
                "position": position,
                "source_url": response.url,
                "source": "apartments_apts_state_bootstrap",
                "raw": record,
                "timestamp": self.job_timestamp,
            }

        next_url = paging.get("nextUrl")
        if next_url and page < self.max_pages and (total_pages is None or page < total_pages) and new_count:
            yield self._request(next_url, response.meta.get("category") or "custom", page + 1)

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
