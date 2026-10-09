from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.abercrombie_categories import ABERCROMBIE_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


class AbercrombieListingSpider(BaseListingSpider):
    """Abercrombie US products from the server-rendered Apollo cache only."""

    name = "abercrombie_listing"
    allowed_domains = ["abercrombie.com", "www.abercrombie.com"]
    categories = ABERCROMBIE_CATEGORIES
    page_size = 90

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "DOWNLOAD_TIMEOUT": 120,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "category_id", "product_id", "item_id",
            "style_id", "title", "brand", "gender", "url", "image_url",
            "color", "colors", "price", "original_price", "currency",
            "discount_text", "price_flag", "badges", "collection",
            "online_availability", "member_price", "promo_message", "page",
            "position", "total_count", "total_pages", "source_url", "source",
            "raw", "timestamp",
        ],
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }
    _marker = (
        "window['APOLLO_STATE__catalog-mfe-web-service-"
        "CategoryPageFrontEnd-config'] = "
    )
    _challenge_markers = (
        "captcha", "access denied", "failed to get successful response",
        "api credits", "proxy authentication required",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        selected = next(
            (entry for entry in self.categories if entry["category"] == self.category),
            {},
        )
        yield self._request(target, 1, selected.get("department"))

    def _request(self, base_url: str, page: int, department: str | None):
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta={"page": page, "base_url": base_url, "department": department},
        )

    def parse(self, response: scrapy.http.Response):
        self._reject_bad_response(response)
        page = int(response.meta.get("page", 1))
        bootstrap = self.extract_apollo_bootstrap(response.text)
        cache = bootstrap.get("CACHE")
        if not isinstance(cache, dict):
            raise RuntimeError(f"Abercrombie bootstrap has no Apollo CACHE at {response.url}")
        category = self._category_result(cache, page)
        references = next(
            (value for key, value in category.items()
             if key.startswith("products(") and isinstance(value, list)),
            None,
        )
        if not references:
            if page > 1:
                return
            raise RuntimeError(f"Abercrombie Apollo category has no products at {response.url}")

        pagination = category.get("pagination") or {}
        current_page = self._integer(pagination.get("currentPage")) or page
        total_pages = self._integer(pagination.get("totalPages")) or 1
        total_count = self._integer(category.get("productTotalCount"))
        emitted = 0
        for position, reference in enumerate(references, start=1):
            key = reference.get("__ref") if isinstance(reference, dict) else None
            product = cache.get(key) if key else None
            if not isinstance(product, dict):
                continue
            part_number = str(product.get("partNumber") or product.get("kic") or "").strip()
            if not part_number or part_number in self._seen:
                continue
            self._seen.add(part_number)
            emitted += 1
            yield self._item(
                product, cache, category, response, current_page, position,
                total_count, total_pages,
            )

        if emitted and current_page < min(self.max_pages, total_pages):
            yield self._request(
                response.meta["base_url"], current_page + 1,
                response.meta.get("department"),
            )

    @classmethod
    def extract_apollo_bootstrap(cls, html: str) -> dict[str, Any]:
        start = (html or "").find(cls._marker)
        if start < 0:
            raise RuntimeError("Abercrombie response has no catalog Apollo bootstrap")
        try:
            value, _ = json.JSONDecoder().raw_decode(html, start + len(cls._marker))
        except json.JSONDecodeError as exc:
            raise RuntimeError("Abercrombie catalog Apollo bootstrap is malformed") from exc
        if not isinstance(value, dict):
            raise RuntimeError("Abercrombie catalog Apollo bootstrap is not an object")
        return value

    @staticmethod
    def _category_result(cache: dict[str, Any], expected_page: int) -> dict[str, Any]:
        root = cache.get("ROOT_QUERY")
        if not isinstance(root, dict):
            raise RuntimeError("Abercrombie Apollo cache has no ROOT_QUERY")
        candidates = [
            value for key, value in root.items()
            if key.startswith("category(") and isinstance(value, dict)
            and isinstance(value.get("pagination"), dict)
        ]
        if not candidates:
            raise RuntimeError("Abercrombie Apollo cache has no category query")
        for candidate in candidates:
            if candidate["pagination"].get("currentPage") == expected_page:
                return candidate
        return candidates[0]

    def _item(
        self, product, cache, category, response, page, position,
        total_count, total_pages,
    ):
        price = product.get("price") or {}
        current_price = self._money(price.get("discountPrice"))
        original_price = self._money(price.get("originalPrice"))
        if current_price is None:
            current_price = original_price or self._money(price.get("description"))
        image_set = product.get("imageSet") or {}
        image_id = image_set.get("primaryFaceOutImage")
        style_id = product.get("kic")
        swatches = self._swatches(product, cache)
        current_swatch = cache.get(f"ProductSwatch:{style_id}", {})
        badges = [
            badge.get("text") for badge in product.get("badges") or []
            if isinstance(badge, dict) and badge.get("text")
        ]
        promo = product.get("promoMessaging") or {}
        member_price = product.get("memberPrice") or {}
        relative_url = str(product.get("productPageUrl") or "").replace("undefined/", "/shop/us/")
        raw = {"product": product, "current_swatch": current_swatch}
        return {
            "category": self.category,
            "department": response.meta.get("department"),
            "category_id": category.get("categoryId"),
            "product_id": str(product.get("id")) if product.get("id") is not None else None,
            "item_id": product.get("partNumber") or style_id,
            "style_id": style_id,
            "title": product.get("name"),
            "brand": "Abercrombie & Fitch",
            "gender": product.get("gender"),
            "url": urljoin("https://www.abercrombie.com", relative_url),
            "image_url": (
                f"https://img.abercrombie.com/is/image/anf/{image_id}?policy=product-medium"
                if image_id else None
            ),
            "color": current_swatch.get("name") if isinstance(current_swatch, dict) else None,
            "colors": [swatch["name"] for swatch in swatches if swatch.get("name")],
            "price": current_price,
            "original_price": original_price,
            "currency": "USD",
            "discount_text": price.get("discountText"),
            "price_flag": price.get("priceFlag"),
            "badges": badges,
            "collection": product.get("collection"),
            "online_availability": product.get("onlineAvailability"),
            "member_price": self._money(member_price.get("description")),
            "promo_message": promo.get("message"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": response.url,
            "source": "abercrombie_catalog_apollo_bootstrap",
            "raw": raw,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _swatches(product: dict[str, Any], cache: dict[str, Any]) -> list[dict[str, Any]]:
        result = []
        for reference in product.get("swatchList") or []:
            key = reference.get("__ref") if isinstance(reference, dict) else None
            entity = cache.get(key) if key else None
            if isinstance(entity, dict):
                result.append(entity)
        return result

    @classmethod
    def _page_url(cls, url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query) if key != "start"]
        if page > 1:
            query.append(("start", str((page - 1) * cls.page_size)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _reject_bad_response(self, response):
        lower = (response.text or "").lower()
        if response.status != 200:
            raise RuntimeError(f"Abercrombie returned HTTP {response.status}: {response.url}")
        if self._marker not in response.text and any(
            marker in lower for marker in self._challenge_markers
        ):
            raise RuntimeError(f"Abercrombie returned a challenge/proxy response: {response.url}")

    @staticmethod
    def _money(value):
        if isinstance(value, dict):
            value = value.get("description") or value.get("value")
        if value is None:
            return None
        match = re.search(r"-?[\d,]+(?:\.\d+)?", str(value))
        return float(match.group(0).replace(",", "")) if match else None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
