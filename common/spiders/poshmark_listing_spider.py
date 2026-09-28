from __future__ import annotations

import json
from urllib.parse import quote

import scrapy
from curl_cffi import requests as curl_requests
from scrapy.http import HtmlResponse

from common.spiders.base_listing_spider import BaseListingSpider


class PoshmarkBrowserDownloadMiddleware:
    """Fetch Poshmark with a browser TLS fingerprint to avoid its HTTP 403 gate."""

    def process_request(self, request, spider):
        if spider.name != "poshmark_listing":
            return None
        result = curl_requests.get(
            request.url,
            headers={key.decode(): value[0].decode() for key, value in request.headers.items()},
            impersonate="chrome",
            timeout=30,
        )
        response_headers = dict(result.headers)
        response_headers.pop("content-encoding", None)
        response_headers.pop("Content-Encoding", None)
        response_headers.pop("content-length", None)
        response_headers.pop("Content-Length", None)
        return HtmlResponse(
            url=str(result.url),
            status=result.status_code,
            headers=response_headers,
            body=result.content,
            encoding="utf-8",
            request=request,
        )


class PoshmarkListingSpider(BaseListingSpider):
    """Extract Poshmark listings from the category page bootstrap state."""

    name = "poshmark_listing"
    allowed_domains = ["poshmark.com", "www.poshmark.com"]

    categories = [
        {"category": "women", "url": "https://poshmark.com/category/Women"},
        {"category": "men", "url": "https://poshmark.com/category/Men"},
        {"category": "kids", "url": "https://poshmark.com/category/Kids"},
        {"category": "home", "url": "https://poshmark.com/category/Home"},
        {"category": "electronics", "url": "https://poshmark.com/category/Electronics"},
        {"category": "pets", "url": "https://poshmark.com/category/Pets"},
    ]

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "common.spiders.poshmark_listing_spider.PoshmarkBrowserDownloadMiddleware": 50,
        },
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
            "size",
            "source",
            "category_url",
            "page",
        ]
    }

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield scrapy.Request(
            target_url,
            callback=self.parse,
            meta={"page": 1, "category": self.category},
            headers=self._headers(),
        )

    def parse(self, response: scrapy.http.Response):
        state = self._extract_initial_state(response.text)
        products = self._extract_products(state)
        if not products:
            raise RuntimeError(f"No Poshmark bootstrap listings found at {response.url}")

        for product in products:
            item_id = product.get("id")
            if not item_id:
                continue
            price = product.get("price_amount") or {}
            original_price = product.get("original_price_amount") or {}
            cover = product.get("cover_shot") or {}
            yield {
                "category": response.meta.get("category"),
                "item_id": item_id,
                "title": product.get("title"),
                "brand": product.get("brand"),
                "url": self._listing_url(product),
                "image_url": cover.get("url_large") or cover.get("url"),
                "price": self._to_float(price.get("val")),
                "original_price": self._to_float(original_price.get("val")),
                "currency": price.get("currency_code"),
                "size": product.get("size"),
                "source": "poshmark_bootstrap_state",
                "category_url": response.url,
                "page": response.meta.get("page", 1),
            }

    def _extract_initial_state(self, html: str) -> dict:
        marker = "window.__INITIAL_STATE__="
        marker_index = html.find(marker)
        start = html.find("{", marker_index) if marker_index >= 0 else -1
        if start < 0:
            return {}

        level = 0
        in_string = False
        escaped = False
        for index, character in enumerate(html[start:], start):
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == "{":
                level += 1
            elif character == "}":
                level -= 1
                if level == 0:
                    value = json.loads(html[start : index + 1])
                    return value if isinstance(value, dict) else {}
        return {}

    @staticmethod
    def _extract_products(state: dict) -> list[dict]:
        grid = (state.get("$_category") or {}).get("gridData") or {}
        return [value for value in grid.get("data") or [] if isinstance(value, dict)]

    @staticmethod
    def _listing_url(product: dict) -> str:
        slug = "-".join((product.get("title") or "listing").split())
        return f"https://poshmark.com/listing/{quote(slug, safe='-')}-{product['id']}"

    @staticmethod
    def _to_float(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        }
