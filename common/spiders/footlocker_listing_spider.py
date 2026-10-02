from __future__ import annotations

import json
import re
import time
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
# from common.spiders.footlocker_categories import FOOTLOCKER_CATEGORIES # Will be fetched dynamically

SITE_BASE = "https://www.footlocker.com"
API_BASE = "https://www.footlocker.com/zgw/search-core/products/v3/search"
PAGE_SIZE = 48

# ScrapeOps option appended to the proxy username for the Akamai-protected
# /zgw API host. The plain route and lower bypass levels returned 403 or
# the Foot Locker EU HTML stub; ``residential=true`` works.
RESIDENTIAL_PROXY = "residential=true"

_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")

def _slugify(value: str) -> str:
    return _SLUG_CLEAN_RE.sub("-", value.lower()).strip("-")

def _iter_nav_nodes(tree: dict[str, Any]):
    # This expects a dictionary structure where each value is a dictionary
    # representing a band, then sub_category, then link.
    # e.g., {"New & Trending": {"New Arrivals": {"All New Arrivals": "/url"}}}
    for band_name, band_contents in tree.items():
        # Skip 'Promo Images' bands as they are not product categories
        if 'Promo Images' in band_name:
            continue
        for sub_name, sub_contents in band_contents.items():
            if 'Promo Images' in sub_name:
                continue
            for link_name, url in sub_contents.items():
                if not url: # Skip empty URLs
                    continue
                # Filter out external links like to footlocker.eu or other domains
                if not url.startswith("/") and not url.startswith(SITE_BASE):
                    continue 
                yield {
                    "band": band_name.strip(),
                    "sub_category": sub_name.strip(),
                    "name": link_name.strip(),
                    "url": url.strip(),
                }

