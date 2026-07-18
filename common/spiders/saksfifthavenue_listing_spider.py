from __future__ import annotations

"""Saks Fifth Avenue listing spider (direct HTML extraction).

Usage examples:
  scrapy crawl saksfifthavenue_listing -a category='men' -a max_pages=1
  scrapy crawl saksfifthavenue_listing -a category_url='https://www.saksfifthavenue.com/c/men' -a max_pages=2
"""

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SaksfifthavenueListingSpider(BaseListingSpider):
    name = "saksfifthavenue_listing"
    allowed_domains = ["saksfifthavenue.com", "www.saksfifthavenue.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    categories = [
        {"category": "women", "url": "https://www.saksfifthavenue.com/c/women-s-apparel"},
        {"category": "men", "url": "https://www.saksfifthavenue.com/c/men"},
        {"category": "shoes", "url": "https://www.saksfifthavenue.com/c/shoes"},
        {"category": "beauty", "url": "https://www.saksfifthavenue.com/c/beauty"},
        {"category": "handbags", "url": "https://www.saksfifthavenue.com/c/handbags"},
    ]

    def start_requests(self):
        target_base = self.resolve_target_url()
        first_url = self._with_page(target_base, 1)
        yield scrapy.Request(first_url, callback=self.parse, meta={"page": 1, "target_base": target_base})

    def parse(self, response: scrapy.http.Response):
        target_base = response.meta.get("target_base") or self.resolve_target_url()
        page = int(response.meta.get("page", 1))

        tiles = response.css("div.product-tile")
        seen: set[str] = set()

        for tile in tiles:
            item = self._extract_tile_item(tile)
            if not item:
                continue

            key = item.get("item_id") or item.get("url")
            if key and key in seen:
                continue
            if key:
                seen.add(key)

            item.update(
                {
                    "mode": "category",
                    "category_url": target_base,
                    "page": page,
                    "source_url": response.url,
                    "source": "saksfifthavenue_direct_html",
                }
            )
            yield item

        if not tiles:
            self.logger.warning("Saks listing produced 0 items page=%s url=%s", page, response.url)

        if page < self.max_pages:
            next_page = page + 1
            next_url = self._with_page(target_base, next_page)
            yield scrapy.Request(next_url, callback=self.parse, meta={"page": next_page, "target_base": target_base})

    @staticmethod
    def _with_page(url: str, page: int, page_size: int = 24) -> str:
        start = max(0, (page - 1) * page_size)
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["start"] = [str(start)]
        qs["sz"] = [str(page_size)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _extract_tile_item(self, tile: scrapy.Selector) -> dict | None:
        rel = tile.css("a.product-tile-url::attr(href), a.thumb-link::attr(href)").get()
        url = self._normalize_url((rel or "").strip()) if rel else None

        item_id = (tile.css("span.bf-product-id::text").get() or "").strip() or None
        if url:
            m = re.search(r"-(\d{10,})\.html", url)
            if m and (not item_id or len(m.group(1)) >= len(item_id)):
                item_id = m.group(1)

        brand = (tile.css(".product-brand ::text").get() or "").strip()
        name = (tile.css(".tile-product-name ::text, .product-description ::text, a.product-tile-url::attr(title)").get() or "").strip()
        if not name and url:
            slug = re.search(r"/product/([^/]+)-\d+\.html", url)
            if slug:
                name = slug.group(1).replace("-", " ").strip().title()

        title = name or brand or None
        if brand and name and not name.lower().startswith(brand.lower()):
            title = f"{brand} {name}".strip()

        price_chunks = [x.strip() for x in tile.css(".price ::text, .bfx-price::text").getall() if x.strip()]
        dedup_chunks: list[str] = []
        for chunk in price_chunks:
            if chunk not in dedup_chunks:
                dedup_chunks.append(chunk)
        price_text = " ".join(dedup_chunks)
        price_val = self._to_float(price_text)

        if not (url and (item_id or title)):
            return None

        return {
            "item_id": item_id,
            "title": title,
            "url": url,
            "price": price_val,
            "price_text": price_text or None,
        }

    @staticmethod
    def _normalize_url(url: str) -> str:
        if not url:
            return ""
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return f"https://www.saksfifthavenue.com{url}"

    @staticmethod
    def _to_float(value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).strip()
        if not text:
            return None
        m = re.search(r"\$\s*([0-9][0-9,]*(?:\.\d+)?)", text)
        if not m:
            return None
        try:
            return float(m.group(1).replace(",", ""))
        except Exception:
            return None
