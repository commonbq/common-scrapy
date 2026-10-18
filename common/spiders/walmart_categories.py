"""Walmart's complete department -> subcategory inventory.

Captured 2026-10-18 from the live ``All Departments`` page
(https://www.walmart.com/all-departments, fetched through the configured
ScrapeOps US proxy). Each ``<h2>`` on that page is a department and its link list
holds the department's top subcategory PLPs, so this inventory is two real levels
deep instead of the bare 23 department hubs it used to hold.

Grouped ``{department: {leaf: {url, label}}}`` mapping as required by the base
listing spider contract. ``leaf`` is the slugified navigation label; every leaf is
globally unique, so the per-department DAG output paths cannot collide. Each
department also keeps a leaf named after its own group key (``electronics`` ->
the department hub) so the documented ``-a category=electronics`` command keeps
working. Hub entries sit last in their group because the DAG factory schedules
only the first three leaves per group: the scheduled tasks are real subcategory
PLPs and the hub stays reachable for a manual run.

Non-taxonomy links are excluded: the ``Savings & Featured Shops`` promo block,
every ``Shop All`` / ``All ...`` alias that points back at the department hub, and
Walmart's ``Exclusively online`` grocery link, which the site serializes with a
literal ellipsis (``/cp/shop-m...your-store/7485418``) in both the anchor and its
embedded JSON and therefore has no crawlable URL.

Six PLPs are linked from two departments. Each URL is stored once, under its
natural department: ``Kids Clothing`` (clothing, not baby-and-kids),
``Video Games`` (video-games), ``Auto Electronics`` (electronics),
``Outdoor Toys`` (toys), ``Party Supplies`` (seasonal-and-celebrations) and
``Toy Shop`` (toys). A department hub always stays with its own group even when
another department links it.

23 departments / 296 leaves, all globally unique.
"""

