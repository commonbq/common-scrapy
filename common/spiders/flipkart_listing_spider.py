from __future__ import annotations

"""Flipkart listings from the server-rendered Redux bootstrap only."""

import json
import re
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.flipkart_categories import FLIPKART_CATEGORIES

SITE = "https://www.flipkart.com"
STATE_RE = re.compile(r"window\.__INITIAL_STATE__\s*=\s*", re.S)


class FlipkartListingSpider(BaseListingSpider):
    """Extract product widgets from ``window.__INITIAL_STATE__`` only."""

    name = "flipkart_listing"
    allowed_domains = ["flipkart.com", "www.flipkart.com", "localhost", "127.0.0.1"]
    categories = FLIPKART_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_name", "item_id", "title", "subtitle", "url",
            "image", "price", "was_price", "currency", "discount_pct", "rating",
            "reviews_count", "availability", "page", "position", "total_count",
            "total_pages", "source_url", "source", "raw", "timestamp",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-IN,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            self.category = self.categories[0]["category"]
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        target = self.resolve_target_url()
        entry = next((row for row in self.categories if row["url"].rstrip("/") == target.rstrip("/")), {})
        yield scrapy.Request(
            target,
            headers=self.headers,
            callback=self.parse,
            meta={
                "category": self.category or entry.get("category") or "custom",
                "category_name": entry.get("name"),
                "page": 1,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Flipkart listing returned HTTP {response.status}: {response.url}")
        state = self._extract_state(response.text, response.url)
        data = self._page_data(state, response.url)
        products, pagination, listing = self._widgets(data)
        if not products:
            raise RuntimeError(f"Flipkart bootstrap contains no product widgets at {response.url}")

        page = self._int(pagination.get("currentPage")) or int(response.meta.get("page", 1))
        total_pages = self._int(pagination.get("totalPages"))
        total_count = self._int(listing.get("totalProducts"))
        category_name = self._text(listing.get("title")) or response.meta.get("category_name")

        for position, product_info in enumerate(products, 1):
            item = self._item(product_info, response, page, position, category_name, total_count, total_pages)
            if item:
                yield item

        if page < self.max_pages and (total_pages is None or page < total_pages):
            yield scrapy.Request(
                self._page_url(response.url, page + 1),
                headers=self.headers,
                callback=self.parse,
                meta={**response.meta, "page": page + 1, "category_name": category_name},
                dont_filter=True,
            )

    @classmethod
    def _extract_state(cls, text: str, url: str) -> dict[str, Any]:
        match = STATE_RE.search(text or "")
        if not match:
            raise RuntimeError(f"Flipkart response has no window.__INITIAL_STATE__ bootstrap at {url}")
        try:
            state, _ = json.JSONDecoder().raw_decode(text, match.end())
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid Flipkart bootstrap JSON at {url}: {exc}") from exc
        if not isinstance(state, dict):
            raise RuntimeError(f"Flipkart bootstrap is not an object at {url}")
        return state

    @staticmethod
    def _page_data(state: dict, url: str) -> dict:
        node: Any = state.get("multiWidgetState", state)
        for key in ("pageDataV4", "page", "data"):
            node = node.get(key) if isinstance(node, dict) else None
        if not isinstance(node, dict):
            raise RuntimeError(f"Flipkart bootstrap has no multiWidgetState.pageDataV4.page.data at {url}")
        return node

    @staticmethod
    def _widgets(data: dict) -> tuple[list[dict], dict, dict]:
        products: list[dict] = []
        pagination: dict = {}
        listing: dict = {}
        for group_id, group in data.items():
            rows = group if isinstance(group, list) else [group]
            for row in rows:
                if not isinstance(row, dict):
                    continue
                widget = row.get("widget") if isinstance(row.get("widget"), dict) else row
                payload = widget.get("data") if isinstance(widget.get("data"), dict) else {}
                if str(group_id) == "10004" and payload.get("totalProducts") is not None:
                    listing = payload
                if payload.get("currentPage") is not None:
                    pagination = payload
                values = payload.get("products")
                if isinstance(values, list):
                    for value in values:
                        if isinstance(value, dict) and isinstance(value.get("productInfo"), dict):
                            products.append(value["productInfo"])
        return products, pagination, listing

    def _item(self, product_info, response, page, position, category_name, total_count, total_pages):
        value = product_info.get("value") if isinstance(product_info.get("value"), dict) else product_info
        item_id = self._text(value.get("id") or product_info.get("id"))
        if not item_id or item_id in self._seen:
            return None
        self._seen.add(item_id)
        titles = value.get("titles") if isinstance(value.get("titles"), dict) else {}
        pricing = value.get("pricing") if isinstance(value.get("pricing"), dict) else {}
        prices = pricing.get("prices") if isinstance(pricing.get("prices"), list) else []
        by_type = {str(row.get("priceType")): row for row in prices if isinstance(row, dict)}
        special = by_type.get("SPECIAL_PRICE", {})
        fsp = by_type.get("FSP", {})
        price = self._money(special.get("value") if special else value.get("special_price"))
        was_price = self._money(fsp.get("value") if fsp else value.get("selling_price"))
        if price is None:
            price = was_price
            was_price = None
        action = product_info.get("action") if isinstance(product_info.get("action"), dict) else {}
        if not action and isinstance(value.get("action"), dict):
            action = value["action"]
        media = value.get("media") if isinstance(value.get("media"), dict) else {}
        images = media.get("images") if isinstance(media.get("images"), list) else []
        image = images[0].get("url") if images and isinstance(images[0], dict) else value.get("media")
        if isinstance(image, str):
            image = image.replace("{@width}", "832").replace("{@height}", "832").replace("{@quality}", "70")
            image = image.replace("http://", "https://", 1)
        rating = value.get("rating") if isinstance(value.get("rating"), dict) else {}
        product_url = self._text(action.get("url") or value.get("url"))
        return {
            "category": response.meta.get("category"),
            "category_name": category_name,
            "item_id": item_id,
            "title": self._text(titles.get("title") or value.get("title")),
            "subtitle": self._text(titles.get("subtitle") or value.get("subtitle")),
            "url": urljoin(SITE, product_url.split("?", 1)[0]) if product_url else None,
            "image": image,
            "price": price,
            "was_price": was_price if was_price != price else None,
            "currency": self._text(special.get("currency") or fsp.get("currency") or value.get("currency")) or "INR",
            "discount_pct": self._number(pricing.get("totalDiscount") or value.get("discount_pct")),
            "rating": self._number(rating.get("average") or rating.get("value") or value.get("rating")),
            "reviews_count": self._int(rating.get("count") or value.get("reviews_count")),
            "availability": self._text(value.get("availability")),
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": response.url,
            "source": "flipkart_initial_state_product_widgets",
            "raw": product_info,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))

    @staticmethod
    def _text(value):
        return str(value).strip() if value is not None and str(value).strip() else None

    @staticmethod
    def _money(value):
        if isinstance(value, dict):
            value = value.get("value") or value.get("amount")
        match = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(value or ""))
        return float(match.group().replace(",", "")) if match else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _int(value):
        try:
            return int(str(value).replace(",", ""))
        except (TypeError, ValueError):
            return None
