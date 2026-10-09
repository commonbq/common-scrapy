# Ace Hardware category inventory.
#
# Seeded from the homepage mega-menu anchors and verified live on 2026-10-05.
# ``cordless-drills`` is the verified product-bearing leaf; the rest are the
# prominent department/seasonal entry points.
#
# ``category`` is a stable slug taken from the storefront path itself
# (``/departments/tools/power-tools/cordless-drills`` -> ``cordless-drills``), so
# it is unique by construction and survives department renames.
#
# ``category_id`` is the site's own Kibo/Mozu category id where the department page
# exposes one. Department index pages ship that id in
# ``data-mz-preload-routeData.categoryId``; it is filled in for the entries whose
# id was observed and left empty where the department page was not probed.
#
# Note on shape: a department such as ``/departments/tools`` is an index page that
# hydrates ``data-mz-preload-routeData`` (with its recursive ``childrenCategories``)
# but carries no ``data-mz-preload-PLPModel``. The spider follows those children
# down to product-bearing leaves instead of emitting zero items.
from __future__ import annotations


BASE_URL = "https://www.acehardware.com"

ACEHARDWARE_CATEGORIES = {
    "Tools": {
        "cordless-drills": {
            "section": "Power Tools",
            "name": "Cordless Drills",
            "url": "https://www.acehardware.com/departments/tools/power-tools/cordless-drills",
            "category_id": "3002",
        },
        "tools": {
            "section": "Tools",
            "name": "Tools",
            "url": "https://www.acehardware.com/departments/tools",
            "category_id": "28",
        },
    },
    "Outdoor Living": {
        "grills-smokers": {
            "section": "Grills & Smokers",
            "name": "Grills & Smokers",
            "url": "https://www.acehardware.com/departments/grills-smokers",
            "category_id": "253",
        },
        "outdoor-living": {
            "section": "Outdoor Living",
            "name": "Outdoor Living",
            "url": "https://www.acehardware.com/departments/outdoor-living",
            "category_id": "",
        },
    },
    "Lawn & Garden": {
        "outdoor-power-equipment": {
            "section": "Outdoor Power Equipment",
            "name": "Outdoor Power Equipment",
            "url": "https://www.acehardware.com/departments/outdoor-power-equipment",
            "category_id": "",
        },
        "lawn-garden": {
            "section": "Lawn & Garden",
            "name": "Lawn & Garden",
            "url": "https://www.acehardware.com/departments/lawn-and-garden",
            "category_id": "",
        },
    },
    "Paint & Supplies": {
        "paint-supplies": {
            "section": "Paint & Supplies",
            "name": "Paint & Supplies",
            "url": "https://www.acehardware.com/departments/paint-and-supplies",
            "category_id": "",
        },
    },
    "Home & Decor": {
        "home-decor": {
            "section": "Home & Decor",
            "name": "Home & Decor",
            "url": "https://www.acehardware.com/departments/home-and-decor",
            "category_id": "",
        },
        "cleaning-disinfectants": {
            "section": "Cleaning & Disinfectants",
            "name": "Cleaning & Disinfectants",
            "url": "https://www.acehardware.com/departments/home-and-decor/cleaning-and-disinfectants",
            "category_id": "",
        },
    },
    "Climate Control": {
        "heating-cooling": {
            "section": "Heating & Cooling",
            "name": "Heating & Cooling",
            "url": "https://www.acehardware.com/departments/heating-and-cooling",
            "category_id": "",
        },
    },
    "Storage & Organization": {
        "storage-organization": {
            "section": "Storage & Organization",
            "name": "Storage & Organization",
            "url": "https://www.acehardware.com/departments/storage-and-organization",
            "category_id": "",
        },
    },
    "Building Supplies": {
        "building-supplies": {
            "section": "Building Supplies",
            "name": "Building Supplies",
            "url": "https://www.acehardware.com/departments/building-supplies",
            "category_id": "",
        },
    },
    "Hardware": {
        "hardware": {
            "section": "Hardware",
            "name": "Hardware",
            "url": "https://www.acehardware.com/departments/hardware",
            "category_id": "",
        },
    },
    "Electrical": {
        "lighting-electrical": {
            "section": "Lighting & Electrical",
            "name": "Lighting & Electrical",
            "url": "https://www.acehardware.com/departments/lighting-and-electrical",
            "category_id": "",
        },
    },
    "Automotive": {
        "automotive-rv-marine": {
            "section": "Automotive, RV & Marine",
            "name": "Automotive, RV & Marine",
            "url": "https://www.acehardware.com/departments/automotive-rv-and-marine",
            "category_id": "",
        },
    },
    "Plumbing": {
        "plumbing": {
            "section": "Plumbing",
            "name": "Plumbing",
            "url": "https://www.acehardware.com/departments/plumbing",
            "category_id": "",
        },
    },
    "Seasonal": {
        "halloween": {
            "section": "Halloween Decor",
            "name": "Halloween Decor",
            "url": "https://www.acehardware.com/departments/halloween-decor",
            "category_id": "",
        },
        "holiday-decor": {
            "section": "Holiday Decor",
            "name": "Holiday Decor",
            "url": "https://www.acehardware.com/departments/holiday-decor-2",
            "category_id": "",
        },
    },
    "YardRx": {
        "ace-yardrx": {
            "section": "YardRx",
            "name": "Ace YardRx",
            "url": "https://www.acehardware.com/departments/ace-yardrx",
            "category_id": "",
        },
    },
    "Brands": {
        "brands": {
            "section": "Brands",
            "name": "Brands",
            "url": "https://www.acehardware.com/departments/brands-category",
            "category_id": "",
        },
    },
}
