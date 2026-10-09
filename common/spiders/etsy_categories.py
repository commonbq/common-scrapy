"""Stable Etsy category seeds used by :mod:`etsy_listing_spider`."""

ETSY_CATEGORIES = [
    {"category": name, "url": f"https://www.etsy.com/c/{name}"}
    for name in (
        "jewelry",
        "home-and-living",
        "clothing",
        "craft-supplies-and-tools",
        "weddings",
        "art-and-collectibles",
        "accessories",
        "bags-and-purses",
        "bath-and-beauty",
        "shoes",
        "toys-and-games",
        "kids-and-baby",
        "paper-and-party-supplies",
        "pet-supplies",
        "electronics-and-accessories",
        "books-movies-and-music",
        "gifts",
        "clothing/womens-clothing",
        "clothing/mens-clothing",
        "home-and-living/furniture",
    )
]
