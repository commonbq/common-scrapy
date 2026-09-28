from __future__ import annotations

import ast
import json
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class KrogerListingSpider(BaseListingSpider):
    """Extract Kroger category listings from the server-rendered Redux state."""

    name = "kroger_listing"
    allowed_domains = ["kroger.com", "www.kroger.com", "127.0.0.1"]

    categories = [
        {"category": "cereal", "url": "https://www.kroger.com/pl/cereal/09002"},
        {"category": "bread", "url": "https://www.kroger.com/pl/bread/03001"},
        {"category": "coffee", "url": "https://www.kroger.com/pl/coffee/11005"},
        {"category": "eggs", "url": "https://www.kroger.com/pl/eggs/02008"},
        {"category": "milk", "url": "https://www.kroger.com/pl/milk/02001"},
        {"category": "snacks", "url": "https://www.kroger.com/pl/snacks/12009"},
    ]

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image_url",
            "price", "regular_price", "currency", "availability", "size",
            "source", "category_url", "page", "raw",
        ]
    }

    _state_pattern = re.compile(
        r"window\.__INITIAL_STATE__\s*=\s*JSON\.parse\('(?P<payload>.*?)'\)\s*;?",
        re.DOTALL,
    )

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield scrapy.Request(
            self._with_page(target_url, 1),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        state = self._extract_initial_state(response.text)
        if state is None:
            raise RuntimeError(f"No Kroger __INITIAL_STATE__ JSON found at {response.url}")

        search_all = state.get("search", {}).get("searchAll", {})
        search_response = search_all.get("response") or {}
        products = search_response.get("products") or []
        if not products:
            raise RuntimeError(f"No Kroger Redux search products found at {response.url}")

        category = response.meta.get("category")
        page = int(response.meta.get("page") or 1)
        seen = set()
        for product in products:
            if not isinstance(product, dict):
                continue
            item_id = product.get("upc") or product.get("id")
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            price_data = product.get("price") or {}
            regular_price = self._number(price_data.get("regular") or product.get("regularPrice"))
            promo_price = self._number(price_data.get("promo") or product.get("promoPrice"))
            product_url = product.get("url") or product.get("productUrl")
            if product_url and product_url.startswith("/"):
                product_url = f"https://www.kroger.com{product_url}"
            images = product.get("images") or []
            image_url = product.get("imageUrl")
            if not image_url and images:
                first_image = images[0]
                image_url = first_image.get("url") if isinstance(first_image, dict) else first_image
            yield {
                "category": category,
                "item_id": item_id,
                "title": product.get("description") or product.get("name"),
                "brand": product.get("brand"),
                "url": product_url,
                "image_url": image_url,
                "price": promo_price if promo_price is not None else regular_price,
                "regular_price": regular_price,
                "currency": price_data.get("currency") or product.get("currency") or "USD",
                "availability": product.get("availability") or ("InStock" if product.get("available", True) else "OutOfStock"),
                "size": product.get("size"),
                "source": "kroger_initial_state_search_products",
                "category_url": self.resolve_target_url(),
                "page": page,
                "raw": product,
            }

        product_info = search_response.get("productsInfo") or {}
        total = int(product_info.get("totalCount") or len(products))
        page_size = int(search_all.get("requestVars", {}).get("pageSize") or len(products))
        if page_size and page * page_size < total and page < self.max_pages and not self.url:
            next_page = page + 1
            yield scrapy.Request(
                self._with_page(self.resolve_target_url(), next_page),
                callback=self.parse,
                headers=self._headers(),
                meta={"category": category, "page": next_page},
            )

    @classmethod
    def _extract_initial_state(cls, html: str) -> dict | None:
        match = cls._state_pattern.search(html or "")
        if not match:
            return None
        decoded = ast.literal_eval("'" + match.group("payload") + "'")
        state = json.loads(decoded)
        return state if isinstance(state, dict) else None

    @staticmethod
    def _number(value):
        if isinstance(value, dict):
            value = value.get("value") or value.get("amount")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    @staticmethod
    def _headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
