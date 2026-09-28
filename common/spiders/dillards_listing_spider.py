from __future__ import annotations

import json
import re
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit, parse_qsl

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


DILLARDS_CATEGORIES = {
    "women": ["/c/women-dresses", "/c/women-tops", "/c/women-pants", "/c/women-jeans", "/c/women-dressy-pants-sets", "/c/women-loungewear", "/c/women-skirts", "/c/women-activewear", "/c/women-sweaters", "/c/women-suits-suit-separates", "/c/women-coats-jackets-vests", "/c/women-jumpsuits-rompers", "/c/women-outdoor-wear", "/c/women-leggings", "/c/women-shorts", "/c/women-swimsuits-cover-ups", "/c/juniors", "/c/women-fan-shop"],
    "lingerie": ["/c/lingerie-bras", "/c/lingerie-pajamas-sleepwear", "/c/lingerie-panties", "/c/lingerie-robes", "/c/lingerie-intimate-lingerie", "/c/lingerie-shapewear", "/c/lingerie-slips", "/c/lingerie-patio-dresses", "/c/lingerie-rompers-bodysuits", "/c/lingerie-bridal"],
    "juniors": ["/c/juniors-dresses", "/c/juniors-tops", "/c/juniors-jeans", "/c/juniors-pants", "/c/juniors-skirts", "/c/juniors-loungewear", "/c/juniors-activewear", "/c/juniors-rompers-jumpsuits", "/c/juniors-hoodies-sweatshirts", "/c/juniors-sweaters", "/c/juniors-jackets-coats", "/c/juniors-leggings", "/c/juniors-shorts-capris", "/c/juniors-blazers-kimonos"],
    "shoes": ["/c/shoes-women-shoes", "/c/shoes-men-shoes", "/c/shoes-kids-shoes", "/c/shoes-shoe-accessories"],
    "handbags": ["/c/handbags-shoulder-bags", "/c/handbags-cross-body-bags", "/c/handbags-totes", "/c/handbags-wallets", "/c/handbags-clutches-evening-bags", "/c/handbags-satchels", "/c/handbags-hobo-bags", "/c/handbags-bucket-bags", "/c/handbags-small-cases", "/c/handbags-backpacks", "/c/handbags-belt-bags-fanny-packs", "/c/handbags-beach-bags", "/c/handbags-diaper-bags"],
    "accessories": ["/c/accessories-jewelry", "/c/accessories-scarves-wraps", "/c/accessories-watches", "/c/accessories-sunglasses-eyewear", "/c/accessories-belts", "/c/accessories-cold-weather-accessories", "/c/accessories-hats", "/c/accessories-hair-accessories", "/c/accessories-socks-footwear", "/c/accessories-tights-pantyhose", "/c/accessories-tech-accessories-cases", "/c/accessories-school-office"],
    "men": ["/c/men-shirts", "/c/men-jeans", "/c/men-pants", "/c/men-suits-and-suit-separates", "/c/men-sweaters", "/c/mens-hoodies-sweatshirts", "/c/men-coats-jackets", "/c/men-activewear", "/c/men-loungewear", "/c/men-fan-shop", "/c/men-pajamas-robes", "/c/men-golf", "/c/men-shorts", "/c/men-swimsuits", "/c/men-accessories", "/c/men-underwear-undershirts-socks", "/c/men-gifts"],
    "kids": ["/c/kids-girls", "/c/kids-boys", "/c/kids-baby-clothing-accessories", "/c/kids-baby-gear", "/c/kids-toys", "/c/kids-accessories"],
    "home": ["/c/home-holiday-shop", "/c/home-bedding", "/c/home-dining-entertaining", "/c/home-bath-personal-care", "/c/home-decor", "/c/home-kitchen", "/c/home-luggage", "/c/home-candles-home-fragrance", "/c/home-outdoor", "/c/home-accent-furniture", "/c/home-pets", "/c/home-vacuums-floor-care", "/c/home-irons-garment-steamers", "/c/home-entertainment", "/c/home-health-fitness", "/c/home-smart-home-devices", "/c/home-gourmet-food", "/c/home-gift-cards"],
    "beauty": ["/c/beauty-gifts-value-sets", "/c/beauty-fragrance", "/c/beauty-makeup", "/c/mens-grooming-products", "/c/beauty-skincare", "/c/beauty-travel", "/c/beauty-hair-care", "/c/beauty-bath-body", "/c/beauty-tools-of-the-trade", "/c/beauty-makeup-bags-cases", "/c/beauty-wellness", "/c/beauty-natural-beauty"],
}


