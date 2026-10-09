from __future__ import annotations

import json
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.mediamarkt_categories import MEDIAMARKT_CATEGORIES


class MediamarktListingSpider(BaseListingSpider):
    """Products from MediaMarkt's server-rendered Apollo bootstrap only."""

    name = "mediamarkt_listing"
    allowed_domains = ["mediamarkt.de", "www.mediamarkt.de", "localhost", "127.0.0.1"]
    categories = MEDIAMARKT_CATEGORIES
    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "DOWNLOAD_TIMEOUT": 120,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "ean", "title", "brand", "url",
            "image_url", "image_alt", "price", "original_price", "currency",
            "discount", "discount_percentage", "rating", "reviews_count",
            "availability", "in_stock", "is_marketplace", "seller",
            "seller_rating", "shipping_cost", "category_ids", "category_path",
            "features", "badges", "page", "position", "total_products",
            "total_pages", "source_url", "source", "raw", "timestamp",
        ],
    }
    _marker = "window.__PRELOADED_STATE__ = "
    _challenge_markers = (
        "<title>just a moment", "cf-chl-", '"api credits"', '"concurrency"',
    )
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.7",
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        target = self.resolve_target_url()
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers=self.headers,
            meta={"page": 1, "base_url": target},
        )

    def parse(self, response: scrapy.http.Response):
        self._reject_bad_response(response)
        page = int(response.meta.get("page", 1))
        state = self.extract_preloaded_state(response.text)
        apollo = state.get("apolloState")
        if not isinstance(apollo, dict):
            raise RuntimeError(f"MediaMarkt bootstrap has no Apollo state at {response.url}")

        listing = self._first_entity(apollo, "ProductListPage")
        summary = self._first_entity(apollo, "ProductList")
        products = listing.get("products") if listing else None
        if not isinstance(products, list) or not products:
            if page > 1:
                return
            raise RuntimeError(f"MediaMarkt bootstrap has no listing products at {response.url}")

        entities = self._entities_by_type_and_id(apollo)
        total_products = self._integer(summary.get("totalProducts")) if summary else None
        total_pages = self._integer(summary.get("maxPage")) if summary else 1
        total_pages = total_pages or 1

        for position, listing_product in enumerate(products, start=1):
            item_id = str(listing_product.get("productId") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            core = entities.get(("CofrCoreFeature", f"Media:de:{item_id}"), {})
            product = entities.get(("GraphqlProduct", item_id), {})
            price_entity = entities.get(("CofrPriceFeature", f"Media:de:{item_id}"), {})
            media = entities.get(("CofrMediaAssetsFeature", f"Media:de:{item_id}"), {})
            status = entities.get(("CofrOnlineStatusFeature", f"Media:de:{item_id}"), {})
            if not core and not product:
                raise RuntimeError(f"MediaMarkt listing product {item_id} has no hydrated entity")
            self._seen.add(item_id)

            price = price_entity.get("price") or {}
            strike_price = price_entity.get("strikePrice") or {}
            seller = price_entity.get("marketplaceSeller") or {}
            image = media.get("productMainImage") or {}
            reviews = core.get("reviewStatistics") or {}
            breadcrumbs = product.get("breadcrumbs") or []
            if not breadcrumbs:
                breadcrumbs = self._breadcrumbs(core, apollo)
            features = self._features(core, apollo)
            badges_entity = entities.get(("CofrBadgesFeature", f"Media:de:{item_id}"), {})
            badges = [
                badge.get("name") for badge in badges_entity.get("computedBadges") or []
                if isinstance(badge, dict) and badge.get("name")
            ]
            relative_url = product.get("url") or core.get("urlRelative") or media.get("urlRelative")
            raw = {
                "listing": listing_product,
                "product": product,
                "core": core,
                "price": price_entity,
                "media": media,
                "status": status,
            }
            yield {
                "category": self.category,
                "item_id": item_id,
                "ean": core.get("ean"),
                "title": product.get("title") or core.get("productName"),
                "brand": product.get("manufacturer") or core.get("manufacturerName"),
                "url": urljoin("https://www.mediamarkt.de", relative_url or ""),
                "image_url": image.get("link"),
                "image_alt": image.get("altText"),
                "price": self._number(price.get("amount")),
                "original_price": self._number(strike_price.get("amount")),
                "currency": price_entity.get("currency"),
                "discount": self._number(price.get("discount")),
                "discount_percentage": self._number(price.get("discountPercentage")),
                "rating": self._number(reviews.get("averageOverallRating")),
                "reviews_count": self._integer(reviews.get("totalReviewCount")),
                "availability": status.get("onlineStatus"),
                "in_stock": status.get("isAvailableAndBuyable"),
                "is_marketplace": core.get("isProductOfTypeMarketplace"),
                "seller": seller.get("sellerName"),
                "seller_rating": self._number(seller.get("sellerRating")),
                "shipping_cost": self._number(price.get("shippingCost")),
                "category_ids": [x.get("categoryId") for x in breadcrumbs if x.get("categoryId")],
                "category_path": [x.get("name") for x in breadcrumbs if x.get("name")],
                "features": features,
                "badges": badges,
                "page": page,
                "position": position,
                "total_products": total_products,
                "total_pages": total_pages,
                "source_url": response.url,
                "source": "mediamarkt_preloaded_apollo_bootstrap",
                "raw": raw,
                "timestamp": self.get_timestamp(),
            }

        if page < min(self.max_pages, total_pages):
            base_url = response.meta.get("base_url") or response.url
            yield scrapy.Request(
                self._page_url(base_url, page + 1),
                callback=self.parse,
                headers=self.headers,
                meta={"page": page + 1, "base_url": base_url},
            )

    @classmethod
    def extract_preloaded_state(cls, html: str) -> dict[str, Any]:
        start = (html or "").find(cls._marker)
        if start < 0:
            raise RuntimeError("MediaMarkt response has no __PRELOADED_STATE__ bootstrap")
        start += len(cls._marker)
        end = html.find("</script>", start)
        if end < 0:
            raise RuntimeError("MediaMarkt __PRELOADED_STATE__ script is unterminated")
        payload = html[start:end].rstrip(" ;\r\n\t")
        try:
            value = json.loads(cls._replace_js_undefined(payload))
        except json.JSONDecodeError as exc:
            raise RuntimeError("MediaMarkt __PRELOADED_STATE__ bootstrap is malformed") from exc
        if not isinstance(value, dict):
            raise RuntimeError("MediaMarkt __PRELOADED_STATE__ bootstrap is not an object")
        return value

    @staticmethod
    def _replace_js_undefined(payload: str) -> str:
        output: list[str] = []
        index = 0
        quote: str | None = None
        escaped = False
        while index < len(payload):
            char = payload[index]
            if quote:
                output.append(char)
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                index += 1
                continue
            if char in ('"', "'"):
                quote = char
                output.append(char)
                index += 1
                continue
            if payload.startswith("undefined", index):
                before = payload[index - 1] if index else ""
                after_index = index + len("undefined")
                after = payload[after_index] if after_index < len(payload) else ""
                if not (before.isalnum() or before in "_$") and not (after.isalnum() or after in "_$"):
                    output.append("null")
                    index = after_index
                    continue
            output.append(char)
            index += 1
        return "".join(output)

    @staticmethod
    def _first_entity(apollo: dict[str, Any], typename: str) -> dict[str, Any]:
        for value in apollo.values():
            if isinstance(value, dict) and value.get("__typename") == typename:
                return value
        return {}

    @staticmethod
    def _entities_by_type_and_id(apollo: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
        result: dict[tuple[str, str], dict[str, Any]] = {}
        for value in apollo.values():
            if not isinstance(value, dict) or not value.get("__typename") or value.get("id") is None:
                continue
            result[(str(value["__typename"]), str(value["id"]))] = value
        return result

    @staticmethod
    def _breadcrumbs(core: dict[str, Any], apollo: dict[str, Any]) -> list[dict[str, Any]]:
        result = []
        for reference in core.get("breadcrumbs") or []:
            entity = apollo.get(reference.get("__ref")) if isinstance(reference, dict) else None
            if isinstance(entity, dict):
                result.append({"categoryId": entity.get("id"), "name": entity.get("categoryName")})
        return result

    @staticmethod
    def _features(core: dict[str, Any], apollo: dict[str, Any]) -> dict[str, Any]:
        result = {}
        for reference in core.get("highlightedFeatures") or []:
            entity = apollo.get(reference.get("__ref")) if isinstance(reference, dict) else None
            if isinstance(entity, dict) and entity.get("name"):
                result[entity["name"]] = entity.get("values")
        return result

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["page"] = str(page)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return None
        return int(value) if float(value).is_integer() else float(value)

    @staticmethod
    def _integer(value: Any) -> int | None:
        try:
            return int(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    def _reject_bad_response(self, response: scrapy.http.Response) -> None:
        body = response.text.lower()
        if response.status >= 400 or any(marker in body for marker in self._challenge_markers):
            raise RuntimeError(
                f"MediaMarkt returned a challenge/proxy response (status={response.status}, "
                f"bytes={len(response.body)}) at {response.url}"
            )
