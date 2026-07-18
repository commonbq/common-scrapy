from __future__ import annotations

import re
from urllib.parse import urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class QvcListingSpider(BaseListingSpider):
    """QVC listing spider using direct category HTML pages."""

    name = "qvc_listing"
    allowed_domains = ["qvc.com", "www.qvc.com"]

    categories = [
        {"category": "beauty", "url": "https://www.qvc.com/c/beauty/-/rhty/c.html"},
        {"category": "fashion", "url": "https://www.qvc.com/c/fashion/-/lglt/c.html"},
        {"category": "home", "url": "https://www.qvc.com/c/for-the-home/-/lglu/c.html"},
        {"category": "kitchen", "url": "https://www.qvc.com/c/kitchen-and-food/-/lglv/c.html"},
    ]

    product_url_re = re.compile(r"https://www\.qvc\.com/[^\s\"')]+\.product\.[^\s\"')]+", re.I)
    price_re = re.compile(r"\$(\d[\d,]*\.\d{2})")

    def start_requests(self):
        category_url = self.resolve_target_url()
        for page in range(1, self.max_pages + 1):
            page_url = self._page_url(category_url, page)
            yield scrapy.Request(
                page_url,
                callback=self.parse,
                meta={"page": page},
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                },
            )

    def parse(self, response: scrapy.http.Response):
        page_text = response.text
        seen: set[str] = set()

        for m in self.product_url_re.finditer(page_text):
            url = m.group(0)
            item_id = self._extract_item_id(url)
            if item_id in seen:
                continue
            seen.add(item_id)

            context = page_text[max(0, m.start() - 220) : min(len(page_text), m.end() + 220)]
            title = self._extract_title(context, url)
            price = self._extract_price(context)

            yield {
                "item_id": item_id,
                "title": title or None,
                "url": url,
                "price": price,
                "source": "qvc_direct_html",
            }

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
        # Common JSON-LD / inline snippets usually include a nearby product title.
        m = re.search(r'"name"\s*:\s*"([^\"]{4,200})"', context, re.I)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()

        slug = urlparse(url).path.rsplit("/", 1)[-1].split(".product.")[0]
        return slug.replace("-", " ").strip()
