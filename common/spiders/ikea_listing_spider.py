from __future__ import annotations

import json
import re
from typing import Any

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.ikea_categories import IKE_A_CATEGORIES


def _load_categories() -> list[dict[str, str]]:
    categories: list[dict[str, str]] = []
    seen: set[str] = set()
    for department, links in IKE_A_CATEGORIES.items():
        for link in links:
            url = link["url"]
            if url in seen:
                continue
            seen.add(url)
            match = re.search(r"-([a-z]*\d+)/?$", url)
            if not match:
                continue
            categories.append(
                {
                    "category": match.group(1),
                    "department": department,
                    "name": link["name"],
                    "url": url,
                }
            )
    return categories


class IkeaListingSpider(BaseListingSpider):
    name = "ikea_listing"
    allowed_domains = ["ikea.com", "www.ikea.com", "sik.search.blue.cdtapps.com"]
    require_category_arg = False

    API_URL = "https://sik.search.blue.cdtapps.com/us/en/search?c=listaf&v=20250507"
    PAGE_SIZE = 24
    categories = _load_categories()

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "item_id",
            "title",
            "product_type",
            "dimensions",
            "url",
            "image_url",
            "image_urls",
            "price",
            "currency",
            "rating",
            "reviews_count",
            "badge",
            "design",
            "availability",
            "page",
            "category_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        category_id = self._category_id(category_url)
        if not category_id:
            raise ValueError(
                "IKEA listing URL must end in a category token such as 'st004' or '10451'"
            )
        yield self._api_request(category_id, category_url, page=1)

    def _api_request(self, category_id: str, category_url: str, *, page: int):
        body = {
            "searchParameters": {"input": category_id, "type": "CATEGORY"},
            "isUserLoggedIn": False,
            "isB2B": False,
            "considerationLevel": "HIGH_TECHNICAL",
            "listingABTest": True,
            "components": [
                {
                    "component": "PRIMARY_AREA",
                    "columns": 4,
                    "types": {
                        "main": "PRODUCT",
                        "breakouts": [
                            "PLANNER",
                            "LOGIN_REMINDER",
                            "MATTRESS_WARRANTY",
                            "AFFORDABILITY",
                            "OFFERS",
                            "NEW_PRODUCT",
                        ],
                    },
                    "filterConfig": {"max-num-filters": 4},
                    "window": {"size": self.PAGE_SIZE, "offset": (page - 1) * self.PAGE_SIZE},
                    "allVariants": False,
                    "forceFilterCalculation": True,
                }
            ],
        }
        return scrapy.Request(
            self.API_URL,
            method="POST",
            body=json.dumps(body, separators=(",", ":")),
            headers={
                "Accept": "application/json",
                "Content-Type": "text/plain;charset=UTF-8",
                "Origin": "https://www.ikea.com",
                "Referer": category_url,
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "Chrome/140.0.0.0 Safari/537.36"
                ),
            },
            callback=self.parse,
            meta={"page": page, "category_id": category_id, "category_url": category_url},
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response, **kwargs):
        page = int(response.meta["page"])
        category_id = response.meta["category_id"]
        category_url = response.meta["category_url"]
        if response.status != 200:
            raise RuntimeError(f"IKEA SIK request failed with HTTP {response.status}: {response.url}")
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError("IKEA SIK returned a non-JSON response") from exc

        if payload.get("component") == "PRIMARY_AREA":
            primary = payload
        else:
            primary = next(
                (
                    result
                    for result in payload.get("results", [])
                    if result.get("component") == "PRIMARY_AREA"
                ),
                None,
            )
        if not primary:
            raise RuntimeError("IKEA SIK response is missing PRIMARY_AREA; schema may have changed")

        products = [entry["product"] for entry in primary.get("items", []) if entry.get("product")]
        if not products and page == 1:
            raise RuntimeError(
                f"IKEA category {category_id!r} returned zero products; it may be a hub-only URL"
            )

        new_products = 0
        for product in products:
            item_id = str(product.get("itemNo") or product.get("id") or "").strip()
            if not item_id:
                # A product without an identifier cannot be deduplicated or linked; fail
                # loudly instead of silently exporting nothing and stopping pagination.
                raise RuntimeError(
                    f"IKEA SIK product entry on page {page} is missing itemNo/id; "
                    "schema may have changed"
                )
            if item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            new_products += 1
            yield self._product_item(product, item_id, category_id, category_url, page)

        window = primary.get("metadata_window") or primary.get("metadata") or {}
        total = (window.get("itemsPerType") or {}).get("PRODUCT") or window.get("max") or 0
        end = int(window.get("end") or page * self.PAGE_SIZE)
        if page < self.max_pages and new_products and end < int(total):
            yield self._api_request(category_id, category_url, page=page + 1)

    @staticmethod
    def _product_item(
        product: dict[str, Any], item_id: str, category_id: str, category_url: str, page: int
    ) -> dict[str, Any]:
        price = product.get("salesPrice") or {}
        images = [image.get("url") for image in product.get("allProductImage", []) if image.get("url")]
        badge = product.get("badge") or product.get("itemTag")
        return {
            "category": category_id,
            "item_id": item_id,
            "title": product.get("name"),
            "product_type": product.get("typeName"),
            "dimensions": product.get("itemMeasureReferenceText"),
            "url": product.get("pipUrl"),
            "image_url": product.get("mainImageUrl"),
            "image_urls": images,
            "price": price.get("numeral"),
            "currency": price.get("currencyCode"),
            "rating": product.get("ratingValue"),
            "reviews_count": product.get("ratingCount"),
            "badge": badge.get("text") if isinstance(badge, dict) else badge,
            "design": product.get("validDesignText"),
            "availability": "InStock" if product.get("onlineSellable") else "OutOfStock",
            "page": page,
            "category_url": category_url,
            "source": "ikea_sik_search",
            "raw": product,
        }

    @staticmethod
    def _category_id(url: str) -> str | None:
        match = re.search(r"-([a-z]*\d+)/?(?:\?.*)?$", url)
        return match.group(1) if match else None
