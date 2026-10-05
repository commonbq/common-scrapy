from __future__ import annotations

"""Backcountry listing spider (issue #222).

Backcountry is a Next.js storefront whose product listing pages are fully
server-rendered.  The whole catalog is present in the ``#__NEXT_DATA__``
hydration payload of an ordinary category request:

    GET https://www.backcountry.com/cat/mens-shirts[?page=N]
        -> <script id="__NEXT_DATA__" type="application/json">

Relevant paths:

    props.pageProps.type                              # "plp-cat"
    props.pageProps.categoryId                        # "bc-mens-shirts"
    props.pageProps.totalCount                        # 1490 products
    props.pageProps.totalPages                        # 36 pages
    props.pageProps.plpData.data.category.edges[]     # 42 products per page
    props.pageProps.plpData.data.category.pageInfo    # hasNextPage/hasPreviousPage
    props.pageProps.__APOLLO_STATE__["Product:<id>"]  # normalized product record

This spider uses exactly ONE data direction -- the Next.js bootstrap
hydration state.  There is **no HTML / JSON-LD fallback**: if
``#__NEXT_DATA__``, ``plpData`` or the product edges disappear the spider fails
loudly instead of silently degrading to a different extraction.

Pagination is ordinary HTML pagination (``?page=N``); page 2 returns a fresh
SSR payload with a disjoint edge set and ``hasPreviousPage=true``.  Products
are de-duplicated by ``Product.id`` and the crawl stops at ``max_pages``,
``totalPages`` or ``hasNextPage=false``.

The site sits behind an AWS WAF: a plain ScrapeOps datacenter request returns a
~2.3 KB challenge page, while the residential route returns the real ~1 MB
category HTML.  ``_residential_proxy()`` appends ``residential=true`` to the
ScrapeOps username, preserving any other username options and the credentials.

The full header taxonomy (14 departments / 109 sections / 469 links) is bundled
in ``backcountry_categories.py``; see that module for how the stable
``<department>/<section>/<name>`` slugs are derived.

Flow:
    category (slug, category_url or url)
        -> /cat/... ?page=N (page=1..max_pages)
        -> emit one item per plpData edge, joined to __APOLLO_STATE__
        -> repeat until max_pages, totalPages, or hasNextPage=false
"""

import json
import re
from typing import Any, Iterable, Iterator
from urllib.parse import quote, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.backcountry_categories import (
    BACKCOUNTRY_BASE_URL,
    BACKCOUNTRY_CATEGORIES,
    BACKCOUNTRY_SLUG_LABELS,
)
from common.spiders.base_listing_spider import BaseListingSpider

SITE_BASE = BACKCOUNTRY_BASE_URL

# The hydration payload is a single <script> block, but the JSON body is large
# (~1 MB HTML) and may contain "</script>" inside a string. Bound the search so
# a malformed page cannot make the regex walk the whole document repeatedly.
NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(?P<payload>.*?)</script>',
    re.S,
)

# ScrapeOps username option that routes through the residential pool. Without
# it the datacenter route only returns the AWS WAF challenge stub.
RESIDENTIAL_OPTION = "residential=true"

# Backcountry serves three product-listing page types from the same SSR
# plumbing: canonical category pages, /rc/ collection pages and brand pages.
PLP_PAGE_TYPES = ("plp-cat", "plp-collection", "plp-brand")

# The AWS WAF challenge stub is ~2.3 KB and identifies itself with
# `window.awsWafCookieDomainList`. Matching on that specific token (rather than
# a generic "captcha"/"access denied") matters: the real ~1 MB category page
# embeds a `grecaptcha-badge` style block, so a loose marker would flag every
# successful response. The other markers cover generic deny/gateway bodies.
CHALLENGE_MARKERS = (
    "awswaf",
    "aws-waf",
    "awswafchallenge",
)
DENY_MARKERS = (
    "access denied",
    "reference #",
    "request unsuccessful",
    "we couldn't retrieve a successful response",
)


def to_float(value: Any) -> float | None:
    """Coerce an aggregates price/discount field; tolerate ints, floats, strings."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace("$", "").replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def to_int(value: Any) -> int | None:
    number = to_float(value)
    return int(number) if number is not None else None


def absolute_url(url: Any) -> str | None:
    """Resolve Backcountry's site-relative PDP paths against the storefront."""
    if not isinstance(url, str):
        return None
    url = url.strip()
    if not url:
        return None
    if url.startswith("//"):
        return f"https:{url}"
    return urljoin(f"{SITE_BASE}/", url)


