from __future__ import annotations

"""Target category/listing spider using Target's RedSky API."""

import html
import json
import re
from typing import Iterable, Optional
from urllib.parse import quote

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


TARGET_CATEGORIES = {
    "grocery": {
        "all": "https://www.target.com/c/grocery/-/N-5xt1a",
        "bakery-bread": "https://www.target.com/c/bakery-bread-grocery/-/N-5xt19",
        "beverages": "https://www.target.com/c/beverages-grocery/-/N-5xt0r",
        "breakfast-cereal": "https://www.target.com/c/breakfast-cereal-grocery/-/N-wo2mp",
        "candy": "https://www.target.com/c/candy-grocery/-/N-5xt0d",
        "coffee": "https://www.target.com/c/coffee-beverages-grocery/-/N-4yi5p",
        "dairy-eggs-cheese": "https://www.target.com/c/dairy-eggs-cheese-grocery/-/N-5xszm",
        "deli": "https://www.target.com/c/deli-grocery/-/N-5hp74",
        "fresh-meat-seafood": "https://www.target.com/c/fresh-meat-seafood-grocery/-/N-5xsyh",
        "frozen-foods": "https://www.target.com/c/frozen-foods-grocery/-/N-5xszd",
        "pantry": "https://www.target.com/c/pantry-grocery/-/N-5xt13",
        "produce": "https://www.target.com/c/produce-grocery/-/N-u7fty",
        "snacks": "https://www.target.com/c/snacks-grocery/-/N-5xsy9",
        "wine-beer-liquor": "https://www.target.com/c/wine-beer-liquor-beverages/-/N-5n5q6",
    },
    "women": {"all": "https://www.target.com/c/women/-/N-5xtd3"},
    "men": {"all": "https://www.target.com/c/men/-/N-18y1l"},
    "kids": {"all": "https://www.target.com/c/kids/-/N-xcoz4"},
    "baby": {"all": "https://www.target.com/c/baby/-/N-5xtly"},
    "home": {"all": "https://www.target.com/c/home/-/N-5xtvd"},
    "kitchen-dining": {"all": "https://www.target.com/c/kitchen-dining/-/N-hz89j"},
    "patio-garden": {"all": "https://www.target.com/c/patio-lawn-garden/-/N-5xtq9"},
    "beauty": {"all": "https://www.target.com/c/beauty/-/N-55r1x"},
    "personal-care": {"all": "https://www.target.com/c/personal-care/-/N-5xtzq"},
    "health": {"all": "https://www.target.com/c/health/-/N-5xu1n"},
    "household-essentials": {"all": "https://www.target.com/c/household-essentials/-/N-5xsz1"},
    "pets": {"all": "https://www.target.com/c/pets/-/N-5xt44"},
    "toys": {"all": "https://www.target.com/c/toys/-/N-5xtb0"},
    "electronics": {"all": "https://www.target.com/c/electronics/-/N-5xtg6"},
    "video-games": {"all": "https://www.target.com/c/video-games/-/N-5xtg5"},
    "sports-outdoors": {"all": "https://www.target.com/c/sports-outdoors/-/N-5xt85"},
    "school-office": {"all": "https://www.target.com/c/school-office-supplies/-/N-5xsxr"},
    "movies-music-books": {"all": "https://www.target.com/c/movies-music-books/-/N-5xsxe"},
    "gift-cards": {"all": "https://www.target.com/c/gift-cards/-/N-5xsxu"},
    "clearance": {"all": "https://www.target.com/c/clearance/-/N-5q0ga"},
}


