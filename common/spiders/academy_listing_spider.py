from __future__ import annotations

"""Academy Sports + Outdoors listing spider (issue #132).

Academy is a React SSR storefront (not Next.js).  It ships one hydration
assignment per component into ``window.ASOData``, keyed by a rotating
``comp-blt<...>`` id, and exposes its catalog through a first-party JSON API.

This spider uses exactly ONE data direction -- the first-party category API:

    GET https://www.academy.com/api/category/v3/{categoryId}
        ?web=true&displayFacets=true&recordsPerPage=N&pageNumber=P

There is **no HTML / JSON-LD fallback**: if the API stops answering the spider
fails loudly instead of silently degrading.  ``pageNumber`` is 1-based on this
endpoint (``page=1`` returns the first slice), and ``nbHits``/``nbPages`` in the
same payload drive the stop condition.

The category taxonomy is bundled in ``academy_categories.py`` (captured from the
global header's ``window.ASOData`` component registry, see that module).

Academy fronts the site with PerimeterX: a datacenter request to ``/c/...``
returns a stub, and the JSON API additionally needs ``bypass=5`` on the
ScrapeOps username.  ``_api_proxy()`` adds that option for API requests.

Flow:
    category (or all categories)
        -> /api/category/v3/{categoryId} (pageNumber=1..max_pages)
        -> emit one item per hit
        -> repeat until max_pages, an empty page, or nbPages exhausted
"""

import json
import re
from typing import Any
from urllib.parse import quote, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.academy_categories import ACADEMY_CATEGORY_INVENTORY

SITE_BASE = "https://www.academy.com"
CATEGORY_ENDPOINT = f"{SITE_BASE}/api/category/v3/"
PDP_BASE = f"{SITE_BASE}/p/"
PAGE_SIZE = 48
IMAGE_BASE = "https://academy.scene7.com/is/image/academy/"

# ScrapeOps option appended to the proxy username for the category API.  The
# plain datacenter route returns PerimeterX stub HTML instead of JSON;
# `bypass=5` was the lightest level that returned product JSON.
API_BYPASS = 5

_SLUG_RE = re.compile(r"[^a-z0-9]+")

# An HTML/JSON body where a product payload was expected means a bot wall or a
# geo-block rather than data. Matched case-insensitively: the WAF varies casing.
CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "are you a human",
    "request unsuccessful",
    "site unavailable",
    "pardon the interruption",
    "perimeterx",
    "_px",
)


