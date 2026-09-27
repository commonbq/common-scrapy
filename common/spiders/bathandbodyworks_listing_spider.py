from __future__ import annotations

import json
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


def _urls(parent: str, *slugs: str) -> dict[str, str]:
    return {
        slug: f"https://www.bathandbodyworks.com/c/{parent}/{slug}"
        for slug in slugs
    }


BATHANDBODYWORKS_CATEGORIES = {
    "body-care": _urls(
        "body-care",
        "all-fragrance", "perfume-cologne", "body-sprays-mists",
        "all-moisturizers", "body-cream", "body-lotion", "all-bath-shower",
        "body-wash-shower-gel", "body-scrub", "travel", "lip-gloss-balms",
        "wellness-body-care", "moisturizing-body-wash",
    ),
    "candles": _urls(
        "all-candles", "3-wick-candles", "4-wick-candles",
        "single-wick-candles", "candle-holders",
    ),
    "home-fragrance": _urls(
        "home-fragrance", "all-wallflowers", "wallflowers-refills",
        "wallflowers-plugs", "reeds", "room-sprays-mists", "car-fragrance",
        "wallflowers-create-your-set", "hanging-fragrance-diffusers",
    ),
    "hand-soaps-sanitizers": _urls(
        "hand-soaps-sanitizers", "all-hand-soaps", "foaming-hand-soap",
        "gel-hand-soaps", "moisturizing-hand-soaps", "revitalizing-hand-soaps",
        "hand-soap-refills", "hand-soap-holders", "all-hand-sanitizers",
        "pocketbac-hand-sanitizers", "hand-sanitizer-sprays",
        "pocketbac-sanitizer-holders",
    ),
    "men": {
        **_urls(
            "mens-shop", "mens-body-care", "mens-fragrance",
            "mens-shower-gel-body-wash", "mens-body-lotion-body-cream",
        ),
        **_urls("mens-collection", "mens-deodorant"),
    },
    "laundry-care": {
        **_urls("laundry-care", "all-laundry"),
        **_urls(
            "home-care/all-laundry", "laundry-detergent", "fragrance-boosters",
            "dryer-sheets",
        ),
    },
    "kitchen-care": _urls(
        "kitchen-care", "all-kitchen-care", "dish-wash", "counter-spray",
    ),
    "gifts": _urls(
        "gifts", "gifts-for-her", "gifts-for-him", "gift-sets",
        "gifts-under-20", "accessories", "boxes-bags",
    ),
}


class BathandbodyworksListingSpider(BaseListingSpider):
    """Bath & Body Works listings from category-page JSON-LD."""

    name = "bathandbodyworks_listing"
    allowed_domains = ["bathandbodyworks.com", "www.bathandbodyworks.com"]
    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}
    categories = BATHANDBODYWORKS_CATEGORIES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def _selected_subcategories(self) -> dict[str, str]:
        if self.category in self.categories:
            return self.categories[self.category]
        available = ", ".join(self.available_categories())
        raise ValueError(
            f"Unknown category '{self.category}'. Available categories: {available}"
        )

    def start_requests(self):
        self._seen_products.clear()
        for subcategory, listing_url in self._selected_subcategories().items():
            yield scrapy.Request(
                self._page_url(listing_url, 1),
                callback=self.parse,
                headers=self._headers(),
                meta={
                    "page": 1,
                    "category": self.category,
                    "subcategory": subcategory,
                    "listing_url": listing_url,
                },
            )

    def parse(self, response: scrapy.http.Response):
        if response.status >= 400 or self._blocked(response.text):
            self.logger.warning(
                "Bath & Body Works listing blocked (status=%s url=%s)",
                response.status,
                response.url,
            )
            return

        page = int(response.meta.get("page", 1))
        yielded = 0
        for product in self._extract_products(response):
            item_id = product["item_id"]
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yielded += 1
            yield {
                **product,
                "category": response.meta["category"],
                "subcategory": response.meta["subcategory"],
                "listing_url": response.meta["listing_url"],
                "page": page,
                "source": "bathandbodyworks_jsonld_itemlist",
                "mode": "category",
            }

        if yielded and page < self.max_pages:
            yield scrapy.Request(
                self._page_url(response.meta["listing_url"], page + 1),
                callback=self.parse,
                headers=self._headers(),
                meta={**response.meta, "page": page + 1},
            )

    @classmethod
    def _extract_products(cls, response: scrapy.http.Response):
        for raw in response.xpath('//script[@type="application/ld+json"]/text()').getall():
            try:
                payload = json.loads(raw)
            except (TypeError, ValueError):
                continue
            nodes = payload if isinstance(payload, list) else [payload]
            for node in nodes:
                if not isinstance(node, dict) or node.get("@type") != "ItemList":
                    continue
                for entry in node.get("itemListElement") or []:
                    item = entry.get("item") if isinstance(entry, dict) else None
                    if not isinstance(item, dict) or item.get("@type") != "Product":
                        continue
                    offers = item.get("offers") if isinstance(item.get("offers"), dict) else {}
                    specs = offers.get("priceSpecification") or []
                    list_price = next(
                        (cls._float(spec.get("price")) for spec in specs
                         if isinstance(spec, dict) and spec.get("priceType") == "https://schema.org/ListPrice"),
                        None,
                    )
                    url = entry.get("url") or item.get("url") or offers.get("url")
                    item_id = item.get("sku") or item.get("@id")
                    if not url or not item_id:
                        continue
                    image = item.get("image")
                    if isinstance(image, list):
                        image = image[0] if image else None
                    brand = item.get("brand")
                    yield {
                        "item_id": str(item_id),
                        "title": item.get("name"),
                        "url": urljoin(response.url, url),
                        "price": cls._float(offers.get("price")),
                        "original_price": list_price,
                        "currency": offers.get("priceCurrency"),
                        "brand": brand.get("name") if isinstance(brand, dict) else brand,
                        "availability": offers.get("availability"),
                        "image_url": urljoin(response.url, image) if image else None,
                        "raw": None,
                    }

    @staticmethod
    def _float(value) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query, keep_blank_values=True)
        if page > 1:
            query["page"] = [str(page)]
        else:
            query.pop("page", None)
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    @staticmethod
    def _blocked(text: str) -> bool:
        lowered = (text or "").lower()
        return any(marker in lowered for marker in ("access denied", "verify you are human", "request blocked"))

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }
