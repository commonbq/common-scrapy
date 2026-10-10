from __future__ import annotations

"""Base spider helpers for listing/search spiders.

Category contract
-----------------
Listing spiders define ``categories`` as a **mapping of group -> leaf**:

    categories = {
        "<group>": {
            "<leaf>": "https://...",              # simple form
            "<leaf>": {"url": "https://...",      # rich form (keeps lookup fields)
                       "slug": "...", ...},
        },
        ...
    }

- ``group`` is a navigation parent (department, section, collection, ...).
- ``leaf`` is the crawl target name; it is what ``-a category=<leaf>`` selects
  and what the Airflow DAG factory schedules one task per.
- Rich leaf values keep any per-row fields the spider reads at runtime
  (``slug``, ``department``, ``category_name``, ...).

A flat ``{leaf: url}`` mapping (no nesting) is also accepted and normalised to a
single ``"all"`` group. The legacy ``[{"category", "url"}, ...]`` sequence is
still accepted for un-migrated spiders and normalised to the same single group.

Helpers: ``iter_categories()`` yields rich leaves ``{group, category, url, ...}``;
``category_entry(name)`` looks a leaf up across every group.
"""

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import scrapy

from datetime import datetime


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def group_categories(
    entries: Sequence[Mapping[str, Any]],
    group_field: str,
    *,
    leaf_field: str = "category",
) -> dict[str, dict[str, dict[str, Any]]]:
    """Group flat ``{category, url, ...}`` rows into the categories mapping.

    Every row's remaining fields are preserved as rich leaf values, so a spider
    that reads ``slug``/``department``/``category_name`` at runtime keeps them::

        group_categories(FOO_CATEGORIES, "department")
        # -> {"<department>": {"<category>": {"url": ..., "slug": ..., ...}}}

    A missing ``group_field`` falls back to a single ``"all"`` group.
    """
    groups: dict[str, dict[str, dict[str, Any]]] = {}
    for entry in entries:
        leaf = entry.get(leaf_field)
        if not isinstance(leaf, str) or not leaf:
            raise ValueError(
                f"{group_field}-grouped entry is missing string {leaf_field!r}"
            )
        group = entry.get(group_field) or "all"
        value = {k: v for k, v in entry.items() if k != leaf_field}
        value.setdefault("category", leaf)
        groups.setdefault(str(group), {})[leaf] = value
    return groups


@dataclass
class ListingArgs:
    max_pages: int = 1
    url: str | None = None
    category: str | None = None
    category_url: str | None = None


