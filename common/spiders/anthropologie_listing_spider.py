from __future__ import annotations

import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class AnthropologieListingSpider(BaseListingSpider):
    name = "anthropologie_listing"
    allowed_domains = ["anthropologie.com", "www.anthropologie.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "women", "url": "https://www.anthropologie.com/womens-clothing"},
        {"category": "dresses", "url": "https://www.anthropologie.com/dresses"},
        {"category": "sale", "url": "https://www.anthropologie.com/sale-all"},
    ]

    def start_requests(self):
        yield scrapy.Request(self.resolve_target_url(), callback=self.parse_html, meta={"page": 1})

    def parse_html(self, response: scrapy.http.Response):
        text = response.text or ""
        lowered = text.lower()

        # Anthropologie pages commonly include recaptcha config JS even when the page is valid,
        # so a raw "captcha" keyword check causes false positives and drops real product pages.
        blocked_markers = (
            "access denied",
            "verify you are human",
            "request blocked",
            "temporarily unavailable",
            "bot detection",
            "challenge-platform",
        )
        looks_blocked = response.status >= 400 or any(marker in lowered for marker in blocked_markers)

        if looks_blocked and "/shop/" not in lowered:
            self.logger.warning("Anthropologie blocked/denied (status=%s)", response.status)
            return

        page = int(response.meta.get("page", 1))
        seen: set[str] = set()

        for a in response.xpath('//a[contains(@href, "/shop/")]'):
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            url = response.urljoin(href)
            if "/shop/" not in url or url in seen:
                continue
            seen.add(url)

            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            title = a.xpath('.//h2/text()').get() or a.xpath('.//text()').get()
            title = re.sub(r"\s+", " ", (title or "")).strip() or None

            context = " ".join((card.xpath('.//text()').getall() if card else a.xpath('.//text()').getall()))
            context = re.sub(r"\s+", " ", context)
            m = re.search(r"\$\s?(\d+(?:\.\d{1,2})?)", context)
            price = float(m.group(1)) if m else None

            image_url = (
                (card.xpath('.//img/@src').get() if card else None)
                or (card.xpath('.//img/@data-src').get() if card else None)
                or a.xpath('.//img/@src').get()
            )

            item_id = None
            mm = re.search(r"/shop/([^?/#]+)", url)
            if mm:
                item_id = mm.group(1)

            yield {
                "item_id": item_id,
                "title": title,
                "url": url,
                "price": price,
                "currency": "USD" if price is not None else None,
                "brand": "Anthropologie",
                "rating": None,
                "reviews_count": None,
                "image_url": image_url,
                "source": "anthropologie_html",
                "mode": "category_html",
                "category_url": self.resolve_target_url(),
                "page": page,
            }
