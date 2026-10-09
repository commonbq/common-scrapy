from __future__ import annotations

import json
import re
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider, group_categories
from common.spiders.petco_categories import PETCO_CATEGORIES


class PetcoListingSpider(BaseListingSpider):
    """Petco category listings from the server-rendered Next.js bootstrap state.

    Petco PLPs are Next.js pages whose `script#__NEXT_DATA__` carries the whole
    first-party Constructor.io response used to paint the grid:

        props.pageProps.pageData.constructorResults.response

    That single object carries the product rows (`results[]`, each with a parent
    `data` block plus its `variations[]`), the category facets (`facets[]`), the
    sub-category groups (`groups[]`), the sort options, the echoed request
    (`page`, `num_results_per_page`, `sort_by`) and `total_num_results`. This
    spider reads only that hydration state: no HTML card scraping, no JSON-LD,
    no secondary request.
    """

    name = "petco_listing"
    allowed_domains = ["petco.com", "www.petco.com", "localhost", "127.0.0.1"]
    categories = group_categories(PETCO_CATEGORIES, "department")
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "subcategory", "category_id", "category_name",
            "breadcrumb_path", "item_id", "title", "brand", "model", "url", "image_url",
            "price", "original_price", "currency", "rating", "reviews_count", "in_stock",
            "bopus_available", "autoship_available", "in_store_only", "rx_item",
            "taxonomy_path", "variants_count", "variant_ids", "facets", "page", "position",
            "total_count", "items_per_page", "sort_by", "sort_order", "search_engine",
            "source_url", "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.iter_categories() if entry["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self._html_headers(),
            meta={
                "category": self.category or "custom",
                "department": selected.get("department"),
                "subcategory": selected.get("subcategory"),
                "page": 1,
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Petco listing returned HTTP {response.status}: {response.url}")

        state = self._extract_next_data(response)
        if not isinstance(state, dict):
            raise RuntimeError(f"No valid Petco __NEXT_DATA__ hydration found at {response.url}")
        page_data = self._page_data(state)
        if not isinstance(page_data, dict):
            raise RuntimeError(f"Petco hydration has no pageProps.pageData at {response.url}")
        results = self._constructor_results(page_data)
        if not isinstance(results, dict):
            raise RuntimeError(
                f"Petco hydration has no pageData.constructorResults.response at {response.url}"
            )

        products = results.get("results")
        if not isinstance(products, list):
            raise RuntimeError(f"Petco Constructor response has no list-valued results at {response.url}")
        if not products:
            raise RuntimeError(f"Petco listing returned zero products at {response.url}")

        request = page_data.get("constructorResults", {}).get("request", {})
        page = self._integer(request.get("page")) or self._integer(response.meta.get("page")) or 1
        for position, product in enumerate(products, start=1):
            data = product.get("data") if isinstance(product, dict) else None
            if not isinstance(data, dict):
                continue
            item_id = str(data.get("catEntryID") or data.get("id") or "")
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield self._item(product, data, page_data, results, request, response, page, position)

        if page >= self.max_pages:
            return
        items_per_page = self._integer(request.get("num_results_per_page")) or len(products)
        total_count = self._integer(results.get("total_num_results")) or 0
        if total_count and page * items_per_page >= total_count:
            return
        yield response.follow(
            self._page_url(response.url, page + 1),
            callback=self.parse,
            headers=self._html_headers(),
            meta={**response.meta, "page": page + 1},
        )

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        """Return `url` with its `page` query parameter set to `page`.

        Petco paginates PLPs with a plain SSR `?page=N`, so the parameter has to
        be replaced (never appended) to keep deeper pages stable.
        """

        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query) if key != "page"]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _extract_next_data(response: scrapy.http.Response) -> dict | None:
        raw = response.css("script#__NEXT_DATA__::text").get()
        if not raw:
            return None
        try:
            value = json.loads(raw)
        except (TypeError, ValueError):
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _page_data(state: dict) -> dict | None:
        props = state.get("props")
        page_props = props.get("pageProps") if isinstance(props, dict) else None
        page_data = page_props.get("pageData") if isinstance(page_props, dict) else None
        return page_data if isinstance(page_data, dict) else None

    @staticmethod
    def _constructor_results(page_data: dict) -> dict | None:
        constructor = page_data.get("constructorResults")
        results = constructor.get("response") if isinstance(constructor, dict) else None
        return results if isinstance(results, dict) else None

    def _item(self, product, data, page_data, results, request, response, page, position):
        variations = [v for v in product.get("variations", []) if isinstance(v, dict)]
        facets = {}
        for facet in data.get("facets", []) or []:
            if not isinstance(facet, dict):
                continue
            name = facet.get("name")
            values = facet.get("values")
            if name and isinstance(values, list) and values:
                facets[name] = list(values)

        price = self._number(data.get("rdprice"))
        original_price = self._number(data.get("listprice"))
        title = product.get("value") or data.get("itemname")
        category_id = str(page_data.get("categoryId") or "") or None
        return {
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "subcategory": response.meta.get("subcategory"),
            "category_id": category_id,
            "category_name": page_data.get("h1title"),
            "breadcrumb_path": self._breadcrumb_path(page_data),
            "item_id": str(data.get("catEntryID") or data.get("id")),
            "title": title,
            "brand": data.get("mfName") or data.get("PTC_OMNI_BRAND_PRIMARY"),
            "model": str(data.get("parentCatEntryID")) if data.get("parentCatEntryID") else None,
            "url": urljoin(response.url, data["url"]) if data.get("url") else None,
            "image_url": data.get("image_url") or data.get("itemimg"),
            "price": price,
            "original_price": original_price,
            "currency": "USD",
            "rating": self._number(data.get("AverageRating")),
            "reviews_count": self._integer(data.get("TotalReviewCount")),
            # The grid only returns priced rows and exposes no stock flag, so
            # availability is derived from the presence of a price.
            "in_stock": price is not None,
            "bopus_available": self._yes(data.get("PTC_OMNI_BOPUS_FLAG")),
            "autoship_available": self._yes(data.get("PTC_OMNI_REPEAT_DELIVERY_FL")),
            "in_store_only": self._yes(data.get("PTC_OMNI_IN_STORE_ONLY_FLAG")),
            "rx_item": self._yes(data.get("PTC_OMNI_RX_FOOD_IND")),
            "taxonomy_path": data.get("PTC_OMNI_TAXONOMY"),
            "variants_count": len(variations),
            "variant_ids": [
                str(v["data"].get("variation_id"))
                for v in variations
                if isinstance(v.get("data"), dict) and v["data"].get("variation_id")
            ],
            "facets": facets,
            "page": page,
            "position": position,
            "total_count": self._integer(results.get("total_num_results")),
            "items_per_page": self._integer(request.get("num_results_per_page")),
            "sort_by": request.get("sort_by"),
            "sort_order": request.get("sort_order"),
            "search_engine": "constructor.io",
            "source_url": response.url,
            "source": "petco_next_data",
            "raw": product,
        }

    @staticmethod
    def _breadcrumb_path(page_data: dict) -> str | None:
        crumbs = [c for c in page_data.get("breadcrumbs", []) or [] if isinstance(c, dict)]
        labels = [c.get("label") for c in crumbs if c.get("label")]
        return " > ".join(labels) if labels else None

    @staticmethod
    def _yes(value):
        return value == "Yes" if isinstance(value, str) else None

    @staticmethod
    def _number(value, fallback=None):
        candidate = value if value is not None else fallback
        if isinstance(candidate, str):
            match = re.search(r"-?\d[\d,]*(?:\.\d+)?", candidate)
            candidate = match.group(0).replace(",", "") if match else None
        try:
            return float(candidate) if candidate is not None and not isinstance(candidate, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _html_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }
