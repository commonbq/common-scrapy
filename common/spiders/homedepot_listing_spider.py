from __future__ import annotations

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.homedepot_categories import HOMEDEPOT_CATEGORIES
from common.spiders.homedepot_search_spider import HomeDepotSearchSpider

# The residential pool is not perfectly reliable, and a ScrapeOps failure arrives
# as HTTP 200, so Scrapy's RetryMiddleware never sees a retryable status. The
# spider therefore re-requests a bounded number of times itself.
MAX_PROXY_RETRIES = 3

# ScrapeOps failure envelope marker (367-byte JSON body served with HTTP 200).
PROXY_ENVELOPE_MARKER = "We couldn't retrieve a successful response"


class HomeDepotListingSpider(BaseListingSpider):
    """Extract category products from Home Depot's embedded Apollo state."""

    name = "homedepot_listing"
    allowed_domains = ["homedepot.com", "www.homedepot.com", "127.0.0.1"]

    # Department landing pages whose PLPs expose products in __APOLLO_STATE__.
    categories = HOMEDEPOT_CATEGORIES

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "sku", "title", "brand", "model", "url",
            "image_url", "price", "original_price", "currency", "rating",
            "reviews_count", "availability", "source", "category_url", "page",
            "timestamp",
        ],
        "HTTPERROR_ALLOW_ALL": True,
    }

    def start_requests(self):
        yield self._request(self.url or self._page_url(1), self.category, 1)

    def _request(self, url: str, category, page: int, retries: int = 0) -> scrapy.Request:
        meta = {"category": category, "page": page, "proxy_retries": retries}
        return scrapy.Request(
            url,
            callback=self.parse,
            errback=self._on_error,
            meta=meta,
            dont_filter=True,
        )

    def _on_error(self, failure):
        """Retry a bounded number of times, then surface the failure."""
        request = failure.request
        retries = int(request.meta.get("proxy_retries", 0))
        if retries < MAX_PROXY_RETRIES:
            self.logger.warning(
                "Home Depot request failed (%s); retrying %s/%s: %s",
                failure.value, retries + 1, MAX_PROXY_RETRIES, request.url,
            )
            yield self._request(
                request.url, request.meta.get("category"),
                int(request.meta.get("page", 1)), retries + 1,
            )
        else:
            self.logger.error(
                "Home Depot request failed after %s attempts: %s (%s)",
                MAX_PROXY_RETRIES + 1, request.url, failure.value,
            )

    def parse(self, response: scrapy.http.Response):
        retries = int(response.meta.get("proxy_retries", 0))

        if self._is_blocked(response):
            if retries < MAX_PROXY_RETRIES:
                self.logger.warning(
                    "Home Depot blocked payload (HTTP %s, %s bytes); retrying %s/%s: %s",
                    response.status, len(response.body), retries + 1,
                    MAX_PROXY_RETRIES, response.url,
                )
                yield self._request(
                    response.url, response.meta.get("category"),
                    int(response.meta.get("page", 1)), retries + 1,
                )
                return
            raise RuntimeError(
                f"Home Depot {response.url} returned a blocked/proxy payload "
                f"(HTTP {response.status}, {len(response.body)} bytes, body starts "
                f"{response.text[:120]!r}) after {MAX_PROXY_RETRIES + 1} attempts; "
                "the response is a challenge/proxy envelope, not a product listing"
            )

        state = HomeDepotSearchSpider._extract_js_object(response.text, "__APOLLO_STATE__")
        if not state:
            if retries < MAX_PROXY_RETRIES:
                self.logger.warning(
                    "Home Depot PLP missing __APOLLO_STATE__; retrying %s/%s: %s",
                    retries + 1, MAX_PROXY_RETRIES, response.url,
                )
                yield self._request(
                    response.url, response.meta.get("category"),
                    int(response.meta.get("page", 1)), retries + 1,
                )
                return
            raise RuntimeError(
                f"Home Depot PLP did not contain __APOLLO_STATE__ at {response.url} "
                f"after {MAX_PROXY_RETRIES + 1} attempts"
            )

        search_model = self._find_search_model(state)
        refs = self._product_refs(search_model)
        if not isinstance(refs, list) or not refs:
            raise RuntimeError(f"No Home Depot Apollo products found at {response.url}")

        category = response.meta.get("category")
        page = int(response.meta.get("page", 1))
        seen = set()
        for ref in refs:
            product = state.get(ref.get("__ref"), {}) if isinstance(ref, dict) else {}
            identifiers = product.get("identifiers") or {}
            item_id = identifiers.get("itemId") or product.get("itemId")
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            pricing = next(
                (product[key] for key in product if isinstance(key, str) and key.startswith("pricing(") and isinstance(product[key], dict)),
                {},
            )
            image = ((product.get("media") or {}).get("images") or [{}])[0] or {}
            reviews = ((product.get("reviews") or {}).get("ratingsReviews") or {})
            canonical = identifiers.get("canonicalUrl")
            yield {
                "category": category,
                "item_id": item_id,
                "sku": identifiers.get("storeSkuNumber"),
                "title": identifiers.get("productLabel"),
                "brand": identifiers.get("brandName"),
                "model": identifiers.get("modelNumber"),
                "url": f"https://www.homedepot.com{canonical}" if canonical and canonical.startswith("/") else canonical,
                "image_url": (image.get("url") or "").replace("<SIZE>", "300") or None,
                "price": self._number(pricing.get("value")),
                "original_price": self._number(pricing.get("original")),
                "currency": pricing.get("currency") or "USD",
                "rating": self._number(reviews.get("averageRating")),
                "reviews_count": self._integer(reviews.get("totalReviews")),
                "availability": product.get("availabilityType") or product.get("availabilityStatus"),
                "source": "homedepot_apollo_state",
                "category_url": self._category_entry()["url"],
                "page": page,
                "timestamp": self.job_timestamp,
            }

        if page < self.max_pages and not self.url:
            next_page = page + 1
            yield self._request(self._page_url(next_page), category, next_page)

    @staticmethod
    def _find_search_model(state: dict):
        """Locate the SearchModel.

        The current storefront nests it in ``ROOT_QUERY`` under a
        ``searchModel({...})`` key; the legacy bootstrap exposed it as a
        top-level ``SearchModel:<...>`` object.
        """
        root = state.get("ROOT_QUERY")
        if isinstance(root, dict):
            for key, value in root.items():
                if isinstance(key, str) and key.startswith("searchModel(") and isinstance(value, dict):
                    return value
        return next(
            (value for value in state.values() if isinstance(value, dict) and value.get("__typename") == "SearchModel"),
            None,
        )

    @staticmethod
    def _product_refs(search_model):
        """Return the ``products`` reference list from any accepted Apollo shape.

        The current shape stores it under a plain ``products`` key; the legacy
        bootstrap used a serialized ``products({...})`` key.
        """
        if not isinstance(search_model, dict):
            return None
        for key in search_model:
            if isinstance(key, str) and key.startswith("products("):
                return search_model.get(key)
        return search_model.get("products")

    @staticmethod
    def _is_blocked(response: scrapy.http.Response) -> bool:
        """Classify HTTP 200 proxy/challenge bodies before parsing selectors."""
        if response.status != 200:
            return True
        text = response.text or ""
        if PROXY_ENVELOPE_MARKER in text:
            return True
        head = text[:400].lstrip().lower()
        return head.startswith("<!doctype html") and "access denied" in text.lower()[:2000]

    def _category_entry(self):
        return self.category_entry(self.category)

    def _page_url(self, page: int) -> str:
        base = self._category_entry()["url"]
        return base if page == 1 else f"{base}?Nao={(page - 1) * 24}"

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None
