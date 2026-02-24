from __future__ import annotations

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class DillardsListingSpider(BaseListingSpider):
    """Dillard's listing spider via inline bootstrap state (window.__INITIAL_STATE__)."""

    name = "dillards_listing"
    allowed_domains = ["dillards.com", "www.dillards.com"]

    categories = [
        {"category": "women", "url": "https://www.dillards.com/c/women"},
        {"category": "men", "url": "https://www.dillards.com/c/men"},
        {"category": "shoes", "url": "https://www.dillards.com/c/shoes"},
        {"category": "handbags", "url": "https://www.dillards.com/c/handbags"},
        {"category": "beauty", "url": "https://www.dillards.com/c/beauty"},
        {"category": "juniors", "url": "https://www.dillards.com/c/juniors"},
        {"category": "home", "url": "https://www.dillards.com/c/home"},
    ]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
    }

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield scrapy.Request(
            target_url,
            callback=self.parse,
            meta={"target_url": target_url, "page": 1, "category": self.category},
            headers=self._headers(),
        )

    def parse(self, response: scrapy.http.Response):
        state = self._extract_initial_state(response.text)
        if not state:
            self.logger.warning("Unable to extract window.__INITIAL_STATE__ from %s", response.url)
            return

        products = self._extract_products(state)
        if not products:
            self.logger.warning("No products found in bootstrap state for %s", response.url)
            return

        current_category = response.meta.get("category")
        for p in products:
            yield {
                "category": current_category,
                "item_id": p.get("partNumber") or p.get("catentryId"),
                "title": p.get("name") or p.get("originalName"),
                "brand": p.get("brand"),
                "url": self._product_url(p),
                "image_url": p.get("fullImage") or p.get("thumbnail") or self._from_swatches(p),
                "price": self._to_float(((p.get("pricing") or {}).get("offerPriceMin"))),
                "price_max": self._to_float(((p.get("pricing") or {}).get("offerPriceMax"))),
                "original_price": self._to_float(((p.get("pricing") or {}).get("listPriceMin"))),
                "original_price_max": self._to_float(((p.get("pricing") or {}).get("listPriceMax"))),
                "rating": self._to_float(p.get("numStars")),
                "reviews_count": self._to_int(p.get("numReviews")),
                "source": "dillards_bootstrap_initial_state",
            }

    def _headers(self) -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

    def _extract_initial_state(self, html: str) -> dict | None:
        m = re.search(r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;\s*</script>", html, re.S | re.I)
        if not m:
            return None
        try:
            data = json.loads(m.group(1))
            return data if isinstance(data, dict) else None
        except Exception:
            self.logger.exception("Failed parsing window.__INITIAL_STATE__ JSON")
            return None

    def _extract_products(self, state: dict) -> list[dict]:
        # Fast path for current page shape.
        try:
            slots = state["contentData"]["layoutContent"]["slots"]
            for slot in slots.values():
                widgets = (slot or {}).get("widgets") or []
                for widget in widgets:
                    products = (widget or {}).get("products")
                    if isinstance(products, list) and products and isinstance(products[0], dict):
                        return products
        except Exception:
            pass

        # Fallback: recursive scan for lists that look like product arrays.
        found: list[dict] = []

        def walk(node):
            if isinstance(node, dict):
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                if node and isinstance(node[0], dict):
                    keys = set(node[0].keys())
                    if {"partNumber", "name", "pricing"}.issubset(keys) or {"catentryId", "name", "pricing"}.issubset(
                        keys
                    ):
                        found.extend([x for x in node if isinstance(x, dict)])
                        return
                for value in node:
                    walk(value)

        walk(state)
        return found

    def _product_url(self, product: dict) -> str | None:
        seo = product.get("seoURL") or product.get("productUrl")
        if isinstance(seo, str) and seo:
            if seo.startswith("http://") or seo.startswith("https://"):
                return seo
            return urljoin("https://www.dillards.com", seo)
        return None

    def _from_swatches(self, product: dict) -> str | None:
        swatches = product.get("swatches") or []
        if not isinstance(swatches, list) or not swatches:
            return None
        first = swatches[0] or {}
        if not isinstance(first, dict):
            return None
        return first.get("imgPath") or first.get("swatchImage")

    def _to_float(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None

    def _to_int(self, value):
        if value is None:
            return None
        try:
            return int(value)
        except Exception:
            return None
