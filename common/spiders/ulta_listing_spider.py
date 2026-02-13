from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.settings import PROXY


class UltaListingSpider(scrapy.Spider):
    name = "ulta_listing"
    allowed_domains = ["ulta.com", "www.ulta.com", "r.jina.ai"]
    custom_settings = {"HTTPERROR_ALLOW_ALL": True}

    def __init__(self, q: str | None = None, url: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = (q or "").strip()
        self.url = (url or "").strip()
        self.max_pages = int(max_pages)

    def start_requests(self):
        target_url = self.url or f"https://www.ulta.com/search?{urlencode({'search': self.q or 'shampoo'})}"
        meta = {"page": 1, "original_url": target_url}
        if PROXY:
            meta["proxy"] = PROXY
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)

    def parse(self, response: scrapy.http.Response):
        if self._is_blocked(response):
            original_url = response.meta.get("original_url") or response.url
            yield scrapy.Request(
                f"https://r.jina.ai/http://{original_url.replace('https://', '').replace('http://', '')}",
                callback=self.parse_jina,
                meta={"page": response.meta.get("page", 1), "original_url": original_url},
            )
            return

        cards = response.css("a[href*='/p/']")
        seen = set()
        for a in cards:
            url = response.urljoin(a.attrib.get("href", ""))
            if not url or url in seen:
                continue
            seen.add(url)
            title = " ".join(t.strip() for t in a.css("*::text").getall() if t.strip())
            price_text = " ".join(a.xpath("ancestor::*[1]//*[contains(text(),'$')]/text()").getall())
            yield {
                "item_id": self._extract_item_id(url),
                "title": title[:300],
                "url": url,
                "price": self._extract_price(price_text),
                "source": "ulta_html",
            }

    def parse_jina(self, response: scrapy.http.Response):
        text = response.text

        # Format commonly has plain text product groups (name + rating + price), no links.
        lines = [ln.strip() for ln in text.splitlines()]
        seen = set()
        for i, line in enumerate(lines):
            if not line or len(line) < 4:
                continue
            if line.lower().startswith(("title:", "url source:", "markdown content:", "sort by", "show filters")):
                continue
            if "out of 5 stars" not in " ".join(lines[i : i + 3]).lower():
                continue

            title = line
            if title in seen:
                continue
            seen.add(title)

            window = " ".join(lines[i : i + 8])
            price = self._extract_price(window)
            rating = self._extract_float(window)
            reviews_count = self._extract_int(window)
            if price is None and rating is None and reviews_count is None:
                continue

            yield {
                "item_id": None,
                "title": title,
                "url": None,
                "image_url": None,
                "price": price,
                "rating": rating,
                "reviews_count": reviews_count,
                "is_sponsored": bool(re.search(r"\bsponsored\b", window, re.I)),
                "source": "r.jina.ai_fallback",
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return
        original_url = response.meta.get("original_url")
        if not original_url:
            return
        next_original = self._with_page(original_url, current_page + 1)
        next_fallback = f"https://r.jina.ai/http://{next_original.replace('https://', '').replace('http://', '')}"
        yield scrapy.Request(next_fallback, callback=self.parse_jina, meta={"page": current_page + 1, "original_url": next_original})

    def _is_blocked(self, response):
        t = (response.text or "").lower()
        return response.status in {307, 403, 412, 418, 429, 503} or "access denied" in t or "robot" in t or "/blocked" in t

    def _with_page(self, url: str, page: int) -> str:
        parsed = urlparse(url)
        q = parse_qs(parsed.query)
        q["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(q, doseq=True)))

    def _extract_item_id(self, url: str) -> str | None:
        m = re.search(r"/p/([^/?#]+)", url)
        return m.group(1) if m else None

    def _extract_image(self, text: str) -> str | None:
        m = re.search(r"!\[[^\]]*\]\((https?://[^)]+)\)", text)
        return m.group(1) if m else None

    def _extract_price(self, text: str) -> float | None:
        m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text or "")
        return float(m.group(1)) if m else None

    def _extract_float(self, text: str) -> float | None:
        m = re.search(r"(\d+(?:\.\d+)?)\s*out of\s*5", text or "", re.I)
        if not m:
            return None
        return float(m.group(1))

    def _extract_int(self, text: str) -> int | None:
        m = re.search(r"(\d[\d,]*)\s+reviews", text or "", re.I)
        if not m:
            m = re.search(r"\((\d[\d,]*)\)", text or "")
        return int(m.group(1).replace(',', '')) if m else None
