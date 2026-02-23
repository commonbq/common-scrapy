from __future__ import annotations

import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SheinListingSpider(BaseListingSpider):
    name = "shein_listing"
    allowed_domains = ["shein.com", "www.shein.com", "us.shein.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "women", "url": "https://us.shein.com/Women-c-2030.html"},
        {"category": "dresses", "url": "https://us.shein.com/Women-Dresses-c-1727.html"},
        {"category": "tops", "url": "https://us.shein.com/Women-Tops-c-1779.html"},
    ]

    def start_requests(self):
        yield scrapy.Request(self.resolve_target_url(), callback=self.parse_html, meta={"page": 1})

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        title = response.xpath('//title/text()').get() or ''
        if 'just a moment' in title.lower():
            self.logger.warning("SHEIN challenge page variant (status=%s)", response.status)
            return

        seen: set[str] = set()
        for a in response.xpath('//a[contains(@href,"-p-") and contains(@href,".html")]'):
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)

            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            text = " ".join(card.xpath('.//text()').getall()) if card else ""
            text = re.sub(r"\s+", " ", text).strip()
            m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
            price = float(m.group(1)) if m else None
            img = (card.xpath('.//img/@src').get() if card else None) or (card.xpath('.//img/@data-src').get() if card else None)
            pid = None
            mp = re.search(r"-p-(\d+)\.html", url)
            if mp:
                pid = mp.group(1)

            yield {
                "item_id": pid,
                "title": text or None,
                "url": url,
                "price": price,
                "currency": "USD" if price is not None else None,
                "brand": "SHEIN",
                "rating": None,
                "reviews_count": None,
                "image_url": img,
                "source": "shein_html",
                "mode": "category_html",
                "category_url": self.resolve_target_url(),
                "page": page,
            }
