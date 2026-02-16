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

    def start_requests(self):
        q = self.q or ""
        target_url = f"https://www.walmart.com/search?{urlencode({'q': q})}"
        meta = self.proxy_meta({"page": 1, "original_url": target_url, "category": f"search:{q}"})
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)
