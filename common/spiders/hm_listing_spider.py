from __future__ import annotations

"""H&M US listings from the server-rendered Next.js PLP hydration state."""

import json
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.hm_categories import HM_CATEGORIES


class HmListingSpider(BaseListingSpider):
    name = "hm_listing"
    allowed_domains = ["hm.com", "www2.hm.com"]
    require_category_arg = False
    categories = HM_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "title", "brand", "url",
            "image_url", "price", "regular_price", "currency", "color",
            "color_hex", "sizes", "availability", "product_category", "page",
            "category_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        if self.url or self.category_url or self.category:
            url = self.resolve_target_url()
            category = self.category or self._category_for_url(url)
            yield self._request(url, category=category, page=1, category_url=url)
            return
        for entry in self.categories:
            yield self._request(entry["url"], category=entry["category"], page=1, category_url=entry["url"])

    def _request(self, url: str, *, category: str, page: int, category_url: str):
        return scrapy.Request(
            url,
            callback=self.parse_listing,
            headers={"Accept": "text/html,application/xhtml+xml", "Referer": "https://www2.hm.com/en_us/index.html"},
            meta={"category": category, "page": page, "category_url": category_url},
        )

    def parse_listing(self, response, **kwargs):
        self._reject_response(response)
        page = int(response.meta.get("page", 1))
        category = response.meta["category"]
        category_url = response.meta["category_url"]
        data = self._product_listing_data(response)
        products = data.get("hits") or data.get("rawProductList") or []
        if not isinstance(products, list) or not products:
            raise RuntimeError(f"H&M hydration returned no products on page {page}: {response.url}")

        emitted = 0
        for product in products:
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("articleCode") or product.get("articleId") or product.get("id") or "")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(product, item_id=item_id, category=category, page=page, category_url=category_url)

        if emitted == 0:
            self.logger.warning("H&M page %s repeated all product IDs; stopping", page)
            return
        pagination = data.get("pagination") or {}
        total_pages = self._int(pagination.get("totalPages")) or page
        next_page = self._int(pagination.get("nextPageNum")) or page + 1
        if page >= self.max_pages or page >= total_pages or next_page <= page:
            return
        yield self._request(
            self._page_url(category_url, next_page),
            category=category,
            page=next_page,
            category_url=category_url,
        )

    def _item(self, product: dict[str, Any], *, item_id: str, category: str, page: int, category_url: str):
        prices = product.get("prices") or []
        prices = [p for p in prices if isinstance(p, dict)]
        current = next((p for p in prices if p.get("priceType") in {"redPrice", "salePrice"}), None)
        regular = next((p for p in prices if p.get("priceType") in {"whitePrice", "regularPrice"}), None)
        current = current or regular or (prices[0] if prices else {})
        color = product.get("productColor") or {}
        sizes = product.get("sizes") or []
        stock_values = [self._int(s.get("stock")) for s in sizes if isinstance(s, dict)]
        department = next((e.get("department") for e in self.categories if e["category"] == category), None)
        return {
            "category": category,
            "department": department,
            "item_id": item_id,
            "title": product.get("title") or product.get("name"),
            "brand": product.get("brandName") or "H&M",
            "url": urljoin("https://www2.hm.com", product.get("pdpUrl") or product.get("url") or ""),
            "image_url": product.get("imageProductSrc") or product.get("imageUrl"),
            "price": current.get("price") or current.get("minPrice"),
            "regular_price": (regular or {}).get("price") or (regular or {}).get("maxPrice"),
            "currency": current.get("currency") or "USD",
            "color": color.get("colorName") or product.get("colorName"),
            "color_hex": color.get("hexColor"),
            "sizes": sizes,
            "availability": "in_stock" if any(v and v > 0 for v in stock_values) else "out_of_stock",
            "product_category": product.get("category"),
            "page": page,
            "category_url": category_url,
            "source": "hm_next_data",
            "raw": product,
            "timestamp": self.job_timestamp,
        }

    @staticmethod
    def _product_listing_data(response) -> dict[str, Any]:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"H&M response is missing __NEXT_DATA__: {response.url}")
        try:
            node: Any = json.loads(raw)["props"]["pageProps"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"H&M returned malformed Next.js hydration: {response.url}") from exc
        stack = [node]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                candidate = value.get("productListingData")
                if isinstance(candidate, dict):
                    return candidate
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
        raise RuntimeError(f"H&M __NEXT_DATA__ is missing productListingData: {response.url}")

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _category_for_url(self, url: str) -> str:
        match = next((e["category"] for e in self.categories if e["url"] == url), None)
        return match or urlsplit(url).path.rsplit("/", 1)[-1].removesuffix(".html")

    @staticmethod
    def _int(value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _reject_response(response) -> None:
        text = response.text[:200000].lower()
        if response.status != 200 or "captcha" in text or "pardon the interruption" in text:
            raise RuntimeError(f"H&M challenge/error response ({response.status}): {response.url}")
