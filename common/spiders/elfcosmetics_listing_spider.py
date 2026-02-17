from __future__ import annotations

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.retail_bootstrap_utils import (
    extract_apollo_state,
    extract_items_from_unknown_state,
    extract_json_ld_products,
    extract_next_data,
)


class ElfcosmeticsListingSpider(BaseListingSpider):
    name = "elfcosmetics_listing"
    allowed_domains = ["elfcosmetics.com", "www.elfcosmetics.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "face", "url": "https://www.elfcosmetics.com/face"},
        {"category": "eyes", "url": "https://www.elfcosmetics.com/eyes"},
        {"category": "lips", "url": "https://www.elfcosmetics.com/lips"},
    ]

    def start_requests(self):
        mode = (getattr(self, "mode", None) or "api").strip().lower()
        target = self.resolve_target_url()
        if mode == "html":
            first = self._with_page(target, 1)
            yield scrapy.Request(first, callback=self.parse_html, meta=self.proxy_meta({"page": 1, "origin": target}))
            return
        if mode == "bootstrap":
            first = self._with_page(target, 1)
            yield scrapy.Request(first, callback=self.parse_bootstrap, meta=self.proxy_meta({"page": 1, "origin": target}))
            return

        api_url = self._build_api_url(page=1)
        if api_url:
            yield scrapy.Request(api_url, callback=self.parse_api, meta=self.proxy_meta({"page": 1, "origin": target}), headers={"accept": "application/json,text/plain,*/*"})
        else:
            first = self._with_page(target, 1)
            yield scrapy.Request(first, callback=self.parse_bootstrap, meta=self.proxy_meta({"page": 1, "origin": target}))

    def _build_api_url(self, page: int) -> str | None:
        # exploratory endpoint used by Shopify-backed storefront search providers
        target = self.resolve_target_url()
        return f"https://www.elfcosmetics.com/search/suggest.json?{urlencode({'q': target, 'resources[type]': 'product', 'page': page})}"

    def parse_api(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        yielded = 0

        try:
            payload = json.loads(response.text)
        except Exception:
            payload = None

        if isinstance(payload, dict):
            for item in extract_items_from_unknown_state(payload, source="elfcosmetics_internal_api"):
                yielded += 1
                item.update({"mode": "category", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            origin = response.meta.get("origin") or self.resolve_target_url()
            first = self._with_page(origin, page)
            yield scrapy.Request(first, callback=self.parse_bootstrap, meta=self.proxy_meta({"page": page, "origin": origin}), dont_filter=True)
            return

    def parse_bootstrap(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        nd = extract_next_data(html)
        if nd:
            for item in extract_items_from_unknown_state(nd, source="elfcosmetics_next_data"):
                yielded += 1
                item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
                yield item

        ap = extract_apollo_state(html)
        if ap:
            for item in extract_items_from_unknown_state(ap, source="elfcosmetics_apollo_state"):
                yielded += 1
                item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            for item in extract_json_ld_products(html):
                yielded += 1
                item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            for item in self._extract_html_cards(response):
                yielded += 1
                item.update({"source": "elfcosmetics_html_fallback", "mode": "category_html", "category_url": response.meta.get("origin"), "page": page})
                yield item

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        count = 0
        for item in self._extract_html_cards(response):
            count += 1
            item.update({"source": "elfcosmetics_html", "mode": "category_html", "category_url": response.meta.get("origin"), "page": page})
            yield item
        if count == 0:
            self.logger.warning("e.l.f. html mode returned 0 items (status=%s)", response.status)

    def _extract_html_cards(self, response: scrapy.http.Response):
        seen: set[str] = set()
        for a in response.xpath('//a[contains(@href,"/products/") or contains(@href,"/p/")]'):
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)
            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            text = re.sub(r"\s+", " ", " ".join(card.xpath('.//text()').getall())).strip() if card else ""
            img = (card.xpath('.//img/@src').get() if card else None) or (card.xpath('.//img/@data-src').get() if card else None)
            m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
            price = float(m.group(1)) if m else None
            yield {
                "item_id": self._extract_id(url),
                "title": text or None,
                "url": url,
                "price": price,
                "currency": "USD" if price is not None else None,
                "brand": "e.l.f. Cosmetics",
                "rating": None,
                "reviews_count": None,
                "image_url": img,
                "raw": None,
            }

    @staticmethod
    def _extract_id(url: str) -> str | None:
        m = re.search(r"(?:variant=|/products/|/p/)([A-Za-z0-9_-]{4,})", url or "")
        return m.group(1) if m else None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
