from __future__ import annotations

import json
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.shopbop_categories import BASE_URL, SHOPBOP_CATEGORIES


# The hydration blob is assigned to this global inside a `DOMContentLoaded` listener.
HYDRATE_MARKER = "window.__shopbop_sca_hydrate__"

# Image `src` values in the payload are storefront-relative paths. The SSR <img> tags the
# same page renders resolve them against this CDN base -- note the `/p` segment, which the
# bare `.../G/01/Shopbop/prod/...` form does not serve (it answers `Not Found`).
IMAGE_CDN = "https://m.media-amazon.com/images/G/01/Shopbop/p"

# Shopbop sizes its images with an Amazon-style transform suffix on the filename stem. The
# raw `.jpg` path in the payload 404s, so the suffix the storefront itself renders is added.
IMAGE_SUFFIX = "._QL90_UX564_.jpg"

# The PLP React Query is identified by its `products` payload, not by its query key name or
# by a generated component/class name.
PRODUCTS_QUERY_KEY = "products"

# The storefront asks the products query for out-of-stock items too when a user opts in;
# the default PLP request sets this false, which is why almost every grid is fully in stock.
PAGE_SIZE = 100


class ShopbopListingSpider(BaseListingSpider):
    """shopbop.com listings from the server-rendered `window.__shopbop_sca_hydrate__` payload."""

    name = "shopbop_listing"
    allowed_domains = ["shopbop.com", "www.shopbop.com", "localhost", "127.0.0.1"]
    categories = SHOPBOP_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "leaf", "folder_id", "item_id", "sku_id",
            "title", "brand", "brand_url", "url", "image_url", "image_url_count", "color",
            "color_code", "color_option_count", "color_options", "size_option_count",
            "size_options", "size_scale", "price", "original_price", "discount_percentage",
            "currency", "on_sale", "final_sale", "out_of_stock", "rating", "reviews_count",
            "product_type", "product_category", "gender", "attribute_icons",
            "page", "position", "total_count", "offset", "source_url", "source", "raw",
            "timestamp",
        ],
    }

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
        selected = next((entry for entry in self.iter_categories() if entry["url"] == target), {})
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
                "offset": 0,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"shopbop listing returned HTTP {response.status}: {response.url}")

        hydrate = self._hydrate(response.text, response.url)
        page_type = hydrate.get("pageType")

        plp = self._products_query(hydrate)
        if plp is None:
            # `/designers` hydrates as pageType="Designer" and `/shop-men` as
            # "MensLandingPage": neither carries a `products` query at all. Those two URLs
            # are excluded from the taxonomy for that reason.
            self.logger.info(
                "No products query in the shopbop hydration at %s (pageType=%r). "
                "Crawl a /br/v=1/<folderId>.htm category to get items.",
                response.url,
                page_type,
            )
            return

        if page_type != "PLP":
            raise RuntimeError(
                f"shopbop hydration at {response.url} reports pageType={page_type!r}, expected 'PLP'"
            )

        page = self._integer(response.meta.get("page")) or 1
        offset = self._integer(response.meta.get("offset")) or 0
        next_offset = self._integer(plp.get("nextOffset"))
        total_count = self._integer(plp.get("totalResults"))
        folder_id = str(plp.get("folderId") or "") or None
        results_title = plp.get("resultsTitle")

        entries = plp.get("products")
        entries = [e for e in entries if isinstance(e, dict)] if isinstance(entries, list) else []
        if not entries:
            raise RuntimeError(
                f"shopbop products query at {response.url} hydrated no product records "
                f"(totalResults={total_count})"
            )

        department, subcategory, leaf = self._taxonomy(response.meta, results_title, folder_id)

        for position, entry in enumerate(entries, start=1):
            product = entry.get("product")
            if not isinstance(product, dict):
                self.logger.warning("Skipping malformed entry %d at %s: no product record", position, response.url)
                continue
            # One item per `productSin`. Colorways and sizes stay in `raw` -- the PLP query
            # does not hydrate per-size records with their own price/stock.
            item_id = str(product.get("productSin") or "").strip()
            if not item_id:
                self.logger.warning("Skipping entry %d at %s: no productSin", position, response.url)
                continue
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(
                product, response, page, position, offset, total_count, next_offset,
                department, subcategory, leaf, folder_id,
            )

        if page >= self.max_pages:
            return
        # `nextOffset` is null on the natural last page (verified on a 81-item category).
        if next_offset is None:
            return
        if total_count is not None and next_offset >= total_count:
            return

        next_url = self._next_page_url(response.url, next_offset)
        if not next_url:
            return
        yield scrapy.Request(
            next_url,
            callback=self.parse,
            headers=response.request.headers,
            meta={**response.meta, "page": page + 1, "offset": next_offset,
                  "department": department, "subcategory": subcategory, "leaf": leaf,
                  "folder_id": folder_id},
            dont_filter=True,
        )

    # ------------------------------------------------------------------ hydration

    @staticmethod
    def _hydrate(document: str, url: str) -> dict:
        """Return the object assigned to `window.__shopbop_sca_hydrate__`.

        The assignment is `window.__shopbop_sca_hydrate__ = { ... };` inside a
        `DOMContentLoaded` listener, so it is read with a balanced `raw_decode` rather
        than a regex -- the blob is a megabyte of nested JSON and contains both `}` and
        `;` inside strings.
        """
        marker = document.find(HYDRATE_MARKER)
        if marker < 0:
            raise RuntimeError(f"No shopbop {HYDRATE_MARKER} hydration blob found at {url}")
        assign = document.find("=", marker) + 1
        while assign < len(document) and document[assign] in " \t\r\n":
            assign += 1
        try:
            hydrate, _ = json.JSONDecoder().raw_decode(document, assign)
        except ValueError as exc:
            raise RuntimeError(
                f"shopbop {HYDRATE_MARKER} at {url} is not a decodable JSON object"
            ) from exc
        if not isinstance(hydrate, dict):
            raise RuntimeError(f"shopbop {HYDRATE_MARKER} at {url} is not a JSON object")
        return hydrate

    @staticmethod
    def _products_query(hydrate: dict) -> dict | None:
        """Find the PLP product result inside the dehydrated React Query cache.

        The cache is reachable at several depths depending on which slots the page
        composes -- `...topLevelSlots["plp-main"].content.slotConfiguration.squareState
        .props.dehydratedState.queries` on a category page, and nested one level deeper
        under a masthead slot on wider grids. Rather than depend on the slot id or the
        generated component names, every `queries` list in the tree is searched for the
        entry that actually hydrates a `products` array.
        """
        for container in ShopbopListingSpider._query_containers(hydrate):
            for query in container:
                if not isinstance(query, dict):
                    continue
                key = query.get("queryKey")
                if not (isinstance(key, list) and key and key[0] == PRODUCTS_QUERY_KEY):
                    continue
                state = query.get("state")
                data = state.get("data") if isinstance(state, dict) else None
                data = data.get("data") if isinstance(data, dict) else None
                if isinstance(data, dict) and isinstance(data.get("products"), list):
                    return data
        return None

    @staticmethod
    def _query_containers(hydrate: dict) -> list:
        containers = []

        def visit(node):
            if isinstance(node, dict):
                queries = node.get("queries")
                if isinstance(queries, list):
                    containers.append(queries)
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)

        visit(hydrate)
        return containers

    # ------------------------------------------------------------------ taxonomy

    @staticmethod
    def _taxonomy(meta: dict, results_title, folder_id: str | None) -> tuple:
        """Prefer the taxonomy the spider was started with, else the page's own titles.

        `-a url=` has no matching taxonomy entry, but the hydration still names the
        category in `resultsTitle` and reports its `folderId`, so those fill the path.
        """
        subcategory = meta.get("subcategory") or (
            str(results_title).strip() if isinstance(results_title, str) and results_title.strip() else None
        )
        department = meta.get("department")
        if not department and subcategory:
            # `apiDepartment` is not consulted here; the group is unknown for `-a url=`
            # runs, so the department stays null rather than being guessed.
            department = None
        return department, subcategory, meta.get("leaf")

    # ------------------------------------------------------------------ items

    def _item(
        self,
        product: dict,
        response,
        page: int,
        position: int,
        offset: int,
        total_count: int | None,
        next_offset: int | None,
        department: str | None,
        subcategory: str | None,
        leaf: str | None,
        folder_id: str | None,
    ) -> dict:
        colors = [c for c in (product.get("colors") or []) if isinstance(c, dict)]
        sizes = [s for s in (product.get("sizes") or []) if isinstance(s, dict)]
        primary_color = colors[0] if colors else {}

        price, original_price, discount, on_sale, final_sale = self._pricing(product, primary_color)
        reviews = product.get("reviews")
        reviews = reviews if isinstance(reviews, dict) else {}
        reviews_count = self._integer(reviews.get("count"))
        icons = [i for i in (product.get("attributeIcons") or []) if isinstance(i, dict)]

        return {
            "category": response.meta.get("category"),
            "department": department,
            "subcategory": subcategory,
            "leaf": leaf,
            "folder_id": folder_id,
            "item_id": str(product.get("productSin") or "") or None,
            "sku_id": str(product.get("productCode") or "").strip() or None,
            "title": str(product.get("shortDescription") or "").strip() or None,
            "brand": str(product.get("designerName") or "").strip() or None,
            "brand_url": self._absolute(product.get("designerUrl"), response.url),
            "url": self._absolute(product.get("productDetailUrl"), response.url),
            "image_url": self._image(primary_color, response.url),
            "image_url_count": self._image_count(primary_color),
            "color": str(primary_color.get("name") or "").strip() or None,
            "color_code": str(primary_color.get("colorCode") or "").strip() or None,
            "color_option_count": len(colors) or None,
            "color_options": self._join(colors, "name"),
            "size_option_count": len(sizes) or None,
            "size_options": self._join(sizes, "name"),
            "size_scale": str(product.get("sizeScaleLocaleLabel") or "").strip() or None,
            "price": price,
            "original_price": original_price,
            "discount_percentage": discount,
            "currency": "USD",
            "on_sale": on_sale,
            "final_sale": final_sale,
            # The default PLP query sets `allowOutOfStockItems: false`, so the storefront
            # filters sold-out products out of the grid before hydration.
            "out_of_stock": not bool(product.get("inStock")),
            # The PLP payload hydrates `average: 0` for every product on the grids checked
            # (women's What's New, women's Sale, men's shoes, beauty makeup), so a rating is
            # only reported when the product actually has reviews behind it.
            "rating": self._number(reviews.get("average")) if reviews_count else None,
            "reviews_count": reviews_count,
            "product_type": str(product.get("productType") or "").strip() or None,
            "product_category": str(product.get("productCategory") or "").strip() or None,
            "gender": str(product.get("gender") or "").strip() or None,
            "attribute_icons": self._join(icons, "label"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "offset": offset,
            "source_url": response.url,
            "source": "shopbop_sca_hydrate_products_query",
            "raw": product,
        }

    @staticmethod
    def _pricing(product: dict, primary_color: dict) -> tuple:
        """Return (price, original_price, discount, on_sale, final_sale).

        `retailPrice.usdPrice` is the numeric pre-discount figure and is present on every
        hydrated product. `lowPrice` / `highPrice` only carry a **formatted** string
        (`"$262.50"`) plus `onSale` and `salePercentage` flags -- there is no numeric sale
        field, so the current price is derived from the retail figure and the percentage.
        That derivation is exact: verified against `lowPrice.price` on all 100 products of
        the women's Sale category (30% off $375.00 -> $262.50). The strings are never
        parsed.
        """
        retail = product.get("retailPrice")
        retail = retail if isinstance(retail, dict) else {}
        original = ShopbopListingSpider._number(retail.get("usdPrice"))

        low = product.get("lowPrice")
        low = low if isinstance(low, dict) else {}
        color_price = primary_color.get("colorPrice")
        color_price = color_price if isinstance(color_price, dict) else {}

        percentage = ShopbopListingSpider._number(low.get("salePercentage"))
        on_sale = bool(low.get("onSale")) and percentage is not None and percentage > 0
        if not on_sale or original is None:
            return original, None, None, False, bool(color_price.get("finalSale"))

        price = round(original * (1 - percentage / 100), 2)
        # A 30%-off ticket that rounds back onto the retail price is not a markdown.
        if price >= original:
            return original, None, None, False, bool(color_price.get("finalSale"))
        return price, original, round(percentage, 2), True, bool(color_price.get("finalSale"))

    def _image(self, color: dict, base: str) -> str | None:
        images = [i for i in (color.get("imagesWithMetadata") or []) if isinstance(i, dict)]
        for image in images:
            resolved = self._absolute(image.get("src"), base)
            if resolved:
                return resolved
        swatch = color.get("swatch")
        if isinstance(swatch, dict):
            return self._absolute(swatch.get("src"), base)
        return None

    @staticmethod
    def _image_count(color: dict) -> int | None:
        images = color.get("imagesWithMetadata")
        return len(images) if isinstance(images, list) and images else None

    @staticmethod
    def _join(rows: list, key: str) -> str | None:
        values = [str(r.get(key)).strip() for r in rows if isinstance(r, dict) and r.get(key)]
        # Deterministic and duplicate-free, but order-preserving for the storefront's own
        # primary-colour-first ordering.
        seen = set()
        unique = []
        for value in values:
            if value not in seen:
                seen.add(value)
                unique.append(value)
        return ", ".join(unique) or None

    # ------------------------------------------------------------------ pagination

    @staticmethod
    def _next_page_url(current_url: str, next_offset: int) -> str | None:
        """Ordinary `?offset=N` pagination, preserving every other query parameter.

        The PLP URL also carries facet/sort state (`?f=...`, `?productSort=...`), so the
        offset is rewritten in place rather than replacing the query string.
        """
        parts = urlsplit(current_url)
        params = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != "offset"]
        params.append(("offset", str(next_offset)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(params), parts.fragment))

    @staticmethod
    def _absolute(url, base: str) -> str | None:
        if not isinstance(url, str) or not url.strip():
            return None
        url = url.strip()
        if url.startswith("http"):
            return url
        if url.startswith("//"):
            return f"https:{url}"
        if url.startswith("/prod/"):
            # Media paths are CDN-relative, not site-relative: `/prod/products/...` is
            # served from the image host, not from `www.shopbop.com`.
            return f"{IMAGE_CDN}{ShopbopListingSpider._sized(url)}"
        return urljoin(base or BASE_URL, url)

    @staticmethod
    def _sized(path: str) -> str:
        """Append the storefront's own image transform to a CDN media path."""
        if not path.lower().endswith(".jpg"):
            return path
        return f"{path[: -len('.jpg')]}{IMAGE_SUFFIX}"

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

