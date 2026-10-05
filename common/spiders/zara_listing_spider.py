from __future__ import annotations

"""Zara US listing spider (issue #208).

Zara's storefront is a hand-rolled SPA with **no** ``__NEXT_DATA__`` and no
server-rendered product cards: the PLP document is a shell and the grid is
fetched by a first-party XHR. This spider therefore uses exactly two JSON
endpoints and nothing else -- there is no HTML or JSON-LD fallback, so if the
API contract changes the spider fails loudly instead of silently returning zero.

1. Taxonomy (runtime, not committed)::

       GET https://www.zara.com/us/en/categories

2. Products per category::

       GET https://www.zara.com/us/en/category/<menuId>/products?ajax=true

   The response root is ``productGroups``; products live at
   ``productGroups[].elements[].commercialComponents[]`` at *every* element --
   elements are a mix of product tiles, editorial blocks and sticky banners, so
   the walk must not assume ``elements[0]``.

Observations that the implementation depends on (all re-verified live):

* **No pagination.** ``?page=2``, ``&offset=100``, ``&limit=100`` and
  ``&sortBy=price`` all return a byte-identical 5,548,128-byte body with the
  same first product id. The endpoint serves the whole category in one shot, so
  ``max_pages`` is honoured but page 2 is never requested for this endpoint --
  the crawl simply stops after the single response.
* **Editorial components carry no name.** Of 976 components in
  ``WOMAN > NEW ARRIVALS > THE NEW``, 919 have a non-empty ``name`` and 57 do
  not (marketing/decorative entries).
* **Outfits are a different ``type``.** 106 named components are
  ``type == "Bundle"`` (``"LOOK"``/``"LOOK 22"``, ``reference`` prefix ``T``,
  ``sectionName`` null, ``seo.irrelevant`` true on 67 of them, and
  ``bundleProducts`` repeats products that are *also* listed standalone). They
  are merchandising outfits, not products; only ``type == "Product"`` is
  emitted. That keeps 813 named products -> 808 unique ids for that category.
* **No ``oldPrice``/``salePrice`` field anywhere in the payload.** A raw grep of
  the 5.5 MB body finds zero occurrences of ``oldPrice``, ``pricePrevious``,
  ``discount``, ``salePrice`` or ``originalPrice``. The PLP XHR exposes only the
  current price, so ``original_price`` is always ``None`` and no discount is
  invented. ``isOnSale`` exists but is ``False`` on 890/919 components.
* **Prices are minor units.** ``price: 12900`` is ``$129.00``; the range across
  the category is 1290 - 130500.
* **Product ids repeat.** Merchandising blocks re-list the same product id
  (max 2 occurrences), so items are deduplicated on ``id`` across a crawl.

Flow::

    taxonomy request (only when no -a category/-a url is given)
        -> one products request per target category
        -> one item per type=="Product" named commercialComponent
"""

import json
import re
from typing import Any

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.zara_categories import (
    CATEGORIES_ENDPOINT,
    PRODUCTS_ENDPOINT_TEMPLATE,
    ZARA_LOCALE_PREFIX,
    ZARA_SITE_BASE,
    parse_taxonomy,
    seo_category_id_from_url,
)

#: xmedia `path` values are already prefixed with `/assets/public/`, so image
#: URLs are built from the site root, not from an `/assets/public` prefix.
IMAGE_BASE = ZARA_SITE_BASE

# The PLP XHR is first-party and answers without a bypass level, but it does
# require a browser-like User-Agent and an `X-Requested-With` header; without
# them the edge answers with the SPA shell instead of JSON.
BROWSER_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

