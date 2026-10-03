"""Bath & Body Works navigation inventory captured from hydrated site-nav state."""

BASE_URL = "https://www.bathandbodyworks.com"

BATHANDBODYWORKS_CATEGORIES = {
    "sale": {"all-sale": "/g/all-sale", "top-offers": "/g/top-offers"},
    "new-and-now": {
        "new-and-now": "/g/new-and-now",
        "top-fragrance-finder": "/g/top-fragrance-finder",
    },
    "gifts": {
        "gifts": "/g/gifts", "gifts-for-her": "/c/gifts/gifts-for-her",
        "gifts-for-him": "/c/gifts/gifts-for-him", "gift-sets": "/c/gifts/gift-sets",
        "gifts-under-20": "/c/gifts/gifts-under-20", "accessories": "/c/gifts/accessories",
        "boxes-bags": "/c/gifts/boxes-bags",
    },
    "body-care": {
        "body-care": "/c/body-care", "all-fragrance": "/c/body-care/all-fragrance",
        "perfume-cologne": "/c/body-care/perfume-cologne", "body-sprays-mists": "/c/body-care/body-sprays-mists",
        "all-moisturizers": "/c/body-care/all-moisturizers", "body-cream": "/c/body-care/body-cream",
        "body-lotion": "/c/body-care/body-lotion", "all-bath-shower": "/c/body-care/all-bath-shower",
        "body-wash-shower-gel": "/c/body-care/body-wash-shower-gel", "body-scrub": "/c/body-care/body-scrub",
        "travel": "/c/body-care/travel", "lip-gloss-balms": "/c/body-care/lip-gloss-balms",
        "wellness-body-care": "/c/body-care/wellness-body-care",
    },
    "candles": {
        "all-candles": "/g/all-candles", "3-wick-candles": "/c/all-candles/3-wick-candles",
        "4-wick-candles": "/c/all-candles/4-wick-candles", "single-wick-candles": "/c/all-candles/single-wick-candles",
        "fall-candles": "/c/all-candles/fall-candles", "candle-holders": "/c/all-candles/candle-holders",
    },
    "home-fragrance": {
        "home-fragrance": "/g/home-fragrance", "all-wallflowers": "/c/home-fragrance/all-wallflowers",
        "wallflowers-refills": "/c/home-fragrance/wallflowers-refills", "wallflowers-plugs": "/c/home-fragrance/wallflowers-plugs",
        "reeds": "/c/home-fragrance/reeds", "room-sprays-mists": "/c/home-fragrance/room-sprays-mists",
        "car-fragrance": "/c/home-fragrance/car-fragrance", "wallflowers-create-your-set": "/c/home-fragrance/wallflowers-create-your-set",
    },
    "hand-soaps-sanitizers": {
        "hand-soaps-sanitizers": "/g/hand-soaps-sanitizers", "all-hand-soaps": "/c/hand-soaps-sanitizers/all-hand-soaps",
        "foaming-hand-soap": "/c/hand-soaps-sanitizers/foaming-hand-soap", "gel-hand-soaps": "/c/hand-soaps-sanitizers/gel-hand-soaps",
        "moisturizing-hand-soaps": "/c/hand-soaps-sanitizers/moisturizing-hand-soaps", "revitalizing-hand-soaps": "/c/hand-soaps-sanitizers/revitalizing-hand-soaps",
        "hand-soap-refills": "/c/hand-soaps-sanitizers/hand-soap-refills", "hand-soap-holders": "/c/hand-soaps-sanitizers/hand-soap-holders",
        "all-hand-sanitizers": "/c/hand-soaps-sanitizers/all-hand-sanitizers", "pocketbac-hand-sanitizers": "/c/hand-soaps-sanitizers/pocketbac-hand-sanitizers",
        "hand-sanitizer-sprays": "/c/hand-soaps-sanitizers/hand-sanitizer-sprays", "pocketbac-sanitizer-holders": "/c/hand-soaps-sanitizers/pocketbac-sanitizer-holders",
        "discover-hand-soaps": "/c/hand-soaps-sanitizers/discover-hand-soaps",
    },
    "mens-shop": {
        "mens-shop": "/g/mens-shop", "mens-body-care": "/c/mens-shop/mens-body-care",
        "mens-fragrance": "/c/mens-shop/mens-fragrance", "mens-shower-gel-body-wash": "/c/mens-shop/mens-shower-gel-body-wash",
        "mens-body-lotion-body-cream": "/c/mens-shop/mens-body-lotion-body-cream", "mens-deodorant": "/c/mens-collection/mens-deodorant",
    },
    "home-care": {
        "home-care": "/g/home-care", "all-laundry": "/c/laundry-care/all-laundry",
        "laundry-detergent": "/c/home-care/all-laundry/laundry-detergent", "fragrance-boosters": "/c/home-care/all-laundry/fragrance-boosters",
        "dryer-sheets": "/c/home-care/all-laundry/dryer-sheets", "all-kitchen-care": "/c/kitchen-care/all-kitchen-care",
        "dish-wash": "/c/kitchen-care/dish-wash", "counter-spray": "/c/kitchen-care/counter-spray",
    },
}


def flattened_categories():
    """Return category aliases accepted by the spider, preserving nav order."""
    return [
        {"category": name, "url": BASE_URL + path}
        for group in BATHANDBODYWORKS_CATEGORIES.values()
        for name, path in group.items()
    ]
