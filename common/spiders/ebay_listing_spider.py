from __future__ import annotations

"""eBay category listing spider.

Requires category_url (or url).

Usage:
  scrapy crawl ebay_listing -a category_url='https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276' -a max_pages=2

Behavior:
- Attempt direct fetch; if challenged, fallback to r.jina.ai for the same URL.
"""

import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class EbayListingSpider(BaseListingSpider):
    name = "ebay_listing"
    allowed_domains = ["ebay.com", "www.ebay.com", "r.jina.ai"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    def __init__(
        self,
        category_url: str | None = None,
        url: str | None = None,
        max_pages: int = 1,
        use_proxy: int | str | None = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.init_listing_args(max_pages=max_pages, use_proxy=use_proxy, url=url, category_url=category_url)

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

        if self._looks_like_challenge(response):
            yield scrapy.Request(
                self._to_jina_url(original_url),
                callback=self.parse_jina,
                meta={"page": page, "original_url": original_url},
            )
            return

        items = list(self._parse_ebay_html(response.text, page=page))
        if not items:
            yield scrapy.Request(
                self._to_jina_url(original_url),
                callback=self.parse_jina,
                meta={"page": page, "original_url": original_url},
            )
            return

        for it in items:
            yield it

        if page < self.args.max_pages:
            next_url = self._with_page(original_url, page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta=self.maybe_proxy_meta({"page": page + 1, "original_url": next_url}),
            )

    def parse_jina(self, response: scrapy.http.Response):
        original_url = response.meta.get("original_url") or ""
        page = int(response.meta.get("page", 1))
        yield from self._parse_ebay_markdown(response.text or "", page=page)

        if page < self.args.max_pages:
            next_url = self._with_page(original_url, page + 1)
            yield scrapy.Request(
                self._to_jina_url(next_url),
                callback=self.parse_jina,
                meta={"page": page + 1, "original_url": next_url},
            )

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs.setdefault("_ipg", ["60"])  # results per page
        qs["_pgn"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    @staticmethod
    def _to_jina_url(url: str) -> str:
        return f"https://r.jina.ai/http://{url}"

    @staticmethod
    def _looks_like_challenge(response: scrapy.http.Response) -> bool:
        if response.status in (301, 302, 307, 308):
            return True
        if "/splashui/challenge" in (response.url or ""):
            return True
        body_l = (response.text or "").lower()
        return "pardon our interruption" in body_l or "splashui/challenge" in body_l

    def _parse_ebay_html(self, html: str, *, page: int):
        for m in re.finditer(r'href="(https://www\.ebay\.com/itm/\d+[^\"]*)"[^>]*>([^<]{3,200})<', html):
            url = m.group(1)
            title = re.sub(r"\s+", " ", m.group(2)).strip()
            item_id = self._extract_item_id(url)
            if not item_id:
                continue
            yield {
                "item_id": item_id,
                "title": title,
                "url": url,
                "source": "ebay_category_html",
                "mode": "category",
                "category_url": self.category_url,
                "page": page,
            }

    def _parse_ebay_markdown(self, text: str, *, page: int):
        pat = re.compile(r"\[(?P<title>[^\]]{3,200})\]\((?P<url>https://www\.ebay\.com/itm/\d+[^)]*)\)")
        seen: set[str] = set()
        for m in pat.finditer(text or ""):
            url = m.group("url")
            if url in seen:
                continue
            seen.add(url)

            title = re.sub(r"\s+", " ", m.group("title")).strip()
            item_id = self._extract_item_id(url)
            if not item_id:
                continue

            start = m.end()
            snippet = (text or "")[start : start + 500]
            price = None
            pm = re.search(r"\$\s?\d[\d,]*\.\d{2}", snippet)
            if pm:
                price = pm.group(0).replace(" ", "")

            yield {
                "item_id": item_id,
                "title": title,
                "url": url,
                "price": price,
                "source": "ebay_category_markdown_via_jina",
                "mode": "category",
                "category_url": self.category_url,
                "page": page,
            }

    @staticmethod
    def _extract_item_id(url: str) -> str | None:
        m = re.search(r"/itm/(\d+)", url)
        return m.group(1) if m else None
