from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.michaels_categories import (
    MICHAELS_CATEGORY_SITEMAP_URL,
    MICHAELS_SITE_BASE,
    available_categories,
    parse_category_sitemap,
    resolve_category,
)

# React Server Component flight chunks are pushed as
# `self.__next_f.push([1,"<JSON string literal>"])`. The literal is matched with a
# full JS-string escape class rather than a lazy `.*?` so an escaped `\"` inside
# the payload cannot terminate the match early.
_FLIGHT_CHUNK_RE = re.compile(
    r"self\.__next_f\.push\(\[\s*1\s*,\s*(\"(?:[^\"\\]|\\.)*\")\s*\]\)",
    re.DOTALL,
)

# The RSC protocol serialises absent values as the literal string "$undefined"
# and unresolvable client references as "$<id>" / "$L<id>" / "$@<id>". Left in
# place they pollute every exported CSV row, so they are normalised to None.
_RSC_SENTINEL_RE = re.compile(r"^\$(?:undefined|@?[0-9A-Za-z_$][\w$]*|D[\w.+-]*|I-?[\w.]*|n)$")

# Body markers of an anti-bot interstitial served with HTTP 200. Michaels sits
# behind Akamai, so a PLP can come back as a challenge page with no flight data.
_CHALLENGE_MARKERS = (
    "access denied",
    "are you a human",
    "captcha",
    "reference #",
    "request unsuccessful",
)

_BADGE_LABELS = {
    "sale": "Sale",
    "clearance": "Clearance",
    "newPdt": "New",
    "greatBuy": "Great Buy",
    "everydayValue": "Everyday Value",
    "doorbuster": "Doorbuster",
    "comingSoon": "Coming Soon",
    "michaelsExclusive": "Michaels Exclusive",
    "michaelsProPack": "Michaels Pro Pack",
    "shipsForFree": "Free Shipping",
    "sameDayDeliveryBadge": "Same Day Delivery",
    "notAvailableToShip": "Store Only",
    "onlineOnly": "Online Only",
    "freeStorePickup": "Free Store Pickup",
    "couponExclusion": "Coupon Excluded",
    "globalNonDiscountable": "Not Discountable",
}


