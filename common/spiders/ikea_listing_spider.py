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

    SIK_BASE_URL = "https://sik.search.blue.cdtapps.com/us/en"
    # IKEA validates the SIK query version server-side: an unknown value returns
    # HTTP 400 rather than an empty result set, so it is pinned to the last known
    # good value but overridable with `-a sik_version=` when IKEA rotates it.
    DEFAULT_SIK_VERSION = "20250507"
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
            "item_no_global",
            "product_class",
            "department",
            "category_path",
            "business_area",
            "product_type_tag",
            "variant_count",
            "colors",
            "quick_facts",
            "image_alt",
            "page",
            "category_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()
        self.sik_version = str(
            kwargs.get("sik_version") or self.DEFAULT_SIK_VERSION
        ).strip()

    @property
    def api_url(self) -> str:
        return f"{self.SIK_BASE_URL}/search?c=listaf&v={self.sik_version}"

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
            self.api_url,
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
            raise RuntimeError(
                f"IKEA SIK request failed with HTTP {response.status}: {response.url}.{self._version_hint()}"
            )
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
            # A retired SIK version is the most common cause: the live API answers
            # `{"status":400,...,"detail":"Invalid API version"}`, which carries no
            # PRIMARY_AREA (and may arrive as 200 through a proxy).
            raise RuntimeError(
                f"IKEA SIK response is missing PRIMARY_AREA; schema may have changed."
                f"{self._version_hint()}"
            )

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
        product: dict[str, Any],
        item_id: str,
        category_id: str,
        category_url: str,
        page: int,
    ) -> dict[str, Any]:
        price = product.get("salesPrice") or {}
        # The API reports the canonical category path for each product, which can
        # differ from the crawled category (cross-listed / variant entries).
        category_path = product.get("categoryPath") or []
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
            "item_no_global": product.get("itemNoGlobal"),
            "product_class": product.get("filterClass"),
            "department": category_path[0].get("name") if category_path else None,
            "category_path": [entry.get("name") for entry in category_path] or None,
            "business_area": (product.get("businessStructure") or {}).get("productAreaName"),
            "product_type_tag": (product.get("optimizelyAttributes") or {}).get("PRODUCT_TYPE"),
            "variant_count": (product.get("gprDescription") or {}).get("numberOfVariants"),
            "colors": [color.get("name") for color in product.get("colors") or []],
            "quick_facts": [
                fact.get("name") for fact in product.get("quickFacts") or [] if fact.get("name")
            ]
            or None,
            "image_alt": product.get("mainImageAlt"),
            "page": page,
            "category_url": category_url,
            "source": "ikea_sik_search",
            "raw": product,
        }

    def _version_hint(self) -> str:
        return (
            " IKEA validates the SIK query version and rejects unknown values with"
            ' {"detail":"Invalid API version"}; retry with'
            f" -a sik_version=<current value> (currently {self.sik_version})."
        )
    @staticmethod
    def _category_id(url: str) -> str | None:
        match = re.search(r"-([a-z]*\d+)/?(?:\?.*)?$", url)
        return match.group(1) if match else None