class BackcountryListingSpider(BaseListingSpider):
    name = "backcountry_listing"
    allowed_domains = ["backcountry.com", "www.backcountry.com"]

    # Direct url=/category_url= runs are supported, so opt out of the base
    # class category-only gate; resolve_target_url() still rejects a run with
    # no target at all.
    require_category_arg = False

    categories = BACKCOUNTRY_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1.5,
        # Let the explicit status checks in parse() run so a WAF/challenge body
        # surfaces the documented actionable error instead of a silent 0.
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "brand",
            "model",
            "url",
            "listing_url",
            "price",
            "original_price",
            "currency",
            "on_sale",
            "discount_percent",
            "availability",
            "in_stock",
            "stock_status",
            "image_url",
            "image",
            "color",
            "colors",
            "color_ids",
            "color_count",
            "total_variations",
            "variations_on_sale",
            "past_season_colors",
            "rating",
            "reviews_count",
            "is_new_arrival",
            "is_past_season",
            "is_exclusive",
            "is_gearhead_pick",
            "department",
            "section",
            "category_name",
            "category_id",
            "category_slug",
            "page",
            "source",
            "raw",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<slug>, category_url=<url>, or url=<url>. "
                "Category slugs look like 'men/clothing/shirts'."
            )
        self._seen: set[str] = set()

    # ------------------------------------------------------------------ crawl

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield self._page_request(self.resolve_target_url(), page=1)

    def _page_request(self, url: str, page: int) -> scrapy.Request:
        meta = {"listing_url": url, "page": page}
        # Resolved per request rather than in __init__: scrapy only attaches
        # `spider.settings` after the spider is constructed, so a cached value
        # computed there would always be None and the plain datacenter proxy
        # would be used instead -- which only returns the WAF challenge stub.
        proxy = self._residential_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            self._page_url(url, page),
            headers=self.headers,
            callback=self.parse,
            cb_kwargs={"listing_url": url, "page": page},
            meta=meta,
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        """Build the ``?page=N`` listing URL, preserving existing filters.

        Brand-filtered taxonomy URLs carry a ``p=...`` query whose syntax uses
        literal ``:`` and ``"`` characters. The query is therefore copied
        verbatim and the page parameter is appended to it, rather than being
        round-tripped through a query encoder that would re-escape those.
        """
        parts = urlsplit(url)
        if page <= 1:
            return url
        # Drop any page parameter already present so repeated calls cannot
        # accumulate `?page=7&page=2`, while leaving the filter syntax alone.
        kept = [
            part
            for part in parts.query.split("&")
            if part and not part.startswith("page=")
        ]
        kept.append(f"page={page}")
        return urlunsplit(
            (parts.scheme, parts.netloc, parts.path, "&".join(kept), parts.fragment)
        )

    def parse(self, response, listing_url: str, page: int) -> Iterator[dict]:
        if response.status != 200:
            raise RuntimeError(
                f"Backcountry listing returned HTTP {response.status}: {response.url}"
            )

        body = response.text
        lowered = body[:20000].lower()
        if any(marker in lowered for marker in CHALLENGE_MARKERS):
            raise RuntimeError(
                "Backcountry returned an AWS WAF challenge instead of the "
                f"category page ({len(body)} bytes): {response.url}. "
                "The residential ScrapeOps route is required "
                "(residential=true appended to the proxy username)."
            )

        try:
            page_props = self._page_props(body, response.url)
        except ValueError as exc:
            # A generic deny page or a ScrapeOps gateway error also lands here;
            # name the proxy remedy when the body looks like one of those.
            hint = ""
            if any(marker in lowered for marker in DENY_MARKERS):
                hint = (
                    " The response looks like a bot-protection deny page; the "
                    "residential ScrapeOps route is required "
                    "(residential=true appended to the proxy username)."
                )
            raise RuntimeError(
                f"Backcountry hydration schema error at {response.url}: {exc}.{hint}"
            ) from exc
        page_type = page_props.get("type")
        if page_type not in PLP_PAGE_TYPES:
            raise RuntimeError(
                f"Backcountry hydration is not a product listing page "
                f"(type={page_type!r}): {response.url}"
            )

        edges = self._product_edges(page_props, response.url)
        if not edges:
            raise RuntimeError(
                f"Backcountry hydration has no product edges: {response.url}"
            )

        apollo_state = page_props.get("__APOLLO_STATE__")
        if not isinstance(apollo_state, dict):
            apollo_state = {}

        labels = self._category_labels(listing_url)
        # The SSR payload always states the listing it rendered (categoryId,
        # collectionId or brand); prefer it over the taxonomy record because it
        # stays correct for ad-hoc URL runs.
        listing_id = (
            page_props.get("categoryId")
            or page_props.get("collectionId")
            or labels.get("category_id")
            or ""
        )
        labels["category_id"] = listing_id

        emitted = 0
        for edge in edges:
            node = self._merge_apollo(edge, apollo_state)
            item = self._product_item(node, listing_url, page, labels)
            item_id = item.get("item_id")
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield item

        if emitted == 0:
            self.logger.warning(
                "Backcountry page %s returned %s edges but no new product IDs",
                page,
                len(edges),
            )

        if page < self.max_pages and self._has_next_page(page_props, page):
            yield self._page_request(listing_url, page + 1)

    def _has_next_page(self, page_props: dict, page: int) -> bool:
        """Stop at ``max_pages``, ``totalPages`` or ``hasNextPage=false``."""
        total_pages = to_int(page_props.get("totalPages"))
        if total_pages:
            return page < total_pages
        page_info = self._listing_block(page_props).get("pageInfo") or {}
        return bool(page_info.get("hasNextPage"))

    # ------------------------------------------------------------- extraction

    @staticmethod
    def _page_props(body: str, url: str) -> dict:
        """Return ``props.pageProps`` from the Next.js hydration payload."""
        match = NEXT_DATA_RE.search(body)
        if not match:
            raise ValueError("missing <script id=\"__NEXT_DATA__\"> payload")
        try:
            payload = json.loads(match.group("payload"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid __NEXT_DATA__ JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("__NEXT_DATA__ was not an object")
        page_props = payload.get("props", {}).get("pageProps")
        if not isinstance(page_props, dict):
            raise ValueError("__NEXT_DATA__.props.pageProps is missing or not an object")
        return page_props

    @staticmethod
    def _listing_block(page_props: dict) -> dict:
        """Return the listing block from ``plpData.data``.

        Backcountry uses three PLP page types, all sharing the same block
        shape (``edges[]``, ``pageInfo``, ``totalCount``) but keyed differently:

            plp-cat        -> plpData.data.category     (categoryId)
            plp-collection -> plpData.data.collection   (collectionId, /rc/ ...)
            plp-brand      -> plpData.data.brand        (brand pages)

        Resolving by shape rather than by page type keeps one extraction path
        for all three instead of forking on a string.
        """
        plp_data = page_props.get("plpData")
        if not isinstance(plp_data, dict):
            raise KeyError("plpData")
        data = plp_data.get("data")
        if not isinstance(data, dict):
            raise KeyError("plpData.data")
        for key in ("category", "collection", "brand"):
            block = data.get(key)
            if isinstance(block, dict):
                return block
        raise KeyError(f"plpData.data.{'/'.join(sorted(data))}")

    def _product_edges(self, page_props: dict, url: str) -> list[dict]:
        try:
            listing = self._listing_block(page_props)
        except KeyError as exc:
            raise RuntimeError(
                f"Backcountry hydration has no PLP data ({exc}) at {url}"
            ) from exc
        edges = listing.get("edges")
        if edges is None:
            raise RuntimeError(f"Backcountry hydration has no product edges at {url}")
        if not isinstance(edges, list):
            raise RuntimeError(
                f"Backcountry hydration edges are {type(edges).__name__}, not a list: {url}"
            )
        nodes = []
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            node = edge.get("node") if isinstance(edge.get("node"), dict) else edge
            if isinstance(node, dict):
                nodes.append(node)
        return nodes

    @staticmethod
    def _merge_apollo(node: dict, apollo_state: dict) -> dict:
        """Prefer the normalized ``__APOLLO_STATE__`` record for a product id.

        The PLP edge and the Apollo cache entry are usually byte-identical, but
        Apollo is the normalized store, so use it when present and fall back to
        the edge node otherwise.
        """
        product_id = node.get("id")
        if not product_id:
            return node
        apollo_node = apollo_state.get(f"Product:{product_id}")
        if not isinstance(apollo_node, dict):
            return node
        merged = dict(node)
        merged.update(apollo_node)
        return merged

    def _category_labels(self, listing_url: str) -> dict[str, str]:
        """Resolve department/section/category labels for a listing URL."""
        slug = self.category or ""
        entry = BACKCOUNTRY_SLUG_LABELS.get(slug)
        if entry is not None and entry["url"] == listing_url:
            return {
                "department": entry["department"],
                "section": entry["section"],
                "category_name": entry["name"],
                "category_slug": entry["slug"],
                "category_id": entry["category_id"],
            }
        # Direct url=/category_url= runs have no slug; fall back to the first
        # taxonomy entry pointing at the same URL so labels are still attached.
        for candidate in BACKCOUNTRY_SLUG_LABELS.values():
            if candidate["url"] == listing_url:
                return {
                    "department": candidate["department"],
                    "section": candidate["section"],
                    "category_name": candidate["name"],
                    "category_slug": candidate["slug"],
                    "category_id": candidate["category_id"],
                }
        return {
            "department": "",
            "section": "",
            "category_name": "",
            "category_slug": "",
            "category_id": "",
        }

    def _product_item(
        self, node: dict, listing_url: str, page: int, labels: dict[str, str]
    ) -> dict:
        aggregates = node.get("aggregates") or {}
        review = node.get("reviewAggregates") or {}
        flags = node.get("flags") or {}
        colors = [c for c in (node.get("colors") or []) if isinstance(c, dict)]

        price = to_float(aggregates.get("minSalePrice"))
        original_price = to_float(aggregates.get("minListPrice"))
        on_sale = (
            price is not None
            and original_price is not None
            and original_price > price
        ) or bool(aggregates.get("variationsOnSale"))

        image_url = None
        for color in colors:
            candidate = absolute_url(color.get("pliImage") or color.get("tileImage"))
            if candidate:
                image_url = candidate
                break

        stock_status = node.get("stockStatus")
        in_stock = stock_status == "IN_STOCK"

        return {
            "item_id": node.get("id"),
            "title": node.get("name"),
            "brand": (node.get("brand") or {}).get("name"),
            "model": None,
            "url": absolute_url(node.get("url")),
            "listing_url": listing_url,
            "price": price,
            "original_price": original_price,
            "currency": "USD",
            "on_sale": on_sale,
            "discount_percent": to_float(aggregates.get("minDiscount")),
            "availability": stock_status,
            "in_stock": in_stock,
            "stock_status": stock_status,
            "image_url": image_url,
            # ``image`` keeps the project-wide field name usable by existing
            # consumers that read ``image`` rather than ``image_url``.
            "image": image_url,
            "color": colors[0].get("name") if colors else None,
            "colors": [c.get("name") for c in colors if c.get("name")],
            "color_ids": [c.get("colorId") for c in colors if c.get("colorId")],
            "color_count": to_int(aggregates.get("totalColors")) or len(colors),
            "total_variations": to_int(aggregates.get("totalVariations")),
            "variations_on_sale": to_int(aggregates.get("variationsOnSale")),
            "past_season_colors": aggregates.get("pastSeasonColors") or [],
            "rating": to_float(review.get("averageRating")),
            "reviews_count": to_int(review.get("totalReviews")),
            "is_new_arrival": bool(flags.get("isNewArrival")),
            "is_past_season": bool(flags.get("isPastSeason")),
            "is_exclusive": bool(flags.get("isExclusive")),
            "is_gearhead_pick": bool(flags.get("isGearheadPick")),
            "department": labels.get("department"),
            "section": labels.get("section"),
            "category_name": labels.get("category_name"),
            "category_id": labels.get("category_id"),
            "category_slug": labels.get("category_slug"),
            "page": page,
            "source": "backcountry_next_data",
            # Verbatim hydration record so downstream consumers can re-derive
            # fields when the SSR schema changes.
            "raw": node,
        }

    # ------------------------------------------------------------------ proxy

    def _residential_proxy(self) -> str | None:
        """Return the ScrapeOps proxy URL with ``residential=true``.

        Backcountry's AWS WAF answers a datacenter request with a ~2.3 KB
        challenge page; the residential pool returns the real ~1 MB category
        HTML. Copy the configured proxy and append the option to the username,
        preserving any existing options and the credentials. The password is
        never logged.
        """
        settings = getattr(self, "settings", None)
        if settings is None:
            return None
        proxy = settings.get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return None
        username = parts.username
        if RESIDENTIAL_OPTION not in username:
            username = f"{username}.{RESIDENTIAL_OPTION}"
        credentials = quote(username, safe=".=_-")
        if parts.password is not None:
            credentials += f":{quote(parts.password, safe='')}"
        host = parts.hostname
        if parts.port is not None:
            host += f":{parts.port}"
        return urlunsplit(
            (parts.scheme, f"{credentials}@{host}", parts.path, parts.query, parts.fragment)
        )