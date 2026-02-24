from __future__ import annotations

import re
from urllib.parse import urlparse

import requests
import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class QvcListingSpider(BaseListingSpider):
    """QVC listing spider via r.jina.ai markdown mirror of category pages."""

    name = "qvc_listing"
    allowed_domains = ["qvc.com", "www.qvc.com"]

    categories = [
        {"category": "beauty", "url": "https://www.qvc.com/c/beauty/-/rhty/c.html"},
        {"category": "fashion", "url": "https://www.qvc.com/c/fashion/-/lglt/c.html"},
        {"category": "home", "url": "https://www.qvc.com/c/for-the-home/-/lglu/c.html"},
        {"category": "kitchen", "url": "https://www.qvc.com/c/kitchen-and-food/-/lglv/c.html"},
    ]

    product_url_re = re.compile(r"https://www\.qvc\.com/[^\s)]+\.product\.[^\s)]+", re.I)
    price_re = re.compile(r"\$(\d[\d,]*\.\d{2})")

    def start_requests(self):
        # Bootstrap request so Scrapy opens/spider lifecycle stays normal.
        yield scrapy.Request("https://www.qvc.com/robots.txt", callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        category_url = self.resolve_target_url()
        seen: set[str] = set()

        for page in range(1, self.max_pages + 1):
            page_url = self._page_url(category_url, page)
            md = self._fetch_markdown(page_url)
            for m in self.product_url_re.finditer(md):
                url = m.group(0)
                item_id = self._extract_item_id(url)
                if item_id in seen:
                    continue
                seen.add(item_id)

                context = md[max(0, m.start() - 180) : m.start()]
                title = self._extract_title(context, url)
                price = self._extract_price(context)

                yield {
                    "item_id": item_id,
                    "title": title or None,
                    "url": url,
                    "price": price,
                    "source": "qvc_markdown_via_r.jina.ai",
                }

    def _fetch_markdown(self, url: str) -> str:
        jina_url = f"https://r.jina.ai/http://{url}"
        r = requests.get(jina_url, timeout=60)
        r.raise_for_status()
        return r.text

    def _page_url(self, url: str, page: int) -> str:
        if page <= 1:
            return url
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}currentPage={page}"

    def _extract_item_id(self, url: str) -> str:
        m = re.search(r"\.product\.([A-Z0-9]+)\.html", url, re.I)
        if m:
            return m.group(1).upper()
        path = urlparse(url).path
        return path.rsplit("/", 1)[-1]

    def _extract_price(self, text: str) -> float | None:
        m = self.price_re.search(text)
        if not m:
            return None
        try:
            return float(m.group(1).replace(",", ""))
        except Exception:
            return None

    def _extract_title(self, context: str, url: str) -> str:
        m = re.search(r"Image\s+\d+:\s*([^\]]+)$", context, re.I)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()

        slug = urlparse(url).path.rsplit("/", 1)[-1].split(".product.")[0]
        return slug.replace("-", " ").strip()
