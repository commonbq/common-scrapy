from __future__ import annotations

"""Backcountry listings parsed from the server-rendered Next.js `__NEXT_DATA__` hydration."""

import json
import re
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.backcountry_categories import BACKCOUNTRY_CATEGORIES, BASE_URL
from common.spiders.base_listing_spider import BaseListingSpider


# ScrapeOps option appended to the proxy username. Backcountry sits behind an AWS
# WAF: the plain datacenter route and every `bypass` level return a 2.4 KB
# `window.awsWafCookieDomainList` interstitial instead of the page, and the
# challenge never resolves server-side. Only the residential route returns the
# real 1 MB+ SSR document.
RESIDENTIAL_PROXY = "residential=true"

# The color swatches hydrate as storefront-relative paths; the CDN host that the
# same SSR response uses for the <img> tags is the canonical origin for them.
IMAGE_CDN = "https://content.backcountry.com"

_NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json"[^>]*>(.*?)</script>', re.S
)


class BackcountryListingSpider(BaseListingSpider):
    """backcountry.com listings from the SSR `#__NEXT_DATA__` PLP + Apollo hydration.

    One direction only: every field is read out of the hydration payload that the
    storefront server-renders into `#__NEXT_DATA__`
    (`props.pageProps.plpData.data.<container>.edges[].node`), joined to the
    normalized product record the same payload carries under
    `props.pageProps.__APOLLO_STATE__["Product:<id>"]`. There is no HTML-card
    fallback, no JSON-LD, and no separate product API call.
    """

    name = "backcountry_listing"
    allowed_domains = ["backcountry.com", "www.backcountry.com"]
    categories = BACKCOUNTRY_CATEGORIES
    # Direct url=/category_url= runs are supported, so opt out of the base class
    # category-only gate; resolve_target_url() still rejects a run with no target.
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.5,
        # Let the explicit status checks in parse() run so a WAF interstitial or
        # an error status surfaces the documented actionable error instead of a
        # successful zero-item crawl.
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "brand",
            "product_type",
            "url",
            "image",
            "image_alt",
            "color",
            "colors",
            "color_option_count",
            "price",
            "original_price",
            "discount_percentage",
            "currency",
            "in_stock",
            "stock_status",
            "availability",
            "rating",
            "reviews_count",
            "is_new_arrival",
            "is_exclusive",
            "is_past_season",
            "is_gearhead_pick",
            "past_season_colors",
            "category",
            "department",
            "section",
            "category_id",
            "page",
            "position",
            "total_count",
            "last_page",
            "source",
            "raw",
        ],
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self) -> Iterable[scrapy.Request]:
        self._seen.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry.get("url") == target), {})
        yield self._page_request(target, page=1, selected=selected)

    def _page_request(self, url: str, *, page: int, selected: dict[str, Any]) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(url, page),
            callback=self.parse,
            headers=self.headers,
            meta={
                "proxy": self._residential_proxy(),
                "page": page,
                "category": self.category or selected.get("category") or "custom",
                "department": selected.get("department"),
                "section": selected.get("section"),
                "category_id": selected.get("category_id"),
            },
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        """Return ``url`` with the storefront's ordinary ``?page=N`` contract applied.

        The PLP is server-rendered per page number (``/cat/mens-shirts?page=2``), and
        the number is echoed back as ``query.page`` in ``#__NEXT_DATA__``. Page 1 is
        left bare so the canonical category URL stays the first request, and any
        existing query string (e.g. a filtered ``/brand/...`` link) is preserved.
        """
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = parse_qsl(parts.query, keep_blank_values=True)
        query = [(k, v) for k, v in query if k != "page"]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _residential_proxy(self) -> str | None:
        """Return the configured proxy with the residential option enabled.

        ScrapeOps credentials are carried as ``<options>:<api_key>@host:port``, so
        the option belongs on the username side and the password is preserved
        verbatim. A proxy that is already residential, or any non-ScrapeOps proxy,
        is returned untouched.
        """
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None
        if "scrapeops" not in proxy.lower():
            return proxy
        parts = urlsplit(proxy)
        if parts.password is None or not parts.hostname:
            return proxy
        if RESIDENTIAL_PROXY.split("=")[-1] in (parts.username or ""):
            return proxy
        username = f"{parts.username}.{RESIDENTIAL_PROXY}"
        return urlunsplit(
            (
                parts.scheme,
                f"{username}:{parts.password}@{parts.hostname}:{parts.port}",
                parts.path,
                parts.query,
                parts.fragment,
            )
        )

    # ------------------------------------------------------------------ parse

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(
                f"backcountry listing returned HTTP {response.status}: {response.url}"
            )
        page_props = self._page_props(response.text, response.url)
        if not isinstance(page_props.get("type"), str) or not page_props["type"].startswith("plp-"):
            # The AWS WAF interstitial and the "no results" landing page both render
            # a document without a PLP payload. Returning silently here is what turns
            # a blocked run into a green, zero-item crawl.
            raise RuntimeError(
                f"backcountry {response.url} has no props.pageProps PLP payload "
                f"(type={page_props.get('type')!r}); the response is a challenge or "
                "an empty landing page, not a product listing"
            )

        plp = page_props.get("plpData")
        plp_data = plp.get("data") if isinstance(plp, dict) else None
        if not isinstance(plp_data, dict):
            raise RuntimeError(f"backcountry hydration has no plpData.data at {response.url}")

        container, container_name = self._listing_container(plp_data)
        if container is None:
            raise RuntimeError(
                f"backcountry hydration at {response.url} has no product container; "
                f"plpData.data keys: {sorted(plp_data)}"
            )

        edges = container.get("edges")
        edges = edges if isinstance(edges, list) else []
        current_page = int(response.meta.get("page") or 1)
        if not edges:
            self.logger.warning(
                "backcountry %s (page %s) returned an ordered container with 0 product edges",
                response.url, current_page,
            )
            return

        apollo = page_props.get("__APOLLO_STATE__")
        apollo = apollo if isinstance(apollo, dict) else {}
        # The PLP container carries the same `Product:<id>` records the Apollo cache
        # holds, so the join is a normalization, not a second source. It is optional:
        # an edge is still exported when only the edge payload is present.
        normalized = self._apollo_products(apollo)
        total_count = self._number(container.get("totalCount")) or self._number(
            page_props.get("totalCount")
        )
        last_page = self._number(page_props.get("totalPages"))
        category_id = page_props.get("categoryId")

        for position, edge in enumerate(edges, start=1):
            if not isinstance(edge, dict):
                continue
            node = edge.get("node")
            node = node if isinstance(node, dict) else None
            if not node:
                continue
            item_id = str(node.get("id") or "").strip()
            if not item_id:
                continue
            if item_id in self._seen:
                continue
            self._seen.add(item_id)
            product = normalized.get(item_id)
            merged = {**(product or {}), **node}
            yield self._item(
                merged,
                response=response,
                node=node,
                page=current_page,
                position=position,
                total_count=total_count,
                last_page=last_page,
                category_id=category_id,
                container_name=container_name,
            )

        yield from self._next_page(response, container, current_page, last_page)

    def _next_page(
        self,
        response: scrapy.http.Response,
        container: dict[str, Any],
        current_page: int,
        last_page: int | None,
    ):
        if current_page >= self.max_pages:
            return
        page_info = container.get("pageInfo")
        page_info = page_info if isinstance(page_info, dict) else {}
        has_next = page_info.get("hasNextPage")
        if has_next is False:
            return
        # `totalPages` is the storefront's own page count and is present on both the
        # category (`plp-cat`) and collection/brand (`plp-collection`/`plp-brand`)
        # containers, so it is a safe bound when `hasNextPage` is absent.
        if has_next is None and last_page is not None and current_page >= last_page:
            return

        selected = next((entry for entry in self.categories if entry.get("url") == response.url), {})
        yield self._page_request(response.url, page=current_page + 1, selected=selected)

    # ------------------------------------------------------------- extraction

    def _page_props(self, html: str, url: str) -> dict[str, Any]:
        match = _NEXT_DATA_RE.search(html or "")
        if not match:
            raise RuntimeError(
                f"backcountry {url} has no #__NEXT_DATA__ script; the SSR hydration "
                "route is unavailable (WAF challenge or a client-only page)"
            )
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"backcountry __NEXT_DATA__ at {url} is not valid JSON") from exc
        props = payload.get("props")
        page_props = props.get("pageProps") if isinstance(props, dict) else None
        if not isinstance(page_props, dict):
            raise RuntimeError(f"backcountry __NEXT_DATA__ at {url} has no props.pageProps")
        return page_props

    @staticmethod
    def _listing_container(plp_data: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
        """Return the one product-bearing container in ``plpData.data``.

        The storefront ships the same envelope under a different key per PLP kind:
        ``category`` for ``plp-cat``, ``collection`` for ``plp-collection`` and
        ``brand`` for ``plp-brand``. Keying off ``pageProps.type`` instead would
        miss filtered ``/rc/`` and ``/brand/`` targets, so the ordered container is
        located by its shape.
        """
        for key in ("category", "collection", "brand"):
            value = plp_data.get(key)
            if isinstance(value, dict) and "edges" in value:
                return value, key
        # Fall back to shape detection so an unlabelled new PLP kind still works.
        for key, value in plp_data.items():
            if isinstance(value, dict) and "edges" in value:
                return value, key
        return None, ""

    @staticmethod
    def _apollo_products(apollo: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Index the normalized `Product:<id>` cache records by product id.

        The cache key is the authoritative id. A record's own ``id`` is used when it
        is present; ``__ref`` is deliberately *not* preferred, because it is a cache
        pointer (``Product:SKU2``) rather than the bare id the edges are keyed by.
        """
        products: dict[str, dict[str, Any]] = {}
        for key, value in apollo.items():
            if not key.startswith("Product:") or not isinstance(value, dict):
                continue
            cache_id = key.split(":", 1)[1]
            record_id = value.get("id") or cache_id
            products[str(record_id)] = value
        return products

    def _item(
        self,
        product: dict[str, Any],
        *,
        response: scrapy.http.Response,
        node: dict[str, Any],
        page: int,
        position: int,
        total_count: int | None,
        last_page: int | None,
        category_id: str | None,
        container_name: str,
    ) -> dict[str, Any]:
        aggregates = product.get("aggregates")
        aggregates = aggregates if isinstance(aggregates, dict) else {}
        flags = product.get("flags")
        flags = flags if isinstance(flags, dict) else {}
        reviews = product.get("reviewAggregates")
        reviews = reviews if isinstance(reviews, dict) else {}
        brand = product.get("brand")
        brand = brand.get("name") if isinstance(brand, dict) else brand

        colors = product.get("colors")
        colors = colors if isinstance(colors, list) else []
        color_names = [
            str(c.get("name")).strip()
            for c in colors
            if isinstance(c, dict) and c.get("name")
        ]
        image = self._first_image(colors)
        stock_status = str(product.get("stockStatus") or "").strip() or None
        # `stockStatus` is the storefront's own enum (IN_STOCK / OUT_OF_STOCK /
        # PREORDER / ...). Anything other than an explicit in-stock value is
        # treated as not buyable so downstream filters do not over-claim.
        in_stock = stock_status == "IN_STOCK"
        min_sale = self._number(aggregates.get("minSalePrice"))
        min_list = self._number(aggregates.get("minListPrice"))
        discount = self._number(aggregates.get("minDiscount"))
        on_sale = bool(discount and discount > 0 and min_sale is not None and min_list is not None
                       and min_sale < min_list)
        if on_sale:
            price, original_price = min_sale, min_list
        else:
            price = min_sale if min_sale is not None else min_list
            original_price = None

        url = product.get("url") or ""
        item: dict[str, Any] = {
            "item_id": str(product.get("id") or "").strip(),
            "title": str(product.get("name") or "").strip() or None,
            "brand": str(brand).strip() if brand else None,
            "product_type": product.get("__typename"),
            "url": urljoin(BASE_URL + "/", str(url).lstrip("/")) if url else response.url,
            "image": image,
            "image_alt": str(product.get("name") or "").strip() or None,
            "color": color_names[0] if color_names else None,
            "colors": color_names or None,
            "color_option_count": len(color_names),
            "price": price,
            "original_price": original_price,
            "discount_percentage": discount or None,
            "currency": "USD",
            "in_stock": in_stock,
            "stock_status": stock_status,
            "availability": "in stock" if in_stock else (stock_status or "unknown"),
            "rating": self._number(reviews.get("averageRating")) or None,
            "reviews_count": self._number(reviews.get("totalReviews")),
            "is_new_arrival": bool(flags.get("isNewArrival")),
            "is_exclusive": bool(flags.get("isExclusive")),
            "is_past_season": bool(flags.get("isPastSeason")),
            "is_gearhead_pick": bool(flags.get("isGearheadPick")),
            "past_season_colors": aggregates.get("pastSeasonColors") or None,
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "section": response.meta.get("section"),
            "category_id": category_id or response.meta.get("category_id"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "last_page": last_page,
            "source": "backcountry_next_data",
            "raw": {
                "node": node,
                "apollo": product if product is not node else None,
                "container": container_name,
                "variations_on_sale": aggregates.get("variationsOnSale"),
                "total_variations": aggregates.get("totalVariations"),
            },
        }
        return item

    @classmethod
    def _first_image(cls, colors: list[Any]) -> str | None:
        """Return an absolute URL for the first hydrated color swatch.

        The PLP edge ships ``tileImage``/``pliImage`` as storefront-relative paths
        (``/images/items/160/FJR/FJRZ133/DANACHWH.jpg``); the CDN origin is the same
        host the SSR HTML uses for its <img> tags, so the path is resolved against
        it rather than against the page URL.
        """
        for color in colors:
            if not isinstance(color, dict):
                continue
            for key in ("tileImage", "pliImage", "image"):
                value = color.get(key)
                if value:
                    return urljoin(IMAGE_CDN, str(value).lstrip("/"))
        return None

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            text = str(value).strip().replace(",", "")
            return float(text) if "." in text else int(text)
        except (TypeError, ValueError):
            return None
