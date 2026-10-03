"""Michaels (michaels.com) category inventory, derived from the category sitemap.

Source of truth: https://www.michaels.com/sitemap_MIK_category.xml

The sitemap is advertised in ``robots.txt`` and carries every PLP the storefront
can render, as an absolute ``<loc>`` URL of the form::

    https://www.michaels.com/shop/<department>/<subcategory>/[/<leaf>]

Verified 2026-10-04 through the repository's configured proxy: 3,611 category
URLs, all unique, nested under 33 top-level departments, up to five levels deep.

Why the sitemap and not the header navigation: the PLP is a Next.js App Router
page whose React Server Component payload (``self.__next_f``) embeds the whole
taxonomy tree, but only for the branch being viewed -- the megamenu links to
departments the sitemap does not spell out as leaf paths, and several header
entries are campaign landing pages that hydrate zero products. The sitemap is
the only source that enumerates the complete set, so it is the single category
source this spider uses.

The inventory is **not** committed as a 3,611-entry literal. It is parsed from
the sitemap at crawl time, so a taxonomy change is picked up on the next run
instead of going stale in a committed snapshot, and the diff stays reviewable.
"""

from __future__ import annotations

import re
from typing import Any

MICHAELS_SITE_BASE = "https://www.michaels.com"
MICHAELS_CATEGORY_SITEMAP_URL = f"{MICHAELS_SITE_BASE}/sitemap_MIK_category.xml"

_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.IGNORECASE)

# The PLP always routes through /shop/; anything else in the category sitemap is
# not a product listing (e.g. a help or brand landing page).
_SHOP_PREFIX = "/shop/"


def category_path_parts(url: str) -> list[str]:
    """`.../shop/kids/art-supplies/art-storage` -> ``['kids', 'art-supplies', 'art-storage']``.

    Strips the scheme/host and every other prefix segment so the caller gets the
    taxonomy path itself. Returns ``[]`` for a non-``/shop/`` URL.
    """
    path = (url or "").split("#", 1)[0].split("?", 1)[0].strip()
    marker = "michaels.com"
    if marker in path:
        path = path.split(marker, 1)[-1]
    segments = [segment for segment in path.split("/") if segment]
    if not segments or segments[0] != "shop":
        return []
    return segments[1:]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def parse_category_sitemap(payload: str | bytes) -> list[dict[str, str]]:
    """Parse the category sitemap into ``BaseListingSpider.categories`` entries.

    Each entry is ``{"category", "department", "subcategory", "url"}``. The
    ``category`` value is the leaf slug, or ``<department>-<leaf>`` when that leaf
    slug is already taken by a different department -- 648 of the 3,611 leaves
    repeat (``decor``, ``pencils``, ``lanterns``, ...), so keying on the bare leaf
    alone would silently collapse two departments into one.
    """
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", "replace")

    paths: list[list[str]] = []
    seen_urls: set[str] = set()
    for match in _LOC_RE.finditer(payload or ""):
        url = match.group(1).strip()
        if url in seen_urls:
            continue
        parts = category_path_parts(url)
        if not parts:
            continue
        seen_urls.add(url)
        paths.append(parts)

    leaf_counts: dict[str, int] = {}
    for parts in paths:
        leaf = parts[-1]
        leaf_counts[leaf] = leaf_counts.get(leaf, 0) + 1

    categories: list[dict[str, str]] = []
    used: set[str] = set()
    for parts in paths:
        department, leaf = parts[0], parts[-1]
        name = leaf if leaf_counts[leaf] == 1 else f"{_slug(department)}-{leaf}"
        # Belt and braces: a department can itself repeat a leaf ("food/crafts"
        # under two roots), so keep disambiguating until the name is free.
        candidate, suffix = name, 2
        while candidate in used:
            candidate = f"{name}-{suffix}"
            suffix += 1
        used.add(candidate)
        url = "/".join([MICHAELS_SITE_BASE, _SHOP_PREFIX.strip("/"), *parts]) + "/"
        categories.append(
            {
                "category": candidate,
                "department": department,
                "subcategory": "/".join(parts[1:]) or department,
                "url": url,
            }
        )
    return categories


def category_index(categories: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """``category`` slug -> inventory entry, for ``-a category=<slug>`` lookup."""
    return {entry["category"]: entry for entry in categories}


def resolve_category(
    categories: list[dict[str, str]],
    *,
    category: str | None = None,
    category_url: str | None = None,
    url: str | None = None,
) -> dict[str, str] | None:
    """Resolve the CLI args to one inventory entry, or ``None`` when unscoped.

    Resolution order is url > category_url > category, matching
    :meth:`BaseListingSpider.resolve_target_url`. A URL is matched on its
    normalized ``/shop/`` path so a trailing slash, an absolute URL and a bare
    path all hit the same entry.
    """
    if category:
        index = category_index(categories)
        entry = index.get(category)
        if entry is not None:
            return entry
        # Fall back to a URL-shaped category arg so `-a category=/shop/...` works.
        if "/" in category:
            return resolve_category(
                categories, category_url=category
            )
        return None

    target = category_url or url
    if not target:
        return None
    wanted = category_path_parts(target)
    if not wanted:
        return None
    for entry in categories:
        if category_path_parts(entry["url"]) == wanted:
            return entry
    return None


def available_categories(categories: list[dict[str, str]], limit: int = 10) -> list[Any]:
    """A short, deterministic sample of category slugs for error messages."""
    return [entry["category"] for entry in categories[:limit]]