WALMART_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {

    "grocery": {
        "ebt-snap-eligible-food": {
            "url": "https://www.walmart.com/cp/snap-online/1465096",
            "label": "EBT/SNAP eligible food",
        },
        "exclusively-online": {
            "url": "https://www.walmart.com/cp/shop-more-than-your-store/7485418",
            "label": "Exclusively online",
        },
        "everyday-meals": {
            "url": "https://www.walmart.com/cp/dinner-tonight/5681029",
            "label": "Everyday meals",
        },
        "fresh-produce": {
            "url": "https://www.walmart.com/cp/fresh-produce/976793",
            "label": "Fresh Produce",
        },
        "meat-seafood": {
            "url": "https://www.walmart.com/cp/meat-seafood/9569500",
            "label": "Meat & Seafood",
        },
        "deli": {
            "url": "https://www.walmart.com/cp/deli/976789",
            "label": "Deli",
        },
        "dairy-eggs": {
            "url": "https://www.walmart.com/cp/dairy-eggs/9176907",
            "label": "Dairy & Eggs",
        },
        "bread-bakery": {
            "url": "https://www.walmart.com/cp/bakery-bread/976779",
            "label": "Bread & Bakery",
        },
        "frozen": {
            "url": "https://www.walmart.com/cp/frozen-foods/976791",
            "label": "Frozen",
        },
        "pantry": {
            "url": "https://www.walmart.com/cp/pantry/976794",
            "label": "Pantry",
        },
        "breakfast-cereal": {
            "url": "https://www.walmart.com/cp/breakfast-cereal/976783",
            "label": "Breakfast & Cereal",
        },
        "bake-center": {
            "url": "https://www.walmart.com/cp/baking/976780",
            "label": "Bake Center",
        },
        "cookies": {
            "url": "https://www.walmart.com/cp/cookies/1001391",
            "label": "Cookies",
        },
        "snacks": {
            "url": "https://www.walmart.com/cp/snacks-cookies-chips/976787",
            "label": "Snacks",
        },
        "candy": {
            "url": "https://www.walmart.com/cp/candy/1096070",
            "label": "Candy",
        },
        "beverages": {
            "url": "https://www.walmart.com/cp/beverages/976782",
            "label": "Beverages",
        },
        "alcohol": {
            "url": "https://www.walmart.com/cp/alcohol/2975985",
            "label": "Alcohol",
        },
        "organic-foods": {
            "url": "https://www.walmart.com/cp/organic-shop/1228024",
            "label": "Organic Foods",
        },
        "gluten-free-foods": {
            "url": "https://www.walmart.com/cp/dietary-lifestyle-shop/5004481",
            "label": "Gluten Free Foods",
        },
        "food-gifts-flowers-shop": {
            "url": "https://www.walmart.com/cp/food-gifts-flowers-shop/1089004",
            "label": "Food Gifts & Flowers Shop",
        },
        "grocery": {
            "url": "https://www.walmart.com/cp/976759",
            "label": "Grocery",
        },
    },
    "home": {
        "furniture": {
            "url": "https://www.walmart.com/cp/furniture/103150",
            "label": "Furniture",
        },
        "mattresses-accessories": {
            "url": "https://www.walmart.com/cp/mattresses-accessories/539386",
            "label": "Mattresses & Accessories",
        },
        "kitchen-dining": {
            "url": "https://www.walmart.com/cp/kitchen-dining/623679",
            "label": "Kitchen & Dining",
        },
        "storage-organization": {
            "url": "https://www.walmart.com/cp/storage-organization/90828",
            "label": "Storage & Organization",
        },
        "luggage-travel": {
            "url": "https://www.walmart.com/cp/luggage/7333633",
            "label": "Luggage & Travel",
        },
        "appliances": {
            "url": "https://www.walmart.com/cp/appliances/90548",
            "label": "Appliances",
        },
        "vacuums-steamers-floorcare": {
            "url": "https://www.walmart.com/cp/vacuums-steamers-floor-care/4047",
            "label": "Vacuums, Steamers & Floorcare",
        },
        "kitchen-appliances": {
            "url": "https://www.walmart.com/cp/kitchen-appliances/90546",
            "label": "Kitchen Appliances",
        },
        "decor": {
            "url": "https://www.walmart.com/cp/decor/133012",
            "label": "Decor",
        },
        "bedding": {
            "url": "https://www.walmart.com/cp/bedding/539103",
            "label": "Bedding",
        },
        "bath": {
            "url": "https://www.walmart.com/cp/bath/539095",
            "label": "Bath",
        },
        "home": {
            "url": "https://www.walmart.com/cp/home/4044",
            "label": "Home, Furniture & Appliances",
        },
    },
    "patio-and-garden": {
        "patio-furniture": {
            "url": "https://www.walmart.com/cp/patio-furniture/91416",
            "label": "Patio Furniture",
        },
        "patio-sets": {
            "url": "https://www.walmart.com/browse/patio-furniture/patio-sets/5428_91416_3013177",
            "label": "Patio Sets",
        },
        "conversation-sets": {
            "url": "https://www.walmart.com/browse/patio-garden/patio-conversation-sets/5428_91416_3013177_1225084",
            "label": "Conversation Sets",
        },
        "outdoor-cooking": {
            "url": "https://www.walmart.com/cp/grills-outdoor-cooking/4089",
            "label": "Outdoor Cooking",
        },
        "gas-grills": {
            "url": "https://www.walmart.com/browse/patio-garden/gas-grills/5428_4089_7375787_7991811",
            "label": "Gas Grills",
        },
        "charcoal": {
            "url": "https://www.walmart.com/browse/patio-garden/lump-charcoal-briquettes/5428_4089_9732116_5377022",
            "label": "Charcoal",
        },
        "outdoor-decor": {
            "url": "https://www.walmart.com/cp/patio-outdoor-decor/1102183",
            "label": "Outdoor Decor",
        },
        "outdoor-rugs": {
            "url": "https://www.walmart.com/browse/patio-garden/outdoor-rugs/5428_1102183_133056",
            "label": "Outdoor Rugs",
        },
        "outdoor-cushions": {
            "url": "https://www.walmart.com/browse/patio-garden/outdoor-cushions/5428_1102183_1225353",
            "label": "Outdoor Cushions",
        },
        "outdoor-power-equipment": {
            "url": "https://www.walmart.com/cp/outdoor-power-equipment/1102182",
            "label": "Outdoor Power Equipment",
        },
        "lawn-mowers": {
            "url": "https://www.walmart.com/browse/patio-garden/lawn-mowers/5428_1102182_1225352",
            "label": "Lawn Mowers",
        },
        "lawn-care": {
            "url": "https://www.walmart.com/browse/patio-garden/lawn-care/5428_4091_6107689",
            "label": "Lawn Care",
        },
        "bird-seed": {
            "url": "https://www.walmart.com/browse/bird-feeders-and-bird-houses/bird-seed-and-food/5428_1102183_7713111_8673767",
            "label": "Bird Seed",
        },
        "pool-chemicals": {
            "url": "https://www.walmart.com/browse/patio-garden/pool-chemicals/5428_132873_8964332",
            "label": "Pool Chemicals",
        },
        "garden-center": {
            "url": "https://www.walmart.com/cp/garden-center/4091",
            "label": "Garden Center",
        },
        "soil": {
            "url": "https://www.walmart.com/browse/patio-garden/soil/5428_4091_1229594_3290662",
            "label": "Soil",
        },
        "mulch": {
            "url": "https://www.walmart.com/browse/patio-garden/mulch/5428_4091_1229594_1229607",
            "label": "Mulch",
        },
        "live-plants": {
            "url": "https://www.walmart.com/browse/live-plants/5428_6061364",
            "label": "Live Plants",
        },
        "patio-and-garden": {
            "url": "https://www.walmart.com/cp/patio-garden/5428",
            "label": "Patio & Garden",
        },
    },
    "home-improvement": {
        "heaters": {
            "url": "https://www.walmart.com/browse/home-improvement/space-heaters/1072864_133032_1161932_1085403",
            "label": "Heaters",
        },
        "humidifiers": {
            "url": "https://www.walmart.com/browse/home-improvement/humidifiers/1072864_133032_1231459_133042",
            "label": "Humidifiers",
        },
        "air-quality": {
            "url": "https://www.walmart.com/browse/home-improvement/air-quality/1072864_133032_1231459",
            "label": "Air Quality",
        },
        "water-purification": {
            "url": "https://www.walmart.com/browse/home-improvement/water-filters/1072864_6610571_1231153",
            "label": "Water Purification",
        },
        "tools": {
            "url": "https://www.walmart.com/cp/tools/1031899",
            "label": "Tools",
        },
        "fasteners": {
            "url": "https://www.walmart.com/browse/home-improvement/fasteners/1072864_1067612_1067614",
            "label": "Fasteners",
        },
        "building-materials": {
            "url": "https://www.walmart.com/browse/home-improvement/building-materials/1072864_1172176",
            "label": "Building Materials",
        },
        "fans": {
            "url": "https://www.walmart.com/browse/home-improvement/fans/1072864_133032_1231458_1230511",
            "label": "Fans",
        },
        "wallpaper-wall-coverings": {
            "url": "https://www.walmart.com/browse/home-improvement/wallpaper-wall-decals-wall-coverings/1072864_7141380",
            "label": "Wallpaper & Wall Coverings",
        },
        "kitchen-renovation": {
            "url": "https://www.walmart.com/browse/home-improvement/kitchen-renovation/1072864_1071485",
            "label": "Kitchen Renovation",
        },
        "bathroom-renovation": {
            "url": "https://www.walmart.com/browse/home-improvement/bathroom-renovation/1072864_1045879",
            "label": "Bathroom Renovation",
        },
        "shower-heads": {
            "url": "https://www.walmart.com/browse/home-improvement/shower-heads/1072864_1045879_1230843_9581595",
            "label": "Shower Heads",
        },
        "toilet-seats-lids": {
            "url": "https://www.walmart.com/browse/home-improvement/toilet-seats-and-lids/1072864_1045879_5533759_4289910_6982244",
            "label": "Toilet Seats & Lids",
        },
        "paint": {
            "url": "https://www.walmart.com/cp/paint/1067617",
            "label": "Paint",
        },
        "flooring": {
            "url": "https://www.walmart.com/browse/home-improvement/flooring/1072864_1067616",
            "label": "Flooring",
        },
        "light-bulbs": {
            "url": "https://www.walmart.com/cp/Light-Bulbs/1228347",
            "label": "Light Bulbs",
        },
        "light-fixtures": {
            "url": "https://www.walmart.com/cp/lighting-light-fixtures/133113",
            "label": "Light Fixtures",
        },
        "garage-storage": {
            "url": "https://www.walmart.com/browse/home-improvement/garage-storage/1072864_1067618",
            "label": "Garage Storage",
        },
        "personal-protective-equipment": {
            "url": "https://www.walmart.com/browse/home-improvement/personal-protective-equipment/1072864_1031899_7124246",
            "label": "Personal Protective Equipment",
        },
        "adhesives-glues": {
            "url": "https://www.walmart.com/browse/paint-supplies-tools/adhesives-glues/1072864_1067617_1067621_1358553",
            "label": "Adhesives & Glues",
        },
        "dehumidifiers": {
            "url": "https://www.walmart.com/browse/air-quality/dehumidifiers/1072864_133032_1231459_112918",
            "label": "Dehumidifiers",
        },
        "air-conditioners": {
            "url": "https://www.walmart.com/browse/home-improvement/air-conditioners/1072864_133032_1231458_133026",
            "label": "Air Conditioners",
        },
        "home-improvement": {
            "url": "https://www.walmart.com/cp/home-improvement/1072864",
            "label": "Home Improvement",
        },
    },
    "clothing": {
        "premium-fashion": {
            "url": "https://www.walmart.com/cp/premium-fashion/7056862",
            "label": "Premium Fashion",
        },
        "now-trending": {
            "url": "https://www.walmart.com/cp/trending/5289731",
            "label": "Now Trending",
        },
        "women": {
            "url": "https://www.walmart.com/cp/womens-clothing/133162",
            "label": "Women",
        },
        "womens-plus": {
            "url": "https://www.walmart.com/cp/womens-plus/133195",
            "label": "Women's Plus",
        },
        "men": {
            "url": "https://www.walmart.com/cp/mens-clothing/133197",
            "label": "Men",
        },
        "young-adult": {
            "url": "https://www.walmart.com/cp/young-adult/9055522",
            "label": "Young Adult",
        },
        "kids": {
            "url": "https://www.walmart.com/cp/kids-clothing/7712430",
            "label": "Kids",
        },
        "baby-toddler": {
            "url": "https://www.walmart.com/browse/clothing/baby-clothes/5438_7712430_8775031_4648145",
            "label": "Baby & Toddler",
        },
        "shoes": {
            "url": "https://www.walmart.com/cp/shoes/1045804",
            "label": "Shoes",
        },
        "jewelry-watches": {
            "url": "https://www.walmart.com/cp/jewelry/3891",
            "label": "Jewelry & Watches",
        },
        "bags-accessories": {
            "url": "https://www.walmart.com/cp/bags-accessories/1045799",
            "label": "Bags & Accessories",
        },
        "clothing": {
            "url": "https://www.walmart.com/cp/clothing/5438",
            "label": "Clothing, Shoes & Accessories",
        },
    },
    "toys": {
        "action-figures": {
            "url": "https://www.walmart.com/cp/action-figures/4172",
            "label": "Action Figures",
        },
        "dolls-dollhouses": {
            "url": "https://www.walmart.com/cp/dolls-dollhouses/4187",
            "label": "Dolls & Dollhouses",
        },
        "learning-toys": {
            "url": "https://www.walmart.com/cp/learning-toys/56125",
            "label": "Learning Toys",
        },
        "dart-blasters": {
            "url": "https://www.walmart.com/browse/toys/nerf-blaster-toys/4171_14521_936979",
            "label": "Dart Blasters",
        },
        "games-puzzles": {
            "url": "https://www.walmart.com/cp/games-puzzles/4191",
            "label": "Games & Puzzles",
        },
        "collectibles": {
            "url": "https://www.walmart.com/cp/collectibles/5967908",
            "label": "Collectibles",
        },
        "cars-drones-rc": {
            "url": "https://www.walmart.com/browse/remote-control-play-vehicles/4171_1111647",
            "label": "Cars, Drones & RC",
        },
        "lego-building-sets": {
            "url": "https://www.walmart.com/browse/building-sets-blocks/4171_4186",
            "label": "LEGO & Building Sets",
        },
        "pretend-play": {
            "url": "https://www.walmart.com/browse/pretend-play/4171_4173",
            "label": "Pretend Play",
        },
        "outdoor-toys": {
            "url": "https://www.walmart.com/cp/outdoor-toys/14521",
            "label": "Outdoor Toys",
        },
        "kids-bikes": {
            "url": "https://www.walmart.com/browse/sports-outdoors/kids-bikes/4125_1081404_9240575",
            "label": "Kids Bikes",
        },
        "ride-on-toys": {
            "url": "https://www.walmart.com/browse/toys/ride-ons/4171_133073_6774653",
            "label": "Ride-on Toys",
        },
        "toys": {
            "url": "https://www.walmart.com/cp/toys/4171",
            "label": "Toys",
        },
    },
    "baby-and-kids": {
        "diapers-wipes": {
            "url": "https://www.walmart.com/cp/diapering/486190",
            "label": "Diapers & Wipes",
        },
        "baby-registry": {
            "url": "https://www.walmart.com/cp/baby-registry/1229485",
            "label": "Baby Registry",
        },
        "baby-clothing": {
            "url": "https://www.walmart.com/browse/5438_7712430_8775031_4648145",
            "label": "Baby Clothing",
        },
        "toddler-clothing": {
            "url": "https://www.walmart.com/browse/5438_7712430_2700757_2676407",
            "label": "Toddler Clothing",
        },
        "baby-and-kids": {
            "url": "https://www.walmart.com/cp/baby-products/5427",
            "label": "Baby & Kids",
        },
    },
    "video-games": {
        "xbox": {
            "url": "https://www.walmart.com/cp/xbox-series-x/9206773",
            "label": "Xbox",
        },
        "playstation": {
            "url": "https://www.walmart.com/cp/playstation-5/3475115",
            "label": "PlayStation",
        },
        "nintendo": {
            "url": "https://www.walmart.com/cp/nintendo-switch/4646529",
            "label": "Nintendo",
        },
        "video-game-accessories": {
            "url": "https://www.walmart.com/browse/video-games/video-game-accessories/2636_1229019",
            "label": "Video Game Accessories",
        },
        "virtual-reality": {
            "url": "https://www.walmart.com/browse/video-games/virtual-reality/2636_5454301",
            "label": "Virtual Reality",
        },
        "video-games": {
            "url": "https://www.walmart.com/cp/video-games/2636",
            "label": "Video Games",
        },
    },
    "electronics": {
        "tv-video": {
            "url": "https://www.walmart.com/cp/tv-video/1060825",
            "label": "TV & Video",
        },
        "home-audio-theater": {
            "url": "https://www.walmart.com/browse/home-audio-theater/3944_77622",
            "label": "Home Audio & Theater",
        },
        "smart-home": {
            "url": "https://www.walmart.com/cp/smart-home/1229875",
            "label": "Smart Home",
        },
        "tablets-accessories": {
            "url": "https://www.walmart.com/cp/ipad-tablets/1078524",
            "label": "Tablets & Accessories",
        },
        "computers": {
            "url": "https://www.walmart.com/cp/computers/3951",
            "label": "Computers",
        },
        "cell-phones": {
            "url": "https://www.walmart.com/cp/cell-phones/1105910",
            "label": "Cell Phones",
        },
        "wearable-tech": {
            "url": "https://www.walmart.com/cp/wearable-technology/1229723",
            "label": "Wearable Tech",
        },
        "cameras-camcorders-drones": {
            "url": "https://www.walmart.com/cp/cameras-camcorders/133277",
            "label": "Cameras, Camcorders & Drones",
        },
        "portable-audio": {
            "url": "https://www.walmart.com/browse/electronics/portable-audio/3944_133251_96469_1037719",
            "label": "Portable Audio",
        },
        "auto-electronics": {
            "url": "https://www.walmart.com/cp/auto-electronics/3947",
            "label": "Auto Electronics",
        },
        "electronics": {
            "url": "https://www.walmart.com/cp/electronics/3944",
            "label": "Electronics",
        },
    },
    "health-and-wellness": {
        "pharmacy": {
            "url": "https://www.walmart.com/cp/pharmacy/5431",
            "label": "Pharmacy",
        },
        "allergy-sinus": {
            "url": "https://www.walmart.com/cp/allergy-sinus/3771182",
            "label": "Allergy & Sinus",
        },
        "vitamins-supplements": {
            "url": "https://www.walmart.com/cp/vitamins-supplements/1005863",
            "label": "Vitamins & Supplements",
        },
        "caregiver-hub": {
            "url": "https://www.walmart.com/cp/caregiver/2915579",
            "label": "Caregiver Hub",
        },
        "protein-fitness-weight-management": {
            "url": "https://www.walmart.com/cp/protein-fitness/1166769",
            "label": "Protein, Fitness, & Weight Management",
        },
        "womens-wellness": {
            "url": "https://www.walmart.com/cp/1767021",
            "label": "Women's Wellness",
        },
        "pain-management": {
            "url": "https://www.walmart.com/cp/pain-management/6972993",
            "label": "Pain Management",
        },
        "first-aid-injury-recovery": {
            "url": "https://www.walmart.com/cp/first-aid/2571007",
            "label": "First Aid & Injury Recovery",
        },
        "vision-center": {
            "url": "https://www.walmart.com/cp/vision-centers/1078944",
            "label": "Vision Center",
        },
        "digestive-health-wellness": {
            "url": "https://www.walmart.com/cp/digestive-health/1396434",
            "label": "Digestive Health & Wellness",
        },
        "cough-cold-flu": {
            "url": "https://www.walmart.com/cp/cough-cold-flu-medicine/4661388",
            "label": "Cough, Cold, & Flu",
        },
        "eyecare": {
            "url": "https://www.walmart.com/cp/9575239",
            "label": "Eyecare",
        },
        "diabetes-management": {
            "url": "https://www.walmart.com/cp/diabetes-support/1231757",
            "label": "Diabetes Management",
        },
        "international-medicine": {
            "url": "https://www.walmart.com/cp/4178898",
            "label": "International Medicine",
        },
        "benefits-hub": {
            "url": "https://www.walmart.com/cp/benefit-programs/4137417",
            "label": "Benefits Hub",
        },
        "health-and-wellness": {
            "url": "https://www.walmart.com/cp/health/976760",
            "label": "Pharmacy, Health & Wellness",
        },
    },
    "personal-care": {
        "multipacks": {
            "url": "https://www.walmart.com/browse/seasonal/personal-care-stock-up/1085632_9267270_7332448",
            "label": "Multipacks",
        },
        "bath-body": {
            "url": "https://www.walmart.com/cp/bath-body/1071969",
            "label": "Bath & Body",
        },
        "oral-care": {
            "url": "https://www.walmart.com/cp/oral-care/1007221",
            "label": "Oral Care",
        },
        "feminine-care": {
            "url": "https://www.walmart.com/browse/personal-care/feminine-care/1005862_1091866",
            "label": "Feminine Care",
        },
        "incontinence": {
            "url": "https://www.walmart.com/browse/personal-care/incontinence/1005862_1225655",
            "label": "Incontinence",
        },
        "sexual-wellness": {
            "url": "https://www.walmart.com/cp/sexual-wellness/1414629",
            "label": "Sexual Wellness",
        },
        "shaving": {
            "url": "https://www.walmart.com/cp/shaving/1007220",
            "label": "Shaving",
        },
        "mens-grooming": {
            "url": "https://www.walmart.com/cp/mens-grooming/1056884",
            "label": "Men's Grooming",
        },
        "sunscreen": {
            "url": "https://www.walmart.com/browse/beauty/sunscreen/1085666_1007039_1001508_8279042",
            "label": "Sunscreen",
        },
        "self-tanners": {
            "url": "https://www.walmart.com/browse/beauty/self-tanners-bronzers/1085666_1007039_1001508_6439038",
            "label": "Self Tanners",
        },
        "personal-care": {
            "url": "https://www.walmart.com/cp/personal-care/1005862",
            "label": "Personal Care",
        },
    },
    "beauty": {
        "premium-beauty": {
            "url": "https://www.walmart.com/cp/premium-beauty/7924299",
            "label": "Premium Beauty",
        },
        "makeup": {
            "url": "https://www.walmart.com/cp/makeup/1007040",
            "label": "Makeup",
        },
        "haircare": {
            "url": "https://www.walmart.com/cp/hair-care/1007219",
            "label": "Haircare",
        },
        "skincare": {
            "url": "https://www.walmart.com/cp/skin-care/1007039",
            "label": "Skincare",
        },
        "fragrance": {
            "url": "https://www.walmart.com/cp/fragrances/133225",
            "label": "Fragrance",
        },
        "nail-care": {
            "url": "https://www.walmart.com/cp/nailcare/3592123",
            "label": "Nail Care",
        },
        "suncare-tanning": {
            "url": "https://www.walmart.com/browse/beauty/facial-sunscreen/1085666_1007039_4046177",
            "label": "Suncare & Tanning",
        },
        "beauty-tech-tools": {
            "url": "https://www.walmart.com/browse/beauty/beauty-tools-tech/1085666_2446618",
            "label": "Beauty Tech & Tools",
        },
        "beauty-mens-grooming": {
            "url": "https://www.walmart.com/cp/mens-essentials/1056884",
            "label": "Men's Grooming",
        },
        "beauty-box": {
            "url": "https://www.walmart.com/browse/beauty/walmart-beauty-box/1085666_4820682_9411485",
            "label": "Beauty Box",
        },
        "beauty": {
            "url": "https://www.walmart.com/cp/beauty/1085666",
            "label": "Beauty",
        },
    },
    "auto-and-tires": {
        "tires": {
            "url": "https://www.walmart.com/cp/tires-accessories/1077064",
            "label": "Tires",
        },
        "batteries-accessories": {
            "url": "https://www.walmart.com/cp/batteries-accessories/1104292",
            "label": "Batteries & Accessories",
        },
        "auto-care-center": {
            "url": "https://www.walmart.com/cp/auto-services/1087266",
            "label": "Auto Care Center",
        },
        "oils-and-fluids": {
            "url": "https://www.walmart.com/cp/oils-fluids/1104294",
            "label": "Oils and Fluids",
        },
        "replacement-auto-parts": {
            "url": "https://www.walmart.com/cp/automotive-replacement-parts/1074765",
            "label": "Replacement Auto Parts",
        },
        "exterior-car-parts-accessories": {
            "url": "https://www.walmart.com/cp/exterior-car-parts-accessories/1074784",
            "label": "Exterior Car Parts & Accessories",
        },
        "interior-accessories": {
            "url": "https://www.walmart.com/cp/interior-parts-accessories/1074769",
            "label": "Interior Accessories",
        },
        "automotive-tools-equipment": {
            "url": "https://www.walmart.com/browse/auto-tires/automotive-tools-equipment/91083_5941050",
            "label": "Automotive Tools & Equipment",
        },
        "auto-detailing-car-care": {
            "url": "https://www.walmart.com/cp/car-detailing/1212910",
            "label": "Auto Detailing & Car Care",
        },
        "wheels-and-rims": {
            "url": "https://www.walmart.com/browse/auto-tires/wheels-and-rims/91083_4375198",
            "label": "Wheels and Rims",
        },
        "truck-parts-accessories": {
            "url": "https://www.walmart.com/cp/truck-accessories-truck-parts/1752665",
            "label": "Truck Parts & Accessories",
        },
        "rv-parts-accessories": {
            "url": "https://www.walmart.com/browse/auto-tires/rv-parts-accessories/91083_2983678",
            "label": "RV Parts & Accessories",
        },
        "oem-parts": {
            "url": "https://www.walmart.com/browse/auto-tires/oem-parts/91083_4108114",
            "label": "OEM Parts",
        },
        "motorcycle-parts-accessories": {
            "url": "https://www.walmart.com/browse/auto-tires/motorcycle-parts-accessories/91083_4530084",
            "label": "Motorcycle Parts & Accessories",
        },
        "vehicles": {
            "url": "https://www.walmart.com/browse/auto-tires/vehicles/91083_5320758",
            "label": "Vehicles",
        },
        "automotive-apparel": {
            "url": "https://www.walmart.com/browse/auto-tires/automotive-apparel/91083_2786870",
            "label": "Automotive Apparel",
        },
        "car-safety-car-security": {
            "url": "https://www.walmart.com/browse/auto-tires/car-safety-car-security/91083_1074766",
            "label": "Car Safety & Car Security",
        },
        "auto-and-tires": {
            "url": "https://www.walmart.com/cp/auto-tires/91083",
            "label": "Auto & Tires",
        },
    },
    "household-essentials": {
        "delivery-subscriptions": {
            "url": "https://www.walmart.com/browse/household-essentials/household-essentials-subscription/1115193_7023530",
            "label": "Delivery Subscriptions",
        },
        "cleaning-supplies": {
            "url": "https://www.walmart.com/browse/household-essentials/cleaning-supplies/1115193_1071966",
            "label": "Cleaning Supplies",
        },
        "laundry": {
            "url": "https://www.walmart.com/browse/household-essentials/laundry/1115193_1071967",
            "label": "Laundry",
        },
        "bathroom": {
            "url": "https://www.walmart.com/browse/household-essentials/bathroom/1115193_1071965",
            "label": "Bathroom",
        },
        "kitchen": {
            "url": "https://www.walmart.com/browse/household-essentials/kitchen/1115193_1071968",
            "label": "Kitchen",
        },
        "paper-plastic": {
            "url": "https://www.walmart.com/browse/household-essentials/paper-plastic/1115193_1073264",
            "label": "Paper & Plastic",
        },
        "air-fresheners": {
            "url": "https://www.walmart.com/browse/household-essentials/air-fresheners/1115193_1025739",
            "label": "Air Fresheners",
        },
        "cold-flu-supplies": {
            "url": "https://www.walmart.com/browse/household-essentials/cough-allergy-supplies/1115193_3787768",
            "label": "Cold & Flu Supplies",
        },
        "pest-control": {
            "url": "https://www.walmart.com/browse/household-essentials/pest-control/1115193_1025745",
            "label": "Pest Control",
        },
        "batteries": {
            "url": "https://www.walmart.com/browse/household-essentials/batteries/1115193_1076905",
            "label": "Batteries",
        },
        "household-essentials": {
            "url": "https://www.walmart.com/cp/household-essentials/1115193",
            "label": "Household Essentials",
        },
    },
    "sports-and-outdoors": {
        "sports": {
            "url": "https://www.walmart.com/cp/sports/4161",
            "label": "Sports",
        },
        "basketball": {
            "url": "https://www.walmart.com/browse/sports-outdoors/basketball/4125_4161_4165",
            "label": "Basketball",
        },
        "football": {
            "url": "https://www.walmart.com/browse/sports-outdoors/football-gear-equipment/4125_4161_434036",
            "label": "Football",
        },
        "golf": {
            "url": "https://www.walmart.com/browse/sports-outdoors/golf-equipment/4125_4161_4152",
            "label": "Golf",
        },
        "pickleball": {
            "url": "https://www.walmart.com/browse/sports-outdoors/pickleball/4125_4161_6675878",
            "label": "Pickleball",
        },
        "soccer": {
            "url": "https://www.walmart.com/browse/sports-outdoors/soccer/4125_4161_432196",
            "label": "Soccer",
        },
        "fitness": {
            "url": "https://www.walmart.com/cp/exercise-fitness/4134",
            "label": "Fitness",
        },
        "outdoor-sports": {
            "url": "https://www.walmart.com/cp/outdoor-sports/546956",
            "label": "Outdoor Sports",
        },
        "bikes": {
            "url": "https://www.walmart.com/cp/bikes/1081404",
            "label": "Bikes",
        },
        "boats-marine": {
            "url": "https://www.walmart.com/cp/boats-marine/1208159",
            "label": "Boats & Marine",
        },
        "camping": {
            "url": "https://www.walmart.com/cp/camping-gear/4128",
            "label": "Camping",
        },
        "fishing": {
            "url": "https://www.walmart.com/cp/fishing-gear/111667",
            "label": "Fishing",
        },
        "hunting": {
            "url": "https://www.walmart.com/cp/hunting/4155",
            "label": "Hunting",
        },
        "sports-shooting": {
            "url": "https://www.walmart.com/cp/shooting/1107532",
            "label": "Sports Shooting",
        },
        "trampolines": {
            "url": "https://www.walmart.com/browse/sports-outdoors/trampolines/4125_1224931_5230",
            "label": "Trampolines",
        },
        "swing-sets": {
            "url": "https://www.walmart.com/browse/toys/swing-sets/4171_14521_6449441",
            "label": "Swing Sets",
        },
        "swimming-pools-spas": {
            "url": "https://www.walmart.com/cp/swimming-pools-and-spas/132873",
            "label": "Swimming Pools & Spas",
        },
        "sports-and-outdoors": {
            "url": "https://www.walmart.com/cp/4125",
            "label": "Sports & Outdoors",
        },
    },
    "pets": {
        "the-pet-event": {
            "url": "https://www.walmart.com/cp/the-pet-event/6286537",
            "label": "The Pet Event",
        },
        "pet-prescriptions": {
            "url": "https://www.walmart.com/cp/8328098",
            "label": "Pet Prescriptions",
        },
        "dog-supplies": {
            "url": "https://www.walmart.com/cp/dogs/202072",
            "label": "Dog Supplies",
        },
        "dog-food": {
            "url": "https://www.walmart.com/browse/pets/dog-food-and-treats/5440_202072_6432755",
            "label": "Dog Food",
        },
        "dog-toys": {
            "url": "https://www.walmart.com/browse/pets/all-dog-toys/5440_202072_2243339_202086",
            "label": "Dog Toys",
        },
        "cat-supplies": {
            "url": "https://www.walmart.com/cp/cats/202073",
            "label": "Cat Supplies",
        },
        "cat-food": {
            "url": "https://www.walmart.com/browse/pets/cat-food/5440_202073_1749780",
            "label": "Cat Food",
        },
        "cat-toys": {
            "url": "https://www.walmart.com/browse/pets/all-cat-toys/5440_202073_2584809_1920023",
            "label": "Cat Toys",
        },
        "fish-aquatic-pets": {
            "url": "https://www.walmart.com/cp/fish-supplies/202074",
            "label": "Fish & Aquatic Pets",
        },
        "farm-animals": {
            "url": "https://www.walmart.com/cp/farm-animals/4024509",
            "label": "Farm Animals",
        },
        "small-animals": {
            "url": "https://www.walmart.com/cp/small-animals/1001299",
            "label": "Small Animals",
        },
        "reptiles": {
            "url": "https://www.walmart.com/cp/reptiles/6833286",
            "label": "Reptiles",
        },
        "birds": {
            "url": "https://www.walmart.com/cp/birds/228734",
            "label": "Birds",
        },
        "pets": {
            "url": "https://www.walmart.com/cp/pet-supplies/5440",
            "label": "Pets",
        },
    },
    "school-and-office-supplies": {
        "school-supplies": {
            "url": "https://www.walmart.com/cp/school-supplies/1086045",
            "label": "School Supplies",
        },
        "teachers-classroom-shop": {
            "url": "https://www.walmart.com/cp/teaching-classroom-supplies/3462603",
            "label": "Teacher’s Classroom Shop",
        },
        "bulk-teaching-supplies": {
            "url": "https://www.walmart.com/browse/teaching-and-classroom-supplies/teachers-supplies-in-bulk/1229749_1086045_3462603_1889202",
            "label": "Bulk Teaching Supplies",
        },
        "school-arts-and-crafts": {
            "url": "https://www.walmart.com/browse/office-supplies/school-arts-crafts/1229749_1086045_1718345",
            "label": "School Arts and Crafts",
        },
        "shipping-moving": {
            "url": "https://www.walmart.com/cp/shipping-moving/2696828",
            "label": "Shipping & Moving",
        },
        "safes-lockboxes": {
            "url": "https://www.walmart.com/browse/home-safety/safes-lockboxes/1072864_1068865_1231016",
            "label": "Safes & Lockboxes",
        },
        "pens": {
            "url": "https://www.walmart.com/browse/office-supplies/pens/1229749_1988510",
            "label": "Pens",
        },
        "notebooks-pads": {
            "url": "https://www.walmart.com/browse/notebooks-pads/1229749_4796182",
            "label": "Notebooks & Pads",
        },
        "calendars-planners": {
            "url": "https://www.walmart.com/browse/office-supplies/planners/1229749_8412191",
            "label": "Calendars & Planners",
        },
        "markers-highlighters": {
            "url": "https://www.walmart.com/browse/office-supplies/markers-and-highlighters/1229749_9081741",
            "label": "Markers & Highlighters",
        },
        "paper": {
            "url": "https://www.walmart.com/browse/paper/1229749_6562796",
            "label": "Paper",
        },
        "pencils-pencil-sharpeners": {
            "url": "https://www.walmart.com/browse/office-supplies/pencils-pencil-sharpeners/1229749_9412206",
            "label": "Pencils & Pencil Sharpeners",
        },
        "school-and-office-supplies": {
            "url": "https://www.walmart.com/cp/office-supplies/1229749",
            "label": "School & Office Supplies",
        },
    },
    "arts-crafts-sewing-and-party-supplies": {
        "sewing-machines-accessories": {
            "url": "https://www.walmart.com/cp/sewing/1094704",
            "label": "Sewing Machines & Accessories",
        },
        "die-cutting": {
            "url": "https://www.walmart.com/browse/arts-crafts-sewing/die-cutting/1334134_3123463",
            "label": "Die Cutting",
        },
        "fabric": {
            "url": "https://www.walmart.com/cp/fabric/4232946",
            "label": "Fabric",
        },
        "arts-crafts-furniture-and-storage": {
            "url": "https://www.walmart.com/browse/arts-crafts-sewing/arts-crafts-furniture-and-storage/1334134_6355365",
            "label": "Arts & Crafts Furniture and Storage",
        },
        "craft-supplies": {
            "url": "https://www.walmart.com/cp/crafting/6172404",
            "label": "Craft Supplies",
        },
        "art-supplies": {
            "url": "https://www.walmart.com/cp/art-supplies/5899871",
            "label": "Art Supplies",
        },
        "knitting-crochet": {
            "url": "https://www.walmart.com/browse/arts-crafts-sewing/knitting-crochet/1334134_4880989",
            "label": "Knitting & Crochet",
        },
        "arts-crafts-for-kids": {
            "url": "https://www.walmart.com/browse/arts-crafts-for-kids/4171_645779",
            "label": "Arts & Crafts for Kids",
        },
        "beading-jewelry-making": {
            "url": "https://www.walmart.com/browse/arts-crafts-sewing/beading-jewelry-making/1334134_4533160",
            "label": "Beading & Jewelry Making",
        },
        "fabric-apparel-crafting": {
            "url": "https://www.walmart.com/browse/arts-crafts-sewing/shop-all-fabric-apparel-crafting/1334134_6172404_3659773_9445686",
            "label": "Fabric & Apparel Crafting",
        },
        "artificial-plants-and-flowers": {
            "url": "https://www.walmart.com/cp/artificial-plants-flowers/4510225",
            "label": "Artificial Plants and Flowers",
        },
        "gift-wrap": {
            "url": "https://www.walmart.com/browse/party-occasions/gift-wrap-supplies/2637_9402292",
            "label": "Gift Wrap",
        },
        "arts-crafts-sewing-and-party-supplies": {
            "url": "https://www.walmart.com/cp/arts-crafts-sewing/1334134",
            "label": "Arts, Crafts, Sewing & Party Supplies",
        },
    },
    "movies-and-tv": {
        "4k-ultra-hd-movies": {
            "url": "https://www.walmart.com/browse/4k-ultra-hd-movies/4096_3315790",
            "label": "4K Ultra HD Movies",
        },
        "blu-ray-movies": {
            "url": "https://www.walmart.com/browse/movies-tv-shows/blu-ray-movies/4096_616859",
            "label": "Blu-ray Movies",
        },
        "dvd-movies": {
            "url": "https://www.walmart.com/browse/movies-tv-shows/dvd-movies/4096_8073310_7001804",
            "label": "DVD Movies",
        },
        "4k-ultra-hd-tv-shows": {
            "url": "https://www.walmart.com/browse/movies-tv-shows/tv-shows-4k-ultra-hd/4096_6003122_2378322",
            "label": "4K Ultra HD TV Shows",
        },
        "blu-ray-tv-shows": {
            "url": "https://www.walmart.com/browse/movies-tv-shows/tv-shows-blu-ray/4096_6003122_8068379",
            "label": "Blu-ray TV Shows",
        },
        "dvd-tv-shows": {
            "url": "https://www.walmart.com/browse/movies-tv-shows/tv-shows-dvd/4096_6003122_3476135",
            "label": "DVD TV Shows",
        },
        "movies-and-tv": {
            "url": "https://www.walmart.com/cp/movies-tv/4096",
            "label": "Movies & TV",
        },
    },
    "music-and-vinyl": {
        "turntables": {
            "url": "https://www.walmart.com/browse/musical-instruments/turntables-record-players/7796869_1097690_6268144_2152355_49600",
            "label": "Turntables",
        },
        "musical-instruments": {
            "url": "https://www.walmart.com/browse/musical-instruments/7796869",
            "label": "Musical instruments",
        },
        "rap-hip-hop": {
            "url": "https://www.walmart.com/browse/music/rap-hip-hop-on-cds-vinyl/4104_4117",
            "label": "Rap & hip-hop",
        },
        "rock": {
            "url": "https://www.walmart.com/browse/music/rock-music/4104_4118",
            "label": "Rock",
        },
        "pop": {
            "url": "https://www.walmart.com/browse/music/pop-music/4104_4115",
            "label": "Pop",
        },
        "country": {
            "url": "https://www.walmart.com/browse/music/country-music/4104_4109",
            "label": "Country",
        },
        "classical": {
            "url": "https://www.walmart.com/browse/music/classical-music-on-cd-or-vinyl/4104_4108",
            "label": "Classical",
        },
        "music-and-vinyl": {
            "url": "https://www.walmart.com/cp/music/4104",
            "label": "Music & Vinyl",
        },
    },
    "books": {
        "kobo-ereaders": {
            "url": "https://www.walmart.com/browse/books/kobo-ereader-devices-accessories/3920_3252253",
            "label": "Kobo eReaders",
        },
        "childrens-books": {
            "url": "https://www.walmart.com/browse/childrens-kids-books/3920_582053",
            "label": "Children's books",
        },
        "textbooks": {
            "url": "https://www.walmart.com/browse/textbooks/3920_582377",
            "label": "Textbooks",
        },
        "teen-young-adult-books": {
            "url": "https://www.walmart.com/browse/books/teen-young-adult-books/3920_1068785",
            "label": "Teen & Young Adult books",
        },
        "magazines": {
            "url": "https://www.walmart.com/browse/books/magazines/3920_3298715",
            "label": "Magazines",
        },
        "biographies-memoires": {
            "url": "https://www.walmart.com/browse/books/biographies-memoirs/3920_5196470",
            "label": "Biographies & Memoires",
        },
        "literature-fiction": {
            "url": "https://www.walmart.com/browse/books/literature-fiction-books/3920_582105",
            "label": "Literature & Fiction",
        },
        "comics-graphic-novels": {
            "url": "https://www.walmart.com/browse/books/comic-books-graphic-novels/3920_1095293",
            "label": "Comics & Graphic Novels",
        },
        "arts-entertainment": {
            "url": "https://www.walmart.com/browse/arts-entertainment-books/3920_582321",
            "label": "Arts & Entertainment",
        },
        "cookbooks-food-wine": {
            "url": "https://www.walmart.com/browse/books/cookbooks-food-wine/3920_3036003",
            "label": "Cookbooks, Food, & Wine",
        },
        "books": {
            "url": "https://www.walmart.com/cp/Books/3920",
            "label": "Books",
        },
    },
    "seasonal-and-celebrations": {
        "baby-shower": {
            "url": "https://www.walmart.com/browse/party-occasions/baby-shower-party-supplies/2637_1042319_4687421",
            "label": "Baby Shower",
        },
        "balloons": {
            "url": "https://www.walmart.com/browse/party-occasions/balloons/2637_1042319_1212898_3956207",
            "label": "Balloons",
        },
        "balloon-arches": {
            "url": "https://www.walmart.com/browse/party-occasions/balloon-arch/2637_1042319_1212898_3956207_2139180_4860386",
            "label": "Balloon Arches",
        },
        "balloons-by-color": {
            "url": "https://www.walmart.com/browse/party-occasions/balloons-by-color/2637_1042319_1212898_3956207_6986611",
            "label": "Balloons by Color",
        },
        "birthday-party-supplies": {
            "url": "https://www.walmart.com/browse/party-occasions/birthday-party-supplies/2637_8972913_8516046",
            "label": "Birthday Party Supplies",
        },
        "gender-reveal": {
            "url": "https://www.walmart.com/browse/party-occasions/gender-reveal-party-supplies/2637_9103747",
            "label": "Gender Reveal",
        },
        "helium-tanks": {
            "url": "https://www.walmart.com/browse/party-occasions/helium-tanks/2637_1042319_1212898_4114382",
            "label": "Helium Tanks",
        },
        "themed-party-supplies": {
            "url": "https://www.walmart.com/browse/party-occasions/themed-party-supplies/2637_5817905",
            "label": "Themed Party Supplies",
        },
        "halloween": {
            "url": "https://www.walmart.com/cp/halloween/9516159",
            "label": "Halloween",
        },
        "game-day": {
            "url": "https://www.walmart.com/cp/game-day/1091906",
            "label": "Game Day",
        },
        "seasonal-and-celebrations": {
            "url": "https://www.walmart.com/cp/party-occasions/2637",
            "label": "Seasonal & Celebrations",
        },
    },
    "gift-cards": {
        "gaming-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/gaming-gift-cards/1094765_96894_8922996_9379468",
            "label": "Gaming Gift Cards",
        },
        "restaurant-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/restaurant-gift-cards/1094765_96894_8922996_8305131",
            "label": "Restaurant Gift Cards",
        },
        "retail-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/retail-gift-cards/1094765_96894_8922996_3374424",
            "label": "Retail Gift Cards",
        },
        "prepaid-gift-cards": {
            "url": "https://www.walmart.com/browse/cell-phones/phone-data-plans/1105910_4960552",
            "label": "Prepaid Gift Cards",
        },
        "entertainment-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/entertainment-gift-cards/1094765_96894_8922996_2765943",
            "label": "Entertainment Gift Cards",
        },
        "travel-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/travel-gift-cards/1094765_96894_8922996_9617007",
            "label": "Travel Gift Cards",
        },
        "lifestyle-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/lifestyle-gift-cards/1094765_96894_8922996_7573523",
            "label": "Lifestyle Gift Cards",
        },
        "plastic-gift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/walmart-plastic-gift-cards/1094765_96894_4851051_2605360_4027391",
            "label": "Plastic Gift Cards",
        },
        "egift-cards": {
            "url": "https://www.walmart.com/browse/gifts-registry/egift-cards/1094765_96894_4851051_2852534",
            "label": "eGift Cards",
        },
        "tax-exempt-program": {
            "url": "https://www.walmart.com/cp/tax-exemption-program/8480422",
            "label": "Tax Exempt Program",
        },
        "iywyk": {
            "url": "https://www.walmart.com/cp/walmart-in-the-know/7781927",
            "label": "#IYWYK",
        },
        "gift-cards": {
            "url": "https://www.walmart.com/cp/gift-cards/96894",
            "label": "Gift Cards",
        },
    },
}
