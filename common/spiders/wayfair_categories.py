from __future__ import annotations

import json
import re
from pathlib import Path


_INVENTORY_PATH = Path(__file__).with_name("wayfair_categories.json")


def _load_inventory() -> dict[str, dict]:
    with _INVENTORY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


WAYFAIR_CATEGORY_INVENTORY = _load_inventory()


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def flatten_wayfair_categories() -> list[dict[str, str]]:
    """Return stable names for every unique navigation target.

    A plain label is used when it is unique (for example, ``sofas``). When the
    menu repeats a label, the department is prefixed to keep the key stable.
    """
    rows: list[tuple[str, str, str]] = []
    for department, group in WAYFAIR_CATEGORY_INVENTORY.items():
        rows.append((department, department, group["url"]))
        rows.extend(
            (department, label, url)
            for label, url in group.get("subcategories", {}).items()
        )

    label_counts: dict[str, int] = {}
    for _, label, _ in rows:
        key = _slug(label)
        label_counts[key] = label_counts.get(key, 0) + 1

    categories: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_keys: set[str] = set()
    for department, label, url in rows:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        label_key = _slug(label)
        key = label_key if label_counts[label_key] == 1 else f"{_slug(department)}-{label_key}"
        if key in seen_keys:
            suffix = 2
            while f"{key}-{suffix}" in seen_keys:
                suffix += 1
            key = f"{key}-{suffix}"
        seen_keys.add(key)
        categories.append({"category": key, "url": url, "department": department})
    return categories


WAYFAIR_CATEGORIES = flatten_wayfair_categories()
