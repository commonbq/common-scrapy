from __future__ import annotations

"""CVS.com shop listing spider (issue #191).

CVS shop pages are a React/Stencil storefront rendered with SSR. Every PLP ships
the complete search result set as a JSON assignment in the page source::

    var initialState = {
      "allCategories": { ... },      # named shop taxonomy
      "productIndexData": {
        "numFound": 3035, "start": 0, "limit": 20, "page": 1,
        "products": [ ... ],         # 20 product objects
        "facets": {...}, "refinements": [...], "breadCrumbs": [...]
      }
    };

This spider uses exactly ONE data direction -- that bootstrap hydration state.
There is **no presentation-markup fallback and no JSON-LD fallback**: if the
assignment or its expected keys disappear the spider fails loudly rather than
silently degrading to card scraping.

Pagination is ordinary query-string SSR (``?page=N``); the same assignment
reports ``start``/``limit``/``page``/``numFound``, which drive the stop
condition without ever guessing a page count.

The category taxonomy is bundled in ``cvs_categories.py`` and was captured from
``initialState.allCategories.allCategories.children`` (see that module).
"""

import json
import re
from typing import Any, Iterable, Iterator
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.cvs_categories import CVS_CATEGORY_INVENTORY

SITE_BASE = "https://www.cvs.com"
SHOP_BASE = f"{SITE_BASE}/shop"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slugify(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")





def _load_categories() -> list[dict[str, Any]]:
    """Flatten the captured taxonomy into unique ``{category,url,...}`` rows.

    The same label can appear under two departments (e.g. "Hair Care" exists under
    both Personal Care and Beauty), so the CLI slug is namespaced with the
    department whenever the plain slug is already taken. Rows are deduplicated on
    the browse URL so every row maps to exactly one category page.
    """
    rows: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    seen_slugs: set[str] = set()

    for department, node in CVS_CATEGORY_INVENTORY.items():
        for path, entry in _walk(node, (department,)):
            url = entry.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            name = path[-1]
            slug = _slugify(name)
            if slug in seen_slugs:
                slug = f"{_slugify(department)}-{slug}"
            # A label can repeat inside one department too (CVS cross-lists e.g.
            # "Compression Hosiery & Stockings" under two Home Health Care
            # branches), so fall back to a path-qualified slug, then a counter.
            if slug in seen_slugs:
                slug = "-".join(_slugify(part) for part in path)
            suffix = 2
            unique = slug
            while unique in seen_slugs:
                unique = f"{slug}-{suffix}"
                suffix += 1
            seen_slugs.add(unique)
            rows.append(
                {
                    "category": unique,
                    "name": name,
                    "url": f"{SITE_BASE}{url}",
                    "department": department,
                    "breadcrumb": list(path),
                    "category_id": entry.get("id"),
                }
            )
    return rows


def _walk(
    node: dict[str, Any], path: tuple[str, ...]
) -> Iterator[tuple[tuple[str, ...], dict[str, Any]]]:
    """Yield ``(path, entry)`` for ``node`` and its descendants, root first.

    The taxonomy module keys subcategories by their display label, so the label is
    threaded in from the mapping key on the way down instead of being stored on the
    node itself.
    """
    yield path, node
    for label, child in (node.get("subcategories") or {}).items():
        if isinstance(child, dict):
            yield from _walk(child, path + (label,))


class CvsListingSpider(BaseListingSpider):
    """Parse CVS PLPs from the ``productIndexData`` bootstrap assignment."""

    name = "cvs_listing"
    allowed_domains = ["cvs.com", "www.cvs.com"]

    # Direct url=/category_url= runs are supported, so opt out of the base class
    # category-only gate; __init__ still rejects a run with no target at all.
    require_category_arg = False

    categories = _load_categories()

    custom_settings = {
        # Each PLP is a ~3.9 MB SSR document; stay polite on one host.
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "brand",
            "url",
            "image",
            "price",
            "original_price",
            "sale_price",
            "carepass_price",
            "unit_price",
            "currency",
            "in_stock",
            "stock_quantity",
            "store_pickup",
            "pickup_in_stock",
            "same_day_in_stock",
            "rating",
            "reviews_count",
            "is_new",
            "is_featured",
            "is_sponsored",
            "hot_deals",
            "fsa_eligible",
            "promo_message",
            "size",
            "count",
            "category",
            "category_name",
            "category_id",
            "department",
            "breadcrumb",
            "page",
            "position",
            "total_count",
            "source_url",
            "source",
            "raw",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{SITE_BASE}/",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                "Available categories: "
                f"{', '.join(self.available_categories()[:20])}"
            )
        # Fail at construction rather than mid-crawl: an unknown slug is a typo,
        # not a crawl to discover on page 2.
        self.resolve_target_url()
        self._seen: set[str] = set()

    # ----------------------------------------------------------------- requests

    def start_requests(self) -> Iterable[scrapy.Request]:
        url = self.resolve_target_url()
        yield self._page_request(url, page=1)

    def _page_request(self, url: str, page: int) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(url, page),
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"listing_url": url, "page": page},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        """Return ``url`` with the ``page`` query parameter set to ``page``."""
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if page <= 1:
            query.pop("page", None)
        else:
            query["page"] = str(page)
        return urlunsplit(
            (parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)
        )

    # ------------------------------------------------------------------- parse

    def parse(self, response: scrapy.http.Response, listing_url: str, page: int):
        if response.status != 200:
            raise RuntimeError(
                f"CVS listing returned HTTP {response.status}: {response.url}"
            )

        payload = self._extract_product_index(response.text, response.url)
        products = payload.get("products")
        if not isinstance(products, list):
            raise RuntimeError(
                f"CVS productIndexData has no products list at {response.url}: "
                f"keys={sorted(payload)[:12]}"
            )

        entry = self._entry_for(listing_url)
        total = self._integer(payload.get("numFound"))
        limit = self._integer(payload.get("limit")) or len(products)
        start = self._integer(payload.get("start"))

        emitted = 0
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item = self._item(product, entry, response, page, position, total)
            if item is None:
                continue
            emitted += 1
            yield item

        if not products or emitted == 0:
            self.logger.info(
                "CVS listing page %s produced no new products (%s products in state); "
                "pagination stopped",
                page,
                len(products),
            )
            return

        if page >= self.max_pages:
            return
        if limit and start is not None and start + limit >= total:
            return
        yield self._page_request(listing_url, page + 1)

    @staticmethod
    def _extract_product_index(text: str, url: str) -> dict[str, Any]:
        """Brace-match the ``var productIndexData = {...};`` assignment."""
        match = re.search(r"var\s+productIndexData\s*=\s*", text)
        if not match:
            raise RuntimeError(
                f"CVS page has no 'var productIndexData =' assignment at {url}; the "
                "bootstrap hydration contract changed and there is no markup fallback."
            )
        decoder = json.JSONDecoder()
        try:
            payload, _ = decoder.raw_decode(text[match.end():].lstrip())
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"CVS productIndexData is not valid JSON at {url}: {exc}"
            ) from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"CVS productIndexData is not an object at {url}")
        return payload

    def _entry_for(self, listing_url: str) -> dict[str, Any]:
        for entry in self.categories:
            if entry["url"] == listing_url:
                return entry
        return {
            "category": _slugify(urlsplit(listing_url).path.rstrip("/").rsplit("/", 1)[-1]),
            "name": None,
            "url": listing_url,
            "department": None,
            "breadcrumb": [],
            "category_id": None,
        }

    # -------------------------------------------------------------------- item

    def _item(
        self,
        product: dict[str, Any],
        entry: dict[str, Any],
        response: scrapy.http.Response,
        page: int,
        position: int,
        total: int | None,
    ) -> dict[str, Any] | None:
        item_id = self._text(product.get("id"))
        if not item_id or item_id in self._seen:
            return None
        self._seen.add(item_id)

        price_info = product.get("priceInfo")
        price_info = price_info if isinstance(price_info, dict) else {}
        variant = product.get("defaultVariant")
        variant = variant if isinstance(variant, dict) else {}
        inventory = variant.get("inventoryInfo")
        inventory = inventory if isinstance(inventory, dict) else {}
        ship = inventory.get("shipInv") if isinstance(inventory.get("shipInv"), dict) else {}
        pick = inventory.get("pickInv") if isinstance(inventory.get("pickInv"), dict) else {}
        sdd = inventory.get("sddInv") if isinstance(inventory.get("sddInv"), dict) else {}
        coupons = variant.get("coupons") if isinstance(variant.get("coupons"), dict) else {}
        variants = [v for v in (product.get("variants") or []) if isinstance(v, dict)]

        list_price = self._number(price_info.get("listPrice"))
        sale_price = self._number(price_info.get("salePrice"))
        # CVS marks a real markdown with salePrice < listPrice; otherwise salePrice
        # simply mirrors listPrice and reporting it as a discount would be wrong.
        price = sale_price or list_price
        on_sale = bool(list_price and sale_price and sale_price < list_price)

        stock_status = self._text(ship.get("locationAvailabilityStatus"))
        return {
            "item_id": item_id,
            "title": self._text(product.get("title")) or self._text(variant.get("displayName")),
            "brand": self._text(product.get("brand")),
            "url": self._absolute(product.get("url")),
            "image": self._absolute(
                variant.get("skuImageUrl")
                or variant.get("skuSwatchImage")
                or product.get("skuDynamicImageUrl")
            ),
            "price": price,
            "original_price": list_price if on_sale else None,
            "sale_price": sale_price if on_sale else None,
            "carepass_price": self._positive_number(price_info.get("carepassPrice")),
            "unit_price": self._text(price_info.get("unitPrice")),
            "currency": "USD",
            "in_stock": self._status_flag(stock_status),
            "stock_quantity": self._integer(ship.get("locationAvailableToPromiseQuantity")),
            "store_pickup": self._flag(variant.get("storePickUpIndicator")),
            "pickup_in_stock": self._status_flag(
                self._text(pick.get("locationAvailabilityStatus"))
            ),
            "same_day_in_stock": self._status_flag(
                self._text(sdd.get("locationAvailabilityStatus"))
            ),
            "rating": self._number(variant.get("averageOverallRating")),
            "reviews_count": self._integer(variant.get("totalReviewCount")),
            "is_new": self._flag(product.get("isNewProduct")),
            "is_featured": self._flag(product.get("isFeatured")),
            "is_sponsored": self._flag(product.get("isSponsored")),
            "hot_deals": self._flag(variant.get("hotDealsIndicator")),
            "fsa_eligible": self._flag(variant.get("fsaIndicator")),
            "promo_message": self._text(price_info.get("promoDescription"))
            or self._text(coupons.get("promoDescription")),
            "size": self._text(variant.get("skuSize")),
            "count": self._text(variant.get("skuCount")),
            "category": entry.get("category"),
            "category_name": entry.get("name"),
            "category_id": entry.get("category_id"),
            "department": entry.get("department"),
            "breadcrumb": entry.get("breadcrumb") or None,
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": "cvs_product_index_hydration",
            # Verbatim hydration entry: variant-level differences (size, price,
            # availability) that the PLP grid does not surface stay re-derivable.
            "raw": {"product": product, "variants": variants},
        }

    @staticmethod
    def _absolute(value: Any) -> str | None:
        text = CvsListingSpider._text(value)
        if not text:
            return None
        if text.startswith("//"):
            return f"https:{text}"
        if text.startswith(("http://", "https://")):
            return text
        return f"{SITE_BASE}{text if text.startswith('/') else '/' + text}"

    @staticmethod
    def _status_flag(status: str | None) -> bool | None:
        if not status:
            return None
        return status.upper() == "IN_STOCK"

    @staticmethod
    def _flag(value: Any) -> bool | None:
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in ("true", "yes", "1"):
                return True
            if lowered in ("false", "no", "0"):
                return False
        return None

    @staticmethod
    def _text(value: Any) -> str | None:
        if value is None or isinstance(value, (dict, list, bool)):
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _number(value: Any) -> float | None:
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, str):
            match = re.search(r"-?\d[\d,]*(?:\.\d+)?", value)
            if not match:
                return None
            value = match.group(0).replace(",", "")
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def _positive_number(cls, value: Any) -> float | None:
        """Parse ``value``, treating 0 as "absent".

        CVS emits ``"0.0"`` for every optional price it does not have (CarePass,
        for example), so a zero means "no value" rather than a free product.
        """
        number = cls._number(value)
        return number or None

    @staticmethod
    def _integer(value: Any) -> int | None:
        number = CvsListingSpider._number(value)
        return int(number) if number is not None else None