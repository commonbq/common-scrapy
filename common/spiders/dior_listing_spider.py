from __future__ import annotations

import json
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.dior_categories import DIOR_CATEGORIES


class DiorListingSpider(BaseListingSpider):
    """DIOR US products from the server-provided Next.js bootstrap only."""

    name = "dior_listing"
    allowed_domains = ["dior.com", "www.dior.com"]
    categories = DIOR_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "sku", "title", "description",
            "brand", "url", "image_url", "price", "currency", "categories",
            "is_new", "available", "page", "position", "source_url", "source",
            "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    async def start(self):
        self._seen.clear()
        target = self.resolve_target_url()
        yield scrapy.Request(
            target, callback=self.parse,
            meta={"page": 0, "base_url": target},
        )

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"DIOR listing returned HTTP {response.status}: {response.url}")
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"DIOR response has no __NEXT_DATA__ bootstrap: {response.url}")
        try:
            page_props = json.loads(raw)["props"]["pageProps"]
            queries = page_props["queriesProductsDictionnary"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"DIOR __NEXT_DATA__ is malformed or has no product queries: {response.url}") from exc
        if not isinstance(queries, dict):
            raise RuntimeError(f"DIOR bootstrap product query dictionary is invalid: {response.url}")

        emitted = 0
        for query in queries.values():
            if not isinstance(query, dict):
                continue
            for hit in query.get("hits", []):
                if not isinstance(hit, dict) or hit.get("type") != "PRODUCT":
                    continue
                item_id = str(hit.get("sku") or hit.get("objectID") or "").strip()
                if not item_id or item_id in self._seen:
                    continue
                self._seen.add(item_id)
                emitted += 1
                page = int(response.meta.get("page", 0))
                props = hit.get("trackingProductProperties") or {}
                listing_images = ((hit.get("views") or {}).get("listing") or {}).get("images") or {}
                image = (listing_images.get("r2x3listing") or {}).get("uri")
                price = hit.get("price") or {}
                yield {
                    "category": self.category,
                    "department": (self.category_entry(self.category) or {}).get("group"),
                    "item_id": item_id,
                    "sku": hit.get("sku"),
                    "title": hit.get("title"),
                    "description": hit.get("subtitle"),
                    "brand": "Dior",
                    "url": urljoin(response.url, (hit.get("productLink") or {}).get("uri") or ""),
                    "image_url": image,
                    "price": price.get("value"),
                    "currency": price.get("currency"),
                    "categories": hit.get("categories") or [],
                    "is_new": hit.get("isNew"),
                    "available": props.get("item_stock") == "In stock",
                    "page": page + 1,
                    "position": hit.get("productIndex", emitted - 1) + 1,
                    "source_url": response.url,
                    "source": "dior_next_data_bootstrap",
                    "raw": hit,
                    "timestamp": self.get_timestamp(),
                }

        if not emitted and int(response.meta.get("page", 0)) == 0:
            raise RuntimeError(f"No DIOR product hits in __NEXT_DATA__ at {response.url}")

        pagination = page_props.get("pagination") or {}
        next_url = pagination.get("next")
        page = int(response.meta.get("page", 0))
        if emitted and next_url and page + 1 < self.max_pages:
            yield scrapy.Request(
                self._next_page_url(response.meta["base_url"], page + 1),
                callback=self.parse,
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _next_page_url(base_url: str, page: int) -> str:
        parts = urlsplit(base_url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))
