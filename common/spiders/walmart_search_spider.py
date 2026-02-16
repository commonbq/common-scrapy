from __future__ import annotations

"""Walmart keyword search spider.

Usage:
  scrapy crawl walmart_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider
from common.spiders.walmart_listing_spider import WalmartListingSpider


class WalmartSearchSpider(BaseSearchSpider, WalmartListingSpider):
    name = "walmart_search"

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        # init BaseSearchSpider args
        scrapy.Spider.__init__(self, *args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages)
        # init WalmartListingSpider fields (it calls BaseListingSpider init helpers)
        WalmartListingSpider.__init__(
            self,
            category=None,
            category_url=None,
            url=None,
            max_pages=self.args.max_pages,
        )

    def start_requests(self):
        q = self.args.q or ""
        target_url = f"https://www.walmart.com/search?{urlencode({'q': q})}"
        meta = self.maybe_proxy_meta({"page": 1, "original_url": target_url, "category": f"search:{q}"})
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)
