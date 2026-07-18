from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urljoin, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class JCPenneyListingSpider(BaseListingSpider):
    """JCPenney listing spider via search-api bootstrap JSON."""

    name = "jcpenney_listing"
    allowed_domains = ["search-api.jcpenney.com", "www.jcpenney.com", "jcpenney.com"]

    categories = [
        {"category": "womens_tops", "url": "https://www.jcpenney.com/g/women/tops?id=cat100210006"},
        {"category": "mens_shirts", "url": "https://www.jcpenney.com/g/men/mens-shirts?id=cat100240025"},
    ]

    def start_requests(self):
        target_url = self.resolve_target_url()
        api_url = self._build_api_url(target_url=target_url, page=1)
        yield scrapy.Request(
            api_url,
            callback=self.parse,
            headers=self._api_headers(target_url),
            meta={"target_url": target_url, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        data = response.json() if response.text else {}
        products = ((data or {}).get("organicZoneInfo") or {}).get("products") or []

        for product in products:
            pp_id = product.get("ppId")
            pdp = product.get("pdpUrl")
            item_url = urljoin("https://www.jcpenney.com", pdp) if isinstance(pdp, str) else None

            current_min = self._to_float(product.get("currentMin"))
            current_max = self._to_float(product.get("currentMax"))
            original_min = self._to_float(product.get("originalMin"))
            original_max = self._to_float(product.get("originalMax"))

            yield {
                "item_id": pp_id,
                "title": product.get("name"),
                "brand": product.get("brand") or product.get("brandName"),
                "url": item_url,
                "image_url": self._first_image(product),
                "price": current_min,
                "price_max": current_max,
                "original_price": original_min,
                "original_price_max": original_max,
                "rating": self._to_float(product.get("averageRating")),
                "reviews_count": self._to_int(product.get("reviewCount")),
                "source": "jcpenney_search_api_v1",
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages or not products:
            return

        target_url = response.meta["target_url"]
        next_page = current_page + 1
        next_url = self._build_api_url(target_url=target_url, page=next_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse,
            headers=self._api_headers(target_url),
            meta={"target_url": target_url, "page": next_page},
        )

    def _build_api_url(self, *, target_url: str, page: int) -> str:
        parsed = urlparse(target_url)
        path = parsed.path
        params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        params.setdefault("productGridView", "medium")
        params.setdefault("responseType", "organic")
        params.setdefault("geoZip", getattr(self, "geo_zip", None) or "98188")
        params["page"] = str(page)
        return f"https://search-api.jcpenney.com/v1/search-service{path}?{urlencode(params)}"

    def _api_headers(self, target_url: str) -> dict[str, str]:
        return {
            "accept": "application/json, text/plain, */*",
            "referer": target_url,
            "origin": "https://www.jcpenney.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
        }

    def _first_image(self, product: dict) -> str | None:
        swatches = product.get("skuSwatch") or []
        if not swatches or not isinstance(swatches, list):
            return None
        first = swatches[0] or {}
        if not isinstance(first, dict):
            return None

        image_id = first.get("colorizedImageId") or first.get("swatchImageId")
        if isinstance(image_id, str) and image_id:
            return f"https://jcpenney.scene7.com/is/image/JCPenney/{image_id}?wid=300&hei=300&op_sharpen=1"
        return None

    def _to_float(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None

    def _to_int(self, value):
        if value is None:
            return None
        try:
            return int(value)
        except Exception:
            return None
