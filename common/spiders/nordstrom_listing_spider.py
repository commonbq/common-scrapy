from __future__ import annotations

import json
import re
from typing import Iterable

import scrapy

from common.settings import PROXY
from common.spiders.base_listing_spider import BaseListingSpider


class NordstromListingSpider(BaseListingSpider):
    """Nordstrom product listing spider.

    Supports listing-style category usage like other spiders:
    -a category=<name>
    -a category_url=<url>
    -a url=<url>

    Backward compatibility:
    -a keyword=<term> still works and maps to Nordstrom search URL.
    """

    name = "nordstrom_listing"
    allowed_domains = ["nordstrom.com", "www.nordstrom.com"]

    handle_httpstatus_all = True

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "FEED_EXPORT_FIELDS": [
            "category",
            "productId",
            "name",
            "brand",
            "labelId",
            "legacyStyleGroupId",
            "defaultCoreChoice",
            "coreProductId",
            "webPathAlias",
            "description",
            "price",
            "salePrice",
            "regularPrice",
            "percentOff",
            "url",
            "image",
            "imageUrls",
            "rating",
            "reviewsCount",
            "reviewsMaxRating",
            "isPickAndNotShip",
            "shipQuantity",
            "marketPickQuantity",
            "pickQuantity",
            "enticementTagTypes",
            "propositionAsOf",
            "isUnilateralMinimumAdvertisedPrice",
            "colorCount",
            "selectedColor",
            "selectedColorFamily",
            "selectedColorFamilyCode",
            "colorVariants",
            "raw",
        ],
    }

    categories = [
        {"category": "women", "url": "https://www.nordstrom.com/browse/women"},
        {"category": "men", "url": "https://www.nordstrom.com/browse/men"},
        {"category": "kids", "url": "https://www.nordstrom.com/browse/kids"},
        {"category": "beauty", "url": "https://www.nordstrom.com/browse/beauty"},
        {"category": "home", "url": "https://www.nordstrom.com/browse/home"},
        {"category": "designer", "url": "https://www.nordstrom.com/browse/designer"},
        {"category": "sale", "url": "https://www.nordstrom.com/browse/sale"},
    ]

    require_category_arg = False

    def start_requests(self) -> Iterable[scrapy.Request]:
        keyword = getattr(self, "keyword", None)

        current_category = None
        if self.category:
            current_category = self.category
            start_url = self.resolve_target_url()
        elif self.category_url:
            current_category = "category_url"
            start_url = self.category_url
        elif self.url:
            current_category = "custom_url"
            start_url = self.url
        elif keyword:
            current_category = "keyword"
            start_url = f"https://www.nordstrom.com/sr?keyword={keyword}"
        else:
            available = ", ".join(self.available_categories())
            raise ValueError(
                "Provide -a category=<name> (recommended), -a category_url=<url>, "
                "-a url=<category/search url>, or -a keyword=<term>. "
                f"Available categories: {available}"
            )

        yield self._make_request(start_url, dont_filter=True, category=current_category)

    def _make_request(
        self,
        url: str,
        *,
        dont_filter: bool = False,
        force_proxy: bool = False,
        category: str | None = None,
    ) -> scrapy.Request:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        meta = {"handle_httpstatus_all": True, "category": category}
        if force_proxy and PROXY:
            meta["proxy"] = PROXY

        return scrapy.Request(url, headers=headers, meta=meta, dont_filter=dont_filter)

    def parse(self, response: scrapy.http.Response):
        text = response.text or ""

        if response.status != 200:
            self.logger.warning(
                "Non-200 response. status=%s proxy=%s url=%s body_head=%r",
                response.status,
                bool(response.meta.get("proxy")),
                response.url,
                (text[:200] if text else ""),
            )

        if "istlWasHere" in text or "We've noticed some unusual activity" in text:
            self.logger.warning(
                "Nordstrom returned anti-bot wrapper HTML (%s). len=%s proxy=%s",
                response.status,
                len(text),
                bool(response.meta.get("proxy")),
            )
            if PROXY and not response.meta.get("proxy"):
                yield self._make_request(
                    response.url,
                    dont_filter=True,
                    force_proxy=True,
                    category=response.meta.get("category"),
                )
                return

        current_category = response.meta.get("category")
        products = self._extract_products_from_html(text, category=current_category)
        if not products:
            self.logger.warning(
                "No embedded product data found in HTML. status=%s len=%s url=%s",
                response.status,
                len(text),
                response.url,
            )
            return

        for p in products:
            yield p

    def _extract_products_from_html(
        self, html: str, *, category: str | None = None
    ) -> list[dict]:
        # 1) Nordstrom SSR blob used by current site: window.__INITIAL_CONFIG__ = {...}
        m_init = re.search(
            r"window\.__INITIAL_CONFIG__\s*=\s*(\{.*?\})\s*</script>", html, re.S | re.I
        )
        if m_init:
            try:
                initial_config = json.loads(m_init.group(1))
                products = self._products_from_nordstrom_initial_config(
                    initial_config, category=category
                )
                if products:
                    return products
            except Exception:
                self.logger.exception("Failed parsing window.__INITIAL_CONFIG__ JSON")

        # 2) Next.js fallback
        m_next = re.search(
            r"<script[^>]+id=\"__NEXT_DATA__\"[^>]*>(?P<data>.*?)</script>",
            html,
            re.S | re.I,
        )
        if m_next:
            blob = m_next.group("data").strip()
            try:
                data = json.loads(blob)
                products = self._products_from_next_data(data, category=category)
                if products:
                    return products
            except Exception:
                self.logger.exception("Failed parsing __NEXT_DATA__ JSON")

        # 3) Generic large-inline-state fallback
        scripts = re.findall(
            r"<script(?![^>]*\bsrc=)[^>]*>(?P<body>.*?)</script>", html, re.S | re.I
        )
        for body in sorted(scripts, key=len, reverse=True)[:4]:
            if (
                "products" not in body
                and "product" not in body
                and "productResults" not in body
            ):
                continue
            m2 = re.search(r"=\s*(\{.*\})\s*;?\s*$", body.strip(), re.S)
            if not m2:
                continue
            try:
                data = json.loads(m2.group(1))
            except Exception:
                continue
            products = self._products_from_generic_state(data, category=category)
            if products:
                return products

        return []

    def _products_from_nordstrom_initial_config(
        self, data: dict, *, category: str | None = None
    ) -> list[dict]:
        product_results = (data or {}).get("productResults") or {}
        products_by_id = product_results.get("productsById")
        if not isinstance(products_by_id, dict) or not products_by_id:
            return []

        out = []
        for product in products_by_id.values():
            if not isinstance(product, dict):
                continue
            out.append(self._normalize_product(product, category=category))
        return out

    def _products_from_next_data(
        self, data: dict, *, category: str | None = None
    ) -> list[dict]:
        found = []

        def walk(obj):
            if isinstance(obj, dict):
                if "products" in obj and isinstance(obj["products"], list):
                    for prod in obj["products"]:
                        if isinstance(prod, dict):
                            found.append(prod)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)

        walk(data)
        return [
            self._normalize_product(p, category=category)
            for p in found
            if self._looks_like_product(p)
        ]

    def _products_from_generic_state(
        self, data: dict, *, category: str | None = None
    ) -> list[dict]:
        found = []

        def walk(obj):
            if isinstance(obj, dict):
                if self._looks_like_product(obj):
                    found.append(obj)
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for it in obj:
                    walk(it)

        walk(data)
        out = []
        seen = set()
        for p in found:
            norm = self._normalize_product(p, category=category)
            key = (
                norm.get("productId")
                or norm.get("url")
                or json.dumps(norm, sort_keys=True)
            )
            if key in seen:
                continue
            seen.add(key)
            out.append(norm)
        return out

    def _looks_like_product(self, obj: dict) -> bool:
        keys = set(obj.keys())
        return (
            ("name" in keys or "productName" in keys or "title" in keys)
            and (
                "price" in keys
                or "prices" in keys
                or "priceRange" in keys
                or "salePrice" in keys
                or "productPageUrl" in keys
            )
        ) or ("productId" in keys and ("name" in keys or "productName" in keys))

    def _normalize_product(self, p: dict, *, category: str | None = None) -> dict:
        proposition = self._select_primary_proposition(p)
        reviews = p.get("reviews") if isinstance(p.get("reviews"), dict) else {}
        default_core_choice = p.get("defaultCoreChoice")
        core_choice = self._find_core_choice(p, default_core_choice)

        name = (
            p.get("title")
            or p.get("copyProductTitle")
            or p.get("name")
            or p.get("productName")
        )
        product_id = p.get("productId") or p.get("id")
        url = (
            p.get("url")
            or p.get("productUrl")
            or p.get("canonicalUrl")
            or p.get("productPageUrl")
        )
        if not url and p.get("webPathAlias") and p.get("id"):
            url = f"https://www.nordstrom.com/s/{p['webPathAlias']}/{p['id']}"
        if url and url.startswith("//"):
            url = "https:" + url
        if url and url.startswith("/"):
            url = "https://www.nordstrom.com" + url

        price = p.get("price")
        if isinstance(price, dict):
            price = self._extract_price_from_nordstrom_price_obj(price)
        if price is None:
            price = p.get("salePrice") or p.get("currentPrice") or p.get("priceRange")
        if price is None and proposition:
            price = self._extract_price_from_min_max_range(
                proposition.get("sellingRetailPriceRange")
            )

        regular_price = None
        sale_price = None
        percent_off = None
        if proposition:
            sale_price = self._extract_price_from_min_max_range(
                proposition.get("sellingRetailPriceRange")
            )
            regular_price = self._extract_price_from_min_max_range(
                proposition.get("baseRetailPriceRange")
            )
            percent_off = self._extract_price_from_min_max_range(
                proposition.get("sellingRetailPercentageOffRange")
            )

        image = p.get("image") or p.get("imageUrl") or p.get("primaryImage")
        if isinstance(image, dict):
            image = image.get("url") or image.get("src")
        if (
            image is None
            and isinstance(p.get("mediaById"), dict)
            and p.get("mediaById")
        ):
            first_media = next(iter(p["mediaById"].values()))
            if isinstance(first_media, dict):
                image = first_media.get("src") or first_media.get("url")
        if image is None and core_choice:
            image = self._extract_image_from_core_choice(core_choice)

        image_urls = self._extract_all_image_urls(p, core_choice)
        enticement_tags = proposition.get("enticementTags") if proposition else None
        availability = proposition.get("availability") if proposition else None
        color_variants = self._extract_color_variants(p)

        return {
            "category": category,
            "productId": product_id,
            "name": name,
            "brand": (
                p.get("brandName") or p.get("brand") or p.get("labelDisplayName")
            ),
            "labelId": p.get("labelId"),
            "legacyStyleGroupId": p.get("legacyStyleGroupId"),
            "defaultCoreChoice": default_core_choice,
            "webPathAlias": p.get("webPathAlias"),
            "description": p.get("copyDescription") or p.get("description"),
            "price": price,
            "salePrice": sale_price,
            "regularPrice": regular_price,
            "percentOff": percent_off,
            "url": url,
            "image": image,
            "imageUrls": image_urls,
            "rating": (
                p.get("reviewStarRating")
                or p.get("rating")
                or reviews.get("averageRating")
            ),
            "reviewsCount": (
                p.get("reviewCount")
                or p.get("reviews_count")
                or reviews.get("numberOfReviews")
            ),
            "reviewsMaxRating": reviews.get("maximumRating"),
            "isPickAndNotShip": (
                availability.get("isPickAndNotShip")
                if isinstance(availability, dict)
                else None
            ),
            "shipQuantity": (
                availability.get("shipQuantity")
                if isinstance(availability, dict)
                else None
            ),
            "marketPickQuantity": (
                availability.get("marketPickQuantity")
                if isinstance(availability, dict)
                else None
            ),
            "pickQuantity": (
                availability.get("pickQuantity")
                if isinstance(availability, dict)
                else None
            ),
            "enticementTagTypes": self._extract_tag_types(enticement_tags),
            "propositionAsOf": proposition.get("asOf") if proposition else None,
            "isUnilateralMinimumAdvertisedPrice": (
                proposition.get("isUnilateralMinimumAdvertisedPrice")
                if proposition
                else None
            ),
            "coreProductId": self._extract_core_product_id(p),
            "colorCount": len(color_variants),
            "colorVariants": color_variants,
            "selectedColor": (
                core_choice.get("displayColorDescription")
                if isinstance(core_choice, dict)
                else None
            ),
            "selectedColorFamily": (
                (core_choice.get("colorFamily") or {}).get("label")
                if isinstance(core_choice, dict)
                else None
            ),
            "selectedColorFamilyCode": (
                (core_choice.get("colorFamily") or {}).get("code")
                if isinstance(core_choice, dict)
                else None
            ),
            "raw": p,
        }

    def _select_primary_proposition(self, p: dict) -> dict | None:
        propositions = p.get("propositions")
        if not isinstance(propositions, list):
            return None

        for proposition in propositions:
            if isinstance(proposition, dict) and (
                (proposition.get("salability") or {}).get("status") == "SELLABLE"
            ):
                return proposition

        for proposition in propositions:
            if isinstance(proposition, dict):
                return proposition
        return None

    def _find_core_choice(self, p: dict, core_choice_id: str | None) -> dict | None:
        for core_product in p.get("coreProducts") or []:
            if not isinstance(core_product, dict):
                continue
            for core_choice in core_product.get("coreChoices") or []:
                if not isinstance(core_choice, dict):
                    continue
                if core_choice_id and core_choice.get("coreChoiceId") == core_choice_id:
                    return core_choice

        for core_product in p.get("coreProducts") or []:
            if not isinstance(core_product, dict):
                continue
            for core_choice in core_product.get("coreChoices") or []:
                if isinstance(core_choice, dict):
                    return core_choice
        return None

    def _extract_core_product_id(self, p: dict) -> str | None:
        for core_product in p.get("coreProducts") or []:
            if isinstance(core_product, dict) and core_product.get("coreProductId"):
                return core_product.get("coreProductId")
        return None

    def _extract_image_from_core_choice(self, core_choice: dict) -> str | None:
        for shot in core_choice.get("orderedShots") or []:
            if isinstance(shot, dict) and shot.get("imageUrl"):
                return shot.get("imageUrl")
        return None

    def _extract_all_image_urls(self, p: dict, core_choice: dict | None) -> list[str]:
        urls = []
        candidates = []

        direct_image = p.get("image") or p.get("imageUrl") or p.get("primaryImage")
        if direct_image:
            candidates.append(direct_image)

        if isinstance(p.get("mediaById"), dict):
            candidates.extend(p["mediaById"].values())

        if isinstance(core_choice, dict):
            candidates.extend(core_choice.get("orderedShots") or [])

        for candidate in candidates:
            if isinstance(candidate, dict):
                url = (
                    candidate.get("imageUrl")
                    or candidate.get("url")
                    or candidate.get("src")
                )
            else:
                url = candidate

            if isinstance(url, str) and url and url not in urls:
                urls.append(url)

        return urls

    def _extract_color_variants(self, p: dict) -> list[dict]:
        variants = []

        for core_product in p.get("coreProducts") or []:
            if not isinstance(core_product, dict):
                continue
            for core_choice in core_product.get("coreChoices") or []:
                if not isinstance(core_choice, dict):
                    continue
                variants.append(core_choice)

        return variants

    def _extract_tag_types(self, tags: list | None) -> list[str]:
        if not isinstance(tags, list):
            return []
        return [
            tag.get("type") for tag in tags if isinstance(tag, dict) and tag.get("type")
        ]

    def _extract_price_from_min_max_range(self, value):
        if not isinstance(value, dict):
            return None

        for key in ("min", "max"):
            candidate = value.get(key)
            if candidate:
                return candidate

        return None

    def _extract_price_from_nordstrom_price_obj(self, price_obj: dict):
        # Nordstrom uses money objects: {units, nanos}. Prefer sale min if available, then total min.
        def money_to_float(m):
            if not isinstance(m, dict):
                return None
            units = m.get("units")
            nanos = m.get("nanos", 0)
            if units is None:
                return None
            try:
                return float(units) + (float(nanos) / 1_000_000_000)
            except Exception:
                return None

        for path in [
            ("salePriceRange", "min"),
            ("totalPriceRange", "min"),
            ("regularPriceRange", "min"),
        ]:
            node = price_obj
            for key in path:
                node = node.get(key) if isinstance(node, dict) else None
            val = money_to_float(node)
            if val is not None:
                return val

        direct = money_to_float(price_obj)
        if direct is not None:
            return direct

        amount = price_obj.get("amount") if isinstance(price_obj, dict) else None
        try:
            return float(amount) if amount is not None else None
        except Exception:
            return None
