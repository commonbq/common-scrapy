from __future__ import annotations

"""Home Depot category listing spider.

Primary strategy:
- Parse listing products from Home Depot Apollo bootstrap embedded in HTML
  (`window.__APOLLO_STATE__`).

Fallback strategy:
- Direct HTML extraction (JSON-LD + product links) when Apollo bootstrap is
  unavailable or blocked.

Usage examples:
  scrapy crawl homedepot_listing -a category='screwdrivers' -a max_pages=1
  scrapy crawl homedepot_listing -a category_url='https://www.homedepot.com/b/Tools-Hand-Tools/Screwdrivers-Nut-Drivers/Screwdrivers/N-5yc1vZc25y' -a max_pages=1
"""

import json
import re
from html import unescape

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.homedepot_search_spider import HomeDepotSearchSpider


class HomeDepotListingSpider(BaseListingSpider):
    name = "homedepot_listing"
    allowed_domains = ["homedepot.com", "www.homedepot.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
    }

    categories = [
        {"category": "screwdrivers", "url": "https://www.homedepot.com/b/Tools-Hand-Tools/Screwdrivers-Nut-Drivers/Screwdrivers/N-5yc1vZc25y"},
        {"category": "drills", "url": "https://www.homedepot.com/b/Tools-Power-Tools-Drills/N-5yc1vZc27r"},
        {"category": "paint", "url": "https://www.homedepot.com/b/Paint/N-5yc1vZar2d"},
        {"category": "light-bulbs", "url": "https://www.homedepot.com/b/Lighting-Light-Bulbs/N-5yc1vZbmwz"},
        {"category": "lumber", "url": "https://www.homedepot.com/b/Lumber-Composites-Dimensional-Lumber/N-5yc1vZc3tc"},
    ]

    def start_requests(self):
        target = self._resolve_target_url()
        yield scrapy.Request(target, callback=self.parse, meta=self.proxy_meta({"original_url": target}))

    def parse(self, response: scrapy.http.Response):
        html = response.text or ""

        if not HomeDepotSearchSpider._is_error_page(html):
            state = HomeDepotSearchSpider._extract_js_object(html, "__APOLLO_STATE__")
            if state:
                tmp = HomeDepotSearchSpider(q="x")
                yielded = 0
                for item in tmp._yield_products_from_apollo(
                    state,
                    mode="category",
                    query=None,
                    category_url=self.category_url or self.url,
                    page=1,
                ):
                    yielded += 1
                    yield item

                if yielded > 0:
                    return

        fallback_items = list(self._extract_from_json_ld(html))
        if not fallback_items:
            fallback_items = list(self._extract_from_product_links(html))

        if not fallback_items:
            self.logger.warning("HomeDepot listing fallback found 0 items (status=%s)", response.status)
            return

        for item in fallback_items:
            item.update(
                {
                    "source": item.get("source") or "homedepot_direct_html_fallback",
                    "mode": "category",
                    "query": None,
                    "category_url": self.category_url or self.url,
                    "page": 1,
                }
            )
            yield item

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

    def _extract_from_json_ld(self, html: str):
        scripts = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html or "",
            flags=re.I | re.S,
        )

        for s in scripts:
            s = (s or "").strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except Exception:
                continue

            nodes = []
            if isinstance(obj, dict):
                if isinstance(obj.get("@graph"), list):
                    nodes.extend(x for x in obj["@graph"] if isinstance(x, dict))
                else:
                    nodes.append(obj)
            elif isinstance(obj, list):
                nodes.extend(x for x in obj if isinstance(x, dict))

            for node in nodes:
                if node.get("@type") not in ("Product", "ListItem"):
                    continue

                if node.get("@type") == "ListItem" and isinstance(node.get("item"), dict):
                    node = node["item"]

                if node.get("@type") != "Product":
                    continue

                offers = node.get("offers") or {}
                if isinstance(offers, list):
                    offers = offers[0] if offers else {}

                url = node.get("url")
                if isinstance(url, str) and url.startswith("/"):
                    url = f"https://www.homedepot.com{url}"

                yield {
                    "item_id": self._extract_item_id(url),
                    "sku": None,
                    "brand": (node.get("brand") or {}).get("name") if isinstance(node.get("brand"), dict) else node.get("brand"),
                    "title": node.get("name"),
                    "model": None,
                    "url": url,
                    "image_url": node.get("image", [None])[0] if isinstance(node.get("image"), list) else node.get("image"),
                    "price": self._to_float((offers or {}).get("price")),
                    "original_price": None,
                    "rating": self._to_float((node.get("aggregateRating") or {}).get("ratingValue")) if isinstance(node.get("aggregateRating"), dict) else None,
                    "reviews_count": self._to_int((node.get("aggregateRating") or {}).get("reviewCount")) if isinstance(node.get("aggregateRating"), dict) else None,
                    "source": "homedepot_jsonld_fallback",
                }

    def _extract_from_product_links(self, html: str):
        pat = re.compile(
            r'<a[^>]+href=["\'](?P<href>(?:https://www\.homedepot\.com)?/p/[^"\']+)["\'][^>]*>(?P<title>.*?)</a>',
            flags=re.I | re.S,
        )

        seen: set[str] = set()
        for m in pat.finditer(html or ""):
            href = m.group("href")
            if href.startswith("/"):
                href = f"https://www.homedepot.com{href}"
            href = href.split("?")[0]
            if href in seen:
                continue
            seen.add(href)

            title_raw = re.sub(r"<[^>]+>", " ", m.group("title") or "")
            title = unescape(re.sub(r"\s+", " ", title_raw).strip()) or None

            yield {
                "item_id": self._extract_item_id(href),
                "sku": None,
                "brand": None,
                "title": title,
                "model": None,
                "url": href,
                "image_url": None,
                "price": None,
                "original_price": None,
                "rating": None,
                "reviews_count": None,
                "source": "homedepot_html_links_fallback",
            }

    @staticmethod
    def _extract_item_id(url: str | None) -> str | None:
        if not url:
            return None
        m = re.search(r"/p/[^/]+/(\d+)", url)
        return m.group(1) if m else None

    @staticmethod
    def _to_float(v):
        try:
            return float(v)
        except Exception:
            return None

    @staticmethod
    def _to_int(v):
        try:
            return int(v)
        except Exception:
            return None
