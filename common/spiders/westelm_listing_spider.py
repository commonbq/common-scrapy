from __future__ import annotations

"""West Elm listings from the store's Constructor.io browse API.

The category HTML is a shell: its ``window.__INITIAL_STATE__`` has empty
``thematicData``/``constructorData`` collections. It does expose the live
Constructor key and the category id. Product data is read exclusively from
``ac.cnstrc.com/browse/group_id/<id>``; there is no HTML/JSON-LD fallback.
"""

import json
import re
from urllib.parse import urlencode

import scrapy
from dotenv import dotenv_values

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.westelm_categories import WESTELM_CATEGORIES

CONSTRUCTOR_KEY_RE = re.compile(r'"constructorKey":"(key_[A-Za-z0-9]+)"')


class WestelmListingSpider(BaseListingSpider):
    name = "westelm_listing"
    allowed_domains = ["westelm.com", "www.westelm.com", "ac.cnstrc.com"]
    categories = WESTELM_CATEGORIES
    BROWSE_BASE = "https://ac.cnstrc.com/browse/group_id/"
    PAGE_SIZE = 100

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "item_id", "sku", "title", "url", "brand", "price",
            "regular_price", "sale_price", "price_min", "price_max",
            "currency", "image_url", "description", "availability_facets",
            "flags", "category", "category_name", "page", "position",
            "total_count", "listing_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = dotenv_values(".env").get("SCRAPEOPS_PROXY")
        if not self.proxy:
            raise ValueError("SCRAPEOPS_PROXY must be configured in .env")
        self.page_size = int(kwargs.get("page_size") or self.PAGE_SIZE)
        self.seen: set[str] = set()

    def start_requests(self):
        entry = self.category_entry(self.category)
        if not entry:
            raise ValueError(f"Unknown category {self.category!r}; available: {', '.join(self.available_categories())}")
        yield scrapy.Request(
            entry["url"], callback=self.parse_context,
            headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36", "accept-language": "en-US,en;q=0.9"},
            meta={"proxy": self.proxy, "category": self.category, "entry": entry},
        )

    def parse_context(self, response):
        if response.status != 200:
            raise RuntimeError(f"West Elm category page returned HTTP {response.status}: {response.url}")
        match = CONSTRUCTOR_KEY_RE.search(response.text)
        if not match:
            raise RuntimeError(f"West Elm bootstrap state has no Constructor key: {response.url}")
        entry = response.meta["entry"]
        yield self._browse_request(
            group_id=entry["group_id"], key=match.group(1), page=1,
            category=response.meta["category"], category_name=entry["category_name"],
            listing_url=response.url,
        )

    def _browse_request(self, *, group_id, key, page, category, category_name, listing_url):
        query = urlencode([
            ("key", key), ("num_results_per_page", self.page_size),
            ("page", page), ("section", "Products"),
        ])
        return scrapy.Request(
            f"{self.BROWSE_BASE}{group_id}?{query}", callback=self.parse_browse,
            headers={"accept": "application/json", "user-agent": "Mozilla/5.0"},
            meta={"proxy": self.proxy, "key": key, "group_id": group_id,
                  "page": page, "category": category, "category_name": category_name,
                  "listing_url": listing_url},
        )

    def parse_browse(self, response):
        if response.status != 200:
            raise RuntimeError(f"West Elm Constructor browse returned HTTP {response.status}: {response.url}")
        try:
            payload = json.loads(response.text)
            result = payload["response"]
            products = result["results"]
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Unexpected West Elm Constructor response at {response.url}") from exc
        if not isinstance(products, list):
            raise RuntimeError(f"West Elm Constructor results are not a list: {response.url}")
        page = int(response.meta["page"])
        for position, product in enumerate(products, start=1):
            data = product.get("data") if isinstance(product, dict) else None
            if not isinstance(data, dict):
                continue
            item_id = str(data.get("id") or data.get("leaderSku") or "")
            if not item_id or item_id in self.seen:
                continue
            self.seen.add(item_id)
            sale = data.get("salePriceMin")
            regular = data.get("regularPriceMin")
            price = sale if sale is not None else regular
            facets = data.get("facets") or []
            yield {
                "item_id": item_id,
                "sku": data.get("leaderSku") or data.get("skuid"),
                "title": data.get("title") or product.get("value"),
                "url": data.get("url"),
                "brand": "West Elm",
                "price": price,
                "regular_price": regular,
                "sale_price": sale,
                "price_min": data.get("lowestPrice"),
                "price_max": data.get("highestPrice"),
                "currency": "USD",
                "image_url": data.get("image_url") or data.get("thumb_image"),
                "description": data.get("description"),
                "availability_facets": {f.get("name"): f.get("values") for f in facets if isinstance(f, dict) and str(f.get("name", "")).startswith("avl")},
                "flags": data.get("flags"),
                "category": response.meta["category"],
                "category_name": response.meta["category_name"],
                "page": page,
                "position": position,
                "total_count": result.get("total_num_results"),
                "listing_url": response.meta["listing_url"],
                "source": "westelm_constructor_browse_api",
                "raw": data,
                "timestamp": self.get_timestamp(),
            }
        if products and page < self.max_pages and page * self.page_size < int(result.get("total_num_results") or 0):
            yield self._browse_request(
                group_id=response.meta["group_id"], key=response.meta["key"], page=page + 1,
                category=response.meta["category"], category_name=response.meta["category_name"],
                listing_url=response.meta["listing_url"],
            )
