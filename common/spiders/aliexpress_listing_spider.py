from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.aliexpress_categories import ALIEXPRESS_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


_INIT_DATA_RE = re.compile(r"window\._dida_config_\._init_data_\s*=\s*\{\s*data\s*:")


class AliexpressListingSpider(BaseListingSpider):
    """AliExpress product listings from the page's embedded search hydration."""

    name = "aliexpress_listing"
    allowed_domains = ["aliexpress.com", "aliexpress.us"]
    categories = ALIEXPRESS_CATEGORIES

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "product_id", "title", "url", "price", "original_price", "currency",
            "image_url", "rating", "orders", "category", "position", "page",
            "total_results", "source_url", "source", "timestamp",
        ],
    }

    def start_requests(self):
        target = self.resolve_target_url()
        category = self.category or "custom"
        entry = self.category_entry(category) if self.category else None
        category_name = entry.get("category_name") if entry else category
        yield self._page_request(target, 1, category_name)

    def _page_request(self, url: str, page: int, category: str):
        page_url = self._page_url(url, page)
        return scrapy.Request(
            page_url,
            callback=self.parse,
            headers={"Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-US,en;q=0.9"},
            meta={"page": page, "category": category, "listing_url": url},
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query) if key != "page"]
        if page > 1:
            query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @classmethod
    def _init_data(cls, response: scrapy.http.Response) -> dict[str, Any]:
        for script in response.xpath('//script[contains(text(), "init-data-start")]/text()').getall():
            match = _INIT_DATA_RE.search(script)
            if not match:
                continue
            start = script.find("{", match.end())
            end = cls._matching_brace(script, start)
            if end is None:
                continue
            try:
                payload = json.loads(script[start:end])
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
                return payload
        raise RuntimeError(f"AliExpress listing bootstrap state missing or invalid: {response.url}")

    @staticmethod
    def _matching_brace(text: str, start: int) -> int | None:
        depth = 0
        quoted = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '"':
                quoted = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return index + 1
        return None

    @staticmethod
    def _walk(value: Any):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from AliexpressListingSpider._walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from AliexpressListingSpider._walk(child)

    @classmethod
    def _products(cls, payload: dict[str, Any]) -> list[dict[str, Any]]:
        products = []
        seen = set()
        for value in cls._walk(payload.get("data")):
            if not isinstance(value.get("productId"), (str, int)):
                continue
            title = value.get("title")
            if not isinstance(title, dict) or not title.get("displayTitle"):
                continue
            product_id = str(value["productId"])
            if product_id not in seen:
                seen.add(product_id)
                products.append(value)
        return products

    @classmethod
    def _page_info(cls, payload: dict[str, Any]) -> dict[str, Any]:
        for value in cls._walk(payload.get("data")):
            if isinstance(value.get("pageInfo"), dict):
                return value["pageInfo"]
            if "totalResults" in value and "pageSize" in value:
                return value
        return {}

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"AliExpress returned HTTP {response.status}: {response.url}")
        payload = self._init_data(response)
        products = self._products(payload)
        if not products:
            raise RuntimeError(f"AliExpress bootstrap has no product records: {response.url}")

        page = int(response.meta["page"])
        category = response.meta["category"]
        page_info = self._page_info(payload)
        total = page_info.get("totalResults")
        for position, product in enumerate(products, start=1):
            prices = product.get("prices") or {}
            sale = prices.get("salePrice") or {}
            original = prices.get("originalPrice") or {}
            evaluation = product.get("evaluation") or product.get("rating") or {}
            trade = product.get("trade") or product.get("orders") or {}
            product_id = str(product["productId"])
            image = (product.get("image") or {}).get("imgUrl")
            product_url = product.get("productUrl") or product.get("url") or f"/item/{product_id}.html"
            yield {
                "product_id": product_id,
                "title": product["title"].get("displayTitle"),
                "url": urljoin("https://www.aliexpress.com", product_url),
                "price": sale.get("minPrice") or original.get("minPrice"),
                "original_price": original.get("minPrice"),
                "currency": sale.get("currencyCode") or original.get("currencyCode") or prices.get("currencySymbol"),
                "image_url": urljoin("https:", image) if image and image.startswith("//") else image,
                "rating": evaluation.get("starRating") if isinstance(evaluation, dict) else evaluation,
                "orders": trade.get("tradeDesc") if isinstance(trade, dict) else trade,
                "category": category,
                "position": position,
                "page": page,
                "total_results": total,
                "source_url": response.url,
                "source": "aliexpress_bootstrap",
                "timestamp": self.get_timestamp().isoformat(),
            }

        page_size = int(page_info.get("pageSize") or len(products))
        if page < self.max_pages and len(products) >= page_size and (total is None or page * page_size < int(total)):
            yield self._page_request(response.meta["listing_url"], page + 1, category)
