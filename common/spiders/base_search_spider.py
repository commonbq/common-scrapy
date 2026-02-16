from __future__ import annotations

"""Base spider helpers for keyword-search spiders.

Standard args:
- q: keyword query (required)
- max_pages: int (default 1)
"""

from dataclasses import dataclass

from common.spiders.base_listing_spider import BaseListingSpider


@dataclass
class SearchArgs:
    q: str | None = None
    max_pages: int = 1


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
    ) -> SearchArgs:
        self.search_args = SearchArgs(
            q=(q or "").strip() or None,
            max_pages=int(max_pages or 1),
        )
        self.max_pages = self.search_args.max_pages
        if not self.search_args.q:
            raise ValueError("Provide -a q=<term>")
        return self.search_args

    @property
    def q(self) -> str | None:
        return getattr(self, "search_args", SearchArgs()).q

    @property
    def search_max_pages(self) -> int:
        return getattr(self, "search_args", SearchArgs(max_pages=1)).max_pages
