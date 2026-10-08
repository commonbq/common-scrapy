from __future__ import annotations

import json
import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.iherb_categories import IHERB_CATEGORIES, url_name_for


CATALOG_API_HOST = "https://catalog.app.iherb.com"
STOREFRONT_HOST = "https://www.iherb.com"
CLOUDINARY_HOST = "https://cloudinary.images-iherb.com"
# The catalog service silently stops answering above 50 items per call.
API_PAGE_SIZE_LIMIT = 50
DEFAULT_PAGE_SIZE = 50
# `$` is what the catalog service returns for a US-geolocated request. The
# service resolves country/currency from the caller IP and never echoes a
# currency code, so the symbol is the only currency signal it exposes.
CURRENCY_BY_SYMBOL = {"$": "USD"}


class IherbListingSpider(BaseListingSpider):
    """iHerb category listings from the first-party catalog JSON API.

    The storefront PLP is server-rendered, but its product grid is *also*
    available as JSON from the same origin's catalog service: the PLP's own
    "load more"/pagination and facet XHRs post to
    ``https://catalog.app.iherb.com/category/{urlName}/products`` and
    ``.../filters``. This spider calls that endpoint directly, so no listing
    markup, JSON-LD block or browser engine is involved, and one response
    carries ~45 product attributes instead of the six `data-ga-*` attributes
    that the SSR cards expose.

    Verified live 2026-10-05: ``POST /category/magnesium/products`` with
    ``{"page": 1, "pageSize": 50}`` returns ``totalSize`` 857 and the first 50
    products; page 2 returns a disjoint id set; the default (Featured) sort
    order of ``/category/supplements/products`` reproduces the storefront
    PLP's ``window.IHR_DL.categoryList`` ids exactly (16567, 64009, 88819,
    67051, ...). ``pageSize`` > 50 makes the service hang, so it is capped.
    """

    name = "iherb_listing"
    allowed_domains = ["catalog.app.iherb.com", "app.iherb.com", "www.iherb.com"]
    categories = IHERB_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "category_url_name",
            "item_id", "part_number", "title", "product_name", "brand",
            "brand_code", "url", "image_url", "price", "list_price", "currency",
            "currency_symbol", "discount_percent", "promo_code", "promo_message",
            "rating", "reviews_count", "in_stock", "availability",
            "back_in_stock_date", "recent_activity", "is_new", "is_shipping_saver",
            "is_featured_brand", "is_iherb_pick", "is_express_delivery",
            "is_autoship", "product_form", "potency", "package_quantity",
            "price_per_serving", "product_status", "group_id", "page", "position",
            "total_count", "items_per_page", "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        page_size = self._page_size(kwargs.get("page_size"))
        sort = str(kwargs.get("sort") or "").strip() or None
        filter_category_ids = self._category_ids(kwargs.get("category_ids"))
        super().__init__(*args, **kwargs)
        # Scrapy.Spider copies every command-line kwarg onto the instance, so
        # assign normalized values after its constructor has run.
        self.page_size = page_size
        self.sort = sort
        self.filter_category_ids = filter_category_ids
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()
        self._previous_page_first_id: str | None = None

    @staticmethod
    def _page_size(value) -> int:
        try:
            requested = int(value) if value is not None else DEFAULT_PAGE_SIZE
        except (TypeError, ValueError):
            requested = DEFAULT_PAGE_SIZE
        return max(1, min(requested, API_PAGE_SIZE_LIMIT))

    @staticmethod
    def _category_ids(value) -> list[str]:
        if not value:
            return []
        raw = value if isinstance(value, (list, tuple)) else str(value).split(",")
        return [str(entry).strip() for entry in raw if str(entry).strip()]

    def start_requests(self):
        self._seen_products.clear()
        self._previous_page_first_id = None
        target = self.resolve_target_url()
        selected = next(
            (entry for entry in self.categories if entry["url"] == target), {}
        )
        url_name = selected.get("url_name") or url_name_for(target)
        if not url_name:
            raise ValueError(
                f"Cannot resolve an iHerb category urlName from {target!r}. "
                "Expected a path like https://www.iherb.com/c/<urlName>."
            )
        yield self._products_request(
            url_name,
            page=1,
            meta={
                "category": selected.get("category") or self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "category_url_name": url_name,
                "listing_url": selected.get("url") or target,
            },
        )

    def _products_request(self, url_name: str, *, page: int, meta: dict):
        payload: dict = {"page": page, "pageSize": self.page_size}
        if self.sort:
            payload["sort"] = self.sort
        if self.filter_category_ids:
            payload["categoryIds"] = self.filter_category_ids
        request_meta = {
            key: meta.get(key)
            for key in (
                "category", "department", "subcategory", "category_url_name",
                "listing_url",
            )
        }
        request_meta["page"] = page
        return scrapy.Request(
            f"{CATALOG_API_HOST}/category/{url_name}/products",
            method="POST",
            body=json.dumps(payload),
            headers=self._api_headers(),
            callback=self.parse,
            errback=self._request_failed,
            # Do not carry Scrapy's downloader-private proxy/auth keys from the
            # previous response. A fresh request lets the project middleware
            # rebuild Proxy-Authorization; reusing them causes a 407 on page 2.
            meta=request_meta,
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response):
        payload = self._payload(response)
        products = payload.get("products")
        if not isinstance(products, list):
            raise RuntimeError(
                "iHerb catalog API returned no products array "
                f"(blocked or contract change): {response.url}"
            )
        page = int(response.meta.get("page", 1))
        if page == 1 and not products:
            raise RuntimeError(
                "iHerb catalog API returned an empty first page "
                f"(blocked response or unknown category): {response.url}"
            )

        total_count = self._integer(payload.get("totalSize"))
        first_id = None
        emitted = 0
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("productId") or "").strip()
            if not item_id:
                continue
            if first_id is None:
                first_id = item_id
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            emitted += 1
            yield self._item(product, response, page, position, total_count)

        if page >= self.max_pages:
            return
        # Stop on an exhausted result set, a repeat of the previous page's first
        # id (the service ignores `page` for some slugs), or a page that
        # contributed nothing new.
        if not emitted or (first_id is not None and first_id == self._previous_page_first_id):
            return
        if total_count is not None and page * self.page_size >= total_count:
            return
        self._previous_page_first_id = first_id
        yield self._products_request(
            response.meta["category_url_name"], page=page + 1, meta=response.meta
        )

    def _payload(self, response: scrapy.http.Response) -> dict:
        if response.status != 200:
            raise RuntimeError(
                f"iHerb catalog API returned HTTP {response.status}: {response.url}"
            )
        body = response.text or ""
        if not body.strip():
            raise RuntimeError(
                f"iHerb catalog API returned an empty body (blocked): {response.url}"
            )
        try:
            payload = json.loads(body)
        except (TypeError, ValueError) as error:
            snippet = body[:160].replace("\n", " ")
            raise RuntimeError(
                f"iHerb catalog API returned non-JSON (bot challenge or error page): "
                f"{response.url} -- {snippet}"
            ) from error
        if not isinstance(payload, dict):
            raise RuntimeError(
                f"iHerb catalog API returned a non-object payload: {response.url}"
            )
        return payload

    def _request_failed(self, failure):
        message = (
            failure.getErrorMessage()
            if hasattr(failure, "getErrorMessage")
            else str(failure)
        )
        raise RuntimeError(f"iHerb catalog API request failed: {message}")

    def _item(self, product: dict, response, page: int, position: int, total_count):
        price = None if product.get("hidePrice") else self._number(product.get("discountPriceValue"))
        if price is None and not product.get("hidePrice"):
            price = self._number(product.get("discountPrice"))
        list_price = None if product.get("hidePrice") else self._number(product.get("listPrice"))
        symbol = product.get("currencySymbol")
        availability = self._availability(product)
        brand_code = product.get("brandCode")
        part_number = product.get("partNumber")
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "category_url_name": response.meta.get("category_url_name"),
            "item_id": str(product.get("productId")),
            "part_number": part_number,
            "title": product.get("displayName"),
            "product_name": product.get("name") or product.get("productName"),
            "brand": product.get("brandName") or product.get("brandLabel"),
            "brand_code": brand_code,
            "url": self._product_url(product.get("url")),
            "image_url": self._image_url(brand_code, part_number, product.get("primaryImageIndex")),
            "price": price,
            "list_price": list_price,
            "currency": CURRENCY_BY_SYMBOL.get(symbol) if symbol else None,
            "currency_symbol": symbol,
            # Only a real price markdown counts as a discount; `discountPercentage`
            # is a promo-code percentage that leaves both prices untouched.
            "discount_percent": self._discount_percent(price, list_price),
            "promo_code": product.get("promoCode"),
            "promo_message": product.get("discountMessage") or product.get("promoCodeMessage"),
            "rating": self._number(product.get("rating")),
            "reviews_count": self._integer(product.get("ratingCount")),
            "in_stock": availability == "in_stock",
            "availability": availability,
            "back_in_stock_date": product.get("backInStockDate"),
            "recent_activity": product.get("recentActivityMessage"),
            "is_new": self._boolean(product.get("isNew")),
            "is_shipping_saver": self._boolean(product.get("isShippingSaver")),
            "is_featured_brand": self._boolean(product.get("isFeaturedBrand")),
            "is_iherb_pick": self._boolean(product.get("isIherbPick")),
            "is_express_delivery": self._boolean(product.get("isExpressDelivery")),
            "is_autoship": self._boolean(product.get("isAutoship")),
            "product_form": product.get("productForm"),
            "potency": product.get("potency"),
            "package_quantity": product.get("packageQuantity"),
            "price_per_serving": product.get("pricePerServing"),
            "product_status": self._integer(product.get("productStatus")),
            "group_id": self._integer(product.get("groupId")),
            "page": page,
            "position": position,
            "total_count": total_count,
            "items_per_page": self.page_size,
            "source_url": response.url,
            "source": "iherb_catalog_api",
            "raw": product,
        }

    @staticmethod
    def _availability(product: dict) -> str:
        if product.get("isOutOfStock"):
            return "out_of_stock"
        if product.get("isDiscontinued"):
            return "discontinued"
        if product.get("isNotAvailable"):
            return "not_available"
        if product.get("prohibited"):
            return "prohibited"
        if product.get("isComingSoon"):
            return "coming_soon"
        if product.get("isSeasonallyUnavailable"):
            return "seasonally_unavailable"
        return "in_stock"

    @staticmethod
    def _discount_percent(price, list_price):
        """Percentage off, derived from prices only when a real markdown exists."""
        if price is None or list_price is None or list_price <= price:
            return None
        return round((list_price - price) / list_price * 100, 2)

    @staticmethod
    def _product_url(url):
        """Rewrite the geo-localized storefront host (``ua.iherb.com``) to the US host.

        The catalog service builds product links from the caller's IP country,
        so the same request can return ``vn.iherb.com``/``ua.iherb.com`` hosts.
        """
        if not url:
            return None
        match = re.match(r"^https?://([^/]*\.)?iherb\.com(/.*)$", url.strip())
        return f"{STOREFRONT_HOST}{match.group(2)}" if match else url

    @staticmethod
    def _image_url(brand_code, part_number, primary_image_index):
        """Rebuild the CDN image URL from the product's identifiers.

        The catalog payload carries ``primaryImageIndex`` but no image URL.
        Cloudinary paths are ``images/<brand>/<brand><part-number>/u/<index>.jpg``
        with the part number's dash removed, which is what the storefront cards
        use too.
        """
        if not brand_code or not part_number or primary_image_index is None:
            return None
        brand = str(brand_code).strip().lower()
        folder = re.sub(r"[^a-z0-9]", "", str(part_number).strip().lower())
        if not brand or not folder:
            return None
        return (
            f"{CLOUDINARY_HOST}/image/upload/f_auto,q_auto:eco/images/"
            f"{brand}/{folder}/u/{primary_image_index}.jpg"
        )

    @staticmethod
    def _number(value):
        if isinstance(value, str):
            value = value.replace(",", "").strip()
            match = re.search(r"-?\d+(?:\.\d+)?", value)
            value = match.group(0) if match else None
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
        return value if isinstance(value, bool) else None

    @staticmethod
    def _api_headers():
        return {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://www.iherb.com",
            "referer": "https://www.iherb.com/",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
        }
