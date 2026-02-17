from __future__ import annotations

import json
import re
from urllib.parse import urlencode, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.retail_bootstrap_utils import (
    extract_apollo_state,
    extract_items_from_unknown_state,
    extract_json_ld_products,
    extract_next_data,
)


class SallybeautyListingSpider(BaseListingSpider):
    name = "sallybeauty_listing"
    allowed_domains = ["sallybeauty.com", "www.sallybeauty.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "hair-color", "url": "https://www.sallybeauty.com/hair-color/"},
        {"category": "hair-care", "url": "https://www.sallybeauty.com/hair-care/"},
        {"category": "nails", "url": "https://www.sallybeauty.com/nails/"},
    ]

    def start_requests(self):
        mode = (getattr(self, "mode", None) or "api").strip().lower()
        target = self.resolve_target_url()
        if mode == "html":
            yield scrapy.Request(target, callback=self.parse_html, meta=self.proxy_meta({"page": 1, "origin": target}))
            return
        if mode == "bootstrap":
            yield scrapy.Request(target, callback=self.parse_bootstrap, meta=self.proxy_meta({"page": 1, "origin": target}))
            return

        # internal endpoint attempt (SFCC-style category grid)
        api_url = self._build_api_url(page=1)
        if api_url:
            yield scrapy.Request(api_url, callback=self.parse_api, meta=self.proxy_meta({"page": 1, "origin": target}), headers={"x-requested-with": "XMLHttpRequest"})
        else:
            yield scrapy.Request(target, callback=self.parse_bootstrap, meta=self.proxy_meta({"page": 1, "origin": target}))

    def _build_api_url(self, page: int) -> str | None:
        u = urlparse(self.resolve_target_url())
        path_parts = [p for p in (u.path or "").split("/") if p]
        if not path_parts:
            return None
        cgid = path_parts[0]
        start = max(page - 1, 0) * 48
        return (
            "https://www.sallybeauty.com/on/demandware.store/Sites-SallyBeauty-Site/default/Search-UpdateGrid?"
            + urlencode({"cgid": cgid, "start": start, "sz": 48, "format": "ajax"})
        )

    def parse_api(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        yielded = 0

        try:
            payload = json.loads(response.text)
        except Exception:
            payload = None

        if isinstance(payload, dict):
            for item in extract_items_from_unknown_state(payload, source="sallybeauty_internal_api"):
                yielded += 1
                item.update({"mode": "category", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            for item in self._extract_html_cards(response):
                yielded += 1
                item.update({"source": "sallybeauty_internal_api_html", "mode": "category", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            origin = response.meta.get("origin") or self.resolve_target_url()
            yield scrapy.Request(origin, callback=self.parse_bootstrap, meta=self.proxy_meta({"page": page, "origin": origin}), dont_filter=True)
            return

        if page < self.max_pages:
            next_page = page + 1
            next_api = self._build_api_url(next_page)
            if next_api:
                yield scrapy.Request(next_api, callback=self.parse_api, meta=self.proxy_meta({"page": next_page, "origin": response.meta.get("origin")}), headers={"x-requested-with": "XMLHttpRequest"})

    def parse_bootstrap(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        nd = extract_next_data(html)
        if nd:
            for item in extract_items_from_unknown_state(nd, source="sallybeauty_next_data"):
                yielded += 1
                item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
                yield item

        ap = extract_apollo_state(html)
        if ap:
            for item in extract_items_from_unknown_state(ap, source="sallybeauty_apollo_state"):
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
                item.update({"source": "sallybeauty_html_fallback", "mode": "category_html", "category_url": response.meta.get("origin"), "page": page})
                yield item

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        count = 0
        for item in self._extract_html_cards(response):
            count += 1
            item.update({"source": "sallybeauty_html", "mode": "category_html", "category_url": response.meta.get("origin"), "page": page})
            yield item
        if count == 0:
            self.logger.warning("Sally Beauty html mode returned 0 items (status=%s)", response.status)

    def _extract_html_cards(self, response: scrapy.http.Response):
        seen: set[str] = set()
        for a in response.xpath('//a[contains(@href,"/p/") or contains(@href,"/product") or contains(@href,".html")]'):
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
            item_id = None
            im = re.search(r"(?:sku=|/p/)([A-Za-z0-9_-]{4,})", url)
            if im:
                item_id = im.group(1)
            yield {
                "item_id": item_id,
                "title": text or None,
                "url": url,
                "price": price,
                "currency": "USD" if price is not None else None,
                "brand": "Sally Beauty",
                "rating": None,
                "reviews_count": None,
                "image_url": img,
                "raw": None,
            }
