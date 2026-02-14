from __future__ import annotations

"""Base spider helpers for keyword-search spiders.

Standard args (convention):
- q: keyword query (required)
- max_pages: int (default 1)
- use_proxy: 0/1 (default 0)

This base class does NOT implement crawling logic.
"""

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider, ListingArgs


class BaseSearchSpider(BaseListingSpider):
    """Base class for keyword-search spiders."""

    def init_search_args(
        self,
        *,
        q: str | None = None,
        max_pages: int | str | None = 1,
        use_proxy: int | str | None = 0,
    ) -> ListingArgs:
        args = self.init_listing_args(max_pages=max_pages, use_proxy=use_proxy, q=q)
        if not args.q:
            raise ValueError("Provide -a q=<term>")
        return args
