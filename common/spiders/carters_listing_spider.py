from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.carters_categories import CARTERS_CATEGORIES


class CartersListingSpider(BaseListingSpider):
    """Carter's US products from server-rendered category listing pages."""

    name = "carters_listing"
    allowed_domains = ["carters.com", "www.carters.com"]
    categories = CARTERS_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "product_id", "title", "url", "image_url", "price", "currency",
            "category", "page", "position", "source_url", "source", "timestamp",
        ],
    }

    def start_requests(self):
        yield self._page_request(self.resolve_target_url(), 1)

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        if page == 1:
            return url
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query) if key != "page"]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _page_request(self, url: str, page: int):
        return scrapy.Request(self._page_url(url, page), callback=self.parse, meta={"page": page})

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Carter's returned HTTP {response.status}: {response.url}")

        cards = response.css(".product-tile")
        page = int(response.meta.get("page", 1))
        if page == 1 and not cards:
            raise RuntimeError(f"Carter's listing has no server-rendered product tiles: {response.url}")

        for position, card in enumerate(cards, start=1):
            href = card.css("a[href*='/p/']::attr(href)").get()
            title = " ".join(card.css(".product-tile-title::text").getall()).strip()
            if not href or not title:
                continue
            image_url = (
                card.css("img.main-image::attr(src)").get()
                or card.css("img.main-image::attr(data-src)").get()
            )
            price_text = " ".join(card.css(".product-tile-price ::text").getall()).strip()
            price_match = re.search(r"\$\s*([\d,]+(?:\.\d{2})?)", price_text)
            product_match = re.search(r"/V_([^/?#]+)", href)
            yield {
                "product_id": product_match.group(1) if product_match else None,
                "title": title,
                "url": response.urljoin(href),
                "image_url": response.urljoin(image_url) if image_url else None,
                "price": price_match.group(1).replace(",", "") if price_match else None,
                "currency": "USD",
                "category": self.category,
                "page": page,
                "position": position,
                "source_url": response.url,
                "source": "carters_server_rendered_listing",
                "timestamp": self.get_timestamp().isoformat(),
            }

        # Pagination is intentionally limited to links present in the server-rendered page.
        if page < self.max_pages:
            next_href = response.css("a[rel='next']::attr(href), a[aria-label*='Next']::attr(href)").get()
            if next_href:
                yield self._page_request(response.urljoin(next_href), page + 1)
