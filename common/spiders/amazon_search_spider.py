from __future__ import annotations

"""Amazon keyword search spider.

Usage:
  scrapy crawl amazon_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy

from common.spiders.amazon_listing_spider import AmazonListingSpider
from common.spiders.base_search_spider import BaseSearchSpider


class AmazonSearchSpider(BaseSearchSpider, AmazonListingSpider):
    name = "amazon_search"

    def start_requests(self):
        query = urlencode({"k": self.q})
        target_url = f"https://www.amazon.com/s?{query}"

        meta = ({"page": 1})
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)
