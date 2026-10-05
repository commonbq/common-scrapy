from __future__ import annotations

"""Urban Outfitters listing spider (issue #211).

Urban Outfitters is a Vue/Pinia SSR storefront, not Next.js.  Every category
page ships its entire product grid in one hydration script::

    <script id="urbnInitialPiniaState" type="mime/invalid">"{...escaped JSON...}"</script>

The script text is a JSON *string* containing JSON, so it decodes twice::

    state = json.loads(json.loads(script_text))
    tiles = state["category"]["pages"][str(page)]["wrapper"]["tiles"]

Each ``PRODUCT`` tile carries the product record, the per-colour SKU slice with
prices, the face-out variant, and review aggregates.  This spider therefore uses
exactly ONE data direction -- the SSR hydration state.  There is **no HTML
tile / JSON-LD fallback**: if the hydration script disappears the spider fails
loudly instead of silently degrading to a partial scrape.  (The payload also
contains a ``category.jsonLd`` block; it is deliberately ignored.)

Pagination is plain SSR too: ``?page=N`` re-renders the route and hydrates only
page ``N``, so no client-side XHR is ever needed.  Page 1 is requested *without*
a ``page`` parameter -- that is the canonical first-page URL, and any existing
refinement query on the category URL is preserved.

Category inventory comes from the sitemap (see
:mod:`common.spiders.urbanoutfitters_categories`) -- the one other request this
spider makes, and it exists only to resolve ``-a category=`` to a PLP URL.

Flow:
    categories_sitemap.xml
        -> resolve -a category= / category_url= / url=
        -> PLP (page 1, then ?page=2..max_pages)
        -> emit one item per unique PRODUCT tile
"""

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.urbanoutfitters_categories import (
    URBN_CATEGORY_SITEMAP_URL,
    URBN_NAV_ROOTS,
    URBN_SITE_BASE,
    available_categories,
    parse_category_sitemap,
    resolve_category,
)

PDP_BASE = f"{URBN_SITE_BASE}/shop/"
IMAGE_BASE = "https://images.urbndata.com/is/image/UrbanOutfitters/"
IMAGE_WIDTH = "wid=640"