class TargetListingSpider(BaseListingSpider):
    require_category_arg = False
    page_size = 24
    _redsky_key: Optional[str] = None
    _visitor_id: Optional[str] = None
    """Target category/search spider using Target's internal (RedSky) API.

    Required:
    - Provide a category, either as `-a category=5xtc0` (Target category id),
      or `-a category_url='https://www.target.com/c/women-s-shoes/-/N-5xtc0'`.

    Optional:
    - `-a keyword=<term>` to combine keyword search within a category.
    """

    name = "target_listing"
    allowed_domains = ["target.com", "www.target.com", "redsky.target.com"]

    categories = TARGET_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "product_id",
            "name",
            "brand",
            "price",
            "original_price",
            "currency",
            "url",
            "image",
            "rating",
            "reviews_count",
            "category",
            "subcategory",
            "page",
            "source",
            "raw",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def _selected_categories(self) -> dict[str, str]:
        if self.category in self.categories:
            return self.categories[self.category]
        available = ", ".join(self.available_categories())
        raise ValueError(
            f"Unknown category '{self.category}'. Available categories: {available}"
        )

    def start_requests(self) -> Iterable[scrapy.Request]:
        # Use a category page as referer/seed. If the user didn't provide a URL,
        # we build a minimal one.
        if not self.category and self.category_url:
            m = re.search(r"/N-([a-z0-9]+)", self.category_url, flags=re.I)
            if m:
                self.category = m.group(1)

        if self.category_url:
            category_id = self._category_id(self.category_url)
            if not category_id:
                raise ValueError("category_url must contain a Target /N-<category id> path")
            self.category = self.category or category_id
            yield self._seed_request(
                self.category_url, category_id, self.category, "custom"
            )
            return

        # Preserve direct Target category IDs while making the documented names
        # expand to every configured child category.
        if (
            self.category
            and self.category not in self.categories
            and re.fullmatch(r"[a-z0-9]+", self.category, flags=re.I)
        ):
            url = f"https://www.target.com/c/-/N-{quote(self.category)}"
            yield self._seed_request(url, self.category, self.category, "all")
            return

        for subcategory, url in self._selected_categories().items():
            yield self._seed_request(
                url, self._category_id(url), self.category, subcategory
            )

    def _seed_request(self, url, category_id, category, subcategory):
        request = self._make_request(url, cb="parse_search_html", dont_filter=True)
        request.meta.update(
            category_id=category_id,
            category=category,
            subcategory=subcategory,
            page=1,
            listing_url=url,
        )
        return request

    @staticmethod
    def _category_id(url: str) -> str | None:
        match = re.search(r"/N-([^/?#]+)", url, flags=re.I)
        return match.group(1) if match else None

    def _make_request(self, url: str, *, cb: str, dont_filter: bool = False) -> scrapy.Request:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        return scrapy.Request(
            url,
            headers=headers,
            meta={"handle_httpstatus_all": True, "disable_proxy": True},
            callback=getattr(self, cb),
            dont_filter=dont_filter,
        )

    def _make_redsky_request(self, *, offset: int, meta: dict | None = None) -> scrapy.Request:
        assert self._redsky_key
        base = "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"

        page_path = None
        listing_url = (meta or {}).get("listing_url") or self.category_url
        if listing_url:
            page_path = re.sub(r"^https?://www\.target\.com", "", listing_url)
        if not page_path:
            page_path = f"/c/-/N-{self.category}"

        params = {
            "key": self._redsky_key,
            "channel": "WEB",
            "count": str(self.page_size),
            "offset": str(offset),
            "page": page_path,
            "pricing_store_id": "3991",
            "visitor_id": self._ensure_visitor_id(),
            "category": (meta or {}).get("category_id") or self.category,
        }
        keyword = getattr(self, "keyword", None)
        if keyword:
            params["keyword"] = keyword
        qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        url = f"{base}?{qs}"

        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "referer": (listing_url or f"https://www.target.com/c/-/N-{quote(self.category)}"),
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

        return scrapy.Request(
            url,
            headers=headers,
            meta={**(meta or {}), "handle_httpstatus_all": True, "disable_proxy": True},
            callback=self.parse_redsky,
            dont_filter=True,
        )

    def _ensure_visitor_id(self) -> str:
        if not self._visitor_id:
            import uuid

            self._visitor_id = str(uuid.uuid4())
        return self._visitor_id

    def parse_search_html(self, response: scrapy.http.Response):
        if response.status != 200:
            self.logger.warning(
                "Target search HTML non-200. status=%s url=%s head=%r",
                response.status,
                response.url,
                (response.text or "")[:200],
            )

        html = response.text or ""

        keys = re.findall(r"\bkey=([a-f0-9]{32})\b", html, flags=re.I)
        key = keys[0] if keys else None
        if not key:
            keys = re.findall(r'"key"\s*:\s*"([a-f0-9]{32})"', html, flags=re.I)
            key = keys[0] if keys else None
        if not key:
            # Recent Target pages embed the RedSky key inside escaped bootstrap
            # JSON as apiKey, often as a longer token where the first 32 hex
            # chars are the plp_search_v2 key.
            keys = re.findall(r'apiKey\\":\\"([a-f0-9]{32,64})', html, flags=re.I)
            if keys:
                key = keys[0][:32]

        if not key:
            self.logger.warning(
                "Could not discover Target RedSky key from HTML; trying known fallback key"
            )
            key = "9f36aeafbe60771e321a7cc95a781407"

        self._redsky_key = key
        yield self._make_redsky_request(offset=0, meta=response.meta)

    def parse_redsky(self, response: scrapy.http.Response):
        if response.status != 200:
            self.logger.warning(
                "RedSky non-200. status=%s url=%s head=%r",
                response.status,
                response.url,
                (response.text or "")[:250],
            )
            return

        try:
            data = json.loads(response.text)
        except Exception:
            self.logger.exception("Failed to parse RedSky JSON")
            return

        products = (
            (((data.get("data") or {}).get("search") or {}).get("products"))
            or (((data.get("data") or {}).get("search") or {}).get("items"))
        )
        if not isinstance(products, list):
            self.logger.warning(
                "Unexpected RedSky shape. top_keys=%s", list(data.keys())[:20]
            )
            return

        for p in products:
            if isinstance(p, dict):
                item = self._normalize_product(p)
                product_id = item.get("product_id")
                if product_id and product_id in self._seen_products:
                    continue
                if product_id:
                    self._seen_products.add(product_id)
                yield {
                    **item,
                    "category": response.meta.get("category"),
                    "subcategory": response.meta.get("subcategory"),
                    "page": response.meta.get("page", 1),
                    "source": "target_redsky_plp_search_v2",
                }

        m = re.search(r"[?&]offset=(\d+)", response.url)
        offset = int(m.group(1)) if m else 0

        search = (data.get("data") or {}).get("search") or {}
        total = (
            search.get("search_response")
            and search["search_response"].get("typed_metadata", {}).get("total_results")
        )
        if total is None:
            total = search.get("total_results") or search.get("total")

        next_offset = offset + self.page_size
        current_page = (offset // self.page_size) + 1

        if self.max_pages and current_page >= self.max_pages:
            return
        if isinstance(total, int) and next_offset >= total:
            return

        yield self._make_redsky_request(
            offset=next_offset,
            meta={**response.meta, "page": current_page + 1},
        )

    def _normalize_product(self, p: dict) -> dict:
        item = p.get("item") or {}
        pd = item.get("product_description") or {}

        title = p.get("title") or p.get("product_title") or p.get("name") or pd.get("title")
        if isinstance(title, str):
            title = html.unescape(title)
        tcin = p.get("tcin") or p.get("id")

        price = None
        original_price = None
        currency = None
        price_block = p.get("price") or p.get("pricing") or {}
        if isinstance(price_block, dict):
            price = (
                price_block.get("formatted_current_price")
                or price_block.get("current_retail")
                or price_block.get("current")
                or price_block.get("value")
            )
            original_price = price_block.get(
                "formatted_comparison_price"
            ) or price_block.get("reg_retail")
            currency = (
                price_block.get("currency")
                or price_block.get("currency_code")
                or "USD"
            )

        url = p.get("url") or (item.get("enrichment") or {}).get("buy_url")
        if url and url.startswith("/"):
            url = "https://www.target.com" + url

        image = None
        images = p.get("images") or p.get("image") or {}
        if isinstance(images, dict):
            image = images.get("primary_uri") or images.get("base_url")

        if not image and isinstance(item, dict):
            enrichment = item.get("enrichment") or {}
            imgs = enrichment.get("images")
            if isinstance(imgs, dict):
                image = imgs.get("primary_image_url") or (imgs.get("alternate_image_urls") or [None])[0]
            elif isinstance(imgs, list) and imgs:
                first = imgs[0]
                if isinstance(first, dict):
                    image = first.get("url") or first.get("base_url")

        primary_brand = item.get("primary_brand") or {}
        brand = (
            primary_brand.get("name")
            if isinstance(primary_brand, dict)
            else primary_brand
        )

        return {
            "product_id": tcin,
            "name": title,
            "brand": p.get("brand") or brand,
            "price": price,
            "original_price": original_price,
            "currency": currency,
            "url": url,
            "image": image,
            "rating": p.get("average_rating") or p.get("rating"),
            "reviews_count": p.get("total_reviews") or p.get("review_count"),
            "raw": p,
        }
