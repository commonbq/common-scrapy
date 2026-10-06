from __future__ import annotations

"""AutoZone product listings from Next.js React Query hydration."""

import json
from typing import Any, Iterable
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit, parse_qsl, urlencode

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class AutozoneListingSpider(BaseListingSpider):
    name = "autozone_listing"
    allowed_domains = ["autozone.com", "www.autozone.com"]
    categories = [
        {"category": slug, "url": "https://www.autozone.com" + path}
        for slug, path in [
            ("oil-filter", "/filters-and-pcv/oil-filter"),
            ("batteries-chargers", "/batteries-starting-and-charging"),
            ("brakes", "/brakes-and-traction-control"),
            ("lighting-electrical", "/electrical-and-lighting"),
            ("wipers-components", "/ignition-tune-up-and-routine-maintenance"),
            ("wash-wax", "/wash-and-wax"),
            ("oil-fluids-chemicals", "/fluids-and-chemicals"),
            ("alternators-starters", "/alternators-and-charging-system"),
            ("towing-trailer", "/truck-and-towing"),
            ("interior-accessories", "/interior-accessories"),
            ("air-conditioning-heating", "/cooling-heating-and-climate-control"),
            ("apparel-clothing-hats", "/apparel-clothing-hats"),
            ("belts-hoses", "/belts-and-hoses"),
            ("body-collision", "/collision-body-parts-and-hardware"),
            ("engines", "/external-engine"),
            ("exhaust-emission-control", "/emission-control-and-exhaust"),
            ("exterior-accessories", "/exterior-accessories"),
            ("filters-pcv", "/filters-and-pcv"),
            ("fuel-air-delivery", "/fuel-and-air-delivery"),
            ("paint-adhesive", "/paint-and-body"),
        ]
    ]
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "part_number", "url",
            "image", "price", "currency", "availability", "in_stock",
            "sponsored", "page", "position", "total_count", "source", "raw",
        ],
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, listing_url: str, page: int) -> scrapy.Request:
        meta = {"category": self.category, "page": page, "listing_url": listing_url}
        proxy = self._residential_proxy()
        if proxy:
            meta["proxy"] = proxy
        return scrapy.Request(
            self._page_url(listing_url, page), headers=self.headers, meta=meta,
            callback=self.parse, dont_filter=True,
        )

    def _residential_proxy(self) -> str | None:
        settings = getattr(self, "settings", {})
        proxy = settings.get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return proxy
        username = unquote(parts.username)
        options = username.split(".")
        if "residential=true" not in options:
            username += ".residential=true"
        if "country=us" not in options:
            username += ".country=us"
        auth = quote(username, safe=".=")
        if parts.password is not None:
            auth += ":" + quote(unquote(parts.password), safe="")
        host = parts.hostname + (f":{parts.port}" if parts.port else "")
        return urlunsplit((parts.scheme, f"{auth}@{host}", parts.path, parts.query, parts.fragment))

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        if page <= 1:
            return url
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))

    @staticmethod
    def _next_data(response) -> dict[str, Any]:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"AutoZone response has no __NEXT_DATA__: {response.url}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"AutoZone __NEXT_DATA__ is malformed: {response.url}") from exc
        return data

    @staticmethod
    def _queries(data: dict[str, Any]) -> list[dict[str, Any]]:
        queries = (((data.get("props") or {}).get("pageProps") or {})
                   .get("dehydratedState", {}).get("queries"))
        if not isinstance(queries, list):
            raise RuntimeError("AutoZone hydration has no React Query query list")
        return queries

    @classmethod
    def _hydrated_results(cls, data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict]]:
        shelf_query = None
        detail_queries = []
        for query in cls._queries(data):
            key = query.get("queryKey") or []
            key_name = str(key[0]).lower() if key else ""
            if key_name == "productshelf-results":
                shelf_query = query
            elif "sku" in key_name and "detail" in key_name:
                detail_queries.append(query)
        if not shelf_query:
            raise RuntimeError("AutoZone hydration has no productshelf-results query")
        pages = (((shelf_query.get("state") or {}).get("data") or {}).get("pages"))
        if not isinstance(pages, list) or not pages:
            raise RuntimeError("AutoZone product shelf query has no pages")
        results = (pages[0] or {}).get("productShelfResults")
        if not isinstance(results, dict) or not isinstance(results.get("skuRecords"), list):
            raise RuntimeError("AutoZone product shelf hydration has no skuRecords")
        if not detail_queries:
            raise RuntimeError("AutoZone hydration has no product SKU details query")
        details = {}
        for detail_query in detail_queries:
            details.update(cls._detail_map((detail_query.get("state") or {}).get("data")))
        if not details:
            raise RuntimeError("AutoZone product SKU details query is empty")
        return results, details

    @classmethod
    def _detail_map(cls, value: Any) -> dict[str, dict]:
        found: dict[str, dict] = {}
        def visit(node: Any) -> None:
            if isinstance(node, dict):
                pricing = node.get("skuPricingAndAvailability")
                availability = node.get("availabilityInfoVO")
                sku = (node.get("itemId") or node.get("skuId") or node.get("sku")
                       or (pricing.get("skuId") if isinstance(pricing, dict) else None)
                       or (availability.get("skuId") if isinstance(availability, dict) else None))
                if sku is not None:
                    found.setdefault(str(sku), node)
                for child in node.values():
                    visit(child)
            elif isinstance(node, list):
                for child in node:
                    visit(child)
        visit(value)
        return found

    @staticmethod
    def _price(detail: dict[str, Any]) -> Any:
        for key in ("price", "retailPrice", "currentPrice", "unitPrice"):
            value = detail.get(key)
            if isinstance(value, dict):
                value = value.get("value") or value.get("amount")
            if value is not None:
                return value
        pricing = (detail.get("pricing") or detail.get("priceData")
                   or detail.get("skuPricingAndAvailability") or {})
        if isinstance(pricing, dict):
            return AutozoneListingSpider._price(pricing)
        return None

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"AutoZone listing returned HTTP {response.status}: {response.url}")
        results, details = self._hydrated_results(self._next_data(response))
        page = response.meta["page"]
        records = results["skuRecords"]
        for position, record in enumerate(records, 1):
            item_id = str(record.get("itemId") or "")
            if not item_id or item_id in self._seen:
                continue
            detail = details.get(item_id)
            if not detail:
                raise RuntimeError(f"AutoZone SKU detail missing for item {item_id}")
            price = self._price(detail)
            if price is None:
                raise RuntimeError(f"AutoZone price missing for item {item_id}")
            self._seen.add(item_id)
            pricing = detail.get("skuPricingAndAvailability") or {}
            stock = detail.get("inStock")
            if stock is None:
                stock = pricing.get("shipToHomeAvailable") or pricing.get("storePickupAvailable")
            availability = (detail.get("availability") or detail.get("stockStatus")
                            or pricing.get("shipToHomeStockLabel") or pricing.get("storePickupStockLabel"))
            if isinstance(availability, dict):
                availability = availability.get("status") or availability.get("label")
            yield {
                "category": response.meta.get("category"), "item_id": item_id,
                "title": record.get("itemDescription"), "brand": record.get("brandName"),
                "part_number": record.get("partNumber"),
                "url": urljoin("https://www.autozone.com", record.get("productDetailsPageUrl") or ""),
                "image": record.get("productImageUrl"), "price": price, "currency": "USD",
                "availability": availability, "in_stock": stock,
                "sponsored": bool(record.get("sponsoredProductFlag")), "page": page,
                "position": position, "total_count": results.get("totalNumberOfRecords"),
                "source": "autozone_next_data", "raw": {"record": record, "detail": detail},
            }
        last = results.get("lastRecordNumber")
        total = results.get("totalNumberOfRecords")
        if page < self.max_pages and isinstance(last, int) and isinstance(total, int) and last < total:
            yield self._request(response.meta["listing_url"], page + 1)

    @classmethod
    def discover_categories(cls, data: dict[str, Any]) -> list[dict[str, str]]:
        page_props = ((data.get("props") or {}).get("pageProps") or {})
        root = page_props.get("topNavProductData", {}).get("rootCategories", [])
        output = []
        for entry in root if isinstance(root, list) else []:
            path = entry.get("url") or entry.get("link") or entry.get("seoUrl")
            name = entry.get("name") or entry.get("title")
            if path and name:
                output.append({"category": str(name), "url": urljoin("https://www.autozone.com", path)})
        return output