class BaseListingSpider(scrapy.Spider):
    """Base class to normalize common spider args and category handling."""

    args: ListingArgs
    # Listing spiders override with the mapping contract (see module docstring).
    categories: Mapping[str, Mapping[str, Any]] | Sequence[Mapping[str, Any]] = []
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
        self._category_cache: dict[str, dict[str, dict[str, Any]]] | None = None
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

    # ------------------------------------------------------------- categories

    @staticmethod
    def _leaf_entry(category: str, value: Any) -> dict[str, Any]:
        """Expand a leaf value into a rich dict carrying at least url/category."""
        if isinstance(value, str):
            return {"category": category, "url": value}
        if isinstance(value, Mapping):
            entry = dict(value)
            entry.setdefault("category", category)
            url = entry.get("url")
            # url may be absent/null when the spider builds requests from other
            # fields (e.g. academy resolves by category_id), but if present it
            # must be a usable string.
            if url is not None and (not isinstance(url, str) or not url):
                raise ValueError(
                    f"categories leaf {category!r} 'url' must be a non-empty string"
                )
            return entry
        raise ValueError(
            f"categories leaf {category!r} must be a url string or a mapping with 'url'"
        )

    def _normalise_categories(self) -> dict[str, dict[str, dict[str, Any]]]:
        """Return ``{group: {leaf: rich_leaf}}`` for any accepted input shape."""
        raw = self.categories

        if isinstance(raw, Mapping):
            # Flat ``{leaf: url}`` mapping -> one synthetic group.
            if raw and all(isinstance(v, str) for v in raw.values()):
                return {
                    "all": {
                        str(k): {"category": str(k), "url": v} for k, v in raw.items()
                    }
                }
            normalised: dict[str, dict[str, dict[str, Any]]] = {}
            for group, leaves in raw.items():
                group_name = str(group)
                if isinstance(leaves, Mapping):
                    normalised[group_name] = {
                        str(leaf): self._leaf_entry(str(leaf), value)
                        for leaf, value in leaves.items()
                    }
                elif isinstance(leaves, Sequence) and not isinstance(
                    leaves, (str, bytes)
                ):
                    bucket: dict[str, dict[str, Any]] = {}
                    for url in leaves:
                        if not isinstance(url, str):
                            raise ValueError(
                                f"categories[{group_name!r}] url list must contain strings"
                            )
                        slug = _slug(url.rstrip("/").rsplit("/", 1)[-1])
                        bucket[slug] = {"category": slug, "url": url}
                    normalised[group_name] = bucket
                elif isinstance(leaves, str):
                    normalised[group_name] = {
                        group_name: {"category": group_name, "url": leaves}
                    }
                else:
                    raise ValueError(
                        f"categories[{group_name!r}] must be a mapping or a list of urls"
                    )
            return normalised

        if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes)):
            leaves = {}
            for i, entry in enumerate(raw):
                if not isinstance(entry, Mapping):
                    raise ValueError(f"categories[{i}] must be a dict")
                category = entry.get("category")
                if not isinstance(category, str) or not category:
                    raise ValueError(f"categories[{i}] missing string 'category'")
                leaves[category] = self._leaf_entry(category, dict(entry))
            return {"all": leaves} if leaves else {}

        raise ValueError(
            "categories must be a mapping of {group: {leaf: url|mapping}} "
            "or a list of {'category','url'} dicts"
        )

    def _all_category_entries(self) -> dict[str, dict[str, dict[str, Any]]]:
        if getattr(self, "_category_cache", None) is None:
            self._category_cache = self._normalise_categories()
        return self._category_cache

    def iter_categories(self):
        """Yield rich leaf dicts: ``{group, category, url, **extras}``."""
        for group, leaves in self._all_category_entries().items():
            for entry in leaves.values():
                yield {"group": group, **entry}

    def category_entry(self, name: str) -> dict[str, Any] | None:
        """Look a leaf up across every group; return its rich entry or None."""
        for group, leaves in self._all_category_entries().items():
            entry = leaves.get(name)
            if entry is not None:
                return {"group": group, **entry}
        return None

    def available_categories(self) -> list[str]:
        return sorted(
            leaf for leaves in self._all_category_entries().values() for leaf in leaves
        )

    def resolve_target_url(self) -> str:
        """Resolve listing URL from url/category_url/category map.

        Priority: url > category_url > category lookup across all groups.
        """
        if self.args.url:
            return self.args.url
        if self.args.category_url:
            return self.args.category_url

        if self.args.category:
            entry = self.category_entry(self.args.category)
            if entry is not None:
                return entry.get("url", "")

        available = ", ".join(self.available_categories())
        raise ValueError(
            f"Unknown category '{self.args.category}'. Available categories: {available}"
        )

    def _validate_categories_schema_if_needed(self):
        if not self.require_category_arg:
            return
        raw = self.categories

        if isinstance(raw, Mapping):
            for group, leaves in raw.items():
                if not isinstance(group, str) or not group:
                    raise ValueError("categories group keys must be non-empty strings")
                if isinstance(leaves, str):
                    continue  # flat {name: url} mapping
                if isinstance(leaves, Mapping):
                    for leaf, value in leaves.items():
                        if not isinstance(leaf, str) or not leaf:
                            raise ValueError(
                                f"categories[{group!r}] leaf keys must be non-empty strings"
                            )
                        if isinstance(value, Mapping):
                            url = value.get("url")
                            if url is not None and (
                                not isinstance(url, str) or not url
                            ):
                                raise ValueError(
                                    f"categories[{group!r}][{leaf!r}] 'url' must be a "
                                    "non-empty string when present"
                                )
                        elif not isinstance(value, str) or not value:
                            raise ValueError(
                                f"categories[{group!r}][{leaf!r}] must be a url or mapping"
                            )
                elif isinstance(leaves, Sequence) and not isinstance(
                    leaves, (str, bytes)
                ):
                    if not all(isinstance(u, str) and u for u in leaves):
                        raise ValueError(
                            f"categories[{group!r}] must be a list of url strings"
                        )
                else:
                    raise ValueError(
                        f"categories[{group!r}] must be a mapping or a list of urls"
                    )
            return

        if not isinstance(raw, list) or not raw:
            raise ValueError(
                "Listing spider must define `categories` as a mapping of "
                "{group: {leaf: url|mapping}} (or a legacy list of "
                "{'category','url'} dicts)"
            )
        for i, entry in enumerate(raw):
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
