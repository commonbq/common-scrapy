from __future__ import annotations

import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit, parse_qsl, urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.belk_categories import BELK_API_BASE, BELK_BASE_URL, BELK_CATEGORIES


class BelkListingSpider(BaseListingSpider):
    """Belk category listings from the first-party search facade.

    Belk is a Next.js App Router site whose category HTML hydration deliberately does *not*
    contain product records. The client calls one first-party JSON endpoint instead:

        https://www.belk.com/ecom/cio/v1/web/category/{categoryPath}?v2=true

    That single endpoint is the only data source this spider uses -- there is no HTML or
    JSON-LD fallback. Pagination is offset based (``start`` / ``sz``), and the response
    carries the complete product tile payload (brand, price ranges, coupons, badges,
    swatches, ratings) plus ``header.count`` and ``pagination.navs``.
    """

    name = "belk_listing"
    allowed_domains = ["belk.com", "www.belk.com", "localhost", "127.0.0.1"]
    categories = BELK_CATEGORIES
    require_category_arg = False

    PAGE_SIZE = 60

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "category_id", "category_title",
            "item_id", "title", "brand", "url", "image_url", "price", "original_price",
            "currency", "discount_percent", "rating", "reviews_count", "badge",
            "coupon_code", "coupon_discount_percent", "coupon_price", "coupon_end_date",
            "promotions", "color", "swatches", "marketplace", "breadcrumb", "page",
            "position", "total_count", "items_per_page", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<path>, category_url=<url>, or url=<api url>. "
                f"belk_categories.py defines {len(self.available_categories())} browse paths, "
                "e.g. 'home/home-decor'."
            )
        self._seen_products: set[str] = set()

    # ------------------------------------------------------------------ request side

    def start_requests(self):
        self._seen_products.clear()
        yield scrapy.Request(
            self._first_api_url(),
            callback=self.parse,
            headers=self._api_headers(),
            meta={"page": 1, **self._meta()},
        )

    def _first_api_url(self) -> str:
        """Resolve the page-1 API URL from -a url / -a category_url / -a category."""
        if self.url:
            return self._as_api_url(self.url)
        if self.category_url:
            return self._as_api_url(self.category_url)

        entry = self._category_entry(self.category)
        if entry is None:
            available = self.available_categories()
            raise ValueError(
                f"Unknown category {self.category!r}. Pass a full browse path from "
                f"belk_categories.py (e.g. 'home/home-decor'), or one of the {len(available)} "
                f"available paths, e.g. " + ", ".join(available[:5]) + "."
            )
        return entry["url"]

    @classmethod
    def _as_api_url(cls, value: str) -> str:
        """Accept either a browse page URL or a ready-made API URL and return the API URL."""
        candidate = value.strip()
        if "/ecom/cio/v1/web/" in candidate:
            return candidate
        path = cls.browse_path(candidate)
        if not path:
            raise ValueError(f"Cannot build a Belk category API URL from {value!r}")
        return f"{BELK_API_BASE}/category/{path}?v2=true"

    def _category_entry(self, category: str | None) -> dict | None:
        """Look a category up by full browse path, then by unique trailing segment."""
        if not category:
            return None
        wanted = category.strip().strip("/")
        for entry in self.categories:
            if entry["category"] == wanted:
                return entry
        tail = "/" + wanted
        matches = [entry for entry in self.categories if entry["category"].endswith(tail)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            names = ", ".join(sorted(entry["category"] for entry in matches))
            raise ValueError(
                f"Ambiguous category '{category}'. It matches {len(matches)} categories: {names}"
            )
        return None

    def _meta(self) -> dict:
        """Taxonomy context for the crawl target.

        ``-a category_url=`` / ``-a url=`` are resolved back through the inventory too, so
        department/subcategory are populated whichever argument form was used.
        """
        entry = None
        if self.category:
            entry = self._category_entry(self.category)
        else:
            for candidate in (self.category_url, self.url):
                if candidate:
                    entry = self._category_entry(self.browse_path(candidate))
                    if entry:
                        break
        entry = entry or {}
        return {
            "category": entry.get("category") or self.category or "custom",
            "department": entry.get("department"),
            "subcategory": entry.get("subcategory"),
            "category_id": entry.get("cgid"),
            "site_url": entry.get("site_url"),
        }

    @staticmethod
    def browse_path(value: str) -> str:
        """Extract the browse path from a Belk URL or a ready-made category API URL."""
        path = urlsplit(value.strip()).path.strip("/")
        # `path` has no leading slash here, so match the API prefix without one.
        marker = "ecom/cio/v1/web/category/"
        if marker in path:
            return path.split(marker, 1)[1]
        return path

    # ------------------------------------------------------------------ response side

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Belk listing API returned HTTP {response.status}: {response.url}")

        payload = self._json_body(response)
        redirect = self._redirect_hint(payload)
        if redirect:
            raise RuntimeError(
                f"Belk category {response.meta.get('category')!r} is a landing page, not a "
                f"product listing; the API redirects to {redirect}. Pick a browse category "
                "from belk_categories.py instead."
            )

        tiles = payload.get("product_tiles")
        if not isinstance(tiles, list):
            missing = self._category_missing(payload)
            if missing:
                raise RuntimeError(
                    f"Belk API does not know category {response.meta.get('category')!r} "
                    f"({missing}). It is in belk_categories.py but is not resolvable by the "
                    f"listing API: {response.url}"
                )
            raise RuntimeError(
                f"Belk API response has no list-valued 'product_tiles' (keys: "
                f"{sorted(payload)}): {response.url}"
            )
        if not tiles:
            raise RuntimeError(
                f"Belk API returned zero product tiles for {response.meta.get('category')!r}: "
                f"{response.url}"
            )

        page = int(response.meta.get("page", 1))
        header = payload.get("header") if isinstance(payload.get("header"), dict) else {}
        meta_data = payload.get("metaData") if isinstance(payload.get("metaData"), dict) else {}
        breadcrumb = [
            crumb.get("name")
            for crumb in (payload.get("breadcrumb") or [])
            if isinstance(crumb, dict) and crumb.get("name")
        ]

        emitted = 0
        for tile in tiles:
            if not isinstance(tile, dict):
                continue
            item_id = str(tile.get("id") or "").strip()
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            emitted += 1
            yield self._item(
                tile,
                response=response,
                page=page,
                position=emitted,
                header=header,
                category_title=header.get("title"),
                category_id=meta_data.get("cgid"),
                breadcrumb=breadcrumb,
            )

        if page >= self.max_pages:
            return
        next_url = self._next_url(response.url, payload, page)
        if next_url:
            yield response.follow(
                next_url,
                callback=self.parse,
                headers=self._api_headers(),
                meta={**response.meta, "page": page + 1},
            )

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _json_body(response) -> dict:
        body = response.text or ""
        try:
            payload = json.loads(body)
        except ValueError as error:
            raise RuntimeError(
                f"Belk API did not return JSON ({response.status}, {len(body)} bytes, "
                f"content-type {response.headers.get('Content-Type')!r}): {body[:200]!r}"
            ) from error
        if not isinstance(payload, dict):
            raise RuntimeError(f"Belk API returned {type(payload).__name__}, expected an object: {response.url}")
        return payload

    @staticmethod
    def _redirect_hint(payload: dict) -> str | None:
        """Landing pages answer with {"metaData": {"redirectUrl": ...}} and no tiles."""
        meta_data = payload.get("metaData")
        if isinstance(meta_data, dict) and meta_data.get("redirectUrl"):
            return meta_data["redirectUrl"]
        return None

    @staticmethod
    def _category_missing(payload: dict) -> str | None:
        """Unknown paths answer with {"status": 404, "message": "Category not found ..."}."""
        if payload.get("status") in (404, "404") and payload.get("message"):
            return str(payload["message"])
        return None

    def _next_url(self, current_url: str, payload: dict, page: int) -> str | None:
        """Build the next page's absolute API URL.

        The API advertises offset pagination itself through ``pagination.navs[*].params``
        (``start=60&sz=60``); those params win when present. Otherwise the offset is simply
        stepped by PAGE_SIZE, and the run stops once ``header.count`` says we are past the end.
        """
        params = {"v2": "true"}
        pagination = payload.get("pagination") if isinstance(payload.get("pagination"), dict) else {}
        for nav in pagination.get("navs") or []:
            if isinstance(nav, dict) and not nav.get("selected") and nav.get("params"):
                params.update(dict(parse_qsl(str(nav["params"]))))
                break
        else:
            count = self._integer(self._mapping(payload.get("header")).get("count"))
            if count is not None and count <= page * self.PAGE_SIZE:
                return None
            params["start"] = str(page * self.PAGE_SIZE)
            params["sz"] = str(self.PAGE_SIZE)

        split = urlsplit(current_url)
        return urlunsplit(
            (split.scheme, split.netloc, split.path, urlencode(params), "")
        )

    @staticmethod
    def _mapping(value):
        return value if isinstance(value, dict) else {}

    def _item(self, tile, *, response, page, position, header, category_title,
              category_id, breadcrumb) -> dict:
        price = self._mapping(tile.get("price"))
        original = self._price_min(price.get("orig"))
        sale = self._price_min(price.get("sale"))
        effective = sale if sale is not None else original
        coupon = self._first_coupon(tile.get("coupons"))
        swatches = tile.get("swatches") if isinstance(tile.get("swatches"), list) else []
        swatch_colors = [
            swatch.get("color") for swatch in swatches
            if isinstance(swatch, dict) and swatch.get("color")
        ]
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "category_id": category_id or response.meta.get("category_id"),
            "category_title": category_title,
            "item_id": str(tile.get("id") or ""),
            "title": tile.get("title"),
            "brand": tile.get("brand"),
            "url": self._absolute(tile.get("url")),
            "image_url": tile.get("image"),
            "price": effective,
            "original_price": original,
            "currency": "USD",
            "discount_percent": self._discount_percent(original, effective),
            "rating": self._number(tile.get("ratingValue")),
            "reviews_count": self._integer(tile.get("reviewCount")),
            "badge": tile.get("badge"),
            "coupon_code": self._mapping(coupon).get("couponCode"),
            "coupon_discount_percent": self._number(self._mapping(coupon).get("cpnDiscount")),
            "coupon_price": self._price_min(self._mapping(coupon).get("promoPrice")),
            "coupon_end_date": self._mapping(coupon).get("endDate"),
            "promotions": self._promotions(tile.get("promotions")),
            "color": swatch_colors[0] if swatch_colors else None,
            "swatches": swatch_colors,
            "marketplace": tile.get("mirakl") if isinstance(tile.get("mirakl"), bool) else None,
            "breadcrumb": breadcrumb,
            "page": page,
            "position": position,
            "total_count": self._integer(header.get("count")),
            "items_per_page": self.PAGE_SIZE,
            "source_url": response.url,
            "source": "belk_cio_category_api",
            "raw": tile,
        }

    @staticmethod
    def _absolute(url):
        if not url:
            return None
        return url if str(url).startswith("http") else urljoin(BELK_BASE_URL, str(url))

    @staticmethod
    def _first_coupon(coupons):
        for coupon in coupons or []:
            if isinstance(coupon, dict):
                return coupon
        return None

    @staticmethod
    def _promotions(promotions):
        """Marketing messages such as {"type": "BOGO", "message": "Buy 1, Get 1 Free"}."""
        messages = []
        for promotion in promotions or []:
            if isinstance(promotion, dict) and promotion.get("message"):
                messages.append(
                    f"{promotion['type']}: {promotion['message']}"
                    if promotion.get("type")
                    else str(promotion["message"])
                )
        return messages

    @staticmethod
    def _price_min(node):
        if not isinstance(node, dict):
            return None
        value = node.get("min")
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _discount_percent(original, sale):
        if not original or sale is None or sale >= original:
            return None
        return round((original - sale) / original * 100, 2)

    @staticmethod
    def _number(value):
        if isinstance(value, str):
            match = re.search(r"-?\d+(?:\.\d+)?", value)
            value = match.group(0) if match else None
        if value is None or isinstance(value, bool):
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        """Parse counts. Belk sends them as display strings: "353", "1.0", "10,000+"."""
        if isinstance(value, str):
            # header.count is capped: "10,000+" means ">= 10000".
            value = value.replace(",", "").replace("+", "").strip()
        if value is None or isinstance(value, bool):
            return None
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _api_headers():
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "referer": BELK_BASE_URL,
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
        }
