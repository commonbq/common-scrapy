from __future__ import annotations

"""Best Buy keyword search spider using Apollo data from the HTTP response.

Usage:
  scrapy crawl bestbuy_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider
from common.spiders.bestbuy_bootstrap_utils import extract_bestbuy_items_from_bootstrap


class BestbuySearchSpider(BaseSearchSpider):
    name = "bestbuy_search"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "skuId", "title", "url", "brand", "price", "originalPrice",
            "discountAmount", "discountPercent", "priceBadge", "isMAP",
            "rating", "reviewCount", "imageUrl", "openBoxCondition",
            "isSponsored", "position", "primaryCategoryId", "campaignId",
            "mode", "query", "page", "source_url", "raw", "timestamp",
        ],
    }

    def start_requests(self):
        first = self._build_search_url(self.q or "")
        yield scrapy.Request(first, callback=self.parse_search_page, meta=({"page": 1}))

    def parse_search_page(self, response: scrapy.http.Response):
        page_num = int(response.meta.get("page", 1))
        html = response.text or ""

        emitted = 0

        for item in extract_bestbuy_items_from_bootstrap(html):
            emitted += 1
            item.update({"mode": "keyword", "query": self.q, "page": page_num, "source_url": response.url})
            yield item

        if emitted == 0:
            self.logger.warning("BestBuy search produced 0 items page=%s status=%s", page_num, response.status)

        if page_num < self.args.max_pages:
            next_page = page_num + 1
            next_url = self._build_search_url(self.q or "", page=next_page)
            yield scrapy.Request(next_url, callback=self.parse_search_page, meta=({"page": next_page}))

    @staticmethod
    def _build_search_url(q: str, page: int = 1) -> str:
        params = {"st": q, "intl": "nosplash"}
        if page > 1:
            params["cp"] = str(page)
        return f"https://www.bestbuy.com/site/searchpage.jsp?{urlencode(params)}"
