from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.victoriassecret_categories import VICTORIASSECRET_CATEGORIES

SITE_BASE = "https://www.victoriassecret.com"
# Page 0 is served from the bare ``/stacks/v46/`` (trailing slash); the load
# more page is ``/stacks/v46/stack``. Dropping the trailing slash makes the
# gateway answer a flat ``404 page not found``.
API_BASE = "https://api.victoriassecret.com/stacks/v46"
PAGE_SIZE = 96

# Images arrive as extension-less relative paths (e.g.
# ``png/zz/26/08/28/01/112955637I65_OM_F``) and resolve under
# ``/p/<w>x<h>/<path>.jpg``. Only the 380x507 rendition is confirmed to serve
# (640x853 and 1200x1500 both 404).
IMAGE_BASE = "https://www.victoriassecret.com/p/380x507"

_CLIENT_PROPS_RE = re.compile(
    r'<script id="clientProps" type="application/json">(.*?)</script>', re.S
)
_PRICE_RE = re.compile(r"-?\d+(?:\.\d+)?")


def slugify(value: str) -> str:
    """Lowercase ASCII slug, matching the sibling listing spiders."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_money(value: Any) -> float | None:
    """Turn ``"$49.95"`` / ``49.95`` into a float, ``None`` when absent."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = _PRICE_RE.search(str(value))
    return float(match.group(0)) if match else None


def load_categories() -> list[dict[str, str]]:
    """Flatten the ``{brand: {top: {path, subcategories: {group: {label: url}}}}}`` tree.

    Slugs are brand-prefixed (``vs-bras``, ``vs-bras-push-up``) because leaf
    labels collide heavily across departments -- "Bestsellers" alone appears
    under BRAS, PANTIES and NEW! for the ``vs`` brand.
    """
    flat: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(slug: str, brand: str, top: str, sub: str | None, url: str) -> None:
        if not url or not url.startswith("http") or slug in seen:
            return
        seen.add(slug)
        entry = {
            "category": slug,
            "brand": brand,
            "top_category": top,
            "url": url,
        }
        if sub:
            entry["sub_category"] = sub
        flat.append(entry)

    for brand, tops in VICTORIASSECRET_CATEGORIES.items():
        for top_name, top_data in tops.items():
            top_url = top_data.get("path") or ""
            if not top_url:
                continue
            top_slug = f"{brand}-{slugify(top_name)}"
            add(top_slug, brand, top_name, None, top_url)
            # ``subcategories`` is a *group* level (``Group 1`` .. ``Group 5``);
            # its values are the real ``{label: url}`` leaves. Group headings
            # are not reachable pages, so descend one more level.
            for group_name, group_data in top_data.get("subcategories", {}).items():
                if not isinstance(group_data, dict):
                    # Tolerate taxonomies that skip the grouping level.
                    group_data = {group_name: group_data}
                for sub_name, sub_url in group_data.items():
                    if not isinstance(sub_url, str) or sub_url == top_url:
                        continue
                    add(f"{top_slug}-{slugify(sub_name)}", brand, top_name, sub_name, sub_url)

    return flat


