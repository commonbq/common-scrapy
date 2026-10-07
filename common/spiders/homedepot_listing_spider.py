from __future__ import annotations

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.homedepot_search_spider import HomeDepotSearchSpider


class HomeDepotListingSpider(BaseListingSpider):
    """Extract category products from Home Depot's embedded Apollo state."""

    name = "homedepot_listing"
    allowed_domains = ["homedepot.com", "www.homedepot.com", "127.0.0.1"]

    # Department landing pages whose PLPs expose products in __APOLLO_STATE__.
    categories = [
        {"category": "appliances", "url": "https://www.homedepot.com/b/Appliances/N-5yc1vZbv1w"},
        {"category": "bath", "url": "https://www.homedepot.com/b/Bath/N-5yc1vZbzb3"},
        {"category": "building-materials", "url": "https://www.homedepot.com/b/Building-Materials/N-5yc1vZaqns"},
        {"category": "decor-and-furniture", "url": "https://www.homedepot.com/b/Home-Decor-Furniture/N-5yc1vZas6p"},
        {"category": "electrical", "url": "https://www.homedepot.com/b/Electrical/N-5yc1vZarcd"},
        {"category": "flooring", "url": "https://www.homedepot.com/b/Flooring/N-5yc1vZaq7r"},
        {"category": "hardware", "url": "https://www.homedepot.com/b/Hardware/N-5yc1vZc21m"},
        {"category": "heating-and-cooling", "url": "https://www.homedepot.com/b/Heating-Venting-Cooling/N-5yc1vZc4k8"},
        {"category": "kitchen", "url": "https://www.homedepot.com/b/Kitchen/N-5yc1vZar4i"},
        {"category": "lawn-and-garden", "url": "https://www.homedepot.com/b/Outdoors-Garden-Center/N-5yc1vZbx6k"},
        {"category": "lighting", "url": "https://www.homedepot.com/b/Lighting/N-5yc1vZbvn5"},
        {"category": "paint", "url": "https://www.homedepot.com/b/Paint/N-5yc1vZar2d"},
        {"category": "plumbing", "url": "https://www.homedepot.com/b/Plumbing/N-5yc1vZbqew"},
        {"category": "storage", "url": "https://www.homedepot.com/b/Storage-Organization/N-5yc1vZas7e"},
        {"category": "tools", "url": "https://www.homedepot.com/b/Tools/N-5yc1vZc1xy"},
    ]

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "sku", "title", "brand", "model", "url",
            "image_url", "price", "original_price", "currency", "rating",
            "reviews_count", "availability", "source", "category_url", "page",
            "timestamp",
        ],
        "HTTPERROR_ALLOW_ALL": True,
    }

    def start_requests(self):
        url = self.url or self._page_url(1)
        yield scrapy.Request(url, callback=self.parse, meta={"category": self.category, "page": 1})

    def parse(self, response: scrapy.http.Response):
        state = HomeDepotSearchSpider._extract_js_object(response.text, "__APOLLO_STATE__")
        if not state:
            raise RuntimeError(f"Home Depot PLP did not contain __APOLLO_STATE__ at {response.url}")

        search_model = next(
            (value for value in state.values() if isinstance(value, dict) and value.get("__typename") == "SearchModel"),
            None,
        )
        product_key = next(
            (key for key in (search_model or {}) if isinstance(key, str) and key.startswith("products(")),
            None,
        )
        refs = (search_model or {}).get(product_key) if product_key else None
        if not isinstance(refs, list) or not refs:
            raise RuntimeError(f"No Home Depot Apollo products found at {response.url}")

        category = response.meta.get("category")
        page = int(response.meta.get("page", 1))
        seen = set()
        for ref in refs:
            product = state.get(ref.get("__ref"), {}) if isinstance(ref, dict) else {}
            identifiers = product.get("identifiers") or {}
            item_id = identifiers.get("itemId") or product.get("itemId")
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            pricing = next(
                (product[key] for key in product if isinstance(key, str) and key.startswith("pricing(") and isinstance(product[key], dict)),
                {},
            )
            image = ((product.get("media") or {}).get("images") or [{}])[0] or {}
            reviews = ((product.get("reviews") or {}).get("ratingsReviews") or {})
            canonical = identifiers.get("canonicalUrl")
            yield {
                "category": category,
                "item_id": item_id,
                "sku": identifiers.get("storeSkuNumber"),
                "title": identifiers.get("productLabel"),
                "brand": identifiers.get("brandName"),
                "model": identifiers.get("modelNumber"),
                "url": f"https://www.homedepot.com{canonical}" if canonical and canonical.startswith("/") else canonical,
                "image_url": (image.get("url") or "").replace("<SIZE>", "300") or None,
                "price": self._number(pricing.get("value")),
                "original_price": self._number(pricing.get("original")),
                "currency": pricing.get("currency") or "USD",
                "rating": self._number(reviews.get("averageRating")),
                "reviews_count": self._integer(reviews.get("totalReviews")),
                "availability": product.get("availabilityType") or product.get("availabilityStatus"),
                "source": "homedepot_apollo_state",
                "category_url": self._category_entry()["url"],
                "page": page,
            }

        if page < self.max_pages and not self.url:
            next_page = page + 1
            yield scrapy.Request(self._page_url(next_page), callback=self.parse, meta={"category": category, "page": next_page})

    def _category_entry(self):
        return next(entry for entry in self.categories if entry["category"] == self.category)

    def _page_url(self, page: int) -> str:
        base = self._category_entry()["url"]
        return base if page == 1 else f"{base}?Nao={(page - 1) * 24}"

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
