from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.settings import PROXY


class NordstromListingSpider(scrapy.Spider):
    name = "nordstrom_listing"
    allowed_domains = ["nordstrom.com", "www.nordstrom.com", "r.jina.ai", "duckduckgo.com", "bing.com", "www.bing.com"]
    custom_settings = {"HTTPERROR_ALLOW_ALL": True}

    def __init__(self, q: str | None = None, url: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = (q or "").strip()
        self.url = (url or "").strip()
        self.max_pages = int(max_pages)

    def start_requests(self):
        target_url = self.url or f"https://www.nordstrom.com/sr?{urlencode({'keyword': self.q or 'sneakers'})}"
        meta = {"page": 1, "original_url": target_url}
        if PROXY:
            meta["proxy"] = PROXY
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)

    def parse(self, response):
        if self._is_blocked(response):
            q = self.q or "sneakers"
            bing_rss = f"https://www.bing.com/search?{urlencode({'q': f'site:nordstrom.com/s/ {q}', 'format': 'rss'})}"
            yield scrapy.Request(bing_rss, callback=self.parse_bing_rss, meta={"page": response.meta.get("page", 1), "query": q})
            return

        cards = response.css("a[href*='/s/']")
        seen = set()
        for a in cards:
            url = response.urljoin(a.attrib.get("href", ""))
            if "/s/" not in url or url in seen:
                continue
            seen.add(url)
            title = " ".join(t.strip() for t in a.css("*::text").getall() if t.strip())
            yield {"item_id": self._extract_item_id(url), "title": title[:300], "url": url, "source": "nordstrom_html"}

    def parse_jina(self, response):
        for chunk in re.split(r"\n(?=\[### )", response.text):
            m = re.search(r"\[###\s+(.*?)\]\((https?://[^)]+)\)", chunk)
            if not m:
                continue
            title, url = m.group(1).strip(), m.group(2).strip()
            if "nordstrom.com" not in url:
                continue
            yield {
                "item_id": self._extract_item_id(url),
                "title": title,
                "url": url,
                "image_url": self._extract_image(chunk),
                "price": self._extract_price(chunk),
                "rating": self._extract_float(chunk),
                "reviews_count": self._extract_int(chunk),
                "is_sponsored": bool(re.search(r"\bsponsored\b", chunk, re.I)),
                "source": "r.jina.ai_fallback",
            }

        p = int(response.meta.get("page", 1))
        if p >= self.max_pages:
            return
        original = response.meta.get("original_url")
        if not original:
            return
        next_original = self._with_page(original, p + 1)
        yield scrapy.Request(
            f"https://r.jina.ai/http://{next_original.replace('https://', '').replace('http://', '')}",
            callback=self.parse_jina,
            meta={"page": p + 1, "original_url": next_original},
        )

    def parse_bing_rss(self, response):
        for item in response.xpath('//item'):
            title = (item.xpath('title/text()').get() or '').strip()
            url = (item.xpath('link/text()').get() or '').strip()
            snippet = (item.xpath('description/text()').get() or '').strip()
            if 'nordstrom.com/s/' not in url:
                continue
            yield {
                "item_id": self._extract_item_id(url),
                "title": title,
                "url": url,
                "price": self._extract_price(snippet),
                "rating": self._extract_float(snippet),
                "reviews_count": self._extract_int(snippet),
                "is_sponsored": False,
                "source": "bing_rss_fallback",
            }

    def _is_blocked(self, response):
        t = (response.text or "").lower()
        return response.status in {307, 403, 412, 418, 429, 503} or "access denied" in t or "robot" in t

    def _with_page(self, url: str, page: int) -> str:
        p = urlparse(url)
        q = parse_qs(p.query)
        q["page"] = [str(page)]
        return urlunparse(p._replace(query=urlencode(q, doseq=True)))

    def _extract_item_id(self, url: str) -> str | None:
        m = re.search(r"/s/[^/?#]+/(\d+)", url)
        return m.group(1) if m else None

    def _extract_image(self, text: str) -> str | None:
        m = re.search(r"!\[[^\]]*\]\((https?://[^)]+)\)", text)
        return m.group(1) if m else None

    def _extract_price(self, text: str) -> float | None:
        m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text or "")
        return float(m.group(1)) if m else None

    def _extract_float(self, text: str) -> float | None:
        m = re.search(r"(\d+(?:\.\d+)?)\s*out of\s*5", text or "", re.I)
        return float(m.group(1)) if m else None

    def _extract_int(self, text: str) -> int | None:
        m = re.search(r"(\d[\d,]*)\s+reviews", text or "", re.I)
        return int(m.group(1).replace(',', '')) if m else None
