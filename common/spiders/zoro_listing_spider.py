"""Zoro category listings from the server-rendered Vuex bootstrap."""

from __future__ import annotations

import json
import math
import re
from typing import Any
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.zoro_categories import ZORO_CATEGORIES


_INITIAL_STATE_RE = re.compile(
    r'window\.INITIAL_STATE\s*=\s*("(?:[^"\\]|\\.)*")', re.DOTALL
)
_CATEGORY_CODE_RE = re.compile(r"/c/([^/]+)/")
_PROXY_ERROR_MARKERS = ("api credits", "proxy authentication required", "ip_forbidden")


class ZoroListingSpider(BaseListingSpider):
    """Extract only ``search.response.records`` from ``window.INITIAL_STATE``.

    Department hubs contain their child taxonomy in the same bootstrap. The
    spider walks that data to schedule leaf PLPs, then follows ``?page=N``.
    Rendered cards and JSON-LD are deliberately not parsed.
    """

    name = "zoro_listing"
    allowed_domains = ["zoro.com", "www.zoro.com", "localhost", "127.0.0.1"]
    categories = ZORO_CATEGORIES
    require_category_arg = False
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "leaf_category", "category_id",
            "item_id", "erp_id", "manufacturer_number", "title", "brand",
            "url", "image_url", "image_urls", "price", "original_price",
            "currency", "price_unit", "minimum_quantity", "package_quantity",
            "availability", "lead_time", "is_ltl", "group_hash", "group_name",
            "group_sku_count", "taxonomy_path", "attributes", "page",
            "position", "total_count", "total_pages", "source_url", "source",
            "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/141.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<department>, category_url=<url>, or url=<url>"
            )
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self.headers,
            meta={"page": 1, "base_url": target, "department": self.category or "custom"},
            dont_filter=True,
        )

    def parse(self, response):
        state = self._initial_state(response)
        search = state.get("search") or {}
        search_response = search.get("response") or {}
        records = search_response.get("records") or []
        page = int(response.meta.get("page", 1))

        if not records:
            if page > 1:
                return
            leaves = self._leaf_categories(state, response.url)
            if not leaves:
                raise RuntimeError(
                    f"Zoro bootstrap had neither product records nor child categories at {response.url}"
                )
            self.logger.info("Zoro department resolved to %d leaf PLPs", len(leaves))
            for leaf in leaves:
                yield scrapy.Request(
                    leaf["url"],
                    callback=self.parse,
                    headers=self.headers,
                    meta={
                        **response.meta,
                        "page": 1,
                        "base_url": leaf["url"],
                        "leaf_category": leaf["name"],
                        "category_id": leaf["code"],
                    },
                )
            return

        pagination = search_response.get("pagination") or {}
        total_count = self._integer(pagination.get("totalSize")) or len(records)
        page_size = self._integer(pagination.get("pageSize")) or len(records)
        total_pages = max(1, math.ceil(total_count / page_size))
        category_id, leaf_name, department, taxonomy_path = self._category_context(
            records, response
        )

        for position, record in enumerate(records, 1):
            if not isinstance(record, dict):
                continue
            product = record.get("product") or {}
            item_id = str(product.get("zoroNo") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(
                record, product, response, page, position, total_count, total_pages,
                category_id, leaf_name, department, taxonomy_path,
            )

        if page < min(total_pages, self.max_pages):
            next_page = page + 1
            yield scrapy.Request(
                self._page_url(response.meta["base_url"], next_page),
                callback=self.parse,
                headers=self.headers,
                meta={**response.meta, "page": next_page},
                dont_filter=True,
            )

    @classmethod
    def _initial_state(cls, response) -> dict[str, Any]:
        if response.status != 200:
            raise RuntimeError(f"Zoro listing returned HTTP {response.status}: {response.url}")
        lowered = response.text[:1000].lower()
        if any(marker in lowered for marker in _PROXY_ERROR_MARKERS):
            raise RuntimeError(f"Zoro listing returned a proxy error payload: {response.url}")
        match = _INITIAL_STATE_RE.search(response.text)
        if not match:
            raise RuntimeError(
                f"Zoro window.INITIAL_STATE missing at {response.url}; possible challenge"
            )
        # Zoro emits JavaScript ``\xHH`` escapes (not valid JSON) in category
        # descriptions. Re-express those bytes as equivalent JSON Unicode
        # escapes and keep both decoding passes strict.
        encoded = re.sub(
            r"\\x([0-9a-fA-F]{2})", r"\\u00\1", match.group(1).replace(r"\'", "'")
        )
        try:
            return json.loads(json.loads(encoded))
        except (TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Invalid Zoro INITIAL_STATE at {response.url}") from exc

    @classmethod
    def _leaf_categories(cls, state: dict[str, Any], url: str) -> list[dict[str, str]]:
        match = _CATEGORY_CODE_RE.search(urlsplit(url).path)
        code = match.group(1) if match else ""
        category_data = ((state.get("category") or {}).get("categoryData") or {})
        root = category_data.get(code)
        if not isinstance(root, dict):
            return []

        leaves: list[dict[str, str]] = []
        seen: set[str] = set()

        def walk(node: dict[str, Any]):
            children = [child for child in (node.get("b") or []) if isinstance(child, dict)]
            if not children:
                child_code = str(node.get("1") or "").strip()
                slug = str(node.get("3") or "").strip()
                if child_code and slug and child_code != code and child_code not in seen:
                    seen.add(child_code)
                    leaves.append({
                        "code": child_code,
                        "name": str(node.get("2") or slug),
                        "url": f"https://www.zoro.com/{slug}/c/{child_code}/",
                    })
                return
            for child in children:
                walk(child)

        walk(root)
        return leaves

    def _item(
        self, record, product, response, page, position, total_count, total_pages,
        category_id, leaf_name, department, taxonomy_path,
    ):
        group = record.get("group") or {}
        item_id = str(product.get("zoroNo"))
        slug = product.get("slug")
        group_hash = group.get("groupHash")
        if group_hash:
            url = f"https://www.zoro.com/{slug}/g/{group_hash}/"
        else:
            url = f"https://www.zoro.com/{slug}/i/{item_id}/"
        media = [
            entry.get("name") for entry in (product.get("media") or [])
            if isinstance(entry, dict) and str(entry.get("type") or "").startswith("image/")
        ]
        image_urls = [
            f"https://www.zoro.com/static/cms/product/full/{quote(name, safe='/._-')}"
            for name in media if name
        ]
        attributes = {
            str(entry.get("name")): entry.get("value")
            for entry in (product.get("attributes") or [])
            if isinstance(entry, dict) and entry.get("name")
        }
        original_price = product.get("originalPrice") or None
        unavailable = product.get("isDiscontinued") or product.get("isForcedOutOfStock")
        return {
            "category": self.category or "custom",
            "department": department,
            "leaf_category": leaf_name,
            "category_id": category_id,
            "item_id": item_id,
            "erp_id": product.get("erpId"),
            "manufacturer_number": product.get("mfrNo"),
            "title": product.get("title") or record.get("title"),
            "brand": product.get("brand") or record.get("brand"),
            "url": url,
            "image_url": image_urls[0] if image_urls else None,
            "image_urls": image_urls,
            "price": product.get("price"),
            "original_price": original_price,
            "currency": "USD",
            "price_unit": product.get("priceUnit"),
            "minimum_quantity": product.get("minRetailQty"),
            "package_quantity": product.get("packageQty"),
            "availability": "OutOfStock" if unavailable else "InStock",
            "lead_time": product.get("leadTime"),
            "is_ltl": product.get("isLTL"),
            "group_hash": group_hash,
            "group_name": group.get("groupName"),
            "group_sku_count": len(group.get("groupSkus") or []),
            "taxonomy_path": taxonomy_path,
            "attributes": attributes,
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": response.url,
            "source": "zoro_initial_state_search_records",
            "raw": record,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _category_context(records, response):
        product = (records[0].get("product") or {}) if records else {}
        path = product.get("primaryCategoryPaths") or []
        pairs = []
        for entry in path:
            if not isinstance(entry, dict):
                continue
            code = entry.get("1") or entry.get("code")
            name = entry.get("2") or entry.get("name")
            if code or name:
                pairs.append((str(code or ""), str(name or "")))
        category_id = response.meta.get("category_id") or (pairs[-1][0] if pairs else None)
        leaf = response.meta.get("leaf_category") or (pairs[-1][1] if pairs else None)
        department = pairs[0][1] if pairs else response.meta.get("department")
        return category_id, leaf, department, " > ".join(name for _, name in pairs)

    @staticmethod
    def _integer(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query) if key != "page"]
        if page > 1:
            query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
