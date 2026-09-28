from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class ElfcosmeticsListingSpider(BaseListingSpider):
    name = "elfcosmetics_listing"
    allowed_domains = ["elfcosmetics.com", "www.elfcosmetics.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "url",
            "price",
            "currency",
            "brand",
            "rating",
            "reviews_count",
            "image_url",
            "category",
            "category_url",
            "page",
            "source",
            "source_url",
            "raw",
        ],
    }

    categories = [
        {"category": "makeup", "url": "https://www.elfcosmetics.com/collections/all-makeup"},
        {"category": "face", "url": "https://www.elfcosmetics.com/collections/face"},
        {"category": "eyes", "url": "https://www.elfcosmetics.com/collections/eyes"},
        {"category": "lips", "url": "https://www.elfcosmetics.com/collections/lips"},
        {"category": "skin-care", "url": "https://www.elfcosmetics.com/collections/skin-care"},
        {"category": "hair", "url": "https://www.elfcosmetics.com/collections/hair"},
        {"category": "brushes", "url": "https://www.elfcosmetics.com/collections/brushes"},
        {"category": "best-sellers", "url": "https://www.elfcosmetics.com/collections/best-sellers"},
        {"category": "whats-new", "url": "https://www.elfcosmetics.com/collections/whats-new"},
    ]

    def start_requests(self):
        target = self.resolve_target_url()
        first = self._with_page(target, 1)
        yield scrapy.Request(first, callback=self.parse, meta={"page": 1, "origin": target})

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        count = 0
        for item in self._extract_html_cards(response):
            count += 1
            item.update(self._context(response, page))
            yield item
        if count == 0:
            self.logger.warning("e.l.f. parser returned 0 items (status=%s)", response.status)
        yield from self._next_page_requests(response, page)

    def _context(self, response: scrapy.http.Response, page: int) -> dict:
        return {
            "source": "elfcosmetics_html",
            "mode": "category_html",
            "category": self.category,
            "category_url": response.meta.get("origin"),
            "page": page,
            "source_url": response.url,
        }

    def _next_page_requests(self, response, page):
        if page >= self.max_pages:
            return
        href = response.xpath('//a[@rel="next"]/@href').get()
        if not href:
            href = response.xpath(f'//a[contains(@href,"page={page + 1}")]/@href').get()
        if href:
            yield response.follow(
                href,
                callback=self.parse,
                meta={"page": page + 1, "origin": response.meta.get("origin")},
            )

    def _extract_html_cards(self, response: scrapy.http.Response):
        seen: set[str] = set()
        # Hydrogen product cards expose their name through this accessible label.
        # Requiring it avoids treating promotional banner links as catalog items.
        links = response.xpath(
            '//a[starts-with(@aria-label,"View details for ") '
            'and (contains(@href,"/products/") or contains(@href,"/p/"))]'
        )
        for a in links:
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)
            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            text = re.sub(r"\s+", " ", " ".join(card.xpath('.//text()').getall())).strip() if card else ""
            title = (a.attrib.get("aria-label") or "").removeprefix("View details for ").strip()
            img = (card.xpath('.//img/@src').get() if card else None) or (card.xpath('.//img/@data-src').get() if card else None)
            m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
            price = float(m.group(1)) if m else None
            yield {
                "item_id": self._extract_id(url),
                "title": title or text or None,
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
