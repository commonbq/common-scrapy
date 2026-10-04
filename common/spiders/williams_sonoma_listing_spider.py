from __future__ import annotations

"""Williams-Sonoma listing spider (issue #160).

The storefront is a "micro-frontend" app whose category pages are shells: the
server-rendered `window.__INITIAL_STATE__` carries the whole page config but
every product collection in it is empty (`shop.collections: {}`,
`productFinderTool.products: []`). The grid only exists after the client calls
Constructor.io. So this spider uses exactly one data direction -- the
Constructor.io **browse API** -- and never falls back to scraping the listing
HTML or to a rendered browser.

Flow:

    category-tree JSON  (taxonomy + group_id inventory)
        -> any category page HTML, once, to read `constructorKey` from
           `window.__INITIAL_STATE__.shop.searchEngineConfig`
        -> GET https://ac.cnstrc.com/browse/group_id/<group_id>
               ?key=...&num_results_per_page=100&page=N&section=Products
        -> emit one item per result
        -> repeat with page=N+1 until N*page_size >= total_num_results,
           the page comes back empty, or max_pages is reached

The key is re-read from page state on every run rather than hardcoded, so a key
rotation is picked up automatically; if it cannot be found the spider fails
loudly instead of falling back to a stale constant.
"""

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.williams_sonoma_categories import (
    CATEGORY_TREE_URL,
    Category,
    SITE_BASE,
    build_index,
    group_id_from_url,
    parse_category_tree,
)

# The key lives inside a JSON blob embedded in the page, so the JSON string
# escapes (`"`, `\u002F`) are already resolved by the time the regex runs.
CONSTRUCTOR_KEY_RE = re.compile(r'"constructorKey":"(key_[A-Za-z0-9]+)"')

# A page that is not JSON means the request was not answered by the API
# (Akamai challenge, geo-block, or an HTML error page).
CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "are you a human",
    "request unsuccessful",
)


