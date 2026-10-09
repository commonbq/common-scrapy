from __future__ import annotations

import json
import re
from urllib.parse import urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.adidas_categories import ADIDAS_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider, group_categories

# `translations["currency.symbol"]` is a template placeholder ("${0}"), so the ISO
# code is derived from the locale adidas ships in the same hydration payload.
_LOCALE_CURRENCY = {"US": "USD", "GB": "GBP", "DE": "EUR", "FR": "EUR"}


class AdidasListingSpider(BaseListingSpider):
    """adidas listings from the server-rendered Next.js `__NEXT_DATA__` hydration."""

    name = "adidas_listing"
    allowed_domains = ["adidas.com", "www.adidas.com", "localhost", "127.0.0.1"]
    categories = group_categories(ADIDAS_CATEGORIES, "department")
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "item_id", "style_id", "title",
            "brand", "product_category", "colorway_count", "colorway_ids", "url",
            "image_url", "hover_image_url", "price", "original_price",
            "discount_percentage", "currency", "rating", "reviews_count", "on_sale",
            "sold_out", "badges", "page", "position", "total_count", "source_url",
            "source", "raw",
            "timestamp",
        ],
    }

    _hydration = re.compile(r'<script id="__NEXT_DATA__" type="application/json"[^>]*>')

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
        selected = next((entry for entry in self.iter_categories() if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
            },
            meta={
                "category": self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "page": 1,
                "start": 0,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"adidas listing returned HTTP {response.status}: {response.url}")
        page_props = self._page_props(response.text, response.url)
        page = int(response.meta.get("page", 1))
        start = int(response.meta.get("start", 0))

        # A request past the last window comes back as pageType "ERROR" with info=null.
        page_type = page_props.get("pageType")
        if page_type != "ProductListingPage":
            if page > 1:
                self.logger.info("Stopping at %s: pageType=%r", response.url, page_type)
                return
            raise RuntimeError(
                f"adidas {response.url} is not a ProductListingPage (pageType={page_type!r})"
            )

        info = page_props.get("info")
        info = info if isinstance(info, dict) else {}
        view_size = self._integer(info.get("viewSize")) or 48
        total_count = self._integer(info.get("count"))
        products = page_props.get("products")
        if not isinstance(products, list):
            raise RuntimeError(f"adidas hydration has no list-valued products at {response.url}")

        currency = self._currency(page_props)
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("id") or "") or None
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, response, page, position, total_count, currency)

        if not products:
            return
        next_start = start + view_size
        if total_count is None or next_start >= total_count:
            return
        if page >= self.max_pages:
            return
        yield scrapy.Request(
            self._with_start(response.url, next_start),
            callback=self.parse,
            headers=response.request.headers,
            meta={**response.meta, "page": page + 1, "start": next_start},
            dont_filter=True,
        )

    def _item(
        self,
        product: dict,
        response,
        page: int,
        position: int,
        total_count: int | None,
        currency: str | None,
    ) -> dict:
        price_data = product.get("priceData")
        price_data = price_data if isinstance(price_data, dict) else {}
        prices = price_data.get("prices")
        prices = prices if isinstance(prices, list) else []
        by_type = {
            str(entry.get("type")): entry
            for entry in prices
            if isinstance(entry, dict) and entry.get("value") is not None
        }
        # adidas ships "sale" (current, discounted) alongside "original" (list) price,
        # and hangs a negative `discountPercentage` off the original entry.
        current = by_type.get("sale") or by_type.get("original") or {}
        original = by_type.get("original") if "sale" in by_type else None
        discount = self._integer(original.get("discountPercentage")) if original else None
        colorways = product.get("colourVariations")
        colorways = colorways if isinstance(colorways, list) else []
        badges = product.get("badges")
        badges = [b.get("text") for b in badges if isinstance(b, dict) and b.get("text")] \
            if isinstance(badges, list) else []
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": str(product.get("id") or "") or None,
            "style_id": str(product.get("modelNumber") or "") or None,
            "title": str(product.get("title") or "") or None,
            "brand": str(product.get("subTitle") or "").strip() or None,
            "product_category": str(product.get("category") or "").strip() or None,
            "colorway_count": len(colorways) or None,
            "colorway_ids": ", ".join(str(c) for c in colorways) if colorways else None,
            "url": product.get("url"),
            "image_url": product.get("image"),
            "hover_image_url": product.get("hoverImage"),
            "price": self._number(current.get("value")),
            "original_price": self._number(original.get("value")) if original else None,
            "discount_percentage": abs(discount) if discount is not None else None,
            "currency": currency,
            "rating": self._non_negative_number(product.get("rating")),
            "reviews_count": self._non_negative_integer(product.get("ratingCount")),
            "on_sale": "sale" in by_type,
            "sold_out": bool(price_data.get("isSoldOut")),
            "badges": ", ".join(badges) if badges else None,
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "adidas_next_data_page_props_products",
            "raw": product,
        }

    def _page_props(self, document: str, url: str) -> dict:
        match = self._hydration.search(document or "")
        if not match:
            raise RuntimeError(f"No adidas __NEXT_DATA__ hydration blob found at {url}")
        try:
            state, _ = json.JSONDecoder().raw_decode(document, match.end())
            page_props = state["props"]["pageProps"]
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(
                f"adidas __NEXT_DATA__ at {url} has no props.pageProps object"
            ) from exc
        if not isinstance(page_props, dict):
            raise RuntimeError(f"adidas __NEXT_DATA__ at {url} has a non-object props.pageProps")
        return page_props

    @staticmethod
    def _currency(page_props: dict) -> str | None:
        context = page_props.get("context")
        context = context if isinstance(context, dict) else {}
        locale = str(context.get("locale") or "").upper()
        region = locale.split("_")[-1] if "_" in locale else ""
        return _LOCALE_CURRENCY.get(region)

    @staticmethod
    def _with_start(url: str, start: int) -> str:
        parts = urlsplit(url)
        query = [
            (key, value)
            for key, value in re.findall(r"([^?&]+)=([^&]*)", parts.query)
            if key != "start"
        ]
        if start:
            query.append(("start", str(start)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _non_negative_number(value):
        number = AdidasListingSpider._number(value)
        return number if number is not None and number >= 0 else None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _non_negative_integer(value):
        # adidas uses -99 as a "no reviews yet" sentinel.
        number = AdidasListingSpider._integer(value)
        return number if number is not None and number >= 0 else None
