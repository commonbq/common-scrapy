from __future__ import annotations

"""Costco category/listing spider.

Usage examples:
  scrapy crawl costco_listing -a category='coffee' -a max_pages=1
  scrapy crawl costco_listing -a category_url='https://www.costco.com/coffee.html' -a max_pages=1
"""

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.retail_bootstrap_utils import extract_next_flight_rows

COSTCO_CATEGORY_SEED = {
    "grocery-household": {
        "all": "https://www.costco.com/grocery-household.html",
        "coffee": "https://www.costco.com/coffee.html",
        "coffee/single-serve": "https://www.costco.com/single-serve-coffee.html",
        "coffee/whole-bean": "https://www.costco.com/whole-bean-coffee.html",
        "coffee/ground": "https://www.costco.com/ground-coffee.html",
        "coffee/instant": "https://www.costco.com/instant-coffee.html",
        "coffee/creamers": "https://www.costco.com/creamer-sweeteners.html",
        "coffee/tea": "https://www.costco.com/tea.html",
        "water": "https://www.costco.com/water.html",
        "snacks": "https://www.costco.com/snacks.html",
        "laundry": "https://www.costco.com/laundry-detergent.html",
        "paper-products": "https://www.costco.com/paper-products.html",
    },
    "health-personal-care": {
        "vitamins": "https://www.costco.com/vitamins.html",
    },
}

_ROOT_CATEGORY_TITLES = {
    "grocery-household": "Grocery & Household",
    "health-personal-care": "Health & Personal Care",
}

DEFAULT_WAREHOUSE_NUMBER = "847"


