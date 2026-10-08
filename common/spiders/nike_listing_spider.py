from __future__ import annotations

"""Nike listing spider (issue #134).

Nike runs a Next.js catch-all route `/w/[[...slug]]`. The product wall is hydrated
into `__NEXT_DATA__` on page 1, and every later page is served by the first-party
product-wall API on `api.nike.com`:

    /discover/product_wall/v1/marketplace/US/language/en/consumerChannelId/<uuid>
        ?path=/w/<slug>&attributeIds=<uuids>&queryType=PRODUCTS&anchor=<n>&count=<n>

This spider uses exactly one data direction -- that hydration state and the
API it points at. There is no HTML card scraping and no rendered-browser
fallback. Both legs return the same product object shape, so items are built by
one parser used by both.

Two details that are load-bearing:

* `api.nike.com` rejects requests without `nike-api-caller-id`, answering HTTP
  200 with `{"errors":[{"code":"NIKE_API_CALLER_ID_HEADER_NOT_PRESENT"}]}`.
* ScrapeOps strips custom request headers by default, so the API leg needs the
  provider's `keep_headers=true` username option; without it the header is
  dropped in transit and Nike returns exactly that error above. The proxy rewrite
  mirrors `costco_listing_spider._search_api_proxy`.
"""

import json
import re
from typing import Any
from urllib.parse import urljoin, urlsplit, urlunsplit, quote

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.nike_categories import NIKE_CATEGORIES

_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")

def category_slug(url: str) -> str:
    """Build a stable `category` key from a Nike listing URL.

    Nike slugs already encode their department (`mens-shoes-nik1zy7ok`,
    `womens-shoes-5e1x6zy7ok`), and the 168 inventory URLs produce 168 distinct
    slugs, so the URL path alone is a unique key.
    """
    path = url.split("nike.com", 1)[-1].split("?", 1)[0].strip("/")
    if path.startswith("w/"):
        path = path[2:]
    return _SLUG_CLEAN_RE.sub("-", path.lower()).strip("-")


def _load_categories() -> list[dict[str, str]]:
    """Flatten the department -> group -> subcategory inventory.

    The subcategory *name* is not unique (Men's "Shoes"/"All Shoes" and
    "New & Featured"/"New Arrivals" are the same page), so entries are keyed by
    URL and the first name seen for that URL wins.
    """
    categories: list[dict[str, str]] = []
    seen: dict[str, int] = {}
    for department, groups in NIKE_CATEGORIES.items():
        for group, subcategories in groups.items():
            for name, url in subcategories.items():
                if url in seen:
                    continue
                seen[url] = 1
                categories.append(
                    {
                        "category": category_slug(url),
                        "department": department,
                        "group": group,
                        "name": name,
                        "url": url,
                    }
                )
    return categories


