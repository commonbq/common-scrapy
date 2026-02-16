from __future__ import annotations

import json
import re
from typing import Any


def extract_bestbuy_items_from_bootstrap(html: str) -> list[dict[str, Any]]:
    """Extract product-like records from BestBuy Apollo bootstrap scripts."""
    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    for payload in _extract_apollo_transport_payloads(html or ""):
        for node in _walk(payload):
            if not _looks_like_product(node):
                continue
            item = _normalize_product(node)
            sku = item.get("item_id")
            if not sku or sku in seen:
                continue
            seen.add(sku)
            out.append(item)

    return out


def extract_bestbuy_items_from_apollo_cache(cache: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract product records from Apollo normalized cache (`cache.extract()`)."""
    if not isinstance(cache, dict):
        return []

    root = cache.get("ROOT_QUERY") if isinstance(cache.get("ROOT_QUERY"), dict) else {}
    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    search_keys = [k for k in root.keys() if isinstance(k, str) and k.startswith("search(")]
    for sk in search_keys:
        ref = (root.get(sk) or {}).get("__ref") if isinstance(root.get(sk), dict) else None
        if not ref:
            continue
        search_obj = cache.get(ref) if isinstance(cache.get(ref), dict) else {}
        docs = search_obj.get("documents") if isinstance(search_obj, dict) else None
        if not isinstance(docs, list):
            continue

        for doc in docs:
            product_ref = None
            if isinstance(doc, dict):
                prod = doc.get("product")
                if isinstance(prod, dict):
                    product_ref = prod.get("__ref")

            if not product_ref:
                continue

            product = cache.get(product_ref)
            if not isinstance(product, dict):
                continue

            item = _normalize_product(product)
            sku = item.get("item_id")
            if not sku or sku in seen:
                continue
            seen.add(sku)
            out.append(item)

    # Fallback for listing pages where SearchConnection.documents is absent:
    # scan normalized cache entries directly.
    if not out:
        for key, val in cache.items():
            if not isinstance(key, str) or not key.startswith("Product:"):
                continue
            if not isinstance(val, dict) or not _looks_like_product(val):
                continue

            item = _normalize_product(val)
            sku = item.get("item_id")
            if not sku or sku in seen:
                continue
            seen.add(sku)
            out.append(item)

    return out


def _extract_apollo_transport_payloads(html: str) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    script_blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, flags=re.S | re.I)

    for block in script_blocks:
        if "ApolloSSRDataTransport" not in block:
            continue

        start = 0
        while True:
            idx = block.find(".push(", start)
            if idx < 0:
                break
            arg_start = idx + len(".push(")
            arg, end_idx = _extract_balanced_parens(block, arg_start)
            start = end_idx
            if not arg:
                continue

            obj = _safe_js_object_load(arg.strip())
            if isinstance(obj, dict):
                payloads.append(obj)

    return payloads


def _extract_balanced_parens(text: str, start_index: int) -> tuple[str | None, int]:
    depth = 1
    in_str = False
    esc = False

    i = start_index
    while i < len(text):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            i += 1
            continue

        if ch == '"':
            in_str = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start_index:i], i + 1
        i += 1

    return None, len(text)


def _safe_js_object_load(raw: str) -> dict[str, Any] | None:
    text = raw.strip()
    if not text:
        return None

    # BestBuy payload is mostly JSON with occasional JS undefined.
    text = re.sub(r"\bundefined\b", "null", text)
    # Remove trailing commas before closing braces/brackets.
    text = re.sub(r",(\s*[}\]])", r"\1", text)

    try:
        obj = json.loads(text)
    except Exception:
        return None

    return obj if isinstance(obj, dict) else None


def _walk(node: Any):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def _looks_like_product(d: dict[str, Any]) -> bool:
    if "skuId" not in d:
        return False
    has_name = isinstance(d.get("name"), dict)
    has_url = isinstance(d.get("url"), dict)
    has_price = any(k.startswith("price(") for k in d.keys())
    return has_name and has_url and has_price


def _normalize_product(d: dict[str, Any]) -> dict[str, Any]:
    name = d.get("name") if isinstance(d.get("name"), dict) else {}
    url = d.get("url") if isinstance(d.get("url"), dict) else {}
    img = d.get("primaryImage") if isinstance(d.get("primaryImage"), dict) else {}
    review = d.get("reviewInfo") if isinstance(d.get("reviewInfo"), dict) else {}

    price_key = next((k for k in d.keys() if isinstance(k, str) and k.startswith("price(")), None)
    price_obj = d.get(price_key) if price_key and isinstance(d.get(price_key), dict) else {}

    pdp = url.get("pdp") or url.get("skuSpecificUrl") or url.get("relativePdp")
    if isinstance(pdp, str) and pdp.startswith("/"):
        pdp = f"https://www.bestbuy.com{pdp}"

    return {
        "item_id": str(d.get("skuId")) if d.get("skuId") is not None else None,
        "title": name.get("short") or name.get("title"),
        "url": pdp,
        "brand": (d.get("brand") or {}).get("name") if isinstance(d.get("brand"), dict) else None,
        "price": price_obj.get("customerPrice") or price_obj.get("displayableCustomerPrice"),
        "currency": "USD",
        "rating": review.get("averageRating"),
        "reviews_count": review.get("reviewCount"),
        "image_url": img.get("href") or img.get("piscesHref"),
        "source": "bestbuy_apollo_bootstrap",
        "raw": d,
    }
