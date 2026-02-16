from __future__ import annotations

"""Best Buy keyword search spider (Playwright-assisted Apollo extraction).

Usage:
  scrapy crawl bestbuy_search -a q=laptop -a max_pages=2
"""

from urllib.parse import urlencode

import scrapy
from playwright.async_api import async_playwright

from common.spiders.base_search_spider import BaseSearchSpider
from common.spiders.bestbuy_bootstrap_utils import extract_bestbuy_items_from_apollo_cache, extract_bestbuy_items_from_bootstrap


class BestbuySearchSpider(BaseSearchSpider):
    name = "bestbuy_search"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages)

    def start_requests(self):
        first = self._build_search_url(self.args.q or "")
        yield scrapy.Request(first, callback=self.parse_search_page, meta=self.maybe_proxy_meta({"page": 1}))

    async def parse_search_page(self, response: scrapy.http.Response):
        page_num = int(response.meta.get("page", 1))
        html = response.text or ""

        emitted = 0

        # Fast path: inline bootstrap parsing from fetched HTML.
        for item in extract_bestbuy_items_from_bootstrap(html):
            emitted += 1
            item.update({"mode": "keyword", "query": self.args.q, "page": page_num, "source_url": response.url})
            yield item

        # Fallback: render with Playwright and pull Apollo cache.
        if emitted == 0:
            cache_obj, rendered_html = await self._fetch_playwright_state(response.url)
            for item in extract_bestbuy_items_from_apollo_cache(cache_obj):
                emitted += 1
                item.update({"mode": "keyword", "query": self.args.q, "page": page_num, "source_url": response.url})
                yield item

            if emitted == 0 and rendered_html:
                for item in extract_bestbuy_items_from_bootstrap(rendered_html):
                    emitted += 1
                    item.update({"mode": "keyword", "query": self.args.q, "page": page_num, "source_url": response.url})
                    yield item

        if emitted == 0:
            self.logger.warning("BestBuy search produced 0 items page=%s status=%s", page_num, response.status)

        if page_num < self.args.max_pages:
            next_page = page_num + 1
            next_url = self._build_search_url(self.args.q or "", page=next_page)
            yield scrapy.Request(next_url, callback=self.parse_search_page, meta=self.maybe_proxy_meta({"page": next_page}))

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

    @staticmethod
    def _build_search_url(q: str, page: int = 1) -> str:
        params = {"st": q, "intl": "nosplash"}
        if page > 1:
            params["cp"] = str(page)
        return f"https://www.bestbuy.com/site/searchpage.jsp?{urlencode(params)}"