class WilliamsSonomaListingSpider(BaseListingSpider):
    name = "williams_sonoma_listing"
    allowed_domains = [
        "williams-sonoma.com",
        "www.williams-sonoma.com",
        "ac.cnstrc.com",
    ]
    # Targets can also come from `-a all_categories=true`, so a bare category arg
    # is not mandatory -- but *some* target selector is.
    require_category_arg = False

    BROWSE_BASE = "https://ac.cnstrc.com"
    PAGE_SIZE = 100

    categories: list[dict[str, str]] = []

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "category_name",
            "parent_category",
            "item_id",
            "title",
            "url",
            "brand",
            "sku",
            "price",
            "regular_price",
            "price_min",
            "price_max",
            "regular_price_min",
            "regular_price_max",
            "sale_price_min",
            "sale_price_max",
            "discount_percent",
            "price_type",
            "currency",
            "image_url",
            "image_alt",
            "alt_images_count",
            "swatches_count",
            "flags",
            "pip_type",
            "quick_buy",
            "description",
            "short_description",
            "product_details",
            "group_ids",
            "page",
            "category_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_categories = str(
            kwargs.get("all_categories", "false")
        ).strip().lower() in {"1", "true", "yes"}
        self.page_size = int(kwargs.get("page_size") or self.PAGE_SIZE)
        self._seen_ids: set[str] = set()
        self._index: dict[str, Category] = {}
        self._constructor_key: str | None = None

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        yield scrapy.Request(
            CATEGORY_TREE_URL,
            callback=self.parse_category_tree,
            headers={"Accept": "application/json"},
            dont_filter=True,
        )

    def parse_category_tree(self, response: scrapy.http.Response):
        """Load the taxonomy, resolve targets, then read the Constructor key."""
        self._reject_challenge(response, "category tree")
        try:
            categories = parse_category_tree(response.text)
        except RuntimeError as exc:
            raise RuntimeError(
                f"Could not load the Williams-Sonoma category tree from "
                f"{CATEGORY_TREE_URL}: {exc}"
            ) from exc
        if not categories:
            raise RuntimeError(
                f"Williams-Sonoma category tree returned no crawlable categories "
                f"from {CATEGORY_TREE_URL} (only header/leftheader labels?); the "
                "taxonomy contract may have changed."
            )
        self._index = build_index(categories)
        self.logger.info(
            "Williams-Sonoma category tree: %s crawlable targets (%s headers excluded)",
            len(self._index),
            len(categories),
        )

        targets = self._resolve_targets()
        if not targets:
            raise ValueError(
                "No Williams-Sonoma category target selected. Use "
                "-a category=<group_id> (e.g. cookware-sets), -a category_url=<url>, "
                "-a url=<url>, or -a all_categories=true."
            )
        self.logger.info(
            "Williams-Sonoma targets: %s", ", ".join(t.group_id for t in targets[:10])
        )

        # The Constructor key is site-global, so one page fetch serves every
        # target -- including the `-a all_categories=true` sweep.
        yield scrapy.Request(
            targets[0].url,
            callback=self.parse_context,
            headers={"Accept": "text/html,application/xhtml+xml"},
            meta={"targets": targets},
            dont_filter=True,
        )

    def _resolve_targets(self) -> list[Category]:
        """Turn the CLI args into concrete categories, validating each id."""
        if self.all_categories:
            return list(self._index.values())

        group_id: str | None = None
        if self.args.category:
            group_id = self.args.category
        else:
            target_url = self.args.category_url or self.args.url
            if target_url:
                group_id = group_id_from_url(target_url)

        if not group_id:
            return []

        category = self._index.get(group_id)
        if category is None:
            raise ValueError(
                f"Unknown Williams-Sonoma category id {group_id!r}; it is not in the "
                "category tree returned by "
                f"{CATEGORY_TREE_URL} ({len(self._index)} ids available). "
                "Use a top-level id such as 'cookware' or a leaf such as "
                "'cookware-sets', or -a all_categories=true."
            )
        return [category]

    def parse_context(self, response: scrapy.http.Response):
        """Read `constructorKey` out of the page's SSR bootstrap state."""
        self._reject_challenge(response, "category page")
        targets = response.meta.get("targets") or []
        match = CONSTRUCTOR_KEY_RE.search(response.text)
        if not match:
            raise RuntimeError(
                f"No constructorKey found in window.__INITIAL_STATE__ on {response.url}. "
                "The Shop micro-frontend bootstrap state may have moved; refusing to "
                "browse with a hardcoded/rotated key."
            )
        self._constructor_key = match.group(1)
        self.logger.info("Williams-Sonoma constructorKey read from %s", response.url)

        for category in targets:
            yield self._browse_request(category, page=1)

    def _browse_request(self, category: Category, *, page: int):
        assert self._constructor_key, "constructorKey must be read before browsing"
        query = urlencode(
            [
                ("key", self._constructor_key),
                ("num_results_per_page", self.page_size),
                ("page", page),
                ("fmt_options[groups_max_depth]", 1),
                ("fmt_options[groups_start]", "current"),
                ("section", "Products"),
            ]
        )
        url = f"{self.BROWSE_BASE}/browse/group_id/{category.group_id}?{query}"
        return scrapy.Request(
            url,
            callback=self.parse_browse,
            headers={
                "Accept": "application/json",
                "Referer": category.url,
                "X-Requested-With": "XMLHttpRequest",
            },
            meta={"category": category, "page": page},
            dont_filter=True,
        )

    # ------------------------------------------------------------------- parse

    def parse_browse(self, response: scrapy.http.Response):
        category: Category = response.meta["category"]
        page = int(response.meta["page"])

        self._reject_challenge(response, "browse API")
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Constructor browse returned a non-JSON body for "
                f"{category.group_id} page {page}: {response.text[:200]!r}"
            ) from exc

        if not isinstance(payload, dict):
            raise RuntimeError(
                f"Constructor browse returned {type(payload).__name__}, expected an "
                f"object envelope for {category.group_id} page {page}; the API "
                "contract may have changed."
            )

        envelope = payload.get("response")
        if not isinstance(envelope, dict):
            raise RuntimeError(
                f"Constructor browse response for {category.group_id} page {page} is "
                f"missing the 'response' envelope (keys: {sorted(payload)}); the API "
                "contract may have changed."
            )
        results = envelope.get("results")
        if not isinstance(results, list):
            raise RuntimeError(
                f"Constructor browse returned results as {type(results).__name__}, "
                f"expected list for {category.group_id} page {page}"
            )

        total = envelope.get("total_num_results") or 0
        try:
            total = int(total)
        except (TypeError, ValueError):
            total = 0

        if not results:
            if total or page == 1:
                # A page-1 empty result is the interesting case: the id is real in
                # the taxonomy but is an editorial/collection hub with no
                # Constructor group behind it. Say so instead of failing quietly.
                self.logger.warning(
                    "Williams-Sonoma category %s (%s) returned 0 products on page %s "
                    "(total_num_results=%s); it is an editorial hub with no browsable "
                    "inventory",
                    category.group_id,
                    category.url,
                    page,
                    total,
                )
            return

        self.logger.info(
            "Williams-Sonoma %s page %s: %s results (total %s)",
            category.group_id,
            page,
            len(results),
            total,
        )

        for result in results:
            product = result.get("data") if isinstance(result, dict) else None
            if not isinstance(product, dict):
                self.logger.warning(
                    "Skipping a browse result with no 'data' object for %s page %s",
                    category.group_id,
                    page,
                )
                continue
            item = self._product_item(product, category, page)
            if item["item_id"] in self._seen_ids:
                continue
            self._seen_ids.add(item["item_id"])
            yield item

        # Pagination: stop at the declared total, at max_pages, or on a page that
        # returned nothing. The total is authoritative when present because
        # Constructor can return a short final page.
        if page >= self.max_pages:
            return
        if total and page * self.page_size >= total:
            return
        yield self._browse_request(category, page=page + 1)

    # ----------------------------------------------------------------- helpers

    def _reject_challenge(self, response: scrapy.http.Response, what: str) -> None:
        if response.status != 200:
            raise RuntimeError(
                f"Williams-Sonoma {what} returned HTTP {response.status} for "
                f"{response.url}"
            )
        content_type = response.headers.get("Content-Type") or b""
        if isinstance(content_type, bytes):
            content_type = content_type.decode("utf-8", "replace")
        if "json" in content_type.lower():
            return
        head = response.text[:2000].lower()
        for marker in CHALLENGE_MARKERS:
            if marker in head:
                raise RuntimeError(
                    f"Williams-Sonoma served an access-denied/challenge body for the "
                    f"{what} at {response.url} (matched {marker!r}); the request was "
                    "not answered by the site."
                )

    def _product_item(
        self,
        product: dict[str, Any],
        category: Category,
        page: int,
    ) -> dict[str, Any]:
        item_id = str(product.get("id") or "").strip()
        if not item_id:
            raise RuntimeError(
                f"Browse result for {category.group_id} page {page} is missing 'id': "
                f"{sorted(product)}; the Constructor contract may have changed."
            )

        # Prefer the sale price, then the lowest listed price, then the regular
        # floor. A discounted item has both, and `salePriceMin` is the one the
        # storefront actually charges.
        sale_min = self._number(product.get("salePriceMin"))
        lowest = self._number(product.get("lowestPrice"))
        regular_min = self._number(product.get("regularPriceMin"))
        price = sale_min or lowest or regular_min

        flags = [str(flag) for flag in product.get("flags") or []]
        raw_url = str(product.get("url") or "").strip()

        return {
            "category": category.group_id,
            "category_name": category.name,
            "parent_category": category.parent_name,
            "item_id": item_id,
            "title": product.get("title"),
            "url": urljoin(SITE_BASE, raw_url) if raw_url else None,
            "brand": self._facet(product, "brand_attr") or self._facet(product, "brand"),
            "sku": product.get("skuid") or product.get("leaderSku"),
            "price": price,
            "regular_price": regular_min,
            "price_min": lowest,
            "price_max": self._number(product.get("highestPrice")),
            "regular_price_min": regular_min,
            "regular_price_max": self._number(product.get("regularPriceMax")),
            "sale_price_min": sale_min,
            "sale_price_max": self._number(product.get("salePriceMax")),
            "discount_percent": self._number(product.get("maxDiscountPercent")),
            "price_type": product.get("productPriceType"),
            "currency": "USD",
            "image_url": (str(product.get("image_url") or "").strip() or None),
            "image_alt": product.get("title"),
            "alt_images_count": self._count(product.get("altImages"), ","),
            "swatches_count": self._count(product.get("swatchPrices"), "~"),
            "flags": flags,
            "pip_type": product.get("pipType"),
            "quick_buy": bool(product.get("eligibleForQuickBuy")),
            "description": product.get("description"),
            "short_description": product.get("productBlurb"),
            # `prodinfo` is the measured spec list, not marketing copy.
            "product_details": product.get("prodinfo"),
            "group_ids": [str(g) for g in product.get("group_ids") or []],
            "page": page,
            "category_url": category.url,
            "source": "williams_sonoma_constructor_browse",
            "raw": product,
        }

    @staticmethod
    def _number(value: Any) -> float | None:
        """Constructor prices arrive as JSON numbers; keep them numeric."""
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            return float(str(value).strip())
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _facet(product: dict[str, Any], name: str) -> str | None:
        """First value of a named per-product facet, if the facet is present."""
        for facet in product.get("facets") or []:
            if not isinstance(facet, dict) or facet.get("name") != name:
                continue
            values = [v for v in facet.get("values") or [] if v not in (None, "")]
            if not values:
                continue
            return ", ".join(str(value) for value in values)
        return None

    @staticmethod
    def _count(value: Any, separator: str) -> int:
        """`altImages` is a comma list, `swatchPrices` a `~` list -- both optional."""
        if not isinstance(value, str) or not value.strip():
            return 0
        return len([part for part in value.split(separator) if part.strip()])