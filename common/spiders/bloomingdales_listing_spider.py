from __future__ import annotations

import re
from urllib.parse import parse_qs, urljoin, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class BloomingdalesListingSpider(BaseListingSpider):
    """Bloomingdale's listing spider via r.jina.ai markdown mirror."""

    name = "bloomingdales_listing"
    allowed_domains = ["r.jina.ai", "bloomingdales.com", "www.bloomingdales.com"]

    categories = [
        {"category": "women", "url": "https://www.bloomingdales.com/shop/womens-apparel?id=2910"},
        {"category": "men", "url": "https://www.bloomingdales.com/shop/mens?id=3864"},
        {"category": "shoes", "url": "https://www.bloomingdales.com/shop/womens-designer-shoes?id=16961"},
        {"category": "beauty", "url": "https://www.bloomingdales.com/shop/makeup-perfume-beauty?id=2921"},
        {"category": "home", "url": "https://www.bloomingdales.com/shop/home?id=3865"},
    ]

    def start_requests(self):
        target_url = self.resolve_target_url()
        mirror_url = self._to_jina_url(target_url)
        yield scrapy.Request(
            mirror_url,
            callback=self.parse,
            meta={"target_url": target_url, "page_index": 1},
            headers={"accept": "text/plain,text/markdown;q=0.9,*/*;q=0.8"},
        )

    def parse(self, response: scrapy.http.Response):
        products = self._extract_products(response.text)
        seen: set[str] = set()

        for product in products:
            item_id = product.get("item_id")
            if item_id and item_id in seen:
                continue
            if item_id:
                seen.add(item_id)
            yield product

    def _extract_products(self, markdown: str) -> list[dict]:
        out: list[dict] = []
        pattern = re.compile(
            r"\[(?P<title>[^\]]+)\]\((?P<url>https?://www\.bloomingdales\.com/shop/product/[^)\s]+)"
            r"(?:\s+\"(?P<title_attr>[^\"]+)\")?\)\s*(?P<price>\$[\d,]+(?:\.\d{2})?)?",
            re.I,
        )

        for m in pattern.finditer(markdown):
            url = m.group("url")
            title = (m.group("title") or "").strip()
            title_attr = (m.group("title_attr") or "").strip()
            clean_title = self._clean_title(title_attr or title)
            price_text = m.group("price")

            parsed = urlparse(url)
            q = parse_qs(parsed.query)
            item_id = (q.get("ID") or q.get("id") or [None])[0]

            out.append(
                {
                    "item_id": str(item_id) if item_id else None,
                    "title": clean_title or None,
                    "url": self._normalize_url(url),
                    "price": self._to_float(price_text.replace("$", "").replace(",", "") if price_text else None),
                    "price_text": price_text,
                    "source": "bloomingdales_markdown_via_r.jina.ai",
                }
            )

        return out

    def _to_jina_url(self, url: str) -> str:
        normalized = url.replace("https://", "").replace("http://", "")
        return f"https://r.jina.ai/http://{normalized}"

    def _normalize_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return urljoin("https://www.bloomingdales.com", url)

    def _clean_title(self, raw: str) -> str:
        text = re.sub(r"\s+", " ", raw).strip()
        text = re.sub(r"^(NEW!?|New:?|Exclusive:?|Shop New:)\s*", "", text, flags=re.I)
        return text.strip()

    def _to_float(self, value: str | None):
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None
