from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urljoin


def _sample_path(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "sample" / name


def _category_slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _load_categories_by_parent() -> dict[str, list[dict[str, Any]]]:
    try:
        payload = json.loads(_sample_path("costco-categories.json").read_text("utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    categories = payload.get("categories_by_parent")
    return categories if isinstance(categories, dict) else {}


def _expand_costco_categories() -> dict[str, dict[str, dict[str, str]]]:
    categories_by_parent = _load_categories_by_parent()
    expanded: dict[str, dict[str, str]] = {}
    for parent_name, entries in categories_by_parent.items():
        if not isinstance(parent_name, str) or not isinstance(entries, list):
            continue
        parent_slug = _category_slug(parent_name)
        if not parent_slug:
            continue
        bucket: dict[str, dict[str, str]] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name")
            url = entry.get("url")
            if not isinstance(name, str) or not isinstance(url, str):
                continue
            child_slug = _category_slug(name)
            if child_slug:
                bucket[f"{parent_slug}-{child_slug}"] = {
                    "url": urljoin("https://www.costco.com", url),
                    "subcategory": child_slug,
                }
        if bucket:
            expanded[parent_slug] = bucket
    return expanded


COSTCO_CATEGORIES = _expand_costco_categories()

# Preserve the reviewed top-level coverage from the existing listing DAG while
# allowing the factory to schedule at most three runnable leaves per group.
_DAG_GROUPS = {
    "2-day-delivery",
    "apple-products",
    "appliances",
    "baby",
    "beauty",
    "cleaning-supplies",
    "clothing-for-men",
    "clothing-for-women",
    "computers",
    "electronics",
    "frozen-foods",
    "furniture",
    "mattresses",
    "personal-care",
    "pet-supplies",
    "produce",
    "refrigerators",
    "snacks",
    "toys",
    "tvs",
}
COSTCO_DAG_CATEGORIES = {
    group: leaves for group, leaves in COSTCO_CATEGORIES.items() if group in _DAG_GROUPS
}
