from __future__ import annotations

import html
import json
import re
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.levi_categories import LEVI_CATEGORIES, LEVI_SITE_BASE


class LevisListingSpider(BaseListingSpider):
    """Levi's listings from the LSCO React SSR hydration blob.

    Every PLP ships a Redux state object installed via
    ``Object.defineProperty(window, "__LSCO_INITIAL_STATE__", {... value: {...}})``.
    The product window already lives in that state at
    ``ssrViewStoreProductList`` -- there is no ``__NEXT_DATA__`` and no product
    XHR to replay, so this spider reads state that is hydrated into the HTML.

    Pagination is a pure SSR re-render: ``?page=<N>`` (0-indexed) returns a new
    document with a fresh state object and the next product window.
    """

    name = "levis_listing"
    allowed_domains = ["levi.com", "www.levi.com", "localhost", "127.0.0.1"]
    categories = LEVI_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "item_id", "title", "brand",
            "url", "image_url", "swatch_url", "price", "original_price",
            "currency", "discount_pct", "rating", "reviews_count", "on_sale",
            "merchant_badge", "promotional_badge", "color_count", "coming_soon",
            "sold_out", "category_code", "page", "position", "total_count",
            "source_url", "source", "raw",
            "timestamp",
        ],
    }

    # The state is wrapped in Object.defineProperty(...). Keep the window short so
    # we cannot latch onto an unrelated ``value:`` elsewhere in the document.
    _state_re = re.compile(r"__LSCO_INITIAL_STATE__[\s\S]{0,400}?value\s*:\s*")

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
                "category": selected.get("category") or self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "base_url": target,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Levi's listing returned HTTP {response.status}: {response.url}")
        state = self._extract_initial_state(response.text)
        if state is None:
            raise RuntimeError(f"No valid Levi's __LSCO_INITIAL_STATE__ object found at {response.url}")
        plp = state.get("ssrViewStoreProductList")
        if not isinstance(plp, dict):
            raise RuntimeError(f"Levi's initial state has no ssrViewStoreProductList at {response.url}")
        products = plp.get("products")
        if not isinstance(products, list):
            raise RuntimeError(f"Levi's ssrViewStoreProductList has no list-valued products at {response.url}")

        pagination = plp.get("pagination") if isinstance(plp.get("pagination"), dict) else {}
        current_page = self._integer(pagination.get("currentPage"))
        total_pages = self._integer(pagination.get("totalPages"))
        total_count = self._integer(pagination.get("totalResults"))
        page = (current_page + 1) if current_page is not None else int(response.meta.get("page", 1))
        category_code = plp.get("categoryCode")

        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("code") or "") or None
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, response, page, position, total_count, category_code)

        if not products:
            return
        if current_page is None or total_pages is None:
            return
        if current_page >= total_pages - 1 or page >= self.max_pages:
            return
        base_url = response.meta.get("base_url") or response.url
        yield scrapy.Request(
            self._with_page(base_url, current_page + 1),
            callback=self.parse,
            headers=response.request.headers,
            meta={**response.meta, "page": page + 1},
        )

    @staticmethod
    def _with_page(url: str, page_index: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "page"]
        query.append(("page", str(page_index)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _item(self, product: dict, response, page: int, position: int, total_count, category_code) -> dict:
        price = self._number((product.get("price") or {}).get("value"))
        if price is None:
            price = self._number((product.get("price") or {}).get("softPrice"))
        regular = self._number((product.get("price") or {}).get("regularPrice"))
        discount_pct = self._number(product.get("discountPCT"))
        on_sale = (regular is not None and price is not None and regular > price) or discount_pct is not None
        original_price = regular if (on_sale and regular is not None) else None

        variants = product.get("variantOptions") if isinstance(product.get("variantOptions"), list) else []
        image_url = self._image_url(product, variants)
        product_url = product.get("url")
        if product_url and product_url.startswith("/"):
            product_url = LEVI_SITE_BASE + product_url
        else:
            product_url = urljoin(response.url, product_url) if product_url else None

        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": str(product.get("code")),
            "title": html.unescape(str(product.get("name") or "")) or None,
            "brand": "Levi's",
            "url": product_url,
            "image_url": image_url,
            "swatch_url": product.get("swatchUrl"),
            "price": price,
            "original_price": original_price,
            "currency": "USD" if price is not None or original_price is not None else None,
            "discount_pct": discount_pct,
            "rating": self._number(product.get("averageOverallRatings")),
            "reviews_count": self._integer(product.get("noOfRatings")),
            "on_sale": on_sale,
            "merchant_badge": product.get("merchantBadge"),
            "promotional_badge": product.get("promotionalBadge"),
            "color_count": len(variants) or None,
            "coming_soon": self._boolean(product.get("comingSoon")),
            "sold_out": self._boolean(product.get("soldOutForever")),
            "category_code": category_code,
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "levis_lsco_initial_state_products",
            "raw": product,
        }

    @classmethod
    def _image_url(cls, product: dict, variants: list) -> str | None:
        for holder in (product, *(variants[:1] if variants else [])):
            if not isinstance(holder, dict):
                continue
            images = ((holder.get("galleryList") or {}).get("galleryImage")) or []
            for image in images:
                if isinstance(image, dict) and image.get("url"):
                    return image["url"]
        return product.get("swatchUrl")

    @classmethod
    def _extract_initial_state(cls, document: str) -> dict | None:
        for match in cls._state_re.finditer(document or ""):
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
