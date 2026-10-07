from __future__ import annotations

"""Nordstrom Rack listings from the server-rendered ItemList JSON-LD."""

import json
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


NORDSTROMRACK_CATEGORIES = {
    "women": "https://www.nordstromrack.com/c/women",
    "men": "https://www.nordstromrack.com/c/men",
    "kids": "https://www.nordstromrack.com/c/kids",
    "shoes": "https://www.nordstromrack.com/c/shoes",
    "bags-and-accessories": "https://www.nordstromrack.com/c/bags-and-accessories",
    "beauty": "https://www.nordstromrack.com/c/beauty",
    "home": "https://www.nordstromrack.com/c/home",
    "clearance": "https://www.nordstromrack.com/c/clearance",
}


class NordstromrackListingSpider(BaseListingSpider):
    name = "nordstromrack_listing"
    allowed_domains = ["nordstromrack.com", "www.nordstromrack.com", "127.0.0.1"]
    require_category_arg = False
    categories = NORDSTROMRACK_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "brand", "price", "price_max", "currency",
            "availability", "url", "image_url", "category", "page", "position",
            "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.category:
            raise ValueError(f"Provide -a category=<name>. Available categories: {', '.join(self.available_categories())}")
        if not (self.url or self.category_url) and self.category not in self.categories:
            raise ValueError(f"Unknown category '{self.category}'. Available categories: {', '.join(self.available_categories())}")
        self._seen: set[str] = set()

    def available_categories(self):
        return sorted(self.categories)

    def start_requests(self):
        url = self.url or self.category_url or self.categories[self.category]
        yield scrapy.Request(self._page_url(url, 1), callback=self.parse, headers=self._headers(),
                             meta={"category": self.category, "page": 1, "listing_url": url})

    def parse(self, response):
        page = int(response.meta.get("page", 1))
        products = self._products(response)
        if response.status != 200 or not products:
            self.logger.error("Nordstrom Rack ItemList missing: status=%s url=%s", response.status, response.url)
            return
        for position, product in products:
            offers = product.get("offers") or {}
            brand = product.get("brand") or {}
            item_id = str(product.get("sku") or product.get("productID") or product.get("url") or "")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            image = product.get("image")
            yield {
                "item_id": item_id, "title": product.get("name"),
                "brand": brand.get("name") if isinstance(brand, dict) else brand,
                "price": self._number(offers.get("lowPrice") or offers.get("price")),
                "price_max": self._number(offers.get("highPrice")),
                "currency": offers.get("priceCurrency"),
                "availability": (offers.get("availability") or "").rsplit("/", 1)[-1] or None,
                "url": response.urljoin(product.get("url")) if product.get("url") else None,
                "image_url": image[0] if isinstance(image, list) and image else image,
                "category": response.meta["category"], "page": page, "position": position,
                "source": "nordstromrack_itemlist_json_ld", "raw": product,
            }
        if page < self.max_pages:
            yield scrapy.Request(self._page_url(response.meta["listing_url"], page + 1), callback=self.parse,
                                 headers=self._headers(), meta={**response.meta, "page": page + 1})

    @staticmethod
    def _products(response):
        found = []
        for raw in response.css('script[type="application/ld+json"]::text').getall():
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            nodes = data.get("@graph", []) if isinstance(data, dict) else []
            nodes = [data, *nodes] if isinstance(data, dict) else data if isinstance(data, list) else []
            for node in nodes:
                if not isinstance(node, dict) or node.get("@type") not in ("ItemList", "CollectionPage"):
                    continue
                entries = node.get("itemListElement") or (node.get("mainEntity") or {}).get("itemListElement") or []
                for index, entry in enumerate(entries, 1):
                    product = entry.get("item") if isinstance(entry, dict) else None
                    if isinstance(product, dict):
                        found.append((entry.get("position") or index, product))
        return found

    @staticmethod
    def _page_url(url, page):
        parts = urlsplit(url); query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if page > 1: query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _number(value):
        try: return float(value) if value not in (None, "") else None
        except (TypeError, ValueError): return None

    @staticmethod
    def _headers():
        return {"accept": "text/html,application/xhtml+xml", "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"}
