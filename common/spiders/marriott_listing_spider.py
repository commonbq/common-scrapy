from __future__ import annotations

"""Marriott destination listings from server-rendered Next.js hydration."""

import json
import re
from typing import Any, Iterable
from urllib.parse import parse_qsl, quote, unquote, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.marriott_categories import MARRIOTT_CATEGORIES


class MarriottListingSpider(BaseListingSpider):
    """Extract Marriott properties only from ``__NEXT_DATA__`` bootstrap state."""

    name = "marriott_listing"
    allowed_domains = ["marriott.com", "www.marriott.com"]
    categories = MARRIOTT_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "brand_code", "title", "url", "description",
            "image_url", "image_alt", "images", "rating", "reviews_count",
            "reviews_text", "reviews_url", "distance_miles", "distance_text",
            "availability_url", "price", "currency", "is_available", "is_bookable",
            "page", "position", "total_count", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        self._seen.clear()
        yield self._request(self.resolve_target_url(), page=1)

    def parse(self, response: scrapy.http.Response, **kwargs):
        self._check_response(response)
        payload = self._next_data(response)
        processed = self._processed_data(payload, response.url)
        hotels = processed.get("hotels")
        if not isinstance(hotels, list):
            raise RuntimeError(f"Marriott hydration hotels schema changed at {response.url}")

        page = int(response.meta.get("page", 1))
        total = self._integer(processed.get("totalProperties"))
        new_ids = 0
        for position, hotel in enumerate(hotels, start=1):
            if not isinstance(hotel, dict):
                continue
            item_id = str(hotel.get("id") or "").strip().upper()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            new_ids += 1
            yield self._item(hotel, response, page, position, total)

        if (
            page < self.max_pages
            and hotels
            and new_ids
            and (total is None or page * len(hotels) < total)
        ):
            yield self._request(response.url, page=page + 1)

    def _request(self, url: str, *, page: int) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(url, page), callback=self.parse, headers=self.headers,
            dont_filter=page > 1,
            meta={
                "proxy": self._residential_proxy(),
                "category": self.category or "custom",
                "page": page,
            },
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
                 if key != "pg"]
        if page > 1:
            query.append(("pg", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _residential_proxy(self) -> str | None:
        """Enable the US residential ScrapeOps route without embedding credentials."""
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return proxy
        username = unquote(parts.username)
        for option in ("residential=true", "country=us"):
            if option not in username.split("."):
                username += "." + option
        auth = quote(username, safe=".=")
        if parts.password is not None:
            auth += ":" + quote(unquote(parts.password), safe="")
        host = parts.hostname + (f":{parts.port}" if parts.port else "")
        return urlunsplit((parts.scheme, f"{auth}@{host}", parts.path, parts.query, parts.fragment))

    @staticmethod
    def _check_response(response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(f"Marriott returned HTTP {response.status}: {response.url}")

    @staticmethod
    def _next_data(response: scrapy.http.Response) -> dict[str, Any]:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Marriott __NEXT_DATA__ missing at {response.url}")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Marriott __NEXT_DATA__ is invalid at {response.url}") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"Marriott __NEXT_DATA__ schema changed at {response.url}")
        return payload

    @classmethod
    def _processed_data(cls, payload: dict[str, Any], url: str) -> dict[str, Any]:
        matches: list[dict[str, Any]] = []

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                processed = value.get("processedData")
                if isinstance(processed, dict) and isinstance(processed.get("hotels"), list):
                    matches.append(processed)
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(payload.get("props", {}).get("pageProps", {}).get("model", {}))
        if len(matches) != 1:
            raise RuntimeError(
                f"Marriott expected one hydrated hotel collection at {url}; found {len(matches)}"
            )
        return matches[0]

    def _item(self, hotel: dict[str, Any], response: scrapy.http.Response,
              page: int, position: int, total: int | None) -> dict[str, Any]:
        title = hotel.get("titleDetails") or {}
        reviews = hotel.get("reviewsDetails") or {}
        footer = hotel.get("footerLinkDetails") or {}
        images = hotel.get("images") if isinstance(hotel.get("images"), list) else []
        first_image = images[0] if images and isinstance(images[0], dict) else {}
        price = self._number(footer.get("priceValue")) if footer.get("hasPrice") else None
        unavailable = footer.get("isHotelUnavailable")
        return {
            "category": response.meta.get("category", self.category or "custom"),
            "item_id": str(hotel.get("id") or "").strip().upper(),
            "brand_code": hotel.get("brandCode") or (hotel.get("brandDetails") or {}).get("brandId"),
            "title": title.get("title"),
            "url": urljoin("https://www.marriott.com", title.get("titleLink") or ""),
            "description": hotel.get("description"),
            "image_url": first_image.get("defaultImageUrl"),
            "image_alt": first_image.get("altText"),
            "images": images,
            "rating": self._number(reviews.get("reviewsAvg")),
            "reviews_count": self._integer_from_text(reviews.get("reviewsText")),
            "reviews_text": reviews.get("reviewsText"),
            "reviews_url": urljoin("https://www.marriott.com", reviews.get("reviewsLink") or ""),
            "distance_miles": self._number_from_text(reviews.get("milesText")),
            "distance_text": reviews.get("milesText"),
            "availability_url": urljoin("https://www.marriott.com", footer.get("href") or ""),
            "price": price,
            "currency": footer.get("currency"),
            "is_available": None if unavailable is None else not unavailable,
            "is_bookable": hotel.get("isHotelBookable"),
            "page": page,
            "position": position,
            "total_count": total,
            "source": "marriott_next_data_hydration",
            "raw": hotel,
            "timestamp": self.job_timestamp,
        }

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if isinstance(value, bool) or value is None:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        return int(number) if number.is_integer() else number

    @classmethod
    def _number_from_text(cls, value: Any) -> int | float | None:
        match = re.search(r"-?\d+(?:\.\d+)?", str(value or "").replace(",", ""))
        return cls._number(match.group()) if match else None

    @staticmethod
    def _integer(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer_from_text(value: Any) -> int | None:
        match = re.search(r"\d[\d,]*", str(value or ""))
        return int(match.group().replace(",", "")) if match else None
