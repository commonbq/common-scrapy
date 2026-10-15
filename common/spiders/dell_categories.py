"""Dell US product-listing entry points.

Source: the live Dell Technologies US header mega-navigation on
https://www.dell.com/en-us (captured 2026-10-15).  Every leaf below is a
first-party product-listing page (``scr`` / ``sac`` / ``ar`` / ``dc`` route)
that renders the ``#ps-wrapper`` Product Stack bootstrap the spider reads.
Product-detail (``spd``/``apd``), landing (``lp``), and category-hub (``sc``)
routes and marketing pages are intentionally excluded.

The mapping keeps Dell's own top-level navigation groups as departments so the
Airflow DagBag schedules one task per leaf and GCS output paths cannot clash.
"""


BASE_URL = "https://www.dell.com"

DELL_CATEGORIES = {
    "laptop-computers": {
        "view-all-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop",
            "department": "laptop-computers",
            "category": "view-all-laptops",
        },
        "gaming-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/gaming",
            "department": "laptop-computers",
            "category": "gaming-laptops",
        },
        "alienware-laptops": {
            "url": "https://www.dell.com/en-us/shop/dell-laptops/scr/laptop/appref=alienware-product-line",
            "department": "laptop-computers",
            "category": "alienware-laptops",
        },
        "dell-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=dell-product-line",
            "department": "laptop-computers",
            "category": "dell-laptops",
        },
        "xps-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=xps-product-line",
            "department": "laptop-computers",
            "category": "xps-laptops",
        },
        "dell-pro-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=dell-pro-product-line",
            "department": "laptop-computers",
            "category": "dell-pro-laptops",
        },
        "dell-pro-essential-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=dell-pro-essential-product-line",
            "department": "laptop-computers",
            "category": "dell-pro-essential-laptops",
        },
        "precision-mobile-workstations": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=precision-product-line",
            "department": "laptop-computers",
            "category": "precision-mobile-workstations",
        },
        "dell-pro-rugged-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=dell-pro-rugged-product-line",
            "department": "laptop-computers",
            "category": "dell-pro-rugged-laptops",
        },
        "dell-pro-education-laptops": {
            "url": "https://www.dell.com/en-us/shop/dell-laptops/scr/laptop/appref=dell-pro-education-product-line",
            "department": "laptop-computers",
            "category": "dell-pro-education-laptops",
        },
        "chromebook-laptops": {
            "url": "https://www.dell.com/en-us/shop/laptop-computers/scr/laptop/appref=dell-chromebook-product-line",
            "department": "laptop-computers",
            "category": "chromebook-laptops",
        },
    },
    "desktop-computers": {
        "view-all-desktops": {
            "url": "https://www.dell.com/en-us/shop/desktop-computers/scr/desktop",
            "department": "desktop-computers",
            "category": "view-all-desktops",
        },
        "gaming-desktops": {
            "url": "https://www.dell.com/en-us/shop/desktop-computers/scr/desktop/gaming",
            "department": "desktop-computers",
            "category": "gaming-desktops",
        },
        "alienware-desktops": {
            "url": "https://www.dell.com/en-us/shop/dell-desktops/scr/desktop/appref=alienware-product-line",
            "department": "desktop-computers",
            "category": "alienware-desktops",
        },
        "dell-desktops": {
            "url": "https://www.dell.com/en-us/shop/desktop-computers/scr/desktop/appref=dell-product-line",
            "department": "desktop-computers",
            "category": "dell-desktops",
        },
        "dell-pro-desktops": {
            "url": "https://www.dell.com/en-us/shop/desktop-computers/scr/desktop/appref=dell-pro-product-line",
            "department": "desktop-computers",
            "category": "dell-pro-desktops",
        },
        "dell-pro-essential-desktops": {
            "url": "https://www.dell.com/en-us/shop/desktop-computers/scr/desktop/appref=dell-pro-essential-product-line",
            "department": "desktop-computers",
            "category": "dell-pro-essential-desktops",
        },
        "precision-fixed-workstations": {
            "url": "https://www.dell.com/en-us/shop/desktop-computers/scr/desktop/appref=precision-product-line",
            "department": "desktop-computers",
            "category": "precision-fixed-workstations",
        },
    },
    "computer-monitors": {
        "view-all-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/all-monitors",
            "department": "computer-monitors",
            "category": "view-all-monitors",
        },
        "gaming-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/gaming-monitors",
            "department": "computer-monitors",
            "category": "gaming-monitors",
        },
        "ultrawide-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/all-monitors/appref=ultrawide-features",
            "department": "computer-monitors",
            "category": "ultrawide-monitors",
        },
        "curved-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/all-monitors/appref=curved-features",
            "department": "computer-monitors",
            "category": "curved-monitors",
        },
        "everyday-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/everyday-monitors",
            "department": "computer-monitors",
            "category": "everyday-monitors",
        },
        "professional-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/professional-monitors",
            "department": "computer-monitors",
            "category": "professional-monitors",
        },
        "ultrasharp-monitors": {
            "url": "https://www.dell.com/en-us/shop/computer-monitors/sac/monitors/performance-monitors",
            "department": "computer-monitors",
            "category": "ultrasharp-monitors",
        },
    },
    "monitor-accessories": {
        "monitor-webcams": {
            "url": "https://www.dell.com/en-us/shop/monitor-accessories/ar/monitor-webcams",
            "department": "monitor-accessories",
            "category": "monitor-webcams",
        },
        "privacy-screens": {
            "url": "https://www.dell.com/en-us/shop/monitor-accessories/ar/privacy-anti-glare-screens",
            "department": "monitor-accessories",
            "category": "privacy-screens",
        },
        "monitor-speakers": {
            "url": "https://www.dell.com/en-us/shop/monitor-accessories/ar/monitor-speakers",
            "department": "monitor-accessories",
            "category": "monitor-speakers",
        },
        "monitor-cables": {
            "url": "https://www.dell.com/en-us/shop/monitor-accessories/ar/monitor-cables",
            "department": "monitor-accessories",
            "category": "monitor-cables",
        },
    },
    "pc-accessories": {
        "gaming-mouse": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-mouse",
            "department": "pc-accessories",
            "category": "gaming-mouse",
        },
        "gaming-keyboards": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-keyboards",
            "department": "pc-accessories",
            "category": "gaming-keyboards",
        },
        "gaming-keyboards-mice": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-keyboards-mice",
            "department": "pc-accessories",
            "category": "gaming-keyboards-mice",
        },
        "gaming-headsets": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-headphones-headsets",
            "department": "pc-accessories",
            "category": "gaming-headsets",
        },
        "gaming-furniture": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-furniture",
            "department": "pc-accessories",
            "category": "gaming-furniture",
        },
        "video-games": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/video-games",
            "department": "pc-accessories",
            "category": "video-games",
        },
        "gaming-consoles": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-consoles",
            "department": "pc-accessories",
            "category": "gaming-consoles",
        },
        "gaming-controllers": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/gaming-controllers",
            "department": "pc-accessories",
            "category": "gaming-controllers",
        },
        "computer-speakers": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/computer-speakers",
            "department": "pc-accessories",
            "category": "computer-speakers",
        },
        "microphones": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/microphones",
            "department": "pc-accessories",
            "category": "microphones",
        },
        "backpacks": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/backpacks",
            "department": "pc-accessories",
            "category": "backpacks",
        },
        "printers": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/printers",
            "department": "pc-accessories",
            "category": "printers",
        },
        "docking-stations": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/docking-stations-accessories",
            "department": "pc-accessories",
            "category": "docking-stations",
        },
        "keyboards-mice": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/keyboards-mice",
            "department": "pc-accessories",
            "category": "keyboards-mice",
        },
        "audio": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/audio",
            "department": "pc-accessories",
            "category": "audio",
        },
        "webcams": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/camera-webcams",
            "department": "pc-accessories",
            "category": "webcams",
        },
        "laptop-bags-cases": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/laptop-bags-cases",
            "department": "pc-accessories",
            "category": "laptop-bags-cases",
        },
        "printers-scanners": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/printers-scanners",
            "department": "pc-accessories",
            "category": "printers-scanners",
        },
        "storage-drives": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/storage-drives-media",
            "department": "pc-accessories",
            "category": "storage-drives",
        },
        "cables-adapters": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/cables-adapters",
            "department": "pc-accessories",
            "category": "cables-adapters",
        },
        "power-adapters": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/power-adapters",
            "department": "pc-accessories",
            "category": "power-adapters",
        },
        "wifi-networking": {
            "url": "https://www.dell.com/en-us/shop/pc-accessories/ar/wifi-networking",
            "department": "pc-accessories",
            "category": "wifi-networking",
        },
    },
    "electronics": {
        "smart-watches": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/smart-watches",
            "department": "electronics",
            "category": "smart-watches",
        },
        "cameras": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/cameras",
            "department": "electronics",
            "category": "cameras",
        },
        "camera-lenses": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/camera-lenses",
            "department": "electronics",
            "category": "camera-lenses",
        },
        "portable-speakers": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/portable-speakers",
            "department": "electronics",
            "category": "portable-speakers",
        },
        "portable-projectors": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/portable-projectors",
            "department": "electronics",
            "category": "portable-projectors",
        },
        "home-audio": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/home-audio",
            "department": "electronics",
            "category": "home-audio",
        },
        "camera-photo-video": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/camera-photo-video",
            "department": "electronics",
            "category": "camera-photo-video",
        },
        "smart-home": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/smart-home",
            "department": "electronics",
            "category": "smart-home",
        },
        "wearables": {
            "url": "https://www.dell.com/en-us/shop/electronics/ar/wearables",
            "department": "electronics",
            "category": "wearables",
        },
    },
    "deals": {
        "all-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc",
            "department": "deals",
            "category": "all-deals",
        },
        "laptop-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc/laptop-deals",
            "department": "deals",
            "category": "laptop-deals",
        },
        "desktop-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc/desktop-deals",
            "department": "deals",
            "category": "desktop-deals",
        },
        "gaming-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc/gaming-pc-deals",
            "department": "deals",
            "category": "gaming-deals",
        },
        "business-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc/business-deals",
            "department": "deals",
            "category": "business-deals",
        },
        "monitor-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc/monitor-deals",
            "department": "deals",
            "category": "monitor-deals",
        },
        "pc-accessories-deals": {
            "url": "https://www.dell.com/en-us/shop/deals/dc/pc-accessories-deals",
            "department": "deals",
            "category": "pc-accessories-deals",
        },
    },
}
