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
