from __future__ import annotations

import json
import re
from urllib.parse import urljoin, urlsplit

import scrapy

from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.basspro_categories import (
    BASSPRO_BASE_URL,
    BASSPRO_CATEGORIES,
    BASSPRO_COVEO_SEARCH_HUB,
    BASSPRO_COVEO_SEARCH_URL,
    BASSPRO_DEFAULT_AQ,
    BASSPRO_TOKEN_URL,
)

COVEO_DOMAIN = "platform.cloud.coveo.com"
SAFE_SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._~-]*$")
NEXT_DATA = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(?P<payload>.*?)</script>', re.S
)
# Akamai's block page, the storefront's own "page not found" JSON, and the
# ScrapeOps gateway error body all need to be loud rather than "0 items".
BLOCK_MARKERS = (
    "access denied",
    "reference #",
    "request unsuccessful",
    "akamai",
    "_incapsula_resource",
    "we couldn't retrieve a successful response",
    "page not found",
)

# Curated ``fieldsToInclude`` list. The unfiltered Coveo payload is ~200 fields
# and ~30 KB per product (mostly the marketing ``categoryname`` tag soup); this
# keeps every identifier, price, availability, rating, facet and spec attribute
# the PLP tiles actually render while cutting the page size by ~60%.
BASSPRO_COVEO_FIELDS = [
    "sku", "sku_int", "productid", "catentry_id", "product_catentry_id", "permanentid",
    "partnumber", "upc", "sapsku", "webid", "model_number", "style_number",
    "sysuri", "uri", "producturlkeyword", "identifiableuri",
    "title", "systitle", "name", "ec_name", "ec_shortdesc", "brand", "ec_brand",
    "category", "subcategory", "department_name", "sub_department_name", "ec_category",
    "thecategories", "groupurlkeywords", "collection", "classification", "class_name",
    "sub_class_name", "type",
    "offerprice", "listprice", "ec_price", "ec_promo_price", "maxofferprice", "maxlistprice",
    "minsavings", "maxsavings", "savings", "percentsavings", "maxpercentsavings", "currency",
    "buyable", "isclearance", "issale", "isfreeoffer", "isnew", "isclubexclusive",
    "instoreonly", "availquantity", "maxavailquantity", "retailstoreinventory",
    "bvavgrating", "bvreviews", "bvratings", "ec_rating",
    "thumbnail", "topthumbnail", "fullimage", "ec_thumbnails", "cloudinary_id",
    "pieces", "gear_ratio", "line_weight", "retrieve", "action", "power", "technology",
    "jda_color", "jda_size", "country_origin_desc", "source", "syssource",
    "isgun", "isammo",
]


