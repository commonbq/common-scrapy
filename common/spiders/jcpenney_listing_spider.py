from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urljoin, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class JCPenneyListingSpider(BaseListingSpider):
    """Extract JCPenney listings from the search-service JSON response."""

    name = "jcpenney_listing"
    allowed_domains = ["search-api.jcpenney.com", "www.jcpenney.com", "jcpenney.com", "127.0.0.1"]

    categories = [
        {"category": "women", "url": "https://www.jcpenney.com/g/women?id=dept20000013"},
        {"category": "womens_tops", "url": "https://www.jcpenney.com/g/women/tops?id=cat100210006"},
        {"category": "men", "url": "https://www.jcpenney.com/g/men?id=dept20000014"},
        {"category": "mens_shirts", "url": "https://www.jcpenney.com/g/men/mens-shirts?id=cat100240025"},
        {"category": "kids", "url": "https://www.jcpenney.com/g/kids?id=dept20000016"},
        {"category": "shoes", "url": "https://www.jcpenney.com/g/shoes?id=dept20000018"},
        {"category": "handbags", "url": "https://www.jcpenney.com/g/handbags-accessories?id=dept20000019"},
        {"category": "jewelry", "url": "https://www.jcpenney.com/g/jewelry-and-watches?id=dept20000020"},
        {"category": "beauty", "url": "https://www.jcpenney.com/g/beauty?id=dept20024960026"},
        {"category": "home", "url": "https://www.jcpenney.com/g/home-store?id=dept20000011"},
    ]

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image_url",
            "price", "price_max", "original_price", "original_price_max",
            "currency", "rating", "reviews_count", "source", "category_url",
            "page", "raw",
        ]
    }

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield scrapy.Request(
            target_url if self.url else self._build_api_url(target_url=target_url, page=1),
            callback=self.parse,
            headers=self._api_headers(target_url),
            meta={"target_url": target_url, "category": self.category, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(f"No JCPenney search-service JSON found at {response.url}") from exc

        organic = (data or {}).get("organicZoneInfo") or {}
        products = organic.get("products") or []
        if not products:
            raise RuntimeError(f"No JCPenney organicZoneInfo products found at {response.url}")

        page = int(response.meta.get("page") or 1)
        category_url = response.meta.get("target_url") or self.resolve_target_url()
        seen = set()
        for product in products:
            if not isinstance(product, dict):
                continue
            item_id = product.get("ppId") or product.get("productId")
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            pdp = product.get("pdpUrl")
            yield {
                "category": response.meta.get("category") or self.category,
                "item_id": item_id,
                "title": product.get("name"),
                "brand": product.get("brand") or product.get("brandName"),
                "url": urljoin("https://www.jcpenney.com", pdp) if isinstance(pdp, str) else None,
                "image_url": self._first_image(product),
                "price": self._number(product.get("currentMin")),
                "price_max": self._number(product.get("currentMax")),
                "original_price": self._number(product.get("originalMin")),
                "original_price_max": self._number(product.get("originalMax")),
                "currency": product.get("currency") or "USD",
                "rating": self._number(product.get("averageRating")),
                "reviews_count": self._integer(product.get("reviewCount")),
                "source": "jcpenney_search_service_organic_zone",
                "category_url": category_url,
                "page": page,
                "raw": product,
            }

        if page >= self.max_pages or self.url:
            return
        total_pages = self._integer(organic.get("totalPages") or data.get("totalPages"))
        if total_pages is not None and page >= total_pages:
            return
        next_page = page + 1
        yield scrapy.Request(
            self._build_api_url(target_url=category_url, page=next_page),
            callback=self.parse,
            headers=self._api_headers(category_url),
            meta={"target_url": category_url, "category": response.meta.get("category"), "page": next_page},
        )

    @staticmethod
    def _build_api_url(*, target_url: str, page: int) -> str:
        parsed = urlparse(target_url)
        params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        params.setdefault("productGridView", "medium")
        params.setdefault("responseType", "organic")
        params.setdefault("geoZip", "98188")
        params["page"] = str(page)
        return f"https://search-api.jcpenney.com/v1/search-service{parsed.path}?{urlencode(params)}"

    @staticmethod
    def _api_headers(target_url: str) -> dict[str, str]:
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "origin": "https://www.jcpenney.com",
            "referer": target_url,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _first_image(product: dict) -> str | None:
        swatches = product.get("skuSwatch") or []
        first = swatches[0] if isinstance(swatches, list) and swatches else {}
        image_id = first.get("colorizedImageId") or first.get("swatchImageId") if isinstance(first, dict) else None
        if not image_id:
            return product.get("imageUrl")
        return f"https://jcpenney.scene7.com/is/image/JCPenney/{image_id}?wid=300&hei=300&op_sharpen=1"

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
