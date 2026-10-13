"""Patagonia storefront navigation categories used by ``patagonia_listing``.

Snapshot of ``clientDataModel.primaryNavigation`` from the US homepage on
2026-10-12. Only ``/shop/`` destinations are crawl targets. Repeated links in
featured collections are assigned to their first navigation group so every leaf
and output path remains unique. Existing public category aliases such as
``packs-gear``, ``fly-fishing`` and ``sale`` are retained.
"""

PATAGONIA_CATEGORIES = {
    "nav-new-featured": {
        "new-arrivals": {
            "url": "https://www.patagonia.com/shop/new-arrivals",
            "name": "New Arrivals",
            "nav_id": "collections-new-arrivals",
        },
        "womens-new-arrivals": {
            "url": "https://www.patagonia.com/shop/womens/new-arrivals",
            "name": "Women's",
            "nav_id": "collections-new-arrivals-womens-link",
        },
        "mens-new-arrivals": {
            "url": "https://www.patagonia.com/shop/mens/new-arrivals",
            "name": "Men's",
            "nav_id": "collections-new-arrivals-mens-link",
        },
        "kids-baby-new-arrivals": {
            "url": "https://www.patagonia.com/shop/kids-baby/new-arrivals",
            "name": "Kids' & Baby",
            "nav_id": "collections-new-arrivals-kids-baby-link",
        },
        "gear-new-arrivals": {
            "url": "https://www.patagonia.com/shop/gear/new-arrivals",
            "name": "Packs & Gear",
            "nav_id": "collections-new-arrivals-packs-gear-link",
        },
        "favorites": {
            "url": "https://www.patagonia.com/shop/favorites",
            "name": "Patagonia Favorites",
            "nav_id": "nav-patagonia-favorites",
        },
        "favorites-nano-puff-insulation": {
            "url": "https://www.patagonia.com/shop/favorites/nano-puff-insulation",
            "name": "Nano Puff® Insulation",
            "nav_id": "collections-nano-puff-insulation",
        },
        "favorites-down-sweater-jackets-vests": {
            "url": "https://www.patagonia.com/shop/favorites/down-sweater-jackets-vests",
            "name": "Down Sweater™ Insulation",
            "nav_id": "collections-down-sweater",
        },
        "favorites-nano-air": {
            "url": "https://www.patagonia.com/shop/favorites/nano-air",
            "name": "Nano-Air® Insulation",
            "nav_id": "collections-nano-air",
        },
        "favorites-regulator-fleece": {
            "url": "https://www.patagonia.com/shop/favorites/regulator-fleece",
            "name": "Regulator® Fleece",
            "nav_id": "collections-regulator",
        },
        "favorites-retro-x-fleece": {
            "url": "https://www.patagonia.com/shop/favorites/retro-x-fleece",
            "name": "Retro-X® Fleece",
            "nav_id": "collections-retro-x",
        },
        "favorites-better-sweater-fleece": {
            "url": "https://www.patagonia.com/shop/favorites/better-sweater-fleece",
            "name": "Better Sweater® Fleece",
            "nav_id": "collection-better-sweaters",
        },
        "favorites-snap-t-fleece": {
            "url": "https://www.patagonia.com/shop/favorites/snap-t-fleece",
            "name": "Snap-T® Fleece",
            "nav_id": "collections-snap-t",
        },
        "gear-bags-black-hole": {
            "url": "https://www.patagonia.com/shop/gear/bags/black-hole",
            "name": "Black Hole® Bags",
            "nav_id": "luggage-black-hole-bags",
        },
        "favorites-capilene-cool-tech-tees": {
            "url": "https://www.patagonia.com/shop/favorites/capilene-cool-tech-tees",
            "name": "Capilene® Cool Tech Tees",
            "nav_id": "collections-cap-cool",
        },
        "favorites-baggies-shorts": {
            "url": "https://www.patagonia.com/shop/favorites/baggies-shorts",
            "name": "Baggies™ Shorts",
            "nav_id": "collections-baggies",
        },
        "category-jackets": {
            "url": "https://www.patagonia.com/shop/category/jackets",
            "name": "Jackets & Vests",
            "nav_id": "jackets",
        },
        "category-fleece": {
            "url": "https://www.patagonia.com/shop/category/fleece",
            "name": "Fleece",
            "nav_id": "fleece",
        },
        "category-sweatshirts-hoodies": {
            "url": "https://www.patagonia.com/shop/category/sweatshirts-hoodies",
            "name": "Sweatshirts & Hoodies",
            "nav_id": "sweatshirts-hoodies",
        },
        "category-sweaters": {
            "url": "https://www.patagonia.com/shop/category/sweaters",
            "name": "Sweaters",
            "nav_id": "sweaters",
        },
        "category-shirts": {
            "url": "https://www.patagonia.com/shop/category/shirts",
            "name": "Shirts",
            "nav_id": "shirts",
        },
        "category-t-shirts": {
            "url": "https://www.patagonia.com/shop/category/t-shirts",
            "name": "T-Shirts",
            "nav_id": "t-shirts",
        },
        "category-pants": {
            "url": "https://www.patagonia.com/shop/category/pants",
            "name": "Pants & Jeans",
            "nav_id": "pants-jeans",
        },
        "category-shorts": {
            "url": "https://www.patagonia.com/shop/category/shorts",
            "name": "Shorts",
            "nav_id": "shorts",
        },
        "category-boardshorts": {
            "url": "https://www.patagonia.com/shop/category/boardshorts",
            "name": "Boardshorts",
            "nav_id": "board-shorts",
        },
        "category-baselayers": {
            "url": "https://www.patagonia.com/shop/category/baselayers",
            "name": "Baselayers",
            "nav_id": "baselayers",
        },
        "category-hats-accessories": {
            "url": "https://www.patagonia.com/shop/category/hats-accessories",
            "name": "Hats & Accessories",
            "nav_id": "hats-accessories",
        },
        "category-socks-underwear": {
            "url": "https://www.patagonia.com/shop/category/socks-underwear",
            "name": "Socks & Underwear",
            "nav_id": "socks-underwear",
        },
        "wetsuits": {
            "url": "https://www.patagonia.com/shop/gear/wetsuits",
            "name": "Wetsuits",
            "nav_id": "nav-shop-by-category-wetsuits-link",
        },
        "gear-waders": {
            "url": "https://www.patagonia.com/shop/gear/waders",
            "name": "Waders",
            "nav_id": "nav-shop-by-category-waders-link",
        },
        "sport-workwear": {
            "url": "https://www.patagonia.com/shop/sport/workwear",
            "name": "Workwear",
            "nav_id": "nav-shop-by-category-workwear-link",
        },
        "sale": {
            "url": "https://www.patagonia.com/shop/web-specials",
            "name": "Web Specials",
            "nav_id": "web-specials",
        },
        "web-specials-womens": {
            "url": "https://www.patagonia.com/shop/web-specials/womens",
            "name": "Women's",
            "nav_id": "web-specials-womens",
        },
        "web-specials-mens": {
            "url": "https://www.patagonia.com/shop/web-specials/mens",
            "name": "Men's",
            "nav_id": "web-specials-mens",
        },
        "web-specials-kids-baby": {
            "url": "https://www.patagonia.com/shop/web-specials/kids-baby",
            "name": "Kids' & Baby",
            "nav_id": "web-specials-kids",
        },
        "web-specials-gear": {
            "url": "https://www.patagonia.com/shop/web-specials/gear",
            "name": "Packs & Gear",
            "nav_id": "web-specials-packs-gear",
        },
        "collections-best-sellers": {
            "url": "https://www.patagonia.com/shop/collections/best-sellers",
            "name": "Best Sellers",
            "nav_id": "collections-essentials",
        },
        "books": {
            "url": "https://www.patagonia.com/shop/books",
            "name": "Books",
            "nav_id": "books",
        },
    },
    "mens": {
        "mens": {
            "url": "https://www.patagonia.com/shop/mens",
            "name": "Men's",
            "nav_id": "mens",
        },
        "all-mens": {
            "url": "https://www.patagonia.com/shop/all-mens",
            "name": "Shop All",
            "nav_id": "mens-all",
        },
        "mens-jackets-vests": {
            "url": "https://www.patagonia.com/shop/mens/jackets-vests",
            "name": "Jackets & Vests",
            "nav_id": "mens-jackets-vests",
        },
        "mens-fleece": {
            "url": "https://www.patagonia.com/shop/mens/fleece",
            "name": "Fleece",
            "nav_id": "mens-fleece",
        },
        "mens-tops": {
            "url": "https://www.patagonia.com/shop/mens/tops",
            "name": "Tops",
            "nav_id": "mens-tops",
        },
        "mens-bottoms": {
            "url": "https://www.patagonia.com/shop/mens/bottoms",
            "name": "Bottoms",
            "nav_id": "mens-bottoms",
        },
        "mens-socks-underwear-baselayers": {
            "url": "https://www.patagonia.com/shop/mens/socks-underwear/baselayers",
            "name": "Baselayers",
            "nav_id": "mens-baselayers",
        },
        "mens-boardshorts-rashguards": {
            "url": "https://www.patagonia.com/shop/mens/boardshorts-rashguards",
            "name": "Boardshorts & Rashguards",
            "nav_id": "mens-boardshorts-rashguards",
        },
        "mens-accessories": {
            "url": "https://www.patagonia.com/shop/mens/accessories",
            "name": "Hats & Accessories",
            "nav_id": "mens-hats-accessories",
        },
        "mens-socks": {
            "url": "https://www.patagonia.com/shop/mens/socks",
            "name": "Socks",
            "nav_id": "mens-socks",
        },
        "wetsuits-1": {
            "url": "https://www.patagonia.com/shop/wetsuits-1",
            "name": "Wetsuits",
            "nav_id": "mens-wetsuits-redirect",
        },
        "gear-waders-mens": {
            "url": "https://www.patagonia.com/shop/gear/waders/mens",
            "name": "Waders",
            "nav_id": "mens-waders-link",
        },
        "mens-workwear-clothing": {
            "url": "https://www.patagonia.com/shop/mens-workwear-clothing",
            "name": "Workwear",
            "nav_id": "sport-workwear-mens-redirect",
        },
        "sport-surfing-mens": {
            "url": "https://www.patagonia.com/shop/sport/surfing/mens",
            "name": "Surf",
            "nav_id": "mens-shop-by-sport-surf-link",
        },
        "sport-trail-running-mens": {
            "url": "https://www.patagonia.com/shop/sport/trail-running/mens",
            "name": "Trail Run",
            "nav_id": "mens-shop-by-sport-trail-run-link",
        },
        "sport-fly-fishing-mens": {
            "url": "https://www.patagonia.com/shop/sport/fly-fishing/mens",
            "name": "Fly Fish",
            "nav_id": "mens-shop-by-sport-fly-fish-link",
        },
        "sport-climbing-mens": {
            "url": "https://www.patagonia.com/shop/sport/climbing/mens",
            "name": "Climb",
            "nav_id": "mens-shop-by-sport-climb-link",
        },
        "sport-mountain-biking-mens": {
            "url": "https://www.patagonia.com/shop/sport/mountain-biking/mens",
            "name": "Mountain Bike",
            "nav_id": "mens-shop-by-sport-mtb-link",
        },
        "sport-skiing-snowboarding-mens": {
            "url": "https://www.patagonia.com/shop/sport/skiing-snowboarding/mens",
            "name": "Snow",
            "nav_id": "mens-shop-by-sport-snow-link",
        },
        "sport-hiking-mens": {
            "url": "https://www.patagonia.com/shop/sport/hiking/mens",
            "name": "Hike",
            "nav_id": "mens-shop-by-sport-hike-link",
        },
        "mens-collections-best-sellers": {
            "url": "https://www.patagonia.com/shop/mens/collections/best-sellers",
            "name": "Best Sellers",
        },
        "mens-jackets-vests-rain-waterproof": {
            "url": "https://www.patagonia.com/shop/mens/jackets-vests/rain-waterproof",
            "name": "Rain Jackets",
        },
        "collections-daily-mens": {
            "url": "https://www.patagonia.com/shop/collections/daily/mens",
            "name": "Daily Collection",
        },
    },
    "womens": {
        "womens": {
            "url": "https://www.patagonia.com/shop/womens",
            "name": "Women's",
            "nav_id": "womens",
        },
        "all-womens": {
            "url": "https://www.patagonia.com/shop/all-womens",
            "name": "Shop All",
            "nav_id": "womens-all",
        },
        "womens-jackets-vests": {
            "url": "https://www.patagonia.com/shop/womens/jackets-vests",
            "name": "Jackets & Vests",
            "nav_id": "womens-jackets-vests",
        },
        "womens-fleece": {
            "url": "https://www.patagonia.com/shop/womens/fleece",
            "name": "Fleece",
            "nav_id": "womens-fleece",
        },
        "womens-tops": {
            "url": "https://www.patagonia.com/shop/womens/tops",
            "name": "Tops",
            "nav_id": "womens-tops",
        },
        "womens-bottoms": {
            "url": "https://www.patagonia.com/shop/womens/bottoms",
            "name": "Bottoms",
            "nav_id": "womens-bottoms",
        },
        "womens-socks-underwear-baselayers": {
            "url": "https://www.patagonia.com/shop/womens/socks-underwear/baselayers",
            "name": "Baselayers",
            "nav_id": "womens-baselayers",
        },
        "womens-dresses-jumpsuits": {
            "url": "https://www.patagonia.com/shop/womens/dresses-jumpsuits",
            "name": "Dresses, Jumpsuits & Overalls",
            "nav_id": "womens-dresses-jumpsuits-overalls",
        },
        "womens-swimwear": {
            "url": "https://www.patagonia.com/shop/womens/swimwear",
            "name": "Swimwear",
            "nav_id": "womens-swimwear",
        },
        "womens-accessories": {
            "url": "https://www.patagonia.com/shop/womens/accessories",
            "name": "Hats & Accessories",
            "nav_id": "womens-hats-accessories",
        },
        "womens-sports-bras": {
            "url": "https://www.patagonia.com/shop/womens/sports-bras",
            "name": "Sports Bras",
            "nav_id": "womens-sports-bras",
        },
        "womens-socks": {
            "url": "https://www.patagonia.com/shop/womens/socks",
            "name": "Socks",
            "nav_id": "womens-socks",
        },
        "wetsuits-2": {
            "url": "https://www.patagonia.com/shop/wetsuits-2",
            "name": "Wetsuits",
            "nav_id": "womens-wetsuits-redirect",
        },
        "gear-waders-womens": {
            "url": "https://www.patagonia.com/shop/gear/waders/womens",
            "name": "Waders",
            "nav_id": "womens-waders-link",
        },
        "womens-workwear-clothing": {
            "url": "https://www.patagonia.com/shop/womens-workwear-clothing",
            "name": "Workwear",
            "nav_id": "sport-workwear-womens-redirect",
        },
        "sport-surfing-womens": {
            "url": "https://www.patagonia.com/shop/sport/surfing/womens",
            "name": "Surf",
            "nav_id": "womens-shop-by-sport-surf-link",
        },
        "sport-trail-running-womens": {
            "url": "https://www.patagonia.com/shop/sport/trail-running/womens",
            "name": "Trail Run",
            "nav_id": "womens-shop-by-sport-trail-run-link",
        },
        "sport-fly-fishing-womens": {
            "url": "https://www.patagonia.com/shop/sport/fly-fishing/womens",
            "name": "Fly Fish",
            "nav_id": "womens-shop-by-sport-fly-fish-link",
        },
        "sport-climbing-womens": {
            "url": "https://www.patagonia.com/shop/sport/climbing/womens",
            "name": "Climb",
            "nav_id": "womens-shop-by-sport-climb-link",
        },
        "sport-mountain-biking-womens": {
            "url": "https://www.patagonia.com/shop/sport/mountain-biking/womens",
            "name": "Mountain Bike",
            "nav_id": "womens-shop-by-sport-mtb-link",
        },
        "sport-skiing-snowboarding-womens": {
            "url": "https://www.patagonia.com/shop/sport/skiing-snowboarding/womens",
            "name": "Snow",
            "nav_id": "womens-shop-by-sport-snow-link",
        },
        "sport-hiking-womens": {
            "url": "https://www.patagonia.com/shop/sport/hiking/womens",
            "name": "Hike",
            "nav_id": "womens-shop-by-sport-hike-link",
        },
        "womens-collections-best-sellers": {
            "url": "https://www.patagonia.com/shop/womens/collections/best-sellers",
            "name": "Best Sellers",
        },
        "womens-jackets-vests-rain-waterproof": {
            "url": "https://www.patagonia.com/shop/womens/jackets-vests/rain-waterproof",
            "name": "Rain Jackets",
        },
        "collections-daily-womens": {
            "url": "https://www.patagonia.com/shop/collections/daily/womens",
            "name": "Daily Collection",
        },
    },
    "kids": {
        "kids-baby": {
            "url": "https://www.patagonia.com/shop/kids-baby",
            "name": "Kids'",
            "nav_id": "kids",
        },
        "all-kids-baby": {
            "url": "https://www.patagonia.com/shop/all-kids-baby",
            "name": "Shop All",
            "nav_id": "kids-all",
        },
        "kids-baby-babies-toddlers": {
            "url": "https://www.patagonia.com/shop/kids-baby/babies-toddlers",
            "name": "Babies & Toddlers (0 - 5T)",
            "nav_id": "kids-babies-toddlers",
        },
        "kids-baby-big-kids": {
            "url": "https://www.patagonia.com/shop/kids-baby/big-kids",
            "name": "Kids' (5 - 18)",
            "nav_id": "kids-big-kids",
        },
        "kids-baby-big-kids-boys": {
            "url": "https://www.patagonia.com/shop/kids-baby/big-kids/boys",
            "name": "Boys' (5 - 18)",
            "nav_id": "kids-boys",
        },
        "kids-baby-big-kids-girls": {
            "url": "https://www.patagonia.com/shop/kids-baby/big-kids/girls",
            "name": "Girls' (5 - 18)",
            "nav_id": "kids-girls",
        },
        "sport-surfing-kids": {
            "url": "https://www.patagonia.com/shop/sport/surfing/kids",
            "name": "Surf",
            "nav_id": "sport-surfing-kids",
        },
        "collections-kids-baby-trail-running": {
            "url": "https://www.patagonia.com/shop/collections/kids-baby/trail-running",
            "name": "Trail Run",
            "nav_id": "kids-running",
        },
        "collections-kids-baby-fly-fishing": {
            "url": "https://www.patagonia.com/shop/collections/kids-baby/fly-fishing",
            "name": "Fly Fish",
            "nav_id": "kids-fishing",
        },
        "collections-kids-baby-climbing": {
            "url": "https://www.patagonia.com/shop/collections/kids-baby/climbing",
            "name": "Climb",
            "nav_id": "kids-climbing",
        },
        "kids-baby-collections-skiing-snowboarding": {
            "url": "https://www.patagonia.com/shop/kids-baby/collections/skiing-snowboarding",
            "name": "Snow",
            "nav_id": "kids-ski-snowboard",
        },
        "collections-kids-baby-hiking": {
            "url": "https://www.patagonia.com/shop/collections/kids-baby/hiking",
            "name": "Hike",
            "nav_id": "kids-hiking",
        },
        "kids-baby-collections-best-sellers": {
            "url": "https://www.patagonia.com/shop/kids-baby/collections/best-sellers",
            "name": "Best Sellers",
        },
        "kids-baby-outerwear": {
            "url": "https://www.patagonia.com/shop/kids-baby/outerwear",
            "name": "Jackets & Vests",
        },
        "kids-baby-fleece": {
            "url": "https://www.patagonia.com/shop/kids-baby/fleece",
            "name": "Fleece",
        },
    },
    "packs-gear": {
        "packs-gear": {
            "url": "https://www.patagonia.com/shop/gear",
            "name": "Packs & Gear",
            "nav_id": "packs-gear",
        },
        "gear-bags": {
            "url": "https://www.patagonia.com/shop/gear/bags",
            "name": "Bags & Luggage",
            "nav_id": "luggage",
        },
        "all-luggage": {
            "url": "https://www.patagonia.com/shop/all-luggage",
            "name": "Shop All",
            "nav_id": "luggage-all",
        },
        "gear-bags-backpacks": {
            "url": "https://www.patagonia.com/shop/gear/bags/backpacks",
            "name": "Backpacks",
            "nav_id": "luggage-backpacks",
        },
        "gear-bags-duffels": {
            "url": "https://www.patagonia.com/shop/gear/bags/duffels",
            "name": "Duffels & Travel Bags",
            "nav_id": "luggage-duffel-bags",
        },
        "gear-bags-hip-packs-slings": {
            "url": "https://www.patagonia.com/shop/gear/bags/hip-packs-slings",
            "name": "Hip Packs & Slings",
            "nav_id": "luggage-hip-packs-slings",
        },
        "gear-bags-totes": {
            "url": "https://www.patagonia.com/shop/gear/bags/totes",
            "name": "Totes",
            "nav_id": "luggage-totes",
        },
        "gear-bags-water-protective": {
            "url": "https://www.patagonia.com/shop/gear/bags/water-protective",
            "name": "Water Protective Bags",
            "nav_id": "luggage-waterproof-bags",
        },
        "gear-bags-technical-packs": {
            "url": "https://www.patagonia.com/shop/gear/bags/technical-packs",
            "name": "Technical Packs",
            "nav_id": "luggage-technical-packs",
        },
        "gear-wetsuits-mens": {
            "url": "https://www.patagonia.com/shop/gear/wetsuits/mens",
            "name": "Men's",
            "nav_id": "mens-wetsuits",
        },
        "gear-wetsuits-womens": {
            "url": "https://www.patagonia.com/shop/gear/wetsuits/womens",
            "name": "Women's",
            "nav_id": "womens-wetsuits",
        },
        "gear-wetsuits-accessories": {
            "url": "https://www.patagonia.com/shop/gear/wetsuits/accessories",
            "name": "Booties, Gloves & Hoods",
            "nav_id": "mens-wetsuits-accessories",
        },
        "gear-wetsuits-big-wave-surfing": {
            "url": "https://www.patagonia.com/shop/gear/wetsuits/big-wave-surfing",
            "name": "Big-Wave Surfing",
            "nav_id": "mens-wetsuits-big-wave-gear",
        },
        "gear-waders-boots": {
            "url": "https://www.patagonia.com/shop/gear/waders/boots",
            "name": "Wading Boots",
            "nav_id": "waders-boots",
        },
        "gear-waders-accessories": {
            "url": "https://www.patagonia.com/shop/gear/waders/accessories",
            "name": "Wader Accessories",
            "nav_id": "waders-accessories",
        },
        "gear-bags-best-sellers": {
            "url": "https://www.patagonia.com/shop/gear/bags/best-sellers",
            "name": "Best Sellers",
        },
        "gear-care": {
            "url": "https://www.patagonia.com/shop/gear/care",
            "name": "Gear Care",
        },
        "gear-drinkware-accessories": {
            "url": "https://www.patagonia.com/shop/gear/drinkware-accessories",
            "name": "Drinkwear",
        },
    },
    "sport": {
        "sport-surfing": {
            "url": "https://www.patagonia.com/shop/sport/surfing",
            "name": "Shop All",
            "nav_id": "sport-surfing-shop-all-link",
        },
        "sport-surfing-packs-gear": {
            "url": "https://www.patagonia.com/shop/sport/surfing/packs-gear",
            "name": "Packs & Gear",
            "nav_id": "sport-surfing-packs-gear",
        },
        "trail-running": {
            "url": "https://www.patagonia.com/shop/sport/trail-running",
            "name": "Shop All",
            "nav_id": "sport-trail-running-shop-all-link",
        },
        "sport-trail-running-packs-gear": {
            "url": "https://www.patagonia.com/shop/sport/trail-running/packs-gear",
            "name": "Packs & Gear",
            "nav_id": "sport-trail-running-packs-gear",
        },
        "fly-fishing": {
            "url": "https://www.patagonia.com/shop/sport/fly-fishing",
            "name": "Shop All",
            "nav_id": "sport-fly-fishing-shop-all-link",
        },
        "gear-bags-technical-packs-fly-fishing": {
            "url": "https://www.patagonia.com/shop/gear/bags/technical-packs/fly-fishing",
            "name": "Packs & Gear",
            "nav_id": "sport-fly-fishing-packs-link",
        },
        "climbing": {
            "url": "https://www.patagonia.com/shop/sport/climbing",
            "name": "Shop All",
            "nav_id": "sport-climbing-shop-all-link",
        },
        "sport-climbing-packs-gear": {
            "url": "https://www.patagonia.com/shop/sport/climbing/packs-gear",
            "name": "Packs & Gear",
            "nav_id": "sport-climbing-packs-gear",
        },
        "mountain-biking": {
            "url": "https://www.patagonia.com/shop/sport/mountain-biking",
            "name": "Shop All",
            "nav_id": "sport-mountain-biking-shop-all-link",
        },
        "sport-mountain-biking-packs-gear": {
            "url": "https://www.patagonia.com/shop/sport/mountain-biking/packs-gear",
            "name": "Packs & Gear",
            "nav_id": "sport-mountain-biking-packs-gear",
        },
        "snow": {
            "url": "https://www.patagonia.com/shop/sport/skiing-snowboarding",
            "name": "Shop All",
            "nav_id": "sport-skiing-snowboarding-shop-all-link",
        },
        "kids-snow-gear": {
            "url": "https://www.patagonia.com/shop/kids-snow-gear",
            "name": "Kids'",
            "nav_id": "sport-skiing-snowboarding-kids",
        },
        "sport-skiing-snowboarding-packs-gear": {
            "url": "https://www.patagonia.com/shop/sport/skiing-snowboarding/packs-gear",
            "name": "Packs & Gear",
            "nav_id": "sport-skiing-snowboarding-packs-gear",
        },
    },
    "provisions": {
        "provisions": {
            "url": "https://www.patagonia.com/shop/provisions",
            "name": "Shop All",
            "nav_id": "provisions-shop-by-category-all-link",
        },
        "provisions-best-sellers": {
            "url": "https://www.patagonia.com/shop/provisions/best-sellers",
            "name": "Best Sellers",
            "nav_id": "provisions-shop-by-category-best-sellers-link",
        },
        "provisions-tinned-fish": {
            "url": "https://www.patagonia.com/shop/provisions/tinned-fish",
            "name": "Tinned Fish",
            "nav_id": "provisions-shop-by-category-tinned-fish-link",
        },
        "provisions-meat-sticks": {
            "url": "https://www.patagonia.com/shop/provisions/meat-sticks",
            "name": "Meat Sticks",
            "nav_id": "provisions-shop-by-category-meat-sticks-link",
        },
        "provisions-organic-crackers": {
            "url": "https://www.patagonia.com/shop/provisions/organic-crackers",
            "name": "Organic Crackers",
            "nav_id": "provisions-shop-by-category-organic-crackers-link",
        },
        "provisions-organic-beer": {
            "url": "https://www.patagonia.com/shop/provisions/organic-beer",
            "name": "Beer",
            "nav_id": "provisions-shop-by-category-beer-link",
        },
        "provisions-variety-packs": {
            "url": "https://www.patagonia.com/shop/provisions/variety-packs",
            "name": "Variety Packs",
            "nav_id": "provisions-shop-by-category-variety-packs-link",
        },
        "provisions-tinned-fish-anchovies": {
            "url": "https://www.patagonia.com/shop/provisions/tinned-fish/anchovies",
            "name": "Anchovies",
            "nav_id": "provisions-tinned-fish-anchovies",
        },
        "provisions-tinned-fish-mackerel": {
            "url": "https://www.patagonia.com/shop/provisions/tinned-fish/mackerel",
            "name": "Mackerel",
            "nav_id": "provisions-tinned-fish-mackerel",
        },
        "provisions-tinned-fish-mussels": {
            "url": "https://www.patagonia.com/shop/provisions/tinned-fish/mussels",
            "name": "Mussels",
            "nav_id": "provisions-tinned-fish-mussels",
        },
        "provisions-tinned-fish-salmon": {
            "url": "https://www.patagonia.com/shop/provisions/tinned-fish/salmon",
            "name": "Salmon",
            "nav_id": "provisions-tinned-fish-salmon",
        },
        "provisions-tinned-fish-sardines": {
            "url": "https://www.patagonia.com/shop/provisions/tinned-fish/sardines",
            "name": "Sardines",
            "nav_id": "provisions-tinned-fish-sardines",
        },
    },
}
