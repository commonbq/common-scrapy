"""Macy's complete storefront category inventory.

Captured 2026-10-14 and re-verified 2026-10-18 from the header mega-menu
flyouts serialized into the homepage HTML (one ``flyout-container`` per
department, each an ordered list of
``https://www.macys.com/shop/<path>?id=<categoryId>`` anchors). The four generic
``/shop/brands`` index links and every facet/refinement anchor (uppercase, ``%``,
``|`` or ``,`` in the path) are dropped; the 858-link ``Sale`` flyout is a promo
surface, not a taxonomy, and is excluded.

Grouped ``{department: {leaf: {url, id}}}`` mapping as required by the base
listing spider contract. ``leaf`` is the full ``/shop``-relative path slug, so the
many labels that recur across departments (``womens-shoes``, ``home-area-rugs``,
``new-trending-*``) stay globally unique for the DAG output paths. ``id`` is the
category id the spider passes to ``/xapi/discover/v1/page``; ``url`` is the
canonical id-bearing storefront URL.
"""

MACYS_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {
    "Women": {
        "womens-clothing": {
            "url": "https://www.macys.com/shop/womens/clothing?id=188851",
            "id": "188851",
        },
        "womens-clothing-activewear": {
            "url": "https://www.macys.com/shop/womens/clothing/activewear?id=29891",
            "id": "29891",
        },
        "womens-clothing-blazers": {
            "url": "https://www.macys.com/shop/womens/clothing/blazers?id=55429",
            "id": "55429",
        },
        "womens-clothing-intimates": {
            "url": "https://www.macys.com/shop/womens/clothing/intimates?id=59459",
            "id": "59459",
        },
        "womens-clothing-sweaters-cashmere": {
            "url": "https://www.macys.com/shop/womens/clothing/sweaters/cashmere?id=262",
            "id": "262",
        },
        "womens-clothing-coats": {
            "url": "https://www.macys.com/shop/womens/clothing/coats?id=269",
            "id": "269",
        },
        "womens-clothing-dresses": {
            "url": "https://www.macys.com/shop/womens/clothing/dresses?id=5449",
            "id": "5449",
        },
        "womens-clothing-hoodies-sweatshirts": {
            "url": "https://www.macys.com/shop/womens/clothing/hoodies-sweatshirts?id=293359",
            "id": "293359",
        },
        "womens-clothing-jeans": {
            "url": "https://www.macys.com/shop/womens/clothing/jeans?id=3111",
            "id": "3111",
        },
        "womens-clothing-jumpsuits": {
            "url": "https://www.macys.com/shop/womens/clothing/jumpsuits?id=50684",
            "id": "50684",
        },
        "womens-clothing-pajamas": {
            "url": "https://www.macys.com/shop/womens/clothing/pajamas?id=59737",
            "id": "59737",
        },
        "womens-clothing-pants": {
            "url": "https://www.macys.com/shop/womens/clothing/pants?id=157",
            "id": "157",
        },
        "womens-clothing-shorts": {
            "url": "https://www.macys.com/shop/womens/clothing/shorts?id=5344",
            "id": "5344",
        },
        "womens-clothing-skirts": {
            "url": "https://www.macys.com/shop/womens/clothing/skirts?id=131",
            "id": "131",
        },
        "womens-clothing-suits": {
            "url": "https://www.macys.com/shop/womens/clothing/suits?id=67592",
            "id": "67592",
        },
        "womens-clothing-sweaters": {
            "url": "https://www.macys.com/shop/womens/clothing/sweaters?id=260",
            "id": "260",
        },
        "womens-clothing-swimwear": {
            "url": "https://www.macys.com/shop/womens/clothing/swimwear?id=8699",
            "id": "8699",
        },
        "womens-clothing-tops": {
            "url": "https://www.macys.com/shop/womens/clothing/tops?id=255",
            "id": "255",
        },
        "womens-clothing-plus-size": {
            "url": "https://www.macys.com/shop/womens/clothing/plus-size?id=188853",
            "id": "188853",
        },
        "womens-clothing-petites": {
            "url": "https://www.macys.com/shop/womens/clothing/petites?id=188854",
            "id": "188854",
        },
        "womens-clothing-junior-teen": {
            "url": "https://www.macys.com/shop/womens/clothing/junior-teen?id=60983",
            "id": "60983",
        },
        "womens-clothing-maternity": {
            "url": "https://www.macys.com/shop/womens/clothing/maternity?id=66718",
            "id": "66718",
        },
        "womens-clothing-dresses-occasion": {
            "url": "https://www.macys.com/shop/womens/clothing/dresses/occasion?id=221092",
            "id": "221092",
        },
        "womens-clothing-dresses-formal": {
            "url": "https://www.macys.com/shop/womens/clothing/dresses/formal?id=339414",
            "id": "339414",
        },
        "womens-clothing-dresses-cocktail-party": {
            "url": "https://www.macys.com/shop/womens/clothing/dresses/cocktail-party?id=339107",
            "id": "339107",
        },
        "womens-clothing-dresses-occasion-wedding-guest": {
            "url": "https://www.macys.com/shop/womens/clothing/dresses/occasion/wedding-guest?id=280756",
            "id": "280756",
        },
        "womens-clothing-junior-teen-dresses-homecoming": {
            "url": "https://www.macys.com/shop/womens/clothing/junior-teen/dresses/homecoming?id=197151",
            "id": "197151",
        },
        "womens-clothing-dresses-seasonal-fall": {
            "url": "https://www.macys.com/shop/womens/clothing/dresses/seasonal/fall?id=339475",
            "id": "339475",
        },
        "womens-shoes": {
            "url": "https://www.macys.com/shop/womens/shoes?id=56233",
            "id": "56233",
        },
        "womens-handbags-wallets-accessories": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories?id=26846",
            "id": "26846",
        },
        "new-trending-new-arrivals-womens": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/womens?id=357988",
            "id": "357988",
        },
        "womens-contemporary-clothing": {
            "url": "https://www.macys.com/shop/womens/contemporary-clothing?id=315756",
            "id": "315756",
        },
        "new-trending-fall-womens-asymmetry": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/asymmetry?id=374376",
            "id": "374376",
        },
        "new-trending-fall-womens-tailored-separates": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/tailored-separates?id=374382",
            "id": "374382",
        },
        "new-trending-fall-womens-voluminous-denim": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/voluminous-denim?id=380167",
            "id": "380167",
        },
        "new-trending-fall-womens-wild-animal": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/wild-animal?id=374384",
            "id": "374384",
        },
        "womens-clothing-jeans-denim-guide-for-her": {
            "url": "https://www.macys.com/shop/womens/clothing/jeans/denim-guide-for-her?id=376268",
            "id": "376268",
        },
        "womens-trends-pre-loved": {
            "url": "https://www.macys.com/shop/womens/trends/pre-loved?id=384082",
            "id": "384082",
        },
        "womens-designer-clothes": {
            "url": "https://www.macys.com/shop/womens/designer-clothes?id=85842",
            "id": "85842",
        },
        "womens-occasion-wedding": {
            "url": "https://www.macys.com/shop/womens/occasion/wedding?id=260270",
            "id": "260270",
        },
        "womens-occasion-workwear": {
            "url": "https://www.macys.com/shop/womens/occasion/workwear?id=39096",
            "id": "39096",
        },
        "sale-limited-time-specials-womens-clothing": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/womens/clothing?id=131745",
            "id": "131745",
        },
        "sale-by-category-womens": {
            "url": "https://www.macys.com/shop/sale/by-category/womens?id=10066",
            "id": "10066",
        },
    },
    "Men": {
        "mens-clothing": {
            "url": "https://www.macys.com/shop/mens/clothing?id=197651",
            "id": "197651",
        },
        "mens-clothing-activewear": {
            "url": "https://www.macys.com/shop/mens/clothing/activewear?id=3296",
            "id": "3296",
        },
        "mens-clothing-blazers-sport-coats": {
            "url": "https://www.macys.com/shop/mens/clothing/blazers-sport-coats?id=16499",
            "id": "16499",
        },
        "mens-clothing-coats": {
            "url": "https://www.macys.com/shop/mens/clothing/coats?id=3763",
            "id": "3763",
        },
        "mens-clothing-shirts-dress-shirts": {
            "url": "https://www.macys.com/shop/mens/clothing/shirts/dress-shirts?id=20635",
            "id": "20635",
        },
        "mens-clothing-sweatshirts": {
            "url": "https://www.macys.com/shop/mens/clothing/sweatshirts?id=25995",
            "id": "25995",
        },
        "mens-clothing-jeans": {
            "url": "https://www.macys.com/shop/mens/clothing/jeans?id=11221",
            "id": "11221",
        },
        "mens-clothing-pajamas": {
            "url": "https://www.macys.com/shop/mens/clothing/pajamas?id=16295",
            "id": "16295",
        },
        "mens-clothing-pants": {
            "url": "https://www.macys.com/shop/mens/clothing/pants?id=89",
            "id": "89",
        },
        "mens-clothing-shirts-polos": {
            "url": "https://www.macys.com/shop/mens/clothing/shirts/polos?id=20640",
            "id": "20640",
        },
        "mens-clothing-shirts": {
            "url": "https://www.macys.com/shop/mens/clothing/shirts?id=20626",
            "id": "20626",
        },
        "mens-clothing-shorts": {
            "url": "https://www.macys.com/shop/mens/clothing/shorts?id=3310",
            "id": "3310",
        },
        "mens-clothing-suits": {
            "url": "https://www.macys.com/shop/mens/clothing/suits?id=17788",
            "id": "17788",
        },
        "mens-clothing-sweaters": {
            "url": "https://www.macys.com/shop/mens/clothing/sweaters?id=4286",
            "id": "4286",
        },
        "mens-clothing-swimwear": {
            "url": "https://www.macys.com/shop/mens/clothing/swimwear?id=3291",
            "id": "3291",
        },
        "mens-clothing-underwear": {
            "url": "https://www.macys.com/shop/mens/clothing/underwear?id=57",
            "id": "57",
        },
        "mens-clothing-big-and-tall": {
            "url": "https://www.macys.com/shop/mens/clothing/big-and-tall?id=45758",
            "id": "45758",
        },
        "mens-shoes": {
            "url": "https://www.macys.com/shop/mens/shoes?id=55822",
            "id": "55822",
        },
        "mens-shoes-athletic-sneakers": {
            "url": "https://www.macys.com/shop/mens/shoes/athletic-sneakers?id=55642",
            "id": "55642",
        },
        "mens-shoes-boots": {
            "url": "https://www.macys.com/shop/mens/shoes/boots?id=55637",
            "id": "55637",
        },
        "mens-shoes-dress": {
            "url": "https://www.macys.com/shop/mens/shoes/dress?id=70405",
            "id": "70405",
        },
        "mens-shoes-dress-loafers-drivers": {
            "url": "https://www.macys.com/shop/mens/shoes/dress/loafers-drivers?id=79687",
            "id": "79687",
        },
        "mens-accessories": {
            "url": "https://www.macys.com/shop/mens/accessories?id=47665",
            "id": "47665",
        },
        "mens-accessories-bags": {
            "url": "https://www.macys.com/shop/mens/accessories/bags?id=45016",
            "id": "45016",
        },
        "mens-accessories-belts": {
            "url": "https://www.macys.com/shop/mens/accessories/belts?id=47673",
            "id": "47673",
        },
        "mens-accessories-hats": {
            "url": "https://www.macys.com/shop/mens/accessories/hats?id=176642",
            "id": "176642",
        },
        "mens-accessories-ties": {
            "url": "https://www.macys.com/shop/mens/accessories/ties?id=53239",
            "id": "53239",
        },
        "mens-accessories-sunglasses": {
            "url": "https://www.macys.com/shop/mens/accessories/sunglasses?id=58262",
            "id": "58262",
        },
        "mens-cologne-grooming": {
            "url": "https://www.macys.com/shop/mens/cologne-grooming?id=392472",
            "id": "392472",
        },
        "new-trending-new-arrivals-mens": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/mens?id=357989",
            "id": "357989",
        },
        "mens-contemporary-clothing": {
            "url": "https://www.macys.com/shop/mens/contemporary-clothing?id=315757",
            "id": "315757",
        },
        "new-trending-fall-mens-leather-suede": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/leather-suede?id=179487",
            "id": "179487",
        },
        "new-trending-fall-mens-chunky-knits": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/chunky-knits?id=374467",
            "id": "374467",
        },
        "mens-clothing-coats-overcoats": {
            "url": "https://www.macys.com/shop/mens/clothing/coats/overcoats?id=302764",
            "id": "302764",
        },
        "new-trending-fall-mens-relaxed-denim": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/relaxed-denim?id=360168",
            "id": "360168",
        },
        "mens-clothing-business-casual": {
            "url": "https://www.macys.com/shop/mens/clothing/business-casual?id=75897",
            "id": "75897",
        },
        "mens-clothing-sweaters-cashmere": {
            "url": "https://www.macys.com/shop/mens/clothing/sweaters/cashmere?id=339911",
            "id": "339911",
        },
        "mens-accessories-cold-weather": {
            "url": "https://www.macys.com/shop/mens/accessories/cold-weather?id=47677",
            "id": "47677",
        },
        "mens-clothing-jeans-denim-guide-for-him": {
            "url": "https://www.macys.com/shop/mens/clothing/jeans/denim-guide-for-him?id=379267",
            "id": "379267",
        },
        "mens-occasion-golf": {
            "url": "https://www.macys.com/shop/mens/occasion/golf?id=367470",
            "id": "367470",
        },
        "mens-occasion-wedding": {
            "url": "https://www.macys.com/shop/mens/occasion/wedding?id=209658",
            "id": "209658",
        },
        "sale-limited-time-specials-limited-time-specials-men": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/limited-time-specials-men?id=143444",
            "id": "143444",
        },
        "sale-great-shoe-sale-mens": {
            "url": "https://www.macys.com/shop/sale/great-shoe-sale/mens?id=65449",
            "id": "65449",
        },
        "sale-by-category-mens": {
            "url": "https://www.macys.com/shop/sale/by-category/mens?id=9559",
            "id": "9559",
        },
    },
    "Beauty": {
        "beauty-fragrance": {
            "url": "https://www.macys.com/shop/beauty/fragrance?id=277259",
            "id": "277259",
        },
        "beauty-fragrance-perfume": {
            "url": "https://www.macys.com/shop/beauty/fragrance/perfume?id=30087",
            "id": "30087",
        },
        "mens-cologne-grooming-cologne": {
            "url": "https://www.macys.com/shop/mens/cologne-grooming/cologne?id=30088",
            "id": "30088",
        },
        "beauty-makeup": {
            "url": "https://www.macys.com/shop/beauty/makeup?id=30077",
            "id": "30077",
        },
        "beauty-makeup-face": {
            "url": "https://www.macys.com/shop/beauty/makeup/face?id=30521",
            "id": "30521",
        },
        "beauty-makeup-eye": {
            "url": "https://www.macys.com/shop/beauty/makeup/eye?id=30520",
            "id": "30520",
        },
        "beauty-makeup-lip": {
            "url": "https://www.macys.com/shop/beauty/makeup/lip?id=30522",
            "id": "30522",
        },
        "beauty-makeup-brushes-tools": {
            "url": "https://www.macys.com/shop/beauty/makeup/brushes-tools?id=56285",
            "id": "56285",
        },
        "beauty-skin-care": {
            "url": "https://www.macys.com/shop/beauty/skin-care?id=30078",
            "id": "30078",
        },
        "beauty-skin-care-moisturizers": {
            "url": "https://www.macys.com/shop/beauty/skin-care/moisturizers?id=30585",
            "id": "30585",
        },
        "beauty-skin-care-serum-treatments": {
            "url": "https://www.macys.com/shop/beauty/skin-care/serum-treatments?id=50363",
            "id": "50363",
        },
        "beauty-skin-care-eye-creams-serums": {
            "url": "https://www.macys.com/shop/beauty/skin-care/eye-creams-serums?id=30558",
            "id": "30558",
        },
        "beauty-skin-care-cleansers-toners": {
            "url": "https://www.macys.com/shop/beauty/skin-care/cleansers-toners?id=30582",
            "id": "30582",
        },
        "beauty-skin-care-sun-care-tanning": {
            "url": "https://www.macys.com/shop/beauty/skin-care/sun-care-tanning?id=336150",
            "id": "336150",
        },
        "beauty-hair-care": {
            "url": "https://www.macys.com/shop/beauty/hair-care?id=60600",
            "id": "60600",
        },
        "beauty-luxury-brands": {
            "url": "https://www.macys.com/shop/beauty/luxury-brands?id=198055",
            "id": "198055",
        },
        "new-trending-new-arrivals-beauty": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/beauty?id=65384",
            "id": "65384",
        },
        "beauty-best-sellers": {
            "url": "https://www.macys.com/shop/beauty/best-sellers?id=250064",
            "id": "250064",
        },
        "beauty-conscious-beauty": {
            "url": "https://www.macys.com/shop/beauty/conscious-beauty?id=58514",
            "id": "58514",
        },
        "new-trending-fall-retro-fresh": {
            "url": "https://www.macys.com/shop/new-trending/fall/retro-fresh?id=374388",
            "id": "374388",
        },
        "beauty-k-beauty": {
            "url": "https://www.macys.com/shop/beauty/k-beauty?id=350604",
            "id": "350604",
        },
        "beauty-gift-sets": {
            "url": "https://www.macys.com/shop/beauty/gift-sets?id=55537",
            "id": "55537",
        },
        "sale-by-category-beauty-beauty-gift-with-purchase": {
            "url": "https://www.macys.com/shop/sale/by-category/beauty/beauty-gift-with-purchase?id=58476",
            "id": "58476",
        },
        "beauty-gift-sets-fragrance": {
            "url": "https://www.macys.com/shop/beauty/gift-sets/fragrance?id=214356",
            "id": "214356",
        },
        "beauty-gift-sets-makeup": {
            "url": "https://www.macys.com/shop/beauty/gift-sets/makeup?id=269156",
            "id": "269156",
        },
        "beauty-gift-sets-skin-care": {
            "url": "https://www.macys.com/shop/beauty/gift-sets/skin-care?id=262557",
            "id": "262557",
        },
        "sale-by-category-beauty": {
            "url": "https://www.macys.com/shop/sale/by-category/beauty?id=66190",
            "id": "66190",
        },
    },
    "Shoes": {
        "womens-shoes-sneakers": {
            "url": "https://www.macys.com/shop/womens/shoes/sneakers?id=26499",
            "id": "26499",
        },
        "womens-shoes-boots": {
            "url": "https://www.macys.com/shop/womens/shoes/boots?id=25122",
            "id": "25122",
        },
        "womens-shoes-booties": {
            "url": "https://www.macys.com/shop/womens/shoes/booties?id=13616",
            "id": "13616",
        },
        "womens-shoes-clogs": {
            "url": "https://www.macys.com/shop/womens/shoes/clogs?id=13621",
            "id": "13621",
        },
        "womens-shoes-comfort": {
            "url": "https://www.macys.com/shop/womens/shoes/comfort?id=27902",
            "id": "27902",
        },
        "womens-shoes-flats": {
            "url": "https://www.macys.com/shop/womens/shoes/flats?id=50295",
            "id": "50295",
        },
        "womens-shoes-high-heels": {
            "url": "https://www.macys.com/shop/womens/shoes/high-heels?id=71123",
            "id": "71123",
        },
        "womens-shoes-loafers": {
            "url": "https://www.macys.com/shop/womens/shoes/loafers?id=339810",
            "id": "339810",
        },
        "womens-shoes-sandals": {
            "url": "https://www.macys.com/shop/womens/shoes/sandals?id=17570",
            "id": "17570",
        },
        "womens-shoes-slippers": {
            "url": "https://www.macys.com/shop/womens/shoes/slippers?id=16108",
            "id": "16108",
        },
        "kids-baby-shoes": {
            "url": "https://www.macys.com/shop/kids-baby/shoes?id=48561",
            "id": "48561",
        },
        "kids-baby-kids-girls-shoes": {
            "url": "https://www.macys.com/shop/kids-baby/kids/girls/shoes?id=209698",
            "id": "209698",
        },
        "kids-baby-kids-boys-shoes": {
            "url": "https://www.macys.com/shop/kids-baby/kids/boys/shoes?id=209702",
            "id": "209702",
        },
        "kids-baby-shoes-baby": {
            "url": "https://www.macys.com/shop/kids-baby/shoes/baby?id=73512",
            "id": "73512",
        },
        "new-trending-new-arrivals-womens-shoes": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/womens/shoes?id=167042",
            "id": "167042",
        },
        "new-trending-fall-womens-slouchy-boot": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/slouchy-boot?id=374377",
            "id": "374377",
        },
        "seasonal-celebrations-seasonal-living-cozy-shop-shoes-slippers-cozy-shoes-slippers": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/seasonal-living/cozy-shop/shoes-slippers/cozy-shoes-slippers?id=382582",
            "id": "382582",
        },
        "sale-great-shoe-sale-womens": {
            "url": "https://www.macys.com/shop/sale/great-shoe-sale/womens?id=340473",
            "id": "340473",
        },
        "sale-by-category-womens-shoes": {
            "url": "https://www.macys.com/shop/sale/by-category/womens/shoes?id=13604",
            "id": "13604",
        },
    },
    "Home": {
        "home-bed-bath-bedding": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding?id=20919",
            "id": "20919",
        },
        "home-bed-bath-bedding-sheets": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/sheets?id=9915",
            "id": "9915",
        },
        "home-bed-bath-bedding-comforters-sets": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/comforters-sets?id=28898",
            "id": "28898",
        },
        "home-bed-bath-bedding-essentials": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/essentials?id=70527",
            "id": "70527",
        },
        "home-bed-bath-bedding-quilts-bedspreads": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/quilts-bedspreads?id=22748",
            "id": "22748",
        },
        "home-bed-bath-bedding-pillows": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/pillows?id=28901",
            "id": "28901",
        },
        "home-bed-bath-bedding-duvet-covers": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/duvet-covers?id=25045",
            "id": "25045",
        },
        "home-bed-bath-bedding-blankets-throws": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/blankets-throws?id=29405",
            "id": "29405",
        },
        "home-bed-bath-bedding-luxury": {
            "url": "https://www.macys.com/shop/home/bed-bath/bedding/luxury?id=7502",
            "id": "7502",
        },
        "home-bed-bath-bath": {
            "url": "https://www.macys.com/shop/home/bed-bath/bath?id=60241",
            "id": "60241",
        },
        "home-bed-bath-bath-towels": {
            "url": "https://www.macys.com/shop/home/bed-bath/bath/towels?id=16853",
            "id": "16853",
        },
        "home-bed-bath-bath-rugs-mats": {
            "url": "https://www.macys.com/shop/home/bed-bath/bath/rugs-mats?id=8240",
            "id": "8240",
        },
        "home-bed-bath-bath-shower-accessories-shower-curtains": {
            "url": "https://www.macys.com/shop/home/bed-bath/bath/shower-accessories/shower-curtains?id=58936",
            "id": "58936",
        },
        "home-bed-bath-bath-accessories": {
            "url": "https://www.macys.com/shop/home/bed-bath/bath/accessories?id=22094",
            "id": "22094",
        },
        "home-kitchen-dining-kitchen": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen?id=291559",
            "id": "291559",
        },
        "home-kitchen-dining-kitchen-coffee-espresso-makers": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/coffee-espresso-makers?id=24732",
            "id": "24732",
        },
        "home-kitchen-dining-kitchen-small-kitchen-appliances-air-fryers": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/small-kitchen-appliances/air-fryers?id=180345",
            "id": "180345",
        },
        "home-kitchen-dining-kitchen-bakeware": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/bakeware?id=31795",
            "id": "31795",
        },
        "home-kitchen-dining-kitchen-cookware": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/cookware?id=7552",
            "id": "7552",
        },
        "home-kitchen-dining-kitchen-knives-cutlery": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/knives-cutlery?id=31760",
            "id": "31760",
        },
        "home-kitchen-dining-kitchen-organization-food-storage-containers": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/organization/food-storage-containers?id=206377",
            "id": "206377",
        },
        "home-kitchen-dining-kitchen-kitchen-gadgets": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/kitchen-gadgets?id=31839",
            "id": "31839",
        },
        "home-kitchen-dining-kitchen-small-kitchen-appliances": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/small-kitchen-appliances?id=7554",
            "id": "7554",
        },
        "home-kitchen-dining-kitchen-small-kitchen-appliances-toasters-toaster-ovens": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/kitchen/small-kitchen-appliances/toasters-toaster-ovens?id=7575",
            "id": "7575",
        },
        "home-furniture-mattress": {
            "url": "https://www.macys.com/shop/home/furniture-mattress?id=29391",
            "id": "29391",
        },
        "home-appliances": {
            "url": "https://www.macys.com/shop/home/appliances?id=12374",
            "id": "12374",
        },
        "home-appliances-vacuums-floor-care": {
            "url": "https://www.macys.com/shop/home/appliances/vacuums-floor-care?id=206370",
            "id": "206370",
        },
        "home-kitchen-dining-dining-entertaining": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining?id=245256",
            "id": "245256",
        },
        "home-kitchen-dining-dining-entertaining-bar-wine-accessories": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining/bar-wine-accessories?id=28973",
            "id": "28973",
        },
        "home-kitchen-dining-dining-entertaining-dinnerware": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining/dinnerware?id=53629",
            "id": "53629",
        },
        "home-kitchen-dining-dining-entertaining-glassware-drinkware": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining/glassware-drinkware?id=65938",
            "id": "65938",
        },
        "home-kitchen-dining-dining-entertaining-flatware-silverware": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining/flatware-silverware?id=7919",
            "id": "7919",
        },
        "home-kitchen-dining-dining-entertaining-serveware": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining/serveware?id=7923",
            "id": "7923",
        },
        "home-kitchen-dining-dining-entertaining-table-linens": {
            "url": "https://www.macys.com/shop/home/kitchen-dining/dining-entertaining/table-linens?id=17199",
            "id": "17199",
        },
        "home-luggage-backpacks": {
            "url": "https://www.macys.com/shop/home/luggage-backpacks?id=16908",
            "id": "16908",
        },
        "home-home-decor": {
            "url": "https://www.macys.com/shop/home/home-decor?id=290059",
            "id": "290059",
        },
        "home-home-decor-window-treatments": {
            "url": "https://www.macys.com/shop/home/home-decor/window-treatments?id=198072",
            "id": "198072",
        },
        "home-home-decor-lighting-lamps": {
            "url": "https://www.macys.com/shop/home/home-decor/lighting-lamps?id=39267",
            "id": "39267",
        },
        "home-area-rugs": {
            "url": "https://www.macys.com/shop/home/area-rugs?id=190877",
            "id": "190877",
        },
        "home-home-decor-candles-diffusers": {
            "url": "https://www.macys.com/shop/home/home-decor/candles-diffusers?id=190352",
            "id": "190352",
        },
        "home-home-decor-pillows-throw-blankets": {
            "url": "https://www.macys.com/shop/home/home-decor/pillows-throw-blankets?id=190365",
            "id": "190365",
        },
        "new-trending-new-arrivals-home-trends-hosting-essentials": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/home/trends/hosting-essentials?id=360202",
            "id": "360202",
        },
        "new-trending-new-arrivals-home": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/home?id=113745",
            "id": "113745",
        },
        "home-best-sellers": {
            "url": "https://www.macys.com/shop/home/best-sellers?id=27233",
            "id": "27233",
        },
        "seasonal-celebrations-holiday-shop": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop?id=30599",
            "id": "30599",
        },
        "seasonal-celebrations-holiday-shop-thanksgiving": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/thanksgiving?id=212260",
            "id": "212260",
        },
        "seasonal-celebrations-holiday-shop-christmas": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas?id=299657",
            "id": "299657",
        },
        "seasonal-celebrations-holiday-shop-christmas-bed-bath-bedding": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/bed-bath/bedding?id=202790",
            "id": "202790",
        },
        "seasonal-celebrations-holiday-shop-christmas-dining-entertaining": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/dining-entertaining?id=341932",
            "id": "341932",
        },
        "electronics": {
            "url": "https://www.macys.com/shop/electronics?id=168970",
            "id": "168970",
        },
        "interests-activities-books": {
            "url": "https://www.macys.com/shop/interests-activities/books?id=363461",
            "id": "363461",
        },
        "interests-activities-gourmet-food": {
            "url": "https://www.macys.com/shop/interests-activities/gourmet-food?id=208664",
            "id": "208664",
        },
        "lifestyle-interests-outdoor-recreation": {
            "url": "https://www.macys.com/shop/lifestyle-interests/outdoor-recreation?id=363512",
            "id": "363512",
        },
        "sale-limited-time-specials-home": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/home?id=42021",
            "id": "42021",
        },
        "sale-lowest-prices-of-the-season-furniture-lowest-prices-of-the-season": {
            "url": "https://www.macys.com/shop/sale/lowest-prices-of-the-season/furniture-lowest-prices-of-the-season?id=70983",
            "id": "70983",
        },
        "sale-by-category-home": {
            "url": "https://www.macys.com/shop/sale/by-category/home?id=24294",
            "id": "24294",
        },
    },
    "Jewelry": {
        "jewelry-watches-jewelry": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry?id=164045",
            "id": "164045",
        },
        "jewelry-watches-jewelry-bracelets": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/bracelets?id=103942",
            "id": "103942",
        },
        "jewelry-watches-jewelry-earrings": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/earrings?id=201856",
            "id": "201856",
        },
        "jewelry-watches-jewelry-necklaces": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/necklaces?id=33487",
            "id": "33487",
        },
        "jewelry-watches-jewelry-rings": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/rings?id=69905",
            "id": "69905",
        },
        "jewelry-watches-jewelry-fine-jewelry-diamond": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/fine-jewelry/diamond?id=57702",
            "id": "57702",
        },
        "jewelry-watches-jewelry-fine-jewelry-diamond-lab-grown": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/fine-jewelry/diamond/lab-grown?id=210857",
            "id": "210857",
        },
        "jewelry-watches-jewelry-fine-jewelry-gold": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/fine-jewelry/gold?id=2904",
            "id": "2904",
        },
        "jewelry-watches-jewelry-fine-jewelry-gemstones": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/fine-jewelry/gemstones?id=2903",
            "id": "2903",
        },
        "jewelry-watches-jewelry-fine-jewelry": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/fine-jewelry?id=65993",
            "id": "65993",
        },
        "jewelry-watches-jewelry-fashion-jewelry": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/fashion-jewelry?id=55352",
            "id": "55352",
        },
        "jewelry-watches-wedding-engagement": {
            "url": "https://www.macys.com/shop/jewelry-watches/wedding-engagement?id=77998",
            "id": "77998",
        },
        "jewelry-watches-wedding-engagement-engagement-rings": {
            "url": "https://www.macys.com/shop/jewelry-watches/wedding-engagement/engagement-rings?id=200053",
            "id": "200053",
        },
        "jewelry-watches-wedding-engagement-wedding-bands": {
            "url": "https://www.macys.com/shop/jewelry-watches/wedding-engagement/wedding-bands?id=200153",
            "id": "200153",
        },
        "jewelry-watches-watches": {
            "url": "https://www.macys.com/shop/jewelry-watches/watches?id=239616",
            "id": "239616",
        },
        "jewelry-watches-watches-mens": {
            "url": "https://www.macys.com/shop/jewelry-watches/watches/mens?id=57386",
            "id": "57386",
        },
        "jewelry-watches-watches-womens": {
            "url": "https://www.macys.com/shop/jewelry-watches/watches/womens?id=57385",
            "id": "57385",
        },
        "jewelry-watches-mens-jewelry": {
            "url": "https://www.macys.com/shop/jewelry-watches/mens-jewelry?id=43877",
            "id": "43877",
        },
        "jewelry-watches-mens-jewelry-necklaces": {
            "url": "https://www.macys.com/shop/jewelry-watches/mens-jewelry/necklaces?id=340153",
            "id": "340153",
        },
        "gifts-every-occasion-by-category-jewelry-watches-red-box-gifts": {
            "url": "https://www.macys.com/shop/gifts/every-occasion/by-category/jewelry-watches/red-box-gifts?id=200851",
            "id": "200851",
        },
        "new-trending-new-arrivals-jewelry-watches": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/jewelry-watches?id=166142",
            "id": "166142",
        },
        "jewelry-watches-trends": {
            "url": "https://www.macys.com/shop/jewelry-watches/trends?id=340196",
            "id": "340196",
        },
        "jewelry-watches-jewelry-the-jewelry-edit": {
            "url": "https://www.macys.com/shop/jewelry-watches/jewelry/the-jewelry-edit?id=395067",
            "id": "395067",
        },
        "jewelry-watches-watches-the-watch-drop": {
            "url": "https://www.macys.com/shop/jewelry-watches/watches/the-watch-drop?id=394677",
            "id": "394677",
        },
        "jewelry-watches-trends-pre-loved": {
            "url": "https://www.macys.com/shop/jewelry-watches/trends/pre-loved?id=385191",
            "id": "385191",
        },
        "sale-diamond-sale": {
            "url": "https://www.macys.com/shop/sale/diamond-sale?id=44780",
            "id": "44780",
        },
        "sale-limited-time-specials-jewelry-watches": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/jewelry-watches?id=139242",
            "id": "139242",
        },
        "sale-by-category-jewelry-watches": {
            "url": "https://www.macys.com/shop/sale/by-category/jewelry-watches?id=228492",
            "id": "228492",
        },
    },
    "Handbags": {
        "womens-handbags-wallets-accessories-handbags-wallets": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags-wallets?id=203051",
            "id": "203051",
        },
        "womens-handbags-wallets-accessories-handbags-designer": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/designer?id=69603",
            "id": "69603",
        },
        "womens-handbags-wallets-accessories-handbags-backpacks": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/backpacks?id=51906",
            "id": "51906",
        },
        "womens-handbags-wallets-accessories-handbags-clutches-evening": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/clutches-evening?id=27691",
            "id": "27691",
        },
        "womens-handbags-wallets-accessories-handbags-crossbody-messenger": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/crossbody-messenger?id=46011",
            "id": "46011",
        },
        "womens-handbags-wallets-accessories-handbags-satchels": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/satchels?id=46013",
            "id": "46013",
        },
        "womens-handbags-wallets-accessories-handbags-shoulder": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/shoulder?id=46014",
            "id": "46014",
        },
        "womens-handbags-wallets-accessories-handbags-tote": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/handbags/tote?id=46015",
            "id": "46015",
        },
        "womens-handbags-wallets-accessories-wallets": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/wallets?id=27689",
            "id": "27689",
        },
        "womens-handbags-wallets-accessories-accessories": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/accessories?id=29440",
            "id": "29440",
        },
        "womens-handbags-wallets-accessories-accessories-sunglasses": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/accessories/sunglasses?id=28295",
            "id": "28295",
        },
        "womens-handbags-wallets-accessories-accessories-cold-weather": {
            "url": "https://www.macys.com/shop/womens/handbags-wallets-accessories/accessories/cold-weather?id=206671",
            "id": "206671",
        },
        "new-trending-new-at-macys-womens-new-arrivals-new-arrivals-handbags": {
            "url": "https://www.macys.com/shop/new-trending/new-at-macys/womens-new-arrivals/new-arrivals-handbags?id=338857",
            "id": "338857",
        },
        "womens-trends-pre-loved-luxury-handbags": {
            "url": "https://www.macys.com/shop/womens/trends/pre-loved/luxury-handbags?id=358276",
            "id": "358276",
        },
        "sale-by-category-womens-handbags-wallets": {
            "url": "https://www.macys.com/shop/sale/by-category/womens/handbags-wallets?id=28273",
            "id": "28273",
        },
        "sale-by-category-womens-accessories": {
            "url": "https://www.macys.com/shop/sale/by-category/womens/accessories?id=341578",
            "id": "341578",
        },
    },
    "Furniture & Mattresses": {
        "home-furniture-mattress-living-room": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room?id=35319",
            "id": "35319",
        },
        "home-furniture-mattress-living-room-chairs": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room/chairs?id=341620",
            "id": "341620",
        },
        "home-furniture-mattress-living-room-coffee-accent-tables": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room/coffee-accent-tables?id=35423",
            "id": "35423",
        },
        "home-furniture-mattress-living-room-couches-sofas": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room/couches-sofas?id=35419",
            "id": "35419",
        },
        "home-furniture-mattress-living-room-couches-sofas-sectional-sofas": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room/couches-sofas/sectional-sofas?id=37394",
            "id": "37394",
        },
        "home-furniture-mattress-living-room-tv-stands": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room/tv-stands?id=35424",
            "id": "35424",
        },
        "home-furniture-mattress-dining-room-kitchen": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/dining-room-kitchen?id=35421",
            "id": "35421",
        },
        "home-furniture-mattress-dining-room-kitchen-dining-room-chairs": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/dining-room-kitchen/dining-room-chairs?id=69960",
            "id": "69960",
        },
        "home-furniture-mattress-dining-room-kitchen-dining-room-sets": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/dining-room-kitchen/dining-room-sets?id=69962",
            "id": "69962",
        },
        "home-furniture-mattress-dining-room-kitchen-dining-room-tables": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/dining-room-kitchen/dining-room-tables?id=69961",
            "id": "69961",
        },
        "home-furniture-mattress-dining-room-kitchen-home-bar": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/dining-room-kitchen/home-bar?id=37823",
            "id": "37823",
        },
        "home-furniture-mattress-home-office-study": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/home-office-study?id=35422",
            "id": "35422",
        },
        "home-furniture-mattress-home-office-study-desks": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/home-office-study/desks?id=261365",
            "id": "261365",
        },
        "home-furniture-mattress-home-office-study-office-chairs": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/home-office-study/office-chairs?id=261364",
            "id": "261364",
        },
        "home-furniture-mattress-living-room-bookshelves-bookcases": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/living-room/bookshelves-bookcases?id=69949",
            "id": "69949",
        },
        "home-furniture-mattress-bedroom": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/bedroom?id=35420",
            "id": "35420",
        },
        "home-furniture-mattress-bedroom-sets": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/bedroom/sets?id=198104",
            "id": "198104",
        },
        "home-furniture-mattress-bedroom-beds": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/bedroom/beds?id=35380",
            "id": "35380",
        },
        "home-furniture-mattress-bedroom-dressers-chests": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/bedroom/dressers-chests?id=69952",
            "id": "69952",
        },
        "home-furniture-mattress-bedroom-nightstands": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/bedroom/nightstands?id=69954",
            "id": "69954",
        },
        "home-furniture-mattress-outdoor-patio": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/outdoor-patio?id=70056",
            "id": "70056",
        },
        "home-furniture-mattress-outdoor-patio-dining-furniture": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/outdoor-patio/dining-furniture?id=175843",
            "id": "175843",
        },
        "home-furniture-mattress-outdoor-patio-lounge-furniture": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/outdoor-patio/lounge-furniture?id=175844",
            "id": "175844",
        },
        "home-furniture-mattress-mattresses": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/mattresses?id=97743",
            "id": "97743",
        },
        "home-furniture-mattress-mattresses-twin": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/mattresses/twin?id=27760",
            "id": "27760",
        },
        "home-furniture-mattress-mattresses-full": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/mattresses/full?id=25955",
            "id": "25955",
        },
        "home-furniture-mattress-mattresses-queen": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/mattresses/queen?id=25956",
            "id": "25956",
        },
        "home-furniture-mattress-mattresses-king": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/mattresses/king?id=25957",
            "id": "25957",
        },
        "home-furniture-mattress-mattresses-california-king": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/mattresses/california-king?id=25958",
            "id": "25958",
        },
        "home-furniture-mattress-in-stock-furniture": {
            "url": "https://www.macys.com/shop/home/furniture-mattress/in-stock-furniture?id=372567",
            "id": "372567",
        },
        "sale-clearance-closeout-home-furniture": {
            "url": "https://www.macys.com/shop/sale/clearance-closeout/home/furniture?id=341192",
            "id": "341192",
        },
        "sale-by-category-home-furniture-mattresses": {
            "url": "https://www.macys.com/shop/sale/by-category/home/furniture-mattresses?id=31260",
            "id": "31260",
        },
    },
    "Holiday Shop": {
        "seasonal-celebrations-holiday-shop-christmas-decorations-ornaments": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/decorations/ornaments?id=30600",
            "id": "30600",
        },
        "seasonal-celebrations-holiday-shop-christmas-decorations": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/decorations?id=111372",
            "id": "111372",
        },
        "seasonal-celebrations-holiday-shop-christmas-christmas-trees": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/christmas-trees?id=341878",
            "id": "341878",
        },
        "seasonal-celebrations-holiday-shop-christmas-decorations-villages": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/decorations/villages?id=111359",
            "id": "111359",
        },
        "seasonal-celebrations-holiday-shop-christmas-decorations-outdoor": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/decorations/outdoor?id=111374",
            "id": "111374",
        },
        "seasonal-celebrations-holiday-shop-christmas-bed-bath": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/bed-bath?id=202765",
            "id": "202765",
        },
        "seasonal-celebrations-holiday-shop-christmas-decorations-candles": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/decorations/candles?id=111370",
            "id": "111370",
        },
        "seasonal-celebrations-holiday-shop-christmas-decorations-advent-calendars": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/christmas/decorations/advent-calendars?id=111375",
            "id": "111375",
        },
        "interests-activities-gourmet-food-candy-chocolate": {
            "url": "https://www.macys.com/shop/interests-activities/gourmet-food/candy-chocolate?id=385167",
            "id": "385167",
        },
        "interests-activities-gourmet-food-gift-baskets": {
            "url": "https://www.macys.com/shop/interests-activities/gourmet-food/gift-baskets?id=207580",
            "id": "207580",
        },
        "seasonal-celebrations-seasonal-living-matching-family-pajamas": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/seasonal-living/matching-family/pajamas?id=67507",
            "id": "67507",
        },
        "kids-baby-occasion-holiday-christmas": {
            "url": "https://www.macys.com/shop/kids-baby/occasion/holiday/christmas?id=394471",
            "id": "394471",
        },
        "seasonal-celebrations-holiday-shop-hanukkah": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/holiday-shop/hanukkah?id=202793",
            "id": "202793",
        },
        "sale-limited-time-specials-holiday-shop": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/holiday-shop?id=270859",
            "id": "270859",
        },
        "sale-by-category-holiday-shop-christmas-decorations": {
            "url": "https://www.macys.com/shop/sale/by-category/holiday-shop/christmas-decorations?id=340559",
            "id": "340559",
        },
        "sale-by-category-holiday-shop": {
            "url": "https://www.macys.com/shop/sale/by-category/holiday-shop?id=340478",
            "id": "340478",
        },
    },
    "Kids & Baby": {
        "kids-baby-toddler-girls": {
            "url": "https://www.macys.com/shop/kids-baby/toddler/girls?id=6581",
            "id": "6581",
        },
        "kids-baby-kids-girls": {
            "url": "https://www.macys.com/shop/kids-baby/kids/girls?id=61998",
            "id": "61998",
        },
        "kids-baby-kids-tween-girls": {
            "url": "https://www.macys.com/shop/kids-baby/kids/tween-girls?id=340933",
            "id": "340933",
        },
        "kids-baby-kids-girls-activewear": {
            "url": "https://www.macys.com/shop/kids-baby/kids/girls/activewear?id=177142",
            "id": "177142",
        },
        "kids-baby-kids-girls-coats-jackets": {
            "url": "https://www.macys.com/shop/kids-baby/kids/girls/coats-jackets?id=188692",
            "id": "188692",
        },
        "kids-baby-kids-girls-dresses": {
            "url": "https://www.macys.com/shop/kids-baby/kids/girls/dresses?id=31460",
            "id": "31460",
        },
        "kids-baby-toddler-boys": {
            "url": "https://www.macys.com/shop/kids-baby/toddler/boys?id=27058",
            "id": "27058",
        },
        "kids-baby-kids-boys": {
            "url": "https://www.macys.com/shop/kids-baby/kids/boys?id=61999",
            "id": "61999",
        },
        "kids-baby-kids-boys-activewear": {
            "url": "https://www.macys.com/shop/kids-baby/kids/boys/activewear?id=177143",
            "id": "177143",
        },
        "kids-baby-kids-boys-coats-jackets": {
            "url": "https://www.macys.com/shop/kids-baby/kids/boys/coats-jackets?id=188754",
            "id": "188754",
        },
        "kids-baby-kids-boys-suits": {
            "url": "https://www.macys.com/shop/kids-baby/kids/boys/suits?id=63016",
            "id": "63016",
        },
        "kids-baby-baby": {
            "url": "https://www.macys.com/shop/kids-baby/baby?id=187458",
            "id": "187458",
        },
        "kids-baby-baby-gear": {
            "url": "https://www.macys.com/shop/kids-baby/baby/gear?id=58376",
            "id": "58376",
        },
        "kids-baby-baby-girls": {
            "url": "https://www.macys.com/shop/kids-baby/baby/girls?id=48692",
            "id": "48692",
        },
        "kids-baby-baby-boys": {
            "url": "https://www.macys.com/shop/kids-baby/baby/boys?id=48693",
            "id": "48693",
        },
        "toys": {
            "url": "https://www.macys.com/shop/toys?id=45269",
            "id": "45269",
        },
        "character-shop": {
            "url": "https://www.macys.com/shop/character-shop?id=339018",
            "id": "339018",
        },
        "kids-baby-occasion-holiday-halloween": {
            "url": "https://www.macys.com/shop/kids-baby/occasion/holiday/halloween?id=201951",
            "id": "201951",
        },
        "new-trending-fall-kids-statement-sweaters": {
            "url": "https://www.macys.com/shop/new-trending/fall/kids/statement-sweaters?id=374469",
            "id": "374469",
        },
        "sale-limited-time-specials-kids-baby": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/kids-baby?id=359887",
            "id": "359887",
        },
        "sale-by-category-kids-baby": {
            "url": "https://www.macys.com/shop/sale/by-category/kids-baby?id=6086",
            "id": "6086",
        },
    },
    "Toys": {
        "toys-age-groups-0-24-months": {
            "url": "https://www.macys.com/shop/toys/age-groups/0-24-months?id=385192",
            "id": "385192",
        },
        "toys-age-groups-2-4-years": {
            "url": "https://www.macys.com/shop/toys/age-groups/2-4-years?id=385367",
            "id": "385367",
        },
        "toys-age-groups-5-7-years": {
            "url": "https://www.macys.com/shop/toys/age-groups/5-7-years?id=210270",
            "id": "210270",
        },
        "toys-age-groups-8-10-years": {
            "url": "https://www.macys.com/shop/toys/age-groups/8-10-years?id=210271",
            "id": "210271",
        },
        "toys-age-groups-11-and-up": {
            "url": "https://www.macys.com/shop/toys/age-groups/11-and-up?id=210273",
            "id": "210273",
        },
        "toys-action-figures-playsets": {
            "url": "https://www.macys.com/shop/toys/action-figures-playsets?id=211558",
            "id": "211558",
        },
        "toys-dolls-dollhouses": {
            "url": "https://www.macys.com/shop/toys/dolls-dollhouses?id=210293",
            "id": "210293",
        },
        "toys-crafts-educational": {
            "url": "https://www.macys.com/shop/toys/crafts-educational?id=385368",
            "id": "385368",
        },
        "toys-games-puzzles": {
            "url": "https://www.macys.com/shop/toys/games-puzzles?id=238020",
            "id": "238020",
        },
        "electronics-kids-tech": {
            "url": "https://www.macys.com/shop/electronics/kids-tech?id=213958",
            "id": "213958",
        },
        "toys-vehicle-remote-control": {
            "url": "https://www.macys.com/shop/toys/vehicle-remote-control?id=215153",
            "id": "215153",
        },
        "character-shop-barbie": {
            "url": "https://www.macys.com/shop/character-shop/barbie?id=211670",
            "id": "211670",
        },
        "new-trending-new-arrivals-toy": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/toy?id=111458",
            "id": "111458",
        },
        "toys-top-toys": {
            "url": "https://www.macys.com/shop/toys/top-toys?id=311256",
            "id": "311256",
        },
        "sale-limited-time-specials-toys": {
            "url": "https://www.macys.com/shop/sale/limited-time-specials/toys?id=340547",
            "id": "340547",
        },
        "sale-by-category-toys": {
            "url": "https://www.macys.com/shop/sale/by-category/toys?id=211966",
            "id": "211966",
        },
    },
    "Gifts": {
        "gifts-holiday-by-recipient-for-her": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-recipient/for-her?id=91442",
            "id": "91442",
        },
        "gifts-holiday-by-recipient-for-him": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-recipient/for-him?id=91458",
            "id": "91458",
        },
        "gifts-holiday-by-recipient-for-kids": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-recipient/for-kids?id=91556",
            "id": "91556",
        },
        "gifts-holiday-by-recipient-for-pets": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-recipient/for-pets?id=348481",
            "id": "348481",
        },
        "gifts-holiday-by-price-under-25": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-price/under-25?id=91605",
            "id": "91605",
        },
        "gifts-holiday-by-price-under-50": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-price/under-50?id=91606",
            "id": "91606",
        },
        "gifts-holiday-by-price-under-100": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-price/under-100?id=91607",
            "id": "91607",
        },
        "gifts-holiday-by-price-luxe": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-price/luxe?id=149867",
            "id": "149867",
        },
        "gifts-holiday-top-100": {
            "url": "https://www.macys.com/shop/gifts/holiday/top-100?id=350767",
            "id": "350767",
        },
        "gifts-holiday-by-category-beauty-fragrances": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/beauty-fragrances?id=91583",
            "id": "91583",
        },
        "gifts-holiday-by-category-blankets-throws": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/blankets-throws?id=262166",
            "id": "262166",
        },
        "gifts-holiday-by-category-shoes": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/shoes?id=262762",
            "id": "262762",
        },
        "gifts-holiday-by-category-coats-jackets": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/coats-jackets?id=378667",
            "id": "378667",
        },
        "gifts-holiday-by-category-fragrances": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/fragrances?id=91587",
            "id": "91587",
        },
        "gifts-holiday-by-category-gourmet-food-candy": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/gourmet-food-candy?id=91546",
            "id": "91546",
        },
        "gifts-holiday-by-category-handbags-accessories": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/handbags-accessories?id=91443",
            "id": "91443",
        },
        "gifts-holiday-by-category-home": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/home?id=346265",
            "id": "346265",
        },
        "gifts-holiday-by-category-jewelry-watches": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/jewelry-watches?id=204254",
            "id": "204254",
        },
        "gifts-holiday-by-category-loungewear-pajamas": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/loungewear-pajamas?id=91450",
            "id": "91450",
        },
        "gifts-holiday-by-category-sweaters-cashmere": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/sweaters-cashmere?id=260264",
            "id": "260264",
        },
        "gifts-holiday-by-category-tech": {
            "url": "https://www.macys.com/shop/gifts/holiday/by-category/tech?id=149866",
            "id": "149866",
        },
        "gifts-holiday-gift-lists-the-cashmere-shop": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/the-cashmere-shop?id=321864",
            "id": "321864",
        },
        "gifts-holiday-gift-lists-chef": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/chef?id=348482",
            "id": "348482",
        },
        "gifts-holiday-gift-lists-coffee-lover-holiday-gifts": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/coffee-lover-holiday-gifts?id=408767",
            "id": "408767",
        },
        "gifts-holiday-gift-lists-fitness-enthusiast": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/fitness-enthusiast?id=69215",
            "id": "69215",
        },
        "gifts-holiday-gift-lists-gamer": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/gamer?id=348493",
            "id": "348493",
        },
        "gifts-holiday-gift-lists-spa-enthusiast": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/spa-enthusiast?id=8683",
            "id": "8683",
        },
        "gifts-holiday-gift-lists-jet-setter": {
            "url": "https://www.macys.com/shop/gifts/holiday/gift-lists/jet-setter?id=200177",
            "id": "200177",
        },
        "gifts-holiday": {
            "url": "https://www.macys.com/shop/gifts/holiday?id=341648",
            "id": "341648",
        },
    },
    "New & Trending": {
        "new-trending-new-arrivals": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals?id=135248",
            "id": "135248",
        },
        "new-trending-new-arrivals-womens-handbags": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/womens/handbags?id=338857",
            "id": "338857",
        },
        "new-trending-new-arrivals-kids-baby": {
            "url": "https://www.macys.com/shop/new-trending/new-arrivals/kids-baby?id=398473",
            "id": "398473",
        },
        "new-trending-fall-womens-statement-sweaters": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/statement-sweaters?id=342758",
            "id": "342758",
        },
        "new-trending-fall-womens-suede": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/suede?id=374380",
            "id": "374380",
        },
        "jewelry-watches-trends-two-tone-jewelry-watches": {
            "url": "https://www.macys.com/shop/jewelry-watches/trends/two-tone-jewelry-watches?id=374386",
            "id": "374386",
        },
        "new-trending-fall-womens-slim-shoulder-bag": {
            "url": "https://www.macys.com/shop/new-trending/fall/womens/slim-shoulder-bag?id=360166",
            "id": "360166",
        },
        "new-trending-fall-mens-tailored-overcoats": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/tailored-overcoats?id=360169",
            "id": "360169",
        },
        "new-trending-fall-mens-puffer-coats": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/puffer-coats?id=374391",
            "id": "374391",
        },
        "new-trending-fall-mens-soft-loafers": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/soft-loafers?id=374394",
            "id": "374394",
        },
        "new-trending-fall-mens-colored-dial-watches": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/colored-dial-watches?id=374468",
            "id": "374468",
        },
        "new-trending-fall-mens-patterned-suits": {
            "url": "https://www.macys.com/shop/new-trending/fall/mens/patterned-suits?id=374392",
            "id": "374392",
        },
        "new-trending-limited-edition-macys-x-american-designers": {
            "url": "https://www.macys.com/shop/new-trending/limited-edition/macys-x-american-designers?id=398474",
            "id": "398474",
        },
        "seasonal-celebrations-wedding": {
            "url": "https://www.macys.com/shop/seasonal-celebrations/wedding?id=357168",
            "id": "357168",
        },
        "womens-occasion-resort-wear": {
            "url": "https://www.macys.com/shop/womens/occasion/resort-wear?id=53427",
            "id": "53427",
        },
        "new-trending-what-to-wear-wear-to-work": {
            "url": "https://www.macys.com/shop/new-trending/what-to-wear/wear-to-work?id=333097",
            "id": "333097",
        },
    },
}
