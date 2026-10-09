from __future__ import annotations

"""Etsy category listings from the server-provided Context bootstrap."""

import json
import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import scrapy
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.etsy_categories import ETSY_CATEGORIES


SOURCE = "etsy_context_bootstrap"
CONTEXT_MARKER = "Etsy.Context.data=assign(Etsy.Context.data ? Etsy.Context.data : {}, "
IMPRESSION_RE = re.compile(
    r"^(?P<item_id>\d+)-(?P<impression_epoch>\d+)-.+?-\d+--"
    r"(?P<shop_id>\d+)-(?P<price_cents>\d+)-(?P<currency>[A-Z]{3})-"
    r"(?P<discount_percent>\d+)-[^-]+-(?P<page>\d+)-(?P<position>\d+)$"
)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


class EtsyListingSpider(BaseListingSpider):
    """Extract products exclusively from Etsy's ``Etsy.Context.data`` state.

    The bootstrap's per-listing encoded impressions contain listing/shop IDs,
    current price, currency, discount, page, and position. Its top-level values
    provide total pages and organic inventory. Rendered cards and JSON-LD are
    deliberately not parsed and there is no product-data fallback.
    """

    name = "etsy_listing"
    allowed_domains = ["etsy.com", "www.etsy.com"]
    categories = ETSY_CATEGORIES
    page_size = 48

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "item_id", "shop_id", "url", "price", "original_price", "currency",
            "discount_percent", "category", "category_url", "page", "position",
            "total_pages", "organic_listings_count", "request_uuid",
            "impression_epoch", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()
        self._session_id = f"etsy{int(self.job_timestamp.timestamp())}"

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield self._page_request(category_url, page=1)

    def _page_request(self, category_url: str, page: int) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(category_url, page),
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": USER_AGENT,
            },
            callback=self.parse,
            meta={
                "category": self.category, "category_url": category_url, "page": page,
                "proxy": self._proxy(), "handle_httpstatus_all": True,
            },
            dont_filter=True,
        )

    def parse(self, response):
        page = int(response.meta["page"])
        if response.status != 200:
            raise CloseSpider(f"Etsy bootstrap returned HTTP {response.status}")
        state = self._context_state(response)
        if not state:
            raise CloseSpider("Etsy document contained no Context bootstrap")
        records = self._impression_records(state)
        if not records:
            raise CloseSpider("Etsy Context bootstrap contained no listing impressions")

        total_pages = self._integer(state.get("total_pages"))
        organic_count = self._integer(state.get("organic_listings_count"))
        for record in records:
            item_id = record["item_id"]
            if item_id in self._seen:
                continue
            self._seen.add(item_id)
            price = int(record["price_cents"]) / 100
            discount = int(record["discount_percent"])
            original = round(price / (1 - discount / 100), 2) if 0 < discount < 100 else None
            yield {
                "item_id": item_id,
                "shop_id": record["shop_id"],
                "url": f"https://www.etsy.com/listing/{item_id}",
                "price": price,
                "original_price": original,
                "currency": record["currency"],
                "discount_percent": discount,
                "category": response.meta["category"],
                "category_url": response.meta["category_url"],
                "page": int(record["page"]),
                "position": int(record["position"]),
                "total_pages": total_pages,
                "organic_listings_count": organic_count,
                "request_uuid": state.get("request_uuid"),
                "impression_epoch": int(record["impression_epoch"]),
                "source": SOURCE,
                "raw": {"encoded_impression": record["encoded_impression"]},
                "timestamp": self.job_timestamp,
            }

        if page < self.max_pages and (total_pages is None or page < total_pages):
            yield self._page_request(response.meta["category_url"], page + 1)

    @staticmethod
    def _context_state(response) -> dict:
        decoder = json.JSONDecoder()
        for script in response.css("script::text").getall():
            if CONTEXT_MARKER not in script:
                continue
            try:
                value, _ = decoder.raw_decode(script.split(CONTEXT_MARKER, 1)[1])
            except (IndexError, json.JSONDecodeError):
                continue
            if isinstance(value, dict):
                return value
        return {}

    @staticmethod
    def _impression_records(state: dict) -> list[dict]:
        records = []
        for key, value in state.items():
            if not key.startswith("listingcard:") or not isinstance(value, dict):
                continue
            encoded = value.get("encoded_impression")
            match = IMPRESSION_RE.match(encoded or "")
            if match:
                records.append({**match.groupdict(), "encoded_impression": encoded})
        records.sort(key=lambda item: (int(item["page"]), int(item["position"])))
        return records

    def _proxy(self) -> str | None:
        proxy = self.settings.get("PROXY")
        if not proxy or "scrapeops.io" not in proxy:
            return proxy
        parsed = urlparse(proxy)
        username = parsed.username or ""
        for option in (
            "residential=true", "country=us", "keep_headers=true", "bypass=5",
            "render_js=true", f"session_id={self._session_id}",
        ):
            if option not in username:
                username += f".{option}"
        host = parsed.hostname or ""
        netloc = f"{username}:{parsed.password or ''}@{host}"
        if parsed.port:
            netloc += f":{parsed.port}"
        return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))

    @staticmethod
    def _page_url(category_url: str, page: int) -> str:
        parsed = urlparse(category_url)
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query["page"] = str(page)
        query["ref"] = "pagination"
        return urlunparse(parsed._replace(query=urlencode(query)))

    @staticmethod
    def _integer(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
