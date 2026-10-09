from __future__ import annotations

"""Etsy category listings from the server-rendered category document.

Each category page embeds an ``application/ld+json`` ``ItemList`` with the
organic products for that page (name, image, canonical listing URL, brand,
offers), and the accompanying ``[data-listing-id]`` listing-card markup
carries shop IDs, ratings, review counts, ad and free-shipping flags.
Pagination follows the server-rendered ``?ref=pagination&page=N`` links.

Etsy's asynchronous Neu Spec search API (``/api/v3/ajax/bespoke/.../neu/specs/async_search_results``)
cannot replace this path: the anonymous ``public`` endpoint answers every
request shape with an empty ``output`` list, and the client's real results
path is an authenticated ``member`` POST gated by CSRF nonce + login session
(verified live against Etsy's own ``chunk-b-etsylibs`` client contract).
"""

import html
import json
import re

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.etsy_categories import ETSY_CATEGORIES


SOURCE = "etsy_itemlist_jsonld"


class EtsyListingSpider(BaseListingSpider):
    """Read Etsy category products from the server-rendered ItemList JSON-LD."""

    name = "etsy_listing"
    allowed_domains = ["etsy.com", "www.etsy.com"]
    categories = ETSY_CATEGORIES
    page_size = 60

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "item_id", "shop_id", "title", "shop", "url", "image",
            "price", "original_price", "currency", "rating", "reviews_count",
            "is_ad", "free_shipping", "category", "page", "position",
            "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield scrapy.Request(
            category_url,
            callback=self.parse,
            meta={"category": self.category, "category_url": category_url, "page": 1},
            headers=self._headers(),
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        entries = self._item_list_entries(response)
        if not entries:
            raise CloseSpider(f"Etsy category document contained no ItemList products at {response.url}")

        cards: dict[str, scrapy.Selector] = {}
        for card in response.css("[data-listing-id]"):
            listing_id = card.attrib.get("data-listing-id")
            if not listing_id:
                continue
            # The same listing can render several card instances (organic and
            # ad variants); prefer the one that carries the shop id.
            current = cards.get(listing_id)
            if current is None or (not current.attrib.get("data-shop-id") and card.attrib.get("data-shop-id")):
                cards[listing_id] = card

        emitted = 0
        for entry in entries:
            product = entry.get("item") if isinstance(entry.get("item"), dict) else entry
            url = self._clean_url(str(product.get("url") or entry.get("url") or ""))
            if not url:
                continue
            item_id = self._listing_id(url)
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            card = cards.get(item_id)
            emitted += 1
            yield self._build_item(
                product,
                card,
                category=response.meta["category"],
                page=page,
                position=entry.get("position") or emitted,
            )

        if page < self.max_pages:
            next_url = self._next_page_url(response, page)
            if next_url:
                yield response.follow(
                    next_url,
                    callback=self.parse,
                    meta={
                        "category": response.meta["category"],
                        "category_url": response.meta["category_url"],
                        "page": page + 1,
                    },
                    headers=self._headers(),
                )

    def _build_item(self, product: dict, card, category: str, page: int, position) -> dict:
        item_id = self._listing_id(str(product.get("url") or ""))
        shop_id = card.attrib.get("data-shop-id") if card is not None else None
        offers = product.get("offers")
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if not isinstance(offers, dict):
            offers = {}
        price_spec = offers.get("priceSpecification")
        if isinstance(price_spec, list):
            price_spec = price_spec[0] if price_spec else None
        brand = product.get("brand")
        if isinstance(brand, dict):
            brand = brand.get("name")
        image = product.get("image")
        if isinstance(image, list):
            image = image[0] if image else None
        text = " ".join(card.css("::text").getall()) if card is not None else ""
        return {
            "item_id": item_id,
            "shop_id": shop_id,
            "title": self._clean(product.get("name")),
            "shop": self._shop_name(card),
            "url": self._clean_url(str(product.get("url") or "")),
            "image": image,
            "price": self._number(offers.get("price")),
            "original_price": self._number(price_spec.get("price")) if isinstance(price_spec, dict) else None,
            "currency": offers.get("priceCurrency") or "USD",
            "rating": self._number(card.css('input[name="rating"]::attr(value)').get()) if card is not None else None,
            "reviews_count": self._integer(text) if card is not None else None,
            "is_ad": "Ad by" in text,
            "free_shipping": "FREE shipping" in text,
            "category": category,
            "page": page,
            "position": position,
            "source": SOURCE,
            "raw": {"listing_id": item_id, "shop_id": shop_id, "brand": brand},
        }

    @staticmethod
    def _item_list_entries(response: scrapy.http.Response) -> list[dict]:
        entries: list[dict] = []
        for text in response.css('script[type="application/ld+json"]::text').getall():
            try:
                value = json.loads(text)
            except (TypeError, json.JSONDecodeError):
                continue
            nodes = value if isinstance(value, list) else [value]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                graph = node.get("@graph") if isinstance(node.get("@graph"), list) else [node]
                for candidate in graph:
                    if isinstance(candidate, dict) and candidate.get("@type") == "ItemList":
                        entries.extend(
                            entry for entry in candidate.get("itemListElement") or [] if isinstance(entry, dict)
                        )
        return entries

    @staticmethod
    def _next_page_url(response: scrapy.http.Response, page: int) -> str | None:
        for anchor in response.css("a[data-page]"):
            try:
                target = int(anchor.attrib.get("data-page", 0))
            except (TypeError, ValueError):
                continue
            if target == page + 1 and anchor.attrib.get("href"):
                return anchor.attrib["href"]
        return None

    @staticmethod
    def _listing_id(url: str) -> str | None:
        match = re.search(r"/listing/(\d+)", url)
        return match.group(1) if match else None

    @staticmethod
    def _clean_url(url: str) -> str:
        return url.split("?")[0] if url else ""

    @staticmethod
    def _shop_name(card) -> str | None:
        if card is None:
            return None
        texts = [t.strip() for t in card.css("[data-seller-name-container] ::text").getall() if t.strip()]
        if not texts:
            return None
        first = texts[0]
        return None if first.startswith(("Ad by", "Ad from")) else first

    @staticmethod
    def _clean(value) -> str | None:
        return " ".join(html.unescape(str(value or "")).split()) or None

    @staticmethod
    def _number(value):
        if value is None:
            return None
        match = re.search(r"[\d,.]+", str(value))
        return float(match.group().replace(",", "")) if match else None

    @staticmethod
    def _integer(value):
        match = re.search(r"\(([\d,.]+)([kKmM]?)\)", value or "")
        if not match:
            return None
        number = float(match.group(1).replace(",", ""))
        multiplier = {"k": 1_000, "m": 1_000_000}.get(match.group(2).lower(), 1)
        return int(number * multiplier)

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
