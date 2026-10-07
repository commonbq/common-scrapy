from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.worldmarket_categories import (
    WORLD_MARKET_BASE_URL,
    WORLD_MARKET_CATEGORIES,
)

API_PATH = "/on/demandware.store/Sites-World_Market-Site/en_US/Search-UpdateGrid"
BLOCK_MARKERS = (
    "failed to get successful response",
    "pardon our interruption",
    "access denied",
    "captcha",
    "_incapsula_resource",
)


def _number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", value)
    return float(match.group(0).replace(",", "")) if match else None


def _flag(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


class WorldmarketListingSpider(BaseListingSpider):
    """World Market products from the first-party SFCC grid API only."""

    name = "worldmarket_listing"
    allowed_domains = ["worldmarket.com", "www.worldmarket.com"]
    categories = WORLD_MARKET_CATEGORIES
    DEFAULT_PAGE_SIZE = 60

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category", "category_url", "category_id", "item_id", "sku", "title",
            "url", "image_url", "price", "original_price", "currency", "availability",
            "rating", "reviews_count", "is_sale", "is_clearance", "is_new", "page",
            "position", "total_count", "source_url", "source", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        self.page_size = int(kwargs.pop("page_size", self.DEFAULT_PAGE_SIZE))
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield scrapy.Request(
            category_url,
            callback=self.parse_category,
            errback=self.on_error,
            meta={"category": self.category or "custom", "category_url": category_url},
            dont_filter=True,
        )

    def parse_category(self, response):
        self._validate_response(response, "category bootstrap")
        cgid = self._extract_cgid(response)
        if not cgid:
            raise CloseSpider(f"World Market category id was absent from {response.url}")
        yield self._api_request(cgid, start=0, meta=response.meta)

    @staticmethod
    def _extract_cgid(response) -> str | None:
        urls = response.css('a[href*="Search-UpdateGrid"]::attr(href)').getall()
        urls += response.css('option[data-url*="Search-UpdateGrid"]::attr(data-url)').getall()
        for raw in urls:
            cgid = parse_qs(urlsplit(raw.replace("&amp;", "&")).query).get("cgid")
            if cgid and cgid[0]:
                return cgid[0]
        match = re.search(r'[?&]cgid=([A-Za-z0-9_-]+)', response.text)
        return match.group(1) if match else None

    def _api_request(self, cgid: str, start: int, meta: dict):
        query = urlencode({"cgid": cgid, "start": start, "sz": self.page_size})
        url = f"{WORLD_MARKET_BASE_URL}{API_PATH}?{query}"
        return scrapy.Request(
            url,
            callback=self.parse_api,
            errback=self.on_error,
            headers={"Accept": "text/html, */*; q=0.01", "X-Requested-With": "XMLHttpRequest"},
            meta={
                "category": meta["category"], "category_url": meta["category_url"],
                "category_id": cgid, "start": start,
            },
            dont_filter=True,
        )

    def parse_api(self, response):
        self._validate_response(response, "Search-UpdateGrid API")
        meta = response.meta
        page = meta["start"] // self.page_size + 1
        tiles = response.css(".product.js-a-tile-data")
        if not tiles:
            raise CloseSpider(f"World Market API returned no product records: {response.url}")

        emitted = 0
        total_count = self._total_count(response)
        for offset, tile in enumerate(tiles, start=1):
            item_id = tile.attrib.get("data-id") or tile.attrib.get("data-sku") or tile.attrib.get("data-collection-id")
            if not item_id or item_id == "null" or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            emitted += 1
            prices = [_number(v) for v in tile.css(".price .value::attr(content), .price .value::text").getall()]
            prices = [v for v in prices if v is not None]
            href = tile.css("a.js-a-product-click::attr(href), a[href*='/p/']::attr(href)").get()
            raw = {key: value for key, value in tile.attrib.items() if key.startswith("data-")}
            yield {
                "category": meta["category"], "category_url": meta["category_url"],
                "category_id": meta["category_id"], "item_id": item_id,
                "sku": tile.attrib.get("data-sku"), "title": tile.attrib.get("data-product-name"),
                "url": urljoin(WORLD_MARKET_BASE_URL, href) if href else None,
                "image_url": tile.attrib.get("data-image-url"), "price": prices[0] if prices else None,
                "original_price": max(prices) if len(prices) > 1 else None, "currency": "USD",
                "availability": tile.attrib.get("data-online-status"),
                "rating": _number(tile.attrib.get("data-rating")),
                "reviews_count": int(_number(tile.attrib.get("data-reviews")) or 0),
                "is_sale": _flag(tile.attrib.get("data-sale-tag")),
                "is_clearance": _flag(tile.attrib.get("data-clearance-tag")),
                "is_new": _flag(tile.attrib.get("data-new-tag")), "page": page,
                "position": meta["start"] + offset, "total_count": total_count,
                "source_url": response.url, "source": "worldmarket_sfcc_search_update_grid_api",
                "raw": raw,
            }

        next_start = meta["start"] + self.page_size
        if emitted and page < self.max_pages and (total_count is None or next_start < total_count):
            yield self._api_request(meta["category_id"], next_start, meta)

    @staticmethod
    def _total_count(response) -> int | None:
        for url in response.css('[data-url*="Search-UpdateGrid"]::attr(data-url), a[href*="Search-UpdateGrid"]::attr(href)').getall():
            value = parse_qs(urlsplit(url.replace("&amp;", "&")).query).get("count")
            if value and value[0].isdigit():
                return int(value[0])
        match = re.search(r'[?&]count=(\d+)', response.text)
        return int(match.group(1)) if match else None

    @staticmethod
    def _validate_response(response, leg: str):
        lowered = response.text.lower()
        if response.status != 200 or not response.body or any(marker in lowered for marker in BLOCK_MARKERS):
            raise CloseSpider(f"World Market {leg} failed ({response.status}): {response.url}")

    def on_error(self, failure):
        raise CloseSpider(f"World Market request failed: {failure.value}")
