from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.settings import PROXY


class MacysListingSpider(scrapy.Spider):
    name = "macys_listing"
    allowed_domains = ["macys.com", "www.macys.com", "r.jina.ai"]
    custom_settings = {"HTTPERROR_ALLOW_ALL": True}

    def __init__(self, q: str | None = None, url: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = (q or "").strip()
        self.url = (url or "").strip()
        self.max_pages = int(max_pages)

    def start_requests(self):
        target_url = self.url or f"https://www.macys.com/shop/featured/{(self.q or 'laptop').replace(' ', '%20')}"
        meta = {"page": 1, "original_url": target_url}
        if PROXY:
            meta["proxy"] = PROXY
        yield scrapy.Request(target_url, callback=self.parse, meta=meta)

    def parse(self, response):
        if self._is_blocked(response):
            original_url = response.meta.get("original_url") or response.url
            yield scrapy.Request(
                f"https://r.jina.ai/http://{original_url.replace('https://', '').replace('http://', '')}",
                callback=self.parse_jina,
                meta={"page": response.meta.get("page", 1), "original_url": original_url},
            )
            return

        cards = response.css("a[href*='/shop/product/']")
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
                "source": "macys_html",
            }

    def parse_jina(self, response):
        lines = [ln.strip() for ln in response.text.splitlines()]
        brand_markers = {"hp", "lenovo", "asus", "dell", "acer", "samsonite", "nimo", "kenneth cole reaction"}

        for i, line in enumerate(lines):
            if not line:
                continue
            if line.lower() not in brand_markers:
                continue

            title = (lines[i + 1].strip() if i + 1 < len(lines) else "")
            if not title or len(title) < 8:
                continue

            window = " ".join(lines[i : i + 10])
            price = self._extract_price(window)
            if price is None:
                continue

            yield {
                "item_id": None,
                "title": f"{line} {title}"[:400],
                "url": None,
                "image_url": None,
                "price": price,
                "rating": self._extract_float(window),
                "reviews_count": self._extract_int(window),
                "is_sponsored": bool(re.search(r"\bsponsored\b", window, re.I)),
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

    def _is_blocked(self, response):
        t = (response.text or "").lower()
        return response.status in {307, 403, 412, 418, 429, 503} or "access denied" in t or "robot" in t

    def _with_page(self, url: str, page: int) -> str:
        p = urlparse(url)
        q = parse_qs(p.query)
        q["page"] = [str(page)]
        return urlunparse(p._replace(query=urlencode(q, doseq=True)))

    def _extract_item_id(self, url: str) -> str | None:
        m = re.search(r"ID=(\d+)", url)
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
        if not m:
            m = re.search(r"\((\d[\d,]*)\)", text or "")
        return int(m.group(1).replace(',', '')) if m else None
