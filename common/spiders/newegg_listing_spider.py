from __future__ import annotations

"""Newegg listings parsed from the server-rendered hydration state."""

import json
import math
import re
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.newegg_categories import NEWEGG_LISTING_CATEGORIES


class NeweggListingSpider(BaseListingSpider):
    name = "newegg_listing"
    allowed_domains = ["newegg.com", "www.newegg.com"]
    # Direct url=/category_url= runs are supported, so opt out of the base class
    # category-only gate; resolve_target_url() still rejects a run with no target.
    require_category_arg = False

    # Complete department -> listing mapping loaded from the captured first-party
    # navigation tree in ``newegg_category_urls.json``.
    categories = NEWEGG_LISTING_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.25,
        # Let the explicit status checks in parse() run so non-2xx responses
        # surface the documented actionable errors.
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "model",
            "brand",
            "price",
            "original_price",
            "currency",
            "url",
            "image",
            "rating",
            "reviews_count",
            "seller",
            "in_stock",
            "shipping_charge",
            "ships_from",
            "category",
            "subcategory",
            "promotions",
            "tags",
            "page",
            "source",
            "raw",
            "timestamp",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
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
        url = self.resolve_target_url()
        yield self._page_request(url, page=1)

    def _page_request(self, url: str, page: int, page_size: int | None = None):
        return scrapy.Request(
            self._page_url(url, page),
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"listing_url": url, "page": page, "page_size": page_size},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        if page <= 1:
            return url
        parts = urlsplit(url)
        path = re.sub(r"/Page-\d+/?$", "", parts.path.rstrip("/"), flags=re.I)
        return urlunsplit((parts.scheme, parts.netloc, f"{path}/Page-{page}", parts.query, ""))

    @staticmethod
    def _extract_initial_state(text: str) -> dict:
        match = re.search(r"window\.__initialState__\s*=\s*", text)
        if not match:
            raise ValueError("missing window.__initialState__")
        decoder = json.JSONDecoder()
        try:
            state, _ = decoder.raw_decode(text[match.end() :].lstrip())
        except json.JSONDecodeError as exc:
            raise ValueError("invalid window.__initialState__ JSON") from exc
        if not isinstance(state, dict):
            raise ValueError("window.__initialState__ was not an object")
        return state

    def parse(self, response, listing_url: str, page: int, page_size: int | None = None):
        if response.status != 200:
            raise RuntimeError(f"Newegg listing returned HTTP {response.status}: {response.url}")
        try:
            state = self._extract_initial_state(response.text)
        except ValueError as exc:
            raise RuntimeError(f"Newegg hydration schema error at {response.url}: {exc}") from exc

        products = state.get("Products")
        if not isinstance(products, list):
            raise RuntimeError(f"Newegg hydration has no Products list: {response.url}")
        if not products:
            self.logger.info("Newegg listing page %s is empty; pagination stopped", page)
            return

        emitted = 0
        for product in products:
            item = self._product_item(product, listing_url, page)
            item_id = item.get("item_id")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield item

        if emitted == 0:
            self.logger.warning("Newegg page %s contained no new product IDs", page)

        total = state.get("TotalItemCount")
        # Recomputing the size from every response inflates last_page when the final
        # page is partial. Keep the first-page size (or an explicit page_size passed
        # down from the previous request) across callbacks.
        page_size = page_size or len(products)
        last_page = math.ceil(total / page_size) if isinstance(total, int) and page_size else page
        if page < self.max_pages and page < last_page:
            yield self._page_request(listing_url, page + 1, page_size)

    @staticmethod
    def _product_item(product: dict, listing_url: str, page: int) -> dict:
        cell = product.get("ItemCell") or {}
        description = cell.get("Description") or {}
        review = cell.get("Review") or {}
        manufacturer = cell.get("ItemManufactory") or {}
        seller = cell.get("Seller") or {}
        category = cell.get("Category") or {}
        subcategory = cell.get("Subcategory") or {}
        image_data = cell.get("Image") or {}
        image_name = (cell.get("NewImage") or {}).get("ImageName")
        patterns = image_data.get("ImagePathPattern") or []
        pattern = next((p.get("PathPattern") for p in patterns if p.get("Size") == 1280), None)
        pattern = pattern or next((p.get("PathPattern") for p in patterns if p.get("PathPattern")), None)
        image = pattern.replace("{ImageName}", image_name).replace("{Size}", "300") if pattern and image_name else None
        item_id = product.get("ProductNumber") or cell.get("Item")
        slug = description.get("UrlKeywords")
        url = f"https://www.newegg.com/{slug}/p/N82E168{item_id.replace('-', '')}" if slug and item_id else None
        return {
            "item_id": item_id,
            "title": description.get("Title"),
            "model": cell.get("Model"),
            "brand": manufacturer.get("Manufactory"),
            "price": cell.get("FinalPrice"),
            "original_price": cell.get("UnitCost"),
            "currency": "USD",
            "url": url,
            "image": image,
            "rating": review.get("RatingOneDecimal"),
            "reviews_count": review.get("HumanRating"),
            "seller": seller.get("SellerName") or "Newegg",
            "in_stock": cell.get("Instock"),
            "shipping_charge": cell.get("ShippingCharge"),
            "ships_from": cell.get("ShipFromCountryName"),
            "category": category.get("RealCategoryName"),
            "subcategory": subcategory.get("SubcategoryDescription"),
            "promotions": cell.get("PromotionInfo"),
            "tags": cell.get("CustomTags"),
            "page": page,
            "source": "newegg_initial_state",
            # Verbatim hydration-state entry so downstream consumers can re-derive
            # fields when the SSR schema changes.
            "raw": product,
        }