def _sample_path(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "sample" / name


def _slug_from_url(url: str, parent_alias: str | None = None) -> str:
    slug = Path(urlparse(url).path).name.removesuffix(".html")
    parts = [part for part in slug.split("-") if part]
    if parent_alias:
        parent_parts = {
            part for part in parent_alias.split("/")[-1].split("-") if part
        }
        trimmed = [part for part in parts if part not in parent_parts]
        if trimmed:
            parts = trimmed
    return "-".join(parts) or slug


def _load_categories_by_parent() -> dict[str, list[dict[str, Any]]]:
    try:
        payload = json.loads(_sample_path("costco-categories.json").read_text("utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    categories = payload.get("categories_by_parent")
    return categories if isinstance(categories, dict) else {}


def _expand_costco_categories() -> dict[str, dict[str, str]]:
    expanded = copy.deepcopy(COSTCO_CATEGORY_SEED)
    categories_by_parent = _load_categories_by_parent()

    for root_slug, root_title in _ROOT_CATEGORY_TITLES.items():
        bucket = expanded.setdefault(root_slug, {})
        url_aliases = {url: alias for alias, url in bucket.items()}
        visited_titles: set[str] = set()

        def visit(parent_title: str, alias_prefix: str | None = None):
            if parent_title in visited_titles:
                return
            visited_titles.add(parent_title)
            for entry in categories_by_parent.get(parent_title, []):
                if not isinstance(entry, dict):
                    continue
                url = entry.get("url")
                title = entry.get("name")
                if not isinstance(url, str) or not isinstance(title, str):
                    continue
                absolute_url = urljoin("https://www.costco.com", url)
                alias = url_aliases.get(absolute_url)
                if alias is None:
                    leaf = _slug_from_url(absolute_url, alias_prefix)
                    alias = f"{alias_prefix}/{leaf}" if alias_prefix else leaf
                    if alias not in bucket:
                        bucket[alias] = absolute_url
                    url_aliases[absolute_url] = alias
                if title in categories_by_parent:
                    visit(title, alias)

        visit(root_title)
    return expanded


COSTCO_CATEGORIES = _expand_costco_categories()


class CostcoListingSpider(BaseListingSpider):
    name = "costco_listing"
    allowed_domains = ["costco.com", "www.costco.com", "gdx-api.costco.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = COSTCO_CATEGORIES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[tuple[str | None, str]] = set()

    def available_categories(self) -> list[str]:
        aliases = {
            alias
            for group in self.categories.values()
            for alias in group
            if alias != "all"
        }
        return sorted(aliases)

    def resolve_target_url(self) -> str:
        if self.url or self.category_url:
            return self.url or self.category_url
        if not self.category:
            available = ", ".join(self.available_categories())
            raise ValueError(
                f"Provide -a category=<name>. Available categories: {available}"
            )
        for group in self.categories.values():
            if self.category in group:
                return group[self.category]
        available = ", ".join(self.available_categories())
        raise ValueError(
            f"Unknown category '{self.category}'. Available categories: {available}"
        )

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield scrapy.Request(
            category_url,
            callback=self.parse,
            meta={"page": 1, "category_url": category_url, "source_url": category_url},
        )

    def parse(self, response: scrapy.http.Response):
        if self._is_blocked_response(response.text, response.status):
            return

        flight = self._extract_flight_context(response.text or "", response.url)
        if not flight:
            self.logger.warning(
                "Costco React Flight discovery failed (status=%s)", response.status
            )
            return

        meta = {
            "category": self.category,
            "category_name": flight["category_title"],
            "category_page_id": flight["page_id"],
            "category_id": flight["category_id"],
            "category_url": self.category_url or self.url or response.url,
            "page": 1,
            "page_size": flight["page_size"],
            "source_url": response.url,
            "subcategories": flight["subcategories"],
            "flight": flight,
        }
        yield self._build_search_request(meta, offset=0, page=1)

    def parse_search(self, response: scrapy.http.Response):
        if self._is_blocked_response(response.text, response.status):
            return

        payload = self._json_body(response)
        if not isinstance(payload, dict):
            self.logger.warning(
                "Costco listing API returned invalid JSON (status=%s)", response.status
            )
            return

        results = self._extract_search_results(payload)
        if not results:
            self.logger.info(
                "Costco listing exhausted (page=%s)", response.meta.get("page", 1)
            )
            return

        page = int(response.meta["page"])
        page_size = int(response.meta["page_size"])
        yielded = 0
        for item in results:
            item_key = item.get("item_id") or item.get("url") or item.get("title")
            seen_key = (
                response.meta.get("category_url"),
                str(item_key),
            ) if item_key is not None else None
            if seen_key and seen_key in self._seen_products:
                continue
            if seen_key:
                self._seen_products.add(seen_key)
            yielded += 1
            yield {
                **item,
                "mode": "category",
                "category": response.meta.get("category"),
                "category_name": response.meta.get("category_name"),
                "category_url": response.meta.get("category_url"),
                "page": page,
                "source_url": response.meta.get("source_url"),
            }

        total_size = self._extract_total_size(payload)
        offset = int(response.meta.get("offset", 0))
        if page < self.max_pages and (
            total_size is None
            or offset + page_size < total_size
            or len(results) >= page_size
        ):
            next_offset = offset + page_size
            yield self._build_search_request(response.meta, next_offset, page + 1)

    def _build_search_request(self, meta: dict[str, Any], offset: int, page: int):
        flight = meta["flight"]
        search_config = flight["search_config"]
        payload = self._build_search_payload(flight, offset)
        request_meta = {
            **meta,
            "offset": offset,
            "page": page,
        }
        return scrapy.Request(
            search_config["endpoint"],
            method=(search_config.get("method") or "POST").upper(),
            headers=self._search_headers(search_config, request_meta["category_url"]),
            body=json.dumps(payload),
            callback=self.parse_search,
            meta=request_meta,
        )

    def _build_search_payload(
        self, flight: dict[str, Any], offset: int
    ) -> dict[str, Any]:
        required = copy.deepcopy(flight["search_config"].get("required_request_parameters") or {})
        required.update(
            {
                "visitorId": self._visitor_id(flight["page_id"]),
                "query": "",
                "pageSize": flight["page_size"],
                "offset": offset,
                "orderBy": None,
                "searchMode": "page",
                "personalizationEnabled": False,
                "warehouseId": flight["warehouse_id"],
                "shipToPostal": "",
                "shipToState": "",
                "deliveryLocations": [flight["warehouse_id"]],
                "filterBy": [
                    f'attributes.category_uri: ANY("{flight["page_id"]}")'
                ],
                "pageCategories": [flight["page_id"]],
            }
        )
        return required

    def _search_headers(
        self, search_config: dict[str, Any], referer: str | None
    ) -> dict[str, str]:
        headers: dict[str, str] = {}
        for key, value in (search_config.get("required_request_headers") or {}).items():
            if isinstance(value, dict):
                if key == "locale":
                    value = value.get("en-us") or value.get("en-US")
                else:
                    value = value.get("USBC")
            if value is None:
                continue
            headers[key] = str(value)
        headers.update(
            {
                "origin": "https://www.costco.com",
                "referer": referer or "https://www.costco.com/",
                "user-agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/146.0.0.0 Safari/537.36"
                ),
            }
        )
        return headers

    def _extract_flight_context(
        self, html: str, source_url: str
    ) -> dict[str, Any] | None:
        rows = extract_next_flight_rows(html)
        if not rows:
            return None
        parsed_rows = self._parse_rows(rows)
        search_config = self._first_key(parsed_rows, "serviceConfigurationGRSSearch")
        page_entry = self._first_key(parsed_rows, "specificPageEntry")
        display_config = self._first_match(
            parsed_rows,
            lambda node: isinstance(node, dict)
            and node.get("pageType") == "category"
            and isinstance(node.get("resultsPerPage"), int),
        )
        if not (
            isinstance(search_config, dict)
            and isinstance(page_entry, dict)
            and isinstance(display_config, dict)
        ):
            return None
        category_info = page_entry.get("category_id") or {}
        page_id = page_entry.get("page_id")
        category_title = (
            category_info.get("category_title")
            or page_entry.get("title")
            or display_config.get("categoryTitle")
        )
        category_id = category_info.get("category_id")
        if not isinstance(page_id, str) or not isinstance(category_id, str):
            return None
        subcategories = self._extract_subcategories(parsed_rows, source_url)
        page_size = int(
            display_config.get("resultsPerPage")
            or (search_config.get("required_request_parameters") or {}).get("pageSize")
            or 20
        )
        page_size = max(1, min(page_size, 96))
        warehouse_number = self._first_key(parsed_rows, "productApiWarehouseNumber")
        if not isinstance(warehouse_number, str):
            warehouse_number = DEFAULT_WAREHOUSE_NUMBER
        return {
            "category_id": category_id,
            "category_title": category_title or self.category or page_id,
            "page_id": page_id,
            "page_size": page_size,
            "search_config": search_config,
            "subcategories": subcategories,
            "warehouse_id": f"{warehouse_number}-wh",
        }

    def _extract_subcategories(
        self, parsed_rows: dict[str, Any], source_url: str
    ) -> list[dict[str, str]]:
        subcategories: list[dict[str, str]] = []
        seen: set[str] = set()
        for row_id, row in parsed_rows.items():
            raw = json.dumps(row)
            if '"Shop by Category"' not in raw:
                continue
            resolved = self._resolve_refs(row, parsed_rows)
            for node in self._walk(resolved):
                if not isinstance(node, dict):
                    continue
                category_data = node.get("categoryData")
                if not isinstance(category_data, dict):
                    continue
                href = category_data.get("hrefUrl")
                title = category_data.get("title")
                if not isinstance(href, str) or not isinstance(title, str):
                    continue
                url = urljoin(source_url, href)
                if url in seen:
                    continue
                seen.add(url)
                subcategories.append(
                    {
                        "title": title,
                        "url": url,
                        "alias": _slug_from_url(url, self.category or None),
                        "row_id": row_id,
                    }
                )
        return subcategories

    @staticmethod
    def _parse_rows(rows: list[str]) -> dict[str, Any]:
        parsed: dict[str, Any] = {}
        for row in rows:
            row_id, _, body = row.partition(":")
            if not body.startswith("["):
                continue
            try:
                parsed[row_id] = json.loads(body)
            except ValueError:
                continue
        return parsed

    def _resolve_refs(
        self, node: Any, parsed_rows: dict[str, Any], depth: int = 0
    ) -> Any:
        if depth > 4:
            return node
        if isinstance(node, str):
            match = re.fullmatch(r"\$L([0-9a-f]+)", node)
            if match and match.group(1) in parsed_rows:
                return self._resolve_refs(parsed_rows[match.group(1)], parsed_rows, depth + 1)
            return node
        if isinstance(node, list):
            return [self._resolve_refs(item, parsed_rows, depth) for item in node]
        if isinstance(node, dict):
            return {
                key: self._resolve_refs(value, parsed_rows, depth)
                for key, value in node.items()
            }
        return node

    @classmethod
    def _first_key(cls, parsed_rows: dict[str, Any], key: str) -> Any:
        for row in parsed_rows.values():
            for node in cls._walk(row):
                if isinstance(node, dict) and key in node:
                    return node[key]
        return None

    @classmethod
    def _first_match(cls, parsed_rows: dict[str, Any], predicate):
        for row in parsed_rows.values():
            for node in cls._walk(row):
                if predicate(node):
                    return node
        return None

    @staticmethod
    def _walk(node: Any):
        if isinstance(node, dict):
            yield node
            for value in node.values():
                yield from CostcoListingSpider._walk(value)
        elif isinstance(node, list):
            for value in node:
                yield from CostcoListingSpider._walk(value)

    @staticmethod
    def _json_body(response: scrapy.http.Response) -> dict[str, Any] | None:
        if response.status != 200:
            return None
        try:
            body = json.loads(response.text)
        except ValueError:
            return None
        return body if isinstance(body, dict) else None

    @staticmethod
    def _extract_total_size(payload: dict[str, Any]) -> int | None:
        search_result = payload.get("searchResult")
        if isinstance(search_result, dict):
            total_size = search_result.get("totalSize")
            if isinstance(total_size, int):
                return total_size
        return None

    def _extract_search_results(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        search_result = payload.get("searchResult")
        results = search_result.get("results") if isinstance(search_result, dict) else None
        if not isinstance(results, list):
            return []
        items: list[dict[str, Any]] = []
        for result in results:
            if not isinstance(result, dict):
                continue
            normalized = self._normalize_search_result(result)
            if normalized:
                items.append(normalized)
        return items

    def _normalize_search_result(self, result: dict[str, Any]) -> dict[str, Any] | None:
        product = result.get("product") or {}
        if not isinstance(product, dict):
            product = {}
        rollups = result.get("variantRollupValues") or {}
        if not isinstance(rollups, dict):
            rollups = {}
        rating = product.get("rating") or result.get("rating") or {}
        if not isinstance(rating, dict):
            rating = {}

        url = product.get("uri") or product.get("url")
        if isinstance(url, str) and url.startswith("/"):
            url = urljoin("https://www.costco.com", url)

        item_id = (
            result.get("id")
            or product.get("itemNumber")
            or product.get("id")
            or self._extract_id_from_url(url)
        )
        title = product.get("title") or product.get("name")
        if item_id is None and title is None and not url:
            return None

        current_price = self._first_float(
            rollups.get("price")
            or rollups.get(
                f"inventory({DEFAULT_WAREHOUSE_NUMBER}-wh, price)"
            )
        )
        original_price = self._first_float(rollups.get("originalPrice"))
        brand = product.get("brand")
        if not brand:
            brands = product.get("brands")
            if isinstance(brands, list) and brands:
                brand = brands[0]
        image_url = self._extract_image_url(product)
        rating_value = rating.get("averageRating") or rating.get("value")
        review_count = rating.get("ratingCount") or rating.get("reviewCount")

        return {
            "item_id": str(item_id) if item_id is not None else None,
            "title": title,
            "url": url,
            "price": current_price,
            "original_price": original_price,
            "currency": product.get("currency") or ("USD" if current_price is not None else None),
            "brand": brand,
            "image_url": image_url,
            "rating": self._first_float(rating_value),
            "reviews_count": self._first_int(review_count),
            "source": "costco_grs_search_api",
            "raw": result,
        }

    @staticmethod
    def _extract_image_url(product: dict[str, Any]) -> str | None:
        images = product.get("images")
        if isinstance(images, list):
            for image in images:
                if isinstance(image, dict):
                    url = image.get("url") or image.get("href") or image.get("src")
                    if isinstance(url, str):
                        return url
                elif isinstance(image, str):
                    return image
        image = product.get("image") or product.get("imageUrl") or product.get("primaryImage")
        if isinstance(image, dict):
            image = image.get("url") or image.get("href") or image.get("src")
        return image if isinstance(image, str) else None

    @staticmethod
    def _extract_id_from_url(url: Any) -> str | None:
        if not isinstance(url, str):
            return None
        match = re.search(r"(\d{6,})", url)
        return match.group(1) if match else None

    @staticmethod
    def _first_float(value: Any) -> float | None:
        if isinstance(value, list):
            value = value[0] if value else None
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            match = re.search(r"(\d+(?:\.\d+)?)", value.replace(",", ""))
            if match:
                return float(match.group(1))
        return None

    @staticmethod
    def _first_int(value: Any) -> int | None:
        if isinstance(value, list):
            value = value[0] if value else None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            digits = re.sub(r"[^\d]", "", value)
            return int(digits) if digits else None
        return None

    @staticmethod
    def _is_blocked_response(text: str | None, status: int) -> bool:
        body = (text or "").lower()
        return status >= 400 or "access denied" in body

    @staticmethod
    def _visitor_id(seed: str) -> str:
        return hashlib.md5(seed.encode("utf-8")).hexdigest()
