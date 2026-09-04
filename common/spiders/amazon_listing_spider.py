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
        "FEED_EXPORT_FIELDS": [
            "asin",
            "title",
            "url",
            "imageUrl",
            "price",
            "rating",
            "reviewsCount",
            "isPrime",
            "isSponsored",
            "badge",
            "category",
            "subCategory",
            "page",
        ],
    }

    categories = [
        {"category": "pillow", "url": "https://www.amazon.com/b?node=1199122"},
        {
            "category": "Home & Kitchen",
            "category_id": "1055398",
            "url": "https://www.amazon.com/b?node=1055398",
        },
        {
            "category": "Beauty & Personal Care",
            "category_id": "3760911",
            "url": "https://www.amazon.com/b?node=3760911",
        },
        {
            "category": "Clothing, Shoes & Jewelry",
            "category_id": "7141123011",
            "url": "https://www.amazon.com/b?node=7141123011",
        },
        {
            "category": "Toys & Games",
            "category_id": "165793011",
            "url": "https://www.amazon.com/b?node=165793011",
        },
        {
            "category": "Electronics",
            "category_id": "172282",
            "url": "https://www.amazon.com/b?node=172282",
        },
        {
            "category": "Sports & Outdoors",
            "category_id": "3375251",
            "url": "https://www.amazon.com/b?node=3375251",
        },
        {
            "category": "Health & Household",
            "category_id": "3760901",
            "url": "https://www.amazon.com/b?node=3760901",
        },
        {
            "category": "Grocery & Gourmet Food",
            "category_id": "16310101",
            "url": "https://www.amazon.com/b?node=16310101",
        },
        {
            "category": "Tools & Home Improvement",
            "category_id": "228013",
            "url": "https://www.amazon.com/b?node=228013",
        },
        {
            "category": "Books",
            "category_id": "283155",
            "url": "https://www.amazon.com/b?node=283155",
        },
    ]

    def start_requests(self):
        target_url = self.resolve_target_url()
        target_url = self._with_page(target_url, 1)
        yield scrapy.Request(
            target_url,
            callback=self.parse,
            meta={"page": 1, "category": self.category},
        )

    def parse(self, response: scrapy.http.Response):
        category = response.meta.get("category")
        current_page = int(response.meta.get("page", 1))
        if current_page == 1:
            sub_categories = response.css(
                "#s-refinements ul[aria-labelledby='n-title'] a.a-link-normal"
            )
            if not sub_categories:
                section_header = response.xpath('//span[text()="Shop by category"]')
                if section_header:
                    section_header = section_header[0]
                    parent = section_header.xpath("./../../../../..")
                    sub_categories = parent.css(
                        ".dcl-carousel .a-carousel-card a.a-link-normal"
                    )

            for sub_category in sub_categories:
                sub_category_url = response.urljoin(
                    sub_category.css("::attr(href)").get()
                )
                sub_category = sub_category.css("span::text").get()
                yield scrapy.Request(
                    sub_category_url,
                    callback=self.parse,
                    meta={
                        "page": 1,
                        "category": category,
                        "sub_category": sub_category,
                    },
                )

        cards = response.css(
            'div.s-main-slot div[data-component-type="s-search-result"][data-asin]'
        )

        if not cards:
            title = (response.css("title::text").get() or "").strip()
            self.logger.warning(
                "No Amazon listing cards found (url=%s, title=%r)",
                response.url,
                title[:120],
            )
            return

        for card in cards:
            asin = (card.attrib.get("data-asin") or "").strip()
            if not asin:
                continue

            title = (
                card.css("h2 a span::text").get()
                or card.css("h2 span::text").get()
                or ""
            ).strip()
            product_href = (
                card.css("h2 a::attr(href)").get()
                or card.css("a.a-link-normal.s-no-outline::attr(href)").get()
                or card.css(f'a[href*="/dp/{asin}"]::attr(href)').get()
            )
            product_url = (
                response.urljoin(product_href)
                if product_href
                else f"https://www.amazon.com/dp/{asin}"
            )
            image_url = card.css("img.s-image::attr(src)").get()
            rating_text = (card.css("span.a-icon-alt::text").get() or "").strip()
            reviews_text = (
                card.css('a[href*="#customerReviews"] span::text').get()
                or card.css('span[aria-label$="ratings"]::text').get()
                or card.css("span.a-size-base.s-underline-text::text").get()
                or ""
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

            badge = (
                card.css("div.puis-status-badge-container.a-section span::text").get()
                or ""
            )
            badge = "" if "in cart" in badge.lower() else badge.strip()
            yield {
                "asin": asin,
                "title": title,
                "url": product_url,
                "imageUrl": image_url,
                "price": price,
                "rating": self._extract_float(rating_text),
                "reviewsCount": self._extract_int(reviews_text),
                "isPrime": bool(card.css("i.a-icon-prime, span.a-prime-icon")),
                "isSponsored": bool(
                    card.xpath('.//*[contains(normalize-space(.), "Sponsored")]')
                ),
                "badge": badge,
                "category": category,
                "subCategory": response.meta.get("sub_category"),
                "page": current_page,
            }

        if current_page >= self.max_pages:
            return

        next_href = response.css(
            "a.s-pagination-next:not(.s-pagination-disabled)::attr(href)"
        ).get()
        if next_href:
            yield response.follow(
                next_href,
                callback=self.parse,
                meta={"page": current_page + 1},
            )
            return

        next_url = self._with_page(response.url, current_page + 1)
        yield scrapy.Request(
            next_url,
            callback=self.parse,
            meta={"page": current_page + 1},
        )

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
        compact = text.replace(",", "").strip().lower()
        short = re.search(r"(\d+(?:\.\d+)?)\s*([km])", compact)
        if short:
            base = float(short.group(1))
            mult = 1_000 if short.group(2) == "k" else 1_000_000
            return int(base * mult)

        cleaned = re.sub(r"[^\d]", "", compact)
        return int(cleaned) if cleaned else None
