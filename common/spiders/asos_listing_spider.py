from __future__ import annotations

import ast
import json
import re
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import scrapy

from common.spiders.asos_categories import ASOS_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


class AsosListingSpider(BaseListingSpider):
    """ASOS US listings using PLP hydration followed by the search API."""

    name = "asos_listing"
    allowed_domains = ["asos.com", "www.asos.com", "localhost", "127.0.0.1"]
    categories = ASOS_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "subcategory", "item_id", "style_id", "title", "brand",
            "url", "image_url", "color", "price", "original_price", "currency",
            "is_marked_down", "is_outlet_price", "is_selling_fast", "page",
            "position", "total_count", "source_url", "source", "raw",
        ],
    }

    _assignment = re.compile(r"window\.asos\.plp\._data\s*=\s*JSON\.parse\(\s*(['\"])")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self._html_headers(),
            meta={
                "category": self.category or "custom",
                "subcategory": selected.get("subcategory"),
                "page": 1,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"ASOS listing returned HTTP {response.status}: {response.url}")
        state = self._extract_hydration(response.text)
        if not isinstance(state, dict):
            raise RuntimeError(f"No valid ASOS window.asos.plp._data hydration found at {response.url}")
        products = state.get("products")
        if not isinstance(products, list):
            raise RuntimeError(f"ASOS hydration has no list-valued products at {response.url}")

        yield from self._emit_products(products, response, state, "asos_plp_hydration")
        if self.max_pages > 1:
            request = self._api_request(response, state, next_page=2)
            if request:
                yield request

    def parse_api(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"ASOS search API returned HTTP {response.status}: {response.url}")
        try:
            payload = json.loads(response.text)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"ASOS search API returned invalid JSON at {response.url}") from exc
        products = payload.get("products") if isinstance(payload, dict) else None
        if not isinstance(products, list):
            raise RuntimeError(f"ASOS search API has no list-valued products at {response.url}")

        yield from self._emit_products(products, response, payload, "asos_search_api")
        page = int(response.meta["page"])
        offset = int(response.meta["api_query"]["offset"])
        limit = int(response.meta["api_query"]["limit"])
        total = self._integer(payload.get("itemCount"))
        if total is None:
            raise RuntimeError(f"ASOS search API has no numeric itemCount at {response.url}")
        if products and page < self.max_pages and offset + len(products) < total:
            query = dict(response.meta["api_query"])
            query["offset"] = offset + limit
            yield scrapy.Request(
                self._api_url(response.meta["cid"], query),
                callback=self.parse_api,
                headers=self._api_headers(response.meta["referer"]),
                meta={**response.meta, "page": page + 1, "api_query": query},
            )

    def _emit_products(self, products, response, payload, source):
        page = int(response.meta.get("page", 1))
        total = self._integer(payload.get("itemCount"))
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("id") or "")
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, response, page, position, total, source)

    def _api_request(self, response, state: dict, next_page: int):
        query = state.get("query")
        if not isinstance(query, dict):
            raise RuntimeError(f"ASOS hydration has no query object for API handoff at {response.url}")
        cid = str(query.get("cid") or parse_qs(urlparse(response.url).query).get("cid", [""])[0])
        limit = self._integer(query.get("limit")) or len(state.get("products", []))
        if not cid or not limit:
            raise RuntimeError(f"ASOS hydration is missing cid/limit for API handoff at {response.url}")
        api_query = self._normalized_query(query)
        api_query.update({"offset": limit, "limit": limit})
        return scrapy.Request(
            self._api_url(cid, api_query),
            callback=self.parse_api,
            headers=self._api_headers(response.url),
            meta={**response.meta, "page": next_page, "cid": cid, "api_query": api_query, "referer": response.url},
        )

    @staticmethod
    def _normalized_query(query: dict) -> dict:
        allowed = {
            "store", "country", "currency", "keyStoreDataversion", "lang",
            "rowlength", "channel", "offset", "limit", "sort", "q",
        }
        result = {key: value for key, value in query.items() if key in allowed and value is not None}
        result.setdefault("store", "US")
        result.setdefault("country", "US")
        result.setdefault("currency", "USD")
        result.setdefault("lang", "en-US")
        result.setdefault("rowlength", 4)
        result.setdefault("channel", "desktop-web")
        return result

    @staticmethod
    def _api_url(cid: str, query: dict) -> str:
        return f"https://www.asos.com/api/product/search/v2/categories/{cid}?{urlencode(query)}"

    def _item(self, product, response, page, position, total, source):
        price = product.get("price") if isinstance(product.get("price"), dict) else {}
        current = price.get("current") if isinstance(price.get("current"), dict) else {}
        previous = price.get("previous") if isinstance(price.get("previous"), dict) else {}
        rrp = price.get("rrp") if isinstance(price.get("rrp"), dict) else {}
        original = previous.get("value") if previous.get("value") is not None else rrp.get("value")
        product_url = product.get("url")
        image_url = product.get("imageUrl")
        return {
            "category": response.meta.get("category"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": str(product.get("id")),
            "style_id": str(product.get("productCode") or product.get("colourWayId") or "") or None,
            "title": product.get("name"),
            "brand": product.get("brandName"),
            "url": urljoin("https://www.asos.com/us/", str(product_url).lstrip("/")) if product_url else None,
            "image_url": self._https_url(image_url),
            "color": product.get("colour"),
            "price": self._number(current.get("value")),
            "original_price": self._number(original),
            "currency": price.get("currency"),
            "is_marked_down": self._boolean(price.get("isMarkedDown")),
            "is_outlet_price": self._boolean(price.get("isOutletPrice")),
            "is_selling_fast": self._boolean(product.get("isSellingFast")),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": source,
            "raw": product,
        }

    @classmethod
    def _extract_hydration(cls, document: str) -> dict | None:
        match = cls._assignment.search(document or "")
        if not match:
            return None
        quote = match.group(1)
        start = match.end()
        escaped = False
        for index in range(start, len(document)):
            char = document[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                raw = document[start:index]
                try:
                    # Python string literal decoding matches the escapes used by this
                    # single/double-quoted JavaScript bootstrap string.
                    decoded = ast.literal_eval(f"{quote}{raw}{quote}")
                    state = json.loads(decoded)
                except (TypeError, ValueError):
                    return None
                return state if isinstance(state, dict) else None
        return None

    @staticmethod
    def _html_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @classmethod
    def _api_headers(cls, referer):
        return {**cls._html_headers(), "accept": "application/json", "referer": referer}

    @staticmethod
    def _https_url(value):
        if not value:
            return None
        value = str(value)
        return value if value.startswith("https://") else "https://" + value.lstrip("/")

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _boolean(value):
        if isinstance(value, bool):
            return value
        return str(value).lower() == "true"
