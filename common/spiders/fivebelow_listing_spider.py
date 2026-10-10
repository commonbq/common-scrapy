from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.fivebelow_categories import FIVEBELOW_CATEGORIES


_FLIGHT_CHUNK_RE = re.compile(
    r"self\.__next_f\.push\(\[\s*1\s*,\s*(\"(?:[^\"\\]|\\.)*\")\s*\]\)",
    re.DOTALL,
)
_ALGOLIA_MARKER = '"algoliaConfig":'
_SEARCH_STATE_MARKER = 'window[Symbol.for("InstantSearchInitialResults")] = '
_CHALLENGE_MARKERS = ("access denied", "captcha", "cf-chl-", "just a moment")


class FiveBelowListingSpider(BaseListingSpider):
    """Five Below variants from its first-party Algolia product-search API."""

    name = "fivebelow_listing"
    allowed_domains = [
        "fivebelow.com",
        "www.fivebelow.com",
        "algolia.net",
    ]
    categories = FIVEBELOW_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "RETRY_HTTP_CODES": [403, 408, 429, 500, 502, 503, 504],
        "RETRY_TIMES": 3,
        # The storefront needs the configured proxy, while Algolia accepts the
        # POST directly. Add the proxy explicitly to the discovery request.
        "DOWNLOADER_MIDDLEWARES": {
            "common.middlewares.CommonDownloaderMiddleware": None,
        },
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "sku", "product_id", "variant_id",
            "style_number", "title", "brand", "url", "image_url",
            "image_urls", "description", "price", "min_price", "max_price",
            "currency", "availability", "in_stock", "department",
            "sub_department", "product_class", "product_subclass", "color",
            "size", "flavor", "age_groups", "taxonomy_paths",
            "order_limit", "local_delivery", "channel_eligibility",
            "inventory_store_count", "release_date", "page", "position",
            "total_count", "total_pages", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/140.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        selected = self._selected_category()
        meta = {"category": selected["category"], "listing_url": selected["url"]}
        proxy = self.settings.get("PROXY")
        if proxy:
            meta["proxy"] = proxy
        yield scrapy.Request(
            meta["listing_url"],
            callback=self.parse_discovery,
            headers=self.headers,
            meta=meta,
            dont_filter=True,
        )

    def _selected_category(self) -> dict[str, str]:
        if self.url or self.category_url:
            return {
                "category": self.category or "custom",
                "url": self.url or self.category_url,
            }
        if self.category:
            selected = self.category_entry(self.category)
            if selected:
                return selected
            available = ", ".join(self.available_categories())
            raise ValueError(
                f"Unknown category '{self.category}'. Available categories: {available}"
            )
        return next(iter(self.iter_categories()))

    def parse_discovery(self, response: scrapy.http.Response):
        self._reject_storefront(response)
        config = self._algolia_config(response.text)
        state = self._search_state(response.text)
        index_name = config.get("indexName")
        search = state.get(index_name) if isinstance(index_name, str) else None
        if not isinstance(search, dict):
            raise RuntimeError(
                f"Five Below search hydration has no {index_name!r} index at {response.url}"
            )
        request_params = search.get("requestParams")
        if not isinstance(request_params, list) or not request_params:
            raise RuntimeError(
                f"Five Below search hydration has no request parameters at {response.url}"
            )
        params = request_params[0]
        if not isinstance(params, dict):
            raise RuntimeError("Five Below hydrated search parameters are malformed")
        yield self._api_request(config, params, response.meta, page=0)

    def parse_api(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(
                f"Five Below Algolia API returned HTTP {response.status}: {response.url}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError("Five Below Algolia API returned invalid JSON") from exc
        results = payload.get("results") if isinstance(payload, dict) else None
        result = results[0] if isinstance(results, list) and results else None
        if not isinstance(result, dict) or not isinstance(result.get("hits"), list):
            raise RuntimeError("Five Below Algolia API response has no result hits")

        page_zero = self._integer(result.get("page")) or 0
        total_count = self._integer(result.get("nbHits"))
        total_pages = self._integer(result.get("nbPages"))
        position = 0
        for hit in result["hits"]:
            if not isinstance(hit, dict):
                continue
            variants = hit.get("variants")
            if not isinstance(variants, list):
                continue
            for variant in variants:
                if not isinstance(variant, dict):
                    continue
                sku = str(variant.get("sku") or "").strip()
                if not sku or sku in self._seen:
                    continue
                self._seen.add(sku)
                position += 1
                yield self._item(
                    hit, variant, response, page_zero + 1, position,
                    total_count, total_pages,
                )

        if total_pages and page_zero + 1 < min(total_pages, self.max_pages):
            yield self._api_request(
                response.meta["config"], response.meta["params"],
                response.meta, page=page_zero + 1,
            )

    def _api_request(self, config, params, meta, page):
        app_id = str(config.get("appId") or "").strip()
        api_key = str(config.get("searchApiKey") or "").strip()
        index_name = str(config.get("indexName") or "").strip()
        if not all((app_id, api_key, index_name)):
            raise RuntimeError("Five Below hydration has an incomplete Algolia config")
        query = dict(params)
        query["page"] = page
        encoded = urlencode(
            {
                key: json.dumps(value, separators=(",", ":"))
                if isinstance(value, (list, dict, bool)) else value
                for key, value in query.items()
            }
        )
        request_meta = {
            "category": meta["category"],
            "listing_url": meta["listing_url"],
            "config": config,
            "params": params,
            "page": page,
        }
        return scrapy.Request(
            f"https://{app_id}-dsn.algolia.net/1/indexes/*/queries",
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Origin": "https://www.fivebelow.com",
                "Referer": meta["listing_url"],
                "X-Algolia-Application-Id": app_id,
                "X-Algolia-API-Key": api_key,
            },
            body=json.dumps({
                "requests": [{"indexName": index_name, "params": encoded}]
            }),
            callback=self.parse_api,
            meta=request_meta,
            dont_filter=True,
        )

    def _item(self, hit, variant, response, page, position, total_count, total_pages):
        attrs = variant.get("attributes")
        attrs = attrs if isinstance(attrs, dict) else {}
        prices = variant.get("prices")
        prices = prices.get("USD") if isinstance(prices, dict) else {}
        prices = prices if isinstance(prices, dict) else {}
        values = prices.get("priceValues")
        first_price = values[0].get("value") if isinstance(values, list) and values and isinstance(values[0], dict) else None
        images = [str(value) for value in variant.get("images") or [] if value]
        inventory = variant.get("inventory")
        inventory = inventory if isinstance(inventory, dict) else {}
        locale = "en-US"
        name = hit.get("name")
        description = hit.get("description")
        slug = hit.get("slug")
        categories = hit.get("categories")
        categories = categories.get(locale) if isinstance(categories, dict) else {}
        categories = categories if isinstance(categories, dict) else {}
        taxonomy_paths = []
        for level in ("lvl0", "lvl1", "lvl2"):
            for path in categories.get(level) or []:
                if path not in taxonomy_paths:
                    taxonomy_paths.append(path)
        product_slug = slug.get(locale) if isinstance(slug, dict) else None
        availability = attrs.get("productState")
        brand = self._first(attrs.get("fmBrand")) or attrs.get("brand") or attrs.get("cleanBrandName")
        return {
            "category": response.meta["category"],
            "item_id": str(variant.get("sku")),
            "sku": variant.get("sku"),
            "product_id": hit.get("objectID"),
            "variant_id": variant.get("id"),
            "style_number": attrs.get("styleNumber"),
            "title": name.get(locale) if isinstance(name, dict) else name,
            "brand": brand,
            "url": urljoin("https://www.fivebelow.com/products/", product_slug) if product_slug else None,
            "image_url": images[0] if images else None,
            "image_urls": images,
            "description": description.get(locale) if isinstance(description, dict) else description,
            "price": self._cents(first_price),
            "min_price": self._cents(prices.get("min")),
            "max_price": self._cents(prices.get("max")),
            "currency": "USD",
            "availability": availability,
            "in_stock": availability == "available",
            "department": attrs.get("department"),
            "sub_department": attrs.get("subDepartment"),
            "product_class": attrs.get("class"),
            "product_subclass": attrs.get("subclass"),
            "color": attrs.get("colorFacet"),
            "size": attrs.get("variantSize") or attrs.get("sizeFacet"),
            "flavor": attrs.get("flavor"),
            "age_groups": attrs.get("age"),
            "taxonomy_paths": taxonomy_paths,
            "order_limit": self._integer(attrs.get("orderLimitQuantity")),
            "local_delivery": self._boolean(attrs.get("localDelivery")),
            "channel_eligibility": attrs.get("channelEligibility"),
            "inventory_store_count": len(inventory),
            "release_date": attrs.get("releaseDateTime"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": response.meta["listing_url"],
            "source": "fivebelow_algolia_product_search_api",
            "raw": {"product": hit, "variant": variant},
        }

    @classmethod
    def _algolia_config(cls, document: str) -> dict[str, Any]:
        chunks = _FLIGHT_CHUNK_RE.findall(document or "")
        flight = "".join(json.loads(chunk) for chunk in chunks)
        offset = flight.find(_ALGOLIA_MARKER)
        if offset < 0:
            raise RuntimeError("Five Below RSC hydration has no Algolia config")
        try:
            config, _ = json.JSONDecoder().raw_decode(
                flight, offset + len(_ALGOLIA_MARKER)
            )
        except ValueError as exc:
            raise RuntimeError("Five Below Algolia config is malformed") from exc
        if not isinstance(config, dict):
            raise RuntimeError("Five Below Algolia config is not an object")
        return config

    @staticmethod
    def _search_state(document: str) -> dict[str, Any]:
        offset = (document or "").find(_SEARCH_STATE_MARKER)
        if offset < 0:
            raise RuntimeError("Five Below page has no InstantSearch hydration")
        try:
            state, _ = json.JSONDecoder().raw_decode(
                document, offset + len(_SEARCH_STATE_MARKER)
            )
        except ValueError as exc:
            raise RuntimeError("Five Below InstantSearch hydration is malformed") from exc
        if not isinstance(state, dict):
            raise RuntimeError("Five Below InstantSearch hydration is not an object")
        return state

    @staticmethod
    def _first(value):
        return value[0] if isinstance(value, list) and value else value

    @staticmethod
    def _cents(value):
        try:
            return round(float(value) / 100, 2) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _boolean(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() == "true"
        return None

    @staticmethod
    def _reject_storefront(response):
        head = response.text[:6000].lower()
        if response.status != 200 or any(marker in head for marker in _CHALLENGE_MARKERS):
            raise RuntimeError(
                f"Five Below storefront returned a challenge/proxy response "
                f"(HTTP {response.status}): {response.url}"
            )
