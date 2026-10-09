from __future__ import annotations

"""L.L.Bean listing spider (issue #172).

L.L.Bean runs a custom React/Redux SSR storefront. The critical detail: **the PLP
HTML contains no products**. The server-rendered blob

    window.__INITIAL_STATE__.searchResultsReducer.searchResults.fusion.metaData

carries only the page descriptor (`pageSize`, `pageNumber`, `categoryId`); its
`docs` array is empty. Products are hydrated client side by one first-party JSON
endpoint behind the UDAL service gateway:

    GET /api/udal/product-discovery/search
        ?categoryId=<id>&pageSize=48&start=<offset>

So this spider uses exactly one data direction -- that JSON endpoint. No PLP HTML
scraping, no sitemap taxonomy, no rendered-browser fallback. If the endpoint
stops answering, the spider fails loudly instead of silently exporting zero rows.

Two further details worth keeping:

* `start` is the only offset parameter the endpoint honours. `pageOffset` /
  `pageNumber` are accepted and silently ignored (page 2 returns page 1), so
  pagination must advance `start` by `pageSize`.
* `docs` are one row per **SKU**, not per product -- the same `itemID_s` /
  `pageID_s` recurs with different `skuID_s` / sizes, so items are de-duplicated
  on `skuID_s`.
"""

import re
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider, group_categories
from common.spiders.llbean_categories import LLBEAN_CATEGORIES

API_URL = "https://www.llbean.com/api/udal/product-discovery/search"
IMAGE_URL = "https://cdni.llbean.net/is/image/wim/{image}?wid=302&hei=352"
PRODUCT_URL = "https://www.llbean.com/llb/shop/{page_id}?page={slug}"
PAGE_SIZE = 48

# category URL -> id, e.g. /llb/shop/509870 -> 509870
_CATEGORY_ID_RE = re.compile(r"/llb/shop/(\d+)")


def category_id_from_url(url: str) -> str | None:
    """Pull the UDAL `categoryId` out of a `/llb/shop/<id>` category URL."""
    match = _CATEGORY_ID_RE.search(url or "")
    return match.group(1) if match else None


class LlbeanListingSpider(BaseListingSpider):
    """L.L.Bean listings from the UDAL product-discovery API."""

    name = "llbean_listing"
    allowed_domains = ["llbean.com", "www.llbean.com", "localhost", "127.0.0.1"]
    categories = group_categories(LLBEAN_CATEGORIES, "department")

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "sku_id", "title", "brand",
            "url", "image_url", "price", "original_price", "currency",
            "rating", "reviews_count", "color", "size", "availability",
            "on_sale", "page", "position", "total_count", "source_url",
            "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_skus: set[str] = set()

    def start_requests(self):
        self._seen_skus.clear()
        target = self.resolve_target_url()
        category_id = category_id_from_url(target)
        if not category_id:
            raise ValueError(
                f"Cannot read a category id from '{target}'. Expected a "
                "https://www.llbean.com/llb/shop/<categoryId> URL."
            )
        selected = next((entry for entry in self.iter_categories() if entry["url"] == target), {})
        yield self._api_request(
            category_id,
            start=0,
            page=1,
            category=selected.get("category") or self.category or "custom",
            department=selected.get("department"),
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(
                f"L.L.Bean product-discovery returned HTTP {response.status}: {response.url}"
            )
        payload = response.json()
        body = payload.get("response")
        if not isinstance(body, dict) or not isinstance(body.get("docs"), list):
            raise RuntimeError(
                f"L.L.Bean product-discovery response has no response.docs list at {response.url}"
            )

        docs = [doc for doc in body["docs"] if isinstance(doc, dict)]
        total_count = self._integer(body.get("numFound"))
        page = int(response.meta.get("page", 1))
        offset = self._integer(body.get("start")) or 0

        for position, doc in enumerate(docs, start=1):
            sku_id = self._first_str(doc, "skuID_s", "id")
            if not sku_id or sku_id in self._seen_skus:
                continue
            self._seen_skus.add(sku_id)
            yield self._item(
                doc,
                response,
                category=response.meta.get("category"),
                department=response.meta.get("department"),
                sku_id=sku_id,
                page=page,
                position=position,
                total_count=total_count,
            )

        if not docs or page >= self.max_pages:
            return
        next_start = offset + len(docs)
        if total_count is not None and next_start >= total_count:
            return
        yield self._api_request(
            response.meta["category_id"],
            start=next_start,
            page=page + 1,
            category=response.meta.get("category"),
            department=response.meta.get("department"),
        )

    def _api_request(
        self,
        category_id: str,
        *,
        start: int,
        page: int,
        category: str | None,
        department: str | None,
    ) -> scrapy.Request:
        query = urlencode(
            {"categoryId": category_id, "pageSize": PAGE_SIZE, "start": start}
        )
        return scrapy.Request(
            f"{API_URL}?{query}",
            callback=self.parse,
            headers={
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9",
                "user-agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
                ),
            },
            meta={
                "category_id": category_id,
                "category": category,
                "department": department,
                "page": page,
            },
        )

    def _item(
        self,
        doc: dict,
        response: scrapy.http.Response,
        *,
        category: str | None,
        department: str | None,
        sku_id: str,
        page: int,
        position: int,
        total_count: int | None,
    ) -> dict:
        full_price = self._money(doc.get("minFullPrice_f"))
        sale_price = self._money(doc.get("minSalePrice_f"))
        on_sale = bool(doc.get("page_onlySaleSKUs_b")) or (
            sale_price is not None and full_price is not None and sale_price < full_price
        )
        price = sale_price if sale_price is not None else full_price
        original_price = full_price if on_sale and full_price != price else None

        page_id = self._first_str(doc, "pageID_s")
        slug = self._first_str(doc, "page_pageParamValue_s")
        product_url = None
        if page_id:
            product_url = PRODUCT_URL.format(page_id=page_id, slug=slug or "")

        image = self._first_str(doc, "thumbnailImage")

        return {
            "category": category,
            "department": department,
            "item_id": sku_id,
            "sku_id": sku_id,
            "title": self._first_str(doc, "page_productName_default_s", "page_name_s"),
            "brand": "L.L.Bean",
            "url": product_url,
            "image_url": IMAGE_URL.format(image=image) if image else None,
            "price": price,
            "original_price": original_price,
            "currency": "USD" if price is not None else None,
            "rating": self._number(doc.get("page_reviews_averageRating_f")),
            "reviews_count": self._integer(doc.get("page_reviews_reviewsCount_i")),
            "color": self._first_str(doc, "item_defaultColor_s"),
            "size": self._first_str(doc, "sku_size_longDescription_s"),
            "availability": self._first_str(doc, "sku_stockStatus_s"),
            "on_sale": on_sale,
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "llbean_udal_product_discovery",
            "raw": doc,
        }

    @staticmethod
    def _first_str(doc: dict, *keys) -> str | None:
        for key in keys:
            value = doc.get(key)
            if value not in (None, "") and not isinstance(value, (dict, list)):
                return str(value)
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

    @staticmethod
    def _money(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None
