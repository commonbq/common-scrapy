from __future__ import annotations

import json
from urllib.parse import quote, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.patagonia_categories import PATAGONIA_CATEGORIES


class PatagoniaListingSpider(BaseListingSpider):
    """Products from Patagonia's first-party SFCC async component API."""

    name = "patagonia_listing"
    allowed_domains = ["patagonia.com", "www.patagonia.com"]
    require_category_arg = False
    categories = [
        {"category": category, "url": url}
        for category, url in PATAGONIA_CATEGORIES.items()
    ]
    api_url = (
        "https://www.patagonia.com/on/demandware.store/"
        "Sites-patagonia-us-Site/en_US/AsyncComponents-ProductList"
    )

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "style_id", "variant_id", "title", "brand",
            "url", "image_url", "hover_image_url", "color", "price",
            "original_price", "currency", "primary_category", "swatch_count",
            "position", "page", "source_url", "source", "timestamp", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("category", "new-arrivals")
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        listing_url = self.resolve_target_url()
        yield self._api_request(listing_url, page=1, start=0)

    def _api_request(self, listing_url: str, *, page: int, start: int):
        category_id = urlparse(listing_url).path.rstrip("/").split("/")[-1]
        url = (
            f"{self.api_url}?cgid={quote(category_id)}&start={start}&sz=16&ajax=true"
        )
        return scrapy.Request(
            url,
            callback=self.parse_api,
            headers={
                "Accept": "text/html",
                "Referer": listing_url,
                "X-Requested-With": "XMLHttpRequest",
            },
            meta={
                "proxy": self._residential_proxy(),
                "listing_url": listing_url,
                "page": page,
                "start": start,
            },
        )

    def parse_api(self, response):
        body_lower = response.body.lower()
        if (
            response.status != 200
            or len(response.body) < 500
            or b"failed to get successful response" in body_lower
            or b"routing to checkout" in body_lower
            or b"captcha" in body_lower
        ):
            self.logger.warning(
                "Patagonia product-list API failed (status=%s, bytes=%s)",
                response.status, len(response.body),
            )
            return
        tiles = response.css("product-tile-simple")
        if not tiles:
            self.logger.warning("Patagonia product-list API returned no product tiles")
            return

        page = response.meta["page"]
        for position, tile in enumerate(tiles, response.meta["start"] + 1):
            raw_text = tile.attrib.get("data-gtm", "")
            try:
                raw = json.loads(raw_text) if raw_text else {}
            except json.JSONDecodeError:
                raw = {}
            gtm_item = self._gtm_item(raw)
            raw_fields = raw if isinstance(raw, dict) else {}
            href = tile.attrib.get("url") or tile.css("a::attr(href)").get()
            product_url = response.urljoin(href) if href else None
            item_id = str(
                gtm_item.get("item_id") or raw_fields.get("product-id") or raw_fields.get("product_id")
                or tile.attrib.get("product-id") or ""
            )
            dedupe_key = item_id or product_url
            if not dedupe_key or dedupe_key in self._seen:
                continue
            self._seen.add(dedupe_key)
            pricing = tile.css("product-tile-pricing")
            price = self._number(
                pricing.attrib.get("sale-price") or gtm_item.get("price")
                or raw_fields.get("sale-price")
            )
            original = self._number(pricing.attrib.get("list-price") or raw_fields.get("list-price"))
            images = tile.css("img::attr(src), img::attr(data-src)").getall()
            yield {
                "category": self.category,
                "item_id": item_id,
                "style_id": gtm_item.get("item_style_id") or raw_fields.get("style-id") or raw_fields.get("style_id"),
                "variant_id": gtm_item.get("item_variation_id") or raw_fields.get("variant-id") or raw_fields.get("variant_id"),
                "title": tile.attrib.get("name") or gtm_item.get("item_name") or raw_fields.get("name") or raw_fields.get("product-name") or tile.css("img::attr(alt)").get(),
                "brand": gtm_item.get("item_brand") or raw_fields.get("brand") or "Patagonia",
                "url": product_url,
                "image_url": self._absolute(response, tile.attrib.get("image") or (images[0] if images else None)),
                "hover_image_url": self._absolute(response, tile.attrib.get("hover-image") or (images[1] if len(images) > 1 else None)),
                "color": gtm_item.get("item_color") or raw_fields.get("color") or raw_fields.get("color-name"),
                "price": price,
                "original_price": original,
                "currency": pricing.attrib.get("currency") or raw_fields.get("currency") or ("USD" if price is not None else None),
                "primary_category": pricing.attrib.get("primary-category") or gtm_item.get("item_category") or raw_fields.get("primary-category"),
                "swatch_count": self._integer(tile.attrib.get("number-of-swatches") or tile.attrib.get("swatch-count") or raw_fields.get("swatch-count")),
                "position": position,
                "page": page,
                "source_url": response.meta["listing_url"],
                "source": "patagonia_sfcc_async_components_api",
                "timestamp": self.get_timestamp().isoformat(),
                "raw": raw,
            }

        if page < self.max_pages and len(tiles) >= 16:
            yield self._api_request(
                response.meta["listing_url"], page=page + 1,
                start=response.meta["start"] + len(tiles),
            )

    def _residential_proxy(self):
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not proxy or "scrapeops" not in proxy.lower():
            return proxy
        parts = urlparse(proxy)
        username = parts.username or ""
        options = username.split(".")[1:]
        for option in ("country=us", "residential=true"):
            if option not in options:
                username += f".{option}"
        host = parts.hostname or ""
        if parts.port:
            host += f":{parts.port}"
        auth = username
        if parts.password is not None:
            auth += f":{parts.password}"
        return urlunparse((parts.scheme, f"{auth}@{host}", parts.path, "", "", ""))

    @staticmethod
    def _number(value):
        try:
            return float(str(value).replace("$", "").replace(",", "").strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _gtm_item(raw):
        payloads = raw if isinstance(raw, list) else [raw]
        for payload in payloads:
            if not isinstance(payload, dict):
                continue
            items = payload.get("ecommerce", {}).get("items", [])
            if items and isinstance(items[0], dict):
                return items[0]
        return {}

    @staticmethod
    def _absolute(response, value):
        return response.urljoin(value) if value else None
