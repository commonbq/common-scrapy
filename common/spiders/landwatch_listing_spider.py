from __future__ import annotations

"""LandWatch listings from the server-rendered ``#__SERVER_STATE__`` payload."""

import json
from typing import Any, Iterable
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.landwatch_categories import LANDWATCH_CATEGORIES


RESIDENTIAL_PROXY = "residential=true"


class LandwatchListingSpider(BaseListingSpider):
    """Extract the authoritative SSR search bootstrap, with no markup fallback."""

    name = "landwatch_listing"
    allowed_domains = ["landwatch.com", "www.landwatch.com"]
    categories = LANDWATCH_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "inventory_id", "title", "url", "image_url",
            "price", "currency", "price_per_acre", "price_change_amount",
            "acres", "acres_display", "property_types", "address", "city", "county",
            "state", "state_code", "zip", "latitude", "longitude", "beds", "baths",
            "half_baths", "home_sqft", "broker_name", "broker_company", "broker_phone",
            "broker_url", "has_house", "has_video", "has_virtual_tour", "image_count",
            "last_updated", "page", "position", "total_count", "source", "raw", "timestamp",
        ],
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        self._seen.clear()
        yield self._request(self.resolve_target_url(), page=1)

    def _request(self, url: str, *, page: int) -> scrapy.Request:
        return scrapy.Request(
            url,
            callback=self.parse,
            headers=self.headers,
            meta={
                "proxy": self._residential_proxy(),
                "page": page,
                "category": self.category or "custom",
            },
            dont_filter=True,
        )

    def _residential_proxy(self) -> str | None:
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not isinstance(proxy, str) or not proxy or "scrapeops" not in proxy.lower():
            return proxy or None
        parts = urlsplit(proxy)
        if not parts.hostname or parts.password is None:
            return proxy
        if RESIDENTIAL_PROXY in (parts.username or ""):
            return proxy
        username = f"{parts.username}.{RESIDENTIAL_PROXY}"
        netloc = f"{username}:{parts.password}@{parts.hostname}:{parts.port}"
        return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"LandWatch returned HTTP {response.status}: {response.url}")

        state = self._server_state(response)
        search_page = state.get("searchPage")
        results = search_page.get("searchResults") if isinstance(search_page, dict) else None
        if not isinstance(results, dict):
            raise RuntimeError(
                f"LandWatch bootstrap at {response.url} has no searchPage.searchResults"
            )
        properties = results.get("propertyResults")
        if not isinstance(properties, list):
            raise RuntimeError(
                f"LandWatch bootstrap at {response.url} has no propertyResults list"
            )

        page = int(response.meta.get("page") or 1)
        category = response.meta.get("category") or self.category or "custom"
        total_count = self._number(results.get("totalCount"), integer=True)
        emitted = 0
        for position, product in enumerate(properties, start=1):
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("siteListingId") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(
                product,
                response=response,
                category=category,
                page=page,
                position=position,
                total_count=total_count,
            )

        if properties and not emitted:
            self.logger.warning("LandWatch page %s contained only duplicate property IDs", page)

        pagination = results.get("paginationData")
        pagination = pagination if isinstance(pagination, dict) else {}
        next_link = pagination.get("nextLink")
        if page < self.max_pages and isinstance(next_link, str) and next_link:
            yield self._request(urljoin(response.url, next_link), page=page + 1)

    @staticmethod
    def _server_state(response: scrapy.http.Response) -> dict[str, Any]:
        raw = response.css("script#__SERVER_STATE__::text").get()
        if not raw:
            raise RuntimeError(
                f"LandWatch {response.url} has no #__SERVER_STATE__; response is blocked "
                "or the bootstrap contract changed"
            )
        try:
            state = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"LandWatch bootstrap at {response.url} is invalid JSON") from exc
        if not isinstance(state, dict):
            raise RuntimeError(f"LandWatch bootstrap at {response.url} is not an object")
        return state

    def _item(
        self,
        product: dict[str, Any],
        *,
        response: scrapy.http.Response,
        category: str,
        page: int,
        position: int,
        total_count: int | None,
    ) -> dict[str, Any]:
        image_id = product.get("thumbnailDocumentId")
        broker_path = product.get("brokerCanonicalUrl")
        return {
            "category": category,
            "item_id": str(product.get("siteListingId")),
            "inventory_id": self._number(product.get("id"), integer=True),
            "title": self._text(product.get("title")),
            "url": urljoin(response.url, product.get("canonicalUrl") or ""),
            "image_url": (
                f"https://assets.landwatch.com/resizedimages/394/0/h/80/1-{image_id}"
                if image_id else None
            ),
            "price": self._number(product.get("price")),
            "currency": "USD",
            "price_per_acre": self._number(product.get("pricePerAcre")),
            "price_change_amount": self._number(product.get("priceChangeAmount")),
            "acres": self._number(product.get("acres")),
            "acres_display": self._text(product.get("acresDisplay")),
            "property_types": product.get("types") or [],
            "address": self._text(product.get("address")),
            "city": self._text(product.get("city")),
            "county": self._text(product.get("county")),
            "state": self._text(product.get("state")),
            "state_code": self._text(product.get("stateAbbreviation") or product.get("stateCode")),
            "zip": self._text(product.get("zip")),
            "latitude": self._number(product.get("latitude")),
            "longitude": self._number(product.get("longitude")),
            "beds": self._number(product.get("beds"), integer=True),
            "baths": self._number(product.get("baths"), integer=True),
            "half_baths": self._number(product.get("halfBaths"), integer=True),
            "home_sqft": self._number(product.get("homesqft"), integer=True),
            "broker_name": self._text(product.get("brokerName")),
            "broker_company": self._text(product.get("brokerCompany")),
            "broker_phone": self._text(product.get("brokerPhone")),
            "broker_url": urljoin(response.url, broker_path) if broker_path else None,
            "has_house": bool(product.get("hasHouse")),
            "has_video": bool(product.get("hasVideo")),
            "has_virtual_tour": bool(product.get("hasVirtualTour")),
            "image_count": self._number(product.get("imageCount"), integer=True),
            "last_updated": self._text(product.get("lastUpdated")),
            "page": page,
            "position": position,
            "total_count": total_count,
            "source": "landwatch_server_state_bootstrap",
            "raw": product,
        }

    @staticmethod
    def _text(value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _number(value: Any, *, integer: bool = False) -> int | float | None:
        if value in (None, "") or isinstance(value, bool):
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        if integer or number.is_integer():
            return int(number)
        return number
