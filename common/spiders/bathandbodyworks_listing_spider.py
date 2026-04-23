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


class BathandbodyworksListingSpider(BaseListingSpider):
    name = "bathandbodyworks_listing"
    allowed_domains = ["bathandbodyworks.com", "www.bathandbodyworks.com"]

    # 改进：更保守的速率限制以绕过PerimeterX
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 2,  # 增加延迟
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,  # 降低并发
        "COOKIES_ENABLED": True,  # 启用cookies
    }

    categories = [
        {
            "category": "body-care",
            "url": "https://www.bathandbodyworks.com/c/body-care",
            "api_cgid": "body-care",
        },
        {
            "category": "home-fragrance",
            "url": "https://www.bathandbodyworks.com/c/home-fragrance",
            "api_cgid": "home-fragrance",
        },
        {
            "category": "hand-soaps",
            "url": "https://www.bathandbodyworks.com/c/hand-soaps",
            "api_cgid": "hand-soaps",
        },
    ]

    def start_requests(self):
        """改进：添加类似Target的浏览器headers"""
        target = self.resolve_target_url()

        # 添加更完整的浏览器headers
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

        # 改进：先尝试HTML模式（更稳定）
        yield scrapy.Request(
            target,
            headers=headers,
            callback=self.parse_bootstrap,
            meta={"page": 1, "origin": target, "handle_httpstatus_all": True},
            dont_filter=True,
        )

    def _build_api_url(self, page: int) -> str | None:
        cgid = None
        if self.category:
            for c in self.categories:
                if c.get("category") == self.category:
                    cgid = c.get("api_cgid")
                    break
        if not cgid:
            u = urlparse(self.resolve_target_url())
            parts = [p for p in (u.path or "").split("/") if p]
            if parts:
                cgid = parts[-1]
        if not cgid:
            return None

        start = max(page - 1, 0) * 48
        return (
            "https://www.bathandbodyworks.com/mobify/proxy/api/search/shopper-search/v1/"
            "organizations/f_ecom_bbdl_prd/product-search?"
            + urlencode(
                {
                    "siteId": "BathAndBodyWorks",
                    "q": "*",
                    "refine": f"cgid={cgid}",
                    "start": start,
                    "count": 48,
                }
            )
        )

    def parse_api(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        yielded = 0

        try:
            payload = json.loads(response.text)
        except Exception:
            payload = None

        if isinstance(payload, dict):
            for item in extract_items_from_unknown_state(payload, source="bathandbodyworks_internal_api"):
                yielded += 1
                item.update({"mode": "category", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            for item in self._extract_html_cards(response):
                yielded += 1
                item.update({"source": "bathandbodyworks_internal_api_html", "mode": "category", "category_url": response.meta.get("origin"), "page": page})
                yield item

        if yielded == 0:
            origin = response.meta.get("origin") or self.resolve_target_url()
            yield scrapy.Request(
                origin,
                callback=self.parse_bootstrap,
                meta={"page": page, "origin": origin},
                dont_filter=True,
            )
            return

        if page < self.max_pages:
            next_page = page + 1
            api_url = self._build_api_url(next_page)
            if api_url:
                headers = {
                    "accept": "application/json",
                    "referer": response.meta.get("origin"),
                    "user-agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0.0.0 Safari/537.36"
                    ),
                }
                yield scrapy.Request(
                    api_url,
                    callback=self.parse_api,
                    meta={"page": next_page, "origin": response.meta.get("origin")},
                    headers=headers,
                )

    def parse_bootstrap(self, response: scrapy.http.Response):
        """改进：增强的bootstrap解析，优先级明确"""
        page = int(response.meta.get("page", 1))
        html = response.text or ""
        yielded = 0

        # 记录响应状态以帮助调试
        self.logger.info(f"Bath & Body Works bootstrap parse: status={response.status}, url={response.url}")

        # 新增：检查是否有PerimeterX拦截
        if "px-captcha" in html.lower() or "perimeterx" in html.lower():
            self.logger.warning("PerimeterX detected on page. Consider using proxy or different approach.")
            # 尝试解析captcha或返回错误item
            yield {
                "error": "PerimeterX captcha detected",
                "url": response.url,
                "status": response.status,
            }
            return

        # 改进：调整提取优先级，优先尝试JSON-LD（更稳定）
        # 1. 首先尝试JSON-LD（结构化数据，通常最容易）
        for item in extract_json_ld_products(html):
            yielded += 1
            item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
            yield item

        # 2. 然后尝试Next.js数据
        if yielded == 0:
            nd = extract_next_data(html)
            if nd:
                for item in extract_items_from_unknown_state(nd, source="bathandbodyworks_next_data"):
                    yielded += 1
                    item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
                    yield item

        # 3. 尝试Apollo状态
        if yielded == 0:
            ap = extract_apollo_state(html)
            if ap:
                for item in extract_items_from_unknown_state(ap, source="bathandbodyworks_apollo_state"):
                    yielded += 1
                    item.update({"mode": "category_bootstrap", "category_url": response.meta.get("origin"), "page": page})
                    yield item

        # 4. 最后尝试HTML解析（改进版）
        if yielded == 0:
            for item in self._extract_html_cards_improved(response):
                yielded += 1
                item.update({"source": "bathandbodyworks_html_fallback", "mode": "category_html", "category_url": response.meta.get("origin"), "page": page})
                yield item

        # 改进：记录结果
        self.logger.info(f"Bath & Body Works bootstrap yielded {yielded} items")

        if yielded == 0:
            # 保存HTML以便调试
            self.logger.warning(f"No items extracted. HTML preview: {html[:500]}")

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        count = 0
        for item in self._extract_html_cards_improved(response):
            count += 1
            item.update({"source": "bathandbodyworks_html", "mode": "category_html", "category_url": response.meta.get("origin"), "page": page})
            yield item
        if count == 0:
            self.logger.warning("Bath & Body Works html mode returned 0 items (status=%s)", response.status)

    def _extract_html_cards_improved(self, response: scrapy.http.Response):
        """改进：更强大的HTML卡片提取"""
        seen: set[str] = set()
        ctype = (response.headers.get(b"content-type") or b"").decode("utf-8", errors="ignore").lower()

        # 处理JSON响应中的URL
        if "json" in ctype and "html" not in ctype:
            for m in re.finditer(
                r'"(?:url|link|productUrl)"\s*:\s*"(?P<u>https?://www\.bathandbodyworks\.com[^"]+)"',
                response.text or "",
            ):
                url = m.group("u")
                if url in seen:
                    continue
                seen.add(url)
                yield {
                    "item_id": self._extract_id(url),
                    "title": None,
                    "url": url,
                    "price": None,
                    "currency": None,
                    "brand": "Bath & Body Works",
                    "rating": None,
                    "reviews_count": None,
                    "image_url": None,
                    "raw": None,
                }
            return

        # 改进：更多XPath选择器，适应不同的页面结构
        selectors = [
            '//a[contains(@href,"/p/") or contains(@href,"/product") or contains(@href,"/pd/")]',
            '//div[contains(@class,"product")]//a',
            '//article//a[contains(@href,"bathandbodyworks.com")]',
            '//li[contains(@class,"product")]//a',
        ]

        for selector in selectors:
            for a in response.xpath(selector):
                href = (a.attrib.get("href") or "").strip()
                if not href:
                    continue
                url = response.urljoin(href)
                # 过滤非产品链接
                if not any(x in url for x in ["/p/", "/product", "/pd/"]):
                    continue
                if url in seen:
                    continue
                seen.add(url)

                # 改进：更好的标题和价格提取
                card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
                text = ""
                img = None
                price = None

                if card:
                    text = re.sub(r"\s+", " ", " ".join(card.xpath('.//text()').getall())).strip()
                    img = card.xpath('.//img/@src').get() or card.xpath('.//img/@data-src').get()
                    price = self._extract_price(text)
                else:
                    text = a.attrib.get("title") or a.attrib.get("aria-label") or ""

                item_id = self._extract_id(url)
                yield {
                    "item_id": item_id,
                    "title": text or None,
                    "url": url,
                    "price": price,
                    "currency": "USD" if price is not None else None,
                    "brand": "Bath & Body Works",
                    "rating": None,
                    "reviews_count": None,
                    "image_url": img,
                    "raw": None,
                }

            # 如果这个选择器找到了产品，就不尝试其他的
            if seen:
                break

    def _extract_html_cards(self, response: scrapy.http.Response):
        """保留原方法兼容性"""
        return self._extract_html_cards_improved(response)

    @staticmethod
    def _extract_price(text: str) -> float | None:
        # 改进：支持更多价格格式
        m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text or "")
        return float(m.group(1)) if m else None

    @staticmethod
    def _extract_id(url: str) -> str | None:
        # 改进：提取更多ID格式
        m = re.search(r"(?:sku=|/p/|/pd/|/product/)([A-Za-z0-9_-]{4,})", url or "")
        return m.group(1) if m else None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
