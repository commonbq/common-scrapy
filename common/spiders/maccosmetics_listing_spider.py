from __future__ import annotations

"""MAC Cosmetics collection spider using Shopify's server-rendered catalog."""

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


COLLECTION_HANDLES = (
    "best-sellers", "eye-lip-treatments", "multi-use", "serums-treatments",
    "eye-makeup", "turquatic", "spf", "matte-lipstick", "tools-accessories",
    "dazzle", "waterproof", "lip-brushes", "moisturizers", "removers-cleansers",
    "makeup-sponges-applicators", "eye-primers", "blue-shades", "purple-shades",
    "lip-balm-primer", "skincare", "mixing-mediums", "liquid-lipstick", "lip",
    "pro-palettes", "face-kits", "berry-lip", "eye-brushes", "lip-liners",
    "face-brushes", "false-eyelashes", "primers", "highlighting-contour",
    "eyebrow", "fragrance", "pink-lipstick", "mascaras",
    "bestselling-lipstick-shades", "face", "eyeliner", "eye-shadow-palettes",
    "lip-gloss", "lip-palettes-kits", "concealer", "blush-bronzer",
    "eye-shadow", "brushes", "foundation", "lipstick", "winter-essentials",
    "mothers-day-gift-guide", "spring-essentials", "pride-looks",
    "refer-a-friend", "fall-favourites", "subscription", "sale", "lip-pairings",
    "minimalist-makeup", "wedding", "gift-by-price", "fall-lip-colours",
    "lip-sale", "setting-spray", "makeup-bags", "eye-accessories", "glow-play",
    "minis", "glitter-pigments", "tools", "value-sets", "double-denim",
    "all-pro", "new", "nudes", "red-lips", "haute-chocolates", "face-powders",
    "mac-in-sepia", "must-haves-halloween",
)


class MaccosmeticsListingSpider(BaseListingSpider):
    name = "maccosmetics_listing"
    allowed_domains = ["maccosmetics.com", "www.maccosmetics.com"]

    categories = [
        {"category": handle, "url": f"https://www.maccosmetics.com/collections/{handle}"}
        for handle in COLLECTION_HANDLES
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "sku", "title", "brand", "product_type",
            "url", "image_url", "price", "currency", "page", "source", "raw",
        ],
    }

    def start_requests(self):
        target = self.resolve_target_url()
        yield scrapy.Request(target, callback=self.parse, meta={"page": 1})

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        products = self._extract_catalog(response.text or "")
        cards = self._extract_cards(response)

        for product in products:
            variants = product.get("variants") or []
            variant = variants[0] if variants and isinstance(variants[0], dict) else {}
            handle = product.get("handle")
            yield {
                "category": self.category,
                "item_id": str(product.get("id")) if product.get("id") is not None else None,
                "sku": variant.get("sku"),
                "title": (cards.get(handle) or {}).get("title") or variant.get("public_title") or variant.get("name"),
                "brand": product.get("vendor"),
                "product_type": product.get("type"),
                "url": urljoin("https://www.maccosmetics.com", f"/products/{handle}") if handle else None,
                "image_url": (cards.get(handle) or {}).get("image_url"),
                "price": self._price(variant.get("price")),
                "currency": "USD",
                "page": page,
                "source": "maccosmetics_shopify_analytics",
                "raw": product,
            }

        if products and page < self.max_pages:
            next_url = response.xpath('//link[@rel="next"]/@href').get()
            if next_url:
                yield response.follow(next_url, callback=self.parse, meta={"page": page + 1})

    @staticmethod
    def _extract_catalog(html: str) -> list[dict]:
        marker = re.search(r"\bvar\s+meta\s*=\s*\{", html)
        if not marker:
            return []
        raw = MaccosmeticsListingSpider._balanced_object(html, marker.end() - 1)
        if not raw:
            return []
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return []
        products = value.get("products") if isinstance(value, dict) else None
        return [p for p in (products or []) if isinstance(p, dict)]

    @staticmethod
    def _balanced_object(text: str, start: int) -> str | None:
        depth = 0
        quoted = escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '"':
                quoted = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start:index + 1]
        return None

    @staticmethod
    def _extract_cards(response: scrapy.http.Response) -> dict[str, dict]:
        cards = {}
        for card in response.xpath("//dynamic-product-card[@data-handle]"):
            handle = card.attrib.get("data-handle")
            image = card.attrib.get("image") or card.xpath(".//img/@src").get()
            if handle:
                cards[handle] = {
                    "title": card.attrib.get("title"),
                    "image_url": response.urljoin(image) if image else None,
                }
        return cards

    @staticmethod
    def _price(value):
        try:
            return round(int(value) / 100, 2)
        except (TypeError, ValueError):
            return None