def parse_number(value):
    """Coveo sends every numeric attribute as a string; tolerate junk and blanks."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace("$", "").lstrip("+")
    if not text:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group(0)) if match else None


def as_int(value):
    number = parse_number(value)
    return int(number) if number is not None else None


def flag(value) -> bool:
    return str(value).strip() in {"1", "true", "True", "yes"}


def first_image(raw: dict) -> str | None:
    for key in ("thumbnail", "topthumbnail", "ec_thumbnails", "fullimage"):
        value = (raw.get(key) or "").strip()
        if value.startswith("http"):
            return value
    return None


class BassproListingSpider(BaseListingSpider):
    """Bass Pro Shops listings from the storefront's Coveo Headless search API.

    Bass Pro runs on a Next.js App Router storefront (``/l/<pageName>`` for level-2
    categories, ``/c/<slug>`` for departments). The server HTML deliberately
    contains **no** product records: ``__NEXT_DATA__.props.pageProps.pageValues``
    only carries page metadata (page id, layout, breadcrumbs, facet config) and
    ``__NEXT_DATA__.props.megaNavHtmlV2`` only carries the navigation tree.

    The product grid is a client-side Coveo Headless search, so this spider talks
    to that one endpoint directly:

    1. ``GET /l/<slug>`` -> page metadata + taxonomy context (proxied).
    2. ``GET /api/v1/coveo/generate-token?refresh=true`` -> short-lived search
       token (proxied, never persisted).
    3. ``POST https://platform.cloud.coveo.com/rest/search/v2`` with
       ``searchHub=basspro-searchhub`` (storefront ``ProductionPipeline``),
       ``aq=... AND @groupurlkeywords=="<slug>"`` and ``firstResult`` offset
       pagination (direct -- see ``_search_request``).

    No HTML product parsing and no JSON-LD fallback exist in this spider; the
    Coveo JSON is the only product source.
    """

    name = "basspro_listing"
    allowed_domains = ["basspro.com", "www.basspro.com", COVEO_DOMAIN, "localhost", "127.0.0.1"]
    categories = BASSPRO_CATEGORIES
    require_category_arg = False

    DEFAULT_PAGE_SIZE = 48

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        # The project middleware force-proxies every request, and the Coveo edge
        # silently discards the POST body of a proxied request (it answers with
        # the unfiltered `totalCount`). This spider therefore routes each leg
        # explicitly: storefront legs through `PROXY`, the Coveo search direct.
        "DOWNLOADER_MIDDLEWARES": {"common.middlewares.CommonDownloaderMiddleware": None},
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "category_id", "page_id",
            "category_url", "category_slug", "category_name", "breadcrumb",
            "item_id", "product_id", "sku", "part_number", "upc", "mpn",
            "title", "brand", "url", "image_url",
            "price", "original_price", "currency", "discount_percent", "savings",
            "rating", "reviews_count", "availability", "quantity", "retail_quantity",
            "is_clearance", "is_sale", "is_new", "is_free_shipping", "is_club_exclusive",
            "in_store_inventory", "collection", "classification", "class_name",
            "category_path", "color", "size", "country_of_origin",
            "pieces", "gear_ratio", "line_weight", "retrieve", "action", "power",
            "store_id", "page", "position", "total_count", "items_per_page",
            "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        page_size = kwargs.pop("page_size", None)
        include_restricted = kwargs.pop("include_restricted", None)
        super().__init__(*args, **kwargs)
        self.page_size = int(page_size or self.DEFAULT_PAGE_SIZE)
        self.include_restricted = flag(include_restricted)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<path>, category_url=<url>, or url=<listing url>. "
                f"basspro_categories.py defines {sum(len(v) for v in self._all_category_entries().values())} entries, "
                "e.g. 'Fishing/Rod & Reel Combos' or the bare slug 'rod-reel-combos'."
            )
        self._seen_items: set[str] = set()

    # ------------------------------------------------------------------ taxonomy

    @property
    def _proxy(self):
        return self.settings.get("PROXY") if "PROXY" in self.settings else None

    def _site_request(self, url: str, callback, **meta):
        """Storefront leg: goes through PROXY when one is configured."""
        return scrapy.Request(
            url,
            callback=callback,
            errback=self.on_error,
            meta={"proxy": self._proxy, **meta},
            dont_filter=True,
        )

    def _search_request(self, body: dict, first_result: int, meta: dict, token: str):
        """Coveo leg: always direct.

        `platform.cloud.coveo.com` answers a proxied POST with HTTP 200 and the
        *unfiltered* result count, because the proxy drops the request body --
        so routing this leg through PROXY silently yields the whole 541k-product
        index instead of the requested category. Left with no `meta['proxy']`.
        """
        return scrapy.Request(
            BASSPRO_COVEO_SEARCH_URL,
            callback=self.parse_search,
            errback=self.on_error,
            method="POST",
            body=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
            meta={"page": first_result // max(self.page_size, 1) + 1, "direct": True, **meta},
            dont_filter=True,
        )

    def resolve_entry(self) -> dict:
        """Resolve -a category / -a category_url / -a url to one taxonomy entry."""
        wanted = self.category
        if not wanted:
            raw = self.category_url or self.url or ""
            path = urlsplit(raw).path.strip("/")
            wanted = path.split("/")[-1] if path else ""

        wanted = (wanted or "").strip()
        if wanted.startswith(BASSPRO_BASE_URL):
            wanted = urlsplit(wanted).path.strip("/").split("/")[-1]

        for entry in self.iter_categories():
            if entry["category"].casefold() == wanted.casefold():
                return entry

        matches = [e for e in self.iter_categories() if e["slug"].casefold() == wanted.casefold()]
        if not matches:
            raise ValueError(
                f"Unknown category {wanted!r}. basspro_categories.py has "
                f"{sum(len(v) for v in self._all_category_entries().values())} entries; use a full path like "
                "'Fishing/Rod & Reel Combos' or a bare slug like 'rod-reel-combos'."
            )
        # 119 slugs are linked from more than one department (e.g. /l/trailer-accessories
        # under both Boating and Outdoor Rec) but they always resolve to the same browse
        # URL, so the bare slug stays unambiguous. Guard anyway in case that ever changes.
        if len({e["url"] for e in matches}) > 1:
            names = ", ".join(e["category"] for e in matches[:6])
            raise ValueError(
                f"Ambiguous category {wanted!r}: {len(matches)} navigation paths use this "
                f"slug for different URLs ({names}). Use the full path, e.g. "
                f"-a category='{matches[0]['category']}'."
            )
        return matches[0]

    @staticmethod
    def validate_slug(slug: str) -> str:
        """The slug is interpolated into an advanced-query string literal."""
        if not SAFE_SLUG.match(slug):
            raise ValueError(
                f"Refusing to use {slug!r} as a Coveo category slug: only "
                "[A-Za-z0-9._~-] is allowed."
            )
        return slug

    # ------------------------------------------------------------------ requests

    def start_requests(self):
        self._seen_items.clear()
        entry = self.resolve_entry()
        yield self._site_request(entry["url"], self.parse_plp, entry=entry)

    def on_error(self, failure):
        request = failure.request
        raise CloseSpider(
            f"{self.name}: request to {request.url} failed ({failure.value}). "
            "The storefront needs a working PROXY route; the Coveo search leg needs a "
            "direct (unproxied) connection because the proxy drops the POST body."
        )

    # ------------------------------------------------------------------ parsing

    @staticmethod
    def _looks_blocked(response) -> str | None:
        body = response.text[:4000].lower()
        for marker in BLOCK_MARKERS:
            if marker in body:
                return marker
        return None

    def parse_plp(self, response):
        """Stage 1 -- page metadata from the Next.js shell."""
        if response.status != 200:
            raise CloseSpider(
                f"{self.name}: {response.url} returned HTTP {response.status}. "
                "Check the PROXY route (direct Akamai returns 403 Access Denied)."
            )
        blocked = self._looks_blocked(response)
        if blocked:
            raise CloseSpider(
                f"{self.name}: {response.url} returned a block/challenge page "
                f"(matched {blocked!r}); no product data can be extracted."
            )

        match = NEXT_DATA.search(response.text)
        if not match:
            raise CloseSpider(
                f"{self.name}: no __NEXT_DATA__ payload in {response.url}. "
                "The storefront markup changed or the page was served as an error page."
            )
        try:
            data = json.loads(match.group("payload"))
        except ValueError as exc:
            raise CloseSpider(f"{self.name}: __NEXT_DATA__ is not valid JSON ({exc}).")

        page_values = (data.get("props", {}).get("pageProps", {}) or {}).get("pageValues", {}) or {}
        if not page_values:
            raise CloseSpider(
                f"{self.name}: __NEXT_DATA__.props.pageProps.pageValues is empty for "
                f"{response.url}; expected pageGroup/pageId metadata for a category page."
            )

        entry = response.meta["entry"]
        slug = self.validate_slug(entry["slug"])
        meta = {
            "entry": entry,
            "slug": slug,
            "page_id": str(page_values.get("pageId") or ""),
            "page_identifier": page_values.get("pageIdentifier")
            or page_values.get("name")
            or entry["category_name"],
            "store_id": str(page_values.get("storeId") or ""),
            "breadcrumbs": [
                crumb.get("label")
                for crumb in (page_values.get("breadcrumbs") or [])
                if crumb.get("label")
            ],
            "facets": [
                (facet.get("srchattridentifier") or "").replace("_cat.", "")
                for facet in (page_values.get("facetList") or [])
            ],
        }
        yield self._site_request(BASSPRO_TOKEN_URL, self.parse_token, **meta)

    def parse_token(self, response):
        """Stage 2 -- exchange the first-party token endpoint for a search token."""
        if response.status != 200:
            raise CloseSpider(
                f"{self.name}: token endpoint {response.url} returned HTTP {response.status}."
            )
        try:
            token = (json.loads(response.text) or {}).get("token")
        except ValueError:
            token = None
        if not token:
            raise CloseSpider(
                f"{self.name}: {BASSPRO_TOKEN_URL} returned no `token` field; "
                f"body starts with {response.text[:200]!r}."
            )
        # `proxy` is deliberately dropped: the Coveo leg must stay direct even
        # though the token response that feeds it was fetched through PROXY.
        # The token itself is short-lived (4 h) and never written to disk.
        yield self._search_request(
            self.search_body(0, response.meta["slug"]),
            0,
            {**self._forwarded_meta(response.meta), "token": token},
            token,
        )

    @staticmethod
    def _forwarded_meta(meta: dict) -> dict:
        """Carry the crawl context to the next leg, minus routing keys."""
        return {k: v for k, v in meta.items() if k not in {"page", "proxy", "direct"}}

    # ------------------------------------------------------------------ Coveo query

    def search_body(self, first_result: int, slug: str) -> dict:
        conditions = [] if self.include_restricted else [BASSPRO_DEFAULT_AQ]
        conditions.append(f'@groupurlkeywords=="{slug}"')
        return {
            "q": "",
            "searchHub": BASSPRO_COVEO_SEARCH_HUB,
            "firstResult": first_result,
            "numberOfResults": self.page_size,
            "excerptLength": 0,
            "aq": " AND ".join(conditions),
            "fieldsToInclude": BASSPRO_COVEO_FIELDS,
        }

    def parse_search(self, response):
        """Stage 3 -- map one Coveo page to items, then request the next page."""
        meta = response.meta
        if response.status != 200:
            raise CloseSpider(
                f"{self.name}: Coveo search returned HTTP {response.status} for {meta['slug']}."
            )
        try:
            data = json.loads(response.text)
        except ValueError as exc:
            raise CloseSpider(f"{self.name}: Coveo search response is not JSON ({exc}).")
        if isinstance(data, dict) and data.get("errorMessage"):
            raise CloseSpider(f"{self.name}: Coveo error: {data['errorMessage']}")
        # Coveo answers some failures with an HTTP 200 and an error document.
        if isinstance(data, dict) and "results" not in data and data.get("message"):
            raise CloseSpider(f"{self.name}: Coveo error: {data['message']}")
        if not isinstance(data, dict) or "results" not in data:
            raise CloseSpider(
                f"{self.name}: unexpected Coveo response shape "
                f"(keys: {sorted(data)[:8] if isinstance(data, dict) else type(data).__name__})."
            )

        results = data.get("results") or []
        total_count = as_int(data.get("totalCount")) or 0
        page = meta.get("page", 1)
        for offset, result in enumerate(results):
            item = self.build_item(result, meta, page, offset, total_count)
            if item is None:
                continue
            key = item["item_id"]
            if key in self._seen_items:
                self.logger.debug("Skipping duplicate basspro item %s", key)
                continue
            self._seen_items.add(key)
            yield item

        first_result = (page - 1) * self.page_size
        consumed = first_result + len(results)
        if len(results) < self.page_size or consumed >= total_count or page >= self.max_pages:
            self.logger.info(
                "basspro %s: %d results over %d page(s) (totalCount=%s)",
                meta["slug"], len(self._seen_items), page, total_count,
            )
            return
        yield self._search_request(
            self.search_body(consumed, meta["slug"]),
            consumed,
            self._forwarded_meta(meta),
            meta["token"],
        )

    # ------------------------------------------------------------------ item mapping

    def build_item(self, result: dict, meta: dict, page: int, offset: int, total_count: int) -> dict | None:
        raw = result.get("raw") or {}
        item_id = str(raw.get("sku") or raw.get("product_catentry_id") or raw.get("catentry_id") or "").strip()
        if not item_id:
            self.logger.warning(
                "Skipping Coveo result without sku/catentry_id: %s", result.get("title")
            )
            return None

        entry = meta["entry"]
        offer = parse_number(raw.get("offerprice") or raw.get("ec_price"))
        listing = parse_number(raw.get("listprice"))
        if listing is not None and offer is not None and listing <= offer:
            listing = None

        buyable = flag(raw.get("buyable"))
        quantity = parse_number(raw.get("availquantity"))
        availability = "InStock" if buyable and (quantity is None or quantity > 0) else "OutOfStock"

        # The Coveo image URLs already carry the storefront's own PLP transform
        # (`?$Prod_PLPThumb$` on assets.basspro.com), so they are used verbatim.
        image = first_image(raw)

        slug = raw.get("producturlkeyword") or ""
        url = urljoin(BASSPRO_BASE_URL, f"/p/{slug}") if slug else None

        return {
            "category": entry["category"],
            "department": entry["department"],
            "subcategory": entry["subcategory"] or raw.get("subcategory") or None,
            "category_id": entry["category_id"] or None,
            "page_id": meta.get("page_id") or None,
            "category_url": entry["url"],
            "category_slug": meta["slug"],
            "category_name": meta.get("page_identifier") or entry["category_name"],
            "breadcrumb": meta.get("breadcrumbs") or None,
            "item_id": item_id,
            "product_id": str(raw.get("productid") or "") or None,
            "sku": str(raw.get("sku") or "") or None,
            "part_number": raw.get("partnumber") or raw.get("webid") or None,
            "upc": raw.get("upc") or None,
            "mpn": raw.get("model_number") or raw.get("style_number") or None,
            "title": raw.get("title") or raw.get("systitle") or raw.get("ec_name") or None,
            "brand": raw.get("ec_brand") or raw.get("brand") or None,
            "url": url,
            "image_url": image,
            "price": offer,
            "original_price": listing,
            "currency": raw.get("currency") or "USD",
            "discount_percent": parse_number(raw.get("percentsavings")),
            "savings": parse_number(raw.get("maxsavings") or raw.get("minsavings")),
            "rating": parse_number(raw.get("bvavgrating") or raw.get("ec_rating")),
            "reviews_count": as_int(raw.get("bvreviews")),
            "availability": availability,
            "quantity": as_int(raw.get("availquantity")),
            "retail_quantity": as_int(raw.get("maxavailquantity")),
            "is_clearance": flag(raw.get("isclearance")),
            "is_sale": flag(raw.get("issale")),
            "is_new": flag(raw.get("isnew")),
            "is_free_shipping": flag(raw.get("isfreeoffer")),
            "is_club_exclusive": flag(raw.get("isclubexclusive")),
            "in_store_inventory": raw.get("retailstoreinventory") or None,
            "collection": raw.get("collection") or None,
            "classification": raw.get("classification") or None,
            "class_name": raw.get("class_name") or None,
            "category_path": raw.get("ec_category") or None,
            "color": raw.get("jda_color") or None,
            "size": raw.get("jda_size") or None,
            "country_of_origin": raw.get("country_origin_desc") or None,
            "pieces": as_int(raw.get("pieces")),
            "gear_ratio": raw.get("gear_ratio") or None,
            "line_weight": raw.get("line_weight") or None,
            "retrieve": raw.get("retrieve") or None,
            "action": raw.get("action") or None,
            "power": raw.get("power") or None,
            "store_id": meta.get("store_id") or None,
            "page": page,
            "position": offset + 1,
            "total_count": total_count,
            "items_per_page": self.page_size,
            "source_url": entry["url"],
            "source": "basspro_coveo",
            "raw": raw,
        }
