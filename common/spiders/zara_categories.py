from __future__ import annotations

"""Zara US category inventory parsed at runtime from the first-party menu API.

The whole taxonomy ships as JSON, so nothing here is hard-coded (issue #208):

    GET https://www.zara.com/us/en/categories        -> application/json
    {"categories": [<node>, ...]}                    2,622 nodes / 6 levels

A node is a product listing page when all of the following hold:

* ``layout == "products-category-view"`` -- the only layout that renders a grid.
  The payload also carries ``marketing-content-view`` (255), ``divider-...``
  (102), ``wonder-club-products-category-view`` (58), ``bamo-``/``origins-``/
  ``galliano-products-category-view`` (48), ``store-locator-view`` and 8 other
  layouts that must not become crawl targets.
* ``irrelevant is False`` -- 921 nodes are explicitly irrelevant (account,
  careers, gift-card balances...) and ``seo.irrelevant`` mirrors it.
* ``seo.keyword`` and ``seo.seoCategoryId`` are present. 2,622 nodes carry
  ``irrelevant`` but only 2,493 carry a usable ``seo`` pair.

That leaves **1,347 eligible nodes -> 912 unique listing URLs** (the rest are the
same category cross-listed under several departments, e.g. the 210 ``VIEW ALL``
menus all point at their parent). Both numbers were re-verified live.

Public-listing URLs are built from the SEO pair, not from the menu label::

    https://www.zara.com/us/en/{seo.keyword}-l{seo.seoCategoryId}.html

The numeric menu ``id`` (e.g. ``2546081``) is *not* in that URL; it is the value
the products endpoint needs, so it is preserved on every entry.

Menu labels are not unique (``VIEW ALL`` x210, ``THE NEW`` x14, ``JACKETS`` x6)
so `-a category=` matches on the full breadcrumb path, which disambiguates.
"""

from typing import Any

ZARA_SITE_BASE = "https://www.zara.com"
ZARA_LOCALE_PREFIX = "/us/en"

CATEGORIES_ENDPOINT = f"{ZARA_SITE_BASE}{ZARA_LOCALE_PREFIX}/categories"
PRODUCTS_ENDPOINT_TEMPLATE = (
    f"{ZARA_SITE_BASE}{ZARA_LOCALE_PREFIX}/category/{{category_id}}/products"
)

#: Only this layout renders a product grid.
PRODUCTS_LAYOUT = "products-category-view"


def listing_url(keyword: str, seo_category_id: int | str) -> str:
    """Build the public PLP URL for a taxonomy node's SEO pair."""
    return f"{ZARA_SITE_BASE}{ZARA_LOCALE_PREFIX}/{keyword}-l{seo_category_id}.html"


def is_product_category(node: dict[str, Any]) -> bool:
    """True when a raw menu node is a crawlable product listing page."""
    if not isinstance(node, dict):
        return False
    if node.get("layout") != PRODUCTS_LAYOUT:
        return False
    if node.get("irrelevant") is not False:
        return False
    seo = node.get("seo")
    if not isinstance(seo, dict):
        return False
    return bool(seo.get("keyword")) and bool(seo.get("seoCategoryId"))


def _walk(node: dict[str, Any], path: tuple[str, ...]):
    """Yield ``(node, path)`` for the node and every descendant."""
    yield node, path
    for child in node.get("subcategories") or []:
        if isinstance(child, dict):
            yield from _walk(child, path + (str(node.get("name") or ""),))


def _iter_raw_nodes(payload: dict[str, Any]):
    for top in payload.get("categories") or []:
        if isinstance(top, dict):
            yield from _walk(top, ())


def category_key(path: tuple[str, ...]) -> str:
    """`-a category=` key: the full breadcrumb so repeated labels stay unique."""
    parts = [part.strip() for part in path if part and part.strip()]
    return " > ".join(parts) if parts else "Zara"


def parse_taxonomy(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten the nested menu payload into deduped listing entries.

    Returns a list of dicts holding ``category`` (breadcrumb key), ``url``,
    ``category_id`` (products-endpoint id), ``seo_category_id``, ``keyword``,
    ``name``, ``section`` and ``path``.
    """
    if not isinstance(payload, dict):
        raise ValueError("Zara categories payload must be a JSON object")

    by_url: dict[str, dict[str, Any]] = {}
    for node, path in _iter_raw_nodes(payload):
        if not is_product_category(node):
            continue
        seo = node["seo"]
        url = listing_url(seo["keyword"], seo["seoCategoryId"])
        # The same category is cross-listed under several parents; the first
        # (document-order deepest-path) breadcrumb wins so the key is stable.
        if url in by_url:
            by_url[url]["departments"].append(path[0] if path else None)
            continue
        by_url[url] = {
            "category": category_key(path + (str(node.get("name") or ""),)),
            "name": node.get("name"),
            "url": url,
            "category_id": node.get("id"),
            "seo_category_id": seo["seoCategoryId"],
            "keyword": seo["keyword"],
            "section": path[0] if path else None,
            "path": list(path) + [str(node.get("name") or "")],
            "departments": [path[0] if path else None],
        }
    return list(by_url.values())


def load_categories(payload: dict[str, Any]) -> list[dict[str, str]]:
    """Flattened ``{'category','url'}`` list for ``BaseListingSpider``."""
    return [
        {"category": entry["category"], "url": entry["url"]}
        for entry in parse_taxonomy(payload)
    ]


def seo_category_id_from_url(url: str) -> str | None:
    """Read the ``l<seoCategoryId>`` id out of a public listing URL.

    This is the **seo** category id, *not* the numeric menu id the products
    endpoint needs: they are different numbers for the same category
    (``WOMAN > NEW ARRIVALS > THE NEW`` is seo ``1180`` but menu ``2546081``).
    A caller holding only a URL therefore still has to resolve the menu id
    through the taxonomy; this helper exists for cross-checking, not for
    building product requests.
    """
    if not url:
        return None
    tail = url.split("?", 1)[0].rstrip("/").rsplit("-l", 1)
    if len(tail) != 2:
        return None
    suffix = tail[1].removesuffix(".html")
    return suffix if suffix.isdigit() else None