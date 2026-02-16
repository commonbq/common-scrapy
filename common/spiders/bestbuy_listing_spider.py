from __future__ import annotations

"""Best Buy category/listing spider (bootstrap-first).

Usage:
  scrapy crawl bestbuy_listing -a category_url='https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000' -a max_pages=1
"""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.bestbuy_bootstrap_utils import extract_bestbuy_items_from_bootstrap


class BestbuyListingSpider(BaseListingSpider):
    name = "bestbuy_listing"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com", "bifrostgw.us.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(
        self,
        category_url: str | None = None,
        url: str | None = None,
        max_pages: int = 1,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.init_listing_args(max_pages=max_pages, url=url, category_url=category_url)

        self.category_url = self.args.category_url
        self.url = self.args.url
        if not (self.category_url or self.url):
            raise ValueError("Provide -a category_url=<url> (or -a url=<url>)")

    def start_requests(self):
        target = self.url or self.category_url or ""
        target = self._with_page(target, 1)
        target = self._ensure_nosplash(target)
        yield scrapy.Request(target, callback=self.parse_listing_page, meta=self.proxy_meta({"page": 1, "original_url": target}))

    def parse_listing_page(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""

        emitted = 0
        for item in extract_bestbuy_items_from_bootstrap(html):
            emitted += 1
            item.update(
                {
                    "mode": "category",
                    "category_url": self.category_url or self.url,
                    "page": page,
                    "source_url": response.url,
                }
            )
            yield item

        if emitted == 0:
            self.logger.warning("No BestBuy bootstrap items found for listing page=%s status=%s", page, response.status)
            return

        if page >= self.args.max_pages:
            return

        next_page = page + 1
        original = response.meta.get("original_url") or (self.url or self.category_url or "")
        next_url = self._ensure_nosplash(self._with_page(original, next_page))
        yield scrapy.Request(
            next_url,
            callback=self.parse_listing_page,
            meta=self.proxy_meta({"page": next_page, "original_url": next_url}),
            dont_filter=True,
        )

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
