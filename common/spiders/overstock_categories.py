"""Overstock (overstock.com) product-listing category seeds.

Kept as a standalone data module (no spider imports) so Airflow's
``_spider_category_groups`` can load it via ``runpy`` at DAG-parse time.
Importing the spider module there would pull in ``common.spiders``, which
collides with the DAG package's ``common.py`` on the Airflow path.

The constant is the grouped ``{department: {leaf: {url, ...}}}`` mapping the
base listing spider contract expects; leaves are what ``-a category=<leaf>``
selects and what the DAG factory schedules one task per.

Leaf keys are unique across all departments so ``category_entry()`` can
resolve any leaf unambiguously.
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
        "dining-kitchen-bar-furniture": {
            "url": "https://www.overstock.com/c/furniture/dining-kitchen-bar-furniture?t=24357",
            "subcategory": "Dining Kitchen Bar Furniture",
        },
        "entryway-furniture": {
            "url": "https://www.overstock.com/c/furniture/entryway-furniture",
            "subcategory": "Entryway Furniture",
        },
        "home-office-furniture": {
            "url": "https://www.overstock.com/c/furniture/home-office-furniture",
            "subcategory": "Home Office Furniture",
        },
        "bathroom-furniture": {
            "url": "https://www.overstock.com/c/furniture/bathroom-furniture",
            "subcategory": "Bathroom Furniture",
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
        "bathroom-lighting": {
            "url": "https://www.overstock.com/c/lighting/bathroom-lighting",
            "subcategory": "Bathroom Lighting",
        },
        "ceiling-fans": {
            "url": "https://www.overstock.com/c/lighting/ceiling-fans",
            "subcategory": "Ceiling Fans",
        },
        "kitchen-lighting": {
            "url": "https://www.overstock.com/c/lighting/kitchen-lighting",
            "subcategory": "Kitchen Lighting",
        },
        "lamps": {
            "url": "https://www.overstock.com/c/lighting/lamps",
            "subcategory": "Lamps",
        },
        "outdoor-lighting": {
            "url": "https://www.overstock.com/c/lighting/outdoor-lighting",
            "subcategory": "Outdoor Lighting",
        },
        "wall-lighting": {
            "url": "https://www.overstock.com/c/lighting/wall-lighting",
            "subcategory": "Wall Lighting",
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
        "doormats": {
            "url": "https://www.overstock.com/c/rugs/doormats",
            "subcategory": "Doormats",
        },
        "kitchen-mats": {
            "url": "https://www.overstock.com/c/rugs/kitchen-mats",
            "subcategory": "Kitchen Mats",
        },
        "one-of-a-kind-rugs": {
            "url": "https://www.overstock.com/c/rugs/one-of-a-kind-rugs",
            "subcategory": "One of a Kind Rugs",
        },
        "outdoor-rugs": {
            "url": "https://www.overstock.com/c/rugs/outdoor-rugs",
            "subcategory": "Outdoor Rugs",
        },
        "rug-pads": {
            "url": "https://www.overstock.com/c/rugs/rug-pads",
            "subcategory": "Rug Pads",
        },
        "stair-tread-rugs": {
            "url": "https://www.overstock.com/c/rugs/stair-tread-rugs",
            "subcategory": "Stair Tread Rugs",
        },
    },
    "Home Decor": {
        "home-decor": {
            "url": "https://www.overstock.com/c/home-decor?t=28396",
            "subcategory": None,
        },
        "art": {
            "url": "https://www.overstock.com/c/art?t=28454",
            "subcategory": "Art",
        },
        "artificial-plants-flowers": {
            "url": "https://www.overstock.com/c/home-decor/artificial-plants-flowers",
            "subcategory": "Artificial Plants & Flowers",
        },
        "clocks": {
            "url": "https://www.overstock.com/c/home-decor/clocks",
            "subcategory": "Clocks",
        },
        "decorative-accessories": {
            "url": "https://www.overstock.com/c/home-decor/decorative-accessories",
            "subcategory": "Decorative Accessories",
        },
        "mirrors": {
            "url": "https://www.overstock.com/c/home-decor/mirrors",
            "subcategory": "Mirrors",
        },
        "throw-pillows": {
            "url": "https://www.overstock.com/c/home-decor/throw-pillows",
            "subcategory": "Throw Pillows",
        },
        "wall-shelves": {
            "url": "https://www.overstock.com/c/home-decor/wall-shelves",
            "subcategory": "Wall Shelves",
        },
        "window-treatments": {
            "url": "https://www.overstock.com/c/home-decor/window-treatments",
            "subcategory": "Window Treatments",
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
        "bed-in-a-bag": {
            "url": "https://www.overstock.com/c/bedding/bed-in-a-bag",
            "subcategory": "Bed-in-a-Bag",
        },
        "bed-pillows": {
            "url": "https://www.overstock.com/c/bedding/bed-pillows",
            "subcategory": "Bed Pillows",
        },
        "bed-protectors": {
            "url": "https://www.overstock.com/c/bedding/bed-protectors",
            "subcategory": "Bed Protectors",
        },
        "bed-sheets-pillowcases": {
            "url": "https://www.overstock.com/c/bedding/bed-sheets-pillowcases",
            "subcategory": "Bed Sheets & Pillowcases",
        },
        "bed-skirts": {
            "url": "https://www.overstock.com/c/bedding/bed-skirts",
            "subcategory": "Bed Skirts",
        },
        "bedding-sets": {
            "url": "https://www.overstock.com/c/bedding/bedding-sets",
            "subcategory": "Bedding Sets",
        },
        "comforters-and-sets": {
            "url": "https://www.overstock.com/c/bedding/comforters-and-sets",
            "subcategory": "Comforters & Sets",
        },
        "comforters-duvet-inserts": {
            "url": "https://www.overstock.com/c/bedding/comforters-duvet-inserts",
            "subcategory": "Comforters & Duvet Inserts",
        },
        "daybed-cover-sets": {
            "url": "https://www.overstock.com/c/bedding/daybed-cover-sets",
            "subcategory": "Daybed Cover Sets",
        },
        "duvet-covers-and-sets": {
            "url": "https://www.overstock.com/c/bedding/duvet-covers-and-sets",
            "subcategory": "Duvet Covers & Sets",
        },
        "mattress-pads-toppers": {
            "url": "https://www.overstock.com/c/bedding/mattress-pads-toppers",
            "subcategory": "Mattress Pads & Toppers",
        },
        "quilts-bedspreads": {
            "url": "https://www.overstock.com/c/bedding/quilts-bedspreads",
            "subcategory": "Quilts & Bedspreads",
        },
    },
    "Patio & Outdoor": {
        "patio-outdoor": {
            "url": "https://www.overstock.com/c/outdoor?t=7907",
            "subcategory": None,
        },
        "patio-furniture": {
            "url": "https://www.overstock.com/c/outdoor/patio-furniture?t=7908",
            "subcategory": "Patio Furniture",
        },
        "outdoor-decor": {
            "url": "https://www.overstock.com/c/outdoor/outdoor-decor",
            "subcategory": "Outdoor Decor",
        },
        "outdoor-heating-cooling": {
            "url": "https://www.overstock.com/c/outdoor/outdoor-heating-cooling",
            "subcategory": "Outdoor Heating & Cooling",
        },
        "outdoor-play": {
            "url": "https://www.overstock.com/c/outdoor/outdoor-play",
            "subcategory": "Outdoor Play",
        },
        "outdoor-shade-structures": {
            "url": "https://www.overstock.com/c/outdoor/outdoor-shade-structures",
            "subcategory": "Outdoor Shade Structures",
        },
    },
    "Kitchen & Dining": {
        "kitchen-dining": {
            "url": "https://www.overstock.com/c/kitchen-dining?t=24566",
            "subcategory": "Kitchen & Dining",
        },
        "cookware": {
            "url": "https://www.overstock.com/c/kitchen-dining/cookware",
            "subcategory": "Cookware",
        },
        "dinnerware": {
            "url": "https://www.overstock.com/c/kitchen-dining/dinnerware",
            "subcategory": "Dinnerware",
        },
        "flatware": {
            "url": "https://www.overstock.com/c/kitchen-dining/flatware",
            "subcategory": "Flatware",
        },
        "small-kitchen-appliances": {
            "url": "https://www.overstock.com/c/kitchen-dining/small-kitchen-appliances",
            "subcategory": "Small Kitchen Appliances",
        },
    },
    "Home Improvement": {
        "home-improvement": {
            "url": "https://www.overstock.com/c/home-improvement?t=31076",
            "subcategory": "Home Improvement",
        },
        "doors": {
            "url": "https://www.overstock.com/c/home-improvement/doors",
            "subcategory": "Doors",
        },
    },
    "Bath": {
        "bath": {
            "url": "https://www.overstock.com/c/bed-bath/bath?t=18647",
            "subcategory": "Bath",
        },
        "bathroom-rugs-bath-mats": {
            "url": "https://www.overstock.com/c/bath/bathroom-rugs-bath-mats",
            "subcategory": "Bathroom Rugs & Bath Mats",
        },
        "shower-curtains-and-accessories": {
            "url": "https://www.overstock.com/c/bath/shower-curtains-and-accessories",
            "subcategory": "Shower Curtains & Accessories",
        },
        "towels": {
            "url": "https://www.overstock.com/c/bath/towels",
            "subcategory": "Towels",
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
        "womens-shoes": {
            "url": "https://www.overstock.com/c/womens/womens-shoes",
            "subcategory": "Women's Shoes",
        },
        "mens-shoes": {
            "url": "https://www.overstock.com/c/mens/mens-shoes",
            "subcategory": "Men's Shoes",
        },
        "womens-accessories": {
            "url": "https://www.overstock.com/c/womens/womens-accessories",
            "subcategory": "Women's Accessories",
        },
        "womens-activewear": {
            "url": "https://www.overstock.com/c/womens-clothing/womens-activewear",
            "subcategory": "Women's Activewear",
        },
        "womens-dresses": {
            "url": "https://www.overstock.com/c/womens-clothing/womens-dresses",
            "subcategory": "Women's Dresses",
        },
        "womens-loungewear": {
            "url": "https://www.overstock.com/c/womens-clothing/womens-loungewear",
            "subcategory": "Women's Loungewear",
        },
        "womens-outerwear": {
            "url": "https://www.overstock.com/c/womens-clothing/womens-outerwear",
            "subcategory": "Women's Outerwear",
        },
        "womens-suits-blazers": {
            "url": "https://www.overstock.com/c/womens-clothing/womens-suits-blazers",
            "subcategory": "Women's Suits & Blazers",
        },
        "womens-tops": {
            "url": "https://www.overstock.com/c/womens-clothing/womens-tops",
            "subcategory": "Women's Tops",
        },
        "mens-bottoms": {
            "url": "https://www.overstock.com/c/mens-bottoms/mens-pants",
            "subcategory": "Men's Bottoms",
        },
        "mens-suits-blazers": {
            "url": "https://www.overstock.com/c/mens-clothing/mens-suits-blazers",
            "subcategory": "Men's Suits & Blazers",
        },
        "mens-sweatshirts": {
            "url": "https://www.overstock.com/c/mens-activewear/mens-sweatshirts",
            "subcategory": "Men's Sweatshirts",
        },
        "mens-tees": {
            "url": "https://www.overstock.com/c/mens-tops/mens-tees",
            "subcategory": "Men's Tees",
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
        "wedding-rings": {
            "url": "https://www.overstock.com/c/jewelry-watches/wedding-rings",
            "subcategory": "Wedding Rings",
        },
        "bracelets": {
            "url": "https://www.overstock.com/c/bracelets/fashion-bracelets",
            "subcategory": "Bracelets",
        },
        "earrings": {
            "url": "https://www.overstock.com/c/earrings/fashion-earrings",
            "subcategory": "Earrings",
        },
        "necklaces": {
            "url": "https://www.overstock.com/c/necklaces/fashion-necklaces",
            "subcategory": "Necklaces",
        },
        "rings": {
            "url": "https://www.overstock.com/c/rings/fashion-rings",
            "subcategory": "Rings",
        },
    },
    "Storage & Organization": {
        "storage-organization": {
            "url": "https://www.overstock.com/c/storage-organization",
            "subcategory": None,
        },
        "closet-storage": {
            "url": "https://www.overstock.com/c/storage-organization/closet-storage",
            "subcategory": "Closet Storage",
        },
        "decorative-storage": {
            "url": "https://www.overstock.com/c/storage-organization/decorative-storage",
            "subcategory": "Decorative Storage",
        },
        "kitchen-storage": {
            "url": "https://www.overstock.com/c/storage-organization/kitchen-storage",
            "subcategory": "Kitchen Storage",
        },
        "outdoor-storage": {
            "url": "https://www.overstock.com/c/storage-organization/outdoor-storage",
            "subcategory": "Outdoor Storage",
        },
        "storage-furniture": {
            "url": "https://www.overstock.com/c/storage-organization/storage-furniture",
            "subcategory": "Storage Furniture",
        },
        "tool-storage": {
            "url": "https://www.overstock.com/c/storage-organization/tool-storage",
            "subcategory": "Tool Storage",
        },
    },
    "Pet Supplies": {
        "pet-supplies": {
            "url": "https://www.overstock.com/c/pet-supplies",
            "subcategory": None,
        },
    },
    "Designer": {
        "designer": {
            "url": "https://www.overstock.com/c/designer",
            "subcategory": None,
        },
        "designer-accessories": {
            "url": "https://www.overstock.com/c/designer/designer-accessories",
            "subcategory": "Designer Accessories",
        },
        "designer-clothing": {
            "url": "https://www.overstock.com/c/designer/designer-clothing",
            "subcategory": "Designer Clothing",
        },
        "designer-handbags": {
            "url": "https://www.overstock.com/c/designer/designer-handbags",
            "subcategory": "Designer Handbags",
        },
        "designer-home": {
            "url": "https://www.overstock.com/c/designer/designer-home",
            "subcategory": "Designer Home",
        },
        "designer-jewelry": {
            "url": "https://www.overstock.com/c/designer/designer-jewelry",
            "subcategory": "Designer Jewelry",
        },
        "designer-pet-accessories": {
            "url": "https://www.overstock.com/c/designer/designer-pet-accessories",
            "subcategory": "Designer Pet Accessories",
        },
        "designer-shoes": {
            "url": "https://www.overstock.com/c/designer/designer-shoes",
            "subcategory": "Designer Shoes",
        },
    },
    "Gifts": {
        "gifts": {
            "url": "https://www.overstock.com/c/gifts",
            "subcategory": None,
        },
    },
}
