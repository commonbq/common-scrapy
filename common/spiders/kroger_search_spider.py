from __future__ import annotations

"""Kroger keyword search spider.

Strategy:
1) Try bootstrap model extraction: __NEXT_DATA__ / __APOLLO_STATE__
2) Fallback JSON-LD product extraction
3) Fallback product link extraction from HTML

Usage:
  scrapy crawl kroger_search -a q=milk -a max_pages=1
"""

import re
from urllib.parse import urlencode

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider
from common.spiders.retail_bootstrap_utils import (
    extract_apollo_state,
    extract_items_from_unknown_state,
    extract_json_ld_products,
    extract_next_data,
)


class KrogerSearchSpider(BaseSearchSpider):
    name = "kroger_search"
    allowed_domains = ["kroger.com", "www.kroger.com", "r.jina.ai"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    def start_requests(self):
        yield scrapy.Request(self._build_url(self.q or "", 1), callback=self.parse, meta=self.proxy_meta({"page": 1}))

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        nd = extract_next_data(html)
        if nd:
            for item in extract_items_from_unknown_state(nd, source="kroger_next_data"):
                yielded += 1
                item.update({"mode": "keyword", "query": self.q, "page": page, "source_url": response.url})
                yield item

        ap = extract_apollo_state(html)
        if ap:
            for item in extract_items_from_unknown_state(ap, source="kroger_apollo_state"):
                yielded += 1
                item.update({"mode": "keyword", "query": self.q, "page": page, "source_url": response.url})
                yield item

        if yielded == 0:
            for item in extract_json_ld_products(html):
                yielded += 1
                item.update({"mode": "keyword", "query": self.q, "page": page, "source_url": response.url})
                yield item

        if yielded == 0:
            for item in self._extract_product_links(html):
                yielded += 1
                item.update({"mode": "keyword", "query": self.q, "page": page, "source_url": response.url})
                yield item

        if yielded == 0:
            self.logger.warning("Kroger search produced 0 items (status=%s)", response.status)

        if page < self.args.max_pages:
            next_page = page + 1
            yield scrapy.Request(self._build_url(self.q or "", next_page), callback=self.parse, meta=self.proxy_meta({"page": next_page}))

    @staticmethod
    def _build_url(q: str, page: int = 1) -> str:
        params = {"query": q, "searchType": "default_search"}
        if page > 1:
            params["page"] = str(page)
        return f"https://www.kroger.com/search?{urlencode(params)}"

    def _extract_product_links(self, html: str):
        pat = re.compile(r'href=["\'](?P<url>/p/[^"\']+)["\']', re.I)
        seen: set[str] = set()
        for m in pat.finditer(html or ""):
            rel = m.group("url")
            url = f"https://www.kroger.com{rel.split('?')[0]}"
            if url in seen:
                continue
            seen.add(url)
            mid = re.search(r"/p/([^/?#]+)", rel)
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
                "source": "kroger_html_links_fallback",
                "raw": None,
            }
