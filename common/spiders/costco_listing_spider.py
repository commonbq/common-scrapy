from __future__ import annotations

"""Costco category/listing spider.

Usage:
  scrapy crawl costco_listing -a category_url='https://www.costco.com/coffee.html' -a max_pages=1
"""

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.retail_bootstrap_utils import (
    extract_apollo_state,
    extract_items_from_unknown_state,
    extract_json_ld_products,
    extract_next_data,
)


class CostcoListingSpider(BaseListingSpider):
    name = "costco_listing"
    allowed_domains = ["costco.com", "www.costco.com", "r.jina.ai"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    def __init__(self, category_url: str | None = None, url: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_listing_args(max_pages=max_pages, url=url, category_url=category_url)
        self.category_url = self.args.category_url
        self.url = self.args.url
        if not (self.category_url or self.url):
            raise ValueError("Provide -a category_url=<url> (or -a url=<url>)")

    def start_requests(self):
        target = self._with_page(self.url or self.category_url or "", 1)
        yield scrapy.Request(target, callback=self.parse, meta=self.proxy_meta({"page": 1}))

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        nd = extract_next_data(html)
        if nd:
            for item in extract_items_from_unknown_state(nd, source="costco_next_data"):
                yielded += 1
                item.update({"mode": "category", "category_url": self.category_url or self.url, "page": page, "source_url": response.url})
                yield item

        ap = extract_apollo_state(html)
        if ap:
            for item in extract_items_from_unknown_state(ap, source="costco_apollo_state"):
                yielded += 1
                item.update({"mode": "category", "category_url": self.category_url or self.url, "page": page, "source_url": response.url})
                yield item

        if yielded == 0:
            for item in extract_json_ld_products(html):
                yielded += 1
                item.update({"mode": "category", "category_url": self.category_url or self.url, "page": page, "source_url": response.url})
                yield item

        if yielded == 0:
            for item in self._extract_product_links(html):
                yielded += 1
                item.update({"mode": "category", "category_url": self.category_url or self.url, "page": page, "source_url": response.url})
                yield item

        if yielded == 0:
            self.logger.warning("Costco listing produced 0 items (status=%s)", response.status)

        if page < self.args.max_pages:
            next_page = page + 1
            next_url = self._with_page(self.url or self.category_url or "", next_page)
            yield scrapy.Request(next_url, callback=self.parse, meta=self.proxy_meta({"page": next_page}))

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _extract_product_links(self, html: str):
        pat = re.compile(r'href=["\'](?P<url>https://www\.costco\.com/[^"\']+\.html)["\']', re.I)
        seen: set[str] = set()
        for m in pat.finditer(html or ""):
            url = m.group("url")
            if "/s?" in url or url in seen:
                continue
            seen.add(url)
            mid = re.search(r"(\d{6,})", url)
            yield {
                "item_id": mid.group(1) if mid else None,
                "title": None,
                "url": url,
                "price": None,
                "currency": None,
                "brand": None,
                "rating": None,
                "reviews_count": None,
                "image_url": None,
                "source": "costco_html_links_fallback",
                "raw": None,
            }
