from __future__ import annotations

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.staples_categories import STAPLES_CATEGORIES


class StaplesListingSpider(BaseListingSpider):
    """Staples category listings from the server-rendered Next.js state."""

    name = "staples_listing"
    allowed_domains = ["staples.com", "www.staples.com", "localhost", "127.0.0.1"]
    categories = STAPLES_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "item_id", "title", "brand",
            "model", "url", "image_url", "price", "currency", "rating",
            "reviews_count", "in_stock", "available_quantity", "inventory_mode",
            "min_delivery_date", "max_delivery_date", "supercategory_id",
            "supercategory_name", "category_id", "category_name", "department_id",
            "department_name", "class_id", "class_name", "page", "position",
            "total_count", "items_per_page", "search_engine", "source_url", "source", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self._html_headers(),
            meta={
                "category": self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "page": 1,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Staples listing returned HTTP {response.status}: {response.url}")

        state = self._extract_next_data(response)
        if not isinstance(state, dict):
            raise RuntimeError(f"No valid Staples __NEXT_DATA__ hydration found at {response.url}")
        search = self._search_state(state)
        if not isinstance(search, dict):
            raise RuntimeError(f"Staples hydration has no searchState object at {response.url}")
        products = search.get("productTileData")
        if not isinstance(products, list):
            raise RuntimeError(f"Staples searchState has no list-valued productTileData at {response.url}")
        if not products:
            raise RuntimeError(f"Staples listing returned zero products at {response.url}")

        page = self._integer(search.get("pageNumber")) or int(response.meta.get("page", 1))
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("itemId") or "")
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, search, response, page, position)

        if page >= self.max_pages:
            return
        next_url = response.css('link[rel="next"]::attr(href)').get()
        if next_url:
            yield response.follow(
                next_url,
                callback=self.parse,
                headers=self._html_headers(),
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _extract_next_data(response: scrapy.http.Response) -> dict | None:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            return None
        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _search_state(state: dict) -> dict | None:
        props = state.get("props")
        store = props.get("initialStateOrStore") if isinstance(props, dict) else None
        search = store.get("searchState") if isinstance(store, dict) else None
        return search if isinstance(search, dict) else None

    def _item(self, product, search, response, page, position):
        hierarchy = product.get("hierarchy") if isinstance(product.get("hierarchy"), dict) else {}
        availability = product.get("itemAvailability") if isinstance(product.get("itemAvailability"), dict) else {}
        supercategory = self._mapping(hierarchy.get("supercategory"))
        category = self._mapping(hierarchy.get("category"))
        department = self._mapping(hierarchy.get("department"))
        product_class = self._mapping(hierarchy.get("class"))
        out_of_stock = product.get("isOutOfStock")
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": str(product.get("itemId")),
            "title": product.get("title"),
            "brand": product.get("brandName") or product.get("manufacturerName"),
            "model": product.get("model"),
            "url": urljoin("https://www.staples.com/", product.get("url")) if product.get("url") else None,
            "image_url": product.get("image"),
            "price": self._number(product.get("priceValue"), product.get("price")),
            "currency": "USD",
            "rating": self._number(product.get("rating")),
            "reviews_count": self._integer(product.get("ratingCount")),
            "in_stock": not out_of_stock if isinstance(out_of_stock, bool) else None,
            "available_quantity": self._integer(availability.get("availableQuantity")),
            "inventory_mode": availability.get("inventoryMode"),
            "min_delivery_date": availability.get("minDeliveryDate"),
            "max_delivery_date": availability.get("maxDeliveryDate"),
            "supercategory_id": supercategory.get("id"),
            "supercategory_name": supercategory.get("name"),
            "category_id": category.get("id"),
            "category_name": category.get("name"),
            "department_id": department.get("id"),
            "department_name": department.get("name"),
            "class_id": product_class.get("id"),
            "class_name": product_class.get("name"),
            "page": page,
            "position": position,
            "total_count": self._integer(search.get("totalCount")),
            "items_per_page": self._integer(search.get("itemsPerPage")),
            "search_engine": search.get("searchEngine"),
            "source_url": response.url,
            "source": "staples_next_data",
            "raw": product,
        }

    @staticmethod
    def _mapping(value):
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _number(value, fallback=None):
        candidate = value if value is not None else fallback
        if isinstance(candidate, str):
            match = re.search(r"-?\d[\d,]*(?:\.\d+)?", candidate)
            candidate = match.group(0).replace(",", "") if match else None
        try:
            return float(candidate) if candidate is not None and not isinstance(candidate, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _html_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
