from __future__ import annotations

"""Sally Beauty listing spider using the rendered SFCC product grid."""

import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SallybeautyListingSpider(BaseListingSpider):
    name = "sallybeauty_listing"
    allowed_domains = ["sallybeauty.com", "www.sallybeauty.com", "127.0.0.1"]

    categories = [
        {"category": "hair-color", "url": "https://www.sallybeauty.com/hair-color/"},
        {"category": "hair-care", "url": "https://www.sallybeauty.com/hair-care/shop-by-product/"},
        {"category": "textured-curly-hair", "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/"},
        {"category": "hair-extensions", "url": "https://www.sallybeauty.com/hair-extensions/"},
        {"category": "tools-brushes", "url": "https://www.sallybeauty.com/tools-and-brushes/"},
        {"category": "nails", "url": "https://www.sallybeauty.com/nails/"},
        {"category": "cosmetics-skin-care", "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/"},
        {"category": "fragrances", "url": "https://www.sallybeauty.com/fragrances/"},
        {"category": "mens-grooming", "url": "https://www.sallybeauty.com/mens-grooming/"},
        {"category": "salon-supplies", "url": "https://www.sallybeauty.com/salon-supplies/"},
        {"category": "new", "url": "https://www.sallybeauty.com/featured/new-and-now/"},
        {"category": "deals", "url": "https://www.sallybeauty.com/deals/"},
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image_url",
            "price", "price_max", "currency", "rating", "reviews_count",
            "page", "source", "category_url",
        ],
    }

    def start_requests(self):
        url = self.resolve_target_url()
        yield scrapy.Request(url, callback=self.parse, meta={"page": 1, "category_url": url})

    async def start(self):
        for request in self.start_requests():
            yield request

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        cards = response.css('[data-pid].product, [data-pid].product-tile, .product-grid .product-tile')
        if not cards:
            raise RuntimeError(f"No Sally Beauty product grid found at {response.url}")
        for card in cards:
            href = card.css('a[href*=".html"]::attr(href)').get()
            title = card.css('.pdp-link a::text, .product-name::text, a.product-name::text').get()
            brand = card.css('.product-brand::text, .brand-name::text').get()
            price_text = " ".join(card.css('.price ::text, .sales ::text').getall())
            prices = [float(value.replace(",", "")) for value in re.findall(r"\$([\d,]+(?:\.\d{2})?)", price_text)]
            image = card.css('img::attr(src), img::attr(data-src)').get()
            yield {
                "category": self.category,
                "item_id": card.attrib.get("data-pid"),
                "title": title.strip() if title else None,
                "brand": brand.strip() if brand else None,
                "url": response.urljoin(href) if href else None,
                "image_url": response.urljoin(image) if image else None,
                "price": prices[0] if prices else None,
                "price_max": prices[-1] if len(prices) > 1 else None,
                "currency": "USD" if prices else None,
                "rating": self._number(card.css('[itemprop="ratingValue"]::attr(content), .ratings::attr(data-rating)').get()),
                "reviews_count": self._integer(card.css('[itemprop="reviewCount"]::attr(content), .review-count::text').get()),
                "page": page,
                "source": (
                    "sallybeauty_sfcc_search_update_grid"
                    if "Search-UpdateGrid" in response.url
                    else "sallybeauty_sfcc_product_grid"
                ),
                "category_url": response.meta.get("category_url", response.url),
            }

        if page >= self.max_pages:
            return

        # SFCC advertises the exact AJAX endpoint, category id, refinements,
        # sort order, and offset in this URL. Follow it rather than trying to
        # reproduce storefront state from the friendly category URL.
        next_url = response.css(
            '[data-url*="Search-UpdateGrid"]::attr(data-url), '
            'a[href*="Search-UpdateGrid"]::attr(href)'
        ).get()
        if next_url:
            yield response.follow(
                next_url,
                callback=self.parse,
                headers={"X-Requested-With": "XMLHttpRequest"},
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        match = re.search(r"[\d,]+", value or "")
        return int(match.group().replace(",", "")) if match else None
