from __future__ import annotations

"""Chewy listings from the server-rendered Next.js bootstrap state."""

import json
import re
from urllib.parse import parse_qs, quote, unquote, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider, group_categories
from common.spiders.chewy_categories import CHEWY_CATEGORIES


class ChewyListingSpider(BaseListingSpider):
    name = "chewy_listing"
    allowed_domains = ["chewy.com", "www.chewy.com"]
    categories = group_categories(CHEWY_CATEGORIES, "department")
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "part_number", "title", "brand", "manufacturer",
            "url", "image", "display_price", "price", "list_price", "autoship_price",
            "currency", "rating", "reviews_count", "is_ad", "page", "position",
            "total_count", "source_url", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url, page):
        meta = {"category": self.category or "custom", "page": page, "base_url": base_url}
        proxy = self._residential_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta=meta,
        )

    def _residential_proxy(self):
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return proxy
        username = unquote(parts.username)
        for option in ("residential=true", "country=us"):
            if option not in username.split("."):
                username += "." + option
        auth = quote(username, safe=".=")
        if parts.password is not None:
            auth += ":" + quote(unquote(parts.password), safe="")
        host = parts.hostname + (f":{parts.port}" if parts.port else "")
        return urlunsplit((parts.scheme, f"{auth}@{host}", parts.path, parts.query, parts.fragment))

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Chewy listing returned HTTP {response.status}: {response.url}")
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Chewy response has no __NEXT_DATA__ hydration: {response.url}")
        try:
            state = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Chewy __NEXT_DATA__ hydration is malformed: {response.url}") from exc
        plp = (((((state.get("props") or {}).get("pageProps") or {}).get("initialState") or {})
                .get("searchSlice") or {}).get("plpData"))
        if not isinstance(plp, dict) or not isinstance(plp.get("products"), list):
            raise RuntimeError(f"Chewy hydration has no searchSlice.plpData.products: {response.url}")

        products = plp["products"]
        page = int(response.meta.get("page", 1))
        new_ids = 0
        for position, product in enumerate(products, 1):
            if not isinstance(product, dict):
                continue
            item_id = product.get("catalogEntryId") or product.get("partNumber")
            title, href = product.get("name"), product.get("href")
            if not item_id or not title or not href or str(item_id) in self._seen:
                continue
            self._seen.add(str(item_id))
            new_ids += 1
            yield self._item(product, response, plp, page, position)

        total = self._integer(plp.get("recordSetTotal"))
        if page < self.max_pages and new_ids and (total is None or len(self._seen) < total):
            yield self._request(response.meta["base_url"], page + 1)

    def _item(self, product, response, plp, page, position):
        image = product.get("image") or product.get("imageUrl") or product.get("primaryImage")
        if isinstance(image, dict):
            image = image.get("url") or image.get("src")
        return {
            "category": response.meta.get("category"),
            "item_id": str(product.get("catalogEntryId") or product.get("partNumber")),
            "part_number": str(product.get("partNumber")) if product.get("partNumber") is not None else None,
            "title": product.get("name"),
            "brand": product.get("manufacturer") or product.get("brand"),
            "manufacturer": product.get("manufacturer"),
            "url": self._product_url(product.get("href")),
            "image": image,
            "display_price": product.get("displayPrice"),
            "price": self._number(product.get("advertisedPrice") or product.get("price")),
            "list_price": self._number(product.get("strikePrice") or product.get("listPrice")),
            "autoship_price": self._number(product.get("autoshipPrice") or product.get("autoshipAdvertisedPrice")),
            "currency": "USD",
            "rating": self._number(product.get("rating")),
            "reviews_count": self._integer(product.get("ratingCount") or product.get("reviewCount")),
            "is_ad": bool(product.get("isAd")),
            "page": page,
            "position": position,
            "total_count": self._integer(plp.get("recordSetTotal")),
            "source_url": response.url,
            "source": "chewy_next_data_bootstrap",
            "raw": product,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _page_url(url, page):
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = dict(parse_qs(parts.query))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query, doseq=True), ""))

    @staticmethod
    def _product_url(href):
        url = urljoin("https://www.chewy.com/", href)
        redirect = parse_qs(urlsplit(url).query).get("redirect", [None])[0]
        return urljoin("https://www.chewy.com/", redirect) if redirect else url

    @staticmethod
    def _number(value):
        if value is None or isinstance(value, bool):
            return None
        match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value))
        return float(match.group(0).replace(",", "")) if match else None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None
