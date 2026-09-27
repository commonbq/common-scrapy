from __future__ import annotations

import json
import re
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


ANTHROPOLOGIE_CATEGORIES = {
    "new": {
        "new-arrivals": "https://www.anthropologie.com/new-arrivals",
    },
    "top-rated": {
        "all": "https://www.anthropologie.com/top-rated-products",
    },
    "dresses": {
        "all": "https://www.anthropologie.com/dress-shop-external",
    },
    "clothing": {
        "all": "https://www.anthropologie.com/clothes",
        "shop-all": "https://www.anthropologie.com/womens-clothing",
    },
    "shoes": {
        "all": "https://www.anthropologie.com/shoes",
    },
    "accessories": {
        "all": "https://www.anthropologie.com/shoes-accessories",
    },
    "weddings": {
        "all": "https://www.anthropologie.com/bhldn-weddings",
    },
    "home-furniture": {
        "all": "https://www.anthropologie.com/house-home",
    },
    "beauty": {
        "all": "https://www.anthropologie.com/beauty-wellness",
    },
    "maeve": {
        "all": "https://www.anthropologie.com/maeve",
    },
    "gifts-holiday": {
        "all": "https://www.anthropologie.com/all-gifts",
    },
    "sale": {
        "all": "https://www.anthropologie.com/sale-all",
    },
}


class AnthropologieListingSpider(BaseListingSpider):
    """Anthropologie listing spider using category-page JSON-LD."""

    name = "anthropologie_listing"
    allowed_domains = ["anthropologie.com", "www.anthropologie.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = ANTHROPOLOGIE_CATEGORIES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def _selected_subcategories(self) -> dict[str, str]:
        if self.category in self.categories:
            return self.categories[self.category]
        available = ", ".join(self.available_categories())
        raise ValueError(
            f"Unknown category '{self.category}'. Available categories: {available}"
        )

    def start_requests(self):
        self._seen_products.clear()
        for subcategory, listing_url in self._selected_subcategories().items():
            yield scrapy.Request(
                self._page_url(listing_url, 1),
                callback=self.parse,
                headers=self._headers(),
                meta={
                    "page": 1,
                    "category": self.category,
                    "subcategory": subcategory,
                    "listing_url": listing_url,
                },
            )

    def parse(self, response: scrapy.http.Response):
        if self._is_blocked_response(response):
            self.logger.warning(
                "Anthropologie listing blocked (status=%s url=%s)",
                response.status,
                response.url,
            )
            return

        page = int(response.meta.get("page", 1))
        products = self._extract_products(response)
        yielded = 0
        for product in products:
            item_id = product["item_id"]
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yielded += 1
            yield {
                **product,
                "category": response.meta.get("category"),
                "subcategory": response.meta.get("subcategory"),
                "listing_url": response.meta.get("listing_url") or response.url,
                "page": page,
                "source": "anthropologie_jsonld_itemlist",
                "mode": "category",
            }

        if yielded and page < self._max_pages_limit():
            yield scrapy.Request(
                self._page_url(
                    response.meta.get("listing_url") or response.url, page + 1
                ),
                callback=self.parse,
                headers=self._headers(),
                meta={**response.meta, "page": page + 1},
            )

    @classmethod
    def _extract_products(cls, response: scrapy.http.Response) -> list[dict]:
        products: list[dict] = []
        for payload in cls._jsonld_payloads(response):
            nodes = payload if isinstance(payload, list) else [payload]
            for node in nodes:
                if not isinstance(node, dict) or node.get("@type") != "ItemList":
                    continue
                for entry in node.get("itemListElement") or []:
                    if not isinstance(entry, dict):
                        continue
                    item = entry.get("item")
                    if not isinstance(item, dict) or item.get("@type") != "Product":
                        continue
                    url = item.get("url")
                    if not isinstance(url, str) or not url:
                        continue
                    canonical_url = urljoin(response.url, url)
                    item_id = cls._item_id(canonical_url)
                    offers = item.get("offers") if isinstance(item.get("offers"), dict) else {}
                    products.append(
                        {
                            "item_id": item_id,
                            "title": item.get("name"),
                            "url": canonical_url,
                            "price": cls._to_float(offers.get("price")),
                            "original_price": None,
                            "currency": offers.get("priceCurrency"),
                            "brand": cls._brand(item.get("brand")),
                            "rating": cls._rating(item.get("aggregateRating")),
                            "reviews_count": cls._reviews_count(
                                item.get("aggregateRating")
                            ),
                            "image_url": cls._image_url(item.get("image"), response.url),
                            "raw": None,
                        }
                    )
        return products

    @staticmethod
    def _jsonld_payloads(response: scrapy.http.Response):
        for raw in response.xpath('//script[@type="application/ld+json"]/text()').getall():
            try:
                yield json.loads(raw)
            except (TypeError, ValueError):
                continue

    @staticmethod
    def _item_id(url: str) -> str:
        match = re.search(r"/shop/([^?/#]+)", url)
        return match.group(1) if match else url

    @staticmethod
    def _brand(value) -> str:
        if isinstance(value, dict):
            value = value.get("name")
        return value if isinstance(value, str) and value else "Anthropologie"

    @staticmethod
    def _rating(value) -> float | None:
        if not isinstance(value, dict):
            return None
        return AnthropologieListingSpider._to_float(value.get("ratingValue"))

    @staticmethod
    def _reviews_count(value) -> int | None:
        if not isinstance(value, dict):
            return None
        raw = value.get("reviewCount") or value.get("ratingCount")
        try:
            return int(raw) if raw is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _image_url(value, base_url: str) -> str | None:
        if isinstance(value, list):
            value = value[0] if value else None
        if isinstance(value, dict):
            value = value.get("url") or value.get("contentUrl")
        return urljoin(base_url, value) if isinstance(value, str) and value else None

    @staticmethod
    def _to_float(value) -> float | None:
        if isinstance(value, bool):
            return None
        try:
            return float(str(value).replace("$", "").replace(",", ""))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query, keep_blank_values=True)
        if page > 1:
            query["page"] = [str(page)]
        else:
            query.pop("page", None)
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    def _max_pages_limit(self) -> int:
        try:
            return max(int(self.max_pages), 1)
        except (TypeError, ValueError):
            return 1

    @staticmethod
    def _is_blocked_response(response: scrapy.http.Response) -> bool:
        lowered = (response.text or "").lower()
        return response.status >= 400 or any(
            marker in lowered
            for marker in (
                "access denied",
                "verify you are human",
                "request blocked",
                "temporarily unavailable",
            )
        )

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
