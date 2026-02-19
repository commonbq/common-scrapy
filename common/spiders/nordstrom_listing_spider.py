from __future__ import annotations

import json
import re
from typing import Iterable

import scrapy

from common.settings import PROXY
from common.spiders.base_listing_spider import BaseListingSpider


class NordstromListingSpider(BaseListingSpider):
    """Nordstrom product listing spider.

    Supports listing-style category usage like other spiders:
    -a category=<name>
    -a category_url=<url>
    -a url=<url>

    Backward compatibility:
    -a keyword=<term> still works and maps to Nordstrom search URL.
    """

    name = "nordstrom_listing"
    allowed_domains = ["nordstrom.com", "www.nordstrom.com"]

    # We want to see proxy failures (ScraperAPI often returns 4xx/5xx).
    handle_httpstatus_all = True

    custom_settings = {
        # Keep it polite; Nordstrom is sensitive.
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
    }

    # Listing-style category map (same interface as other listing spiders).
    categories = [
        {"category": "women", "url": "https://www.nordstrom.com/browse/women"},
        {"category": "men", "url": "https://www.nordstrom.com/browse/men"},
        {"category": "kids", "url": "https://www.nordstrom.com/browse/kids"},
        {"category": "beauty", "url": "https://www.nordstrom.com/browse/beauty"},
        {"category": "home", "url": "https://www.nordstrom.com/browse/home"},
        {"category": "designer", "url": "https://www.nordstrom.com/browse/designer"},
        {"category": "sale", "url": "https://www.nordstrom.com/browse/sale"},
    ]

    # Allow url/category_url/keyword flows without forcing category argument.
    require_category_arg = False

    def start_requests(self) -> Iterable[scrapy.Request]:
        keyword = getattr(self, "keyword", None)

        current_category = None
        if self.category:
            current_category = self.category
            start_url = self.resolve_target_url()
        elif self.category_url:
            current_category = "category_url"
            start_url = self.category_url
        elif self.url:
            current_category = "custom_url"
            start_url = self.url
        elif keyword:
            current_category = "keyword"
            start_url = f"https://www.nordstrom.com/sr?keyword={keyword}"
        else:
            available = ", ".join(self.available_categories())
            raise ValueError(
                "Provide -a category=<name> (recommended), -a category_url=<url>, "
                "-a url=<category/search url>, or -a keyword=<term>. "
                f"Available categories: {available}"
            )

        yield self._make_request(start_url, dont_filter=True, category=current_category)

    def _make_request(
        self,
        url: str,
        *,
        dont_filter: bool = False,
        force_proxy: bool = False,
        category: str | None = None,
    ) -> scrapy.Request:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        meta = {"handle_httpstatus_all": True, "category": category}
        # Only use proxy when explicitly forced, to avoid unnecessary proxy usage.
        if force_proxy and PROXY:
            meta["proxy"] = PROXY

        return scrapy.Request(url, headers=headers, meta=meta, dont_filter=dont_filter)

    def parse(self, response: scrapy.http.Response):
        text = response.text or ""

        if response.status != 200:
            self.logger.warning(
                "Non-200 response. status=%s proxy=%s url=%s body_head=%r",
                response.status,
                bool(response.meta.get("proxy")),
                response.url,
                (text[:200] if text else ""),
            )

        # Detect common anti-bot wrapper content.
        if "istlWasHere" in text or "We've noticed some unusual activity" in text:
            self.logger.warning(
                "Nordstrom returned anti-bot wrapper HTML (%s). len=%s proxy=%s",
                response.status,
                len(text),
                bool(response.meta.get("proxy")),
            )
            # If we somehow got here without proxy, retry once with proxy.
            if PROXY and not response.meta.get("proxy"):
                yield self._make_request(
                    response.url,
                    dont_filter=True,
                    force_proxy=True,
                    category=response.meta.get("category"),
                )
                return

        current_category = response.meta.get("category")
        products = self._extract_products_from_html(text, category=current_category)
        if not products:
            self.logger.warning(
                "No embedded product data found in HTML. status=%s len=%s url=%s",
                response.status,
                len(text),
                response.url,
            )
            return

        for p in products:
            yield p

    def _extract_products_from_html(self, html: str, *, category: str | None = None) -> list[dict]:
        """Try a few common patterns for embedded listing data."""

        # 1) Next.js: <script id="__NEXT_DATA__" type="application/json">{...}</script>
        m = re.search(r"<script[^>]+id=\"__NEXT_DATA__\"[^>]*>(?P<data>.*?)</script>", html, re.S | re.I)
        if m:
            blob = m.group("data").strip()
            try:
                data = json.loads(blob)
                products = self._products_from_next_data(data, category=category)
                if products:
                    return products
            except Exception:
                self.logger.exception("Failed parsing __NEXT_DATA__ JSON")

        # 2) JSON in an inline script: try to find a big JSON object containing 'products' or 'productResults'.
        #    (This is heuristic; we keep it conservative to avoid false positives.)
        scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(?P<body>.*?)</script>", html, re.S | re.I)
        for body in sorted(scripts, key=len, reverse=True)[:3]:
            if "products" not in body and "product" not in body and "productResults" not in body:
                continue
            # Attempt to extract a JSON object assignment: window.__SOME__ = {...};
            m2 = re.search(r"=\s*(\{.*\})\s*;\s*$", body.strip(), re.S)
            if not m2:
                continue
            candidate = m2.group(1)
            try:
                data = json.loads(candidate)
            except Exception:
                continue
            products = self._products_from_generic_state(data, category=category)
            if products:
                return products

        return []

    def _products_from_next_data(self, data: dict, *, category: str | None = None) -> list[dict]:
        """Extract products from a Next.js __NEXT_DATA__ payload (site-specific; best-effort)."""
        found = []

        def walk(obj):
            if isinstance(obj, dict):
                if "products" in obj and isinstance(obj["products"], list):
                    for prod in obj["products"]:
                        if isinstance(prod, dict):
                            found.append(prod)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)

        walk(data)
        return [self._normalize_product(p, category=category) for p in found if self._looks_like_product(p)]

    def _products_from_generic_state(self, data: dict, *, category: str | None = None) -> list[dict]:
        found = []

        def walk(obj):
            if isinstance(obj, dict):
                if self._looks_like_product(obj):
                    found.append(obj)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)

        walk(data)
        # de-dupe by id/url if possible
        out = []
        seen = set()
        for p in found:
            norm = self._normalize_product(p, category=category)
            key = norm.get("product_id") or norm.get("url") or json.dumps(norm, sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            out.append(norm)
        return out

    def _looks_like_product(self, obj: dict) -> bool:
        keys = set(obj.keys())
        return (
            ("name" in keys or "productName" in keys or "title" in keys)
            and ("price" in keys or "prices" in keys or "priceRange" in keys or "salePrice" in keys)
        ) or ("productId" in keys and ("name" in keys or "productName" in keys))

    def _normalize_product(self, p: dict, *, category: str | None = None) -> dict:
        name = p.get("name") or p.get("productName") or p.get("title")
        product_id = p.get("productId") or p.get("id") or p.get("sku")
        url = p.get("url") or p.get("productUrl") or p.get("canonicalUrl")
        if url and url.startswith("//"):
            url = "https:" + url
        if url and url.startswith("/"):
            url = "https://www.nordstrom.com" + url

        price = p.get("price")
        if price is None:
            price = p.get("salePrice") or p.get("currentPrice") or p.get("priceRange")

        image = p.get("image") or p.get("imageUrl") or p.get("primaryImage")
        if isinstance(image, dict):
            image = image.get("url") or image.get("src")

        return {
            "category": category,
            "product_id": product_id,
            "name": name,
            "price": price,
            "url": url,
            "image": image,
            "raw": p,
        }
