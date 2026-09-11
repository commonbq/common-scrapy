from __future__ import annotations

"""Best Buy category/listing spider (Playwright-assisted Apollo extraction).

Usage examples:
  scrapy crawl bestbuy_listing -a category='laptops' -a max_pages=1
"""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.bestbuy_bootstrap_utils import (
    extract_bestbuy_items_from_apollo,
)


class BestbuyListingSpider(BaseListingSpider):
    name = "bestbuy_listing"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "skuId",
            "title",
            "url",
            "brand",
            "price",
            "originalPrice",
            "discountAmount",
            "discountPercent",
            "priceBadge",
            "isMAP",
            "rating",
            "reviewCount",
            "imageUrl",
            "openBoxCondition",
            "isSponsored",
            "position",
            "primaryCategoryId",
            "campaignId",
            "category",
            "subCategory",
            "page",
            "listingUrl",
            "raw",
            "timestamp",
        ]
    }

    categories = [
        {
            "category": "laptops",
            "url": "https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000",
        },
        {
            "category": "tvs",
            "url": "https://www.bestbuy.com/site/tv-home-theater/televisions/abcat0101001.c?id=abcat0101001",
        },
        {
            "category": "headphones",
            "url": "https://www.bestbuy.com/site/headphones/all-headphones/abcat0204000.c?id=abcat0204000",
        },
        {
            "category": "monitors",
            "url": "https://www.bestbuy.com/site/computer-cards-components/monitors/abcat0509000.c?id=abcat0509000",
        },
        {
            "category": "cell-phones",
            "url": "https://www.bestbuy.com/site/cell-phones/all-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005",
        },
    ]

    def start_requests(self):
        target = self._resolve_target_url()
        target = self._ensure_nosplash(self._with_page(target, 1))
        yield scrapy.Request(
            target,
            callback=self.parse_listing_page,
            meta={"page": 1},
        )

    async def parse_listing_page(self, response: scrapy.http.Response):
        page_num = int(response.meta.get("page", 1))
        items = extract_bestbuy_items_from_apollo(response.text)
        for item in items:
            item.update(
                {
                    "category": self.category,
                    "subCategory": response.meta.get("sub_category"),
                    "page": page_num,
                    "listingUrl": response.url,
                    "timestamp": self.get_timestamp(),
                }
            )
            yield item

        subcategories: dict[str, str] = {}
        if page_num == 1:
            for link in response.css("main a.cn-carousel-item"):
                href = link.attrib.get("href")
                if not href:
                    continue
                subcategory_url = response.urljoin(href)
                subcategory_name = link.xpath(
                    "normalize-space(string(.))"
                ).get()
                subcategories[subcategory_name] = subcategory_url

        if subcategories:
            self.logger.info(
                "BestBuy category page: following %s subcategories",
                len(subcategories),
            )
            for subcategory_name, subcategory_url in subcategories.items():
                url = self._ensure_nosplash(self._with_page(subcategory_url, 1))
                yield scrapy.Request(
                    url,
                    callback=self.parse_listing_page,
                    meta={
                        "page": 1,
                        "sub_category": subcategory_name,
                    },
                )

        if not items:
            self.logger.warning(
                "BestBuy listing produced 0 items page=%s status=%s",
                page_num,
                response.status,
            )

        if items and page_num < self.args.max_pages:
            next_page = page_num + 1
            next_url = self._ensure_nosplash(
                self._with_page(response.url, next_page)
            )
            yield scrapy.Request(
                next_url,
                callback=self.parse_listing_page,
                meta={
                    "page": next_page,
                    "is_subcategory": response.meta.get("is_subcategory", False),
                    "sub_category": response.meta.get("sub_category"),
                },
            )

    def _resolve_target_url(self) -> str:
        if self.url:
            return self.url
        if self.category_url:
            return self.category_url
        for entry in self.categories:
            if entry.get("category") == self.category:
                self.category_url = entry.get("url")
                return self.category_url
        names = ", ".join(sorted([c["category"] for c in self.categories]))
        raise ValueError(f"Unknown category '{self.category}'. Use one of: {names}")

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["cp"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    @staticmethod
    def _ensure_nosplash(url: str) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["intl"] = ["nosplash"]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
