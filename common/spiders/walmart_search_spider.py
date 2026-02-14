from __future__ import annotations

"""Walmart keyword search spider.

Usage:
  scrapy crawl walmart_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy

from common.settings import PROXY
from common.spiders.walmart_listing_spider import WalmartListingSpider


class WalmartSearchSpider(WalmartListingSpider):
    name = "walmart_search"

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        if not q:
            raise ValueError("Provide -a q=<term>")
        super().__init__(q=q, max_pages=max_pages, *args, **kwargs)

    def start_requests(self):
        target_url = f"https://www.walmart.com/search?{urlencode({'q': self.q})}"
        meta = {"page": 1, "original_url": target_url, "category": f"search:{self.q}"}
        if PROXY:
            meta["proxy"] = PROXY
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)
