from __future__ import annotations

"""Zumper rentals extracted exclusively from server-rendered bootstrap state."""

from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.retail_bootstrap_utils import extract_preloaded_state
from common.spiders.zumper_categories import ZUMPER_CATEGORIES


class ZumperListingSpider(BaseListingSpider):
    name = "zumper_listing"
    allowed_domains = ["zumper.com", "www.zumper.com"]
    categories = ZUMPER_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "item_id", "listing_id", "building_id", "title", "building_name",
            "url", "address", "city", "state", "zipcode", "latitude", "longitude",
            "min_price", "max_price", "currency", "min_bedrooms", "max_bedrooms",
            "min_bathrooms", "max_bathrooms", "min_square_feet", "max_square_feet",
            "amenities", "pets", "rating", "phone", "image_urls", "date_available",
            "category", "city_id", "page", "position", "total_count", "has_more",
            "timestamp", "source", "raw",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url: str, page: int) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(base_url, page), headers=self.headers, callback=self.parse,
            meta={"proxy": self.settings.get("PROXY"), "page": page, "base_url": base_url},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query) if key != "page"]
        if page > 1:
            query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Zumper returned HTTP {response.status}: {response.url}")
        lower = response.text[:300000].lower()
        if len(response.body) < 5000 or any(marker in lower for marker in (
            "access denied", "captcha", "pardon the interruption",
            "failed to get successful response",
        )):
            raise RuntimeError(f"Zumper returned a challenge/proxy page: {response.url}")

        state = extract_preloaded_state(response.text)
        if not state:
            raise RuntimeError(f"Zumper response has no __PRELOADED_STATE__: {response.url}")
        current = state.get("currentSearch") or {}
        groups = current.get("listables") or {}
        records = self._records(groups)
        if not records:
            raise RuntimeError(f"Zumper bootstrap has no currentSearch.listables: {response.url}")

        page = int(response.meta.get("page", 1))
        city = self._market(state)
        total = city.get("listing_count") or current.get("firstPageCount")
        has_more = bool(current.get("hasMoreListables"))
        emitted = 0
        for position, raw in enumerate(records, 1):
            item_id = self._item_id(raw)
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(raw, response, city, item_id, page, position, total, has_more)

        if has_more and emitted and page < self.max_pages:
            yield self._request(response.meta["base_url"], page + 1)

    @staticmethod
    def _records(groups: Any) -> list[dict[str, Any]]:
        if not isinstance(groups, dict):
            return []
        records: list[dict[str, Any]] = []
        for key in ("featured", "listables", "spotlight", "nearby"):
            value = groups.get(key) or []
            if isinstance(value, list):
                records.extend(row for row in value if isinstance(row, dict))
        return records

    @staticmethod
    def _market(state: dict[str, Any]) -> dict[str, Any]:
        cities = (state.get("geo") or {}).get("cities") or []
        return cities[0] if cities and isinstance(cities[0], dict) else {}

    @staticmethod
    def _item_id(raw: dict[str, Any]) -> str | None:
        value = raw.get("pb_id") or raw.get("pl_id") or raw.get("listing_id")
        return str(value) if value is not None else None

    def _item(self, raw, response, city, item_id, page, position, total, has_more):
        image_ids = raw.get("image_ids") or []
        return {
            "item_id": item_id,
            "listing_id": raw.get("listing_id"),
            "building_id": raw.get("building_id") or raw.get("pb_id"),
            "title": raw.get("building_name") or raw.get("title") or raw.get("address"),
            "building_name": raw.get("building_name"),
            "url": urljoin(response.url, raw.get("url") or raw.get("pb_url") or raw.get("pl_url") or ""),
            "address": raw.get("address"), "city": raw.get("city") or city.get("name"),
            "state": raw.get("state") or city.get("state"), "zipcode": raw.get("zipcode"),
            "latitude": raw.get("lat"), "longitude": raw.get("lng"),
            "min_price": raw.get("min_price"), "max_price": raw.get("max_price"), "currency": "USD",
            "min_bedrooms": raw.get("min_bedrooms"), "max_bedrooms": raw.get("max_bedrooms"),
            "min_bathrooms": raw.get("min_bathrooms"), "max_bathrooms": raw.get("max_bathrooms"),
            "min_square_feet": raw.get("min_square_feet"), "max_square_feet": raw.get("max_square_feet"),
            "amenities": raw.get("amenity_tags") or [], "pets": raw.get("pets") or [],
            "rating": raw.get("rating") or raw.get("external_rating"), "phone": raw.get("phone"),
            "image_urls": [f"https://img.zumpercdn.com/{image_id}/1280x960" for image_id in image_ids],
            "date_available": raw.get("date_available"), "category": self.category or "custom",
            "city_id": city.get("city_id"), "page": page, "position": position,
            "total_count": total, "has_more": has_more, "timestamp": self.get_timestamp(),
            "source": "zumper_preloaded_state", "raw": raw,
        }
