from __future__ import annotations

import json
import re
from html import unescape
from urllib.parse import parse_qs, parse_qsl, urlencode, urljoin, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


BLOOMINGDALES_CATEGORIES = {
    "new-now": "https://www.bloomingdales.com/shop/fashion-lookbooks-videos-style-guide?id=13668",
    "women": "https://www.bloomingdales.com/shop/womens-apparel?id=2910",
    "beauty": "https://www.bloomingdales.com/shop/makeup-perfume-beauty?id=2921",
    "shoes": "https://www.bloomingdales.com/shop/womens-designer-shoes?id=16961",
    "handbags": "https://www.bloomingdales.com/shop/handbags?id=16958",
    "jewelry-accessories": "https://www.bloomingdales.com/shop/jewelry-accessories?id=3376",
    "men": "https://www.bloomingdales.com/shop/mens?id=3864",
    "kids": "https://www.bloomingdales.com/shop/kids?id=3866",
    "home": "https://www.bloomingdales.com/shop/home?id=3865",
    "sale": "https://www.bloomingdales.com/shop/sale?id=3977",
    "gifts": "https://www.bloomingdales.com/shop/gifts?id=3948",
    "designers": "https://www.bloomingdales.com/shop/all-designers?id=1001351",
}


class BloomingdalesListingSpider(BaseListingSpider):
    """Bloomingdale's listing spider using Nuxt SSR state as the single source of truth."""

    name = "bloomingdales_listing"
    allowed_domains = ["bloomingdales.com", "www.bloomingdales.com"]

    categories = [
        {"category": category, "url": url}
        for category, url in BLOOMINGDALES_CATEGORIES.items()
    ]

    def start_requests(self):
        target_url = self.resolve_target_url()
        yield scrapy.Request(
            self._page_url(target_url, 1),
            callback=self.parse,
            meta={"page": 1, "seed_category_url": target_url, "_seen_item_ids": set()},
            headers=self._request_headers(),
        )

    def parse(self, response: scrapy.http.Response):
        if self._is_blocked_response(response):
            raise RuntimeError(
                f"Bloomingdale's listing blocked for {response.url} (status={response.status})"
            )

        state = self._extract_nuxt_state(response.text)
        if not state:
            raise ValueError("Bloomingdale's Nuxt state contract missing in response")

        category_metadata = self._extract_category_metadata(state, response.url)
        page = int(response.meta.get("page", 1) or 1)
        seen_item_ids = response.meta.get("_seen_item_ids") or set()

        if (
            page == 1
            and not response.meta.get("resolved_leaf")
            and self._is_splash_state(state)
            and category_metadata["leaf_urls"]
        ):
            redirect_leaf = self._select_leaf_url(
                category_metadata["leaf_urls"],
                response.meta.get("seed_category_url", response.url),
            )
            yield scrapy.Request(
                self._page_url(redirect_leaf, 1),
                callback=self.parse,
                meta={
                    "page": 1,
                    "resolved_leaf": True,
                    "seed_category_url": response.meta.get("seed_category_url", response.url),
                    "_seen_item_ids": seen_item_ids,
                },
                headers=self._request_headers(),
            )
            return

        extracted_products = self._extract_products(state)
        for product in extracted_products:
            item_id = product.get("item_id")
            if item_id and item_id in seen_item_ids:
                continue
            if item_id:
                seen_item_ids.add(item_id)

            product["category"] = self.category
            product["seed_category_url"] = response.meta.get("seed_category_url", response.url)
            product["subcategory_urls"] = category_metadata["subcategories"]
            product["facet_urls"] = category_metadata["facets"]
            yield product

        if page >= self.max_pages:
            return
        has_next_page_signal = self._has_next_page_signal(state, page)
        if has_next_page_signal is False:
            return
        if not extracted_products and has_next_page_signal is not True:
            return

        yield scrapy.Request(
            self._page_url(response.url, page + 1),
            callback=self.parse,
            meta={
                "page": page + 1,
                "resolved_leaf": response.meta.get("resolved_leaf", False),
                "seed_category_url": response.meta.get("seed_category_url", response.url),
                "_seen_item_ids": seen_item_ids,
            },
            headers=self._request_headers(),
        )

    def _extract_products(self, state: list) -> list[dict]:
        products_by_id: dict[int, dict] = {}
        url_nodes: list[dict] = []

        for node in state:
            if not isinstance(node, dict):
                continue

            if "id" in node and "detail" in node:
                pid = self._resolve_ref(state, node.get("id"))
                if isinstance(pid, int):
                    products_by_id[pid] = node

            if "productUrl" in node and "productId" in node:
                url_nodes.append(node)

        out: list[dict] = []
        for node in url_nodes:
            raw_url = self._resolve_ref(state, node.get("productUrl"))
            pid = self._resolve_ref(state, node.get("productId"))
            if not isinstance(raw_url, str):
                continue

            product_node = products_by_id.get(pid) if isinstance(pid, int) else None
            detail = (
                self._resolve_ref(state, (product_node or {}).get("detail"))
                if product_node
                else {}
            )
            pricing = (
                self._resolve_ref(state, (product_node or {}).get("pricing"))
                if product_node
                else {}
            )

            price, price_text, original_price, original_price_text = self._extract_prices(
                pricing if isinstance(pricing, dict) else {}
            )
            url = self._canonical_product_url(raw_url)
            item_id = self._extract_item_id(url, pid)

            out.append(
                {
                    "item_id": item_id,
                    "title": self._clean_title(
                        self._first_nested_value(
                            detail,
                            "name",
                            "productName",
                            "title",
                        )
                        or ""
                    )
                    or None,
                    "url": url,
                    "price": price,
                    "price_text": price_text,
                    "original_price": original_price,
                    "original_price_text": original_price_text,
                    "image": self._extract_image(detail),
                    "brand": self._extract_brand(detail),
                    "rating": self._extract_rating(detail),
                    "review_count": self._extract_review_count(detail),
                    "source": "bloomingdales_nuxt_state",
                }
            )

        return out

    def _extract_nuxt_state(self, html_text: str) -> list:
        m = re.search(
            r'<script[^>]+data-nuxt-data="nuxt-app"[^>]*>(?P<data>.*?)</script>',
            html_text,
            re.I | re.S,
        )
        if not m:
            return []

        try:
            parsed = json.loads(m.group("data"))
        except json.JSONDecodeError:
            return []

        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            for key in ("data", "state", "payload"):
                value = parsed.get(key)
                if isinstance(value, list):
                    return value
        return []

    def _resolve_ref(self, state: list, value, depth: int = 0):
        if depth > 50:
            return value

        if isinstance(value, int) and 0 <= value < len(state):
            return self._resolve_ref(state, state[value], depth + 1)

        if isinstance(value, list):
            return [self._resolve_ref(state, v, depth + 1) for v in value]

        if isinstance(value, dict):
            return {k: self._resolve_ref(state, v, depth + 1) for k, v in value.items()}

        return value

    def _extract_prices(
        self, pricing: dict
    ) -> tuple[float | None, str | None, float | None, str | None]:
        def money_pair(node) -> tuple[float | None, str | None]:
            if not isinstance(node, dict):
                return None, None
            text = node.get("formattedValue") if isinstance(node.get("formattedValue"), str) else None
            numeric = self._to_float(node.get("value"))
            if numeric is None and text:
                numeric = self._to_float(text)
            return numeric, text

        price = pricing.get("price") if isinstance(pricing, dict) else None
        tiered = price.get("tieredPrice") if isinstance(price, dict) else None
        if isinstance(tiered, list):
            ordered_pairs: list[tuple[float | None, str | None]] = []
            for tier in tiered:
                values = (tier or {}).get("values")
                if not isinstance(values, list):
                    continue
                for value_node in values:
                    pair = money_pair(value_node)
                    if pair != (None, None):
                        ordered_pairs.append(pair)
            if ordered_pairs:
                current = ordered_pairs[0]
                original = next(
                    (
                        pair
                        for pair in ordered_pairs[1:]
                        if pair[0] is None or current[0] is None or pair[0] != current[0]
                    ),
                    (None, None),
                )
                return current[0], current[1], original[0], original[1]

        current = self._first_nested_value(pricing, "salePrice", "currentPrice", "promoPrice", "value")
        original = self._first_nested_value(pricing, "originalPrice", "wasPrice", "regularPrice", "listPrice")
        current_val = self._to_float(current)
        original_val = self._to_float(original)
        if current_val is not None or original_val is not None:
            current_text = str(current) if isinstance(current, str) else None
            original_text = str(original) if isinstance(original, str) else None
            return current_val, current_text, original_val, original_text

        return None, None, None, None

    def _extract_category_metadata(self, state: list, current_url: str) -> dict[str, list[str]]:
        urls: list[str] = []
        seen_urls: set[str] = set()
        visited_refs: set[int] = set()

        def walk(node):
            if isinstance(node, str):
                normalized = self._normalize_category_url(node)
                if normalized and self._is_shop_category_url(normalized):
                    if normalized not in seen_urls:
                        seen_urls.add(normalized)
                        urls.append(normalized)
                return
            if isinstance(node, int) and 0 <= node < len(state):
                if node in visited_refs:
                    return
                visited_refs.add(node)
                walk(state[node])
                return
            if isinstance(node, dict):
                for child in node.values():
                    walk(child)
            elif isinstance(node, list):
                for child in node:
                    walk(child)

        for index in range(len(state)):
            walk(index)

        subcategories: list[str] = []
        facets: list[str] = []
        leaf_urls: list[str] = []

        for url in urls:
            if self._is_facet_url(url):
                facets.append(url)
            else:
                subcategories.append(url)
                if self._is_leaf_category_url(url):
                    leaf_urls.append(url)

        return {
            "subcategories": subcategories,
            "facets": facets,
            "leaf_urls": leaf_urls,
        }

    def _is_splash_state(self, state: list) -> bool:
        visited_refs: set[int] = set()

        def walk(node) -> bool:
            if isinstance(node, int) and 0 <= node < len(state):
                if node in visited_refs:
                    return False
                visited_refs.add(node)
                return walk(state[node])
            if isinstance(node, dict):
                splash_ref = node.get("isSplashRef")
                if splash_ref is True:
                    return True
                if (
                    isinstance(splash_ref, int)
                    and 0 <= splash_ref < len(state)
                    and state[splash_ref] is True
                ):
                    return True
                return any(walk(value) for value in node.values())
            if isinstance(node, list):
                return any(walk(value) for value in node)
            return False

        return any(walk(index) for index in range(len(state)))

    def _extract_item_id(self, product_url: str, fallback_pid) -> str | None:
        q = parse_qs(urlparse(product_url).query)
        value = (q.get("ID") or q.get("id") or [fallback_pid])[0]
        if value is None:
            return None
        return str(value)

    def _canonical_product_url(self, url: str) -> str:
        normalized = self._normalize_url(url)
        parsed = urlparse(normalized)
        query = parse_qs(parsed.query)
        canonical_query: list[tuple[str, str]] = []
        for key in ("ID", "id"):
            for val in query.get(key, []):
                canonical_query.append((key, val))
        for key in ("CategoryID", "categoryid"):
            for val in query.get(key, []):
                canonical_query.append((key, val))
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(canonical_query),
                "",
            )
        )

    def _normalize_category_url(self, url: str) -> str | None:
        if not isinstance(url, str) or not url.strip():
            return None

        normalized = self._normalize_url(url.strip())
        parsed = urlparse(normalized)
        if parsed.netloc not in {"www.bloomingdales.com", "bloomingdales.com"}:
            return None
        if "/shop/" not in parsed.path or "/shop/product/" in parsed.path:
            return None

        drop_keys = {
            "Pageindex",
            "pageindex",
            "cm_sp",
            "cm_mmc",
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "trackingid",
            "trackingId",
        }
        params = [
            (k, v)
            for k, v in parse_qsl(parsed.query, keep_blank_values=True)
            if k not in drop_keys
        ]
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(params),
                "",
            )
        )

    def _is_shop_category_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return (
            parsed.netloc in {"www.bloomingdales.com", "bloomingdales.com"}
            and "/shop/" in parsed.path
            and "/shop/product/" not in parsed.path
        )

    def _is_leaf_category_url(self, url: str) -> bool:
        segments = [segment for segment in urlparse(url).path.strip("/").split("/") if segment]
        return len(segments) > 2 and segments[0] == "shop"

    def _is_facet_url(self, url: str) -> bool:
        facet_keys = {
            "prefn1",
            "prefv1",
            "prefn2",
            "prefv2",
            "edge",
            "sortBy",
            "keyword",
            "searchpass",
        }
        keys = {k for k, _ in parse_qsl(urlparse(url).query, keep_blank_values=True)}
        return bool(keys & facet_keys)

    def _has_next_page_signal(self, state: list, page: int) -> bool | None:
        saw_pagination = False
        visited_refs: set[int] = set()

        def walk(node) -> bool:
            nonlocal saw_pagination
            if isinstance(node, int) and 0 <= node < len(state):
                if node in visited_refs:
                    return False
                visited_refs.add(node)
                return walk(state[node])
            if isinstance(node, dict):
                total_pages = node.get("totalPages") or node.get("totalpages")
                current_page = (
                    node.get("currentPage")
                    or node.get("currentpage")
                    or node.get("pageIndex")
                    or node.get("Pageindex")
                    or node.get("pageindex")
                )
                total_pages_int = self._to_int(total_pages)
                current_page_int = self._to_int(current_page)
                if total_pages_int is not None:
                    saw_pagination = True
                    if total_pages_int > page:
                        return True
                if (
                    total_pages_int is not None
                    and current_page_int is not None
                    and current_page_int < total_pages_int
                ):
                    saw_pagination = True
                    return True
                return any(walk(value) for value in node.values())
            if isinstance(node, list):
                return any(walk(value) for value in node)
            return False

        has_next = any(walk(node) for node in state)
        if has_next:
            return True
        if saw_pagination:
            return False
        return None

    def _select_leaf_url(self, leaf_urls: list[str], seed_url: str) -> str:
        seed_path = urlparse(seed_url).path.strip("/").split("/")
        branch_prefix = "/".join(seed_path[:2]) if len(seed_path) >= 2 else ""
        if branch_prefix:
            for url in leaf_urls:
                path = urlparse(url).path.strip("/")
                if path.startswith(branch_prefix):
                    return url
        return leaf_urls[0]

    def _extract_brand(self, detail: dict) -> str | None:
        if not isinstance(detail, dict):
            return None
        brand = self._first_nested_value(detail, "brandName", "designer", "brand")
        if isinstance(brand, dict):
            brand = brand.get("name") or brand.get("label")
        return self._clean_title(brand or "") or None

    def _extract_image(self, detail: dict) -> str | None:
        image = self._first_nested_value(
            detail,
            "image",
            "images",
            "primaryImage",
            "imageUrl",
            "img",
        )
        if isinstance(image, dict):
            image = image.get("url") or image.get("imageUrl") or image.get("src")
        if isinstance(image, list) and image:
            first = image[0]
            if isinstance(first, dict):
                image = first.get("url") or first.get("imageUrl") or first.get("src")
            else:
                image = first
        if not isinstance(image, str):
            return None
        return self._normalize_url(image)

    def _extract_rating(self, detail: dict) -> float | None:
        rating = self._first_nested_value(detail, "rating", "ratingValue", "averageRating")
        if isinstance(rating, dict):
            rating = rating.get("value") or rating.get("rating") or rating.get("average")
        return self._to_float(rating)

    def _extract_review_count(self, detail: dict) -> int | None:
        reviews = self._first_nested_value(
            detail,
            "reviewCount",
            "reviewsCount",
            "totalReviews",
            "numReviews",
            "reviews",
        )
        if isinstance(reviews, dict):
            reviews = reviews.get("count") or reviews.get("total") or reviews.get("reviews")
        return self._to_int(reviews)

    def _first_nested_value(self, node, *keys):
        if isinstance(node, dict):
            for key in keys:
                if key in node and node[key] not in (None, ""):
                    return node[key]
            for value in node.values():
                found = self._first_nested_value(value, *keys)
                if found not in (None, ""):
                    return found
        elif isinstance(node, list):
            for value in node:
                found = self._first_nested_value(value, *keys)
                if found not in (None, ""):
                    return found
        return None

    def _is_blocked_response(self, response: scrapy.http.Response) -> bool:
        body_lower = (response.text or "").lower()
        return response.status >= 400 or (
            "access denied" in body_lower
            or "captcha" in body_lower
            or "request blocked" in body_lower
        )

    def _request_headers(self) -> dict[str, str]:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

    def _page_url(self, url: str, page: int) -> str:
        parsed = urlparse(url)
        params = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if k.lower() != "pageindex"]
        if page > 1:
            params.append(("pageindex", str(page)))
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                urlencode(params),
                parsed.fragment,
            )
        )

    def _normalize_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return urljoin("https://www.bloomingdales.com", url)

    def _clean_title(self, raw: str) -> str:
        text = re.sub(r"\\u0026", "&", raw)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"^(NEW!?|New:?|Exclusive:?|Shop New:)\s*", "", text, flags=re.I)
        return unescape(text.strip())

    def _to_float(self, value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()
        if not text:
            return None

        currency = re.search(r"\$\s*([0-9][0-9,]*(?:\.\d+)?)", text)
        token = currency.group(1) if currency else None

        if token is None:
            m = re.search(r"-?\d{1,3}(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?", text)
            if not m:
                return None
            token = m.group(0)

        try:
            return float(token.replace(",", ""))
        except Exception:
            return None

    def _to_int(self, value) -> int | None:
        number = self._to_float(value)
        if number is None:
            return None
        return int(number)
