"""LoopNet's national property searches, grouped by transaction type.

The inventory mirrors the sale and lease navigation exposed by LoopNet's
national search pages (verified 2026-10-13). Leaf names are globally unique so
the DAG's per-category output paths cannot collide across groups.
"""


LOOPNET_CATEGORIES = {
    "for-sale": {
        "commercial-real-estate-for-sale":
            "https://www.loopnet.com/search/commercial-real-estate/usa/for-sale/",
        "office-buildings-for-sale":
            "https://www.loopnet.com/search/office-buildings/usa/for-sale/",
        "industrial-properties-for-sale":
            "https://www.loopnet.com/search/industrial-properties/usa/for-sale/",
        "retail-properties-for-sale":
            "https://www.loopnet.com/search/retail-properties/usa/for-sale/",
        "restaurants-for-sale":
            "https://www.loopnet.com/search/restaurants/usa/for-sale/",
        "shopping-centers-for-sale":
            "https://www.loopnet.com/search/shopping-centers/usa/for-sale/",
        "specialty-properties-for-sale":
            "https://www.loopnet.com/search/specialty-properties/usa/for-sale/",
        "health-care-facilities-for-sale":
            "https://www.loopnet.com/search/health-care-facilities/usa/for-sale/",
        "laboratories-for-sale":
            "https://www.loopnet.com/search/laboratories/usa/for-sale/",
        "sports-entertainment-properties-for-sale":
            "https://www.loopnet.com/search/sports-entertainment-properties/usa/for-sale/",
        "multifamily-properties-for-sale":
            "https://www.loopnet.com/search/multifamily-properties/usa/for-sale/",
        "apartment-buildings-for-sale":
            "https://www.loopnet.com/search/apartment-buildings/usa/for-sale/",
        "hospitality-properties-for-sale":
            "https://www.loopnet.com/search/hospitality-properties/usa/for-sale/",
        "land-for-sale":
            "https://www.loopnet.com/search/land/usa/for-sale/",
    },
    "for-lease": {
        "commercial-real-estate-for-lease":
            "https://www.loopnet.com/search/commercial-real-estate/usa/for-lease/",
        "office-space-for-lease":
            "https://www.loopnet.com/search/office-space/usa/for-lease/",
        "medical-offices-for-lease":
            "https://www.loopnet.com/search/medical-offices/usa/for-lease/",
        "coworking-space-for-lease":
            "https://www.loopnet.com/search/coworking-space/usa/for-lease/",
        "industrial-space-for-lease":
            "https://www.loopnet.com/search/industrial-space/usa/for-lease/",
        "retail-space-for-lease":
            "https://www.loopnet.com/search/retail-space/usa/for-lease/",
        "restaurants-for-lease":
            "https://www.loopnet.com/search/restaurants/usa/for-lease/",
        "flex-space-for-lease":
            "https://www.loopnet.com/search/flex-space/usa/for-lease/",
        "laboratories-for-lease":
            "https://www.loopnet.com/search/laboratories/usa/for-lease/",
        "land-for-lease":
            "https://www.loopnet.com/search/land/usa/for-lease/",
    },
    "auctions": {
        "commercial-real-estate-auctions":
            "https://www.loopnet.com/search/commercial-real-estate/usa/auctions/",
    },
}
