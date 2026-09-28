from __future__ import annotations

import json

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class SheinListingSpider(BaseListingSpider):
    """Extract SHEIN category products from server-rendered ItemList JSON-LD."""

    name = "shein_listing"
    allowed_domains = ["shein.com", "www.shein.com", "us.shein.com"]

    categories = [
        {"category": "women", "url": "https://us.shein.com/Women-c-2030.html"},
        {"category": "curve", "url": "https://us.shein.com/Curve-Plus-Size-c-1888.html"},
        {"category": "men", "url": "https://us.shein.com/Men-c-2026.html"},
        {"category": "kids", "url": "https://us.shein.com/Kids-c-2031.html"},
        {"category": "baby", "url": "https://us.shein.com/Baby-c-2032.html"},
        {"category": "home", "url": "https://us.shein.com/Home-Living-c-2034.html"},
        {"category": "beauty", "url": "https://us.shein.com/Beauty-Health-c-1864.html"},
        {"category": "shoes", "url": "https://us.shein.com/Shoes-c-1745.html"},
        {"category": "bags", "url": "https://us.shein.com/Bags-c-1764.html"},
        {"category": "jewelry", "url": "https://us.shein.com/Jewelry-Accessories-c-1765.html"},
        {"category": "sports", "url": "https://us.shein.com/Sports-Outdoor-c-3195.html"},
    ]

    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "category",
            "item_id",
            "title",
            "brand",
            "url",
            "image_url",
            "price",
            "currency",
            "availability",
            "position",
            "source",
            "category_url",
            "page",
            "raw",
        ]
    }

    def start_requests(self):
        yield scrapy.Request(
            self.resolve_target_url(),
            callback=self.parse,
            meta={"category": self.category, "page": 1, "allow_offsite": bool(self.url)},
            headers=self._headers(),
        )

    def parse(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        entries = self._item_list_entries(response)
        if not entries:
            raise RuntimeError(f"No SHEIN ItemList JSON-LD products found at {response.url}")

        seen: set[str] = set()
        for entry in entries:
            product = entry.get("item") if isinstance(entry.get("item"), dict) else entry
            url = response.urljoin(product.get("url") or entry.get("url") or "")
            item_id = product.get("sku") or product.get("productID")
            dedupe_key = str(item_id or url)
            if not dedupe_key or dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            offers = product.get("offers") if isinstance(product.get("offers"), dict) else {}
            brand = product.get("brand")
            if isinstance(brand, dict):
                brand = brand.get("name")
            image = product.get("image")
            if isinstance(image, list):
                image = image[0] if image else None
            yield {
                "category": response.meta.get("category"),
                "item_id": item_id,
                "title": product.get("name"),
                "brand": brand,
                "url": url,
                "image_url": response.urljoin(image) if image else None,
                "price": self._to_float(offers.get("price") or offers.get("lowPrice")),
                "currency": offers.get("priceCurrency"),
                "availability": self._schema_name(offers.get("availability")),
                "position": entry.get("position"),
                "source": "shein_itemlist_jsonld",
                "category_url": response.url,
                "page": page,
                "raw": product,
            }

        if page < self.max_pages:
            next_url = response.css('link[rel="next"]::attr(href)').get()
            if next_url:
                yield response.follow(
                    next_url,
                    callback=self.parse,
                    meta={
                        "category": response.meta.get("category"),
                        "page": page + 1,
                        "allow_offsite": response.meta.get("allow_offsite", False),
                    },
                    headers=self._headers(),
                )

    @staticmethod
    def _item_list_entries(response: scrapy.http.Response) -> list[dict]:
        entries: list[dict] = []
        for text in response.css('script[type="application/ld+json"]::text').getall():
            try:
                value = json.loads(text)
            except (TypeError, json.JSONDecodeError):
                continue
            nodes = value if isinstance(value, list) else [value]
            for node in nodes:
                if not isinstance(node, dict):
                    continue
                graph = node.get("@graph") if isinstance(node.get("@graph"), list) else [node]
                for candidate in graph:
                    if isinstance(candidate, dict) and candidate.get("@type") == "ItemList":
                        entries.extend(
                            entry for entry in candidate.get("itemListElement") or [] if isinstance(entry, dict)
                        )
        return entries

    @staticmethod
    def _to_float(value):
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _schema_name(value):
        return value.rsplit("/", 1)[-1] if isinstance(value, str) else None

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        }
