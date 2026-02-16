from __future__ import annotations

"""Best Buy category/listing spider using discovered GraphQL persisted queries.

Usage:
  scrapy crawl bestbuy_listing -a category_url='https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000' -a max_pages=1 -a use_proxy=1
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.bestbuy_search_spider import BestbuySearchSpider


class BestbuyListingSpider(BaseListingSpider):
    name = "bestbuy_listing"
    allowed_domains = ["bestbuy.com", "www.bestbuy.com", "bifrostgw.us.bestbuy.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(
        self,
        category_url: str | None = None,
        url: str | None = None,
        max_pages: int = 1,
        use_proxy: int | str | None = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.init_listing_args(max_pages=max_pages, use_proxy=use_proxy, url=url, category_url=category_url)

        self.category_url = self.args.category_url
        self.url = self.args.url
        if not (self.category_url or self.url):
            raise ValueError("Provide -a category_url=<url> (or -a url=<url>)")

    def start_requests(self):
        target = self.url or self.category_url or ""
        target = self._with_page(target, 1)
        yield scrapy.Request(target, callback=self.parse_listing_page, meta=self.maybe_proxy_meta({"page": 1, "original_url": target}))

    def parse_listing_page(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        html = response.text or ""

        endpoint = BestbuySearchSpider._extract_graphql_endpoint(html) or "https://www.bestbuy.com/gateway/graphql"
        candidates = BestbuySearchSpider._extract_persisted_queries(html)
        if not candidates:
            self.logger.warning("No GraphQL persisted-query candidates found for listing page=%s", page)
            return

        ranked = sorted(
            candidates,
            key=lambda c: (
                0 if any(x in (c.get("operation_name") or "").lower() for x in ["product", "list", "plp", "browse", "search"]) else 1,
                0 if c.get("variables") else 1,
            ),
        )
        chosen = ranked[0]

        vars_obj = BestbuySearchSpider._patch_variables(chosen.get("variables") or {}, query=None, page=page)

        body = {
            "operationName": chosen.get("operation_name"),
            "variables": vars_obj,
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
            body=__import__("json").dumps(body, separators=(",", ":")),
            headers=headers,
            callback=self.parse_graphql,
            meta=self.maybe_proxy_meta(
                {
                    "page": page,
                    "graphql_endpoint": endpoint,
                    "operation_name": chosen.get("operation_name"),
                    "category_url": self.category_url or self.url,
                    "original_url": response.meta.get("original_url") or response.url,
                }
            ),
            dont_filter=True,
        )

    def parse_graphql(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        category_url = response.meta.get("category_url")

        if response.status != 200:
            self.logger.warning("BestBuy listing GraphQL non-200 status=%s body=%r", response.status, (response.text or "")[:260])
            return

        try:
            payload = response.json()
        except Exception:
            self.logger.warning("BestBuy listing GraphQL invalid JSON body=%r", (response.text or "")[:260])
            return

        if isinstance(payload, list):
            payload = payload[0] if payload else {}

        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            self.logger.warning("BestBuy listing GraphQL missing data keys=%s", list(payload.keys()) if isinstance(payload, dict) else type(payload))
            return

        emitted = 0
        for rec in BestbuySearchSpider._walk_listing_like(self, data):
            emitted += 1
            rec.update(
                {
                    "source": "bestbuy_graphql",
                    "mode": "category",
                    "category_url": category_url,
                    "page": page,
                    "graphql_operation": response.meta.get("operation_name"),
                    "graphql_endpoint": response.meta.get("graphql_endpoint"),
                }
            )
            yield rec

        if emitted == 0:
            self.logger.warning("BestBuy listing GraphQL returned 0 listing-like records")

        if page >= self.args.max_pages:
            return

        next_page = page + 1
        original = response.meta.get("original_url") or (self.url or self.category_url or "")
        next_url = self._with_page(original, next_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse_listing_page,
            meta=self.maybe_proxy_meta({"page": next_page, "original_url": next_url}),
            dont_filter=True,
        )

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["cp"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