class DillardsListingSpider(BaseListingSpider):
    """Extract Dillard's catalog entries from its authoritative bootstrap JSON."""

    name = "dillards_listing"
    allowed_domains = ["dillards.com", "www.dillards.com"]
    require_category_arg = False
    categories = DILLARDS_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "subcategory", "item_id", "part_number", "title", "brand",
            "url", "image_url", "price", "price_max", "currency", "rating",
            "reviews_count", "page", "source", "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.category:
            raise ValueError(f"Provide -a category=<name>. Available categories: {', '.join(self.available_categories())}")
        if not (self.url or self.category_url) and self.category not in self.categories:
            raise ValueError(f"Unknown category '{self.category}'. Available categories: {', '.join(self.available_categories())}")
        self._seen_ids: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def start_requests(self):
        if self.url or self.category_url:
            urls = [self.url or self.category_url]
        else:
            urls = [urljoin("https://www.dillards.com", path) for path in self.categories[self.category]]

        for url in urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers=self._headers(),
                meta={"category": self.category, "subcategory": urlsplit(url).path.removeprefix("/c/"), "page": 1},
            )

    def parse(self, response: scrapy.http.Response):
        state = self._extract_initial_state(response.text)
        if not state:
            self.logger.warning("Missing Dillard's bootstrap state: status=%s url=%s", response.status, response.url)
            return

        widget = self._catalog_widget(state)
        if not widget:
            self.logger.warning("No CatalogEntryList found for %s", response.url)
            return

        page = int(widget.get("currentPage") or response.meta.get("page") or 1)
        for product in widget.get("products") or []:
            item_id = str(product.get("catentryId") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            pricing = product.get("pricing") or {}
            slug = product.get("nameForURL")
            yield {
                "category": response.meta.get("category"),
                "subcategory": response.meta.get("subcategory"),
                "item_id": item_id,
                "part_number": product.get("partNumber"),
                "title": product.get("originalName") or product.get("name"),
                "brand": product.get("brand"),
                "url": urljoin("https://www.dillards.com", f"/p/{slug}/{item_id}") if slug else None,
                "image_url": self._image_url(product.get("fullImage")),
                "price": self._number(pricing.get("offerPriceMin")),
                "price_max": self._number(pricing.get("offerPriceMax")),
                "currency": "USD",
                "rating": self._number(product.get("numStars")),
                "reviews_count": self._integer(product.get("numReviews")),
                "page": page,
                "source": "dillards_bootstrap_initial_state",
                "raw": product,
            }

        total_pages = int(float(widget.get("totalPages") or 1))
        if page < min(total_pages, self.max_pages):
            yield response.follow(
                self._page_url(response.url, page + 1),
                callback=self.parse,
                headers=self._headers(),
                meta={**response.meta, "page": page + 1},
            )

    @staticmethod
    def _extract_initial_state(html: str) -> dict | None:
        match = re.search(r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*;\s*</script>", html, re.S | re.I)
        if not match:
            return None
        try:
            state = json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
        return state if isinstance(state, dict) else None

    @staticmethod
    def _catalog_widget(state: dict) -> dict | None:
        slots = (((state.get("contentData") or {}).get("layoutContent") or {}).get("slots") or {})
        for slot in slots.values():
            for widget in (slot or {}).get("widgets") or []:
                if widget.get("widgetType") == "CatalogEntryList" and isinstance(widget.get("products"), list):
                    return widget
        return None

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["pageNumber"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _image_url(image: str | None) -> str | None:
        if not image:
            return None
        return f"https://dimg.dillards.com/is/image/DillardsZoom/{image}?wid=600&hei=600&qlt=90"

    @staticmethod
    def _number(value):
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        }
