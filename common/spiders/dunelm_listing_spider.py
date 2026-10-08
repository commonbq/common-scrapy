from __future__ import annotations

"""Dunelm listings from the server-rendered Redux product bootstrap."""

import json
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.dunelm_categories import CATEGORIES


class DunelmListingSpider(BaseListingSpider):
    name = "dunelm_listing"
    allowed_domains = ["dunelm.com", "www.dunelm.com"]
    categories = [
        {"category": category, "url": url} for category, url in CATEGORIES.items()
    ]

    custom_settings = {
        "PROXY": "",
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.25,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "url", "image",
            "price", "price_min", "price_max", "was_price_min", "was_price_max",
            "currency", "rating", "reviews_count", "colors", "taxonomy",
            "primary_web_category", "sku_ids", "sku_count",
            "click_and_collect_eligible", "is_bundle", "sticker", "page",
            "listing_url", "inventory_total", "total_pages", "source", "raw",
            "timestamp",
        ],
    }

    def start_requests(self):
        yield scrapy.Request(
            self.resolve_target_url(),
            callback=self.parse_listing,
            meta={"page": 1, "discovery_depth": 0},
        )

    def parse_listing(self, response):
        page = int(response.meta.get("page", 1))
        state = self._extract_state(response)
        products, search = self._products_and_search(state)

        if not products and page == 1 and response.meta.get("discovery_depth", 0) < 2:
            leaf_url = self._first_leaf_url(response)
            if leaf_url:
                self.logger.info("No product bootstrap; following leaf PLP %s", leaf_url)
                yield scrapy.Request(
                    leaf_url,
                    callback=self.parse_listing,
                    meta={"page": 1, "discovery_depth": response.meta["discovery_depth"] + 1},
                )
                return

        if not products:
            self.logger.warning(
                "Dunelm bootstrap contained no products: status=%s url=%s",
                response.status,
                response.url,
            )
            return

        result = search.get("res") or {}
        hit_order = {
            str(hit.get("productId")): (index, str(hit.get("mostRelevantSkuId") or ""))
            for index, hit in enumerate(result.get("hits") or [])
        }
        ordered_products = sorted(
            products.values(),
            key=lambda product: hit_order.get(str(product.get("id")), (len(products), ""))[0],
        )
        for product in ordered_products:
            relevant_sku = hit_order.get(str(product.get("id")), (0, ""))[1]
            yield self._item_from_product(
                product,
                relevant_sku_id=relevant_sku,
                state=state,
                page=page,
                listing_url=response.url,
                search_result=result,
            )

        total_pages = int(result.get("nbPages") or 1)
        if page < min(self.max_pages, total_pages):
            yield scrapy.Request(
                self._with_page(response.url, page + 1),
                callback=self.parse_listing,
                meta={"page": page + 1, "discovery_depth": 2},
            )

    @staticmethod
    def _extract_state(response) -> dict:
        text = response.css("#ssr-state-data::text").get()
        if not text:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _products_and_search(state: dict) -> tuple[dict, dict]:
        redux = state.get("reduxState") or {}
        products = (redux.get("product") or {}).get("partialProductById") or {}
        searches = (redux.get("searchProduct") or {}).get("results") or []
        search = searches[0] if searches else {}
        return products, search

    def _first_leaf_url(self, response) -> str | None:
        root_path = urlparse(self.resolve_target_url()).path.rstrip("/") + "/"
        candidates = set()
        for href in response.css('a[href*="/category/"]::attr(href)').getall():
            url = response.urljoin(href).split("#", 1)[0].split("?", 1)[0]
            path = urlparse(url).path
            if path.startswith(root_path) and path.rstrip("/") != root_path.rstrip("/"):
                candidates.add(url)
        return min(candidates, key=lambda url: (urlparse(url).path.count("/"), len(url))) if candidates else None

    def _item_from_product(
        self, product, *, relevant_sku_id, state, page, listing_url, search_result
    ):
        skus = product.get("skus") or []
        sku = next(
            (entry for entry in skus if str(entry.get("id")) == relevant_sku_id),
            skus[0] if skus else {},
        )
        price_range = product.get("priceRange") or {}
        current_price = (sku.get("price") or {}).get("current")
        image_name = ((sku.get("media") or {}).get("image") or [None])[0]
        image_cdn = (
            ((state.get("reduxState") or {}).get("config") or {}).get("imagesCDNUrl")
            or "https://images.dunelm.com"
        ).rstrip("/")
        taxonomy = [entry.get("label") for entry in product.get("category") or [] if entry.get("label")]
        product_slug = str(product.get("productUrl") or "").lstrip("/")
        return {
            "category": self.category,
            "item_id": str(product.get("id") or ""),
            "title": product.get("name"),
            "brand": product.get("brand"),
            "url": f"https://www.dunelm.com/product/{product_slug}" if product_slug else None,
            "image": f"{image_cdn}/{image_name}" if image_name else None,
            "price": current_price if current_price is not None else price_range.get("min"),
            "price_min": price_range.get("min"),
            "price_max": price_range.get("max"),
            "was_price_min": price_range.get("wasMin"),
            "was_price_max": price_range.get("wasMax"),
            "currency": "GBP",
            "rating": product.get("rating"),
            "reviews_count": product.get("totalReviewCount") or sku.get("totalReviewCount"),
            "colors": product.get("colors") or [],
            "taxonomy": taxonomy,
            "primary_web_category": product.get("primaryWebCategory"),
            "sku_ids": [str(entry.get("id")) for entry in skus if entry.get("id")],
            "sku_count": product.get("skuCount") or sku.get("skuCount") or len(skus),
            "click_and_collect_eligible": sku.get("clickAndCollectEligible"),
            "is_bundle": product.get("isBundle"),
            "sticker": product.get("sticker"),
            "page": page,
            "listing_url": listing_url,
            "inventory_total": search_result.get("nbHits"),
            "total_pages": search_result.get("nbPages"),
            "source": "dunelm_redux_ssr_bootstrap",
            "raw": product,
            "timestamp": self.get_timestamp(),
        }

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunparse(parts._replace(query=urlencode(query)))

