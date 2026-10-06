from __future__ import annotations

"""Booking.com accommodations from server-rendered Apollo hydration."""

import json
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.booking_categories import BOOKING_CATEGORIES


class BookingListingSpider(BaseListingSpider):
    """Extract Booking search pages using only their anonymous Apollo cache."""

    name = "booking_listing"
    allowed_domains = ["booking.com", "www.booking.com"]
    categories = BOOKING_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "url", "image_url", "price",
            "original_price", "currency", "rating", "reviews_count", "stars",
            "district", "city", "country", "latitude", "longitude",
            "property_type", "page", "position", "total_count", "source", "raw",
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
        yield scrapy.Request(
            self.resolve_target_url(), callback=self.parse_city, headers=self.headers,
            meta={"proxy": self._proxy(), "category": self.category or "custom"},
        )

    def parse_city(self, response: scrapy.http.Response):
        self._check_response(response)
        root = self._apollo_root(response)
        matches = [v for k, v in root.items() if k.startswith("lxAccommodations(")]
        if len(matches) != 1 or not isinstance(matches[0], dict):
            raise RuntimeError(
                f"booking city Apollo contract missing lxAccommodations at {response.url}"
            )
        web = matches[0].get("web") or {}
        snippet = web.get("searchResultSnippet") or {}
        destination = web.get("destination") or {}
        identifier = destination.get("identifier") or {}
        search_url = snippet.get("seeAllUrl")
        dest_id = identifier.get("destId")
        if not search_url or dest_id is None:
            raise RuntimeError(
                f"booking city Apollo contract has no seeAllUrl/destId at {response.url}"
            )
        yield self._search_request(
            urljoin(response.url, search_url), page=1,
            category=response.meta["category"], dest_id=dest_id,
        )

    def parse_search(self, response: scrapy.http.Response):
        self._check_response(response)
        root = self._apollo_root(response)
        search_queries = root.get("searchQueries")
        if not isinstance(search_queries, dict):
            raise RuntimeError(f"booking search Apollo contract missing searchQueries at {response.url}")
        matches = [v for k, v in search_queries.items() if k.startswith("search(")]
        if len(matches) != 1 or not isinstance(matches[0], dict):
            raise RuntimeError(f"booking search Apollo contract missing unique search output at {response.url}")
        output = matches[0]
        results = output.get("results")
        pagination = output.get("pagination")
        if not isinstance(results, list) or not isinstance(pagination, dict):
            raise RuntimeError(f"booking search Apollo result schema changed at {response.url}")

        page = int(response.meta["page"])
        total = self._number(pagination.get("nbResultsTotal"))
        rows = int(self._number(pagination.get("nbResultsPerPage")) or len(results) or 25)
        for position, result in enumerate(results, start=1):
            if not isinstance(result, dict):
                continue
            basic = result.get("basicPropertyData") or {}
            item_id = str(basic.get("id") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(result, response, page, position, total)

        if page < self.max_pages and results and (total is None or page * rows < total):
            yield self._search_request(
                response.url, page=page + 1, category=response.meta["category"],
                dest_id=response.meta["dest_id"], rows=rows,
            )

    def _search_request(self, url: str, *, page: int, category: str,
                        dest_id: int | str, rows: int = 25) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(url, page, rows), callback=self.parse_search,
            headers=self.headers, dont_filter=True,
            meta={"proxy": self._proxy(), "page": page, "category": category, "dest_id": dest_id},
        )

    @staticmethod
    def _page_url(url: str, page: int, rows: int = 25) -> str:
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                 if k not in {"offset", "rows", "aid", "label", "sid"}]
        query.extend((("rows", str(rows)), ("offset", str((page - 1) * rows))))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _proxy(self) -> str | None:
        return getattr(self, "settings", {}).get("PROXY")

    @staticmethod
    def _check_response(response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(f"booking returned HTTP {response.status}: {response.url}")

    @staticmethod
    def _apollo_root(response: scrapy.http.Response) -> dict[str, Any]:
        matches = []
        for text in response.xpath('//script[@type="application/json"]/text()').getall():
            try:
                payload = json.loads(text)
            except (TypeError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict) and isinstance(payload.get("ROOT_QUERY"), dict):
                matches.append(payload["ROOT_QUERY"])
        if len(matches) != 1:
            raise RuntimeError(
                f"booking expected one Apollo ROOT_QUERY at {response.url}; found {len(matches)}"
            )
        return matches[0]

    def _item(self, result: dict[str, Any], response: scrapy.http.Response,
              page: int, position: int, total: float | None) -> dict[str, Any]:
        basic = result.get("basicPropertyData") or {}
        location = basic.get("location") or {}
        reviews = basic.get("reviews") or {}
        photo = ((basic.get("photos") or {}).get("main") or {}).get("highResUrl") or {}
        display_price = (((result.get("priceDisplayInfoIrene") or {}).get("displayPrice") or {})
                         .get("amountPerStay") or {})
        before = (((result.get("priceDisplayInfoIrene") or {}).get("priceBeforeDiscount") or {})
                  .get("amountPerStay") or {})
        item_id = str(basic.get("id"))
        page_name = basic.get("pageName")
        title = (result.get("displayName") or {}).get("text")
        return {
            "category": response.meta["category"], "item_id": item_id, "title": title,
            "url": f"https://www.booking.com/hotel/{location.get('countryCode')}/{page_name}.html",
            "image_url": urljoin("https://cf.bstatic.com", photo.get("relativeUrl") or ""),
            "price": self._number(display_price.get("amountUnformatted")),
            "original_price": self._number(before.get("amountUnformatted")),
            "currency": display_price.get("currency"),
            "rating": self._number(reviews.get("totalScore")),
            "reviews_count": self._number(reviews.get("reviewsCount")),
            "stars": self._number((basic.get("starRating") or {}).get("value")),
            "district": (result.get("location") or {}).get("popularFreeDistrictName"),
            "city": location.get("city"), "country": location.get("countryCode"),
            "latitude": self._number(location.get("latitude")),
            "longitude": self._number(location.get("longitude")),
            "property_type": basic.get("accommodationTypeId"), "page": page,
            "position": position, "total_count": total,
            "source": "booking_apollo_hydration", "raw": result,
        }

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            number = float(value)
            return int(number) if number.is_integer() else number
        except (TypeError, ValueError):
            return None
