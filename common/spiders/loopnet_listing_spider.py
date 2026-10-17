from __future__ import annotations

"""LoopNet listings from the server-rendered search results page.

LoopNet's category page is a server-rendered search-results page. Every listing
card is present in the HTML as an ``article.placard-card`` element, and the page
ships the full search state in an obfuscated ``window.gState`` JSON blob. That
blob carries the authoritative search criteria, the result count, and the
per-listing latitude/longitude pairs (which the placard HTML does not repeat).

The previous implementation hydrated the site's private ``viewdata.set(...)``
bootstrap and replayed it against ``POST /services/search``. LoopNet has since
removed that bootstrap *and* that service now rejects replayed requests, so the
spider emitted zero items and the run log had no ``item_scraped_count``
(commonbq/common-scrapy#379). This spider now reads the one authoritative
product source the page actually serves: the server-rendered placards plus the
``window.gState`` search state.
"""

import codecs
import json
import re
from typing import Any

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.loopnet_categories import LOOPNET_CATEGORIES

# The gState JSON string is offset by three code points (a simple obfuscation):
# every printable ASCII byte in the embedded string is shifted down by 3.
_SHIFT = 3
_GSTATE_RE = re.compile(r'window\.gState\s*=\s*"((?:[^"\\]|\\.)*)"', re.S)
_CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "pardon the interruption",
    "concurrency limit",
    "failed to get successful response",
)
_PRICE_RE = re.compile(r"\$\s*([\d,]+(?:\.\d+)?)")


def _unshift(value: str) -> str:
    out = []
    for char in value:
        code = ord(char)
        if 32 <= code <= 126:
            shifted = code - _SHIFT
            out.append(chr(shifted if shifted >= 32 else shifted + 95))
        else:
            out.append(char)
    return "".join(out)


