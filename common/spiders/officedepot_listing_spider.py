from __future__ import annotations

import json
import re
import html
from typing import Any
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider

SITE_BASE = "https://www.officedepot.com"
CATEGORY_API_URL = "https://ma.officedepot.com/header-menu-excel/products.json"

_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")
_PRICE_CLEAN_RE = re.compile(r"[^0-9.]")
_UNDEF_RE = re.compile(r"\bundefined\b")


def _slugify(value: str) -> str:
    return _SLUG_CLEAN_RE.sub("-", value.lower()).strip("-")


def _parse_price(formatted_price: str | None) -> float | None:
    if formatted_price:
        try:
            return float(_PRICE_CLEAN_RE.sub("", formatted_price))
        except ValueError:
            pass
    return None


def _match_braces(text: str, start: int) -> int:
    """Return the index of the ``}`` matching the ``{`` at ``start`` (or -1).

    Brace counting is string-aware so ``}`` characters inside JSON strings do
    not terminate the object early.
    """
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _extract_js_object(text: str, key: str) -> str | None:
    """Extract the ``{...}`` object literal that follows ``key`` in ``text``."""
    key_idx = text.find(key)
    if key_idx == -1:
        return None
    open_idx = text.find("{", key_idx + len(key))
    if open_idx == -1:
        return None
    close_idx = _match_braces(text, open_idx)
    if close_idx == -1:
        return None
    return text[open_idx:close_idx + 1]


