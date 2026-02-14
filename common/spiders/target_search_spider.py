from __future__ import annotations

"""Target search spider.

This is the renamed version of the original `target_listing` spider.

- New name: `target_search`
- Backwards-compatible alias remains as `target_listing` (deprecated)
"""

import json
import re
from typing import Iterable, Optional
from urllib.parse import quote

import scrapy

from common.settings import PROXY


class TargetSearchSpider(scrapy.Spider):
    """Target category/search spider using Target's internal (RedSky) API.

    Required:
    - Provide a category, either as `-a category=5xtc0` (Target category id),
      or `-a category_url='https://www.target.com/c/women-s-shoes/-/N-5xtc0'`.

    Optional:
    - `-a keyword=<term>` to combine keyword search within a category.
    """

    name = "target_search"
    allowed_domains = ["target.com", "www.target.com", "redsky.target.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(
        self,
        category: str | None = None,
        category_url: str | None = None,
        keyword: str | None = None,
        max_pages: str | int | None = 1,
        page_size: str | int | None = 24,
        use_proxy: str | int | None = 0,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.category_url = (category_url or "").strip() or None
        self.category = (category or "").strip() or None
        self.keyword = (keyword or "").strip() or None

        if not (self.category or self.category_url):
            raise ValueError("Provide -a category=<id> or -a category_url=<target category url>")

        if not self.category and self.category_url:
            # Extract Target category id from URLs like: /c/.../-/N-5xtc0
            m = re.search(r"/N-([a-z0-9]+)", self.category_url, flags=re.I)
            if m:
                self.category = m.group(1)

        if not self.category:
            raise ValueError("Could not derive category id. Provide -a category=<id> (e.g. 5xtc0)")
        self.max_pages = int(max_pages or 1)
        self.page_size = int(page_size or 24)
        self.use_proxy = bool(int(use_proxy or 0))
        self._redsky_key: Optional[str] = None
        self._visitor_id: Optional[str] = None

    def start_requests(self) -> Iterable[scrapy.Request]:
        # Use a category page as referer/seed. If the user didn't provide a URL,
        # we build a minimal one.
        if self.category_url:
            url = self.category_url
        else:
            url = f"https://www.target.com/c/-/N-{quote(self.category)}"

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
        return scrapy.Request(
            url,
            headers=headers,
            meta=meta,
            callback=getattr(self, cb),
            dont_filter=dont_filter,
        )

    def _make_redsky_request(self, *, offset: int) -> scrapy.Request:
        assert self._redsky_key
        base = "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"

        page_path = None
        if self.category_url:
            page_path = re.sub(r"^https?://www\.target\.com", "", self.category_url)
        if not page_path:
            page_path = f"/c/-/N-{self.category}"

        params = {
            "key": self._redsky_key,
            "channel": "WEB",
            "count": str(self.page_size),
            "offset": str(offset),
            "page": page_path,
            "pricing_store_id": "3991",
            "visitor_id": self._ensure_visitor_id(),
            "category": self.category,
        }
        if self.keyword:
            params["keyword"] = self.keyword
        qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        url = f"{base}?{qs}"

        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "referer": (self.category_url or f"https://www.target.com/c/-/N-{quote(self.category)}"),
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        }

        meta = {"handle_httpstatus_all": True}
        if self.use_proxy and PROXY:
            meta["proxy"] = PROXY

        return scrapy.Request(
            url,
            headers=headers,
            meta=meta,
            callback=self.parse_redsky,
            dont_filter=True,
        )

    def _ensure_visitor_id(self) -> str:
        if not self._visitor_id:
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

        keys = re.findall(r"\bkey=([a-f0-9]{32})\b", html, flags=re.I)
        key = keys[0] if keys else None
        if not key:
            keys = re.findall(r'"key"\s*:\s*"([a-f0-9]{32})"', html, flags=re.I)
            key = keys[0] if keys else None

        if not key:
            self.logger.warning(
                "Could not discover Target RedSky key from HTML; trying known fallback key"
            )
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

        products = (
            (((data.get("data") or {}).get("search") or {}).get("products"))
            or (((data.get("data") or {}).get("search") or {}).get("items"))
        )
        if not isinstance(products, list):
            self.logger.warning(
                "Unexpected RedSky shape. top_keys=%s", list(data.keys())[:20]
            )
            return

        for p in products:
            if isinstance(p, dict):
                yield self._normalize_product(p)

        m = re.search(r"[?&]offset=(\d+)", response.url)
        offset = int(m.group(1)) if m else 0

        search = (data.get("data") or {}).get("search") or {}
        total = (
            search.get("search_response")
            and search["search_response"].get("typed_metadata", {}).get("total_results")
        )
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
        item = p.get("item") or {}
        pd = item.get("product_description") or {}

        title = p.get("title") or p.get("product_title") or p.get("name") or pd.get("title")
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

        if not image and isinstance(item, dict):
            enrichment = item.get("enrichment") or {}
            imgs = enrichment.get("images")
            if isinstance(imgs, dict):
                image = imgs.get("primary_image_url") or (imgs.get("alternate_image_urls") or [None])[0]
            elif isinstance(imgs, list) and imgs:
                first = imgs[0]
                if isinstance(first, dict):
                    image = first.get("url") or first.get("base_url")

        return {
            "product_id": tcin,
            "name": title,
            "price": price,
            "url": url,
            "image": image,
            "raw": p,
        }
