from __future__ import annotations

"""eBay category listing spider (Marko hydration state first).

Usage examples:
  scrapy crawl ebay_listing -a category='laptops' -a max_pages=2
  scrapy crawl ebay_listing -a category_url='https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276' -a max_pages=2
"""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.ebay_bootstrap_utils import (
    extract_subcategories_from_html,
    extract_marko_products,
)
from common.spiders.ebay_categories import EBAY_CATEGORIES


class EbayListingSpider(BaseListingSpider):
    name = "ebay_listing"
    allowed_domains = ["ebay.com", "www.ebay.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    categories = EBAY_CATEGORIES

    def start_requests(self):
        if self.args.category not in self.categories:
            raise ValueError(
                f"Invalid category '{self.args.category}'. Available categories: {list(self.categories.keys())}"
            )

        for subCategory, subCategoryUrl in self.categories[self.args.category].items():
            self.logger.info(
                f"Starting requests for subCategory: {subCategory} ({subCategoryUrl})"
            )
            yield scrapy.Request(
                subCategoryUrl,
                callback=self.parse,
                meta={
                    "page": 1,
                    "category": self.args.category,
                    "subCategory": subCategory,
                },
            )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))

        ecommerce_context = {
            "category": response.meta.get("category"),
            "subCategory": response.meta.get("subCategory"),
            "page": page,
            "listingUrl": response.url,
        }

        items = extract_marko_products(response.text)
        for item in items:
            item.update(ecommerce_context)
            yield item

        if page == 1:
            for subCategory in extract_subcategories_from_html(response.text):
                subCategory_url = response.urljoin(subCategory["url"])
                yield scrapy.Request(
                    subCategory_url,
                    callback=self.parse,
                    meta={
                        "page": 1,
                        "category": response.meta.get("category"),
                        "subCategory": subCategory["subCategory"],
                    },
                )

        if page < self.args.max_pages and items:
            next_url = self._with_page(response.url, page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={
                    **response.meta,
                    "page": page + 1,
                },
            )

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs.setdefault("_ipg", ["60"])
        qs["_pgn"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
