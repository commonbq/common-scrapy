"""Stable, product-bearing REI category shortcuts."""

BASE_URL = "https://www.rei.com"

REI_CATEGORIES = [
    {"category": slug, "url": f"{BASE_URL}/c/{slug}"}
    for slug in (
        "hiking-footwear",
        "hiking-backpacks",
        "tents",
        "sleeping-bags",
        "sleeping-pads",
        "camp-kitchen",
        "camp-furniture",
        "water-bottles",
        "headlamps",
        "gps",
        "first-aid",
        "trekking-poles-hiking-staffs",
        "climbing-shoes",
        "climbing-harnesses",
        "bikes",
        "bike-helmets",
        "kayaks",
        "mens-jackets",
        "womens-jackets",
        "kids-footwear",
    )
]
