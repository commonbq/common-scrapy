from __future__ import annotations

import json
import re
from typing import Any


def extract_next_data(html: str) -> dict[str, Any] | None:
    m = re.search(
        r'<script[^>]*id=["\']__NEXT_DATA__["\'][^>]*>(?P<json>.*?)</script>',
        html or "",
        flags=re.S | re.I,
    )
    if not m:
        return None
    try:
        obj = json.loads(m.group("json"))
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def extract_apollo_state(html: str) -> dict[str, Any] | None:
    m = re.search(r"(?:window\.)?__APOLLO_STATE__\s*=\s*\{", html or "")
    if not m:
        return None

    start = m.end() - 1
    obj_text = _extract_balanced_braces(html, start)
    if not obj_text:
        return None

    try:
        obj = json.loads(obj_text)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def extract_preloaded_state(html: str) -> dict[str, Any] | None:
    m = re.search(r'"__PRELOADED_STATE__"\s*:\s*\{', html or "")
    if not m:
        m = re.search(r'(?:window\.)?__PRELOADED_STATE__\s*=\s*\{', html or "")
    if not m:
        return None

    start = m.end() - 1
    obj_text = _extract_balanced_braces(html, start)
    if not obj_text:
        return None

    try:
        obj = json.loads(obj_text)
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None


def extract_json_ld_products(html: str):
    scripts = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html or "",
        flags=re.S | re.I,
    )
    for s in scripts:
        s = (s or "").strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except Exception:
            continue

        for node in _iter_jsonld_nodes(obj):
            if not isinstance(node, dict):
                continue

            if node.get("@type") == "ListItem" and isinstance(node.get("item"), dict):
                node = node["item"]

            if node.get("@type") != "Product":
                continue

            offers = node.get("offers") or {}
            if isinstance(offers, list):
                offers = offers[0] if offers else {}

            url = node.get("url")
            if isinstance(url, str) and url.startswith("/"):
                url = None

            yield {
                "item_id": _extract_id_from_url(url),
                "title": node.get("name"),
                "url": url,
                "price": _to_float((offers or {}).get("price")) if isinstance(offers, dict) else None,
                "currency": (offers or {}).get("priceCurrency") if isinstance(offers, dict) else None,
                "brand": (node.get("brand") or {}).get("name") if isinstance(node.get("brand"), dict) else node.get("brand"),
                "rating": _to_float((node.get("aggregateRating") or {}).get("ratingValue")) if isinstance(node.get("aggregateRating"), dict) else None,
                "reviews_count": _to_int((node.get("aggregateRating") or {}).get("reviewCount")) if isinstance(node.get("aggregateRating"), dict) else None,
                "image_url": node.get("image", [None])[0] if isinstance(node.get("image"), list) else node.get("image"),
                "source": "jsonld_fallback",
                "raw": node,
            }


def extract_items_from_unknown_state(state: dict[str, Any], source: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []

    for node in _walk(state):
        if _looks_like_listing(node):
            hits.append(_normalize_listing(node, source=source))

    out: list[dict[str, Any]] = []
    seen: set[tuple[str | None, str | None, str | None]] = set()
    for h in hits:
        key = (h.get("item_id"), h.get("title"), h.get("url"))
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out


def _walk(node: Any):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def _looks_like_listing(d: dict[str, Any]) -> bool:
    keys = {k.lower() for k in d.keys()}
    has_title = any(k in keys for k in ["title", "name", "displayname", "productname", "itemtitle"])
    has_id_or_url = any(k in keys for k in ["id", "itemid", "productid", "skuid", "sku", "url", "producturl", "itemweburl", "canonicalurl"])
    has_price = any(k in keys for k in ["price", "currentprice", "saleprice", "regularprice", "displayprice"])
    return has_title and has_id_or_url and has_price


def _normalize_listing(d: dict[str, Any], *, source: str) -> dict[str, Any]:
    title = d.get("title") or d.get("name") or d.get("displayName") or d.get("productName") or d.get("itemTitle")
    item_id = d.get("itemId") or d.get("productId") or d.get("id") or d.get("skuId") or d.get("sku")

    url = d.get("url") or d.get("productUrl") or d.get("itemWebUrl") or d.get("canonicalUrl")
    if isinstance(url, dict):
        url = url.get("url") or url.get("pdp") or url.get("relativePdp")

    raw_price = d.get("price") or d.get("currentPrice") or d.get("salePrice") or d.get("regularPrice") or d.get("displayPrice")
    price = None
    currency = None
    if isinstance(raw_price, dict):
        price = _to_float(raw_price.get("value") or raw_price.get("amount") or raw_price.get("price") or raw_price.get("currentPrice") or raw_price.get("customerPrice"))
        currency = raw_price.get("currency") or raw_price.get("currencyCode")
    elif isinstance(raw_price, (int, float, str)):
        price = _to_float(raw_price)

    image = d.get("image") or d.get("imageUrl") or d.get("thumbnail") or d.get("primaryImage")
    if isinstance(image, dict):
        image = image.get("href") or image.get("url") or image.get("src")

    rating = d.get("rating") or d.get("averageRating")
    reviews = d.get("reviewCount") or d.get("reviewsCount") or d.get("numberOfReviews")

    brand = d.get("brand")
    if isinstance(brand, dict):
        brand = brand.get("name")

    return {
        "item_id": str(item_id) if item_id is not None else _extract_id_from_url(url),
        "title": title,
        "url": url,
        "price": price,
        "currency": currency,
        "brand": brand,
        "rating": _to_float(rating),
        "reviews_count": _to_int(reviews),
        "image_url": image,
        "source": source,
        "raw": d,
    }


def _extract_balanced_braces(text: str, start_index: int) -> str | None:
    if start_index < 0 or start_index >= len(text) or text[start_index] != "{":
        return None

    depth = 0
    in_str = False
    esc = False

    for i in range(start_index, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start_index : i + 1]
    return None


def _iter_jsonld_nodes(obj: Any):
    if isinstance(obj, dict):
        graph = obj.get("@graph")
        if isinstance(graph, list):
            for x in graph:
                if isinstance(x, dict):
                    yield x
        else:
            yield obj
    elif isinstance(obj, list):
        for x in obj:
            if isinstance(x, dict):
                yield x


def _extract_id_from_url(url: Any) -> str | None:
    if not isinstance(url, str):
        return None
    m = re.search(r"/(\d{6,})", url)
    return m.group(1) if m else None


def _to_float(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"(\d+(?:[\.,]\d+)?)", v.replace(",", ""))
        if not m:
            return None
        try:
            return float(m.group(1))
        except Exception:
            return None
    return None


def _to_int(v: Any) -> int | None:
    if v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        d = re.sub(r"[^\d]", "", v)
        if d:
            return int(d)
    return None
