from __future__ import annotations

"""DICK'S Sporting Goods listing spider (issue #164).

DICK'S storefront is an Angular (NgRx) SPA served behind Akamai.  Neither the
category page nor the product grid is present in the returned HTML: the PLP
ships only a shell plus a ``<script id="dcsg-ngx-plp-server-state">`` blob that
carries category metadata/facets but **no product cards**.  This spider
therefore uses exactly one data direction -- the first-party catalog
product-search JSON API:

    GET https://prod-catalog-product-api.dickssportinggoods.com/v2/search
        ?searchVO=<urlencoded JSON>

with ``selectedCategory = "12301_<catgroupId>"`` (``12301`` is DICK'S online
catalog id, ``storeId`` is ``15108``).  There is no HTML fallback: if the API
stops answering the spider fails loudly instead of silently degrading to an
empty shell grid.

The category taxonomy comes from a second first-party API (the same one the
SPA's ``seoDao.makeSEODataRequest$`` calls), captured once into
``dickssportinggoods_categories.py``:

    GET https://api-search.dickssportinggoods.com/seo-category/v1/categories
        ?seoUrl=<seoToken>&storeId=15108&children=true&published=true

Akamai protection requires the configured project proxy for the catalog host.
``_search_api_proxy()`` attaches that route explicitly to product requests.

Flow:
    category (or all categories)
        -> v2/search (searchVO, pageNumber=N, pageSize=48)
        -> emit one item per productVO
        -> repeat with pageNumber=N+1 until max_pages, an empty page, or the
           reported totalCount is exhausted
"""

import json
import re
import time
from typing import Any
from urllib.parse import urlencode

import scrapy

from common.settings import PROXY
from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.dickssportinggoods_categories import (
    DICKSSPORTINGGOODS_CATEGORY_INVENTORY,
)

SEARCH_ENDPOINT = "https://prod-catalog-product-api.dickssportinggoods.com/v2/search"
SITE_BASE = "https://www.dickssportinggoods.com"
CATALOG_ID = "12301"
STORE_ID = 15108
PAGE_SIZE = 48
IMAGE_BASE = "https://dks.scene7.com/is/image/dkscdn/"
IMAGE_PRESET = "?$DSG_ProductCard$"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def _iter_nodes(node: dict[str, Any]):
    yield node
    for child in node.get("subcategories") or []:
        if isinstance(child, dict):
            yield from _iter_nodes(child)


def _load_categories() -> list[dict[str, Any]]:
    """Flatten the nested SEO inventory into unique ``{category,url,...}`` rows.

    Cross-listed nodes repeat under several departments with an identical URL
    and ``catgroupId``, so dedupe on the URL and collect every department that
    references the node.
    """
    by_url: dict[str, dict[str, Any]] = {}
    ordered: list[dict[str, Any]] = []
    for department, root in DICKSSPORTINGGOODS_CATEGORY_INVENTORY.items():
        for node in _iter_nodes(root):
            url = node.get("url")
            catgroup_id = node.get("catgroupId")
            if not url or catgroup_id is None:
                continue
            entry = by_url.get(url)
            if entry is None:
                entry = {
                    "category": node.get("seoUrl") or _slugify(url),
                    "name": node.get("name") or department,
                    "url": url,
                    "catgroupId": catgroup_id,
                    "page_type": node.get("pageType"),
                    "departments": [department],
                }
                by_url[url] = entry
                ordered.append(entry)
            elif department not in entry["departments"]:
                entry["departments"].append(department)
    return ordered


