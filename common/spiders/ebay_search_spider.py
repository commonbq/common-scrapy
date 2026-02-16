from __future__ import annotations

"""eBay keyword search spider (bootstrap/model-state first).

Usage:
  scrapy crawl ebay_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider
from common.spiders.ebay_bootstrap_utils import extract_items_from_next_data, extract_json_ld_products, extract_next_data


class EbaySearchSpider(BaseSearchSpider):
    name = "ebay_search"
    allowed_domains = ["ebay.com", "www.ebay.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages)

    def start_requests(self):
        url = self._build_search_url(self.args.q or "")
        yield scrapy.Request(url, callback=self.parse, meta=self.proxy_meta({"page": 1, "original_url": url}))

    def parse(self, response: scrapy.http.Response):
        original_url = response.meta.get("original_url") or response.url
        page = int(response.meta.get("page", 1))

        yielded = 0

        next_data = extract_next_data(response.text or "")
        if next_data:
            for item in extract_items_from_next_data(next_data):
                item.update(
                    {
                        "mode": "keyword",
                        "query": self.args.q,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yielded += 1
                yield item

        if yielded == 0:
            for item in extract_json_ld_products(response.text or ""):
                item.update(
                    {
                        "mode": "keyword",
                        "query": self.args.q,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yield item

        if page < self.args.max_pages:
            next_url = self._with_page(original_url, page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta=self.proxy_meta({"page": page + 1, "original_url": next_url}),
            )

    @staticmethod
    def _build_search_url(q: str) -> str:
        return f"https://www.ebay.com/sch/i.html?{urlencode({'_nkw': q, '_ipg': 60})}"

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["_pgn"] = [str(page)]
        qs.setdefault("_ipg", ["60"])
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
