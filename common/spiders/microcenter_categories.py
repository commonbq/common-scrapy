from __future__ import annotations

"""Micro Center navigation inventory captured from the storefront mega-menu.

The packaged JSON preserves all 20 departments, 118 groups, and 578 navigation
links. ``MICROCENTER_CATEGORIES`` deduplicates repeated destinations while
retaining every navigation context on the resulting category record.
"""

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, unquote_plus, urlparse


_INVENTORY = Path(__file__).with_name("microcenter_categories.json")


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _category_id(url: str) -> str | None:
    filters = parse_qs(urlparse(url).query).get("fq", [])
    match = re.search(r"\|(\d+)(?:,|$)", unquote_plus(filters[0])) if filters else None
    return match.group(1) if match else None


def load_categories() -> list[dict]:
    tree = json.loads(_INVENTORY.read_text(encoding="utf-8"))
    by_url: dict[str, dict] = {}
    used_slugs: set[str] = set()
    for department, groups in tree.items():
        for group, links in groups.items():
            for link in links:
                url = link["url"]
                context = {"department": department, "group": group, "name": link["name"]}
                if url in by_url:
                    by_url[url]["navigation_contexts"].append(context)
                    continue

                category_id = _category_id(url)
                base = _slug(link["name"]) or "category"
                category = base
                if category in used_slugs:
                    suffix = category_id or hashlib.sha1(url.encode()).hexdigest()[:8]
                    category = f"{base}-{suffix}"
                if category in used_slugs:
                    category = f"{category}-{hashlib.sha1(url.encode()).hexdigest()[:8]}"
                used_slugs.add(category)
                by_url[url] = {
                    "category": category,
                    "category_id": category_id,
                    "department": department,
                    "group": group,
                    "name": link["name"],
                    "url": url,
                    "navigation_contexts": [context],
                }
    return list(by_url.values())


MICROCENTER_CATEGORIES = load_categories()
