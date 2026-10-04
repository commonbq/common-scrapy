from __future__ import annotations

import json
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.bathandbodyworks_categories import flattened_categories


class BathAndBodyWorksListingSpider(BaseListingSpider):
    """Extract products only from the server-rendered React Query hydration."""

    name = "bathandbodyworks_listing"
    allowed_domains = ["bathandbodyworks.com", "www.bathandbodyworks.com"]
    # This spider supports direct `url=`/`category_url=` runs, so it must opt out of
    # the base class's category-only gate; resolve_target_url() still rejects a run
    # with no usable target.
    require_category_arg = False
    categories = flattened_categories()

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "upc", "title", "brand", "url", "image_url",
            "price", "regular_price", "currency", "availability", "rating",
            "reviews_count", "product_type", "fragrance", "size", "color",
            "position", "source", "category_url", "page", "raw",
        ]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_ids: set[str] = set()

    def start_requests(self):
        yield scrapy.Request(
            self.resolve_target_url(), callback=self.parse,
            meta={"category": self.category, "page": 1, "allow_offsite": bool(self.url)},
            headers=self._headers(),
        )

    def parse(self, response: scrapy.http.Response):
        page_number = int(response.meta.get("page", 1))
        product_page = self._hydrated_product_page(response)
        hits = product_page.get("hits")
        if not isinstance(hits, list) or not hits:
            raise RuntimeError(f"No Bath & Body Works hydrated product hits found at {response.url}")

        for position, product in enumerate(hits, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("productId") or product.get("id") or "")
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            yield self._item(response, product, page_number, position)

        total = self._to_int(product_page.get("total")) or len(hits)
        offset = self._to_int(product_page.get("offset")) or len(hits)
        if page_number < self.max_pages and offset < total:
            yield response.follow(
                self._with_start(response.url, offset), callback=self.parse,
                meta={"category": response.meta.get("category"), "page": page_number + 1,
                      "allow_offsite": response.meta.get("allow_offsite", False)},
                headers=self._headers(), dont_filter=True,
            )

    def _item(self, response, product, page, position):
        availability = product.get("availability") or {}
        images = [
            image.get("disBaseLink") or image.get("link")
            for group in product.get("imageGroups") or [] if isinstance(group, dict)
            for image in group.get("images") or [] if isinstance(image, dict)
        ]
        sale_price = product.get("c_salePrice")
        price = sale_price if sale_price is not None else product.get("price")
        return {
            "category": response.meta.get("category"), "item_id": product.get("productId") or product.get("id"),
            "upc": product.get("upc"), "title": product.get("name"), "brand": product.get("brand") or "Bath & Body Works",
            "url": response.urljoin(product.get("slugUrl") or ""), "image_url": images[0] if images else None,
            "price": self._to_float(price), "regular_price": self._to_float(product.get("c_listPrice") or product.get("price")),
            "currency": product.get("currency"), "availability": "InStock" if availability.get("webOrderable") else "OutOfStock",
            "rating": self._to_float(product.get("c_bvAverageRating")), "reviews_count": self._to_int(product.get("c_bvReviewCount")),
            "product_type": product.get("c_productType") or product.get("c_form"), "fragrance": product.get("c_fragranceName"),
            "size": product.get("c_size"), "color": product.get("c_color"), "position": position,
            "source": "bathandbodyworks_mobify_react_query", "category_url": response.url, "page": page, "raw": product,
        }

    @staticmethod
    def _hydrated_product_page(response):
        text = response.css("script#mobify-data::text").get()
        if not text:
            raise RuntimeError(f"No Bath & Body Works mobify-data hydration found at {response.url}")
        try:
            state = json.loads(text)["__PRELOADED_STATE__"]["__reactQuery"]["queries"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Invalid Bath & Body Works mobify-data hydration at {response.url}") from exc
        for query in state:
            key = query.get("queryKey") if isinstance(query, dict) else None
            if isinstance(key, list) and key and key[0] == "products":
                pages = query.get("state", {}).get("data", {}).get("pages")
                if isinstance(pages, list) and pages and isinstance(pages[0], dict):
                    return pages[0]
        raise RuntimeError(f"No Bath & Body Works products query found at {response.url}")

    @staticmethod
    def _with_start(url, start):
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["start"] = str(start)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _to_float(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_int(value):
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _headers():
        return {"accept": "text/html,application/xhtml+xml", "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
