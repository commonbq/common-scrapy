from __future__ import annotations

import json
import re
from typing import Any


def extract_bestbuy_items_from_bootstrap(html: str) -> list[dict[str, Any]]:
    """Extract product-like records from BestBuy Apollo bootstrap scripts."""
    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    for payload in _extract_apollo_transport_payloads(html):
        for node in _walk(payload):
            product = node
            listing_context: dict[str, Any] = {}

            # The current category response nests each Product in a
            # BestMediaAdsAcceptedSku record. Capture useful listing metadata
            # from that wrapper before the recursive walk reaches Product.
            nested_product = node.get("product") if isinstance(node, dict) else None
            if isinstance(nested_product, dict) and _looks_like_product(nested_product):
                product = nested_product
                listing_context = {
                    "isSponsored": node.get("__typename") == "BestMediaAdsAcceptedSku",
                    "position": node.get("rank"),
                    "primaryCategoryId": node.get("primaryCategoryId"),
                    "campaignId": node.get("campaignId"),
                }

            if not isinstance(product, dict) or not _looks_like_product(product):
                continue

            item = _normalize_product(product)
            item.update(listing_context)
            sku = item.get("skuId")
            if sku not in seen:
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
    # Older Apollo responses key this field with its GraphQL arguments (for
    # example ``price(locationId:...)``).  Current Next.js listing responses,
    # including the saved sample, expose it as a regular ``price`` field.
    has_price = isinstance(d.get("price"), dict) or any(
        isinstance(k, str) and k.startswith("price(") for k in d.keys()
    )
    return has_name and has_url and has_price


def _normalize_product(d: dict[str, Any]) -> dict[str, Any]:
    name = d.get("name") if isinstance(d.get("name"), dict) else {}
    url = d.get("url") if isinstance(d.get("url"), dict) else {}
    img = d.get("primaryImage") if isinstance(d.get("primaryImage"), dict) else {}
    review = d.get("reviewInfo") if isinstance(d.get("reviewInfo"), dict) else {}

    price_obj = d.get("price") if isinstance(d.get("price"), dict) else None
    if price_obj is None:
        price_key = next(
            (k for k in d.keys() if isinstance(k, str) and k.startswith("price(")), None
        )
        price_obj = (
            d.get(price_key) if price_key and isinstance(d.get(price_key), dict) else {}
        )

    pdp = url.get("pdp") or url.get("skuSpecificUrl") or url.get("relativePdp")
    if isinstance(pdp, str) and pdp.startswith("/"):
        pdp = f"https://www.bestbuy.com{pdp}"

    title = name.get("short") or name.get("title")
    current_price = _first_present(
        price_obj, "customerPrice", "currentPrice", "displayableCustomerPrice"
    )
    original_price = _first_present(price_obj, "regularPrice", "originalPrice")
    brand = (
        (d.get("brand") or {}).get("name")
        if isinstance(d.get("brand"), dict)
        else d.get("brand")
    )
    if not brand and isinstance(title, str) and " - " in title:
        # Best Buy's short product names consistently start with "Brand - ".
        brand = title.split(" - ", 1)[0].strip() or None

    return {
        "skuId": str(d.get("skuId")) if d.get("skuId") is not None else None,
        "title": title,
        "url": pdp,
        "brand": brand,
        "price": current_price,
        "originalPrice": original_price,
        "discountAmount": price_obj.get("totalSavings"),
        "discountPercent": price_obj.get("totalSavingsPercent"),
        "priceBadge": price_obj.get("preferredBadging")
        or price_obj.get("saleEventMessageType"),
        "isMAP": price_obj.get("isMAP"),
        "rating": review.get("averageRating"),
        "reviewCount": review.get("reviewCount"),
        "imageUrl": img.get("href") or img.get("piscesHref"),
        "openBoxCondition": d.get("openBoxCondition"),
        "raw": d,
    }


def _first_present(values: dict[str, Any], *keys: str) -> Any:
    """Return the first present, non-null value without discarding zeroes."""
    for key in keys:
        if key in values and values[key] is not None:
            return values[key]
    return None
