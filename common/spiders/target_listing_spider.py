from __future__ import annotations

import json
import re
from typing import Iterable, Optional
from urllib.parse import quote

import scrapy

from common.settings import PROXY


class TargetListingSpider(scrapy.Spider):
    """Target product listing spider using Target's internal (RedSky) API.

    Strategy:
    1) Fetch Target search HTML (public page) to discover the current RedSky `key`.
    2) Call RedSky PLP Search API (`plp_search_v2`) with pagination (offset/count).

    Usage examples:
      - Keyword search:
        scrapy crawl target_listing -a keyword=sneakers

      - Specify max_pages (default 1):
        scrapy crawl target_listing -a keyword=sneakers -a max_pages=3

    Notes:
    - Target's API key can rotate. We try to extract it from the HTML.
    - If `PROXY` is configured (common/settings/base.py reads .env), you can force
      proxying by passing `-a use_proxy=1`.
    """

    name = "target_listing"
    allowed_domains = ["target.com", "www.target.com", "redsky.target.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(
        self,
        keyword: str | None = None,
        max_pages: str | int | None = 1,
        page_size: str | int | None = 24,
        use_proxy: str | int | None = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not keyword:
            raise ValueError("Provide -a keyword=<term>")
        self.keyword = keyword
        self.max_pages = int(max_pages or 1)
        self.page_size = int(page_size or 24)
        self.use_proxy = bool(int(use_proxy or 0))
        self._redsky_key: Optional[str] = None
        self._visitor_id: Optional[str] = None

    def start_requests(self) -> Iterable[scrapy.Request]:
        url = f"https://www.target.com/s?searchTerm={quote(self.keyword)}"
        yield self._make_request(url, cb="parse_search_html", dont_filter=True)

    def _make_request(self, url: str, *, cb: str, dont_filter: bool = False) -> scrapy.Request:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        meta = {"handle_httpstatus_all": True}
        if self.use_proxy and PROXY:
            meta["proxy"] = PROXY
        return scrapy.Request(url, headers=headers, meta=meta, callback=getattr(self, cb), dont_filter=dont_filter)

    def _make_redsky_request(self, *, offset: int) -> scrapy.Request:
        assert self._redsky_key
        base = "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"

        # Minimal params that work for PLP searches.
        params = {
            "key": self._redsky_key,
            "keyword": self.keyword,
            # Must be an enum value; lowercase `web` triggers a 400.
            "channel": "WEB",
            "count": str(self.page_size),
            "offset": str(offset),
            # Required by the API.
            "page": f"/s?searchTerm={self.keyword}",
            "pricing_store_id": "3991",
            "visitor_id": self._ensure_visitor_id(),
        }
        qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        url = f"{base}?{qs}"

        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "referer": f"https://www.target.com/s?searchTerm={quote(self.keyword)}",
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

        meta = {"handle_httpstatus_all": True}
        if self.use_proxy and PROXY:
            meta["proxy"] = PROXY

        return scrapy.Request(url, headers=headers, meta=meta, callback=self.parse_redsky, dont_filter=True)

    def _ensure_visitor_id(self) -> str:
        if not self._visitor_id:
            # Target appears to accept UUID v4 as visitor_id.
            import uuid

            self._visitor_id = str(uuid.uuid4())
        return self._visitor_id

    def parse_search_html(self, response: scrapy.http.Response):
        if response.status != 200:
            self.logger.warning(
                "Target search HTML non-200. status=%s proxy=%s url=%s head=%r",
                response.status,
                bool(response.meta.get("proxy")),
                response.url,
                (response.text or "")[:200],
            )

        html = response.text or ""

        # Try to find the RedSky API key in the HTML.
        # Common pattern: ...redsky_aggregations...key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        keys = re.findall(r"\bkey=([a-f0-9]{32})\b", html, flags=re.I)
        key = keys[0] if keys else None
        if not key:
            # Sometimes key appears as JSON field: "key":"..."
            keys = re.findall(r'"key"\s*:\s*"([a-f0-9]{32})"', html, flags=re.I)
            key = keys[0] if keys else None

        if not key:
            self.logger.warning("Could not discover Target RedSky key from HTML; trying known fallback key")
            # Known public key (can rotate). If this stops working, we need a fresh HTML capture.
            key = "9f36aeafbe6070d7c5b2a22f2f63c6fd"

        self._redsky_key = key
        yield self._make_redsky_request(offset=0)

    def parse_redsky(self, response: scrapy.http.Response):
        if response.status != 200:
            self.logger.warning(
                "RedSky non-200. status=%s proxy=%s url=%s head=%r",
                response.status,
                bool(response.meta.get("proxy")),
                response.url,
                (response.text or "")[:250],
            )
            return

        try:
            data = json.loads(response.text)
        except Exception:
            self.logger.exception("Failed to parse RedSky JSON")
            return

        # Best-effort: search in a few known paths.
        products = (
            (((data.get("data") or {}).get("search") or {}).get("products"))
            or (((data.get("data") or {}).get("search") or {}).get("items"))
        )
        if not isinstance(products, list):
            # Some responses wrap differently; log keys for debugging.
            self.logger.warning("Unexpected RedSky shape. top_keys=%s", list(data.keys())[:20])
            return

        for p in products:
            if not isinstance(p, dict):
                continue
            yield self._normalize_product(p)

        # Pagination: offset is in query string.
        m = re.search(r"[?&]offset=(\d+)", response.url)
        offset = int(m.group(1)) if m else 0

        # Attempt to determine total.
        total = None
        search = (data.get("data") or {}).get("search") or {}
        total = search.get("search_response") and search["search_response"].get("typed_metadata", {}).get("total_results")
        if total is None:
            total = search.get("total_results") or search.get("total")

        next_offset = offset + self.page_size
        current_page = (offset // self.page_size) + 1

        if self.max_pages and current_page >= self.max_pages:
            return

        if isinstance(total, int) and next_offset >= total:
            return

        yield self._make_redsky_request(offset=next_offset)

    def _normalize_product(self, p: dict) -> dict:
        # These field names vary a bit by response shape.
        item = p.get("item") or {}
        pd = item.get("product_description") or {}

        title = (
            p.get("title")
            or p.get("product_title")
            or p.get("name")
            or pd.get("title")
        )
        tcin = p.get("tcin") or p.get("id")

        price = None
        price_block = p.get("price") or p.get("pricing") or {}
        if isinstance(price_block, dict):
            price = (
                price_block.get("formatted_current_price")
                or price_block.get("current_retail")
                or price_block.get("current")
                or price_block.get("value")
            )

        url = p.get("url") or (item.get("enrichment") or {}).get("buy_url")
        if url and url.startswith("/"):
            url = "https://www.target.com" + url

        image = None
        images = p.get("images") or p.get("image") or {}
        if isinstance(images, dict):
            image = images.get("primary_uri") or images.get("base_url")
        if not image and isinstance(p.get("item"), dict):
            image = (((p["item"].get("enrichment") or {}).get("images") or [{}])[0] or {}).get("base_url")

        return {
            "product_id": tcin,
            "name": title,
            "price": price,
            "url": url,
            "image": image,
            "raw": p,
        }
