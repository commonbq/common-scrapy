"""O'Reilly listings from the server-rendered ``window._ost`` bootstrap."""

from __future__ import annotations

import re
from html import unescape
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.oreilly_categories import OREILLY_CATEGORIES


class OreillyListingSpider(BaseListingSpider):
    name = "oreilly_listing"
    allowed_domains = ["oreillyauto.com", "www.oreillyauto.com"]
    categories = OREILLY_CATEGORIES
    require_category_arg = False
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category", "category_path", "item_id", "title", "url", "image",
            "price", "original_price", "sale_price", "currency", "availability",
            "brand", "line_code", "page", "position", "total_results",
            "total_pages", "timestamp", "source", "raw",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError("Provide -a category=<name>, category_url=<url>, or url=<url>")
        self._seen = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        selected = next((x for x in self.categories if x["url"] == target), {})
        yield self._request(target, 1, selected.get("category_path"))

    def _request(self, url, page, category_path):
        return scrapy.Request(self._page_url(url, page), headers=self.headers, callback=self.parse,
            meta={"proxy": self._residential_proxy(), "page": page,
                  "category_path": category_path}, dont_filter=True)

    def _residential_proxy(self):
        proxy = self.settings.get("PROXY")
        if not proxy or "scrapeops" not in proxy.lower() or "residential=true" in proxy:
            return proxy
        parts = urlsplit(proxy)
        if not parts.password or not parts.hostname:
            return proxy
        username = f"{parts.username}.country=us.residential=true"
        return urlunsplit((parts.scheme, f"{username}:{parts.password}@{parts.hostname}:{parts.port}",
                           parts.path, parts.query, parts.fragment))

    @staticmethod
    def _page_url(url, page):
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query) if k.lower() not in {"page", "pagenumber"}]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _scalar(text, name):
        match = re.search(rf"window\._ost\.{name}\s*=\s*['\"]?([0-9]+)", text)
        return int(match.group(1)) if match else None

    @classmethod
    def products(cls, text):
        starts = list(re.finditer(r"var\s+broadleafProductId\s*=\s*['\"]?([0-9]+)", text))
        hrefs = {m.group(1): urljoin("https://www.oreillyauto.com", unescape(m.group(2)))
                 for m in re.finditer(r'data-id=["\']([0-9]+)["\'][^>]*href=["\']([^"\']+)', text)}
        products = []
        for index, start in enumerate(starts):
            block = text[start.start(): starts[index + 1].start() if index + 1 < len(starts) else len(text)]
            pid = start.group(1)
            def value(pattern):
                match = re.search(pattern, block, re.S)
                return unescape(match.group(1)).strip() if match else None
            item_id = value(r"var\s+itemId\s*=\s*['\"](.*?)['\"]")
            title = value(r"item_name\s*:\s*['\"](.*?)['\"]") or value(rf"window\[`_{pid}_name`\]\s*=\s*['\"](.*?)['\"]")
            price = value(r"['\"]?price['\"]?\s*:\s*([0-9.]+)")
            retail = value(r"['\"]?retailPrice['\"]?\s*:\s*([0-9.]+)")
            sale = value(r"['\"]?salePrice['\"]?\s*:\s*([0-9.]+)")
            currency = value(r"['\"]?currencyCode['\"]?\s*:\s*['\"](.*?)['\"]")
            image = value(rf"window\[(?:`_|['\"]_){pid}_primaryImage(?:`|['\"])\]\s*=\s*['\"](.*?)['\"]")
            if item_id and title:
                line, _, part = item_id.partition("|")
                products.append({"item_id": item_id, "title": title, "url": hrefs.get(pid),
                    "image": image, "price": float(price) if price else None,
                    "original_price": float(retail) if retail else None,
                    "sale_price": float(sale) if sale else None, "currency": currency,
                    "availability": value(r"['\"]?availability['\"]?\s*:\s*['\"](.*?)['\"]") or "available",
                    "brand": value(r"['\"]?item_brand['\"]?\s*:\s*['\"](.*?)['\"]"),
                    "line_code": line or None, "raw": {"broadleaf_product_id": pid, "part_number": part}})
        return products

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"O'Reilly listing returned HTTP {response.status}: {response.url}")
        total_results = self._scalar(response.text, "totalResults")
        total_pages = self._scalar(response.text, "totalPages")
        products = self.products(response.text)
        if total_results is None or total_pages is None or not products:
            raise RuntimeError(f"O'Reilly bootstrap missing totals/products at {response.url}; possible challenge")
        page = int(response.meta["page"])
        for position, item in enumerate(products, 1):
            if item["item_id"] in self._seen:
                continue
            self._seen.add(item["item_id"])
            yield {"category": self.category or "custom", "category_path": response.meta.get("category_path"),
                   **item, "page": page, "position": position, "total_results": total_results,
                   "total_pages": total_pages, "timestamp": self.get_timestamp(),
                   "source": "oreilly_ost_bootstrap"}
        if page < min(total_pages, self.max_pages):
            yield self._request(response.url, page + 1, response.meta.get("category_path"))
