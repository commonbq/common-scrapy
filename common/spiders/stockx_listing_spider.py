from __future__ import annotations

"""StockX category spider backed by the page's Next.js browse state."""

import json
from collections.abc import Iterable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


STOCKX_CATEGORIES = {
    "sneakers": {"all": "https://stockx.com/sneakers"},
    "apparel": {"all": "https://stockx.com/apparel"},
    "electronics": {"all": "https://stockx.com/electronics"},
    "trading-cards": {"all": "https://stockx.com/trading-cards"},
    "collectibles": {"all": "https://stockx.com/collectibles"},
}


class StockxListingSpider(BaseListingSpider):
    name = "stockx_listing"
    allowed_domains = ["stockx.com", "www.stockx.com"]
    categories = STOCKX_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "brand",
            "price",
            "highest_bid",
            "last_sale_price",
            "currency",
            "url",
            "image_url",
            "product_category",
            "category",
            "subcategory",
            "page",
            "source",
            "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def start_requests(self) -> Iterable[scrapy.Request]:
        if self.url or self.category_url:
            url = self.url or self.category_url
            yield self._request(url, self.category or "custom", "custom", 1)
            return

        if self.category not in self.categories:
            available = ", ".join(self.available_categories())
            raise ValueError(
                f"Unknown category '{self.category}'. Available categories: {available}"
            )

        for subcategory, url in self.categories[self.category].items():
            yield self._request(url, self.category, subcategory, 1)

    def _request(self, url: str, category: str, subcategory: str, page: int):
        return scrapy.Request(
            self._with_page(url, page),
            callback=self.parse,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
                ),
            },
            meta={
                "category": category,
                "subcategory": subcategory,
                "page": page,
                "listing_url": url,
                "handle_httpstatus_all": True,
            },
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        script = response.css("script#__NEXT_DATA__::text").get()
        if response.status != 200 and not script:
            self.logger.error(
                "StockX listing request failed without browse state: status=%s url=%s",
                response.status,
                response.url,
            )
            return
        if not script:
            self.logger.error(
                "StockX response has no __NEXT_DATA__ browse state; refusing fallback parsing"
            )
            return
        if response.status != 200:
            self.logger.warning(
                "StockX returned status=%s but included a usable Next.js browse state",
                response.status,
            )

        try:
            state = json.loads(script)
            browse = self._find_browse_query(state)
        except (json.JSONDecodeError, TypeError, KeyError):
            self.logger.exception("Could not parse StockX Next.js browse state")
            return

        if not browse:
            self.logger.error("StockX __NEXT_DATA__ contains no authoritative browse result")
            return

        edges = browse.get("results", {}).get("edges") or []
        for edge in edges:
            node = edge.get("node") or {}
            product = node.get("product") or node
            item_id = product.get("id") or product.get("uuid")
            slug = product.get("urlKey")
            if not item_id or not slug or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)

            market = product.get("market") or node.get("market") or {}
            market_state = market.get("state") or {}
            statistics = market.get("statistics") or {}
            media = product.get("media") or {}
            yield {
                "item_id": item_id,
                "title": product.get("title"),
                "brand": product.get("brand"),
                "price": self._amount(market_state.get("lowestAsk")),
                "highest_bid": self._amount(market_state.get("highestBid")),
                "last_sale_price": self._amount(statistics.get("lastSale")),
                "currency": "USD",
                "url": f"https://stockx.com/{slug}",
                "image_url": media.get("smallImageUrl") or media.get("thumbUrl"),
                "product_category": product.get("productCategory"),
                "category": response.meta["category"],
                "subcategory": response.meta["subcategory"],
                "page": page,
                "source": "stockx_next_data_browse",
                "raw": product,
            }

        page_info = browse.get("results", {}).get("pageInfo") or {}
        page_count = int(page_info.get("pageCount") or page)
        if page < min(self.max_pages, page_count):
            yield self._request(
                response.meta["listing_url"],
                response.meta["category"],
                response.meta["subcategory"],
                page + 1,
            )

    @staticmethod
    def _find_browse_query(state: dict) -> dict | None:
        queries = (
            state.get("props", {})
            .get("pageProps", {})
            .get("req", {})
            .get("appContext", {})
            .get("states", {})
            .get("query", {})
            .get("value", {})
            .get("queries", [])
        )
        for query in queries:
            browse = query.get("state", {}).get("data", {}).get("browse")
            if isinstance(browse, dict) and isinstance(browse.get("results"), dict):
                return browse
        return None

    @staticmethod
    def _amount(value):
        return value.get("amount") if isinstance(value, dict) else None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        query = parse_qs(parts.query)
        if page > 1:
            query["page"] = [str(page)]
        else:
            query.pop("page", None)
        return urlunparse(parts._replace(query=urlencode(query, doseq=True)))
