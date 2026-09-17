from __future__ import annotations

import json
import re
from typing import Any, Iterable

from parsel import Selector


def extract_marko_products(html: str) -> list[dict[str, Any]]:
    """Extract eBay search-result products from Marko hydration state."""
    sel = Selector(text=html or "")
    cards: list[dict[str, Any]] = []
    seen: set[str] = set()

    for script in sel.css("script"):
        source = script.xpath("string()").get() or ""
        if "$brwweb_C" not in source:
            continue
        for payload in _iter_marko_payloads(source):
            for card in _iter_marko_listing_cards(payload):
                product_id = _as_str(card.get("listingId"))
                if not product_id or product_id in seen:
                    continue
                seen.add(product_id)
                cards.append(card)

    return [
        _normalize_marko_listing(card, position)
        for position, card in enumerate(cards, start=1)
    ]


def extract_subcategories_from_html(html: str) -> list[dict[str, Any]]:
    """Return the subcategory name and URL for each browse destination tile."""
    sel = Selector(text=html or "")
    out: list[dict[str, Any]] = []
    seen: set[tuple[str | None, str | None]] = set()

    for card in sel.css(".dp-browse-destinations-module div.su-card-container"):
        url = card.css("a.su-item-card__title::attr(href)").get()
        title = " ".join(
            t.strip()
            for t in card.css(
                "a.su-item-card__title *::text, a.su-item-card__title::text"
            ).getall()
            if t.strip()
        )
        if not _is_plausible_ebay_browse_card(title=title, url=url):
            continue

        key = (title, url)
        if key in seen:
            continue
        seen.add(key)

        out.append(
            {
                "subCategory": title,
                "url": url,
            }
        )

    return out


def _iter_marko_payloads(source: str) -> Iterable[Any]:
    """Decode JSON arguments passed to eBay's ``$brwweb_C.concat(...)``."""
    decoder = json.JSONDecoder()
    cursor = 0
    marker = ".concat("
    while True:
        marker_index = source.find(marker, cursor)
        if marker_index < 0:
            return
        json_start = marker_index + len(marker)
        try:
            payload, consumed = decoder.raw_decode(source[json_start:])
        except (TypeError, ValueError, json.JSONDecodeError):
            cursor = json_start
            continue
        yield payload
        cursor = json_start + consumed


