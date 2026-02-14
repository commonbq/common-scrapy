from __future__ import annotations

"""Home Depot category listing spider.

This spider parses listing products from Home Depot's Apollo bootstrap embedded in
HTML (window.__APOLLO_STATE__).

Usage:
  scrapy crawl homedepot_listing -a category_url='https://www.homedepot.com/b/Tools-Hand-Tools/Screwdrivers-Nut-Drivers/Screwdrivers/N-5yc1vZc25y' -a max_pages=1

Notes:
- Direct requests may return an anti-bot error page in this environment.
- When Apollo bootstrap is present, we parse without needing GraphQL replay.
"""

from typing import Any

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.homedepot_search_spider import HomeDepotSearchSpider


class HomeDepotListingSpider(BaseListingSpider):
    name = "homedepot_listing"
    allowed_domains = ["homedepot.com", "www.homedepot.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
    }

    def __init__(
        self,
        category_url: str | None = None,
        url: str | None = None,
        max_pages: int = 1,
        use_proxy: int | str | None = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.init_listing_args(max_pages=max_pages, use_proxy=use_proxy, url=url, category_url=category_url)

        self.category_url = self.args.category_url
        self.url = self.args.url

        if not (self.category_url or self.url):
            raise ValueError("Provide -a category_url=<url> (or -a url=<url>)")

    def start_requests(self):
        target = self.url or self.category_url or ""
        yield scrapy.Request(target, callback=self.parse, meta=self.maybe_proxy_meta({"original_url": target}))

    def parse(self, response: scrapy.http.Response):
        html = response.text or ""
        if HomeDepotSearchSpider._is_error_page(html):
            self.logger.warning("HomeDepot returned error/bot page; no Apollo bootstrap found")
            return

        state = HomeDepotSearchSpider._extract_js_object(html, "__APOLLO_STATE__")
        if not state:
            self.logger.warning("HomeDepot page did not contain __APOLLO_STATE__")
            return

        # Reuse parsing logic from search spider.
        tmp = HomeDepotSearchSpider(q="x")  # dummy instance for method binding
        yield from tmp._yield_products_from_apollo(
            state,
            mode="category",
            query=None,
            category_url=self.category_url or self.url,
            page=1,
        )
