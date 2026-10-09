"""Abercrombie & Fitch US product-listing category seeds."""

BASE_URL = "https://www.abercrombie.com/shop/us"

_CATEGORY_GROUPS = {
    "Women's": [
        "womens", "womens-new-arrivals", "womens-tops--1", "womens-bottoms--1",
        "womens-dresses-and-jumpsuits", "womens-coats-and-jackets", "womens-sweaters",
        "womens-activewear", "womens-accessories", "womens-shoes", "womens-swim",
        "womens-sleep-and-intimates", "womens-fragrance", "womens-office-approved",
        "womens-clearance",
    ],
    "Men's": [
        "mens", "mens-new-arrivals", "mens-tops--1", "mens-bottoms--1",
        "mens-coats-and-jackets", "mens-sweatshirts-and-sweatpants", "mens-activewear",
        "mens-shoes", "mens-accessories", "mens-suits", "mens-swim", "mens-underwear",
        "mens-cologne", "mens-office-approved", "mens-clearance",
    ],
    "Kids": ["kids", "a-and-f-kids", "baby-and-toddler-640646318"],
    "Brand/Collections": ["jeans", "activewear", "new", "sale"],
}

ABERCROMBIE_CATEGORIES = [
    {"category": slug, "department": department, "url": f"{BASE_URL}/{slug}"}
    for department, slugs in _CATEGORY_GROUPS.items()
    for slug in slugs
]
