from __future__ import annotations

import json
import re
from urllib.parse import urlencode, urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.uniqlo_categories import UNIQLO_CATEGORIES, UNIQLO_CATEGORY_PATHS

PRODUCTS_API = "https://www.uniqlo.com/us/api/commerce/v5/en/products"
PRODUCT_URL = "https://www.uniqlo.com/us/en/products/{product_id}"


class UniqloListingSpider(BaseListingSpider):
    """UNIQLO US category listings from the first-party commerce BFF products API.

    The SSR shell of every UNIQLO page ships ``window.__PRELOADED_STATE__`` with the
    full navigation taxonomy but an *empty* product grid
    (``search.search.productIds == []``); the React app hydrates it client-side over
    XHR against ``/us/api/commerce/v5/en/products``. This spider uses that single
    authoritative source -- no HTML card scraping, no JSON-LD.

    Note on identifiers: the BFF ``productId`` is *not* unique per row -- the same
    ``E424873-000`` is returned once per colourway with a different
    ``representativeColorDisplayCode``. UNIQLO's own hydration state identifies rows
    as ``<productId>-<colorCode>`` (``"E424873-000-00"``), so the spider joins the
    two to get a stable ``item_id``.
    """

    name = "uniqlo_listing"
    allowed_domains = [
        "uniqlo.com",
        "www.uniqlo.com",
        "image.uniqlo.com",
        "localhost",
        "127.0.0.1",
    ]
    categories = UNIQLO_CATEGORIES
    require_category_arg = False

    page_size = 36

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_name", "department", "subcategory", "item_id",
            "style_id", "title", "brand", "gender", "color", "color_code", "url",
            "image_url", "price", "original_price", "currency", "on_sale",
            "promotion_text", "rating", "reviews_count", "available_sizes",
            "page", "position", "total_count", "items_per_page", "taxonomy_path",
            "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                "Categories are the 2741 UNIQLO US taxonomy URLs; see the README table."
            )
        self._seen_products: set[str] = set()

    def _category_hint(self) -> str:
        """A short, sample-backed category hint.

        The UNIQLO taxonomy has 2741 leaves; dumping every slug into a
        ``ValueError`` would bury the actual mistake.
        """
        names = super().available_categories()
        return (
            f"Known categories: {len(names)} total, e.g. "
            f"{', '.join(names[:12])}, ... "
            f"(first: {self.categories[0]['url']})."
        )

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        entry = self._lookup(target)
        meta = {
            "category": self.category or entry.get("category") or "custom",
            "category_name": entry.get("category_name"),
            "department": entry.get("department"),
            "subcategory": entry.get("subcategory"),
            "taxonomy_path": entry.get("path"),
            "offset": 0,
            "page": 1,
        }
        yield scrapy.Request(
            self._products_url(entry["path"], 0),
            callback=self.parse,
            headers=self._api_headers(),
            meta=meta,
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"UNIQLO products API returned HTTP {response.status}: {response.url}")

        payload = self._json_object(response)
        result = payload.get("result")
        if not isinstance(result, dict):
            raise RuntimeError(f"UNIQLO products API returned no result object at {response.url}")

        products = result.get("items")
        if not isinstance(products, list):
            raise RuntimeError(f"UNIQLO products API result has no list-valued items at {response.url}")

        pagination = result.get("pagination") if isinstance(result.get("pagination"), dict) else {}
        page = int(response.meta.get("page", 1))
        total_count = self._integer(pagination.get("total"))
        items_per_page = self._integer(pagination.get("count")) or len(products)
        offset = self._integer(pagination.get("offset"))
        if offset is None:
            offset = int(response.meta.get("offset", 0))

        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = self._item_id(product)
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, response, page, position, total_count, items_per_page)

        if page >= self.max_pages or not products:
            return
        next_offset = offset + len(products)
        if total_count is not None and next_offset >= total_count:
            return

        yield scrapy.Request(
            self._products_url(response.meta.get("taxonomy_path"), next_offset),
            callback=self.parse,
            headers=self._api_headers(),
            meta={**response.meta, "offset": next_offset, "page": page + 1},
        )

    # -- extraction -----------------------------------------------------------

    def _item(
        self,
        product: dict,
        response: scrapy.http.Response,
        page: int,
        position: int,
        total_count: int | None,
        items_per_page: int,
    ) -> dict:
        product_id = str(product.get("productId") or "").strip()
        color_code = str(product.get("representativeColorDisplayCode") or "") or None
        prices = product.get("prices") if isinstance(product.get("prices"), dict) else {}
        base = prices.get("base") if isinstance(prices.get("base"), dict) else {}
        promo = prices.get("promo") if isinstance(prices.get("promo"), dict) else {}

        # The BFF nests the *regular* price under ``base`` and the *discounted*
        # price under ``promo``; ``isDualPrice`` marks a row that genuinely shows
        # both. So ``promo`` is the price you actually pay and ``base`` is the
        # struck-through "original". Mapping them the other way round would report
        # every sale at full price.
        base_value = self._money(base.get("value"))
        promo_value = self._money(promo.get("value"))
        on_sale = bool(
            promo_value is not None
            and (prices.get("isDualPrice") or base_value != promo_value)
        )
        price = promo_value if on_sale and promo_value is not None else base_value
        original_price = base_value if on_sale else None
        currency = self._currency(promo) or self._currency(base)
        rating = product.get("rating") if isinstance(product.get("rating"), dict) else {}

        return {
            "category": response.meta.get("category"),
            "category_name": response.meta.get("category_name"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "item_id": self._item_id(product),
            "style_id": self._style_id(product_id),
            "title": str(product.get("name") or "").strip() or None,
            "brand": "UNIQLO",
            "gender": str(product.get("genderName") or "").strip() or None,
            "color": self._color_name(product, color_code),
            "color_code": color_code,
            "url": PRODUCT_URL.format(product_id=product_id) if product_id else None,
            "image_url": self._image_url(product, color_code),
            "price": price,
            "original_price": original_price,
            "currency": currency,
            "on_sale": on_sale,
            "promotion_text": str(product.get("promotionText") or "").strip() or None,
            "rating": self._number(rating.get("average")),
            "reviews_count": self._integer(rating.get("count")),
            "available_sizes": self._size_names(product),
            "page": page,
            "position": position,
            "total_count": total_count,
            "items_per_page": items_per_page,
            "taxonomy_path": response.meta.get("taxonomy_path"),
            "source_url": response.url,
            "source": "uniqlo_commerce_bff_products",
            "raw": product,
        }

    def _lookup(self, url: str) -> dict:
        """Resolve a listing URL to its taxonomy entry (and id path)."""
        normalized = url.split("#", 1)[0].rstrip("/")
        for entry in self.categories:
            if entry.get("url", "").rstrip("/") == normalized:
                return entry
        path = UNIQLO_CATEGORY_PATHS.get(normalized)
        if path:
            return {"url": url, "path": path, "category": self.category or "custom"}
        raise ValueError(
            f"'{url}' is not a known UNIQLO US category URL, so its taxonomy id path "
            f"cannot be resolved. {self._category_hint()}"
        )

    @staticmethod
    def _products_url(taxonomy_path: str | None, offset: int) -> str:
        query = urlencode({"path": taxonomy_path, "limit": UniqloListingSpider.page_size, "offset": offset})
        return f"{PRODUCTS_API}?{query}"

    @staticmethod
    def _api_headers() -> dict:
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "referer": "https://www.uniqlo.com/us/en/",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _json_object(response: scrapy.http.Response) -> dict:
        try:
            payload = json.loads(response.text)
        except ValueError as exc:
            raise RuntimeError(f"UNIQLO products API returned non-JSON at {response.url}: {exc}") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"UNIQLO products API returned a non-object payload at {response.url}")
        return payload

    @staticmethod
    def _item_id(product: dict) -> str:
        """`<productId>-<colorCode>`, UNIQLO's own per-colourway row id.

        ``productId`` alone repeats across colourways, so joining the representative
        colour code is what makes the id unique (and matches the ids UNIQLO's
        hydration state uses in ``search.*.search.productIds``).
        """
        product_id = str(product.get("productId") or "").strip()
        if not product_id:
            return ""
        color_code = str(product.get("representativeColorDisplayCode") or "").strip()
        return f"{product_id}-{color_code}" if color_code else product_id

    @staticmethod
    def _style_id(product_id: str) -> str | None:
        # "E424873-000" -> "424873" (the style number used by the image CDN paths).
        match = re.match(r"^[A-Z]?(\d+)-\d+$", product_id or "")
        return match.group(1) if match else None

    @staticmethod
    def _color_name(product: dict, color_code: str | None) -> str | None:
        colors = product.get("colors") if isinstance(product.get("colors"), list) else []
        for color in colors:
            if not isinstance(color, dict):
                continue
            if color_code and str(color.get("displayCode") or "") != str(color_code):
                continue
            name = str(color.get("name") or "").strip()
            if name:
                return name.title()
        representative = product.get("representative")
        if isinstance(representative, dict) and isinstance(representative.get("color"), dict):
            name = str(representative["color"].get("name") or "").strip()
            return name.title() if name else None
        return None

    @staticmethod
    def _image_url(product: dict, color_code: str | None) -> str | None:
        images = product.get("images") if isinstance(product.get("images"), dict) else {}
        main = images.get("main") if isinstance(images.get("main"), dict) else {}
        for key in (color_code, "00"):
            if not key:
                continue
            entry = main.get(str(key))
            if isinstance(entry, dict) and entry.get("image"):
                return urljoin("https://image.uniqlo.com/", str(entry["image"]))
        for entry in main.values():
            if isinstance(entry, dict) and entry.get("image"):
                return urljoin("https://image.uniqlo.com/", str(entry["image"]))
        return None

    @staticmethod
    def _size_names(product: dict) -> list[str]:
        sizes = product.get("sizes") if isinstance(product.get("sizes"), list) else []
        names: list[str] = []
        for size in sizes:
            if isinstance(size, dict) and size.get("name"):
                names.append(str(size["name"]))
            elif isinstance(size, str):
                names.append(size)
        return names

    @staticmethod
    def _currency(prices: dict) -> str | None:
        currency = prices.get("currency")
        if isinstance(currency, dict) and currency.get("code"):
            return str(currency["code"])
        if isinstance(currency, str) and currency:
            return currency
        return None

    @staticmethod
    def _money(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
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
