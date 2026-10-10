"""Stable World Market department/category seeds.

The product spider resolves the SFCC category id from each landing page and then
uses only ``Search-UpdateGrid`` for product extraction.
"""

WORLD_MARKET_BASE_URL = "https://www.worldmarket.com"

WORLD_MARKET_CATEGORIES = {
    "furniture": {
        "furniture-shop-all-furniture": {
            "url": "https://www.worldmarket.com/c/furniture/shop-all-furniture/",
            "department": "furniture",
            "category": "furniture-shop-all-furniture",
        },
    },
    "holidays": {
        "holidays": {
            "url": "https://www.worldmarket.com/c/holidays/",
            "department": "holidays",
            "category": "holidays",
        },
    },
    "outdoor": {
        "outdoor": {
            "url": "https://www.worldmarket.com/c/outdoor/",
            "department": "outdoor",
            "category": "outdoor",
        },
    },
    "rugs": {
        "rugs": {
            "url": "https://www.worldmarket.com/c/rugs/",
            "department": "rugs",
            "category": "rugs",
        },
    },
    "decor-and-pillows": {
        "decor-pillows": {
            "url": "https://www.worldmarket.com/c/decor-and-pillows/",
            "department": "decor-and-pillows",
            "category": "decor-pillows",
        },
    },
    "lighting": {
        "lighting": {
            "url": "https://www.worldmarket.com/c/lighting/",
            "department": "lighting",
            "category": "lighting",
        },
    },
    "wall-decor-and-mirrors": {
        "wall-decor-mirrors": {
            "url": "https://www.worldmarket.com/c/wall-decor-and-mirrors/",
            "department": "wall-decor-and-mirrors",
            "category": "wall-decor-mirrors",
        },
    },
    "kitchen": {
        "kitchen": {
            "url": "https://www.worldmarket.com/c/kitchen/",
            "department": "kitchen",
            "category": "kitchen",
        },
    },
    "dining": {
        "dining": {
            "url": "https://www.worldmarket.com/c/dining/",
            "department": "dining",
            "category": "dining",
        },
    },
    "food-and-drinks": {
        "food-drinks": {
            "url": "https://www.worldmarket.com/c/food-and-drinks/",
            "department": "food-and-drinks",
            "category": "food-drinks",
        },
    },
    "bath": {
        "bath": {
            "url": "https://www.worldmarket.com/c/bath/",
            "department": "bath",
            "category": "bath",
        },
    },
    "gifts": {
        "gifts": {
            "url": "https://www.worldmarket.com/c/gifts/",
            "department": "gifts",
            "category": "gifts",
        },
    },
    "sale": {
        "sale": {
            "url": "https://www.worldmarket.com/c/sale/",
            "department": "sale",
            "category": "sale",
        },
    },
}
