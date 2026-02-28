from __future__ import annotations

"""Kroger category/listing spider.

Usage examples:
  scrapy crawl kroger_listing -a category='cereal' -a max_pages=1
  scrapy crawl kroger_listing -a category_url='https://www.kroger.com/pl/cereal/09002' -a max_pages=1
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


class KrogerListingSpider(BaseListingSpider):
    name = "kroger_listing"
    allowed_domains = ["kroger.com", "www.kroger.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "cereal", "url": "https://www.kroger.com/pl/cereal/09002"},
        {"category": "milk", "url": "https://www.kroger.com/pl/milk/02001"},
        {"category": "eggs", "url": "https://www.kroger.com/pl/eggs/02008"},
        {"category": "bread", "url": "https://www.kroger.com/pl/bread/03001"},
        {"category": "coffee", "url": "https://www.kroger.com/pl/coffee/11005"},
        {"category": "snacks", "url": "https://www.kroger.com/pl/snacks/12009"},
    ]

    def start_requests(self):
        target = self._resolve_target_url()
        target = self._with_page(target, 1)
        yield scrapy.Request(target, callback=self.parse, meta=({"page": 1}))

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        nd = extract_next_data(html)
        if nd:
            for item in extract_items_from_unknown_state(nd, source="kroger_next_data"):
                yielded += 1
                item.update({"mode": "category", "category_url": self.category_url or self.url, "page": page, "source_url": response.url})
                yield item

        ap = extract_apollo_state(html)
        if ap:
            for item in extract_items_from_unknown_state(ap, source="kroger_apollo_state"):
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

        if yielded == 0 and not response.meta.get("listing_fallback_attempted"):
            inferred_q = self._infer_query_from_url(self.category_url or self.url or response.url)
            if inferred_q:
                fallback_url = f"https://www.kroger.com/search?{urlencode({'query': inferred_q, 'searchType': 'default_search'})}"
                self.logger.warning("Kroger listing empty; retrying via search fallback: %s", fallback_url)
                yield scrapy.Request(
                    fallback_url,
                    callback=self.parse,
                    meta=({"page": page, "listing_fallback_attempted": True}),
                    dont_filter=True,
                )
                return

        if yielded == 0:
            self.logger.warning("Kroger listing produced 0 items (status=%s)", response.status)

        if page < self.args.max_pages:
            next_page = page + 1
            next_url = self._with_page(self._resolve_target_url(), next_page)
            yield scrapy.Request(next_url, callback=self.parse, meta=({"page": next_page}))

    def _resolve_target_url(self) -> str:
        if self.url:
            return self.url
        if self.category_url:
            return self.category_url
        for entry in self.categories:
            if entry.get("category") == self.category:
                self.category_url = entry.get("url")
                return self.category_url
        names = ", ".join(sorted([c["category"] for c in self.categories]))
        raise ValueError(f"Unknown category '{self.category}'. Use one of: {names}")

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _infer_query_from_url(self, url: str) -> str | None:
        p = urlparse(url)
        m = re.search(r"/pl/([^/]+)/", p.path or "")
        if not m:
            return None
        slug = (m.group(1) or "").strip().replace("-", " ")
        return slug or None

    def _extract_product_links(self, html: str):
        direct_pat = re.compile(r'href=["\'](?P<url>/p/[^"\']+)["\']', re.I)
        escaped_pat = re.compile(r'\\/p\\/(?P<id>[A-Za-z0-9_-]+)')
        seen: set[str] = set()
        for m in direct_pat.finditer(html or ""):
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

        for m in escaped_pat.finditer(html or ""):
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
