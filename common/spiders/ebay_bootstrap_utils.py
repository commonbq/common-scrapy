from __future__ import annotations

import json
import re
from typing import Any, Iterable


def extract_next_data(html: str) -> dict[str, Any] | None:
    """Return parsed __NEXT_DATA__ payload when present."""
    m = re.search(
        r"<script[^>]*\bid=(?:['\"])?__NEXT_DATA__(?:['\"])?[^>]*>(?P<json>.*?)</script>",
        html or "",
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return None
    try:
        return json.loads(m.group("json"))
    except Exception:
        return None


def extract_json_ld_products(html: str) -> Iterable[dict[str, Any]]:
    """Best-effort fallback for Product entries in application/ld+json blocks."""
    for m in re.finditer(
        r"<script[^>]*\btype=(?:['\"])?application/ld\+json(?:['\"])?[^>]*>(?P<json>.*?)</script>",
        html or "",
        flags=re.DOTALL | re.IGNORECASE,
    ):
        raw = (m.group("json") or "").strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue

        for node in _iter_jsonld_nodes(obj):
            if not isinstance(node, dict):
                continue

            # Product node directly.
            if node.get("@type") == "Product":
                product_nodes = [node]
            # ItemList often wraps products under itemListElement[].item.
            elif node.get("@type") == "ItemList" and isinstance(node.get("itemListElement"), list):
                product_nodes = []
                for el in node.get("itemListElement", []):
                    if isinstance(el, dict):
                        cand = el.get("item") if isinstance(el.get("item"), dict) else el
                        if isinstance(cand, dict) and cand.get("@type") == "Product":
                            product_nodes.append(cand)
            else:
                product_nodes = []

            for p in product_nodes:
                offers = p.get("offers", {})
                if isinstance(offers, list):
                    offers = offers[0] if offers else {}

                url = p.get("url")
                yield {
                    "item_id": _extract_item_id(url),
                    "title": p.get("name"),
                    "url": url,
                    "price": _coerce_num((offers or {}).get("price")),
                    "currency": (offers or {}).get("priceCurrency"),
                    "image_url": p.get("image", [None])[0] if isinstance(p.get("image"), list) else p.get("image"),
                    "source": "ebay_jsonld_fallback",
                }


def extract_items_from_next_data(next_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Walk unknown Next.js structure and normalize records that look like listings."""
    hits: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if _looks_like_listing(node):
                hits.append(_normalize_listing(node))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(next_data)

    out: list[dict[str, Any]] = []
    seen: set[tuple[str | None, str | None, str | None]] = set()
    for h in hits:
        key = (h.get("item_id"), h.get("title"), h.get("url"))
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out


def _looks_like_listing(d: dict[str, Any]) -> bool:
    has_title = any(k in d for k in ("title", "itemTitle", "name"))
    has_id_or_url = any(k in d for k in ("itemId", "legacyItemId", "id", "itemWebUrl", "itemHref", "url"))
    has_price = any(k in d for k in ("price", "currentPrice", "displayPrice"))
    return has_title and has_id_or_url and has_price


def _normalize_listing(d: dict[str, Any]) -> dict[str, Any]:
    raw_price = d.get("price") or d.get("currentPrice") or d.get("displayPrice")
    price, currency = _coerce_price(raw_price)

    shipping = d.get("shipping") if isinstance(d.get("shipping"), dict) else {}
    shipping_cost = shipping.get("cost") if isinstance(shipping, dict) else {}

    seller = d.get("seller") if isinstance(d.get("seller"), dict) else {}
    condition = d.get("condition") if isinstance(d.get("condition"), dict) else {}

    images = d.get("images") or d.get("image") or d.get("thumbnailImages")
    image_url = None
    if isinstance(images, list) and images:
        image_url = images[0] if isinstance(images[0], str) else images[0].get("imageUrl")
    elif isinstance(images, dict):
        image_url = images.get("imageUrl") or images.get("url")
    elif isinstance(images, str):
        image_url = images

    url = d.get("itemWebUrl") or d.get("itemHref") or d.get("url")

    return {
        "item_id": _as_str(d.get("itemId") or d.get("legacyItemId") or d.get("id") or _extract_item_id(url)),
        "title": d.get("title") or d.get("itemTitle") or d.get("name"),
        "url": url,
        "price": price,
        "currency": currency,
        "shipping": _coerce_num((shipping_cost or {}).get("value")) if isinstance(shipping_cost, dict) else None,
        "shipping_currency": (shipping_cost or {}).get("currency") if isinstance(shipping_cost, dict) else None,
        "seller": seller.get("username") or seller.get("name"),
        "seller_feedback_score": seller.get("feedbackScore"),
        "condition": condition.get("displayName") or condition.get("name"),
        "location": _coerce_location(d),
        "image_url": image_url,
        "listing_type": _coerce_listing_type(d),
        "source": "ebay_next_data",
    }


def _coerce_location(d: dict[str, Any]) -> str | None:
    loc = d.get("location")
    if isinstance(loc, str):
        return loc
    if isinstance(loc, dict):
        parts = [loc.get("city"), loc.get("state"), loc.get("country")]
        parts = [p for p in parts if p]
        return ", ".join(parts) if parts else None
    return d.get("itemLocation")


def _coerce_listing_type(d: dict[str, Any]) -> str | None:
    listing = d.get("listing")
    if isinstance(listing, dict):
        return listing.get("listingType")
    return d.get("listingType")


def _coerce_price(raw_price: Any) -> tuple[float | None, str | None]:
    if isinstance(raw_price, dict):
        v = raw_price.get("value") or raw_price.get("amount")
        c = raw_price.get("currency") or raw_price.get("currencyCode")
        return _coerce_num(v), c
    if isinstance(raw_price, str):
        m = re.search(r"([\d,.]+)", raw_price)
        return (_coerce_num(m.group(1)) if m else None), None
    return None, None


def _coerce_num(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        vv = v.replace(",", "").strip()
        try:
            return float(vv)
        except Exception:
            return None
    return None


def _as_str(v: Any) -> str | None:
    return str(v) if v is not None else None


def _extract_item_id(url: str | None) -> str | None:
    if not url:
        return None
    m = re.search(r"/itm/(\d+)", url)
    return m.group(1) if m else None


def _iter_jsonld_nodes(obj: Any) -> Iterable[dict[str, Any]]:
    if isinstance(obj, dict):
        graph = obj.get("@graph")
        if isinstance(graph, list):
            for g in graph:
                if isinstance(g, dict):
                    yield g
        else:
            yield obj
    elif isinstance(obj, list):
        for x in obj:
            if isinstance(x, dict):
                yield x
