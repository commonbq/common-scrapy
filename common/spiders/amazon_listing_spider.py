from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class AmazonListingSpider(BaseListingSpider):
    name = "amazon_listing"
    allowed_domains = ["amazon.com", "www.amazon.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        "DOWNLOAD_DELAY": 0,
    }

    categories = [
        {"category": "electronics", "url": "https://www.amazon.com/s?k=electronics"},
        {"category": "fashion", "url": "https://www.amazon.com/s?k=fashion"},
        {"category": "beauty", "url": "https://www.amazon.com/s?k=beauty"},
        {"category": "home-kitchen", "url": "https://www.amazon.com/s?k=home+kitchen"},
        {"category": "toys-games", "url": "https://www.amazon.com/s?k=toys+games"},
        {"category": "sports-outdoors", "url": "https://www.amazon.com/s?k=sports+outdoors"},
        {"category": "grocery", "url": "https://www.amazon.com/s?k=grocery"},
        {"category": "books", "url": "https://www.amazon.com/s?k=books"},
    ]

    def start_requests(self):
        target_url = self.resolve_target_url()
        target_url = self._with_page(target_url, 1)
        yield scrapy.Request(target_url, callback=self.parse, meta={"page": 1})

    def parse(self, response: scrapy.http.Response):
        cards = response.css('div.s-main-slot div[data-component-type="s-search-result"][data-asin]')

        if not cards:
            title = (response.css("title::text").get() or "").strip()
            self.logger.warning("No Amazon listing cards found (url=%s, title=%r)", response.url, title[:120])

        for card in cards:
            asin = (card.attrib.get("data-asin") or "").strip()
            if not asin:
                continue

            title = (card.css("h2 a span::text").get() or card.css("h2 span::text").get() or "").strip()
            product_url = response.urljoin(card.css("h2 a::attr(href)").get() or "")
            image_url = card.css("img.s-image::attr(src)").get()
            rating_text = (card.css("span.a-icon-alt::text").get() or "").strip()
            reviews_text = (card.css("span.a-size-base.s-underline-text::text").get() or "").strip()
            price_whole = (card.css("span.a-price-whole::text").get() or "").strip()
            price_fraction = (card.css("span.a-price-fraction::text").get() or "").strip()

            price = None
            if price_whole:
                whole = price_whole.replace(",", "").replace(".", "")
                if whole.isdigit():
                    price = float(f"{whole}.{price_fraction or '00'}")

            yield {
                "asin": asin,
                "title": title,
                "url": product_url,
                "image_url": image_url,
                "price": price,
                "rating": self._extract_float(rating_text),
                "reviews_count": self._extract_int(reviews_text),
                "is_prime": bool(card.css("i.a-icon-prime, span.a-prime-icon")),
                "is_sponsored": bool(card.xpath('.//*[contains(normalize-space(.), "Sponsored")]')),
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        next_href = response.css("a.s-pagination-next:not(.s-pagination-disabled)::attr(href)").get()
        if next_href:
            yield response.follow(next_href, callback=self.parse, meta={"page": current_page + 1})
            return

        next_url = self._with_page(response.url, current_page + 1)
        yield scrapy.Request(next_url, callback=self.parse, meta={"page": current_page + 1})

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _extract_float(self, text: str) -> float | None:
        match = re.search(r"(\d+(?:\.\d+)?)", text)
        return float(match.group(1)) if match else None

    def _extract_int(self, text: str) -> int | None:
        cleaned = re.sub(r"[^\d]", "", text)
        return int(cleaned) if cleaned else None
