from __future__ import annotations

"""RE/MAX sale listings from the Next.js RSC bootstrap state only."""

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.remax_categories import REMAX_CATEGORIES


_FLIGHT_CHUNK_RE = re.compile(
    r"self\.__next_f\.push\(\[\s*1\s*,\s*(\"(?:[^\"\\]|\\.)*\")\s*\]\)",
    re.DOTALL,
)
_RESULTS_MARKER = '"listingResultsUnfiltered":'
_RSC_SENTINELS = re.compile(r"^\$(?:undefined|@?[0-9A-Za-z_$][\w$]*|D[\w.+-]*|I-?[\w.]*)$")
_CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "failed to get successful response",
    "pardon the interruption",
)


class RemaxListingSpider(BaseListingSpider):
    """Extract the authoritative listing records hydrated into RE/MAX PLPs.

    RE/MAX uses the Next.js App Router.  Each server-rendered search page carries
    a ``listingResultsUnfiltered`` object in its React Server Component flight
    stream.  This spider reads that bootstrap record directly and deliberately
    does not parse rendered cards or JSON-LD.
    """

    name = "remax_listing"
    allowed_domains = ["remax.com", "www.remax.com"]
    categories = REMAX_CATEGORIES

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "listing_id", "mls_source_id", "property_id",
            "title", "address", "street", "city", "state", "postal_code", "url",
            "image_url", "image_urls", "image_count", "price", "currency", "beds",
            "baths", "living_area", "living_area_unit", "lot_size_acres",
            "property_type", "transaction_type", "is_rental", "banners",
            "open_houses", "agent_name", "agent_phone", "office_name",
            "office_phone", "office_email", "mls_name", "page", "position",
            "total_count", "source_url", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()

    def start_requests(self):
        self._seen.clear()
        base_url = self.resolve_target_url()
        yield scrapy.Request(
            self._page_url(base_url, 1),
            callback=self.parse,
            headers=self.headers,
            meta={"category": self.category, "base_url": base_url, "page": 1},
        )

    def parse(self, response: scrapy.http.Response):
        self._validate_response(response)
        state = self._bootstrap(response.text, response.url)
        listings = state.get("results")
        if not isinstance(listings, list):
            raise RuntimeError(
                f"RE/MAX RSC bootstrap has no listing result list at {response.url}"
            )

        page = int(response.meta.get("page", 1))
        total_count = self._integer(state.get("totalResults"))
        new_count = 0
        for position, record in enumerate(listings, start=1):
            if not isinstance(record, dict):
                continue
            raw = self._clean_rsc(record)
            item_id = str(
                raw.get("uniqueListingId") or raw.get("uPI") or raw.get("listingId") or ""
            ).strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            new_count += 1
            yield self._item(raw, response, page, position, total_count)

        if page < self.max_pages and listings and new_count:
            yield scrapy.Request(
                self._page_url(response.meta["base_url"], page + 1),
                callback=self.parse,
                headers=self.headers,
                meta={**response.meta, "page": page + 1},
                dont_filter=True,
            )

    def _item(
        self,
        raw: dict[str, Any],
        response: scrapy.http.Response,
        page: int,
        position: int,
        total_count: int | None,
    ) -> dict[str, Any]:
        location = raw.get("location") if isinstance(raw.get("location"), dict) else {}
        images = raw.get("listingImages") if isinstance(raw.get("listingImages"), list) else []
        image_urls = [image.get("src") for image in images if isinstance(image, dict) and image.get("src")]
        size = raw.get("listingSize") if isinstance(raw.get("listingSize"), dict) else {}
        address = raw.get("listingAddressFull") or location.get("listingAddressFull")
        listing_url = raw.get("listingUrl")
        return {
            "category": response.meta["category"],
            "item_id": str(raw.get("uniqueListingId") or raw.get("uPI") or raw.get("listingId")),
            "listing_id": raw.get("listingId"),
            "mls_source_id": raw.get("oUID"),
            "property_id": raw.get("uPI"),
            "title": address,
            "address": address,
            "street": raw.get("listingAddress1") or location.get("listingAddress1"),
            "city": location.get("city"),
            "state": location.get("state"),
            "postal_code": location.get("postalCode"),
            "url": urljoin("https://www.remax.com", listing_url) if listing_url else None,
            "image_url": image_urls[0] if image_urls else None,
            "image_urls": image_urls,
            "image_count": len(image_urls),
            "price": self._number(raw.get("listPriceRaw")),
            "currency": raw.get("currencyType") or "USD",
            "beds": self._number(raw.get("beds")),
            "baths": self._number(raw.get("baths")),
            "living_area": self._number(raw.get("livingArea") or size.get("value")),
            "living_area_unit": size.get("text"),
            "lot_size_acres": self._number(raw.get("lotSizeAcres")),
            "property_type": raw.get("propertyType"),
            "transaction_type": raw.get("uiTransactionType"),
            "is_rental": raw.get("isRental"),
            "banners": raw.get("banners") or [],
            "open_houses": raw.get("openHouses"),
            "agent_name": raw.get("listAgentFullName"),
            "agent_phone": raw.get("listAgentPreferredPhone"),
            "office_name": raw.get("listOfficeName"),
            "office_phone": raw.get("listOfficePhone"),
            "office_email": raw.get("listOfficeEmail"),
            "mls_name": raw.get("displayLogoAlt"),
            "page": page,
            "position": position,
            "total_count": total_count,
            "source_url": response.url,
            "source": "remax_nextjs_rsc_bootstrap",
            "raw": raw,
            "timestamp": self.job_timestamp,
        }

    @classmethod
    def _bootstrap(cls, document: str, url: str = "response") -> dict[str, Any]:
        chunks = _FLIGHT_CHUNK_RE.findall(document or "")
        if not chunks:
            raise RuntimeError(f"RE/MAX response has no Next.js RSC flight chunks at {url}")
        try:
            payload = "".join(json.loads(chunk) for chunk in chunks)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"RE/MAX RSC flight chunk is malformed at {url}: {exc}") from exc
        offset = payload.find(_RESULTS_MARKER)
        if offset < 0:
            raise RuntimeError(
                f"RE/MAX RSC bootstrap has no listingResultsUnfiltered object at {url}"
            )
        try:
            state, _ = json.JSONDecoder().raw_decode(payload, offset + len(_RESULTS_MARKER))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"RE/MAX listing bootstrap is malformed at {url}: {exc}") from exc
        if not isinstance(state, dict):
            raise RuntimeError(f"RE/MAX listing bootstrap is not an object at {url}")
        return cls._clean_rsc(state)

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        search_query: dict[str, Any] = {}
        if query.get("searchQuery"):
            try:
                decoded = json.loads(query["searchQuery"])
                if isinstance(decoded, dict):
                    search_query = decoded
            except json.JSONDecodeError:
                pass
        search_query["pageNumber"] = page
        if page == 1 and not query.get("searchQuery"):
            return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))
        query["searchQuery"] = json.dumps(search_query, separators=(",", ":"))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))

    @classmethod
    def _clean_rsc(cls, value: Any) -> Any:
        if isinstance(value, str):
            return None if _RSC_SENTINELS.match(value) else value
        if isinstance(value, list):
            return [cls._clean_rsc(entry) for entry in value]
        if isinstance(value, dict):
            return {key: cls._clean_rsc(entry) for key, entry in value.items()}
        return value

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if value in (None, "", "-") or isinstance(value, bool):
            return None
        try:
            number = float(str(value).replace(",", "").strip())
        except (TypeError, ValueError):
            return None
        return int(number) if number.is_integer() else number

    @classmethod
    def _integer(cls, value: Any) -> int | None:
        number = cls._number(value)
        return int(number) if number is not None else None

    @staticmethod
    def _validate_response(response: scrapy.http.Response) -> None:
        if response.status != 200:
            raise RuntimeError(f"RE/MAX returned HTTP {response.status}: {response.url}")
        head = response.text[:5000].lower()
        if len(response.body) < 5000 or any(marker in head for marker in _CHALLENGE_MARKERS):
            raise RuntimeError(f"RE/MAX returned a challenge/proxy response: {response.url}")
