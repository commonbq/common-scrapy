from __future__ import annotations

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.utils import dict_get


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
            "item_id",
            "sku_id",
            "brand",
            "title",
            "url",
            "image_url",
            "list_price",
            "sale_price",
            "rating",
            "reviews_count",
            "is_sponsored",
            "source",
            "mode",
            "page",
            "category_url",
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

    module_params = {
        "gti": "761dff0b-9c5c-411d-b508-3ee9f646e7cb",
        "loginStatus": "anonymous",
        "retailerVisitorId": "bff8c299-5cd1-4012-ae07-2c4ce39c6e45",
        "breakpoint": "XL",
    }
    GRAPHQL_URL = "https://www.ulta.com/dxl/graphql?ultasite=en-us"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._html_fallback_started = False

    def start_requests(self):
        category_url = self._with_page(self.resolve_target_url(), page=1)
        mode = (getattr(self, "mode", None) or "graphql").strip().lower()

        if mode == "html":
            self._html_fallback_started = True
            yield scrapy.Request(
                category_url,
                callback=self.parse_html_listing,
                meta={"page": 1, "category_url": category_url, "mode": "html"},
                dont_filter=True,
            )
            return

        yield self._build_page_request(category_url)

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _build_page_request(
        self, category_url: str, meta: dict | None = None
    ) -> scrapy.Request:
        payload = {
            "query": self._page_query(),
            "variables": {"moduleParams": {}, "url": {"path": category_url}},
            "operationName": "Page",
        }
        req_meta = {"page": 1, "category_url": category_url, "mode": "graphql"}
        if meta:
            req_meta.update(meta)
        return scrapy.Request(
            self.GRAPHQL_URL,
            method="POST",
            body=json.dumps(payload),
            callback=self.parse_page_definition,
            headers=self._headers(operation="Page", referer=category_url),
            meta=req_meta,
            dont_filter=True,
        )

    @staticmethod
    def _page_query() -> str:
        return (
            'query Page($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON, $url: JSON) '
            '{ Page: Page(stagingHost: $stagingHost, previewOptions: $previewOptions, '
            'moduleParams: $moduleParams, url: $url, deliveryKey: "SDK") '
            "{ content customResponseAttributes meta __typename } }"
        )

    def _build_payload(self, category_url: str, content_id: str) -> dict:
        query = (
            "query NonCachedPage($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON) "
            "{ Page: NonCachedPage(stagingHost:$stagingHost, previewOptions:$previewOptions, "
            'moduleParams:$moduleParams, url: {path: "'
            + category_url
            + '"}, contentId: "'
            + content_id
            + '") { content customResponseAttributes meta __typename } }'
        )
        return {
            "query": query,
            "variables": {"moduleParams": self.module_params},
            "operationName": "NonCachedPage",
        }

    def parse_page_definition(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        if not payload:
            self.logger.warning("Ulta Page query failed for category %s", self.category)
            yield from self._schedule_html_fallback(response)
            return

        modules = dict_get(payload, "data.Page.content.modules") or []
        content_id = None
        for module in modules:
            if isinstance(module, dict) and module.get("type") == "ProductListingResults":
                content_id = module.get("id")
                break

        if not content_id:
            self.logger.warning(
                "Could not locate ProductListingResults contentId for category %s",
                self.category,
            )
            yield from self._schedule_html_fallback(response)
            return

        category_url = response.meta.get("category_url") or self.resolve_target_url()
        page = int(response.meta.get("page", 1))
        page_url = self._with_page(category_url, page=page)
        yield scrapy.Request(
            self.GRAPHQL_URL,
            method="POST",
            body=json.dumps(self._build_payload(page_url, content_id)),
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=page_url),
            meta={
                "page": page,
                "category_url": category_url,
                "content_id": content_id,
                "rediscovery_attempted": bool(
                    response.meta.get("rediscovery_attempted")
                ),
            },
            dont_filter=True,
        )

    def parse_listing(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        current_page = int(response.meta.get("page", 1))
        if not payload:
            self.logger.warning(
                "Ulta NonCachedPage query failed for category %s on page %s",
                self.category,
                current_page,
            )
            retry = self._retry_with_rediscovery(
                response, reason="NonCachedPage query failed"
            )
            if retry is not None:
                yield retry
            else:
                yield from self._schedule_html_fallback(response)
            return

        items = dict_get(payload, "data.Page.content.items") or []
        if not items and current_page == 1:
            self.logger.warning(
                "No items found for category %s on page %s",
                self.category,
                current_page,
            )
            retry = self._retry_with_rediscovery(
                response, reason="NonCachedPage returned 0 items"
            )
            if retry is not None:
                yield retry
            else:
                yield from self._schedule_html_fallback(response)
            return

        category_url = response.meta.get("category_url") or self.resolve_target_url()

        for item in items:
            action = item.get("action") or {}
            raw_url = action.get("url")
            yield {
                "category": self.category,
                "item_id": item.get("productId"),
                "sku_id": item.get("skuId"),
                "brand": item.get("brandName"),
                "title": item.get("productName"),
                "url": response.urljoin(raw_url) if raw_url else None,
                "image_url": self._extract_image_url(item),
                "list_price": item.get("listPrice"),
                "sale_price": item.get("salePrice"),
                "rating": self._to_float(item.get("rating")),
                "reviews_count": self._to_int(item.get("reviewCount")),
                "is_sponsored": bool(item.get("sponsored")),
                "source": "ulta_dxl_graphql",
                "mode": "category",
                "page": current_page,
                "category_url": category_url,
            }

        if current_page >= self.max_pages or not items:
            return

        next_page = current_page + 1
        content_id = response.meta.get("content_id")
        next_page_url = self._with_page(category_url, page=next_page)
        if not content_id:
            self.logger.warning(
                "Missing contentId for category %s before requesting page %s",
                self.category,
                next_page,
            )
            yield self._build_page_request(
                category_url,
                meta={
                    "page": next_page,
                    "category_url": category_url,
                    "rediscovery_attempted": True,
                },
            )
            return
        yield scrapy.Request(
            self.GRAPHQL_URL,
            method="POST",
            body=json.dumps(self._build_payload(next_page_url, content_id)),
            callback=self.parse_listing,
            headers=self._headers(operation="NonCachedPage", referer=next_page_url),
            meta={
                "page": next_page,
                "category_url": category_url,
                "content_id": content_id,
                "rediscovery_attempted": False,
            },
        )

    def parse_html_listing(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        category_url = response.meta.get("category_url") or self.resolve_target_url()
        seen: set[str] = set()
        yielded = 0

        anchors = response.xpath('//a[contains(@href,"/p/")]')
        for anchor in anchors:
            href = (anchor.attrib.get("href") or "").strip()
            if "/p/" not in href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)

            card = anchor.xpath('ancestor::*[self::article or self::li or self::div][1]')
            title = " ".join(card.xpath('.//text()').getall()).strip() if card else ""
            title = re.sub(r"\s+", " ", title)
            image_url = None
            if card:
                image_url = card.xpath('.//img/@src').get() or card.xpath(
                    './/img/@data-src'
                ).get()

            price_values = re.findall(r"\$\d+(?:\.\d{2})?", title)
            list_price = price_values[0] if price_values else None
            sale_price = None
            if len(price_values) > 1:
                sale_price = price_values[0]
                list_price = price_values[1]

            sku_match = re.search(r"[?&]sku=(\d+)", url)
            sku_id = sku_match.group(1) if sku_match else None

            yield {
                "category": self.category,
                "item_id": sku_id,
                "sku_id": sku_id,
                "brand": None,
                "title": title or None,
                "url": url,
                "image_url": image_url,
                "list_price": list_price,
                "sale_price": sale_price,
                "rating": None,
                "reviews_count": None,
                "is_sponsored": False,
                "source": "ulta_direct_html",
                "mode": "category_html",
                "page": page,
                "category_url": category_url,
            }
            yielded += 1

        if yielded == 0:
            self.logger.warning(
                "Ulta HTML mode yielded 0 items for category %s (status=%s)",
                self.category,
                response.status,
            )
            return

        if page >= self.max_pages:
            return

        next_page = page + 1
        next_url = self._with_page(category_url, next_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse_html_listing,
            meta={"page": next_page, "category_url": category_url, "mode": "html"},
            dont_filter=True,
        )

    def _retry_with_rediscovery(
        self, response: scrapy.http.Response, *, reason: str | None = None
    ) -> scrapy.Request | None:
        if int(response.meta.get("page", 1)) != 1:
            return None
        if response.meta.get("rediscovery_attempted"):
            return None
        category_url = response.meta.get("category_url") or self.resolve_target_url()
        if reason:
            self.logger.info("Ulta listing %s; rediscovering contentId", reason)
        return self._build_page_request(
            category_url,
            meta={
                "page": 1,
                "category_url": category_url,
                "rediscovery_attempted": True,
            },
        )

    def _schedule_html_fallback(self, response: scrapy.http.Response):
        if self._html_fallback_started:
            return []
        self._html_fallback_started = True
        category_url = self._with_page(
            response.meta.get("category_url") or self.resolve_target_url(),
            page=1,
        )
        self.logger.info("Falling back to Ulta listing HTML parser")
        return [
            scrapy.Request(
                category_url,
                callback=self.parse_html_listing,
                meta={"page": 1, "category_url": category_url, "mode": "html"},
                dont_filter=True,
            )
        ]

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

    @staticmethod
    def _to_json(response: scrapy.http.Response) -> dict | None:
        try:
            return json.loads(response.text)
        except Exception:
            return None

    @staticmethod
    def _extract_image_url(item: dict) -> str | None:
        for key in ("image", "altImage"):
            image = item.get(key)
            if isinstance(image, dict) and image.get("imageUrl"):
                return image.get("imageUrl")
            if isinstance(image, str):
                return image
        return None

    @staticmethod
    def _to_float(value):
        try:
            return float(value)
        except Exception:
            return None

    @staticmethod
    def _to_int(value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        try:
            return int(value)
        except Exception:
            return None
