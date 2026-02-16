from __future__ import annotations

"""Ulta keyword search spider.

This is extracted from the previous `ulta_listing` spider behavior.

Usage:
  scrapy crawl ulta_search -a q=shampoo -a max_pages=2
"""

import json
from urllib.parse import urlencode

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider


class UltaSearchSpider(BaseSearchSpider):
    """Ulta search spider using Ulta's GraphQL APIs (/dxl/graphql)."""

    name = "ulta_search"
    allowed_domains = ["ulta.com", "www.ulta.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages)
        self.q = self.args.q or "shampoo"
        self.max_pages = self.args.max_pages
        self.base_path = f"https://www.ulta.com/search?search={self.q.replace(' ', '+')}"

        # Discovered from the site runtime behavior.
        self.module_params = {
            "gti": "4c5ae407-6d39-4bc2-8b88-c3c73b90c19c",
            "loginStatus": "anonymous",
            "retailerVisitorId": "bff8c299-5cd1-4012-ae07-2c4ce39c6e45",
            "breakpoint": "LG",
        }

    def start_requests(self):
        page_query = (
            'query Page($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON, $url: JSON) '
            '{ Page: Page(stagingHost: $stagingHost, previewOptions: $previewOptions, '
            'moduleParams: $moduleParams, url: $url, deliveryKey: "SDK") '
            '{ content customResponseAttributes meta __typename } }'
        )
        variables = {"moduleParams": {}, "url": {"path": self.base_path}}
        url = self._build_graphql_get_url(page_query, "Page", variables)
        yield scrapy.Request(url, callback=self.parse_page_definition, headers=self._headers())

    def parse_page_definition(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        if not payload:
            self.logger.warning("Ulta Page query failed")
            return

        modules = payload.get("data", {}).get("Page", {}).get("content", {}).get("modules", [])

        content_id = None
        for m in modules:
            if isinstance(m, dict) and m.get("type") == "ProductListingResults":
                content_id = m.get("id")
                break

        if not content_id:
            self.logger.warning("Could not locate ProductListingResults contentId")
            return

        first_url = self._build_noncached_url(content_id=content_id, page=1)
        yield scrapy.Request(
            first_url,
            callback=self.parse_listing,
            headers=self._headers(),
            meta={"content_id": content_id, "page": 1},
        )

    def parse_listing(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        if not payload:
            self.logger.warning(
                "Ulta NonCachedPage query failed for page=%s", response.meta.get("page")
            )
            return

        content = payload.get("data", {}).get("Page", {}).get("content", {})
        items = content.get("items", []) or []

        for item in items:
            action = item.get("action") or {}
            rating_raw = item.get("rating")
            review_raw = item.get("reviewCount")

            yield {
                "item_id": item.get("productId"),
                "sku_id": item.get("skuId"),
                "brand": item.get("brandName"),
                "title": item.get("productName"),
                "url": action.get("url"),
                "image_url": self._extract_image_url(item),
                "list_price": item.get("listPrice"),
                "sale_price": item.get("salePrice"),
                "rating": self._to_float(rating_raw),
                "reviews_count": self._to_int(review_raw),
                "is_sponsored": bool(item.get("sponsored")),
                "source": "ulta_dxl_graphql",
                "mode": "keyword",
                "query": self.q,
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        if not items:
            return

        next_page = current_page + 1
        content_id = response.meta.get("content_id")
        next_url = self._build_noncached_url(content_id=content_id, page=next_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse_listing,
            headers=self._headers(),
            meta={"content_id": content_id, "page": next_page},
        )

    def _build_noncached_url(self, content_id: str, page: int) -> str:
        path = self.base_path if page == 1 else f"{self.base_path}&page={page}"

        query = (
            'query NonCachedPage($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON) '
            '{ Page: NonCachedPage(stagingHost:$stagingHost, previewOptions:$previewOptions, '
            'moduleParams:$moduleParams, url: {path: "'
            + path
            + '"}, contentId: "'
            + content_id
            + '") { content customResponseAttributes meta __typename } }'
        )

        variables = {"moduleParams": self.module_params}
        return self._build_graphql_get_url(query, "NonCachedPage", variables)

    def _build_graphql_get_url(self, query: str, operation_name: str, variables: dict) -> str:
        params = {
            "ultasite": "en-us",
            "user-agent": "gomez",
            "query": query,
            "operationName": operation_name,
            "variables": json.dumps(variables, separators=(",", ":")),
        }
        return f"https://www.ulta.com/dxl/graphql?{urlencode(params)}"

    def _headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0",
            "accept": "application/json,text/plain,*/*",
            "content-type": "application/json",
        }

    def _to_json(self, response: scrapy.http.Response) -> dict | None:
        try:
            return json.loads(response.text)
        except Exception:
            return None

    def _extract_image_url(self, item: dict) -> str | None:
        for key in ("image", "altImage"):
            img = item.get(key)
            if isinstance(img, dict):
                if img.get("imageUrl"):
                    return img.get("imageUrl")
            elif isinstance(img, str):
                return img
        return None

    def _to_float(self, value):
        try:
            return float(value)
        except Exception:
            return None

    def _to_int(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        try:
            return int(value)
        except Exception:
            return None
