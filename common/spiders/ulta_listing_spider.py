from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class UltaListingSpider(BaseListingSpider):
    """Ulta category listing spider.

    Examples:
    - scrapy crawl ulta_listing -a category='shampoo' -a max_pages=1
    """

    name = "ulta_listing"
    allowed_domains = ["ulta.com", "www.ulta.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "PROXY_KEEP_HEADERS": True,
    }

    categories = [
        {
            "category": "face",
            "url": "https://www.ulta.com/shop/makeup/face",
        },
    ]

    module_params = {
        "gti": "761dff0b-9c5c-411d-b508-3ee9f646e7cb",
        "loginStatus": "anonymous",
        "retailerVisitorId": "bff8c299-5cd1-4012-ae07-2c4ce39c6e45",
        "breakpoint": "XL",
    }
    CONTENT_ID = "cb7c0efb-8772-4abc-9be0-4dfaf1b625ee"
    GRAPHQL_URL = "https://www.ulta.com/dxl/graphql?ultasite=en-us"

    def start_requests(self):
        category_url = self.resolve_target_url()
        category_url = self._with_page(category_url, page=1)
        payload = self._build_payload(category_url)
        yield scrapy.Request(
            self.GRAPHQL_URL,
            method="POST",
            body=json.dumps(payload),
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=category_url),
            meta={
                "page": 1,
                "category_url": category_url,
            },
        )

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _build_payload(self, path: str) -> str:
        query = (
            "query NonCachedPage($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON) "
            "{ Page: NonCachedPage(stagingHost:$stagingHost, previewOptions:$previewOptions, "
            'moduleParams:$moduleParams, url: {path: "'
            + path
            + '"}, contentId: "'
            + self.CONTENT_ID
            + '") { content customResponseAttributes meta __typename } }'
        )
        variables = {"moduleParams": self.module_params}
        return {
            "query": query,
            "variables": variables,
            "operationName": "NonCachedPage",
        }

    def parse_listing(self, response: scrapy.http.Response):
        payload = response.json()
        content = payload.get("data", {}).get("Page", {}).get("content", {})
        items = content.get("items", []) or []
        for item in items:
            yield {
                **item,
                "category": self.category,
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages or not items:
            return

        next_page = current_page + 1
        category_url = self._with_page(
            response.meta.get("category_url") or self.resolve_target_url(),
            page=next_page,
        )
        payload = self._build_payload(category_url)
        yield scrapy.Request(
            self.GRAPHQL_URL,
            method="POST",
            body=json.dumps(payload),
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=category_url),
            meta=(
                {
                    "page": next_page,
                    "category_url": category_url,
                    "cookiejar": response.meta.get("cookiejar"),
                }
            ),
        )

    def _headers(
        self, operation: str | None = None, referer: str | None = None
    ) -> dict:
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
            "accept": "application/json,text/plain,*/*",
            "accept-language": "en-US,en;q=0.9",
            "apollographql-client-name": "ulta-graph",
            "content-type": "application/json",
            "x-forwarded-proto": "https",
            "x-ulta-client-channel": "web",
            "x-ulta-client-country": "US",
            "x-ulta-client-locale": "en-US",
            "x-ulta-dxl-query-id": operation,
            "x-ulta-graph-module-name": "ProductListingResults",
            "x-ulta-graph-type": "query",
            "x_ulta_site": "CB",
        }
        if referer:
            headers["Referer"] = referer
        return headers
