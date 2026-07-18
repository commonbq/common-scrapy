from __future__ import annotations

import json

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class PoshmarkListingSpider(BaseListingSpider):
    """Poshmark listing spider via inline bootstrap state (window.__INITIAL_STATE__)."""

    name = "poshmark_listing"
    allowed_domains = ["poshmark.com", "www.poshmark.com"]

    categories = [
        {"category": "women", "url": "https://poshmark.com/category/Women"},
        {"category": "men", "url": "https://poshmark.com/category/Men"},
        {"category": "kids", "url": "https://poshmark.com/category/Kids"},
        {"category": "home", "url": "https://poshmark.com/category/Home"},
        {"category": "electronics", "url": "https://poshmark.com/category/Electronics"},
        {"category": "pets", "url": "https://poshmark.com/category/Pets"},
    ]

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
            item_id = p.get("id")
            listing_url = f"https://poshmark.com/listing/{(p.get('title') or '').replace(' ', '-')}-{item_id}" if item_id else None
            price = (p.get("price_amount") or {}).get("val")
            original_price = (p.get("original_price_amount") or {}).get("val")
            cover = p.get("cover_shot") or {}
            yield {
                "category": current_category,
                "item_id": item_id,
                "title": p.get("title"),
                "brand": p.get("brand"),
                "url": listing_url,
                "image_url": cover.get("url_large") or cover.get("url") or cover.get("url_small"),
                "price": self._to_float(price),
                "original_price": self._to_float(original_price),
                "currency": (p.get("price_amount") or {}).get("currency_code"),
                "size": p.get("size"),
                "source": "poshmark_bootstrap_initial_state",
                "mode": "category_bootstrap",
                "category_url": response.url,
                "page": 1,
            }

    def _extract_initial_state(self, html: str) -> dict | None:
        needle = "window.__INITIAL_STATE__="
        i = html.find(needle)
        if i < 0:
            return None

        start = html.find("{", i)
        if start < 0:
            return None

        level = 0
        in_string = False
        escape = False
        end = None
        for idx, ch in enumerate(html[start:], start):
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue

            if ch == '"':
                in_string = True
            elif ch == "{":
                level += 1
            elif ch == "}":
                level -= 1
                if level == 0:
                    end = idx + 1
                    break

        if not end:
            return None

        try:
            data = json.loads(html[start:end])
            return data if isinstance(data, dict) else None
        except Exception:
            self.logger.exception("Failed parsing window.__INITIAL_STATE__ JSON")
            return None

    @staticmethod
    def _extract_products(state: dict) -> list[dict]:
        try:
            data = (((state.get("$_category") or {}).get("gridData") or {}).get("data") or [])
            return [x for x in data if isinstance(x, dict)]
        except Exception:
            return []

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _to_float(value):
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None
