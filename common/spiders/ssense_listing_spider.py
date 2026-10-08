from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.ssense_categories import SSENSE_CATEGORIES


_FLIGHT_CHUNK_RE = re.compile(
    r"self\.__next_f\.push\(\[\s*1\s*,\s*(\"(?:[^\"\\]|\\.)*\")\s*\]\)",
    re.DOTALL,
)
_CARD_RE = re.compile(
    r'"href":"(?P<href>/[^"\\]+/product/[^"\\]+/(?P<id>\d+))"'
    r'.{0,3500}?"src":"(?P<image>https://(?:res\.cloudinary\.com/ssenseweb|img\.ssensemedia\.com)/[^"\\]+)"',
    re.DOTALL,
)
_PAGINATION_RE = re.compile(
    r'"paginationInfo":\{"currentPage":(?P<current>\d+),"totalPages":(?P<total>\d+)\}'
)
_CHALLENGE_MARKERS = (
    "just a moment",
    "cf-chl-",
    "enable javascript and cookies",
    "captcha",
    '"api credits"',
    '"concurrency"',
)


class SsenseListingSpider(BaseListingSpider):
    """SSENSE products from the server-rendered Next.js RSC bootstrap only."""

    name = "ssense_listing"
    allowed_domains = ["ssense.com", "www.ssense.com", "localhost", "127.0.0.1"]
    categories = SSENSE_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "sku", "title", "brand_id",
            "brand", "category_ids", "url", "image_url", "price",
            "original_price", "currency", "on_sale", "available", "page",
            "position", "total_pages", "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self._headers(),
            meta={"page": 1, "base_url": target},
        )

    def parse(self, response: scrapy.http.Response):
        self._reject_bad_response(response)
        page = int(response.meta.get("page", 1))
        flight = self._flight_payload(response.text)
        products = self._products(flight)
        cards = self._cards(flight)
        current_page, total_pages = self._pagination(flight)

        if not products:
            if page > 1:
                return
            raise RuntimeError(
                f"No product_listing_page products in SSENSE RSC bootstrap at {response.url}"
            )

        for position, product in enumerate(products, start=1):
            item_id = str(product.get("productId") or "").strip()
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            card = cards.get(item_id, {})
            href = card.get("href")
            image = card.get("image")
            final_price = self._number(product.get("finalPrice"))
            regular_price = self._number(product.get("regularPrice"))
            yield {
                "category": self.category,
                "department": product.get("gender"),
                "item_id": item_id,
                "sku": self._sku_from_image(image),
                "title": product.get("productName"),
                "brand_id": product.get("brandId"),
                "brand": product.get("brandName"),
                "category_ids": product.get("allCategoryIds") or [],
                "url": self._product_url(response, href),
                "image_url": self._image_url(image),
                "price": final_price,
                "original_price": regular_price,
                "currency": product.get("currency"),
                "on_sale": (
                    final_price is not None
                    and regular_price is not None
                    and final_price < regular_price
                ),
                "available": True,
                "page": current_page or page,
                "position": position,
                "total_pages": total_pages,
                "source_url": response.url,
                "source": "ssense_next_rsc_bootstrap",
                "raw": product,
                "timestamp": self.get_timestamp(),
            }

        if page < min(self.max_pages, total_pages):
            yield scrapy.Request(
                self._with_page(response.meta.get("base_url") or response.url, page + 1),
                callback=self.parse,
                headers=self._headers(),
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _flight_payload(html: str) -> str:
        chunks: list[str] = []
        for match in _FLIGHT_CHUNK_RE.finditer(html or ""):
            try:
                chunks.append(json.loads(match.group(1)))
            except json.JSONDecodeError:
                continue
        if not chunks:
            raise RuntimeError("SSENSE response contained no Next.js RSC flight chunks")
        return "".join(chunks)

    @staticmethod
    def _products(flight: str) -> list[dict[str, Any]]:
        anchor = '"itemListId":"product_listing_page"'
        products: list[dict[str, Any]] = []
        cursor = 0
        while True:
            event = flight.find(anchor, cursor)
            if event < 0:
                break
            start = flight.find('"products":', event)
            if start < 0:
                break
            start += len('"products":')
            try:
                value, consumed = json.JSONDecoder().raw_decode(flight[start:])
            except json.JSONDecodeError:
                cursor = event + len(anchor)
                continue
            if isinstance(value, list):
                products.extend(row for row in value if isinstance(row, dict))
            cursor = start + consumed
        return products

    @staticmethod
    def _cards(flight: str) -> dict[str, dict[str, str]]:
        return {
            match.group("id"): {
                "href": match.group("href"),
                "image": match.group("image"),
            }
            for match in _CARD_RE.finditer(flight)
        }

    @staticmethod
    def _pagination(flight: str) -> tuple[int, int]:
        match = _PAGINATION_RE.search(flight)
        if not match:
            return 0, 1
        return int(match.group("current")), int(match.group("total"))

    @staticmethod
    def _product_url(response: scrapy.http.Response, href: str | None) -> str | None:
        if not href:
            return None
        if href.startswith(("/men/", "/women/", "/everything-else/")):
            href = "/en-us" + href
        return "https://www.ssense.com" + href

    @staticmethod
    def _image_url(image: str | None) -> str | None:
        return image.replace("__IMAGE_PARAMS__", "f_auto,q_85,w_640") if image else None

    @staticmethod
    def _sku_from_image(image: str | None) -> str | None:
        if not image:
            return None
        match = re.search(r"/([^/?]+)_1\.(?:jpe?g|webp)(?:\?|$)", image, re.IGNORECASE)
        return match.group(1) if match else None

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if not isinstance(value, (int, float)):
            return None
        return int(value) if float(value).is_integer() else float(value)

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _reject_bad_response(response: scrapy.http.Response) -> None:
        body = response.text.lower()
        if response.status >= 400 or any(marker in body for marker in _CHALLENGE_MARKERS):
            raise RuntimeError(
                f"SSENSE returned a challenge/proxy response (status={response.status}, "
                f"bytes={len(response.body)}) at {response.url}"
            )
