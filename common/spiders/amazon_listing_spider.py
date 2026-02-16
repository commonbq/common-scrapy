from __future__ import annotations

import re
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class AmazonListingSpider(BaseListingSpider):
    name = "amazon_listing"
    allowed_domains = ["amazon.com", "www.amazon.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        "DOWNLOAD_DELAY": 0,
    }

    # A small allowlist of common Amazon category nodes (browse node ids).
    # Users can also provide a full category_url.
    categories = {
        "electronics": "172282",
        "fashion": "7141123011",
        "beauty": "3760911",
        "home-kitchen": "1055398",
        "toys-games": "165793011",
        "sports-outdoors": "3375251",
        "grocery": "16310101",
        "books": "283155",
    }

    def __init__(
        self,
        category: str | None = None,
        category_node: str | None = None,
        category_url: str | None = None,
        url: str | None = None,
        max_pages: int = 1,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.init_listing_args(
            max_pages=max_pages,
            url=url,
            category=category,
            category_url=category_url,
        )

        self.category = (category or "").strip().lower()
        self.category_node = (category_node or "").strip()
        self.category_url = (category_url or "").strip()
        self.url = (url or "").strip()
        self.max_pages = self.args.max_pages

        if not (self.category_url or self.category_node or self.category or self.url):
            raise ValueError(
                "Provide -a category=<name> or -a category_node=<id> or -a category_url=<url> (or -a url=<custom url>). "
                "For keyword search use amazon_search"
            )

        if not self.category_node and self.category:
            self.category_node = self.categories.get(self.category, "")

    def start_requests(self):
        target_url = self.url or self.category_url
        if not target_url:
            node = self.category_node
            if not node:
                raise ValueError("Unknown category. Use one of: %s" % ", ".join(sorted(self.categories.keys())))
            query = urlencode({"i": "aps", "bbn": node, "rh": f"n:{node}"})
            target_url = f"https://www.amazon.com/s?{query}"

        yield scrapy.Request(target_url, callback=self.parse, meta={"page": 1})

    def parse(self, response: scrapy.http.Response):
        cards = response.css(
            'div.s-main-slot div[data-component-type="s-search-result"][data-asin]'
        )

        for card in cards:
            asin = (card.attrib.get("data-asin") or "").strip()
            if not asin:
                continue

            title = (
                card.css("h2 a span::text").get()
                or card.css("h2 span::text").get()
                or ""
            ).strip()
            product_url = response.urljoin(card.css("h2 a::attr(href)").get() or "")
            image_url = card.css("img.s-image::attr(src)").get()
            rating_text = (card.css("span.a-icon-alt::text").get() or "").strip()
            reviews_text = (
                card.css("span.a-size-base.s-underline-text::text").get() or ""
            ).strip()
            price_whole = (card.css("span.a-price-whole::text").get() or "").strip()
            price_fraction = (
                card.css("span.a-price-fraction::text").get() or ""
            ).strip()

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
                "is_sponsored": bool(
                    card.xpath('.//*[contains(normalize-space(.), "Sponsored")]')
                ),
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        next_href = response.css(
            "a.s-pagination-next:not(.s-pagination-disabled)::attr(href)"
        ).get()
        if not next_href:
            return

        yield response.follow(
            next_href,
            callback=self.parse,
            meta={"page": current_page + 1},
        )

    def _extract_float(self, text: str) -> float | None:
        match = re.search(r"(\d+(?:\.\d+)?)", text)
        if not match:
            return None
        return float(match.group(1))

    def _extract_int(self, text: str) -> int | None:
        cleaned = re.sub(r"[^\d]", "", text)
        if not cleaned:
            return None
        return int(cleaned)
