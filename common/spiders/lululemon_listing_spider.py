from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.lululemon_categories import LULULEMON_CATEGORIES

# The residential pool is not perfectly reliable: roughly one request in three
# still comes back as a ScrapeOps failure envelope (HTTP 200, 367-byte JSON).
# Deterministic failures are invisible to Scrapy's RetryMiddleware because the
# status is 200, so the spider re-requests a bounded number of times itself.
MAX_PROXY_RETRIES = 3


class LululemonListingSpider(BaseListingSpider):
    """Extract Lululemon listings from the Next.js dehydrated query state."""

    name = "lululemon_listing"
    allowed_domains = ["shop.lululemon.com", "lululemon.com", "127.0.0.1"]

    categories = LULULEMON_CATEGORIES

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category",
            "item_id",
            "title",
            "brand",
            "url",
            "image_url",
            "price",
            "original_price",
            "currency",
            "availability",
            "color_count",
            "source",
            "category_url",
            "page",
            "raw",
            "timestamp",
        ]
    }

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield self._listing_request(self._with_page(target_url, 1), self.category, 1)

    def _listing_request(self, url: str, category, page: int, retries: int = 0):
        return scrapy.Request(
            url,
            callback=self.parse,
            errback=self._on_error,
            headers=self._headers(),
            meta={
                "category": category,
                "page": page,
                "proxy_retries": retries,
            },
            dont_filter=True,
        )

    def _on_error(self, failure):
        """Retry a bounded number of times, then surface the failure.

        A proxy envelope is an HTTP 200 body, so ``_reject_non_html`` raises
        instead of letting RetryMiddleware see a retryable status. Re-requesting
        here keeps a transient residential miss from becoming a silent
        zero-item run; a real contract change still fails after the last try.
        """
        request = failure.request
        retries = int(request.meta.get("proxy_retries", 0))
        if retries < MAX_PROXY_RETRIES:
            self.logger.warning(
                "Lululemon request failed (%s); retrying %s/%s: %s",
                failure.value,
                retries + 1,
                MAX_PROXY_RETRIES,
                request.url,
            )
            yield self._listing_request(
                request.url,
                request.meta.get("category"),
                request.meta.get("page", 1),
                retries + 1,
            )
        else:
            self.logger.error(
                "Lululemon request failed after %s attempts: %s (%s)",
                MAX_PROXY_RETRIES + 1,
                request.url,
                failure.value,
            )
            return

    def parse(self, response: scrapy.http.Response):
        if self._is_proxy_payload(response):
            retries = int(response.meta.get("proxy_retries", 0))
            if retries < MAX_PROXY_RETRIES:
                self.logger.warning(
                    "Lululemon proxy envelope (%s); retrying %s/%s: %s",
                    response.text[:80],
                    retries + 1,
                    MAX_PROXY_RETRIES,
                    response.url,
                )
                yield self._listing_request(
                    response.url,
                    response.meta.get("category"),
                    int(response.meta.get("page", 1)),
                    retries + 1,
                )
                return
            raise RuntimeError(
                f"Lululemon {response.url} did not return an HTML document "
                f"after {MAX_PROXY_RETRIES + 1} attempts (body starts "
                f"{response.text[:120]!r}); the response is a proxy/challenge "
                "payload, not a product listing"
            )
        self._reject_non_html(response)
        data = response.css("script#__NEXT_DATA__::text").get()
        if not data:
            raise RuntimeError(f"No Lululemon __NEXT_DATA__ found at {response.url}")
        page_state = self._page_state(json.loads(data))
        if page_state is None:
            raise RuntimeError(
                f"No Lululemon category page data found at {response.url}"
            )
        products = page_state["products"]
        if not products:
            raise RuntimeError(
                f"No Lululemon category products found at {response.url}"
            )

        category = response.meta.get("category")
        page = int(response.meta.get("page") or page_state["current_page"] or 1)
        for raw_product in products:
            normalized = self._normalize_product(raw_product)
            if normalized is None:
                continue
            yield self._item(normalized, category, page, response)

        total_pages = page_state["total_pages"]
        if page < min(total_pages, self.max_pages):
            next_page = page + 1
            yield self._listing_request(
                self._with_page(response.url, next_page), category, next_page
            )

    def _item(self, product: dict, category, page: int, response):
        url = product["url"]
        if url and url.startswith("/"):
            url = f"https://shop.lululemon.com{url}"
        return {
            "category": category,
            "item_id": product["item_id"],
            "title": product["title"],
            "brand": "lululemon",
            "url": url,
            "image_url": product["image_url"],
            "price": product["price"],
            "original_price": product["original_price"],
            "currency": product["currency"],
            "availability": product["availability"],
            "color_count": product["color_count"],
            "source": "next_data_category_page_query",
            "category_url": response.url,
            "page": page,
            "raw": product["raw"],
        }

    def _is_proxy_payload(self, response: scrapy.http.Response) -> bool:
        """True when the body is a proxy/challenge payload, not a document.

        The ScrapeOps datacenter route answers shop.lululemon.com with an HTTP
        200 55-byte JSON error envelope; ``response.css`` on a JSON body raises
        ``ValueError: Cannot use css on a Selector of type 'json'``, which reads
        as a parser bug and hides the routing failure.
        """
        if response.status != 200:
            return False
        content_type = (response.headers.get("Content-Type") or b"").decode(
            "utf-8", "replace"
        ).lower()
        return "html" not in content_type and not response.text.lstrip().startswith("<")

    def _reject_non_html(self, response: scrapy.http.Response) -> None:
        """Reject a non-HTML status before extraction reaches the selectors."""
        if response.status != 200:
            raise RuntimeError(
                f"Lululemon listing returned HTTP {response.status}: {response.url}"
            )
        if self._is_proxy_payload(response):
            raise RuntimeError(
                f"Lululemon {response.url} did not return an HTML document "
                f"(body starts {response.text[:120]!r}); the response is a "
                "proxy/challenge payload, not a product listing"
            )

    def _page_state(self, data: dict) -> dict | None:
        """Return the category feed and pagination for either Next.js contract.

        Lululemon re-platformed its category grid: the legacy
        ``CategoryPageDataQuery`` query carried a flat ``products`` list, while
        the current ``catalogPageData`` query returns a JSON:API document whose
        product entities live in ``included`` and whose paging is expressed as
        ``totalCount``/``limit``/``offset``. Both are handled so a fixture from
        either era keeps working.
        """
        queries = (
            data.get("props", {})
            .get("pageProps", {})
            .get("dehydratedState", {})
            .get("queries", [])
        )
        for query in queries:
            key = query.get("queryKey")
            if not isinstance(key, list) or not key:
                continue
            pages = (query.get("state", {}).get("data") or {}).get("pages") or []
            if not pages or not isinstance(pages[0], dict):
                continue
            page0 = pages[0]
            if key[0] == "CategoryPageDataQuery":
                return {
                    "products": page0.get("products") or [],
                    "current_page": int(page0.get("currentPage") or 1),
                    "total_pages": int(page0.get("totalProductPages") or 1),
                }
            if key[0] == "catalogPageData":
                attributes = (page0.get("data") or {}).get("attributes") or {}
                total = int(attributes.get("totalCount") or 0)
                limit = int(attributes.get("limit") or 40) or 40
                offset = int(attributes.get("offset") or 0)
                return {
                    "products": [
                        entity
                        for entity in page0.get("included") or []
                        if isinstance(entity, dict) and entity.get("type") == "products"
                    ],
                    "current_page": offset // limit + 1,
                    "total_pages": max(1, -(-total // limit)),
                }
        return None

    def _normalize_product(self, product: dict) -> dict | None:
        """Map a legacy or JSON:API product onto the shared item fields."""
        if not isinstance(product, dict):
            return None
        attributes = product.get("attributes")
        if isinstance(attributes, dict):
            return self._normalize_jsonapi(product, attributes)
        return self._normalize_legacy(product)

    @staticmethod
    def _normalize_legacy(product: dict) -> dict | None:
        item_id = (
            product.get("productId")
            or product.get("repositoryId")
            or product.get("unifiedId")
        )
        if not item_id:
            return None
        swatches = [v for v in product.get("swatches") or [] if isinstance(v, dict)]
        return {
            "item_id": item_id,
            "title": product.get("displayName"),
            "url": product.get("pdpUrl"),
            "image_url": (
                swatches[0].get("img") or swatches[0].get("swatch")
            ) if swatches else None,
            "price": LululemonListingSpider._number(
                product.get("productSalePrice") or product.get("listPrice")
            ),
            "original_price": LululemonListingSpider._number(product.get("listPrice")),
            "currency": product.get("currencyCode"),
            "availability": "InStock" if product.get("isInStock", True) else "OutOfStock",
            "color_count": len(swatches),
            "raw": product,
        }

    @staticmethod
    def _normalize_jsonapi(entity: dict, attributes: dict) -> dict | None:
        item_id = attributes.get("unifiedId") or entity.get("id")
        if not item_id:
            return None
        variant_colors = [
            color
            for style in attributes.get("styles") or []
            if isinstance(style, dict)
            for color in style.get("colors") or []
            if isinstance(color, dict)
        ]
        price_entry = next(
            (c["price"] for c in variant_colors if isinstance(c.get("price"), dict)),
            {},
        )
        image_url = next(
            (
                images[0]["url"]
                for c in variant_colors
                if isinstance(c.get("images"), list)
                for images in [c["images"]]
                if images and isinstance(images[0], dict) and images[0].get("url")
            ),
            None,
        )
        if not image_url:
            swatches = attributes.get("colors") or []
            if swatches and isinstance(swatches[0], dict):
                image_url = swatches[0].get("url")
        availability = any(
            (c.get("availability") or {}).get("isAvailable")
            for c in variant_colors
        )
        return {
            "item_id": item_id,
            "title": attributes.get("name"),
            "url": attributes.get("url"),
            "image_url": image_url,
            "price": LululemonListingSpider._number(
                price_entry.get("salePrice") or price_entry.get("listPrice")
            ),
            "original_price": LululemonListingSpider._number(
                price_entry.get("listPrice")
            ),
            "currency": price_entry.get("currencyCode"),
            "availability": "InStock" if availability else "OutOfStock",
            "color_count": len(attributes.get("colors") or []),
            "raw": attributes,
        }

    @staticmethod
    def _number(value):
        if isinstance(value, dict):
            value = value.get("amount") or value.get("value")
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
