from __future__ import annotations

"""Walgreens listing spider using only the page's Redux bootstrap state."""

import json
import re
from typing import Any, Iterable
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.walgreens_categories import WALGREENS_CATEGORIES

SITE = "https://www.walgreens.com"
STATE_RE = re.compile(r"window\.getInitialState\s*=\s*function\s*\([^)]*\)\s*\{\s*return\s*", re.S)
CHALLENGE_MARKERS = ("bm-verify", "/_sec/verify", "akamai")


class WalgreensListingSpider(BaseListingSpider):
    name = "walgreens_listing"
    allowed_domains = ["walgreens.com", "www.walgreens.com"]
    require_category_arg = False
    categories = WALGREENS_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_id", "product_id", "sku_id", "article_id",
            "upc", "title", "brand", "url", "image", "price",
            "regular_price", "sale_price", "currency", "rating",
            "reviews_count", "inventory_status", "page", "position",
            "total_count", "total_pages", "source_url", "raw",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/149.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError("Provide category, category_url, or url")
        self.resolve_target_url()
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, listing_url: str, page: int) -> scrapy.Request:
        category_id = self._category_id(listing_url)
        url = f"{SITE}/store/c/productlist/N={category_id}/{page}/ShopAll={category_id}"
        meta = {}
        proxy = self._render_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            url,
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"listing_url": listing_url, "page": page},
            dont_filter=True,
            meta=meta,
        )

    def _render_proxy(self) -> str | None:
        """Ask ScrapeOps to render JS without embedding or copying credentials."""
        proxy = self.settings.get("PROXY") if hasattr(self, "settings") else None
        if not isinstance(proxy, str) or not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return proxy
        username = unquote(parts.username)
        for option in ("render_js=true", "country=us"):
            if option not in username.split("."):
                username += f".{option}"
        auth = quote(username, safe=".=")
        if parts.password is not None:
            auth += ":" + quote(unquote(parts.password), safe="")
        host = parts.hostname + (f":{parts.port}" if parts.port else "")
        return urlunsplit((parts.scheme, f"{auth}@{host}", parts.path, parts.query, parts.fragment))

    def parse(self, response: scrapy.http.Response, listing_url: str, page: int):
        if response.status != 200:
            raise RuntimeError(f"Walgreens returned HTTP {response.status}: {response.url}")
        state = self._extract_state(response.text, response.url)
        search = state.get("searchResult")
        if not isinstance(search, dict):
            raise RuntimeError(f"Walgreens state has no searchResult at {response.url}")
        rows = search.get("productList")
        if not isinstance(rows, list):
            raise RuntimeError(f"Walgreens searchResult has no productList at {response.url}")
        summary = search.get("summary") if isinstance(search.get("summary"), dict) else {}
        total = self._int(summary.get("productInfoCount") or summary.get("allProductTotalResults"))
        total_pages = self._int(summary.get("totalNumPages"))
        category_id = self._category_id(listing_url)
        emitted = 0
        for position, row in enumerate(rows, 1):
            if not isinstance(row, dict):
                continue
            product = row.get("productInfo")
            if not isinstance(product, dict):
                continue
            item = self._item(product, category_id, response, page, position, total, total_pages)
            if item:
                emitted += 1
                yield item
        if not rows or not emitted or page >= self.max_pages:
            return
        if total_pages is not None and page >= total_pages:
            return
        yield self._request(listing_url, page + 1)

    @staticmethod
    def _extract_state(text: str, url: str) -> dict[str, Any]:
        match = STATE_RE.search(text)
        if not match:
            lowered = text.lower()
            kind = "Akamai challenge" if any(x in lowered for x in CHALLENGE_MARKERS) else "missing hydration"
            raise RuntimeError(f"Walgreens {kind} at {url}; expected window.getInitialState bootstrap")
        try:
            state, _ = json.JSONDecoder().raw_decode(text[match.end():].lstrip())
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid Walgreens bootstrap JSON at {url}: {exc}") from exc
        if not isinstance(state, dict):
            raise RuntimeError(f"Walgreens bootstrap is not an object at {url}")
        return state

    def _item(self, product, category_id, response, page, position, total, total_pages):
        product_id = self._text(product.get("prodId") or product.get("productId"))
        if not product_id or product_id in self._seen:
            return None
        self._seen.add(product_id)
        price_info = product.get("priceInfo") if isinstance(product.get("priceInfo"), dict) else {}
        sale = self._money(price_info.get("salePrice") or price_info.get("singleUnitSalePrice"))
        regular = self._money(price_info.get("regularPrice"))
        return {
            "category": self.category,
            "category_id": category_id,
            "product_id": product_id,
            "sku_id": self._text(product.get("skuId")),
            "article_id": self._text(product.get("articleId")),
            "upc": self._text(product.get("upc")),
            "title": self._text(product.get("productDisplayName") or product.get("productName")),
            "brand": self._text(
                product.get("brandName")
                or product.get("subBrandName")
                or product.get("beautyCategoryName")
                or product.get("brand")
            ),
            "url": urljoin(SITE, self._text(product.get("productURL")) or ""),
            "image": urljoin("https:", self._text(product.get("imageUrl450") or product.get("imageUrl")) or ""),
            "price": sale if sale is not None else regular,
            "regular_price": regular,
            "sale_price": sale,
            "currency": "USD",
            "rating": self._number(product.get("averageRating")),
            "reviews_count": self._int(product.get("reviewCount")),
            "inventory_status": self._text(product.get("onlineInvStatus")),
            "page": page,
            "position": position,
            "total_count": total,
            "total_pages": total_pages,
            "source_url": response.url,
            "raw": product,
        }

    @staticmethod
    def _category_id(url: str) -> str:
        match = re.search(r"(?:ID=|N=|ShopAll=)(\d+)", url)
        if not match:
            raise ValueError(f"Cannot determine Walgreens category ID from {url}")
        return match.group(1)

    @staticmethod
    def _text(value):
        return str(value).strip() if value is not None and str(value).strip() else None

    @staticmethod
    def _int(value):
        try:
            return int(str(value).replace(",", ""))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _number(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def _money(cls, value):
        text = cls._text(value)
        if not text:
            return None
        match = re.search(r"-?\d[\d,]*(?:\.\d+)?", text)
        return float(match.group().replace(",", "")) if match else None
