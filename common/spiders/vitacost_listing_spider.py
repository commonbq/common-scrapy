from __future__ import annotations

import html
import json
import re
from urllib.parse import urlencode, urljoin, urlparse

import scrapy

from common.settings import PROXY
from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.vitacost_categories import (
    BASE_URL,
    FILTER_API_URL,
    SHOP_DOMAIN,
    VITACOST_CATEGORIES,
)

# Boost caps `limit` server-side (a 100 request came back with 20 products), so the spider
# clamps to the largest page size the API actually honours.
DEFAULT_PAGE_SIZE = 48
MAX_PAGE_SIZE = 50

_BOOST_HEADER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
_STOREFRONT_HEADER = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
)

# The Boost app boots each collection page with the numeric Shopify collection id, which is the
# only value the API accepts as `collection_scope`:
#   function readPayload(){return {generalSettings:{page: "collection",
#     collection_id: 458194583867, collection_handle: "vitamins", ...}}}
# So the storefront page is fetched once per run purely to resolve that id -- every product
# field below is read from the JSON API, and no product HTML is parsed.
_COLLECTION_ID = re.compile(r'collection_id["\']?\s*:\s*"?(\d{6,})')

_BOOST_HOST = urlparse(FILTER_API_URL).hostname or "services.mybcapps.com"


