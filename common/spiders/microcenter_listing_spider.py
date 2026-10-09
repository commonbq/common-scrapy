from __future__ import annotations

"""Micro Center listings from structured server-rendered product-card state."""

import math
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider, group_categories
from common.spiders.microcenter_categories import MICROCENTER_CATEGORIES


class MicrocenterListingSpider(BaseListingSpider):
    name = "microcenter_listing"
    allowed_domains = [
        "microcenter.com", "www.microcenter.com", "productimages.microcenter.com",
        "127.0.0.1", "localhost",  # explicit fixture/custom-URL verification
    ]
    categories = group_categories(MICROCENTER_CATEGORIES, "department")
    page_size = 24

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "department", "group", "category", "category_name", "navigation_contexts",
            "item_id", "sku", "title", "brand", "url", "image", "price",
            "original_price", "currency", "availability", "stock_count", "store_name",
            "store_id", "promotion", "page", "position", "total_count", "last_page",
            "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        self.store_id = str(kwargs.get("store_id") or "121").strip()
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()
        self._category_record = next(
            (entry for entry in self.iter_categories() if entry["category"] == self.category), {}
        )

    def start_requests(self):
        url = self._with_query(self.resolve_target_url(), storeid=self.store_id, page="1")
        yield scrapy.Request(url, callback=self.parse, meta={"page": 1})

    def parse(self, response):
        page = int(response.meta.get("page", 1))
        if self._blocked(response):
            self.logger.error("Micro Center challenge/proxy response status=%s page=%s", response.status, page)
            return

        cards = response.css("li.product_wrapper")
        if not cards:
            self.logger.warning("Micro Center returned no structured product cards on page %s", page)
            return

        total_count = self._total_count(response)
        last_page = max(1, math.ceil(total_count / self.page_size)) if total_count else page
        emitted = 0
        for card in cards:
            state = card.css("a.productClickItemV2[data-id]").attrib
            item_id = state.get("data-id")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            stock_text = self._text(card.css("div.stock ::text").getall())
            stock_match = re.search(r"(\d+)\+?\s*IN STOCK", stock_text, re.I)
            original = self._money(card.css("div.price strike ::text").getall())
            price = self._number(state.get("data-price"))
            yield {
                "department": self._category_record.get("department"),
                "group": self._category_record.get("group"),
                "category": self.category,
                "category_name": self._category_record.get("name"),
                "navigation_contexts": self._category_record.get("navigation_contexts", []),
                "item_id": item_id,
                "sku": self._value(card, "input[name=sku]::attr(value)") or self._sku(card),
                "title": state.get("data-name") or self._text(card.css("div.h2 a ::text").getall()),
                "brand": state.get("data-brand"),
                "url": response.urljoin(state.get("href", "")),
                "image": response.urljoin(card.css("img.SearchResultProductImage::attr(src)").get() or ""),
                "price": price,
                "original_price": original,
                "currency": "USD",
                "availability": stock_text or self._text(card.css("div.footerrestrictions ::text").getall()),
                "stock_count": int(stock_match.group(1)) if stock_match else None,
                "store_name": self._text(card.css("span.storeName ::text").getall()).removeprefix("at ").strip() or None,
                "store_id": self._value(card, "input[name=store_id]::attr(value)") or self.store_id,
                "promotion": self._text(card.css("div.highlight ::text").getall()) or None,
                "page": page,
                "position": self._integer(state.get("data-position")),
                "total_count": total_count,
                "last_page": last_page,
                "source": "microcenter_card_state_bootstrap",
                "raw": dict(state),
                "timestamp": self.get_timestamp(),
            }

        if emitted and page < min(last_page, self.max_pages):
            next_page = page + 1
            yield scrapy.Request(
                self._with_query(response.url, storeid=self.store_id, page=str(next_page)),
                callback=self.parse,
                meta={"page": next_page},
            )

    @staticmethod
    def _with_query(url: str, **updates: str) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query.update(updates)
        return urlunsplit(parts._replace(query=urlencode(query)))

    @staticmethod
    def _text(values) -> str:
        return " ".join(" ".join(values).split())

    @classmethod
    def _money(cls, values):
        match = re.search(r"\$?([\d,]+(?:\.\d+)?)", cls._text(values))
        return cls._number(match.group(1)) if match else None

    @staticmethod
    def _number(value):
        try:
            return float(str(value).replace(",", ""))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _value(card, selector):
        return card.css(selector).get()

    @staticmethod
    def _sku(card):
        match = re.search(r"SKU:\s*(\d+)", " ".join(card.css("p.sku ::text").getall()), re.I)
        return match.group(1) if match else None

    @staticmethod
    def _total_count(response) -> int | None:
        text = " ".join(response.css("#bottomPagination .status ::text").getall())
        match = re.search(r"of\s+([\d,]+)\s+items", text, re.I)
        return int(match.group(1).replace(",", "")) if match else None

    @staticmethod
    def _blocked(response) -> bool:
        body = response.text.lower()
        return response.status >= 400 or any(marker in body for marker in (
            "just a moment", "cf-chl-", "api credits", "failed to get successful response",
            "access denied", "captcha",
        ))
