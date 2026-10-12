"""Best Buy's complete top-level department inventory.

Source: the "Shop electronics in every department" section on Best Buy's
electronics landing page, checked 2026-10-12.  Existing crawl-target names are
retained where they already select a useful product listing.
"""

BESTBUY_CATEGORIES = {
    "appliances": {
        "appliances": "https://www.bestbuy.com/site/electronics/home-appliances/abcat0900000.c?id=abcat0900000",
    },
    "tv-home-theater": {
        "tvs": "https://www.bestbuy.com/site/tv-home-theater/televisions/abcat0101001.c?id=abcat0101001",
    },
    "computers-tablets": {
        "laptops": "https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000",
        "monitors": "https://www.bestbuy.com/site/computer-cards-components/monitors/abcat0509000.c?id=abcat0509000",
    },
    "cameras-camcorders": {
        "cameras-camcorders": "https://www.bestbuy.com/site/electronics/cameras-camcorders/abcat0400000.c?id=abcat0400000",
    },
    "cell-phones": {
        "cell-phones": "https://www.bestbuy.com/site/cell-phones/all-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005",
    },
    "audio": {
        "headphones": "https://www.bestbuy.com/site/headphones/all-headphones/abcat0204000.c?id=abcat0204000",
    },
    "video-games": {
        "video-games": "https://www.bestbuy.com/site/electronics/video-games/abcat0700000.c?id=abcat0700000",
    },
    "car-electronics-gps": {
        "car-electronics-gps": "https://www.bestbuy.com/site/electronics/car-audio-gps/abcat0300000.c?id=abcat0300000",
    },
    "wearable-technology": {
        "wearable-technology": "https://www.bestbuy.com/site/electronics/wearable-technology/pcmcat332000050000.c?id=pcmcat332000050000",
    },
    "health-wellness-personal-care": {
        "health-wellness-personal-care": "https://www.bestbuy.com/site/electronics/health-wellness/pcmcat242800050021.c?id=pcmcat242800050021",
    },
    "home-furniture-office": {
        "home-furniture-office": "https://www.bestbuy.com/site/electronics/home/pcmcat312300050015.c?id=pcmcat312300050015",
    },
    "smart-home-security-wifi": {
        "smart-home-security-wifi": "https://www.bestbuy.com/site/electronics/home-security-safety/pcmcat254000050002.c?id=pcmcat254000050002",
    },
    "toys-games-crafts": {
        "toys-games-crafts": "https://www.bestbuy.com/site/electronics/toys-games-crafts/pcmcat252700050006.c?id=pcmcat252700050006",
    },
    "best-buy-outlet": {
        "best-buy-outlet": "https://www.bestbuy.com/site/electronics/outlet-refurbished-clearance/pcmcat142300050026.c?id=pcmcat142300050026",
    },
}
