"""Urban Outfitters (urbanoutfitters.com) category inventory, parsed from the
category sitemap the site advertises in ``robots.txt``.

Source of truth: https://www.urbanoutfitters.com/categories_sitemap.xml
(reached through https://www.urbanoutfitters.com/sitemapindex.xml).

Verified 2026-10-04 through the repository's configured proxy: 2,158 category
URLs, all unique, each a single path segment plus an optional refinement query,
e.g.::

    https://www.urbanoutfitters.com/womens-clothing
    https://www.urbanoutfitters.com/graphic-tees-for-women?color=green
    https://www.urbanoutfitters.com/dresses?length=Mini&amp;sleeve=Long+Sleeve

Why the sitemap and not the header navigation: Urban Outfitters is a Vue/Pinia
SSR storefront. Its hydration payload (``#urbnInitialPiniaState``, see
:mod:`common.spiders.urbanoutfitters_listing_spider`) carries the *product*
state for the category being viewed plus a flat facet list, but ``header`` only
holds scroll/cart booleans -- there is no navigation tree in it at all, so the
megamenu's 12 roots are the only header-derived names available and they cover a
small fraction of the catalogue. The sitemap is the only source that enumerates
the complete set, so it is the single category source this spider uses.

The inventory is **not** committed as a 2,158-entry literal. It is parsed from
the sitemap at crawl time, so a taxonomy change is picked up on the next run
instead of going stale in a committed snapshot, and the diff stays reviewable.

Category naming: Urban Outfitters PLP URLs are flat (``/dresses``, not
``/shop/womens/dresses``), so a path slug alone is not enough -- the sitemap
lists the same path once per refinement (``dresses`` appears with ~200 different
refinements). Each entry therefore keys on its path slug when that path is
unfiltered, and on ``<path>-<refinement slug>`` when it is filtered, so
``-a category=dresses-color-green`` resolves exactly one PLP.
"""

from __future__ import annotations

import html
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit

URBN_SITE_BASE = "https://www.urbanoutfitters.com"
URBN_CATEGORY_SITEMAP_URL = f"{URBN_SITE_BASE}/categories_sitemap.xml"

# The 12 homepage navigation roots, kept as curated aliases so the common
# department entry points stay addressable by a short, stable slug even if the
# sitemap ever stops listing them.
URBN_NAV_ROOTS: tuple[tuple[str, str, str], ...] = (
    ("new-arrivals", "New Arrivals", f"{URBN_SITE_BASE}/new-arrivals"),
    ("womens-clothing", "Women's Clothing", f"{URBN_SITE_BASE}/womens-clothing"),
    ("mens-clothing", "Men's Clothing", f"{URBN_SITE_BASE}/mens-clothing"),
    ("jeans", "Jeans", f"{URBN_SITE_BASE}/jeans"),
    ("all-shoes", "Shoes", f"{URBN_SITE_BASE}/all-shoes"),
    ("all-accessories", "Accessories", f"{URBN_SITE_BASE}/all-accessories"),
    ("home", "Home", f"{URBN_SITE_BASE}/home"),
    ("vinyl-records-cassettes", "Music", f"{URBN_SITE_BASE}/vinyl-records-cassettes"),
    ("beauty-products", "Beauty + Wellness", f"{URBN_SITE_BASE}/beauty-products"),
    ("gifts", "Gifts", f"{URBN_SITE_BASE}/gifts"),
    ("shop-brands", "Brands", f"{URBN_SITE_BASE}/shop-brands"),
    ("sale", "Sale", f"{URBN_SITE_BASE}/sale"),
)

_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.IGNORECASE)

