from __future__ import annotations

"""Kroger keyword search spider.

Strategy:
1) Try bootstrap model extraction: __NEXT_DATA__ / __APOLLO_STATE__
2) Fallback JSON-LD product extraction
3) Fallback product link extraction from HTML
4) If empty, retry with alternate sort orders to bust CDN/cache variants

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
    allowed_domains = ["kroger.com", "www.kroger.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}
    sort_variants = [None, "bestMatch", "sale"]

    def start_requests(self):
        yield scrapy.Request(
            self._build_url(self.q or "", 1),
            callback=self.parse,
            meta={"page": 1, "sort_index": 0},
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        sort_index = int(response.meta.get("sort_index", 0))
        html = response.text or ""
        yielded = 0

        if "Access Denied" in html and "kroger.com/search" in html:
            self.logger.warning("Kroger returned Access Denied page (status=%s)", response.status)

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

        if yielded == 0 and sort_index + 1 < len(self.sort_variants):
            next_sort_idx = sort_index + 1
            retry_url = self._build_url(self.q or "", page, sort=self.sort_variants[next_sort_idx])
            self.logger.warning(
                "Kroger search empty; retrying with sort variant %s: %s",
                self.sort_variants[next_sort_idx],
                retry_url,
            )
            yield scrapy.Request(
                retry_url,
                callback=self.parse,
                meta={"page": page, "sort_index": next_sort_idx},
                dont_filter=True,
            )
            return

        if yielded == 0:
            self.logger.warning("Kroger search produced 0 items (status=%s)", response.status)

        if page < self.args.max_pages:
            next_page = page + 1
            yield scrapy.Request(
                self._build_url(self.q or "", next_page),
                callback=self.parse,
                meta={"page": next_page, "sort_index": 0},
            )

    @staticmethod
    def _build_url(q: str, page: int = 1, sort: str | None = None) -> str:
        params = {"query": q, "searchType": "default_search"}
        if page > 1:
            params["page"] = str(page)
        if sort:
            params["sort"] = sort
        return f"https://www.kroger.com/search?{urlencode(params)}"

    def _extract_product_links(self, html: str):
        patterns = [
            re.compile(r'href=["\'](?P<url>/p/[^"\']+)["\']', re.I),
            re.compile(r'\\/p\\/(?P<id>[A-Za-z0-9_-]+)'),
        ]
        seen: set[str] = set()

        for m in patterns[0].finditer(html or ""):
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

        for m in patterns[1].finditer(html or ""):
            pid = m.group("id")
            url = f"https://www.kroger.com/p/{pid}"
            if url in seen:
                continue
            seen.add(url)
            yield {
                "item_id": pid,
                "title": None,
                "url": url,
                "price": None,
                "currency": None,
                "brand": None,
                "rating": None,
                "reviews_count": None,
                "image_url": None,
                "source": "kroger_html_links_escaped_fallback",
                "raw": None,
            }
