from __future__ import annotations

import re
from urllib.parse import urljoin, urlsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


QVC_CATEGORIES = {
    "fashion": ["https://www.qvc.com/c/fashion/-/lglt/c.html"],
}


class QvcListingSpider(BaseListingSpider):
    """Extract QVC listings from the server-rendered category product grid."""

    name = "qvc_listing"
    allowed_domains = ["qvc.com", "www.qvc.com"]
    require_category_arg = False
    categories = QVC_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image_url",
            "price", "original_price", "currency", "rating", "reviews_count",
            "page", "source",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.category:
            raise ValueError(
                f"Provide -a category=<name>. Available categories: {', '.join(self.available_categories())}"
            )
        if not (self.url or self.category_url) and self.category not in self.categories:
            raise ValueError(
                f"Unknown category '{self.category}'. Available categories: {', '.join(self.available_categories())}"
            )
        target_host = urlsplit(self.url or self.category_url or "").hostname
        if target_host and target_host not in self.allowed_domains:
            self.allowed_domains = [*self.allowed_domains, target_host]
        self._seen_ids: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def start_requests(self):
        urls = [self.url or self.category_url] if (self.url or self.category_url) else self.categories[self.category]
        for url in urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers=self._headers(),
                meta={"category": self.category, "page": 1, "handle_httpstatus_all": True},
            )

    def parse(self, response: scrapy.http.Response):
        cards = response.css("article.product-card[data-product-id]")
        if not cards:
            self.logger.warning(
                "QVC product grid unavailable: status=%s url=%s", response.status, response.url
            )
            return

        page = int(response.meta.get("page") or 1)
        for card in cards:
            item_id = (card.attrib.get("data-product-id") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            yield {
                "category": response.meta.get("category"),
                "item_id": item_id,
                "title": self._text(card.css(".product-card__title::text").get()),
                "brand": self._text(card.css(".product-card__brand::text").get()),
                "url": urljoin(response.url, card.css("a.product-card__link::attr(href)").get() or ""),
                "image_url": urljoin(response.url, card.css("img.product-card__image::attr(src)").get() or ""),
                "price": self._number(card.css(".product-card__price::attr(data-price)").get()),
                "original_price": self._number(card.css(".product-card__original-price::attr(data-price)").get()),
                "currency": card.css(".product-card__price::attr(data-currency)").get() or "USD",
                "rating": self._number(card.css(".product-card__rating::attr(data-rating)").get()),
                "reviews_count": self._integer(card.css(".product-card__rating::attr(data-review-count)").get()),
                "page": page,
                "source": "qvc_server_rendered_product_grid",
            }

        next_href = response.css("a.pagination__next::attr(href)").get()
        if next_href and page < self.max_pages:
            yield response.follow(
                next_href,
                callback=self.parse,
                headers=self._headers(),
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _text(value: str | None) -> str | None:
        return " ".join(value.split()) if value else None

    @staticmethod
    def _number(value):
        if value in (None, ""):
            return None
        match = re.search(r"-?\d+(?:\.\d+)?", str(value).replace(",", ""))
        return float(match.group()) if match else None

    @staticmethod
    def _integer(value):
        number = QvcListingSpider._number(value)
        return int(number) if number is not None else None

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        }
