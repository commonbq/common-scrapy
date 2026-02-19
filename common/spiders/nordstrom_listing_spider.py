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

    handle_httpstatus_all = True

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
    }

    categories = [
        {"category": "women", "url": "https://www.nordstrom.com/browse/women"},
        {"category": "men", "url": "https://www.nordstrom.com/browse/men"},
        {"category": "kids", "url": "https://www.nordstrom.com/browse/kids"},
        {"category": "beauty", "url": "https://www.nordstrom.com/browse/beauty"},
        {"category": "home", "url": "https://www.nordstrom.com/browse/home"},
        {"category": "designer", "url": "https://www.nordstrom.com/browse/designer"},
        {"category": "sale", "url": "https://www.nordstrom.com/browse/sale"},
    ]

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

        if "istlWasHere" in text or "We've noticed some unusual activity" in text:
            self.logger.warning(
                "Nordstrom returned anti-bot wrapper HTML (%s). len=%s proxy=%s",
                response.status,
                len(text),
                bool(response.meta.get("proxy")),
            )
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
        # 1) Nordstrom SSR blob used by current site: window.__INITIAL_CONFIG__ = {...}
        m_init = re.search(r"window\.__INITIAL_CONFIG__\s*=\s*(\{.*?\})\s*</script>", html, re.S | re.I)
        if m_init:
            try:
                initial_config = json.loads(m_init.group(1))
                products = self._products_from_nordstrom_initial_config(initial_config, category=category)
                if products:
                    return products
            except Exception:
                self.logger.exception("Failed parsing window.__INITIAL_CONFIG__ JSON")

        # 2) Next.js fallback
        m_next = re.search(r"<script[^>]+id=\"__NEXT_DATA__\"[^>]*>(?P<data>.*?)</script>", html, re.S | re.I)
        if m_next:
            blob = m_next.group("data").strip()
            try:
                data = json.loads(blob)
                products = self._products_from_next_data(data, category=category)
                if products:
                    return products
            except Exception:
                self.logger.exception("Failed parsing __NEXT_DATA__ JSON")

        # 3) Generic large-inline-state fallback
        scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(?P<body>.*?)</script>", html, re.S | re.I)
        for body in sorted(scripts, key=len, reverse=True)[:4]:
            if "products" not in body and "product" not in body and "productResults" not in body:
                continue
            m2 = re.search(r"=\s*(\{.*\})\s*;?\s*$", body.strip(), re.S)
            if not m2:
                continue
            try:
                data = json.loads(m2.group(1))
            except Exception:
                continue
            products = self._products_from_generic_state(data, category=category)
            if products:
                return products

        return []

    def _products_from_nordstrom_initial_config(self, data: dict, *, category: str | None = None) -> list[dict]:
        product_results = (data or {}).get("productResults") or {}
        products_by_id = product_results.get("productsById")
        if not isinstance(products_by_id, dict) or not products_by_id:
            return []

        out = []
        for product in products_by_id.values():
            if not isinstance(product, dict):
                continue
            out.append(self._normalize_product(product, category=category))
        return out

    def _products_from_next_data(self, data: dict, *, category: str | None = None) -> list[dict]:
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
            and (
                "price" in keys
                or "prices" in keys
                or "priceRange" in keys
                or "salePrice" in keys
                or "productPageUrl" in keys
            )
        ) or ("productId" in keys and ("name" in keys or "productName" in keys))

    def _normalize_product(self, p: dict, *, category: str | None = None) -> dict:
        name = p.get("name") or p.get("productName") or p.get("title")
        product_id = p.get("productId") or p.get("id") or p.get("sku") or p.get("styleNumber")
        url = p.get("url") or p.get("productUrl") or p.get("canonicalUrl") or p.get("productPageUrl")
        if url and url.startswith("//"):
            url = "https:" + url
        if url and url.startswith("/"):
            url = "https://www.nordstrom.com" + url

        price = p.get("price")
        if isinstance(price, dict):
            price = self._extract_price_from_nordstrom_price_obj(price)
        if price is None:
            price = p.get("salePrice") or p.get("currentPrice") or p.get("priceRange")

        image = p.get("image") or p.get("imageUrl") or p.get("primaryImage")
        if isinstance(image, dict):
            image = image.get("url") or image.get("src")
        if image is None and isinstance(p.get("mediaById"), dict) and p.get("mediaById"):
            first_media = next(iter(p["mediaById"].values()))
            if isinstance(first_media, dict):
                image = first_media.get("src") or first_media.get("url")

        return {
            "category": category,
            "product_id": product_id,
            "name": name,
            "brand": p.get("brandName") or p.get("brand"),
            "price": price,
            "url": url,
            "image": image,
            "rating": p.get("reviewStarRating") or p.get("rating"),
            "reviews_count": p.get("reviewCount") or p.get("reviews_count"),
            "raw": p,
        }

    def _extract_price_from_nordstrom_price_obj(self, price_obj: dict):
        # Nordstrom uses money objects: {units, nanos}. Prefer sale min if available, then total min.
        def money_to_float(m):
            if not isinstance(m, dict):
                return None
            units = m.get("units")
            nanos = m.get("nanos", 0)
            if units is None:
                return None
            try:
                return float(units) + (float(nanos) / 1_000_000_000)
            except Exception:
                return None

        for path in [
            ("salePriceRange", "min"),
            ("totalPriceRange", "min"),
            ("regularPriceRange", "min"),
        ]:
            node = price_obj
            for key in path:
                node = node.get(key) if isinstance(node, dict) else None
            val = money_to_float(node)
            if val is not None:
                return val

        direct = money_to_float(price_obj)
        if direct is not None:
            return direct

        amount = price_obj.get("amount") if isinstance(price_obj, dict) else None
        try:
            return float(amount) if amount is not None else None
        except Exception:
            return None
