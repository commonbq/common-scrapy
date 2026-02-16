from __future__ import annotations

"""Base spider helpers for keyword-search spiders.

Standard args:
- q: keyword query (required)
- max_pages: int (default 1)
"""

from common.spiders.base_listing_spider import BaseListingSpider, ListingArgs


class BaseSearchSpider(BaseListingSpider):
    """Base class for keyword-search spiders."""

    # Search spiders do not require listing category maps.
    require_category_arg: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_search_args(
            q=kwargs.get("q"),
            max_pages=kwargs.get("max_pages", 1),
        )

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