class MichaelsListingSpider(BaseListingSpider):
    """Michaels listings from the Next.js App Router RSC hydration payload.

    Michaels is a Next.js App Router storefront, so there is no
    ``__NEXT_DATA__`` blob: the server streams React Server Components through
    ``self.__next_f.push(...)``. Concatenating those chunks yields one text
    buffer in which the whole product grid -- 40 rows, fully priced, rated and
    badged -- is already present as ``initialProducts``, next to
    ``initialTotal`` (the true category size) and ``initialFilters`` (facets with
    counts). Nothing has to be re-requested client-side and nothing is scraped
    out of rendered DOM, so this spider uses exactly one data direction: the
    server-rendered hydration state.

    Pagination is plain SSR: ``?page=<N>`` re-renders the route and hydrates the
    next window. A page past the end comes back as a valid document with
    ``initialProducts: []`` and ``initialTotal: 0``, so it ends the crawl instead
    of erroring.

    Category inventory comes from the sitemap (see
    :mod:`common.spiders.michaels_categories`) -- the one other request this
    spider makes, and it exists only to resolve ``-a category=`` to a PLP URL and
    to label items with their department.
    """

    name = "michaels_listing"
    allowed_domains = [
        "michaels.com",
        "www.michaels.com",
        "localhost",
        "127.0.0.1",
    ]

    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "item_id", "sku",
            "master_sku", "title", "brand", "product_category", "taxonomy_path",
            "url", "image_url", "image_urls", "image_count", "price",
            "original_price", "currency", "on_sale", "rating", "reviews_count",
            "color", "color_count", "variant_count", "badges", "promotion_message",
            "promotion_expiry", "store_pickup", "same_day_delivery",
            "ships_for_free", "available_to_ship", "in_stock", "is_sponsored",
            "is_exclusive", "is_online_only", "is_pro_pack", "is_bundle",
            "page", "position", "total_count", "source_url", "source", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<slug>, category_url=<url>, or url=<url>, "
                "e.g. -a category=floral-arrangements. Categories are loaded from "
                f"{MICHAELS_CATEGORY_SITEMAP_URL}."
            )
        self._seen_products: set[str] = set()
        self._categories: list[dict[str, str]] = []
        self._target: dict[str, str] | None = None

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_products.clear()
        yield scrapy.Request(
            MICHAELS_CATEGORY_SITEMAP_URL,
            callback=self.parse_category_sitemap,
            headers=self._html_headers(),
            dont_filter=True,
        )

    def parse_category_sitemap(self, response: scrapy.http.Response):
        self._reject_challenge(response, "category sitemap")
        categories = parse_category_sitemap(response.text)
        if not categories:
            raise RuntimeError(
                f"No /shop/ category URLs found in {response.url}. The sitemap "
                "contract may have changed, or the response was not the sitemap."
            )
        self._categories = categories
        departments = {entry["department"] for entry in categories}
        self.logger.info(
            "Michaels category sitemap: %d categories across %d departments",
            len(categories),
            len(departments),
        )

        target = resolve_category(
            categories,
            category=self.category,
            category_url=self.category_url,
            url=self.url,
        )
        if target is None:
            # An unknown slug is a user error and should say so immediately
            # rather than after a full page render.
            raise ValueError(
                f"Unknown Michaels category {self.category or self.category_url or self.url!r}. "
                f"{len(categories)} categories are in the sitemap; examples: "
                f"{', '.join(available_categories(categories))}. Pass a slug from "
                f"{MICHAELS_CATEGORY_SITEMAP_URL}, or -a category_url=/shop/<path>/."
            )
        self._target = target
        yield scrapy.Request(
            target["url"],
            callback=self.parse,
            headers=self._html_headers(),
            meta={"category": target, "page": 1, "base_url": target["url"]},
        )

    # ------------------------------------------------------------------- parse

    def parse(self, response: scrapy.http.Response):
        self._reject_challenge(response, "category page")
        target: dict[str, str] = response.meta["category"]
        page = int(response.meta.get("page", 1))

        flight = self._flight_payload(response.text)
        products = self._initial_products(flight)
        total_count = self._initial_total(flight)
        filters = self._initial_filters(flight)

        if not products:
            # A page past the end renders a valid document with an empty grid.
            if page > 1:
                self.logger.info(
                    "Stopping at %s page %s: no hydrated products",
                    target["category"],
                    page,
                )
                return
            raise RuntimeError(
                f"No initialProducts in the Michaels hydration payload at "
                f"{response.url} (total={total_count}, facets={len(filters)}). "
                "The category may be a campaign landing page with no PLP grid."
            )

        self.logger.info(
            "Michaels %s page %s: %d products (total %s, facets %s)",
            target["category"],
            page,
            len(products),
            total_count,
            len(filters),
        )

        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("skuNumber") or product.get("id") or "").strip()
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, target, response, page, position, total_count)

        if page >= self.max_pages:
            return
        if total_count and page * len(products) >= total_count:
            return
        base_url = response.meta.get("base_url") or target["url"]
        yield scrapy.Request(
            self._with_page(base_url, page + 1),
            callback=self.parse,
            headers=self._html_headers(),
            meta={**response.meta, "page": page + 1},
        )

    # ----------------------------------------------------------------- helpers

    def _item(
        self,
        product: dict[str, Any],
        target: dict[str, str],
        response: scrapy.http.Response,
        page: int,
        position: int,
        total_count: int | None,
    ) -> dict[str, Any]:
        raw = self._clean_rsc(product)
        price = self._number(raw.get("price"))
        original_price = self._number(raw.get("originalPrice"))
        badges = raw.get("badges") if isinstance(raw.get("badges"), dict) else {}
        availability = raw.get("availability") if isinstance(raw.get("availability"), dict) else {}
        images = [str(url) for url in raw.get("images") or [] if url]
        analytics = raw.get("analyticsProductDetailView")
        analytics = analytics if isinstance(analytics, dict) else {}
        swatches = raw.get("colorSwatches") if isinstance(raw.get("colorSwatches"), list) else []
        pdp_url = str(raw.get("pdpUrl") or "").strip()

        on_sale = bool(raw.get("badge")) or bool(badges.get("sale")) or (
            original_price is not None and price is not None and original_price > price
        )
        discount_percentage = None
        if on_sale and original_price and price and original_price > price:
            discount_percentage = round((original_price - price) / original_price * 100, 2)

        return {
            "category": target["category"],
            "department": target["department"],
            "subcategory": target["subcategory"],
            "item_id": str(raw.get("skuNumber") or raw.get("id") or ""),
            "sku": raw.get("skuNumber"),
            "master_sku": raw.get("masterSku"),
            "title": raw.get("name"),
            "brand": raw.get("brand"),
            "product_category": raw.get("category"),
            "taxonomy_path": analytics.get("fullTaxonomyPath"),
            "url": urljoin(MICHAELS_SITE_BASE + "/", pdp_url) if pdp_url else None,
            "image_url": raw.get("image"),
            "image_urls": images,
            "image_count": len(images) or None,
            "price": price,
            "original_price": original_price,
            "currency": "USD" if price is not None else None,
            "on_sale": on_sale,
            "rating": self._number(raw.get("rating")),
            "reviews_count": self._number(raw.get("reviewCount")),
            "color": raw.get("color"),
            "color_count": len(swatches) or None,
            "variant_count": raw.get("variantCount") or None,
            "badges": self._badges(badges),
            "promotion_message": raw.get("promotionMessage"),
            "promotion_expiry": raw.get("promotionExpiry"),
            "store_pickup": availability.get("storePickup"),
            "same_day_delivery": badges.get("sameDayDeliveryBadge"),
            "ships_for_free": badges.get("shipsForFree"),
            "available_to_ship": availability.get("shipToMe"),
            "in_stock": (
                bool(availability.get("shipToMe")) or bool(availability.get("storePickup"))
            ),
            "is_sponsored": raw.get("isSponsored"),
            "is_exclusive": raw.get("isExclusive"),
            "is_online_only": badges.get("onlineOnly") or raw.get("isOnlineOnly"),
            "is_pro_pack": raw.get("isProPack"),
            "is_bundle": raw.get("isBundle"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "michaels_nextjs_rsc_initial_products",
            # The protocol sentinels ("$undefined") are stripped so an exported
            # row carries the values the storefront actually renders.
            "raw": raw,
        }

    @classmethod
    def _badges(cls, badges: dict[str, Any]) -> list[str]:
        """Flatten the boolean badge map into the labels the PLP renders."""
        return [
            label
            for key, label in _BADGE_LABELS.items()
            if badges.get(key) is True
        ]

    @classmethod
    def _flight_payload(cls, document: str) -> str:
        """Concatenate every ``self.__next_f.push`` chunk into one text buffer."""
        chunks = _FLIGHT_CHUNK_RE.findall(document or "")
        if not chunks:
            raise RuntimeError(
                "No self.__next_f flight chunks in the document. Michaels may have "
                "moved off the React Server Component wire format, or the response "
                "was not a rendered App Router page."
            )
        # Each chunk is a JSON string literal; json.loads unwraps the escaping.
        return "".join(json.loads(chunk) for chunk in chunks)

    @classmethod
    def _decode_prop(cls, payload: str, name: str, expected: type) -> Any:
        """Decode the value of a top-level prop inside the flight buffer."""
        match = re.search(rf'"{re.escape(name)}":', payload)
        if not match:
            raise RuntimeError(
                f"The Michaels hydration payload has no {name!r} prop. Expected the "
                f"PLP RSC payload; found props: "
                f"{sorted(set(re.findall(r'\"(initial[A-Za-z]+)\":', payload))) or 'none'}."
            )
        start = match.end()
        while start < len(payload) and payload[start] in " \t\r\n":
            start += 1
        try:
            value, _ = json.JSONDecoder().raw_decode(payload, start)
        except ValueError as exc:
            raise RuntimeError(
                f"Michaels {name!r} prop is not decodable JSON at offset {start}: {exc}"
            ) from exc
        if not isinstance(value, expected):
            raise RuntimeError(
                f"Michaels {name!r} is {type(value).__name__}, expected "
                f"{expected.__name__}; the RSC contract may have changed."
            )
        return value

    @classmethod
    def _initial_products(cls, payload: str) -> list[Any]:
        return cls._decode_prop(payload, "initialProducts", list)

    @classmethod
    def _initial_filters(cls, payload: str) -> list[Any]:
        try:
            return cls._decode_prop(payload, "initialFilters", list)
        except RuntimeError:
            return []

    @classmethod
    def _initial_total(cls, payload: str) -> int | None:
        match = re.search(r'"initialTotal":\s*(\d+)', payload)
        return int(match.group(1)) if match else None

    @classmethod
    def _clean_rsc(cls, value: Any) -> Any:
        """Recursively drop RSC sentinels so exported values are real values."""
        if isinstance(value, str):
            return None if _RSC_SENTINEL_RE.match(value) else value
        if isinstance(value, list):
            return [cls._clean_rsc(entry) for entry in value]
        if isinstance(value, dict):
            return {key: cls._clean_rsc(entry) for key, entry in value.items()}
        return value

    def _reject_challenge(self, response: scrapy.http.Response, what: str) -> None:
        if response.status != 200:
            raise RuntimeError(
                f"Michaels {what} returned HTTP {response.status} for {response.url}"
            )
        head = response.text[:4000].lower()
        for marker in _CHALLENGE_MARKERS:
            if marker in head:
                raise RuntimeError(
                    f"Michaels served an access-denied/challenge body for the {what} "
                    f"at {response.url} (matched {marker!r}); the request was not "
                    "answered by the storefront."
                )

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
    def _with_page(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != "page"]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _number(value: Any) -> float | int | None:
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            text = str(value).strip().replace("$", "").replace(",", "")
            return float(text) if "." in text else int(text)
        except (TypeError, ValueError):
            return None