from __future__ import annotations

import json
import re
from urllib.parse import urlencode, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class MacysListingSpider(BaseListingSpider):
    """Macy's listing spider via /xapi/discover/v1/page (through r.jina.ai)."""

    name = "macys_listing"
    allowed_domains = ["r.jina.ai", "macys.com", "www.macys.com"]

    categories = [
        {"category": "laptops", "url": "https://www.macys.com/shop/featured/laptop"},
        {"category": "shoes", "url": "https://www.macys.com/shop/featured/shoes"},
        {"category": "dresses", "url": "https://www.macys.com/shop/featured/dresses"},
        {"category": "fragrance", "url": "https://www.macys.com/shop/featured/fragrance"},
        {"category": "bedding", "url": "https://www.macys.com/shop/featured/bedding"},
    ]

    def start_requests(self):
        page_index = 1
        api_url = self._build_macys_api_url(page_index)
        yield scrapy.Request(
            self._to_jina_url(api_url),
            callback=self.parse,
            meta={"page_index": page_index, "api_url": api_url, "pathname": self._default_pathname()},
        )

    def parse(self, response: scrapy.http.Response):
        payload = self._extract_json_payload(response.text)
        if not payload:
            self.logger.warning("Unable to extract Macy's JSON payload")
            return

        redirect_pathname = self._extract_redirect_pathname(payload)
        redirected = bool(response.meta.get("redirected"))
        if redirect_pathname and not redirected:
            page_index = int(response.meta.get("page_index", 1))
            redirect_api = self._build_macys_api_url(page_index=page_index, pathname=redirect_pathname)
            yield scrapy.Request(
                self._to_jina_url(redirect_api),
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
            self._to_jina_url(next_api),
            callback=self.parse,
            meta={"page_index": next_page, "api_url": next_api, "pathname": pathname, "redirected": True},
        )

    def _build_macys_api_url(self, page_index: int, pathname: str | None = None) -> str:
        pathname = pathname or self._default_pathname()
        sort = (getattr(self, "sort", None) or "PRICE_LOW_TO_HIGH").strip()

        params = {
            "pathname": pathname,
            "_navigationType": "SEARCH",
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
        return f"https://www.macys.com/xapi/discover/v1/page?{urlencode(params)}"

    def _default_pathname(self) -> str:
        target_url = self.resolve_target_url()
        parsed = urlparse(target_url)
        return parsed.path or "/"

    def _extract_redirect_pathname(self, payload: dict) -> str | None:
        redirect = (payload or {}).get("redirect") or {}
        url = (redirect or {}).get("url")
        if not isinstance(url, str) or not url.strip():
            return None
        parsed = urlparse(url.strip())
        return parsed.path or None

    def _to_jina_url(self, url: str) -> str:
        return f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"

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
        for entry in collection:
            product = (entry or {}).get("product") or {}
            detail = product.get("detail") or {}
            pricing = product.get("pricing") or {}
            imagery = product.get("imagery") or {}

            price_value, price_text = self._extract_price(pricing)
            review_stats = detail.get("reviewStatistics") or {}

            product_id = product.get("id")
            product_url = self._product_url(product)

            out.append(
                {
                    "item_id": str(product_id) if product_id is not None else None,
                    "title": detail.get("name"),
                    "brand": detail.get("brand"),
                    "url": product_url,
                    "image_url": self._extract_image(imagery),
                    "price": price_value,
                    "price_text": price_text,
                    "rating": self._to_float(
                        review_stats.get("avgRating")
                        or review_stats.get("averageRating")
                        or review_stats.get("rating")
                    ),
                    "reviews_count": self._to_int(
                        review_stats.get("totalReviews")
                        or review_stats.get("reviewCount")
                        or review_stats.get("count")
                    ),
                    "source": "macys_xapi_discover_v1_page_via_r.jina.ai",
                }
            )

        return out

    def _find_product_collection(self, payload: dict) -> list[dict]:
        # Keep fast-path for known shape.
        try:
            collection = payload["body"]["canvas"]["rows"][0]["rowSortableGrid"]["zones"][1]["sortableGrid"]["collection"]
            if isinstance(collection, list):
                return collection
        except Exception:
            pass

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
                    return primary[k]
        if isinstance(primary, str) and primary:
            return primary

        additional = imagery.get("additionalImageSource")
        if isinstance(additional, list) and additional:
            first = additional[0]
            if isinstance(first, dict):
                return first.get("url") or first.get("imageUrl")
            if isinstance(first, str):
                return first
        return None

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
