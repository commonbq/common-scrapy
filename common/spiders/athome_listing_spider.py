from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlencode, urljoin, urlsplit

import scrapy

from common.spiders.athome_categories import ATHOME_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


API_ENDPOINT = (
    "https://www.athome.com/on/demandware.store/"
    "Sites-athome-sfra-Site/default/Search-UpdateGrid"
)


class AthomeListingSpider(BaseListingSpider):
    """At Home products from the SFRA Search-UpdateGrid AJAX API only."""

    name = "athome_listing"
    allowed_domains = ["athome.com", "www.athome.com", "static.athome.com"]
    categories = ATHOME_CATEGORIES
    require_category_arg = False
    page_size = 24

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "RETRY_HTTP_CODES": [403, 408, 429, 500, 502, 503, 504],
        "RETRY_TIMES": 3,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category", "category_name", "category_url", "item_id", "master_id",
            "representative_id", "title", "url", "image_url", "image_alt",
            "image_srcset", "price", "currency", "price_type", "is_clearance",
            "rating", "reviews_count", "badges", "availability_badges",
            "more_options", "page", "position", "offset", "page_size",
            "total_count", "price_cache_timestamp", "source_url", "source",
            "raw", "timestamp",
        ],
    }
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        entry = self._selected_category()
        yield self._api_request(entry, page=1, offset=0)

    def _selected_category(self) -> dict[str, Any]:
        target = self.url or self.category_url
        if target:
            slug = urlsplit(target).path.strip("/").split("/")[-1]
            entry = self.category_entry(slug)
        elif self.category:
            wanted = self.category.casefold()
            entry = next(
                (
                    row for row in self.iter_categories()
                    if wanted in {row["category"].casefold(), row.get("name", "").casefold()}
                ),
                None,
            )
        else:
            entry = next(iter(self.iter_categories()))
        if entry is None:
            available = ", ".join(self.available_categories())
            raise ValueError(
                f"Unknown At Home category '{self.category or target}'. "
                f"Available categories: {available}"
            )
        return entry

    def _api_request(self, entry: dict[str, Any], *, page: int, offset: int):
        query = urlencode(
            {
                "cgid": entry["category"],
                "prefn1": "hiddenFromSearch",
                "prefv1": "false",
                "start": offset,
                "sz": self.page_size,
            }
        )
        return scrapy.Request(
            f"{API_ENDPOINT}?{query}",
            callback=self.parse_api,
            headers={**self.headers, "Referer": entry["url"]},
            meta={"entry": entry, "page": page, "offset": offset},
            dont_filter=True,
        )

    def parse_api(self, response):
        if response.status != 200:
            raise RuntimeError(
                f"At Home Search-UpdateGrid API returned HTTP {response.status}: "
                f"{response.url}"
            )
        cards = response.css("div.product-tile")
        if not cards:
            raise RuntimeError(
                f"At Home Search-UpdateGrid API returned no product payload: {response.url}"
            )

        entry = response.meta["entry"]
        page = int(response.meta["page"])
        offset = int(response.meta["offset"])
        total = self._integer(
            response.css("[data-product-count]::attr(data-product-count)").get()
        )
        for position, card in enumerate(cards, 1):
            item_id = self._tile_attribute(card, "data-pid")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(card, response, entry, page, position, offset, total)

        next_offset = offset + self.page_size
        if page < self.max_pages and (total is None or next_offset < total):
            yield self._api_request(entry, page=page + 1, offset=next_offset)

    def _item(self, card, response, entry, page, position, offset, total):
        link = card.css("a.product-image::attr(href)").get()
        image = card.css("img.tile-image")
        pricing = card.css(".product-pricing")
        pricing_data = card.css(".product-pricing .Pricing")
        price_text = "".join(card.css(".product-pricing .fancy.price *::text").getall())
        rating = self._number(card.css(".rating-number::text").get())
        reviews = self._integer(card.css(".rating-count::text").re_first(r"([\d,]+)"))
        badges = self._clean_texts(card.css(".badge-container .badge ::text").getall())
        availability = self._clean_texts(
            card.css(".availability-badges .badge ::text").getall()
        )
        raw = {
            "tile": dict(card.attrib),
            "link_aria_label": card.css("a.product-image::attr(aria-label)").get(),
            "pricing": dict(pricing.attrib) if pricing else {},
            "price": dict(pricing_data.attrib) if pricing_data else {},
        }
        return {
            "category": entry["category"],
            "category_name": entry["name"],
            "category_url": entry["url"],
            "item_id": self._tile_attribute(card, "data-pid"),
            "master_id": self._tile_attribute(card, "data-master-pid"),
            "representative_id": self._tile_attribute(card, "data-reppid"),
            "title": self._text(card.css("h3.pt-name::text").get()),
            "url": urljoin("https://www.athome.com", link) if link else None,
            "image_url": image.attrib.get("src") if image else None,
            "image_alt": image.attrib.get("alt") if image else None,
            "image_srcset": image.attrib.get("srcset") if image else None,
            "price": self._number(price_text),
            "currency": "USD",
            "price_type": pricing.attrib.get("data-price-type") if pricing else None,
            "is_clearance": self._boolean(
                pricing_data.attrib.get("data-isclearance") if pricing_data else None
            ),
            "rating": rating,
            "reviews_count": reviews,
            "badges": badges,
            "availability_badges": availability,
            "more_options": self._text(
                card.css(".product-moreoptions::text").get()
            ),
            "page": page,
            "position": position,
            "offset": offset,
            "page_size": self.page_size,
            "total_count": total,
            "price_cache_timestamp": (
                pricing_data.attrib.get("data-cache-timestamp") if pricing_data else None
            ),
            "source_url": response.url,
            "source": "athome_sfra_search_updategrid_api",
            "raw": raw,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _text(value):
        return " ".join(value.split()) if isinstance(value, str) else None

    @classmethod
    def _clean_texts(cls, values):
        return [text for value in values if (text := cls._text(value))]

    @staticmethod
    def _tile_attribute(card, name):
        parent_value = card.xpath(
            f"ancestor::div[contains(concat(' ', normalize-space(@class), ' '), "
            f"' product ')][1]/@{name}"
        ).get()
        return parent_value or card.css(f"*[{name}]::attr({name})").get()

    @staticmethod
    def _number(value):
        if value is None:
            return None
        compact = re.sub(r"[^\d,.-]", "", str(value))
        match = re.search(r"-?[\d,]+(?:\.\d+)?", compact)
        try:
            return float(match.group(0).replace(",", "")) if match else None
        except ValueError:
            return None

    @staticmethod
    def _integer(value):
        if value is None:
            return None
        match = re.search(r"[\d,]+", str(value))
        try:
            return int(match.group(0).replace(",", "")) if match else None
        except ValueError:
            return None

    @staticmethod
    def _boolean(value):
        if value is None:
            return None
        return str(value).strip().lower() == "true"
