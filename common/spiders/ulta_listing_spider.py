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
    }

    categories = [
        {"category": "shampoo", "url": "https://www.ulta.com/shop/hair/shampoo-conditioner/shampoo"},
        {"category": "conditioner", "url": "https://www.ulta.com/shop/hair/shampoo-conditioner/conditioner"},
        {"category": "cleanser", "url": "https://www.ulta.com/shop/makeup/face/foundation/face-primer"},
        {"category": "mascara", "url": "https://www.ulta.com/shop/makeup/eyes/mascara"},
        {"category": "moisturizer", "url": "https://www.ulta.com/shop/skin-care/moisturizers"},
    ]

    module_params = {
        "gti": "4c5ae407-6d39-4bc2-8b88-c3c73b90c19c",
        "loginStatus": "anonymous",
        "retailerVisitorId": "bff8c299-5cd1-4012-ae07-2c4ce39c6e45",
        "breakpoint": "LG",
    }

    def start_requests(self):
        target = self._target_with_sort(self.resolve_target_url())
        page_query = (
            'query Page($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON, $url: JSON) '
            '{ Page: Page(stagingHost: $stagingHost, previewOptions: $previewOptions, '
            'moduleParams: $moduleParams, url: $url, deliveryKey: "SDK") '
            '{ content customResponseAttributes meta __typename } }'
        )
        variables = {"moduleParams": {}, "url": {"path": target}}
        url = self._build_graphql_get_url(page_query, "Page", variables)
        meta = {
            "page": 1,
            "category_url": target,
            "cookiejar": self.name,
            "disable_proxy": True,
        }
        yield scrapy.Request(
            url,
            callback=self.parse_page_definition,
            headers=self._headers(operation="Page", referer=target),
            meta=meta,
            dont_filter=True,
        )

    def parse_page_definition(self, response: scrapy.http.Response):

        payload = self._to_json(response)
        if not payload:
            self.logger.warning("Ulta Page query failed")
            retry = self._build_unsorted_page_retry(response)
            if retry is not None:
                yield retry
            return

        modules = payload.get("data", {}).get("Page", {}).get("content", {}).get("modules", [])

        content_id = None
        for m in modules:
            if isinstance(m, dict) and m.get("type") == "ProductListingResults":
                content_id = m.get("id")
                break

        if not content_id:
            self.logger.warning("Could not locate ProductListingResults contentId")
            retry = self._build_unsorted_page_retry(response)
            if retry is not None:
                yield retry
            return

        category_url = response.meta.get("category_url") or self._target_with_sort(self.resolve_target_url())
        first_url = self._build_noncached_url(content_id=content_id, page=1, category_url=category_url)
        yield scrapy.Request(
            first_url,
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=category_url),
            meta=({
                "content_id": content_id,
                "page": 1,
                "disable_proxy": True,
                "category_url": category_url,
                "cookiejar": response.meta.get("cookiejar"),
            }),
        )

    def parse_listing(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        if not payload:
            self.logger.warning("Ulta NonCachedPage query failed for page=%s", response.meta.get("page"))
            retry = self._build_unsorted_listing_retry(response)
            if retry is not None:
                yield retry
            return

        content = payload.get("data", {}).get("Page", {}).get("content", {})
        items = content.get("items", []) or []

        if not items and int(response.meta.get("page", 1)) == 1:
            retry = self._build_unsorted_listing_retry(response)
            if retry is not None:
                yield retry
            return

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
                "mode": "category",
                "category_url": response.meta.get("category_url") or self.resolve_target_url(),
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages or not items:
            return

        next_page = current_page + 1
        content_id = response.meta.get("content_id")
        category_url = response.meta.get("category_url") or self._target_with_sort(self.resolve_target_url())
        next_url = self._build_noncached_url(content_id=content_id, page=next_page, category_url=category_url)
        yield scrapy.Request(
            next_url,
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=category_url),
            meta=({
                "content_id": content_id,
                "page": next_page,
                "disable_proxy": True,
                "category_url": category_url,
                "cookiejar": response.meta.get("cookiejar"),
            }),
        )

    def _build_unsorted_page_retry(self, response: scrapy.http.Response):
        if response.meta.get("unsorted_page_retry"):
            return None
        category_url = response.meta.get("category_url") or self._target_with_sort(self.resolve_target_url())
        unsorted_url = self._without_sort(category_url)
        if unsorted_url == category_url:
            return None

        page_query = (
            'query Page($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON, $url: JSON) '
            '{ Page: Page(stagingHost: $stagingHost, previewOptions: $previewOptions, '
            'moduleParams: $moduleParams, url: $url, deliveryKey: "SDK") '
            '{ content customResponseAttributes meta __typename } }'
        )
        variables = {"moduleParams": {}, "url": {"path": unsorted_url}}
        url = self._build_graphql_get_url(page_query, "Page", variables)
        self.logger.info("Retrying Ulta Page query without sort parameter")
        return scrapy.Request(
            url,
            callback=self.parse_page_definition,
            headers=self._headers(operation="Page", referer=unsorted_url),
            meta={
                "page": 1,
                "category_url": unsorted_url,
                "cookiejar": response.meta.get("cookiejar"),
                "disable_proxy": True,
                "unsorted_page_retry": True,
            },
            dont_filter=True,
        )

    def _build_unsorted_listing_retry(self, response: scrapy.http.Response):
        if response.meta.get("unsorted_listing_retry"):
            return None
        if int(response.meta.get("page", 1)) != 1:
            return None
        content_id = response.meta.get("content_id")
        if not content_id:
            return None

        category_url = response.meta.get("category_url") or self._target_with_sort(self.resolve_target_url())
        unsorted_url = self._without_sort(category_url)
        if unsorted_url == category_url:
            return None

        self.logger.info("Retrying Ulta NonCachedPage query without sort parameter")
        retry_url = self._build_noncached_url(content_id=content_id, page=1, category_url=unsorted_url)
        return scrapy.Request(
            retry_url,
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=unsorted_url),
            meta={
                "content_id": content_id,
                "page": 1,
                "disable_proxy": True,
                "category_url": unsorted_url,
                "cookiejar": response.meta.get("cookiejar"),
                "unsorted_listing_retry": True,
            },
            dont_filter=True,
        )

    @staticmethod
    def _without_sort(url: str) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs.pop("sort", None)
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _build_noncached_url(self, content_id: str, page: int, category_url: str) -> str:
        path = self._with_page(category_url, page)

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

    def _headers(self, operation: str | None = None, referer: str | None = None) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "accept": "application/json,text/plain,*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "apollo-require-preflight": "true",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-fetch-dest": "empty",
        }
        if operation:
            headers["x-apollo-operation-name"] = operation
        if referer:
            headers["Referer"] = referer
        return headers

    def _target_with_sort(self, target: str) -> str:
        sort = (getattr(self, "sort", None) or "").strip().lower()
        param = self._sort_param(sort)
        if not param:
            return target
        parts = urlparse(target)
        qs = parse_qs(parts.query)
        qs["sort"] = [param]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _sort_param(self, sort: str) -> str | None:
        order_map = {
            "bestseller": "bestSeller",
            "new": "newArrivals",
            "price_low": "priceLowToHigh",
            "price_high": "priceHighToLow",
            "rating": "topRated",
        }
        if not sort:
            return None
        if sort in order_map.values():
            return sort
        return order_map.get(sort)

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

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

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