class NikeListingSpider(BaseListingSpider):
    name = "nike_listing"
    allowed_domains = ["nike.com", "www.nike.com", "api.nike.com"]
    require_category_arg = False

    SITE_BASE = "https://www.nike.com"
    API_BASE = "https://api.nike.com"
    API_CALLER_ID = "nike:dotcom:browse:wall.client:2.0"
    NEXT_DATA_RE = re.compile(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        re.S,
    )

    categories = _load_categories()

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "department",
            "group",
            "item_id",
            "title",
            "subtitle",
            "url",
            "image_url",
            "price",
            "list_price",
            "discount_percent",
            "employee_price",
            "currency",
            "color",
            "color_hex",
            "color_description",
            "product_type",
            "availability",
            "badge",
            "promotion",
            "is_new_until",
            "page",
            "category_url",
            "source",
            "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nike returns one wall page per requested anchor, and a product code can
        # legitimately repeat across pages of the same listing while a product
        # shared by two categories must not be dropped. Keying on both matches
        # the repository convention (see gamestop/adidas).
        self._seen: set[tuple[str, str]] = set()
        self._validate_inventory()

    def _validate_inventory(self) -> None:
        """Enforce the inventory contract that the base class skips.

        `require_category_arg` is False so that `-a url=` / `-a category_url=`
        runs reach `start_requests()`, which means
        `_validate_categories_schema_if_needed` returns early and a malformed
        entry would only surface later as a confusing lookup failure.
        """
        if not isinstance(self.categories, list) or not self.categories:
            raise ValueError(
                "Nike inventory must define `categories` as a non-empty list of "
                "{'category','url'} dicts"
            )
        for i, entry in enumerate(self.categories):
            if not isinstance(entry, dict):
                raise ValueError(f"categories[{i}] must be a dict")
            for key in ("category", "url"):
                if not isinstance(entry.get(key), str) or not entry[key]:
                    raise ValueError(f"categories[{i}] missing string '{key}'")
            if self._category_for(entry["url"]) != entry["category"]:
                raise ValueError(
                    f"categories[{i}] 'category' {entry['category']!r} does not match "
                    f"the slug in its url {entry['url']!r}"
                )

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield self._listing_request(category_url, page=1)

    def _listing_request(self, category_url: str, *, page: int):
        return scrapy.Request(
            category_url,
            callback=self.parse_listing,
            headers={
                "Accept": "text/html,application/xhtml+xml",
                "Referer": f"{self.SITE_BASE}/",
            },
            meta={
                "page": page,
                "category_url": category_url,
                "category": self._category_for(category_url),
            },
        )

    def _api_request(self, next_path: str, *, page: int, category_url: str, category: str):
        """Request the next product-wall page from `api.nike.com`.

        `next_path` is always read from the previous response's own pagination
        field; the channel/attribute UUIDs and the anchor are never hard-coded
        here, because Nike rotates them and a stale value fails the request.
        """
        request = scrapy.Request(
            urljoin(self.API_BASE, next_path),
            callback=self.parse_api,
            headers={
                "Accept": "application/json",
                "nike-api-caller-id": self.API_CALLER_ID,
                "Origin": self.SITE_BASE,
                "Referer": category_url,
            },
            meta={
                "page": page,
                "category_url": category_url,
                "category": category,
            },
        )
        proxy = self._api_proxy()
        if proxy:
            request.meta["proxy"] = proxy
        return request

    # ------------------------------------------------------------------ parse

    def parse_listing(self, response: scrapy.http.Response, **kwargs):
        page = int(response.meta["page"])
        category_url = response.meta["category_url"]
        category = response.meta["category"]
        self._reject_challenge(response)

        wall = self._wall_from_html(response)
        yield from self._emit_wall(wall, page=page, category_url=category_url, category=category, source="nike_next_data")

        if page >= self.max_pages:
            return
        next_path = (wall.get("pageData") or {}).get("next") or ""
        if not next_path:
            self.logger.info(
                "Nike %s hydration reported no next page; category has a single page",
                category_url,
            )
            return
        yield self._api_request(
            next_path, page=page + 1, category_url=category_url, category=category
        )

    def parse_api(self, response: scrapy.http.Response, **kwargs):
        page = int(response.meta["page"])
        category_url = response.meta["category_url"]
        category = response.meta["category"]
        self._reject_challenge(response)

        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Nike product-wall API returned a non-JSON body for page {page} of "
                f"{category_url}: {response.text[:200]!r}"
            ) from exc

        # A rejected caller id is answered with HTTP 200 and an `errors` array,
        # so a status check alone would treat it as a valid empty page.
        errors = payload.get("errors")
        if errors:
            codes = [e.get("code") for e in errors if isinstance(e, dict)]
            raise RuntimeError(
                f"Nike product-wall API rejected the request for page {page} of "
                f"{category_url} (codes: {codes}); the nike-api-caller-id header is "
                "most likely being stripped by the proxy -- use keep_headers=true."
            )
        if "productGroupings" not in payload:
            raise RuntimeError(
                f"Nike product-wall API response for page {page} of {category_url} is "
                f"missing 'productGroupings' (keys: {sorted(payload)}); the API "
                "contract may have changed."
            )

        yield from self._emit_wall(
            payload,
            page=page,
            category_url=category_url,
            category=category,
            source="nike_product_wall_api",
        )

        if page >= self.max_pages:
            return
        next_path = (payload.get("pages") or {}).get("next") or ""
        if not next_path:
            self.logger.info("Nike %s page %s was the last API page", category_url, page)
            return
        yield self._api_request(
            next_path, page=page + 1, category_url=category_url, category=category
        )

    def _emit_wall(
        self,
        wall: dict[str, Any],
        *,
        page: int,
        category_url: str,
        category: str | None,
        source: str,
    ):
        """Emit one item per product in `productGroupings[].products[]`.

        The page-1 hydration state and the API response share this shape, so a
        single parser covers both. Grouping is *not* the unit of output: a group
        holds every colorway it collects and each has its own `productCode`, so
        collapsing to one item per group would silently drop colorways.
        """
        groupings = wall.get("productGroupings")
        if not isinstance(groupings, list):
            raise RuntimeError(
                f"Nike wall for {category_url} page {page} has no 'productGroupings' "
                f"list (type: {type(groupings).__name__}); the hydration contract "
                "may have changed."
            )

        emitted = 0
        for grouping in groupings:
            if not isinstance(grouping, dict):
                continue
            products = grouping.get("products")
            if not isinstance(products, list):
                continue
            for product in products:
                if not isinstance(product, dict):
                    continue
                item = self._product_item(
                    product,
                    category=category,
                    category_url=category_url,
                    page=page,
                    source=source,
                )
                key = (category or category_url, item["item_id"])
                if key in self._seen:
                    continue
                self._seen.add(key)
                emitted += 1
                yield item

        page_data = wall.get("pageData") or wall.get("pages") or {}
        self.logger.info(
            "Nike %s page %s: %s products from %s groupings (total %s, %s pages)",
            category_url,
            page,
            emitted,
            len(groupings),
            page_data.get("totalResources"),
            page_data.get("totalPages"),
        )

    # ----------------------------------------------------------------- helpers

    def _wall_from_html(self, response: scrapy.http.Response) -> dict[str, Any]:
        match = self.NEXT_DATA_RE.search(response.text)
        if not match:
            raise RuntimeError(
                f"Nike listing page {response.url} has no script#__NEXT_DATA__ block; "
                "the storefront markup changed or the response was not the rendered PLP."
            )
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Nike listing page {response.url} has a malformed __NEXT_DATA__ payload: {exc}"
            ) from exc

        wall = (payload.get("props") or {}).get("pageProps", {}).get("initialState", {}).get("Wall")
        if not isinstance(wall, dict):
            raise RuntimeError(
                f"Nike listing page {response.url} has no "
                "props.pageProps.initialState.Wall hydration state; the category URL "
                "may be retired."
            )
        return wall

    def _reject_challenge(self, response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(
                f"Nike returned HTTP {response.status} for {response.url}"
            )
        ctype = response.headers.get("Content-Type") or b""
        if isinstance(ctype, bytes):
            ctype = ctype.decode("utf-8", "replace")
        if "json" in ctype.lower() or "html" in ctype.lower():
            return
        head = response.text[:2000].lower()
        for marker in ("access denied", "captcha", "are you a human", "request unsuccessful"):
            if marker in head:
                raise RuntimeError(
                    f"Nike served an access-denied/challenge body for {response.url} "
                    f"(matched {marker!r}); the request was not answered by the storefront."
                )

    def _api_proxy(self) -> str | None:
        """Preserve `nike-api-caller-id` when requests route through ScrapeOps.

        ScrapeOps strips custom request headers by default, and Nike answers a
        request that arrives without `nike-api-caller-id` with HTTP 200 and a
        `NIKE_API_CALLER_ID_HEADER_NOT_PRESENT` error body.
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
        if ".keep_headers=true" not in username:
            username = f"{username}.keep_headers=true"
        credentials = quote(username, safe=".=_-")
        if parts.password is not None:
            credentials += f":{quote(parts.password, safe='')}"
        host = parts.hostname
        if parts.port is not None:
            host += f":{parts.port}"
        return urlunsplit(
            (parts.scheme, f"{credentials}@{host}", parts.path, parts.query, parts.fragment)
        )

    def _category_for(self, url: str) -> str:
        for entry in self.categories:
            if entry["url"] == url:
                return entry["category"]
        return category_slug(url)

    def _department_for(self, category: str) -> str | None:
        for entry in self.categories:
            if entry["category"] == category:
                return entry.get("department")
        return None

    def _group_for(self, category: str) -> str | None:
        for entry in self.categories:
            if entry["category"] == category:
                return entry.get("group")
        return None

    def _product_item(
        self,
        product: dict[str, Any],
        *,
        category: str | None,
        category_url: str,
        page: int,
        source: str,
    ) -> dict[str, Any]:
        item_id = str(product.get("productCode") or "").strip()
        if not item_id:
            raise RuntimeError(
                f"Nike product entry is missing 'productCode' (keys: {sorted(product)}); "
                "the product-wall contract may have changed."
            )

        copy = product.get("copy") or {}
        prices = product.get("prices") or {}
        colors = product.get("displayColors") or {}
        simple_color = colors.get("simpleColor") or {}
        images = product.get("colorwayImages") or {}
        pdp = product.get("pdpUrl") or {}
        promotion = self._promotion(product.get("promotions"))

        current = prices.get("currentPrice")
        initial = prices.get("initialPrice")
        discount = prices.get("discountPercentage") or None

        return {
            "category": category,
            "department": self._department_for(category) if category else None,
            "group": self._group_for(category) if category else None,
            "item_id": item_id,
            "title": copy.get("title"),
            "subtitle": copy.get("subTitle"),
            "url": pdp.get("url") or (urljoin(self.SITE_BASE, pdp["path"]) if pdp.get("path") else None),
            "image_url": images.get("squarishURL") or images.get("portraitURL"),
            "price": current,
            # Nike lists the pre-discount figure in `initialPrice`; only report it
            # as the list price when there is actually a discount, so an
            # undiscounted item does not report the same value twice as if it
            # had been marked down.
            "list_price": initial if discount else None,
            "discount_percent": discount,
            "employee_price": prices.get("employeePrice"),
            "currency": prices.get("currency"),
            "color": simple_color.get("label"),
            "color_hex": simple_color.get("hex"),
            "color_description": colors.get("colorDescription"),
            "product_type": product.get("productType"),
            "availability": self._availability(product),
            "badge": product.get("badgeLabel"),
            "promotion": promotion,
            "is_new_until": product.get("isNewUntil"),
            "page": page,
            "category_url": category_url,
            "source": source,
            "raw": product,
        }

    @staticmethod
    def _availability(product: dict[str, Any]) -> str:
        attributes = product.get("featuredAttributes") or []
        if isinstance(attributes, list):
            if "COMING_SOON" in attributes:
                return "PreOrder"
            if "RESTOCK" in attributes:
                return "BackInStock"
        return "InStock"

    @staticmethod
    def _promotion(promotions: Any) -> str | None:
        """Read the customer-facing promotion title, if any.

        Nike exposes these as `{promotionId, visibilities: [{title, subtitle, ...}]}`
        and only under a `PW` (product wall) visibility, so the first visible
        entry is the one the storefront renders.
        """
        if not isinstance(promotions, dict):
            return None
        for visibility in promotions.get("visibilities") or []:
            if not isinstance(visibility, dict):
                continue
            title = (visibility.get("title") or "").strip()
            if title:
                return title
        return None
