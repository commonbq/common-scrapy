from __future__ import annotations

import html
import json
import re
from urllib.parse import urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.newegg_categories import (
    NEWEGG_CATEGORIES,
    NEWEGG_LISTING_CATEGORIES,
    NEWEGG_SITE_BASE,
    url_kind,
)

# Newegg's ImagePathPattern ladder tops out at ProductImageOriginal (~6 MB per
# image). Rung 180 serves the 200px rendition (~25 KB) and is a sane default
# for a full-category crawl; override with -a image_size=1280 for originals.
DEFAULT_IMAGE_SIZE = 180


class NeweggListingSpider(BaseListingSpider):
    """Newegg listings from the server-rendered ``window.__initialState__`` blob.

    Every category page ships its first result window inline. The document
    contains exactly one ``window.__initialState__ = {...}`` assignment holding
    ``Products[]``, ``TotalItemCount`` and ``PageInfo`` -- no Next.js flight
    data, no product XHR, and no ``application/ld+json`` to reconcile against.
    This spider reads that hydration object directly.

    Pagination is a plain SSR re-render: page 1 uses the leaf URL and later pages
    append ``/Page-{n}``, which returns a new document with a fresh state object.
    """

    name = "newegg_listing"
    allowed_domains = ["newegg.com", "www.newegg.com", "localhost", "127.0.0.1"]
    # Full taxonomy so any captured node resolves by name; `SubCategory` nodes
    # are the ones that actually render products.
    categories = NEWEGG_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "item_id", "title", "brand",
            "model", "url", "image_url", "price", "original_price", "currency",
            "discount_pct", "rating", "reviews_count", "on_sale", "in_stock",
            "seller", "ships_from", "shipping_charge", "promotional_badge",
            "group_item_count", "category_name", "subcategory_name", "page",
            "position", "total_count", "source_url", "source", "raw",
        ],
    }

    # Newegg emits one assignment per document; match it narrowly and then
    # balance-brace decode from the first ``{`` instead of running a greedy
    # regex across arbitrary <script> bodies.
    _assignment = re.compile(r"window\.__initialState__\s*=\s*")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_size = int(kwargs.get("image_size") or DEFAULT_IMAGE_SIZE)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"{len(NEWEGG_LISTING_CATEGORIES)} product-listing categories are available, "
                f"e.g. {', '.join(e['category'] for e in NEWEGG_LISTING_CATEGORIES[:3])}"
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
                "category": selected.get("category") or self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "base_url": target,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Newegg listing returned HTTP {response.status}: {response.url}")

        state = self._extract_initial_state(response.text)
        if state is None:
            raise RuntimeError(
                f"No decodable window.__initialState__ object found at {response.url}. "
                "Newegg markup likely changed; the hydration blob is the only supported data source."
            )

        products = state.get("Products")
        if not isinstance(products, list):
            raise RuntimeError(
                f"Newegg __initialState__.Products is missing or not a list at {response.url} "
                f"(keys: {sorted(state)[:8]})"
            )

        page = int(response.meta.get("page", 1))
        total_count = self._integer(state.get("TotalItemCount"))

        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            cell = product.get("ItemCell")
            if not isinstance(cell, dict):
                self.logger.warning("Skipping Newegg product with no ItemCell at %s", response.url)
                continue
            item_id = str(cell.get("Item") or product.get("ProductNumber") or "").strip()
            if not item_id:
                self.logger.warning("Skipping Newegg product with no item id at %s", response.url)
                continue
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, cell, response, page, position, total_count)

        if not products:
            kind = url_kind(response.url)
            self.logger.info(
                "Newegg returned zero products at %s (%s node). Store and Category "
                "nodes are navigation hubs and render no items; point -a category at "
                "a SubCategory leaf to crawl products.",
                response.url,
                kind,
            )
            return
        if page >= self.max_pages:
            return

        total_pages = self._total_pages(total_count, len(products))
        if total_pages is not None and page >= total_pages:
            return

        yield scrapy.Request(
            self._with_page(response.meta.get("base_url") or response.url, page + 1),
            callback=self.parse,
            headers=response.request.headers,
            meta={**response.meta, "page": page + 1},
        )

    @staticmethod
    def _total_pages(total_count: int | None, page_size: int) -> int | None:
        if not total_count or not page_size:
            return None
        return max(1, -(-total_count // page_size))

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        """Append ``/Page-{n}`` for page 2+, stripping any page already present."""
        parts = urlsplit(url)
        path = parts.path.rstrip("/")
        path = re.sub(r"/Page-\d+$", "", path)
        if page > 1:
            path = f"{path}/Page-{page}"
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

    def _item(
        self,
        product: dict,
        cell: dict,
        response,
        page: int,
        position: int,
        total_count: int | None,
    ) -> dict:
        description = cell.get("Description") if isinstance(cell.get("Description"), dict) else {}
        review = cell.get("Review") if isinstance(cell.get("Review"), dict) else {}
        seller = cell.get("Seller") if isinstance(cell.get("Seller"), dict) else {}
        factory = cell.get("ItemManufactory") if isinstance(cell.get("ItemManufactory"), dict) else {}
        category = cell.get("Category") if isinstance(cell.get("Category"), dict) else {}
        subcategory = cell.get("Subcategory") if isinstance(cell.get("Subcategory"), dict) else {}
        promotion = cell.get("PromotionInfo") if isinstance(cell.get("PromotionInfo"), dict) else {}
        tags = cell.get("CustomTags") if isinstance(cell.get("CustomTags"), dict) else {}

        price = self._number(cell.get("FinalPrice"))
        original_price = self._number(cell.get("UnitCost"))
        if original_price is None:
            map_price = self._number(cell.get("MapPrice"))
            if map_price is not None and price is not None and map_price > price:
                original_price = map_price
        discount_pct = None
        if price and original_price and original_price > price:
            discount_pct = round((original_price - price) / original_price * 100, 2)
        on_sale = discount_pct is not None

        item_id = str(cell.get("Item") or product.get("ProductNumber") or "")
        badges = [str(value) for value in tags.values() if value]
        promo_text = promotion.get("PromotionText") or promotion.get("DisplayPromotionText")
        if promo_text:
            badges.append(str(promo_text))
        shipping_charge = self._number(cell.get("ShippingCharge"))

        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": item_id,
            "title": html.unescape(str(description.get("Title") or "")).strip() or None,
            "brand": factory.get("Manufactory") or None,
            "model": cell.get("Model") or None,
            "url": self._product_url(description, cell, item_id),
            "image_url": self._image_url(cell, self.image_size),
            "price": price,
            "original_price": original_price,
            "currency": "USD" if price is not None else None,
            "discount_pct": discount_pct,
            "rating": self._number(review.get("RatingOneDecimal")) or self._number(review.get("Rating")),
            "reviews_count": self._integer(review.get("HumanRating")),
            "on_sale": on_sale,
            "in_stock": self._boolean(cell.get("Instock")),
            "seller": seller.get("SellerName") or "Newegg",
            "ships_from": cell.get("ShipFromCountryName") or None,
            "shipping_charge": shipping_charge,
            "promotional_badge": " | ".join(badges) or None,
            "group_item_count": self._integer(product.get("GroupItemCount")),
            "category_name": category.get("RealCategoryName") or None,
            "subcategory_name": subcategory.get("SubcategoryDescription") or None,
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "newegg_initial_state_products",
            "raw": product,
        }

    @staticmethod
    def _product_url(description: dict, cell: dict, item_id: str) -> str | None:
        """Newegg PDP URLs are ``/{url-keywords}/p/{item-id}``.

        Both halves come from the hydration object, so no HTML anchor scraping
        is needed. ``UrlKeywords`` is only a slug -- the trailing item id is
        what actually identifies the SKU.
        """
        if not item_id:
            return None
        keywords = str(description.get("UrlKeywords") or "").strip().strip("/")
        if not keywords:
            return f"{NEWEGG_SITE_BASE}/p/{item_id}"
        return f"{NEWEGG_SITE_BASE}/{keywords}/p/{item_id}"

    @staticmethod
    def _image_url(cell: dict, size: int | None) -> str | None:
        """Resolve the thumbnail through the page's own ``ImagePathPattern`` list.

        Newegg publishes one pattern per rendition and orders them ascending.
        ``Size`` is a ladder index rather than the rendered pixel width -- the
        180 entry actually serves ``ProductImageCompressAll200`` -- so the
        largest entry at or below the requested rung is used. The top of the
        ladder is ``ProductImageOriginal`` at roughly 6 MB per image, which is
        far too heavy to mirror for a whole listing; the 180 rung lands around
        25 KB.
        """
        new_image = cell.get("NewImage") if isinstance(cell.get("NewImage"), dict) else {}
        image_name = new_image.get("ImageName") or cell.get("ItemCellImageName")
        image = cell.get("Image") if isinstance(cell.get("Image"), dict) else {}
        patterns = image.get("ImagePathPattern") if isinstance(image.get("ImagePathPattern"), list) else []
        if not image_name:
            return None

        usable = sorted(
            (
                (pattern["Size"], pattern["PathPattern"])
                for pattern in patterns
                if isinstance(pattern, dict)
                and isinstance(pattern.get("Size"), int)
                and pattern["Size"] > 0
                and isinstance(pattern.get("PathPattern"), str)
                and pattern["PathPattern"]
            ),
            key=lambda entry: entry[0],
        )
        if not usable:
            return None

        wanted = size or DEFAULT_IMAGE_SIZE
        at_or_below = [entry for entry in usable if entry[0] <= wanted]
        chosen = at_or_below[-1] if at_or_below else usable[0]
        return chosen[1].replace("{Size}", str(chosen[0])).replace("{ImageName}", image_name)

    @classmethod
    def _extract_initial_state(cls, document: str) -> dict | None:
        """Balance-decode the object assigned to ``window.__initialState__``."""
        for match in cls._assignment.finditer(document or ""):
            start = document.find("{", match.end())
            if start == -1:
                continue
            try:
                state, _ = json.JSONDecoder().raw_decode(document, start)
            except (TypeError, ValueError):
                continue
            if isinstance(state, dict):
                return state
        return None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _boolean(value):
        if isinstance(value, bool):
            return value
        return str(value).lower() == "true"
