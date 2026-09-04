from __future__ import annotations

"""Base spider helpers for listing/search spiders.

Conventions:
- Listing spiders should define `categories` as:
  [
    {"category": "name", "url": "https://..."},
    ...
  ]
- Listing spiders must accept `-a category=<name>`.
- If `category` is missing/invalid, raise with available category names.
"""

from dataclasses import dataclass

import scrapy

from common.settings import PROXY
from datetime import datetime

@dataclass
class ListingArgs:
    max_pages: int = 1
    url: str | None = None
    category: str | None = None
    category_url: str | None = None


class BaseListingSpider(scrapy.Spider):
    """Base class to normalize common spider args and category handling."""

    args: ListingArgs
    # Listing spiders should override with the required format.
    categories: list[dict[str, str]] = []
    # BaseSearchSpider overrides this to False.
    require_category_arg: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_listing_args(
            max_pages=kwargs.get("max_pages", 1),
            url=kwargs.get("url"),
            category=kwargs.get("category"),
            category_url=kwargs.get("category_url"),
        )
        self._validate_categories_schema_if_needed()
        if self.require_category_arg:
            self._require_category_arg()

        self.job_timestamp = datetime.utcnow()

    def get_timestamp(self) -> datetime:
        return datetime.utcnow()

    def init_listing_args(
        self,
        *,
        max_pages: int | str | None = 1,
        url: str | None = None,
        category: str | None = None,
        category_url: str | None = None,
    ) -> ListingArgs:
        self.args = ListingArgs(
            max_pages=int(max_pages or 1),
            url=(url or "").strip() or None,
            category=(category or "").strip() or None,
            category_url=(category_url or "").strip() or None,
        )
        return self.args

    @property
    def max_pages(self) -> int:
        return self.args.max_pages

    @max_pages.setter
    def max_pages(self, value: int | str):
        self.args.max_pages = int(value)

    @property
    def url(self) -> str | None:
        return self.args.url

    @url.setter
    def url(self, value: str | None):
        self.args.url = (value or "").strip() or None

    @property
    def category(self) -> str | None:
        return self.args.category

    @category.setter
    def category(self, value: str | None):
        self.args.category = (value or "").strip() or None

    @property
    def category_url(self) -> str | None:
        return self.args.category_url

    @category_url.setter
    def category_url(self, value: str | None):
        self.args.category_url = (value or "").strip() or None

    def proxy_meta(self, meta: dict | None = None) -> dict:
        meta = dict(meta or {})
        if PROXY:
            meta["proxy"] = PROXY
        return meta

    # Backwards-compatible alias retained for compatibility.
    def maybe_proxy_meta(self, meta: dict | None = None) -> dict:
        return dict(meta or {})

    def available_categories(self) -> list[str]:
        names: list[str] = []
        for entry in self.categories or []:
            if isinstance(entry, dict) and isinstance(entry.get("category"), str):
                names.append(entry["category"])
        return sorted(names)

    def resolve_target_url(self) -> str:
        """Resolve listing URL from url/category_url/category map.

        Priority: url > category_url > category lookup in categories[].
        """
        if self.args.url:
            return self.args.url
        if self.args.category_url:
            return self.args.category_url

        if self.args.category:
            for entry in self.categories or []:
                if entry.get("category") == self.args.category:
                    return entry.get("url", "")

        available = ", ".join(self.available_categories())
        raise ValueError(f"Unknown category '{self.args.category}'. Available categories: {available}")

    def _validate_categories_schema_if_needed(self):
        if not self.require_category_arg:
            return
        if not isinstance(self.categories, list) or not self.categories:
            raise ValueError("Listing spider must define `categories` as a non-empty list of {'category','url'} dicts")
        for i, entry in enumerate(self.categories):
            if not isinstance(entry, dict):
                raise ValueError(f"categories[{i}] must be a dict")
            if not isinstance(entry.get("category"), str) or not entry.get("category"):
                raise ValueError(f"categories[{i}] missing string 'category'")
            if not isinstance(entry.get("url"), str) or not entry.get("url"):
                raise ValueError(f"categories[{i}] missing string 'url'")

    def _require_category_arg(self):
        if self.args.category:
            return
        available = ", ".join(self.available_categories())
        raise ValueError(f"Provide -a category=<name>. Available categories: {available}")
