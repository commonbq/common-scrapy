from __future__ import annotations

"""Best Buy keyword search spider using discovered GraphQL persisted queries.

Flow:
1) Load Best Buy search page HTML
2) Discover GraphQL endpoint + persisted query metadata from embedded runtime config
3) Replay discovered persisted query against /gateway/graphql
4) Normalize listing-like product records

Usage:
  scrapy crawl bestbuy_search -a q=laptop -a max_pages=1

Notes:
- Best Buy runtime changes often; this spider is defensive and generic.
"""

import json
import re
from typing import Any
from urllib.parse import urlencode

import scrapy

from common.spiders.base_search_spider import BaseSearchSpider


class BestbuySearchSpider(BaseSearchSpider):
    name = "bestbuy_search"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com", "bifrostgw.us.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(self, q: str | None = None, max_pages: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(q=q, max_pages=max_pages)

    def start_requests(self):
        first = self._build_search_url(self.args.q or "")
        yield scrapy.Request(first, callback=self.parse_search_page, meta=self.maybe_proxy_meta({"page": 1, "original_url": first}))

    def parse_search_page(self, response: scrapy.http.Response):
        html = response.text or ""
        page = int(response.meta.get("page", 1))

        endpoint = self._extract_graphql_endpoint(html) or "https://www.bestbuy.com/gateway/graphql"
        candidates = self._extract_persisted_queries(html)

        if not candidates:
            self.logger.warning("No GraphQL persisted-query candidates discovered on page=%s", page)
            return

        # Prefer candidates likely related to product list/search.
        ranked = sorted(
            candidates,
            key=lambda c: (
                0 if any(x in (c.get("operation_name") or "").lower() for x in ["search", "product", "list", "plp"]) else 1,
                0 if c.get("variables") else 1,
            ),
        )

        chosen = ranked[0]
        variables = self._patch_variables(chosen.get("variables") or {}, query=self.args.q, page=page)

        body = {
            "operationName": chosen.get("operation_name"),
            "variables": variables,
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": chosen.get("sha256_hash"),
                }
            },
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://www.bestbuy.com",
            "referer": response.url,
            "user-agent": "Mozilla/5.0",
        }

        yield scrapy.Request(
            endpoint,
            method="POST",
            body=json.dumps(body, separators=(",", ":")),
            headers=headers,
            callback=self.parse_graphql,
            meta=self.maybe_proxy_meta(
                {
                    "query": self.args.q,
                    "page": page,
                    "graphql_endpoint": endpoint,
                    "operation_name": chosen.get("operation_name"),
                    "sha256_hash": chosen.get("sha256_hash"),
                }
            ),
            dont_filter=True,
        )

    def parse_graphql(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        query = response.meta.get("query")

        if response.status != 200:
            self.logger.warning("BestBuy GraphQL non-200 status=%s body=%r", response.status, (response.text or "")[:260])
            return

        try:
            payload = json.loads(response.text)
        except Exception:
            self.logger.warning("BestBuy GraphQL invalid JSON body=%r", (response.text or "")[:260])
            return

        if isinstance(payload, list):
            payload = payload[0] if payload else {}

        if isinstance(payload, dict) and payload.get("errors"):
            self.logger.warning("BestBuy GraphQL errors=%s", payload.get("errors"))

        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            self.logger.warning("BestBuy GraphQL missing data keys=%s", list(payload.keys()) if isinstance(payload, dict) else type(payload))
            return

        emitted = 0
        for rec in self._walk_listing_like(data):
            emitted += 1
            rec.update(
                {
                    "source": "bestbuy_graphql",
                    "mode": "keyword",
                    "query": query,
                    "page": page,
                    "graphql_operation": response.meta.get("operation_name"),
                    "graphql_endpoint": response.meta.get("graphql_endpoint"),
                }
            )
            yield rec

        if emitted == 0:
            self.logger.warning("BestBuy GraphQL returned 0 listing-like records for operation=%s", response.meta.get("operation_name"))

        if page >= self.args.max_pages:
            return

        # Replay with page+1 by requesting search page with _page hint and rediscovering persisted query.
        next_page = page + 1
        next_url = self._build_search_url(query or "", page=next_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse_search_page,
            meta=self.maybe_proxy_meta({"page": next_page, "original_url": next_url}),
            dont_filter=True,
        )

    @staticmethod
    def _build_search_url(q: str, page: int = 1) -> str:
        params = {"st": q}
        if page > 1:
            params["cp"] = str(page)
        return f"https://www.bestbuy.com/site/searchpage.jsp?{urlencode(params)}"

    @staticmethod
    def _extract_graphql_endpoint(html: str) -> str | None:
        h = html or ""
        patterns = [
            r'"clientUrl"\s*:\s*"(?P<u>/gateway/graphql[^\"]*)"',
            r'"egpUrl"\s*:\s*"(?P<u>https://www\.bestbuy\.com/gateway/graphql[^\"]*)"',
            r'"endpoint"\s*:\s*"(?P<u>https://[^\"]+/gateway/graphql[^\"]*)"',
        ]
        for p in patterns:
            m = re.search(p, h, flags=re.I)
            if m:
                u = (m.group("u") or "").replace("\\/", "/")
                if u.startswith("/"):
                    return f"https://www.bestbuy.com{u}"
                return u
        return None

    @staticmethod
    def _extract_persisted_queries(html: str) -> list[dict[str, Any]]:
        h = (html or "").replace("\\/", "/")
        out: list[dict[str, Any]] = []

        # Pattern where operation + hash + optional variables are all visible in one object-ish blob.
        p = re.compile(
            r'operationName"\s*:\s*"(?P<op>[A-Za-z0-9_\-]+)".{0,1200}?sha256Hash"\s*:\s*"(?P<hash>[a-f0-9]{64})".{0,2000}?(?:variables"\s*:\s*(?P<vars>\{.*?\}))?',
            flags=re.I | re.S,
        )

        for m in p.finditer(h):
            op = m.group("op")
            sh = m.group("hash")
            vars_obj = BestbuySearchSpider._safe_json_obj(m.group("vars")) if m.group("vars") else {}
            out.append({"operation_name": op, "sha256_hash": sh, "variables": vars_obj})

        # Dedup by operation+hash
        dedup: dict[tuple[str, str], dict[str, Any]] = {}
        for c in out:
            key = (c.get("operation_name") or "", c.get("sha256_hash") or "")
            if key not in dedup:
                dedup[key] = c
        return list(dedup.values())

    @staticmethod
    def _safe_json_obj(s: str | None) -> dict[str, Any]:
        if not s:
            return {}
        try:
            obj = json.loads(s)
            return obj if isinstance(obj, dict) else {}
        except Exception:
            return {}

    @staticmethod
    def _patch_variables(variables: dict[str, Any], *, query: str | None, page: int) -> dict[str, Any]:
        # Best effort variable patching; works when runtime embeds default vars.
        v = json.loads(json.dumps(variables or {}))
        q = query or ""

        # Common names for keyword term
        for key in ["query", "searchTerm", "search", "keyword", "term", "q", "queryText"]:
            if key in v and isinstance(v.get(key), str):
                v[key] = q

        # Common nested shapes
        for parent in ["input", "request", "params", "searchInput"]:
            node = v.get(parent)
            if isinstance(node, dict):
                for key in ["query", "search", "searchTerm", "keyword", "term", "q"]:
                    if key in node and isinstance(node.get(key), str):
                        node[key] = q

                # page / offset hints
                if "page" in node and isinstance(node.get("page"), (int, float, str)):
                    node["page"] = page
                if "currentPage" in node and isinstance(node.get("currentPage"), (int, float, str)):
                    node["currentPage"] = page
                if "offset" in node and isinstance(node.get("offset"), (int, float, str)):
                    try:
                        per_page = int(node.get("limit") or node.get("pageSize") or 24)
                    except Exception:
                        per_page = 24
                    node["offset"] = max(0, (page - 1) * per_page)

        # Root-level page args
        if "page" in v and isinstance(v.get("page"), (int, float, str)):
            v["page"] = page
        if "currentPage" in v and isinstance(v.get("currentPage"), (int, float, str)):
            v["currentPage"] = page

        return v

    def _walk_listing_like(self, node: Any):
        if isinstance(node, dict):
            if self._looks_like_listing(node):
                item = self._normalize_listing(node)
                if item.get("title") and (item.get("item_id") or item.get("url")):
                    yield item
            for val in node.values():
                yield from self._walk_listing_like(val)
        elif isinstance(node, list):
            for val in node:
                yield from self._walk_listing_like(val)

    @staticmethod
    def _looks_like_listing(d: dict[str, Any]) -> bool:
        keys = {k.lower() for k in d.keys()}
        has_title = any(k in keys for k in ["name", "title", "shortname", "displayname"])
        has_id = any(k in keys for k in ["sku", "skuid", "id", "productid", "itemid"])
        has_url = any(k in keys for k in ["url", "canonicalurl", "path"])
        has_price = any(k in keys for k in ["price", "currentprice", "saleprice", "regularprice"])
        return has_title and (has_id or has_url) and has_price

    @staticmethod
    def _normalize_listing(d: dict[str, Any]) -> dict[str, Any]:
        title = d.get("name") or d.get("title") or d.get("shortName") or d.get("displayName")
        item_id = d.get("sku") or d.get("skuId") or d.get("id") or d.get("productId") or d.get("itemId")

        url = d.get("url") or d.get("canonicalUrl") or d.get("path")
        if isinstance(url, str) and url.startswith("/"):
            url = f"https://www.bestbuy.com{url}"

        price = None
        currency = None
        for key in ["currentPrice", "salePrice", "price", "regularPrice"]:
            if key not in d:
                continue
            raw = d.get(key)
            if isinstance(raw, dict):
                price = raw.get("value") or raw.get("amount") or raw.get("price")
                currency = raw.get("currency") or raw.get("currencyCode")
            else:
                price = raw
            if price is not None:
                break

        image_url = d.get("image") or d.get("imageUrl") or d.get("thumbnail")
        if isinstance(image_url, dict):
            image_url = image_url.get("url")

        return {
            "item_id": str(item_id) if item_id is not None else None,
            "title": title,
            "url": url,
            "brand": d.get("brand") or d.get("manufacturer"),
            "price": price,
            "currency": currency,
            "rating": d.get("rating") or d.get("averageRating"),
            "reviews_count": d.get("reviewCount") or d.get("numberOfReviews"),
            "image_url": image_url,
            "raw": d,
        }