# An HTML body where JSON was expected means a geo-block / bot wall, not a
# product payload. Matched case-insensitively because the edge varies casing.
CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "are you a human",
    "request unsuccessful",
    "enable javascript",
    "pardon the interruption",
)

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def _iter_components(payload: dict[str, Any]):
    """Yield every named commercial component across all groups/elements.

    ``elements`` mixes product tiles with editorial blocks, so products are not
    at a fixed depth -- walk every ``commercialComponents`` list and drop the
    unnamed (editorial) entries.
    """
    for group in payload.get("productGroups") or []:
        if not isinstance(group, dict):
            continue
        for element in group.get("elements") or []:
            if not isinstance(element, dict):
                continue
            for component in element.get("commercialComponents") or []:
                if not isinstance(component, dict):
                    continue
                if not component.get("name"):
                    continue  # editorial / decorative block, not a product
                yield component


class ZaraListingSpider(BaseListingSpider):
    name = "zara_listing"
    allowed_domains = [
        "zara.com",
        "www.zara.com",
        "localhost",
        "127.0.0.1",
    ]
    require_category_arg = False

    categories: list[dict[str, Any]] = []

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "section",
            "category_name",
            "category_id",
            "category_url",
            "item_id",
            "partnumber",
            "display_reference",
            "title",
            "kind",
            "url",
            "image_url",
            "image_alt",
            "colors",
            "color_count",
            "price",
            "original_price",
            "currency",
            "discount_percent",
            "availability",
            "coming_soon",
            "in_stock",
            "brand",
            "family_name",
            "subfamily_name",
            "grid_position",
            "page",
            "position",
            "total_count",
            "source_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        # The products endpoint needs the numeric *menu* id, which is not part
        # of the public listing URL, so `-a category_id=` is accepted to make a
        # bare `-a url=` run possible. Ignored when a taxonomy entry matches.
        self.explicit_category_id = (kwargs.get("category_id") or "").strip() or None
        super().__init__(*args, **kwargs)
        self._seen_items: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_items.clear()
        # `self.categories` is populated at runtime from /us/en/categories, so
        # it is empty at this point: any run (even `-a category=`) has to
        # hydrate the taxonomy first to turn a breadcrumb name / URL into the
        # menu id the products endpoint needs.
        yield scrapy.Request(
            CATEGORIES_ENDPOINT,
            callback=self.parse_categories,
            headers=self._api_headers(),
            errback=self._request_failed,
            dont_filter=True,
        )

    def _products_request(self, entry: dict[str, Any], *, page: int):
        url = PRODUCTS_ENDPOINT_TEMPLATE.format(category_id=entry["category_id"])
        url = f"{url}?ajax=true"
        return scrapy.Request(
            url,
            callback=self.parse_products,
            headers=self._api_headers(referer=entry["url"]),
            meta={"entry": entry, "page": page},
            errback=self._request_failed,
            dont_filter=True,
        )

    def _entry_for(self, target: str) -> dict[str, Any]:
        for entry in self.categories:
            if entry["url"] == target or entry["category"] == self.category:
                return entry

        # A raw URL (from -a url=) that matches no taxonomy entry. The menu id
        # is not part of the public URL, so it has to be supplied explicitly.
        category_id = self.explicit_category_id
        if not category_id:
            available = ", ".join(self.available_categories()[:20])
            raise ValueError(
                f"Unknown category '{self.category or target}'. The Zara products "
                "endpoint needs the numeric menu category id, which is not in the "
                "public URL, so the target must be one of the taxonomy entries -- or "
                f"pass -a category_id=<id> explicitly. Available categories (first 20): "
                f"{available}"
            )
        return {
            "category": self.category or _slugify(target),
            "name": self.category or _slugify(target),
            "url": target,
            "category_id": category_id,
            "seo_category_id": seo_category_id_from_url(target),
        }

    def _request_failed(self, failure):
        request = failure.request
        raise RuntimeError(
            f"Zara API request failed for {request.url}: {failure.value}"
        )

    # ----------------------------------------------------------------- headers

    def _api_headers(self, referer: str | None = None) -> dict[str, str]:
        """Browser-like headers. The edge answers the SPA shell without a UA."""
        headers = dict(BROWSER_HEADERS)
        headers["Origin"] = ZARA_SITE_BASE
        headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        )
        if referer:
            headers["Referer"] = referer
        return headers

    # ------------------------------------------------------------------ parse

    def parse_categories(self, response: scrapy.http.Response):
        payload = self._json_object(response, "categories")
        entries = parse_taxonomy(payload)
        if not entries:
            raise RuntimeError(
                "Zara /us/en/categories returned no product-category nodes at "
                f"{response.url}; the menu contract changed (expected >= 1 entry)."
            )
        self.categories = entries
        self.logger.info(
            "Zara taxonomy hydrated: %d unique product categories", len(entries)
        )

        selected = list(entries)
        if self.url or self.category_url or self.category:
            selected = [self._entry_for(self.resolve_target_url())]
        for entry in selected:
            yield self._products_request(entry, page=1)

    def parse_products(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        entry = response.meta["entry"]
        payload = self._json_object(response, "products")

        components = list(_iter_components(payload))
        if not components:
            raise RuntimeError(
                "Zara products response had no named commercialComponents at "
                f"{response.url}; the productGroups contract changed."
            )

        # Only type=="Product" is a product; type=="Bundle" is a "LOOK" outfit
        # whose bundleProducts re-list items that already exist standalone.
        products = [
            component for component in components
            if component.get("type") == "Product"
        ]
        if not products:
            raise RuntimeError(
                f"Zara products response at {response.url} contained "
                f"{len(components)} named components but none of type 'Product'."
            )

        total = len(products)
        emitted = 0
        for position, product in enumerate(products, start=1):
            item = self._item(product, response, entry, page, position, total)
            if item is None:
                continue
            emitted += 1
            yield item

        self.logger.info(
            "Zara %s: %d products in response, %d emitted (page %d)",
            entry["category"], total, emitted, page,
        )

        # The endpoint serves the whole category in one response; verified that
        # page/offset/limit/sort parameters are ignored (byte-identical bodies).
        # `max_pages` is honoured for the contract, but requesting page 2 would
        # only re-fetch the identical payload and yield duplicates only.
        return

    def _json_object(self, response: scrapy.http.Response, what: str) -> dict[str, Any]:
        if response.status != 200:
            raise RuntimeError(
                f"Zara {what} endpoint returned HTTP {response.status}: {response.url}"
            )
        body = response.text or ""
        lowered = body.lower()
        if any(marker in lowered for marker in CHALLENGE_MARKERS):
            raise RuntimeError(
                f"Zara {what} endpoint returned a bot-challenge page at "
                f"{response.url}: {body[:200]!r}"
            )
        try:
            payload = json.loads(body)
        except ValueError as exc:
            raise RuntimeError(
                f"Zara {what} endpoint returned non-JSON at {response.url}: {body[:200]!r}"
            ) from exc
        if not isinstance(payload, dict):
            raise RuntimeError(
                f"Zara {what} endpoint returned a non-object payload at {response.url}"
            )
        return payload

    # ------------------------------------------------------------------- item

    def _item(self, product, response, entry, page, position, total):
        item_id = self._text(product.get("id"))
        if not item_id or item_id in self._seen_items:
            return None
        self._seen_items.add(item_id)

        seo = product.get("seo") if isinstance(product.get("seo"), dict) else {}
        detail = product.get("detail") if isinstance(product.get("detail"), dict) else {}
        colors = detail.get("colors") if isinstance(detail.get("colors"), list) else []
        primary_color = colors[0] if colors and isinstance(colors[0], dict) else {}
        available = product.get("availableColors")
        available = available if isinstance(available, list) else []

        # Prices are minor units (12900 -> $129.00). The PLP XHR carries no
        # original/discount price at all, so nothing is inferred here.
        price = self._decimal(product.get("price"))
        original_price = self._decimal(product.get("oldPrice"))
        discount = None
        if price is not None and original_price and original_price > price:
            discount = round((original_price - price) / original_price * 100, 2)

        availability = (product.get("availability") or "").strip() or None
        coming_soon = bool(availability) and availability.lower() in ("coming_soon",)

        return {
            "category": entry.get("category"),
            "section": product.get("sectionName") or entry.get("section"),
            "category_name": entry.get("name"),
            "category_id": entry.get("category_id"),
            "category_url": entry.get("url"),
            "item_id": item_id,
            "partnumber": self._text(product.get("reference")),
            "display_reference": self._text(detail.get("displayReference")),
            "title": self._text(product.get("name")),
            "kind": product.get("kind"),
            "url": self._product_url(seo, entry),
            "image_url": self._image_url(colors),
            "image_alt": self._text(product.get("name")),
            "colors": self._color_names(available),
            "color_count": len(available) or len(colors) or None,
            "price": price,
            "original_price": original_price,
            "currency": "USD",
            "discount_percent": discount,
            "availability": availability,
            "coming_soon": coming_soon,
            "in_stock": bool(availability) and availability.lower() == "in_stock",
            "brand": self._brand(product.get("brand")),
            "family_name": self._text(product.get("familyName")),
            "subfamily_name": self._text(product.get("subfamilyName")),
            "grid_position": product.get("gridPosition"),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": "zara_api",
            "raw": product,
        }

    def _product_url(self, seo: dict[str, Any], entry: dict[str, Any]) -> str:
        """Zara PDP URL is ``/us/en/{keyword}-p{seoProductId}.html``.

        Verified: keyword ``zw-collection-floral-jacket`` + ``seoProductId``
        ``04088260`` -> ``https://www.zara.com/us/en/zw-collection-floral-jacket-p04088260.html``.
        """
        keyword = self._text(seo.get("keyword"))
        product_id = self._text(seo.get("seoProductId"))
        if not keyword or not product_id:
            return entry.get("url")
        return f"{ZARA_SITE_BASE}{ZARA_LOCALE_PREFIX}/{keyword}-p{product_id}.html"

    def _image_url(self, colors: list[dict[str, Any]]) -> str | None:
        """Best still image for a product, ranked by media quality.

        ``xmedia`` mixes ``set == 1`` (product shots, ``-p``/``-a1`` suffixes),
        ``set == 2`` (3D/animation blocks, often a bare directory path) and
        video entries. Only 417/919 products carry a set-1 image, so set 2 is the
        fallback. A ``deliveryUrl`` is an absolute ``.jpg`` on static.zara.net
        and is preferred over the extension-less CDN path; it is absent for the
        3D directory paths.
        """
        best: tuple[int, str] | None = None
        for color in colors:
            if not isinstance(color, dict):
                continue
            for media in color.get("xmedia") or []:
                if not isinstance(media, dict) or media.get("type") != "image":
                    continue
                path = self._text(media.get("path"))
                delivery = self._text(
                    (media.get("extraInfo") or {}).get("deliveryUrl")
                    if isinstance(media.get("extraInfo"), dict) else None
                )
                if delivery:
                    url, rank = delivery, 0
                elif path:
                    # A trailing-slash path is a 3D directory, not a still.
                    url, rank = f"{IMAGE_BASE}{path}", 2 if path.endswith("/") else 1
                else:
                    continue
                # set == 1 wins within the same rank tier.
                tier = rank * 2 + (0 if media.get("set") == 1 else 1)
                if best is None or tier < best[0]:
                    best = (tier, url)
        return best[1] if best else None

    def _color_names(self, available: list[dict[str, Any]]) -> list[str] | None:
        names = [
            self._text(entry.get("colorName"))
            for entry in available
            if isinstance(entry, dict) and self._text(entry.get("colorName"))
        ]
        return names or None

    def _brand(self, brand) -> str | None:
        if isinstance(brand, dict):
            return self._text(brand.get("brandGroupCode"))
        return self._text(brand)

    def _decimal(self, value) -> float | None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        if value <= 0:
            return None
        # Minor units -> major units. Zara always sends USD.
        return round(value / 100, 2)

    def _text(self, value) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None