from __future__ import annotations

"""Base spider helpers for keyword-search spiders.

Standard args (convention):
- q: keyword query (required)
- max_pages: int (default 1)

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
    ) -> ListingArgs:
        args = self.init_listing_args(max_pages=max_pages, q=q)
        if not args.q:
            raise ValueError("Provide -a q=<term>")
        return args
