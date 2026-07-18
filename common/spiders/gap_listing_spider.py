from __future__ import annotations

import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class GapListingSpider(BaseListingSpider):
    name = "gap_listing"
    allowed_domains = ["gap.com", "www.gap.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "women", "url": "https://www.gap.com/browse/category.do?cid=13658"},
        {"category": "men", "url": "https://www.gap.com/browse/category.do?cid=6998"},
        {"category": "girls", "url": "https://www.gap.com/browse/category.do?cid=14257"},
    ]

    def start_requests(self):
        yield scrapy.Request(self.resolve_target_url(), callback=self.parse_html, meta={"page": 1})

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        if "access denied" in (response.text or "").lower():
            self.logger.warning("Gap access denied variant (status=%s)", response.status)
            return

        seen: set[str] = set()
        for a in response.xpath('//a[contains(@href,"/browse/product.do")]'):
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
            mp = re.search(r"[?&]pid=([^&]+)", url)
            if mp:
                pid = mp.group(1)

            yield {
                "item_id": pid,
                "title": text or None,
                "url": url,
                "price": price,
                "currency": "USD" if price is not None else None,
                "brand": "Gap",
                "rating": None,
                "reviews_count": None,
                "image_url": img,
                "source": "gap_html",
                "mode": "category_html",
                "category_url": self.resolve_target_url(),
                "page": page,
            }
