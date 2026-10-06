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

ACEHARDWARE_CATEGORIES = [
    {
        "category": "cordless-drills",
        "department": "Tools",
        "section": "Power Tools",
        "name": "Cordless Drills",
        "url": "https://www.acehardware.com/departments/tools/power-tools/cordless-drills",
        "category_id": "3002",
    },
    {
        "category": "grills-smokers",
        "department": "Outdoor Living",
        "section": "Grills & Smokers",
        "name": "Grills & Smokers",
        "url": "https://www.acehardware.com/departments/grills-smokers",
        "category_id": "253",
    },
    {
        "category": "outdoor-power-equipment",
        "department": "Lawn & Garden",
        "section": "Outdoor Power Equipment",
        "name": "Outdoor Power Equipment",
        "url": "https://www.acehardware.com/departments/outdoor-power-equipment",
        "category_id": "",
    },
    {
        "category": "outdoor-living",
        "department": "Outdoor Living",
        "section": "Outdoor Living",
        "name": "Outdoor Living",
        "url": "https://www.acehardware.com/departments/outdoor-living",
        "category_id": "",
    },
    {
        "category": "lawn-garden",
        "department": "Lawn & Garden",
        "section": "Lawn & Garden",
        "name": "Lawn & Garden",
        "url": "https://www.acehardware.com/departments/lawn-and-garden",
        "category_id": "",
    },
    {
        "category": "paint-supplies",
        "department": "Paint & Supplies",
        "section": "Paint & Supplies",
        "name": "Paint & Supplies",
        "url": "https://www.acehardware.com/departments/paint-and-supplies",
        "category_id": "",
    },
    {
        "category": "tools",
        "department": "Tools",
        "section": "Tools",
        "name": "Tools",
        "url": "https://www.acehardware.com/departments/tools",
        "category_id": "28",
    },
    {
        "category": "home-decor",
        "department": "Home & Decor",
        "section": "Home & Decor",
        "name": "Home & Decor",
        "url": "https://www.acehardware.com/departments/home-and-decor",
        "category_id": "",
    },
    {
        "category": "heating-cooling",
        "department": "Climate Control",
        "section": "Heating & Cooling",
        "name": "Heating & Cooling",
        "url": "https://www.acehardware.com/departments/heating-and-cooling",
        "category_id": "",
    },
    {
        "category": "storage-organization",
        "department": "Storage & Organization",
        "section": "Storage & Organization",
        "name": "Storage & Organization",
        "url": "https://www.acehardware.com/departments/storage-and-organization",
        "category_id": "",
    },
    {
        "category": "building-supplies",
        "department": "Building Supplies",
        "section": "Building Supplies",
        "name": "Building Supplies",
        "url": "https://www.acehardware.com/departments/building-supplies",
        "category_id": "",
    },
    {
        "category": "hardware",
        "department": "Hardware",
        "section": "Hardware",
        "name": "Hardware",
        "url": "https://www.acehardware.com/departments/hardware",
        "category_id": "",
    },
    {
        "category": "lighting-electrical",
        "department": "Electrical",
        "section": "Lighting & Electrical",
        "name": "Lighting & Electrical",
        "url": "https://www.acehardware.com/departments/lighting-and-electrical",
        "category_id": "",
    },
    {
        "category": "automotive-rv-marine",
        "department": "Automotive",
        "section": "Automotive, RV & Marine",
        "name": "Automotive, RV & Marine",
        "url": "https://www.acehardware.com/departments/automotive-rv-and-marine",
        "category_id": "",
    },
    {
        "category": "plumbing",
        "department": "Plumbing",
        "section": "Plumbing",
        "name": "Plumbing",
        "url": "https://www.acehardware.com/departments/plumbing",
        "category_id": "",
    },
    {
        "category": "cleaning-disinfectants",
        "department": "Home & Decor",
        "section": "Cleaning & Disinfectants",
        "name": "Cleaning & Disinfectants",
        "url": "https://www.acehardware.com/departments/home-and-decor/cleaning-and-disinfectants",
        "category_id": "",
    },
    {
        "category": "halloween",
        "department": "Seasonal",
        "section": "Halloween Decor",
        "name": "Halloween Decor",
        "url": "https://www.acehardware.com/departments/halloween-decor",
        "category_id": "",
    },
    {
        "category": "holiday-decor",
        "department": "Seasonal",
        "section": "Holiday Decor",
        "name": "Holiday Decor",
        "url": "https://www.acehardware.com/departments/holiday-decor-2",
        "category_id": "",
    },
    {
        "category": "ace-yardrx",
        "department": "YardRx",
        "section": "YardRx",
        "name": "Ace YardRx",
        "url": "https://www.acehardware.com/departments/ace-yardrx",
        "category_id": "",
    },
    {
        "category": "brands",
        "department": "Brands",
        "section": "Brands",
        "name": "Brands",
        "url": "https://www.acehardware.com/departments/brands-category",
        "category_id": "",
    },
]
