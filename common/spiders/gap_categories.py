from __future__ import annotations

"""Gap US category inventory, refreshed from the live Gap category sitemap.

Source of truth: https://www.gap.com/native-category-sitemap.xml (advertised in
https://www.gap.com/robots.txt), cross-checked against the public commerce search API
(https://api.gap.com/commerce/search/products/v2/cc?cid=<cid>) which returns a product
page for every entry below. Every ``cid`` was verified live on 2026-10-14.

The inventory is a ``{department: {leaf: {url, subcategory, department}}}`` mapping. Leaf
keys are group-qualified (``<department>-<slug>``) so the bare leaf name used as the DAG
output path cannot collide across departments. ``-a category=<department>`` still
expands to every leaf in that department through the base class parent-selector support.
"""

GAP_CATEGORIES = {
    "women": {
        "women-maternity": {
            "url": "https://www.gap.com/browse/women/maternity?cid=1127956",
            "subcategory": "maternity",
            "department": "women",
        },
        "women-new-arrivals": {
            "url": "https://www.gap.com/browse/women/new-arrivals?cid=8792",
            "subcategory": "new-arrivals",
            "department": "women",
        },
        "women-bags": {
            "url": "https://www.gap.com/browse/women/bags?cid=3046544",
            "subcategory": "bags",
            "department": "women",
        },
        "women-belts": {
            "url": "https://www.gap.com/browse/women/belts?cid=3046545",
            "subcategory": "belts",
            "department": "women",
        },
        "women-bag-charms": {
            "url": "https://www.gap.com/browse/women/bag-charms?cid=3055531",
            "subcategory": "bag-charms",
            "department": "women",
        },
        "women-socks-and-tights": {
            "url": "https://www.gap.com/browse/women/socks-and-tights?cid=3041522",
            "subcategory": "socks-and-tights",
            "department": "women",
        },
        "women-shop-all-accessories": {
            "url": "https://www.gap.com/browse/women/shop-all-accessories?cid=3041527",
            "subcategory": "shop-all-accessories",
            "department": "women",
        },
        "women-shoes": {
            "url": "https://www.gap.com/browse/women/shoes?cid=3023112",
            "subcategory": "shoes",
            "department": "women",
        },
        "women-hats": {
            "url": "https://www.gap.com/browse/women/hats?cid=3046546",
            "subcategory": "hats",
            "department": "women",
        },
        "women-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/women/cold-weather-accessories?cid=1184924",
            "subcategory": "cold-weather-accessories",
            "department": "women",
        },
        "women-sale": {
            "url": "https://www.gap.com/browse/women/sale?cid=65179",
            "subcategory": "sale",
            "department": "women",
        },
        "women-responsibly-made-shop": {
            "url": "https://www.gap.com/browse/women/responsibly-made-shop?cid=1147561",
            "subcategory": "responsibly-made-shop",
            "department": "women",
        },
        "women-cashsoft-shop": {
            "url": "https://www.gap.com/browse/women/cashsoft-shop?cid=3022755",
            "subcategory": "cashsoft-shop",
            "department": "women",
        },
        "women-jeans": {
            "url": "https://www.gap.com/browse/women/jeans?cid=5664",
            "subcategory": "jeans",
            "department": "women",
        },
        "women-gapfit-activewear": {
            "url": "https://www.gap.com/browse/women/gapfit-activewear?cid=1117374",
            "subcategory": "gapfit-activewear",
            "department": "women",
        },
        "women-dresses": {
            "url": "https://www.gap.com/browse/women/dresses?cid=13658",
            "subcategory": "dresses",
            "department": "women",
        },
        "women-shop-all-styles": {
            "url": "https://www.gap.com/browse/women/shop-all-styles?cid=1127938",
            "subcategory": "shop-all-styles",
            "department": "women",
        },
        "women-jewelry": {
            "url": "https://www.gap.com/browse/women/jewelry?cid=1192034",
            "subcategory": "jewelry",
            "department": "women",
        },
        "women-matching-sets": {
            "url": "https://www.gap.com/browse/women/matching-sets?cid=3021346",
            "subcategory": "matching-sets",
            "department": "women",
        },
        "women-shirts-and-tops": {
            "url": "https://www.gap.com/browse/women/shirts-and-tops?cid=34608",
            "subcategory": "shirts-and-tops",
            "department": "women",
        },
        "women-denim-dressing": {
            "url": "https://www.gap.com/browse/women/denim-dressing?cid=3021975",
            "subcategory": "denim-dressing",
            "department": "women",
        },
        "women-pajamas-and-loungewear": {
            "url": "https://www.gap.com/browse/women/pajamas-and-loungewear?cid=29504",
            "subcategory": "pajamas-and-loungewear",
            "department": "women",
        },
        "women-pants": {
            "url": "https://www.gap.com/browse/women/pants?cid=1011761",
            "subcategory": "pants",
            "department": "women",
        },
        "women-outerwear-and-jackets": {
            "url": "https://www.gap.com/browse/women/outerwear-and-jackets?cid=5736",
            "subcategory": "outerwear-and-jackets",
            "department": "women",
        },
        "women-sweatshirts-and-sweatpants": {
            "url": "https://www.gap.com/browse/women/sweatshirts-and-sweatpants?cid=1041168",
            "subcategory": "sweatshirts-and-sweatpants",
            "department": "women",
        },
        "women-sweaters": {
            "url": "https://www.gap.com/browse/women/sweaters?cid=5745",
            "subcategory": "sweaters",
            "department": "women",
        },
        "women-underwear": {
            "url": "https://www.gap.com/browse/women/underwear?cid=1015387",
            "subcategory": "underwear",
            "department": "women",
        },
        "women-bras": {
            "url": "https://www.gap.com/browse/women/bras?cid=34524",
            "subcategory": "bras",
            "department": "women",
        },
        "women-gapbody": {
            "url": "https://www.gap.com/browse/women/gapbody?cid=1140272",
            "subcategory": "gapbody",
            "department": "women",
        },
        "women-fall-trend-edit": {
            "url": "https://www.gap.com/browse/women/fall-trend-edit?cid=3051140",
            "subcategory": "fall-trend-edit",
            "department": "women",
        },
        "women-t-shirts-and-tanks": {
            "url": "https://www.gap.com/browse/women/t-shirts-and-tanks?cid=17076",
            "subcategory": "t-shirts-and-tanks",
            "department": "women",
        },
        "women-shorts": {
            "url": "https://www.gap.com/browse/women/shorts?cid=1041308",
            "subcategory": "shorts",
            "department": "women",
        },
        "women-skirts": {
            "url": "https://www.gap.com/browse/women/skirts?cid=1082574",
            "subcategory": "skirts",
            "department": "women",
        },
    },
    "men": {
        "men-accessories": {
            "url": "https://www.gap.com/browse/men/accessories?cid=5300",
            "subcategory": "accessories",
            "department": "men",
        },
        "men-new-arrivals": {
            "url": "https://www.gap.com/browse/men/new-arrivals?cid=11900",
            "subcategory": "new-arrivals",
            "department": "men",
        },
        "men-shorts": {
            "url": "https://www.gap.com/browse/men/shorts?cid=5156",
            "subcategory": "shorts",
            "department": "men",
        },
        "men-belts": {
            "url": "https://www.gap.com/browse/men/belts?cid=3046395",
            "subcategory": "belts",
            "department": "men",
        },
        "men-pajamas": {
            "url": "https://www.gap.com/browse/men/pajamas?cid=5270",
            "subcategory": "pajamas",
            "department": "men",
        },
        "men-sweatshirts-and-sweatpants": {
            "url": "https://www.gap.com/browse/men/sweatshirts-and-sweatpants?cid=1066503",
            "subcategory": "sweatshirts-and-sweatpants",
            "department": "men",
        },
        "men-hats": {
            "url": "https://www.gap.com/browse/men/hats?cid=3046393",
            "subcategory": "hats",
            "department": "men",
        },
        "men-bags": {
            "url": "https://www.gap.com/browse/men/bags?cid=3046394",
            "subcategory": "bags",
            "department": "men",
        },
        "men-jeans": {
            "url": "https://www.gap.com/browse/men/jeans?cid=6998",
            "subcategory": "jeans",
            "department": "men",
        },
        "men-denim-dressing": {
            "url": "https://www.gap.com/browse/men/denim-dressing?cid=3022657",
            "subcategory": "denim-dressing",
            "department": "men",
        },
        "men-coats-and-jackets": {
            "url": "https://www.gap.com/browse/men/coats-and-jackets?cid=5168",
            "subcategory": "coats-and-jackets",
            "department": "men",
        },
        "men-shop-all-styles": {
            "url": "https://www.gap.com/browse/men/shop-all-styles?cid=1127944",
            "subcategory": "shop-all-styles",
            "department": "men",
        },
        "men-sale": {
            "url": "https://www.gap.com/browse/men/sale?cid=65289",
            "subcategory": "sale",
            "department": "men",
        },
        "men-sweaters": {
            "url": "https://www.gap.com/browse/men/sweaters?cid=5180",
            "subcategory": "sweaters",
            "department": "men",
        },
        "men-underwear": {
            "url": "https://www.gap.com/browse/men/underwear?cid=3046089",
            "subcategory": "underwear",
            "department": "men",
        },
        "men-pants": {
            "url": "https://www.gap.com/browse/men/pants?cid=80799",
            "subcategory": "pants",
            "department": "men",
        },
        "men-t-shirts": {
            "url": "https://www.gap.com/browse/men/t-shirts?cid=5225",
            "subcategory": "t-shirts",
            "department": "men",
        },
        "men-shirts": {
            "url": "https://www.gap.com/browse/men/shirts?cid=15043",
            "subcategory": "shirts",
            "department": "men",
        },
        "men-gap-hill-city": {
            "url": "https://www.gap.com/browse/men/gap-hill-city?cid=3052355",
            "subcategory": "gap-hill-city",
            "department": "men",
        },
        "men-polos": {
            "url": "https://www.gap.com/browse/men/polos?cid=83056",
            "subcategory": "polos",
            "department": "men",
        },
        "men-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/men/cold-weather-accessories?cid=1046553",
            "subcategory": "cold-weather-accessories",
            "department": "men",
        },
        "men-socks": {
            "url": "https://www.gap.com/browse/men/socks?cid=3046096",
            "subcategory": "socks",
            "department": "men",
        },
        "men-cozy-shop": {
            "url": "https://www.gap.com/browse/men/cozy-shop?cid=3057496",
            "subcategory": "cozy-shop",
            "department": "men",
        },
        "men-work-shop": {
            "url": "https://www.gap.com/browse/men/work-shop?cid=1192698",
            "subcategory": "work-shop",
            "department": "men",
        },
    },
    "boys": {
        "boys-pants": {
            "url": "https://www.gap.com/browse/boys/pants?cid=6187",
            "subcategory": "pants",
            "department": "boys",
        },
        "boys-pajamas": {
            "url": "https://www.gap.com/browse/boys/pajamas?cid=9470",
            "subcategory": "pajamas",
            "department": "boys",
        },
        "boys-jeans": {
            "url": "https://www.gap.com/browse/boys/jeans?cid=6189",
            "subcategory": "jeans",
            "department": "boys",
        },
        "boys-back-to-school-shop": {
            "url": "https://www.gap.com/browse/boys/back-to-school-shop?cid=1161642",
            "subcategory": "back-to-school-shop",
            "department": "boys",
        },
        "boys-uniform-shop": {
            "url": "https://www.gap.com/browse/boys/uniform-shop?cid=1060990",
            "subcategory": "uniform-shop",
            "department": "boys",
        },
        "boys-new-arrivals": {
            "url": "https://www.gap.com/browse/boys/new-arrivals?cid=63896",
            "subcategory": "new-arrivals",
            "department": "boys",
        },
        "boys-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/boys/cold-weather-accessories?cid=3011655",
            "subcategory": "cold-weather-accessories",
            "department": "boys",
        },
        "boys-shoes": {
            "url": "https://www.gap.com/browse/boys/shoes?cid=1082280",
            "subcategory": "shoes",
            "department": "boys",
        },
        "boys-accessories": {
            "url": "https://www.gap.com/browse/boys/accessories?cid=96875",
            "subcategory": "accessories",
            "department": "boys",
        },
        "boys-bags-and-backpack": {
            "url": "https://www.gap.com/browse/boys/bags-and-backpack?cid=3046590",
            "subcategory": "bags-and-backpack",
            "department": "boys",
        },
        "boys-hats": {
            "url": "https://www.gap.com/browse/boys/hats?cid=3046592",
            "subcategory": "hats",
            "department": "boys",
        },
        "boys-shirts": {
            "url": "https://www.gap.com/browse/boys/shirts?cid=6197",
            "subcategory": "shirts",
            "department": "boys",
        },
        "boys-character-shop": {
            "url": "https://www.gap.com/browse/boys/character-shop?cid=1128444",
            "subcategory": "character-shop",
            "department": "boys",
        },
        "boys-shorts": {
            "url": "https://www.gap.com/browse/boys/shorts?cid=6191",
            "subcategory": "shorts",
            "department": "boys",
        },
        "boys-t-shirts": {
            "url": "https://www.gap.com/browse/boys/t-shirts?cid=1070923",
            "subcategory": "t-shirts",
            "department": "boys",
        },
        "boys-socks-and-underwear": {
            "url": "https://www.gap.com/browse/boys/socks-and-underwear?cid=1107335",
            "subcategory": "socks-and-underwear",
            "department": "boys",
        },
        "boys-sale": {
            "url": "https://www.gap.com/browse/boys/sale?cid=65217",
            "subcategory": "sale",
            "department": "boys",
        },
        "boys-swimsuits": {
            "url": "https://www.gap.com/browse/boys/swimsuits?cid=1075793",
            "subcategory": "swimsuits",
            "department": "boys",
        },
        "boys-joggers-and-sweatpants": {
            "url": "https://www.gap.com/browse/boys/joggers-and-sweatpants?cid=1085428",
            "subcategory": "joggers-and-sweatpants",
            "department": "boys",
        },
        "boys-matching-sets": {
            "url": "https://www.gap.com/browse/boys/matching-sets?cid=3054945",
            "subcategory": "matching-sets",
            "department": "boys",
        },
        "boys-shop-husky-s-xxl": {
            "url": "https://www.gap.com/browse/boys/shop-husky-s-xxl?cid=1050027",
            "subcategory": "shop-husky-s-xxl",
            "department": "boys",
        },
        "boys-his-favorites": {
            "url": "https://www.gap.com/browse/boys/his-favorites?cid=3051389",
            "subcategory": "his-favorites",
            "department": "boys",
        },
        "boys-sweaters": {
            "url": "https://www.gap.com/browse/boys/sweaters?cid=1175613",
            "subcategory": "sweaters",
            "department": "boys",
        },
        "boys-coats-and-jackets": {
            "url": "https://www.gap.com/browse/boys/coats-and-jackets?cid=6205",
            "subcategory": "coats-and-jackets",
            "department": "boys",
        },
        "boys-cozy-shop": {
            "url": "https://www.gap.com/browse/boys/cozy-shop?cid=1133131",
            "subcategory": "cozy-shop",
            "department": "boys",
        },
        "boys-denim-dressing": {
            "url": "https://www.gap.com/browse/boys/denim-dressing?cid=3042737",
            "subcategory": "denim-dressing",
            "department": "boys",
        },
        "boys-gapfit-and-activewear": {
            "url": "https://www.gap.com/browse/boys/gapfit-and-activewear?cid=1050851",
            "subcategory": "gapfit-and-activewear",
            "department": "boys",
        },
        "boys-sweatshirts-and-sweatpants": {
            "url": "https://www.gap.com/browse/boys/sweatshirts-and-sweatpants?cid=1117991",
            "subcategory": "sweatshirts-and-sweatpants",
            "department": "boys",
        },
        "boys-polos": {
            "url": "https://www.gap.com/browse/boys/polos?cid=3024160",
            "subcategory": "polos",
            "department": "boys",
        },
        "boys-shop-all-styles": {
            "url": "https://www.gap.com/browse/boys/shop-all-styles?cid=1127945",
            "subcategory": "shop-all-styles",
            "department": "boys",
        },
    },
    "girls": {
        "girls-uniform-shop": {
            "url": "https://www.gap.com/browse/girls/uniform-shop?cid=1061822",
            "subcategory": "uniform-shop",
            "department": "girls",
        },
        "girls-back-to-school-shop": {
            "url": "https://www.gap.com/browse/girls/back-to-school-shop?cid=1151802",
            "subcategory": "back-to-school-shop",
            "department": "girls",
        },
        "girls-new-arrivals": {
            "url": "https://www.gap.com/browse/girls/new-arrivals?cid=63895",
            "subcategory": "new-arrivals",
            "department": "girls",
        },
        "girls-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/girls/cold-weather-accessories?cid=1108132",
            "subcategory": "cold-weather-accessories",
            "department": "girls",
        },
        "girls-bags-and-backpacks": {
            "url": "https://www.gap.com/browse/girls/bags-and-backpacks?cid=3046567",
            "subcategory": "bags-and-backpacks",
            "department": "girls",
        },
        "girls-shoes": {
            "url": "https://www.gap.com/browse/girls/shoes?cid=1082288",
            "subcategory": "shoes",
            "department": "girls",
        },
        "girls-accessories": {
            "url": "https://www.gap.com/browse/girls/accessories?cid=56233",
            "subcategory": "accessories",
            "department": "girls",
        },
        "girls-hats": {
            "url": "https://www.gap.com/browse/girls/hats?cid=3046564",
            "subcategory": "hats",
            "department": "girls",
        },
        "girls-character-shop": {
            "url": "https://www.gap.com/browse/girls/character-shop?cid=1129256",
            "subcategory": "character-shop",
            "department": "girls",
        },
        "girls-socks-and-underwear": {
            "url": "https://www.gap.com/browse/girls/socks-and-underwear?cid=1107336",
            "subcategory": "socks-and-underwear",
            "department": "girls",
        },
        "girls-sweaters": {
            "url": "https://www.gap.com/browse/girls/sweaters?cid=1161843",
            "subcategory": "sweaters",
            "department": "girls",
        },
        "girls-dresses": {
            "url": "https://www.gap.com/browse/girls/dresses?cid=6300",
            "subcategory": "dresses",
            "department": "girls",
        },
        "girls-sweatshirts-and-sweatpants": {
            "url": "https://www.gap.com/browse/girls/sweatshirts-and-sweatpants?cid=1056270",
            "subcategory": "sweatshirts-and-sweatpants",
            "department": "girls",
        },
        "girls-shop-all-styles": {
            "url": "https://www.gap.com/browse/girls/shop-all-styles?cid=1127946",
            "subcategory": "shop-all-styles",
            "department": "girls",
        },
        "girls-rompers-and-jumpsuits": {
            "url": "https://www.gap.com/browse/girls/rompers-and-jumpsuits?cid=1141739",
            "subcategory": "rompers-and-jumpsuits",
            "department": "girls",
        },
        "girls-jeans": {
            "url": "https://www.gap.com/browse/girls/jeans?cid=6276",
            "subcategory": "jeans",
            "department": "girls",
        },
        "girls-cozy-shop": {
            "url": "https://www.gap.com/browse/girls/cozy-shop?cid=1135179",
            "subcategory": "cozy-shop",
            "department": "girls",
        },
        "girls-coats-and-jackets": {
            "url": "https://www.gap.com/browse/girls/coats-and-jackets?cid=6303",
            "subcategory": "coats-and-jackets",
            "department": "girls",
        },
        "girls-t-shirts": {
            "url": "https://www.gap.com/browse/girls/t-shirts?cid=14417",
            "subcategory": "t-shirts",
            "department": "girls",
        },
        "girls-matching-sets": {
            "url": "https://www.gap.com/browse/girls/matching-sets?cid=1189408",
            "subcategory": "matching-sets",
            "department": "girls",
        },
        "girls-pajamas": {
            "url": "https://www.gap.com/browse/girls/pajamas?cid=6323",
            "subcategory": "pajamas",
            "department": "girls",
        },
        "girls-skirts": {
            "url": "https://www.gap.com/browse/girls/skirts?cid=3024180",
            "subcategory": "skirts",
            "department": "girls",
        },
        "girls-favorites": {
            "url": "https://www.gap.com/browse/girls/favorites?cid=3051457",
            "subcategory": "favorites",
            "department": "girls",
        },
        "girls-pants": {
            "url": "https://www.gap.com/browse/girls/pants?cid=13148",
            "subcategory": "pants",
            "department": "girls",
        },
        "girls-swimsuits": {
            "url": "https://www.gap.com/browse/girls/swimsuits?cid=1075777",
            "subcategory": "swimsuits",
            "department": "girls",
        },
        "girls-denim-dressing": {
            "url": "https://www.gap.com/browse/girls/denim-dressing?cid=3042736",
            "subcategory": "denim-dressing",
            "department": "girls",
        },
        "girls-shirts-and-tops": {
            "url": "https://www.gap.com/browse/girls/shirts-and-tops?cid=1153699",
            "subcategory": "shirts-and-tops",
            "department": "girls",
        },
        "girls-sale": {
            "url": "https://www.gap.com/browse/girls/sale?cid=65194",
            "subcategory": "sale",
            "department": "girls",
        },
        "girls-shorts": {
            "url": "https://www.gap.com/browse/girls/shorts?cid=14403",
            "subcategory": "shorts",
            "department": "girls",
        },
    },
    "baby-and-toddler": {
        "baby-and-toddler-new-arrivals-for-baby": {
            "url": "https://www.gap.com/browse/baby-and-toddler/new-arrivals-for-baby?cid=63863",
            "subcategory": "new-arrivals-for-baby",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-new-arrivals-for-him": {
            "url": "https://www.gap.com/browse/baby-and-toddler/new-arrivals-for-him?cid=95575",
            "subcategory": "new-arrivals-for-him",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-new-arrivals-for-her": {
            "url": "https://www.gap.com/browse/baby-and-toddler/new-arrivals-for-her?cid=14249",
            "subcategory": "new-arrivals-for-her",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-toys-and-gifts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/toys-and-gifts?cid=3018073",
            "subcategory": "toys-and-gifts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-furniture-and-decor": {
            "url": "https://www.gap.com/browse/baby-and-toddler/furniture-and-decor?cid=3018070",
            "subcategory": "furniture-and-decor",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-gear": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-gear?cid=3018072",
            "subcategory": "baby-gear",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-shop-all-accessories-baby-and-toddler": {
            "url": "https://www.gap.com/browse/baby-and-toddler/shop-all-accessories-baby-and-toddler?cid=3057152",
            "subcategory": "shop-all-accessories-baby-and-toddler",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-coats-jackets": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-coats-jackets?cid=8770",
            "subcategory": "girl-coats-jackets",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-pajamas": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-pajamas?cid=95697",
            "subcategory": "baby-pajamas",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-outfits-sets": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-outfits-sets?cid=1188469",
            "subcategory": "girl-outfits-sets",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-sweatshirts-sweatpants": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-sweatshirts-sweatpants?cid=17846",
            "subcategory": "girl-sweatshirts-sweatpants",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-newborn-essentials": {
            "url": "https://www.gap.com/browse/baby-and-toddler/newborn-essentials?cid=1027221",
            "subcategory": "newborn-essentials",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-shorts-skirts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-shorts-skirts?cid=1121815",
            "subcategory": "girl-shorts-skirts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-coats-jackets": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-coats-jackets?cid=1016108",
            "subcategory": "boy-coats-jackets",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-sweatshirts-and-sweatpant": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-sweatshirts-and-sweatpant?cid=1016107",
            "subcategory": "boy-sweatshirts-and-sweatpant",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-socks-underwear": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-socks-underwear?cid=1034157",
            "subcategory": "boy-socks-underwear",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-pajamas": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-pajamas?cid=1016109",
            "subcategory": "boy-pajamas",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-outfits-sets": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-outfits-sets?cid=1188470",
            "subcategory": "boy-outfits-sets",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-sale": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-sale?cid=3054525",
            "subcategory": "baby-sale",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-pants": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-pants?cid=1016106",
            "subcategory": "boy-pants",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-jeans": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-jeans?cid=6359",
            "subcategory": "boy-jeans",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-shorts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-shorts?cid=1102201",
            "subcategory": "baby-shorts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-halloween-shop": {
            "url": "https://www.gap.com/browse/baby-and-toddler/halloween-shop?cid=1068469",
            "subcategory": "halloween-shop",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-sale": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-sale?cid=65263",
            "subcategory": "girl-sale",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-bodysuits": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-bodysuits?cid=95598",
            "subcategory": "baby-bodysuits",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-one-pieces": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-one-pieces?cid=1027203",
            "subcategory": "baby-one-pieces",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-gifts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-gifts?cid=1055119",
            "subcategory": "baby-gifts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-sweaters": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-sweaters?cid=1175810",
            "subcategory": "baby-sweaters",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-leggings-pants": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-leggings-pants?cid=12378",
            "subcategory": "girl-leggings-pants",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-shorts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-shorts?cid=1121839",
            "subcategory": "boy-shorts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-toddler-boy-multi-packs": {
            "url": "https://www.gap.com/browse/baby-and-toddler/toddler-boy-multi-packs?cid=3034885",
            "subcategory": "toddler-boy-multi-packs",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-toddler-girl-multi-packs": {
            "url": "https://www.gap.com/browse/baby-and-toddler/toddler-girl-multi-packs?cid=3034884",
            "subcategory": "toddler-girl-multi-packs",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-sweatshirts-and-sweatpants": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-sweatshirts-and-sweatpants?cid=3041729",
            "subcategory": "baby-sweatshirts-and-sweatpants",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-swimsuits": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-swimsuits?cid=1072981",
            "subcategory": "girl-swimsuits",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-swimsuits": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-swimsuits?cid=1072982",
            "subcategory": "boy-swimsuits",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-mix-match": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-mix-match?cid=1059829",
            "subcategory": "girl-mix-match",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-mix-match": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-mix-match?cid=1059828",
            "subcategory": "boy-mix-match",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-bottoms": {
            "url": "https://www.gap.com/browse/baby-and-toddler/bottoms?cid=7191",
            "subcategory": "bottoms",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-polos": {
            "url": "https://www.gap.com/browse/baby-and-toddler/polos?cid=3024164",
            "subcategory": "polos",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-boy-shop-all-styles": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-boy-shop-all-styles?cid=1127948",
            "subcategory": "baby-boy-shop-all-styles",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-shirts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-shirts?cid=1016169",
            "subcategory": "boy-shirts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-nursery": {
            "url": "https://www.gap.com/browse/baby-and-toddler/nursery?cid=3010841",
            "subcategory": "nursery",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-girl-shop-all-styles": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-girl-shop-all-styles?cid=1127947",
            "subcategory": "baby-girl-shop-all-styles",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-t-shirts-graphics": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-t-shirts-graphics?cid=1016096",
            "subcategory": "boy-t-shirts-graphics",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-gap-x-disney": {
            "url": "https://www.gap.com/browse/baby-and-toddler/gap-x-disney?cid=1192771",
            "subcategory": "gap-x-disney",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-brannan-bear-collection": {
            "url": "https://www.gap.com/browse/baby-and-toddler/brannan-bear-collection?cid=3056215",
            "subcategory": "brannan-bear-collection",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-shoes-and-accessories": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-shoes-and-accessories?cid=3054558",
            "subcategory": "boy-shoes-and-accessories",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-shop-all-styles": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-shop-all-styles?cid=1127952",
            "subcategory": "girl-shop-all-styles",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-jeans": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-jeans?cid=6427",
            "subcategory": "girl-jeans",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-shop-all-styles": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-shop-all-styles?cid=1127955",
            "subcategory": "boy-shop-all-styles",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-multi-packs": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-multi-packs?cid=1146519",
            "subcategory": "baby-multi-packs",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-outfit-sets": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-outfit-sets?cid=1098333",
            "subcategory": "baby-outfit-sets",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-t-shirts": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-t-shirts?cid=6444",
            "subcategory": "girl-t-shirts",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-tops": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-tops?cid=1132758",
            "subcategory": "girl-tops",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-dresses": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-dresses?cid=6436",
            "subcategory": "girl-dresses",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-girl-dresses": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-girl-dresses?cid=6437",
            "subcategory": "baby-girl-dresses",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-swimsuits": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-swimsuits?cid=1120931",
            "subcategory": "baby-swimsuits",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-pajamas": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-pajamas?cid=76918",
            "subcategory": "girl-pajamas",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-cozy-shop": {
            "url": "https://www.gap.com/browse/baby-and-toddler/cozy-shop?cid=1138346",
            "subcategory": "cozy-shop",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-sweaters": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-sweaters?cid=1175977",
            "subcategory": "girl-sweaters",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-socks-underwear": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-socks-underwear?cid=1033898",
            "subcategory": "girl-socks-underwear",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-sweaters": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-sweaters?cid=1175972",
            "subcategory": "boy-sweaters",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-my-first-denim": {
            "url": "https://www.gap.com/browse/baby-and-toddler/my-first-denim?cid=1133690",
            "subcategory": "my-first-denim",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-denim-dressing": {
            "url": "https://www.gap.com/browse/baby-and-toddler/denim-dressing?cid=3042738",
            "subcategory": "denim-dressing",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-shoes-accessories": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-shoes-accessories?cid=1086661",
            "subcategory": "baby-shoes-accessories",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-sale": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-sale?cid=65236",
            "subcategory": "boy-sale",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-cold-weather-accessories?cid=3040428",
            "subcategory": "girl-cold-weather-accessories",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-cold-weather-accessories?cid=3040427",
            "subcategory": "baby-cold-weather-accessories",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-boy-cold-weather-accessories": {
            "url": "https://www.gap.com/browse/baby-and-toddler/boy-cold-weather-accessories?cid=3040429",
            "subcategory": "boy-cold-weather-accessories",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-baby-coats-jackets": {
            "url": "https://www.gap.com/browse/baby-and-toddler/baby-coats-jackets?cid=1108608",
            "subcategory": "baby-coats-jackets",
            "department": "baby-and-toddler",
        },
        "baby-and-toddler-girl-shoes-and-accessories": {
            "url": "https://www.gap.com/browse/baby-and-toddler/girl-shoes-and-accessories?cid=3054541",
            "subcategory": "girl-shoes-and-accessories",
            "department": "baby-and-toddler",
        },
    },
    "maternity": {
        "maternity-shorts": {
            "url": "https://www.gap.com/browse/maternity/shorts?cid=1025764",
            "subcategory": "shorts",
            "department": "maternity",
        },
        "maternity-sweaters": {
            "url": "https://www.gap.com/browse/maternity/sweaters?cid=1019160",
            "subcategory": "sweaters",
            "department": "maternity",
        },
        "maternity-maternity-essentials": {
            "url": "https://www.gap.com/browse/maternity/maternity-essentials?cid=1020890",
            "subcategory": "maternity-essentials",
            "department": "maternity",
        },
        "maternity-jeans": {
            "url": "https://www.gap.com/browse/maternity/jeans?cid=6013",
            "subcategory": "jeans",
            "department": "maternity",
        },
        "maternity-sale": {
            "url": "https://www.gap.com/browse/maternity/sale?cid=65302",
            "subcategory": "sale",
            "department": "maternity",
        },
        "maternity-skirts": {
            "url": "https://www.gap.com/browse/maternity/skirts?cid=3026780",
            "subcategory": "skirts",
            "department": "maternity",
        },
        "maternity-activewear": {
            "url": "https://www.gap.com/browse/maternity/activewear?cid=1050384",
            "subcategory": "activewear",
            "department": "maternity",
        },
        "maternity-nursing": {
            "url": "https://www.gap.com/browse/maternity/nursing?cid=1023948",
            "subcategory": "nursing",
            "department": "maternity",
        },
        "maternity-bestsellers": {
            "url": "https://www.gap.com/browse/maternity/bestsellers?cid=3026100",
            "subcategory": "bestsellers",
            "department": "maternity",
        },
        "maternity-coordinating-shop": {
            "url": "https://www.gap.com/browse/maternity/coordinating-shop?cid=3026102",
            "subcategory": "coordinating-shop",
            "department": "maternity",
        },
        "maternity-shoes-and-accessories": {
            "url": "https://www.gap.com/browse/maternity/shoes-and-accessories?cid=1088548",
            "subcategory": "shoes-and-accessories",
            "department": "maternity",
        },
        "maternity-dresses": {
            "url": "https://www.gap.com/browse/maternity/dresses?cid=1008565",
            "subcategory": "dresses",
            "department": "maternity",
        },
        "maternity-babymoon-shop": {
            "url": "https://www.gap.com/browse/maternity/babymoon-shop?cid=3016031",
            "subcategory": "babymoon-shop",
            "department": "maternity",
        },
        "maternity-t-shirts-and-tanks": {
            "url": "https://www.gap.com/browse/maternity/t-shirts-and-tanks?cid=6049",
            "subcategory": "t-shirts-and-tanks",
            "department": "maternity",
        },
        "maternity-pajamas-and-loungewear": {
            "url": "https://www.gap.com/browse/maternity/pajamas-and-loungewear?cid=1021874",
            "subcategory": "pajamas-and-loungewear",
            "department": "maternity",
        },
        "maternity-hospital-checklist": {
            "url": "https://www.gap.com/browse/maternity/hospital-checklist?cid=3020244",
            "subcategory": "hospital-checklist",
            "department": "maternity",
        },
        "maternity-bras-undies-and-more": {
            "url": "https://www.gap.com/browse/maternity/bras-undies-and-more?cid=1020009",
            "subcategory": "bras-undies-and-more",
            "department": "maternity",
        },
        "maternity-shirts": {
            "url": "https://www.gap.com/browse/maternity/shirts?cid=1014424",
            "subcategory": "shirts",
            "department": "maternity",
        },
        "maternity-pants": {
            "url": "https://www.gap.com/browse/maternity/pants?cid=1014425",
            "subcategory": "pants",
            "department": "maternity",
        },
        "maternity-shop-by-trimester": {
            "url": "https://www.gap.com/browse/maternity/shop-by-trimester?cid=1175142",
            "subcategory": "shop-by-trimester",
            "department": "maternity",
        },
    },
    "new": {
        "new-gapstudio": {
            "url": "https://www.gap.com/browse/new/gapstudio?cid=3045197",
            "subcategory": "gapstudio",
            "department": "new",
        },
        "new-family-matching-pjs": {
            "url": "https://www.gap.com/browse/new/family-matching-pjs?cid=1072174",
            "subcategory": "family-matching-pjs",
            "department": "new",
        },
        "new-nfl-collection": {
            "url": "https://www.gap.com/browse/new/nfl-collection?cid=3052354",
            "subcategory": "nfl-collection",
            "department": "new",
        },
        "new-logo-shop": {
            "url": "https://www.gap.com/browse/new/logo-shop?cid=1173983",
            "subcategory": "logo-shop",
            "department": "new",
        },
        "new-cozy-shop": {
            "url": "https://www.gap.com/browse/new/cozy-shop?cid=3022957",
            "subcategory": "cozy-shop",
            "department": "new",
        },
        "new-gapvintage": {
            "url": "https://www.gap.com/browse/new/gapvintage?cid=3030341",
            "subcategory": "gapvintage",
            "department": "new",
        },
        "new-get-blue-collection": {
            "url": "https://www.gap.com/browse/new/get-blue-collection?cid=3055063",
            "subcategory": "get-blue-collection",
            "department": "new",
        },
        "new-fall-denim-shop": {
            "url": "https://www.gap.com/browse/new/fall-denim-shop?cid=3056440",
            "subcategory": "fall-denim-shop",
            "department": "new",
        },
    },
    "gapx": {
        "gapx-gap-malbon": {
            "url": "https://www.gap.com/browse/gapx/gap-malbon?cid=3047264",
            "subcategory": "gap-malbon",
            "department": "gapx",
        },
        "gapx-los-tacos-no-1-collection": {
            "url": "https://www.gap.com/browse/gapx/los-tacos-no-1-collection?cid=3055939",
            "subcategory": "los-tacos-no-1-collection",
            "department": "gapx",
        },
        "gapx-gap-x-whitney-lichtenstein-collection": {
            "url": "https://www.gap.com/browse/gapx/gap-x-whitney-lichtenstein-collection?cid=3057767",
            "subcategory": "gap-x-whitney-lichtenstein-collection",
            "department": "gapx",
        },
        "gapx-simpsons-collection": {
            "url": "https://www.gap.com/browse/gapx/simpsons-collection?cid=3057525",
            "subcategory": "simpsons-collection",
            "department": "gapx",
        },
        "gapx-gap-a-p-c": {
            "url": "https://www.gap.com/browse/gapx/gap-a-p-c?cid=3056788",
            "subcategory": "gap-a-p-c",
            "department": "gapx",
        },
        "gapx-sesame-street-collection": {
            "url": "https://www.gap.com/browse/gapx/sesame-street-collection?cid=3056723",
            "subcategory": "sesame-street-collection",
            "department": "gapx",
        },
    },
    "matching": {
        "matching-destination-lets-coordinate": {
            "url": "https://www.gap.com/browse/matching/destination-lets-coordinate?cid=1070833",
            "subcategory": "destination-lets-coordinate",
            "department": "matching",
        },
        "matching-disney-shop": {
            "url": "https://www.gap.com/browse/matching/disney-shop?cid=1192757",
            "subcategory": "disney-shop",
            "department": "matching",
        },
        "matching-star-wars-shop": {
            "url": "https://www.gap.com/browse/matching/star-wars-shop?cid=3011173",
            "subcategory": "star-wars-shop",
            "department": "matching",
        },
    },
    "vacation-shop": {
        "vacation-shop-shorts": {
            "url": "https://www.gap.com/browse/vacation-shop/shorts?cid=3016445",
            "subcategory": "shorts",
            "department": "vacation-shop",
        },
        "vacation-shop-t-shirts-and-tanks": {
            "url": "https://www.gap.com/browse/vacation-shop/t-shirts-and-tanks?cid=3016448",
            "subcategory": "t-shirts-and-tanks",
            "department": "vacation-shop",
        },
        "vacation-shop-swim": {
            "url": "https://www.gap.com/browse/vacation-shop/swim?cid=3016446",
            "subcategory": "swim",
            "department": "vacation-shop",
        },
        "vacation-shop-dresses": {
            "url": "https://www.gap.com/browse/vacation-shop/dresses?cid=3016447",
            "subcategory": "dresses",
            "department": "vacation-shop",
        },
        "vacation-shop-destination-summer-party": {
            "url": "https://www.gap.com/browse/vacation-shop/destination-summer-party?cid=3016450",
            "subcategory": "destination-summer-party",
            "department": "vacation-shop",
        },
    },
    "gift-shop": {
        "gift-shop-party-shop": {
            "url": "https://www.gap.com/browse/gift-shop/party-shop?cid=3011561",
            "subcategory": "party-shop",
            "department": "gift-shop",
        },
        "gift-shop-gift-shop": {
            "url": "https://www.gap.com/browse/gift-shop/gift-shop?cid=3024953",
            "subcategory": "gift-shop",
            "department": "gift-shop",
        },
    },
}
