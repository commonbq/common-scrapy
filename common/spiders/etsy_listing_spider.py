from __future__ import annotations

"""Etsy category listings from the first-party asynchronous Neu Spec API."""

import json
import re
from urllib.parse import urlencode, urlparse, urlunparse

import scrapy
from parsel import Selector
from scrapy.exceptions import CloseSpider

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.etsy_categories import ETSY_CATEGORIES


API_URL = "https://www.etsy.com/api/v3/ajax/bespoke/public/neu/specs/async_search_results"


class EtsyListingSpider(BaseListingSpider):
    """Read Etsy search cards returned by its own pagination API.

    The category document, JSON-LD, and directly rendered category cards are not
    product-data fallbacks. Every exported record comes from the JSON Neu Spec
    response's ``async_search_results`` fragment.
    """

    name = "etsy_listing"
    allowed_domains = ["etsy.com", "www.etsy.com"]
    categories = ETSY_CATEGORIES
    page_size = 48

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "item_id", "shop_id", "title", "shop", "url", "image",
            "price", "original_price", "currency", "rating", "reviews_count",
            "is_ad", "free_shipping", "category", "page", "position",
            "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        category_url = self.resolve_target_url()
        yield self._api_request(category_url, 1)

    def _api_request(self, category_url: str, page: int) -> scrapy.Request:
        # The Neu Spec client passes each spec's args as a single JSON string
        # (specs[<key>][0]=<spec_name>&specs[<key>][1]=<json>); the exploded
        # bracket form is rejected with 400 "Missing input parameter:
        # [search_request_params]".
        #
        # Proxy composition note: the render/JS engine strips non-standard
        # headers, so any composition containing render_js=true loses the
        # required ``x-etsy-protection`` header and the API answers
        # 400 "Missing required header x-etsy-protection". keep_headers=true
        # alone is the only observed route that preserves the header and
        # reaches Etsy without a captcha interstitial.
        facet = urlparse(category_url).path.removeprefix("/c/").strip("/")
        args = {
            "search_request_params": {
                "detected_locale": {"language": "en-US", "currency_code": "USD", "region": "US"},
                "name_map": {"results_per_page": "result_count"},
                "parameters": {
                    "page": page,
                    "ref": "pagination",
                    "facet": facet,
                    "page_type": "category",
                    "result_count": self.page_size,
                    "referrer": category_url,
                },
            },
            "request_type": "pagination_preact",
            "is_eligible_for_spa_reformulations": "false",
        }
        params = [
            ("specs[async_search_results][0]", "Search2_ApiSpecs_WebSearch"),
            ("specs[async_search_results][1]", json.dumps(args, separators=(",", ":"))),
            ("view_data_event_name", "search_async_pagination_specview_rendered"),
        ]
        return scrapy.Request(
            f"{API_URL}?{urlencode(params)}",
            headers={
                "Accept": "application/json",
                "Referer": category_url,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
                "x-detected-locale": "USD|en-US|US",
                "x-etsy-protection": "1",
            },
            callback=self.parse_api,
            meta={
                "category": self.category,
                "category_url": category_url,
                "page": page,
                "proxy": self._api_proxy(),
                "handle_httpstatus_all": True,
            },
            dont_filter=True,
        )

    def _api_proxy(self) -> str | None:
        proxy = self.settings.get("PROXY")
        if not proxy or "scrapeops.io" not in proxy:
            return proxy
        parsed = urlparse(proxy)
        username = parsed.username or ""
        for option in (
            "keep_headers=true",
        ):
            if option not in username:
                username += f".{option}"
        netloc = f"{username}:{parsed.password or ''}@{parsed.hostname}:{parsed.port}"
        return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))

    def parse_api(self, response):
        page = response.meta["page"]
        if response.status != 200:
            raise CloseSpider(f"Etsy Neu Spec API returned HTTP {response.status}")
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise CloseSpider("Etsy Neu Spec API returned non-JSON") from exc
        if payload.get("status") and not payload.get("output"):
            raise CloseSpider(f"Etsy Neu Spec API proxy error: {payload['status']}")

        output = payload.get("output") or {}
        if isinstance(output, list):
            # The endpoint returns `output` as a list of spec payloads rather
            # than a single dict; merge dicts or use the first HTML fragment.
            dict_entries = [entry for entry in output if isinstance(entry, dict)]
            str_entries = [entry for entry in output if isinstance(entry, str) and entry.strip()]
            if dict_entries:
                merged: dict = {}
                for entry in dict_entries:
                    merged.update(entry)
                output = merged
            elif str_entries:
                output = {"async_search_results": str_entries[0]}
            else:
                output = {}
        fragment = output.get("async_search_results") or output.get("results")
        if not isinstance(fragment, str) or not fragment.strip():
            raise CloseSpider("Etsy Neu Spec API returned no async_search_results fragment")

        items = list(self._parse_cards(fragment, response.meta["category"], page))
        if not items:
            raise CloseSpider("Etsy Neu Spec API fragment contained no product cards")
        yield from items

        if page < self.max_pages and len(items) >= self.page_size:
            yield self._api_request(response.meta["category_url"], page + 1)

    def _parse_cards(self, fragment: str, category: str, page: int):
        selector = Selector(text=fragment)
        cards = selector.css("[data-listing-id]")
        unique_cards = []
        seen_here = set()
        for card in cards:
            item_id = card.attrib.get("data-listing-id")
            if item_id and item_id not in seen_here:
                seen_here.add(item_id)
                unique_cards.append(card)

        for offset, card in enumerate(unique_cards, 1):
            item_id = card.attrib["data-listing-id"]
            if item_id in self._seen:
                continue
            self._seen.add(item_id)
            link = card.css("a[href*='/listing/']::attr(href)").get()
            price = self._number(card.css(".currency-value::text").get())
            original = self._number(card.css(".wt-text-strikethrough .currency-value::text").get())
            review_text = " ".join(card.css("[class*='rating'] ::text, [class*='review'] ::text").getall())
            rating = self._number(card.css("input[name='rating']::attr(value)").get())
            reviews = self._integer(review_text)
            text = " ".join(card.css("::text").getall())
            yield {
                "item_id": item_id,
                "shop_id": card.attrib.get("data-shop-id"),
                "title": self._clean(card.css("h3::text").get() or card.css("a[title]::attr(title)").get()),
                "shop": self._clean(card.css("[data-seller-name-container]::text").get()),
                "url": link.split("?")[0] if link else None,
                "image": card.css("img::attr(src)").get(),
                "price": price,
                "original_price": original,
                "currency": "USD",
                "rating": rating,
                "reviews_count": reviews,
                "is_ad": "Ad by" in text,
                "free_shipping": "FREE shipping" in text,
                "category": category,
                "page": page,
                "position": (page - 1) * self.page_size + offset,
                "source": "etsy_neu_search_api",
                "raw": {"listing_id": item_id, "shop_id": card.attrib.get("data-shop-id")},
            }

    @staticmethod
    def _clean(value):
        return " ".join((value or "").split()) or None

    @staticmethod
    def _number(value):
        if value is None:
            return None
        match = re.search(r"[\d,.]+", value)
        return float(match.group().replace(",", "")) if match else None

    @staticmethod
    def _integer(value):
        match = re.search(r"\(([\d,.]+)([kKmM]?)\)", value or "")
        if not match:
            return None
        number = float(match.group(1).replace(",", ""))
        multiplier = {"k": 1_000, "m": 1_000_000}.get(match.group(2).lower(), 1)
        return int(number * multiplier)
