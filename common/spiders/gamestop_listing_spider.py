from __future__ import annotations

"""GameStop listing spider (issue #159).

GameStop runs on Salesforce Commerce Cloud (Demandware) with a Constructor.io
"hybrid" browse front end. The critical detail: **the PLP HTML contains no
product data**. The server renders empty tile shells that carry only a
`data-pid`, and `main.js` then hydrates every tile from a first-party JSON
controller:

    /on/demandware.store/Sites-gamestop-us-Site/default/Tile-GetProductsJSON
        ?deliveryAttribute=&data=<comma-separated-pids>&useTileImage=true

So this spider uses exactly one data direction -- that JSON controller. No HTML
tile scraping, no Constructor.io browse API, no rendered-browser fallback. If the
controller stops answering, the spider fails loudly instead of silently
degrading to empty tile shells.

Flow:
    category page (or Search-UpdateGrid fragment)
        -> parse data-pid list + data-cnstrc-num-results total
        -> batch pids (TILE_BATCH_SIZE per request) to Tile-GetProductsJSON
        -> emit one item per returned product
        -> repeat with Search-UpdateGrid?cgid=<slug>&start=<n>&sz=<sz>
           until start >= total or max_pages is reached

Note the `cgid` used for pagination is the Demandware category id (`consoles`,
`toys-and-collectibles-funko`, ...), which is *not* the friendly URL slug. It is
read back from the page's own `Search-UpdateGrid` link rather than derived from
the URL, because the two diverge for most categories.
"""

import json
import re
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.gamestop_categories import GAMESTOP_CATEGORIES

_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")


def _slugify(value: str) -> str:
    return _SLUG_CLEAN_RE.sub("-", value.lower()).strip("-")


def category_slug(url: str) -> str:
    """Build a stable, unique `category` key from a GameStop category URL.

    Leaf slugs collide across departments (`nintendo-switch` exists under both
    `video-games` and `consoles-hardware`), so the full URL path is used, e.g.
    `consoles-hardware-nintendo-switch`.
    """
    # `%7C` decodes to a pipe ("xbox-series-x|s"), which must be normalized before
    # slugging or the key reads `x-7cs`.
    path = unquote(url.split("gamestop.com", 1)[-1].split("?", 1)[0].strip("/"))
    return _slugify(path)


def _load_categories() -> list[dict[str, str]]:
    categories: list[dict[str, str]] = []
    seen: set[str] = set()
    for department, urls in GAMESTOP_CATEGORIES.items():
        for url in urls:
            if url in seen:
                continue
            seen.add(url)
            slug = category_slug(url)
            categories.append(
                {
                    "category": slug,
                    "department": department,
                    "name": url.rstrip("/").rsplit("/", 1)[-1]
                    .replace("%7C", "|")
                    .replace("-", " "),
                    "url": url,
                }
            )
    return categories


