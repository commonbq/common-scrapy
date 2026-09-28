from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class LululemonListingSpider(BaseListingSpider):
    """Extract Lululemon listings from the Next.js dehydrated query state."""

    name = "lululemon_listing"
    allowed_domains = ["shop.lululemon.com", "lululemon.com", "127.0.0.1"]

    categories = [
        {"category": "women", "url": "https://shop.lululemon.com/c/womens-clothes/_/N-7z5"},
        {"category": "women-leggings", "url": "https://shop.lululemon.com/c/womens-leggings/_/N-8r6"},
        {"category": "women-tops", "url": "https://shop.lululemon.com/c/womens-tops/_/N-1z0xsl3"},
        {"category": "women-shorts", "url": "https://shop.lululemon.com/c/women-shorts/_/N-7we"},
        {"category": "men", "url": "https://shop.lululemon.com/c/men/_/N-1z13zi2"},
        {"category": "men-pants", "url": "https://shop.lululemon.com/c/men-pants/_/N-7ub"},
        {"category": "men-shirts", "url": "https://shop.lululemon.com/c/men-tops/_/N-1z0xl9f"},
        {"category": "men-shorts", "url": "https://shop.lululemon.com/c/men-shorts/_/N-7u7"},
        {"category": "bags", "url": "https://shop.lululemon.com/c/bags/_/N-1z0xl1c"},
        {"category": "accessories", "url": "https://shop.lululemon.com/c/accessories/_/N-8a4"},
        {"category": "shoes", "url": "https://shop.lululemon.com/c/shoes/_/N-1z0xss0"},
        {"category": "we-made-too-much", "url": "https://shop.lululemon.com/c/sale/_/N-1z0xcmk"},
    ]

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category",
            "item_id",
            "title",
            "brand",
            "url",
            "image_url",
            "price",
            "original_price",
            "currency",
            "availability",
            "color_count",
            "source",
            "category_url",
            "page",
            "raw",
        ]
    }

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield scrapy.Request(
            self._with_page(target_url, 1),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        data = response.css("script#__NEXT_DATA__::text").get()
        if not data:
            raise RuntimeError(f"No Lululemon __NEXT_DATA__ found at {response.url}")
        category_data = self._extract_category_data(json.loads(data))
        pages = category_data.get("pages") if category_data else None
        page_data = pages[0] if pages and isinstance(pages[0], dict) else {}
        products = page_data.get("products") or []
        if not products:
            raise RuntimeError(f"No Lululemon CategoryPageDataQuery products found at {response.url}")

        category = response.meta.get("category")
        page = int(page_data.get("currentPage") or response.meta.get("page") or 1)
        for product in products:
            if not isinstance(product, dict):
                continue
            swatches = [value for value in product.get("swatches") or [] if isinstance(value, dict)]
            product_url = product.get("pdpUrl")
            if product_url and product_url.startswith("/"):
                product_url = f"https://shop.lululemon.com{product_url}"
            yield {
                "category": category,
                "item_id": product.get("productId") or product.get("repositoryId") or product.get("unifiedId"),
                "title": product.get("displayName"),
                "brand": "lululemon",
                "url": product_url,
                "image_url": (swatches[0].get("img") or swatches[0].get("swatch")) if swatches else None,
                "price": self._number(product.get("productSalePrice") or product.get("listPrice")),
                "original_price": self._number(product.get("listPrice")),
                "currency": product.get("currencyCode"),
                "availability": "InStock" if product.get("isInStock", True) else "OutOfStock",
                "color_count": len(swatches),
                "source": "next_data_category_page_query",
                "category_url": response.url,
                "page": page,
                "raw": product,
            }

        total_pages = int(page_data.get("totalProductPages") or 1)
        if page < min(total_pages, self.max_pages):
            next_page = page + 1
            yield scrapy.Request(
                self._with_page(response.url, next_page),
                callback=self.parse,
                headers=self._headers(),
                meta={"category": category, "page": next_page},
            )

    @staticmethod
    def _extract_category_data(data: dict) -> dict | None:
        queries = data.get("props", {}).get("pageProps", {}).get("dehydratedState", {}).get("queries", [])
        for query in queries:
            key = query.get("queryKey")
            if isinstance(key, list) and key and key[0] == "CategoryPageDataQuery":
                result = query.get("state", {}).get("data")
                return result if isinstance(result, dict) else None
        return None

    @staticmethod
    def _number(value):
        if isinstance(value, dict):
            value = value.get("amount") or value.get("value")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