class VictoriassecretListingSpider(BaseListingSpider):
    """Victoria's Secret / PINK listings via the first-party ``stacks`` JSON API.

    Single data direction: the category SSR page is read only to discover the
    ``collectionId`` (and brand / ``isBrasOrPanties`` flag) for the requested
    category, then every product comes from ``api.victoriassecret.com``. There is
    no HTML card scraping and no browser fallback.
    """

    name = "victoriassecret_listing"
    allowed_domains = ["victoriassecret.com", "www.victoriassecret.com", "api.victoriassecret.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category",
            "brand",
            "top_category",
            "sub_category",
            "item_id",
            "master_style_id",
            "name",
            "family",
            "color",
            "url",
            "image_url",
            "price",
            "list_price",
            "sale_price",
            "alt_prices",
            "currency",
            "rating",
            "reviews_count",
            "swatch_count",
            "is_new",
            "is_clearance",
            "is_gift_card",
            "page",
            "category_url",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        # Set before BaseListingSpider.__init__, which validates the schema.
        self.categories = load_categories()
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    # -- category plumbing -------------------------------------------------

    def _category_entry(self) -> dict[str, str]:
        for entry in self.categories:
            if entry["category"] == self.category:
                return entry
        raise ValueError(
            f"Unknown category '{self.category}'. "
            f"Available: {', '.join(self.available_categories())}"
        )

    # -- stage 1: category page -> collection id ---------------------------

    def start_requests(self):
        entry = self._category_entry()
        yield scrapy.Request(
            entry["url"],
            callback=self.parse_category_page,
            headers={"Accept": "text/html,application/xhtml+xml"},
            meta={"category": entry},
            dont_filter=True,
        )

    def parse_category_page(self, response: scrapy.http.Response):
        entry = response.meta["category"]
        match = _CLIENT_PROPS_RE.search(response.text)
        if not match:
            self.logger.error('No <script id="clientProps"> block on %s', response.url)
            return
        try:
            client_props = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            self.logger.error("clientProps is not valid JSON on %s: %s", response.url, exc)
            return

        collection_id = (client_props.get("cmsPage") or {}).get("collectionId")
        query_params: dict[str, Any] = {}
        for query in (client_props.get("reactQueryState") or {}).get("queries", []):
            key = query.get("queryKey") or []
            if len(key) > 4 and key[0] == "collectionStacks" and isinstance(key[4], dict):
                query_params = key[4]
                collection_id = collection_id or query_params.get("collectionId")
                break

        if not collection_id:
            self.logger.error("No collectionId in clientProps for %s", response.url)
            return

        # The API brand follows the page's own brand (vs / pink); the taxonomy
        # slug is only a shortcut and must not be re-derived from it.
        brand = client_props.get("brand") or entry["brand"]

        yield self._api_request(
            entry,
            collection_id=str(collection_id),
            brand=str(brand),
            is_bras_or_panties=bool(query_params.get("isBrasOrPanties")),
            offset=0,
            total=None,
        )

    # -- stage 2: stacks API ----------------------------------------------

    def _api_request(
        self,
        entry: dict[str, str],
        *,
        collection_id: str,
        brand: str,
        is_bras_or_panties: bool,
        offset: int,
        total: int | None,
    ) -> scrapy.Request:
        params = {
            "activeCountry": "US",
            "collectionId": collection_id,
            "orderBy": "REC",
            "limit": PAGE_SIZE,
            "isDomestic": "true",
            "isBrasOrPanties": "true" if is_bras_or_panties else "false",
            "brand": brand,
            "maxSwatches": 8,
            "isPersonalized": "true",
            "isWishlistEnabled": "true",
            "recCues": "true",
        }
        # Page 0 -> ``/stacks/v46/`` (note trailing slash) returns the list *and*
        # ``TotalItems``. Later pages -> ``/stacks/v46/stack`` with ``offset``.
        path = "/" if offset == 0 else "/stack"
        if offset:
            params["offset"] = offset
        url = f"{API_BASE}{path}?{urlencode(params)}"
        return scrapy.Request(
            url,
            callback=self.parse_api_response,
            headers={"Accept": "application/json", "Referer": entry["url"]},
            meta={
                "category": entry,
                "collection_id": collection_id,
                "brand": brand,
                "is_bras_or_panties": is_bras_or_panties,
                "offset": offset,
                "total": total,
            },
            dont_filter=True,
        )

    def parse_api_response(self, response: scrapy.http.Response):
        entry = response.meta["category"]
        offset = response.meta["offset"]
        if response.status != 200:
            self.logger.error("API HTTP %s for %s", response.status, response.url)
            return
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as exc:
            self.logger.error("API returned non-JSON for %s: %s", response.url, exc)
            return

        # Page 0 -> ``{"stacks": [{"list": [...]}], "TotalItems": n}``.
        # Later pages -> ``{"productList": [...]}`` at the top level.
        total = response.meta.get("total")
        if offset == 0 and isinstance(data.get("stacks"), list) and data["stacks"]:
            stack = data["stacks"][0] or {}
            products = stack.get("list") or []
            total = data.get("TotalItems") or stack.get("totalProducts") or 0
        else:
            products = data.get("productList") or []

        if not products:
            self.logger.info(
                "No products at offset %s for %s (total=%s)", offset, entry["url"], total
            )
            return

        for product in products:
            item = self._product_item(product, entry, page=offset // PAGE_SIZE + 1)
            if item is not None:
                yield item

        # Advance by what the API actually served, not by PAGE_SIZE.
        next_offset = offset + len(products)
        if offset == 0 and not total:
            self.logger.warning("No TotalItems for %s; stopping after page 1", entry["url"])
            return
        if total is not None and next_offset >= total:
            return
        if (offset // PAGE_SIZE) + 1 >= self.max_pages:
            return

        yield self._api_request(
            entry,
            collection_id=response.meta["collection_id"],
            brand=response.meta["brand"],
            is_bras_or_panties=response.meta["is_bras_or_panties"],
            offset=next_offset,
            total=total,
        )

    # -- item mapping ------------------------------------------------------

    def _product_item(
        self, product: dict[str, Any], entry: dict[str, str], *, page: int
    ) -> dict[str, Any] | None:
        item_id = str(product.get("id") or "").strip()
        if not item_id:
            self.logger.warning("Skipping product with no id in %s", entry["url"])
            return None
        if item_id in self._seen_ids:
            return None
        self._seen_ids.add(item_id)

        images = product.get("productImages") or []
        image_url = urljoin(f"{IMAGE_BASE}/", f"{images[0]}.jpg") if images else None

        price = parse_money(product.get("price"))
        sale_price = parse_money(product.get("salePrice"))
        # Shelf price stays in ``price``; a live sale price becomes ``sale_price``
        # and the shelf price is mirrored into ``list_price``.
        return {
            "category": entry["category"],
            "brand": entry["brand"],
            "top_category": entry["top_category"],
            "sub_category": entry.get("sub_category"),
            "item_id": item_id,
            "master_style_id": product.get("masterStyleId"),
            "name": product.get("name"),
            "family": product.get("family"),
            "color": product.get("genericColor"),
            "url": urljoin(SITE_BASE, product.get("url") or ""),
            "image_url": image_url,
            "price": sale_price if sale_price is not None else price,
            "list_price": price if sale_price is not None else None,
            "sale_price": sale_price,
            "alt_prices": product.get("altPrices") or [],
            "currency": "USD",
            "rating": product.get("rating"),
            "reviews_count": product.get("totalReviewCount"),
            "swatch_count": product.get("swatchCount"),
            "is_new": product.get("isNew"),
            "is_clearance": product.get("isClearance"),
            "is_gift_card": product.get("isGiftCard"),
            "page": page,
            "category_url": entry["url"],
            "source": self.name,
            "raw": product,
        }