class DickssportinggoodsListingSpider(BaseListingSpider):
    name = "dickssportinggoods_listing"
    allowed_domains = [
        "dickssportinggoods.com",
        "www.dickssportinggoods.com",
        "prod-catalog-product-api.dickssportinggoods.com",
        "api-search.dickssportinggoods.com",
    ]
    require_category_arg = False

    categories = _load_categories()

    PAGE_SIZE = PAGE_SIZE

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "department",
            "category_name",
            "category_id",
            "category_url",
            "category_page_type",
            "catalog_id",
            "store_id",
            "item_id",
            "partnumber",
            "parent_partnumber",
            "title",
            "brand",
            "url",
            "image_url",
            "image_alt",
            "price",
            "list_price",
            "map_price",
            "discount_percent",
            "currency",
            "rating",
            "reviews_count",
            "is_coming_soon",
            "is_color_pinned",
            "product_attributes",
            "primary_category",
            "page",
            "position",
            "total_count",
            "source_url",
            "source",
            "raw",
        ],
    }

    # An HTML body where JSON was expected means a bot wall / geo-block, not a
    # product payload. Matched case-insensitively because the WAF varies casing.
    CHALLENGE_MARKERS = (
        "access denied",
        "captcha",
        "are you a human",
        "request unsuccessful",
        "site unavailable",
        "pardon the interruption",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_items: set[str] = set()
        # Injectable clock so price-window selection is deterministic in tests.
        self._now_ms: int | None = None

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_items.clear()
        for entry in self._target_categories():
            yield self._search_request(entry, page=1)

    def _target_categories(self) -> list[dict[str, Any]]:
        target = self.resolve_target_url() if (self.url or self.category_url or self.category) else None
        if target is None:
            return list(self.categories)
        for entry in self.categories:
            if entry["url"] == target or entry["category"] == self.category:
                return [entry]
        available = ", ".join(self.available_categories()[:20])
        raise ValueError(
            f"Unknown category '{self.category or target}'. The catalog product API "
            "needs a DICK'S catgroupId, so the target must be one of the bundled "
            f"inventory entries. Available categories (first 20): {available}"
        )

    def _search_request(self, entry: dict[str, Any], *, page: int):
        search_vo = {
            "selectedCategory": f"{CATALOG_ID}_{entry['catgroupId']}",
            "selectedStore": "",
            "selectedSort": 0,
            "selectedFilters": {},
            "storeId": STORE_ID,
            "pageNumber": page - 1,
            "pageSize": self.PAGE_SIZE,
            "searchTypes": ["COLOR_PINNING"],
            "isFamilyPage": True,
        }
        url = f"{SEARCH_ENDPOINT}?{urlencode({'searchVO': json.dumps(search_vo, separators=(',', ':'))})}"
        meta: dict[str, Any] = {
            "entry": entry,
            "category": entry["category"],
            "department": entry.get("departments", [None])[0],
            "page": page,
        }
        proxy = self._search_api_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            url,
            callback=self.parse_search,
            headers=self._api_headers(entry["url"]),
            meta=meta,
            dont_filter=True,
        )

    # ------------------------------------------------------------------ parse

    def parse_search(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        entry = response.meta["entry"]
        payload = self._json_payload(response)

        products = payload.get("productVOs") or []
        total = self._integer(payload.get("totalCount"))
        if not isinstance(products, list):
            raise RuntimeError(f"DICK'S v2/search returned no productVOs list at {response.url}")

        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item = self._item(product, response, entry, page, position, total)
            if item is not None:
                yield item

        if page >= self.max_pages or not products:
            return
        consumed = page * self.PAGE_SIZE
        if total is not None and consumed >= total:
            return
        yield self._search_request(entry, page=page + 1)

    def _json_payload(self, response: scrapy.http.Response) -> dict[str, Any]:
        if response.status != 200:
            raise RuntimeError(
                f"DICK'S v2/search returned HTTP {response.status}: {response.url}"
            )
        body = response.text or ""
        lowered = body.lower()
        if any(marker in lowered for marker in self.CHALLENGE_MARKERS):
            raise RuntimeError(
                f"DICK'S v2/search returned a bot-challenge page at {response.url}; "
                "the catalog host needs a working configured proxy route."
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"DICK'S v2/search returned non-JSON body at {response.url}: {body[:200]!r}"
            ) from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"DICK'S v2/search returned a non-object payload at {response.url}")
        return payload

    # ------------------------------------------------------------------- item

    def _item(self, product, response, entry, page, position, total):
        item_id = self._text(product.get("catentryId")) or self._text(product.get("partnumber"))
        if not item_id or item_id in self._seen_items:
            return None
        self._seen_items.add(item_id)

        attributes = self._attributes(product.get("attributes"))
        price, list_price, map_price = self._prices(product.get("floatFacets"))
        image_name = (
            product.get("swatchPartnumber")
            or product.get("fullImage")
            or product.get("thumbnail")
        )
        path = product.get("dsgSeoUrl") or product.get("assetSeoUrl")
        title = product.get("name")
        indicators = product.get("dsgPriceIndicators")
        indicators = indicators if isinstance(indicators, dict) else {}

        return {
            "category": entry["category"],
            "department": entry.get("departments", [None])[0],
            "category_name": entry.get("name"),
            "category_id": entry.get("catgroupId"),
            "category_url": entry.get("url"),
            "category_page_type": entry.get("page_type"),
            "catalog_id": CATALOG_ID,
            "store_id": STORE_ID,
            "item_id": item_id,
            "partnumber": self._text(product.get("partnumber")),
            "parent_partnumber": product.get("parentPartnumber"),
            "title": title,
            "brand": product.get("mfName") or attributes.get("X_BRAND"),
            "url": f"{SITE_BASE}{path}" if path else None,
            "image_url": f"{IMAGE_BASE}{image_name}{IMAGE_PRESET}" if image_name else None,
            "image_alt": title,
            "price": price,
            "list_price": list_price,
            "map_price": map_price,
            "discount_percent": self._number(indicators.get("dealsPercentage")),
            "currency": "USD",
            "rating": self._number(product.get("ratingValue")),
            "reviews_count": self._integer(product.get("ratingCount")),
            "is_coming_soon": self._bool(product.get("isComingSoon")),
            "is_color_pinned": self._bool(product.get("isColorPinned")),
            "product_attributes": attributes or None,
            "primary_category": attributes.get("PRIMARY_CATEGORY_DSG "),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": "dickssportinggoods_search_api",
            "raw": product,
        }

    def _prices(self, facets):
        """Resolve (price, list_price, map_price) from the ``floatFacets`` list.

        Current price is the ``offerprice`` facet whose ``[start,end]`` window
        contains "now"; the sample carries several historical/upcoming windows,
        so taking the first (or the min) would report the wrong price. Windows
        use epoch milliseconds.
        """
        now_ms = self._now_ms if self._now_ms is not None else int(time.time() * 1000)
        list_price = None
        map_price = None
        active_offer = None
        for facet in facets or []:
            if not isinstance(facet, dict):
                continue
            identifier = facet.get("identifier")
            value = self._number(facet.get("value"))
            if identifier == "dickssportinggoodslistprice":
                list_price = value
            elif identifier == "dickssportinggoodsmapprice":
                map_price = value if value else None
            elif identifier == "dickssportinggoodsofferprice":
                start = facet.get("startDateTime")
                end = facet.get("endDateTime")
                if start is not None and end is not None and start <= now_ms <= end:
                    active_offer = value
        price = active_offer if active_offer is not None else list_price
        return price, list_price, map_price

    @staticmethod
    def _attributes(raw_attributes) -> dict[str, Any]:
        if not isinstance(raw_attributes, str) or not raw_attributes:
            return {}
        try:
            parsed = json.loads(raw_attributes)
        except (TypeError, ValueError):
            return {}
        if not isinstance(parsed, list):
            return {}
        merged: dict[str, Any] = {}
        for pair in parsed:
            if isinstance(pair, dict):
                merged.update(pair)
        return merged

    # ------------------------------------------------------------------ proxy

    def _search_api_proxy(self) -> str | None:
        """Return the configured project proxy for the product API.

        ``PROXY`` is normally loaded from ``.env`` by ``common.settings`` and
        is not registered as a Scrapy setting. Keep routing explicit so API
        requests cannot accidentally go direct, and preserve the configured
        provider route unchanged.
        """
        configured = self.settings.get("PROXY") if hasattr(self, "settings") else None
        proxy = configured or PROXY
        return proxy if isinstance(proxy, str) and proxy else None

    # ------------------------------------------------------------------ utils

    def _api_headers(self, referer: str) -> dict[str, str]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": referer,
            "Origin": SITE_BASE,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _text(value):
        return None if value is None else str(value)

    @staticmethod
    def _bool(value):
        return bool(value) if isinstance(value, bool) else None

    @staticmethod
    def _number(value):
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, str):
            match = re.search(r"-?\d[\d,]*(?:\.\d+)?", value)
            value = match.group(0).replace(",", "") if match else None
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        if isinstance(value, bool) or value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
