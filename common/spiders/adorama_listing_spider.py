from __future__ import annotations

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.adorama_categories import ADORAMA_BASE_URL, ADORAMA_CATEGORIES
from common.spiders.base_listing_spider import BaseListingSpider


class AdoramaListingSpider(BaseListingSpider):
    """Adorama category listings from the server-rendered Next.js state.

    Adorama listing pages are Next.js SSR routes (``/l/[[...param]]``). The
    authoritative product payload ships in the HTML as
    ``script#__NEXT_DATA__`` -> ``props.pageProps.products[]`` (24 per page), so
    no browser execution and no listing XHR is required. Adorama also exposes
    ``/api/products-v2`` and ``/api/productOptions/`` endpoints, but those are
    PDP variant APIs (and are DataDome-sensitive), so they are not used here.

    Pagination is query-based: page 1 is the bare URL and later pages append
    ``?startAt={n}``, taken from ``pageProps.nextPageUrl``.
    """

    name = "adorama_listing"
    allowed_domains = ["adorama.com", "www.adorama.com", "localhost", "127.0.0.1"]
    categories = ADORAMA_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "category_path", "item_id",
            "variant_sku", "title", "brand", "manufacturer", "model", "url",
            "image_url", "price", "list_price", "savings_amount",
            "savings_percent", "currency", "badge", "stock", "stock_label",
            "in_stock", "is_available_for_purchase", "is_used", "is_refurbished",
            "is_preorder",
            "rating", "reviews_count", "highlights", "free_shipping",
            "category_id", "category_path_hierarchy", "page", "position", "total_count",
            "items_per_page", "page_type", "source_url", "source", "raw",
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
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self._html_headers(),
            meta={
                "category": self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "category_path": selected.get("path"),
                "page": 1,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Adorama listing returned HTTP {response.status}: {response.url}")

        state = self._extract_next_data(response)
        if not isinstance(state, dict):
            raise RuntimeError(f"No valid Adorama __NEXT_DATA__ hydration found at {response.url}")

        page_props = self._page_props(state)
        if not isinstance(page_props, dict):
            raise RuntimeError(f"Adorama hydration has no props.pageProps object at {response.url}")

        page_type = (page_props.get("pageInfo") or {}).get("pageType")
        products = page_props.get("products")
        if not isinstance(products, list):
            raise RuntimeError(f"Adorama pageProps has no list-valued products at {response.url}")
        if page_type == "bcmsSitePage":
            raise RuntimeError(
                f"Adorama returned a CMS landing page (pageType=bcmsSitePage) with no product "
                f"grid at {response.url}. Use a depth-2+ category URL such as "
                f"{ADORAMA_BASE_URL}/l/Photography/Cameras"
            )
        if not products:
            raise RuntimeError(f"Adorama listing returned zero products at {response.url}")

        page = int(response.meta.get("page", 1))
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            sku = str(product.get("sku") or "")
            if not sku or sku in self._seen_products:
                continue
            self._seen_products.add(sku)
            yield self._item(product, page_props, response, page, position)

        if page >= self.max_pages:
            return
        next_url = page_props.get("nextPageUrl")
        if next_url:
            yield response.follow(
                next_url,
                callback=self.parse,
                headers=self._html_headers(),
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _extract_next_data(response: scrapy.http.Response) -> dict | None:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            return None
        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _page_props(state: dict) -> dict | None:
        props = state.get("props")
        page_props = props.get("pageProps") if isinstance(props, dict) else None
        return page_props if isinstance(page_props, dict) else None

    def _item(self, product, page_props, response, page, position):
        prices = self._mapping(product.get("prices"))
        flags = self._mapping(product.get("flags"))
        sub_status = self._mapping(product.get("subStatus"))
        ratings = self._mapping(product.get("ratings"))
        stock = product.get("stock")
        main_image = product.get("mainImageName")
        product_url = product.get("productUrl")

        persuasion = product.get("persuasionStrategies")
        persuasion_message = None
        if isinstance(persuasion, list) and persuasion and isinstance(persuasion[0], dict):
            persuasion_message = persuasion[0].get("message")

        badge = (product.get("badgeText") or "").strip() or persuasion_message
        stock_label = (sub_status.get("name") or "").strip() or None
        highlights = product.get("highlights")

        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "category_path": response.meta.get("category_path"),
            "item_id": str(product.get("sku")),
            "variant_sku": product.get("variantSku"),
            "title": product.get("productTitle") or product.get("shortTitle"),
            "brand": product.get("brand"),
            "manufacturer": product.get("mfr"),
            "model": product.get("mfr"),
            "url": urljoin(f"{ADORAMA_BASE_URL}/", product_url) if product_url else None,
            "image_url": f"{ADORAMA_BASE_URL}/images/product/{main_image}" if main_image else None,
            "price": self._number(prices.get("price")),
            "list_price": self._number(prices.get("highPrice")),
            "savings_amount": self._number(self._mapping(prices.get("youSave")).get("dollar")),
            "savings_percent": self._number(self._mapping(prices.get("youSave")).get("percent")),
            "currency": "USD",
            "badge": badge,
            "stock": stock,
            "stock_label": stock_label,
            "in_stock": self._in_stock(stock, stock_label),
            "is_available_for_purchase": flags.get("isAvailableForPurchase"),
            "is_used": bool(flags.get("isUsed")) if "isUsed" in flags else None,
            "is_refurbished": bool(flags.get("isRefurbished")) if "isRefurbished" in flags else None,
            "is_preorder": bool(flags.get("isPreOrder")) if "isPreOrder" in flags else None,
            "rating": self._number(ratings.get("averageRatingStars")),
            "reviews_count": self._integer(ratings.get("count")),
            "highlights": highlights if isinstance(highlights, list) else None,
            "free_shipping": (product.get("freeShipTypeName") or "").strip() or None,
            "category_id": self._stringify(product.get("categoryId")),
            "category_path_hierarchy": product.get("categoryPath"),
            "page": page,
            "position": position,
            "total_count": self._total_count(page_props),
            "items_per_page": self._integer(page_props.get("defaultPerPage")),
            "page_type": (page_props.get("pageInfo") or {}).get("pageType"),
            "source_url": response.url,
            "source": "adorama_next_data",
            "raw": product,
        }

    @staticmethod
    def _in_stock(stock, stock_label):
        """Physical stock state for the SKU.

        ``flags.isAvailableForPurchase`` is deliberately not used here: Adorama
        sets it True for pre-order and "New Item" SKUs whose ``stock`` is
        ``"Out"``. It is exported separately as ``is_available_for_purchase``.
        """
        text = f"{stock or ''} {stock_label or ''}".strip().lower()
        if not text:
            return None
        if "out" in text or "unavailable" in text or "backorder" in text:
            return False
        return "in" in text

    @staticmethod
    def _total_count(page_props):
        stats = page_props.get("itemsStats")
        if not isinstance(stats, dict):
            return None
        total = 0
        seen = False
        for value in stats.values():
            count = AdoramaListingSpider._integer(
                value.get("count") if isinstance(value, dict) else None
            )
            if count is not None:
                total += count
                seen = True
        return total if seen else None

    @staticmethod
    def _mapping(value):
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _stringify(value):
        return str(value) if value is not None else None

    @staticmethod
    def _number(value):
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, str):
            match = re.search(r"-?\d[\d,]*(?:\.\d+)?", value)
            value = match.group(0).replace(",", "") if match else None
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _html_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
