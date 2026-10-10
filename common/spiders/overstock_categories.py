"""Overstock (overstock.com) product-listing category seeds.

Kept as a standalone data module (no spider imports) so Airflow's
``_spider_category_groups`` can load it via ``runpy`` at DAG-parse time.
Importing the spider module there would pull in ``common.spiders``, which
collides with the DAG package's ``common.py`` on the Airflow path.

The constant is the grouped ``{department: {leaf: {url, ...}}}`` mapping the
base listing spider contract expects; leaves are what ``-a category=<leaf>``
selects and what the DAG factory schedules one task per.
"""

OVERSTOCK_CATEGORIES: dict[str, dict[str, dict[str, object]]] = {
    "Furniture": {
        "furniture": {
            "url": "https://www.overstock.com/c/furniture?t=24352",
            "subcategory": None,
        },
        "living-room-furniture": {
            "url": "https://www.overstock.com/c/furniture/living-room-furniture?t=24359",
            "subcategory": "Living Room Furniture",
        },
        "bedroom-furniture": {
            "url": "https://www.overstock.com/c/furniture/bedroom-furniture?t=24356",
            "subcategory": "Bedroom Furniture",
        },
    },
    "Rugs": {
        "rugs": {
            "url": "https://www.overstock.com/c/rugs?t=17602",
            "subcategory": None,
        },
        "area-rugs": {
            "url": "https://www.overstock.com/c/rugs/area-rugs?t=17603",
            "subcategory": "Area Rugs",
        },
    },
    "Patio": {
        "patio-outdoor": {
            "url": "https://www.overstock.com/c/outdoor?t=7907",
            "subcategory": None,
        },
        "patio-furniture": {
            "url": "https://www.overstock.com/c/outdoor/patio-furniture?t=7908",
            "subcategory": "Patio Furniture",
        },
    },
    "Lighting": {
        "lighting": {
            "url": "https://www.overstock.com/c/lighting?t=31087",
            "subcategory": None,
        },
        "ceiling-lighting": {
            "url": "https://www.overstock.com/c/lighting/ceiling-lighting?t=31290",
            "subcategory": "Ceiling Lighting",
        },
    },
    "Decor": {
        "home-decor": {
            "url": "https://www.overstock.com/c/home-decor?t=28396",
            "subcategory": None,
        },
        "art": {
            "url": "https://www.overstock.com/c/art?t=28454",
            "subcategory": "Art",
        },
    },
    "Bedding": {
        "bedding": {
            "url": "https://www.overstock.com/c/bed-bath/bedding?t=1",
            "subcategory": None,
        },
        "mattresses": {
            "url": "https://www.overstock.com/c/mattresses?t=24351",
            "subcategory": "Mattresses",
        },
    },
    "Apparel": {
        "apparel": {
            "url": "https://www.overstock.com/c/clothing-shoes?t=75555",
            "subcategory": None,
        },
        "womens-clothing": {
            "url": "https://www.overstock.com/c/womens/womens-clothing?t=75703",
            "subcategory": "Women's Clothing",
        },
        "mens-clothing": {
            "url": "https://www.overstock.com/c/mens/mens-clothing?t=75687",
            "subcategory": "Men's Clothing",
        },
    },
    "Jewelry & Watches": {
        "jewelry-watches": {
            "url": "https://www.overstock.com/c/jewelry-watches?t=71533",
            "subcategory": None,
        },
        "watches": {
            "url": "https://www.overstock.com/c/jewelry-watches/watches?t=78255",
            "subcategory": "Watches",
        },
    },
    "More": {
        "kitchen-dining": {
            "url": "https://www.overstock.com/c/kitchen-dining?t=24566",
            "subcategory": "Kitchen & Dining",
        },
        "home-improvement": {
            "url": "https://www.overstock.com/c/home-improvement?t=31076",
            "subcategory": "Home Improvement",
        },
    },
}
