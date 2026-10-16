from __future__ import annotations

"""Nordstrom Rack listings from the server-rendered product state.

The category inventory (grouped ``{department: {leaf: url}}``) comes from the
site's own ``navigation-sitemap.xml``; see
:mod:`common.spiders.nordstromrack_categories`.

Routing
-------
On the default datacenter and on the premium route ``nordstromrack.com``
answers the category page with an HTTP-200 anti-bot stub (~250 KB, no product
data, ``window['istlWasHere']`` challenge) or a tiny ScrapeOps failure
envelope. The real ~4.8 MB server-rendered document only arrives on the US
residential route (``country=us,residential=true``).

Product source
--------------
The category page ships its whole result grid in one hydration script::

    <script>window.__INITIAL_CONFIG__ = {"...": ...}</script>

and the products live at ``productResults.productsById`` (keyed by product id).
The spider reads that object first; the older Schema.org ``ItemList`` JSON-LD
block is kept as a fallback so a captured fixture from either era keeps
parsing. When neither is present the response is an anti-bot / proxy stub, not
a product listing, and the spider says so instead of emitting an empty run.
"""

import json
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.nordstromrack_categories import NORDSTROMRACK_CATEGORIES

# The residential pool is not perfectly reliable: some requests still come back
# as a ScrapeOps failure envelope (HTTP 200, 367-byte JSON). Deterministic
# failures are invisible to Scrapy's RetryMiddleware because the status is 200,
# so the spider re-requests a bounded number of times itself.
MAX_PROXY_RETRIES = 3

# Matches ``window.__INITIAL_CONFIG__ = { ... }`` up to the closing script tag.
_INITIAL_CONFIG_RE = re.compile(r"window\.__INITIAL_CONFIG__\s*=\s*")
_SCRIPT_END = "</script>"


