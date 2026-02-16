from __future__ import annotations

"""Home Depot keyword search spider.

Preferred approach: use the Apollo bootstrap objects embedded in the PLP HTML:
- window.__APOLLO_OPERATIONS
- window.__APOLLO_STATE__

In this environment, direct requests may sometimes return an anti-bot "Error Page"
without Apollo data. When Apollo bootstrap is present, we parse products from it.

Usage:
  scrapy crawl homedepot_search -a q=screwdriver -a max_pages=1
"""

import json
import re
from dataclasses import dataclass
from typing import Any

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider


@dataclass
class ApolloExtract:
    operations: dict[str, Any] | None
    state: dict[str, Any] | None


class HomeDepotSearchSpider(BaseSearchSpider):
    name = "homedepot_search"
    allowed_domains = ["homedepot.com", "www.homedepot.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
    }

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages)

    def start_requests(self):
        url = self._build_search_url(self.args.q or "")
        yield scrapy.Request(url, callback=self.parse, meta=self.maybe_proxy_meta({"page": 1, "original_url": url}))

    def parse(self, response: scrapy.http.Response):
        html = response.text or ""

        if self._is_error_page(html):
            self.logger.warning("HomeDepot returned error/bot page; no Apollo bootstrap found")
            return

        apollo = self._extract_apollo(html)
        if not apollo.state:
            self.logger.warning("HomeDepot page did not contain __APOLLO_STATE__")
            return

        yield from self._yield_products_from_apollo(
            apollo.state,
            mode="keyword",
            query=self.args.q,
            category_url=None,
            page=1,
        )

    @staticmethod
    def _build_search_url(q: str) -> str:
        # NCNI-5 seems commonly present on their search URLs.
        return f"https://www.homedepot.com/s/{q}?NCNI-5"

    @staticmethod
    def _is_error_page(html: str) -> bool:
        h = (html or "").lower()
        return "oops!! something went wrong" in h or "error page" in h and "homedepot" in h

    def _extract_apollo(self, html: str) -> ApolloExtract:
        ops = self._extract_js_object(html, "__APOLLO_OPERATIONS")
        state = self._extract_js_object(html, "__APOLLO_STATE__")
        return ApolloExtract(operations=ops, state=state)

    def _yield_products_from_apollo(
        self,
        state: dict[str, Any],
        *,
        mode: str,
        query: str | None,
        category_url: str | None,
        page: int,
    ):
        # Find the SearchModel root.
        search_model = None
        for k, v in state.items():
            if isinstance(v, dict) and v.get("__typename") == "SearchModel":
                search_model = v
                break

        if not search_model:
            self.logger.warning("No SearchModel found in __APOLLO_STATE__")
            return

        prod_key = None
        for k in search_model.keys():
            if isinstance(k, str) and k.startswith("products("):
                prod_key = k
                break

        if not prod_key:
            self.logger.warning("No products(...) key found under SearchModel")
            return

        refs = search_model.get(prod_key) or []
        if not isinstance(refs, list):
            self.logger.warning("Unexpected products(...) value type: %s", type(refs))
            return

        for r in refs:
            if not isinstance(r, dict) or "__ref" not in r:
                continue
            obj = state.get(r["__ref"]) or {}
            if not isinstance(obj, dict):
                continue

            identifiers = obj.get("identifiers") or {}
            pricing = None
            for k in obj.keys():
                if isinstance(k, str) and k.startswith("pricing("):
                    pricing = obj.get(k)
                    break

            media = obj.get("media") or {}
            image_url = None
            try:
                img = (media.get("images") or [None])[0] or {}
                image_url = (img.get("url") or "").replace("<SIZE>", "300") or None
            except Exception:
                image_url = None

            rating = None
            reviews_count = None
            rr = ((obj.get("reviews") or {}).get("ratingsReviews") or {})
            if rr:
                try:
                    rating = float(rr.get("averageRating")) if rr.get("averageRating") is not None else None
                except Exception:
                    rating = None
                try:
                    reviews_count = int(rr.get("totalReviews")) if rr.get("totalReviews") is not None else None
                except Exception:
                    reviews_count = None

            canonical = identifiers.get("canonicalUrl")
            url = f"https://www.homedepot.com{canonical}" if canonical else None

            yield {
                "item_id": identifiers.get("itemId") or obj.get("itemId"),
                "sku": identifiers.get("storeSkuNumber"),
                "brand": identifiers.get("brandName"),
                "title": identifiers.get("productLabel"),
                "model": identifiers.get("modelNumber"),
                "url": url,
                "image_url": image_url,
                "price": (pricing or {}).get("value") if isinstance(pricing, dict) else None,
                "original_price": (pricing or {}).get("original") if isinstance(pricing, dict) else None,
                "rating": rating,
                "reviews_count": reviews_count,
                "source": "homedepot_apollo_bootstrap",
                "mode": mode,
                "query": query,
                "category_url": category_url,
                "page": page,
            }

    @staticmethod
    def _extract_js_object(html: str, marker: str) -> dict[str, Any] | None:
        # Supports either:
        #   window.__MARKER__={...}
        #   __MARKER__={...}
        m = re.search(rf"(?:window\.)?{re.escape(marker)}\s*=\s*\{{", html)
        if not m:
            return None

        start = m.end() - 1  # points to the opening '{'
        obj_text = HomeDepotSearchSpider._extract_balanced_braces(html, start)
        if not obj_text:
            return None

        try:
            return json.loads(obj_text)
        except Exception:
            return None

    @staticmethod
    def _extract_balanced_braces(text: str, start_index: int) -> str | None:
        # Extract JSON object starting at start_index (which must be '{').
        if start_index < 0 or start_index >= len(text) or text[start_index] != "{":
            return None

        depth = 0
        in_str = False
        esc = False
        for i in range(start_index, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue

            if ch == '"':
                in_str = True
                continue

            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start_index : i + 1]

        return None
