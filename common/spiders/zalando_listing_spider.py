"""Zalando listing products from the server-provided GraphQL hydration cache."""

from __future__ import annotations

import json
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

import scrapy
from dotenv import dotenv_values

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.zalando_categories import ZALANDO_CATEGORIES


class ZalandoListingSpider(BaseListingSpider):
    name = "zalando_listing"
    allowed_domains = ["zalando.de", "www.zalando.de", "en.zalando.de"]
    categories = ZALANDO_CATEGORIES
    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "page", "position", "item_id", "sku", "name",
            "brand", "price", "original_price", "currency", "url",
            "image_url", "available_sizes", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = dotenv_values(".env").get("SCRAPEOPS_PROXY")
        if not self.proxy:
            raise ValueError("SCRAPEOPS_PROXY must be configured in .env")
        self.seen = set()

    async def start(self):
        if self.url or self.category_url:
            target = self.url or self.category_url
            category = self.category or "custom"
        else:
            entry = self.category_entry(self.category)
            if not entry:
                raise ValueError(f"Unknown category {self.category!r}")
            target, category = entry["url"], self.category
        yield scrapy.Request(
            target, callback=self.parse,
            meta={"proxy": self.proxy, "page": 1, "category": category,
                  "base_url": target},
            headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
                     "accept-language": "en-US,en;q=0.9"},
        )

    @staticmethod
    def _hydration(response):
        caches = []
        markers = ("window.__hydrationDataConsume(", "runtime['hydratePartial'](")
        for script in response.xpath("//script/text()").getall():
          for marker in markers:
            offset = script.find(marker)
            if offset < 0:
                continue
            start = offset + len(marker)
            depth = 0
            quoted = escaped = False
            for index in range(start, len(script)):
                char = script[index]
                if quoted:
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        quoted = False
                elif char == '"':
                    quoted = True
                elif char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        payload = json.loads(script[start:index + 1])
                        caches.extend(payload.get("graphqlCache", payload.get("cache", {})).values())
                        break
        if caches:
            return {"graphqlCache": {str(i): value for i, value in enumerate(caches)}}
        raise ValueError(f"Zalando hydration cache not found at {response.url}")

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Zalando returned HTTP {response.status}: {response.url}")
        state = self._hydration(response)
        products = {}
        collection_edges = []
        for entry in state.get("graphqlCache", {}).values():
            data = entry.get("data") or {}
            product = data.get("product")
            if isinstance(product, dict) and product.get("id"):
                products[product["id"]] = product
            collection = data.get("collection") or {}
            collection_edges.extend((collection.get("entities") or {}).get("edges") or [])

        self.logger.info("Hydration cache: %d products, %d collection edges", len(products), len(collection_edges))

        page = int(response.meta.get("page", 1))
        emitted = 0
        for position, edge in enumerate(collection_edges, 1):
            product_id = ((edge.get("node") or {}).get("id"))
            product = products.get(product_id)
            if not product or product_id in self.seen:
                continue
            self.seen.add(product_id)
            emitted += 1
            price = product.get("displayPrice") or {}
            gallery = product.get("gallery") or []
            first_image = (gallery[0].get("galleryMedium") or gallery[0].get("gallerySmall") or {}) if gallery else {}
            yield {
                "category": response.meta["category"], "page": page,
                "position": position, "item_id": product_id,
                "sku": product.get("sku"), "name": product.get("name"),
                "brand": (product.get("brand") or {}).get("name"),
                "price": price.get("trackingCurrentAmount"),
                "original_price": (((price.get("original") or {}).get("amount") or 0) / 100 or None),
                "currency": ((price.get("original") or {}).get("currency")),
                "url": product.get("uri"), "image_url": first_image.get("uri"),
                "available_sizes": [simple.get("size") for simple in product.get("simples", []) if simple.get("size")],
                "source_url": response.url, "source": "zalando_bootstrap",
                "raw": product,
            }

        if not emitted and page == 1:
            raise RuntimeError(f"No hydrated product records found at {response.url} (products={len(products)}, edges={len(collection_edges)})")
        if page < self.max_pages and collection_edges:
            parts = urlsplit(response.meta["base_url"])
            query = dict(parse_qsl(parts.query, keep_blank_values=True))
            query["p"] = str(page + 1)
            next_url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
            yield scrapy.Request(next_url, callback=self.parse,
                                 meta={**response.meta, "page": page + 1},
                                 headers=response.request.headers, dont_filter=True)
