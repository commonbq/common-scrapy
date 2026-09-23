from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.ulta_search_spider import UltaSearchSpider


class UltaListingSpider(BaseListingSpider):
    """Ulta category listing spider.

    Examples:
    - scrapy crawl ulta_listing -a category='makeup' -a max_pages=1
    """

    name = "ulta_listing"
    allowed_domains = ["ulta.com", "www.ulta.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "PROXY_KEEP_HEADERS": True,
        "FEED_EXPORT_FIELDS": [
            "category",
            "skuId",
            "action",
            "productId",
            "bookmarked",
            "image",
            "altImage",
            "bookmarkAccessibility",
            "addToBagAccessibility",
            "badge",
            "sponsored",
            "brandName",
            "productName",
            "priceLabel",
            "rating",
            "reviewCount",
            "listPrice",
            "salePrice",
            "discount",
            "promoText",
            "additionalOffersText",
            "reviewAccessibilityLabel",
            "variantLabel",
            "kitPrice",
            "formatOnLoadBeacon",
            "formatOnViewBeacon",
            "sponsoredBadgeLabel",
            "isLimitedStock",
            "productCardTags",
            "badgeTags",
            "dataCapture",
        ],
    }

    categories = [
        {
            "category": "makeup",
            "url": "https://www.ulta.com/shop/makeup/all",
        },
        {
            "category": "skin-care",
            "url": "https://www.ulta.com/shop/skin-care/all",
        },
        {
            "category": "hair-care",
            "url": "https://www.ulta.com/shop/hair/all",
        },
        {
            "category": "fragrance",
            "url": "https://www.ulta.com/shop/fragrance/all",
        },
        {
            "category": "body-care",
            "url": "https://www.ulta.com/shop/body-care/all",
        },
    ]

    GRAPHQL_URL = "https://www.ulta.com/dxl/graphql?ultasite=en-us"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products = set()

    async def start(self):
        for request in self.start_requests():
            yield request

    def start_requests(self):
        meta = {
            "page": 1,
            "category_url": self._with_page(self.resolve_target_url(), 1),
        }
        yield self._graphql_request(meta)

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query, keep_blank_values=True)
        qs.pop("page", None)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _graphql_request(self, meta, content_id=None):
        # Carry crawl state only. HttpProxyMiddleware strips credentials from
        # meta["proxy"]; copying that URL to a new request loses authentication.
        # Let the project middleware apply the configured proxy afresh.
        meta = {
            key: value
            for key, value in meta.items()
            if key
            in {"page", "category_url", "cookiejar", "content_id", "rediscovered"}
        }
        meta["dont_retry"] = True
        meta["dont_cache"] = True
        path = meta["category_url"]
        if content_id:
            meta["content_id"] = content_id
            payload = self._build_payload(path, content_id)
            callback = self.parse_listing
        else:
            meta.pop("content_id", None)
            payload = {
                "query": UltaSearchSpider._page_query(),
                "variables": {"moduleParams": {}, "url": {"path": path}},
                "operationName": "Page",
            }
            callback = self.parse_page_definition
        return scrapy.Request(
            self.GRAPHQL_URL,
            method="POST",
            body=json.dumps(payload),
            headers=self._headers(payload["operationName"], path),
            callback=callback,
            errback=self._request_failed,
            meta=meta,
            dont_filter=bool(meta.get("rediscovered")),
        )

    def _build_payload(self, path: str, content_id: str) -> dict:
        query = (
            "query NonCachedPage($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON) "
            "{ Page: NonCachedPage(stagingHost:$stagingHost, previewOptions:$previewOptions, "
            "moduleParams:$moduleParams, url: {path: "
            + json.dumps(path)
            + "}, contentId: "
            + json.dumps(content_id)
            + ") { content customResponseAttributes meta __typename } }"
        )
        return {
            "query": query,
            "variables": {
                "moduleParams": {"breakpoint": "XL", "loginStatus": "anonymous"}
            },
            "operationName": "NonCachedPage",
        }

    @staticmethod
    def _content(response):
        if response.status != 200:
            return None
        try:
            payload = json.loads(response.text)
            if payload.get("errors"):
                return None
            content = payload["data"]["Page"]["content"]
            return content if isinstance(content, dict) else None
        except (ValueError, KeyError, TypeError, AttributeError):
            return None

    @classmethod
    def _find_module(cls, node):
        if isinstance(node, dict):
            if (
                node.get("type") == "ProductListingResults"
                and isinstance(node.get("id"), str)
                and node["id"]
            ):
                return node["id"]
            children = node.values()
        elif isinstance(node, list):
            children = node
        else:
            return None
        for child in children:
            content_id = cls._find_module(child)
            if content_id:
                return content_id
        return None

    def parse_page_definition(self, response):
        content_id = self._find_module(self._content(response))
        if not content_id:
            self.logger.warning(
                "Ulta module discovery failed (status=%s)", response.status
            )
            return
        yield self._graphql_request(response.meta, content_id)

    def parse_listing(self, response):
        content = self._content(response)
        items = content.get("items") if content is not None else None
        if not isinstance(items, list):
            self.logger.warning(
                "Ulta listing response invalid (status=%s)", response.status
            )
            return
        items = [item for item in items if isinstance(item, dict)]
        page = response.meta["page"]
        if not items:
            if page == 1 and not response.meta.get("rediscovered"):
                yield self._graphql_request({**response.meta, "rediscovered": True})
            else:
                self.logger.info("Ulta listing exhausted (page=%s)", page)
            return
        yielded = False
        for item in items:
            action = item.get("action") or {}
            url = action.get("url") if isinstance(action, dict) else None
            key = item.get("skuId") or item.get("productId") or url
            if key and key in self._seen_products:
                continue
            if key:
                self._seen_products.add(key)
            yielded = True
            yield {**item, "category": self.category}
        if yielded and page < self.max_pages:
            meta = {
                **response.meta,
                "page": page + 1,
                "category_url": self._with_page(
                    response.meta["category_url"], page + 1
                ),
            }
            yield self._graphql_request(meta, response.meta["content_id"])

    def _request_failed(self, failure):
        self.logger.warning("Ulta request failed: %s", failure.type.__name__)

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
