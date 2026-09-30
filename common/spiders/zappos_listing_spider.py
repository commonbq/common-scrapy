from __future__ import annotations

import html
import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.zappos_categories import ZAPPOS_CATEGORIES


class ZapposListingSpider(BaseListingSpider):
    """Zappos listings from the server-rendered Redux hydration state."""

    name = "zappos_listing"
    allowed_domains = ["zappos.com", "www.zappos.com", "localhost", "127.0.0.1"]
    categories = ZAPPOS_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "style_id", "title", "brand",
            "color", "url", "image_url", "price", "original_price", "currency",
            "rating", "reviews_count", "on_sale", "page", "position",
            "total_count", "source_url", "source", "raw",
        ],
    }

    _assignment = re.compile(r"window\.__INITIAL_STATE__\s*=\s*", re.DOTALL)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
            },
            meta={"category": self.category or "custom", "department": selected.get("department"), "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Zappos listing returned HTTP {response.status}: {response.url}")
        state = self._extract_initial_state(response.text)
        if state is None:
            raise RuntimeError(f"No valid Zappos window.__INITIAL_STATE__ object found at {response.url}")
        products_state = state.get("products")
        products = products_state.get("list") if isinstance(products_state, dict) else None
        if not isinstance(products, list):
            raise RuntimeError(f"Zappos initial state has no list-valued products.list at {response.url}")

        page = int(response.meta.get("page", 1))
        total_count = self._integer(products_state.get("totalProductCount"))
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("productId") or "") or None
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, response, page, position, total_count)

        next_href = response.css('link[rel="next"]::attr(href)').get()
        if next_href and page < self.max_pages:
            yield response.follow(
                next_href,
                callback=self.parse,
                headers=response.request.headers,
                meta={**response.meta, "page": page + 1},
            )

    def _item(self, product: dict, response, page: int, position: int, total_count: int | None) -> dict:
        price = self._money(product.get("price"))
        original_price = self._money(product.get("originalPrice"))
        product_url = product.get("productUrl") or product.get("productSeoUrl")
        image_url = product.get("thumbnailImageUrl")
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "item_id": str(product.get("productId")),
            "style_id": str(product.get("styleId")) if product.get("styleId") is not None else None,
            "title": html.unescape(str(product.get("productName") or "")) or None,
            "brand": html.unescape(str(product.get("brandName") or "")) or None,
            "color": html.unescape(str(product.get("color") or "")) or None,
            "url": urljoin(response.url, product_url) if product_url else None,
            "image_url": urljoin(response.url, image_url) if image_url else None,
            "price": price,
            "original_price": original_price,
            "currency": "USD" if price is not None or original_price is not None else None,
            "rating": self._number(product.get("reviewRating")),
            "reviews_count": self._integer(product.get("reviewCount")),
            "on_sale": self._boolean(product.get("onSale")),
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "zappos_initial_state_products",
            "raw": product,
        }

    @classmethod
    def _extract_initial_state(cls, document: str) -> dict | None:
        match = cls._assignment.search(document or "")
        if not match:
            return None
        try:
            state, _ = json.JSONDecoder().raw_decode(document, match.end())
        except (TypeError, ValueError):
            return None
        return state if isinstance(state, dict) else None

    @staticmethod
    def _money(value):
        match = re.search(r"[0-9][0-9,]*(?:\.\d+)?", str(value or ""))
        return float(match.group(0).replace(",", "")) if match else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _boolean(value):
        if isinstance(value, bool):
            return value
        return str(value).lower() == "true"
