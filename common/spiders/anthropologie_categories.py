"""Anthropologie category inventory captured from the US site on 2026-09-27."""

ANTHROPOLOGIE_CATEGORIES = {
    "clothing": [
        {"category": "womens-clothing", "url": "https://www.anthropologie.com/womens-clothing"},
        {"category": "womens-clothing-ca", "url": "https://www.anthropologie.com/en-ca/womens-clothing"},
        {"category": "womens-clothing-page-2", "url": "https://www.anthropologie.com/womens-clothing?page=2"},
        {"category": "dresses", "url": "https://www.anthropologie.com/dresses"},
        {"category": "dresses-long-sleeve", "url": "https://www.anthropologie.com/dresses?sleevelength=Long+Sleeve"},
        {"category": "dresses-shift", "url": "https://www.anthropologie.com/dresses?style=Shift"},
        {"category": "dresses-slip", "url": "https://www.anthropologie.com/dresses?style=Slip"},
        {"category": "shoes", "url": "https://www.anthropologie.com/shoes"},
    ],
    "sale": [
        {"category": "sale", "url": "https://www.anthropologie.com/sale-all"},
    ],
}


def flattened_categories() -> list[dict[str, str]]:
    return [entry for entries in ANTHROPOLOGIE_CATEGORIES.values() for entry in entries]
