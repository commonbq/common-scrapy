from __future__ import annotations

"""Adorama listings parsed from the server-rendered Next.js hydration state.

Single authoritative source: the `__NEXT_DATA__` bootstrap embedded in the
category HTML. Adorama has no client-side listing XHR for `/l/...` pages -- the
SSR payload already carries a full page of products, so hydration parsing is the
whole contract and no HTML-card or JSON-LD fallback is used.

Pagination is query-based (`?startAt={n}`, 24 per page), and every page advertises
the following page as `pageProps.nextPageUrl`.
"""

import json
from collections.abc import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.adorama_categories import (
    ADORAMA_BASE_URL,
    ADORAMA_CATEGORIES,
    ADORAMA_PAGE_SIZE,
)
from common.spiders.base_listing_spider import BaseListingSpider


class AdoramaListingSpider(BaseListingSpider):
    name = "adorama_listing"
    allowed_domains = ["adorama.com", "www.adorama.com"]

    # `category`/`category_url`/`url` are all accepted, so opt out of the base
    # class category-only gate; resolve_target_url() still rejects a bare run.
    require_category_arg = False

    categories = ADORAMA_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.5,
        # Let the explicit status check in parse() run so a DataDome block or 5xx
        # surfaces the documented actionable error instead of a generic one.
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "sku",
            "title",
            "brand",
            "manufacturer",
            "model",
            "price",
            "original_price",
            "currency",
            "savings",
            "url",
            "image",
            "in_stock",
            "stock_status",
            "condition",
            "badge",
            "shipping",
            "category",
            "subcategory",
            "department",
            "page",
            "position",
            "total_count",
            "source",
            "raw",
        ],
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories()[:10])} "
                f"(+{len(self.available_categories()) - 10} more)"
            )
        if self.category and self.category not in {entry["category"] for entry in self.categories}:
            raise ValueError(f"Unknown category '{self.category}'. {self._available_hint()}")
        self._seen_skus: set[str] = set()

    def _available_hint(self) -> str:
        names = self.available_categories()
        return f"Available categories: {', '.join(names[:10])} (+{len(names) - 10} more)"

    def start_requests(self) -> Iterable[scrapy.Request]:
        url = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == url), {})
        yield self._page_request(url, page=1, selected=selected)

    def _page_request(self, url: str, *, page: int, selected: dict | None = None):
        meta = {
            "category": selected.get("label") if selected else (self.category or "custom"),
            "subcategory": selected.get("subcategory") if selected else None,
            "department": selected.get("department") if selected else None,
            "page": page,
            "listing_url": url,
            "handle_httpstatus_all": True,
        }
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
        """Return `url` for page 1, else `url?startAt={(page-1)*24}`."""
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["startAt"] = str((page - 1) * ADORAMA_PAGE_SIZE)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _extract_hydration(text: str) -> dict:
        """Decode the balanced `<script id="__NEXT_DATA__">` JSON payload.

        Uses a real HTML parser plus `json.loads` so the whole document's other
        inline scripts can never leak into the result the way a greedy regex over
        `<script>` blocks would.
        """
        from scrapy.http import HtmlResponse

        holder = HtmlResponse(
            url="https://www.adorama.com/",
            body=text,
            encoding="utf-8",
        )
        script = holder.css("script#__NEXT_DATA__::text").get()
        if not script:
            raise ValueError("no <script id=\"__NEXT_DATA__\"> bootstrap in response")
        try:
            state = json.loads(script)
        except json.JSONDecodeError as exc:
            raise ValueError(f"__NEXT_DATA__ is not valid JSON: {exc}") from exc
        if not isinstance(state, dict):
            raise ValueError("__NEXT_DATA__ did not decode to an object")
        return state

    @staticmethod
    def _page_props(state: dict) -> dict:
        props = (state.get("props") or {}).get("pageProps")
        if not isinstance(props, dict):
            raise ValueError("__NEXT_DATA__ has no props.pageProps object")
        return props

    def parse(self, response, listing_url: str | None = None, page: int | None = None):
        listing_url = listing_url or response.meta.get("listing_url") or response.url
        page = page if page is not None else int(response.meta.get("page", 1))
        if response.status != 200:
            raise RuntimeError(
                f"Adorama listing returned HTTP {response.status}: {response.url}. "
                "DataDome guards the storefront; escalate the proxy (residential=true, "
                "render_js=true) if this persists."
            )
        try:
            state = self._extract_hydration(response.text)
            props = self._page_props(state)
        except ValueError as exc:
            raise RuntimeError(f"Adorama hydration schema error at {response.url}: {exc}") from exc

        page_info = props.get("pageInfo") if isinstance(props.get("pageInfo"), dict) else {}
        page_type = page_info.get("pageType")
        if page_type and page_type != "listPage":
            raise RuntimeError(
                f"Adorama {response.url} hydrated pageType={page_type!r}, not 'listPage'; "
                "department landing pages carry no product grid"
            )

        products = props.get("products")
        if not isinstance(products, list):
            raise RuntimeError(f"Adorama hydration has no props.pageProps.products list: {response.url}")
        if not products:
            self.logger.info("Adorama listing page %s is empty; pagination stopped", page)
            return

        total = self._total_count(props)
        emitted = 0
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item = self._product_item(product, response, page, position, total)
            item_id = item.get("item_id")
            if not item_id or item_id in self._seen_skus:
                continue
            self._seen_skus.add(item_id)
            emitted += 1
            yield item

        if emitted == 0:
            self.logger.warning(
                "Adorama page %s contained no new SKUs (all %s already seen)", page, len(products)
            )

        next_url = props.get("nextPageUrl")
        if page < self.max_pages and emitted and next_url:
            yield self._page_request(self._absolute(next_url), page=page + 1)

    @staticmethod
    def _absolute(url: str) -> str:
        return url if url.startswith("http") else f"{ADORAMA_BASE_URL}{url}"

    @staticmethod
    def _total_count(props: dict) -> int | None:
        stats = props.get("itemsStats")
        if isinstance(stats, dict):
            new = stats.get("New")
            if isinstance(new, dict) and isinstance(new.get("count"), int):
                return new["count"]
        return None

    def _product_item(
        self, product: dict, response, page: int, position: int, total: int | None
    ) -> dict:
        prices = product.get("prices") if isinstance(product.get("prices"), dict) else {}
        you_save = prices.get("youSave") if isinstance(prices.get("youSave"), dict) else {}
        flags = product.get("flags") if isinstance(product.get("flags"), dict) else {}
        sub_status = (
            product.get("subStatus") if isinstance(product.get("subStatus"), dict) else {}
        )

        sku = str(product.get("sku") or product.get("variantSku") or "")
        meta = response.meta
        image_name = product.get("mainImageName")
        persuasion = [
            entry.get("message")
            for entry in (product.get("persuasionStrategies") or [])
            if isinstance(entry, dict) and entry.get("message")
        ]
        condition = "refurbished" if flags.get("isRefurbished") else (
            "used" if flags.get("isUsed") else "new"
        )
        in_stock = bool(
            flags.get("isAvailableForPurchase") and str(product.get("stock", "")).lower() != "out"
        )

        return {
            "item_id": sku,
            "sku": sku,
            "title": product.get("productTitle") or product.get("shortTitle"),
            "brand": product.get("brand"),
            "manufacturer": product.get("mfr"),
            "model": product.get("mfr"),
            "price": prices.get("price"),
            "original_price": prices.get("highPrice"),
            "currency": "USD",
            "savings": you_save.get("dollar"),
            "url": self._absolute(product.get("productUrl")) if product.get("productUrl") else None,
            "image": (
                f"{ADORAMA_BASE_URL}/images/product/{image_name}" if image_name else None
            ),
            "in_stock": in_stock,
            "stock_status": sub_status.get("name") or product.get("stock"),
            "condition": condition,
            "badge": product.get("badgeText") or (persuasion[0] if persuasion else None),
            "shipping": (product.get("freeShipTypeName") or "").strip() or None,
            "category": meta.get("category") or product.get("categoryPath"),
            "subcategory": meta.get("subcategory"),
            "department": meta.get("department"),
            "page": page,
            "position": position,
            "total_count": total,
            "source": "adorama_next_data_products",
            "raw": product,
        }