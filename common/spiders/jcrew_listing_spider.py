from __future__ import annotations

"""J.Crew US listing spider backed exclusively by the Next.js hydration state."""

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.jcrew_categories import JCREW_LISTING_CATEGORIES

SITE_URL = "https://www.jcrew.com"
_NEXT_DATA_RE = re.compile(
    r'<script[^>]*\bid=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
_CHALLENGE_MARKERS = (
    "access denied", "pardon the interruption", "are you a human",
    "request unsuccessful", "verify you are human",
)


def parse_next_data(html: str) -> dict[str, Any]:
    """Decode the authoritative Next.js hydration payload or fail loudly."""
    if any(marker in html.lower() for marker in _CHALLENGE_MARKERS):
        raise ValueError("J.Crew returned an anti-bot/challenge page, not a listing")
    match = _NEXT_DATA_RE.search(html)
    if not match:
        raise ValueError("J.Crew listing is missing the __NEXT_DATA__ hydration payload")
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError("J.Crew __NEXT_DATA__ payload is invalid JSON") from exc
    state = (
        payload.get("props", {}).get("initialState", {})
        if isinstance(payload, dict) else {}
    )
    product_array = state.get("array", {}).get("data", {}).get("productArray") if isinstance(state, dict) else None
    if not isinstance(product_array, dict) or not isinstance(product_array.get("productList"), list):
        raise ValueError("J.Crew __NEXT_DATA__ has no productArray.productList")
    return payload


def hydrated_products(payload: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    state = payload["props"]["initialState"]["array"]["data"]["productArray"]
    product_list = state["productList"]
    if not product_list or not isinstance(product_list[0], dict):
        raise ValueError("J.Crew hydration has no first-page product collection")
    products = product_list[0].get("products")
    pagination = state.get("pagination")
    if not isinstance(products, list) or not isinstance(pagination, dict):
        raise ValueError("J.Crew hydration has invalid products or pagination metadata")
    return products, pagination


class JcrewListingSpider(BaseListingSpider):
    name = "jcrew_listing"
    allowed_domains = ["jcrew.com", "www.jcrew.com", "localhost", "127.0.0.1"]
    categories = JCREW_LISTING_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "title", "description",
            "primary_category_id", "url", "price", "original_price", "currency",
            "rating", "reviews_count", "page", "position", "total_count",
            "source_url", "source", "raw", "timestamp",
        ],
    }

    def category_entry(self, name: str) -> dict[str, Any] | None:
        entry = super().category_entry(name)
        if entry is not None:
            return entry
        # Preserve the legacy display-label lookup and first-match order.
        for entry in self.iter_categories():
            if entry["label"] == name:
                return {**entry, "category": name}
        return None

    async def start(self):
        self._seen_products: set[str] = set()
        target = self.resolve_target_url()
        if self.url or self.category_url:
            selected = next((entry for entry in self.iter_categories() if entry["url"] == target), {})
        else:
            selected = self.category_entry(self.category) or {}
        yield scrapy.Request(
            target,
            callback=self.parse,
            errback=self._request_failed,
            headers=self._headers(),
            meta={"category": selected.get("category") or self.category or "custom",
                  "department": selected.get("group"), "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"J.Crew listing returned HTTP {response.status}: {response.url}")
        try:
            payload = parse_next_data(response.text)
            products, pagination = hydrated_products(payload)
        except ValueError as exc:
            raise RuntimeError(f"Could not parse J.Crew listing at {response.url}: {exc}") from exc

        page = int(response.meta.get("page", 1))
        page_index = self._integer(pagination.get("pageIndex"))
        total_pages = self._integer(pagination.get("totalPage"))
        if page_index is None or total_pages is None or total_pages < 1:
            raise RuntimeError(f"J.Crew hydration has invalid pagination metadata: {pagination!r}")
        if page_index != page:
            raise RuntimeError(f"J.Crew returned pageIndex={page_index} for requested page={page}")
        if not products and page_index <= total_pages:
            raise RuntimeError(f"J.Crew page {page} is empty despite totalPage={total_pages}")

        total_count = self._integer(pagination.get("totalResults") or pagination.get("totalCount"))
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            product_url = product.get("url")
            item_id = (
                self._text(product.get("productCode"))
                or self._text(product.get("baseProductCode"))
                or self._text(product.get("representedSkuId"))
                or (urlsplit(product_url).path.rstrip("/").rsplit("/", 1)[-1] if product_url else None)
            )
            if not item_id or item_id in self._seen_products:
                if not item_id:
                    self.logger.warning(
                        "Skipping hydrated product without a stable product code or URL (page=%s, position=%s)",
                        page_index,
                        position,
                    )
                continue
            self._seen_products.add(item_id)
            list_price = product.get("listPrice")
            price = self._money(product.get("searchPrice"))
            if price is None and isinstance(list_price, dict):
                price = self._money(list_price.get("amount"))
            was = product.get("was")
            original_price = self._money(product.get("originalPrice"))
            if original_price is None and isinstance(was, dict):
                original_price = self._money(was.get("amount"))
            if original_price is None and isinstance(list_price, dict):
                listed = self._money(list_price.get("amount"))
                if listed is not None and price is not None and listed > price:
                    original_price = listed
            yield {
                "category": response.meta.get("category"),
                "department": response.meta.get("department"),
                "item_id": item_id,
                "title": self._text(product.get("productDescription")),
                "description": self._text(product.get("productDescription")),
                "primary_category_id": self._text(product.get("primaryCategoryId")),
                "url": urljoin(SITE_URL, product_url) if product_url else None,
                "price": price,
                "original_price": original_price,
                "currency": "USD" if price is not None else None,
                "rating": self._number(product.get("bvAverageRating")),
                "reviews_count": self._integer(product.get("bvReviewCount")),
                "page": page_index,
                "position": position,
                "total_count": total_count,
                "source_url": response.url,
                "source": "jcrew_next_data",
                "raw": product,
            }

        if page_index < total_pages and page < self.max_pages:
            yield scrapy.Request(
                self._page_url(response.url, page_index + 1),
                callback=self.parse,
                errback=self._request_failed,
                headers=self._headers(response.url),
                meta={**response.meta, "page": page_index + 1},
            )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _headers(referer: str | None = None) -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            **({"referer": referer} if referer else {}),
        }

    @staticmethod
    def _request_failed(failure):
        raise RuntimeError(f"J.Crew listing request failed: {failure.request.url}: {failure.value}")

    @staticmethod
    def _text(value):
        return str(value).strip() if value is not None and not isinstance(value, (dict, list)) else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _money(value):
        try:
            result = float(value) if value is not None and not isinstance(value, bool) else None
            return result if result is not None and result >= 0 else None
        except (TypeError, ValueError):
            return None
