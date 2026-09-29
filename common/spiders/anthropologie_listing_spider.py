from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.anthropologie_categories import flattened_categories
from common.spiders.base_listing_spider import BaseListingSpider


class AnthropologieListingSpider(BaseListingSpider):
    """Extract product listings from Anthropologie's Pinia SSR hydration state."""

    name = "anthropologie_listing"
    allowed_domains = ["www.anthropologie.com", "anthropologie.com", "127.0.0.1"]
    categories = flattened_categories()

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category",
            "item_id",
            "style_number",
            "title",
            "brand",
            "url",
            "image_url",
            "price",
            "original_price",
            "currency",
            "availability",
            "rating",
            "reviews_count",
            "color",
            "color_count",
            "badges",
            "source",
            "category_url",
            "page",
            "position",
            "raw",
        ]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_product_ids: set[str] = set()

    def start_requests(self):
        yield scrapy.Request(
            self._with_page(self.resolve_target_url(), 1),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        raw_state = response.css("script#urbnInitialPiniaState::text").get()
        if not raw_state:
            raise RuntimeError(f"No Anthropologie urbnInitialPiniaState found at {response.url}")
        try:
            state = json.loads(json.loads(raw_state.strip()))
        except (TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Invalid Anthropologie Pinia state at {response.url}") from exc

        category_state = state.get("category") or {}
        page = int(category_state.get("currentPage") or response.meta.get("page") or 1)
        page_state = (category_state.get("pages") or {}).get(str(page)) or {}
        tiles = (page_state.get("wrapper") or {}).get("tiles") or []
        product_tiles = [tile for tile in tiles if isinstance(tile, dict) and tile.get("recordType") == "PRODUCT"]
        if not product_tiles:
            raise RuntimeError(f"No Anthropologie Pinia product tiles found at {response.url}")

        for position, tile in enumerate(product_tiles, 1):
            product = tile.get("product") or {}
            item_id = product.get("productId") or product.get("styleNumber")
            if not item_id or item_id in self.seen_product_ids:
                continue
            self.seen_product_ids.add(item_id)
            sku = tile.get("skuInfo") or {}
            reviews = tile.get("reviews") or {}
            color = tile.get("faceOutColorCode") or product.get("defaultColorCode")
            image = tile.get("faceOutImage") or product.get("defaultImage")
            slug = product.get("productSlug")
            yield {
                "category": response.meta.get("category"),
                "item_id": item_id,
                "style_number": product.get("styleNumber"),
                "title": product.get("displayName"),
                "brand": product.get("brand"),
                "url": f"https://www.anthropologie.com/shop/{slug}?color={color}&type=STANDARD" if slug else None,
                "image_url": f"https://images.urbndata.com/is/image/Anthropologie/{image}?$an-category$" if image else None,
                "price": self._number(sku.get("salePriceLow") or sku.get("listPriceLow")),
                "original_price": self._number(sku.get("listPriceLow")),
                "currency": "USD",
                "availability": "InStock" if sku.get("hasAvailableSku") else "OutOfStock",
                "rating": self._number(reviews.get("averageRating")),
                "reviews_count": reviews.get("count"),
                "color": color,
                "color_count": len((product.get("facets") or {}).get("colors") or []),
                "badges": [badge.get("type") for badge in product.get("badges") or [] if isinstance(badge, dict)],
                "source": "urbn_pinia_hydration",
                "category_url": response.url,
                "page": page,
                "position": position,
                "raw": tile,
            }

        total_pages = int(category_state.get("totalPages") or 1)
        if page < min(total_pages, self.max_pages):
            next_page = page + 1
            yield scrapy.Request(
                self._with_page(response.url, next_page),
                callback=self.parse,
                headers=self._headers(),
                meta={"category": response.meta.get("category"), "page": next_page},
            )

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
