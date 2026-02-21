from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class KohlsListingSpider(BaseListingSpider):
    name = "kohls_listing"
    allowed_domains = ["kohls.com", "www.kohls.com"]

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    categories = [
        {
            "category": "women",
            "url": "https://www.kohls.com/catalog/womens-clothing.jsp",
            "cn": "Gender:Womens+Department:Clothing",
        },
        {
            "category": "men",
            "url": "https://www.kohls.com/catalog/mens-clothing.jsp",
            "cn": "Gender:Mens+Department:Clothing",
        },
        {
            "category": "sale",
            "url": "https://www.kohls.com/catalog/sale.jsp",
            "cn": "Promotions:Clearance+Promotions:Sale",
        },
    ]

    def start_requests(self):
        page = 1
        api_url = self._build_api_url(page=page)
        yield scrapy.Request(api_url, callback=self.parse, headers=self._headers(), meta={"page": page})

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        payload = self._to_json(response)
        if not isinstance(payload, dict):
            self.logger.warning("Kohls listing non-JSON/blocked response status=%s", response.status)
            return

        products = ((payload.get("payload") or {}).get("products") or [])
        for p in products:
            prices = (p.get("prices") or [{}])[0]
            reg = ((prices.get("regularPrice") or {}).get("minPrice"))
            sale = ((prices.get("salePrice") or {}).get("minPrice"))
            image = p.get("imageUrl") or p.get("imageURL")
            url = p.get("productDetailsUrl") or p.get("url")
            if isinstance(url, str) and url.startswith("/"):
                url = f"https://www.kohls.com{url}"
            yield {
                "item_id": p.get("productId") or p.get("id"),
                "title": p.get("productTitle") or p.get("title"),
                "url": url,
                "price": sale or reg,
                "regular_price": reg,
                "sale_price": sale,
                "currency": "USD" if (sale or reg) is not None else None,
                "brand": p.get("brand") or p.get("brandName"),
                "rating": p.get("averageRating"),
                "reviews_count": p.get("reviews"),
                "image_url": image,
                "source": "kohls_web_catalog_api",
                "mode": "category",
                "category_url": self.category_url or self.url,
                "page": page,
            }

        if page >= self.max_pages or not products:
            return

        next_page = page + 1
        next_url = self._build_api_url(page=next_page)
        yield scrapy.Request(next_url, callback=self.parse, headers=self._headers(), meta={"page": next_page})

    def _build_api_url(self, page: int) -> str:
        cn = self._resolve_cn()
        limit = 120
        offset = (page - 1) * limit
        params = {
            "limit": limit,
            "offset": offset,
            "storeNum": 977,
            "isDefaultStore": "true",
            "includeStoreOnlyProducts": "true",
            "isLTL": "true",
            "channel": "web",
        }
        return f"https://www.kohls.com/web/catalog/{cn}?{urlencode(params)}"

    def _resolve_cn(self) -> str:
        if self.category:
            for c in self.categories:
                if c.get("category") == self.category:
                    return c.get("cn")
        # best effort from explicit URL fallback
        u = self.url or self.category_url or ""
        parsed = urlparse(u)
        qs = parse_qs(parsed.query)
        cn = qs.get("CN", [None])[0]
        if cn:
            return cn
        raise ValueError("Provide -a category=<name> for kohls_listing")

    def _headers(self) -> dict:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "channel": "web",
            "user-agent": "Mozilla/5.0",
            "referer": self.category_url or self.url or "https://www.kohls.com/",
        }

    def _to_json(self, response: scrapy.http.Response):
        try:
            return json.loads(response.text)
        except Exception:
            return None
