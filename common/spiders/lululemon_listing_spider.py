from __future__ import annotations

import json
import re
from typing import Iterable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class LululemonListingSpider(BaseListingSpider):
    """Lululemon listing spider using embedded Next.js bootstrap data.

    Extracts products from __NEXT_DATA__ -> dehydratedState -> CategoryPageDataQuery.
    Supports:
      -a category=<name>
      -a category_url=<url>
      -a url=<url>
      -a max_pages=<n>
    """

    name = "lululemon_listing"
    allowed_domains = ["shop.lululemon.com", "lululemon.com"]
    require_category_arg = False

    categories = [
        {"category": "women-shorts", "url": "https://shop.lululemon.com/c/women-shorts/n11ybt"},
        {"category": "women-leggings", "url": "https://shop.lululemon.com/c/women-leggings/n1udsq"},
        {"category": "men-shorts", "url": "https://shop.lululemon.com/c/men-shorts/n1u6m4"},
        {"category": "bags", "url": "https://shop.lululemon.com/c/bags/n1rdci"},
    ]

    def start_requests(self) -> Iterable[scrapy.Request]:
        if self.category or self.category_url or self.url:
            start_url = self.resolve_target_url()
            current_category = self.category or "custom"
        else:
            current_category = self.categories[0]["category"]
            start_url = self.categories[0]["url"]

        yield scrapy.Request(
            url=self._with_page(start_url, 1),
            headers=self._headers(),
            meta={"category": current_category, "page": 1},
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response):
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text, re.S)
        if not match:
            self.logger.warning("No __NEXT_DATA__ blob found: %s", response.url)
            return

        try:
            data = json.loads(match.group(1))
        except Exception:
            self.logger.exception("Failed to parse __NEXT_DATA__ JSON: %s", response.url)
            return

        category_data = self._extract_category_data(data)
        if not category_data:
            self.logger.warning("CategoryPageDataQuery not found: %s", response.url)
            return

        pages = category_data.get("pages") or []
        if not pages:
            return

        page_data = pages[0] if isinstance(pages[0], dict) else {}
        products = page_data.get("products") or []

        category = response.meta.get("category")
        for product in products:
            if not isinstance(product, dict):
                continue
            yield self._normalize_product(product, category=category)

        current_page = int(page_data.get("currentPage") or response.meta.get("page") or 1)
        total_pages = int(page_data.get("totalProductPages") or 1)
        if current_page < min(total_pages, self.max_pages):
            next_page = current_page + 1
            yield scrapy.Request(
                url=self._with_page(response.url, next_page),
                headers=self._headers(),
                meta={"category": category, "page": next_page},
                callback=self.parse,
                dont_filter=True,
            )

    def _extract_category_data(self, data: dict) -> dict | None:
        queries = (
            data.get("props", {})
            .get("pageProps", {})
            .get("dehydratedState", {})
            .get("queries", [])
        )
        for query in queries:
            key = query.get("queryKey")
            if isinstance(key, list) and key and key[0] == "CategoryPageDataQuery":
                return query.get("state", {}).get("data")
        return None

    def _normalize_product(self, product: dict, *, category: str | None) -> dict:
        pdp_url = product.get("pdpUrl")
        if isinstance(pdp_url, str) and pdp_url.startswith("/"):
            pdp_url = f"https://shop.lululemon.com{pdp_url}"

        image = None
        swatches = product.get("swatches")
        if isinstance(swatches, list) and swatches and isinstance(swatches[0], dict):
            image = swatches[0].get("img") or swatches[0].get("swatch")

        return {
            "category": category,
            "product_id": product.get("productId") or product.get("repositoryId") or product.get("unifiedId"),
            "name": product.get("displayName"),
            "brand": "lululemon",
            "price": product.get("productSalePrice") or product.get("listPrice"),
            "currency": product.get("currencyCode"),
            "url": pdp_url,
            "image": image,
            "raw": product,
        }

    def _headers(self) -> dict:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

    def _with_page(self, url: str, page: int) -> str:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))