class LoopnetListingSpider(BaseListingSpider):
    name = "loopnet_listing"
    allowed_domains = ["loopnet.com", "www.loopnet.com"]
    categories = LOOPNET_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "item_id", "property_id", "title", "url", "address", "city",
            "state", "postal_code", "country", "property_type",
            "transaction_type", "price", "price_display", "currency",
            "size", "size_display", "latitude", "longitude", "status",
            "image_url", "category", "page", "position", "total_count",
            "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen: set[str] = set()

    def start_requests(self):
        yield scrapy.Request(
            self.resolve_target_url(), callback=self.parse_page, headers=self.headers,
            meta={"proxy": getattr(self, "settings", {}).get("PROXY"), "page": 1},
            dont_filter=True,
        )

    # ------------------------------------------------------------- page state

    @staticmethod
    def _search_state(text: str, url: str = "response") -> dict[str, Any]:
        """Decode LoopNet's ``window.gState`` search-state blob."""
        lower = text[:200000].lower()
        if any(marker in lower for marker in _CHALLENGE_MARKERS):
            raise RuntimeError(f"LoopNet returned a challenge/proxy page: {url}")
        match = _GSTATE_RE.search(text)
        if not match:
            raise RuntimeError(f"LoopNet response has no gState bootstrap: {url}")
        try:
            state = json.loads(_unshift(codecs.decode(match.group(1), "unicode_escape")))
        except (json.JSONDecodeError, ValueError, TypeError) as exc:
            raise RuntimeError(f"Invalid LoopNet gState bootstrap at {url}: {exc}") from exc
        if not isinstance(state, dict):
            raise RuntimeError(f"LoopNet gState bootstrap is not an object at {url}")
        return state

    @classmethod
    def _coordinates(cls, state: dict[str, Any]) -> dict[str, tuple[float, float]]:
        """Join listing id -> (lat, lon) from the ``as.sp`` map-pin string."""
        raw = ((state.get("as") or {}).get("sp")) or ""
        if not isinstance(raw, str):
            return {}
        coordinates: dict[str, tuple[float, float]] = {}
        for chunk in raw.split("~"):
            parts = chunk.split("|")
            if len(parts) < 4 or not parts[0]:
                continue
            try:
                coordinates.setdefault(parts[0], (float(parts[2]), float(parts[3])))
            except (ValueError, TypeError):
                continue
        return coordinates

    @staticmethod
    def _total_results(state: dict[str, Any]) -> int | None:
        search = (state.get("as") or {}).get("sc") or {}
        for key in ("mrc", "count"):
            value = (state.get("as") or {}).get(key)
            if isinstance(value, int):
                return value
        page_size = (search.get("pagingCriteria") or {}).get("pageSize")
        return page_size if isinstance(page_size, int) else None

    # ---------------------------------------------------------- placard parse

    @staticmethod
    def _placard_records(html: str) -> list[dict[str, Any]]:
        selector = scrapy.Selector(text=html)
        records = []
        for card in selector.css("article.placard-card"):
            listing_id = card.attrib.get("data-lk") or card.attrib.get("data-gtm-listing_id")
            if not listing_id:
                continue
            data_rows = [
                " ".join(part.strip() for part in row.css("span::text").getall() if part.strip())
                for row in card.css("p.data-row")
            ]
            price_display = next((row for row in data_rows if "$" in row), None)
            price_match = _PRICE_RE.search(price_display or "")
            size_display = next((row for row in data_rows if "SF" in row or "AC" in row), None)
            size_match = re.search(r"([\d,]+(?:\.\d+)?)\s*(?:-|SF|AC)", size_display or "")
            address_tail = card.css("p.placard-address::text").get()
            records.append({
                "ListingId": listing_id,
                "PropertyId": card.attrib.get("data-gtm-listing_id"),
                "Title": card.css("span.building-name::text").get()
                or card.css("a.placard-link::attr(title)").get(),
                "Address": address_tail,
                "ListingUrl": card.css("a.placard-link::attr(href)").get(),
                "City": card.attrib.get("data-automation-city"),
                "State": card.attrib.get("data-automation-state"),
                "PostalCode": card.attrib.get("data-automation-postal-code"),
                "CountryCode": card.attrib.get("data-automation-country"),
                "PropertyType": card.attrib.get("data-automation-property-type"),
                "ListingType": card.attrib.get("data-automation-transaction-type"),
                "Price": float(price_match.group(1).replace(",", "")) if price_match else None,
                "PriceDisplay": price_display,
                "Size": float(size_match.group(1).replace(",", "")) if size_match else None,
                "SizeDisplay": size_display,
                "ImageUrl": card.css("img.embla__slide__img::attr(src)").get(),
                "Position": card.attrib.get("data-gtm-listing_position"),
            })
        return records

    # ------------------------------------------------------------------ parse

    def parse_page(self, response):
        if response.status != 200:
            raise RuntimeError(f"LoopNet returned HTTP {response.status}: {response.url}")
        state = self._search_state(response.text, response.url)
        coordinates = self._coordinates(state)
        records = self._placard_records(response.text)
        if not records:
            raise RuntimeError(f"LoopNet page returned no placard listings: {response.url}")

        page = int(response.meta.get("page", 1))
        total = self._total_results(state)
        for position, raw in enumerate(records, 1):
            item_id = str(raw["ListingId"])
            if item_id in self.seen:
                continue
            self.seen.add(item_id)
            latitude, longitude = coordinates.get(item_id, (None, None))
            yield {
                "item_id": item_id,
                "property_id": raw.get("PropertyId"),
                "title": raw.get("Title"),
                "url": raw.get("ListingUrl"),
                "address": raw.get("Address"),
                "city": raw.get("City"),
                "state": raw.get("State"),
                "postal_code": raw.get("PostalCode"),
                "country": raw.get("CountryCode"),
                "property_type": raw.get("PropertyType"),
                "transaction_type": raw.get("ListingType"),
                "price": raw.get("Price"),
                "price_display": raw.get("PriceDisplay"),
                "currency": "USD",
                "size": raw.get("Size"),
                "size_display": raw.get("SizeDisplay"),
                "latitude": latitude,
                "longitude": longitude,
                "status": "Active",
                "image_url": raw.get("ImageUrl"),
                "category": self.category or "custom",
                "page": page,
                "position": int(raw.get("Position") or position),
                "total_count": total,
                "source": "loopnet_placard_html",
                "raw": raw,
                "timestamp": self.job_timestamp,
            }

        if page < self.max_pages and records:
            next_url = response.url.rstrip("/") + f"/{page + 1}/"
            proxy = getattr(self, "settings", {}).get("PROXY")
            yield scrapy.Request(
                next_url, callback=self.parse_page, headers=self.headers,
                meta={"proxy": proxy, "page": page + 1},
                dont_filter=True,
            )
