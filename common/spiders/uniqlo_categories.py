from __future__ import annotations

"""UNIQLO US navigation taxonomy flattened into the listing ``categories`` contract.

The tree is harvested from ``window.__PRELOADED_STATE__.taxonomies`` (present in the
SSR shell of every UNIQLO page) and committed as ``sample/uniqlo-categories.json``:
4 genders / 46 classes / 212 categories / 2479 subcategories = 2741 URLs.

Each entry keeps the Fast Retailing taxonomy id chain the commerce BFF products
endpoint expects in its ``path`` query parameter
(``genderId[,classId[,categoryId[,subCategoryId]]]``), so the spider can page any
category without re-resolving the URL against the live site.
"""

import json
import re
from pathlib import Path
from typing import Any

_SAMPLE_NAME = "uniqlo-categories.json"
_CHILD_KEYS = ("classes", "categories", "subcategories")


def _sample_path(name: str) -> Path:
    here = Path(__file__).resolve()
    for parent in (here.parent.parent.parent, *here.parents):
        candidate = parent / "sample" / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Could not locate sample/{name} relative to {here}")


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(label).lower()).strip("-")


def load_uniqlo_inventory() -> dict[str, Any]:
    """Return the nested gender -> class -> category -> subcategory inventory."""
    payload = json.loads(_sample_path(_SAMPLE_NAME).read_text("utf-8"))
    return payload if isinstance(payload, dict) else {}


def _unique_name(label: str, trail: list[str], used: set[str]) -> str:
    """Slug a label, widening to the full trail and then a counter on collision.

    Slugs collide a lot in this tree ("vest" sits under several categories), so
    every one of the 2741 URLs has to stay individually addressable.
    """
    for candidate in (_slug(label), _slug("-".join([*trail, label]))):
        if candidate not in used:
            used.add(candidate)
            return candidate
    stem = _slug("-".join([*trail, label])) or _slug(label)
    suffix = 2
    while f"{stem}-{suffix}" in used:
        suffix += 1
    used.add(f"{stem}-{suffix}")
    return f"{stem}-{suffix}"


def _walk(
    node: dict[str, Any],
    trail: list[str],
    ids: list[str],
    out: list[dict[str, Any]],
    seen: set[str],
    used: set[str],
) -> None:
    url = node.get("url")
    if not isinstance(url, str) or not url or url in seen:
        return
    seen.add(url)

    label = str(node.get("name") or url)
    chain = [*ids, node.get("id")]

    entry: dict[str, Any] = {
        "category": _unique_name(label, trail, used),
        "url": url,
        "path": ",".join(str(part) for part in chain if part is not None),
        "category_name": label,
    }
    if trail:
        entry["department"] = trail[0]
    if len(trail) > 1:
        entry["subcategory"] = trail[1]
    out.append(entry)

    children: dict[str, Any] = {}
    for key in _CHILD_KEYS:
        value = node.get(key)
        if isinstance(value, dict):
            children = value
            break
    for child in children.values():
        if isinstance(child, dict):
            _walk(child, [*trail, label], chain, out, seen, used)


def _flatten_inventory() -> list[dict[str, Any]]:
    categories: list[dict[str, Any]] = []
    seen: set[str] = set()
    used: set[str] = set()
    for gender in load_uniqlo_inventory().values():
        if isinstance(gender, dict):
            _walk(gender, [], [], categories, seen, used)
    return categories


UNIQLO_CATEGORY_INVENTORY = load_uniqlo_inventory()
UNIQLO_CATEGORIES = _flatten_inventory()

# url -> taxonomy id path, used to resolve -a category_url / -a url targets.
UNIQLO_CATEGORY_PATHS: dict[str, str] = {
    entry["url"]: entry["path"] for entry in UNIQLO_CATEGORIES
}
