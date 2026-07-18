from __future__ import annotations

import re
from typing import Iterable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy
from parsel import Selector
from playwright.async_api import async_playwright

from common.spiders.base_listing_spider import BaseListingSpider


class NordstromrackListingSpider(BaseListingSpider):
    """Nordstrom Rack listing spider (Playwright-rendered HTML extraction).

    Example:
      scrapy crawl nordstromrack_listing -a category=dresses -a max_pages=1 -O nordstromrack_listing.jsonl
    """

    name = "nordstromrack_listing"
    allowed_domains = ["nordstromrack.com", "www.nordstromrack.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    categories = [
        {"category": "dresses", "url": "https://www.nordstromrack.com/shop/women/clothing/dresses"},
        {"category": "women", "url": "https://www.nordstromrack.com/shop/women"},
        {"category": "men", "url": "https://www.nordstromrack.com/shop/men"},
        {"category": "shoes", "url": "https://www.nordstromrack.com/shop/shoes"},
    ]

    require_category_arg = False

    def start_requests(self) -> Iterable[scrapy.Request]:
        target = self.resolve_target_url() if (self.url or self.category_url or self.category) else self.categories[0]["url"]
        target = self._with_page(target, 1)
        yield scrapy.Request(target, callback=self.parse_listing_page, meta={"page": 1})

    async def parse_listing_page(self, response: scrapy.http.Response):
        page_num = int(response.meta.get("page", 1))
        target_url = response.url

        rendered_html = await self._render_with_playwright(target_url)
        if not rendered_html:
            self.logger.warning("Nordstrom Rack Playwright render failed page=%s url=%s", page_num, target_url)
            return

        emitted = 0
        sel = Selector(text=rendered_html)
        seen: set[str] = set()

        for a in sel.css('a[href*="/s/"]'):
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            if href.startswith("/"):
                url = f"https://www.nordstromrack.com{href}"
            else:
                url = href
            url = url.split("#", 1)[0]
            if "/s/" not in url:
                continue

            # Deduplicate review anchors and color variants to one canonical listing URL.
            url = re.sub(r"([?&])color=[^&]+", "", url).rstrip("?&")
            if url in seen:
                continue
            seen.add(url)

            product_id_match = re.search(r"/s/[^/]+/(\d+)", url)
            product_id = product_id_match.group(1) if product_id_match else None

            name = (
                a.attrib.get("title")
                or a.attrib.get("aria-label")
                or a.css("::text").get(default="").strip()
                or None
            )
            if name and name.endswith(", Image"):
                name = name[:-7]

            image = None
            parent = a.xpath("ancestor::*[self::article or self::div][1]")
            if parent:
                image = parent.css("img::attr(src)").get()

            yield {
                "category": self.category or "custom",
                "product_id": product_id,
                "name": name,
                "url": url,
                "image": image,
                "source_url": target_url,
                "page": page_num,
                "mode": "listing",
            }
            emitted += 1

        if emitted == 0:
            self.logger.warning("Nordstrom Rack listing produced 0 items page=%s url=%s", page_num, target_url)

        if page_num < self.args.max_pages:
            next_page = page_num + 1
            next_url = self._with_page(self.resolve_target_url() if (self.url or self.category_url or self.category) else self.categories[0]["url"], next_page)
            yield scrapy.Request(next_url, callback=self.parse_listing_page, meta={"page": next_page})

    async def _render_with_playwright(self, url: str) -> str:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(locale="en-US", user_agent="Mozilla/5.0")
                page = await context.new_page()
                await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                await page.wait_for_timeout(4000)
                html = await page.content()
                await context.close()
                await browser.close()
                return html
        except Exception as exc:
            self.logger.warning("Playwright render failed for Nordstrom Rack: %s", exc)
            return ""

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