def _slugify(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def _iter_nodes(node: dict[str, Any]):
    yield node
    for child in node.get("subcategories") or []:
        if isinstance(child, dict):
            yield from _iter_nodes(child)


def _load_categories() -> list[dict[str, Any]]:
    """Flatten the header taxonomy into unique ``{category,url,...}`` rows.

    Cross-listed nodes repeat under several departments with an identical
    ``categoryId`` (e.g. "Shoes + Boots" / "Men's Shoes" both resolve to
    ``15646``), so dedupe on the categoryId and collect every department that
    references it. Entries without a canonical browse URL stay addressable by
    ``-a category=<name>`` but their ``url`` is ``None``.
    """
    by_id: dict[str, dict[str, Any]] = {}
    ordered: list[dict[str, Any]] = []
    for department in ACADEMY_CATEGORY_INVENTORY:
        if not isinstance(department, dict):
            continue
        department_name = department.get("name") or ""
        for node in _iter_nodes(department):
            category_id = str(node.get("categoryId") or "").strip()
            name = node.get("name") or department_name
            if not category_id:
                continue
            url = node.get("url")
            slug = _slugify(url.rsplit("/", 1)[-1]) if url else _slugify(name)
            if department_name and slug and department_name != name:
                slug = f"{_slugify(department_name)}-{slug}"
            entry = by_id.get(category_id)
            if entry is None:
                entry = {
                    "category": slug or _slugify(name),
                    "name": name,
                    "url": url,
                    "category_id": category_id,
                    "seo_url": node.get("seoUrl"),
                    "departments": [department_name],
                }
                by_id[category_id] = entry
                ordered.append(entry)
                continue
            if department_name and department_name not in entry["departments"]:
                entry["departments"].append(department_name)
            # A parent department node often reuses a child's id without a browse
            # URL (e.g. "Deals + Clearance" == "Hot Deals" == 210952). Prefer the
            # cross-listing that has a canonical URL so `-a url=...` resolves.
            if url and not entry["url"]:
                entry["url"] = url
                entry["seo_url"] = node.get("seoUrl")
                entry["category"] = slug or entry["category"]
                if name:
                    entry["name"] = name
    return ordered


class AcademyListingSpider(BaseListingSpider):
    name = "academy_listing"
    allowed_domains = ["academy.com", "www.academy.com", "academy.scene7.com"]
    require_category_arg = False

    categories = _load_categories()

    PAGE_SIZE = PAGE_SIZE

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "department",
            "category_name",
            "category_id",
            "category_url",
            "item_id",
            "partnumber",
            "parent_partnumber",
            "sku_id",
            "title",
            "brand",
            "url",
            "image_url",
            "image_alt",
            "price",
            "list_price",
            "map_price",
            "sale_price",
            "promo_message",
            "promo_code",
            "promo_price",
            "currency",
            "rating",
            "reviews_count",
            "color",
            "size",
            "in_stock",
            "free_shipping",
            "gift_card",
            "primary_category",
            "category_ids",
            "page",
            "position",
            "total_count",
            "source_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_items: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        self._seen_items.clear()
        for entry in self._target_categories():
            yield self._category_request(entry, page=1)

    def _target_categories(self) -> list[dict[str, Any]]:
        if not (self.url or self.category_url or self.category):
            return list(self.categories)
        for entry in self.categories:
            if entry["category"] == self.category:
                return [entry]
        target = self.url or self.category_url
        if target:
            for entry in self.categories:
                if entry["url"] == target:
                    return [entry]
        available = ", ".join(self.available_categories()[:20])
        raise ValueError(
            f"Unknown category '{self.category or target}'. The Academy category API "
            "needs a numeric categoryId, so the target must be one of the bundled "
            f"inventory entries. Available categories (first 20): {available}"
        )

    def _category_request(self, entry: dict[str, Any], *, page: int):
        url = f"{CATEGORY_ENDPOINT}{entry['category_id']}?" + urlencode(
            {
                "web": "true",
                "displayFacets": "true",
                "recordsPerPage": self.PAGE_SIZE,
                "pageNumber": page,
            }
        )
        meta: dict[str, Any] = {
            "entry": entry,
            "category": entry["category"],
            "page": page,
        }
        proxy = self._api_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            url,
            callback=self.parse_category,
            headers=self._api_headers(entry.get("url") or f"{SITE_BASE}/"),
            meta=meta,
            dont_filter=True,
        )

    # ------------------------------------------------------------------ parse

    def parse_category(self, response: scrapy.http.Response):
        page = int(response.meta["page"])
        entry = response.meta["entry"]
        payload = self._json_payload(response)

        products = payload.get("hits")
        if not isinstance(products, list):
            raise RuntimeError(
                f"Academy category API returned no hits list at {response.url}: "
                f"keys={sorted(payload)[:12]}"
            )
        total = self._integer(payload.get("nbHits"))
        nb_pages = self._integer(payload.get("nbPages"))

        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item = self._item(product, response, entry, page, position, total)
            if item is not None:
                yield item

        if page >= self.max_pages or not products:
            return
        if nb_pages is not None and page >= nb_pages:
            return
        if total is not None and page * self.PAGE_SIZE >= total:
            return
        yield self._category_request(entry, page=page + 1)

    def _json_payload(self, response: scrapy.http.Response) -> dict[str, Any]:
        if response.status != 200:
            raise RuntimeError(
                f"Academy category API returned HTTP {response.status}: {response.url}"
            )
        body = response.text or ""
        lowered = body.lower()
        if any(marker in lowered for marker in CHALLENGE_MARKERS):
            raise RuntimeError(
                f"Academy category API returned a bot-challenge page at {response.url}; "
                "the API host needs the ScrapeOps bypass proxy."
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Academy category API returned non-JSON body at {response.url}: {body[:200]!r}"
            ) from exc
        if not isinstance(payload, dict):
            raise RuntimeError(
                f"Academy category API returned a non-object payload at {response.url}"
            )
        return payload

    # ------------------------------------------------------------------- item

    def _item(self, product, response, entry, page, position, total):
        item_id = self._text(product.get("uniqueId")) or self._text(product.get("catentryId"))
        if not item_id or item_id in self._seen_items:
            return None
        self._seen_items.add(item_id)

        sku = product.get("defaultSku")
        sku = sku if isinstance(sku, dict) else {}
        attributes = product.get("definingAttributes")
        attributes = attributes if isinstance(attributes, dict) else {}
        descriptive = product.get("descriptiveAttributes")
        descriptive = descriptive if isinstance(descriptive, dict) else {}

        title = product.get("name")
        part_number = self._text(product.get("partNumber"))
        # `seoURL` is a bare slug; the canonical PDP path is /p/<slug>/<partNumber>.
        slug = product.get("seoURL")
        url = f"{PDP_BASE}{slug}/{part_number}" if slug and part_number else (
            f"{SITE_BASE}/{slug}" if slug else None
        )
        image = product.get("xfullimage") or product.get("fullImage") or product.get("thumbnail")
        image_url = self._absolute_image(image)

        sale_price = self._number(product.get("salePrice"))
        if not sale_price:
            sale_price = self._number(sku.get("salePrice"))
        min_price = self._number(product.get("minEffectivePrice")) or self._number(
            product.get("minProductPrice")
        )
        price = sale_price or min_price
        list_price = self._number(sku.get("listPrice")) or self._number(product.get("mapPrice"))
        map_price = self._number(product.get("mapPrice"))
        if list_price and price and list_price < price:
            # Some responses put the struck-through price only in `mapPrice`.
            list_price = map_price or list_price

        return {
            "category": entry["category"],
            "department": entry.get("departments", [None])[0],
            "category_name": entry.get("name"),
            "category_id": entry["category_id"],
            "category_url": entry.get("url"),
            "item_id": item_id,
            "partnumber": part_number,
            "parent_partnumber": self._text(product.get("parentPartNumber")),
            "sku_id": self._text(sku.get("skuId")),
            "title": title,
            "brand": product.get("facet_Brand"),
            "url": url,
            "image_url": image_url,
            "image_alt": title,
            "price": price,
            "list_price": list_price,
            "map_price": map_price,
            "sale_price": sale_price,
            "promo_message": self._text(product.get("promoMessage")) or None,
            "promo_code": self._text(product.get("promoCode")) or None,
            "promo_price": self._number(product.get("promoPrice")),
            "currency": "USD",
            "rating": self._number(descriptive.get("averageRating"))
            or self._number(product.get("averageRating")),
            "reviews_count": self._integer(descriptive.get("reviewcount"))
            or self._integer(product.get("reviewCount")),
            "color": self._text(sku.get("color")) or self._text(attributes.get("Color")),
            "size": self._text(attributes.get("Size")),
            "in_stock": self._bool(product.get("sellable")),
            "free_shipping": self._bool(product.get("freeShipping")),
            "gift_card": product.get("giftCardFlag") == "Y",
            "primary_category": product.get("primaryCatgroupName"),
            "category_ids": product.get("categoryIds"),
            "page": page,
            "position": position,
            "total_count": total,
            "source_url": response.url,
            "source": "academy_category_api",
            "raw": product,
        }

    @staticmethod
    def _absolute_image(value):
        if not value:
            return None
        value = str(value)
        if value.startswith("//"):
            return f"https:{value}"
        if value.startswith("http"):
            return value
        return f"{IMAGE_BASE}{value}"

    # ------------------------------------------------------------------ proxy

    def _api_proxy(self) -> str | None:
        """Return the ScrapeOps proxy URL with the API-host bypass option.

        The academy.com JSON API is PerimeterX-protected: the plain datacenter
        route returns a stub while ``bypass=5`` returns product JSON. Copy the
        configured proxy and append the option to the username, preserving
        credentials.
        """
        if not hasattr(self, "settings"):
            return None
        proxy = self.settings.get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return None
        username = parts.username
        if ".bypass=" not in username:
            username = f"{username}.bypass={API_BYPASS}"
        credentials = quote(username, safe=".=_-")
        if parts.password is not None:
            credentials += f":{quote(parts.password, safe='')}"
        host = parts.hostname
        if parts.port is not None:
            host += f":{parts.port}"
        return urlunsplit(
            (parts.scheme, f"{credentials}@{host}", parts.path, parts.query, parts.fragment)
        )

    # ------------------------------------------------------------------ utils

    def _api_headers(self, referer: str) -> dict[str, str]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": referer,
            "Origin": SITE_BASE,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _text(value):
        if value is None or value == "":
            return None
        if isinstance(value, (list, tuple)):
            value = value[0] if value else None
            if value is None:
                return None
        return str(value).strip() or None

    @staticmethod
    def _bool(value):
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
    def _number(value):
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None
            match = re.search(r"-?\d[\d,]*(?:\.\d+)?", value)
            value = match.group(0).replace(",", "") if match else None
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        if isinstance(value, bool) or value is None:
            return None
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None
