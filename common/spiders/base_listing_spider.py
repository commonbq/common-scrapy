from __future__ import annotations

"""Base spider helpers for listing/search spiders.

Goal: standardize common arguments and behaviors across purpose-built spiders.

Common args (convention):
- max_pages: int (default 1)
- url: optional override (full URL)
- category: optional category id/name
- category_url: optional category URL
- q: optional keyword query (for *search* spiders)

This base class does NOT implement crawling logic; spiders still implement
start_requests/parse.
"""

from dataclasses import dataclass

import scrapy

from common.settings import PROXY


@dataclass
class ListingArgs:
    max_pages: int = 1
    url: str | None = None
    category: str | None = None
    category_url: str | None = None
    q: str | None = None


class BaseListingSpider(scrapy.Spider):
    """Base class to normalize common spider args."""

    args: ListingArgs

    def init_listing_args(
        self,
        *,
        max_pages: int | str | None = 1,
        url: str | None = None,
        category: str | None = None,
        category_url: str | None = None,
        q: str | None = None,
    ) -> ListingArgs:
        self.args = ListingArgs(
            max_pages=int(max_pages or 1),
            url=(url or "").strip() or None,
            category=(category or "").strip() or None,
            category_url=(category_url or "").strip() or None,
            q=(q or "").strip() or None,
        )
        return self.args

    def proxy_meta(self, meta: dict | None = None) -> dict:
        meta["proxy"] = PROXY
        return meta