class NordstromrackListingSpider(BaseListingSpider):
    name = "nordstromrack_listing"
    allowed_domains = ["nordstromrack.com", "www.nordstromrack.com", "127.0.0.1"]
    require_category_arg = False
    categories = NORDSTROMRACK_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "brand", "price", "price_max", "currency",
            "availability", "url", "image_url", "category", "page", "position",
            "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<leaf>. Available categories: "
                f"{', '.join(self.available_categories())}"
            )
        if not (self.url or self.category_url) and self.category_entry(self.category) is None:
            raise ValueError(
                f"Unknown category {self.category!r}. Available categories: "
                f"{', '.join(self.available_categories())}"
            )
        self._seen: set[str] = set()

    def start_requests(self):
        url = self.url or self.category_url
        if not url:
            entry = self.category_entry(self.category)
            url = entry.get("url")
        yield self._listing_request(url, self.category, 1)

    def _listing_request(self, url, category, page: int, retries: int = 0):
        return scrapy.Request(
            self._page_url(url, page),
            callback=self.parse,
            errback=self._on_error,
            headers=self._headers(),
            meta={
                "category": category,
                "page": page,
                "listing_url": url,
                "proxy_retries": retries,
            },
            dont_filter=True,
        )

    def _on_error(self, failure):
        """Retry a bounded number of times, then surface the failure."""
        request = failure.request
        retries = int(request.meta.get("proxy_retries", 0))
        if retries < MAX_PROXY_RETRIES:
            self.logger.warning(
                "Nordstrom Rack request failed (%s); retrying %s/%s: %s",
                failure.value, retries + 1, MAX_PROXY_RETRIES, request.url,
            )
            yield self._listing_request(
                request.meta.get("listing_url"), request.meta.get("category"),
                int(request.meta.get("page", 1)), retries + 1,
            )
        else:
            self.logger.error(
                "Nordstrom Rack request failed after %s attempts: %s (%s)",
                MAX_PROXY_RETRIES + 1, request.url, failure.value,
            )

    def parse(self, response):
        if self._is_proxy_payload(response):
            retries = int(response.meta.get("proxy_retries", 0))
            if retries < MAX_PROXY_RETRIES:
                self.logger.warning(
                    "Nordstrom Rack proxy envelope (%s); retrying %s/%s: %s",
                    response.text[:80], retries + 1, MAX_PROXY_RETRIES, response.url,
                )
                yield self._listing_request(
                    response.meta.get("listing_url"), response.meta.get("category"),
                    int(response.meta.get("page", 1)), retries + 1,
                )
                return
            raise RuntimeError(
                f"Nordstrom Rack {response.url} did not return an HTML document "
                f"after {MAX_PROXY_RETRIES + 1} attempts (body starts "
                f"{response.text[:120]!r}); the response is a proxy/challenge "
                "payload, not a product listing"
            )
        if response.status != 200:
            self.logger.error(
                "Nordstrom Rack listing returned HTTP %s: %s",
                response.status, response.url,
            )
            return

        page = int(response.meta.get("page", 1))
        products = self._products(response)
        if not products:
            self.logger.error(
                "Nordstrom Rack product grid missing: status=%s bytes=%s url=%s",
                response.status, len(response.body), response.url,
            )
            return
        for position, product in products:
            item = self._item(product, response, page, position)
            if item is None:
                continue
            yield item
        if page < self.max_pages:
            yield self._listing_request(
                response.meta["listing_url"], response.meta["category"], page + 1,
            )

    # ------------------------------------------------------------------ parsing

    def _item(self, product: dict, response, page: int, position: int) -> dict | None:
        """Map either a JSON-LD ``Product`` or an ``INITIAL_CONFIG`` product."""
        if product.get("@type") == "Product":
            return self._item_from_jsonld(product, response, page, position)
        return self._item_from_config(product, response, page, position)

    def _item_from_config(self, product: dict, response, page: int, position: int) -> dict | None:
        item_id = str(product.get("id") or "")
        if not item_id or item_id in self._seen:
            return None
        self._seen.add(item_id)
        propositions = product.get("propositions") or [{}]
        prop = propositions[0] if isinstance(propositions, list) and propositions else {}
        sell = prop.get("sellingRetailPriceRange") or {}
        compare = prop.get("compareAtRetailPriceRange") or {}
        return {
            "item_id": item_id,
            "title": product.get("copyProductTitle") or product.get("name"),
            "brand": product.get("labelDisplayName"),
            "price": self._number(sell.get("min")),
            "price_max": self._number(sell.get("max")) or self._number(compare.get("max")),
            "currency": "USD",
            "availability": self._availability(prop),
            "url": self._product_url(product, response),
            "image_url": self._config_image(product),
            "category": response.meta["category"],
            "page": page,
            "position": position,
            "source": "nordstromrack_initial_config",
            "raw": product,
        }

    def _item_from_jsonld(self, product: dict, response, page: int, position: int) -> dict | None:
        offers = product.get("offers") or {}
        brand = product.get("brand") or {}
        item_id = str(product.get("sku") or product.get("productID") or product.get("url") or "")
        if not item_id or item_id in self._seen:
            return None
        self._seen.add(item_id)
        image = product.get("image")
        return {
            "item_id": item_id,
            "title": product.get("name"),
            "brand": brand.get("name") if isinstance(brand, dict) else brand,
            "price": self._number(offers.get("lowPrice") or offers.get("price")),
            "price_max": self._number(offers.get("highPrice")),
            "currency": offers.get("priceCurrency"),
            "availability": (offers.get("availability") or "").rsplit("/", 1)[-1] or None,
            "url": response.urljoin(product.get("url")) if product.get("url") else None,
            "image_url": image[0] if isinstance(image, list) and image else image,
            "category": response.meta["category"],
            "page": page,
            "position": position,
            "source": "nordstromrack_itemlist_json_ld",
            "raw": product,
        }

    @staticmethod
    def _availability(prop: dict) -> str | None:
        salability = prop.get("salability") or {}
        status = salability.get("status")
        return status.title() if isinstance(status, str) and status else None

    @staticmethod
    def _config_image(product: dict) -> str | None:
        for core in product.get("coreProducts") or []:
            for choice in core.get("coreChoices") or []:
                for shot in choice.get("orderedShots") or []:
                    url = shot.get("imageUrl")
                    if url:
                        return url
        return None

    @staticmethod
    def _product_url(product: dict, response) -> str | None:
        alias = product.get("webPathAlias")
        item_id = product.get("id")
        if alias and item_id:
            return response.urljoin(f"/s/{alias}/{item_id}")
        return None

    def _products(self, response):
        """Return ``(position, product)`` pairs from the richest available source."""
        products = self._products_from_config(response)
        if products:
            return products
        return self._products_from_jsonld(response)

    @staticmethod
    def _products_from_config(response) -> list[tuple[int, dict]]:
        data = NordstromrackListingSpider._initial_config(response)
        if not data:
            return []
        by_id = ((data.get("productResults") or {}).get("productsById")) or {}
        if not isinstance(by_id, dict):
            return []
        return [
            (index, product)
            for index, product in enumerate(by_id.values(), 1)
            if isinstance(product, dict)
        ]

    @staticmethod
    def _products_from_jsonld(response) -> list[tuple[int, dict]]:
        found = []
        for raw in response.css('script[type="application/ld+json"]::text').getall():
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            nodes = data.get("@graph", []) if isinstance(data, dict) else []
            nodes = [data, *nodes] if isinstance(data, dict) else data if isinstance(data, list) else []
            for node in nodes:
                if not isinstance(node, dict) or node.get("@type") not in ("ItemList", "CollectionPage"):
                    continue
                entries = node.get("itemListElement") or (node.get("mainEntity") or {}).get("itemListElement") or []
                for index, entry in enumerate(entries, 1):
                    product = entry.get("item") if isinstance(entry, dict) else None
                    if isinstance(product, dict):
                        found.append((entry.get("position") or index, product))
        return found

    @staticmethod
    def _initial_config(response) -> dict | None:
        """Parse ``window.__INITIAL_CONFIG__`` out of the document, if present."""
        text = response.text
        match = _INITIAL_CONFIG_RE.search(text)
        if not match:
            return None
        start = match.end()
        end = text.find(_SCRIPT_END, start)
        if end == -1:
            end = len(text)
        raw = text[start:end].strip().rstrip(";").strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    def _is_proxy_payload(self, response: scrapy.http.Response) -> bool:
        """True when the body is a proxy/challenge payload, not a document."""
        if response.status != 200:
            return False
        content_type = (response.headers.get("Content-Type") or b"").decode(
            "utf-8", "replace"
        ).lower()
        if "html" in content_type:
            return False
        head = response.text.lstrip()
        if head.startswith("<"):
            return False
        # A ScrapeOps failure envelope is a small JSON object, not a page.
        return True

    @staticmethod
    def _page_url(url, page):
        parts = urlsplit(url); query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if page > 1: query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _number(value):
        try: return float(value) if value not in (None, "") else None
        except (TypeError, ValueError): return None

    @staticmethod
    def _headers():
        return {"accept": "text/html,application/xhtml+xml", "accept-language": "en-US,en;q=0.9",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"}
