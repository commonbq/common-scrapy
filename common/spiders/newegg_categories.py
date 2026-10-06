"""Newegg listing inventory, captured from the first-party RolloverMenu endpoint.

Source of truth:

    GET https://www.newegg.com/api/RolloverMenu?CountryCode=USA

Captured 2026-10-04 UTC from the US storefront. The payload nests **1,789**
navigation nodes under ``RollOverMenu[]`` across **17** top-level departments.
``StoreType=0`` nodes are pure grouping labels with no listing behind them, so
they are not crawlable and are excluded. The remaining nodes resolve to
**1,557** distinct listing URLs, all shipped in ``newegg_category_urls.json``.

URL resolution rules, applied while capturing the inventory:

1. ``CustomLink`` wins whenever present. Newegg emits these protocol-relative
   (``//www.newegg.com/...``), so the scheme is pinned to ``https``.
2. ``StoreType=1`` -> ``https://www.newegg.com/{slug}/Store/ID-{StoreId}``
3. ``StoreType=2`` -> ``https://www.newegg.com/{slug}/Category/ID-{StoreId}``
4. ``StoreType=3`` -> ``https://www.newegg.com/{slug}/SubCategory/ID-{StoreId}``

``{slug}`` is the store name lower-cased with every run of non-alphanumeric
characters collapsed into a single ``-``.

The sidecar JSON is a nested tree of ``department -> label -> ... -> url``. A
node that is both a listing *and* a parent carries its own URL under the
reserved ``@url`` key.

Two classes of ``CustomLink`` are deliberately dropped because they do not
serve a crawlable taxonomy listing: off-domain links that leave the storefront
(``neweggbusiness.com``, partner vendors), and non-taxonomy storefront paths
(``/p/pl?N=...`` keyword search, ``/insider``, ``/tools``, promotional pages,
``EventSaleStore`` / ``RefurbishedStore``). Only URLs shaped like
``/{slug}/{Store,Category,SubCategory}/ID-{id}`` are kept.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

NEWEGG_SITE_BASE = "https://www.newegg.com"
NEWEGG_MENU_URL = f"{NEWEGG_SITE_BASE}/api/RolloverMenu?CountryCode=USA"

_INVENTORY_PATH = Path(__file__).resolve().parent / "newegg_category_urls.json"
_SELF_KEY = "@url"


def _category_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")


def url_kind(url: str) -> str:
    """``SubCategory`` pages are product listings; ``Store``/``Category`` are hubs.

    Verified against the live storefront on 2026-10-04: sampled
    ``SubCategory`` URLs served a populated ``Products`` array every time,
    while ``Store`` and ``Category`` nodes rendered a navigation hub with zero
    products. The spider logs an explicit diagnostic when pointed at a hub.
    """
    return url.rstrip("/").split("/")[-2]


def _load_tree() -> dict[str, dict]:
    """Return the captured department tree, or an empty mapping when unusable."""
    try:
        payload = json.loads(_INVENTORY_PATH.read_text("utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    departments = payload.get("departments") if isinstance(payload, dict) else None
    return departments if isinstance(departments, dict) else {}


def _entry(here: tuple[str, ...], department: str, url: str) -> dict[str, str]:
    return {
        "category": "-".join(filter(None, (_category_slug(part) for part in here))),
        "department": department,
        "subcategory": " > ".join(here),
        "url": url,
        "kind": url_kind(url),
    }


def _walk(node, breadcrumb: tuple[str, ...], department: str, out: list[dict]) -> None:
    """Flatten the nested inventory into the base spider's category contract."""
    for label in sorted(node):
        if label == _SELF_KEY:
            continue
        value = node[label]
        if isinstance(value, str):
            out.append(_entry(breadcrumb + (label,), department, value))
        elif isinstance(value, dict):
            if isinstance(value.get(_SELF_KEY), str):
                out.append(_entry(breadcrumb + (label,), department, value[_SELF_KEY]))
            _walk(value, breadcrumb + (label,), department, out)


def _flatten_categories() -> list[dict[str, str]]:
    """Flatten the captured inventory into ``BaseListingSpider.categories``."""
    tree = _load_tree()
    categories: list[dict[str, str]] = []
    for department in sorted(tree):
        node = tree[department]
        if isinstance(node, dict):
            _walk(node, (), department, categories)

    seen_urls: set[str] = set()
    seen_names: set[str] = set()
    deduped: list[dict[str, str]] = []
    for entry in categories:
        if entry["url"] in seen_urls:
            continue
        seen_urls.add(entry["url"])
        name = entry["category"] or "category"
        if name in seen_names:
            prefix = _category_slug(entry["department"])
            name = f"{prefix}-{name}" if prefix else f"{name}-2"
            suffix = 2
            while name in seen_names:
                name = f"{prefix}-{entry['category']}-{suffix}"
                suffix += 1
        entry["category"] = name
        seen_names.add(name)
        deduped.append(entry)
    return deduped


NEWEGG_CATEGORIES: list[dict[str, str]] = _flatten_categories()
NEWEGG_LISTING_CATEGORIES: list[dict[str, str]] = [
    entry for entry in NEWEGG_CATEGORIES if entry["kind"] == "SubCategory"
]
