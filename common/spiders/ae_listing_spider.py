from __future__ import annotations

import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class AeListingSpider(BaseListingSpider):
    """American Eagle listing spider.

    Current reliable path in this environment is HTML card parsing from category pages.
    """

    name = "ae_listing"
    allowed_domains = ["ae.com", "www.ae.com"]

    categories = [
        {"category": "women-tops", "url": "https://www.ae.com/us/en/c/women/tops/cat10049"},
        {"category": "women-jeans", "url": "https://www.ae.com/us/en/c/women/jeans/cat6430042"},
        {"category": "men-tops", "url": "https://www.ae.com/us/en/c/men/shirts/cat150044"},
    ]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    def start_requests(self):
        target = self.resolve_target_url()
        yield scrapy.Request(target, callback=self.parse_html, meta={"page": 1, "origin": target})

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        yielded = 0
        for item in self._extract_html_cards(response):
            yielded += 1
            item.update(
                {
                    "source": "ae_html",
                    "mode": "category_html",
                    "category_url": response.meta.get("origin") or response.url,
                    "page": page,
                }
            )
            yield item

        if yielded == 0:
            self.logger.warning("AE html mode returned 0 items (status=%s url=%s)", response.status, response.url)

    def _extract_html_cards(self, response: scrapy.http.Response):
        seen: set[str] = set()
        for a in response.xpath('//a[contains(@href,"/p/")]'):
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            url = response.urljoin(href)
            if "/us/en/p/" not in url:
                continue
            if url in seen:
                continue
            seen.add(url)

            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            title = a.xpath('.//h3/text()').get() or (card.xpath('.//h3/text()').get() if card else None)
            title = re.sub(r"\s+", " ", (title or "")).strip() or None

            text_blob = re.sub(r"\s+", " ", " ".join(card.xpath('.//text()').getall())).strip() if card else ""
            price_matches = re.findall(r"\$(\d+(?:\.\d{1,2})?)", text_blob)
            price = float(price_matches[0]) if price_matches else None
            original_price = float(price_matches[1]) if len(price_matches) > 1 else None

            img = None
            if card:
                img = card.xpath('.//img/@src').get() or card.xpath('.//img/@data-src').get()
            if img:
                img = response.urljoin(img)

            item_id = url.rstrip("/").split("/")[-1]
            yield {
                "item_id": item_id,
                "title": title,
                "url": url,
                "price": price,
                "original_price": original_price,
                "currency": "USD" if price is not None else None,
                "brand": "American Eagle",
                "rating": None,
                "reviews_count": None,
                "image_url": img,
                "raw": None,
            }
