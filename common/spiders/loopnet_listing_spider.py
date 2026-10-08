from __future__ import annotations

"""LoopNet listings from its first-party JSON search service only."""

import json
import re
from typing import Any
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.loopnet_categories import LOOPNET_CATEGORIES


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
            self.resolve_target_url(), callback=self.parse_bootstrap, headers=self.headers,
            meta={"proxy": self.settings.get("PROXY")}, dont_filter=True,
        )

    @staticmethod
    def _bootstrap(text: str, url: str = "response") -> dict[str, Any]:
        lower = text[:200000].lower()
        if any(marker in lower for marker in (
            "failed to get successful response", "access denied", "captcha",
            "concurrency limit", "pardon the interruption",
        )):
            raise RuntimeError(f"LoopNet returned a challenge/proxy page: {url}")
        marker = "viewdata.set("
        start = text.find(marker)
        if start < 0:
            raise RuntimeError(f"LoopNet response has no viewdata bootstrap: {url}")
        try:
            state, _ = json.JSONDecoder().raw_decode(text[start + len(marker):])
        except (json.JSONDecodeError, TypeError) as exc:
            raise RuntimeError(f"Invalid LoopNet viewdata bootstrap at {url}: {exc}") from exc
        return state

    def parse_bootstrap(self, response):
        if response.status != 200:
            raise RuntimeError(f"LoopNet returned HTTP {response.status}: {response.url}")
        state = self._bootstrap(response.text, response.url)
        criteria = state.get("criteria")
        if not isinstance(criteria, dict):
            raise RuntimeError(f"LoopNet bootstrap has no search criteria: {response.url}")
        criteria["PageNumber"] = 1
        yield self._api_request(criteria, 1, response.url)

    def _api_request(self, criteria: dict[str, Any], page: int, referer: str):
        payload = {
            "pageguid": None,
            "criteria": {**criteria, "PageNumber": page},
            "savedsearcheditmode": False,
        }
        return scrapy.Request(
            "https://www.loopnet.com/services/search", method="POST",
            body=json.dumps(payload, separators=(",", ":")), callback=self.parse_api,
            headers={**self.headers, "accept": "application/json, text/plain, */*",
                     "content-type": "application/json;charset=UTF-8",
                     "x-requested-with": "XMLHttpRequest", "referer": referer},
            meta={"proxy": self.settings.get("PROXY"), "criteria": criteria,
                  "page": page, "referer": referer}, dont_filter=True,
        )

    @staticmethod
    def _value(row: dict[str, Any], *names: str):
        for name in names:
            value = row.get(name)
            if value not in (None, "", []):
                return value
        return None

    @classmethod
    def _records(cls, data: dict[str, Any]) -> list[dict[str, Any]]:
        """Select structured records, including the search API's placard fragment."""
        candidates = [
            data.get("Listings"), data.get("SearchResults"), data.get("Results"),
            data.get("MapPins"), (data.get("Map") or {}).get("Pins") if isinstance(data.get("Map"), dict) else None,
            (data.get("SearchPlacards") or {}).get("Items") if isinstance(data.get("SearchPlacards"), dict) else None,
        ]
        for candidate in candidates:
            if isinstance(candidate, list) and candidate and all(isinstance(x, dict) for x in candidate):
                return candidate
        placards = data.get("Placards") or data.get("SearchPlacards") or {}
        if isinstance(placards, dict):
            html = placards.get("HTML") or placards.get("Html")
            if isinstance(html, str):
                return cls._placard_records(html, placards)
        return []

    @staticmethod
    def _text(node, css: str) -> str | None:
        values = node.css(css).getall()
        value = " ".join(part.strip() for part in values if part.strip()).strip()
        return value or None

    @classmethod
    def _placard_records(cls, html: str, placards: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        selector = scrapy.Selector(text=html)
        coordinates: dict[str, dict[str, Any]] = {}
        event_raw = None
        if isinstance(placards, dict):
            event_raw = placards.get("PlacardsEventModel") or placards.get("placardsEventModel")
        if not event_raw:
            event_raw = selector.css("[placard-event-model]::attr(placard-event-model)").get()
        if isinstance(event_raw, str):
            try:
                event = json.loads(event_raw)
                coordinates = {
                    str(row.get("ListingID")): row
                    for row in event.get("ListingSearchResultItems", [])
                    if isinstance(row, dict) and row.get("ListingID") is not None
                }
            except (json.JSONDecodeError, TypeError):
                pass
        records = []
        for card in selector.css("article.placard[data-id]"):
            listing_id = card.attrib.get("data-id")
            price_display = cls._text(card, "ul.data-points-a li[name='Price'] *::text, ul.data-points-a li[name='Price']::text")
            price_match = re.search(r"[\d,]+(?:\.\d+)?", price_display or "")
            title = cls._text(card, "a.left-h6 *::text, a.left-h6::text") or cls._text(card, "a.left-h4 *::text, a.left-h4::text")
            address = cls._text(card, "a.left-h4 *::text, a.left-h4::text")
            location = cls._text(card, "a.right-h6 *::text, a.right-h6::text")
            coord = coordinates.get(str(listing_id), {})
            records.append({
                "ListingId": listing_id,
                "PropertyId": card.attrib.get("gtm-listing-property-id"),
                "Title": title, "Address": address,
                "ListingUrl": card.css("a.left-h4::attr(href), a.left-h6::attr(href), .placard-pseudo a::attr(ng-href)").get(),
                "City": card.attrib.get("gtm-listing-city"),
                "State": card.attrib.get("gtm-listing-state"),
                "PostalCode": card.attrib.get("gtm-listing-zip"),
                "CountryCode": card.attrib.get("gtm-listing-country"),
                "PropertyType": card.attrib.get("gtm-listing-property-type-name"),
                "ListingType": card.attrib.get("gtm-listing-search-type"),
                "Price": float(price_match.group().replace(",", "")) if price_match else None,
                "PriceDisplay": price_display,
                "SizeDisplay": cls._text(card, "a.right-h4 *::text, a.right-h4::text"),
                "LocationDisplay": location,
                "Latitude": coord.get("Latitude"), "Longitude": coord.get("Longitude"),
                "ImageUrl": card.css(".carousel-inner .slide.active img::attr(src), .carousel-inner img::attr(src)").get(),
                "Position": card.attrib.get("data-gtm-listing_position"),
            })
        return records

    def parse_api(self, response):
        if response.status != 200:
            raise RuntimeError(f"LoopNet search API returned HTTP {response.status}: {response.url}")
        try:
            envelope = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"LoopNet search API returned invalid JSON: {exc}") from exc
        data = envelope.get("data", envelope)
        if not isinstance(data, dict):
            raise RuntimeError("LoopNet search API returned no data object")
        records = self._records(data)
        if not records:
            summary = {key: type(value).__name__ for key, value in data.items()}
            raise RuntimeError(f"LoopNet search API returned no structured listing records: {summary}")

        page = int(response.meta["page"])
        total = self._value(data.get("MetaState") or {}, "TotalResultCount", "totalResultCount")
        emitted = 0
        for position, raw in enumerate(records, 1):
            item_id = self._value(raw, "ListingId", "listingId", "ListingID", "Id", "id", "PropertyId", "propertyId")
            if item_id is None or str(item_id) in self.seen:
                continue
            item_id = str(item_id)
            self.seen.add(item_id)
            emitted += 1
            yield {
                "item_id": item_id,
                "property_id": self._value(raw, "PropertyId", "propertyId", "PID", "pid"),
                "title": self._value(raw, "Title", "title", "Name", "name", "PropertyName", "propertyName"),
                "url": urljoin("https://www.loopnet.com", self._value(raw, "Url", "url", "ListingUrl", "listingUrl") or ""),
                "address": self._value(raw, "Address", "address", "AddressLine", "addressLine"),
                "city": self._value(raw, "City", "city"), "state": self._value(raw, "State", "state"),
                "postal_code": self._value(raw, "Zip", "zip", "PostalCode", "postalCode"),
                "country": self._value(raw, "Country", "country", "CountryCode", "countryCode"),
                "property_type": self._value(raw, "PropertyType", "propertyType", "PropertyTypeName"),
                "transaction_type": self._value(raw, "SearchType", "searchType", "ListingType", "listingType"),
                "price": self._value(raw, "Price", "price", "PriceValue", "priceValue"),
                "price_display": self._value(raw, "PriceDisplay", "priceDisplay", "PriceText", "priceText"),
                "currency": self._value(raw, "Currency", "currency", "CurrencyCode", "currencyCode") or "USD",
                "size": self._value(raw, "Size", "size", "SizeValue", "sizeValue"),
                "size_display": self._value(raw, "SizeDisplay", "sizeDisplay", "SizeText", "sizeText"),
                "latitude": self._value(raw, "Latitude", "latitude", "Lat", "lat"),
                "longitude": self._value(raw, "Longitude", "longitude", "Lon", "lon", "Lng", "lng"),
                "status": self._value(raw, "Status", "status"),
                "image_url": self._value(raw, "ImageUrl", "imageUrl", "PhotoUrl", "photoUrl"),
                "category": self.category or "custom", "page": page, "position": position,
                "total_count": total, "source": "loopnet_search_api", "raw": raw,
                "timestamp": self.job_timestamp,
            }

        meta = data.get("MetaState") or {}
        more = bool(self._value(meta, "HasMoreResults", "hasMoreResults", "MoreResultsChar"))
        if emitted and page < self.max_pages and (more or not total or page * len(records) < int(total)):
            yield self._api_request(response.meta["criteria"], page + 1, response.meta["referer"])
