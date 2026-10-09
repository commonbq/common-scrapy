from __future__ import annotations

import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.parse import quote, urlencode, urlsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.wickes_categories import WICKES_CATEGORIES


_PRODUCT_STATE_RE = re.compile(
    r"\bvar\s+product\s*=\s*(\{.*?\})\s*(?=var\s+currentPosition)",
    re.DOTALL,
)
_JS_KEY_RE = re.compile(r"([,{]\s*)([A-Za-z_$][\w$]*)\s*:")
_CATEGORY_CODE_RE = re.compile(r"/c/(\d+)(?:[/?#]|$)")
_CHALLENGE_MARKERS = (
    "access denied",
    "captcha",
    "failed to get successful response",
    "request unsuccessful",
)


class WickesListingSpider(BaseListingSpider):
    """Wickes products from the server-rendered analytics bootstrap only.

    Both the initial PLP and each load-more response initialise the same
    ``var product = {...}`` analytics records. Those records are the sole
    product-data direction: rendered product cards and JSON-LD are not parsed.
    """

    name = "wickes_listing"
    allowed_domains = ["wickes.co.uk", "www.wickes.co.uk", "localhost", "127.0.0.1"]
    categories = WICKES_CATEGORIES

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "brand", "product_category",
            "variant", "url", "price", "currency", "page", "position",
            "source_url", "source", "raw", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen: set[str] = set()
        target_url = self.resolve_target_url()
        match = _CATEGORY_CODE_RE.search(urlsplit(target_url).path)
        if not match:
            raise ValueError(f"Wickes category URL has no numeric /c/<id>: {target_url}")
        self._category_code = match.group(1)
        self._target_url = target_url

    def start_requests(self):
        self._seen.clear()
        yield scrapy.Request(
            self._target_url,
            callback=self.parse,
            headers=self._headers(),
            meta={"page": 1},
            dont_filter=True,
        )

    def parse(self, response: scrapy.http.Response):
        self._reject_bad_response(response)
        page = int(response.meta.get("page", 1))
        records = self.extract_bootstrap_products(response.text)
        if not records:
            if page == 1:
                raise RuntimeError(
                    f"Wickes response has no analytics product bootstrap: {response.url}"
                )
            return

        emitted = 0
        for position, record in enumerate(records, 1):
            item_id = self._string(record.get("id"))
            title = self._string(record.get("name"))
            if not item_id or not title or item_id in self._seen:
                continue
            self._seen.add(item_id)
            emitted += 1
            yield {
                "category": self.category,
                "item_id": item_id,
                "title": title,
                "brand": self._string(record.get("brand")),
                "product_category": self._string(record.get("category")),
                "variant": self._string(record.get("variant")),
                "url": f"https://www.wickes.co.uk/p/{quote(item_id, safe='')}",
                "price": self._number(record.get("price")),
                "currency": "GBP",
                "page": page,
                "position": position,
                "source_url": response.url,
                "source": "wickes_analytics_bootstrap",
                "raw": record,
                "timestamp": self.get_timestamp(),
            }

        if emitted and page < self.max_pages:
            yield scrapy.Request(
                self._results_url(page),
                callback=self.parse,
                headers=self._headers(),
                meta={"page": page + 1},
                dont_filter=True,
            )

    @staticmethod
    def extract_bootstrap_products(text: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for match in _PRODUCT_STATE_RE.finditer(text):
            # Hybris escapes apostrophes inside its double-quoted JavaScript
            # strings (``Collector\'s``). That is valid JavaScript but not a
            # valid JSON escape, so remove only that redundant escape before
            # handing the otherwise JSON-compatible literal to json.loads.
            json_text = match.group(1).replace("\\'", "'")
            json_text = _JS_KEY_RE.sub(r'\1"\2":', json_text)
            try:
                record = json.loads(json_text)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Malformed Wickes analytics product bootstrap: {exc}") from exc
            if isinstance(record, dict):
                records.append(record)
        return records

    def _results_url(self, page: int) -> str:
        query = urlencode({"q": ":relevance", "page": page, "sort": "relevance"})
        return f"https://www.wickes.co.uk/c/{self._category_code}/results/view?{query}"

    @staticmethod
    def _headers() -> dict[str, str]:
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
        }

    @staticmethod
    def _string(value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _number(value: Any) -> int | float | None:
        try:
            number = Decimal(str(value).replace(",", "").strip())
        except (InvalidOperation, ValueError, AttributeError):
            return None
        return int(number) if number == number.to_integral() else float(number)

    @staticmethod
    def _reject_bad_response(response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(f"Wickes returned HTTP {response.status}: {response.url}")
        lower = response.text[:200_000].lower()
        if any(marker in lower for marker in _CHALLENGE_MARKERS):
            raise RuntimeError(f"Wickes returned a challenge/proxy page: {response.url}")