class GamestopListingSpider(BaseListingSpider):
    name = "gamestop_listing"
    allowed_domains = ["gamestop.com", "www.gamestop.com", "media.gamestop.com"]
    require_category_arg = False

    SITE_BASE = "https://www.gamestop.com"
    CONTROLLER_BASE = "/on/demandware.store/Sites-gamestop-us-Site/default"
    TILE_CONTROLLER = f"{CONTROLLER_BASE}/Tile-GetProductsJSON"
    GRID_CONTROLLER = f"{CONTROLLER_BASE}/Search-UpdateGrid"

    # GameStop's own grid controller honours `sz` well past the default 20 (60 was
    # verified live), but the tile JSON controller is only ever fed one page worth
    # of pids, so these stay coupled to a single grid request.
    PAGE_SIZE = 60
    # Upper bound on pids per Tile-GetProductsJSON call. The storefront batches
    # 20 in main.js; larger batches are untested against the controller, so the
    # request is chunked rather than risking a silently truncated response.
    TILE_BATCH_SIZE = 20

    categories = _load_categories()

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "department",
            "item_id",
            "title",
            "url",
            "image_url",
            "image_alt",
            "price",
            "list_price",
            "pro_price",
            "price_min",
            "price_max",
            "currency",
            "availability",
            "is_digital_product",
            "badge",
            "rating",
            "reviews_count",
            "market_price",
            "release_date",
            "product_platform",
            "short_description",
            "page",
            "category_url",
            "source",
            "raw",
        ],
    }

    # A response that is not the JSON envelope (bot wall, geo-block, controller
    # error page) looks like an HTML body. Matched case-insensitively on purpose.
    CHALLENGE_MARKERS = (
        "access denied",
        "captcha",
        "are you a human",
        "request unsuccessful",
        "pardon the interruption",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield self._grid_request(category_url, page=1)

    def _grid_request(
        self,
        category_url: str,
        *,
        page: int,
        cgid: str | None = None,
        start: int = 0,
    ):
        """Request a grid of tile shells.

        Page 1 fetches the friendly category URL. Later pages use the Demandware
        `Search-UpdateGrid` controller with the `cgid` discovered from page 1 --
        the friendly slug (`consoles-hardware`) is not a valid cgid (`consoles`).

        `start` is the running item offset rather than `page * PAGE_SIZE`: the
        friendly category URL renders the storefront's default page size (20),
        which is smaller than `PAGE_SIZE`, so a computed offset would skip items.
        """
        if page == 1 or not cgid:
            url = category_url
        else:
            url = urljoin(
                self.SITE_BASE,
                f"{self.GRID_CONTROLLER}?{urlencode({'cgid': cgid, 'start': start, 'sz': self.PAGE_SIZE})}",
            )
        return scrapy.Request(
            url,
            callback=self.parse_grid,
            headers={
                "Accept": "text/html,application/xhtml+xml",
                "Referer": category_url,
                "X-Requested-With": "XMLHttpRequest",
            },
            meta={
                "page": page,
                "category_url": category_url,
                "cgid": cgid,
                "start": start,
            },
            dont_filter=True,
        )

    # ------------------------------------------------------------------ parse

    def parse_grid(self, response: scrapy.http.Response, **kwargs):
        page = int(response.meta["page"])
        category_url = response.meta["category_url"]
        cgid = response.meta.get("cgid")
        start = int(response.meta.get("start") or 0)
        self._reject_challenge(response)

        pids = response.css('[data-pid]::attr(data-pid)').getall()
        if not pids:
            # An empty grid means the cgid/URL does not resolve to a product
            # listing. Silently returning would hide a broken category map.
            raise RuntimeError(
                f"GameStop grid returned no [data-pid] tiles for page {page} of "
                f"{category_url}; the category slug/cgid may be stale "
                "(SFCC renders an empty shell grid rather than a 404)."
            )

        total = self._total_results(response)
        # The friendly slug is not the Demandware cgid, so resolve it here from the
        # grid page itself (the tile JSON response carries no navigation links).
        cgid = cgid or self._cgid_from(response)
        self.logger.info(
            "GameStop %s page %s: %s pids (total %s, cgid %s)",
            category_url,
            page,
            len(pids),
            total,
            cgid,
        )

        for batch_start in range(0, len(pids), self.TILE_BATCH_SIZE):
            batch = pids[batch_start : batch_start + self.TILE_BATCH_SIZE]
            yield self._tile_request(
                batch,
                category_url=category_url,
                page=page,
                cgid=cgid,
                # Only the first batch continues pagination; otherwise page 2 would
                # be requested once per batch.
                allow_next_page=batch_start == 0,
                total=total,
                # Pagination advances by the whole grid, not this batch: a 60-pid
                # grid sent as 3 batches must still advance past all 60.
                grid_start=start,
                grid_size=len(pids),
            )

    def _tile_request(
        self,
        pids: list[str],
        *,
        category_url: str,
        page: int,
        cgid: str | None,
        allow_next_page: bool,
        total: int | None = None,
        grid_start: int = 0,
        grid_size: int = 0,
    ):
        # The param is `data` (comma list) or `pid` (single) -- `pids=` returns an
        # empty productsJSON.
        query = urlencode({"deliveryAttribute": "", "data": ",".join(pids), "useTileImage": "true"})
        return scrapy.Request(
            urljoin(self.SITE_BASE, f"{self.TILE_CONTROLLER}?{query}"),
            callback=self.parse_tiles,
            headers={
                "Accept": "application/json",
                "Referer": category_url,
                "X-Requested-With": "XMLHttpRequest",
            },
            meta={
                "page": page,
                "category_url": category_url,
                "cgid": cgid,
                "pids": pids,
                "total": total,
                "grid_start": grid_start,
                "grid_size": grid_size,
                "allow_next_page": allow_next_page,
                "category": self._category_for(category_url),
            },
            dont_filter=True,
        )

    def parse_tiles(self, response: scrapy.http.Response, **kwargs):
        page = int(response.meta["page"])
        category_url = response.meta["category_url"]
        cgid = response.meta.get("cgid")
        category = response.meta.get("category")
        total = response.meta.get("total")
        grid_start = int(response.meta.get("grid_start") or 0)
        grid_size = int(response.meta.get("grid_size") or 0)
        self._reject_challenge(response)

        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"GameStop Tile-GetProductsJSON returned a non-JSON body for page {page} "
                f"of {category_url}: {response.text[:200]!r}"
            ) from exc

        products = payload.get("productsJSON")
        if products is None:
            raise RuntimeError(
                f"GameStop Tile-GetProductsJSON response is missing 'productsJSON' "
                f"(keys: {sorted(payload)}); the controller contract may have changed."
            )
        if not isinstance(products, dict):
            raise RuntimeError(
                f"GameStop Tile-GetProductsJSON returned productsJSON as "
                f"{type(products).__name__}, expected object"
            )

        # An empty dict means the pid batch was expired/invalid. This is expected
        # for retired pids, so log it and continue instead of crashing the crawl.
        if not products:
            self.logger.warning(
                "GameStop returned an empty productsJSON for a %s-pid batch on page %s "
                "of %s; skipping the batch",
                len(response.meta.get("pids") or []),
                page,
                category_url,
            )
            return

        emitted = 0
        for product in products.values():
            item = self._product_item(product, category_url, category, page)
            if item is None:
                continue
            if item["item_id"] in self._seen_ids:
                continue
            self._seen_ids.add(item["item_id"])
            emitted += 1
            yield item

        if not response.meta.get("allow_next_page") or page >= self.max_pages:
            return

        if total is None:
            total = self._total_results(response)
        # Next offset is the end of the grid this batch came from -- not the end of
        # the batch, which would re-request the middle of the grid.
        next_start = grid_start + (grid_size or len(response.meta.get("pids") or []))
        if total and next_start >= int(total):
            return
        if not emitted:
            # No new ids on a later page means the grid looped or the category
            # ran out; stop rather than paginating forever.
            return

        if not cgid:
            # Without a cgid the next page cannot be requested through
            # Search-UpdateGrid; stop rather than re-requesting page 1 forever.
            self.logger.warning(
                "No Demandware cgid found for %s; stopping after page %s",
                category_url,
                page,
            )
            return
        yield self._grid_request(category_url, page=page + 1, cgid=cgid, start=next_start)

    # ----------------------------------------------------------------- helpers

    def _reject_challenge(self, response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(
                f"GameStop returned HTTP {response.status} for {response.url}"
            )
        ctype = response.headers.get("Content-Type") or b""
        if isinstance(ctype, bytes):
            ctype = ctype.decode("utf-8", "replace")
        if "json" in ctype.lower():
            return
        head = response.text[:2000].lower()
        for marker in self.CHALLENGE_MARKERS:
            if marker in head:
                raise RuntimeError(
                    f"GameStop served an access-denied/challenge body for {response.url} "
                    f"(matched {marker!r}); the request was not answered by the storefront."
                )

    @staticmethod
    def _total_results(response: scrapy.http.Response) -> int:
        """Read `data-cnstrc-num-results` from a grid fragment."""
        match = response.css('[data-cnstrc-num-results]::attr(data-cnstrc-num-results)').get()
        if not match:
            return 0
        try:
            return int(str(match).strip())
        except ValueError:
            return 0

    @staticmethod
    def _cgid_from(response: scrapy.http.Response) -> str | None:
        """Recover the Demandware cgid from the page's own Search-UpdateGrid link.

        The friendly URL slug is not the cgid (`consoles-hardware` -> `consoles`,
        `collectibles/funko` -> `toys-and-collectibles-funko`), and the mapping is
        not derivable offline, so it is read from the sort/grid links the server
        already rendered.
        """
        if not getattr(response, "selector", None):
            return None
        for href in response.css("a::attr(href)").getall():
            if "Search-UpdateGrid" not in href:
                continue
            query = href.split("?", 1)[-1]
            for key, value in parse_qsl(query, keep_blank_values=True):
                if key == "cgid" and value:
                    return value
        return None

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

    def _product_item(
        self,
        product: dict[str, Any],
        category_url: str,
        category: str | None,
        page: int,
    ) -> dict[str, Any] | None:
        item_id = str(product.get("id") or "").strip()
        if not item_id:
            raise RuntimeError(
                f"GameStop tile entry is missing 'id': {sorted(product)}; "
                "the Tile-GetProductsJSON contract may have changed."
            )

        price = product.get("price") or {}
        sale = (price.get("sale") or "").strip() or None
        base = (price.get("base") or "").strip() or None
        availability = product.get("availability") or {}
        ratings = product.get("ratings") or {}
        image = product.get("image") or {}
        raw_url = (product.get("url") or "").strip()

        return {
            "category": category,
            "department": self._department_for(category) if category else None,
            "item_id": item_id,
            "title": product.get("name"),
            "url": urljoin(self.SITE_BASE, raw_url) if raw_url else None,
            "image_url": (image.get("base") or "").strip() or None,
            "image_alt": image.get("title"),
            # Prefer the sale price, fall back to base -- GameStop fills exactly one
            # of the two for a given tile.
            "price": sale or base,
            "list_price": base,
            "pro_price": (price.get("pro") or "").strip() or None,
            "price_min": (price.get("min") or "").strip() or None,
            "price_max": (price.get("max") or "").strip() or None,
            "currency": "USD",
            "availability": self._availability(availability),
            "is_digital_product": bool(availability.get("isDigitalProduct")),
            "badge": product.get("badge"),
            "rating": ratings.get("percentage"),
            "reviews_count": ratings.get("count"),
            "market_price": product.get("marketPrice"),
            "release_date": product.get("releaseDate"),
            "product_platform": product.get("productPlatform") or None,
            "short_description": product.get("shortDescription") or None,
            "page": page,
            "category_url": category_url,
            "source": "gamestop_tile_json",
            "raw": product,
        }

    @staticmethod
    def _availability(availability: dict[str, Any]) -> str:
        if availability.get("available"):
            return "InStock"
        if availability.get("readyToOrder"):
            return "PreOrder"
        if availability.get("preorder"):
            return "PreOrder"
        return "OutOfStock"