class VitacostProxyMiddleware:
    """Proxy the Shopify storefront only, leaving the Boost filter API on a direct connection.

    `common.middlewares.CommonDownloaderMiddleware` proxies every request, but the configured
    ScrapeOps tunnel refuses to CONNECT to `services.mybcapps.com` (`TunnelError`), and the
    Boost endpoint answers directly. This middleware replaces the project one for this spider:
    storefront requests keep using `settings.PROXY`, Boost requests set no proxy at all.
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if request.meta.get("proxy"):
            return None
        if (urlparse(request.url).hostname or "") == _BOOST_HOST:
            return None
        proxy = spider.settings.get("PROXY") if "PROXY" in spider.settings else PROXY
        if proxy:
            request.meta["proxy"] = proxy
        return None


class VitacostListingSpider(BaseListingSpider):
    """vitacost.com listings from the Boost AI Search `bc-sf-filter` JSON API.

    Vitacost runs a Shopify (Dawn) storefront with the Boost AI Search & Discovery app. The
    product grid is rendered server side, but every field the spider exports is read from the
    first-party filter API the app itself calls:

        GET https://services.mybcapps.com/bc-sf-filter/filter
            ?_=pf&shop=icost.myshopify.com&collection_scope=<id>&page=<n>&limit=<n>
            &pg=collection_page&event_type=init&build_filter_tree=true&sort=best-selling

    The API returns whole normalized product records (`price_min`, `compare_at_price_min`,
    `percent_sale_min`, `images_info`, `variants`, `collections`, `metafields`), which is far
    more than the rendered cards expose, so this spider never parses product HTML.
    """

    name = "vitacost_listing"
    allowed_domains = ["vitacost.com", "www.vitacost.com", "services.mybcapps.com", "localhost", "127.0.0.1"]
    categories = VITACOST_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOADER_MIDLIERES": {
            "common.middlewares.CommonDownloaderMiddleware": None,
            "common.spiders.vitacost_listing_spider.VitacostProxyMiddleware": 543,
        },
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "handle", "collection_id", "item_id",
            "title", "url", "brand", "product_type", "product_category", "tags", "price",
            "original_price", "discount_percentage", "currency", "on_sale", "out_of_stock",
            "in_stock_quantity", "image_url", "image_alt", "image_count", "sku", "barcode",
            "option_count", "options", "package_quantity", "form", "strength", "badges",
            "description", "rating", "reviews_count", "published_at", "page", "position",
            "total_count", "scraped_timestamp", "source_url", "source", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self.page_size = self._clamp_page_size(
            kwargs["limit"] if kwargs.get("limit") is not None else kwargs.get("page_size")
        )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.categories if entry["url"] == target), {})
        handle = self._handle(target)
        if not handle:
            raise ValueError(
                f"Cannot derive a Shopify collection handle from {target!r}; expected a "
                "/collections/<handle> URL."
            )
        yield scrapy.Request(
            target,
            callback=self.parse_collection_page,
            errback=self.on_error,
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": _STOREFRONT_HEADER,
            },
            meta={
                "category": self.category or selected.get("category") or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "handle": handle,
                "collection_url": target,
                "page": 0,
            },
        )

    # ------------------------------------------------------------------ collection id

    def parse_collection_page(self, response):
        """Resolve the numeric collection id, then hand off to the Boost filter API."""
        collection_id = self._collection_id(response.text)
        if not collection_id:
            self.logger.error(
                "No numeric collection id in %s; the Boost filter API only accepts a numeric "
                "collection_scope, so pagination cannot continue.",
                response.url,
            )
            return
        yield self._api_request(response, collection_id, 1)

    def _collection_id(self, document: str) -> str | None:
        match = _COLLECTION_ID.search(document or "")
        return match.group(1) if match else None

    # ------------------------------------------------------------------ filter API

    def _api_request(self, response, collection_id: str, page: int) -> scrapy.Request:
        params = {
            "_": "pf",
            "shop": SHOP_DOMAIN,
            "collection_scope": collection_id,
            "page": page,
            "limit": self.page_size,
            "pg": "collection_page",
            "event_type": "init",
            "build_filter_tree": "true",
            "sort": "best-selling",
        }
        return scrapy.Request(
            f"{FILTER_API_URL}?{urlencode(params)}",
            callback=self.parse_filter_api,
            errback=self.on_error,
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9",
                "origin": BASE_URL,
                "referer": response.meta.get("collection_url", BASE_URL),
                "user-agent": _BOOST_HEADER,
            },
            # The storefront response meta carries the proxy the downloader middleware added;
            # the Boost request must not inherit it (see VitacostProxyMiddleware).
            meta={key: value for key, value in response.meta.items() if key != "proxy"}
            | {"collection_id": collection_id, "page": page},
            dont_filter=True,
        )

    def parse_filter_api(self, response):
        if response.status != 200:
            self.logger.error("Boost filter API returned HTTP %s for %s", response.status, response.url)
            return
        try:
            payload = json.loads(response.text)
        except ValueError as exc:
            self.logger.error("Boost filter API returned non-JSON at %s: %s", response.url, exc)
            return
        if not isinstance(payload, dict):
            self.logger.error("Boost filter API returned a non-object envelope at %s", response.url)
            return
        if payload.get("message"):
            self.logger.error("Boost filter API error at %s: %s", response.url, payload["message"])
            return

        page = response.meta.get("page") or 1
        products = payload.get("products")
        products = [p for p in products if isinstance(p, dict)] if isinstance(products, list) else []
        total = self._integer(payload.get("total_product"))
        if not products:
            self.logger.info(
                "No products on page %d of %s (total_product=%s). Stopping.",
                page, response.meta.get("collection_url"), total,
            )
            return

        new_items = 0
        for position, product in enumerate(products, start=1):
            item_id = str(product.get("id") or "").strip()
            if not item_id:
                self.logger.warning("Skipping a product with no id on page %d of %s", page, response.url)
                continue
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            new_items += 1
            yield self._item(product, response, page, position, total)

        # A page that only repeats products the crawler already has means the API is looping.
        if new_items == 0:
            self.logger.info("Page %d of %s repeated only known products. Stopping.", page, response.url)
            return
        if page >= self.max_pages:
            return
        if total is not None and page * self.page_size >= total:
            self.logger.info(
                "Reached total_product=%d after %d page(s) of %d. Stopping.",
                total, page, self.page_size,
            )
            return
        yield self._api_request(response, response.meta["collection_id"], page + 1)

    # ------------------------------------------------------------------ item mapping

    def _item(self, product: dict, response, page: int, position: int, total: int | None) -> dict:
        price = self._number(product.get("price_min"))
        original = self._number(product.get("compare_at_price_min"))
        discount = self._number(product.get("percent_sale_min"))
        if not discount and price and original and original > price:
            discount = round((original - price) / original * 100, 2)
        on_sale = bool(original and price and original > price)
        if original is not None and (price is None or original <= price):
            # `compare_at_price_min` is populated with the current price on non-reduced items.
            original = None

        images = product.get("images_info")
        images = [i for i in images if isinstance(i, dict)] if isinstance(images, list) else []
        images = sorted(images, key=lambda i: self._integer(i.get("position")) or 0)
        primary = images[0] if images else {}
        variants = product.get("variants")
        variants = [v for v in variants if isinstance(v, dict)] if isinstance(variants, list) else []
        options = self._options(product.get("options_with_values"))
        stock = [self._integer(v.get("inventory_quantity")) or 0 for v in variants]
        tags = product.get("tags")
        tags = tags if isinstance(tags, list) else []
        metafields = self._metafields(product.get("metafields"))
        # `review_count` is always 0 in this API; the real counts live in the merchant's
        # Judge.me metafields, and `review_ratings` mirrors the `rating` metafield value.
        rating_meta = self._json_field(metafields.get("rating"), "value")
        reviews_count = self._integer(metafields.get("rating_count")) or self._integer(
            product.get("review_count")
        )

        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "handle": response.meta.get("handle"),
            "collection_id": response.meta.get("collection_id"),
            "item_id": str(product.get("id") or ""),
            "title": str(product.get("title") or "").strip() or None,
            "url": urljoin(BASE_URL, f"/products/{product.get('handle')}/"),
            "brand": str(product.get("vendor") or "").strip() or None,
            "product_type": self._joined(product.get("product_type")),
            "product_category": str(product.get("product_category") or "").strip() or None,
            "tags": ", ".join(str(t) for t in tags) or None,
            "price": price,
            "original_price": original,
            "discount_percentage": discount if on_sale else None,
            "currency": "USD",
            "on_sale": on_sale,
            "out_of_stock": not bool(product.get("available")),
            "in_stock_quantity": sum(stock) or None,
            "image_url": str(primary.get("src") or "").strip() or None,
            "image_alt": str(primary.get("alt") or "").strip() or None,
            "image_count": self._integer(product.get("total_images")) or len(images) or None,
            "sku": str(product.get("skus")[0]).strip()
            if isinstance(product.get("skus"), list) and product.get("skus") else None,
            "barcode": str(product.get("barcodes")[0]).strip()
            if isinstance(product.get("barcodes"), list) and product.get("barcodes") else None,
            "option_count": len(options) or None,
            "options": self._flatten_options(options),
            "package_quantity": metafields.get("PackageQuantity"),
            "form": metafields.get("Form"),
            "strength": metafields.get("Strength"),
            "badges": self._badges(metafields),
            "description": self._description(product.get("body_html")),
            "rating": self._number(rating_meta) or self._number(product.get("review_ratings")),
            "reviews_count": reviews_count or None,
            "published_at": str(product.get("published_at") or "").strip() or None,
            "page": page,
            "position": position,
            "total_count": total,
            "scraped_timestamp": self.get_timestamp(),
            "source_url": response.url,
            "source": "vitacost_boost_filter_api",
            "raw": self._raw(product),
        }

    @staticmethod
    def _raw(product: dict) -> dict:
        """The API record minus `body_html`, which is the full page copy and dwarfs the rest."""
        return {key: value for key, value in product.items() if key != "body_html"}

    @staticmethod
    def _metafields(raw) -> dict:
        """`metafields` is a flat `[{key, value, namespace, ...}]` list on the API record."""
        result: dict[str, str] = {}
        if not isinstance(raw, list):
            return result
        for entry in raw:
            if isinstance(entry, dict) and entry.get("key"):
                result[str(entry["key"])] = str(entry.get("value") or "").strip()
        return result

    @staticmethod
    def _badges(metafields: dict) -> str | None:
        """`Clearance` / `OnSale` metafields carry the merchandising flags, or "Full Price"."""
        flags = {
            value
            for value in (metafields.get("Clearance"), metafields.get("OnSale"))
            if value and value.lower() != "full price"
        }
        return ", ".join(sorted(flags)) or None

    @staticmethod
    def _json_field(value, field: str):
        if not isinstance(value, str) or not value.strip():
            return None
        try:
            parsed = json.loads(value)
        except ValueError:
            return None
        return parsed.get(field) if isinstance(parsed, dict) else None

    @staticmethod
    def _options(raw) -> list[dict]:
        options = raw if isinstance(raw, list) else []
        result = []
        for option in options:
            if not isinstance(option, dict):
                continue
            values = option.get("values")
            values = [v for v in values if isinstance(v, dict)] if isinstance(values, list) else []
            titles = [str(v.get("title") or "").strip() for v in values]
            titles = [t for t in titles if t and t != "Default Title"]
            if not titles:
                continue
            result.append({"name": str(option.get("label") or option.get("name") or "").strip(), "values": titles})
        return result

    @staticmethod
    def _flatten_options(options: list[dict]) -> str | None:
        parts = [
            f"{o['name']}: {', '.join(o['values'])}"
            for o in options
            if o.get("name") and o.get("values")
        ]
        return "; ".join(parts) or None

    @staticmethod
    def _joined(value) -> str | None:
        if isinstance(value, list):
            value = [str(v).strip() for v in value if str(v).strip()]
            return ", ".join(value) or None
        text = str(value or "").strip()
        return text or None

    @staticmethod
    def _description(body_html) -> str | None:
        if not isinstance(body_html, str) or not body_html.strip():
            return None
        text = re.sub(r"<[^>]+>", " ", body_html)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        return text[:400] or None

    @staticmethod
    def _handle(url: str | None) -> str | None:
        if not url:
            return None
        path = url.split("?", 1)[0].split("#", 1)[0].rstrip("/")
        if "/collections/" not in path:
            return None
        handle = path.rsplit("/collections/", 1)[-1].strip("/")
        return handle or None

    @staticmethod
    def _clamp_page_size(value) -> int:
        try:
            size = int(value)
        except (TypeError, ValueError):
            size = DEFAULT_PAGE_SIZE
        size = max(1, min(size, MAX_PAGE_SIZE))
        return size

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

    def on_error(self, failure):
        request = failure.request
        self.logger.error(
            "Request failed for %s (page=%s): %s", request.url, request.meta.get("page"), failure.value
        )