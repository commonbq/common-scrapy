"""Decathlon US category inventory captured from the live primary navigation on 2026-10-15.

Every collection below is a real ``/collections/<handle>/products.json`` endpoint that
returned HTTP 200 with at least one product when checked the same day (``shop-all`` is the
top-level All Sports collection). Leaf keys are the collection handles; they are globally
unique across the groups (a handle keeps its first primary-nav placement), so DAG task ids
and GCS output paths cannot collide."""

DECATHLON_CATEGORIES = {
    "all-sports": {
        "shop-all": {
            "url": "https://www.decathlon.com/collections/shop-all",
            "department": "all-sports",
            "category": "shop-all",
        },
        "camp-hike": {
            "url": "https://www.decathlon.com/collections/camp-hike",
            "department": "all-sports",
            "category": "camp-hike",
        },
        "backpacks-bags": {
            "url": "https://www.decathlon.com/collections/backpacks-bags",
            "department": "all-sports",
            "category": "backpacks-bags",
        },
        "hiking-jackets": {
            "url": "https://www.decathlon.com/collections/hiking-jackets",
            "department": "all-sports",
            "category": "hiking-jackets",
        },
        "hiking-clothing": {
            "url": "https://www.decathlon.com/collections/hiking-clothing",
            "department": "all-sports",
            "category": "hiking-clothing",
        },
        "base-layers-thermal-underwear": {
            "url": "https://www.decathlon.com/collections/base-layers-thermal-underwear",
            "department": "all-sports",
            "category": "base-layers-thermal-underwear",
        },
        "footwear": {
            "url": "https://www.decathlon.com/collections/footwear",
            "department": "all-sports",
            "category": "footwear",
        },
        "hiking-camp-accessories": {
            "url": "https://www.decathlon.com/collections/hiking-camp-accessories",
            "department": "all-sports",
            "category": "hiking-camp-accessories",
        },
        "camp-ready-all-your-outdoor-essentials": {
            "url": "https://www.decathlon.com/collections/camp-ready-all-your-outdoor-essentials",
            "department": "all-sports",
            "category": "camp-ready-all-your-outdoor-essentials",
        },
        "camping-tents": {
            "url": "https://www.decathlon.com/collections/camping-tents",
            "department": "all-sports",
            "category": "camping-tents",
        },
        "sleeping": {
            "url": "https://www.decathlon.com/collections/sleeping",
            "department": "all-sports",
            "category": "sleeping",
        },
        "kitchen": {
            "url": "https://www.decathlon.com/collections/kitchen",
            "department": "all-sports",
            "category": "kitchen",
        },
        "camp-furniture": {
            "url": "https://www.decathlon.com/collections/camp-furniture",
            "department": "all-sports",
            "category": "camp-furniture",
        },
        "hydration": {
            "url": "https://www.decathlon.com/collections/hydration",
            "department": "all-sports",
            "category": "hydration",
        },
        "running": {
            "url": "https://www.decathlon.com/collections/running",
            "department": "all-sports",
            "category": "running",
        },
        "kiprun-shoes": {
            "url": "https://www.decathlon.com/collections/kiprun-shoes",
            "department": "all-sports",
            "category": "kiprun-shoes",
        },
        "running-clothing": {
            "url": "https://www.decathlon.com/collections/running-clothing",
            "department": "all-sports",
            "category": "running-clothing",
        },
        "running-belts-hydration-vests": {
            "url": "https://www.decathlon.com/collections/running-belts-hydration-vests",
            "department": "all-sports",
            "category": "running-belts-hydration-vests",
        },
        "bike": {
            "url": "https://www.decathlon.com/collections/bike",
            "department": "all-sports",
            "category": "bike",
        },
        "home-trainers": {
            "url": "https://www.decathlon.com/collections/home-trainers",
            "department": "all-sports",
            "category": "home-trainers",
        },
        "cycling-clothing": {
            "url": "https://www.decathlon.com/collections/cycling-clothing",
            "department": "all-sports",
            "category": "cycling-clothing",
        },
        "cycling-shoes": {
            "url": "https://www.decathlon.com/collections/cycling-shoes",
            "department": "all-sports",
            "category": "cycling-shoes",
        },
        "cycling-gloves": {
            "url": "https://www.decathlon.com/collections/cycling-gloves",
            "department": "all-sports",
            "category": "cycling-gloves",
        },
        "snow-ski": {
            "url": "https://www.decathlon.com/collections/snow-ski",
            "department": "all-sports",
            "category": "snow-ski",
        },
        "jackets-outerwear": {
            "url": "https://www.decathlon.com/collections/jackets-outerwear",
            "department": "all-sports",
            "category": "jackets-outerwear",
        },
        "hiking-fleeces-mid-layers": {
            "url": "https://www.decathlon.com/collections/hiking-fleeces-mid-layers",
            "department": "all-sports",
            "category": "hiking-fleeces-mid-layers",
        },
        "ski-beanies-gloves-socks": {
            "url": "https://www.decathlon.com/collections/ski-beanies-gloves-socks",
            "department": "all-sports",
            "category": "ski-beanies-gloves-socks",
        },
        "snow-boots": {
            "url": "https://www.decathlon.com/collections/snow-boots",
            "department": "all-sports",
            "category": "snow-boots",
        },
        "mens": {
            "url": "https://www.decathlon.com/collections/mens",
            "department": "all-sports",
            "category": "mens",
        },
    },
    "men": {
        "mens-jackets": {
            "url": "https://www.decathlon.com/collections/mens-jackets",
            "department": "men",
            "category": "mens-jackets",
        },
        "mens-down-jackets": {
            "url": "https://www.decathlon.com/collections/mens-down-jackets",
            "department": "men",
            "category": "mens-down-jackets",
        },
        "mens-rain-snow-jacket": {
            "url": "https://www.decathlon.com/collections/mens-rain-snow-jacket",
            "department": "men",
            "category": "mens-rain-snow-jacket",
        },
        "mens-fleeces-mid-layers": {
            "url": "https://www.decathlon.com/collections/mens-fleeces-mid-layers",
            "department": "men",
            "category": "mens-fleeces-mid-layers",
        },
        "mens-windbreaker-jackets": {
            "url": "https://www.decathlon.com/collections/mens-windbreaker-jackets",
            "department": "men",
            "category": "mens-windbreaker-jackets",
        },
        "mens-winter-jackets-coats": {
            "url": "https://www.decathlon.com/collections/mens-winter-jackets-coats",
            "department": "men",
            "category": "mens-winter-jackets-coats",
        },
        "mens-tops": {
            "url": "https://www.decathlon.com/collections/mens-tops",
            "department": "men",
            "category": "mens-tops",
        },
        "mens-shirts": {
            "url": "https://www.decathlon.com/collections/mens-shirts",
            "department": "men",
            "category": "mens-shirts",
        },
        "mens-long-sleeved-t-shirts": {
            "url": "https://www.decathlon.com/collections/mens-long-sleeved-t-shirts",
            "department": "men",
            "category": "mens-long-sleeved-t-shirts",
        },
        "mens-pants-shorts": {
            "url": "https://www.decathlon.com/collections/mens-pants-shorts",
            "department": "men",
            "category": "mens-pants-shorts",
        },
        "mens-pants": {
            "url": "https://www.decathlon.com/collections/mens-pants",
            "department": "men",
            "category": "mens-pants",
        },
        "mens-shorts": {
            "url": "https://www.decathlon.com/collections/mens-shorts",
            "department": "men",
            "category": "mens-shorts",
        },
        "mens-base-layers": {
            "url": "https://www.decathlon.com/collections/mens-base-layers",
            "department": "men",
            "category": "mens-base-layers",
        },
        "mens-merino-wool-apparel": {
            "url": "https://www.decathlon.com/collections/mens-merino-wool-apparel",
            "department": "men",
            "category": "mens-merino-wool-apparel",
        },
        "mens-hats-beanies": {
            "url": "https://www.decathlon.com/collections/mens-hats-beanies",
            "department": "men",
            "category": "mens-hats-beanies",
        },
        "mens-socks": {
            "url": "https://www.decathlon.com/collections/mens-socks",
            "department": "men",
            "category": "mens-socks",
        },
        "mens-footwear": {
            "url": "https://www.decathlon.com/collections/mens-footwear",
            "department": "men",
            "category": "mens-footwear",
        },
        "mens-deals": {
            "url": "https://www.decathlon.com/collections/mens-deals",
            "department": "men",
            "category": "mens-deals",
        },
        "womens": {
            "url": "https://www.decathlon.com/collections/womens",
            "department": "men",
            "category": "womens",
        },
    },
    "women": {
        "womens-jackets": {
            "url": "https://www.decathlon.com/collections/womens-jackets",
            "department": "women",
            "category": "womens-jackets",
        },
        "womens-down-jackets": {
            "url": "https://www.decathlon.com/collections/womens-down-jackets",
            "department": "women",
            "category": "womens-down-jackets",
        },
        "womens-rain-snow-jacket": {
            "url": "https://www.decathlon.com/collections/womens-rain-snow-jacket",
            "department": "women",
            "category": "womens-rain-snow-jacket",
        },
        "womens-fleeces-mid-layers": {
            "url": "https://www.decathlon.com/collections/womens-fleeces-mid-layers",
            "department": "women",
            "category": "womens-fleeces-mid-layers",
        },
        "womens-windbreaker-jackets": {
            "url": "https://www.decathlon.com/collections/womens-windbreaker-jackets",
            "department": "women",
            "category": "womens-windbreaker-jackets",
        },
        "womens-winter-jackets": {
            "url": "https://www.decathlon.com/collections/womens-winter-jackets",
            "department": "women",
            "category": "womens-winter-jackets",
        },
        "womens-tops": {
            "url": "https://www.decathlon.com/collections/womens-tops",
            "department": "women",
            "category": "womens-tops",
        },
        "womens-shirts": {
            "url": "https://www.decathlon.com/collections/womens-shirts",
            "department": "women",
            "category": "womens-shirts",
        },
        "womens-bottoms": {
            "url": "https://www.decathlon.com/collections/womens-bottoms",
            "department": "women",
            "category": "womens-bottoms",
        },
        "womens-pants-leggings": {
            "url": "https://www.decathlon.com/collections/womens-pants-leggings",
            "department": "women",
            "category": "womens-pants-leggings",
        },
        "womens-shorts-skirts": {
            "url": "https://www.decathlon.com/collections/womens-shorts-skirts",
            "department": "women",
            "category": "womens-shorts-skirts",
        },
        "womens-base-layers": {
            "url": "https://www.decathlon.com/collections/womens-base-layers",
            "department": "women",
            "category": "womens-base-layers",
        },
        "womens-merino-wool": {
            "url": "https://www.decathlon.com/collections/womens-merino-wool",
            "department": "women",
            "category": "womens-merino-wool",
        },
        "womens-hat-beanies": {
            "url": "https://www.decathlon.com/collections/womens-hat-beanies",
            "department": "women",
            "category": "womens-hat-beanies",
        },
        "womens-gloves": {
            "url": "https://www.decathlon.com/collections/womens-gloves",
            "department": "women",
            "category": "womens-gloves",
        },
        "womens-footwear": {
            "url": "https://www.decathlon.com/collections/womens-footwear",
            "department": "women",
            "category": "womens-footwear",
        },
        "womens-deals": {
            "url": "https://www.decathlon.com/collections/womens-deals",
            "department": "women",
            "category": "womens-deals",
        },
        "all-kids-outdoor-gear": {
            "url": "https://www.decathlon.com/collections/all-kids-outdoor-gear",
            "department": "women",
            "category": "all-kids-outdoor-gear",
        },
    },
    "kids-outdoor": {
        "kids-backpacks": {
            "url": "https://www.decathlon.com/collections/kids-backpacks",
            "department": "kids-outdoor",
            "category": "kids-backpacks",
        },
        "kids-outdoor-clothing": {
            "url": "https://www.decathlon.com/collections/kids-outdoor-clothing",
            "department": "kids-outdoor",
            "category": "kids-outdoor-clothing",
        },
        "kids-outdoor-footwear": {
            "url": "https://www.decathlon.com/collections/kids-outdoor-footwear",
            "department": "kids-outdoor",
            "category": "kids-outdoor-footwear",
        },
        "rain-snow-jackets": {
            "url": "https://www.decathlon.com/collections/rain-snow-jackets",
            "department": "kids-outdoor",
            "category": "rain-snow-jackets",
        },
        "all-hiking-backpacks": {
            "url": "https://www.decathlon.com/collections/all-hiking-backpacks",
            "department": "kids-outdoor",
            "category": "all-hiking-backpacks",
        },
        "duffel-bags": {
            "url": "https://www.decathlon.com/collections/duffel-bags",
            "department": "kids-outdoor",
            "category": "duffel-bags",
        },
        "best-sellers": {
            "url": "https://www.decathlon.com/collections/best-sellers",
            "department": "kids-outdoor",
            "category": "best-sellers",
        },
        "new-arrivals": {
            "url": "https://www.decathlon.com/collections/new-arrivals",
            "department": "kids-outdoor",
            "category": "new-arrivals",
        },
    },
}
