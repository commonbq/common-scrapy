from __future__ import annotations

"""DigiKey listings parsed exclusively from the Next.js bootstrap payload."""

import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.digikey_categories import DIGIKEY_CATEGORIES


class DigikeyListingSpider(BaseListingSpider):
    name = "digikey_listing"
    allowed_domains = ["digikey.com", "www.digikey.com"]
    categories = DIGIKEY_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "product_id", "product_number", "manufacturer_part_number", "title",
            "manufacturer", "url", "price", "currency", "stock_quantity",
            "stock_label", "category", "category_name", "category_url", "page",
            "position", "total_products", "source", "timestamp",
        ],
    }

    def start_requests(self):
        entry = self.category_entry(self.category)
        if self.url:
            target = self.url
        elif self.category_url:
            target = self.category_url
        elif entry:
            target = entry["url"]
        else:
            raise ValueError(f"Unknown category {self.category!r}; choose one of {self.available_categories()}")
        yield self._request(target, 1, entry or {})

    def _request(self, url: str, page: int, entry: dict) -> scrapy.Request:
        parts = urlparse(url)
        query = parse_qs(parts.query)
        query["page"] = [str(page)]
        return scrapy.Request(
            urlunparse(parts._replace(query=urlencode(query, doseq=True))),
            callback=self.parse,
            meta={"page": page, "category_entry": entry, "proxy": self.settings.get("PROXY")},
        )

    def parse(self, response):
        page = int(response.meta["page"])
        script = response.css('script#__NEXT_DATA__::text').get()
        if not script:
            raise CloseSpider("DigiKey page did not contain the Next.js bootstrap")
        try:
            data = json.loads(script)["props"]["pageProps"]["envelope"]["data"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise CloseSpider(f"Unrecognized DigiKey bootstrap structure: {exc}") from exc

        products = data.get("products")
        if not isinstance(products, list) or not products:
            # Navigation/category landing pages carry the next taxonomy level
            # in the same bootstrap; follow it until reaching product leaves.
            subcategories = (data.get("category") or {}).get("subCategories") or []
            if subcategories:
                for child in subcategories:
                    child_url = child.get("url")
                    if child_url:
                        yield self._request(response.urljoin(child_url), 1, response.meta["category_entry"])
                return
            raise CloseSpider("DigiKey bootstrap contained neither products nor subcategories")
        entry = response.meta["category_entry"]
        category_name = entry.get("category_name") or (data.get("category") or {}).get("label") or self.category
        for position, row in enumerate(products, 1):
            parts = {component.get("type"): component.get("value") for component in row if isinstance(component, dict)}
            detail = parts.get("productDetail") or {}
            compare = parts.get("compare") or {}
            inventory = parts.get("qtyAvailable") or []
            prices = parts.get("unitPrice") or []
            if not detail.get("productId"):
                continue
            identity = compare or {}
            manufacturer = identity.get("manufacturer") or {}
            if not manufacturer:
                manufacturer_link = detail.get("manufacturer") or {}
                manufacturer = manufacturer_link.get("value") or {}
            manufacturer_name = manufacturer.get("name") or manufacturer.get("label")
            if not manufacturer_name:
                # The bootstrap's stable detail path includes the supplier slug.
                slug = (detail.get("detailUrl") or "").split("/")
                if len(slug) > 4 and slug[4]:
                    manufacturer_name = slug[4].replace("-", " ").title()
            stock = next((stock for stock in inventory if stock.get("label") == "In Stock"), {})
            price = prices[0].get("unitPrice") if prices else None
            yield {
                "product_id": detail.get("productId"),
                "product_number": identity.get("productNumber"),
                "manufacturer_part_number": detail.get("productNumber") or identity.get("manufacturerPartNumber"),
                "title": detail.get("description") or identity.get("shortDescription"),
                "manufacturer": manufacturer_name,
                "url": response.urljoin(detail.get("detailUrl", "")),
                "price": price,
                "currency": "USD",
                "stock_quantity": stock.get("quantity"),
                "stock_label": stock.get("label"),
                "category": self.category,
                "category_name": category_name,
                "category_url": response.url.split("?", 1)[0],
                "page": page,
                "position": position,
                "total_products": data.get("productCount"),
                "source": "digikey_next_data",
                "timestamp": self.job_timestamp,
            }
        if page < self.max_pages and len(products) >= 25:
            yield self._request(response.url.split("?", 1)[0], page + 1, entry)
