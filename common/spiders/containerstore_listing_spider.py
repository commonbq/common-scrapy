from __future__ import annotations

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.containerstore_categories import BASE_URL, CONTAINERSTORE_CATEGORIES




class ContainerStoreListingSpider(BaseListingSpider):
    """containerstore.com listings from the server-rendered Next.js `__NEXT_DATA__` hydration."""

    name = "containerstore_listing"
    allowed_domains = ["containerstore.com", "www.containerstore.com", "localhost", "127.0.0.1"]
    categories = CONTAINERSTORE_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "leaf", "item_id", "sku_id", "title",
            "url", "image_url", "image_alt", "product_type", "color_option_count",
            "color_options", "price", "original_price", "discount_percentage", "currency",
            "on_sale", "out_of_stock", "rating", "reviews_count", "badge", "page", "position",
            "total_count", "last_page", "source_url", "source", "raw",
        ],
    }

    _hydration = re.compile(r'<script id="__NEXT_DATA__" type="application/json"[^>]*>')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
            },
            meta={
                "category": self.category or selected.get("category") or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "leaf": selected.get("leaf"),
                "page": 1,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"containerstore listing returned HTTP {response.status}: {response.url}")
        page_props = self._page_props(response.text, response.url)
        initial_state = page_props.get("initialState")
        if not isinstance(initial_state, dict):
            raise RuntimeError(f"containerstore __NEXT_DATA__ at {response.url} has no props.pageProps.initialState")
        plp = initial_state.get("plp")
        if not isinstance(plp, dict):
            raise RuntimeError(f"containerstore hydration has no plp state at {response.url}")
        plp_data = plp.get("data")
        plp_data = plp_data if isinstance(plp_data, dict) else {}
        current_page = self._integer(plp_data.get("currentPage")) or 1
        product_ids = self._page_product_ids(plp, current_page)

        # `pageType` is not a usable signal here: a leaf that hydrates as `PrismicTemplate`
        # carries a full 60-item grid, while a `/12` page can hydrate as `Category` with none.
        # The presence of an ordered grid in `plp.entities` is the only reliable discriminator,
        # and department pages carry none -- they render a subcategory tile grid instead.
        if not product_ids:
            self._log_non_product_page(response, page_props, plp_data, current_page)
            return

        # The breadcrumbs the storefront ships are the authoritative department / subcategory /
        # leaf path, so they fill the taxonomy fields even when the spider was driven by
        # `-a url=` and has no matching entry in `categories`.
        department, subcategory, leaf = self._crumbs(response.meta, plp_data)
        total_count = self._integer(plp_data.get("totalCount"))
        last_page = self._integer(plp_data.get("lastPage"))
        entities = self._product_entities(initial_state)

        for position, product_id in enumerate(product_ids, start=1):
            product = entities.get(str(product_id))
            if not isinstance(product, dict):
                self.logger.warning(
                    "Skipping product id %s at %s: no matching products.entities record",
                    product_id, response.url,
                )
                continue
            item_id = str(product.get("id") or product_id)
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(
                product, response, current_page, position, total_count, last_page,
                department, subcategory, leaf,
            )

        if current_page >= self.max_pages:
            return
        if last_page is not None and current_page >= last_page:
            return

        next_url = self._next_page_url(response.url, plp_data, current_page)
        if not next_url:
            return
        yield scrapy.Request(
            next_url,
            callback=self.parse,
            headers=response.request.headers,
            meta={**response.meta, "page": current_page + 1, "department": department,
                  "subcategory": subcategory, "leaf": leaf},
            dont_filter=True,
        )

    def _log_non_product_page(self, response, page_props: dict, plp_data: dict, page: int) -> None:
        """Department pages hydrate a subcategory tile grid instead of a product grid."""
        if page > 1:
            self.logger.info("Stopping at %s: page %d has an empty product grid", response.url, page)
            return
        tiles = plp_data.get("categories")
        tiles = [t for t in tiles if isinstance(t, dict) and t.get("generatedUrl")] \
            if isinstance(tiles, list) else []
        self.logger.info(
            "No product grid at %s (pageType=%r, totalCount=%s, %d subcategory tile(s)). "
            "Crawl a `/12` or `/123` leaf category to get items.",
            response.url,
            page_props.get("pageType"),
            plp_data.get("totalCount"),
            len(tiles),
        )

    @staticmethod
    def _crumbs(meta: dict, plp_data: dict) -> tuple:
        """Prefer the taxonomy the spider was started with; fall back to page breadcrumbs.

        The breadcrumb depth mirrors the catalogue levels: a `/1` department page lists one
        crumb, a `/12` subcategory two, and a `/123` leaf three.
        """
        crumbs = plp_data.get("breadcrumbs")
        names = [c.get("name") for c in crumbs if isinstance(c, dict) and c.get("name")] \
            if isinstance(crumbs, list) else []
        department = meta.get("department") or (names[0] if names else None)
        subcategory = meta.get("subcategory") or (names[1] if len(names) > 1 else None)
        leaf = meta.get("leaf") or (names[2] if len(names) > 2 else None)
        return department, subcategory, leaf

    def _item(
        self,
        product: dict,
        response,
        page: int,
        position: int,
        total_count: int | None,
        last_page: int | None,
        department: str | None,
        subcategory: str | None,
        leaf: str | None,
    ) -> dict:
        price_data = product.get("price")
        price_data = price_data if isinstance(price_data, dict) else {}
        # The storefront labels the pre-discount amount `retailPrice` and the current one
        # `salePrice`, but only fills in the numeric `minRetailPrice` / `minSalePrice` when the
        # product is genuinely reduced. The displayed strings are "$4.49 - $71.91" ranges for
        # multisku products, so they cannot be parsed into a single figure.
        price = self._number(price_data.get("minSalePrice"))
        original_price = self._number(price_data.get("minRetailPrice"))
        discount = None
        if price is not None and original_price:
            discount = round((original_price - price) / original_price * 100, 2)
            if discount <= 0:
                # `isOnSale` is frequently true with zero savings; only a real reduction counts.
                price, original_price, discount = original_price, None, None

        swatches = product.get("colorSwatcheInfo")
        swatches = swatches if isinstance(swatches, dict) else {}
        values = swatches.get("values")
        values = [v for v in values if isinstance(v, dict)] if isinstance(values, list) else []
        badge = product.get("badge")
        badge = badge if isinstance(badge, dict) else {}

        return {
            "category": response.meta.get("category"),
            "department": department,
            "subcategory": subcategory,
            "leaf": leaf,
            "item_id": str(product.get("id") or "") or None,
            "sku_id": str(product.get("skuId") or "") or None,
            "title": str(product.get("displayName") or "").strip() or None,
            "url": self._absolute(product.get("productGeneratedUrl"), response.url),
            "image_url": self._absolute(product.get("imageUrl"), response.url),
            "image_alt": str(product.get("imageAltText") or "").strip() or None,
            "product_type": str(product.get("productType") or "").strip() or None,
            "color_option_count": len(values) or None,
            "color_options": ", ".join(str(v.get("value")) for v in values if v.get("value")) or None,
            "price": price,
            "original_price": original_price,
            "discount_percentage": discount,
            "currency": str(product.get("currency") or "").strip() or None,
            "on_sale": bool(price_data.get("isOnSale")),
            "out_of_stock": bool(product.get("isOutOfStock")),
            "rating": self._number(product.get("rating")),
            "reviews_count": self._integer(product.get("reviewCount")),
            "badge": str(badge.get("name") or "").strip() or None,
            "page": page,
            "position": position,
            "total_count": total_count,
            "last_page": last_page,
            "source_url": response.url,
            "source": "containerstore_next_data_products_entities",
            "raw": product,
        }

    def _page_props(self, document: str, url: str) -> dict:
        match = self._hydration.search(document or "")
        if not match:
            raise RuntimeError(f"No containerstore __NEXT_DATA__ hydration blob found at {url}")
        try:
            state, _ = json.JSONDecoder().raw_decode(document, match.end())
            page_props = state["props"]["pageProps"]
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(
                f"containerstore __NEXT_DATA__ at {url} has no props.pageProps object"
            ) from exc
        if not isinstance(page_props, dict):
            raise RuntimeError(f"containerstore __NEXT_DATA__ at {url} has a non-object props.pageProps")
        return page_props

    @staticmethod
    def _page_product_ids(plp: dict, current_page: int) -> list:
        """`plp.entities[str(page)]` holds the ordered ids for that page only."""
        entities = plp.get("entities")
        page_entity = entities.get(str(current_page)) if isinstance(entities, dict) else None
        product_ids = page_entity.get("products") if isinstance(page_entity, dict) else None
        return [pid for pid in product_ids if isinstance(pid, int)] if isinstance(product_ids, list) else []

    @staticmethod
    def _product_entities(initial_state: dict) -> dict:
        """`products.entities` is the normalized product record map keyed by product id."""
        products = initial_state.get("products")
        entities = products.get("entities") if isinstance(products, dict) else None
        return entities if isinstance(entities, dict) else {}

    def _next_page_url(self, current_url: str, plp_data: dict, current_page: int) -> str | None:
        """Pagination is plain SSR: the payload hands over the absolute path to the next page."""
        next_url = plp_data.get("nextPageUrl")
        if isinstance(next_url, str) and next_url.strip():
            return urljoin(current_url, next_url.strip())
        last_page = self._integer(plp_data.get("lastPage"))
        if last_page and current_page < last_page:
            page_size = self._integer(plp_data.get("pageSize")) or 60
            return f"{current_url}?p={current_page * page_size}&ps={page_size}"
        return None

    @staticmethod
    def _absolute(url, base: str) -> str | None:
        if not isinstance(url, str) or not url.strip():
            return None
        url = url.strip()
        return url if url.startswith("http") else urljoin(base or BASE_URL, url)

    @staticmethod
    def _number(value):
        if isinstance(value, bool) or value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        if isinstance(value, bool) or value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None