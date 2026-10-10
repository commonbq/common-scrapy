from __future__ import annotations

import json
import math
import re
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit

import scrapy
from parsel import Selector

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.dollargeneral_categories import DOLLAR_GENERAL_CATEGORIES


SESSION_URL = "https://www.dollargeneral.com/bin/dg/user"
SEARCH_API_URL = "https://dggo.dollargeneral.com/omni/api/v5/search/shoppinglist/product/Provider"
PAGE_SIZE = 24
MAX_API_RETRIES = 2
PROXY_FAILURE = "Failed to get successful response from website"


class DollargeneralListingSpider(BaseListingSpider):
    """Dollar General listings from its first-party Omni product-search API.

    The guest-session servlet issues the anonymous tokens used by the public
    storefront. Product rows then come exclusively from the Omni API; rendered
    cards and JSON-LD are never parsed as product-data fallbacks.
    """

    name = "dollargeneral_listing"
    allowed_domains = [
        "www.dollargeneral.com", "dollargeneral.com", "dggo.dollargeneral.com",
        "localhost", "127.0.0.1",
    ]
    categories = DOLLAR_GENERAL_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "api_category", "item_id", "sku", "title", "url",
            "image_url", "price", "original_price", "unit_price", "currency",
            "product_category", "category_ids", "uom", "uom_unit",
            "available_quantity", "available_stock_store", "inventory_status",
            "is_sellable", "is_bopis_eligible", "is_ship_to_home",
            "ship_to_home_quantity", "is_deliverable", "deals_status", "rating",
            "reviews_count", "record_type", "root_sv", "store_number", "page",
            "position", "total_count", "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_url = getattr(self, "session_url", SESSION_URL)
        self.api_url = getattr(self, "api_url", SEARCH_API_URL)
        self._seen: set[str] = set()
        self._target = self.category_entry(self.category) if self.category else next(
            iter(self.iter_categories())
        )

    def start_requests(self):
        self._seen.clear()
        yield scrapy.Request(
            f"{self.session_url}?timestamp={int(self.job_timestamp.timestamp() * 1000)}",
            callback=self.parse_session,
            headers=self._session_headers(),
            dont_filter=True,
            meta={"api_retry": 0},
        )

    def parse_session(self, response: scrapy.http.Response):
        data = self._json_body(response)
        if self._is_proxy_failure(data):
            yield self._retry(response.request, "guest-session proxy failure")
            return
        required = (
            "idToken", "appToken", "appSessionToken", "partnerApiToken",
            "customerGuid", "uniqueDeviceId",
        )
        missing = [key for key in required if not data.get(key)]
        store_number = str((data.get("storeInfo") or {}).get("sn") or "").strip()
        if missing or not store_number:
            raise RuntimeError(
                f"Dollar General guest session missing {', '.join(missing) or 'storeInfo.sn'}"
            )
        tokens = {key: str(data[key]) for key in required}
        yield self._api_request(tokens=tokens, store_number=store_number, page=1)

    def parse_api(self, response: scrapy.http.Response):
        if PROXY_FAILURE.lower() in response.text.lower():
            yield self._retry(response.request, "Omni API proxy failure")
            return
        if response.status != 200:
            raise RuntimeError(f"Dollar General Omni API returned HTTP {response.status}")

        page = int(response.meta["page"])
        records, total_count = self._parse_api_payload(response)
        if not records:
            raise RuntimeError(
                f"Dollar General Omni API returned no products for {self._target['api_category']!r}"
            )

        new_count = 0
        for position, record in enumerate(records, 1):
            item_id = self._string(record.get("UPC") or record.get("upc"))
            title = self._string(record.get("Description") or record.get("description"))
            if not item_id or not title or item_id in self._seen:
                continue
            self._seen.add(item_id)
            new_count += 1
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "product"
            yield {
                "category": self.category,
                "api_category": self._target["api_category"],
                "item_id": item_id,
                "sku": self._string(record.get("Sku") or record.get("SKU")),
                "title": title,
                "url": f"https://www.dollargeneral.com/p/{quote(slug)}/{item_id}",
                "image_url": self._string(record.get("Image")),
                "price": self._number(record.get("Price")),
                "original_price": self._number(record.get("OriginalPrice")),
                "unit_price": self._number(record.get("UnitPrice")),
                "currency": "USD",
                "product_category": self._string(record.get("Category")),
                "category_ids": record.get("CategoryIDList") or record.get("CategoryIdList"),
                "uom": self._string(record.get("UOM")),
                "uom_unit": self._string(record.get("UOMUnit")),
                "available_quantity": self._number(record.get("AvailableQty")),
                "available_stock_store": self._number(record.get("AvailableStockStore")),
                "inventory_status": self._number(record.get("InventoryStatus")),
                "is_sellable": self._boolean(record.get("Sellable", record.get("IsSellable"))),
                "is_bopis_eligible": self._boolean(record.get("BopisEligible", record.get("IsBopisEligible"))),
                "is_ship_to_home": self._boolean(record.get("IsShipToHome")),
                "ship_to_home_quantity": self._number(record.get("ShipToHomeQuantity")),
                "is_deliverable": self._boolean(record.get("IsDeliverable")),
                "deals_status": self._string(record.get("DealsStatus")),
                "rating": self._number(record.get("AverageRating")),
                "reviews_count": self._number(record.get("RatingReviewCount")),
                "record_type": self._string(record.get("RecordType")),
                "root_sv": self._string(record.get("RootSV")),
                "store_number": response.meta["store_number"],
                "page": page,
                "position": position,
                "total_count": total_count,
                "source_url": self.api_url,
                "source": "dollargeneral_omni_search_api",
                "raw": record,
            }

        total_pages = math.ceil(total_count / PAGE_SIZE) if total_count else page
        if new_count and page < min(self.max_pages, total_pages):
            yield self._api_request(
                tokens=response.meta["tokens"],
                store_number=response.meta["store_number"],
                page=page + 1,
            )

    def _api_request(self, *, tokens: dict[str, str], store_number: str, page: int):
        body = {
            "StoreNbr": int(store_number),
            "SearchTerm": "*",
            "PageSize": PAGE_SIZE,
            "PageStartRecordIndex": (page - 1) * PAGE_SIZE,
            "Filters": {
                "category": [self._target["api_category"]],
                "brand": [], "dgDelivery": False, "dgPickUp": False,
                "dgShipTohome": False, "soldAtStore": True, "inStock": False,
            },
            "IncludeSponsored": False,
            "IncludeShipToHome": True,
            "IncludeDeals": True,
            "offerSourceType": 0,
            "SearchType": 0,
        }
        return scrapy.Request(
            self.api_url,
            method="POST",
            body=json.dumps(body, separators=(",", ":")),
            callback=self.parse_api,
            headers=self._api_headers(tokens),
            dont_filter=True,
            meta={
                "tokens": tokens, "store_number": store_number, "page": page,
                "api_retry": 0, "proxy": self._api_proxy(),
            },
        )

    def _parse_api_payload(self, response: scrapy.http.Response) -> tuple[list[dict[str, Any]], int]:
        text = response.text.lstrip()
        if text.startswith("{"):
            data = json.loads(text)
            return list(data.get("Items") or []), int((data.get("PaginationInfo") or {}).get("TotalRecords") or 0)

        selector = Selector(text=response.text, type="xml")
        records: list[dict[str, Any]] = []
        for node in selector.xpath('//*[local-name()="ProductSearchItem"]'):
            record: dict[str, Any] = {}
            for child in node.xpath("./*"):
                key = child.xpath("local-name()").get()
                values = child.xpath('.//*[local-name()="string"]/text()').getall()
                record[key] = values or child.xpath("string(.)").get(default="").strip() or None
            records.append(record)
        total = selector.xpath('string(//*[local-name()="PaginationInfo"]/*[local-name()="TotalRecords"])').get()
        return records, int(total or 0)

    def _retry(self, request: scrapy.Request, reason: str) -> scrapy.Request:
        retries = int(request.meta.get("api_retry", 0)) + 1
        if retries > MAX_API_RETRIES:
            raise RuntimeError(f"Dollar General {reason} after {MAX_API_RETRIES + 1} attempts")
        self.logger.warning("Retrying Dollar General request (%s, attempt %d)", reason, retries + 1)
        return request.replace(dont_filter=True, meta={**request.meta, "api_retry": retries})

    def _api_proxy(self) -> str | None:
        proxy = self.settings.get("PROXY") if hasattr(self, "settings") else None
        if not isinstance(proxy, str) or not proxy:
            return None
        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return proxy
        username = parts.username
        if ".keep_headers=true" not in username:
            username = f"{username}.keep_headers=true"
        credentials = quote(username, safe=".=_-")
        if parts.password is not None:
            credentials += f":{quote(parts.password, safe='')}"
        host = parts.hostname + (f":{parts.port}" if parts.port else "")
        return urlunsplit((parts.scheme, f"{credentials}@{host}", parts.path, parts.query, parts.fragment))

    @staticmethod
    def _session_headers() -> dict[str, str]:
        return {"Accept": "application/json", "Referer": "https://www.dollargeneral.com/"}

    @staticmethod
    def _api_headers(tokens: dict[str, str]) -> dict[str, str]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.dollargeneral.com",
            "Referer": "https://www.dollargeneral.com/",
            "Authorization": f"Bearer {tokens['idToken']}",
            "X-DG-AppToken": tokens["appToken"],
            "X-DG-AppSessionToken": tokens["appSessionToken"],
            "X-DG-partnerApiToken": tokens["partnerApiToken"],
            "X-DG-customerGuid": tokens["customerGuid"],
            "X-DG-deviceUniqueId": tokens["uniqueDeviceId"],
            "X-DG-CLOUD-SERVICE": "omni",
        }

    @staticmethod
    def _json_body(response: scrapy.http.Response) -> dict[str, Any]:
        try:
            return json.loads(response.text)
        except (json.JSONDecodeError, TypeError) as exc:
            raise RuntimeError(f"Dollar General session response was not JSON: {exc}") from exc

    @staticmethod
    def _is_proxy_failure(data: dict[str, Any]) -> bool:
        return PROXY_FAILURE.lower() in str(data.get("status") or "").lower()

    @staticmethod
    def _string(value: Any) -> str | None:
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if value in (None, ""):
            return None
        try:
            number = float(value)
            return int(number) if number.is_integer() else number
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _boolean(value: Any) -> bool | None:
        if isinstance(value, bool):
            return value
        if value in (None, ""):
            return None
        lowered = str(value).strip().lower()
        if lowered in {"true", "1"}:
            return True
        if lowered in {"false", "0"}:
            return False
        return None
