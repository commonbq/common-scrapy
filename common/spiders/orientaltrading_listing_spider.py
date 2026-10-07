from __future__ import annotations

import re
from urllib.parse import parse_qsl, urljoin, urlsplit, urlunsplit

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.orientaltrading_categories import (
    ORIENTAL_TRADING_BASE_URL,
    ORIENTAL_TRADING_CATEGORIES,
)


BLOCK_MARKERS = (
    "access denied",
    "captcha",
    "failed to get successful response",
    "pardon our interruption",
    "request blocked",
)


def _number(value: str | None) -> float | None:
    if not value:
        return None
    match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", value)
    return float(match.group(0).replace(",", "")) if match else None


def _integer(value: str | None) -> int | None:
    number = _number(value)
    return int(number) if number is not None else None


def _clean_url(value: str | None) -> str | None:
    if not value:
        return None
    absolute = urljoin(ORIENTAL_TRADING_BASE_URL, value)
    parts = urlsplit(absolute)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


class OrientaltradingListingSpider(BaseListingSpider):
    """Oriental Trading products from its first-party quick-view API only."""

    name = "orientaltrading_listing"
    allowed_domains = ["orientaltrading.com", "www.orientaltrading.com"]
    categories = ORIENTAL_TRADING_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_url", "item_id", "sku", "title", "url",
            "image_url", "image_urls", "price", "original_price", "currency",
            "quantity", "availability", "rating", "reviews_count", "brand",
            "product_category_id", "product_category_name", "badge", "description",
            "page", "position", "discovery_url", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        self.api_limit = int(kwargs.pop("api_limit", 0) or 0)
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()
        self._seen_pages: set[str] = set()

    def start_requests(self):
        url = self.resolve_target_url()
        yield scrapy.Request(
            url,
            callback=self.parse_listing,
            errback=self.on_error,
            meta={"category": self.category or "custom", "category_url": url, "page": 1},
            dont_filter=True,
        )

    def parse_listing(self, response):
        self._validate_response(response, "listing discovery")
        self._seen_pages.add(response.url)
        links = response.css("a.js_quickview[href*='productQuickView']::attr(href)").getall()
        if not links:
            raise CloseSpider(f"Oriental Trading exposed no quick-view API records: {response.url}")

        scheduled = 0
        for position, href in enumerate(links, start=1):
            query = dict(parse_qsl(urlsplit(href).query))
            sku = query.get("sku")
            if not sku or sku in self._seen_ids:
                continue
            if self.api_limit and scheduled >= self.api_limit:
                break
            self._seen_ids.add(sku)
            scheduled += 1
            yield scrapy.Request(
                response.urljoin(href),
                callback=self.parse_api,
                errback=self.on_error,
                headers={"Accept": "text/html, */*; q=0.01", "X-Requested-With": "XMLHttpRequest"},
                meta={
                    "category": response.meta["category"],
                    "category_url": response.meta["category_url"],
                    "discovery_url": response.url,
                    "page": response.meta["page"],
                    "position": position,
                    "sku": sku,
                },
                dont_filter=True,
            )

        if response.meta["page"] < self.max_pages:
            next_href = response.css('link[rel="next"]::attr(href), a[rel="next"]::attr(href)').get()
            if next_href:
                next_url = response.urljoin(next_href)
                if next_url not in self._seen_pages:
                    yield scrapy.Request(
                        next_url,
                        callback=self.parse_listing,
                        errback=self.on_error,
                        meta={**response.meta, "page": response.meta["page"] + 1},
                        dont_filter=True,
                    )

    def parse_api(self, response):
        self._validate_response(response, "quick-view API")
        root = response.css("#quickview_item")
        if not root:
            raise CloseSpider(f"Oriental Trading quick-view API record was absent: {response.url}")

        def hidden(name: str) -> str | None:
            return root.css(f'input[name="{name}"]::attr(value)').get()

        sku = root.attrib.get("data-sku") or hidden("sku") or response.meta["sku"]
        title = root.css("#pdp_main_item_details a.c_module_hover_text::text").get()
        product_url = root.css(
            '#pdp_main_item_details a.c_module_hover_text::attr(href), a[aria-label="See Product Details"]::attr(href)'
        ).get()
        images = list(dict.fromkeys(root.css(".c_sku_image img[data-src]::attr(data-src)").getall()))
        description = " ".join(root.css(".c_sku_description_trimmed ::text").getall()).strip() or None
        rating = _number(hidden("rating") or root.css(".c_rating::attr(title)").get())
        reviews_count = _integer(hidden("reviews") or root.css(".c_rating_count::text").get())
        price = _number(hidden("price") or root.css(".u_txtPrice ::text").get())
        original_match = re.search(r"item_was_price\s*=\s*([\d,.]+)", response.text)
        original_price = _number(original_match.group(1)) if original_match else None
        availability_code = hidden("stock_status")
        raw = {
            field: hidden(field)
            for field in (
                "sku", "name", "price", "stock_status", "rating", "reviews", "brand",
                "category_id", "category_name", "badge", "uom", "case", "item_type",
            )
            if hidden(field) is not None
        }
        yield {
            "category": response.meta["category"],
            "category_url": response.meta["category_url"],
            "item_id": sku,
            "sku": sku,
            "title": title.strip() if title else hidden("name"),
            "url": _clean_url(product_url),
            "image_url": images[0] if images else None,
            "image_urls": images,
            "price": price,
            "original_price": original_price if original_price != price else None,
            "currency": "USD",
            "quantity": hidden("uom") or hidden("case"),
            "availability": {"IN": "in_stock", "OUT": "out_of_stock"}.get(availability_code, availability_code),
            "rating": rating,
            "reviews_count": reviews_count,
            "brand": hidden("brand"),
            "product_category_id": hidden("category_id"),
            "product_category_name": hidden("category_name"),
            "badge": hidden("badge"),
            "description": description,
            "page": response.meta["page"],
            "position": response.meta["position"],
            "discovery_url": response.meta["discovery_url"],
            "source_url": response.url,
            "source": "orientaltrading_quick_view_api",
            "raw": raw,
            "timestamp": self.job_timestamp,
        }

    @staticmethod
    def _validate_response(response, leg: str):
        lowered = response.text.lower()
        if response.status != 200 or not response.body or any(marker in lowered for marker in BLOCK_MARKERS):
            raise CloseSpider(f"Oriental Trading {leg} failed ({response.status}): {response.url}")

    def on_error(self, failure):
        raise CloseSpider(f"Oriental Trading request failed: {failure.value}")
