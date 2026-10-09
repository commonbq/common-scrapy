from __future__ import annotations

"""HSN listings from the storefront's first-party Constructor browse API.

The public HSN Constructor client supplies its current API key. Product records,
totals, and pagination all come from the JSON API; the spider intentionally has
no category-page, product-card, or JSON-LD fallback.
"""

import json
from html import unescape
import re
from urllib.parse import urlencode, urlsplit

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.hsn_categories import HSN_CATEGORIES


CONSTRUCTOR_CLIENT_URL = "https://cnstrc.com/js/cust/hsn_1oWza0.js"
PRODUCTION_KEY_RE = re.compile(
    r'\["www\.hsn\.com","www07\.hsn\.com"\]\.includes\([^)]*\)\?"(key_[A-Za-z0-9_-]+)"'
)
ANY_KEY_RE = re.compile(r"key_[A-Za-z0-9_-]{12,}")
BLOCK_MARKERS = ("access denied", "captcha", "failed to get successful response")


class HsnListingSpider(BaseListingSpider):
    name = "hsn_listing"
    allowed_domains = ["hsn.com", "www.hsn.com", "cnstrc.com", "ac.cnstrc.com"]
    categories = HSN_CATEGORIES
    API_BASE = "https://ac.cnstrc.com"
    PAGE_SIZE = 60

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        # Both public Constructor hosts work directly. This also avoids a known
        # environment-level 407 on a second proxied HTTPS CONNECT.
        "PROXY": "",
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category", "category_url", "category_id", "item_id", "variation_id",
            "web_product_id", "sku", "title", "description", "url", "image_url",
            "image_name", "image_manifest_received_date", "price",
            "currency", "group_ids", "is_slotted", "page", "position",
            "total_count", "total_pages", "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        self.page_size = int(kwargs.pop("page_size", self.PAGE_SIZE))
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()
        self._constructor_key: str | None = None

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield scrapy.Request(
            CONSTRUCTOR_CLIENT_URL,
            callback=self.parse_constructor_client,
            errback=self.on_error,
            meta={"category": self.category, "category_url": category_url},
            dont_filter=True,
        )

    def parse_constructor_client(self, response):
        self._validate_response(response, "Constructor client")
        match = PRODUCTION_KEY_RE.search(response.text)
        if not match:
            keys = list(dict.fromkeys(ANY_KEY_RE.findall(response.text)))
            if len(keys) != 1:
                raise CloseSpider(
                    f"Could not identify HSN's production Constructor key in {response.url}"
                )
            self._constructor_key = keys[0]
        else:
            self._constructor_key = match.group(1)
        yield self._api_request(page=1, meta=response.meta)

    def _api_request(self, *, page: int, meta: dict):
        if not self._constructor_key:
            raise RuntimeError("Constructor key must be discovered before browsing")
        category_id = urlsplit(meta["category_url"]).path.rstrip("/").split("/")[-1].upper()
        query = urlencode(
            {
                "key": self._constructor_key,
                "num_results_per_page": self.page_size,
                "page": page,
                "section": "Products",
            }
        )
        return scrapy.Request(
            f"{self.API_BASE}/browse/group_id/{category_id}?{query}",
            callback=self.parse_api,
            errback=self.on_error,
            headers={"Accept": "application/json", "Referer": meta["category_url"]},
            meta={**meta, "category_id": category_id, "page": page},
            dont_filter=True,
        )

    def parse_api(self, response):
        self._validate_response(response, "Constructor browse API")
        try:
            payload = json.loads(response.text)
            api_response = payload["response"]
            results = api_response["results"]
            total_count = int(api_response["total_num_results"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise CloseSpider(f"Invalid HSN Constructor response from {response.url}: {exc}") from exc

        meta = response.meta
        page = int(meta["page"])
        total_pages = (total_count + self.page_size - 1) // self.page_size
        for offset, result in enumerate(results, start=1):
            data = result.get("data") or {}
            item_id = str(data.get("id") or data.get("webm_id") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            price_cents = data.get("price")
            image_name = data.get("image_name")
            yield {
                "category": meta["category"],
                "category_url": meta["category_url"],
                "category_id": meta["category_id"],
                "item_id": item_id,
                "variation_id": data.get("variation_id"),
                "web_product_id": data.get("webp_id") or data.get("webm_id"),
                "sku": image_name.split("_", 1)[0] if isinstance(image_name, str) else None,
                "title": unescape(result.get("value") or "") or None,
                "description": unescape(data.get("description") or "") or None,
                "url": data.get("url"),
                "image_url": data.get("image_url"),
                "image_name": image_name,
                "image_manifest_received_date": data.get("image_manifest_received_date"),
                "price": price_cents / 100 if isinstance(price_cents, (int, float)) else None,
                "currency": "USD",
                "group_ids": data.get("group_ids") or [],
                "is_slotted": bool(result.get("is_slotted")),
                "page": page,
                "position": (page - 1) * self.page_size + offset,
                "total_count": total_count,
                "total_pages": total_pages,
                "source_url": response.url,
                "source": "hsn_constructor_browse_api",
                "raw": result,
                "timestamp": self.job_timestamp,
            }

        if results and page < self.max_pages and page < total_pages:
            yield self._api_request(page=page + 1, meta=meta)

    @staticmethod
    def _validate_response(response, leg: str):
        lowered = response.text.lower()
        if response.status != 200 or not response.body or any(x in lowered for x in BLOCK_MARKERS):
            raise CloseSpider(f"HSN {leg} failed ({response.status}): {response.url}")

    def on_error(self, failure):
        raise CloseSpider(f"HSN request failed: {failure.value}")
