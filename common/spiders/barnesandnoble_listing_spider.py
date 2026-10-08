from __future__ import annotations

"""Barnes & Noble products from its first-party Shopify Storefront API."""

import json
import re

import scrapy

from common.spiders.barnesandnoble_categories import BARNESANDNOBLE_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


PRODUCTS_QUERY = """
query Products($first: Int!, $query: String!, $after: String) {
  products(first: $first, query: $query, after: $after) {
    nodes {
      id title handle description vendor productType availableForSale
      createdAt updatedAt publishedAt tags onlineStoreUrl
      featuredImage { url altText width height }
      images(first: 10) { nodes { url altText width height } }
      options { name values }
      priceRange {
        minVariantPrice { amount currencyCode }
        maxVariantPrice { amount currencyCode }
      }
      compareAtPriceRange {
        minVariantPrice { amount currencyCode }
        maxVariantPrice { amount currencyCode }
      }
      variants(first: 20) {
        nodes {
          id title sku availableForSale
          price { amount currencyCode }
          compareAtPrice { amount currencyCode }
          image { url altText width height }
          selectedOptions { name value }
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


class BarnesandnobleListingSpider(BaseListingSpider):
    """Discover rotating credentials, then extract products only via GraphQL."""

    name = "barnesandnoble_listing"
    allowed_domains = [
        "barnesandnoble.com", "www.barnesandnoble.com", "myshopify.com",
        "e9c22f-3.myshopify.com",
    ]
    categories = BARNESANDNOBLE_CATEGORIES
    page_size = 50

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        # Both the Oxygen storefront and Shopify API are directly reachable;
        # a proxy tunnel strips the Storefront POST body in this environment.
        "PROXY": "",
        "FEED_EXPORT_FIELDS": [
            "category", "search_query", "item_id", "variant_id", "ean",
            "title", "handle", "description", "vendor", "format", "url",
            "image_url", "image_alt", "images", "price", "min_price",
            "max_price", "compare_price", "currency", "available", "tags",
            "options", "variants", "created_at", "updated_at", "published_at",
            "page", "position", "source_url", "source", "raw", "timestamp",
        ],
    }
    _challenge_markers = ("captcha", "access denied", "robot or human", "cloudflare")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        selected = next((x for x in self.categories if x["url"] == target), {})
        query = selected.get("search_query") or (self.category or "").replace("-", " ")
        yield scrapy.Request(
            target, callback=self.parse_bootstrap, headers=self._storefront_headers(),
            meta={"category": selected.get("category") or self.category or "custom", "search_query": query},
        )

    def parse_bootstrap(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Barnes & Noble bootstrap returned HTTP {response.status}: {response.url}")
        lowered = response.text[:300000].lower()
        if any(marker in lowered for marker in self._challenge_markers):
            raise RuntimeError(f"Barnes & Noble challenge page returned at {response.url}")
        domain = self._bootstrap_value(response.text, "publicStoreDomain")
        version = self._bootstrap_value(response.text, "publicStorefrontApiVersion")
        token = self._bootstrap_value(response.text, "storefrontAccessToken")
        if not (domain and version and token):
            raise RuntimeError(f"Barnes & Noble Storefront API bootstrap is missing at {response.url}")
        if not domain.endswith(".myshopify.com"):
            raise RuntimeError(f"Unexpected Barnes & Noble Storefront API domain: {domain}")
        meta = {**response.meta, "api_url": f"https://{domain}/api/{version}/graphql.json", "token": token}
        yield self._api_request(after=None, page=1, meta=meta)

    def _api_request(self, *, after, page: int, meta: dict):
        body = json.dumps({
            "query": PRODUCTS_QUERY,
            "variables": {"first": self.page_size, "query": meta["search_query"], "after": after},
        })
        return scrapy.Request(
            meta["api_url"], method="POST", body=body, callback=self.parse_api,
            headers={
                "accept": "application/json", "content-type": "application/json",
                "origin": "https://www.barnesandnoble.com",
                "referer": "https://www.barnesandnoble.com/",
                "x-shopify-storefront-access-token": meta["token"],
            },
            # The storefront accepts direct requests. Keeping the collection
            # proxy tunnel on this second host can trigger a proxy-side 407.
            meta={
                key: meta[key]
                for key in ("category", "search_query", "api_url", "token")
            } | {"page": page, "disable_proxy": True},
            dont_filter=True,
        )

    def parse_api(self, response: scrapy.http.Response):
        payload = self._api_payload(response)
        if payload.get("errors"):
            raise RuntimeError(f"Barnes & Noble Storefront API GraphQL errors: {payload['errors']!r}")
        products = ((payload.get("data") or {}).get("products") or {})
        nodes = products.get("nodes")
        if not isinstance(nodes, list):
            raise RuntimeError(f"Barnes & Noble Storefront API returned no products array: {response.url}")
        page = int(response.meta["page"])
        if page == 1 and not nodes:
            raise RuntimeError(f"Barnes & Noble Storefront API returned an empty first page: {response.url}")
        emitted = 0
        for position, product in enumerate(nodes, start=1):
            if not isinstance(product, dict):
                continue
            item_id = self._gid(product.get("id"))
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(product, response, page, position, item_id)
        page_info = products.get("pageInfo") or {}
        cursor = page_info.get("endCursor")
        if page < self.max_pages and emitted and page_info.get("hasNextPage") and cursor:
            yield self._api_request(after=cursor, page=page + 1, meta=response.meta)

    def _item(self, product, response, page, position, item_id):
        variants = ((product.get("variants") or {}).get("nodes") or [])
        first = variants[0] if variants and isinstance(variants[0], dict) else {}
        price_range = product.get("priceRange") or {}
        compare_range = product.get("compareAtPriceRange") or {}
        minimum = price_range.get("minVariantPrice") or {}
        maximum = price_range.get("maxVariantPrice") or {}
        compare = compare_range.get("maxVariantPrice") or {}
        featured = product.get("featuredImage") or {}
        images = ((product.get("images") or {}).get("nodes") or [])
        price = self._number((first.get("price") or {}).get("amount"))
        compare_price = self._number((first.get("compareAtPrice") or {}).get("amount"))
        if not compare_price:
            compare_price = self._number(compare.get("amount"))
        return {
            "category": response.meta["category"], "search_query": response.meta["search_query"],
            "item_id": item_id, "variant_id": self._gid(first.get("id")),
            "ean": first.get("sku") or product.get("handle"), "title": product.get("title"),
            "handle": product.get("handle"), "description": product.get("description"),
            "vendor": product.get("vendor"), "format": product.get("productType"),
            "url": product.get("onlineStoreUrl"), "image_url": featured.get("url"),
            "image_alt": featured.get("altText"), "images": images,
            "price": price if price is not None else self._number(minimum.get("amount")),
            "min_price": self._number(minimum.get("amount")),
            "max_price": self._number(maximum.get("amount")), "compare_price": compare_price,
            "currency": (first.get("price") or {}).get("currencyCode") or minimum.get("currencyCode"),
            "available": bool(product.get("availableForSale")), "tags": product.get("tags") or [],
            "options": product.get("options") or [], "variants": variants,
            "created_at": product.get("createdAt"), "updated_at": product.get("updatedAt"),
            "published_at": product.get("publishedAt"), "page": page, "position": position,
            "source_url": response.url, "source": "barnesandnoble_storefront_graphql_api",
            "raw": product, "timestamp": self.job_timestamp,
        }

    @staticmethod
    def _bootstrap_value(document: str, key: str):
        for pattern in (
            rf'"{re.escape(key)}"\s*:\s*"([^"\\]+)',
            rf'{re.escape(key)}\\",\\"([^"\\]+)',
        ):
            match = re.search(pattern, document)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def _api_payload(response):
        if response.status != 200:
            raise RuntimeError(f"Barnes & Noble Storefront API returned HTTP {response.status}: {response.url}")
        try:
            payload = json.loads(response.text)
        except ValueError as exc:
            raise RuntimeError(f"Barnes & Noble Storefront API returned non-JSON: {response.url}") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"Barnes & Noble Storefront API returned a non-object: {response.url}")
        return payload

    @staticmethod
    def _gid(value):
        return str(value).rsplit("/", 1)[-1] if value else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _storefront_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