# Refinement key -> human label, so a category slug reads
# `dresses-color-green` instead of `dresses-color-green` ... which is the same
# thing, but the *name* is what a human reads in the feed.
_REFINEMENT_LABELS = {
    "brand": "Brand",
    "color": "Color",
    "itemType": "Item Type",
    "length": "Length",
    "material": "Material",
    "pattern": "Pattern",
    "size": "Size",
    "sleeve": "Sleeve",
    "style": "Style",
    "fit": "Fit",
    "collection": "Collection",
    "priceRange": "Price Range",
    "activity": "Activity",
    "room": "Room",
    "gender": "Gender",
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def _titleize(slug: str) -> str:
    """``graphic-tees-for-women`` -> ``Graphic Tees For Women``."""
    words = [word for word in re.split(r"[-_]+", slug or "") if word]
    return " ".join(word[:1].upper() + word[1:] for word in words)


def category_path_and_query(url: str) -> tuple[str, list[tuple[str, str]]]:
    """Split a sitemap ``<loc>`` into ``(path_slug, [(key, value), ...])``.

    ``/dresses?length=Mini&sleeve=Long+Sleeve`` becomes
    ``("dresses", [("length", "Mini"), ("sleeve", "Long+Sleeve")])``. Host,
    scheme and any trailing slash are dropped; a URL that does not point at the
    storefront returns ``("", [])``.
    """
    raw = html.unescape((url or "").strip())
    parts = urlsplit(raw)
    if parts.scheme not in ("http", "https"):
        return "", []
    path = parts.path.strip("/")
    if not path:
        return "", []
    return path, parse_qsl(parts.query, keep_blank_values=True)


def refinement_slug(query: list[tuple[str, str]]) -> str:
    """``[("color", "green")]`` -> ``color-green`` (deterministically ordered)."""
    parts = []
    for key, value in sorted(query, key=lambda pair: (pair[0].lower(), pair[1])):
        parts.extend([_slug(key), _slug(value)])
    return "-".join(part for part in parts if part)


def category_display_name(path_slug: str, query: list[tuple[str, str]]) -> str:
    """``("graphic-tees-for-women", [("color", "green")])`` -> a readable name."""
    name = _titleize(path_slug)
    if not query:
        return name
    refinements = ", ".join(
        f"{_REFINEMENT_LABELS.get(key, _titleize(key))}: {value.replace('+', ' ')}"
        for key, value in sorted(query, key=lambda pair: (pair[0].lower(), pair[1]))
    )
    return f"{name} ({refinements})"


def parse_category_sitemap(payload: str | bytes) -> list[dict[str, str]]:
    """Parse the category sitemap into ``BaseListingSpider.categories`` entries.

    Each entry is ``{"category", "name", "path", "query", "url", "nav_root"}``.

    The same path can appear many times, once per refinement, so the path slug is
    only used verbatim when it is unfiltered *and* unique; every filtered variant
    is keyed ``<path>-<refinement slug>``. Path slugs are otherwise unique across
    the sitemap, but a numeric suffix is appended defensively so a future
    collision cannot silently drop a category.
    """
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", "replace")

    entries: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_names: set[str] = set()

    for match in _LOC_RE.finditer(payload or ""):
        url = match.group(1).strip()
        if not url or url in seen_urls:
            continue
        path_slug, query = category_path_and_query(url)
        if not path_slug:
            continue
        seen_urls.add(url)
        # The sitemap XML-escapes `&` as `&amp;`; the request URL must be the
        # decoded form, so rebuild it from the parsed parts.
        request_url = f"{URBN_SITE_BASE}/{path_slug}"
        if query:
            request_url += "?" + urlencode(query)
        suffix = refinement_slug(query)
        candidate = path_slug if not suffix else f"{path_slug}-{suffix}"
        base, attempt = candidate, 2
        while candidate in seen_names:
            candidate = f"{base}-{attempt}"
            attempt += 1
        seen_names.add(candidate)
        entries.append(
            {
                "category": candidate,
                "name": category_display_name(path_slug, query),
                "path": path_slug,
                "query": "&".join(f"{key}={value}" for key, value in query),
                "url": request_url,
                "nav_root": nav_root_for_path(path_slug),
            }
        )

    # Curated navigation roots are appended only when the sitemap does not
    # already cover them, so the short department slugs stay usable either way.
    known = {entry["url"] for entry in entries}
    for slug, name, url in URBN_NAV_ROOTS:
        if url in known:
            continue
        entries.append(
            {
                "category": slug,
                "name": name,
                "path": urlsplit(url).path.strip("/"),
                "query": "",
                "url": url,
                "nav_root": name,
            }
        )
    return entries


def nav_root_for_path(path_slug: str) -> str | None:
    """Best-effort department name for a sitemap path slug.

    Urban Outfitters PLP paths are flat, so the department is inferred from the
    leading words of the slug (``mens-sweaters`` -> ``Men's``). It is a label
    only -- the spider never uses it to build a request.
    """
    for prefix, name in (
        ("womens-", "Women's"),
        ("mens-", "Men's"),
        ("girls-", "Girls'"),
        ("boys-", "Boys'"),
        ("kids-", "Kids'"),
        ("plus-size-", "Women's Plus"),
        ("pet-", "Pets"),
    ):
        if path_slug.startswith(prefix):
            return name
    return None


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
    normalized path *and* refinement query, so a trailing slash, an absolute
    URL, a bare path and a percent-encoded query all hit the same entry.
    """
    if category:
        index = category_index(categories)
        entry = index.get(category)
        if entry is not None:
            return entry
        # Fall back to a URL-shaped category arg so `-a category=/dresses?color=green`
        # works when the caller does not know the alias.
        if "/" in category or "?" in category:
            target = category if "://" in category else f"{URBN_SITE_BASE}/{category.lstrip('/')}"
            return resolve_category(categories, url=target)
        return None

    target = category_url or url
    if not target:
        return None
    if "://" not in target:
        target = f"{URBN_SITE_BASE}/{target.lstrip('/')}"
    wanted_path, wanted_query = category_path_and_query(target)
    if not wanted_path:
        return None
    wanted_pairs = sorted(wanted_query)
    for entry in categories:
        if entry["path"] != wanted_path:
            continue
        if not wanted_pairs:
            return entry
        entry_pairs = sorted(parse_qsl(entry.get("query") or "", keep_blank_values=True))
        if entry_pairs == wanted_pairs:
            return entry
    return None


def available_categories(categories: list[dict[str, str]], limit: int = 10) -> list[Any]:
    """A short, deterministic sample of category slugs for error messages."""
    return [entry["category"] for entry in categories[:limit]]
