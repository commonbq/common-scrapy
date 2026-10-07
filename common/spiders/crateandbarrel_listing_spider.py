from __future__ import annotations

import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.crateandbarrel_categories import CRATEANDBARREL_CATEGORIES


class CrateandbarrelListingSpider(BaseListingSpider):
    """Products hydrated into the first-party React ProductListing component."""

    name = "crateandbarrel_listing"
    allowed_domains = ["crateandbarrel.com", "www.crateandbarrel.com"]
    categories = CRATEANDBARREL_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_TIMEOUT": 120,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "family_id", "title", "brand", "url",
            "image_url", "price", "price_min", "price_max", "regular_price",
            "currency", "rating", "reviews_count", "is_new", "is_free_shipping",
            "colors", "department", "page", "position", "source", "raw",
            "timestamp",
        ],
    }
    _marker = "ReactDOM.hydrate(React.createElement(ProductListing, JSON.parse('"
    _end_marker = "')), document.getElementById"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def resolve_target_url(self) -> str:
        if self.url or self.category_url:
            return self.url or self.category_url
        try:
            return self.categories[self.category]
        except KeyError:
            available = ", ".join(self.available_categories())
            raise ValueError(f"Unknown category '{self.category}'. Available: {available}") from None

    def start_requests(self):
        self._seen.clear()
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, url: str, page: int):
        meta = {"page": page}
        proxy = self._residential_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            self._page_url(url, page), callback=self.parse,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36",
            },
            meta=meta, dont_filter=True,
        )

    def parse(self, response):
        page = int(response.meta["page"])
        try:
            props = self.extract_product_listing(response.text)
        except (ValueError, json.JSONDecodeError) as exc:
            self.logger.warning("ProductListing bootstrap unavailable at %s: %s", response.url, exc)
            return
        products = props.get("productData") or []
        for position, product in enumerate(products, 1):
            item_id = str(product.get("sku") or "")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            colors = [x.get("name") for x in (product.get("colorBar") or {}).get("choices") or [] if x.get("name")]
            price = self._number(product.get("currentPrice"))
            yield {
                "category": self.category, "item_id": item_id,
                "family_id": product.get("familyId"),
                "title": product.get("name") or product.get("title"),
                "brand": "Crate & Barrel",
                "url": urljoin("https://www.crateandbarrel.com", product.get("navigateUrl") or ""),
                "image_url": product.get("imageUrlHighRes") or product.get("imageUrl"),
                "price": price,
                "price_min": self._number(product.get("currentPriceMin")) or price,
                "price_max": self._number(product.get("currentPriceMax")) or price,
                "regular_price": self._number(product.get("regularPrice")),
                "currency": "USD" if price is not None else None,
                "rating": self._number(product.get("ratingValue")),
                "reviews_count": product.get("reviewCount"),
                "is_new": product.get("isNew"),
                "is_free_shipping": product.get("isFreeShipping"),
                "colors": colors, "department": product.get("department"),
                "page": page, "position": position,
                "source": "crateandbarrel_productlisting_bootstrap", "raw": product,
            }
        if products and props.get("hasMoreItems") and page < self.max_pages:
            yield self._request(response.url, page + 1)

    @classmethod
    def extract_product_listing(cls, text: str) -> dict:
        start = text.find(cls._marker)
        if start < 0:
            raise ValueError("React ProductListing marker not found")
        start += len(cls._marker)
        end = text.find(cls._end_marker, start)
        if end < 0:
            raise ValueError("React ProductListing terminator not found")
        return json.loads(cls._decode_js_string(text[start:end]))

    @staticmethod
    def _decode_js_string(value: str) -> str:
        result, i = [], 0
        escapes = {"n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f", "v": "\v", "0": "\0", "'": "'", '"': '"', "\\": "\\"}
        while i < len(value):
            if value[i] != "\\":
                result.append(value[i]); i += 1; continue
            if i + 1 >= len(value):
                result.append("\\"); break
            char = value[i + 1]
            if char == "u" and i + 5 < len(value):
                result.append(chr(int(value[i + 2:i + 6], 16))); i += 6
            elif char == "x" and i + 3 < len(value):
                result.append(chr(int(value[i + 2:i + 4], 16))); i += 4
            elif char in "\r\n":
                i += 2
            else:
                result.append(escapes.get(char, char)); i += 2
        return "".join(result)

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        if page == 1:
            return url
        parts = urlsplit(url)
        path = re.sub(r"/\d+/?$", f"/{page}", parts.path.rstrip("/"))
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, ""))

    def _residential_proxy(self):
        proxy = self.settings.get("PROXY")
        if not proxy:
            return None
        parts = urlsplit(proxy); username = parts.username or ""
        for option in ("residential=true", "bypass=5"):
            if option not in username:
                username = f"{username}.{option}"
        auth = f"{username}:{parts.password}@{parts.hostname}:{parts.port}"
        return urlunsplit((parts.scheme, auth, parts.path, parts.query, parts.fragment))

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None
