from __future__ import annotations

"""eBay category listing spider (bootstrap/model-state first).

Requires category_url (or url).

Usage:
  scrapy crawl ebay_listing -a category_url='https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276' -a max_pages=2
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.ebay_bootstrap_utils import extract_items_from_next_data, extract_json_ld_products, extract_next_data


class EbayListingSpider(BaseListingSpider):
    name = "ebay_listing"
    allowed_domains = ["ebay.com", "www.ebay.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
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
        target_url = self.url or self.category_url or ""
        target_url = self._with_page(target_url, 1)
        yield scrapy.Request(target_url, callback=self.parse, meta=self.maybe_proxy_meta({"page": 1, "original_url": target_url}))

    def parse(self, response: scrapy.http.Response):
        original_url = response.meta.get("original_url") or response.url
        page = int(response.meta.get("page", 1))

        yielded = 0

        next_data = extract_next_data(response.text or "")
        if next_data:
            for item in extract_items_from_next_data(next_data):
                item.update(
                    {
                        "mode": "category",
                        "category_url": self.category_url,
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
                        "mode": "category",
                        "category_url": self.category_url,
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
                meta=self.maybe_proxy_meta({"page": page + 1, "original_url": next_url}),
            )

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs.setdefault("_ipg", ["60"])
        qs["_pgn"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
