from __future__ import annotations

"""StockX listing spider (bootstrap-first via __NEXT_DATA__).

Usage:
  scrapy crawl stockx_listing -a category='sneakers' -a max_pages=1
  scrapy crawl stockx_listing -a category_url='https://stockx.com/sneakers' -a max_pages=1
"""

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.retail_bootstrap_utils import (
    extract_items_from_unknown_state,
    extract_json_ld_products,
    extract_next_data,
)


class StockxListingSpider(BaseListingSpider):
    name = "stockx_listing"
    allowed_domains = ["stockx.com", "www.stockx.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "sneakers", "url": "https://stockx.com/sneakers"},
        {"category": "apparel", "url": "https://stockx.com/apparel"},
        {"category": "electronics", "url": "https://stockx.com/electronics"},
        {"category": "trading-cards", "url": "https://stockx.com/trading-cards"},
        {"category": "collectibles", "url": "https://stockx.com/collectibles"},
    ]

    def start_requests(self):
        target = self.resolve_target_url()
        target = self._with_page(target, 1)
        yield scrapy.Request(target, callback=self.parse, meta={"page": 1})

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        nd = extract_next_data(html)
        if nd:
            for item in extract_items_from_unknown_state(nd, source="stockx_next_data"):
                item["url"] = self._absolutize(item.get("url"))
                if not item.get("url"):
                    continue
                yielded += 1
                item.update(
                    {
                        "mode": "category_bootstrap",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yield item

        if yielded == 0:
            for item in extract_json_ld_products(html):
                item["url"] = self._absolutize(item.get("url"))
                if not item.get("url"):
                    continue
                yielded += 1
                item.update(
                    {
                        "mode": "category_bootstrap",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yield item

        if yielded == 0:
            for item in self._extract_html_links(html):
                yielded += 1
                item.update(
                    {
                        "mode": "category_html",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yield item

        if yielded == 0:
            self.logger.warning("StockX listing produced 0 items (status=%s page=%s)", response.status, page)

        if page < self.max_pages:
            next_page = page + 1
            next_url = self._with_page(self.resolve_target_url(), next_page)
            yield scrapy.Request(next_url, callback=self.parse, meta={"page": next_page})

    def _extract_html_links(self, html: str):
        seen: set[str] = set()
        # Product links are usually simple slugs off domain root.
        pat = re.compile(r'href=["\'](?P<u>/(?!about|help|news|login|signup|account|sell|buy|sneakers|apparel|electronics|collectibles|trading-cards)[a-z0-9][a-z0-9\-]{3,})["\']', re.I)
        for m in pat.finditer(html or ""):
            rel = m.group("u")
            url = self._absolutize(rel)
            if not url or url in seen:
                continue
            seen.add(url)
            slug = rel.strip("/")
            yield {
                "item_id": slug,
                "title": slug.replace("-", " ").title(),
                "url": url,
                "price": None,
                "currency": None,
                "brand": None,
                "rating": None,
                "reviews_count": None,
                "image_url": None,
                "source": "stockx_html_links_fallback",
                "raw": None,
            }

    @staticmethod
    def _absolutize(url: str | None) -> str | None:
        if not isinstance(url, str) or not url:
            return None
        if url.startswith("//"):
            return f"https:{url}"
        if url.startswith("/"):
            return f"https://stockx.com{url}"
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
