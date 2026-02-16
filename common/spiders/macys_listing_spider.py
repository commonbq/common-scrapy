from __future__ import annotations

import json
import re
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class MacysListingSpider(BaseListingSpider):
    require_category_arg = False
    """
    Macy's listing spider using Macy's own listing API endpoint:
      /xapi/discover/v1/page

    Direct calls from this host are blocked by Akamai, so this spider routes the
    exact Macy's API URL through r.jina.ai for retrieval, then parses the JSON.
    """

    name = "macys_listing"
    allowed_domains = ["r.jina.ai", "macys.com", "www.macys.com"]

    def __init__(
        self,
        q: str | None = None,
        sort: str | None = None,
        max_pages: int = 1,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.init_listing_args(max_pages=max_pages, q=q)

        self.q = (q or "laptop").strip()
        self.sort = (sort or "PRICE_LOW_TO_HIGH").strip()
        self.max_pages = self.args.max_pages

    def start_requests(self):
        page_index = 1
        api_url = self._build_macys_api_url(page_index)
        yield scrapy.Request(
            self._to_jina_url(api_url),
            callback=self.parse,
            meta={"page_index": page_index, "api_url": api_url},
        )

    def parse(self, response: scrapy.http.Response):
        payload = self._extract_json_payload(response.text)
        if not payload:
            self.logger.warning("Unable to extract Macy's JSON payload")
            return

        items = self._extract_products(payload)
        for item in items:
            yield item

        current_page = int(response.meta.get("page_index", 1))
        if current_page >= self.max_pages:
            return

        if not items:
            return

        next_page = current_page + 1
        next_api = self._build_macys_api_url(next_page)
        yield scrapy.Request(
            self._to_jina_url(next_api),
            callback=self.parse,
            meta={"page_index": next_page, "api_url": next_api},
        )

    def _build_macys_api_url(self, page_index: int) -> str:
        pathname = f"/shop/featured/{self.q.replace(' ', '%20')}"
        params = {
            "pathname": pathname,
            "_navigationType": "SEARCH",
            "_shoppingMode": "SITE",
            "sortBy": self.sort,
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

    def _to_jina_url(self, url: str) -> str:
        return f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"

    def _extract_json_payload(self, text: str) -> dict | None:
        start = text.find('{"meta"')
        if start == -1:
            return None

        candidate = text[start:]
        end = candidate.rfind("}")
        if end == -1:
            return None

        raw_json = candidate[: end + 1]
        try:
            return json.loads(raw_json)
        except json.JSONDecodeError:
            return None

    def _extract_products(self, payload: dict) -> list[dict]:
        try:
            collection = payload["body"]["canvas"]["rows"][0]["rowSortableGrid"]["zones"][1]["sortableGrid"]["collection"]
        except Exception:
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
