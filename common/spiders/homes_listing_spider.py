from __future__ import annotations

import json
import re

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.homes_categories import HOMES_CATEGORIES


GSTATE_RE = re.compile(r'window\.gState\s*=\s*"((?:[^"\\]|\\.)*)"')
BLOCK_MARKERS = (
    "failed to get successful response",
    "pardon our interruption",
    "captcha",
    "access denied",
)


def decode_gstate(text: str) -> dict:
    """Decode Homes.com's printable-ASCII Caesar encoded JSON bootstrap."""
    match = GSTATE_RE.search(text)
    if not match:
        raise ValueError("window.gState bootstrap was absent")
    encoded = json.loads(f'"{match.group(1)}"')
    decoded = "".join(
        chr(32 + (ord(char) - 35) % 95) if 32 <= ord(char) <= 126 else char
        for char in encoded
    )
    return json.loads(decoded)


def parse_price(value: str) -> float | None:
    match = re.fullmatch(r"\s*\$?([\d,.]+)\s*([KM])?\s*", value or "", re.I)
    if not match:
        return None
    number = float(match.group(1).replace(",", ""))
    multiplier = {"K": 1_000, "M": 1_000_000}.get((match.group(2) or "").upper(), 1)
    return number * multiplier


class HomesListingSpider(BaseListingSpider):
    """Homes.com map listings from the server-embedded gState bootstrap only."""

    name = "homes_listing"
    allowed_domains = ["homes.com", "www.homes.com"]
    categories = HOMES_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category",
            "category_url",
            "item_id",
            "listing_key",
            "price",
            "price_raw",
            "currency",
            "latitude",
            "longitude",
            "grouped_listings",
            "map_rank",
            "total_count",
            "result_size",
            "source_url",
            "source",
            "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield scrapy.Request(
            category_url,
            callback=self.parse,
            errback=self.on_error,
            meta={"category": self.category or "custom", "category_url": category_url},
            dont_filter=True,
        )

    def parse(self, response):
        lowered = response.text.lower()
        if response.status != 200 or any(marker in lowered for marker in BLOCK_MARKERS):
            raise CloseSpider(f"Homes.com bootstrap request failed ({response.status}): {response.url}")
        try:
            state = decode_gstate(response.text)
            search = state["as"]
            markers = search["p"]
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise CloseSpider(f"Invalid Homes.com gState bootstrap at {response.url}: {exc}") from exc
        if not isinstance(markers, str) or not markers:
            raise CloseSpider(f"Homes.com gState contains no map listings: {response.url}")

        result_size = search.get("sc", {}).get("pagingCriteria", {}).get("resultSize")
        emitted = 0
        for map_rank, record in enumerate(markers.split("~"), start=1):
            fields = record.split("|")
            if len(fields) < 6:
                continue
            price_raw, listing_key, group_raw, latitude, longitude, item_id = fields[:6]
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            emitted += 1
            grouped_listings = None
            if group_raw:
                try:
                    grouped_listings = json.loads(group_raw)
                except json.JSONDecodeError:
                    grouped_listings = None
            raw = {
                "price": price_raw,
                "listing_key": listing_key,
                "group": group_raw or None,
                "latitude": latitude,
                "longitude": longitude,
                "property_key": item_id,
                "extra": fields[6:],
            }
            yield {
                "category": response.meta["category"],
                "category_url": response.meta["category_url"],
                "item_id": item_id,
                "listing_key": listing_key,
                "price": parse_price(price_raw),
                "price_raw": price_raw,
                "currency": "USD",
                "latitude": float(latitude) if latitude else None,
                "longitude": float(longitude) if longitude else None,
                "grouped_listings": grouped_listings,
                "map_rank": map_rank,
                "total_count": search.get("count"),
                "result_size": result_size,
                "source_url": response.url,
                "source": "homes_gstate_map_bootstrap",
                "raw": raw,
                "timestamp": self.job_timestamp,
            }
        if not emitted:
            raise CloseSpider(f"Homes.com gState yielded no valid map listings: {response.url}")

    def on_error(self, failure):
        raise CloseSpider(f"Homes.com request failed: {failure.value}")
