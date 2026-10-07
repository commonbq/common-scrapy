"""Stable World Market department/category seeds.

The product spider resolves the SFCC category id from each landing page and then
uses only ``Search-UpdateGrid`` for product extraction.
"""

WORLD_MARKET_BASE_URL = "https://www.worldmarket.com"

WORLD_MARKET_CATEGORIES = [
    {"category": "furniture-shop-all-furniture", "url": f"{WORLD_MARKET_BASE_URL}/c/furniture/shop-all-furniture/"},
    {"category": "holidays", "url": f"{WORLD_MARKET_BASE_URL}/c/holidays/"},
    {"category": "outdoor", "url": f"{WORLD_MARKET_BASE_URL}/c/outdoor/"},
    {"category": "rugs", "url": f"{WORLD_MARKET_BASE_URL}/c/rugs/"},
    {"category": "decor-pillows", "url": f"{WORLD_MARKET_BASE_URL}/c/decor-and-pillows/"},
    {"category": "lighting", "url": f"{WORLD_MARKET_BASE_URL}/c/lighting/"},
    {"category": "wall-decor-mirrors", "url": f"{WORLD_MARKET_BASE_URL}/c/wall-decor-and-mirrors/"},
    {"category": "kitchen", "url": f"{WORLD_MARKET_BASE_URL}/c/kitchen/"},
    {"category": "dining", "url": f"{WORLD_MARKET_BASE_URL}/c/dining/"},
    {"category": "food-drinks", "url": f"{WORLD_MARKET_BASE_URL}/c/food-and-drinks/"},
    {"category": "bath", "url": f"{WORLD_MARKET_BASE_URL}/c/bath/"},
    {"category": "gifts", "url": f"{WORLD_MARKET_BASE_URL}/c/gifts/"},
    {"category": "sale", "url": f"{WORLD_MARKET_BASE_URL}/c/sale/"},
]
