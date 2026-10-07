from __future__ import annotations

import json
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.rightmove_categories import RIGHTMOVE_CATEGORIES


class RightmoveListingSpider(BaseListingSpider):
    """Rightmove sale listings from the server-rendered Next.js hydration."""

    name = "rightmove_listing"
    allowed_domains = ["rightmove.co.uk", "www.rightmove.co.uk", "localhost", "127.0.0.1"]
    categories = RIGHTMOVE_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "url", "address", "price", "price_display",
            "price_currency", "bedrooms", "bathrooms", "property_type", "tenure",
            "size", "latitude", "longitude", "summary", "key_features", "photo",
            "photos", "image_count", "floorplan_count", "virtual_tour_count", "agent",
            "agent_phone", "branch_id", "first_visible_date", "added_or_reduced",
            "transaction_type", "tags", "product_label", "result_count", "total_pages",
            "location_id", "category", "page", "position", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name|all>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        if self.category and self.category != "all" and self.category not in self.available_categories():
            raise ValueError(
                f"Unknown category '{self.category}'. Available categories: "
                f"{', '.join(self.available_categories())}"
            )
        self._seen_ids: set[str] = set()

    def start_requests(self):
        self._seen_ids.clear()
        targets = self.categories if self.category == "all" else [{
            "category": self.category or "custom", "url": self.resolve_target_url()
        }]
        for target in targets:
            yield scrapy.Request(
                target["url"],
                callback=self.parse,
                headers=self._html_headers(),
                meta={"category": target["category"], "page": 1},
            )

    def parse(self, response: scrapy.http.Response):
        self._validate_response(response)
        state = self._extract_next_data(response)
        search_results = self._search_results(state)
        if not isinstance(search_results, dict):
            raise RuntimeError(f"Rightmove __NEXT_DATA__ has no searchResults at {response.url}")
        properties = search_results.get("properties")
        if not isinstance(properties, list):
            raise RuntimeError(f"Rightmove searchResults has no list-valued properties at {response.url}")
        if not properties:
            raise RuntimeError(f"Rightmove listing returned zero properties at {response.url}")

        pagination = self._mapping(search_results.get("pagination"))
        page = self._integer(pagination.get("page")) or int(response.meta.get("page", 1))
        for position, prop in enumerate(properties, start=1):
            if not isinstance(prop, dict):
                continue
            item_id = str(prop.get("id") or "")
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            yield self._item(prop, search_results, response, page, position)

        total_pages = min(self._integer(pagination.get("total")) or page, 42)
        next_index = self._integer(pagination.get("next"))
        last_index = self._integer(pagination.get("last"))
        if page < min(self.max_pages, total_pages) and next_index is not None and (
            last_index is None or next_index <= last_index
        ):
            yield response.follow(
                self._page_url(response.url, next_index),
                callback=self.parse,
                headers=self._html_headers(),
                meta={**response.meta, "page": page + 1},
            )

    def _item(self, prop, search_results, response, page, position):
        price = self._mapping(prop.get("price"))
        display_prices = price.get("displayPrices") if isinstance(price.get("displayPrices"), list) else []
        display_price = self._mapping(display_prices[0]).get("displayPrice") if display_prices else None
        location = self._mapping(prop.get("location"))
        customer = self._mapping(prop.get("customer"))
        tenure = self._mapping(prop.get("tenure"))
        images = prop.get("images") if isinstance(prop.get("images"), list) else []
        photos = [image.get("srcUrl") for image in images if isinstance(image, dict) and image.get("srcUrl")]
        features = prop.get("keyFeatures") if isinstance(prop.get("keyFeatures"), list) else []
        product_label = self._mapping(prop.get("productLabel"))
        search_location = self._mapping(search_results.get("location"))
        search_parameters = self._mapping(search_results.get("searchParameters"))
        return {
            "item_id": str(prop.get("id")),
            "title": prop.get("displayAddress") or prop.get("heading"),
            "url": urljoin("https://www.rightmove.co.uk", prop.get("propertyUrl") or ""),
            "address": prop.get("displayAddress"),
            "price": self._integer(price.get("amount")),
            "price_display": display_price,
            "price_currency": price.get("currencyCode"),
            "bedrooms": self._integer(prop.get("bedrooms")),
            "bathrooms": self._integer(prop.get("bathrooms")),
            "property_type": prop.get("propertyTypeFullDescription") or prop.get("propertySubType"),
            "tenure": tenure.get("tenureType"),
            "size": prop.get("displaySize"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "summary": prop.get("summary"),
            "key_features": [feature.get("description") for feature in features if isinstance(feature, dict) and feature.get("description")],
            "photo": photos[0] if photos else None,
            "photos": photos,
            "image_count": self._integer(prop.get("numberOfImages")),
            "floorplan_count": self._integer(prop.get("numberOfFloorplans")),
            "virtual_tour_count": self._integer(prop.get("numberOfVirtualTours")),
            "agent": customer.get("branchDisplayName") or customer.get("brandTradingName"),
            "agent_phone": customer.get("contactTelephone"),
            "branch_id": customer.get("branchId"),
            "first_visible_date": prop.get("firstVisibleDate"),
            "added_or_reduced": prop.get("addedOrReduced"),
            "transaction_type": prop.get("transactionType"),
            "tags": prop.get("tags") if isinstance(prop.get("tags"), list) else [],
            "product_label": product_label.get("productLabelText"),
            "result_count": self._integer(search_results.get("resultCount")),
            "total_pages": self._integer(self._mapping(search_results.get("pagination")).get("total")),
            "location_id": search_location.get("id") or search_parameters.get("locationIdentifier"),
            "category": response.meta.get("category"),
            "page": page,
            "position": position,
            "source": "rightmove_next_data",
            "raw": prop,
            "timestamp": self.job_timestamp.isoformat(),
        }

    @staticmethod
    def _extract_next_data(response):
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            return None
        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            return None
        return value if isinstance(value, dict) else None

    @classmethod
    def _search_results(cls, state):
        props = cls._mapping(state).get("props")
        page_props = cls._mapping(props).get("pageProps")
        return cls._mapping(page_props).get("searchResults")

    @staticmethod
    def _validate_response(response):
        body = response.text or ""
        lowered = body.lower()
        if response.status != 200:
            raise RuntimeError(f"Rightmove listing returned HTTP {response.status}: {response.url}")
        markers = ("failed to get successful response", "pardon the interruption", "captcha")
        if len(response.body) < 5000 or any(marker in lowered for marker in markers):
            raise RuntimeError(f"Rightmove listing returned a challenge or proxy-error payload at {response.url}")

    @staticmethod
    def _page_url(url, index):
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["index"] = str(index)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _mapping(value):
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _integer(value):
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _html_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-GB,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
