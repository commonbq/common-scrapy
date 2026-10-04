from __future__ import annotations

"""Williams-Sonoma category inventory loader (issue #160).

The full taxonomy is served by a first-party JSON endpoint -- there is no
sitemap that mirrors it and the category HTML never renders the whole menu:

    GET https://www.williams-sonoma.com/api/catalog/v1/category/categorytree/shop/data.json

Root shape is ``{"id": "shop", "type": "shoproot", "categories": [...]}`` and
every node carries ``id`` / ``type`` / ``name`` with optional nested
``categories``. Node ``type`` values observed on 2026-10-02:

    supercat (46)  topcat (358)  subcat (2764)  linkcat (418)  linksubcat (1)
    header (213)   leftheader (13)

``header`` / ``leftheader`` nodes are *section labels* ("Cookware Essentials"),
not shoppable destinations, so they are excluded -- they only carry a
``referenceCategoryPath`` pointing at a sibling "view all" target.

That leaves ~3,587 concrete category ids, which map one-to-one onto Constructor.io
browse ``group_id`` values. This module turns the raw tree into that flat,
deduplicated crawl-target list; nothing is hardcoded, so a taxonomy change on
the storefront is picked up on the next run instead of going stale in a
committed snapshot.
"""

import html
import json
from dataclasses import dataclass, field
from typing import Any

SITE_BASE = "https://www.williams-sonoma.com"
CATEGORY_TREE_URL = (
    f"{SITE_BASE}/api/catalog/v1/category/categorytree/shop/data.json"
)

# Non-shoppable section labels. Everything else in the tree is a real category.
NON_CATEGORY_TYPES = frozenset({"header", "leftheader"})


@dataclass(frozen=True)
class Category:
    """One crawl target: a Constructor.io ``group_id`` plus its page metadata."""

    group_id: str
    name: str
    node_type: str
    url: str
    parent_id: str | None = None
    parent_name: str | None = None
    depth: int = 0
    group_ids: tuple[str, ...] = field(default=())


def _text(value: Any) -> str:
    """Tree names arrive HTML-escaped ("Fry Pans &amp; Skillets")."""
    if not isinstance(value, str):
        return ""
    # `unescape` last: names can legitimately contain a literal `&` from a
    # double-escaped source and we would rather ship `&amp;` than lose the char.
    return html.unescape(value).strip()


def category_url_for(path: list[str]) -> str:
    """`["cookware", "cookware-sets"]` -> the storefront category page URL."""
    return "/".join([SITE_BASE, "shop", *path]) + "/"


def parse_category_tree(payload: str | bytes) -> list[Category]:
    """Flatten the category-tree JSON into an ordered, deduplicated target list.

    Dedupe is by ``group_id``: the tree repeats ids across the
    supercat/topcat/subcat split, and a repeated id is the *same* Constructor
    group, so keeping the first (shallowest, top-down walk) occurrence is what
    keeps one crawl target from being requested twice.
    """
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", "replace")
    try:
        root = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Williams-Sonoma category tree is not valid JSON: {exc}"
        ) from exc
    if not isinstance(root, dict):
        raise RuntimeError(
            "Williams-Sonoma category tree root is "
            f"{type(root).__name__}, expected object"
        )

    categories: list[Category] = []
    seen: set[str] = set()

    def walk(nodes: Any, path: list[str], parent: Category | None) -> None:
        if not isinstance(nodes, list):
            return
        for node in nodes:
            if not isinstance(node, dict):
                continue
            group_id = _text(node.get("id"))
            if not group_id:
                continue
            if _text(node.get("type")) in NON_CATEGORY_TYPES:
                continue
            if group_id in seen:
                # The tree repeats ids across the supercat/topcat/subcat split.
                # A repeat is the same Constructor group, so re-registering it
                # would queue a duplicate crawl target -- but its children may
                # not have been visited yet, so recurse regardless.
                walk(node.get("categories"), [*path, group_id], parent)
                continue
            node_path = [*path, group_id]
            category = Category(
                group_id=group_id,
                name=_text(node.get("name")) or group_id,
                node_type=_text(node.get("type")),
                url=category_url_for(node_path),
                parent_id=parent.group_id if parent else None,
                parent_name=parent.name if parent else None,
                depth=len(node_path) - 1,
                group_ids=tuple(node_path),
            )
            seen.add(group_id)
            categories.append(category)
            walk(node.get("categories"), node_path, category)

    walk(root.get("categories"), [], None)
    return categories


def build_index(categories: list[Category]) -> dict[str, Category]:
    """``group_id`` -> :class:`Category` lookup."""
    return {category.group_id: category for category in categories}


def group_id_from_url(url: str) -> str:
    """Extract the trailing category id from a shop URL.

    `/shop/cookware/cookware-sets/` -> `cookware-sets`. Handles query strings and
    fragments, and tolerates a non-`/shop/` prefix so a pasted product URL fails
    loudly in the spider rather than silently browsing "products".
    """
    path = url.split("#", 1)[0].split("?", 1)[0].strip()
    for marker in ("williams-sonoma.com",):
        if marker in path:
            path = path.split(marker, 1)[-1]
    segments = [segment for segment in path.split("/") if segment]
    if "shop" not in segments:
        # Guard against silently browsing the wrong Constructor group: a product
        # or search URL has no category segment to read.
        raise ValueError(
            f"Expected a /shop/<category>/ URL to derive a category id, got {url!r}"
        )
    segments = segments[segments.index("shop") + 1 :]
    if not segments:
        raise ValueError(f"Shop URL has no category segment: {url!r}")
    return segments[-1]