from __future__ import annotations

"""Gymshark listings from the server-rendered Next.js hydration only."""

import json
import math
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.gymshark_categories import GYMSHARK_CATEGORIES


class GymsharkListingSpider(BaseListingSpider):
    """Extract the Algolia ``ssrQuery`` embedded in ``#__NEXT_DATA__``.

    This is deliberately a single data direction: product fields, counts and
    pagination all come from the structured Next.js hydration. Rendered product
    cards and JSON-LD are never parsed as fallbacks.
    """

    name = "gymshark_listing"
    allowed_domains = ["gymshark.com", "www.gymshark.com"]
    categories = GYMSHARK_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "sku", "title", "brand", "product_type", "handle",
            "url", "image", "image_alt", "colour", "canonical_colour",
            "gender", "fit", "activities", "price", "compare_at_price",
            "discount_percentage", "currency", "in_stock", "sizes_in_stock",
            "available_sizes", "inventory_quantity", "rating", "reviews_count",
            "labels", "category", "page", "position", "total_count",
            "total_pages", "query_id", "source", "raw", "timestamp",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url() if (self.url or self.category_url or self.category) else self.categories[0]["url"]
        category = self.category or self._category_for_url(target)
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self.headers,
            meta={"page_index": 0, "base_url": target, "category": category},
        )

    def parse(self, response: scrapy.http.Response):
        self._reject_bad_response(response)
        page_props = self._page_props(response)
        query = page_props.get("ssrQuery")
        if not isinstance(query, dict):
            raise RuntimeError(f"Gymshark hydration has no props.pageProps.ssrQuery at {response.url}")

        hits = query.get("hits")
        if not isinstance(hits, list):
            raise RuntimeError(f"Gymshark ssrQuery.hits is not a list at {response.url}")
        page_index = self._integer(query.get("page"), response.meta.get("page_index", 0))
        hits_per_page = self._integer(query.get("hitsPerPage"), len(hits))
        total_count = self._integer(query.get("nbHits"), len(hits))
        total_pages = math.ceil(total_count / hits_per_page) if hits_per_page else 1
        category = response.meta.get("category") or self._category_for_url(response.meta.get("base_url", response.url))

        for position, hit in enumerate(hits, start=1):
            if not isinstance(hit, dict):
                continue
            item_id = str(hit.get("id") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(
                hit,
                item_id=item_id,
                category=category,
                page=page_index + 1,
                position=position,
                total_count=total_count,
                total_pages=total_pages,
                query_id=query.get("queryID"),
            )

        next_index = page_index + 1
        if next_index < min(self.max_pages, total_pages):
            yield scrapy.Request(
                self._with_page(response.meta.get("base_url", response.url), next_index),
                callback=self.parse,
                headers=self.headers,
                meta={**response.meta, "page_index": next_index},
            )

    def _item(
        self,
        hit: dict[str, Any],
        *,
        item_id: str,
        category: str,
        page: int,
        position: int,
        total_count: int,
        total_pages: int,
        query_id: Any,
    ) -> dict[str, Any]:
        media = hit.get("featuredMedia") if isinstance(hit.get("featuredMedia"), dict) else {}
        rating = hit.get("rating") if isinstance(hit.get("rating"), dict) else {}
        sizes = hit.get("availableSizes") if isinstance(hit.get("availableSizes"), list) else []
        inventory = sum(
            value for row in sizes if isinstance(row, dict)
            for value in [self._number(row.get("inventoryQuantity"))] if value is not None
        )
        return {
            "item_id": item_id,
            "sku": hit.get("sku"),
            "title": hit.get("title"),
            "brand": "Gymshark",
            "product_type": hit.get("type"),
            "handle": hit.get("handle"),
            "url": f"https://www.gymshark.com/products/{hit.get('handle')}" if hit.get("handle") else None,
            "image": media.get("src"),
            "image_alt": media.get("alt"),
            "colour": hit.get("colour"),
            "canonical_colour": hit.get("canonicalColour"),
            "gender": hit.get("gender") or [],
            "fit": hit.get("fit"),
            "activities": hit.get("activities") or [],
            "price": self._number(hit.get("price")),
            "compare_at_price": self._number(hit.get("compareAtPrice")),
            "discount_percentage": self._number(hit.get("discountPercentage")),
            "currency": "USD",
            "in_stock": hit.get("inStock"),
            "sizes_in_stock": hit.get("sizeInStock") or [],
            "available_sizes": sizes,
            "inventory_quantity": inventory,
            "rating": self._number(rating.get("average")),
            "reviews_count": self._integer(rating.get("count"), 0),
            "labels": hit.get("labels") or [],
            "category": category,
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "query_id": query_id,
            "source": "gymshark_next_data_ssr_query",
            "raw": hit,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _page_props(response: scrapy.http.Response) -> dict[str, Any]:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Gymshark response has no #__NEXT_DATA__ hydration at {response.url}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Gymshark #__NEXT_DATA__ is malformed at {response.url}") from exc
        props = data.get("props") if isinstance(data, dict) else None
        page_props = props.get("pageProps") if isinstance(props, dict) else None
        return page_props if isinstance(page_props, dict) else {}

    @staticmethod
    def _with_page(url: str, page_index: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page_index)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _category_for_url(self, url: str) -> str:
        path = urlsplit(url).path.rstrip("/")
        for row in self.categories:
            if urlsplit(row["url"]).path.rstrip("/") == path:
                return row["category"]
        return path.removeprefix("/collections/").replace("/", "-") or "custom"

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        return int(value) if float(value).is_integer() else float(value)

    @staticmethod
    def _integer(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return int(default)

    @staticmethod
    def _reject_bad_response(response: scrapy.http.Response) -> None:
        body = response.text.lower()
        markers = ("just a moment", "cf-chl-", "captcha", '"api credits"')
        if response.status != 200 or any(marker in body for marker in markers):
            raise RuntimeError(
                f"Gymshark returned a challenge/proxy response (status={response.status}, "
                f"bytes={len(response.body)}) at {response.url}"
            )
