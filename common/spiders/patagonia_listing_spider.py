from __future__ import annotations

import json
import re
from urllib.parse import quote, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.patagonia_categories import PATAGONIA_CATEGORIES

# The storefront's own "Load More" control calls this SFCC search grid
# endpoint.  The old ``AsyncComponents-ProductList`` endpoint now returns a
# full page shell with no product tiles, so the grid is fetched here instead.
_GRID_RE = re.compile(r"cgid=([A-Za-z0-9_-]+)")


class PatagoniaListingSpider(BaseListingSpider):
    """Products from Patagonia's first-party SFCC search grid."""

    name = "patagonia_listing"
    allowed_domains = ["patagonia.com", "www.patagonia.com"]
    require_category_arg = False
    categories = PATAGONIA_CATEGORIES
    api_url = (
        "https://www.patagonia.com/on/demandware.store/"
        "Sites-patagonia-us-Site/en_US/Search-UpdateGrid"
    )
    page_size = 16

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
        yield scrapy.Request(
            listing_url,
            callback=self.parse_listing,
            headers=self._headers(listing_url),
            meta={
                "listing_url": listing_url,
            },
        )

    def parse_listing(self, response):
        """Resolve the category id from the listing page, then fetch its grid."""
        if self._blocked(response):
            self.logger.warning(
                "Patagonia listing page unavailable (status=%s, bytes=%s)",
                response.status, len(response.body),
            )
            return
        cgid = self._extract_cgid(response) or self._nav_id()
        if not cgid:
            self.logger.warning(
                "Patagonia listing page exposed no category id at %s", response.url
            )
            return
        yield self._api_request(response.meta["listing_url"], cgid=cgid, page=1, start=0)

    def _api_request(self, listing_url: str, *, cgid: str, page: int, start: int):
        url = f"{self.api_url}?cgid={quote(cgid)}&start={start}&sz={self.page_size}"
        return scrapy.Request(
            url,
            callback=self.parse_api,
            headers=self._headers(listing_url),
            meta={
                "listing_url": listing_url,
                "cgid": cgid,
                "page": page,
                "start": start,
            },
        )

    def _extract_cgid(self, response) -> str | None:
        for cgid in _GRID_RE.findall(response.text):
            if cgid and cgid != "root":
                return cgid
        return None

    def _nav_id(self) -> str | None:
        entry = self.category_entry(self.category) if self.category else None
        nav_id = entry.get("nav_id") if isinstance(entry, dict) else None
        return nav_id if isinstance(nav_id, str) and nav_id else None

    @staticmethod
    def _blocked(response) -> bool:
        # NOTE: the storefront's normal pages embed a ``recaptcha`` *config*
        # blob, so a bare ``captcha`` substring is not a challenge signal.  Only
        # the interstitial title / proxy envelope indicate a failed route.
        body_lower = response.body.lower()
        return (
            response.status != 200
            or len(response.body) < 500
            or b"failed to get successful response" in body_lower
            or b"routing to checkout" in body_lower
            or b"hang tight!" in body_lower
        )

    def parse_api(self, response):
        if self._blocked(response):
            self.logger.warning(
                "Patagonia product grid failed (status=%s, bytes=%s)",
                response.status, len(response.body),
            )
            return
        tiles = response.css("product-tile, product-tile-simple")
        if not tiles:
            self.logger.warning("Patagonia product grid returned no product tiles")
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
            image = (
                tile.attrib.get("image")
                or tile.css('meta[itemprop="image"]::attr(content)').get()
                or tile.css("product-tile-image::attr(base)").get()
                or tile.css("img::attr(data-src)").get()
                or self._cover_image(tile)
            )
            hover = tile.attrib.get("hover-image") or tile.css(
                "img::attr(data-hover-src)"
            ).get()
            yield {
                "category": self.category,
                "item_id": item_id,
                "style_id": gtm_item.get("item_style_id") or raw_fields.get("style-id") or raw_fields.get("style_id"),
                "variant_id": gtm_item.get("item_variation_id") or raw_fields.get("variant-id") or raw_fields.get("variant_id"),
                "title": tile.attrib.get("name") or gtm_item.get("item_name") or raw_fields.get("name") or raw_fields.get("product-name") or tile.css("img::attr(alt)").get(),
                "brand": gtm_item.get("item_brand") or raw_fields.get("brand") or "Patagonia",
                "url": product_url,
                "image_url": self._absolute(response, image),
                "hover_image_url": self._absolute(response, hover),
                "color": gtm_item.get("item_color") or raw_fields.get("color") or raw_fields.get("color-name"),
                "price": price,
                "original_price": original,
                "currency": pricing.attrib.get("currency") or raw_fields.get("currency") or ("USD" if price is not None else None),
                "primary_category": pricing.attrib.get("primary-category") or gtm_item.get("item_category") or raw_fields.get("primary-category"),
                "swatch_count": self._integer(tile.attrib.get("number-of-swatches") or tile.attrib.get("swatch-count") or raw_fields.get("swatch-count")),
                "position": position,
                "page": page,
                "source_url": response.meta["listing_url"],
                "source": "patagonia_sfcc_search_grid",
                "timestamp": self.get_timestamp().isoformat(),
                "raw": raw,
            }

        if page < self.max_pages and len(tiles) >= self.page_size:
            yield self._api_request(
                response.meta["listing_url"],
                cgid=response.meta["cgid"],
                page=page + 1,
                start=response.meta["start"] + len(tiles),
            )

    @staticmethod
    def _headers(referer: str) -> dict[str, str]:
        return {
            "Accept": "text/html",
            "Referer": referer,
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _cover_image(tile):
        """Return the tile's real cover image, skipping the 1x1 lazy placeholder."""
        for src in tile.css("img::attr(src)").getall():
            if src and "images/1x1.png" not in src:
                return src
        return None

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
