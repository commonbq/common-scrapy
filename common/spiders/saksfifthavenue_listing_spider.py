from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SaksfifthavenueListingSpider(BaseListingSpider):
    """Saks listings from the server-rendered Salesforce product grid."""

    name = "saksfifthavenue_listing"
    allowed_domains = ["saksfifthavenue.com", "www.saksfifthavenue.com", "localhost", "127.0.0.1"]

    SAKS_CATEGORIES = {
        "women": {"apparel": "https://www.saksfifthavenue.com/c/women-s-apparel"},
        "men": {"all": "https://www.saksfifthavenue.com/c/men"},
        "shoes": {"all": "https://www.saksfifthavenue.com/c/shoes"},
        "handbags": {"all": "https://www.saksfifthavenue.com/c/handbags"},
        "jewelry-accessories": {"all": "https://www.saksfifthavenue.com/c/jewelry-accessories"},
        "beauty": {"all": "https://www.saksfifthavenue.com/c/beauty"},
        "kids": {"all": "https://www.saksfifthavenue.com/c/kids"},
        "home": {"all": "https://www.saksfifthavenue.com/c/home"},
    }
    categories = SAKS_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category", "subcategory", "item_id", "title", "brand", "url",
            "image_url", "price", "original_price", "currency", "availability",
            "badge", "page", "source_url", "source",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def _selected_subcategories(self) -> dict[str, str]:
        if self.url or self.category_url:
            return {"custom": self.resolve_target_url()}
        try:
            return self.categories[self.category]
        except KeyError:
            available = ", ".join(self.available_categories())
            raise ValueError(f"Unknown category '{self.category}'. Available categories: {available}") from None

    def start_requests(self):
        self._seen_products.clear()
        for subcategory, category_url in self._selected_subcategories().items():
            yield scrapy.Request(
                self._with_page(category_url, 1),
                callback=self.parse,
                meta={"category": self.category, "subcategory": subcategory,
                      "category_url": category_url, "page": 1},
            )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        tiles = response.css("div.product-tile[data-itemid], div.product-tile")
        if not tiles:
            raise ValueError(f"Saks product grid absent (status={response.status}, url={response.url})")

        for tile in tiles:
            item = self._extract_tile(tile, response.url)
            key = item.get("item_id") or item.get("url")
            if not key or key in self._seen_products:
                continue
            self._seen_products.add(key)
            item.update({
                "category": response.meta.get("category"),
                "subcategory": response.meta.get("subcategory"),
                "page": page,
                "source_url": response.url,
                "source": "saks_server_rendered_product_grid",
            })
            yield item

        next_href = response.css('link[rel="next"]::attr(href), a[rel="next"]::attr(href)').get()
        if next_href and page < self.max_pages:
            yield response.follow(next_href, callback=self.parse, meta={**response.meta, "page": page + 1})

    @classmethod
    def _extract_tile(cls, tile: scrapy.Selector, base_url: str) -> dict:
        href = tile.css("a.product-tile-url::attr(href), a.thumb-link::attr(href)").get()
        url = urljoin(base_url, href) if href else None
        item_id = tile.attrib.get("data-itemid") or tile.css("[data-pid]::attr(data-pid), .bf-product-id::text").get()
        if not item_id and url:
            match = re.search(r"-(\d{8,})\.html", url)
            item_id = match.group(1) if match else None
        brand = cls._text(tile.css(".product-brand ::text, .product-brand::text").getall())
        name = cls._text(tile.css(".tile-product-name ::text, .product-description ::text").getall())
        title = name if not brand or name.lower().startswith(brand.lower()) else f"{brand} {name}"
        current = cls._money(cls._text(tile.css(".sales .value::text, .sales::text, .bfx-price::text").getall()))
        original = cls._money(cls._text(tile.css(".strike-through .value::text, .strike-through::text").getall()))
        return {
            "item_id": item_id.strip() if item_id else None,
            "title": title or None,
            "brand": brand or None,
            "url": url,
            "image_url": tile.css("img.tile-image::attr(src), img::attr(data-src), img::attr(src)").get(),
            "price": current,
            "original_price": original,
            "currency": "USD" if current is not None else None,
            "availability": tile.css("[data-availability]::attr(data-availability)").get(),
            "badge": cls._text(tile.css(".product-badge ::text, .badge::text").getall()) or None,
        }

    @staticmethod
    def _text(parts: list[str]) -> str:
        return " ".join(part.strip() for part in parts if part.strip())

    @staticmethod
    def _money(value: str):
        match = re.search(r"([0-9][0-9,]*(?:\.\d+)?)", value or "")
        return float(match.group(1).replace(",", "")) if match else None

    @staticmethod
    def _with_page(url: str, page: int, page_size: int = 24) -> str:
        parts = urlparse(url)
        query = parse_qs(parts.query)
        query.update({"start": [str((page - 1) * page_size)], "sz": [str(page_size)]})
        return urlunparse(parts._replace(query=urlencode(query, doseq=True)))
