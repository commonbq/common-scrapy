from __future__ import annotations

"""Amazon keyword search spider.

Usage:
  scrapy crawl amazon_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy

from common.settings import PROXY
from common.spiders.amazon_listing_spider import AmazonListingSpider
from common.spiders.base_search_spider import BaseSearchSpider


class AmazonSearchSpider(BaseSearchSpider, AmazonListingSpider):
    name = "amazon_search"

    def __init__(self, q: str | None = None, max_pages: int = 1, use_proxy: int | str | None = 0, *args, **kwargs):
        scrapy.Spider.__init__(self, *args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages, use_proxy=use_proxy)
        self.q = self.args.q or ""
        self.max_pages = self.args.max_pages

    def start_requests(self):
        query = urlencode({"k": self.q})
        target_url = f"https://www.amazon.com/s?{query}"

        meta = self.maybe_proxy_meta({"page": 1})
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)