def _iter_marko_listing_cards(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        action = value.get("action") if isinstance(value.get("action"), dict) else {}
        url = action.get("URL")
        ordering = (
            value.get("itemPropertyOrdering")
            if isinstance(value.get("itemPropertyOrdering"), dict)
            else {}
        )
        if (
            value.get("_type") == "ListingItemCard"
            and value.get("listingId")
            and isinstance(url, str)
            and "displayPrice" in value
            and "imageContainer" in value
            and "LIST_LAYOUT" in ordering
        ):
            yield value
        for child in value.values():
            yield from _iter_marko_listing_cards(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_marko_listing_cards(child)


def _normalize_marko_listing(card: dict[str, Any], position: int) -> dict[str, Any]:
    action = card.get("action") if isinstance(card.get("action"), dict) else {}
    price, currency = _marko_money(card.get("displayPrice"))
    original_price, original_currency = _marko_money(card.get("previousPrice"))

    title_spans = _marko_text_spans(card.get("title"))
    title = " ".join(
        text for text in title_spans if text.lower() not in {"new listing", "sponsored"}
    ).strip()
    is_new_listing = any(text.lower() == "new listing" for text in title_spans)

    condition_text = _marko_text(card.get("listingCondition"))
    condition = condition_text
    brand = None
    if condition_text and "·" in condition_text:
        condition, brand = [part.strip() for part in condition_text.split("·", 1)]

    image_container = (
        card.get("imageContainer")
        if isinstance(card.get("imageContainer"), dict)
        else {}
    )
    image_values = [image_container.get("image")]
    secondary_images = image_container.get("secondaryImages")
    if isinstance(secondary_images, list):
        image_values.extend(secondary_images)
    image_urls = []
    for image in image_values:
        image_url = image.get("URL") if isinstance(image, dict) else None
        if image_url and image_url not in image_urls:
            image_urls.append(image_url)

    shipping_text = _marko_text(card.get("logisticsCost"))
    shipping_cost, shipping_currency = _money(shipping_text)
    if shipping_text and "free" in shipping_text.lower():
        shipping_cost = 0.0
        shipping_currency = currency

    quantity_text = _marko_text(card.get("quantity"))
    hotness_text = _marko_text(card.get("itemHotness"))
    purchase_options = _marko_text(card.get("purchaseOptions"))
    search = card.get("__search") if isinstance(card.get("__search"), dict) else {}
    watch_text = _marko_text(search.get("watchCountTotal"))
    product_review = (
        card.get("productReview") if isinstance(card.get("productReview"), dict) else {}
    )

    record = {
        "productId": _as_str(card.get("listingId")),
        "title": title or None,
        "url": action.get("URL"),
        "price": price,
        "currency": currency,
        "originalPrice": original_price,
        "originalCurrency": original_currency,
        "discountPercentage": _discount_percentage(price, original_price),
        "imageUrl": image_urls[0] if image_urls else None,
        "imageUrls": image_urls,
        "condition": condition,
        "brand": brand,
        "quantityAvailable": _count_from_text(quantity_text),
        "quantityText": quantity_text,
        "shippingCost": shipping_cost,
        "shippingCurrency": shipping_currency,
        "shippingText": shipping_text,
        "deliveryText": _marko_text(card.get("deliveryOptions")),
        "purchaseOptions": purchase_options,
        "acceptsBestOffer": (
            True
            if purchase_options and "best offer" in purchase_options.lower()
            else None
        ),
        "soldCount": (
            _count_from_text(hotness_text)
            if hotness_text and "sold" in hotness_text.lower()
            else None
        ),
        "hotnessText": hotness_text,
        "watchCount": _count_from_text(watch_text),
        "watchText": watch_text,
        "isSponsored": bool(card.get("sponsoredInfo")),
        "isNewListing": True if is_new_listing else None,
        "ratingValue": _marko_scalar(product_review.get("reviews")),
        "reviewCount": _coerce_int(_marko_scalar(product_review.get("reviewCount"))),
        "position": position,
        "raw": card,
    }
    return {
        key: value for key, value in record.items() if value is not None and value != []
    }


def _marko_text_spans(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return []
    spans = value.get("textSpans")
    if isinstance(spans, list):
        return [
            str(span["text"]).strip()
            for span in spans
            if isinstance(span, dict) and span.get("text")
        ]
    return _marko_text_spans(value.get("text"))


def _marko_text(value: Any) -> str | None:
    text = " ".join(_marko_text_spans(value)).strip()
    return text or None


def _marko_scalar(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    scalar = value.get("value")
    if isinstance(scalar, dict):
        return scalar.get("value")
    return scalar


def _marko_money(value: Any) -> tuple[float | None, str | None]:
    if not isinstance(value, dict):
        return None, None
    money = value.get("value")
    if not isinstance(money, dict):
        return None, None
    return _coerce_num(money.get("value")), _as_str(money.get("currency"))


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


def _coerce_int(value: Any) -> int | None:
    number = _coerce_num(value)
    return int(number) if number is not None else None


def _money(text: str | None) -> tuple[float | None, str | None]:
    if not text:
        return None, None
    match = re.search(r"(?:(USD|GBP|EUR)\s*)?([£$€])?\s*([\d,]+(?:\.\d+)?)", text, re.I)
    if not match:
        return None, None
    currency = (match.group(1) or "").upper() or {
        "$": "USD",
        "£": "GBP",
        "€": "EUR",
    }.get(match.group(2))
    return _coerce_num(match.group(3)), currency


def _count_from_text(text: str | None) -> int | None:
    if not text:
        return None
    match = re.search(r"([\d,]+)", text)
    return int(match.group(1).replace(",", "")) if match else None


def _discount_percentage(
    price: float | None, original_price: float | None
) -> float | None:
    if price is None or not original_price or price > original_price:
        return None
    return round((original_price - price) / original_price * 100, 2)


def _as_str(v: Any) -> str | None:
    return str(v) if v is not None else None


def _is_plausible_ebay_browse_card(*, title: str | None, url: str | None) -> bool:
    if not url:
        return False
    normalized = url.lower()
    if "/b/" not in normalized and "/sch/i.html" not in normalized:
        return False
    t = (title or "").strip().lower()
    if not t or t in {"shop on ebay", "shop on ebay!"}:
        return False
    if "shop on ebay" in t and len(t) <= 20:
        return False
    return True