# The hydration script is emitted as one long line; match it non-greedily but
# anchor on the closing tag so a `</script>` inside a JSON string cannot escape.
_PINIA_RE = re.compile(
    r'<script[^>]*\bid="urbnInitialPiniaState"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)

# Body markers of an anti-bot / error interstitial that can be served with HTTP
# 200. The storefront sits behind Datadome, whose own loader in the <head>
# contains "exposeCaptchaFunction", so "captcha" is deliberately NOT a marker --
# it false-positives on every real page.
_CHALLENGE_MARKERS = (
    "access denied",
    "are you a human",
    "pardon the interruption",
    "request unsuccessful",
    "site unavailable",
)


def _titleize(value: str) -> str:
    words = [word for word in re.split(r"[-_]+", value or "") if word]
    return " ".join(word[:1].upper() + word[1:] for word in words)

_BADGE_LABELS = {
    "NEW_COLOR_AVAILABLE": "New Color Available",
    "UO_EXCLUSIVE": "UO Exclusive",
    "BEST_SELLER": "Best Seller",
    "ON_SALE": "Sale",
    "CLEARANCE": "Clearance",
    "LIMITED_EDITION": "Limited Edition",
    "RESTOCKED": "Restocked",
}


class UrbanOutfittersListingSpider(BaseListingSpider):
    """Urban Outfitters listings from the SSR Pinia hydration payload."""

    name = "urbanoutfitters_listing"
    allowed_domains = [
        "urbanoutfitters.com",
        "www.urbanoutfitters.com",
        "localhost",
        "127.0.0.1",
    ]

    require_category_arg = False

    # Seed inventory so `-a category=<slug>` is valid (and documented) before the
    # sitemap is fetched; parse_category_sitemap() replaces it with the full set.
    categories = [
        {"category": slug, "name": name, "url": url, "nav_root": name}
        for slug, name, url in URBN_NAV_ROOTS
    ]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category",
            "category_name",
            "category_path",
            "category_query",
            "nav_root",
            "item_id",
            "style_id",
            "sku_id",
            "title",
            "brand",
            "url",
            "image_url",
            "image_alt",
            "price",
            "price_high",
            "sale_price",
            "list_price",
            "list_price_high",
            "currency",
            "on_sale",
            "markdown_state",
            "discount_percentage",
            "rating",
            "reviews_count",
            "color",
            "color_code",
            "color_hex",
            "color_count",
            "swatch_url",
            "badges",
            "callout",
            "in_stock",
            "sold_out",
            "gift_card",
            "app_exclusive",
            "configurable",
            "page",
            "position",
            "total_count",
            "total_pages",
            "source_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<slug>, category_url=<url>, or url=<url>, "
                f"e.g. -a category=new-arrivals. Categories are loaded from "
                f"{URBN_CATEGORY_SITEMAP_URL}."
            )
        self._seen_products: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_products.clear()
        yield scrapy.Request(
            URBN_CATEGORY_SITEMAP_URL,
            callback=self.parse_category_sitemap,
            headers=self._html_headers(),
            dont_filter=True,
        )

    def parse_category_sitemap(self, response: scrapy.http.Response):
        self._reject_challenge(response, "category sitemap")
        categories = parse_category_sitemap(response.text)
        if not categories:
            raise RuntimeError(
                f"No category URLs found in {response.url}. The sitemap contract may "
                "have changed, or the response was not the sitemap."
            )
        self.categories = categories
        self.logger.info(
            "Urban Outfitters category sitemap: %d categories (%d refinement "
            "variants, %d navigation roots)",
            len(categories),
            sum(1 for entry in categories if entry.get("query")),
            sum(1 for entry in categories if entry.get("nav_root")),
        )

        target = resolve_category(
            categories,
            category=self.category,
            category_url=self.category_url,
            url=self.url,
        )
        if target is None:
            raise ValueError(
                f"Unknown Urban Outfitters category "
                f"{self.category or self.category_url or self.url!r}. "
                f"{len(categories)} categories are in the sitemap; examples: "
                f"{', '.join(available_categories(categories))}. Pass a slug from "
                f"{URBN_CATEGORY_SITEMAP_URL}, or -a category_url=/<path>[?<refinement>]."
            )

        yield self._page_request(target, page=1)

    def _page_request(self, target: dict[str, str], *, page: int):
        return scrapy.Request(
            self._page_url(target["url"], page),
            callback=self.parse,
            headers=self._html_headers(),
            meta={"category": target, "page": page, "base_url": target["url"]},
            dont_filter=True,
        )

    # ------------------------------------------------------------------- parse

    def parse(self, response: scrapy.http.Response):
        self._reject_challenge(response, "category page")
        target: dict[str, str] = response.meta["category"]
        page = int(response.meta.get("page", 1))

        state = self._pinia_state(response.text)
        tiles = self._tiles(state)
        if not tiles:
            # A page past the end hydrates an empty tile array, which ends the
            # crawl instead of erroring.
            if page > 1:
                self.logger.info(
                    "Stopping at %s page %s: no hydrated product tiles",
                    target["category"],
                    page,
                )
                return
            raise RuntimeError(
                f"No product tiles in the Urban Outfitters hydration payload at "
                f"{response.url} (slug={state.get('category', {}).get('slug')!r}). "
                "The category may be a campaign landing page with no PLP grid."
            )

        category_state = state.get("category") if isinstance(state.get("category"), dict) else {}
        total_count = self._integer(category_state.get("totalRecordCount"))
        total_pages = self._integer(category_state.get("totalPages"))
        slug = category_state.get("slug")

        self.logger.info(
            "Urban Outfitters %s page %s: %d tiles (total %s, pages %s, slug %s)",
            target["category"],
            page,
            len(tiles),
            total_count,
            total_pages,
            slug,
        )

        emitted = 0
        for position, tile in enumerate(tiles, start=1):
            if not isinstance(tile, dict) or tile.get("recordType") != "PRODUCT":
                continue
            product = tile.get("product")
            if not isinstance(product, dict):
                continue
            item_id = self._text(product.get("productId"))
            # The same style is often tiled once per face-out colourway, so the
            # grid is not unique by productId; dedupe on the stable style id and
            # keep the first (grid order) occurrence.
            key = item_id or self._text(product.get("styleNumber"))
            if not key or key in self._seen_products:
                continue
            self._seen_products.add(key)
            emitted += 1
            yield self._item(tile, target, response, page, position, total_count, total_pages)

        if page >= self.max_pages:
            return
        if total_pages is not None and page >= total_pages:
            return
        if total_count is not None and page * len(tiles) >= total_count:
            return
        if not emitted:
            # Every tile was a duplicate of an earlier page: the grid wrapped.
            self.logger.info(
                "Stopping at %s page %s: no new products", target["category"], page
            )
            return
        yield self._page_request(target, page=page + 1)

    # ------------------------------------------------------------------- item

    def _item(
        self,
        tile: dict[str, Any],
        target: dict[str, str],
        response: scrapy.http.Response,
        page: int,
        position: int,
        total_count: int | None,
        total_pages: int | None,
    ) -> dict[str, Any]:
        product = tile["product"]
        sku_info = tile.get("skuInfo")
        sku_info = sku_info if isinstance(sku_info, dict) else {}
        reviews = tile.get("reviews")
        reviews = reviews if isinstance(reviews, dict) else {}

        title = product.get("displayName")
        brand = product.get("brand")
        style_number = self._text(product.get("styleNumber"))
        color_code = self._text(tile.get("faceOutColorCode")) or self._text(
            product.get("defaultColorCode")
        )
        slug = self._text(product.get("productSlug"))
        url = f"{PDP_BASE}{slug}" if slug else None

        # Prices are per-colour ranges: `<style>_<color>` SKUs each carry their
        # own low/high pair, so the tile reports the cheapest and dearest colour.
        sale_low = self._number(sku_info.get("salePriceLow"))
        sale_high = self._number(sku_info.get("salePriceHigh"))
        list_low = self._number(sku_info.get("listPriceLow"))
        list_high = self._number(sku_info.get("listPriceHigh"))
        price = sale_low if sale_low is not None else list_low
        on_sale = bool(sku_info.get("hasMarkdown")) and bool(
            sale_low is not None and list_low is not None and list_low > sale_low
        )
        discount_percentage = None
        if on_sale and price and list_low and list_low > price:
            discount_percentage = round((list_low - price) / list_low * 100, 2)

        colors = self._colors(sku_info, color_code)
        badges = self._badges(product.get("badges"))
        callout = product.get("browseCallOutPrimary") or product.get("browseCallOutSecondary")
        sold_out = bool(product.get("displaySoldOut"))
        has_available_sku = sku_info.get("hasAvailableSku")

        return {
            "category": target["category"],
            "category_name": target.get("name"),
            "category_path": target.get("path"),
            "category_query": target.get("query") or None,
            "nav_root": target.get("nav_root"),
            "item_id": self._text(product.get("productId")),
            "style_id": style_number,
            "sku_id": self._style_sku(style_number, color_code),
            "title": title,
            "brand": brand,
            "url": url,
            "image_url": self._image_url(tile.get("faceOutImage") or product.get("defaultImage")),
            "image_alt": title,
            "price": price,
            "price_high": sale_high if sale_high != sale_low else None,
            "sale_price": sale_low if on_sale else None,
            "list_price": list_low if on_sale else None,
            "list_price_high": list_high if on_sale and list_high != list_low else None,
            "currency": "USD" if price is not None else None,
            "on_sale": on_sale,
            "markdown_state": sku_info.get("markdownState"),
            "discount_percentage": discount_percentage,
            "rating": self._number(reviews.get("averageRating")),
            "reviews_count": self._integer(reviews.get("count")),
            "color": colors["color"],
            "color_code": color_code,
            "color_hex": colors["color_hex"],
            "color_count": colors["color_count"],
            "swatch_url": colors["swatch_url"] or None,
            "badges": badges,
            "callout": callout,
            "in_stock": (
                bool(has_available_sku) if isinstance(has_available_sku, bool)
                else (not sold_out if has_available_sku is None else None)
            ),
            "sold_out": sold_out,
            "gift_card": bool(product.get("isGiftCard") or product.get("isEgiftCard")),
            "app_exclusive": product.get("isAppExclusive"),
            "configurable": product.get("configurationEnabled"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "total_pages": total_pages,
            "source_url": response.url,
            "source": "urbanoutfitters_pinia_ssr_tiles",
            # The whole hydrated tile: prices and the colour slice live on
            # `skuInfo`, next to `product`, so `product` alone would drop them.
            "raw": tile,
        }

    @classmethod
    def _colors(cls, sku_info: dict[str, Any], color_code: str | None) -> dict[str, Any]:
        """Resolve the face-out colour from ``skuInfo.primarySlice.sliceItems``."""
        primary = sku_info.get("primarySlice")
        primary = primary if isinstance(primary, dict) else {}
        slice_items = primary.get("sliceItems")
        slice_items = [item for item in slice_items or [] if isinstance(item, dict)]

        match = None
        for item in slice_items:
            if color_code and str(item.get("code")) == str(color_code):
                match = item
                break
        if match is None and slice_items:
            match = slice_items[0]

        return {
            "color": (match or {}).get("displayName"),
            "color_hex": (match or {}).get("hexColor") or None,
            "swatch_url": (match or {}).get("swatchUrl"),
            "color_count": len(slice_items) or None,
        }

    @classmethod
    def _badges(cls, badges: Any) -> list[str] | None:
        """Flatten the badge list into the labels the PLP renders."""
        labels = []
        for badge in badges or []:
            if not isinstance(badge, dict):
                continue
            badge_type = badge.get("type")
            if not badge_type:
                continue
            labels.append(_BADGE_LABELS.get(badge_type, _titleize(badge_type)))
        return labels or None

    @staticmethod
    def _style_sku(style_number: str | None, color_code: str | None) -> str | None:
        if style_number and color_code:
            return f"{style_number}_{color_code}"
        return style_number or color_code

    @staticmethod
    def _image_url(image: Any) -> str | None:
        if not image:
            return None
        image = str(image).strip()
        if not image:
            return None
        if image.startswith("http"):
            return image
        return f"{IMAGE_BASE}{image}?{IMAGE_WIDTH}"

    # ------------------------------------------------------------- hydration

    @classmethod
    def _pinia_state(cls, document: str) -> dict[str, Any]:
        """Double-decode ``#urbnInitialPiniaState`` into the hydration object.

        The script body is a JSON string literal wrapping JSON, so it has to be
        decoded twice; a single pass yields a string, not a dict.
        """
        match = _PINIA_RE.search(document or "")
        if not match:
            raise RuntimeError(
                "No #urbnInitialPiniaState script in the document. Urban Outfitters "
                "may have changed the hydration id or moved to a different wire "
                "format; this spider deliberately has no HTML fallback."
            )
        raw = match.group(1).strip()
        try:
            state = json.loads(json.loads(raw))
        except ValueError as exc:
            raise RuntimeError(
                f"Urban Outfitters hydration state is not decodable JSON "
                f"(first 120 chars: {raw[:120]!r}): {exc}"
            ) from exc
        if not isinstance(state, dict):
            raise RuntimeError(
                "Urban Outfitters hydration state decoded to "
                f"{type(state).__name__}, expected dict; the double-decode contract "
                "may have changed."
            )
        return state

    @classmethod
    def _tiles(cls, state: dict[str, Any]) -> list[Any]:
        """``category.pages[<currentPage>].wrapper.tiles`` for the served page."""
        category = state.get("category")
        category = category if isinstance(category, dict) else {}
        pages = category.get("pages")
        pages = pages if isinstance(pages, dict) else {}
        page_key = str(category.get("currentPage") or 1)
        page = pages.get(page_key)
        if not isinstance(page, dict):
            available = sorted(pages)[:10]
            raise RuntimeError(
                f"No hydrated page {page_key} in the Urban Outfitters payload "
                f"(pages present: {available}). Pagination is driven by ?page=N, "
                "which hydrates only the page it serves."
            )
        wrapper = page.get("wrapper")
        wrapper = wrapper if isinstance(wrapper, dict) else {}
        tiles = wrapper.get("tiles")
        return tiles if isinstance(tiles, list) else []

    # ----------------------------------------------------------------- guards

    def _reject_challenge(self, response: scrapy.http.Response, what: str) -> None:
        if response.status != 200:
            raise RuntimeError(
                f"Urban Outfitters {what} returned HTTP {response.status} for {response.url}"
            )
        head = response.text[:4000].lower()
        for marker in _CHALLENGE_MARKERS:
            if marker in head:
                raise RuntimeError(
                    f"Urban Outfitters served an access-denied/challenge body for the "
                    f"{what} at {response.url} (matched {marker!r}); the request was "
                    "not answered by the storefront."
                )
        # The edge serves a "404 Not Found" stub page (HTTP 200) for query
        # patterns it blocks; it is not a category page.
        if "404 not found" in head:
            raise RuntimeError(
                f"Urban Outfitters served a 404 stub for the {what} at "
                f"{response.url}; the URL was not answered by the storefront."
            )

    # ------------------------------------------------------------------ utils

    @staticmethod
    def _html_headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        """Page 1 is the bare category URL; pages >= 2 carry ``?page=N``.

        Existing refinement params (``?color=green``) are preserved, and any
        ``page`` already on the URL is replaced rather than duplicated.
        """
        parts = urlsplit(url)
        query = [
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() != "page"
        ]
        if page > 1:
            query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _text(value: Any) -> str | None:
        if value is None:
            return None
        return str(value).strip() or None

    @staticmethod
    def _number(value: Any) -> float | int | None:
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            number: float | int = value
        else:
            try:
                number = float(str(value).strip().replace("$", "").replace(",", ""))
            except (TypeError, ValueError):
                return None
        return int(number) if float(number).is_integer() else number

    @staticmethod
    def _integer(value: Any) -> int | None:
        number = UrbanOutfittersListingSpider._number(value)
        return int(number) if number is not None else None