from __future__ import annotations

"""Tokopedia product listings from its first-party SearchProductV5 GraphQL API."""

import json
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.tokopedia_categories import TOKOPEDIA_CATEGORIES

API_URL = "https://gql.tokopedia.com/graphql/SearchProductV5Query"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
QUERY = """query SearchProductV5Query($params: String!) {
  searchProductV5(params: $params) {
    header { totalData responseCode }
    data { totalDataText products {
      id name url price { text number original discountPercentage }
      shop { name city tier }
      category { name breadcrumb }
      rating freeShipping { url }
      labelGroups { position title }
    } }
  }
}"""


class TokopediaListingSpider(BaseListingSpider):
    name = "tokopedia_listing"
    allowed_domains = ["tokopedia.com", "gql.tokopedia.com"]
    categories = TOKOPEDIA_CATEGORIES
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "category_id", "item_id", "title",
            "url", "price", "original_price", "discount_percent", "currency",
            "rating", "shop_name", "shop_city", "shop_tier", "category_name",
            "category_breadcrumb", "free_shipping", "sold_count_display",
            "page", "position", "total_count", "source_url", "source", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    async def start(self):
        if self.url or self.category_url:
            target = self.url or self.category_url
            entry = {"url": target, "category_id": "", "category": self.category or "custom", "group": None}
        else:
            entry = self.category_entry(self.category)
            if not entry:
                raise ValueError(f"Unknown Tokopedia category {self.category!r}")
        yield scrapy.Request(
            entry["url"], callback=self._bootstrap, errback=self._request_failed,
            meta={"category_entry": entry},
            headers={"User-Agent": USER_AGENT, "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8"},
        )

    def _bootstrap(self, response):
        if response.status != 200:
            raise RuntimeError(f"Tokopedia category bootstrap returned HTTP {response.status}: {response.url}")
        entry = response.meta["category_entry"]
        category_id = entry.get("category_id")
        if not category_id:
            raise RuntimeError("Tokopedia category has no verified category id")
        yield self._api_request(entry, category_id, page=1)

    def _api_request(self, entry, category_id: str, page: int):
        params = urlencode({
            "device": "desktop", "l_name": "sre", "ob": "23", "page": str(page),
            "q": "sepatu", "rows": "60", "safe_search": "false",
            "sc": category_id, "source": "search", "st": "product",
            "start": str((page - 1) * 60),
        })
        body = [{
            "operationName": "SearchProductV5Query",
            "variables": {"params": params},
            "query": QUERY,
        }]
        yield_request = scrapy.Request(
            API_URL, method="POST", body=json.dumps(body), callback=self.parse_api,
            errback=self._request_failed, dont_filter=True,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Origin": "https://www.tokopedia.com",
                "Referer": entry["url"],
                "x-source": "tokopedia-lite",
                "x-tkpd-lite-service": "zeus",
                "x-device": "desktop-0.0",
                "x-version": "844d199",
            },
            meta={"entry": entry, "category_id": category_id, "page": page},
        )
        return yield_request

    def parse_api(self, response):
        if response.status != 200:
            raise RuntimeError(f"Tokopedia SearchProductV5 API returned HTTP {response.status}: {response.text[:250]}")
        try:
            payload = response.json()
            result = payload[0]["data"]["searchProductV5"]
            products = result["data"]["products"]
            header = result.get("header") or {}
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Tokopedia SearchProductV5 returned an unexpected response: {response.text[:500]}") from exc
        if not isinstance(products, list) or not products:
            raise RuntimeError(f"Tokopedia SearchProductV5 returned no products for category {response.meta['category_id']}")

        entry = response.meta["entry"]
        page = response.meta["page"]
        try:
            total_count = int(header.get("totalData"))
        except (ValueError, TypeError):
            total_count = None
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("id") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            price = product.get("price") or {}
            shop = product.get("shop") or {}
            category = product.get("category") or {}
            sold = next((label.get("title") for label in product.get("labelGroups", [])
                         if label.get("position") == "ri_product_credibility"), None)
            yield {
                "category": entry.get("category"), "department": entry.get("group"),
                "category_id": response.meta["category_id"], "item_id": item_id,
                "title": product.get("name"), "url": product.get("url"),
                "price": price.get("number"), "original_price": price.get("original"),
                "discount_percent": price.get("discountPercentage"), "currency": "IDR",
                "rating": product.get("rating"), "shop_name": shop.get("name"),
                "shop_city": shop.get("city"), "shop_tier": shop.get("tier"),
                "category_name": category.get("name"),
                "category_breadcrumb": category.get("breadcrumb"),
                "free_shipping": bool((product.get("freeShipping") or {}).get("url")),
                "sold_count_display": sold, "page": page, "position": position,
                "total_count": total_count, "source_url": response.url,
                "source": "tokopedia_search_product_v5", "raw": product,
            }

        if total_count and page < min((total_count + 59) // 60, 5) and page < self.max_pages:
            yield self._api_request(entry, response.meta["category_id"], page + 1)

    def _request_failed(self, failure):
        raise RuntimeError(f"Tokopedia request failed: {failure.value}")
