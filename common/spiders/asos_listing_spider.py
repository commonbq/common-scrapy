from __future__ import annotations

import ast
import json
import re
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import scrapy

from common.spiders.asos_categories import ASOS_CATEGORIES, ASOS_DEPARTMENT_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


class AsosListingSpider(BaseListingSpider):
    """ASOS US listings using PLP hydration followed by the search API."""

    name = "asos_listing"
    allowed_domains = ["asos.com", "www.asos.com", "localhost", "127.0.0.1"]
    categories = ASOS_DEPARTMENT_CATEGORIES + ASOS_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "subcategory", "item_id", "style_id", "title", "brand",
            "url", "image_url", "color", "price", "original_price", "currency",
            "is_marked_down", "is_outlet_price", "is_selling_fast", "page",
            "position", "total_count", "source_url", "source", "raw",
            "timestamp",
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
        selected = self._selected_entry(target)
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

    def _selected_entry(self, target: str) -> dict:
        """Return the category entry that describes the resolved target URL.

        `categories` puts the department shortcuts ahead of the generated
        inventory aliases, and the department shortcuts share their URLs with the
        `women-view-all` / `men-view-all` aliases (all four point at the same
        department "New In" listing). Matching on URL alone therefore labelled an
        explicit `category=women-view-all` run as `subcategory="New In"` instead
        of its own `"View all"` label. Resolve a supplied category by its own
        category key first, then fall back to the URL lookup that serves
        `category_url=` and `url=` crawls.
        """
        if self.category:
            for entry in self.categories or []:
                if entry.get("category") == self.category:
                    return entry
        return next((entry for entry in (self.categories or []) if entry.get("url") == target), {})

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"ASOS listing returned HTTP {response.status}: {response.url}")
        if self._is_challenge(response.text):
            raise RuntimeError(
                f"ASOS listing returned an Akamai access-denied/challenge page at {response.url}; "
                "check the configured proxy"
            )
        state = self._extract_hydration(response.text)
        if not isinstance(state, dict):
            raise RuntimeError(f"No valid ASOS window.asos.plp._data hydration found at {response.url}")
        state = self._search_state(state)
        products = state.get("products")
        if not isinstance(products, list):
            raise RuntimeError(f"ASOS hydration has no list-valued products at {response.url}")

        yield from self._emit_products(products, response, state, "asos_plp_hydration")
        total = self._integer(state.get("itemCount"))
        query = state.get("query")
        offset = self._integer(query.get("offset")) if isinstance(query, dict) else None
        if self.max_pages > 1 and products and total is None:
            raise RuntimeError(f"ASOS hydration has no numeric itemCount at {response.url}")
        if self.max_pages > 1 and products and total is not None and (offset or 0) + len(products) < total:
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
                meta=self._api_meta(response.meta, page=page + 1, api_query=query),
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
        offset = self._integer(query.get("offset")) or 0
        api_query = self._normalized_query(query)
        api_query.update({"offset": offset + limit, "limit": limit})
        return scrapy.Request(
            self._api_url(cid, api_query),
            callback=self.parse_api,
            headers=self._api_headers(response.url),
            meta=self._api_meta(
                response.meta,
                page=next_page,
                cid=cid,
                api_query=api_query,
                referer=response.url,
            ),
        )

    # Fields the PLP bootstrap sends that are not part of the search API request
    # contract. Everything else in the hydrated query is forwarded verbatim so that
    # refined categories (e.g. `women-adidas`, which hydrate from `/refine/.../`) keep
    # their brand/size/price filters on the page-2 handoff instead of silently
    # widening back to the bare CID.
    _non_api_query_fields = {
        "browsedRegion", "deliveryCurrency", "experiment", "isSearchPage",
        "page", "searchTerm", "web analytics", "personalisation",
    }

    @staticmethod
    def _api_meta(base_meta: dict, **overrides) -> dict:
        """Copy spider state onto an API request without leaking proxy credentials.

        `HttpProxyMiddleware` rewrites `meta["proxy"]` to the credential-free URL and
        stashes the credentialed one in `meta["_auth_proxy"]` before the request is
        sent. Copying either key forward makes the follow-up request look like it was
        already authenticated, so the middleware reuses the sanitized URL without
        re-attaching `Proxy-Authorization` and the API leg fails with HTTP 407.
        Dropping both lets the project middleware restore auth on every API request.
        """
        meta = {key: value for key, value in base_meta.items() if key not in ("proxy", "_auth_proxy")}
        meta.update(overrides)
        return meta

    @classmethod
    def _normalized_query(cls, query: dict) -> dict:
        result = {}
        for key, value in query.items():
            if value is None or key in cls._non_api_query_fields:
                continue
            if isinstance(value, (str, int, float, bool)):
                result[key] = value
            elif isinstance(value, (dict, list)):
                # ASOS encodes structured filters (priceFilter, sizeFilter) as JSON
                # in the query string, matching the hydrated contract.
                result[key] = json.dumps(value, separators=(",", ":"))
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
        price = product.get("price")
        # The PLP bootstrap now sends a bare numeric `price` with `description` and
        # `image`, while the search API keeps the nested price object with `name` and
        # `imageUrl`. Normalize both shapes into the exported field contract.
        if isinstance(price, dict):
            current = price.get("current") if isinstance(price.get("current"), dict) else {}
            previous = price.get("previous") if isinstance(price.get("previous"), dict) else {}
            rrp = price.get("rrp") if isinstance(price.get("rrp"), dict) else {}
            original = previous.get("value") if previous.get("value") is not None else rrp.get("value")
            current_value = current.get("value")
            currency = price.get("currency")
        else:
            current_value = price
            original = product.get("reducedPrice")
            currency = product.get("currency") or "USD"
        product_url = product.get("url")
        image_url = product.get("imageUrl") or product.get("image")
        return {
            "category": response.meta.get("category"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": str(product.get("id")),
            "style_id": str(product.get("productCode") or product.get("colourWayId") or "") or None,
            "title": product.get("name") or product.get("description"),
            "brand": product.get("brandName"),
            "url": urljoin("https://www.asos.com/us/", str(product_url).lstrip("/")) if product_url else None,
            "image_url": self._https_url(image_url),
            "color": product.get("colour"),
            "price": self._number(current_value),
            "original_price": self._number(original),
            "currency": currency,
            "is_marked_down": self._boolean(price.get("isMarkedDown")) if isinstance(price, dict)
                            else self._boolean(product.get("isSale")),
            "is_outlet_price": self._boolean(price.get("isOutletPrice")) if isinstance(price, dict)
                                else self._boolean(product.get("isOutlet")),
            "is_selling_fast": self._boolean(product.get("isSellingFast")),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": source,
            "raw": product,
        }

    @classmethod
    def _search_state(cls, state: dict) -> dict:
        """Return the node that carries products/itemCount/query.

        ASOS moved the listing payload under a `search` object while keeping the
        older flat shape working, so accept both. Verified live 2026-10-01: the
        current response hydrates `state["search"]["products"]` with the products
        list, `itemCount` and `query` as siblings.
        """
        search = state.get("search")
        if isinstance(search, dict) and isinstance(search.get("products"), list):
            return search
        return state

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
                except (SyntaxError, TypeError, ValueError):
                    return None
                return state if isinstance(state, dict) else None
        return None

    @staticmethod
    def _is_challenge(document: str) -> bool:
        text = (document or "").lower()
        markers = (
            "access denied",
            "reference #18.",
            "akamai bot manager",
            "_abck",
            "bm_sz",
        )
        return any(marker in text for marker in markers)

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
