from __future__ import annotations

"""eBay keyword search spider.

eBay actively challenges automated traffic (splashui/challenge). In this
environment, direct fetch may hit the challenge. We attempt direct fetch and
fallback to r.jina.ai text extraction for the same URL.

Usage:
  scrapy crawl ebay_search -a q=laptop -a max_pages=2

Notes:
- This implementation is HTML/markdown-based; once we can access a stable JSON
  endpoint without challenge we can swap parsing to that internal endpoint.
"""

import re
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider


class EbaySearchSpider(BaseSearchSpider):
    name = "ebay_search"
    allowed_domains = ["ebay.com", "www.ebay.com", "r.jina.ai"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    def __init__(self, q: str | None = None, max_pages: int = 1, use_proxy: int | str | None = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages, use_proxy=use_proxy)

    def start_requests(self):
        url = self._build_search_url(self.args.q or "")
        yield scrapy.Request(url, callback=self.parse, meta=self.maybe_proxy_meta({"page": 1, "original_url": url}))

    def parse(self, response: scrapy.http.Response):
        original_url = response.meta.get("original_url") or response.url
        page = int(response.meta.get("page", 1))

        if self._looks_like_challenge(response):
            jina_url = self._to_jina_url(original_url)
            yield scrapy.Request(
                jina_url,
                callback=self.parse_jina,
                meta={"page": page, "original_url": original_url},
            )
            return

        # If we didn't get challenged, try parsing as text/html.
        items = list(self._parse_ebay_html(response.text, mode="keyword", query=self.args.q, page=page))
        if not items:
            # eBay sometimes serves a 200 challenge page; fallback to jina anyway.
            jina_url = self._to_jina_url(original_url)
            yield scrapy.Request(
                jina_url,
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
        text = response.text or ""

        # r.jina.ai returns markdown-ish text; parse links.
        yield from self._parse_ebay_markdown(text, mode="keyword", query=self.args.q, page=page)

        if page < self.args.max_pages:
            next_url = self._with_page(original_url, page + 1)
            yield scrapy.Request(
                self._to_jina_url(next_url),
                callback=self.parse_jina,
                meta={"page": page + 1, "original_url": next_url},
            )

    @staticmethod
    def _build_search_url(q: str) -> str:
        return f"https://www.ebay.com/sch/i.html?{urlencode({'_nkw': q, '_ipg': 60})}"

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["_pgn"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    @staticmethod
    def _to_jina_url(url: str) -> str:
        # Use http:// prefix as required by r.jina.ai for remote fetch
        return f"https://r.jina.ai/http://{url}"

    @staticmethod
    def _looks_like_challenge(response: scrapy.http.Response) -> bool:
        # eBay often returns 200 with a bot challenge HTML.
        if response.status in (301, 302, 307, 308):
            return True
        if "/splashui/challenge" in (response.url or ""):
            return True
        body = (response.text or "")
        body_l = body.lower()
        return (
            "pardon our interruption" in body_l
            or "splashui/challenge" in body_l
            or "bot" in body_l and "interruption" in body_l
        )

    def _parse_ebay_html(self, html: str, *, mode: str, query: str | None, page: int):
        # Minimal HTML parsing via regex; eBay markup changes often.
        # Prefer markdown parsing via r.jina.ai when challenged.
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
                "source": "ebay_srp_html",
                "mode": mode,
                "query": query,
                "page": page,
            }

    def _parse_ebay_markdown(self, text: str, *, mode: str, query: str | None, page: int):
        # Capture markdown links: [Title](https://www.ebay.com/itm/123?...)
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

            # Attempt to extract price from nearby context.
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
                "source": "ebay_srp_markdown_via_jina",
                "mode": mode,
                "query": query,
                "page": page,
            }

    @staticmethod
    def _extract_item_id(url: str) -> str | None:
        m = re.search(r"/itm/(\d+)", url)
        return m.group(1) if m else None
