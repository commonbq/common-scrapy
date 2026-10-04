from __future__ import annotations

import json
import re
from pathlib import Path


_INVENTORY_PATH = Path(__file__).with_name("wayfair_categories.json")

# Navigation entries that are not product listings. The full inventory is kept in
# WAYFAIR_CATEGORY_INVENTORY, but only classified listing targets are exposed as
# runnable categories so the spider never announces a hub or informational page as
# a crawl target.
#
#   - magazine hubs   (/m/..., Wayfair's editorial/landing pages)
#   - advice/help     (/ideas-and-advice/, /help/...)
#   - informational   (financing, design services)
_INFORMATIONAL_MARKERS = ("/help/", "/affirm", "design-services", "/ideas-and-advice/")
_MAGAZINE_MARKERS = ("/m/",)


def _load_inventory() -> dict[str, dict]:
    with _INVENTORY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


WAYFAIR_CATEGORY_INVENTORY = _load_inventory()


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def classify_target(url: str, *, is_department_root: bool = False) -> str:
    """Return ``listing`` for a crawlable product listing, else ``hub``/``informational``.

    Wayfair exposes department roots as marketing hubs that render recommendation
    carousels rather than a paginated listing, so they are classified as hubs even
    though their URL looks like a ``/cat/`` page.
    """
    if is_department_root:
        return "hub"
    lowered = url.lower()
    if any(marker in lowered for marker in _INFORMATIONAL_MARKERS):
        return "informational"
    if any(marker in lowered for marker in _MAGAZINE_MARKERS):
        return "hub"
    return "listing"


def flatten_wayfair_categories() -> list[dict[str, str]]:
    """Return stable names for every unique product-listing target.

    A plain label is used when it is unique (for example, ``sofas``). When the
    menu repeats a label, the department is prefixed to keep the key stable.
    Hubs and informational pages are preserved in WAYFAIR_CATEGORY_INVENTORY but
    excluded from the runnable categories.
    """
    rows: list[tuple[str, str, str, bool]] = []
    for department, group in WAYFAIR_CATEGORY_INVENTORY.items():
        rows.append((department, department, group["url"], True))
        rows.extend(
            (department, label, url, False)
            for label, url in group.get("subcategories", {}).items()
        )

    label_counts: dict[str, int] = {}
    for _, label, _, _ in rows:
        key = _slug(label)
        label_counts[key] = label_counts.get(key, 0) + 1

    categories: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_keys: set[str] = set()
    for department, label, url, is_department_root in rows:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        if classify_target(url, is_department_root=is_department_root) != "listing":
            continue
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
