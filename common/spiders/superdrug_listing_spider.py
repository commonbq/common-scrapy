from __future__ import annotations

import json
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.superdrug_categories import SUPERDRUG_CATEGORIES


SOURCE = "superdrug_spartacus_bootstrap"


class SuperdrugListingSpider(BaseListingSpider):
    """Superdrug products from the Angular Spartacus transfer-state bootstrap."""

    name = "superdrug_listing"
    allowed_domains = ["superdrug.com", "www.superdrug.com", "localhost", "127.0.0.1"]
    categories = SUPERDRUG_CATEGORIES
    page_size = 8

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "base_product", "ean", "title", "brand",
            "url", "image_url", "price", "original_price", "currency",
            "unit_price", "discount_percent", "rating", "reviews_count",
            "availability", "age_restricted", "licensed_type",
            "marketplace_product", "new_in", "promotion_urls", "taxonomy_path",
            "page", "position", "page_size", "total_pages", "total_count",
            "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def resolve_target_url(self) -> str:
        if self.url:
            return self.url
        if self.category_url:
            return self.category_url
        if self.category in self.categories:
            return self.categories[self.category]
        available = ", ".join(self.available_categories())
        raise ValueError(f"Unknown category {self.category!r}. Available categories: {available}")

    def start_requests(self):
        target = self.resolve_target_url()
        yield scrapy.Request(
            self._page_url(target, 0),
            callback=self.parse,
            headers=self._headers(),
            meta={"category": self.category or "custom", "base_url": target, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        if response.status != 200:
            raise RuntimeError(f"Superdrug listing returned HTTP {response.status}: {response.url}")
        lowered = response.text[:10000].lower()
        if "access denied" in lowered or "reference #" in lowered:
            raise RuntimeError(f"Superdrug returned an access-denied page at {response.url}")

        model = self._listing_model(response)
        products = model.get("products")
        pagination = model.get("pagination")
        if not isinstance(products, list) or not isinstance(pagination, dict):
            raise RuntimeError(
                f"Superdrug bootstrap has no product list/pagination model at {response.url}"
            )
        if not products:
            if page > 1:
                return
            raise RuntimeError(f"Superdrug bootstrap returned no products at {response.url}")

        total_count = self._integer(pagination.get("totalResults"))
        total_pages = self._integer(pagination.get("totalPages"))
        page_size = self._integer(pagination.get("pageSize")) or self.page_size
        emitted = 0
        for position, product in enumerate(products, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("code") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(
                product, response, page, position, page_size, total_pages, total_count
            )

        current_page = self._integer(pagination.get("currentPage"))
        current_page = page - 1 if current_page is None else current_page
        if (
            emitted
            and page < self.max_pages
            and total_pages is not None
            and current_page + 1 < total_pages
        ):
            yield scrapy.Request(
                self._page_url(response.meta["base_url"], current_page + 1),
                callback=self.parse,
                headers=self._headers(),
                # HttpProxyMiddleware replaces ``proxy`` with a credential-free
                # URL after the first request.  Let the project middleware attach
                # fresh credentials instead of copying that mutated state.
                meta={
                    **{
                        key: value
                        for key, value in response.meta.items()
                        if key not in ("proxy", "_auth_proxy")
                    },
                    "page": page + 1,
                },
            )

    @staticmethod
    def _listing_model(response: scrapy.http.Response) -> dict:
        raw = response.css("script#spartacus-app-state::text").get()
        if not raw:
            raise RuntimeError(f"No Superdrug Spartacus app state at {response.url}")
        try:
            state = json.loads(raw)
        except (TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Invalid Superdrug Spartacus app state at {response.url}") from exc
        model = state.get("mp-product-list.model$") if isinstance(state, dict) else None
        if not isinstance(model, dict):
            raise RuntimeError(f"No mp-product-list model in Superdrug app state at {response.url}")
        return model

    def _item(self, product, response, page, position, page_size, total_pages, total_count):
        price = product.get("price") if isinstance(product.get("price"), dict) else {}
        brand = product.get("masterBrand")
        brand = brand.get("name") if isinstance(brand, dict) else brand
        stock = product.get("stock") if isinstance(product.get("stock"), dict) else {}
        images = product.get("images") if isinstance(product.get("images"), dict) else {}
        primary = images.get("PRIMARY") if isinstance(images.get("PRIMARY"), dict) else {}
        thumbnail = primary.get("thumbnail") if isinstance(primary.get("thumbnail"), dict) else {}
        promotions = product.get("promotions") if isinstance(product.get("promotions"), list) else []
        return {
            "category": response.meta["category"],
            "item_id": str(product.get("code")),
            "base_product": product.get("baseProduct"),
            "ean": product.get("ean"),
            "title": product.get("name"),
            "brand": brand,
            "url": urljoin("https://www.superdrug.com", product.get("url") or ""),
            "image_url": urljoin("https://media.superdrug.com", thumbnail.get("url") or ""),
            "price": self._number(price.get("value")),
            "original_price": self._number(price.get("oldValue")),
            "currency": price.get("currencyIso") or "GBP",
            "unit_price": product.get("contentUnitPrice"),
            "discount_percent": self._number(product.get("discountRoundel")),
            "rating": self._number(product.get("averageRating")),
            "reviews_count": self._integer(product.get("numberOfReviews")),
            "availability": stock.get("stockLevelStatus"),
            "age_restricted": bool(product.get("ageRestricted")),
            "licensed_type": product.get("licensedType"),
            "marketplace_product": bool(product.get("marketplaceProduct")),
            "new_in": bool(product.get("newIn")),
            "promotion_urls": [
                urljoin("https://www.superdrug.com", promotion["promotionUrl"])
                for promotion in promotions
                if isinstance(promotion, dict) and promotion.get("promotionUrl")
            ],
            "taxonomy_path": product.get("categoryNameHierarchy"),
            "page": page,
            "position": position,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_count": total_count,
            "source_url": response.url,
            "source": SOURCE,
            "raw": product,
            "timestamp": self.get_timestamp(),
        }

    def _page_url(self, url: str, current_page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query.update({"pageSize": str(self.page_size), "currentPage": str(current_page)})
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
        }

    @staticmethod
    def _integer(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None
