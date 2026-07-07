from __future__ import annotations

import json
from urllib.parse import urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SephoraListingSpider(BaseListingSpider):
    name = "sephora_listing"
    allowed_domains = ["sephora.com", "www.sephora.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category",
            "productId",
            "skuId",
            "title",
            "url",
            "price",
            "salePrice",
            "valuePrice",
            "brand",
            "rating",
            "reviewsCount",
            "imageUrl",
            "altImageUrl",
            "imageAltText",
            "biExclusiveLevel",
            "isAppExclusive",
            "isBI",
            "isBestseller",
            "isLimitedEdition",
            "isLimitedTimeOffer",
            "isNew",
            "isOnlineOnly",
            "isSephoraExclusive",
            "moreColors",
            "swatchType",
            "swatchCount",
            "swatchSkuIds",
            "swatchSelectors",
            "onSaleData",
            "pickupEligible",
            "sameDayEligible",
            "shipToHomeEligible",
            "sponsored",
            "page",
            "rawProduct",
            "timestamp",
        ],
    }

    categories = [
        {
            "category": "makeup",
            "url": "https://www.sephora.com/shop/makeup-cosmetics",
            "slug": "makeup-cosmetics",
        },
        {
            "category": "skincare",
            "url": "https://www.sephora.com/shop/skincare",
            "slug": "skincare",
        },
        {
            "category": "gifts",
            "url": "https://www.sephora.com/shop/gifts",
            "slug": "gifts",
        },
        {
            "category": "fragrance",
            "url": "https://www.sephora.com/shop/fragrance",
            "slug": "fragrance",
        },
    ]

    def start_requests(self):
        page = 1
        api = self._build_api_url(page)
        yield scrapy.Request(
            api, callback=self.parse, headers=self._headers(), meta={"page": page}
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        data = self._to_json(response)
        if not isinstance(data, dict):
            self.logger.warning(
                "Sephora listing non-JSON/blocked response status=%s", response.status
            )
            return

        products = data.get("products") or []

        for p in products:
            url = p.get("targetUrl") or p.get("url")
            if isinstance(url, str) and url.startswith("/"):
                url = f"https://www.sephora.com{url}"

            image = self._extract_image_url(p.get("heroImage") or p.get("image"))
            alt_image = self._extract_image_url(p.get("altImage"))

            current_sku = p.get("currentSku") or {}
            sku_or_product = lambda field: current_sku.get(field, p.get(field))
            swatch_selectors = p.get("swatchSelectors") or []
            swatch_sku_ids = [
                swatch.get("skuId")
                for swatch in swatch_selectors
                if isinstance(swatch, dict) and swatch.get("skuId")
            ]

            yield {
                "category": self._current_category_name(),
                "productId": p.get("productId"),
                "skuId": current_sku.get("skuId"),
                "title": p.get("displayName") or p.get("productName"),
                "url": url,
                "price": self._to_float(current_sku.get("listPrice")),
                "salePrice": self._to_float(current_sku.get("salePrice")),
                "valuePrice": self._to_float(current_sku.get("valuePrice")),
                "brand": p.get("brandName"),
                "rating": self._to_float(p.get("rating")),
                "reviewsCount": self._to_int(p.get("reviews")),
                "imageUrl": image,
                "altImageUrl": alt_image,
                "currentSku": current_sku,
                "imageAltText": current_sku.get("imageAltText"),
                "biExclusiveLevel": current_sku.get("biExclusiveLevel"),
                "isAppExclusive": current_sku.get("isAppExclusive"),
                "isBI": current_sku.get("isBI"),
                "isBestseller": current_sku.get("isBestseller"),
                "isLimitedEdition": current_sku.get("isLimitedEdition"),
                "isLimitedTimeOffer": current_sku.get("isLimitedTimeOffer"),
                "isNew": current_sku.get("isNew"),
                "isOnlineOnly": current_sku.get("isOnlineOnly"),
                "isSephoraExclusive": current_sku.get("isSephoraExclusive"),
                "moreColors": self._to_int(p.get("moreColors")),
                "swatchType": p.get("swatchType"),
                "swatchCount": len(swatch_selectors),
                "swatchSkuIds": swatch_sku_ids,
                "swatchSelectors": json.dumps(swatch_selectors),
                "onSaleData": p.get("onSaleData"),
                "pickupEligible": p.get("pickupEligible"),
                "sameDayEligible": p.get("sameDayEligible"),
                "shipToHomeEligible": p.get("shipToHomeEligible"),
                "sponsored": p.get("sponsored"),
                "page": page,
                "rawProduct": json.dumps(p),
                "timestamp": self.get_timestamp(),
            }

        if page >= self.max_pages or not products:
            return

        next_page = page + 1
        yield scrapy.Request(
            self._build_api_url(next_page),
            callback=self.parse,
            headers=self._headers(),
            meta={"page": next_page},
        )

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

    def _current_category_name(self) -> str | None:
        if self.category:
            return self.category

        u = self.url or self.category_url or ""
        for c in self.categories:
            if c.get("url") == u:
                return c.get("category")
        return None

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
    def _extract_image_url(value):
        if isinstance(value, dict):
            return value.get("src") or value.get("url")
        return value

    @staticmethod
    def _to_float(v):
        try:
            v = v.replace("$", "").strip()
            return float(v)
        except Exception:
            return None

    @staticmethod
    def _to_int(v):
        try:
            return int(str(v).replace(",", ""))
        except Exception:
            return None
