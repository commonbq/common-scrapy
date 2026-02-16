from __future__ import annotations

"""Best Buy category/listing spider (Playwright-assisted Apollo extraction).

Usage examples:
  scrapy crawl bestbuy_listing -a category='laptops' -a max_pages=1
  scrapy crawl bestbuy_listing -a category_url='https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000' -a max_pages=1
"""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy
from playwright.async_api import async_playwright

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.bestbuy_bootstrap_utils import extract_bestbuy_items_from_apollo_cache, extract_bestbuy_items_from_bootstrap


class BestbuyListingSpider(BaseListingSpider):
    name = "bestbuy_listing"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    categories = [
        {"category": "laptops", "url": "https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000"},
        {"category": "tvs", "url": "https://www.bestbuy.com/site/tv-home-theater/televisions/abcat0101001.c?id=abcat0101001"},
        {"category": "headphones", "url": "https://www.bestbuy.com/site/headphones/all-headphones/abcat0204000.c?id=abcat0204000"},
        {"category": "monitors", "url": "https://www.bestbuy.com/site/computer-cards-components/monitors/abcat0509000.c?id=abcat0509000"},
        {"category": "cell-phones", "url": "https://www.bestbuy.com/site/cell-phones/all-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005"},
    ]

    def start_requests(self):
        target = self._resolve_target_url()
        target = self._ensure_nosplash(self._with_page(target, 1))
        yield scrapy.Request(target, callback=self.parse_listing_page, meta=self.maybe_proxy_meta({"page": 1}))

    async def parse_listing_page(self, response: scrapy.http.Response):
        page_num = int(response.meta.get("page", 1))
        html = response.text or ""

        emitted = 0

        for item in extract_bestbuy_items_from_bootstrap(html):
            emitted += 1
            item.update(
                {
                    "mode": "category",
                    "category_url": self.category_url or self.url,
                    "page": page_num,
                    "source_url": response.url,
                }
            )
            yield item

        if emitted == 0:
            cache_obj, rendered_html = await self._fetch_playwright_state(response.url)
            for item in extract_bestbuy_items_from_apollo_cache(cache_obj):
                emitted += 1
                item.update(
                    {
                        "mode": "category",
                        "category_url": self.category_url or self.url,
                        "page": page_num,
                        "source_url": response.url,
                    }
                )
                yield item

            if emitted == 0 and rendered_html:
                for item in extract_bestbuy_items_from_bootstrap(rendered_html):
                    emitted += 1
                    item.update(
                        {
                            "mode": "category",
                            "category_url": self.category_url or self.url,
                            "page": page_num,
                            "source_url": response.url,
                        }
                    )
                    yield item

        if emitted == 0:
            self.logger.warning("BestBuy listing produced 0 items page=%s status=%s", page_num, response.status)

        if page_num < self.args.max_pages:
            next_page = page_num + 1
            next_url = self._ensure_nosplash(self._with_page(self._resolve_target_url(), next_page))
            yield scrapy.Request(next_url, callback=self.parse_listing_page, meta=self.maybe_proxy_meta({"page": next_page}))

    async def _fetch_playwright_state(self, url: str) -> tuple[dict, str]:
        cache_obj: dict = {}
        html = ""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(locale="en-US", user_agent="Mozilla/5.0")
                page = await context.new_page()
                await page.goto(url, wait_until="domcontentloaded", timeout=90000)
                await page.wait_for_timeout(3000)
                cache_obj = await page.evaluate(
                    """() => {
                      const s = Object.getOwnPropertySymbols(window).find(x => String(x).includes('ApolloClientSingleton'));
                      if (!s || !window[s] || !window[s].cache || !window[s].cache.extract) return {};
                      try { return window[s].cache.extract() || {}; } catch (e) { return {}; }
                    }"""
                )
                html = await page.content()
                await context.close()
                await browser.close()
        except Exception as exc:
            self.logger.warning("Playwright fallback failed: %s", exc)
        return cache_obj if isinstance(cache_obj, dict) else {}, html

    def _resolve_target_url(self) -> str:
        if self.url:
            return self.url
        if self.category_url:
            return self.category_url
        for entry in self.categories:
            if entry.get("category") == self.category:
                self.category_url = entry.get("url")
                return self.category_url
        names = ", ".join(sorted([c["category"] for c in self.categories]))
        raise ValueError(f"Unknown category '{self.category}'. Use one of: {names}")

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["cp"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    @staticmethod
    def _ensure_nosplash(url: str) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["intl"] = ["nosplash"]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
