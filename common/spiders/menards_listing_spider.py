from __future__ import annotations

import html
import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.menards_categories import MENARDS_CATEGORIES


class MenardsListingSpider(BaseListingSpider):
    """Menards listings from the storefront's category JSON endpoint."""

    name = "menards_listing"
    allowed_domains = ["menards.com", "www.menards.com", "127.0.0.1"]
    categories = [{"category": key, "url": url} for key, url in MENARDS_CATEGORIES.items()]
    api_url = "https://www.menards.com/main/search/category.ajx"
    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "sku", "title", "brand", "url", "image_url",
            "price", "original_price", "currency", "availability", "rating",
            "reviews_count", "page", "position", "total_count", "category_url", "source",
        ],
        "HTTPERROR_ALLOW_ALL": True,
        "COOKIES_ENABLED": True,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen_ids: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield scrapy.Request(category_url, callback=self.parse_category,
            headers={"Accept": "text/html,application/xhtml+xml"},
            meta={"category": self.category, "category_url": category_url})

    def parse_category(self, response):
        self._assert_response(response, expect_json=False)
        category_id = self._category_id(response.url, response.text)
        yield self._api_request(category_id, response.meta["category"], response.meta["category_url"], 1)

    def parse_api(self, response):
        self._assert_response(response, expect_json=True)
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Menards API returned malformed JSON at {response.url}") from exc
        result = payload.get("searchResult")
        if not isinstance(result, dict) or not isinstance(result.get("items"), list):
            raise RuntimeError(f"Menards API response is missing searchResult.items at {response.url}")
        items = result["items"]
        page = response.meta["page"]
        total = self._integer(result.get("totalItems") or result.get("totalCount"))
        emitted = 0
        for position, product in enumerate(items, 1):
            if not isinstance(product, dict):
                continue
            item = self._item(product, response.meta, position, total)
            if not item["item_id"] or item["item_id"] in self.seen_ids:
                continue
            self.seen_ids.add(item["item_id"])
            emitted += 1
            yield item
        if items and emitted and page < self.max_pages and (total is None or page * len(items) < total):
            yield self._api_request(response.meta["category_id"], response.meta["category"], response.meta["category_url"], page + 1)

    def _api_request(self, category_id, category, category_url, page):
        body = {"categoryId": category_id, "firstRequest": page == 1, "page": page,
                "sortBy": "BEST_MATCH", "selectedFacets": [], "inStockToday": False}
        return scrapy.Request(self.api_url, method="POST", body=json.dumps(body, separators=(",", ":")),
            headers={"Accept": "application/json", "Content-Type": "application/json", "Referer": category_url},
            callback=self.parse_api, dont_filter=True,
            meta={"proxy": self._api_proxy(), "category_id": category_id, "category": category,
                  "category_url": category_url, "page": page})

    def _api_proxy(self):
        proxy = self.settings.get("PROXY") if hasattr(self, "settings") else None
        if not isinstance(proxy, str) or "scrapeops" not in proxy.lower():
            return proxy
        parts = urlsplit(proxy)
        if not parts.username or parts.password is None or not parts.hostname:
            return proxy
        options = parts.username.split(".")
        keys = {option.split("=", 1)[0] for option in options}
        for option in ("country=us", "residential=true", "bypass=5"):
            if option.split("=", 1)[0] not in keys:
                options.append(option)
        port = f":{parts.port}" if parts.port else ""
        netloc = f"{'.'.join(options)}:{parts.password}@{parts.hostname}{port}"
        return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))

    @staticmethod
    def _category_id(url, text):
        match = re.search(r"/c-(\d+)\.htm", url)
        if not match:
            match = re.search(r'["\']categoryId["\']\s*:\s*["\']?(\d+)', html.unescape(text))
        if not match:
            raise RuntimeError(f"Could not resolve Menards categoryId from {url}")
        return match.group(1)

    @staticmethod
    def _assert_response(response, *, expect_json):
        lowered = response.text[:10000].lower()
        blocked = any(x in lowered for x in ("incapsula", "captcha", "pardon the interruption", "failed to get successful response"))
        category_contract = "search-parameters" in response.text.lower()
        if response.status != 200 or (blocked and (expect_json or not category_contract)):
            raise RuntimeError(f"Menards request was blocked or failed ({response.status}) at {response.url}")
        if expect_json and lowered.lstrip().startswith("<"):
            raise RuntimeError(f"Menards API returned HTML instead of JSON at {response.url}")

    @classmethod
    def _item(cls, product, meta, position, total):
        item_id = cls._first(product, "productId", "id", "sku", "skuId", "partNumber")
        path = cls._first(product, "productUrl", "url", "pdpUrl", "link")
        image = cls._first(product, "imageUrl", "image", "primaryImage", "thumbnail")
        price = product.get("price") if isinstance(product.get("price"), dict) else {}
        rating = product.get("rating") if isinstance(product.get("rating"), dict) else {}
        return {
            "category": meta["category"], "item_id": str(item_id) if item_id is not None else None,
            "sku": cls._first(product, "sku", "skuId", "modelNumber", "partNumber"),
            "title": cls._first(product, "title", "name", "productName"),
            "brand": cls._first(product, "brand", "brandName", "manufacturer"),
            "url": urljoin("https://www.menards.com", path) if path else None,
            "image_url": image.get("url") if isinstance(image, dict) else image,
            "price": cls._number(cls._first(price, "current", "value", "salePrice") or cls._first(product, "currentPrice", "salePrice")),
            "original_price": cls._number(cls._first(price, "regular", "original", "listPrice") or cls._first(product, "regularPrice", "originalPrice")),
            "currency": cls._first(price, "currency", "currencyCode") or product.get("currency") or "USD",
            "availability": cls._first(product, "availability", "stockStatus", "inventoryStatus"),
            "rating": cls._number(cls._first(rating, "value", "average") or cls._first(product, "averageRating", "ratingValue")),
            "reviews_count": cls._integer(cls._first(rating, "count", "reviewCount") or cls._first(product, "reviewCount", "reviewsCount")),
            "page": meta["page"], "position": position, "total_count": total,
            "category_url": meta["category_url"], "source": "menards_category_api",
        }

    @staticmethod
    def _first(mapping, *keys):
        return next((mapping[key] for key in keys if isinstance(mapping, dict) and mapping.get(key) is not None), None)

    @staticmethod
    def _number(value):
        try:
            return float(str(value).replace("$", "").replace(",", "")) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
