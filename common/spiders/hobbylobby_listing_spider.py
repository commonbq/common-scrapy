from __future__ import annotations

"""Hobby Lobby products from the server-rendered InstantSearch bootstrap."""

import json
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.hobbylobby_categories import HOBBY_LOBBY_CATEGORIES

SITE_BASE = "https://www.hobbylobby.com"
BOOTSTRAP_MARKER = 'InstantSearchInitialResults'
SOURCE = "hobbylobby_instantsearch_bootstrap"


class HobbylobbyListingSpider(BaseListingSpider):
    """Extract the authoritative Algolia InstantSearch SSR state only."""

    name = "hobbylobby_listing"
    allowed_domains = ["hobbylobby.com", "www.hobbylobby.com"]
    require_category_arg = False
    categories = [
        {"category": category, "url": url}
        for category, url in HOBBY_LOBBY_CATEGORIES.items()
    ]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_url", "item_id", "sku", "product_id",
            "product_key", "title", "url", "pdp_url", "brand", "description",
            "price", "lowest_price", "highest_price", "original_price",
            "highest_original_price", "discounted_price", "discount_name",
            "discount_names", "currency", "in_stock", "availability",
            "online_status", "is_new", "on_sale", "assorted", "product_unit",
            "volume", "type", "department", "product_category", "subcategory",
            "category_names", "categories", "category_keys", "quantity", "medium",
            "color", "color_family", "material", "rating", "reviews_count",
            "image", "images", "vendor_sku", "product_online_date", "online_date",
            "last_modified_at", "active_variant_count", "back_in_stock_eligible",
            "your_price", "approval_status", "page", "position", "total_count",
            "total_pages", "source_url", "source", "raw", "timestamp",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self.resolve_target_url()
        self._seen_ids: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield self._request(category_url, category_url, 1)

    def _request(self, category_url: str, listing_url: str, page: int):
        settings = getattr(self, "settings", None)
        proxy = settings.get("PROXY") if settings is not None else None
        return scrapy.Request(
            self._page_url(listing_url, page),
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"category_url": category_url, "listing_url": listing_url, "page": page},
            meta={"proxy": proxy},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if page <= 1:
            query.pop("page", None)
        else:
            query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def parse(self, response, category_url: str, listing_url: str, page: int):
        if response.status != 200:
            raise RuntimeError(f"Hobby Lobby listing returned HTTP {response.status}: {response.url}")

        payload = self._extract_bootstrap(response.text, response.url)
        result = self._search_result(payload, response.url)
        hits = result.get("hits")
        if not isinstance(hits, list):
            raise RuntimeError(
                f"Hobby Lobby InstantSearch result has no hits list at {response.url}"
            )

        total_count = self._integer(result.get("nbHits"))
        total_pages = self._integer(result.get("nbPages")) or 1
        emitted = 0
        for position, hit in enumerate(hits, start=1):
            if not isinstance(hit, dict):
                continue
            item_id = str(hit.get("objectID") or hit.get("sku") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            emitted += 1
            yield self._item(
                hit, item_id, response.url, category_url, page, position,
                total_count, total_pages,
            )

        if emitted and page < min(total_pages, self.max_pages):
            yield self._request(category_url, listing_url, page + 1)

    @staticmethod
    def _extract_bootstrap(text: str, url: str) -> dict[str, Any]:
        """Decode the assignment with JSONDecoder brace matching, never regex."""
        search_from = 0
        decoder = json.JSONDecoder()
        while True:
            marker = text.find(BOOTSTRAP_MARKER, search_from)
            if marker < 0:
                break
            assignment = text.find("=", marker)
            if assignment < 0:
                break
            start = assignment + 1
            while start < len(text) and text[start].isspace():
                start += 1
            try:
                value, _ = decoder.raw_decode(text, start)
            except json.JSONDecodeError:
                search_from = marker + len(BOOTSTRAP_MARKER)
                continue
            if isinstance(value, dict):
                return value
            search_from = marker + len(BOOTSTRAP_MARKER)
        raise RuntimeError(
            "Hobby Lobby InstantSearch bootstrap was absent or invalid at "
            f"{url}; no HTML-card or JSON-LD fallback is used"
        )

    @staticmethod
    def _search_result(payload: dict[str, Any], url: str) -> dict[str, Any]:
        for index_state in payload.values():
            if not isinstance(index_state, dict):
                continue
            for result in index_state.get("results") or []:
                if isinstance(result, dict) and isinstance(result.get("hits"), list):
                    return result
        raise RuntimeError(f"Hobby Lobby InstantSearch results were absent at {url}")

    def _item(
        self, hit: dict[str, Any], item_id: str, source_url: str,
        category_url: str, page: int, position: int,
        total_count: int | None, total_pages: int,
    ) -> dict[str, Any]:
        image_urls = [
            image.get("url") for image in (hit.get("images") or [])
            if isinstance(image, dict) and image.get("url")
        ]
        return {
            "category": self.category or "custom",
            "category_url": category_url,
            "item_id": item_id,
            "sku": hit.get("sku"),
            "product_id": hit.get("productID"),
            "product_key": hit.get("productKey"),
            "title": hit.get("name") or hit.get("productName"),
            "url": self._absolute(hit.get("variantUrl")),
            "pdp_url": self._absolute(hit.get("pdpUrl")),
            "brand": hit.get("brand"),
            "description": hit.get("product.description") or hit.get("details"),
            "price": self._number(hit.get("variant.price")),
            "lowest_price": self._number(hit.get("product.lowestPrice")),
            "highest_price": self._number(hit.get("product.highestPrice")),
            "original_price": self._number(hit.get("product.lowestOriginalPrice")),
            "highest_original_price": self._number(hit.get("product.highestOriginalPrice")),
            "discounted_price": self._number(hit.get("sku.discountedPrice")),
            "discount_name": hit.get("sku.discountName"),
            "discount_names": hit.get("product.discountNames") or [],
            "currency": "USD",
            "in_stock": hit.get("isInStock"),
            "availability": hit.get("availability"),
            "online_status": hit.get("onlineStatus"),
            "is_new": hit.get("isNew"),
            "on_sale": hit.get("on_sale"),
            "assorted": hit.get("assorted"),
            "product_unit": hit.get("product-unit"),
            "volume": hit.get("volume"),
            "type": hit.get("type"),
            "department": hit.get("department"),
            "product_category": hit.get("category"),
            "subcategory": hit.get("subcategory"),
            "category_names": hit.get("categoryNames") or [],
            "categories": hit.get("categories") or {},
            "category_keys": hit.get("categoryKeys") or [],
            "quantity": hit.get("quantity"),
            "medium": hit.get("medium") or [],
            "color": hit.get("color"),
            "color_family": hit.get("color-family"),
            "material": hit.get("material"),
            "rating": self._number(hit.get("ratings.average")),
            "reviews_count": self._integer(hit.get("ratings.count")),
            "image": image_urls[0] if image_urls else None,
            "images": image_urls,
            "vendor_sku": hit.get("vendor-sku"),
            "product_online_date": hit.get("product-online-date"),
            "online_date": hit.get("onlineDate"),
            "last_modified_at": hit.get("lastModifiedAt"),
            "active_variant_count": self._integer(hit.get("activeVariantCount")),
            "back_in_stock_eligible": hit.get("backInStockEligible"),
            "your_price": hit.get("yourPrice"),
            "approval_status": hit.get("approvalStatus"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": source_url,
            "source": SOURCE,
            "raw": hit,
            "timestamp": self.job_timestamp,
        }

    @staticmethod
    def _absolute(value: Any) -> str | None:
        return urljoin(SITE_BASE, value) if isinstance(value, str) and value else None

    @staticmethod
    def _number(value: Any) -> float | None:
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value: Any) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
