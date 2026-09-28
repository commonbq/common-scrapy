from __future__ import annotations

import json
import re
from urllib.parse import urljoin, urlsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


QVC_CATEGORIES = {
    "fashion": ["https://www.qvc.com/c/fashion/-/lglt/c.html"],
}


class QvcListingSpider(BaseListingSpider):
    """Extract QVC's server-rendered listing cards and embedded page state."""

    name = "qvc_listing"
    allowed_domains = ["qvc.com", "www.qvc.com"]
    require_category_arg = False
    categories = QVC_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "category_id", "item_id", "title", "brand", "url",
            "image_url", "price", "original_price", "currency", "rating",
            "reviews_count", "badge", "shipping_promo", "special_price_code",
            "installment_count", "colors_count", "total_products", "page", "source",
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
        cards = response.css("#searchResults .galleryItem[data-item-id]")
        if not cards:
            self.logger.warning(
                "QVC product grid unavailable: status=%s url=%s", response.status, response.url
            )
            return

        state = self._bootstrap_state(response.text)
        page = self._integer(state.get("currentPage")) or int(response.meta.get("page") or 1)
        category_id = state.get("category_id")
        total_products = self._integer(
            response.css("#searchResults::attr(data-total-products)").get()
        )

        for card in cards:
            item_id = (card.attrib.get("data-item-id") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)

            link = card.css(".productInfoWrapper > a[href]::attr(href)").get()
            image = card.css(".productImg img::attr(data-src)").get()
            rating_text = card.css(".productRatings .sr-only::text").get()
            reviews_text = card.css(".productNumberOfReviews [aria-hidden=true]::text").get()
            badge = card.css(".productBadge span::text, .productPromo::text").get()

            yield {
                "category": response.meta.get("category"),
                "category_id": category_id,
                "item_id": item_id,
                "title": self._text(card.attrib.get("data-cnstrc-item-name")),
                "brand": None,
                "url": urljoin(response.url, link or ""),
                "image_url": urljoin(response.url, image or ""),
                "price": self._number(
                    card.css(".priceSell::attr(data-sale-price)").get()
                    or card.attrib.get("data-cnstrc-item-price")
                ),
                "original_price": self._number(
                    card.css(".priceOld [aria-hidden=true]::text").get()
                ),
                "currency": "USD",
                "rating": self._number(rating_text),
                "reviews_count": self._integer(reviews_text),
                "badge": self._text(badge),
                "shipping_promo": self._text(card.css(".productPromoShipping::text").get()),
                "special_price_code": card.attrib.get("data-item-spc"),
                "installment_count": self._integer(
                    card.css(".productEZPay::attr(data-install-num)").get()
                ),
                "colors_count": len(card.css(".colorList .swatch[data-colorcode]")),
                "total_products": total_products,
                "page": page,
                "source": "qvc_server_rendered_gallery_with_utag_state",
            }

        next_href = response.css('link[rel="next"]::attr(href)').get()
        if next_href and page < self.max_pages:
            yield response.follow(
                next_href,
                callback=self.parse,
                headers=self._headers(),
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _bootstrap_state(html: str) -> dict:
        match = re.search(r"\bvar\s+utag_data\s*=\s*({.*?})\s*;", html, re.DOTALL)
        if not match:
            return {}
        try:
            state = json.loads(match.group(1))
        except json.JSONDecodeError:
            return {}
        return state if isinstance(state, dict) else {}

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
