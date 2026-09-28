from __future__ import annotations

from urllib.parse import parse_qs, urlencode, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class GapListingSpider(BaseListingSpider):
    """Gap product listings from the public commerce search API."""

    name = "gap_listing"
    allowed_domains = ["gap.com", "www.gap.com", "api.gap.com"]

    GAP_CATEGORIES = {
        "women": {
            "dresses": "https://www.gap.com/browse/category.do?cid=13658",
            "new-arrivals": "https://www.gap.com/browse/category.do?cid=8792",
            "jeans": "https://www.gap.com/browse/category.do?cid=5664",
            "tops": "https://www.gap.com/browse/category.do?cid=17076",
            "pants": "https://www.gap.com/browse/category.do?cid=5736",
            "sweaters": "https://www.gap.com/browse/category.do?cid=5745",
        },
        "men": {
            "all": "https://www.gap.com/browse/category.do?cid=6998",
            "new-arrivals": "https://www.gap.com/browse/category.do?cid=1127938",
            "jeans": "https://www.gap.com/browse/category.do?cid=34524",
            "pants": "https://www.gap.com/browse/category.do?cid=34608",
        },
        "girls": {"all": "https://www.gap.com/browse/category.do?cid=14257"},
    }
    categories = GAP_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category",
            "subcategory",
            "item_id",
            "style_id",
            "title",
            "brand",
            "url",
            "image_url",
            "color",
            "price",
            "original_price",
            "currency",
            "availability",
            "rating",
            "reviews_count",
            "page",
            "source",
            "raw",
        ],
    }

    api_url = "https://api.gap.com/commerce/search/products/v2/cc"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def _selected_subcategories(self) -> dict[str, str]:
        try:
            return self.categories[self.category]
        except KeyError:
            available = ", ".join(self.available_categories())
            raise ValueError(
                f"Unknown category '{self.category}'. Available categories: {available}"
            ) from None

    @staticmethod
    def _cid(url: str) -> str:
        return (parse_qs(urlparse(url).query).get("cid") or [""])[0]

    def start_requests(self):
        self._seen_products.clear()
        selected = self._selected_subcategories()
        if self.url or self.category_url:
            selected = {"custom": self.resolve_target_url()}
        for subcategory, listing_url in selected.items():
            yield self._api_request(listing_url, subcategory, page=1)

    def _api_request(self, listing_url: str, subcategory: str, page: int):
        query = urlencode({"cid": self._cid(listing_url), "page": page - 1})
        return scrapy.Request(
            f"{self.api_url}?{query}",
            callback=self.parse_api,
            headers={
                "Accept": "application/json",
                "Origin": "https://www.gap.com",
                "Referer": listing_url,
            },
            meta={
                "page": page,
                "category": self.category,
                "subcategory": subcategory,
                "listing_url": listing_url,
            },
        )

    def parse_api(self, response: scrapy.http.Response):
        try:
            payload = response.json()
        except ValueError:
            self.logger.warning("Gap API returned invalid JSON (status=%s)", response.status)
            return
        page = int(response.meta["page"])
        for product in payload.get("products") or []:
            if not isinstance(product, dict):
                continue
            style_id = str(product.get("styleId") or "")
            colors = product.get("styleColors") or []
            color = colors[0] if colors and isinstance(colors[0], dict) else {}
            item_id = str(color.get("ccId") or style_id)
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            images = color.get("images") or []
            image = next((x.get("path") for x in images if x.get("type") == "P01"), None)
            price = self._float(color.get("effectivePrice"))
            original_price = self._float(color.get("regularPrice"))
            yield {
                "category": response.meta.get("category"),
                "subcategory": response.meta.get("subcategory"),
                "item_id": item_id,
                "style_id": style_id,
                "title": product.get("styleName"),
                "brand": "Gap",
                "url": f"https://www.gap.com/browse/product.do?pid={item_id}",
                "image_url": f"https://www.gap.com{image}" if image else None,
                "color": color.get("ccShortDescription") or color.get("ccName"),
                "price": price,
                "original_price": original_price,
                "currency": "USD" if price is not None else None,
                "availability": color.get("inventoryStatus"),
                "rating": self._float(product.get("reviewScore")),
                "reviews_count": product.get("reviewCount"),
                "page": page,
                "source": "gap_commerce_search_v2",
                "raw": product,
            }

        pagination = payload.get("pagination") or {}
        total_pages = int(pagination.get("pageNumberTotal") or 0)
        if page < min(self.max_pages, total_pages):
            yield self._api_request(
                response.meta["listing_url"], response.meta["subcategory"], page + 1
            )

    @staticmethod
    def _float(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None
