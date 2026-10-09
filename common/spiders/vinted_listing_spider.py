from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.vinted_categories import VINTED_CATEGORIES


_FLIGHT_CHUNK_RE = re.compile(
    r'self\.__next_f\.push\(\[\s*1\s*,\s*("(?:[^"\\]|\\.)*")\s*\]\)',
    re.DOTALL,
)
_ITEMS_MARKER_RE = re.compile(r'"items":\s*\{\s*"items":\s*')
_RSC_SENTINEL_RE = re.compile(r"^\$(?:undefined|@?[0-9A-Za-z_$][\w$]*|D[\w.+-]*|I-?[\w.]*|n)$")
_PROXY_ERROR_MARKERS = (
    '"api credits"',
    '"concurrency"',
    "proxy authentication required",
    "access denied",
    "captcha",
)


class VintedListingSpider(BaseListingSpider):
    """Vinted catalog items from Next.js RSC hydration state only."""

    name = "vinted_listing"
    allowed_domains = ["vinted.com", "www.vinted.com", "localhost", "127.0.0.1"]
    categories = VINTED_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "category_id", "category_name", "category_path",
            "item_id", "title", "brand", "condition", "size", "url",
            "image_url", "image_urls", "price", "discounted_price", "currency",
            "service_fee", "total_price", "favourite_count", "is_promoted",
            "seller_id", "seller_is_business", "content_source", "search_score",
            "page", "position", "per_page", "total_entries", "total_pages",
            "category_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_ids: set[str] = set()

    def start_requests(self):
        category = self._category_entry()
        yield self._request(category["url"], category, page=1)

    def parse(self, response: scrapy.http.Response, **kwargs):
        self._reject_bad_response(response)
        category = response.meta["category_entry"]
        page = int(response.meta["page"])
        payload = self._flight_payload(response.text)
        records, pagination = self._catalog_items(payload)

        if not records:
            if page > 1:
                self.logger.info("Stopping %s at page %s: no hydrated items", category["category"], page)
                return
            raise RuntimeError(f"Vinted RSC payload has no catalog items at {response.url}")

        emitted = 0
        for position, record in enumerate(records, start=1):
            product = record.get("productItem") if isinstance(record, dict) else None
            if not isinstance(product, dict):
                continue
            item_id = str(product.get("id") or record.get("id") or "").strip()
            if not item_id or item_id in self._seen_ids:
                continue
            self._seen_ids.add(item_id)
            emitted += 1
            yield self._item(record, product, category, response, page, position, pagination)

        total_pages = self._integer(pagination.get("total_pages"))
        if page < self.max_pages and emitted and (total_pages is None or page < total_pages):
            yield self._request(self._with_page(category["url"], page + 1), category, page=page + 1)

    def _item(self, record, product, category, response, page, position, pagination):
        raw = self._clean_rsc(record)
        product = raw["productItem"]
        box = product.get("itemBox") if isinstance(product.get("itemBox"), dict) else {}
        user = product.get("user") if isinstance(product.get("user"), dict) else {}
        tracking = raw.get("catalogTracking") if isinstance(raw.get("catalogTracking"), dict) else {}
        price = product.get("price") if isinstance(product.get("price"), dict) else {}
        discounted = product.get("priceWithDiscount") if isinstance(product.get("priceWithDiscount"), dict) else {}
        fee = product.get("serviceFee") if isinstance(product.get("serviceFee"), dict) else {}
        total = product.get("totalItemPrice") if isinstance(product.get("totalItemPrice"), dict) else {}
        images = [url for url in product.get("thumbnailUrls") or [] if isinstance(url, str)]
        if not images and product.get("thumbnailUrl"):
            images = [product["thumbnailUrl"]]
        brand, condition, size = self._item_attributes(box)

        return {
            "category": category["category"],
            "category_id": category["id"],
            "category_name": category["name"],
            "category_path": category["path"],
            "item_id": str(product.get("id") or raw.get("id")),
            "title": product.get("title"),
            "brand": brand,
            "condition": condition,
            "size": size,
            "url": urljoin("https://www.vinted.com/", product.get("url") or ""),
            "image_url": product.get("thumbnailUrl"),
            "image_urls": images,
            "price": self._number(price.get("amount")),
            "discounted_price": self._number(discounted.get("amount")),
            "currency": price.get("currencyCode") or discounted.get("currencyCode"),
            "service_fee": self._number(fee.get("amount")),
            "total_price": self._number(total.get("amount")),
            "favourite_count": self._integer(product.get("favouriteCount")),
            "is_promoted": product.get("isPromoted"),
            "seller_id": user.get("id"),
            "seller_is_business": user.get("isBusiness"),
            "content_source": tracking.get("contentSource"),
            "search_score": self._number(tracking.get("searchScore")),
            "page": page,
            "position": position,
            "per_page": self._integer(pagination.get("per_page")),
            "total_entries": self._integer(pagination.get("total_entries")),
            "total_pages": self._integer(pagination.get("total_pages")),
            "category_url": response.url,
            "source": "vinted_nextjs_rsc_catalog_items",
            "raw": raw,
            "timestamp": self.get_timestamp(),
        }

    def _category_entry(self) -> dict[str, Any]:
        target = self.resolve_target_url()
        normalized = target.rstrip("/")
        for entry in self.iter_categories():
            if entry["category"] == self.category or entry["url"].rstrip("/") == normalized:
                return entry
        match = re.search(r"/catalog/(\d+)-([^/?#]+)", target)
        if not match:
            raise ValueError(f"Vinted URL is not a catalog URL: {target}")
        return {"category": match.group(2), "id": int(match.group(1)), "name": match.group(2), "path": match.group(2), "url": target}

    def _request(self, url: str, category: dict[str, Any], *, page: int):
        return scrapy.Request(
            url,
            callback=self.parse,
            headers=self._headers(),
            meta={"category_entry": category, "page": page},
            dont_filter=True,
        )

    @classmethod
    def _flight_payload(cls, document: str) -> str:
        chunks = _FLIGHT_CHUNK_RE.findall(document or "")
        if not chunks:
            raise RuntimeError("Vinted response has no Next.js RSC flight chunks")
        return "".join(json.loads(chunk) for chunk in chunks)

    @classmethod
    def _catalog_items(cls, payload: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        decoder = json.JSONDecoder()
        for match in _ITEMS_MARKER_RE.finditer(payload):
            try:
                records, end = decoder.raw_decode(payload, match.end())
            except (TypeError, ValueError):
                continue
            if not isinstance(records, list) or not any(
                isinstance(entry, dict) and isinstance(entry.get("productItem"), dict)
                for entry in records
            ):
                continue
            # ``raw_decode`` returns an absolute end offset when given ``idx``.
            tail = payload[end : end + 1000]
            pagination_match = re.search(r'^\s*,\s*"pagination":\s*', tail)
            pagination: dict[str, Any] = {}
            if pagination_match:
                try:
                    value, _ = decoder.raw_decode(tail, pagination_match.end())
                    if isinstance(value, dict):
                        pagination = value
                except ValueError:
                    pass
            return records, pagination
        raise RuntimeError("Vinted RSC payload has no structured catalog items state")

    @staticmethod
    def _item_attributes(box: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
        label = str(box.get("accessibilityLabel") or "")
        brand_match = re.search(r", Brand: (.*?), Condition:", label)
        condition_match = re.search(r", Condition: (.*?)(?:, Size:|, [-\d.,]+\s+[A-Z$€£])", label)
        size_match = re.search(r", Size: (.*?), [-\d.,]+\s+[A-Z$€£]", label)
        second = [part.strip() for part in str(box.get("secondLine") or "").split(" · ") if part.strip()]
        condition = condition_match.group(1) if condition_match else (second[-1] if second else None)
        size = size_match.group(1) if size_match else (second[0] if len(second) > 1 else None)
        return (brand_match.group(1) if brand_match else None, condition, size)

    def _reject_bad_response(self, response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(f"Vinted returned HTTP {response.status} for {response.url}")
        head = response.text[:4000].lower()
        marker = next((entry for entry in _PROXY_ERROR_MARKERS if entry in head), None)
        if marker:
            raise RuntimeError(f"Vinted returned a challenge/proxy error body ({marker}) for {response.url}")

    @classmethod
    def _clean_rsc(cls, value: Any) -> Any:
        if isinstance(value, str):
            return None if _RSC_SENTINEL_RE.match(value) else value
        if isinstance(value, list):
            return [cls._clean_rsc(entry) for entry in value]
        if isinstance(value, dict):
            return {key: cls._clean_rsc(entry) for key, entry in value.items()}
        return value

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        }

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key != "page"]
        query.append(("page", str(page)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    @staticmethod
    def _number(value: Any) -> float | int | None:
        if value is None or isinstance(value, bool):
            return None
        try:
            number = float(str(value).replace(",", "").strip())
            return int(number) if number.is_integer() else number
        except (TypeError, ValueError):
            return None

    @classmethod
    def _integer(cls, value: Any) -> int | None:
        number = cls._number(value)
        return int(number) if number is not None else None
