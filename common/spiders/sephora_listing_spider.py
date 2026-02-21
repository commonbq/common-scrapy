from __future__ import annotations

import json
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SephoraListingSpider(BaseListingSpider):
    name = "sephora_listing"
    allowed_domains = ["sephora.com", "www.sephora.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {"category": "makeup", "url": "https://www.sephora.com/shop/makeup-cosmetics", "slug": "makeup-cosmetics"},
        {"category": "skincare", "url": "https://www.sephora.com/shop/skincare", "slug": "skincare"},
        {"category": "gifts", "url": "https://www.sephora.com/shop/gifts", "slug": "gifts"},
        {"category": "fragrance", "url": "https://www.sephora.com/shop/fragrance", "slug": "fragrance"},
    ]

    def start_requests(self):
        page = 1
        api = self._build_api_url(page)
        yield scrapy.Request(api, callback=self.parse, headers=self._headers(), meta={"page": page})

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        data = self._to_json(response)
        if not isinstance(data, dict):
            self.logger.warning("Sephora listing non-JSON/blocked response status=%s", response.status)
            return

        products = data.get("products") or []
        for p in products:
            url = p.get("targetUrl") or p.get("url")
            if isinstance(url, str) and url.startswith("/"):
                url = f"https://www.sephora.com{url}"
            image = p.get("heroImage") or p.get("image")
            if isinstance(image, dict):
                image = image.get("src") or image.get("url")
            yield {
                "item_id": p.get("productId") or p.get("skuId"),
                "title": p.get("displayName") or p.get("productName"),
                "url": url,
                "price": self._to_float(p.get("currentSku") and (p.get("currentSku") or {}).get("listPrice")) or self._to_float(p.get("currentSku") and (p.get("currentSku") or {}).get("salePrice")),
                "currency": "USD",
                "brand": p.get("brandName"),
                "rating": self._to_float(p.get("rating")),
                "reviews_count": self._to_int(p.get("reviews")),
                "image_url": image,
                "source": "sephora_catalog_api",
                "mode": "category",
                "category_url": self.category_url or self.url,
                "page": page,
            }

        if page >= self.max_pages or not products:
            return

        next_page = page + 1
        yield scrapy.Request(self._build_api_url(next_page), callback=self.parse, headers=self._headers(), meta={"page": next_page})

    def _build_api_url(self, page: int) -> str:
        slug = self._resolve_slug()
        params = {
            "targetSearchEngine": "NLP",
            "currentPage": page,
            "pageSize": 60,
            "content": "true",
            "includeRegionsMap": "true",
            "pickupRampup": "true",
            "pickupStoreId": "0018",
            "sddRampup": "true",
            "sddZipcode": "95050-6730",
            "includeEDD": "true",
            "loc": "en-US",
            "ch": "rwd",
        }
        return f"https://www.sephora.com/api/v2/catalog/categories/{slug}/seo?{urlencode(params)}"

    def _resolve_slug(self) -> str:
        if self.category:
            for c in self.categories:
                if c.get("category") == self.category:
                    return c.get("slug")
        u = self.url or self.category_url or ""
        for c in self.categories:
            if c.get("url") == u:
                return c.get("slug")
        raise ValueError("Provide -a category=<name> for sephora_listing")

    def _headers(self) -> dict:
        return {
            "accept": "application/json",
            "x-api-key": "nQc7BFt78yJBvfYDKtle9APd5RrX984i",
            "x-requested-source": "rwd",
            "user-agent": "Mozilla/5.0",
            "referer": self.category_url or self.url or "https://www.sephora.com/",
        }

    @staticmethod
    def _to_json(response: scrapy.http.Response):
        try:
            return json.loads(response.text)
        except Exception:
            return None

    @staticmethod
    def _to_float(v):
        try:
            return float(v)
        except Exception:
            return None

    @staticmethod
    def _to_int(v):
        try:
            return int(str(v).replace(",", ""))
        except Exception:
            return None
