from __future__ import annotations

import html
import json
import re
from urllib.parse import urlencode, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.utils import dict_get


class MacysListingSpider(BaseListingSpider):
    """Macy's listing spider via /xapi/discover/v1/page."""
    name = "macys_listing"
    allowed_domains = ["macys.com", "www.macys.com"]

    categories = [
        {"category": "fragrance", "url": "https://www.macys.com/shop/beauty/fragrance", "id": "277259"},
        {"category": "skin-care", "url": "https://www.macys.com/shop/beauty/skin-care", "id": "30078"},
        {"category": "makeup", "url": "https://www.macys.com/shop/beauty/makeup", "id": "30077"},
        {"category": "hair-care", "url": "https://www.macys.com/shop/beauty/hair-care", "id": "60600"},
    ]

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "productId",
            "title",
            "brand",
            "url",
            "productUrl",
            "imageUrl",
            "additionalImageUrls",
            "price",
            "priceText",
            "priceType",
            "rating",
            "reviewsCount",
            "typeName",
            "categoryId",
            "isActive",
            "isAvailable",
            "isRegistrable",
            "isMemberProduct",
            "intlSuppressProduct",
            "badgeCount",
            "badgeHeaders",
            "rawProduct",
            "timestamp",
        ],
    }

    def start_requests(self):
        page_index = 1
        api_url = self._build_macys_api_url(page_index)
        yield scrapy.Request(
            api_url,
            callback=self.parse,
            meta={"page_index": page_index, "api_url": api_url, "pathname": self._default_pathname()},
        )

    def parse(self, response: scrapy.http.Response):
        payload = response.json()
        if not payload:
            self.logger.warning("Unable to extract Macy's JSON payload")
            return

        redirect_pathname = self._extract_redirect_pathname(payload)
        redirected = bool(response.meta.get("redirected"))
        if redirect_pathname and not redirected:
            page_index = int(response.meta.get("page_index", 1))
            redirect_api = self._build_macys_api_url(page_index=page_index, pathname=redirect_pathname)
            self.logger.info(f"Redirecting to Macy's API URL: {redirect_api} (pathname: {redirect_pathname})")
            yield scrapy.Request(
                redirect_api,
                callback=self.parse,
                meta={
                    "page_index": page_index,
                    "api_url": redirect_api,
                    "pathname": redirect_pathname,
                    "redirected": True,
                },
            )
            return

        items = self._extract_products(payload)
        for item in items:
            yield item

        current_page = int(response.meta.get("page_index", 1))
        if current_page >= self.max_pages or not items:
            return

        next_page = current_page + 1
        pathname = response.meta.get("pathname") or self._default_pathname()
        next_api = self._build_macys_api_url(next_page, pathname=pathname)
        yield scrapy.Request(
            next_api,
            callback=self.parse,
            meta={"page_index": next_page, "api_url": next_api, "pathname": pathname, "redirected": True},
        )

    def _get_category_id(self) -> str | None:
        for entry in self.categories:
            if entry.get("category") == self.category:
                return entry.get("id")

    def _build_macys_api_url(self, page_index: int, pathname: str | None = None) -> str:
        pathname = pathname or self._default_pathname()
        category_id = self._get_category_id()

        sort = (getattr(self, "sort", None) or "ORIGINAL").strip()

        params = {
            "id": category_id,
            "_navigationType": "BROWSE",
            "_shoppingMode": "SITE",
            "sortBy": sort,
            "productsPerPage": 60,
            "pageIndex": page_index,
            "_application": "SITE",
            "_regionCode": "US",
            "currencyCode": "USD",
            "size": "medium",
            "_deviceType": "DESKTOP",
            "_customerState": "GUEST",
        }
        return f"https://www.macys.com/xapi/discover/v1/page?pathname={pathname}&{urlencode(params)}"

    def _default_pathname(self) -> str:
        target_url = self.resolve_target_url()
        parsed = urlparse(target_url)
        return parsed.path or "/"

    def _extract_redirect_pathname(self, payload: dict) -> str | None:
        url = dict_get(payload or {}, "redirect.url")
        if not isinstance(url, str) or not url.strip():
            return None
        parsed = urlparse(url.strip())
        return parsed.path or None

    def _extract_json_payload(self, text: str) -> dict | None:
        start = text.find("{")
        if start == -1:
            return None

        candidate = text[start:]
        end = candidate.rfind("}")
        if end == -1:
            return None

        raw_json = candidate[: end + 1]
        try:
            payload = json.loads(raw_json)
            return payload if isinstance(payload, dict) else None
        except json.JSONDecodeError:
            return None

    def _extract_products(self, payload: dict) -> list[dict]:
        collection = self._find_product_collection(payload)
        if not collection:
            return []

        out: list[dict] = []
        products = [entry["product"] for entry in collection if entry.get("product")]

        for product in products:
            detail = product.get("detail") or {}
            pricing = product.get("pricing") or {}
            imagery = product.get("imagery") or {}
            availability = product.get("availability") or {}
            flags = detail.get("flags") or {}
            taxonomy = dict_get(product, "relationships.taxonomy") or {}
            selected_color = dict_get(product, "traits.colors.selectedColor") or {}
            selected_color_imagery = selected_color.get("imagery") or {}

            price_value, price_text = self._extract_price(pricing)
            review_stats = self._extract_review_stats(detail)

            product_id = product.get("id")
            identifier = product.get("identifier") or {}
            identifier_product_id = identifier.get("productId")
            product_url = self._product_url(product)
            image_url = self._extract_image(selected_color_imagery or imagery)
            additional_image_urls = self._extract_additional_images(selected_color_imagery or imagery)
            badges = pricing.get("badges") or []

            out.append(
                {
                    "productId": product_id or identifier_product_id,
                    "title": self._decode_text(detail.get("name")),
                    "brand": self._decode_text(detail.get("brand")),
                    "url": product_url,
                    "productUrl": self._normalize_product_path(identifier.get("productUrl")),
                    "imageUrl": image_url,
                    "additionalImageUrls": json.dumps(additional_image_urls) if additional_image_urls else None,
                    "price": price_value,
                    "priceText": price_text,
                    "priceType": self._extract_price_type(pricing),
                    "rating": self._to_float(
                        review_stats.get("avgRating")
                        or review_stats.get("averageRating")
                        or review_stats.get("rating")
                    ),
                    "reviewsCount": self._to_int(
                        review_stats.get("totalReviews")
                        or review_stats.get("reviewCount")
                        or review_stats.get("count")
                    ),
                    "typeName": detail.get("typeName"),
                    "categoryId": self._to_int(taxonomy.get("defaultCategoryId")),
                    "isActive": availability.get("active"),
                    "isAvailable": availability.get("available"),
                    "isRegistrable": flags.get("registrable"),
                    "isMemberProduct": flags.get("memberProduct"),
                    "intlSuppressProduct": flags.get("intlSuppressProduct"),
                    "badgeCount": len(badges),
                    "badgeHeaders": json.dumps(self._extract_badge_headers(badges)) if badges else None,
                    "rawProduct": json.dumps(product),
                    "timestamp": self.get_timestamp(),
                }
            )

        return out

    def _find_product_collection(self, payload: dict) -> list[dict]:
        # Keep fast-path for known shape.
        collection = dict_get(payload, "body.canvas.rows.0.rowSortableGrid.zones.1.sortableGrid.collection")
        if isinstance(collection, list):
            return collection

        # Fallback: recursively find a plausible product collection list.
        def walk(node):
            if isinstance(node, dict):
                collection = node.get("collection")
                if isinstance(collection, list) and collection:
                    first = collection[0] if collection else None
                    if isinstance(first, dict) and isinstance(first.get("product"), dict):
                        return collection
                for value in node.values():
                    found = walk(value)
                    if found:
                        return found
            elif isinstance(node, list):
                for value in node:
                    found = walk(value)
                    if found:
                        return found
            return []

        return walk(payload) or []

    def _product_url(self, product: dict) -> str | None:
        identifier = product.get("identifier") or {}
        identifier_url = self._normalize_product_path(identifier.get("productUrl"))
        if identifier_url:
            return identifier_url

        pid = product.get("id")
        slug = ((product.get("detail") or {}).get("name") or "").strip().lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
        if pid and slug:
            return f"https://www.macys.com/shop/product/{slug}?ID={pid}"
        if pid:
            return f"https://www.macys.com/shop/product?ID={pid}"
        return None

    def _extract_image(self, imagery: dict) -> str | None:
        primary = imagery.get("primaryImage") or {}
        if isinstance(primary, dict):
            for k in ("url", "imageUrl", "image", "filePath"):
                if primary.get(k):
                    return self._normalize_image_url(primary[k])
        if isinstance(primary, str) and primary:
            return self._normalize_image_url(primary)

        additional = imagery.get("additionalImageSource")
        if isinstance(additional, list) and additional:
            first = additional[0]
            if isinstance(first, dict):
                return self._normalize_image_url(
                    first.get("url") or first.get("imageUrl") or first.get("filePath")
                )
            if isinstance(first, str):
                return self._normalize_image_url(first)
        return None

    def _extract_additional_images(self, imagery: dict) -> list[str]:
        urls: list[str] = []
        additional = imagery.get("additionalImageSource")
        if not isinstance(additional, list):
            return urls

        for image in additional:
            if isinstance(image, dict):
                candidate = image.get("url") or image.get("imageUrl") or image.get("filePath")
            else:
                candidate = image
            normalized = self._normalize_image_url(candidate)
            if normalized and normalized not in urls:
                urls.append(normalized)
        return urls

    def _extract_price(self, pricing: dict) -> tuple[float | None, str | None]:
        price = pricing.get("price") or {}
        tiered = price.get("tieredPrice") or []
        if not tiered:
            return None, None
        values = (tiered[0] or {}).get("values") or []
        if not values:
            return None, None

        first = values[0] or {}
        value = self._to_float(first.get("value"))
        text = first.get("formattedValue")
        return value, text

    def _extract_price_type(self, pricing: dict) -> str | None:
        price = pricing.get("price") or {}
        tiered = price.get("tieredPrice") or []
        if not tiered:
            return None
        values = (tiered[0] or {}).get("values") or []
        if not values:
            return None
        return (values[0] or {}).get("type")

    def _extract_review_stats(self, detail: dict) -> dict:
        review_stats = detail.get("reviewStatistics") or {}
        aggregate = review_stats.get("aggregate")
        if isinstance(aggregate, dict):
            return aggregate
        return review_stats

    def _extract_badge_headers(self, badges: list[dict]) -> list[str]:
        headers: list[str] = []
        for badge in badges:
            if not isinstance(badge, dict):
                continue
            value = self._decode_text(badge.get("header") or badge.get("checkoutDescription"))
            if value and value not in headers:
                headers.append(value)
        return headers

    def _normalize_product_path(self, product_url: str | None) -> str | None:
        if not isinstance(product_url, str) or not product_url.strip():
            return None
        if product_url.startswith("http://") or product_url.startswith("https://"):
            return product_url
        if product_url.startswith("/"):
            return f"https://www.macys.com{product_url}"
        return f"https://www.macys.com/{product_url.lstrip('/')}"

    def _normalize_image_url(self, value: str | None) -> str | None:
        if not isinstance(value, str) or not value.strip():
            return None
        value = value.strip()
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return f"https://slimages.macysassets.com/is/image/MCY/products/{value}?$thumb$"

    def _decode_text(self, value: str | None) -> str | None:
        if not isinstance(value, str):
            return None
        return html.unescape(value).strip() or None

    def _to_float(self, v):
        if v is None:
            return None
        try:
            return float(v)
        except Exception:
            return None

    def _to_int(self, v):
        if v is None:
            return None
        try:
            return int(v)
        except Exception:
            return None
