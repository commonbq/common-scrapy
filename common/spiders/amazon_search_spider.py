from __future__ import annotations

"""Amazon keyword search spider.

Usage:
  scrapy crawl amazon_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy

from common.settings import PROXY
from common.spiders.amazon_listing_spider import AmazonListingSpider


class AmazonSearchSpider(AmazonListingSpider):
    name = "amazon_search"

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        if not q:
            raise ValueError("Provide -a q=<term>")
        # Bypass AmazonListingSpider.__init__ requirements; we only need keyword flow.
        scrapy.Spider.__init__(self, *args, **kwargs)
        self.q = (q or "").strip()
        self.max_pages = int(max_pages)

    def start_requests(self):
        query = urlencode({"k": self.q})
        target_url = f"https://www.amazon.com/s?{query}"

        meta = {"page": 1}
        if PROXY:
            meta["proxy"] = PROXY

        yield scrapy.Request(target_url, callback=self.parse, meta=meta)