class FootlockerListingSpider(BaseListingSpider):
    name = "footlocker_listing"
    allowed_domains = [
        "footlocker.com",
        "www.footlocker.com",
    ]
    require_category_arg = False # Will be overridden after category resolution

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25, # Be gentle for HTML requests
        "FEED_EXPORT_FIELDS": [
            "band",
            "sub_category",
            "category", # This will be the category_slug
            "item_id",
            "title",
            "url",
            "image_url",
            "price",
            "original_price",
            "currency",
            "availability",
            "brand",
            "rating",
            "reviews_count",
            "page",
            "category_url", # The URL of the category page
            "source", # API for this spider
            "raw", # Unmodified product dict from API
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # _categories_to_resolve will be populated from header.public.json
        self._categories_to_resolve: list[dict[str, Any]] = [] 
        self._resolved_categories: list[dict[str, Any]] = []
        self._category_resolution_in_progress = False

    def start_requests(self):
        # Stage 0: Initial setup - fetch categories from header.public.json
        if not self._categories_to_resolve and not self._category_resolution_in_progress:
            self._category_resolution_in_progress = True
            self.logger.info("Fetching categories from header.public.json...")
            yield scrapy.Request(
                urljoin(SITE_BASE, "/api/content/en/header.public.json"),
                callback=self.parse_header_json_for_categories,
                meta={'proxy': self._search_api_proxy(plain=True)} # Use plain proxy for header.json
            )
        elif self._category_resolution_in_progress:
            # Stage 1: Resolve searchParams for all categories
            yield from self._resolve_category_search_params()
        else:
            # Stage 2: Start API crawls using resolved categories
            yield from self._start_api_crawls()

    def parse_header_json_for_categories(self, response: scrapy.http.Response):
        # Expecting JSON response
        data = json.loads(response.text)
        # The structure is data["page"]["components"][N]["list"][M]["categories"]
        # So we need to dig into the structure.
        # Issue summary shows structure where "New & Trending" is a top-level key.
        # Let's rebuild that structure from data["page"]["components"]
        rebuilt_tree = {}
        for component in data.get("page", {}).get("components", []):
            if component.get("type") == "header_section":
                for section_item in component.get("list", []):
                    if section_item.get("type") == "headerCategory":
                        band_name = section_item.get("name")
                        if band_name:
                            rebuilt_tree[band_name] = {}
                            for cat_item in section_item.get("categories", {}).get("list", []):
                                sub_name = cat_item.get("name")
                                if sub_name:
                                    rebuilt_tree[band_name][sub_name] = {}
                                    for link_item in cat_item.get("links", {}).get("list", []):
                                        link_name = link_item.get("text")
                                        link_url = link_item.get("url")
                                        if link_name and link_url:
                                            rebuilt_tree[band_name][sub_name][link_name] = link_url
        
        # Now populate _categories_to_resolve from the rebuilt tree
        for entry in _iter_nav_nodes(rebuilt_tree):
            self._categories_to_resolve.append(entry)
        
        # Now initiate the searchParams resolution stage
        self._category_resolution_in_progress = True # Indicate that we are moving to next stage
        yield from self._resolve_category_search_params()

    def _resolve_category_search_params(self):
        self.logger.info(f"Starting category searchParams resolution for {len(self._categories_to_resolve)} categories...")
        requests_sent_count = 0
        for entry in self._categories_to_resolve:
            if "searchParams" in entry:
                continue # Already resolved

            if '?query=' in entry["url"]:
                # Directly extract searchParams from the URL
                query_part = entry["url"].split('?query=', 1)[1]
                entry["searchParams"] = unquote(query_part)
                entry["category_slug"] = _slugify(entry["name"])
                self._resolved_categories.append(entry)
                self.logger.debug(f"Resolved query-based category: {entry['name']} -> {entry['searchParams']}")
            else:
                # Need to fetch HTML to get searchParams
                full_url = urljoin(SITE_BASE, entry["url"])
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_search_params_from_html,
                    meta={'entry': entry, 'dont_merge_cookies': True, 'priority': 100, 'proxy': self._search_api_proxy(plain=True)}
                )
                requests_sent_count += 1
        
        if requests_sent_count == 0 and len(self._resolved_categories) == len(self._categories_to_resolve):
            # All categories were either query-based or previously resolved.
            self._category_resolution_in_progress = False
            yield from self._start_api_crawls()

    def parse_search_params_from_html(self, response: scrapy.http.Response):
        entry = response.meta['entry']
        search_params = self._extract_search_params_from_html(response)
        if search_params:
            entry["searchParams"] = search_params
            entry["category_slug"] = _slugify(entry["name"])
            self._resolved_categories.append(entry)
            self.logger.debug(f"Resolved HTML-based category: {entry['name']} -> {entry['searchParams']}")
        else:
            self.logger.warning(f"Could not resolve searchParams for {entry['url']}")
        
        # Check if all categories have been resolved
        if len(self._resolved_categories) == len(self._categories_to_resolve):
            self._category_resolution_in_progress = False
            yield from self._start_api_crawls()

    def _extract_search_params_from_html(self, response: scrapy.http.Response) -> str | None:
        script_blob = response.xpath('//script[contains(., "window.footlocker = {")]/text()').get()
        if not script_blob:
            return None
        try:
            # Find the window.footlocker = { ... } object
            match = re.search(r"window\.footlocker\\s*=\\s*(\\{.*?\\})\\s*;?", script_blob, re.DOTALL)
            if not match:
                self.logger.warning(f"Could not find window.footlocker state in script for {response.url}")
                return None
            full_js_obj_str = match.group(1)

            # Find STATE_FROM_SERVER within that object
            state_from_server_match = re.search(r"STATE_FROM_SERVER\\s*:\\s*(\\{.*?\\})", full_js_obj_str, re.DOTALL)
            if not state_from_server_match:
                self.logger.warning(f"Could not find STATE_FROM_SERVER within window.footlocker for {response.url}")
                return None
            state_from_server_str = state_from_server_match.group(1)
            state = json.loads(state_from_server_str)
            
            # The key in page.category can vary. Iterate to find a matching one.
            category_map = state.get('page', {}).get('category', {})
            for url_key, details in category_map.items():
                if url_key.split('?')[0] == response.url.split('?')[0]:
                    return details.get("searchParams")
        except Exception as e:
            self.logger.error(f"Error parsing STATE_FROM_SERVER on {response.url}: {e}")
        return None

    def available_categories(self) -> list[str]:
        names: list[str] = []
        for entry in self._resolved_categories:
            if isinstance(entry, dict) and isinstance(entry.get("category_slug"), str):
                names.append(entry["category_slug"])
        return sorted(names)

    def resolve_target_url(self) -> str:
        # For this spider, the initial URL is either a direct category URL for searchParams resolution
        # or the API_BASE for product fetching. This method is mainly used by BaseListingSpider
        # for initial category arg validation, but our start_requests handles the flow.
        if self.args.url:
            return self.args.url
        # If a category is specified, we expect it to be resolved into an entry later.
        # This function might be called early by BaseListingSpider init.
        return SITE_BASE # Placeholder, actual URL will be built in _api_request

    def _start_api_crawls(self):
        self.logger.info("All categories resolved. Starting API crawls...")
        if self.args.category:
            found_entry = None
            for entry in self._resolved_categories:
                if entry["category_slug"] == self.args.category:
                    found_entry = entry
                    break
            if found_entry:
                yield self._api_request(found_entry["searchParams"], found_entry["url"], page=0, metadata=found_entry)
            else:
                raise ValueError(f"Unknown category '{self.args.category}'. Available: {self.available_categories()}")
        elif self.args.url: # If an explicit URL was passed, it should have been resolved already
            # Find the resolved entry for the explicit URL
            found_entry = None
            for entry in self._resolved_categories:
                if entry["url"] == self.args.url:
                    found_entry = entry
                    break
            if found_entry:
                yield self._api_request(found_entry["searchParams"], found_entry["url"], page=0, metadata=found_entry)
            else:
                self.logger.error(f"Could not find resolved searchParams for URL: {self.args.url}. This should not happen.")
        else:
            for entry in self._resolved_categories:
                self.logger.info(f"Starting API crawl for category: {entry['name']} ({entry['category_slug']})")
                yield self._api_request(entry["searchParams"], entry["url"], page=0, metadata=entry)

    def _api_request(self, search_params: str, category_url: str, page: int, metadata: dict[str, Any]):
        api_url = f"{API_BASE}?query={search_params}&pageType=search&pageSize={PAGE_SIZE}&currentPage={page}"
        return scrapy.Request(
            api_url,
            callback=self.parse_api_products,
            headers={
                "X-API-LANG": "en",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
                "Referer": category_url,
                "Origin": SITE_BASE,
            },
            meta={
                "category_url": category_url,
                "search_params": search_params,
                "page": page,
                "proxy": self._search_api_proxy(), # Use residential proxy for API
                "metadata": metadata,
            },
            dont_filter=True,
        )

    def _search_api_proxy(self, plain: bool = False) -> str | None:
        if not hasattr(self, "settings"):
            return None
        proxy = self.settings.get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None

        parts = urlsplit(proxy)
        if parts.hostname != "proxy.scrapeops.io" or not parts.username:
            return proxy

        if plain: # For HTML requests, use plain datacenter proxy
            return proxy

        username = parts.username
        if RESIDENTIAL_PROXY not in username:
            username = f"{username}.{RESIDENTIAL_PROXY}"

        credentials = unquote(username, safe=".:=_") # Unquote first, then re-quote for safety
        if parts.password is not None:
            credentials += f":{unquote(parts.password, safe='')}" # Also unquote password
        
        # The quote/unquote logic for credentials is tricky.
        # Scrapy passes the raw proxy string from settings.
        # If it's already encoded, unquoting might break it.
        # Let's assume proxy from settings is already correctly encoded.
        # Just append the residential part if not present.

        if RESIDENTIAL_PROXY not in parts.username:
            new_username = f"{parts.username}.{RESIDENTIAL_PROXY}"
            # Reconstruct the URL with the modified username
            return urlunsplit((parts.scheme, f"{new_username}:{parts.password}@{parts.hostname}:{parts.port}", parts.path, parts.query, parts.fragment))
        return proxy


    def parse_api_products(self, response: scrapy.http.Response):
        data = json.loads(response.text)
        pagination = data.get("pagination", {})
        products = data.get("products", [])

        category_url = response.meta["category_url"]
        # search_params = response.meta["search_params"] # Not needed for item processing
        current_page = response.meta["page"]
        metadata = response.meta["metadata"]

        if not products:
            self.logger.info(f"No products found for {category_url} (page {current_page})")
            return

        for product in products:
            item = self.new_item()
            item["band"] = metadata["band"]
            item["sub_category"] = metadata["sub_category"]
            item["category"] = metadata["category_slug"] # Use the resolved category_slug
            item["item_id"] = product.get("sku") or product.get("baseProduct")
            item["title"] = product.get("name")
            item["url"] = urljoin(SITE_BASE, f"/product/{item['item_id']}.html")
            image_base = "https://images.footlocker.com/is/image/EBFL2/"
            if product.get("imageSku"):
                item["image_url"] = f"{image_base}{product.get('imageSku')}"
            elif product.get("baseProduct"):
                item["image_url"] = f"{image_base}{product.get('baseProduct')}"
            else:
                item["image_url"] = None

            price_obj = product.get("price", {})
            original_price_obj = product.get("originalPrice", {})
            item["price"] = price_obj.get("value")
            item["original_price"] = original_price_obj.get("value")
            item["currency"] = price_obj.get("currencyIso") or "USD"
            item["availability"] = "InStock" if product.get("isAvailable") else "OutOfStock"
            # Prefer brand from product.brand, else try to extract from title
            item["brand"] = product.get("brand")
            if not item["brand"] and item["title"]:
                first_word = item["title"].split(" ", 1)[0]
                # Simple heuristic: if first word is capitalized, might be a brand
                if first_word and first_word[0].isupper():
                    item["brand"] = first_word

            item["rating"] = product.get("reviewRatings", {}).get("rating")
            item["reviews_count"] = product.get("reviewRatings", {}).get("reviews")
            item["page"] = current_page + 1
            item["category_url"] = category_url
            item["source"] = "footlocker_api"
            item["raw"] = product
            yield item

        total_pages = pagination.get("totalPages")
        if total_pages is not None and current_page + 1 < total_pages and current_page + 1 < self.max_pages:
            yield self._api_request(response.meta["search_params"], category_url, current_page + 1, metadata)
