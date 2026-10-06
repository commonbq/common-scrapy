from __future__ import annotations

"""Realtor.com listings from React Router's streamed SSR bootstrap state."""

import json
import re
from typing import Any, Iterable
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.realtor_categories import CATEGORIES


ENQUEUE = re.compile(r"streamController\.enqueue\(")
PATCH = re.compile(r"P(\d+):(.*?)(?:\n)?\Z", re.S)


class RealtorListingSpider(BaseListingSpider):
    name = "realtor_listing"
    allowed_domains = ["realtor.com", "www.realtor.com"]
    categories = CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "listing_id", "title", "address", "city", "state",
            "postal_code", "url", "status", "status_text", "price", "price_min",
            "price_max", "currency", "beds", "baths", "sqft", "lot_sqft",
            "property_type", "latitude", "longitude", "image", "photo_count",
            "broker", "builder", "flags", "has_3d_tour", "has_video_tour",
            "has_virtual_tour", "list_date", "category", "listing_url", "page",
            "position", "total_count", "source", "timestamp", "raw",
        ],
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self) -> Iterable[scrapy.Request]:
        self._seen.clear()
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url: str, page: int) -> scrapy.Request:
        url = base_url.rstrip("/") if page == 1 else f"{base_url.rstrip('/')}/pg-{page}"
        return scrapy.Request(
            url,
            callback=self.parse,
            headers=self.headers,
            meta={"proxy": self._realtor_proxy(), "page": page, "base_url": base_url},
            dont_filter=True,
        )

    def _realtor_proxy(self) -> str | None:
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not isinstance(proxy, str) or not proxy or "scrapeops" not in proxy.lower():
            return proxy or None
        parts = urlsplit(proxy)
        if not parts.username or parts.password is None or not parts.hostname:
            return proxy
        options = parts.username.split(".")
        keys = {part.split("=", 1)[0] for part in options}
        for option in ("residential=true", "bypass=5"):
            if option.split("=", 1)[0] not in keys:
                options.append(option)
        port = f":{parts.port}" if parts.port else ""
        netloc = f"{'.'.join(options)}:{parts.password}@{parts.hostname}{port}"
        return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Realtor.com returned HTTP {response.status}: {response.url}")
        stripped = response.text.lstrip()
        if stripped.startswith("{"):
            raise RuntimeError(f"Realtor.com returned a proxy failure envelope: {response.url}")
        lowered = response.text[:100_000].lower()
        if "captcha" in lowered or "access denied" in lowered:
            raise RuntimeError(f"Realtor.com returned a challenge page: {response.url}")

        root = self._decode_router_stream(response.text)
        try:
            srp = root["loaderData"]["srp"]
            search = srp["search"]
            properties = search["properties"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError(f"Realtor.com stream has no authoritative srp.search state: {response.url}") from exc
        if not isinstance(properties, list):
            raise RuntimeError(f"Realtor.com srp.search.properties is malformed: {response.url}")
        if not properties:
            self.logger.info("Realtor.com authoritative result set is empty on page %s", response.meta["page"])
            return

        page = int(response.meta["page"])
        emitted = 0
        for position, record in enumerate(properties, 1):
            if not isinstance(record, dict):
                continue
            item_id = str(record.get("property_id") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield self._item(record, response, page, position, search.get("total"))

        if emitted and page < self.max_pages:
            yield self._request(response.meta["base_url"], page + 1)

    @classmethod
    def _decode_router_stream(cls, html: str) -> dict[str, Any]:
        chunks: list[str] = []
        decoder = json.JSONDecoder()
        for match in ENQUEUE.finditer(html):
            try:
                value, _ = decoder.raw_decode(html[match.end():])
            except json.JSONDecodeError as exc:
                raise RuntimeError("Malformed React Router enqueue string") from exc
            if not isinstance(value, str):
                raise RuntimeError("React Router enqueue argument is not a string")
            chunks.append(value)
        if not chunks:
            raise RuntimeError("Missing React Router streamed SSR state")
        try:
            table = json.loads(chunks[0])
        except json.JSONDecodeError as exc:
            raise RuntimeError("Malformed React Router indexed root") from exc
        if not isinstance(table, list):
            raise RuntimeError("React Router indexed root is not an array")

        patches: dict[int, Any] = {}
        for chunk in chunks[1:]:
            match = PATCH.fullmatch(chunk)
            if not match:
                continue
            try:
                payload = json.loads(match.group(2))
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Malformed React Router patch P{match.group(1)}") from exc
            patch_id = int(match.group(1))
            if isinstance(payload, list):
                patches[patch_id] = len(table)
                table.extend(payload)
            else:
                patches[patch_id] = payload

        memo: dict[int, Any] = {}

        def resolve(value: Any) -> Any:
            if isinstance(value, int) and not isinstance(value, bool):
                return None if value < 0 else resolve_index(value)
            if isinstance(value, list):
                if len(value) == 2 and value[0] == "P" and isinstance(value[1], int):
                    return resolve(patches.get(value[1], -5))
                return [resolve(entry) for entry in value]
            if isinstance(value, dict):
                return {
                    str(resolve(int(key[1:]))): resolve(entry)
                    for key, entry in value.items()
                    if key.startswith("_") and key[1:].isdigit()
                }
            return value

        def resolve_index(index: int) -> Any:
            if index >= len(table):
                raise RuntimeError(f"React Router reference {index} is out of range")
            if index in memo:
                return memo[index]
            raw = table[index]
            if isinstance(raw, dict):
                target: dict[str, Any] = {}
                memo[index] = target
                target.update(resolve(raw))
                return target
            if isinstance(raw, list):
                if len(raw) == 2 and raw[0] == "P":
                    return resolve(raw)
                target_list: list[Any] = []
                memo[index] = target_list
                target_list.extend(resolve(raw))
                return target_list
            return raw

        result = resolve_index(0)
        if not isinstance(result, dict):
            raise RuntimeError("React Router resolved root is not an object")
        return result

    def _item(self, record: dict[str, Any], response, page: int, position: int, total: Any):
        description = record.get("description") if isinstance(record.get("description"), dict) else {}
        location = record.get("location") if isinstance(record.get("location"), dict) else {}
        address = location.get("address") if isinstance(location.get("address"), dict) else {}
        coordinate = address.get("coordinate") if isinstance(address.get("coordinate"), dict) else {}
        photo = record.get("primary_photo") if isinstance(record.get("primary_photo"), dict) else {}
        line1 = record.get("addressLine1") or address.get("line")
        line2 = record.get("addressLine2") or " ".join(filter(None, [address.get("city"), address.get("state_code"), address.get("postal_code")]))
        return {
            "item_id": str(record.get("property_id")),
            "listing_id": record.get("listing_id"),
            "title": ", ".join(filter(None, [line1, line2])),
            "address": line1, "city": address.get("city"), "state": address.get("state_code"),
            "postal_code": address.get("postal_code"),
            "url": urljoin("https://www.realtor.com/realestateandhomes-detail/", str(record.get("ldpSlug") or "")),
            "status": record.get("status"), "status_text": record.get("statusText"),
            "price": record.get("list_price"), "price_min": record.get("priceMin"),
            "price_max": record.get("priceMax"), "currency": "USD",
            "beds": description.get("beds"), "baths": description.get("baths_consolidated"),
            "sqft": description.get("sqft"), "lot_sqft": description.get("lot_sqft"),
            "property_type": description.get("type"),
            "latitude": coordinate.get("lat", record.get("lat")),
            "longitude": coordinate.get("lon", record.get("lng")),
            "image": photo.get("href"), "photo_count": record.get("photo_count"),
            "broker": record.get("brokerageName"), "builder": record.get("builder"),
            "flags": record.get("flags"), "has_3d_tour": record.get("has3DTour"),
            "has_video_tour": record.get("hasVideoTour"), "has_virtual_tour": record.get("hasVirtualTour"),
            "list_date": record.get("list_date"), "category": self.category,
            "listing_url": response.url, "page": page, "position": position,
            "total_count": total, "source": "realtor_react_router_stream",
            "timestamp": self.get_timestamp(), "raw": record,
        }