class OfficedepotListingSpider(BaseListingSpider):
    name = "officedepot_listing"
    allowed_domains = [
        "officedepot.com",
        "www.officedepot.com",
        "ma.officedepot.com",
    ]
    require_category_arg = False  # Categories are resolved dynamically.

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "department",
            "sub_category",
            "category",
            "item_id",
            "title",
            "brand",
            "url",
            "image_url",
            "price",
            "original_price",
            "list_price",
            "currency",
            "availability",
            "rating",
            "reviews_count",
            "item_number",
            "description",
            "catalog_labels",
            "category_id",
            "page",
            "category_url",
            "breadcrumbs",
            "source",
            "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._categories_to_resolve: list[dict[str, Any]] = []
        self._slug_index: dict[str, dict[str, Any]] = {}  # slug -> entry
        self._category_resolution_in_progress = False
        self._seen_ids: set[str] = set()

    def start_requests(self):
        if not self._categories_to_resolve and not self._category_resolution_in_progress:
            self._category_resolution_in_progress = True
            self.logger.info("Fetching categories from header-menu-excel/products.json...")
            yield scrapy.Request(
                CATEGORY_API_URL,
                callback=self.parse_categories_json,
                meta={"proxy": self._search_api_proxy(plain=True)},
            )
        else:
            yield from self._start_listing_crawls()

    def parse_categories_json(self, response: scrapy.http.Response):
        try:
            data = json.loads(response.text)
            menu_list = data.get("responseObject", {}).get("menuList", [])

            def _walk_category_tree(nodes: list[dict], department: str, sub_category: str):
                for node in nodes:
                    name = (node.get("name") or "").strip()
                    url = (node.get("url") or "").strip()
                    if url.startswith("/b/"):
                        entry = {
                            "department": department,
                            "sub_category": sub_category,
                            "name": name,
                            "url": url,
                        }
                        self._categories_to_resolve.append(entry)
                        self._add_to_slug_index(entry)
                    _walk_category_tree(node.get("hierarchy") or [], department, name)

            for department_node in menu_list:
                department_name = (department_node.get("name") or "").strip()
                department_url = (department_node.get("url") or "").strip()
                if department_url.startswith("/b/"):
                    entry = {
                        "department": department_name,
                        "sub_category": "",
                        "name": department_name,
                        "url": department_url,
                    }
                    self._categories_to_resolve.append(entry)
                    self._add_to_slug_index(entry)
                _walk_category_tree(department_node.get("hierarchy") or [], department_name, "")

            self.logger.info(f"Resolved {len(self._categories_to_resolve)} browse categories.")

            if self.args.category:
                if self.args.category not in self._slug_index:
                    raise ValueError(
                        f"Unknown category '{self.args.category}'. "
                        f"Available: {self.available_categories()}"
                    )
                self._categories_to_resolve = [self._slug_index[self.args.category]]

            self._category_resolution_in_progress = False
            yield from self._start_listing_crawls()

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse category JSON from {response.url}: {e}")
        except ValueError as e:
            self.logger.error(f"Category resolution error: {e}")

    def _add_to_slug_index(self, entry: dict[str, Any]):
        plain_slug = _slugify(entry["name"])
        qualified_slug = _slugify(f"{entry['department']}-{entry['name']}")

        if plain_slug not in self._slug_index or self._slug_index[plain_slug]["url"] == entry["url"]:
            self._slug_index[plain_slug] = entry
        self._slug_index[qualified_slug] = entry

    def _start_listing_crawls(self):
        self.logger.info("Starting listing crawls...")
        for entry in self._categories_to_resolve:
            category_url = urljoin(SITE_BASE, entry["url"])
            yield self._listing_request(category_url, page=1, metadata=entry)

    def _listing_request(self, url: str, page: int, metadata: dict[str, Any]):
        parsed = urlsplit(url)
        query_params = dict(
            qs.split("=", 1) for qs in parsed.query.split("&") if "=" in qs
        )
        query_params["page"] = str(page)
        new_query = "&".join(f"{k}={v}" for k, v in query_params.items())
        page_url = urlunsplit(parsed._replace(query=new_query))

        return scrapy.Request(
            page_url,
            callback=self.parse_listing_page,
            meta={
                "page": page,
                "metadata": metadata,
                "proxy": self._search_api_proxy(plain=True),
                "max_pages": self.max_pages,
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            },
            dont_filter=True,
        )

    def parse_listing_page(self, response: scrapy.http.Response):
        script_blob = response.xpath(
            '//script[contains(., "window.ODSEARCHBROWSE_INITIAL_STATE =")]/text()'
        ).get()
        if not script_blob:
            self.logger.warning(
                f"Could not find window.ODSEARCHBROWSE_INITIAL_STATE in script for {response.url}"
            )
            return

        state_str = _extract_js_object(script_blob, "window.ODSEARCHBROWSE_INITIAL_STATE")
        if not state_str:
            self.logger.warning(
                f"Could not extract ODSEARCHBROWSE_INITIAL_STATE object for {response.url}"
            )
            return

        processed_state_str = _UNDEF_RE.sub("null", state_str)
        try:
            state = json.loads(processed_state_str)
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Failed to parse ODSEARCHBROWSE_INITIAL_STATE JSON from {response.url}: {e}"
            )
            return

        products_data = state.get("products") or {}
        products = products_data.get("products") or []
        total_products = products_data.get("total") or 0

        current_page = response.meta["page"]
        metadata = response.meta["metadata"]
        max_pages = response.meta["max_pages"]
        breadcrumbs = [b.get("Description") for b in state.get("breadcrumbs") or []]

        if not products:
            self.logger.info(f"No products found for {response.url} (page {current_page})")
            return

        for product in products:
            item_id = product.get("id")
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)

            global_price = product.get("globalPrice") or {}
            bv = product.get("bvRating") or {}

            item: dict[str, Any] = {}
            item["department"] = metadata["department"]
            item["sub_category"] = metadata["sub_category"] or None
            item["category"] = metadata["name"]
            item["item_id"] = str(item_id)
            item["item_number"] = product.get("itemNumber") or str(item_id)
            item["title"] = html.unescape(product.get("shortDescription") or "")
            item["brand"] = product.get("brand")
            sku_url = product.get("skuUrl")
            item["url"] = urljoin(SITE_BASE, sku_url) if sku_url else None
            item["image_url"] = product.get("thumbImage")
            item["price"] = _parse_price((global_price.get("sellPrice") or {}).get("formattedPrice"))
            item["original_price"] = _parse_price(
                (global_price.get("regularPrice") or {}).get("formattedPrice")
            )
            item["list_price"] = _parse_price((global_price.get("listPrice") or {}).get("formattedPrice"))
            item["currency"] = "USD"

            availability_status = (product.get("availabilityStatus") or "").lower()
            if "out of stock" in availability_status or "backordered" in availability_status:
                item["availability"] = "OutOfStock"
            elif "in stock" in availability_status:
                item["availability"] = "InStock"
            else:
                item["availability"] = availability_status or None

            item["rating"] = bv.get("averageOverallRating")
            item["reviews_count"] = bv.get("totalReviewCount")
            item["description"] = html.unescape((product.get("description") or "").strip())
            item["catalog_labels"] = product.get("catalogLabels") or []
            item["category_id"] = product.get("categoryId")
            item["page"] = current_page
            item["category_url"] = response.url
            item["breadcrumbs"] = breadcrumbs
            item["source"] = "officedepot_bootstrap"
            item["raw"] = product
            yield item

        page_size = len(products)
        next_page = current_page + 1
        if page_size > 0 and current_page * page_size < total_products and next_page <= max_pages:
            yield self._listing_request(response.url, next_page, metadata)

    def available_categories(self) -> list[str]:
        return sorted(self._slug_index.keys())

    def resolve_target_url(self) -> str:
        return SITE_BASE

    def _search_api_proxy(self, plain: bool = False) -> str | None:
        if not hasattr(self, "settings"):
            return None
        proxy = self.settings.get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None
        # Office Depot serves real HTML on the plain datacenter route; no
        # residential/bypass option is required. Pass the proxy through verbatim.
        return proxy
