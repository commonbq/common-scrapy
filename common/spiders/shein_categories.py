"""SHEIN US category taxonomy captured from the live navigation on 2026-10-19.

The outer keys are the site's 25 top-level departments.  Leaf names are globally
unique because Airflow output paths use the bare leaf key; legacy top-level
selectors such as ``women`` and ``electronics`` remain valid.  Repeated menu
targets are kept only at their first occurrence, tracking parameters are omitted,
and store-home links are excluded because they are not category PLPs.
"""

SHEIN_CATEGORIES = {
    "new-in": {
        "new-in": {
            "url": "https://us.shein.com/recommend/New-In-sc-10050082658.html",
            "label": "New In",
            "section": "Top category",
        },
        "new-in-view-all": {
            "url": "https://us.shein.com/recommend/Women-New-in-sc-10050026724.html",
            "label": "View All",
            "section": "New in Women's Clothing",
        },
        "new-in-tops": {
            "url": "https://us.shein.com/recommend/New-in-Tops-sc-10050028993.html",
            "label": "Tops",
            "section": "New in Women's Clothing",
        },
        "new-in-t-shirts": {
            "url": "https://us.shein.com/recommend/New-in-Shirts-sc-10050028996.html",
            "label": "T-shirts",
            "section": "New in Women's Clothing",
        },
        "new-in-blouses": {
            "url": "https://us.shein.com/recommend/New-in-Blouses-sc-10050028999.html",
            "label": "Blouses",
            "section": "New in Women's Clothing",
        },
        "new-in-tank-tops-camis": {
            "url": "https://us.shein.com/recommend/New-in-Tank-Tops-sc-10050029000.html",
            "label": "Tank Tops & Camis",
            "section": "New in Women's Clothing",
        },
        "new-in-dresses": {
            "url": "https://us.shein.com/recommend/New-in-Dresses-sc-10050029004.html",
            "label": "Dresses",
            "section": "New in Women's Clothing",
        },
        "new-in-long-dresses": {
            "url": "https://us.shein.com/recommend/New-Long-Dresses-sc-10050029432.html",
            "label": "Long Dresses",
            "section": "New in Women's Clothing",
        },
        "new-in-knitwear": {
            "url": "https://us.shein.com/recommend/New-in-Knitwear-sc-10050029288.html",
            "label": "Knitwear",
            "section": "New in Women's Clothing",
        },
        "new-in-sweaters": {
            "url": "https://us.shein.com/recommend/New-in-Sweaters-sc-10050029289.html",
            "label": "Sweaters",
            "section": "New in Women's Clothing",
        },
        "new-in-bottoms": {
            "url": "https://us.shein.com/recommend/New-in-Bottoms-sc-10050029290.html",
            "label": "Bottoms",
            "section": "New in Women's Clothing",
        },
        "new-in-pants": {
            "url": "https://us.shein.com/recommend/New-in-Pants-sc-10050029291.html",
            "label": "Pants",
            "section": "New in Women's Clothing",
        },
        "new-in-outerwear": {
            "url": "https://us.shein.com/recommend/New-in-Outerwear-sc-10050029414.html",
            "label": "Outerwear",
            "section": "New in Women's Clothing",
        },
        "new-in-winter-coats": {
            "url": "https://us.shein.com/new/New-in-winter-coats-sc-0021703468.html",
            "label": "Winter Coats",
            "section": "New in Women's Clothing",
        },
        "new-in-denim": {
            "url": "https://us.shein.com/recommend/New-in-Denim-sc-10050029416.html",
            "label": "Denim",
            "section": "New in Women's Clothing",
        },
        "new-in-co-ords": {
            "url": "https://us.shein.com/recommend/New-two-piece-set-sc-10050029417.html",
            "label": "Co-ords",
            "section": "New in Women's Clothing",
        },
        "new-in-sweatshirts": {
            "url": "https://us.shein.com/recommend/New-Sweatshirts-sc-10050029418.html",
            "label": "Sweatshirts",
            "section": "New in Women's Clothing",
        },
        "new-in-bodysuits-jumpsuits": {
            "url": "https://us.shein.com/recommend/New-Bodysuits-sc-10050029419.html",
            "label": "Bodysuits&Jumpsuits",
            "section": "New in Women's Clothing",
        },
        "new-in-suits": {
            "url": "https://us.shein.com/recommend/New-Suits-sc-10050029420.html",
            "label": "Suits",
            "section": "New in Women's Clothing",
        },
        "new-in-beachwear": {
            "url": "https://us.shein.com/recommend/New-Beachwear-sc-10050029422.html",
            "label": "Beachwear",
            "section": "New in Women's Clothing",
        },
        "new-in-maternity": {
            "url": "https://us.shein.com/recommend/New-Maternity-sc-10050029423.html",
            "label": "Maternity",
            "section": "New in Women's Clothing",
        },
        "new-in-wedding": {
            "url": "https://us.shein.com/recommend/New-Wedding-sc-10050029425.html",
            "label": "Wedding",
            "section": "New in Women's Clothing",
        },
        "new-in-party-wear": {
            "url": "https://us.shein.com/recommend/New-Party-Wear-sc-10050029426.html",
            "label": "Party Wear",
            "section": "New in Women's Clothing",
        },
        "new-in-sleep-lounge": {
            "url": "https://us.shein.com/recommend/New-in-women-Sleep-sc-10050013237.html",
            "label": "Sleep & Lounge",
            "section": "New in Women's Clothing",
        },
        "new-in-underwear": {
            "url": "https://us.shein.com/recommend/New-in-women-underwear-sc-10050013238.html",
            "label": "Underwear",
            "section": "New in Women's Clothing",
        },
        "new-in-view-all-00210832": {
            "url": "https://us.shein.com/new/Plus-Size-New-In-15-Days-sc-00210832.html",
            "label": "View All",
            "section": "New in Curve Clothing",
        },
        "new-in-tops-00211498": {
            "url": "https://us.shein.com/new/Plus-Tops-New-In-15-Days-sc-00211498.html",
            "label": "Tops",
            "section": "New in Curve Clothing",
        },
        "new-in-dresses-00203657": {
            "url": "https://us.shein.com/new/New-In-Curve-Dresses-sc-00203657.html",
            "label": "Dresses",
            "section": "New in Curve Clothing",
        },
        "new-in-bottoms-00203670": {
            "url": "https://us.shein.com/new/New-In-Curve-Bottoms-sc-00203670.html",
            "label": "Bottoms",
            "section": "New in Curve Clothing",
        },
        "new-in-blouses-00203667": {
            "url": "https://us.shein.com/new/New-In-Curve-Blouses-sc-00203667.html",
            "label": "Blouses",
            "section": "New in Curve Clothing",
        },
        "new-in-t-shirts-00203666": {
            "url": "https://us.shein.com/new/New-In-Curve-Tees-sc-00203666.html",
            "label": "T-shirts",
            "section": "New in Curve Clothing",
        },
        "new-in-sweaters-00203665": {
            "url": "https://us.shein.com/new/New-In-Curve-Sweats-sc-00203665.html",
            "label": "Sweaters",
            "section": "New in Curve Clothing",
        },
        "new-in-denim-00203671": {
            "url": "https://us.shein.com/new/New-In-Curve-Denim-sc-00203671.html",
            "label": "Denim",
            "section": "New in Curve Clothing",
        },
        "new-in-co-ords-00203659": {
            "url": "https://us.shein.com/new/New-In-Curve-Sets-sc-00203659.html",
            "label": "Co-ords",
            "section": "New in Curve Clothing",
        },
        "new-in-sweatshirts-00205009": {
            "url": "https://us.shein.com/new/New-In-Curve-Sweatshirts-sc-00205009.html",
            "label": "Sweatshirts",
            "section": "New in Curve Clothing",
        },
        "new-in-jackets-coats": {
            "url": "https://us.shein.com/new/New-In-Curve-Outwear-sc-00203674.html",
            "label": "Jackets & Coats",
            "section": "New in Curve Clothing",
        },
        "new-in-jumpsuits": {
            "url": "https://us.shein.com/new/New-In-Curve-Jumpsuits-sc-00203658.html",
            "label": "Jumpsuits",
            "section": "New in Curve Clothing",
        },
        "new-in-bodysuits": {
            "url": "https://us.shein.com/new/New-In-Curve-Bodysuits-sc-00203664.html",
            "label": "Bodysuits",
            "section": "New in Curve Clothing",
        },
        "new-in-suits-10050030326": {
            "url": "https://us.shein.com/recommend/Plus-New-In-Suits-sc-10050030326.html",
            "label": "Suits",
            "section": "New in Curve Clothing",
        },
        "new-in-beachwear-10050095420": {
            "url": "https://us.shein.com/recommend/BeachwearCurve-sc-10050095420.html",
            "label": "Beachwear",
            "section": "New in Curve Clothing",
        },
        "new-in-wedding-10050095421": {
            "url": "https://us.shein.com/recommend/weddingCurve-sc-10050095421.html",
            "label": "Wedding",
            "section": "New in Curve Clothing",
        },
        "new-in-party-wear-10050095422": {
            "url": "https://us.shein.com/recommend/PartywearCurve-sc-10050095422.html",
            "label": "Party Wear",
            "section": "New in Curve Clothing",
        },
        "new-in-lingerie-loungewear": {
            "url": "https://us.shein.com/recommend/New-In-Curve-Lingerie-Loungewear-sc-10050006735.html",
            "label": "Lingerie & Loungewear",
            "section": "New in Curve Clothing",
        },
        "new-in-my-little-pony": {
            "url": "https://us.shein.com/StoreSelection/My-Little-Pony-sc-16050018625.html",
            "label": "My Little Pony",
            "section": "Officially Licensed Collabs",
        },
        "new-in-mean-girls": {
            "url": "https://us.shein.com/StoreSelection/Mean-Girls-sc-16050014042.html",
            "label": "Mean Girls",
            "section": "Officially Licensed Collabs",
        },
        "new-in-teenage-mutant-ninja-turtles": {
            "url": "https://us.shein.com/StoreSelection/TEENAGE-MUTANT-NINJA-TURTLES-sc-16050014336.html",
            "label": "TEENAGE MUTANT NINJA TURTLES",
            "section": "Officially Licensed Collabs",
        },
        "new-in-adventure-time": {
            "url": "https://us.shein.com/StoreSelection/Adventure-Time-sc-16050017357.html",
            "label": "Adventure Time",
            "section": "Officially Licensed Collabs",
        },
        "new-in-transformers": {
            "url": "https://us.shein.com/StoreSelection/Transformers-sc-16050018961.html",
            "label": "Transformers",
            "section": "Officially Licensed Collabs",
        },
        "new-in-harley-quinn": {
            "url": "https://us.shein.com/recommend/Harley-Quinn-JOKER-sc-10050092680.html",
            "label": "Harley Quinn",
            "section": "Officially Licensed Collabs",
        },
        "new-in-trolls": {
            "url": "https://us.shein.com/StoreSelection/Trolls-sc-16050070620.html",
            "label": "Trolls",
            "section": "Officially Licensed Collabs",
        },
        "new-in-kung-fu-panda": {
            "url": "https://us.shein.com/StoreSelection/Kungfu-Panda-sc-16050070625.html",
            "label": "Kung Fu Panda",
            "section": "Officially Licensed Collabs",
        },
        "new-in-hot-stuff": {
            "url": "https://us.shein.com/StoreSelection/Hot-stuff-sc-16050070619.html",
            "label": "Hot Stuff",
            "section": "Officially Licensed Collabs",
        },
        "new-in-strawberry-shortcake": {
            "url": "https://us.shein.com/StoreSelection/Strawberry-Shortcake-sc-16050014323.html",
            "label": "Strawberry Shortcake",
            "section": "Officially Licensed Collabs",
        },
        "new-in-frida-kahlo": {
            "url": "https://us.shein.com/StoreSelection/Frida-Kahlo-sc-16050014314.html",
            "label": "Frida Kahlo",
            "section": "Officially Licensed Collabs",
        },
        "new-in-x-felipe-collab": {
            "url": "https://us.shein.com/StoreSelection/SHEIN-X-Felipe-sc-16050025126.html",
            "label": "x FELIPE COLLAB",
            "section": "#SHEIN X",
        },
        "new-in-it-girl": {
            "url": "https://us.shein.com/StoreSelection/Y2Kool-Best-Sellers-sc-16050012223.html",
            "label": "IT GIRL",
            "section": "#SHEIN X",
        },
        "new-in-boho-elegant": {
            "url": "https://us.shein.com/StoreSelection/Best-Sellers-sc-16050011861.html",
            "label": "BOHO ELEGANT",
            "section": "#SHEIN X",
        },
        "new-in-nye-party": {
            "url": "https://us.shein.com/StoreSelection/SHEIN-X-Party-Sequin-Collection-sc-16050018232.html",
            "label": "NYE PARTY",
            "section": "#SHEIN X",
        },
        "new-in-new-in": {
            "url": "https://us.shein.com/StoreSelection/SHEIN-X-New-Arrivals-sc-16050012231.html",
            "label": "NEW IN",
            "section": "#SHEIN X",
        },
        "new-in-best-seller": {
            "url": "https://us.shein.com/StoreSelection/SHEIN-X-Best-Sellers-sc-16050012230.html",
            "label": "BEST SELLER",
            "section": "#SHEIN X",
        },
        "new-in-sale": {
            "url": "https://us.shein.com/StoreSelection/SHEINX-Clearance-sc-16050012232.html",
            "label": "Sale",
            "section": "#SHEIN X",
        },
        "new-in-women-jewelry-accs": {
            "url": "https://us.shein.com/recommend/SHEIN-sc-10050023194.html",
            "label": "Women Jewelry & Accs",
            "section": "New in Other Categories",
        },
        "new-in-women-shoes": {
            "url": "https://us.shein.com/new/New-In-Shoes-sc-00200195.html",
            "label": "Women Shoes",
            "section": "New in Other Categories",
        },
        "new-in-women-bags": {
            "url": "https://us.shein.com/new/New-In-Bags-sc-00200196.html",
            "label": "Women Bags",
            "section": "New in Other Categories",
        },
        "new-in-men-clothing": {
            "url": "https://us.shein.com/new/Men-new-in-sc-00200410.html",
            "label": "Men Clothing",
            "section": "New in Other Categories",
        },
        "new-in-kids": {
            "url": "https://us.shein.com/recommend/Kids-New-In-All-sc-10050070623.html",
            "label": "Kids",
            "section": "New in Other Categories",
        },
        "new-in-baby-maternity": {
            "url": "https://us.shein.com/new/BABY-MATERNITY-sc-002143931.html",
            "label": "Baby & Maternity",
            "section": "New in Other Categories",
        },
        "new-in-men-s-underwear": {
            "url": "https://us.shein.com/recommend/New-in-Men-Underwear-sc-10050013244.html",
            "label": "Men's Underwear",
            "section": "New in Other Categories",
        },
        "new-in-men-s-loungewear": {
            "url": "https://us.shein.com/recommend/New-in-Men-Loungewear-sc-10050013245.html",
            "label": "Men's Loungewear",
            "section": "New in Other Categories",
        },
        "new-in-men-s-socks-accessories": {
            "url": "https://us.shein.com/recommend/Men-socks-accessories-sc-10050013247.html",
            "label": "Men's Socks & Accessories",
            "section": "New in Other Categories",
        },
        "new-in-home-kitchen": {
            "url": "https://us.shein.com/recommend/Home-and-Living-New-In-sc-100121307.html",
            "label": "Home & Kitchen",
            "section": "New in Other Categories",
        },
        "new-in-tools-home-improvement": {
            "url": "https://us.shein.com/recommend/Tools-and-Home-Improvement-New-In-sc-100121311.html",
            "label": "Tools & Home Improvement",
            "section": "New in Other Categories",
        },
        "new-in-home-textile": {
            "url": "https://us.shein.com/recommend/Home-Textile-and-Sewing-New-In-sc-100121309.html",
            "label": "Home Textile",
            "section": "New in Other Categories",
        },
        "new-in-sports-outdoor": {
            "url": "https://us.shein.com/recommend/Sports-and-Outdoor-New-In-sc-100121305.html",
            "label": "Sports & Outdoor",
            "section": "New in Other Categories",
        },
        "new-in-office-school-supplies": {
            "url": "https://us.shein.com/recommend/Office-and-School-Supplies-New-In-sc-100121323.html",
            "label": "Office & School Supplies",
            "section": "New in Other Categories",
        },
        "new-in-electronics": {
            "url": "https://us.shein.com/recommend/Electronics-New-In-sc-100121184.html",
            "label": "Electronics",
            "section": "New in Other Categories",
        },
        "new-in-automotive": {
            "url": "https://us.shein.com/recommend/Automotive-New-In-sc-100121185.html",
            "label": "Automotive",
            "section": "New in Other Categories",
        },
        "new-in-pet-supplies": {
            "url": "https://us.shein.com/recommend/Pet-Supplies-New-In-sc-100121330.html",
            "label": "Pet Supplies",
            "section": "New in Other Categories",
        },
        "new-in-bags-luggage": {
            "url": "https://us.shein.com/new/LUGGAGE-TRAVEL-new-sc-002143992.html",
            "label": "Bags & Luggage",
            "section": "New in Other Categories",
        },
        "new-in-appliances": {
            "url": "https://us.shein.com/recommend/Appliances-New-In-sc-100121319.html",
            "label": "Appliances",
            "section": "New in Other Categories",
        },
        "new-in-toys": {
            "url": "https://us.shein.com/recommend/Toys-New-In-sc-100121328.html",
            "label": "Toys",
            "section": "New in Other Categories",
        },
        "new-in-view-all-10050027625": {
            "url": "https://us.shein.com/recommend/New-in-customized-sc-10050027625.html",
            "label": "View All",
            "section": "New in Customized Gifts",
        },
        "new-in-home-textile-10050014432": {
            "url": "https://us.shein.com/recommend/home-textile-customized-gifts-sc-10050014432.html",
            "label": "Home Textile",
            "section": "New in Customized Gifts",
        },
        "new-in-home-living": {
            "url": "https://us.shein.com/recommend/Home-Living-sc-10050000879.html",
            "label": "Home & Living",
            "section": "New in Customized Gifts",
        },
        "new-in-jewelry-watches": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Jewelry-Watches-sc-10050009108.html",
            "label": "Jewelry & Watches",
            "section": "New in Customized Gifts",
        },
        "new-in-cell-phones-accessories": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Cell-Phones-and-Accessories-sc-10050009222.html",
            "label": "Cell Phones & Accessories",
            "section": "New in Customized Gifts",
        },
        "new-in-office-school-supplies-10050009231": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Office-School-Supplies-sc-10050009231.html",
            "label": "Office & School Supplies",
            "section": "New in Customized Gifts",
        },
        "new-in-apparel-accessories": {
            "url": "https://us.shein.com/recommend/Customized-acc-sc-10050013283.html",
            "label": "Apparel Accessories",
            "section": "New in Customized Gifts",
        },
        "new-in-bags-luggage-10050009221": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Bags-and-Luggage-sc-10050009221.html",
            "label": "Bags & Luggage",
            "section": "New in Customized Gifts",
        },
        "new-in-underwear-sleepwear": {
            "url": "https://us.shein.com/recommend/New-in-customized-under-sleep-sc-10050013291.html",
            "label": "Underwear & Sleepwear",
            "section": "New in Customized Gifts",
        },
        "new-in-pet-supplies-10050009153": {
            "url": "https://us.shein.com/recommend/342134322-sc-10050009153.html",
            "label": "Pet Supplies",
            "section": "New in Customized Gifts",
        },
        "new-in-tools-home-improvement-10050009227": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Tools-and-Home-Improvement-sc-10050009227.html",
            "label": "Tools & Home Improvement",
            "section": "New in Customized Gifts",
        },
        "new-in-women-apparel": {
            "url": "https://us.shein.com/recommend/customized-gifts-sc-10050008591.html",
            "label": "Women Apparel",
            "section": "New in Customized Gifts",
        },
        "new-in-beauty-health": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Beauty-and-Health-sc-10050009150.html",
            "label": "Beauty & Health",
            "section": "New in Customized Gifts",
        },
        "new-in-kids-10050009149": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Kids-sc-10050009149.html",
            "label": "Kids",
            "section": "New in Customized Gifts",
        },
        "new-in-sports-outdoor-10050009218": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Sports-and-Outdoor-sc-10050009218.html",
            "label": "Sports & Outdoor",
            "section": "New in Customized Gifts",
        },
        "new-in-men": {
            "url": "https://us.shein.com/recommend/New-in-Customized-Men-sc-10050009113.html",
            "label": "Men",
            "section": "New in Customized Gifts",
        },
    },
    "sale": {
        "sale": {
            "url": "https://us.shein.com/sale/All-Sale-sc-0051884505.html",
            "label": "Sale",
            "section": "Top category",
        },
        "sale-women": {
            "url": "https://us.shein.com/recommend/Women-sale-sc-10050026150.html",
            "label": "Women",
            "section": "Shop by Category",
        },
        "sale-curve": {
            "url": "https://us.shein.com/recommend/curve-sc-10050026165.html",
            "label": "Curve",
            "section": "Shop by Category",
        },
        "sale-women-tops": {
            "url": "https://us.shein.com/recommend/Women-Tops-sc-10050026151.html",
            "label": "Women Tops",
            "section": "Shop by Category",
        },
        "sale-women-dresses": {
            "url": "https://us.shein.com/recommend/Women-Dresses-sc-10050026152.html",
            "label": "Women Dresses",
            "section": "Shop by Category",
        },
        "sale-women-knitwear": {
            "url": "https://us.shein.com/recommend/Women-Knitwear-sc-10050026153.html",
            "label": "Women Knitwear",
            "section": "Shop by Category",
        },
        "sale-women-bottoms": {
            "url": "https://us.shein.com/recommend/Women-Bottoms-sc-10050026154.html",
            "label": "Women Bottoms",
            "section": "Shop by Category",
        },
        "sale-women-denim": {
            "url": "https://us.shein.com/recommend/Women-Denim-sc-10050026155.html",
            "label": "Women Denim",
            "section": "Shop by Category",
        },
        "sale-women-two-pieces": {
            "url": "https://us.shein.com/recommend/Women-Two-piece-sc-10050026157.html",
            "label": "Women Two Pieces",
            "section": "Shop by Category",
        },
        "sale-sleep-lounge": {
            "url": "https://us.shein.com/recommend/sale-women-Sleep-Lounge-sc-10050013280.html",
            "label": "Sleep & Lounge",
            "section": "Shop by Category",
        },
        "sale-underwear": {
            "url": "https://us.shein.com/recommend/sale-Underwear-sc-10050013253.html",
            "label": "Underwear",
            "section": "Shop by Category",
        },
        "sale-kids": {
            "url": "https://us.shein.com/hotsale/Kids-On-Sale-sc-0031653311.html",
            "label": "Kids",
            "section": "Shop by Category",
        },
        "sale-baby": {
            "url": "https://us.shein.com/hotsale/Baby-On-Sale-sc-0031653314.html",
            "label": "Baby",
            "section": "Shop by Category",
        },
        "sale-shoes": {
            "url": "https://us.shein.com/recommend/shoessale-sc-10050085845.html",
            "label": "Shoes",
            "section": "Shop by Category",
        },
        "sale-home-living": {
            "url": "https://us.shein.com/recommend/Home-Living-sc-10050000879.html",
            "label": "Home & Living",
            "section": "Shop by Category",
        },
        "sale-beauty-health": {
            "url": "https://us.shein.com/recommend/SHEIN-sc-10050023232.html",
            "label": "Beauty & Health",
            "section": "Shop by Category",
        },
        "sale-sports-outdoors": {
            "url": "https://us.shein.com/sale/Sport-SALE-sc-0051700655.html",
            "label": "Sports & Outdoors",
            "section": "Shop by Category",
        },
        "sale-socks-lingerie-accessories": {
            "url": "https://us.shein.com/recommend/sale-Socks-lingerie-accessories-sc-10050013257.html",
            "label": "Socks & Lingerie Accessories",
            "section": "Shop by Category",
        },
        "sale-women-jewelry": {
            "url": "https://us.shein.com/recommend/Women-Jewelry-Sale-sc-10050013873.html",
            "label": "Women Jewelry",
            "section": "Shop by Category",
        },
        "sale-men-jewelry": {
            "url": "https://us.shein.com/sale/Men-Jewelry-Sale-sc-005253323.html",
            "label": "Men Jewelry",
            "section": "Shop by Category",
        },
        "sale-accessories": {
            "url": "https://us.shein.com/sale/Accessories-Sale-sc-005215718.html",
            "label": "Accessories",
            "section": "Shop by Category",
        },
        "sale-bags-luggage": {
            "url": "https://us.shein.com/sale/Bags-Sale-sc-0051654811.html",
            "label": "Bags & Luggage",
            "section": "Shop by Category",
        },
        "sale-tools-home-improvement": {
            "url": "https://us.shein.com/recommend/tools-home-improvement-sc-10050000902.html",
            "label": "Tools & Home Improvement",
            "section": "Shop by Category",
        },
        "sale-home-textile": {
            "url": "https://us.shein.com/sale/Home-Textile-on-Sales-sc-0051655174.html",
            "label": "Home Textile",
            "section": "Shop by Category",
        },
        "sale-cell-phones-accessories": {
            "url": "https://us.shein.com/sale/Cellphone-ACC-Sale-sc-0051654816.html",
            "label": "Cell Phones Accessories",
            "section": "Shop by Category",
        },
        "sale-toys-games": {
            "url": "https://us.shein.com/recommend/Toys-Games-sc-10050000904.html",
            "label": "Toys & Games",
            "section": "Shop by Category",
        },
        "sale-office-school-supplies": {
            "url": "https://us.shein.com/recommend/Office-School-Supplies-sc-10050000903.html",
            "label": "Office & School Supplies",
            "section": "Shop by Category",
        },
        "sale-appliances": {
            "url": "https://us.shein.com/style/salesdianqi-sc-0011655083.html",
            "label": "Appliances",
            "section": "Shop by Category",
        },
        "sale-pet-supplies": {
            "url": "https://us.shein.com/sale/Pet-ALL-CATEGORY-sc-0051655092.html",
            "label": "Pet Supplies",
            "section": "Shop by Category",
        },
        "sale-customization": {
            "url": "https://us.shein.com/recommend/customization-sc-10050013875.html",
            "label": "Customization",
            "section": "Shop by Category",
        },
        "sale-intimates": {
            "url": "https://us.shein.com/recommend/sale-women-intimates-sc-10050013284.html",
            "label": "Intimates",
            "section": "Shop by Category",
        },
        "sale-women-sales": {
            "url": "https://us.shein.com/Women-sales-sc-10050109887.html",
            "label": "Women sales",
            "section": "Shop by Category",
        },
        "sale-sale": {
            "url": "https://us.shein.com/sale/New-In-Sale-sc-005215727.html",
            "label": "Sale",
            "section": "Special Offers",
        },
        "sale-bestsellers-on-sale": {
            "url": "https://us.shein.com/sale/Bestsellers-On-Sale-sc-005215734.html",
            "label": "Bestsellers on Sale",
            "section": "Special Offers",
        },
        "sale-special-sale": {
            "url": "https://us.shein.com/recommend/Sale-sc-1001712617.html",
            "label": "Special Sale",
            "section": "Special Offers",
        },
        "sale-motf": {
            "url": "https://us.shein.com/sale/MOTF-little-price-sc-00539416.html",
            "label": "MOTF",
            "section": "Brands",
        },
        "sale-emery-rose": {
            "url": "https://us.shein.com/sale/EMERY-ROSE-On-SALE-sc-00552256.html",
            "label": "EMERY ROSE",
            "section": "Brands",
        },
        "sale-luvlette": {
            "url": "https://us.shein.com/Brands/Luvlette-SALE-sc-01460011.html",
            "label": "LUVLETTE",
            "section": "Brands",
        },
        "sale-dazy": {
            "url": "https://us.shein.com/sale/DAZY-SALE-sc-00552227.html",
            "label": "DAZY",
            "section": "Brands",
        },
        "sale-romwe": {
            "url": "https://us.shein.com/sale/ROMWE-SALE-sc-00568793.html",
            "label": "ROMWE",
            "section": "Brands",
        },
        "sale-glowmode": {
            "url": "https://us.shein.com/sale/GLOWMODE-SALE-sc-0051654552.html",
            "label": "GLOWMODE",
            "section": "Brands",
        },
        "sale-cuccoo": {
            "url": "https://us.shein.com/sale/Cuccoo-Sale-sc-00555109.html",
            "label": "CUCCOO",
            "section": "Brands",
        },
        "sale-anewsta": {
            "url": "https://us.shein.com/Series/Anewsta-sc-666205663.html",
            "label": "Anewsta",
            "section": "Brands",
        },
        "sale-missguided": {
            "url": "https://us.shein.com/StoreSelection/MISSGUIDED-SALE-sc-16050023326.html",
            "label": "MISSGUIDED",
            "section": "Brands",
        },
        "sale-sumwon": {
            "url": "https://us.shein.com/StoreSelection/SUMWON-Sale-sc-16050023327.html",
            "label": "SUMWON",
            "section": "Brands",
        },
    },
    "women": {
        "women": {
            "url": "https://us.shein.com/RecommendSelection/Women-Clothing-sc-017172961.html",
            "label": "Women Clothing",
            "section": "Top category",
        },
        "women-view-all": {
            "url": "https://us.shein.com/Women-Clothing-c-2030.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "women-new-in": {
            "url": "https://us.shein.com/recommend/NEW-IN-sc-10050029500.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "women-top-rated": {
            "url": "https://us.shein.com/recommend/Top-rated-sc-10050029503.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "women-tops": {
            "url": "https://us.shein.com/Women-Tops,-Blouses-Tee-c-1766.html",
            "label": "Tops",
            "section": "Shop by Category",
        },
        "women-t-shirts": {
            "url": "https://us.shein.com/Women-T-Shirts-c-1738.html",
            "label": "T-shirts",
            "section": "Shop by Category",
        },
        "women-blouses": {
            "url": "https://us.shein.com/Women-Blouses-c-1733.html",
            "label": "Blouses",
            "section": "Shop by Category",
        },
        "women-tank-tops-camis": {
            "url": "https://us.shein.com/Women-Tank-Tops-Camis-c-1779.html",
            "label": "Tank Tops & Camis",
            "section": "Shop by Category",
        },
        "women-dresses": {
            "url": "https://us.shein.com/Women-Dresses-c-12472.html",
            "label": "Dresses",
            "section": "Shop by Category",
        },
        "women-long-dresses": {
            "url": "https://us.shein.com/Women-Midi-Dresses-c-12478.html",
            "label": "Long Dresses",
            "section": "Shop by Category",
        },
        "women-mini-dresses": {
            "url": "https://us.shein.com/Women-Mini-Dresses-c-12475.html",
            "label": "Mini Dresses",
            "section": "Shop by Category",
        },
        "women-knitwear": {
            "url": "https://us.shein.com/Women-Knitwear-c-2216.html",
            "label": "Knitwear",
            "section": "Shop by Category",
        },
        "women-sweaters": {
            "url": "https://us.shein.com/Women-Sweaters-c-1734.html",
            "label": "Sweaters",
            "section": "Shop by Category",
        },
        "women-bottoms": {
            "url": "https://us.shein.com/Women-Bottoms-c-1767.html",
            "label": "Bottoms",
            "section": "Shop by Category",
        },
        "women-pants": {
            "url": "https://us.shein.com/Women-Pants-c-1740.html",
            "label": "Pants",
            "section": "Shop by Category",
        },
        "women-outerwear": {
            "url": "https://us.shein.com/Women-Outerwear-c-2037.html",
            "label": "Outerwear",
            "section": "Shop by Category",
        },
        "women-denim": {
            "url": "https://us.shein.com/Women-Denim-c-1930.html",
            "label": "Denim",
            "section": "Shop by Category",
        },
        "women-co-ords": {
            "url": "https://us.shein.com/Women-Co-ords-c-2040.html",
            "label": "Co-ords",
            "section": "Shop by Category",
        },
        "women-sweatshirts": {
            "url": "https://us.shein.com/Women-Sweatshirts-Hoodies-c-1773.html",
            "label": "Sweatshirts",
            "section": "Shop by Category",
        },
        "women-jumpsuits-bodysuits": {
            "url": "https://us.shein.com/Women-Jumpsuits-Bodysuits-c-3287.html",
            "label": "Jumpsuits & Bodysuits",
            "section": "Shop by Category",
        },
        "women-suits": {
            "url": "https://us.shein.com/Women-Suits-c-2036.html",
            "label": "Suits",
            "section": "Shop by Category",
        },
        "women-beachwear": {
            "url": "https://us.shein.com/Women-Beachwear-c-2039.html",
            "label": "Beachwear",
            "section": "Shop by Category",
        },
        "women-party-wear": {
            "url": "https://us.shein.com/Women-Party-Wear-c-5360.html",
            "label": "Party Wear",
            "section": "Shop by Category",
        },
        "women-maternity-clothing": {
            "url": "https://us.shein.com/Maternity-Clothing-c-4437.html",
            "label": "Maternity Clothing",
            "section": "Shop by Category",
        },
        "women-wedding": {
            "url": "https://us.shein.com/Women-Wedding-c-3090.html",
            "label": "Wedding",
            "section": "Shop by Category",
        },
        "women-women-ageless-clothing": {
            "url": "https://us.shein.com/Women-Senior-Clothing-c-14476.html",
            "label": "Women Ageless Clothing",
            "section": "Shop by Category",
        },
        "women-new-season": {
            "url": "https://us.shein.com/NEW-SEASON-sc-10050108866.html",
            "label": "NEW SEASON",
            "section": "Shop by Category",
        },
        "women-long-dresses-12476": {
            "url": "https://us.shein.com/Women-Long-Dresses-c-12476.html",
            "label": "Long Dresses",
            "section": "Dresses",
        },
        "women-short-dresses": {
            "url": "https://us.shein.com/Women-Short-Dresses-c-1727.html",
            "label": "Short Dresses",
            "section": "Dresses",
        },
        "women-maxi-dresses": {
            "url": "https://us.shein.com/Women-Maxi-Dresses-c-12480.html",
            "label": "Maxi Dresses",
            "section": "Dresses",
        },
        "women-knit-tops": {
            "url": "https://us.shein.com/Women-Knit-Tops-c-2217.html",
            "label": "Knit Tops",
            "section": "Knitwear",
        },
        "women-lightweight-cardigans": {
            "url": "https://us.shein.com/Women-Lightweight-Cardigans-c-12318.html",
            "label": "Lightweight Cardigans",
            "section": "Knitwear",
        },
        "women-sweater-dresses": {
            "url": "https://us.shein.com/Women-Sweater-Dresses-c-2218.html",
            "label": "Sweater Dresses",
            "section": "Knitwear",
        },
        "women-sweater-co-ords": {
            "url": "https://us.shein.com/Women-Sweater-Co-ords-c-2220.html",
            "label": "Sweater Co-ords",
            "section": "Knitwear",
        },
        "women-cardigans": {
            "url": "https://us.shein.com/Women-Cardigans-c-2219.html",
            "label": "Cardigans",
            "section": "Knitwear",
        },
        "women-sweater-vests": {
            "url": "https://us.shein.com/Women-Sweater-Vests-c-3807.html",
            "label": "Sweater Vests",
            "section": "Knitwear",
        },
        "women-sweater-skirts": {
            "url": "https://us.shein.com/Women-Sweater-Skirts-c-2221.html",
            "label": "Sweater Skirts",
            "section": "Knitwear",
        },
        "women-skirts": {
            "url": "https://us.shein.com/Women-Skirts-c-1732.html",
            "label": "Skirts",
            "section": "Bottoms",
        },
        "women-shorts": {
            "url": "https://us.shein.com/Women-Shorts-c-1912.html",
            "label": "Shorts",
            "section": "Bottoms",
        },
        "women-sweatpants": {
            "url": "https://us.shein.com/Women-Sweatpants-c-2990.html",
            "label": "Sweatpants",
            "section": "Bottoms",
        },
        "women-leggings": {
            "url": "https://us.shein.com/Women-Leggings-c-1871.html",
            "label": "Leggings",
            "section": "Bottoms",
        },
        "women-jackets": {
            "url": "https://us.shein.com/Women-Jackets-c-1776.html",
            "label": "Jackets",
            "section": "Outerwear",
        },
        "women-coats": {
            "url": "https://us.shein.com/Women-Coats-c-1735.html",
            "label": "Coats",
            "section": "Outerwear",
        },
        "women-winter-coats": {
            "url": "https://us.shein.com/Women-Winter-Coats-c-3052.html",
            "label": "Winter Coats",
            "section": "Outerwear",
        },
        "women-overcoats": {
            "url": "https://us.shein.com/Women-Overcoats-c-3051.html",
            "label": "Overcoats",
            "section": "Outerwear",
        },
        "women-lightweight-jackets": {
            "url": "https://us.shein.com/Women-Lightweight-Jackets-c-12312.html",
            "label": "Lightweight Jackets",
            "section": "Outerwear",
        },
        "women-faux-fur-coats": {
            "url": "https://us.shein.com/Women-Faux-Fur-Coats-c-3054.html",
            "label": "Faux Fur Coats",
            "section": "Outerwear",
        },
        "women-trench-coats": {
            "url": "https://us.shein.com/Women-Trench-Coats-c-3050.html",
            "label": "Trench Coats",
            "section": "Outerwear",
        },
        "women-down-coats": {
            "url": "https://us.shein.com/Women-Down-Coats-c-3053.html",
            "label": "Down Coats",
            "section": "Outerwear",
        },
        "women-jeans": {
            "url": "https://us.shein.com/Women-Jeans-c-1934.html",
            "label": "Jeans",
            "section": "Denim",
        },
        "women-denim-skirts": {
            "url": "https://us.shein.com/Women-Denim-Skirts-c-1937.html",
            "label": "Denim Skirts",
            "section": "Denim",
        },
        "women-denim-shorts": {
            "url": "https://us.shein.com/Women-Denim-Shorts-c-1935.html",
            "label": "Denim Shorts",
            "section": "Denim",
        },
        "women-denim-jackets-coats": {
            "url": "https://us.shein.com/Women-Denim-Jackets-Coats-c-1933.html",
            "label": "Denim Jackets & Coats",
            "section": "Denim",
        },
        "women-denim-overalls-jumpsuits": {
            "url": "https://us.shein.com/Women-Denim-Overalls-Jumpsuits-c-1936.html",
            "label": "Denim Overalls & Jumpsuits",
            "section": "Denim",
        },
        "women-denim-dresses": {
            "url": "https://us.shein.com/Women-Denim-Dresses-c-1931.html",
            "label": "Denim Dresses",
            "section": "Denim",
        },
        "women-denim-tops": {
            "url": "https://us.shein.com/Women-Denim-Tops-c-1932.html",
            "label": "Denim Tops",
            "section": "Denim",
        },
        "women-denim-two-piece-outfits": {
            "url": "https://us.shein.com/Women-Denim-Two-piece-Outfits-c-2052.html",
            "label": "Denim Two-piece Outfits",
            "section": "Denim",
        },
        "women-view-all-1773": {
            "url": "https://us.shein.com/Women-Sweatshirts-c-1773.html",
            "label": "View All",
            "section": "Hoodies & Sweatshirts",
        },
        "women-hoodies": {
            "url": "https://us.shein.com/recommend/Hoodies-sc-10050029555.html",
            "label": "Hoodies",
            "section": "Hoodies & Sweatshirts",
        },
        "women-sweatshirts-10050029559": {
            "url": "https://us.shein.com/recommend/Sweatshirts-sc-10050029559.html",
            "label": "Sweatshirts",
            "section": "Hoodies & Sweatshirts",
        },
        "women-jumpsuits": {
            "url": "https://us.shein.com/Women-Jumpsuits-c-1860.html",
            "label": "Jumpsuits",
            "section": "Jumpsuits & Bodysuits",
        },
        "women-bodysuits": {
            "url": "https://us.shein.com/Women-Bodysuits-c-1882.html",
            "label": "Bodysuits",
            "section": "Jumpsuits & Bodysuits",
        },
        "women-unitards": {
            "url": "https://us.shein.com/Women-Unitards-c-3289.html",
            "label": "Unitards",
            "section": "Jumpsuits & Bodysuits",
        },
        "women-blazers": {
            "url": "https://us.shein.com/Women-Blazers-c-1739.html",
            "label": "Blazers",
            "section": "Suits",
        },
        "women-suit-sets": {
            "url": "https://us.shein.com/Women-Suit-Sets-c-2977.html",
            "label": "Suit Sets",
            "section": "Suits",
        },
        "women-suit-pants": {
            "url": "https://us.shein.com/Women-Suit-Pants-c-3097.html",
            "label": "Suit Pants",
            "section": "Suits",
        },
        "women-lightweight-blazers": {
            "url": "https://us.shein.com/Women-Lightweight-Blazers-c-12316.html",
            "label": "Lightweight Blazers",
            "section": "Suits",
        },
        "women-bikini-sets": {
            "url": "https://us.shein.com/Women-Bikini-Sets-c-1866.html",
            "label": "Bikini Sets",
            "section": "Beachwear",
        },
        "women-one-pieces": {
            "url": "https://us.shein.com/Women-One-Pieces-c-2193.html",
            "label": "One-pieces",
            "section": "Beachwear",
        },
        "women-cover-ups": {
            "url": "https://us.shein.com/Women-Cover-Ups-c-2176.html",
            "label": "Cover Ups",
            "section": "Beachwear",
        },
        "women-tankinis": {
            "url": "https://us.shein.com/Women-Tankinis-c-2194.html",
            "label": "Tankinis",
            "section": "Beachwear",
        },
        "women-bikini-bottoms": {
            "url": "https://us.shein.com/Women-Bikini-Bottoms-c-2293.html",
            "label": "Bikini Bottoms",
            "section": "Beachwear",
        },
        "women-bikini-tops": {
            "url": "https://us.shein.com/Women-Bikini-Tops-c-2291.html",
            "label": "Bikini Tops",
            "section": "Beachwear",
        },
        "women-kimonos": {
            "url": "https://us.shein.com/Women-Kimonos-c-1878.html",
            "label": "Kimonos",
            "section": "Beachwear",
        },
        "women-burkinis": {
            "url": "https://us.shein.com/Women-Burkinis-c-8838.html",
            "label": "Burkinis",
            "section": "Beachwear",
        },
        "women-rashguards": {
            "url": "https://us.shein.com/Women-Rashguards-c-8836.html",
            "label": "Rashguards",
            "section": "Beachwear",
        },
        "women-swim-dresses": {
            "url": "https://us.shein.com/Women-Swim-Dresses-c-8835.html",
            "label": "Swim Dresses",
            "section": "Beachwear",
        },
        "women-boardshorts": {
            "url": "https://us.shein.com/Women-Boardshorts-c-8837.html",
            "label": "Boardshorts",
            "section": "Beachwear",
        },
        "women-view-all-3088": {
            "url": "https://us.shein.com/Weddings-Events-c-3088.html",
            "label": "View All",
            "section": "Wedding",
        },
        "women-bridesmaid-dresses": {
            "url": "https://us.shein.com/Bridesmaid-Dresses-c-3091.html",
            "label": "Bridesmaid Dresses",
            "section": "Wedding",
        },
        "women-wedding-dresses": {
            "url": "https://us.shein.com/Wedding-Dresses-c-3089.html",
            "label": "Wedding Dresses",
            "section": "Wedding",
        },
        "women-mother-of-the-bride-dresses": {
            "url": "https://us.shein.com/Mother-of-the-Bride-Dresses-c-3096.html",
            "label": "Mother of the Bride Dresses",
            "section": "Wedding",
        },
        "women-bridal-shower-dresses": {
            "url": "https://us.shein.com/Bridal-Shower-Dresses-c-9502.html",
            "label": "Bridal Shower Dresses",
            "section": "Wedding",
        },
        "women-wedding-other-wear": {
            "url": "https://us.shein.com/Wedding-Other-Wear-c-12042.html",
            "label": "Wedding Other Wear",
            "section": "Wedding",
        },
        "women-wedding-jumpsuits-suits": {
            "url": "https://us.shein.com/Wedding-Jumpsuits-Suits-c-14463.html",
            "label": "Wedding Jumpsuits & Suits",
            "section": "Wedding",
        },
        "women-bridal-robes-kimonos": {
            "url": "https://us.shein.com/Bridal-Robes-Kimonos-c-14466.html",
            "label": "Bridal Robes & Kimonos",
            "section": "Wedding",
        },
        "women-formal-evening-dresses": {
            "url": "https://us.shein.com/Women-Formal-Evening-Dresses-c-9548.html",
            "label": "Formal & Evening Dresses",
            "section": "Party Wear",
        },
        "women-cocktail-dresses": {
            "url": "https://us.shein.com/Women-Cocktail-Dresses-c-8035.html",
            "label": "Cocktail Dresses",
            "section": "Party Wear",
        },
        "women-prom-dresses": {
            "url": "https://us.shein.com/Women-Prom-Dresses-c-5361.html",
            "label": "Prom Dresses",
            "section": "Party Wear",
        },
        "women-party-other-wear": {
            "url": "https://us.shein.com/Women-Party-Other-Wear-c-5362.html",
            "label": "Party Other Wear",
            "section": "Party Wear",
        },
        "women-homecoming-dresses": {
            "url": "https://us.shein.com/recommend/Homecoming-Dresses-sc-10050030290.html",
            "label": "Homecoming Dresses",
            "section": "Party Wear",
        },
        "women-semi-formal-dresses": {
            "url": "https://us.shein.com/recommend/Semi-formal-Dresses-sc-10050030291.html",
            "label": "Semi-formal Dresses",
            "section": "Party Wear",
        },
        "women-maxi-party-dresses": {
            "url": "https://us.shein.com/recommend/Maxi-Party-Dresses-sc-10050030292.html",
            "label": "Maxi Party Dresses",
            "section": "Party Wear",
        },
        "women-modest-evening-dresses": {
            "url": "https://us.shein.com/recommend/Modest-Evening-Dresses-sc-10050030293.html",
            "label": "Modest Evening Dresses",
            "section": "Party Wear",
        },
        "women-maternity-dresses": {
            "url": "https://us.shein.com/Maternity-Dresses-c-2366.html",
            "label": "Maternity Dresses",
            "section": "Maternity Clothing",
        },
        "women-maternity-two-piece-suits": {
            "url": "https://us.shein.com/Maternity-Two-piece-Suits-c-2376.html",
            "label": "Maternity Two-piece Suits",
            "section": "Maternity Clothing",
        },
        "women-maternity-bottoms": {
            "url": "https://us.shein.com/Maternity-Bottoms-c-3234.html",
            "label": "Maternity Bottoms",
            "section": "Maternity Clothing",
        },
        "women-maternity-tops": {
            "url": "https://us.shein.com/Maternity-Tops-c-3616.html",
            "label": "Maternity Tops",
            "section": "Maternity Clothing",
        },
        "women-maternity-denim": {
            "url": "https://us.shein.com/Maternity-Denim-c-4185.html",
            "label": "Maternity Denim",
            "section": "Maternity Clothing",
        },
        "women-nursing": {
            "url": "https://us.shein.com/Nursing-c-5667.html",
            "label": "Nursing",
            "section": "Maternity Clothing",
        },
        "women-maternity-jumpsuits-bodysuits": {
            "url": "https://us.shein.com/Maternity-Jumpsuits-Bodysuits-c-8980.html",
            "label": "Maternity Jumpsuits & Bodysuits",
            "section": "Maternity Clothing",
        },
        "women-maternity-activewear": {
            "url": "https://us.shein.com/Maternity-Activewear-c-9559.html",
            "label": "Maternity Activewear",
            "section": "Maternity Clothing",
        },
        "women-maternity-knitwear": {
            "url": "https://us.shein.com/Maternity-Knitwear-c-13973.html",
            "label": "Maternity Knitwear",
            "section": "Maternity Clothing",
        },
        "women-maternity-outerwear": {
            "url": "https://us.shein.com/Maternity-Outerwear-c-13974.html",
            "label": "Maternity Outerwear",
            "section": "Maternity Clothing",
        },
        "women-labor-delivery-wear": {
            "url": "https://us.shein.com/Labor-Delivery-Wear-c-12311.html",
            "label": "Labor & Delivery Wear",
            "section": "Maternity Clothing",
        },
        "women-view-all-3618": {
            "url": "https://us.shein.com/World-Apparel-c-3618.html",
            "label": "View All",
            "section": "World Apparel",
        },
        "women-arabian-dresses": {
            "url": "https://us.shein.com/Arabian-Dresses-c-1924.html",
            "label": "Arabian Dresses",
            "section": "World Apparel",
        },
        "women-dirndl-dresses": {
            "url": "https://us.shein.com/Traditional-German-Clothing-c-12040.html",
            "label": "Dirndl Dresses",
            "section": "World Apparel",
        },
        "women-yukatas": {
            "url": "https://us.shein.com/Yukatas-c-10158.html",
            "label": "Yukatas",
            "section": "World Apparel",
        },
        "women-cheongsam": {
            "url": "https://us.shein.com/Cheongsam-c-6635.html",
            "label": "Cheongsam",
            "section": "World Apparel",
        },
        "women-ethnic-fusion-wear": {
            "url": "https://us.shein.com/Ethnic-Fusion-Wear-c-2358.html",
            "label": "Ethnic & Fusion Wear",
            "section": "World Apparel",
        },
        "women-kaftan-jalabiya": {
            "url": "https://us.shein.com/Kaftan-Jalabiya-c-3025.html",
            "label": "Kaftan & Jalabiya",
            "section": "World Apparel",
        },
        "women-abayas": {
            "url": "https://us.shein.com/Abayas-c-3026.html",
            "label": "Abayas",
            "section": "World Apparel",
        },
        "women-hanfu": {
            "url": "https://us.shein.com/category/hanfu-all-sc-008284003.html",
            "label": "Hanfu",
            "section": "World Apparel",
        },
        "women-view-all-9096": {
            "url": "https://us.shein.com/Women-Uniforms-Special-Clothing-c-9096.html",
            "label": "View All",
            "section": "Women Uniforms & Special Clothing",
        },
        "women-uniforms-scrubs": {
            "url": "https://us.shein.com/Women-Uniforms-Scrubs-c-9098.html",
            "label": "Uniforms & Scrubs",
            "section": "Women Uniforms & Special Clothing",
        },
        "women-costumes-cosplay-clothing": {
            "url": "https://us.shein.com/Women-Costumes-Cosplay-Clothing-c-9103.html",
            "label": "Costumes & Cosplay Clothing",
            "section": "Women Uniforms & Special Clothing",
        },
    },
    "kids": {
        "kids": {
            "url": "https://us.shein.com/RecommendSelection/Kids-sc-017185550.html",
            "label": "Kids",
            "section": "Top category",
        },
        "kids-view-all": {
            "url": "https://us.shein.com/Kids-c-2031.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "kids-top-rated": {
            "url": "https://us.shein.com/recommend/All_Kids-Shop-By-Category_Top-Rated-sc-1004695175.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "kids-new-in": {
            "url": "https://us.shein.com/recommend/All_Kids-Shop-By-Category_New-in-sc-1004695112.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "kids-teen-girls-13-16-yrs": {
            "url": "https://us.shein.com/recommend/Kids-Teen-Girls-Clothing-All-sc-1004714752.html",
            "label": "Teen Girls (13-16 Yrs)",
            "section": "Shop by Category",
        },
        "kids-tween-girls-8-12-yrs": {
            "url": "https://us.shein.com/recommend/Kids-Tween-Girls-Clothing-All-sc-1004714748.html",
            "label": "Tween Girls (8-12 Yrs)",
            "section": "Shop by Category",
        },
        "kids-young-girls-4-7-yrs": {
            "url": "https://us.shein.com/recommend/Kids-Young-Girls-Clothing-All-sc-1004714744.html",
            "label": "Young Girls（4-7 Yrs）",
            "section": "Shop by Category",
        },
        "kids-teen-boys-13-16yrs": {
            "url": "https://us.shein.com/recommend/Kids-Teen-Boys-Clothing-All-sc-1004714754.html",
            "label": "Teen Boys（13-16Yrs）",
            "section": "Shop by Category",
        },
        "kids-tween-boys-8-12yrs": {
            "url": "https://us.shein.com/recommend/Kids-Tween-Boys-Clothing-All-sc-1004714750.html",
            "label": "Tween Boys (8-12Yrs)",
            "section": "Shop by Category",
        },
        "kids-young-boys-4-7yrs": {
            "url": "https://us.shein.com/recommend/Kids-Young-Boys-Clothing-All-sc-1004714746.html",
            "label": "Young Boys（4-7Yrs）",
            "section": "Shop by Category",
        },
        "kids-baby-girls-0-3-yrs": {
            "url": "https://us.shein.com/recommend/Navigation-Baby-Girls-Clothing-All-sc-1004715039.html",
            "label": "Baby Girls (0-3 Yrs)",
            "section": "Shop by Category",
        },
        "kids-baby-boys-0-3yrs": {
            "url": "https://us.shein.com/recommend/Navigation-Baby-Boys-Clothing-All-sc-1004715040.html",
            "label": "Baby Boys(0-3Yrs)",
            "section": "Shop by Category",
        },
        "kids-newborn-0-9m": {
            "url": "https://us.shein.com/Newborn-Baby-Clothing-c-13039.html",
            "label": "Newborn (0-9M)",
            "section": "Shop by Category",
        },
        "kids-shoes": {
            "url": "https://us.shein.com/category/Kids-and-Teen-Shoes-sc-008390145.html",
            "label": "Shoes",
            "section": "Shop by Category",
        },
        "kids-kids-accessories": {
            "url": "https://us.shein.com/style/Kids-Accessories-all-sc-0011883999.html",
            "label": "Kids Accessories",
            "section": "Shop by Category",
        },
        "kids-baby-supplies": {
            "url": "https://us.shein.com/style/Baby-Acc-All-sc-0011884000.html",
            "label": "Baby Supplies",
            "section": "Shop by Category",
        },
        "kids-all-kids-shop-by-category-best-sellers": {
            "url": "https://us.shein.com/All_Kids-Shop-By-Category_Best-Sellers-sc-10050108879.html",
            "label": "All_Kids Shop By Category_Best Sellers",
            "section": "Shop by Category",
        },
        "kids-holiday": {
            "url": "https://us.shein.com/recommend/Holiday-sc-10050107159.html",
            "label": "Holiday",
            "section": "Shop by Trends",
        },
        "kids-fall-winter": {
            "url": "https://us.shein.com/recommend/FW26-sc-10050095578.html",
            "label": "Fall & Winter",
            "section": "Shop by Trends",
        },
        "kids-trend-stores": {
            "url": "https://us.shein.com/recommend/kids-differentiated-stores-sc-100699186.html",
            "label": "Trend Stores",
            "section": "Shop by Trends",
        },
        "kids-cotton": {
            "url": "https://us.shein.com/trends/Cotton-Kids-sc-006890772.html",
            "label": "Cotton",
            "section": "Shop by Trends",
        },
        "kids-family-outfits": {
            "url": "https://us.shein.com/trends/Family-Outfits-sc-006264269.html",
            "label": "Family Outfits",
            "section": "Shop by Trends",
        },
        "kids-sets": {
            "url": "https://us.shein.com/Young-Girls-Sets-c-14002.html",
            "label": "Sets",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-tops": {
            "url": "https://us.shein.com/Young-Girls-Tops-c-2818.html",
            "label": "Tops",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-dresses": {
            "url": "https://us.shein.com/Young-Girls-Dresses-c-2065.html",
            "label": "Dresses",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-denim": {
            "url": "https://us.shein.com/Young-Girls-Denim-c-2573.html",
            "label": "Denim",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-bottoms": {
            "url": "https://us.shein.com/Young-Girls-Bottoms-c-2819.html",
            "label": "Bottoms",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-outerwear": {
            "url": "https://us.shein.com/Young-Girls-Outerwear-c-2557.html",
            "label": "Outerwear",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-sweatshirts": {
            "url": "https://us.shein.com/Young-Girls-Sweatshirts-c-2115.html",
            "label": "Sweatshirts",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-knitwear": {
            "url": "https://us.shein.com/Young-Girls-Knitwear-c-2527.html",
            "label": "Knitwear",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-partywear": {
            "url": "https://us.shein.com/Young-Girls-Partywear-c-2383.html",
            "label": "Partywear",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-underwear": {
            "url": "https://us.shein.com/Young-Girls-Underwear-c-13735.html",
            "label": "Underwear",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-pajamas": {
            "url": "https://us.shein.com/Young-Girls-Pajamas-c-4767.html",
            "label": "Pajamas",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-beachwear": {
            "url": "https://us.shein.com/Young-Girls-Beachwear-c-3292.html",
            "label": "Beachwear",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-bodysuits-jumpsuits": {
            "url": "https://us.shein.com/Young-Girls-Bodysuits-Jumpsuits-c-2067.html",
            "label": "Bodysuits & Jumpsuits",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-skirts": {
            "url": "https://us.shein.com/Young-Girls-Skirts-c-2123.html",
            "label": "Skirts",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-activewear": {
            "url": "https://us.shein.com/Young-Girls-Activewear-c-4769.html",
            "label": "Activewear",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-costumes": {
            "url": "https://us.shein.com/Young-Girls-Costumes-c-7128.html",
            "label": "Costumes",
            "section": "Young Girls Clothing(4-7Yrs)",
        },
        "kids-view-all-14003": {
            "url": "https://us.shein.com/Tween-Girls-Sets-c-14003.html",
            "label": "View All",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-tops-2813": {
            "url": "https://us.shein.com/Tween-Girls-Tops-c-2813.html",
            "label": "Tops",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-denim-2572": {
            "url": "https://us.shein.com/Tween-Girls-Denim-c-2572.html",
            "label": "Denim",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-dresses-2005": {
            "url": "https://us.shein.com/Tween-Girls-Dresses-c-2005.html",
            "label": "Dresses",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-bottoms-2816": {
            "url": "https://us.shein.com/Tween-Girls-Bottoms-c-2816.html",
            "label": "Bottoms",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-sweatshirts-2013": {
            "url": "https://us.shein.com/Tween-Girls-Sweatshirts-c-2013.html",
            "label": "Sweatshirts",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-knitwear-2526": {
            "url": "https://us.shein.com/Tween-Girls-Knitwear-c-2526.html",
            "label": "Knitwear",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-outerwear-2555": {
            "url": "https://us.shein.com/Tween-Girls-Outerwear-c-2555.html",
            "label": "Outerwear",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-pajamas-2008": {
            "url": "https://us.shein.com/Tween-Girls-Pajamas-c-2008.html",
            "label": "Pajamas",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-underwear-13734": {
            "url": "https://us.shein.com/Tween-Girls-Underwear-c-13734.html",
            "label": "Underwear",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-partywear-2382": {
            "url": "https://us.shein.com/Tween-Girls-Partywear-c-2382.html",
            "label": "Partywear",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-bodysuits-jumpsuits-2007": {
            "url": "https://us.shein.com/Tween-Girls-Bodysuits-Jumpsuits-c-2007.html",
            "label": "Bodysuits & Jumpsuits",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-beachwear-3291": {
            "url": "https://us.shein.com/Tween-Girls-Beachwear-c-3291.html",
            "label": "Beachwear",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-activewear-4770": {
            "url": "https://us.shein.com/Tween-Girls-Activewear-c-4770.html",
            "label": "Activewear",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-skirts-2011": {
            "url": "https://us.shein.com/Tween-Girls-Skirts-c-2011.html",
            "label": "Skirts",
            "section": "Tween Girls Clothing(8-12Yrs)",
        },
        "kids-view-all-6760": {
            "url": "https://us.shein.com/Teen-Girls-Clothing-c-6760.html",
            "label": "View All",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-denim-6797": {
            "url": "https://us.shein.com/Teen-Girls-Denim-c-6797.html",
            "label": "Denim",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-sets-14007": {
            "url": "https://us.shein.com/Teen-Girls-Sets-c-14007.html",
            "label": "Sets",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-tops-6761": {
            "url": "https://us.shein.com/Teen-Girls-Tops-c-6761.html",
            "label": "Tops",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-bottoms-6770": {
            "url": "https://us.shein.com/Teen-Girls-Bottoms-c-6770.html",
            "label": "Bottoms",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-dresses-6766": {
            "url": "https://us.shein.com/Teen-Girls-Dresses-c-6766.html",
            "label": "Dresses",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-sweatshirts-6775": {
            "url": "https://us.shein.com/Teen-Girls-Sweatshirts-c-6775.html",
            "label": "Sweatshirts",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-knitwear-6784": {
            "url": "https://us.shein.com/Teen-Girls-Knitwear-c-6784.html",
            "label": "Knitwear",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-outerwear-6776": {
            "url": "https://us.shein.com/Teen-Girls-Outerwear-c-6776.html",
            "label": "Outerwear",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-underwear-13736": {
            "url": "https://us.shein.com/Teen-Girls-Underwear-c-13736.html",
            "label": "Underwear",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-beachwear-6791": {
            "url": "https://us.shein.com/Teen-Girls-Beachwear-c-6791.html",
            "label": "Beachwear",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-pajamas-6806": {
            "url": "https://us.shein.com/Teen-Girls-Pajamas-c-6806.html",
            "label": "Pajamas",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-partywear-6768": {
            "url": "https://us.shein.com/Teen-Girls-Partywear-c-6768.html",
            "label": "Partywear",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-bodysuits-jumpsuits-6767": {
            "url": "https://us.shein.com/Teen-Girls-Bodysuits-Jumpsuits-c-6767.html",
            "label": "Bodysuits & Jumpsuits",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-skirts-6769": {
            "url": "https://us.shein.com/Teen-Girls-Skirts-c-6769.html",
            "label": "Skirts",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-activewear-6808": {
            "url": "https://us.shein.com/Teen-Girls-Activewear-c-6808.html",
            "label": "Activewear",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-hanfu": {
            "url": "https://us.shein.com/Teen-Girls-Hanfu-c-6809.html",
            "label": "Hanfu",
            "section": "Teen Girls Clothing (13-16 Yrs)",
        },
        "kids-view-all-2059": {
            "url": "https://us.shein.com/Young-Boys-Clothing-c-2059.html",
            "label": "View All",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-sets-14004": {
            "url": "https://us.shein.com/Young-Boys-Sets-c-14004.html",
            "label": "Sets",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-tops-2812": {
            "url": "https://us.shein.com/Young-Boys-Tops-c-2812.html",
            "label": "Tops",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-sweatshirts-2106": {
            "url": "https://us.shein.com/Young-Boys-Sweatshirts-c-2106.html",
            "label": "Sweatshirts",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-knitwear-2525": {
            "url": "https://us.shein.com/Young-Boys-Knitwear-c-2525.html",
            "label": "Knitwear",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-outerwear-2553": {
            "url": "https://us.shein.com/Young-Boys-Outerwear-c-2553.html",
            "label": "Outerwear",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-denim-2571": {
            "url": "https://us.shein.com/Young-Boys-Denim-c-2571.html",
            "label": "Denim",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-bottoms-3615": {
            "url": "https://us.shein.com/Young-Boys-Bottoms-c-3615.html",
            "label": "Bottoms",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-pajamas-4764": {
            "url": "https://us.shein.com/Young-Boys-Pajamas-c-4764.html",
            "label": "Pajamas",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-suits": {
            "url": "https://us.shein.com/Young-Boys-Suits-c-6563.html",
            "label": "Suits",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-underwear-13732": {
            "url": "https://us.shein.com/Young-Boys-Underwear-c-13732.html",
            "label": "Underwear",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-swimwear": {
            "url": "https://us.shein.com/Young-Boys-Swimwear-c-2113.html",
            "label": "Swimwear",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-activewear-4766": {
            "url": "https://us.shein.com/Young-Boys-Activewear-c-4766.html",
            "label": "Activewear",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-costumes-7130": {
            "url": "https://us.shein.com/Young-Boys-Costumes-c-7130.html",
            "label": "Costumes",
            "section": "Young Boys Clothing(3-7Yrs)",
        },
        "kids-view-all-1990": {
            "url": "https://us.shein.com/Tween-Boys-Clothing-c-1990.html",
            "label": "View All",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-sets-14001": {
            "url": "https://us.shein.com/Tween-Boys-Sets-c-14001.html",
            "label": "Sets",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-tops-2600": {
            "url": "https://us.shein.com/Tween-Boys-Tops-c-2600.html",
            "label": "Tops",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-sweatshirts-1998": {
            "url": "https://us.shein.com/Tween-Boys-Sweatshirts-c-1998.html",
            "label": "Sweatshirts",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-knitwear-2524": {
            "url": "https://us.shein.com/Tween-Boys-Knitwear-c-2524.html",
            "label": "Knitwear",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-outerwear-2551": {
            "url": "https://us.shein.com/Tween-Boys-Outerwear-c-2551.html",
            "label": "Outerwear",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-bottoms-3621": {
            "url": "https://us.shein.com/Tween-Boys-Bottoms-c-3621.html",
            "label": "Bottoms",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-denim-2570": {
            "url": "https://us.shein.com/Tween-Boys-Denim-c-2570.html",
            "label": "Denim",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-pajamas-1994": {
            "url": "https://us.shein.com/Tween-Boys-Pajamas-c-1994.html",
            "label": "Pajamas",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-underwear-13731": {
            "url": "https://us.shein.com/Tween-Boys-Underwear-c-13731.html",
            "label": "Underwear",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-suits-6560": {
            "url": "https://us.shein.com/Tween-Boys-Suits-c-6560.html",
            "label": "Suits",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-swimwear-2398": {
            "url": "https://us.shein.com/Tween-Boys-Swimwear-c-2398.html",
            "label": "Swimwear",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-activewear-4771": {
            "url": "https://us.shein.com/Tween-Boys-Activewear-c-4771.html",
            "label": "Activewear",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-hanfu-6561": {
            "url": "https://us.shein.com/Tween-Boys-Hanfu-c-6561.html",
            "label": "Hanfu",
            "section": "Tween Boys Clothing(8-12Yrs)",
        },
        "kids-view-all-14008": {
            "url": "https://us.shein.com/Teen-Boys-Sets-c-14008.html",
            "label": "View All",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-tops-6679": {
            "url": "https://us.shein.com/Teen-Boys-Tops-c-6679.html",
            "label": "Tops",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-sweatshirts-6725": {
            "url": "https://us.shein.com/Teen-Boys-Sweatshirts-c-6725.html",
            "label": "Sweatshirts",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-knitwear-6727": {
            "url": "https://us.shein.com/Teen-Boys-Knitwear-c-6727.html",
            "label": "Knitwear",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-outerwear-6726": {
            "url": "https://us.shein.com/Teen-Boys-Outerwear-c-6726.html",
            "label": "Outerwear",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-denim-6729": {
            "url": "https://us.shein.com/Teen-Boys-Denim-c-6729.html",
            "label": "Denim",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-bottoms-6680": {
            "url": "https://us.shein.com/Teen-Boys-Bottoms-c-6680.html",
            "label": "Bottoms",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-pajamas-6730": {
            "url": "https://us.shein.com/Teen-Boys-Pajamas-c-6730.html",
            "label": "Pajamas",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-underwear-13733": {
            "url": "https://us.shein.com/Teen-Boys-Underwear-c-13733.html",
            "label": "Underwear",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-suits-6733": {
            "url": "https://us.shein.com/Teen-Boys-Suits-c-6733.html",
            "label": "Suits",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-swimwear-6728": {
            "url": "https://us.shein.com/Teen-Boys-Swimwear-c-6728.html",
            "label": "Swimwear",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-activewear-6732": {
            "url": "https://us.shein.com/Teen-Boys-Activewear-c-6732.html",
            "label": "Activewear",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-hanfu-6734": {
            "url": "https://us.shein.com/Teen-Boys-Hanfu-c-6734.html",
            "label": "Hanfu",
            "section": "Teen Boys Clothing (13-16 Yrs)",
        },
        "kids-view-all-2057": {
            "url": "https://us.shein.com/Kids-Shoes-c-2057.html",
            "label": "View All",
            "section": "Shoes",
        },
        "kids-sneakers": {
            "url": "https://us.shein.com/Kids-Sneakers-c-2072.html",
            "label": "Sneakers",
            "section": "Shoes",
        },
        "kids-flats": {
            "url": "https://us.shein.com/Kids-Flats-c-2071.html",
            "label": "Flats",
            "section": "Shoes",
        },
        "kids-sandals": {
            "url": "https://us.shein.com/Kids-Sandals-c-3344.html",
            "label": "Sandals",
            "section": "Shoes",
        },
        "kids-boots": {
            "url": "https://us.shein.com/Kids-Boots-c-2074.html",
            "label": "Boots",
            "section": "Shoes",
        },
        "kids-slippers": {
            "url": "https://us.shein.com/Kids-Slippers-c-6871.html",
            "label": "Slippers",
            "section": "Shoes",
        },
        "kids-clogs": {
            "url": "https://us.shein.com/Kids-Clogs-c-3297.html",
            "label": "Clogs",
            "section": "Shoes",
        },
        "kids-athletic-shoes": {
            "url": "https://us.shein.com/Kids-Athletic-Shoes-c-6248.html",
            "label": "Athletic Shoes",
            "section": "Shoes",
        },
        "kids-loafers-oxfords": {
            "url": "https://us.shein.com/Kids-Loafers-Oxfords-c-12378.html",
            "label": "Loafers & Oxfords",
            "section": "Shoes",
        },
        "kids-pumps": {
            "url": "https://us.shein.com/Kids-Pumps-c-9650.html",
            "label": "Pumps",
            "section": "Shoes",
        },
        "kids-water-shoes": {
            "url": "https://us.shein.com/style/Kids-Water-Shoes-sc-0011711516.html",
            "label": "Water Shoes",
            "section": "Shoes",
        },
        "kids-roller-shoes": {
            "url": "https://us.shein.com/style/Kids-Roller-Shoes-sc-0011711624.html",
            "label": "Roller Shoes",
            "section": "Shoes",
        },
        "kids-dancing-shoes": {
            "url": "https://us.shein.com/style/Kids-Dancing-Shoes-sc-0011711562.html",
            "label": "Dancing Shoes",
            "section": "Shoes",
        },
        "kids-view-all-2384": {
            "url": "https://us.shein.com/Kids-Bags-Luggage-c-2384.html",
            "label": "View All",
            "section": "Bags & Luggage",
        },
        "kids-backpacks": {
            "url": "https://us.shein.com/Kids-Backpacks-c-2385.html",
            "label": "Backpacks",
            "section": "Bags & Luggage",
        },
        "kids-crossbody-bags": {
            "url": "https://us.shein.com/Kids-Crossbody-Bags-c-2068.html",
            "label": "Crossbody Bags",
            "section": "Bags & Luggage",
        },
        "kids-satchels": {
            "url": "https://us.shein.com/Kids-Satchels-c-3299.html",
            "label": "Satchels",
            "section": "Bags & Luggage",
        },
        "kids-bag-sets": {
            "url": "https://us.shein.com/Kids-Bag-Sets-c-2388.html",
            "label": "Bag Sets",
            "section": "Bags & Luggage",
        },
        "kids-waist-bags": {
            "url": "https://us.shein.com/Kids-Waist-Bags-c-2386.html",
            "label": "Waist Bags",
            "section": "Bags & Luggage",
        },
        "kids-shoulder-tote-bags": {
            "url": "https://us.shein.com/Kids-Shoulder-Tote-Bags-c-2387.html",
            "label": "Shoulder & Tote Bags",
            "section": "Bags & Luggage",
        },
        "kids-wallets-cardholders": {
            "url": "https://us.shein.com/Kids-Wallets-Cardholders-c-2389.html",
            "label": "Wallets & Cardholders",
            "section": "Bags & Luggage",
        },
        "kids-toiletry-bags": {
            "url": "https://us.shein.com/Kids-Toiletry-Bags-c-11928.html",
            "label": "Toiletry Bags",
            "section": "Bags & Luggage",
        },
        "kids-luggage-travel-bags": {
            "url": "https://us.shein.com/Kids-Luggage-Travel-Bags-c-6361.html",
            "label": "Luggage & Travel Bags",
            "section": "Bags & Luggage",
        },
        "kids-sport-outdoor-bags": {
            "url": "https://us.shein.com/Kids-Sport-Outdoor-Bags-c-11513.html",
            "label": "Sport & Outdoor Bags",
            "section": "Bags & Luggage",
        },
        "kids-kids-bag-accessories": {
            "url": "https://us.shein.com/Kids-Bag-Accessories-c-8867.html",
            "label": "Kids Bag Accessories",
            "section": "Bags & Luggage",
        },
        "kids-kids-trolley-bags-and-suits": {
            "url": "https://us.shein.com/Kids-Trolley-Bags-And-Suits-c-6364.html",
            "label": "Kids Trolley Bags And Suits",
            "section": "Bags & Luggage",
        },
        "kids-view-all-2022": {
            "url": "https://us.shein.com/Kids-Accessories-c-2022.html",
            "label": "View All",
            "section": "Accessories",
        },
        "kids-hair-accessories": {
            "url": "https://us.shein.com/Kids-Hair-Accessories-c-2023.html",
            "label": "Hair Accessories",
            "section": "Accessories",
        },
        "kids-socks-tights": {
            "url": "https://us.shein.com/category/Kids-Socks-And-Tigthts-sc-008127806.html",
            "label": "Socks & Tights",
            "section": "Accessories",
        },
        "kids-hats": {
            "url": "https://us.shein.com/Baby-Kids-Hats-c-4799.html",
            "label": "Hats",
            "section": "Accessories",
        },
        "kids-gloves": {
            "url": "https://us.shein.com/Baby-Kids-Gloves-c-4800.html",
            "label": "Gloves",
            "section": "Accessories",
        },
        "kids-glasses-eyewear-accessories": {
            "url": "https://us.shein.com/Kids-Glasses-Eyewear-Accessories-c-3850.html",
            "label": "Glasses & Eyewear Accessories",
            "section": "Accessories",
        },
        "kids-scarves": {
            "url": "https://us.shein.com/Kids-Scarves-c-2085.html",
            "label": "Scarves",
            "section": "Accessories",
        },
        "kids-jewelry-watches": {
            "url": "https://us.shein.com/Kids-Jewelry-Watches-c-2453.html",
            "label": "Jewelry & Watches",
            "section": "Accessories",
        },
        "kids-belts-suspenders": {
            "url": "https://us.shein.com/Kids-Belts-Suspenders-c-2076.html",
            "label": "Belts & Suspenders",
            "section": "Accessories",
        },
        "kids-earmuffs": {
            "url": "https://us.shein.com/Kids-Earmuffs-c-2099.html",
            "label": "Earmuffs",
            "section": "Accessories",
        },
        "kids-buttons-pins": {
            "url": "https://us.shein.com/Kids-Buttons-Pins-c-9183.html",
            "label": "Buttons & Pins",
            "section": "Accessories",
        },
        "kids-school-supplies": {
            "url": "https://us.shein.com/Kids-School-Supplies-c-12319.html",
            "label": "School Supplies",
            "section": "Accessories",
        },
        "kids-hair-tools": {
            "url": "https://us.shein.com/Kids-Hair-Tools-c-12329.html",
            "label": "Hair Tools",
            "section": "Accessories",
        },
        "kids-kids-bedding": {
            "url": "https://us.shein.com/Kids-Bedding-c-11519.html",
            "label": "Kids Bedding",
            "section": "Accessories",
        },
        "kids-sports-outdoor-supplies": {
            "url": "https://us.shein.com/Kids-Sports-Outdoor-Supplies-c-12320.html",
            "label": "Sports & Outdoor Supplies",
            "section": "Accessories",
        },
        "kids-kids-collar-accessories": {
            "url": "https://us.shein.com/Kids-Collar-Accessories-c-12330.html",
            "label": "Kids Collar & Accessories",
            "section": "Accessories",
        },
        "kids-customized-kids-supplies": {
            "url": "https://us.shein.com/Customized-Kids-Supplies-c-12516.html",
            "label": "Customized Kids Supplies",
            "section": "Accessories",
        },
    },
    "curve": {
        "curve": {
            "url": "https://us.shein.com/RecommendSelection/Curve-sc-017172964.html",
            "label": "Curve",
            "section": "Top category",
        },
        "curve-view-all": {
            "url": "https://us.shein.com/Women-Plus-Clothing-c-1888.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "curve-new-in": {
            "url": "https://us.shein.com/new/Plus-Size-New-In-15-Days-sc-00210832.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "curve-top-rated": {
            "url": "https://us.shein.com/recommend/Top-Rated-Women-Plus-Clothing-sc-100160427.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "curve-tops": {
            "url": "https://us.shein.com/Plus-Size-Tops-c-2225.html",
            "label": "Tops",
            "section": "Shop by Category",
        },
        "curve-dresses": {
            "url": "https://us.shein.com/Plus-Size-Dresses-c-1889.html",
            "label": "Dresses",
            "section": "Shop by Category",
        },
        "curve-bottoms": {
            "url": "https://us.shein.com/Plus-Size-Bottoms-c-2226.html",
            "label": "Bottoms",
            "section": "Shop by Category",
        },
        "curve-blouses": {
            "url": "https://us.shein.com/Plus-Size-Blouses-c-1891.html",
            "label": "Blouses",
            "section": "Shop by Category",
        },
        "curve-t-shirts": {
            "url": "https://us.shein.com/Plus-Size-T-shirts-c-1890.html",
            "label": "T-shirts",
            "section": "Shop by Category",
        },
        "curve-knitwear": {
            "url": "https://us.shein.com/Plus-Size-Knitwear-c-2227.html",
            "label": "Knitwear",
            "section": "Shop by Category",
        },
        "curve-denim": {
            "url": "https://us.shein.com/Plus-Size-Denim-c-2248.html",
            "label": "Denim",
            "section": "Shop by Category",
        },
        "curve-jumpsuits-bodysuits": {
            "url": "https://us.shein.com/Plus-Size-Jumpsuits-Bodysuits-c-3611.html",
            "label": "Jumpsuits & Bodysuits",
            "section": "Shop by Category",
        },
        "curve-jackets-coats": {
            "url": "https://us.shein.com/Plus-Size-Outerwears-c-2249.html",
            "label": "Jackets & Coats",
            "section": "Shop by Category",
        },
        "curve-hoodies-sweatshirts": {
            "url": "https://us.shein.com/Plus-Size-Sweatshirts-c-2056.html",
            "label": "Hoodies & Sweatshirts",
            "section": "Shop by Category",
        },
        "curve-suits": {
            "url": "https://us.shein.com/Plus-Size-Suits-c-3612.html",
            "label": "Suits",
            "section": "Shop by Category",
        },
        "curve-pants": {
            "url": "https://us.shein.com/Plus-Size-Pants-c-1893.html",
            "label": "Pants",
            "section": "Shop by Category",
        },
        "curve-beachwear": {
            "url": "https://us.shein.com/Women-Plus-Beachwear-c-3613.html",
            "label": "Beachwear",
            "section": "Shop by Category",
        },
        "curve-intimates": {
            "url": "https://us.shein.com/Women-Plus-Intimates-c-2347.html",
            "label": "Intimates",
            "section": "Shop by Category",
        },
        "curve-sleep-lounge": {
            "url": "https://us.shein.com/Women-Plus-Sleep-Lounge-c-2346.html",
            "label": "Sleep & Lounge",
            "section": "Shop by Category",
        },
        "curve-activewear": {
            "url": "https://us.shein.com/Women-Plus-Activewear-c-2491.html",
            "label": "Activewear",
            "section": "Shop by Category",
        },
        "curve-party-wear": {
            "url": "https://us.shein.com/Women-Plus-Party-Wear-c-5363.html",
            "label": "Party Wear",
            "section": "Shop by Category",
        },
        "curve-wedding": {
            "url": "https://us.shein.com/Women-Plus-Wedding-c-3734.html",
            "label": "Wedding",
            "section": "Shop by Category",
        },
        "curve-best-reviewed-women-plus-clothing": {
            "url": "https://us.shein.com/Best-Reviewed-Women-Plus-Clothing-sc-10050114895.html",
            "label": "Best Reviewed Women Plus Clothing",
            "section": "Shop by Category",
        },
        "curve-tank-tops-camis": {
            "url": "https://us.shein.com/Plus-Size-Tank-Tops-Camis-c-2180.html",
            "label": "Tank Tops & Camis",
            "section": "Tops",
        },
        "curve-other-tops": {
            "url": "https://us.shein.com/Plus-Size-Women-Tops-c-2232.html",
            "label": "Other Tops",
            "section": "Tops",
        },
        "curve-long-sleeve": {
            "url": "https://us.shein.com/style/Long-Sleeve-Curve-Tops-sc-00103768.html",
            "label": "Long Sleeve",
            "section": "Tops",
        },
        "curve-fall-dresses": {
            "url": "https://us.shein.com/style/Plus-Fall-Dresses-sc-00127357.html",
            "label": "Fall Dresses",
            "section": "Dresses",
        },
        "curve-casual-dresses": {
            "url": "https://us.shein.com/recommend/Plus-Size-Casual-Dresses-sc-100176456.html",
            "label": "Casual Dresses",
            "section": "Dresses",
        },
        "curve-boho-dresses": {
            "url": "https://us.shein.com/recommend/Plus-Size-Boho-Dresses-sc-100176463.html",
            "label": "Boho Dresses",
            "section": "Dresses",
        },
        "curve-elegant-dresses": {
            "url": "https://us.shein.com/recommend/Plus-Size-Elegant-Dresses-sc-100176464.html",
            "label": "Elegant Dresses",
            "section": "Dresses",
        },
        "curve-glamorous-dresses": {
            "url": "https://us.shein.com/style/Plus-Glamorous-Dresses-sc-00110884.html",
            "label": "Glamorous Dresses",
            "section": "Dresses",
        },
        "curve-short-dresses": {
            "url": "https://us.shein.com/style/Plus-Short-Dresses-sc-00110881.html",
            "label": "Short Dresses",
            "section": "Dresses",
        },
        "curve-midi-dresses": {
            "url": "https://us.shein.com/recommend/Plus-Size-Midi-Dresses-sc-100176405.html",
            "label": "Midi Dresses",
            "section": "Dresses",
        },
        "curve-long-dresses": {
            "url": "https://us.shein.com/recommend/Plus-Size-Long-Dresses-sc-100176406.html",
            "label": "Long Dresses",
            "section": "Dresses",
        },
        "curve-leggings": {
            "url": "https://us.shein.com/Plus-Size-Leggings-c-2233.html",
            "label": "Leggings",
            "section": "Bottoms",
        },
        "curve-jeans": {
            "url": "https://us.shein.com/Plus-Size-Jeans-c-2055.html",
            "label": "Jeans",
            "section": "Bottoms",
        },
        "curve-sweatpants": {
            "url": "https://us.shein.com/Plus-Size-Sweatpants-c-2989.html",
            "label": "Sweatpants",
            "section": "Bottoms",
        },
        "curve-skirts": {
            "url": "https://us.shein.com/Plus-Size-Skirts-c-1892.html",
            "label": "Skirts",
            "section": "Bottoms",
        },
        "curve-denim-shorts": {
            "url": "https://us.shein.com/Plus-Size-Denim-Shorts-c-2236.html",
            "label": "Denim Shorts",
            "section": "Bottoms",
        },
        "curve-shorts": {
            "url": "https://us.shein.com/Plus-Size-Shorts-c-1968.html",
            "label": "Shorts",
            "section": "Bottoms",
        },
        "curve-suit-pants": {
            "url": "https://us.shein.com/Plus-Size-Suit-Pants-c-3178.html",
            "label": "Suit Pants",
            "section": "Bottoms",
        },
        "curve-denim-jackets": {
            "url": "https://us.shein.com/Plus-Size-Denim-Jackets-c-2235.html",
            "label": "Denim Jackets",
            "section": "Denim",
        },
        "curve-denim-skirts": {
            "url": "https://us.shein.com/Plus-Size-Denim-Skirts-c-2237.html",
            "label": "Denim Skirts",
            "section": "Denim",
        },
        "curve-denim-overalls": {
            "url": "https://us.shein.com/Plus-Size-Denim-Overalls-c-2247.html",
            "label": "Denim Overalls",
            "section": "Denim",
        },
        "curve-denim-dresses": {
            "url": "https://us.shein.com/Plus-Size-Denim-Dresses-c-2234.html",
            "label": "Denim Dresses",
            "section": "Denim",
        },
        "curve-denim-tops": {
            "url": "https://us.shein.com/Plus-Size-Denim-Tops-c-2238.html",
            "label": "Denim Tops",
            "section": "Denim",
        },
        "curve-denim-two-piece-outfits": {
            "url": "https://us.shein.com/Plus-Size-Denim-Two-piece-Outfits-c-2246.html",
            "label": "Denim Two-piece Outfits",
            "section": "Denim",
        },
        "curve-sweaters": {
            "url": "https://us.shein.com/Plus-Size-Sweaters-c-1939.html",
            "label": "Sweaters",
            "section": "Sweaters",
        },
        "curve-cardigans": {
            "url": "https://us.shein.com/Plus-Size-Cardigans-c-2241.html",
            "label": "Cardigans",
            "section": "Sweaters",
        },
        "curve-knit-tops": {
            "url": "https://us.shein.com/Plus-Size-Knit-Tops-c-2239.html",
            "label": "Knit Tops",
            "section": "Sweaters",
        },
        "curve-sweater-vests": {
            "url": "https://us.shein.com/Plus-Size-Sweater-Vests-c-3930.html",
            "label": "Sweater Vests",
            "section": "Sweaters",
        },
        "curve-sweater-dresses": {
            "url": "https://us.shein.com/Plus-Size-Sweater-Dresses-c-2240.html",
            "label": "Sweater Dresses",
            "section": "Sweaters",
        },
        "curve-sweater-co-ords": {
            "url": "https://us.shein.com/Plus-Size-Sweater-Co-ords-c-2244.html",
            "label": "Sweater Co-ords",
            "section": "Sweaters",
        },
        "curve-sweater-skirts": {
            "url": "https://us.shein.com/Plus-Size-Sweater-Skirts-c-2242.html",
            "label": "Sweater Skirts",
            "section": "Sweaters",
        },
        "curve-sweater-pants": {
            "url": "https://us.shein.com/Plus-Size-Sweater-Pants-c-2243.html",
            "label": "Sweater Pants",
            "section": "Sweaters",
        },
        "curve-view-all-00802131": {
            "url": "https://us.shein.com/category/Plus-Size-Sets-sc-00802131.html",
            "label": "View All",
            "section": "Jumpsuits & Co-ords",
        },
        "curve-co-ords": {
            "url": "https://us.shein.com/Plus-Size-Co-Ords-c-1928.html",
            "label": "Co-ords",
            "section": "Jumpsuits & Co-ords",
        },
        "curve-skirt-sets": {
            "url": "https://us.shein.com/style/Curvy-Skirt-Sets-sc-00103785.html",
            "label": "Skirt Sets",
            "section": "Jumpsuits & Co-ords",
        },
        "curve-pant-co-ords": {
            "url": "https://us.shein.com/style/Curvy-Pant-Sets-sc-00103783.html",
            "label": "Pant Co-ords",
            "section": "Jumpsuits & Co-ords",
        },
        "curve-jumpsuits": {
            "url": "https://us.shein.com/Plus-Size-Jumpsuits-c-1927.html",
            "label": "Jumpsuits",
            "section": "Jumpsuits & Co-ords",
        },
        "curve-bodysuits": {
            "url": "https://us.shein.com/Plus-Size-Bodysuits-c-2019.html",
            "label": "Bodysuits",
            "section": "Jumpsuits & Co-ords",
        },
        "curve-jackets": {
            "url": "https://us.shein.com/Plus-Size-Jackets-c-2245.html",
            "label": "Jackets",
            "section": "Jackets & Coats",
        },
        "curve-coats": {
            "url": "https://us.shein.com/Plus-Size-Coats-c-1940.html",
            "label": "Coats",
            "section": "Jackets & Coats",
        },
        "curve-winter-coats": {
            "url": "https://us.shein.com/Plus-Size-Winter-Coats-c-3131.html",
            "label": "Winter Coats",
            "section": "Jackets & Coats",
        },
        "curve-overcoats": {
            "url": "https://us.shein.com/Plus-Size-Overcoats-c-3130.html",
            "label": "Overcoats",
            "section": "Jackets & Coats",
        },
        "curve-trench-coats": {
            "url": "https://us.shein.com/Plus-Size-Trench-Coats-c-3100.html",
            "label": "Trench Coats",
            "section": "Jackets & Coats",
        },
        "curve-hoodies": {
            "url": "https://us.shein.com/recommend/Plus-Size-Hoodies-sc-100152305.html",
            "label": "Hoodies",
            "section": "Hoodies & Sweatshirts",
        },
        "curve-sweatshirts": {
            "url": "https://us.shein.com/recommend/Plus-Size-Sweatshirts-sc-100152306.html",
            "label": "Sweatshirts",
            "section": "Hoodies & Sweatshirts",
        },
        "curve-blazers": {
            "url": "https://us.shein.com/Plus-Size-Blazers-c-2179.html",
            "label": "Blazers",
            "section": "Suits",
        },
        "curve-suit-sets": {
            "url": "https://us.shein.com/Plus-Size-Suit-Sets-c-2943.html",
            "label": "Suit Sets",
            "section": "Suits",
        },
        "curve-bikini-sets": {
            "url": "https://us.shein.com/Plus-Size-Bikini-Sets-c-1941.html",
            "label": "Bikini Sets",
            "section": "Beachwear",
        },
        "curve-one-pieces": {
            "url": "https://us.shein.com/Plus-Size-One-Pieces-c-2230.html",
            "label": "One-pieces",
            "section": "Beachwear",
        },
        "curve-tankinis": {
            "url": "https://us.shein.com/Plus-Size-Tankinis-c-2231.html",
            "label": "Tankinis",
            "section": "Beachwear",
        },
        "curve-cover-ups": {
            "url": "https://us.shein.com/Plus-Size-Cover-Ups-c-2229.html",
            "label": "Cover Ups",
            "section": "Beachwear",
        },
        "curve-swim-dresses": {
            "url": "https://us.shein.com/Plus-Size-Swim-Dresses-c-8839.html",
            "label": "Swim Dresses",
            "section": "Beachwear",
        },
        "curve-bikini-bottoms": {
            "url": "https://us.shein.com/Plus-Size-Bikini-Bottoms-c-2296.html",
            "label": "Bikini Bottoms",
            "section": "Beachwear",
        },
        "curve-bikini-tops": {
            "url": "https://us.shein.com/Plus-Size-Bikini-Tops-c-2295.html",
            "label": "Bikini Tops",
            "section": "Beachwear",
        },
        "curve-kimonos": {
            "url": "https://us.shein.com/Plus-Size-Kimonos-c-2050.html",
            "label": "Kimonos",
            "section": "Beachwear",
        },
        "curve-dresses-4239": {
            "url": "https://us.shein.com/Women-Plus-Size-Sports-Dresses-c-4239.html",
            "label": "Dresses",
            "section": "Activewear",
        },
        "curve-tops-4240": {
            "url": "https://us.shein.com/Women-Plus-Size-Sports-Tops-c-4240.html",
            "label": "Tops",
            "section": "Activewear",
        },
        "curve-bottoms-4243": {
            "url": "https://us.shein.com/Women-Plus-Size-Sports-Bottoms-c-4243.html",
            "label": "Bottoms",
            "section": "Activewear",
        },
        "curve-sets": {
            "url": "https://us.shein.com/Women-Plus-Size-Sports-Sets-c-2494.html",
            "label": "Sets",
            "section": "Activewear",
        },
        "curve-bodysuits-jumpsuits": {
            "url": "https://us.shein.com/Women-Plus-Size-Sports-Bodysuits-Jumpsuits-c-7138.html",
            "label": "Bodysuits & Jumpsuits",
            "section": "Activewear",
        },
        "curve-swimwear": {
            "url": "https://us.shein.com/Women-Plus-Size-Sports-Swimwear-c-10048.html",
            "label": "Swimwear",
            "section": "Activewear",
        },
        "curve-intimates-8868": {
            "url": "https://us.shein.com/Women-Plus-Sports-Intimates-c-8868.html",
            "label": "Intimates",
            "section": "Activewear",
        },
        "curve-shapewear": {
            "url": "https://us.shein.com/Women-Plus-Sports-Shapewear-c-14461.html",
            "label": "Shapewear",
            "section": "Activewear",
        },
        "curve-bras-bralettes": {
            "url": "https://us.shein.com/Plus-Size-Bras-Bralettes-c-2354.html",
            "label": "Bras & Bralettes",
            "section": "Intimates",
        },
        "curve-sexy-lingerie": {
            "url": "https://us.shein.com/Plus-Size-Sexy-Lingerie-c-1944.html",
            "label": "Sexy Lingerie",
            "section": "Intimates",
        },
        "curve-panties": {
            "url": "https://us.shein.com/Plus-Size-Panties-c-2355.html",
            "label": "Panties",
            "section": "Intimates",
        },
        "curve-corsets-shapewear": {
            "url": "https://us.shein.com/Plus-Size-Corsets-Shapewear-c-3856.html",
            "label": "Corsets & Shapewear",
            "section": "Intimates",
        },
        "curve-bra-panty-sets": {
            "url": "https://us.shein.com/Plus-Size-Bra-Panty-Sets-c-2353.html",
            "label": "Bra & Panty Sets",
            "section": "Intimates",
        },
        "curve-lingerie-accessories": {
            "url": "https://us.shein.com/Plus-Size-Lingerie-Accessories-c-2356.html",
            "label": "Lingerie Accessories",
            "section": "Intimates",
        },
        "curve-sexy-costumes": {
            "url": "https://us.shein.com/Plus-Size-Sexy-Costumes-c-2839.html",
            "label": "Sexy Costumes",
            "section": "Intimates",
        },
        "curve-pajama-sets": {
            "url": "https://us.shein.com/Plus-Size-Pajama-Sets-c-1938.html",
            "label": "Pajama Sets",
            "section": "Sleep & Lounge",
        },
        "curve-nightgowns-sleepshirts": {
            "url": "https://us.shein.com/Plus-Size-Nightgowns-Sleepshirts-c-2348.html",
            "label": "Nightgowns & Sleepshirts",
            "section": "Sleep & Lounge",
        },
        "curve-robes-robe-sets": {
            "url": "https://us.shein.com/Plus-Size-Robes-Robe-Sets-c-2349.html",
            "label": "Robes & Robe Sets",
            "section": "Sleep & Lounge",
        },
        "curve-sleep-jumpsuits": {
            "url": "https://us.shein.com/Plus-Size-Sleep-Jumpsuits-c-2350.html",
            "label": "Sleep Jumpsuits",
            "section": "Sleep & Lounge",
        },
        "curve-sleep-bottoms": {
            "url": "https://us.shein.com/Plus-Size-Sleep-Bottoms-c-2351.html",
            "label": "Sleep Bottoms",
            "section": "Sleep & Lounge",
        },
        "curve-bridesmaid-dresses": {
            "url": "https://us.shein.com/Women-Plus-Bridesmaid-Dresses-c-3099.html",
            "label": "Bridesmaid Dresses",
            "section": "Wedding",
        },
        "curve-mother-of-the-bride-dresses": {
            "url": "https://us.shein.com/Plus-Size-Mother-of-the-Bride-Dresses-c-9132.html",
            "label": "Mother of the Bride Dresses",
            "section": "Wedding",
        },
        "curve-wedding-dresses": {
            "url": "https://us.shein.com/Women-Plus-Wedding-Dresses-c-3098.html",
            "label": "Wedding Dresses",
            "section": "Wedding",
        },
        "curve-bridal-shower-dresses": {
            "url": "https://us.shein.com/Women-Plus-Bridal-Shower-Dresses-c-9501.html",
            "label": "Bridal Shower Dresses",
            "section": "Wedding",
        },
        "curve-wedding-other-wear": {
            "url": "https://us.shein.com/Women-Plus-Wedding-Other-Wear-c-12043.html",
            "label": "Wedding Other Wear",
            "section": "Wedding",
        },
        "curve-formal-evening-dresses": {
            "url": "https://us.shein.com/Women-Plus-Formal-Evening-Dresses-c-9549.html",
            "label": "Formal & Evening Dresses",
            "section": "Party Wear",
        },
        "curve-cocktail-dresses": {
            "url": "https://us.shein.com/Women-Plus-Cocktail-Dresses-c-8036.html",
            "label": "Cocktail Dresses",
            "section": "Party Wear",
        },
        "curve-prom-dresses": {
            "url": "https://us.shein.com/Women-Plus-Prom-Dresses-c-5364.html",
            "label": "Prom Dresses",
            "section": "Party Wear",
        },
        "curve-party-other-wear": {
            "url": "https://us.shein.com/Women-Plus-Party-Jumpsuits-c-5365.html",
            "label": "Party Other Wear",
            "section": "Party Wear",
        },
        "curve-arabian-wear": {
            "url": "https://us.shein.com/Plus-Size-Arabian-Wear-c-2987.html",
            "label": "Arabian Wear",
            "section": "World Apparel",
        },
        "curve-arabian-dresses": {
            "url": "https://us.shein.com/Plus-Size-Arabian-Dresses-c-2987.html",
            "label": "Arabian Dresses",
            "section": "World Apparel",
        },
        "curve-kaftan-jalabiya": {
            "url": "https://us.shein.com/Plus-Size-Kaftan-Jalabiya-c-13401.html",
            "label": "Kaftan & Jalabiya",
            "section": "World Apparel",
        },
        "curve-romwe": {
            "url": "https://us.shein.com/category/ROMWE-CURVE-PLUS-sc-00893687.html",
            "label": "ROMWE",
            "section": "Brands We Love",
        },
        "curve-dazy": {
            "url": "https://us.shein.com/trends/Dazy-Plus-sc-006251666.html",
            "label": "DAZY",
            "section": "Brands We Love",
        },
        "curve-emery-rose": {
            "url": "https://us.shein.com/Brands-recommend/EMERY-ROSE-CURVE-sc-024161666.html",
            "label": "EMERY ROSE",
            "section": "Brands We Love",
        },
        "curve-forever-21-x-shein-x": {
            "url": "https://us.shein.com/category/FOREVER-21-Plus-Clothing-sc-008488816.html",
            "label": "Forever 21 x SHEIN X",
            "section": "Brands We Love",
        },
        "curve-view-all-66698741": {
            "url": "https://us.shein.com/Series/SHEIN-Collection-Curve-New-Hot-sc-66698741.html",
            "label": "View All",
            "section": "SHEIN Collection",
        },
    },
    "men": {
        "men": {
            "url": "https://us.shein.com/RecommendSelection/Men-Clothing-sc-017172963.html",
            "label": "Men Clothing",
            "section": "Top category",
        },
        "men-view-all": {
            "url": "https://us.shein.com/Men-Apparel-c-2026.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "men-new-in": {
            "url": "https://us.shein.com/recommend/New-In-Men-clothing-sc-10050009164.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "men-top-rated": {
            "url": "https://us.shein.com/recommend/men-top-rated-sc-10050009166.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "men-tops": {
            "url": "https://us.shein.com/Men-Tops-c-1970.html",
            "label": "Tops",
            "section": "Shop by Category",
        },
        "men-bottoms": {
            "url": "https://us.shein.com/Men-Bottoms-c-2045.html",
            "label": "Bottoms",
            "section": "Shop by Category",
        },
        "men-denim": {
            "url": "https://us.shein.com/Men-Denim-c-1973.html",
            "label": "Denim",
            "section": "Shop by Category",
        },
        "men-co-ords": {
            "url": "https://us.shein.com/Men-Co-ords-c-2044.html",
            "label": "Co-ords",
            "section": "Shop by Category",
        },
        "men-suits-separates": {
            "url": "https://us.shein.com/Men-Suits-Separates-c-3614.html",
            "label": "Suits & Separates",
            "section": "Shop by Category",
        },
        "men-hoodies-sweatshirts": {
            "url": "https://us.shein.com/Men-Hoodies-Sweatshirts-c-2047.html",
            "label": "Hoodies & Sweatshirts",
            "section": "Shop by Category",
        },
        "men-plus-size": {
            "url": "https://us.shein.com/Men-Plus-Size-Clothing-c-6279.html",
            "label": "Plus Size",
            "section": "Shop by Category",
        },
        "men-outerwear": {
            "url": "https://us.shein.com/Men-Outerwear-c-1971.html",
            "label": "Outerwear",
            "section": "Shop by Category",
        },
        "men-knitwear": {
            "url": "https://us.shein.com/Men-Knitwear-c-3871.html",
            "label": "Knitwear",
            "section": "Shop by Category",
        },
        "men-swimwear": {
            "url": "https://us.shein.com/Men-Swimwear-c-3792.html",
            "label": "Swimwear",
            "section": "Shop by Category",
        },
        "men-underwear-sleepwear": {
            "url": "https://us.shein.com/recommend/Underwear-Sleepwear-sc-10050009160.html",
            "label": "Underwear & Sleepwear",
            "section": "Shop by Category",
        },
        "men-autumn-winter": {
            "url": "https://us.shein.com/recommend/category-men-winter-sc-1002108368.html",
            "label": "Autumn-Winter",
            "section": "Shop by Category",
        },
        "men-sweatpants": {
            "url": "https://us.shein.com/Men-Sweatpants-c-2988.html",
            "label": "Sweatpants",
            "section": "Shop by Category",
        },
        "men-shirts": {
            "url": "https://us.shein.com/Men-Shirts-c-1979.html",
            "label": "Shirts",
            "section": "Shop by Category",
        },
        "men-jeans": {
            "url": "https://us.shein.com/Men-Jeans-c-1989.html",
            "label": "Jeans",
            "section": "Shop by Category",
        },
        "men-men-top-picks": {
            "url": "https://us.shein.com/Men-Top-Picks-sc-10050114901.html",
            "label": "Men Top Picks",
            "section": "Shop by Category",
        },
        "men-t-shirts": {
            "url": "https://us.shein.com/Men-T-Shirts-c-1980.html",
            "label": "T-shirts",
            "section": "Tops",
        },
        "men-polo-shirts": {
            "url": "https://us.shein.com/Men-Polo-Shirts-c-1981.html",
            "label": "Polo Shirts",
            "section": "Tops",
        },
        "men-tank-tops": {
            "url": "https://us.shein.com/recommend/category-tank-shirts-sc-1002100403.html",
            "label": "Tank Tops",
            "section": "Tops",
        },
        "men-graphics": {
            "url": "https://us.shein.com/recommend/category-mentop-graphic-sc-1002108512.html",
            "label": "Graphics",
            "section": "Tops",
        },
        "men-pants": {
            "url": "https://us.shein.com/Men-Pants-c-1978.html",
            "label": "Pants",
            "section": "Bottoms",
        },
        "men-shorts": {
            "url": "https://us.shein.com/Men-Shorts-c-1976.html",
            "label": "Shorts",
            "section": "Bottoms",
        },
        "men-joggers": {
            "url": "https://us.shein.com/recommend/category-men-joggers-sc-1002108532.html",
            "label": "Joggers",
            "section": "Bottoms",
        },
        "men-cargo-pants": {
            "url": "https://us.shein.com/recommend/category-men-cargo-sc-1002108550.html",
            "label": "Cargo Pants",
            "section": "Bottoms",
        },
        "men-denim-jackets": {
            "url": "https://us.shein.com/Men-Denim-Jackets-c-1986.html",
            "label": "Denim Jackets",
            "section": "Denim",
        },
        "men-denim-shirts": {
            "url": "https://us.shein.com/Men-Denim-Shirts-c-1987.html",
            "label": "Denim Shirts",
            "section": "Denim",
        },
        "men-denim-co-ords": {
            "url": "https://us.shein.com/Men-Denim-Co-ords-c-9036.html",
            "label": "Denim Co-ords",
            "section": "Denim",
        },
        "men-denim-jumpsuits-overalls": {
            "url": "https://us.shein.com/Men-Denim-Jumpsuits-and-Overalls-c-6280.html",
            "label": "Denim Jumpsuits & Overalls",
            "section": "Denim",
        },
        "men-t-shirt-co-ords": {
            "url": "https://us.shein.com/Men-T-Shirt-Co-ords-c-1975.html",
            "label": "T-Shirt Co-ords",
            "section": "Co-ords",
        },
        "men-shirts-9037": {
            "url": "https://us.shein.com/Men-Shirt-Co-ords-c-9037.html",
            "label": "Shirts",
            "section": "Co-ords",
        },
        "men-polo-co-ords": {
            "url": "https://us.shein.com/Men-Polo-Co-ords-c-9038.html",
            "label": "Polo Co-ords",
            "section": "Co-ords",
        },
        "men-outerwear-9042": {
            "url": "https://us.shein.com/Men-Outerwear-Co-ords-c-9042.html",
            "label": "Outerwear",
            "section": "Co-ords",
        },
        "men-hoodies-sweatshirts-1004602565": {
            "url": "https://us.shein.com/recommend/Hoodie-Sweatshirt-Co-ords-sc-1004602565.html",
            "label": "Hoodies & Sweatshirts",
            "section": "Co-ords",
        },
        "men-suits": {
            "url": "https://us.shein.com/Men-Suits-c-2484.html",
            "label": "Suits",
            "section": "Suits & Separates",
        },
        "men-suit-pants": {
            "url": "https://us.shein.com/Men-Suit-Pants-c-3179.html",
            "label": "Suit Pants",
            "section": "Suits & Separates",
        },
        "men-blazers": {
            "url": "https://us.shein.com/Men-Blazers-c-1982.html",
            "label": "Blazers",
            "section": "Suits & Separates",
        },
        "men-waistcoats": {
            "url": "https://us.shein.com/Men-Waistcoats-c-6276.html",
            "label": "Waistcoats",
            "section": "Suits & Separates",
        },
        "men-tuxedos": {
            "url": "https://us.shein.com/recommend/category-menzhengzhuang-Tuxedo-sc-1002108765.html",
            "label": "Tuxedos",
            "section": "Suits & Separates",
        },
        "men-hoodies": {
            "url": "https://us.shein.com/Men-Hoodies-c-8872.html",
            "label": "Hoodies",
            "section": "Hoodies & Sweatshirts",
        },
        "men-sweatshirts": {
            "url": "https://us.shein.com/Men-Sweatshirts-c-1974.html",
            "label": "Sweatshirts",
            "section": "Hoodies & Sweatshirts",
        },
        "men-zip-up-hoodies": {
            "url": "https://us.shein.com/Men-Zip-up-Hoodies-c-8869.html",
            "label": "Zip-up Hoodies",
            "section": "Hoodies & Sweatshirts",
        },
        "men-graphics-1002108633": {
            "url": "https://us.shein.com/recommend/category-menhoddies-graphic-sc-1002108633.html",
            "label": "Graphics",
            "section": "Hoodies & Sweatshirts",
        },
        "men-crewneck": {
            "url": "https://us.shein.com/recommend/category-menhoodies-Crewneck-sc-1002108652.html",
            "label": "Crewneck",
            "section": "Hoodies & Sweatshirts",
        },
        "men-tops-6304": {
            "url": "https://us.shein.com/Men-Plus-Size-Tops-c-6304.html",
            "label": "Tops",
            "section": "Plus Size Clothing",
        },
        "men-bottoms-6322": {
            "url": "https://us.shein.com/Men-Plus-Size-Bottoms-c-6322.html",
            "label": "Bottoms",
            "section": "Plus Size Clothing",
        },
        "men-co-ords-6316": {
            "url": "https://us.shein.com/Men-Plus-Size-Co-ords-c-6316.html",
            "label": "Co-ords",
            "section": "Plus Size Clothing",
        },
        "men-denim-6287": {
            "url": "https://us.shein.com/Men-Plus-Size-Denim-c-6287.html",
            "label": "Denim",
            "section": "Plus Size Clothing",
        },
        "men-hoodies-sweatshirts-6302": {
            "url": "https://us.shein.com/Men-Plus-Size-Hoodies-Sweatshirts-c-6302.html",
            "label": "Hoodies & Sweatshirts",
            "section": "Plus Size Clothing",
        },
        "men-outerwear-6293": {
            "url": "https://us.shein.com/Men-Plus-Size-Outerwear-c-6293.html",
            "label": "Outerwear",
            "section": "Plus Size Clothing",
        },
        "men-suits-separates-6315": {
            "url": "https://us.shein.com/Men-Plus-Size-Suits-Separates-c-6315.html",
            "label": "Suits & Separates",
            "section": "Plus Size Clothing",
        },
        "men-knitwear-6305": {
            "url": "https://us.shein.com/Men-Plus-Size-Knitwear-c-6305.html",
            "label": "Knitwear",
            "section": "Plus Size Clothing",
        },
        "men-jackets-coats": {
            "url": "https://us.shein.com/Men-Jackets-Coats-c-1983.html",
            "label": "Jackets & Coats",
            "section": "Outerwear",
        },
        "men-winter-coats": {
            "url": "https://us.shein.com/Men-Winter-Coats-c-3138.html",
            "label": "Winter Coats",
            "section": "Outerwear",
        },
        "men-overcoats": {
            "url": "https://us.shein.com/Men-Overcoats-c-3137.html",
            "label": "Overcoats",
            "section": "Outerwear",
        },
        "men-down-coats": {
            "url": "https://us.shein.com/Men-Down-Coats-c-3139.html",
            "label": "Down Coats",
            "section": "Outerwear",
        },
        "men-trench-coats": {
            "url": "https://us.shein.com/Men-Trench-Coats-c-3136.html",
            "label": "Trench Coats",
            "section": "Outerwear",
        },
        "men-vests": {
            "url": "https://us.shein.com/Men-Vests-c-6277.html",
            "label": "Vests",
            "section": "Outerwear",
        },
        "men-shackets": {
            "url": "https://us.shein.com/Men-Shackets-c-6278.html",
            "label": "Shackets",
            "section": "Outerwear",
        },
        "men-faux-fur-coats": {
            "url": "https://us.shein.com/Men-Faux-Fur-Coats-c-3140.html",
            "label": "Faux Fur Coats",
            "section": "Outerwear",
        },
        "men-pullovers": {
            "url": "https://us.shein.com/Men-Sweaters-c-1977.html",
            "label": "Pullovers",
            "section": "Sweaters",
        },
        "men-knit-tops": {
            "url": "https://us.shein.com/Men-Knit-Tops-c-3872.html",
            "label": "Knit Tops",
            "section": "Sweaters",
        },
        "men-sweater-vests": {
            "url": "https://us.shein.com/Men-Sweater-Vests-c-3873.html",
            "label": "Sweater Vests",
            "section": "Sweaters",
        },
        "men-cardigans": {
            "url": "https://us.shein.com/Men-Cardigans-c-3874.html",
            "label": "Cardigans",
            "section": "Sweaters",
        },
        "men-sweater-co-ords": {
            "url": "https://us.shein.com/Men-Sweater-Co-ords-c-3875.html",
            "label": "Sweater Co-ords",
            "section": "Sweaters",
        },
        "men-beach-shorts": {
            "url": "https://us.shein.com/Men-Beach-Shorts-c-2025.html",
            "label": "Beach Shorts",
            "section": "Swimwear",
        },
        "men-swim-shorts": {
            "url": "https://us.shein.com/Men-Swim-Shorts-c-3797.html",
            "label": "Swim Shorts",
            "section": "Swimwear",
        },
        "men-beach-sets": {
            "url": "https://us.shein.com/Men-Beach-Sets-c-8846.html",
            "label": "Beach Sets",
            "section": "Swimwear",
        },
        "men-swim-rashguards": {
            "url": "https://us.shein.com/category/category-Men-Swim-Rashguards-sc-0082258832.html",
            "label": "Swim Rashguards",
            "section": "Swimwear",
        },
        "men-underwear": {
            "url": "https://us.shein.com/recommend/men-underwear-sc-10050009240.html",
            "label": "Underwear",
            "section": "Underwear & Sleepwear",
        },
        "men-loungewear": {
            "url": "https://us.shein.com/recommend/men-loungewear-sc-10050009241.html",
            "label": "Loungewear",
            "section": "Underwear & Sleepwear",
        },
        "men-shapewear": {
            "url": "https://us.shein.com/recommend/men-Shapewear-sc-10050009243.html",
            "label": "Shapewear",
            "section": "Underwear & Sleepwear",
        },
        "men-socks": {
            "url": "https://us.shein.com/recommend/chongdie-men-socks-sc-1002854489.html",
            "label": "Socks",
            "section": "Underwear & Sleepwear",
        },
        "men-jumpsuits-overalls": {
            "url": "https://us.shein.com/Men-Jumpsuits-Overalls-c-6275.html",
            "label": "Jumpsuits & Overalls",
            "section": "More Categories",
        },
        "men-uniforms-special-clothing": {
            "url": "https://us.shein.com/Men-Uniforms-Special-Clothing-c-12726.html",
            "label": "Uniforms & Special Clothing",
            "section": "More Categories",
        },
        "men-traditional-cultural-wear": {
            "url": "https://us.shein.com/Men-Traditional-Cultural-Wear-c-12615.html",
            "label": "Traditional & Cultural Wear",
            "section": "More Categories",
        },
        "men-customized-clothing": {
            "url": "https://us.shein.com/recommend/category-men-customized-sc-1002102022.html",
            "label": "Customized Clothing",
            "section": "More Categories",
        },
    },
    "shoes": {
        "shoes": {
            "url": "https://us.shein.com/RecommendSelection/Shoes-sc-017172966.html",
            "label": "Shoes",
            "section": "Top category",
        },
        "shoes-view-all": {
            "url": "https://us.shein.com/Shoes-c-3636.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "shoes-top-rated": {
            "url": "https://us.shein.com/recommend/Women-Shoes-Top-Rated-sc-100166528.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "shoes-winter-chic": {
            "url": "https://us.shein.com/recommend/Winter-Steps-sc-10050109954.html",
            "label": "Winter Chic",
            "section": "Shop by Category",
        },
        "shoes-sale": {
            "url": "https://us.shein.com/promotion/inseansonBFSALE-sc-0251984747.html",
            "label": "Sale",
            "section": "Shop by Category",
        },
        "shoes-women-fashion-boots": {
            "url": "https://us.shein.com/Women-Fashion-Boots-c-3180.html",
            "label": "Women Fashion Boots",
            "section": "Shop by Category",
        },
        "shoes-women-sneakers": {
            "url": "https://us.shein.com/Women-Sneakers-c-3191.html",
            "label": "Women Sneakers",
            "section": "Shop by Category",
        },
        "shoes-women-pumps": {
            "url": "https://us.shein.com/Women-Pumps-c-1750.html",
            "label": "Women Pumps",
            "section": "Shop by Category",
        },
        "shoes-women-sandals": {
            "url": "https://us.shein.com/Women-Flat-Sandals-c-3184.html",
            "label": "Women Sandals",
            "section": "Shop by Category",
        },
        "shoes-women-flats": {
            "url": "https://us.shein.com/Women-Flats-c-1881.html",
            "label": "Women Flats",
            "section": "Shop by Category",
        },
        "shoes-women-slippers": {
            "url": "https://us.shein.com/Women-Slippers-c-3187.html",
            "label": "Women Slippers",
            "section": "Shop by Category",
        },
        "shoes-women-wedges-flatform": {
            "url": "https://us.shein.com/Women-Wedges-Flatform-c-1749.html",
            "label": "Women Wedges & Flatform",
            "section": "Shop by Category",
        },
        "shoes-women-outdoor-shoes": {
            "url": "https://us.shein.com/Women-Outdoor-Shoes-c-6875.html",
            "label": "Women Outdoor Shoes",
            "section": "Shop by Category",
        },
        "shoes-men-sneakers": {
            "url": "https://us.shein.com/Men-Sneakers-c-2093.html",
            "label": "Men Sneakers",
            "section": "Shop by Category",
        },
        "shoes-men-skateboarding-shoes": {
            "url": "https://us.shein.com/Men-Skateboarding-Shoes-c-12449.html",
            "label": "Men Skateboarding Shoes",
            "section": "Shop by Category",
        },
        "shoes-men-boots": {
            "url": "https://us.shein.com/Men-Boots-c-12456.html",
            "label": "Men Boots",
            "section": "Shop by Category",
        },
        "shoes-dress-shoes": {
            "url": "https://us.shein.com/Dress-Shoes-c-2091.html",
            "label": "Dress Shoes",
            "section": "Shop by Category",
        },
        "shoes-men-slippers": {
            "url": "https://us.shein.com/Men-Slippers-c-2330.html",
            "label": "Men Slippers",
            "section": "Shop by Category",
        },
        "shoes-women-athletic-shoes": {
            "url": "https://us.shein.com/Women-Athletic-Shoes-c-6882.html",
            "label": "Women Athletic Shoes",
            "section": "Shop by Category",
        },
        "shoes-men-loafers": {
            "url": "https://us.shein.com/Men-Loafers-c-2092.html",
            "label": "Men Loafers",
            "section": "Shop by Category",
        },
        "shoes-wide-fit-shoes": {
            "url": "https://us.shein.com/Wide-Fit-Shoes-c-5928.html",
            "label": "Wide Fit Shoes",
            "section": "Shop by Category",
        },
        "shoes-shoe-accessories": {
            "url": "https://us.shein.com/Shoe-Accessories-c-4803.html",
            "label": "Shoe Accessories",
            "section": "Shop by Category",
        },
        "shoes-customized-shoes": {
            "url": "https://us.shein.com/recommend/customized-shoes-sc-10050007919.html",
            "label": "Customized Shoes",
            "section": "Shop by Category",
        },
        "shoes-quickship": {
            "url": "https://us.shein.com/recommend/shoes-btg-sc-1005030388.html",
            "label": "QuickShip",
            "section": "Shop by Category",
        },
        "shoes-backtoschool-deals": {
            "url": "https://us.shein.com/backtoschool-deals-sc-10050099939.html",
            "label": "backtoschool deals",
            "section": "Shop by Category",
        },
        "shoes-view-all-008370473": {
            "url": "https://us.shein.com/category/Boots-sc-008370473.html",
            "label": "View All",
            "section": "Boots",
        },
        "shoes-women-ankle-boots-booties": {
            "url": "https://us.shein.com/Women-Ankle-Boots-Booties-c-1748.html",
            "label": "Women Ankle Boots & Booties",
            "section": "Boots",
        },
        "shoes-women-mid-calf-boots": {
            "url": "https://us.shein.com/Women-Mid-Calf-Boots-c-8506.html",
            "label": "Women Mid-calf Boots",
            "section": "Boots",
        },
        "shoes-women-over-the-knee-boots": {
            "url": "https://us.shein.com/Women-Over-the-Knee-Boots-c-8508.html",
            "label": "Women Over-the-knee Boots",
            "section": "Boots",
        },
        "shoes-women-knee-high-boots": {
            "url": "https://us.shein.com/Women-Knee-High-Boots-c-8507.html",
            "label": "Women Knee-high Boots",
            "section": "Boots",
        },
        "shoes-women-equestrian-boots-western-boots": {
            "url": "https://us.shein.com/Women-Western-Boots-c-6881.html",
            "label": "Women Equestrian Boots & Western Boots",
            "section": "Boots",
        },
        "shoes-snow-boots": {
            "url": "https://us.shein.com/Women-Snow-Boots-c-3182.html",
            "label": "Snow Boots",
            "section": "Boots",
        },
        "shoes-view-all-008370468": {
            "url": "https://us.shein.com/category/Sneakers-sc-008370468.html",
            "label": "View All",
            "section": "Sneakers",
        },
        "shoes-women-casual-shoes": {
            "url": "https://us.shein.com/Women-Casual-Shoes-c-1913.html",
            "label": "Women Casual Shoes",
            "section": "Sneakers",
        },
        "shoes-women-sports-shoes": {
            "url": "https://us.shein.com/Women-Sports-Shoes-c-3192.html",
            "label": "Women Sports Shoes",
            "section": "Sneakers",
        },
        "shoes-women-wedge-sneakers": {
            "url": "https://us.shein.com/Women-Wedge-Sneakers-c-3193.html",
            "label": "Women Wedge Sneakers",
            "section": "Sneakers",
        },
        "shoes-men-canvas-shoes": {
            "url": "https://us.shein.com/Men-Canvas-Shoes-c-12451.html",
            "label": "Men Canvas Shoes",
            "section": "Sneakers",
        },
        "shoes-women-canvas-shoes": {
            "url": "https://us.shein.com/Women-Canvas-Shoes-c-12446.html",
            "label": "Women Canvas Shoes",
            "section": "Sneakers",
        },
        "shoes-customized-women-sneakers": {
            "url": "https://us.shein.com/Customized-Women-Sneakers-c-12525.html",
            "label": "Customized Women Sneakers",
            "section": "Sneakers",
        },
        "shoes-customized-men-sneakers": {
            "url": "https://us.shein.com/Customized-Men-Sneakers-c-12534.html",
            "label": "Customized Men Sneakers",
            "section": "Sneakers",
        },
        "shoes-view-all-008370460": {
            "url": "https://us.shein.com/category/Sandals-sc-008370460.html",
            "label": "View All",
            "section": "Sandals",
        },
        "shoes-women-heeled-sandals": {
            "url": "https://us.shein.com/Women-Heeled-Sandals-c-1751.html",
            "label": "Women Heeled Sandals",
            "section": "Sandals",
        },
        "shoes-women-platforms-wedge-sandals": {
            "url": "https://us.shein.com/Women-Platforms-Wedge-Sandals-c-3186.html",
            "label": "Women Platforms & Wedge Sandals",
            "section": "Sandals",
        },
        "shoes-women-sports-sandals": {
            "url": "https://us.shein.com/Women-Sports-Sandals-c-3185.html",
            "label": "Women Sports Sandals",
            "section": "Sandals",
        },
        "shoes-men-sandals": {
            "url": "https://us.shein.com/Men-Sandals-c-2095.html",
            "label": "Men Sandals",
            "section": "Sandals",
        },
        "shoes-view-all-008370478": {
            "url": "https://us.shein.com/category/Slippers-sc-008370478.html",
            "label": "View All",
            "section": "Slippers",
        },
        "shoes-women-slides": {
            "url": "https://us.shein.com/Women-Slides-c-2866.html",
            "label": "Women Slides",
            "section": "Slippers",
        },
        "shoes-women-home-slippers": {
            "url": "https://us.shein.com/Women-Home-Slippers-c-1929.html",
            "label": "Women Home Slippers",
            "section": "Slippers",
        },
        "shoes-women-flip-flops": {
            "url": "https://us.shein.com/Women-Flip-Flops-c-3188.html",
            "label": "Women Flip-flops",
            "section": "Slippers",
        },
        "shoes-men-clogs": {
            "url": "https://us.shein.com/Men-Clogs-c-3925.html",
            "label": "Men Clogs",
            "section": "Slippers",
        },
        "shoes-women-clogs": {
            "url": "https://us.shein.com/Women-Clogs-c-3189.html",
            "label": "Women Clogs",
            "section": "Slippers",
        },
        "shoes-customized-men-slippers": {
            "url": "https://us.shein.com/Customized-Men-Slippers-c-12535.html",
            "label": "Customized Men Slippers",
            "section": "Slippers",
        },
        "shoes-customized-women-slippers": {
            "url": "https://us.shein.com/Customized-Women-Slippers-c-12536.html",
            "label": "Customized Women Slippers",
            "section": "Slippers",
        },
        "shoes-view-all-008370475": {
            "url": "https://us.shein.com/category/Flats-sc-008370475.html",
            "label": "View All",
            "section": "Flats",
        },
        "shoes-women-oxfords-shoes": {
            "url": "https://us.shein.com/Women-Oxfords-Shoes-c-12448.html",
            "label": "Women Oxfords Shoes",
            "section": "Flats",
        },
        "shoes-women-loafers-shoes": {
            "url": "https://us.shein.com/Women-Loafers-Shoes-c-12452.html",
            "label": "Women Loafers Shoes",
            "section": "Flats",
        },
        "shoes-view-all-0011816101": {
            "url": "https://us.shein.com/style/sportandworkallin-sc-0011816101.html",
            "label": "View All",
            "section": "Sport & Work",
        },
        "shoes-men-athletic-shoes": {
            "url": "https://us.shein.com/Men-Athletic-Shoes-c-6965.html",
            "label": "Men Athletic Shoes",
            "section": "Sport & Work",
        },
        "shoes-men-outdoor-shoes": {
            "url": "https://us.shein.com/Men-Outdoor-Shoes-c-6983.html",
            "label": "Men Outdoor Shoes",
            "section": "Sport & Work",
        },
        "shoes-women-work-safety-shoes": {
            "url": "https://us.shein.com/Women-Work-Safety-Shoes-c-12457.html",
            "label": "Women Work & Safety Shoes",
            "section": "Sport & Work",
        },
        "shoes-men-work-safety-shoes": {
            "url": "https://us.shein.com/Men-Work-Safety-Shoes-c-12455.html",
            "label": "Men Work & Safety Shoes",
            "section": "Sport & Work",
        },
        "shoes-women-skateboarding-shoes": {
            "url": "https://us.shein.com/Women-Skateboarding-Shoes-c-12453.html",
            "label": "Women Skateboarding Shoes",
            "section": "Sport & Work",
        },
        "shoes-shoe-diy-decorations": {
            "url": "https://us.shein.com/Shoe-DIY-Decorations-c-11515.html",
            "label": "Shoe DIY Decorations",
            "section": "Shoe Accessories",
        },
        "shoes-shoe-care-tools": {
            "url": "https://us.shein.com/Shoe-Care-Tools-c-4814.html",
            "label": "Shoe Care & Tools",
            "section": "Shoe Accessories",
        },
        "shoes-customized-shoe-accessories": {
            "url": "https://us.shein.com/Customized-Shoe-Accessories-c-13517.html",
            "label": "Customized Shoe Accessories",
            "section": "Shoe Accessories",
        },
        "shoes-cuccoo": {
            "url": "https://us.shein.com/Brands/Cuccoo-sc-01437340.html",
            "label": "CUCCOO",
            "section": "Brands",
        },
        "shoes-styleloop": {
            "url": "https://us.shein.com/Brands/Styleloop-brand-new-in-sc-014198189.html",
            "label": "Styleloop",
            "section": "Brands",
        },
        "shoes-dola-lovely": {
            "url": "https://us.shein.com/Brands/Dola-Lovely-sc-014276196.html",
            "label": "Dola Lovely",
            "section": "Brands",
        },
        "shoes-sugerpunk": {
            "url": "https://us.shein.com/Brands/SugerPunk-sc-014276973.html",
            "label": "Sugerpunk",
            "section": "Brands",
        },
        "shoes-ressula": {
            "url": "https://us.shein.com/recommend/Ressula-sc-10050003065.html",
            "label": "Ressula",
            "section": "Brands",
        },
        "shoes-shein-haute": {
            "url": "https://us.shein.com/category/SHEIN-Haute-Shoes-sc-008543715.html",
            "label": "SHEIN HAUTE",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-szl": {
            "url": "https://us.shein.com/style/CUCCOO-SZL-sc-0011678790.html",
            "label": "CUCCOO SZL",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-bizchic": {
            "url": "https://us.shein.com/style/CUCCOO-BIZCHIC-sc-0011678872.html",
            "label": "CUCCOO BIZCHIC",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-chicest": {
            "url": "https://us.shein.com/style/CUCCOO-CHICEST-sc-0011678815.html",
            "label": "CUCCOO CHICEST",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-dollmod": {
            "url": "https://us.shein.com/style/CUCCOO-DOLLMOD-sc-0011678877.html",
            "label": "CUCCOO DOLLMOD",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-tilawa": {
            "url": "https://us.shein.com/style/CUCCOO-TILAWA-sc-0011678802.html",
            "label": "CUCCOO TILAWA",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-easi": {
            "url": "https://us.shein.com/style/CUCCOO-EASI-sc-0011678863.html",
            "label": "CUCCOO EASI",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-basics": {
            "url": "https://us.shein.com/style/CUCCOO-BASICS-sc-0011967768.html",
            "label": "CUCCOO BASICS",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-hitchd": {
            "url": "https://us.shein.com/style/CUCCOO-HITCHD-sc-0011967788.html",
            "label": "CUCCOO HITCHD",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-curves": {
            "url": "https://us.shein.com/style/CUCCOO-Curves-sc-0011967794.html",
            "label": "CUCCOO Curves",
            "section": "SHEIN Collection",
        },
        "shoes-cuccoo-quty": {
            "url": "https://us.shein.com/style/CUCCOO-QUTY-sc-0011967797.html",
            "label": "CUCCOO QUTY",
            "section": "SHEIN Collection",
        },
    },
    "underwear-sleepwear": {
        "underwear-sleepwear": {
            "url": "https://us.shein.com/RecommendSelection/Underwear-Sleepwear-sc-017172965.html",
            "label": "Underwear & Sleepwear",
            "section": "Top category",
        },
        "underwear-sleepwear-view-all": {
            "url": "https://us.shein.com/Underwear-Sleepwear-c-2038.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-top-rated": {
            "url": "https://us.shein.com/recommend/top-rated-underwear-sleepwear-sc-10050013297.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-new-in": {
            "url": "https://us.shein.com/recommend/new-in-sc-10050111337.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-sleep-lounge": {
            "url": "https://us.shein.com/Women-Sleep-Lounge-c-3626.html",
            "label": "Women Sleep & Lounge",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-bras": {
            "url": "https://us.shein.com/Women-Bras-c-3625.html",
            "label": "Women Bras",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-panties": {
            "url": "https://us.shein.com/Women-Panties-c-4295.html",
            "label": "Women Panties",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-sexy-lingerie-costumes": {
            "url": "https://us.shein.com/Women-Sexy-Lingerie-Costumes-c-4292.html",
            "label": "Women Sexy Lingerie & Costumes",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-shapewear": {
            "url": "https://us.shein.com/Women-Shapewear-c-3812.html",
            "label": "Women Shapewear",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-men": {
            "url": "https://us.shein.com/style/MEN-UNDERWEAR-SLEEPWEAR-sc-001233323.html",
            "label": "Men",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-plus-sleep-and-lounge": {
            "url": "https://us.shein.com/Women-Plus-Sleep-and-Lounge-c-2346.html",
            "label": "Women Plus Sleep and Lounge",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-women-plus-intimates": {
            "url": "https://us.shein.com/Women-Plus-Intimates-c-2347.html",
            "label": "Women Plus Intimates",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-autumn-winter": {
            "url": "https://us.shein.com/recommend/Underwear-Sleepwear-fw-sc-10050013293.html",
            "label": "Autumn-Winter",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-accessories": {
            "url": "https://us.shein.com/recommend/Accessories-sc-10050000551.html",
            "label": "Accessories",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-socks": {
            "url": "https://us.shein.com/recommend/Socks-sc-10050000550.html",
            "label": "Socks",
            "section": "Shop by Category",
        },
        "underwear-sleepwear-sleepwear": {
            "url": "https://us.shein.com/Women-Sleepwear-c-2332.html",
            "label": "Sleepwear",
            "section": "Women Sleep & Lounge",
        },
        "underwear-sleepwear-pajama-sets": {
            "url": "https://us.shein.com/recommend/Pajama-Sets-sc-10050111371.html",
            "label": "Pajama Sets",
            "section": "Women Sleep & Lounge",
        },
        "underwear-sleepwear-night-dresses": {
            "url": "https://us.shein.com/recommend/Night-Dresses-sc-10050111377.html",
            "label": "Night Dresses",
            "section": "Women Sleep & Lounge",
        },
        "underwear-sleepwear-robes": {
            "url": "https://us.shein.com/recommend/Robes-sc-10050111382.html",
            "label": "Robes",
            "section": "Women Sleep & Lounge",
        },
        "underwear-sleepwear-jumpsuits-bottoms": {
            "url": "https://us.shein.com/recommend/Jumpsuits-bottoms-sc-10050111386.html",
            "label": "Jumpsuits & Bottoms",
            "section": "Women Sleep & Lounge",
        },
        "underwear-sleepwear-bras-bralettes": {
            "url": "https://us.shein.com/Women-Bras-Bralettes-c-2203.html",
            "label": "Bras & Bralettes",
            "section": "Bras",
        },
        "underwear-sleepwear-bra-panty-sets": {
            "url": "https://us.shein.com/Women-Bra-Panty-Sets-c-2270.html",
            "label": "Bra & Panty Sets",
            "section": "Bras",
        },
        "underwear-sleepwear-push-up": {
            "url": "https://us.shein.com/recommend/Push-up-bra-sc-10050060507.html",
            "label": "Push Up",
            "section": "Bras",
        },
        "underwear-sleepwear-strapless-bandeau": {
            "url": "https://us.shein.com/recommend/strapless-bra-sc-10050043972.html",
            "label": "Strapless & Bandeau",
            "section": "Bras",
        },
        "underwear-sleepwear-wireless-seamless": {
            "url": "https://us.shein.com/recommend/Wireless-Seamless-sc-10050043975.html",
            "label": "Wireless & Seamless",
            "section": "Bras",
        },
        "underwear-sleepwear-unlined-bra": {
            "url": "https://us.shein.com/recommend/Unlined-Bra-sc-10050044002.html",
            "label": "Unlined Bra",
            "section": "Bras",
        },
        "underwear-sleepwear-backless-bra": {
            "url": "https://us.shein.com/recommend/Backless-Bra-sc-10050044004.html",
            "label": "Backless Bra",
            "section": "Bras",
        },
        "underwear-sleepwear-sports-bra": {
            "url": "https://us.shein.com/recommend/category-women-sports-bra-sc-1002207131.html",
            "label": "Sports Bra",
            "section": "Bras",
        },
        "underwear-sleepwear-briefs": {
            "url": "https://us.shein.com/Women-Briefs-c-2205.html",
            "label": "Briefs",
            "section": "Women Panties",
        },
        "underwear-sleepwear-thongs": {
            "url": "https://us.shein.com/Women-Thongs-c-4297.html",
            "label": "Thongs",
            "section": "Women Panties",
        },
        "underwear-sleepwear-boyshorts-safety-shorts": {
            "url": "https://us.shein.com/Women-Slip-Shorts-c-4298.html",
            "label": "Boyshorts & Safety Shorts",
            "section": "Women Panties",
        },
        "underwear-sleepwear-string-panties": {
            "url": "https://us.shein.com/Women-Boyshorts-c-4296.html",
            "label": "String Panties",
            "section": "Women Panties",
        },
        "underwear-sleepwear-sexy-sets": {
            "url": "https://us.shein.com/Women-Sexy-Lingerie-Sets-c-1862.html",
            "label": "Sexy Sets",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-sexy-lingerie-dresses": {
            "url": "https://us.shein.com/Women-Sexy-Lingerie-Dresses-c-8820.html",
            "label": "Sexy Lingerie Dresses",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-sexy-bodysuits": {
            "url": "https://us.shein.com/Women-Sexy-Bodysuits-c-8821.html",
            "label": "Sexy Bodysuits",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-crotchless-panties": {
            "url": "https://us.shein.com/Women-Crotchless-Panties-c-8819.html",
            "label": "Crotchless Panties",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-sexy-bustiers-corsets": {
            "url": "https://us.shein.com/Women-Sexy-Bustiers-Corsets-c-8822.html",
            "label": "Sexy Bustiers & Corsets",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-costumes": {
            "url": "https://us.shein.com/recommend/Women-Costumes-sc-1004661478.html",
            "label": "Costumes",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-sexy-accessories": {
            "url": "https://us.shein.com/Women-Sexy-and-Costume-Accessories-c-14056.html",
            "label": "Sexy Accessories",
            "section": "Women Sexy Lingerie & Costumes",
        },
        "underwear-sleepwear-view-all-3627": {
            "url": "https://us.shein.com/Women-Socks-Hosiery-c-3627.html",
            "label": "View All",
            "section": "Women Socks",
        },
        "underwear-sleepwear-tights": {
            "url": "https://us.shein.com/Women-Tights-c-3290.html",
            "label": "Tights",
            "section": "Women Socks",
        },
        "underwear-sleepwear-crew-socks": {
            "url": "https://us.shein.com/Women-Crew-Socks-c-1899.html",
            "label": "Crew Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-ankle-socks": {
            "url": "https://us.shein.com/Women-Ankle-Socks-c-4301.html",
            "label": "Ankle Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-leg-warmers": {
            "url": "https://us.shein.com/hotsale/category-Leg-Warmers-sc-0031742310.html",
            "label": "Leg Warmers",
            "section": "Women Socks",
        },
        "underwear-sleepwear-sports-socks": {
            "url": "https://us.shein.com/Women-Sports-Socks-c-4306.html",
            "label": "Sports Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-invisible-socks": {
            "url": "https://us.shein.com/Women-Invisible-Socks-c-4300.html",
            "label": "Invisible Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-over-the-calf-socks": {
            "url": "https://us.shein.com/Women-Over-the-Calf-Socks-c-4303.html",
            "label": "Over the Calf Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-over-the-knee-socks": {
            "url": "https://us.shein.com/Women-Over-the-Knee-Socks-c-4304.html",
            "label": "Over the Knee Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-fishnet-tights": {
            "url": "https://us.shein.com/Women-Fishnet-Tights-c-9635.html",
            "label": "Fishnet Tights",
            "section": "Women Socks",
        },
        "underwear-sleepwear-toe-socks": {
            "url": "https://us.shein.com/Women-Toe-Socks-c-4302.html",
            "label": "Toe Socks",
            "section": "Women Socks",
        },
        "underwear-sleepwear-shapewear-sets": {
            "url": "https://us.shein.com/Women-Shapewear-Sets-c-3827.html",
            "label": "Shapewear Sets",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-corsets-and-bustier": {
            "url": "https://us.shein.com/Women-Corsets-and-Bustier-c-14058.html",
            "label": "Corsets and Bustier",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-waist-trainers-corset-tops": {
            "url": "https://us.shein.com/category/category-Waist-Trainers-Tops-sc-0081742368.html",
            "label": "Waist trainers & corset tops",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-shapewear-bottoms": {
            "url": "https://us.shein.com/Women-Shapewear-Bottoms-c-3134.html",
            "label": "Shapewear Bottoms",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-shapewear-slips": {
            "url": "https://us.shein.com/Women-Shapewear-Slips-c-3832.html",
            "label": "Shapewear Slips",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-shapewear-bodysuits": {
            "url": "https://us.shein.com/Women-Shapewear-Bodysuits-c-3822.html",
            "label": "Shapewear Bodysuits",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-shapewear-tops": {
            "url": "https://us.shein.com/Women-Shapewear-Tops-c-14060.html",
            "label": "Shapewear Tops",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-shapewear-accessories": {
            "url": "https://us.shein.com/Women-Shapewear-Accessories-c-12798.html",
            "label": "Shapewear Accessories",
            "section": "Women Shapewear",
        },
        "underwear-sleepwear-view-all-12832": {
            "url": "https://us.shein.com/Women-Lingerie-Accessories-c-12832.html",
            "label": "View All",
            "section": "Women Lingerie Accessories",
        },
        "underwear-sleepwear-sticky-bra": {
            "url": "https://us.shein.com/Women-Sticky-Bra-c-12840.html",
            "label": "Sticky Bra",
            "section": "Women Lingerie Accessories",
        },
        "underwear-sleepwear-bra-accessories": {
            "url": "https://us.shein.com/Women-Bra-Accessories-c-12839.html",
            "label": "Bra Accessories",
            "section": "Women Lingerie Accessories",
        },
        "underwear-sleepwear-shape-shifters-protectors": {
            "url": "https://us.shein.com/Women-Shape-Shifters-Protectors-c-12838.html",
            "label": "Shape Shifters & Protectors",
            "section": "Women Lingerie Accessories",
        },
        "underwear-sleepwear-disposable-accessories": {
            "url": "https://us.shein.com/Women-Disposable-Lingerie-Accessories-c-12844.html",
            "label": "Disposable Accessories",
            "section": "Women Lingerie Accessories",
        },
        "underwear-sleepwear-view-all-10050111568": {
            "url": "https://us.shein.com/recommend/Women-curve-sc-10050111568.html",
            "label": "View All",
            "section": "Women Curve",
        },
        "underwear-sleepwear-sleep-lounge": {
            "url": "https://us.shein.com/Women-Plus-Sleep-Lounge-c-2346.html",
            "label": "Sleep & Lounge",
            "section": "Women Curve",
        },
        "underwear-sleepwear-bras": {
            "url": "https://us.shein.com/Plus-Size-Bras-c-12779.html",
            "label": "Bras",
            "section": "Women Curve",
        },
        "underwear-sleepwear-panties": {
            "url": "https://us.shein.com/Plus-Size-Panties-c-2355.html",
            "label": "Panties",
            "section": "Women Curve",
        },
        "underwear-sleepwear-shapewear": {
            "url": "https://us.shein.com/Plus-Size-Corsets-Shapewear-c-3856.html",
            "label": "Shapewear",
            "section": "Women Curve",
        },
        "underwear-sleepwear-view-all-10050111593": {
            "url": "https://us.shein.com/recommend/Thermal-Underwear-sc-10050111593.html",
            "label": "View All",
            "section": "Thermal Underwear",
        },
        "underwear-sleepwear-women-thermal-sets": {
            "url": "https://us.shein.com/Women-Thermal-Underwear-Sets-c-2214.html",
            "label": "Women Thermal Sets",
            "section": "Thermal Underwear",
        },
        "underwear-sleepwear-women-thermal-accessories": {
            "url": "https://us.shein.com/Women-Thermal-Accessories-c-12841.html",
            "label": "Women Thermal Accessories",
            "section": "Thermal Underwear",
        },
        "underwear-sleepwear-men-thermal-sets": {
            "url": "https://us.shein.com/Men-Thermal-Underwear-Sets-c-4321.html",
            "label": "Men Thermal Sets",
            "section": "Thermal Underwear",
        },
        "underwear-sleepwear-men-thermal-accessories": {
            "url": "https://us.shein.com/Men-Thermal-Underwear-Accessories-c-12842.html",
            "label": "Men Thermal Accessories",
            "section": "Thermal Underwear",
        },
        "underwear-sleepwear-men-thermal-bottom": {
            "url": "https://us.shein.com/Men-Thermal-Underwear-Bottoms-c-4320.html",
            "label": "Men Thermal Bottom",
            "section": "Thermal Underwear",
        },
        "underwear-sleepwear-view-all-1972": {
            "url": "https://us.shein.com/Men-Loungewear-c-1972.html",
            "label": "View All",
            "section": "Men Loungewear",
        },
        "underwear-sleepwear-sets": {
            "url": "https://us.shein.com/Men-Loungewear-Sets-c-3743.html",
            "label": "Sets",
            "section": "Men Loungewear",
        },
        "underwear-sleepwear-bottoms": {
            "url": "https://us.shein.com/Men-Loungewear-Bottoms-c-3742.html",
            "label": "Bottoms",
            "section": "Men Loungewear",
        },
        "underwear-sleepwear-robes-1984": {
            "url": "https://us.shein.com/Men-Loungewear-Robes-c-1984.html",
            "label": "Robes",
            "section": "Men Loungewear",
        },
        "underwear-sleepwear-onepieces": {
            "url": "https://us.shein.com/Men-Loungewear-Onepieces-c-3744.html",
            "label": "Onepieces",
            "section": "Men Loungewear",
        },
        "underwear-sleepwear-tops": {
            "url": "https://us.shein.com/category/category-loungewear-basic-tops-sc-0081742482.html",
            "label": "Tops",
            "section": "Men Loungewear",
        },
        "underwear-sleepwear-view-all-4323": {
            "url": "https://us.shein.com/Men-Underwear-c-4323.html",
            "label": "View All",
            "section": "Men Underwear",
        },
        "underwear-sleepwear-trunks": {
            "url": "https://us.shein.com/Men-Trunks-c-1985.html",
            "label": "Trunks",
            "section": "Men Underwear",
        },
        "underwear-sleepwear-boxers": {
            "url": "https://us.shein.com/Men-Boxers-c-4325.html",
            "label": "Boxers",
            "section": "Men Underwear",
        },
        "underwear-sleepwear-briefs-4324": {
            "url": "https://us.shein.com/Men-Briefs-c-4324.html",
            "label": "Briefs",
            "section": "Men Underwear",
        },
        "underwear-sleepwear-sexy-underwear": {
            "url": "https://us.shein.com/category/category-Sexy-Underwear-sc-0081745238.html",
            "label": "Sexy Underwear",
            "section": "Men Underwear",
        },
        "underwear-sleepwear-shapewear-6562": {
            "url": "https://us.shein.com/Men-Shapewear-c-6562.html",
            "label": "Shapewear",
            "section": "Men Underwear",
        },
        "underwear-sleepwear-view-all-4307": {
            "url": "https://us.shein.com/Men-Socks-c-4307.html",
            "label": "View All",
            "section": "Men Socks",
        },
        "underwear-sleepwear-crew-socks-2145": {
            "url": "https://us.shein.com/Men-Crew-Socks-c-2145.html",
            "label": "Crew Socks",
            "section": "Men Socks",
        },
        "underwear-sleepwear-ankle-socks-4309": {
            "url": "https://us.shein.com/Men-Ankle-Socks-c-4309.html",
            "label": "Ankle Socks",
            "section": "Men Socks",
        },
        "underwear-sleepwear-invisible-socks-4308": {
            "url": "https://us.shein.com/Men-Invisible-Socks-c-4308.html",
            "label": "Invisible Socks",
            "section": "Men Socks",
        },
        "underwear-sleepwear-sports-socks-4313": {
            "url": "https://us.shein.com/Men-Sports-Socks-c-4313.html",
            "label": "Sports Socks",
            "section": "Men Socks",
        },
        "underwear-sleepwear-knee-high-socks": {
            "url": "https://us.shein.com/Men-Knee-High-Socks-c-4310.html",
            "label": "Knee High Socks",
            "section": "Men Socks",
        },
        "underwear-sleepwear-customized-socks": {
            "url": "https://us.shein.com/category/category-Customized-socks-sc-0081745363.html",
            "label": "Customized Socks",
            "section": "Customized",
        },
        "underwear-sleepwear-customized-loungewear": {
            "url": "https://us.shein.com/category/category-Customized-loungewear-sc-0081745370.html",
            "label": "Customized Loungewear",
            "section": "Customized",
        },
        "underwear-sleepwear-customized-underwear": {
            "url": "https://us.shein.com/category/category-Customized-underwear-sc-0081745504.html",
            "label": "Customized Underwear",
            "section": "Customized",
        },
    },
    "home": {
        "home": {
            "url": "https://us.shein.com/RecommendSelection/Home-Kitchen-sc-017185546.html",
            "label": "Home & Living",
            "section": "Top category",
        },
        "home-view-all": {
            "url": "https://us.shein.com/Home-Living-c-2032.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "home-new-in": {
            "url": "https://us.shein.com/recommend/Home-Living-New-In-sc-10050001039.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "home-sale": {
            "url": "https://us.shein.com/recommend/sale-Home-Living-sc-10050001114.html",
            "label": "Sale",
            "section": "Shop by Category",
        },
        "home-brands": {
            "url": "https://us.shein.com/recommend/home-brands-sc-10050067933.html",
            "label": "Brands",
            "section": "Shop by Category",
        },
        "home-happy-halloween": {
            "url": "https://us.shein.com/recommend/26-home-halloween-sc-10050095675.html",
            "label": "Happy Halloween",
            "section": "Shop by Category",
        },
        "home-kitchen-dining": {
            "url": "https://us.shein.com/Kitchen-Dining-c-1948.html",
            "label": "Kitchen & Dining",
            "section": "Shop by Category",
        },
        "home-home-decor": {
            "url": "https://us.shein.com/Home-Decor-c-1954.html",
            "label": "Home Decor",
            "section": "Shop by Category",
        },
        "home-event-party-supplies": {
            "url": "https://us.shein.com/Event-Party-Supplies-c-2496.html",
            "label": "Event & Party Supplies",
            "section": "Shop by Category",
        },
        "home-storage-organization": {
            "url": "https://us.shein.com/Storage-Organization-c-2298.html",
            "label": "Storage & Organization",
            "section": "Shop by Category",
        },
        "home-bathroom": {
            "url": "https://us.shein.com/Bathroom-c-2300.html",
            "label": "Bathroom",
            "section": "Shop by Category",
        },
        "home-arts-crafts-sewing": {
            "url": "https://us.shein.com/Arts,Crafts-Sewing-c-3497.html",
            "label": "Arts, Crafts & Sewing",
            "section": "Shop by Category",
        },
        "home-household-cleaning-personal-care": {
            "url": "https://us.shein.com/Household-Cleaning-c-3988.html",
            "label": "Household Cleaning & Personal Care",
            "section": "Shop by Category",
        },
        "home-outdoor-garden": {
            "url": "https://us.shein.com/Outdoor-Garden-c-3350.html",
            "label": "Outdoor & Garden",
            "section": "Shop by Category",
        },
        "home-home-essentials": {
            "url": "https://us.shein.com/Home-Essentials-c-1959.html",
            "label": "Home Essentials",
            "section": "Shop by Category",
        },
        "home-household-merchandises": {
            "url": "https://us.shein.com/Household-Merchandises-c-3989.html",
            "label": "Household Merchandises",
            "section": "Shop by Category",
        },
        "home-musical-instruments-accessories": {
            "url": "https://us.shein.com/Musical-Instruments-Accessories-c-4862.html",
            "label": "Musical Instruments & Accessories",
            "section": "Shop by Category",
        },
        "home-save-home-living": {
            "url": "https://us.shein.com/Save-Home-Living-sc-10050114905.html",
            "label": "Save Home Living",
            "section": "Shop by Category",
        },
        "home-tapestries": {
            "url": "https://us.shein.com/Tapestries-c-7988.html",
            "label": "Tapestries",
            "section": "Picks for You",
        },
        "home-bathroom-shelves-corner-shelves": {
            "url": "https://us.shein.com/Bathroom-Shelves-Corner-Shelves-c-8273.html",
            "label": "Bathroom Shelves & Corner Shelves",
            "section": "Picks for You",
        },
        "home-bathroom-accessory-sets": {
            "url": "https://us.shein.com/Bathroom-Accessory-Sets-c-6044.html",
            "label": "Bathroom Accessory Sets",
            "section": "Picks for You",
        },
        "home-christmas-party-supplies": {
            "url": "https://us.shein.com/Christmas-Party-Supplies-c-8162.html",
            "label": "Christmas Party Supplies",
            "section": "Picks for You",
        },
        "home-towel-sets": {
            "url": "https://us.shein.com/Towel-Sets-c-3403.html",
            "label": "Towel Sets",
            "section": "Picks for You",
        },
        "home-smoking-accessories-accessory-sets": {
            "url": "https://us.shein.com/Smoking-Accessories-Accessory-Sets-c-13936.html",
            "label": "Smoking Accessories& Accessory Sets",
            "section": "Picks for You",
        },
        "home-office-trash-can": {
            "url": "https://us.shein.com/Office-Trash-Can-c-11850.html",
            "label": "Office Trash Can",
            "section": "Picks for You",
        },
        "home-makeup-organizers-display-cases": {
            "url": "https://us.shein.com/Makeup-Organizers-Display-Cases-c-4447.html",
            "label": "Makeup Organizers & Display Cases",
            "section": "Picks for You",
        },
        "home-storage-drawers": {
            "url": "https://us.shein.com/Storage-Drawers-c-3547.html",
            "label": "Storage Drawers",
            "section": "Picks for You",
        },
        "home-decorative-painting-calligraphy": {
            "url": "https://us.shein.com/Decorative-Painting-Calligraphy-c-1955.html",
            "label": "Decorative Painting & Calligraphy",
            "section": "Picks for You",
        },
        "home-bath-mats": {
            "url": "https://us.shein.com/Bath-Mats-c-2302.html",
            "label": "Bath Mats",
            "section": "Picks for You",
        },
        "home-decorative-hanging-ornaments": {
            "url": "https://us.shein.com/Decorative-Hanging-Ornaments-c-2519.html",
            "label": "Decorative Hanging Ornaments",
            "section": "Picks for You",
        },
        "home-shower-caps": {
            "url": "https://us.shein.com/Shower-Caps-c-3382.html",
            "label": "Shower Caps",
            "section": "Picks for You",
        },
        "home-decorative-crafts": {
            "url": "https://us.shein.com/Decorative-Crafts-c-8438.html",
            "label": "Decorative Crafts",
            "section": "Picks for You",
        },
        "home-wall-paper": {
            "url": "https://us.shein.com/Wall-Paper-c-3488.html",
            "label": "Wall Paper",
            "section": "Picks for You",
        },
        "home-floating-shelves-for-wall": {
            "url": "https://us.shein.com/Floating-Shelves-for-Wall-c-11718.html",
            "label": "Floating Shelves for Wall",
            "section": "Picks for You",
        },
        "home-artificial-flowers": {
            "url": "https://us.shein.com/Artificial-Flowers-c-3432.html",
            "label": "Artificial Flowers",
            "section": "Picks for You",
        },
        "home-household-gloves": {
            "url": "https://us.shein.com/Household-Gloves-c-3505.html",
            "label": "Household Gloves",
            "section": "Picks for You",
        },
    },
    "jewelry": {
        "jewelry": {
            "url": "https://us.shein.com/RecommendSelection/Jewelry-Accessories-sc-017291431.html",
            "label": "Jewelry & Accessories",
            "section": "Top category",
        },
        "jewelry-top-rated": {
            "url": "https://us.shein.com/recommend/Top-Rated-Jew-Acc-sc-10050008937.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "jewelry-winter-chic": {
            "url": "https://us.shein.com/recommend/Winter-Accs-and-Jewelry-sc-10050111326.html",
            "label": "Winter Chic",
            "section": "Shop by Category",
        },
        "jewelry-halloween": {
            "url": "https://us.shein.com/recommend/Halloween-ACC-sc-10050102758.html",
            "label": "Halloween",
            "section": "Shop by Category",
        },
        "jewelry-trendy": {
            "url": "https://us.shein.com/recommend/trendy-jew-sc-10050060329.html",
            "label": "Trendy",
            "section": "Shop by Category",
        },
        "jewelry-women-scarves-earmuffs": {
            "url": "https://us.shein.com/recommend/Women-Scarves-Earmuffs-sc-10050008949.html",
            "label": "Women Scarves & Earmuffs",
            "section": "Shop by Category",
        },
        "jewelry-women-belts-accessories": {
            "url": "https://us.shein.com/Women-Belts-Belts-Accessories-c-3868.html",
            "label": "Women Belts & Accessories",
            "section": "Shop by Category",
        },
        "jewelry-women-s-earrings": {
            "url": "https://us.shein.com/Women-s-Earrings-c-4202.html",
            "label": "Women's Earrings",
            "section": "Shop by Category",
        },
        "jewelry-women-s-necklaces": {
            "url": "https://us.shein.com/Women-s-Necklaces-c-4208.html",
            "label": "Women's Necklaces",
            "section": "Shop by Category",
        },
        "jewelry-women-s-rings-bracelets": {
            "url": "https://us.shein.com/style/Women-Rings-and-Bracelets-sc-001312477.html",
            "label": "Women's Rings & Bracelets",
            "section": "Shop by Category",
        },
        "jewelry-women-hair-accessories": {
            "url": "https://us.shein.com/Women-Hair-Accessories-c-3013.html",
            "label": "Women Hair Accessories",
            "section": "Shop by Category",
        },
        "jewelry-men-fashion-accessories": {
            "url": "https://us.shein.com/Men-Accessories-c-2027.html",
            "label": "Men Fashion Accessories",
            "section": "Shop by Category",
        },
        "jewelry-jewelry-making": {
            "url": "https://us.shein.com/Jewelry-Making-c-4219.html",
            "label": "Jewelry Making",
            "section": "Shop by Category",
        },
        "jewelry-fine-jewelry": {
            "url": "https://us.shein.com/Fine-Jewelry-c-3035.html",
            "label": "Fine Jewelry",
            "section": "Shop by Category",
        },
        "jewelry-watches-accs": {
            "url": "https://us.shein.com/style/View-All-Watches-sc-001277150.html",
            "label": "Watches & Accs",
            "section": "Shop by Category",
        },
        "jewelry-wedding-event": {
            "url": "https://us.shein.com/Wedding-Event-c-5907.html",
            "label": "Wedding & Event",
            "section": "Shop by Category",
        },
        "jewelry-gender-neutral-accessories": {
            "url": "https://us.shein.com/Gender-Neutral-Accessories-c-9289.html",
            "label": "Gender Neutral Accessories",
            "section": "Shop by Category",
        },
        "jewelry-men-s-fashion-jewelry": {
            "url": "https://us.shein.com/Men-s-Fashion-Jewelry-c-6191.html",
            "label": "Men's Fashion Jewelry",
            "section": "Shop by Category",
        },
        "jewelry-body-jewelry-others": {
            "url": "https://us.shein.com/Women-Body-Jewelry-Sets-c-4885.html",
            "label": "Body Jewelry & Others",
            "section": "Shop by Category",
        },
        "jewelry-jewelry-storage-organization": {
            "url": "https://us.shein.com/Jewelry-Organizers-Gift-Wrapping-Supplies-c-4656.html",
            "label": "Jewelry Storage & Organization",
            "section": "Shop by Category",
        },
        "jewelry-jewelry-casting-supplies": {
            "url": "https://us.shein.com/Jewelry-Casting-Supplies-c-13077.html",
            "label": "Jewelry Casting Supplies",
            "section": "Shop by Category",
        },
        "jewelry-customized-jewelry": {
            "url": "https://us.shein.com/recommend/Customized-Jewelry-sc-10050013269.html",
            "label": "Customized Jewelry",
            "section": "Shop by Category",
        },
        "jewelry-customized-accessories": {
            "url": "https://us.shein.com/Customized-Accessories-c-9145.html",
            "label": "Customized Accessories",
            "section": "Shop by Category",
        },
        "jewelry-women-chain-bracelets": {
            "url": "https://us.shein.com/Women-Chain-Bracelets-c-1758.html",
            "label": "Women Chain Bracelets",
            "section": "Picks for You",
        },
        "jewelry-women-belly-ring": {
            "url": "https://us.shein.com/Women-Belly-Ring-c-4878.html",
            "label": "Women Belly Ring",
            "section": "Picks for You",
        },
        "jewelry-women-earring-sets": {
            "url": "https://us.shein.com/Women-Earring-Sets-c-4207.html",
            "label": "Women Earring Sets",
            "section": "Picks for You",
        },
        "jewelry-smartwatch-band": {
            "url": "https://us.shein.com/Smartwatch-Band-c-3064.html",
            "label": "Smartwatch Band",
            "section": "Picks for You",
        },
        "jewelry-watchbands": {
            "url": "https://us.shein.com/Watchbands-c-3030.html",
            "label": "Watchbands",
            "section": "Picks for You",
        },
        "jewelry-women-nose-ring": {
            "url": "https://us.shein.com/Women-Nose-Ring-c-4876.html",
            "label": "Women Nose Ring",
            "section": "Picks for You",
        },
        "jewelry-women-bracelet-sets": {
            "url": "https://us.shein.com/Women-Bracelet-Sets-c-4201.html",
            "label": "Women Bracelet Sets",
            "section": "Picks for You",
        },
        "jewelry-women-ring-sets": {
            "url": "https://us.shein.com/Women-Ring-Sets-c-4218.html",
            "label": "Women Ring Sets",
            "section": "Picks for You",
        },
        "jewelry-women-bangles": {
            "url": "https://us.shein.com/Women-Bangles-c-4198.html",
            "label": "Women Bangles",
            "section": "Picks for You",
        },
        "jewelry-women-pendant-necklaces": {
            "url": "https://us.shein.com/Women-Pendant-Necklaces-c-1755.html",
            "label": "Women Pendant Necklaces",
            "section": "Picks for You",
        },
        "jewelry-women-tooth-jewelry": {
            "url": "https://us.shein.com/Women-Tooth-Jewelry-c-7623.html",
            "label": "Women Tooth Jewelry",
            "section": "Picks for You",
        },
        "jewelry-women-chokers": {
            "url": "https://us.shein.com/Women-Chokers-c-4209.html",
            "label": "Women Chokers",
            "section": "Picks for You",
        },
        "jewelry-customized-fashion-word-necklaces": {
            "url": "https://us.shein.com/Customized-Fashion-Word-Necklaces-c-8762.html",
            "label": "Customized Fashion Word Necklaces",
            "section": "Picks for You",
        },
        "jewelry-women-quartz-watches": {
            "url": "https://us.shein.com/Women-Quartz-Watches-c-1920.html",
            "label": "Women Quartz Watches",
            "section": "Picks for You",
        },
    },
    "beauty": {
        "beauty": {
            "url": "https://us.shein.com/RecommendSelection/Beauty-Health-sc-017172970.html",
            "label": "Beauty & Health",
            "section": "Top category",
        },
        "beauty-view-all": {
            "url": "https://us.shein.com/Beauty-Health-c-1864.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "beauty-beauty-hub": {
            "url": "https://us.shein.com/recommend/Beauty-sc-10050088372.html",
            "label": "Beauty Hub",
            "section": "Shop by Category",
        },
        "beauty-k-beauty": {
            "url": "https://us.shein.com/recommend/K-beauty-sc-10050031458.html",
            "label": "K-beauty",
            "section": "Shop by Category",
        },
        "beauty-quality-brands": {
            "url": "https://us.shein.com/recommend/Brands-sc-10050049991.html",
            "label": "Quality Brands",
            "section": "Shop by Category",
        },
        "beauty-makeup": {
            "url": "https://us.shein.com/Makeup-c-2042.html",
            "label": "Makeup",
            "section": "Shop by Category",
        },
        "beauty-beauty-tools": {
            "url": "https://us.shein.com/Beauty-Tools-c-2041.html",
            "label": "Beauty Tools",
            "section": "Shop by Category",
        },
        "beauty-nail-hand-foot-care": {
            "url": "https://us.shein.com/category/Nail-Hand-and-Foot-Care-sc-0081657895.html",
            "label": "Nail, Hand & Foot Care",
            "section": "Shop by Category",
        },
        "beauty-press-on-nails": {
            "url": "https://us.shein.com/Press-On-Nails-c-1869.html",
            "label": "Press on Nails",
            "section": "Shop by Category",
        },
        "beauty-eyelashes": {
            "url": "https://us.shein.com/Eyelashes-c-3638.html",
            "label": "Eyelashes",
            "section": "Shop by Category",
        },
        "beauty-wigs-accs": {
            "url": "https://us.shein.com/Wigs-Accs-c-3644.html",
            "label": "Wigs & Accs",
            "section": "Shop by Category",
        },
        "beauty-personal-care": {
            "url": "https://us.shein.com/Personal-Care-c-2171.html",
            "label": "Personal Care",
            "section": "Shop by Category",
        },
        "beauty-hair-care": {
            "url": "https://us.shein.com/category/Hair-Care-sc-0081657900.html",
            "label": "Hair Care",
            "section": "Shop by Category",
        },
        "beauty-skin-care": {
            "url": "https://us.shein.com/category/Skin-Care-sc-0081657909.html",
            "label": "Skin Care",
            "section": "Shop by Category",
        },
        "beauty-makeup-bag-storage": {
            "url": "https://us.shein.com/Makeup-Bag-Storage-c-8494.html",
            "label": "Makeup Bag & Storage",
            "section": "Shop by Category",
        },
        "beauty-fragrances-aromatherapy": {
            "url": "https://us.shein.com/Fragrances-Aromatherapy-c-4801.html",
            "label": "Fragrances & Aromatherapy",
            "section": "Shop by Category",
        },
        "beauty-personal-care-appliance": {
            "url": "https://us.shein.com/Personal-Care-Appliance-c-3862.html",
            "label": "Personal Care Appliance",
            "section": "Shop by Category",
        },
        "beauty-health-care": {
            "url": "https://us.shein.com/category/Health-Care-sc-0081656854.html",
            "label": "Health Care",
            "section": "Shop by Category",
        },
        "beauty-dietary-supplements": {
            "url": "https://us.shein.com/Dietary-Supplements-c-7416.html",
            "label": "Dietary Supplements",
            "section": "Shop by Category",
        },
        "beauty-sexual-wellness": {
            "url": "https://us.shein.com/Sexual-Wellness-c-4451.html",
            "label": "Sexual Wellness",
            "section": "Shop by Category",
        },
        "beauty-false-eyelashes-and-adhesives-kits": {
            "url": "https://us.shein.com/False-Eyelashes-and-Adhesives-Kits-c-4832.html",
            "label": "False Eyelashes and Adhesives Kits",
            "section": "Picks for You",
        },
        "beauty-brushes-sets": {
            "url": "https://us.shein.com/Brushes-Sets-c-1865.html",
            "label": "Brushes Sets",
            "section": "Picks for You",
        },
        "beauty-perfume": {
            "url": "https://us.shein.com/Perfume-c-4805.html",
            "label": "Perfume",
            "section": "Picks for You",
        },
        "beauty-individual-eyelashes": {
            "url": "https://us.shein.com/Individual-Eyelashes-c-3867.html",
            "label": "Individual Eyelashes",
            "section": "Picks for You",
        },
        "beauty-handmade-false-nails": {
            "url": "https://us.shein.com/Handmade-False-Nails-c-14506.html",
            "label": "Handmade False Nails",
            "section": "Picks for You",
        },
        "beauty-makeup-bags": {
            "url": "https://us.shein.com/Makeup-Bags-c-1909.html",
            "label": "Makeup Bags",
            "section": "Picks for You",
        },
        "beauty-single-eyeshadow": {
            "url": "https://us.shein.com/Single-Eyeshadow-c-8989.html",
            "label": "Single Eyeshadow",
            "section": "Picks for You",
        },
        "beauty-false-eyelashes": {
            "url": "https://us.shein.com/False-Eyelashes-c-2251.html",
            "label": "False Eyelashes",
            "section": "Picks for You",
        },
        "beauty-facial-cleaning-tools": {
            "url": "https://us.shein.com/Facial-Cleaning-Tools-c-2472.html",
            "label": "Facial Cleaning Tools",
            "section": "Picks for You",
        },
        "beauty-styling-tools": {
            "url": "https://us.shein.com/Styling-Tools-c-3701.html",
            "label": "Styling Tools",
            "section": "Picks for You",
        },
        "beauty-human-lace-wigs": {
            "url": "https://us.shein.com/Human-Lace-Wigs-c-3843.html",
            "label": "Human Lace Wigs",
            "section": "Picks for You",
        },
        "beauty-vitamins-minerals": {
            "url": "https://us.shein.com/Vitamins-Minerals-c-7432.html",
            "label": "Vitamins/Minerals",
            "section": "Picks for You",
        },
    },
    "baby": {
        "baby": {
            "url": "https://us.shein.com/RecommendSelection/Baby-Maternity-sc-017172967.html",
            "label": "Baby & Maternity",
            "section": "Top category",
        },
        "baby-view-all": {
            "url": "https://us.shein.com/recommend/All_Baby-Shop-By-Category_View-All-sc-1004696117.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "baby-top-rated": {
            "url": "https://us.shein.com/recommend/All_Baby-Shop-By-Category_Top-Rated-sc-1004696237.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "baby-new-in": {
            "url": "https://us.shein.com/recommend/All_Baby-Shop-By-Category_New-in-sc-1004696153.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "baby-baby-boys-0-3yrs": {
            "url": "https://us.shein.com/Baby-Boys-Clothing-c-6440.html",
            "label": "Baby Boys(0-3Yrs)",
            "section": "Shop by Category",
        },
        "baby-baby-girls-0-3-yrs": {
            "url": "https://us.shein.com/Baby-Girls-Clothing-c-3225.html",
            "label": "Baby Girls (0-3 Yrs)",
            "section": "Shop by Category",
        },
        "baby-newborn-0-9m": {
            "url": "https://us.shein.com/Newborn-Baby-Clothing-c-13039.html",
            "label": "Newborn(0-9M)",
            "section": "Shop by Category",
        },
        "baby-baby-unisex": {
            "url": "https://us.shein.com/style/Unisex-Baby-sc-00128045.html",
            "label": "Baby Unisex",
            "section": "Shop by Category",
        },
        "baby-baby-supplies": {
            "url": "https://us.shein.com/style/Baby-Acc-All-sc-0011884000.html",
            "label": "Baby Supplies",
            "section": "Shop by Category",
        },
        "baby-baby-shoes": {
            "url": "https://us.shein.com/Baby-Shoes-c-2063.html",
            "label": "Baby Shoes",
            "section": "Shop by Category",
        },
        "baby-baby-toys": {
            "url": "https://us.shein.com/Baby-Toys-c-5977.html",
            "label": "Baby Toys",
            "section": "Shop by Category",
        },
        "baby-pregnancy-maternity": {
            "url": "https://us.shein.com/style/Pregnancy-And-Maternity-sc-0011891748.html",
            "label": "Pregnancy & Maternity",
            "section": "Shop by Category",
        },
        "baby-maternity-clothing": {
            "url": "https://us.shein.com/Maternity-Clothing-c-4437.html",
            "label": "Maternity Clothing",
            "section": "Shop by Category",
        },
        "baby-newborn-baby-sets": {
            "url": "https://us.shein.com/Newborn-Baby-Sets-c-13046.html",
            "label": "Newborn Baby Sets",
            "section": "Picks for You",
        },
        "baby-baby-girls-bodysuits": {
            "url": "https://us.shein.com/Baby-Girls-Bodysuits-c-2838.html",
            "label": "Baby Girls Bodysuits",
            "section": "Picks for You",
        },
        "baby-baby-boys-jumpsuits": {
            "url": "https://us.shein.com/Baby-Boys-Jumpsuits-c-6445.html",
            "label": "Baby Boys Jumpsuits",
            "section": "Picks for You",
        },
        "baby-baby-boys-tops": {
            "url": "https://us.shein.com/Baby-Boys-Tops-c-6461.html",
            "label": "Baby Boys Tops",
            "section": "Picks for You",
        },
        "baby-baby-boys-t-shirt-co-ords": {
            "url": "https://us.shein.com/Baby-Boys-T-Shirt-Co-ords-c-6454.html",
            "label": "Baby Boys T-Shirt Co-ords",
            "section": "Picks for You",
        },
        "baby-baby-boys-hoodie-sweatshirt-co-ords": {
            "url": "https://us.shein.com/Baby-Boys-Hoodie-Sweatshirt-Co-ords-c-14037.html",
            "label": "Baby Boys Hoodie & Sweatshirt Co-ords",
            "section": "Picks for You",
        },
        "baby-baby-girls-dresses": {
            "url": "https://us.shein.com/Baby-Girls-Dresses-c-2135.html",
            "label": "Baby Girls Dresses",
            "section": "Picks for You",
        },
        "baby-baby-girls-hoodie-sweatshirt-co-ords": {
            "url": "https://us.shein.com/Baby-Girls-Hoodie-Sweatshirt-Co-ords-c-14044.html",
            "label": "Baby Girls Hoodie & Sweatshirt Co-ords",
            "section": "Picks for You",
        },
        "baby-baby-boys-outerwear-co-ords": {
            "url": "https://us.shein.com/Baby-Boys-Outerwear-Co-ords-c-14034.html",
            "label": "Baby Boys Outerwear Co-ords",
            "section": "Picks for You",
        },
        "baby-newborn-baby-pajamas": {
            "url": "https://us.shein.com/Newborn-Baby-Pajamas-c-13044.html",
            "label": "Newborn Baby Pajamas",
            "section": "Picks for You",
        },
        "baby-nursery-storage": {
            "url": "https://us.shein.com/Nursery-Storage-c-6374.html",
            "label": "Nursery Storage",
            "section": "Picks for You",
        },
        "baby-newborn-baby-bodysuits": {
            "url": "https://us.shein.com/Newborn-Baby-Bodysuits-c-13051.html",
            "label": "Newborn Baby Bodysuits",
            "section": "Picks for You",
        },
        "baby-baby-girls-sweaters": {
            "url": "https://us.shein.com/Baby-Girls-Sweaters-c-2460.html",
            "label": "Baby Girls Sweaters",
            "section": "Picks for You",
        },
    },
    "bags": {
        "bags": {
            "url": "https://us.shein.com/RecommendSelection/Bags-Luggage-sc-017174546.html",
            "label": "Bags & Luggage",
            "section": "Top category",
        },
        "bags-view-all": {
            "url": "https://us.shein.com/Bags-Luggage-c-3637.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "bags-top-rated": {
            "url": "https://us.shein.com/hotsale/Bags-Hot-Sale-sc-003521678.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "bags-winter-chic": {
            "url": "https://us.shein.com/recommend/Cozy-Bags-sc-10050109952.html",
            "label": "Winter Chic",
            "section": "Shop by Category",
        },
        "bags-women-bags": {
            "url": "https://us.shein.com/Women-Bags-c-2043.html",
            "label": "Women Bags",
            "section": "Shop by Category",
        },
        "bags-luggage-travel-gear": {
            "url": "https://us.shein.com/Luggage-Travel-Gear-c-4099.html",
            "label": "Luggage & Travel Gear",
            "section": "Shop by Category",
        },
        "bags-lunch-bags": {
            "url": "https://us.shein.com/Lunch-Bag-c-9079.html",
            "label": "Lunch Bags",
            "section": "Shop by Category",
        },
        "bags-men-bags": {
            "url": "https://us.shein.com/Men-Bags-c-2090.html",
            "label": "Men Bags",
            "section": "Shop by Category",
        },
        "bags-wallets-cardholders": {
            "url": "https://us.shein.com/Wallets-Cardholders-c-4258.html",
            "label": "Wallets & Cardholders",
            "section": "Shop by Category",
        },
        "bags-bag-accessories": {
            "url": "https://us.shein.com/Bag-Accessories-c-4268.html",
            "label": "Bag Accessories",
            "section": "Shop by Category",
        },
        "bags-hot-deals": {
            "url": "https://us.shein.com/hotsale/Hot-Deals-sc-0031656702.html",
            "label": "Hot Deals",
            "section": "Shop by Category",
        },
        "bags-sheintrendy": {
            "url": "https://us.shein.com/recommend/SHEINtrendy-sc-10050013230.html",
            "label": "#SHEINtrendy",
            "section": "Shop by Category",
        },
        "bags-customized-bags": {
            "url": "https://us.shein.com/recommend/Customized-Bags-sc-10050009168.html",
            "label": "Customized Bags",
            "section": "Shop by Category",
        },
        "bags-newchic": {
            "url": "https://us.shein.com/new/New-Arrivals-sc-0021043511.html",
            "label": "Newchic",
            "section": "Women Bags",
        },
        "bags-shoulder-bags": {
            "url": "https://us.shein.com/Women-Shoulder-Bags-c-1764.html",
            "label": "Shoulder Bags",
            "section": "Women Bags",
        },
        "bags-top-handle-bags": {
            "url": "https://us.shein.com/Women-Top-Handle-Bags-c-2155.html",
            "label": "Top Handle Bags",
            "section": "Women Bags",
        },
        "bags-backpacks": {
            "url": "https://us.shein.com/Women-Backpacks-c-4256.html",
            "label": "Backpacks",
            "section": "Women Bags",
        },
        "bags-bag-sets": {
            "url": "https://us.shein.com/Women-Bag-Sets-c-2157.html",
            "label": "Bag Sets",
            "section": "Women Bags",
        },
        "bags-crossbody-bags": {
            "url": "https://us.shein.com/Women-Crossbody-c-2152.html",
            "label": "Crossbody Bags",
            "section": "Women Bags",
        },
        "bags-tote-bags": {
            "url": "https://us.shein.com/Women-Tote-Bags-c-2844.html",
            "label": "Tote Bags",
            "section": "Women Bags",
        },
        "bags-evening-bags": {
            "url": "https://us.shein.com/Women-Evening-Bags-c-3876.html",
            "label": "Evening Bags",
            "section": "Women Bags",
        },
        "bags-wallets-cardholders-100150772": {
            "url": "https://us.shein.com/recommend/Women-Wallets-Cardholders-sc-100150772.html",
            "label": "Wallets & Cardholders",
            "section": "Women Bags",
        },
        "bags-waist-bags-arm-bags": {
            "url": "https://us.shein.com/trends/Bags-and-Luggage-sc-0061655176.html",
            "label": "Waist Bags & Arm Bags",
            "section": "Women Bags",
        },
        "bags-wristlet-bags-clutches": {
            "url": "https://us.shein.com/trends/Bags-and-Luggage-sc-0061655182.html",
            "label": "Wristlet Bags & Clutches",
            "section": "Women Bags",
        },
        "bags-customized-women-bags": {
            "url": "https://us.shein.com/Customized-Women-Shoulder-Bags-c-9521.html",
            "label": "Customized Women Bags",
            "section": "Women Bags",
        },
        "bags-travel-accessories-supplies": {
            "url": "https://us.shein.com/Travel-Accessories-Supplies-c-4284.html",
            "label": "Travel Accessories & Supplies",
            "section": "Luggage & Travel Gear",
        },
        "bags-travel-storage": {
            "url": "https://us.shein.com/Travel-Storage-c-9077.html",
            "label": "Travel Storage",
            "section": "Luggage & Travel Gear",
        },
        "bags-travel-bags": {
            "url": "https://us.shein.com/Travel-Bags-c-9068.html",
            "label": "Travel Bags",
            "section": "Luggage & Travel Gear",
        },
        "bags-luggage": {
            "url": "https://us.shein.com/Luggage-c-4283.html",
            "label": "Luggage",
            "section": "Luggage & Travel Gear",
        },
        "bags-travel-essentials": {
            "url": "https://us.shein.com/trends/Travel-Bags-sc-0061651556.html",
            "label": "Travel Essentials",
            "section": "Luggage & Travel Gear",
        },
        "bags-travel-tote-backpacks": {
            "url": "https://us.shein.com/Travel-Tote-Backpacks-c-9071.html",
            "label": "Travel Tote Backpacks",
            "section": "Luggage & Travel Gear",
        },
        "bags-make-up-bags": {
            "url": "https://us.shein.com/Make-Up-Bags-c-4455.html",
            "label": "Make Up Bags",
            "section": "Luggage & Travel Gear",
        },
        "bags-suitcases": {
            "url": "https://us.shein.com/Suitcases-c-4102.html",
            "label": "Suitcases",
            "section": "Luggage & Travel Gear",
        },
        "bags-customized-travel-accessories-supplies": {
            "url": "https://us.shein.com/Customized-Travel-Accesories-Supplies-c-11648.html",
            "label": "Customized Travel Accessories & Supplies",
            "section": "Luggage & Travel Gear",
        },
        "bags-customized-travel-bags": {
            "url": "https://us.shein.com/Customized-Travel-Bags-c-11664.html",
            "label": "Customized Travel Bags",
            "section": "Luggage & Travel Gear",
        },
        "bags-backpacks-4280": {
            "url": "https://us.shein.com/Men-Backpacks-c-4280.html",
            "label": "Backpacks",
            "section": "Men Bags",
        },
        "bags-waist-bags": {
            "url": "https://us.shein.com/Men-Waist-Bags-c-2150.html",
            "label": "Waist Bags",
            "section": "Men Bags",
        },
        "bags-bag-sets-3741": {
            "url": "https://us.shein.com/Men-Bag-Sets-c-3741.html",
            "label": "Bag Sets",
            "section": "Men Bags",
        },
        "bags-crossbody-bags-message-bags": {
            "url": "https://us.shein.com/category/Crossbody-Bags-and-Message-Bags-sc-0081655163.html",
            "label": "Crossbody Bags & Message Bags",
            "section": "Men Bags",
        },
        "bags-clutches-wristlet-bags": {
            "url": "https://us.shein.com/Men-Clutches-Wristlet-Bags-c-4279.html",
            "label": "Clutches & Wristlet Bags",
            "section": "Men Bags",
        },
        "bags-tote-bags-2128": {
            "url": "https://us.shein.com/Men-Tote-Bags-c-2128.html",
            "label": "Tote Bags",
            "section": "Men Bags",
        },
        "bags-briefcase": {
            "url": "https://us.shein.com/Men-Briefcase-c-2159.html",
            "label": "Briefcase",
            "section": "Men Bags",
        },
        "bags-wallets-cardholders-100150344": {
            "url": "https://us.shein.com/recommend/Men-Wallets-Cardholders-sc-100150344.html",
            "label": "Wallets & Cardholders",
            "section": "Men Bags",
        },
        "bags-view-all-4458": {
            "url": "https://us.shein.com/Functional-Bags-c-4458.html",
            "label": "View All",
            "section": "Functional Bags",
        },
        "bags-sports-bags": {
            "url": "https://us.shein.com/Sport-Bag-c-13353.html",
            "label": "Sports Bags",
            "section": "Functional Bags",
        },
        "bags-storage-bags": {
            "url": "https://us.shein.com/Storage-Bag-c-4460.html",
            "label": "Storage Bags",
            "section": "Functional Bags",
        },
        "bags-digital-bags": {
            "url": "https://us.shein.com/Digital-Bags-c-4464.html",
            "label": "Digital Bags",
            "section": "Functional Bags",
        },
        "bags-laptop-bags": {
            "url": "https://us.shein.com/Laptop-Bag-c-4467.html",
            "label": "Laptop Bags",
            "section": "Functional Bags",
        },
        "bags-tool-bags": {
            "url": "https://us.shein.com/Tool-Bag-c-4466.html",
            "label": "Tool Bags",
            "section": "Functional Bags",
        },
        "bags-hiking-daypacks": {
            "url": "https://us.shein.com/trends/Hiking-Daypacks-sc-0061656337.html",
            "label": "Hiking Daypacks",
            "section": "Functional Bags",
        },
        "bags-other-storage": {
            "url": "https://us.shein.com/Other-Storage-c-4463.html",
            "label": "Other Storage",
            "section": "Functional Bags",
        },
        "bags-cloth-storage-bags": {
            "url": "https://us.shein.com/trends/Cloth-Storage-Bag-sc-0061655187.html",
            "label": "Cloth Storage Bags",
            "section": "Functional Bags",
        },
        "bags-customized-digital-bags": {
            "url": "https://us.shein.com/Customized-Digital-Bags-c-11666.html",
            "label": "Customized Digital Bags",
            "section": "Functional Bags",
        },
        "bags-customized-laptop-bags": {
            "url": "https://us.shein.com/Customized-Laptop-Bags-c-11661.html",
            "label": "Customized Laptop Bags",
            "section": "Functional Bags",
        },
        "bags-customized-lunch-bag": {
            "url": "https://us.shein.com/Customized-Lunch-Bag-c-11659.html",
            "label": "Customized Lunch Bag",
            "section": "Functional Bags",
        },
        "bags-customized-sports-bag": {
            "url": "https://us.shein.com/Customized-Sports-Bag-c-11663.html",
            "label": "Customized Sports Bag",
            "section": "Functional Bags",
        },
        "bags-customized-storage-bags": {
            "url": "https://us.shein.com/Customized-Storage-Bags-c-11658.html",
            "label": "Customized Storage Bags",
            "section": "Functional Bags",
        },
        "bags-customized-tool-bags": {
            "url": "https://us.shein.com/Customized-Tool-Bags-c-11665.html",
            "label": "Customized Tool Bags",
            "section": "Functional Bags",
        },
        "bags-small-wallets": {
            "url": "https://us.shein.com/Small-Wallets-c-2154.html",
            "label": "Small Wallets",
            "section": "Wallets & Cardholders",
        },
        "bags-card-holders": {
            "url": "https://us.shein.com/Card-Holders-c-4263.html",
            "label": "Card Holders",
            "section": "Wallets & Cardholders",
        },
        "bags-long-wallets": {
            "url": "https://us.shein.com/Long-Wallets-c-4262.html",
            "label": "Long Wallets",
            "section": "Wallets & Cardholders",
        },
        "bags-coin-purses-key-cases": {
            "url": "https://us.shein.com/category/Coin-Purses-and-Key-Cases-sc-0081655172.html",
            "label": "Coin Purses & Key Cases",
            "section": "Wallets & Cardholders",
        },
        "bags-phone-wallets": {
            "url": "https://us.shein.com/Phone-Wallets-c-4259.html",
            "label": "Phone Wallets",
            "section": "Wallets & Cardholders",
        },
        "bags-customized-wallets-cardholders": {
            "url": "https://us.shein.com/Customized-Wallets-Cardholders-c-9520.html",
            "label": "Customized Wallets & Cardholders",
            "section": "Wallets & Cardholders",
        },
        "bags-bag-charms": {
            "url": "https://us.shein.com/Bag-Charms-c-2158.html",
            "label": "Bag Charms",
            "section": "Bag Accessories",
        },
        "bags-bag-straps": {
            "url": "https://us.shein.com/Bag-Straps-c-4269.html",
            "label": "Bag Straps",
            "section": "Bag Accessories",
        },
        "bags-bag-inserts": {
            "url": "https://us.shein.com/Bag-Inserts-c-4270.html",
            "label": "Bag Inserts",
            "section": "Bag Accessories",
        },
        "bags-diy-bag-accessories": {
            "url": "https://us.shein.com/DIY-Bag-Accessories-c-4272.html",
            "label": "DIY Bag Accessories",
            "section": "Bag Accessories",
        },
        "bags-bag-covers": {
            "url": "https://us.shein.com/Bag-Covers-c-4271.html",
            "label": "Bag Covers",
            "section": "Bag Accessories",
        },
        "bags-customized-bag-accessories": {
            "url": "https://us.shein.com/Customized-Bag-Accessories-c-9523.html",
            "label": "Customized Bag Accessories",
            "section": "Bag Accessories",
        },
        "bags-disney": {
            "url": "https://us.shein.com/recommend/Disney-Bags-sc-1004633271.html",
            "label": "Disney",
            "section": "Brands",
        },
        "bags-sanrio": {
            "url": "https://us.shein.com/recommend/Sanrio-Bags-sc-1004633281.html",
            "label": "Sanrio",
            "section": "Brands",
        },
        "bags-tom-jerry": {
            "url": "https://us.shein.com/recommend/Tom-and-Jerry-Bags-sc-10050002314.html",
            "label": "Tom & Jerry",
            "section": "Brands",
        },
        "bags-the-powerpuff-girls": {
            "url": "https://us.shein.com/recommend/The-Powerpuff-Girls-Bags-sc-10050002315.html",
            "label": "The Powerpuff Girls",
            "section": "Brands",
        },
        "bags-scooby-doo": {
            "url": "https://us.shein.com/recommend/Scooby-Doo-Bags-sc-10050002316.html",
            "label": "Scooby-Doo",
            "section": "Brands",
        },
        "bags-harry-potter": {
            "url": "https://us.shein.com/recommend/Harry-Portter-Bags-sc-10050002317.html",
            "label": "Harry Potter",
            "section": "Brands",
        },
        "bags-looney-tunes": {
            "url": "https://us.shein.com/recommend/LOONEY-TUNES-Bags-sc-10050002318.html",
            "label": "Looney Tunes",
            "section": "Brands",
        },
    },
    "sports": {
        "sports": {
            "url": "https://us.shein.com/RecommendSelection/Sports-Outdoors-sc-017185553.html",
            "label": "Sports & Outdoors",
            "section": "Top category",
        },
        "sports-view-all": {
            "url": "https://us.shein.com/category/Activewear-sc-008646473.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "sports-new-in": {
            "url": "https://us.shein.com/new/New-In-Activewear-sc-00257290.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "sports-top-rated": {
            "url": "https://us.shein.com/hotsale/Activewear-Top-Rated-sc-00334060.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "sports-brands": {
            "url": "https://us.shein.com/trends/sports-brands-collection-sc-006216879.html",
            "label": "Brands",
            "section": "Shop by Category",
        },
        "sports-women-activewear": {
            "url": "https://us.shein.com/Women-Activewear-c-1894.html",
            "label": "Women Activewear",
            "section": "Shop by Category",
        },
        "sports-curve-activewear": {
            "url": "https://us.shein.com/Women-Plus-Activewear-c-2491.html",
            "label": "Curve Activewear",
            "section": "Shop by Category",
        },
        "sports-men-activewear": {
            "url": "https://us.shein.com/category/MEN-Sports-and-Outdoor-sc-008238503.html",
            "label": "Men Activewear",
            "section": "Shop by Category",
        },
        "sports-women-outdoor-apparel": {
            "url": "https://us.shein.com/Women-Outdoor-Apparel-c-5106.html",
            "label": "Women Outdoor Apparel",
            "section": "Shop by Category",
        },
        "sports-sports-outdoor-shoes": {
            "url": "https://us.shein.com/Sports-Outdoor-Shoes-c-8776.html",
            "label": "Sports & Outdoor Shoes",
            "section": "Shop by Category",
        },
        "sports-camping-hiking": {
            "url": "https://us.shein.com/category/Camping-and-Hiking-Equipment-and-Activewear-sc-008191729.html",
            "label": "Camping & Hiking",
            "section": "Shop by Activity",
        },
        "sports-fitness": {
            "url": "https://us.shein.com/Fitness-c-4331.html",
            "label": "Fitness",
            "section": "Shop by Activity",
        },
        "sports-swimming": {
            "url": "https://us.shein.com/trends/Water-Sports-sc-006216787.html",
            "label": "Swimming",
            "section": "Shop by Activity",
        },
        "sports-cycling": {
            "url": "https://us.shein.com/trends/Cycling-Apparel-and-Accessories-sc-006137552.html",
            "label": "Cycling",
            "section": "Shop by Activity",
        },
        "sports-gym-equipment": {
            "url": "https://us.shein.com/category/Gym-Equipment-sc-0082051769.html",
            "label": "Gym Equipment",
            "section": "Shop by Activity",
        },
        "sports-winter-sports": {
            "url": "https://us.shein.com/trends/Winter-Sports-sc-006238028.html",
            "label": "Winter Sports",
            "section": "Shop by Activity",
        },
        "sports-yoga": {
            "url": "https://us.shein.com/Yoga/Pilate-c-8520.html",
            "label": "Yoga",
            "section": "Shop by Activity",
        },
        "sports-team-sports": {
            "url": "https://us.shein.com/Team-Sports-c-4409.html",
            "label": "Team Sports",
            "section": "Shop by Activity",
        },
        "sports-fishing": {
            "url": "https://us.shein.com/trends/Fishing-sc-006137551.html",
            "label": "Fishing",
            "section": "Shop by Activity",
        },
        "sports-boxing-fighting-dance-gymnastics": {
            "url": "https://us.shein.com/Boxing-Fighting-Dance-Gymnastics-c-8975.html",
            "label": "Boxing Fighting & Dance Gymnastics",
            "section": "Shop by Activity",
        },
        "sports-sports-game": {
            "url": "https://us.shein.com/trends/Sports-Game-sc-006216780.html",
            "label": "Sports Game",
            "section": "Shop by Activity",
        },
        "sports-women-s-outdoor-athletic-shoes": {
            "url": "https://us.shein.com/Women-s-Outdoor-Athletic-Shoes-c-8603.html",
            "label": "Women's Outdoor Athletic Shoes",
            "section": "Shoes & Accessories",
        },
        "sports-men-s-outdoor-athletic-shoes": {
            "url": "https://us.shein.com/Men-s-Outdoor-Athletic-Shoes-c-8593.html",
            "label": "Men's Outdoor Athletic Shoes",
            "section": "Shoes & Accessories",
        },
        "sports-professional-sports-shoes": {
            "url": "https://us.shein.com/Professional-Sports-Shoes-c-6156.html",
            "label": "Professional Sports Shoes",
            "section": "Shoes & Accessories",
        },
        "sports-sports-accessories": {
            "url": "https://us.shein.com/Sports-Outdoor-Accessories-c-4329.html",
            "label": "Sports Accessories",
            "section": "Shoes & Accessories",
        },
        "sports-sports-safety-shaper": {
            "url": "https://us.shein.com/Sports-Shaper-Sports-Safety-c-5247.html",
            "label": "Sports Safety & Shaper",
            "section": "Shoes & Accessories",
        },
        "sports-sports-socks": {
            "url": "https://us.shein.com/Athletic-Socks-c-4330.html",
            "label": "Sports Socks",
            "section": "Shoes & Accessories",
        },
        "sports-sports-bags-bottle": {
            "url": "https://us.shein.com/category/Sports-Bags-and-Bottle-sc-008216893.html",
            "label": "Sports Bags & Bottle",
            "section": "Shoes & Accessories",
        },
        "sports-customized-accessories": {
            "url": "https://us.shein.com/recommend/Customized-Accessories-sc-1005190752.html",
            "label": "Customized Accessories",
            "section": "Shoes & Accessories",
        },
        "sports-active-tops": {
            "url": "https://us.shein.com/Women-Active-Tops-c-2181.html",
            "label": "Active Tops",
            "section": "Women Activewear",
        },
        "sports-active-sets": {
            "url": "https://us.shein.com/Women-Active-Sets-c-2183.html",
            "label": "Active Sets",
            "section": "Women Activewear",
        },
        "sports-active-bottoms": {
            "url": "https://us.shein.com/Women-Active-Bottoms-c-2182.html",
            "label": "Active Bottoms",
            "section": "Women Activewear",
        },
        "sports-sports-bras": {
            "url": "https://us.shein.com/Women-Sports-Bras-c-2184.html",
            "label": "Sports Bras",
            "section": "Women Activewear",
        },
        "sports-sports-shorts": {
            "url": "https://us.shein.com/Women-Sports-Shorts-c-2188.html",
            "label": "Sports Shorts",
            "section": "Women Activewear",
        },
        "sports-swimwear": {
            "url": "https://us.shein.com/recommend/Sport-Swim-sc-1005066451.html",
            "label": "Swimwear",
            "section": "Women Activewear",
        },
        "sports-sports-leggings-pants": {
            "url": "https://us.shein.com/category/Sports-Leggings-and-Pants-sc-008116362.html",
            "label": "Sports Leggings & Pants",
            "section": "Women Activewear",
        },
        "sports-sweatshirt": {
            "url": "https://us.shein.com/trends/hoodie-and-sweatshirt-sc-006216895.html",
            "label": "Sweatshirt",
            "section": "Women Activewear",
        },
        "sports-bodysuits-dresses": {
            "url": "https://us.shein.com/category/Sport-Bodysuits-and-Dresses-sc-0081667178.html",
            "label": "Bodysuits & Dresses",
            "section": "Women Activewear",
        },
        "sports-sports-jackets": {
            "url": "https://us.shein.com/Women-Sports-Jackets-c-2187.html",
            "label": "Sports Jackets",
            "section": "Women Activewear",
        },
        "sports-outdoor-clothing": {
            "url": "https://us.shein.com/category/Outdoor-Clothing-sc-008216762.html",
            "label": "Outdoor Clothing",
            "section": "Women Activewear",
        },
        "sports-active-tops-4240": {
            "url": "https://us.shein.com/Plus-Size-Sports-Tops-c-4240.html",
            "label": "Active Tops",
            "section": "Plus Activewear",
        },
        "sports-active-bottoms-4243": {
            "url": "https://us.shein.com/Plus-Size-Sports-Bottoms-c-4243.html",
            "label": "Active Bottoms",
            "section": "Plus Activewear",
        },
        "sports-active-sets-2494": {
            "url": "https://us.shein.com/Plus-Size-Sports-Sets-c-2494.html",
            "label": "Active Sets",
            "section": "Plus Activewear",
        },
        "sports-sports-bras-2357": {
            "url": "https://us.shein.com/Plus-Size-Sports-Bras-c-2357.html",
            "label": "Sports Bras",
            "section": "Plus Activewear",
        },
        "sports-bodysuits-jumpsuits": {
            "url": "https://us.shein.com/Plus-Size-Sports-Jumpsuits-c-4245.html",
            "label": "Bodysuits & Jumpsuits",
            "section": "Plus Activewear",
        },
        "sports-view-all-2443": {
            "url": "https://us.shein.com/Men-Activewear-c-2443.html",
            "label": "View All",
            "section": "Men Activewear",
        },
        "sports-active-tops-008238511": {
            "url": "https://us.shein.com/category/Men-Active-Tops-sc-008238511.html",
            "label": "Active Tops",
            "section": "Men Activewear",
        },
        "sports-active-bottoms-008238517": {
            "url": "https://us.shein.com/category/Men-Active-Bottoms-sc-008238517.html",
            "label": "Active Bottoms",
            "section": "Men Activewear",
        },
        "sports-glowmode": {
            "url": "https://us.shein.com/new/Glowmode-sc-002389085.html",
            "label": "GLOWMODE",
            "section": "Brands We Love",
        },
        "sports-nike": {
            "url": "https://us.shein.com/style/Nike-sc-0011579816.html",
            "label": "Nike",
            "section": "Brands We Love",
        },
        "sports-adidas": {
            "url": "https://us.shein.com/style/Adidas-sc-0011579878.html",
            "label": "Adidas",
            "section": "Brands We Love",
        },
        "sports-puma": {
            "url": "https://us.shein.com/style/Puma-sc-0011580557.html",
            "label": "Puma",
            "section": "Brands We Love",
        },
        "sports-new-balance": {
            "url": "https://us.shein.com/Brands/New-Balance-sc-014318642.html",
            "label": "New Balance",
            "section": "Brands We Love",
        },
        "sports-converse": {
            "url": "https://us.shein.com/recommend/Converse-Sport-sc-10050009070.html",
            "label": "Converse",
            "section": "Brands We Love",
        },
        "sports-timberland": {
            "url": "https://us.shein.com/recommend/Timberland-1020-sc-10050021347.html",
            "label": "Timberland",
            "section": "Brands We Love",
        },
        "sports-the-north-face": {
            "url": "https://us.shein.com/recommend/The-North-Face-1020-sc-10050021349.html",
            "label": "The North Face",
            "section": "Brands We Love",
        },
    },
    "home-textile": {
        "home-textile": {
            "url": "https://us.shein.com/RecommendSelection/Home-Textile-sc-017172972.html",
            "label": "Home Textiles",
            "section": "Top category",
        },
        "home-textile-view-all": {
            "url": "https://us.shein.com/Home-Textile-c-4083.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "home-textile-new-in": {
            "url": "https://us.shein.com/recommend/Home-Textile-New-in-sc-10050089395.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "home-textile-summer": {
            "url": "https://us.shein.com/recommend/Home-Textiles-Summer-sc-10050053607.html",
            "label": "Summer",
            "section": "Shop by Category",
        },
        "home-textile-bedding": {
            "url": "https://us.shein.com/Bedding-c-1942.html",
            "label": "Bedding",
            "section": "Shop by Category",
        },
        "home-textile-couch-sofa-decor": {
            "url": "https://us.shein.com/Couch-Sofa-Decor-c-3494.html",
            "label": "Couch & Sofa Decor",
            "section": "Shop by Category",
        },
        "home-textile-decorative-pillows-inserts-covers": {
            "url": "https://us.shein.com/Decorative-Pillows,-Inserts,-Covers-c-8359.html",
            "label": "Decorative Pillows, Inserts, & Covers",
            "section": "Shop by Category",
        },
        "home-textile-window-treatments": {
            "url": "https://us.shein.com/Window-Treatments-c-3446.html",
            "label": "Window Treatments",
            "section": "Shop by Category",
        },
        "home-textile-rugs-carpets": {
            "url": "https://us.shein.com/Rugs-Carpets-c-3490.html",
            "label": "Rugs & Carpets",
            "section": "Shop by Category",
        },
        "home-textile-blankets-throws": {
            "url": "https://us.shein.com/Blankets-Throws-c-8354.html",
            "label": "Blankets & Throws",
            "section": "Shop by Category",
        },
        "home-textile-kitchen-table-linens": {
            "url": "https://us.shein.com/Kitchen-Table-Linens-c-8360.html",
            "label": "Kitchen & Table Linens",
            "section": "Shop by Category",
        },
        "home-textile-wall-textile": {
            "url": "https://us.shein.com/Wall-Textile-c-9137.html",
            "label": "Wall Textile",
            "section": "Shop by Category",
        },
        "home-textile-pillows-positioners": {
            "url": "https://us.shein.com/Pillows-Positioners-c-6929.html",
            "label": "Pillows & Positioners",
            "section": "Shop by Category",
        },
        "home-textile-lumbar-pillow-chair-cushions": {
            "url": "https://us.shein.com/Lumbar-Pillow-Chair-Cushions-c-8911.html",
            "label": "Lumbar Pillow & Chair Cushions",
            "section": "Shop by Category",
        },
        "home-textile-towels-towel-sets": {
            "url": "https://us.shein.com/Towels-Towel-Sets-c-8387.html",
            "label": "Towels & Towel Sets",
            "section": "Shop by Category",
        },
        "home-textile-household-textile-sundries": {
            "url": "https://us.shein.com/Household-Textile-Sundries-c-8422.html",
            "label": "Household Textile Sundries",
            "section": "Shop by Category",
        },
        "home-textile-duvet-covers-sets": {
            "url": "https://us.shein.com/Duvet-Covers-Sets-c-1943.html",
            "label": "Duvet Covers Sets",
            "section": "Bedding",
        },
        "home-textile-fitted-sheets": {
            "url": "https://us.shein.com/Fitted-Sheets-c-3417.html",
            "label": "Fitted Sheets",
            "section": "Bedding",
        },
        "home-textile-sheet-sets-with-pillowcases": {
            "url": "https://us.shein.com/Sheet-Sets-with-Pillowcases-c-2307.html",
            "label": "Sheet Sets with Pillowcases",
            "section": "Bedding",
        },
        "home-textile-pillowcases-shams": {
            "url": "https://us.shein.com/Pillowcases-Shams-c-3426.html",
            "label": "Pillowcases & Shams",
            "section": "Bedding",
        },
        "home-textile-quilts": {
            "url": "https://us.shein.com/Quilts-c-3419.html",
            "label": "Quilts",
            "section": "Bedding",
        },
        "home-textile-duvet-covers": {
            "url": "https://us.shein.com/Duvet-Covers-c-2311.html",
            "label": "Duvet Covers",
            "section": "Bedding",
        },
        "home-textile-bed-skirts": {
            "url": "https://us.shein.com/Bed-Skirts-c-2315.html",
            "label": "Bed Skirts",
            "section": "Bedding",
        },
        "home-textile-mattress-pads": {
            "url": "https://us.shein.com/Mattress-Pads-c-4250.html",
            "label": "Mattress Pads",
            "section": "Bedding",
        },
        "home-textile-flat-sheets": {
            "url": "https://us.shein.com/Flat-Sheets-c-3425.html",
            "label": "Flat Sheets",
            "section": "Bedding",
        },
        "home-textile-mattress-protectors-encasements": {
            "url": "https://us.shein.com/Mattress-Protectors-Encasements-c-8436.html",
            "label": "Mattress Protectors & Encasements",
            "section": "Bedding",
        },
        "home-textile-sheet-fasteners-grippers": {
            "url": "https://us.shein.com/Sheet-Fasteners-Grippers-c-3424.html",
            "label": "Sheet Fasteners & Grippers",
            "section": "Bedding",
        },
        "home-textile-mosquito-net": {
            "url": "https://us.shein.com/Mosquito-Net-c-4090.html",
            "label": "Mosquito Net",
            "section": "Bedding",
        },
        "home-textile-comforters": {
            "url": "https://us.shein.com/Comforters-c-4246.html",
            "label": "Comforters",
            "section": "Bedding",
        },
        "home-textile-comforter-sets": {
            "url": "https://us.shein.com/Comforter-Sets-c-4247.html",
            "label": "Comforter Sets",
            "section": "Bedding",
        },
        "home-textile-duvets-down-comforters": {
            "url": "https://us.shein.com/Duvets-Down-Comforters-c-4248.html",
            "label": "Duvets & Down Comforters",
            "section": "Bedding",
        },
        "home-textile-sleeping-bags": {
            "url": "https://us.shein.com/Sleeping-Bags-c-8361.html",
            "label": "Sleeping Bags",
            "section": "Bedding",
        },
        "home-textile-quilt-sets": {
            "url": "https://us.shein.com/Quilt-Sets-c-8367.html",
            "label": "Quilt Sets",
            "section": "Bedding",
        },
        "home-textile-mattress-toppers": {
            "url": "https://us.shein.com/Mattress-Toppers-c-6933.html",
            "label": "Mattress Toppers",
            "section": "Bedding",
        },
        "home-textile-air-mattresses": {
            "url": "https://us.shein.com/Air-Mattresses-c-8363.html",
            "label": "Air Mattresses",
            "section": "Bedding",
        },
        "home-textile-bed-skirt-pins-clips": {
            "url": "https://us.shein.com/Bed-Skirt-Pins-Clips-c-8365.html",
            "label": "Bed Skirt Pins & Clips",
            "section": "Bedding",
        },
        "home-textile-electric-heating-pad": {
            "url": "https://us.shein.com/Electric-Heating-Pad-c-8362.html",
            "label": "Electric Heating Pad",
            "section": "Bedding",
        },
        "home-textile-dormitory-bedding": {
            "url": "https://us.shein.com/Dormitory-Bedding-c-13261.html",
            "label": "Dormitory Bedding",
            "section": "Bedding",
        },
        "home-textile-sofa-covers": {
            "url": "https://us.shein.com/Sofa-Covers-c-3495.html",
            "label": "Sofa Covers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-chair-covers": {
            "url": "https://us.shein.com/Chair-Covers-c-2175.html",
            "label": "Chair Covers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-recliner-slipcovers": {
            "url": "https://us.shein.com/Recliner-Slipcovers-c-8407.html",
            "label": "Recliner Slipcovers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-futon-slipcovers": {
            "url": "https://us.shein.com/Sofa-Covers-c-11782.html",
            "label": "Futon Slipcovers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-armrest-covers": {
            "url": "https://us.shein.com/Armrest-Covers-c-8412.html",
            "label": "Armrest Covers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-sofa-chair-leg-grippers": {
            "url": "https://us.shein.com/Sofa-Chair-Leg-Grippers-c-8416.html",
            "label": "Sofa & Chair Leg Grippers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-outdoor-sofas-covers": {
            "url": "https://us.shein.com/Outdoor-Sofas-Covers-c-8410.html",
            "label": "Outdoor Sofas Covers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-bean-bag-covers": {
            "url": "https://us.shein.com/Bean-Bag-Covers-c-13255.html",
            "label": "Bean Bag Covers",
            "section": "Couch & Sofa Decor",
        },
        "home-textile-cushion-cover": {
            "url": "https://us.shein.com/Cushion-Cover-c-1947.html",
            "label": "Cushion Cover",
            "section": "Decorative Pillows, Inserts, & Covers",
        },
        "home-textile-decorative-throw-pillows": {
            "url": "https://us.shein.com/Decorative-Throw-Pillows-c-4087.html",
            "label": "Decorative & Throw Pillows",
            "section": "Decorative Pillows, Inserts, & Covers",
        },
        "home-textile-customized-cushion-covers": {
            "url": "https://us.shein.com/Customized-Cushion-Covers-c-8755.html",
            "label": "Customized Cushion Covers",
            "section": "Decorative Pillows, Inserts, & Covers",
        },
        "home-textile-customized-decorative-pillows": {
            "url": "https://us.shein.com/Customized-Decorative-Pillows-c-9133.html",
            "label": "Customized Decorative Pillows",
            "section": "Decorative Pillows, Inserts, & Covers",
        },
        "home-textile-curtains": {
            "url": "https://us.shein.com/Curtains-c-2018.html",
            "label": "Curtains",
            "section": "Window Treatments",
        },
        "home-textile-sheer-panels": {
            "url": "https://us.shein.com/Sheer-Panels-c-3457.html",
            "label": "Sheer Panels",
            "section": "Window Treatments",
        },
        "home-textile-door-curtains": {
            "url": "https://us.shein.com/Door-Curtains-c-3453.html",
            "label": "Door Curtains",
            "section": "Window Treatments",
        },
        "home-textile-window-valance": {
            "url": "https://us.shein.com/Window-Valance-c-3459.html",
            "label": "Window Valance",
            "section": "Window Treatments",
        },
        "home-textile-window-screens": {
            "url": "https://us.shein.com/Window-Screens-c-4082.html",
            "label": "Window Screens",
            "section": "Window Treatments",
        },
        "home-textile-blackout-curtains-shades": {
            "url": "https://us.shein.com/Blackout-Curtains-Shades-c-8431.html",
            "label": "Blackout Curtains & Shades",
            "section": "Window Treatments",
        },
        "home-textile-window-stickers-films": {
            "url": "https://us.shein.com/Window-Stickers-Films-c-8435.html",
            "label": "Window Stickers & Films",
            "section": "Window Treatments",
        },
        "home-textile-kitchen-window-curtains": {
            "url": "https://us.shein.com/Kitchen-Window-Curtains-c-8432.html",
            "label": "Kitchen Window Curtains",
            "section": "Window Treatments",
        },
        "home-textile-shower-curtains": {
            "url": "https://us.shein.com/Shower-Curtains-c-8433.html",
            "label": "Shower Curtains",
            "section": "Window Treatments",
        },
        "home-textile-blinds-shades-shutters": {
            "url": "https://us.shein.com/Blinds,-Shades-Shutters-c-8434.html",
            "label": "Blinds, Shades & Shutters",
            "section": "Window Treatments",
        },
        "home-textile-curtain-tracks-accessories": {
            "url": "https://us.shein.com/Curtain-Tracks-Accessories-c-8983.html",
            "label": "Curtain Tracks & Accessories",
            "section": "Window Treatments",
        },
        "home-textile-area-rugs-sets": {
            "url": "https://us.shein.com/Area-Rugs-Sets-c-3493.html",
            "label": "Area Rugs & Sets",
            "section": "Rugs & Carpets",
        },
        "home-textile-kitchen-mats-rugs": {
            "url": "https://us.shein.com/Kitchen-Mats-Rugs-c-8401.html",
            "label": "Kitchen Mats & Rugs",
            "section": "Rugs & Carpets",
        },
        "home-textile-door-mats": {
            "url": "https://us.shein.com/Door-Mats-c-1956.html",
            "label": "Door Mats",
            "section": "Rugs & Carpets",
        },
        "home-textile-kids-floor-mats": {
            "url": "https://us.shein.com/Kids-Floor-Mats-c-8402.html",
            "label": "Kids Floor Mats",
            "section": "Rugs & Carpets",
        },
        "home-textile-interlocking-floor-mats": {
            "url": "https://us.shein.com/Interlocking-Floor-Mats-c-8403.html",
            "label": "Interlocking Floor Mats",
            "section": "Rugs & Carpets",
        },
        "home-textile-bathroom-laundry-mats": {
            "url": "https://us.shein.com/Bathroom-Laundry-Mats-c-8399.html",
            "label": "Bathroom & Laundry Mats",
            "section": "Rugs & Carpets",
        },
        "home-textile-runner-rugs": {
            "url": "https://us.shein.com/Runner-Rugs-c-8400.html",
            "label": "Runner Rugs",
            "section": "Rugs & Carpets",
        },
        "home-textile-carpet-padding-grippers": {
            "url": "https://us.shein.com/Carpet-Padding-Grippers-c-8406.html",
            "label": "Carpet Padding & Grippers",
            "section": "Rugs & Carpets",
        },
        "home-textile-exercise-mats": {
            "url": "https://us.shein.com/Exercise-Mats-c-8404.html",
            "label": "Exercise Mats",
            "section": "Rugs & Carpets",
        },
        "home-textile-blankets": {
            "url": "https://us.shein.com/Blankets-c-2305.html",
            "label": "Blankets",
            "section": "Blankets & Throws",
        },
        "home-textile-throws": {
            "url": "https://us.shein.com/Throws-c-3421.html",
            "label": "Throws",
            "section": "Blankets & Throws",
        },
        "home-textile-wearable-blankets": {
            "url": "https://us.shein.com/Wearable-Blankets-c-4249.html",
            "label": "Wearable Blankets",
            "section": "Blankets & Throws",
        },
        "home-textile-weighted-blankets": {
            "url": "https://us.shein.com/Weighted-Blankets-c-8369.html",
            "label": "Weighted Blankets",
            "section": "Blankets & Throws",
        },
        "home-textile-tablecloths": {
            "url": "https://us.shein.com/Tablecloths-c-1952.html",
            "label": "Tablecloths",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-table-runners": {
            "url": "https://us.shein.com/Table-Runners-c-3588.html",
            "label": "Table Runners",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-table-napkins": {
            "url": "https://us.shein.com/Table-Napkins-c-3583.html",
            "label": "Table Napkins",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-tabletop-mat": {
            "url": "https://us.shein.com/Tabletop-Mat-c-8413.html",
            "label": "Tabletop Mat",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-oven-grilling-mitts": {
            "url": "https://us.shein.com/Potholders-Oven-Mitts-c-8419.html",
            "label": "Oven & Grilling Mitts",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-potholders": {
            "url": "https://us.shein.com/Potholders-c-8419.html",
            "label": "Potholders",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-place-mats": {
            "url": "https://us.shein.com/Place-Mats-c-8414.html",
            "label": "Place Mats",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-aprons": {
            "url": "https://us.shein.com/Aprons-c-8417.html",
            "label": "Aprons",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-dish-cloths-dish-towels": {
            "url": "https://us.shein.com/Dish-Cloths-Dish-Towels-c-8418.html",
            "label": "Dish Cloths & Dish Towels",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-food-tent": {
            "url": "https://us.shein.com/Food-Tent-c-8421.html",
            "label": "Food Tent",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-customized-aprons": {
            "url": "https://us.shein.com/Customized-Aprons-c-9141.html",
            "label": "Customized Aprons",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-customized-place-mat": {
            "url": "https://us.shein.com/Customized-Place-Mat-c-9143.html",
            "label": "Customized Place Mat",
            "section": "Kitchen & Table Linens",
        },
        "home-textile-tapestry": {
            "url": "https://us.shein.com/Tapestry-c-2301.html",
            "label": "Tapestry",
            "section": "Wall Textile",
        },
        "home-textile-wall-hanging": {
            "url": "https://us.shein.com/Wall-Hanging-c-9560.html",
            "label": "Wall Hanging",
            "section": "Wall Textile",
        },
        "home-textile-bed-pillows": {
            "url": "https://us.shein.com/Bed-Pillows-c-4089.html",
            "label": "Bed Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-travel-pillows": {
            "url": "https://us.shein.com/Travel-Pillows-c-4088.html",
            "label": "Travel Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-neck-cervical-pillows": {
            "url": "https://us.shein.com/Neck-Cervical-Pillows-c-8379.html",
            "label": "Neck & Cervical Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-body-pillows": {
            "url": "https://us.shein.com/Body-Pillows-c-6931.html",
            "label": "Body Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-maternity-pillows": {
            "url": "https://us.shein.com/Maternity-Pillows-c-8375.html",
            "label": "Maternity Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-reading-bed-rest-pillows": {
            "url": "https://us.shein.com/Reading-Bed-Rest-Pillows-c-8372.html",
            "label": "Reading & Bed Rest Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-massage-pillows": {
            "url": "https://us.shein.com/Massage-Pillows-c-6930.html",
            "label": "Massage Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-other-function-pillows-positioners": {
            "url": "https://us.shein.com/Other-Function-Pillows-Positioners-c-8380.html",
            "label": "Other Function Pillows & Positioners",
            "section": "Pillows & Positioners",
        },
        "home-textile-bed-wedges-body-positioners": {
            "url": "https://us.shein.com/Bed-Wedges-Body-Positioners-c-8378.html",
            "label": "Bed Wedges & Body Positioners",
            "section": "Pillows & Positioners",
        },
        "home-textile-nap-pillows": {
            "url": "https://us.shein.com/Nap-Pillows-c-8382.html",
            "label": "Nap Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-leg-positioner-pillows": {
            "url": "https://us.shein.com/Leg-Positioner-Pillows-c-8377.html",
            "label": "Leg Positioner Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-latex-pillows": {
            "url": "https://us.shein.com/Latex-Pillows-c-8383.html",
            "label": "Latex Pillows",
            "section": "Pillows & Positioners",
        },
        "home-textile-chair-pads": {
            "url": "https://us.shein.com/Chair-Pads-c-5068.html",
            "label": "Chair Pads",
            "section": "Lumbar Pillow & Chair Cushions",
        },
        "home-textile-lumbar-pillows-seat-cushions": {
            "url": "https://us.shein.com/Lumbar-Pillows-Seat-Cushions-c-8373.html",
            "label": "Lumbar Pillows & Seat Cushions",
            "section": "Lumbar Pillow & Chair Cushions",
        },
        "home-textile-outdoor-pillows-cushions": {
            "url": "https://us.shein.com/Outdoor-Pillows-Cushions-c-8376.html",
            "label": "Outdoor Pillows & Cushions",
            "section": "Lumbar Pillow & Chair Cushions",
        },
        "home-textile-bath-towels": {
            "url": "https://us.shein.com/Bath-Towels-c-8389.html",
            "label": "Bath Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-compressed-towels": {
            "url": "https://us.shein.com/Bath-Towel-Sets-c-8388.html",
            "label": "Compressed Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-kitchen-towels": {
            "url": "https://us.shein.com/Kitchen-Towels-c-8394.html",
            "label": "Kitchen Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-hand-towels": {
            "url": "https://us.shein.com/Hand-Towels-c-8396.html",
            "label": "Hand Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-towels": {
            "url": "https://us.shein.com/Towels-c-8391.html",
            "label": "Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-kids-bath-towels": {
            "url": "https://us.shein.com/Kids-Bath-Towels-c-8392.html",
            "label": "Kids Bath Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-beach-towels-bath-sheets": {
            "url": "https://us.shein.com/Beach-Towels-Bath-sheets-c-8390.html",
            "label": "Beach Towels & Bath Sheets",
            "section": "Towels & Towel Sets",
        },
        "home-textile-quick-dry-towels-cooling-towels": {
            "url": "https://us.shein.com/Quick-Dry-Towels-Cooling-Towels-c-8398.html",
            "label": "Quick Dry Towels & Cooling Towels",
            "section": "Towels & Towel Sets",
        },
        "home-textile-washcloths-bath-sponges": {
            "url": "https://us.shein.com/Washcloths-Bath-Sponges-c-8393.html",
            "label": "Washcloths & Bath Sponges",
            "section": "Towels & Towel Sets",
        },
        "home-textile-hair-drying-cap": {
            "url": "https://us.shein.com/Hair-Drying-Cap-c-13260.html",
            "label": "Hair Drying Cap",
            "section": "Towels & Towel Sets",
        },
        "home-textile-oversleeves": {
            "url": "https://us.shein.com/Oversleeves-c-8428.html",
            "label": "Oversleeves",
            "section": "Household Textile Sundries",
        },
        "home-textile-winter-thermal-cover": {
            "url": "https://us.shein.com/Winter-Thermal-Cover-c-8424.html",
            "label": "Winter Thermal Cover",
            "section": "Household Textile Sundries",
        },
        "home-textile-eyemasks-earmuffs": {
            "url": "https://us.shein.com/Eyemasks-Earmuffs-c-8429.html",
            "label": "Eyemasks & Earmuffs",
            "section": "Household Textile Sundries",
        },
        "home-textile-hand-foot-warmers": {
            "url": "https://us.shein.com/Hand-Foot-Warmers-c-8430.html",
            "label": "Hand & Foot Warmers",
            "section": "Household Textile Sundries",
        },
        "home-textile-dustproof-cover": {
            "url": "https://us.shein.com/Dustproof-Cover-c-8423.html",
            "label": "Dustproof Cover",
            "section": "Household Textile Sundries",
        },
        "home-textile-windproof-quilts": {
            "url": "https://us.shein.com/Windproof-Quilts-c-8425.html",
            "label": "Windproof Quilts",
            "section": "Household Textile Sundries",
        },
        "home-textile-shade-cloth": {
            "url": "https://us.shein.com/Shade-Cloth-c-8427.html",
            "label": "Shade Cloth",
            "section": "Household Textile Sundries",
        },
        "home-textile-tarps-tie-downs": {
            "url": "https://us.shein.com/Tarps-Tie-Downs-c-8426.html",
            "label": "Tarps & Tie-downs",
            "section": "Household Textile Sundries",
        },
        "home-textile-fabric-storage": {
            "url": "https://us.shein.com/Fabric-Storage-c-13263.html",
            "label": "Fabric Storage",
            "section": "Household Textile Sundries",
        },
        "home-textile-house-slippers": {
            "url": "https://us.shein.com/House-Slippers-c-13254.html",
            "label": "House Slippers",
            "section": "Household Textile Sundries",
        },
        "home-textile-madison-park": {
            "url": "https://us.shein.com/Brands/madison-park-sc-014225431.html",
            "label": "Madison Park",
            "section": "Brands We Love",
        },
        "home-textile-intelligent-design": {
            "url": "https://us.shein.com/Brands/Intelligent-Design-sc-014225487.html",
            "label": "Intelligent Design",
            "section": "Brands We Love",
        },
    },
    "cell-phones-accessories": {
        "cell-phones-accessories": {
            "url": "https://us.shein.com/RecommendSelection/Cell-Phones-Accessories-sc-017706910.html",
            "label": "Cell Phones & Accessories",
            "section": "Top category",
        },
        "cell-phones-accessories-view-all": {
            "url": "https://us.shein.com/Cell-Phones-Accessories-c-2274.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-new-in": {
            "url": "https://us.shein.com/recommend/New-In-sc-10050010272.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-top-rated": {
            "url": "https://us.shein.com/recommend/Top-Rated-sc-10050010271.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-phone-cases": {
            "url": "https://us.shein.com/Phone-Cases-c-8953.html",
            "label": "Phone Cases",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-cellphones": {
            "url": "https://us.shein.com/Cellphones-c-4703.html",
            "label": "Cellphones",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-cases": {
            "url": "https://us.shein.com/Cases-c-3340.html",
            "label": "Cases",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-screen-protectors": {
            "url": "https://us.shein.com/Screen-Protectors-c-3648.html",
            "label": "Screen Protectors",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-phone-accessories": {
            "url": "https://us.shein.com/Phone-Accessories-c-3649.html",
            "label": "Phone Accessories",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-chargers": {
            "url": "https://us.shein.com/Chargers-c-3325.html",
            "label": "Chargers",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-phone-mounts-holders": {
            "url": "https://us.shein.com/Phone-Mounts-Holders-c-3319.html",
            "label": "Phone Mounts & Holders",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-cable-cable-accessories": {
            "url": "https://us.shein.com/Cable-Cable-Accessories-c-3332.html",
            "label": "Cable & Cable Accessories",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-cell-phone-photo-accessories": {
            "url": "https://us.shein.com/Cell-Phone-Photo-Accessories-c-3327.html",
            "label": "Cell Phone Photo & " "Accessories",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-customized-cell-phones-accessories": {
            "url": "https://us.shein.com/recommend/Customized-Cell-Phones-Accs-sc-10050010293.html",
            "label": "Customized Cell " "Phones & " "Accessories",
            "section": "Shop by " "Category",
        },
        "cell-phones-accessories-top-picks": {
            "url": "https://us.shein.com/Top-Picks-sc-10050114909.html",
            "label": "Top Picks",
            "section": "Shop by Category",
        },
        "cell-phones-accessories-fashion-phone-cases": {
            "url": "https://us.shein.com/Fashion-Phone-Cases-c-1925.html",
            "label": "Fashion Phone Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-basic-phone-cases": {
            "url": "https://us.shein.com/Basic-Phone-Cases-c-13520.html",
            "label": "Basic Phone Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-other-phone-cases": {
            "url": "https://us.shein.com/recommend/Other-Phone-Cases-sc-10050010291.html",
            "label": "Other Phone Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-earphone-cases": {
            "url": "https://us.shein.com/Earphone-Cases-c-8958.html",
            "label": "Earphone Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-pad-cases": {
            "url": "https://us.shein.com/Pad-Cases-c-8962.html",
            "label": "Pad Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-smartwatch-cases-watch-strap": {
            "url": "https://us.shein.com/Smartwatch-Cases-Watch-Strap-c-12724.html",
            "label": "Smartwatch Cases & " "Watch Strap",
            "section": "Cases",
        },
        "cell-phones-accessories-other-cases": {
            "url": "https://us.shein.com/recommend/Other-Cases-sc-10050010297.html",
            "label": "Other Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-customized-cases": {
            "url": "https://us.shein.com/recommend/Customized-Cases-sc-10050010880.html",
            "label": "Customized Cases",
            "section": "Cases",
        },
        "cell-phones-accessories-phone-screen-protectors": {
            "url": "https://us.shein.com/Phone-Screen-Protectors-c-2289.html",
            "label": "Phone Screen Protectors",
            "section": "Screen Protectors",
        },
        "cell-phones-accessories-lens-protectors": {
            "url": "https://us.shein.com/Lens-Protectors-c-3710.html",
            "label": "Lens Protectors",
            "section": "Screen Protectors",
        },
        "cell-phones-accessories-pad-screen-protectors": {
            "url": "https://us.shein.com/Pad-Screen-Protectors-c-3712.html",
            "label": "Pad Screen Protectors",
            "section": "Screen Protectors",
        },
        "cell-phones-accessories-watch-screen-protectors": {
            "url": "https://us.shein.com/Watch-Screen-Protectors-c-3713.html",
            "label": "Watch Screen Protectors",
            "section": "Screen Protectors",
        },
        "cell-phones-accessories-cell-phone-lanyards": {
            "url": "https://us.shein.com/Cell-Phone-Lanyards-c-3335.html",
            "label": "Cell Phone Lanyards",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-stylus-pen-accessories": {
            "url": "https://us.shein.com/Stylus-Pen-Accessories-c-12721.html",
            "label": "Stylus Pen & Accessories",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-cell-phone-waterproof-bags": {
            "url": "https://us.shein.com/Cell-Phone-Waterproof-Bags-c-3334.html",
            "label": "Cell Phone Waterproof " "Bags",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-charger-cable-adapters": {
            "url": "https://us.shein.com/Charger-Cable-Adapters-c-3331.html",
            "label": "Charger Cable Adapters",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-maintenance-upkeep-repairs": {
            "url": "https://us.shein.com/Maintenance,-Upkeep-Repairs-c-8967.html",
            "label": "Maintenance, Upkeep & " "Repairs",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-cell-phone-replacement-parts": {
            "url": "https://us.shein.com/Cell-Phone-Replacement-Parts-c-4690.html",
            "label": "Cell Phone Replacement " "Parts",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-adhesive-cardholders": {
            "url": "https://us.shein.com/Adhesive-Cardholders-c-3704.html",
            "label": "Adhesive Cardholders",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-mobile-game-auxiliary-accessories": {
            "url": "https://us.shein.com/Mobile-Game-Auxiliary-Accessories-c-12722.html",
            "label": "Mobile Game " "Auxiliary " "Accessories",
            "section": "Phone " "Accessories",
        },
        "cell-phones-accessories-phone-fan": {
            "url": "https://us.shein.com/Phone-Fan-c-3695.html",
            "label": "Phone Fan",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-phone-cooler": {
            "url": "https://us.shein.com/Phone-Cooler-c-12760.html",
            "label": "Phone Cooler",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-wireless-display-receiver": {
            "url": "https://us.shein.com/Wireless-Display-Receiver-c-12754.html",
            "label": "Wireless Display Receiver",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-cell-phone-armbands": {
            "url": "https://us.shein.com/Cell-Phone-Armbands-c-2277.html",
            "label": "Cell Phone Armbands",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-phone-separation-alert-device": {
            "url": "https://us.shein.com/Phone-Separation-Alert-Device-c-12756.html",
            "label": "Phone Separation " "Alert Device",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-phone-belt-bag": {
            "url": "https://us.shein.com/Phone-Belt-Bag-c-12761.html",
            "label": "Phone Belt Bag",
            "section": "Phone Accessories",
        },
        "cell-phones-accessories-power-bank": {
            "url": "https://us.shein.com/Power-Bank-c-9779.html",
            "label": "Power Bank",
            "section": "Chargers",
        },
        "cell-phones-accessories-wall-charger": {
            "url": "https://us.shein.com/Wall-Charger-c-3326.html",
            "label": "Wall Charger",
            "section": "Chargers",
        },
        "cell-phones-accessories-wireless-charger": {
            "url": "https://us.shein.com/Wireless-Charger-c-2276.html",
            "label": "Wireless Charger",
            "section": "Chargers",
        },
        "cell-phones-accessories-cell-phones-car-charger": {
            "url": "https://us.shein.com/Cell-Phones-Car-Charger-c-9781.html",
            "label": "Cell Phones Car Charger",
            "section": "Chargers",
        },
        "cell-phones-accessories-charging-station": {
            "url": "https://us.shein.com/Charging-Station-c-3322.html",
            "label": "Charging Station",
            "section": "Chargers",
        },
        "cell-phones-accessories-cell-phones-solar-panels": {
            "url": "https://us.shein.com/Cell-Phones-Solar-Panels-c-9780.html",
            "label": "Cell Phones Solar Panels",
            "section": "Chargers",
        },
        "cell-phones-accessories-phone-holders": {
            "url": "https://us.shein.com/Phone-Holders-c-2278.html",
            "label": "Phone Holders",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-automobile-phone-cradles": {
            "url": "https://us.shein.com/Automobile-Phone-Cradles-c-8969.html",
            "label": "Automobile Phone Cradles",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-phone-grip-holder": {
            "url": "https://us.shein.com/Phone-Grip-Holder-c-3323.html",
            "label": "Phone Grip Holder",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-phone-rings": {
            "url": "https://us.shein.com/Phone-Rings-c-3320.html",
            "label": "Phone Rings",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-gooseneck-phone-mount": {
            "url": "https://us.shein.com/Gooseneck-Phone-Mount-c-3324.html",
            "label": "Gooseneck Phone Mount",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-cell-phone-handlebar-mounts": {
            "url": "https://us.shein.com/Cell-Phone-Handlebar-Mounts-c-8970.html",
            "label": "Cell Phone Handlebar " "Mounts",
            "section": "Phone Mounts & " "Holders",
        },
        "cell-phones-accessories-headphone-stands": {
            "url": "https://us.shein.com/Headphone-Stands-c-8971.html",
            "label": "Headphone Stands",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-screen-expanders-magnifiers": {
            "url": "https://us.shein.com/Screen-Expanders-Magnifiers-c-3714.html",
            "label": "Screen Expanders & " "Magnifiers",
            "section": "Phone Mounts & " "Holders",
        },
        "cell-phones-accessories-customized-phone-holder": {
            "url": "https://us.shein.com/Customized-Phone-Holder-c-10149.html",
            "label": "Customized Phone Holder",
            "section": "Phone Mounts & Holders",
        },
        "cell-phones-accessories-cables": {
            "url": "https://us.shein.com/Cables-c-2281.html",
            "label": "Cables",
            "section": "Cable & Cable Accessories",
        },
        "cell-phones-accessories-cable-protectors": {
            "url": "https://us.shein.com/Cable-Protectors-c-8965.html",
            "label": "Cable Protectors",
            "section": "Cable & Cable Accessories",
        },
        "cell-phones-accessories-cable-storage": {
            "url": "https://us.shein.com/Cable-Storage-c-3333.html",
            "label": "Cable Storage",
            "section": "Cable & Cable Accessories",
        },
        "cell-phones-accessories-phone-external-flashes-selfie-lights": {
            "url": "https://us.shein.com/Phone-External-Flashes-Selfie-Lights-c-3328.html",
            "label": "Phone External " "Flashes & " "Selfie Lights",
            "section": "Cell Phone " "Photo & " "Accessories",
        },
        "cell-phones-accessories-selfiestick-tripod-head": {
            "url": "https://us.shein.com/Selfiestick-Tripod-Head-c-2489.html",
            "label": "Selfiestick & Tripod Head",
            "section": "Cell Phone Photo & " "Accessories",
        },
        "cell-phones-accessories-phone-lens": {
            "url": "https://us.shein.com/Phone-Lens-c-2490.html",
            "label": "Phone Lens",
            "section": "Cell Phone Photo & Accessories",
        },
        "cell-phones-accessories-live-streaming-equipment-accessories": {
            "url": "https://us.shein.com/Live-Streaming-Equipment-Accessories-c-12758.html",
            "label": "Live Streaming " "Equipment & " "Accessories",
            "section": "Cell Phone " "Photo & " "Accessories",
        },
        "cell-phones-accessories-wireless-camera-shutter": {
            "url": "https://us.shein.com/Wireless-Camera-Shutter-c-12759.html",
            "label": "Wireless Camera Shutter",
            "section": "Cell Phone Photo & " "Accessories",
        },
        "cell-phones-accessories-handheld-gimbals-stabilizers": {
            "url": "https://us.shein.com/Handheld-Gimbals-Stabilizers-c-9782.html",
            "label": "Handheld Gimbals & " "Stabilizers",
            "section": "Cell Phone Photo & " "Accessories",
        },
        "cell-phones-accessories-reflector": {
            "url": "https://us.shein.com/Reflector-c-12753.html",
            "label": "Reflector",
            "section": "Cell Phone Photo & Accessories",
        },
        "cell-phones-accessories-view-all-10050010284": {
            "url": "https://us.shein.com/recommend/View-all-sc-10050010284.html",
            "label": "View All",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-apple": {
            "url": "https://us.shein.com/recommend/Apple-sc-10050095469.html",
            "label": "Apple",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-samsung": {
            "url": "https://us.shein.com/recommend/Samsung-sc-10050095470.html",
            "label": "Samsung",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-xiaomi": {
            "url": "https://us.shein.com/recommend/Xiaomi-sc-10050095472.html",
            "label": "Xiaomi",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-realme": {
            "url": "https://us.shein.com/recommend/Realme-sc-10050095474.html",
            "label": "Realme",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-huawei": {
            "url": "https://us.shein.com/recommend/Huawei-sc-10050095475.html",
            "label": "Huawei",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-oppo": {
            "url": "https://us.shein.com/recommend/OPPO-sc-10050095476.html",
            "label": "OPPO",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-vivo": {
            "url": "https://us.shein.com/recommend/vivo-sc-10050095478.html",
            "label": "vivo",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-miniso": {
            "url": "https://us.shein.com/recommend/Miniso-sc-10050095480.html",
            "label": "Miniso",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-anker": {
            "url": "https://us.shein.com/recommend/anker-sc-10050095481.html",
            "label": "anker",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-ugreen": {
            "url": "https://us.shein.com/recommend/UGREEN-sc-10050095482.html",
            "label": "UGREEN",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-remax": {
            "url": "https://us.shein.com/recommend/REMAX-sc-10050095483.html",
            "label": "REMAX",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-giippa": {
            "url": "https://us.shein.com/recommend/GIIPPA-sc-10050095484.html",
            "label": "GIIPPA",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-koolife": {
            "url": "https://us.shein.com/recommend/KOOLIFE-sc-10050095485.html",
            "label": "KOOLIFE",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-danycase": {
            "url": "https://us.shein.com/recommend/DANYCASE-sc-10050095486.html",
            "label": "DANYCASE",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-servo": {
            "url": "https://us.shein.com/recommend/SERVO-sc-10050095487.html",
            "label": "SERVO",
            "section": "Brands We Love",
        },
        "cell-phones-accessories-oukitel": {
            "url": "https://us.shein.com/recommend/OUKITEL-sc-10050095488.html",
            "label": "OUKITEL",
            "section": "Brands We Love",
        },
    },
    "electronics": {
        "electronics": {
            "url": "https://us.shein.com/RecommendSelection/Electronics-sc-017706908.html",
            "label": "Electronics",
            "section": "Top category",
        },
        "electronics-view-all": {
            "url": "https://us.shein.com/RecommendSelection/Electronics-sc-017172971.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "electronics-new-in": {
            "url": "https://us.shein.com/new/New-In-sc-002264296.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "electronics-top-rated": {
            "url": "https://us.shein.com/recommend/Top-Rated-sc-10050004992.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "electronics-computer-office": {
            "url": "https://us.shein.com/Computer-Office-c-2275.html",
            "label": "Computer & Office",
            "section": "Shop by Category",
        },
        "electronics-consumer-electronic": {
            "url": "https://us.shein.com/Consumer-Electronic-c-4671.html",
            "label": "Consumer Electronic",
            "section": "Shop by Category",
        },
        "electronics-wearable-devices": {
            "url": "https://us.shein.com/Wearable-Devices-c-3337.html",
            "label": "Wearable Devices",
            "section": "Shop by Category",
        },
        "electronics-automotive": {
            "url": "https://us.shein.com/Automotive-c-3657.html",
            "label": "Automotive",
            "section": "Shop by Category",
        },
        "electronics-speaker": {
            "url": "https://us.shein.com/Speaker-c-2487.html",
            "label": "Speaker",
            "section": "Shop by Category",
        },
        "electronics-wireless-earbuds": {
            "url": "https://us.shein.com/Wireless-Earbuds-c-3306.html",
            "label": "Wireless Earbuds",
            "section": "Shop by Category",
        },
        "electronics-headset": {
            "url": "https://us.shein.com/Headset-c-3305.html",
            "label": "Headset",
            "section": "Shop by Category",
        },
        "electronics-memory-cards": {
            "url": "https://us.shein.com/Memory-Cards-c-3724.html",
            "label": "Memory Cards",
            "section": "Shop by Category",
        },
        "electronics-security-cameras": {
            "url": "https://us.shein.com/Security-Cameras-c-4724.html",
            "label": "Security Cameras",
            "section": "Shop by Category",
        },
        "electronics-laptop-bags-cases": {
            "url": "https://us.shein.com/Laptop-Bags-Cases-c-3317.html",
            "label": "Laptop Bags & Cases",
            "section": "Shop by Category",
        },
        "electronics-top-value": {
            "url": "https://us.shein.com/Top-Value-sc-10050114910.html",
            "label": "Top Value",
            "section": "Shop by Category",
        },
        "electronics-camera-photo": {
            "url": "https://us.shein.com/Camera-Photo-c-4682.html",
            "label": "Camera & Photo",
            "section": "Consumer Electronic",
        },
        "electronics-home-audio-video": {
            "url": "https://us.shein.com/Home-Audio-Video-c-4677.html",
            "label": "Home Audio & Video",
            "section": "Consumer Electronic",
        },
        "electronics-headphone-earphone": {
            "url": "https://us.shein.com/Headphone-Earphone-c-3303.html",
            "label": "Headphone & Earphone",
            "section": "Consumer Electronic",
        },
        "electronics-portable-audio-video": {
            "url": "https://us.shein.com/Portable-Audio-Video-c-4675.html",
            "label": "Portable Audio & Video",
            "section": "Consumer Electronic",
        },
        "electronics-game-consoles-accessories": {
            "url": "https://us.shein.com/Games-c-3777.html",
            "label": "Game Consoles & Accessories",
            "section": "Consumer Electronic",
        },
        "electronics-smart-electronics": {
            "url": "https://us.shein.com/Smart-Electronics-c-4683.html",
            "label": "Smart Electronics",
            "section": "Consumer Electronic",
        },
        "electronics-walkie-talkie-accessories": {
            "url": "https://us.shein.com/Walkie-Talkie-Accessories-c-8482.html",
            "label": "Walkie Talkie & Accessories",
            "section": "Consumer Electronic",
        },
        "electronics-accessories-parts": {
            "url": "https://us.shein.com/Accessories-Parts-c-9702.html",
            "label": "Accessories & Parts",
            "section": "Consumer Electronic",
        },
        "electronics-smart-watches": {
            "url": "https://us.shein.com/Smart-Watches-c-3338.html",
            "label": "Smart Watches",
            "section": "Smart Watches & Accs",
        },
        "electronics-smart-glasses": {
            "url": "https://us.shein.com/Smart-Glasses-c-13463.html",
            "label": "Smart Glasses",
            "section": "Smart Watches & Accs",
        },
        "electronics-smart-band": {
            "url": "https://us.shein.com/Smart-Band-c-13466.html",
            "label": "Smart Band",
            "section": "Smart Watches & Accs",
        },
        "electronics-keyboards-mouses": {
            "url": "https://us.shein.com/Keyboards-Mouses-c-3310.html",
            "label": "Keyboards & Mouses",
            "section": "Computer & Office",
        },
        "electronics-office-electronics": {
            "url": "https://us.shein.com/Office-Electronics-c-4706.html",
            "label": "Office Electronics",
            "section": "Computer & Office",
        },
        "electronics-storage-devices": {
            "url": "https://us.shein.com/Storage-Devices-c-3646.html",
            "label": "Storage Devices",
            "section": "Computer & Office",
        },
        "electronics-computer-components": {
            "url": "https://us.shein.com/Computer-Components-c-4726.html",
            "label": "Computer Components",
            "section": "Computer & Office",
        },
        "electronics-tablets-pc": {
            "url": "https://us.shein.com/Tablets-PC-c-4741.html",
            "label": "Tablets PC",
            "section": "Computer & Office",
        },
        "electronics-mouse-pads-wrist-rests": {
            "url": "https://us.shein.com/Mouse-Pads-Wrist-Rests-c-3308.html",
            "label": "Mouse Pads & Wrist Rests",
            "section": "Computer & Office",
        },
        "electronics-computer-peripherals": {
            "url": "https://us.shein.com/Computer-Peripherals-c-4733.html",
            "label": "Computer Peripherals",
            "section": "Computer & Office",
        },
        "electronics-computer-accessories": {
            "url": "https://us.shein.com/Computer-Accessories-c-3647.html",
            "label": "Computer Accessories",
            "section": "Computer & Office",
        },
        "electronics-laptops": {
            "url": "https://us.shein.com/Laptops-c-7828.html",
            "label": "Laptops",
            "section": "Computer & Office",
        },
        "electronics-pc-stands-fan": {
            "url": "https://us.shein.com/PC-Stands-Fan-c-3315.html",
            "label": "PC Stands & Fan",
            "section": "Computer & Office",
        },
        "electronics-monitors": {
            "url": "https://us.shein.com/Monitors-c-6964.html",
            "label": "Monitors",
            "section": "Computer & Office",
        },
        "electronics-kids-tablets": {
            "url": "https://us.shein.com/Kids-Tablets-c-7830.html",
            "label": "Kids Tablets",
            "section": "Computer & Office",
        },
        "electronics-desktop-pcs": {
            "url": "https://us.shein.com/Desktop-PCs-c-8952.html",
            "label": "Desktop PCs",
            "section": "Computer & Office",
        },
        "electronics-networking": {
            "url": "https://us.shein.com/Networking-c-4716.html",
            "label": "Networking",
            "section": "Computer & Office",
        },
        "electronics-lenovo": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095213.html",
            "label": "Lenovo",
            "section": "Shop by Brands",
        },
        "electronics-apple": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095217.html",
            "label": "Apple",
            "section": "Shop by Brands",
        },
        "electronics-jbl": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095219.html",
            "label": "JBL",
            "section": "Shop by Brands",
        },
        "electronics-hp": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095221.html",
            "label": "HP",
            "section": "Shop by Brands",
        },
        "electronics-attack-shark": {
            "url": "https://us.shein.com/StoreSelection/Brand-Collections-sc-16050095222.html",
            "label": "ATTACK SHARK",
            "section": "Shop by Brands",
        },
        "electronics-playstation": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095223.html",
            "label": "PlayStation",
            "section": "Shop by Brands",
        },
        "electronics-kodak": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095225.html",
            "label": "KODAK",
            "section": "Shop by Brands",
        },
        "electronics-fujifilm": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095226.html",
            "label": "FujiFilm",
            "section": "Shop by Brands",
        },
        "electronics-acer": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095228.html",
            "label": "Acer",
            "section": "Shop by Brands",
        },
        "electronics-nintendo": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095229.html",
            "label": "Nintendo",
            "section": "Shop by Brands",
        },
        "electronics-blackview": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095233.html",
            "label": "Blackview",
            "section": "Shop by Brands",
        },
        "electronics-kingston": {
            "url": "https://us.shein.com/BrandZone/Brand-Collections-sc-18850095234.html",
            "label": "KINGSTON",
            "section": "Shop by Brands",
        },
    },
    "toys-games": {
        "toys-games": {
            "url": "https://us.shein.com/RecommendSelection/Toys-Games-sc-017172978.html",
            "label": "Toys & Games",
            "section": "Top category",
        },
        "toys-games-view-all": {
            "url": "https://us.shein.com/Toys-Games-c-4328.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "toys-games-new-in": {
            "url": "https://us.shein.com/recommend/New-In-Toys-Games-sc-10050001035.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "toys-games-sale": {
            "url": "https://us.shein.com/recommend/Toys-Games-sc-10050000904.html",
            "label": "Sale",
            "section": "Shop by Category",
        },
        "toys-games-top-rated": {
            "url": "https://us.shein.com/recommend/toys-top-rated-sc-10050027891.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "toys-games-kids-educational-toys": {
            "url": "https://us.shein.com/Kids-Educational-Toys-c-6996.html",
            "label": "Kids Educational Toys",
            "section": "Shop by Category",
        },
        "toys-games-kids-dolls-stuffed-toys": {
            "url": "https://us.shein.com/Kids-Dolls-Stuffed-Toys-c-7288.html",
            "label": "Kids Dolls & Stuffed Toys",
            "section": "Shop by Category",
        },
        "toys-games-hobbies-collections-parties": {
            "url": "https://us.shein.com/Hobbies,-Collections,-Parties-c-7163.html",
            "label": "Hobbies, Collections, Parties",
            "section": "Shop by Category",
        },
        "toys-games-kids-arts-crafts": {
            "url": "https://us.shein.com/Kids-Arts-Crafts-c-6995.html",
            "label": "Kids Arts & Crafts",
            "section": "Shop by Category",
        },
        "toys-games-games-entertainment": {
            "url": "https://us.shein.com/Games-Entertainment-c-7169.html",
            "label": "Games & Entertainment",
            "section": "Shop by Category",
        },
        "toys-games-kids-outdoor-play": {
            "url": "https://us.shein.com/Kids-Outdoor-Play-c-7515.html",
            "label": "Kids Outdoor Play",
            "section": "Shop by Category",
        },
        "toys-games-kids-block-toys-action-figures": {
            "url": "https://us.shein.com/Kids-Block-Toys-Action-Figures-c-7099.html",
            "label": "Kids Block Toys & Action Figures",
            "section": "Shop by Category",
        },
        "toys-games-kids-dress-up-pretend-toys": {
            "url": "https://us.shein.com/Kids-Dress-Up-Pretend-Toys-c-4669.html",
            "label": "Kids Dress up & Pretend Toys",
            "section": "Shop by Category",
        },
        "toys-games-kids-vehicle-remote-control-toys": {
            "url": "https://us.shein.com/Kids-Vehicle-Remote-Control-Toys-c-7289.html",
            "label": "Kids Vehicle & Remote Control Toys",
            "section": "Shop by Category",
        },
        "toys-games-blind-box": {
            "url": "https://us.shein.com/Blind-Box-c-14361.html",
            "label": "Blind Box",
            "section": "Shop by Category",
        },
        "toys-games-baby-toddler-toys": {
            "url": "https://us.shein.com/Baby-Toddler-Toys-c-7513.html",
            "label": "Baby & Toddler Toys",
            "section": "Shop by Category",
        },
        "toys-games-kids-reading-writing": {
            "url": "https://us.shein.com/Reading-Writing-c-7064.html",
            "label": "Kids Reading & Writing",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-preschool-toys": {
            "url": "https://us.shein.com/Preschool-Toys-c-7021.html",
            "label": "Kids Preschool Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-interactive-games": {
            "url": "https://us.shein.com/Kids-Interactive-Games-c-2858.html",
            "label": "Kids Interactive Games",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-electronic-learning-toys": {
            "url": "https://us.shein.com/Kids-Electronic-Learning-Toys-c-7070.html",
            "label": "Kids Electronic Learning Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-other-kids-educational-toys": {
            "url": "https://us.shein.com/Other-Kids-Educational-Toys-c-2851.html",
            "label": "Other Kids Educational Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-music-toys": {
            "url": "https://us.shein.com/Kids-Music-Toys-c-9743.html",
            "label": "Kids Music Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-puzzles": {
            "url": "https://us.shein.com/Puzzles-c-7004.html",
            "label": "Kids Puzzles",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-shape-color-recognition": {
            "url": "https://us.shein.com/Shape-Color-Recognition-c-7076.html",
            "label": "Kids Shape & Color Recognition",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-alphabet-number-toys": {
            "url": "https://us.shein.com/Alphabet-Number-Toys-c-7082.html",
            "label": "Kids Alphabet & Number Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-other-kids-electric-educational-toys": {
            "url": "https://us.shein.com/Other-Kids-Electric-Educational-Toys-c-7002.html",
            "label": "Other Kids Electric Educational Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-walkie-talkies": {
            "url": "https://us.shein.com/Kids-Walkie-Talkies-c-7091.html",
            "label": "Kids Walkie Talkies",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-optics": {
            "url": "https://us.shein.com/Kids-Optics-c-7042.html",
            "label": "Kids Optics",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-electronic-pets": {
            "url": "https://us.shein.com/Kids-Electronic-Pets-c-7083.html",
            "label": "Kids Electronic Pets",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-magic-cubes": {
            "url": "https://us.shein.com/Kids-Magic-Cubes-c-8448.html",
            "label": "Kids Magic Cubes",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-stem-toys": {
            "url": "https://us.shein.com/Kids-STEM-Toys-c-7088.html",
            "label": "Kids STEM Toys",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-marble-runs": {
            "url": "https://us.shein.com/Kids-Marble-Runs-c-7055.html",
            "label": "Kids Marble Runs",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-habitats": {
            "url": "https://us.shein.com/Kids-Habitats-c-7062.html",
            "label": "Kids Habitats",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-detective-spy": {
            "url": "https://us.shein.com/Kids-Detective-Spy-c-7060.html",
            "label": "Kids Detective & Spy",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-solar-power-kits": {
            "url": "https://us.shein.com/Kids-Solar-Power-Kits-c-7058.html",
            "label": "Kids Solar Power Kits",
            "section": "Kids Educational Toys",
        },
        "toys-games-kids-plush-stuffed-toys": {
            "url": "https://us.shein.com/Plush-Stuffed-Toys-c-7291.html",
            "label": "Kids Plush & Stuffed Toys",
            "section": "Kids Dolls & Stuffed Toys",
        },
        "toys-games-kids-doll-toys": {
            "url": "https://us.shein.com/Doll-Toys-c-7290.html",
            "label": "Kids Doll Toys",
            "section": "Kids Dolls & Stuffed Toys",
        },
        "toys-games-kids-puppets-puppet-theaters": {
            "url": "https://us.shein.com/Kids-Puppets-Puppet-Theaters-c-7292.html",
            "label": "Kids Puppets & Puppet Theaters",
            "section": "Kids Dolls & Stuffed Toys",
        },
        "toys-games-kids-stickers-collage": {
            "url": "https://us.shein.com/Stickers-Collage-c-7040.html",
            "label": "Kids Stickers & Collage",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-craft-kits": {
            "url": "https://us.shein.com/Craft-Kits-c-7003.html",
            "label": "Kids Craft Kits",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-clay-plasticine": {
            "url": "https://us.shein.com/Clay-Plasticine-c-6998.html",
            "label": "Kids Clay & Plasticine",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-drawing-writing-boards": {
            "url": "https://us.shein.com/Drawing-Writing-Boards-c-7061.html",
            "label": "Kids Drawing & Writing Boards",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-adhesives": {
            "url": "https://us.shein.com/Kids-Adhesives-c-7037.html",
            "label": "Kids Adhesives",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-aprons-smocks": {
            "url": "https://us.shein.com/Kids-Aprons-Smocks-c-6997.html",
            "label": "Kids Aprons & Smocks",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-easels": {
            "url": "https://us.shein.com/Kids-Easels-c-7036.html",
            "label": "Kids Easels",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-kids-3d-diy-stickers": {
            "url": "https://us.shein.com/Kids-3D/DIY-Stickers-c-14473.html",
            "label": "Kids 3D/DIY Stickers",
            "section": "Kids Arts & Crafts",
        },
        "toys-games-game-supplies": {
            "url": "https://us.shein.com/Game-Supplies-c-7173.html",
            "label": "Game Supplies",
            "section": "Games & Entertainment",
        },
        "toys-games-adult-blocks-figures": {
            "url": "https://us.shein.com/Adult-Blocks-Figures-c-7167.html",
            "label": "Adult Blocks & Figures",
            "section": "Games & Entertainment",
        },
        "toys-games-electronic-remote-control-toys": {
            "url": "https://us.shein.com/Electronic-Remote-Control-Toys-c-7171.html",
            "label": "Electronic & Remote Control Toys",
            "section": "Games & Entertainment",
        },
        "toys-games-kids-tricycles-scooters-wagons": {
            "url": "https://us.shein.com/Kids-Tricycles,-Scooters,-Wagons-c-7522.html",
            "label": "Kids Tricycles, Scooters, & Wagons",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-swimming-pools-outdoor-water-toys": {
            "url": "https://us.shein.com/Swimming-Pools-Outdoor-Water-Toys-c-7526.html",
            "label": "Kids Swimming Pools & Outdoor Water " "Toys",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-play-tents-tunnels": {
            "url": "https://us.shein.com/Play-Tents-Tunnels-c-7523.html",
            "label": "Kids Play Tents & Tunnels",
            "section": "Kids Outdoor Play",
        },
        "toys-games-other-kids-sports-outdoor-play": {
            "url": "https://us.shein.com/Other-Kids-Sports-Outdoor-Play-c-2857.html",
            "label": "Other Kids Sports & Outdoor Play",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-toy-sports": {
            "url": "https://us.shein.com/Toy-Sports-c-7527.html",
            "label": "Kids Toy Sports",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-fitness-equipment": {
            "url": "https://us.shein.com/Kids-Fitness-Equipment-c-7556.html",
            "label": "Kids Fitness Equipment",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-bubbles": {
            "url": "https://us.shein.com/Kids-Bubbles-c-8345.html",
            "label": "Kids Bubbles",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-outdoor-blasters-foam-play": {
            "url": "https://us.shein.com/Outdoor-Blasters-Foam-Play-c-7518.html",
            "label": "Kids Outdoor Blasters & Foam Play",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-play-sets-playground-equipment": {
            "url": "https://us.shein.com/Kids-Play-Sets-Playground-Equipment-c-7521.html",
            "label": "Kids Play Sets & Playground Equipment",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-ball-pits-accessories": {
            "url": "https://us.shein.com/Kids-Ball-Pits-Accessories-c-7516.html",
            "label": "Kids Ball Pits & Accessories",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-sandboxes-beach-toys": {
            "url": "https://us.shein.com/Kids-Sandboxes-Beach-Toys-c-7528.html",
            "label": "Kids Sandboxes & Beach Toys",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-outdoor-flying-toys": {
            "url": "https://us.shein.com/Kids-Outdoor-Flying-Toys-c-7519.html",
            "label": "Kids Outdoor Flying Toys",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-nature-exploration-toys": {
            "url": "https://us.shein.com/Kids-Nature-Exploration-Toys-c-7567.html",
            "label": "Kids Nature Exploration Toys",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-balance-boards": {
            "url": "https://us.shein.com/Kids-Balance-Boards-c-7537.html",
            "label": "Kids Balance Boards",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-pogo-sticks-hoppers": {
            "url": "https://us.shein.com/Kids-Pogo-Sticks-Hoppers-c-7524.html",
            "label": "Kids Pogo Sticks & Hoppers",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-bean-bags-footbags": {
            "url": "https://us.shein.com/Kids-Bean-Bags-Footbags-c-7517.html",
            "label": "Kids Bean Bags & Footbags",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-slumber-bags": {
            "url": "https://us.shein.com/Kids-Slumber-Bags-c-7607.html",
            "label": "Kids Slumber Bags",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-yo-yos": {
            "url": "https://us.shein.com/Kids-Yo-yos-c-7580.html",
            "label": "Kids Yo-yos",
            "section": "Kids Outdoor Play",
        },
        "toys-games-kids-building-block-sets": {
            "url": "https://us.shein.com/Building-Block-Sets-c-2855.html",
            "label": "Kids Building Block Sets",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-magnetic-building-block-toys": {
            "url": "https://us.shein.com/Magnetic-Building-Block-Toys-c-7119.html",
            "label": "Kids Magnetic Building Block Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-animal-figure-toys": {
            "url": "https://us.shein.com/Animal-Figure-Toys-c-8453.html",
            "label": "Kids Animal Figure Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-block-vehicles": {
            "url": "https://us.shein.com/Block-Vehicles-c-7100.html",
            "label": "Kids Block Vehicles",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-other-kids-block-toys": {
            "url": "https://us.shein.com/Other-Kids-Block-Toys-c-4662.html",
            "label": "Other Kids Block Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-building-block-toys": {
            "url": "https://us.shein.com/Kids-Building-Block-Toys-c-7115.html",
            "label": "Kids Building Block Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-electronic-block-toys": {
            "url": "https://us.shein.com/Kids-Electronic-Block-Toys-c-7120.html",
            "label": "Kids Electronic Block Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-stacking-block-toys": {
            "url": "https://us.shein.com/Kids-Stacking-Block-Toys-c-7116.html",
            "label": "Kids Stacking Block Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-building-block-collections-and-accessories": {
            "url": "https://us.shein.com/Kids-Building-Block-Collections-and-Accessories-c-7117.html",
            "label": "Kids Building Block " "Collections and Accessories",
            "section": "Kids Block Toys & Action " "Figures",
        },
        "toys-games-kids-gear-building-toys": {
            "url": "https://us.shein.com/Kids-Gear-Building-Toys-c-7118.html",
            "label": "Kids Gear Building Toys",
            "section": "Kids Block Toys & Action Figures",
        },
        "toys-games-kids-dress-up-sets": {
            "url": "https://us.shein.com/Dress-Up-Sets-c-7360.html",
            "label": "Kids Dress up Sets",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-kitchen-toys": {
            "url": "https://us.shein.com/Kitchen-Toys-c-7298.html",
            "label": "Kids Kitchen Toys",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-dress-up-accessories": {
            "url": "https://us.shein.com/Dress-Up-Accessories-c-7301.html",
            "label": "Kids Dress up Accessories",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-other-kids-dress-up-pretend-toys": {
            "url": "https://us.shein.com/Other-Kids-Dress-Up-Pretend-Toys-c-2178.html",
            "label": "Other Kids Dress Up & Pretend Toys",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-play-tools": {
            "url": "https://us.shein.com/Play-Tools-c-7356.html",
            "label": "Kids Play Tools",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-money-banking": {
            "url": "https://us.shein.com/Money-Banking-c-7329.html",
            "label": "Kids Money & Banking",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-medical-kits": {
            "url": "https://us.shein.com/Kids-Medical-Kits-c-7327.html",
            "label": "Kids Medical Kits",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-pretend-phones-smartphone-toys": {
            "url": "https://us.shein.com/Kids-Pretend-Phones-Smartphone-Toys-c-7323.html",
            "label": "Kids Pretend Phones & Smartphone Toys",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-magnetic-felt-playboards": {
            "url": "https://us.shein.com/Kids-Magnetic-Felt-Playboards-c-7331.html",
            "label": "Kids Magnetic & Felt Playboards",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-housekeeping-toys": {
            "url": "https://us.shein.com/Housekeeping-Toys-c-7300.html",
            "label": "Kids Housekeeping Toys",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-electric-dress-up-pretend-toys": {
            "url": "https://us.shein.com/Electric-Dress-Up-Pretend-Toys-c-7308.html",
            "label": "Kids Electric Dress up & Pretend Toys",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-dressers": {
            "url": "https://us.shein.com/Kids-Dressers-c-7361.html",
            "label": "Kids Dressers",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-shops-accessories": {
            "url": "https://us.shein.com/Shops-Accessories-c-7299.html",
            "label": "Kids Shops & Accessories",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-purses": {
            "url": "https://us.shein.com/Kids-Purses-c-7358.html",
            "label": "Kids Purses",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-pretend-jewelry-boxes": {
            "url": "https://us.shein.com/Kids-Pretend-Jewelry-Boxes-c-7325.html",
            "label": "Kids Pretend Jewelry Boxes",
            "section": "Kids Dress up & Pretend Toys",
        },
        "toys-games-kids-play-vehicles": {
            "url": "https://us.shein.com/Kids-Play-Vehicles-c-7297.html",
            "label": "Kids Play Vehicles",
            "section": "Kids Vehicle & Remote Control Toys",
        },
        "toys-games-kids-remote-control-vehicles": {
            "url": "https://us.shein.com/Kids-Remote-Control-Vehicles-c-7293.html",
            "label": "Kids Remote Control Vehicles",
            "section": "Kids Vehicle & Remote Control Toys",
        },
        "toys-games-kids-remote-control-robots": {
            "url": "https://us.shein.com/Kids-Remote-Control-Robots-c-7294.html",
            "label": "Kids Remote Control Robots",
            "section": "Kids Vehicle & Remote Control Toys",
        },
        "toys-games-other-kids-remote-app-controlled-parts": {
            "url": "https://us.shein.com/Kids-Remote-App-Control-Parts-c-7296.html",
            "label": "Other Kids Remote & App Controlled " "Parts",
            "section": "Kids Vehicle & Remote Control Toys",
        },
        "toys-games-collectible-blind-box": {
            "url": "https://us.shein.com/Collectible-Blind-Box-c-14363.html",
            "label": "Collectible Blind Box",
            "section": "Blind Box",
        },
        "toys-games-toys-blind-box": {
            "url": "https://us.shein.com/Toys-Blind-Box-c-14362.html",
            "label": "Toys Blind Box",
            "section": "Blind Box",
        },
        "toys-games-baby-early-development-activity-toys": {
            "url": "https://us.shein.com/Baby-Early-Development-Activity-Toys-c-7514.html",
            "label": "Baby Early Development & Activity Toys",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-baby-musical-toys": {
            "url": "https://us.shein.com/Baby-Musical-Toys-c-7532.html",
            "label": "Baby Musical Toys",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-baby-rattles-plush-rings": {
            "url": "https://us.shein.com/Rattles-Plush-Rings-c-7531.html",
            "label": "Baby Rattles & Plush Rings",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-baby-bath-toys": {
            "url": "https://us.shein.com/Baby-Bath-Toys-c-8443.html",
            "label": "Baby Bath Toys",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-baby-stationary-activity-centers": {
            "url": "https://us.shein.com/Baby-Stationary-Activity-Centers-c-7544.html",
            "label": "Baby Stationary Activity Centers",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-baby-ride-on-stick-horses": {
            "url": "https://us.shein.com/Baby-Ride-on-Stick-Horses-c-7530.html",
            "label": "Baby Ride-on Stick Horses",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-baby-indoor-climbers-play-structures": {
            "url": "https://us.shein.com/Baby-Indoor-Climbers-Play-Structures-c-7533.html",
            "label": "Baby Indoor Climbers & Play Structures",
            "section": "Baby & Toddler Toys",
        },
        "toys-games-lego": {
            "url": "https://us.shein.com/recommend/Toys-LEGO-sc-10050029269.html",
            "label": "LEGO",
            "section": "Brands We Love",
        },
        "toys-games-pop-mart": {
            "url": "https://us.shein.com/recommend/Toys-Pop-Mart-sc-10050029271.html",
            "label": "Pop Mart",
            "section": "Brands We Love",
        },
        "toys-games-miniso": {
            "url": "https://us.shein.com/recommend/Toys-Miniso-sc-10050029270.html",
            "label": "Miniso",
            "section": "Brands We Love",
        },
        "toys-games-hasbro": {
            "url": "https://us.shein.com/recommend/Toys-Hasbro-sc-10050029275.html",
            "label": "Hasbro",
            "section": "Brands We Love",
        },
        "toys-games-funko": {
            "url": "https://us.shein.com/recommend/Toys-Funko-sc-10050029276.html",
            "label": "Funko",
            "section": "Brands We Love",
        },
        "toys-games-zuru": {
            "url": "https://us.shein.com/recommend/Toys-ZURU-sc-10050029273.html",
            "label": "ZURU",
            "section": "Brands We Love",
        },
        "toys-games-mattel": {
            "url": "https://us.shein.com/recommend/Toys-Mattel-sc-10050029274.html",
            "label": "Mattel",
            "section": "Brands We Love",
        },
    },
    "tools-home-improvement": {
        "tools-home-improvement": {
            "url": "https://us.shein.com/RecommendSelection/Tools-Home-Improvement-sc-017185547.html",
            "label": "Tools & Home Improvement",
            "section": "Top category",
        },
        "tools-home-improvement-view-all": {
            "url": "https://us.shein.com/Furniture-c-4577.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "tools-home-improvement-new-in": {
            "url": "https://us.shein.com/recommend/Tools-Home-Improvement-New-In-sc-10050001038.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "tools-home-improvement-sale": {
            "url": "https://us.shein.com/recommend/sale-Tool-PL-FR-DE-sc-10050001108.html",
            "label": "Sale",
            "section": "Shop by Category",
        },
        "tools-home-improvement-top-rated": {
            "url": "https://us.shein.com/recommend/tools-top-rated-sc-10050008596.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "tools-home-improvement-lighting-lamp": {
            "url": "https://us.shein.com/Lighting-Lamp-c-2299.html",
            "label": "Lighting & Lamp",
            "section": "Shop by Category",
        },
        "tools-home-improvement-tools": {
            "url": "https://us.shein.com/Tools-c-4469.html",
            "label": "Tools",
            "section": "Shop by Category",
        },
        "tools-home-improvement-hardware": {
            "url": "https://us.shein.com/Hardware-c-3524.html",
            "label": "Hardware",
            "section": "Shop by Category",
        },
        "tools-home-improvement-kitchen-bathroom-fixtures": {
            "url": "https://us.shein.com/Kitchen-Bathroom-Fixtures-c-4495.html",
            "label": "Kitchen & Bathroom Fixtures",
            "section": "Shop by Category",
        },
        "tools-home-improvement-home-protective-equipment": {
            "url": "https://us.shein.com/Home-Protective-Equipment-c-4470.html",
            "label": "Home Protective Equipment",
            "section": "Shop by Category",
        },
        "tools-home-improvement-patio-furniture-accessories": {
            "url": "https://us.shein.com/Patio-Furniture-Accessories-c-4925.html",
            "label": "Patio Furniture & " "Accessories",
            "section": "Shop by Category",
        },
        "tools-home-improvement-painting-supplies-wall-treatments": {
            "url": "https://us.shein.com/Painting-Supplies-Wall-Treatments-c-4573.html",
            "label": "Painting Supplies & " "Wall Treatments",
            "section": "Shop by Category",
        },
        "tools-home-improvement-measurement-analysis-instruments": {
            "url": "https://us.shein.com/Measurement-Analysis-Instruments-c-4468.html",
            "label": "Measurement & " "Analysis Instruments",
            "section": "Shop by Category",
        },
        "tools-home-improvement-electrical-equipments-supplies": {
            "url": "https://us.shein.com/Electrical-Equipments-Supplies-c-4471.html",
            "label": "Electrical Equipments " "& Supplies",
            "section": "Shop by Category",
        },
        "tools-home-improvement-building-supplies": {
            "url": "https://us.shein.com/Building-Supplies-c-5619.html",
            "label": "Building Supplies",
            "section": "Shop by Category",
        },
        "tools-home-improvement-welding": {
            "url": "https://us.shein.com/Welding-c-5472.html",
            "label": "Welding",
            "section": "Shop by Category",
        },
        "tools-home-improvement-bedroom-furniture": {
            "url": "https://us.shein.com/Bedroom-Furniture-c-4938.html",
            "label": "Bedroom Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-living-room-furniture": {
            "url": "https://us.shein.com/Living-Room-Furniture-c-4991.html",
            "label": "Living Room Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-dining-room-furniture": {
            "url": "https://us.shein.com/Dining-Room-Furniture-c-4932.html",
            "label": "Dining Room Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-home-office-furniture": {
            "url": "https://us.shein.com/Home-Office-Furniture-c-4580.html",
            "label": "Home Office Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-game-recreation-room-furniture": {
            "url": "https://us.shein.com/Game-Recreation-Room-Furniture-c-4978.html",
            "label": "Game & Recreation Room " "Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-kids-furniture": {
            "url": "https://us.shein.com/Kids-Furniture-c-4984.html",
            "label": "Kids' Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-entryway-furniture": {
            "url": "https://us.shein.com/Entryway-Furniture-c-4959.html",
            "label": "Entryway Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-accent-furniture": {
            "url": "https://us.shein.com/Accent-Furniture-c-4926.html",
            "label": "Accent Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-bathroom-furniture": {
            "url": "https://us.shein.com/Bathroom-Furniture-c-4923.html",
            "label": "Bathroom Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-kitchen-furniture": {
            "url": "https://us.shein.com/Kitchen-Furniture-c-5608.html",
            "label": "Kitchen Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-nursery-furniture": {
            "url": "https://us.shein.com/Nursery-Furniture-c-5020.html",
            "label": "Nursery Furniture",
            "section": "Furniture",
        },
        "tools-home-improvement-furniture-replacement-parts": {
            "url": "https://us.shein.com/Furniture-Replacement-Parts-c-5571.html",
            "label": "Furniture Replacement " "Parts",
            "section": "Furniture",
        },
        "tools-home-improvement-novelty-lighting": {
            "url": "https://us.shein.com/Novelty-Lighting-c-3373.html",
            "label": "Novelty Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-lamps-shades": {
            "url": "https://us.shein.com/Lamps-Shades-c-4615.html",
            "label": "Lamps & Shades",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-outdoor-lighting": {
            "url": "https://us.shein.com/Outdoor-Lighting-c-3375.html",
            "label": "Outdoor Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-festival-lighting": {
            "url": "https://us.shein.com/Festival-Lighting-c-12689.html",
            "label": "Festival Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-ceiling-lights-fans": {
            "url": "https://us.shein.com/Ceiling-Lights-Fans-c-4596.html",
            "label": "Ceiling Lights & Fans",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-indoor-lighting": {
            "url": "https://us.shein.com/Indoor-Lighting-c-3371.html",
            "label": "Indoor Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-customized-lighting": {
            "url": "https://us.shein.com/Customized-Lighting-c-8920.html",
            "label": "Customized Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-portable-lighting": {
            "url": "https://us.shein.com/Portable-Lighting-c-3376.html",
            "label": "Portable Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-commercial-lighting": {
            "url": "https://us.shein.com/Commercial-Lighting-c-4586.html",
            "label": "Commercial Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-light-accessories": {
            "url": "https://us.shein.com/Light-Accessories-c-4644.html",
            "label": "Light Accessories",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-professional-lighting": {
            "url": "https://us.shein.com/Professional-Lighting-c-4588.html",
            "label": "Professional Lighting",
            "section": "Lighting & Lamp",
        },
        "tools-home-improvement-view-all-4501": {
            "url": "https://us.shein.com/Hand-Tools-c-4501.html",
            "label": "View All",
            "section": "Tools",
        },
        "tools-home-improvement-power-tools": {
            "url": "https://us.shein.com/Power-Tools-c-14243.html",
            "label": "Power Tools",
            "section": "Tools",
        },
        "tools-home-improvement-tool-accessories": {
            "url": "https://us.shein.com/Tool-Accessories-c-5470.html",
            "label": "Tool Accessories",
            "section": "Tools",
        },
        "tools-home-improvement-garden-tools": {
            "url": "https://us.shein.com/Garden-Tools-c-4567.html",
            "label": "Garden Tools",
            "section": "Tools",
        },
        "tools-home-improvement-storage-tool-organization": {
            "url": "https://us.shein.com/Storage-Tool-Organization-c-4575.html",
            "label": "Storage & Tool Organization",
            "section": "Tools",
        },
        "tools-home-improvement-woodworking-machinery-parts": {
            "url": "https://us.shein.com/Woodworking-Machinery-Parts-c-5462.html",
            "label": "Woodworking Machinery & " "Parts",
            "section": "Tools",
        },
        "tools-home-improvement-customized-tools": {
            "url": "https://us.shein.com/BBQ-c-6920.html",
            "label": "Customized Tools",
            "section": "Tools",
        },
        "tools-home-improvement-adhesives-sealers": {
            "url": "https://us.shein.com/Adhesives-Sealers-c-4520.html",
            "label": "Adhesives & Sealers",
            "section": "Hardware",
        },
        "tools-home-improvement-cabinet-hardware": {
            "url": "https://us.shein.com/Cabinet-Hardware-c-4486.html",
            "label": "Cabinet Hardware",
            "section": "Hardware",
        },
        "tools-home-improvement-door-hardware-locks": {
            "url": "https://us.shein.com/Door-Hardware-Locks-c-4475.html",
            "label": "Door Hardware & Locks",
            "section": "Hardware",
        },
        "tools-home-improvement-furniture-hardware": {
            "url": "https://us.shein.com/Furniture-Hardware-c-4524.html",
            "label": "Furniture Hardware",
            "section": "Hardware",
        },
        "tools-home-improvement-fasteners-hooks": {
            "url": "https://us.shein.com/Fasteners-Hooks-c-5173.html",
            "label": "Fasteners & Hooks",
            "section": "Hardware",
        },
        "tools-home-improvement-brackets-clamps": {
            "url": "https://us.shein.com/Brackets-Clamps-c-5177.html",
            "label": "Brackets & Clamps",
            "section": "Hardware",
        },
        "tools-home-improvement-magnetic-materials": {
            "url": "https://us.shein.com/Magnetic-Materials-c-5524.html",
            "label": "Magnetic Materials",
            "section": "Hardware",
        },
        "tools-home-improvement-window-hardware": {
            "url": "https://us.shein.com/Window-Hardware-c-4511.html",
            "label": "Window Hardware",
            "section": "Hardware",
        },
        "tools-home-improvement-hasps-locks": {
            "url": "https://us.shein.com/Hasps-Locks-c-4533.html",
            "label": "Hasps & Locks",
            "section": "Hardware",
        },
        "tools-home-improvement-tarps-tie-downs": {
            "url": "https://us.shein.com/Personal-Protective-Equipment-c-4549.html",
            "label": "Tarps & Tie-Downs",
            "section": "Hardware",
        },
        "tools-home-improvement-faucets-accessories": {
            "url": "https://us.shein.com/Faucets-Accessories-c-3529.html",
            "label": "Faucets & Accessories",
            "section": "Hardware",
        },
        "tools-home-improvement-power-transmission": {
            "url": "https://us.shein.com/Power-Transmission-c-5519.html",
            "label": "Power Transmission",
            "section": "Hardware",
        },
        "tools-home-improvement-floor-drain": {
            "url": "https://us.shein.com/Floor-Drain-c-3531.html",
            "label": "Floor Drain",
            "section": "Hardware",
        },
        "tools-home-improvement-hanging-hardware": {
            "url": "https://us.shein.com/Hanging-Hardware-c-10130.html",
            "label": "Hanging Hardware",
            "section": "Hardware",
        },
        "tools-home-improvement-springs": {
            "url": "https://us.shein.com/Springs-c-5514.html",
            "label": "Springs",
            "section": "Hardware",
        },
        "tools-home-improvement-view-all-4495": {
            "url": "https://us.shein.com/Bathroom-Fixtures-c-4495.html",
            "label": "View All",
            "section": "Kitchen & Bathroom Fixtures",
        },
        "tools-home-improvement-bathroom-fixtures": {
            "url": "https://us.shein.com/Bathroom-Fixtures-c-14244.html",
            "label": "Bathroom Fixtures",
            "section": "Kitchen & Bathroom Fixtures",
        },
        "tools-home-improvement-kitchen-fixtures": {
            "url": "https://us.shein.com/Kitchen-Fixtures-c-4542.html",
            "label": "Kitchen Fixtures",
            "section": "Kitchen & Bathroom Fixtures",
        },
        "tools-home-improvement-plumbing": {
            "url": "https://us.shein.com/Plumbing-c-4547.html",
            "label": "Plumbing",
            "section": "Kitchen & Bathroom Fixtures",
        },
        "tools-home-improvement-water-filtration-softeners": {
            "url": "https://us.shein.com/Water-Filtration-Softeners-c-9328.html",
            "label": "Water Filtration & " "Softeners",
            "section": "Kitchen & Bathroom " "Fixtures",
        },
        "tools-home-improvement-view-all-4470": {
            "url": "https://us.shein.com/Safety-Protective-Equipment-c-4470.html",
            "label": "View All",
            "section": "Safety & Protective Equipment",
        },
        "tools-home-improvement-home-security-systems": {
            "url": "https://us.shein.com/Home-Security-Systems-c-10064.html",
            "label": "Home Security Systems",
            "section": "Safety & Protective " "Equipment",
        },
        "tools-home-improvement-access-control": {
            "url": "https://us.shein.com/Access-Control-c-5578.html",
            "label": "Access Control",
            "section": "Safety & Protective Equipment",
        },
        "tools-home-improvement-safes": {
            "url": "https://us.shein.com/Safes-c-10066.html",
            "label": "Safes",
            "section": "Safety & Protective Equipment",
        },
        "tools-home-improvement-security-alarm": {
            "url": "https://us.shein.com/Security-Alarm-c-4565.html",
            "label": "Security Alarm",
            "section": "Safety & Protective Equipment",
        },
        "tools-home-improvement-emergency-kits-supplies": {
            "url": "https://us.shein.com/Emergency-Kits-Supplies-c-4576.html",
            "label": "Emergency Kits & Supplies",
            "section": "Safety & Protective " "Equipment",
        },
        "tools-home-improvement-safety-signs-signals": {
            "url": "https://us.shein.com/Safety-Signs-Signals-c-10400.html",
            "label": "Safety Signs & Signals",
            "section": "Safety & Protective Equipment",
        },
        "tools-home-improvement-wall-sticker": {
            "url": "https://us.shein.com/Wall-Sticker-c-5190.html",
            "label": "Wall Sticker",
            "section": "Painting Supplies & Wall Treatments",
        },
        "tools-home-improvement-window-films": {
            "url": "https://us.shein.com/Window-Films-c-5192.html",
            "label": "Window Films",
            "section": "Painting Supplies & Wall Treatments",
        },
        "tools-home-improvement-painting-supplies-tools": {
            "url": "https://us.shein.com/Painting-Supplies-Tools-c-10062.html",
            "label": "Painting Supplies & Tools",
            "section": "Painting Supplies & Wall " "Treatments",
        },
        "tools-home-improvement-paint": {
            "url": "https://us.shein.com/Paint-c-5196.html",
            "label": "Paint",
            "section": "Painting Supplies & Wall Treatments",
        },
        "tools-home-improvement-wall-repair": {
            "url": "https://us.shein.com/Wall-Repair-c-10132.html",
            "label": "Wall Repair",
            "section": "Painting Supplies & Wall Treatments",
        },
        "tools-home-improvement-window-stickers": {
            "url": "https://us.shein.com/Window-Stickers-c-5193.html",
            "label": "Window Stickers",
            "section": "Painting Supplies & Wall " "Treatments",
        },
        "tools-home-improvement-wall-panels": {
            "url": "https://us.shein.com/Wall-Panels-c-11974.html",
            "label": "Wall Panels",
            "section": "Painting Supplies & Wall Treatments",
        },
        "tools-home-improvement-wallpaper-borders": {
            "url": "https://us.shein.com/Wallpaper-Borders-c-5189.html",
            "label": "Wallpaper Borders",
            "section": "Painting Supplies & Wall " "Treatments",
        },
        "tools-home-improvement-paint-application": {
            "url": "https://us.shein.com/Paint-Application-c-5199.html",
            "label": "Paint Application",
            "section": "Painting Supplies & Wall " "Treatments",
        },
        "tools-home-improvement-finishes-sealers-stains": {
            "url": "https://us.shein.com/Wallpapers-c-4602.html",
            "label": "Finishes, Sealers & Stains",
            "section": "Painting Supplies & Wall " "Treatments",
        },
        "tools-home-improvement-wall-tapestry": {
            "url": "https://us.shein.com/Wall-Tapestry-c-10405.html",
            "label": "Wall Tapestry",
            "section": "Painting Supplies & Wall Treatments",
        },
        "tools-home-improvement-counters": {
            "url": "https://us.shein.com/Counters-c-5183.html",
            "label": "Counters",
            "section": "Measurement & Analysis Instruments",
        },
        "tools-home-improvement-optical-instruments": {
            "url": "https://us.shein.com/Optical-Instruments-c-5150.html",
            "label": "Optical Instruments",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-weighing-scales": {
            "url": "https://us.shein.com/Weighing-Scales-c-4473.html",
            "label": "Weighing Scales",
            "section": "Measurement & Analysis Instruments",
        },
        "tools-home-improvement-measuring-gauging-tools": {
            "url": "https://us.shein.com/Measuring-Gauging-Tools-c-5154.html",
            "label": "Measuring & Gauging Tools",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-electronic-measuring-instruments": {
            "url": "https://us.shein.com/Electronic-Measuring-Instruments-c-5494.html",
            "label": "Electronic Measuring " "Instruments",
            "section": "Measurement & " "Analysis " "Instruments",
        },
        "tools-home-improvement-electrical-instruments": {
            "url": "https://us.shein.com/Electrical-Instruments-c-5152.html",
            "label": "Electrical Instruments",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-temperature-humidity-instruments": {
            "url": "https://us.shein.com/Temperature-Humidity-Instruments-c-9303.html",
            "label": "Temperature Humidity " "Instruments",
            "section": "Measurement & " "Analysis " "Instruments",
        },
        "tools-home-improvement-temperature-instruments": {
            "url": "https://us.shein.com/Temperature-Instruments-c-4472.html",
            "label": "Temperature Instruments",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-borescopes": {
            "url": "https://us.shein.com/Borescopes-c-4476.html",
            "label": "Borescopes",
            "section": "Measurement & Analysis Instruments",
        },
        "tools-home-improvement-analyzers": {
            "url": "https://us.shein.com/Analyzers-c-5513.html",
            "label": "Analyzers",
            "section": "Measurement & Analysis Instruments",
        },
        "tools-home-improvement-testing-equipment": {
            "url": "https://us.shein.com/Testing-Equipment-c-5719.html",
            "label": "Testing Equipment",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-thermometers-weather-instruments": {
            "url": "https://us.shein.com/Thermometers-Weather-Instruments-c-11878.html",
            "label": "Thermometers & " "Weather Instruments",
            "section": "Measurement & " "Analysis " "Instruments",
        },
        "tools-home-improvement-marking-tools": {
            "url": "https://us.shein.com/Marking-Tools-c-9312.html",
            "label": "Marking Tools",
            "section": "Measurement & Analysis Instruments",
        },
        "tools-home-improvement-timers": {
            "url": "https://us.shein.com/Timers-c-4474.html",
            "label": "Timers",
            "section": "Measurement & Analysis Instruments",
        },
        "tools-home-improvement-pressure-measuring-instruments": {
            "url": "https://us.shein.com/Pressure-Measuring-Instruments-c-5706.html",
            "label": "Pressure Measuring " "Instruments",
            "section": "Measurement & " "Analysis " "Instruments",
        },
        "tools-home-improvement-level-measuring-instruments": {
            "url": "https://us.shein.com/Level-Measuring-Instruments-c-5538.html",
            "label": "Level Measuring " "Instruments",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-instrument-parts-accessories": {
            "url": "https://us.shein.com/Instrument-Parts-Accessories-c-5512.html",
            "label": "Instrument Parts & " "Accessories",
            "section": "Measurement & Analysis " "Instruments",
        },
        "tools-home-improvement-physical-measuring-instruments": {
            "url": "https://us.shein.com/Physical-Measuring-Instruments-c-5525.html",
            "label": "Physical Measuring " "Instruments",
            "section": "Measurement & " "Analysis " "Instruments",
        },
        "tools-home-improvement-electrical-sockets-accessories": {
            "url": "https://us.shein.com/Electrical-Sockets-Accessories-c-4481.html",
            "label": "Electrical Sockets & " "Accessories",
            "section": "Electrical " "Equipments & " "Supplies",
        },
        "tools-home-improvement-wiring-accessories": {
            "url": "https://us.shein.com/Wiring-Accessories-c-4482.html",
            "label": "Wiring Accessories",
            "section": "Electrical Equipments & " "Supplies",
        },
        "tools-home-improvement-family-intelligence-system": {
            "url": "https://us.shein.com/Family-Intelligence-System-c-5592.html",
            "label": "Family Intelligence System",
            "section": "Electrical Equipments & " "Supplies",
        },
        "tools-home-improvement-connectors-terminals": {
            "url": "https://us.shein.com/Connectors-Terminals-c-5556.html",
            "label": "Connectors & Terminals",
            "section": "Electrical Equipments & " "Supplies",
        },
        "tools-home-improvement-power-supplies": {
            "url": "https://us.shein.com/Power-Supplies-c-4480.html",
            "label": "Power Supplies",
            "section": "Electrical Equipments & Supplies",
        },
        "tools-home-improvement-wires-cables-cable-assemblies": {
            "url": "https://us.shein.com/Wires,-Cables-Cable-Assemblies-c-5539.html",
            "label": "Wires, Cables & Cable " "Assemblies",
            "section": "Electrical Equipments " "& Supplies",
        },
        "tools-home-improvement-solar-power": {
            "url": "https://us.shein.com/Solar-Power-c-5552.html",
            "label": "Solar Power",
            "section": "Electrical Equipments & Supplies",
        },
        "tools-home-improvement-electrical-tools-hardware": {
            "url": "https://us.shein.com/Electrical-Tools-Hardware-c-10058.html",
            "label": "Electrical Tools & Hardware",
            "section": "Electrical Equipments & " "Supplies",
        },
        "tools-home-improvement-switches-dimmers": {
            "url": "https://us.shein.com/Switches-Dimmers-c-10059.html",
            "label": "Switches & Dimmers",
            "section": "Electrical Equipments & Supplies",
        },
        "tools-home-improvement-circuit-breakers-load-centers-and-fuses": {
            "url": "https://us.shein.com/Circuit-Breakers,-Load-Centers,-and-Fuses-c-14246.html",
            "label": "Circuit " "Breakers, " "Load Centers, " "and Fuses",
            "section": "Electrical " "Equipments " "& Supplies",
        },
        "tools-home-improvement-motors-parts": {
            "url": "https://us.shein.com/Motors-Parts-c-5558.html",
            "label": "Motors & Parts",
            "section": "Electrical Equipments & Supplies",
        },
        "tools-home-improvement-relays": {
            "url": "https://us.shein.com/Relays-c-5541.html",
            "label": "Relays",
            "section": "Electrical Equipments & Supplies",
        },
        "tools-home-improvement-hvac": {
            "url": "https://us.shein.com/HVAC-c-9327.html",
            "label": "HVAC",
            "section": "Building Supplies",
        },
        "tools-home-improvement-flooring-products": {
            "url": "https://us.shein.com/Flooring-Products-c-7096.html",
            "label": "Flooring Products",
            "section": "Building Supplies",
        },
        "tools-home-improvement-doors-gates-windows": {
            "url": "https://us.shein.com/Doors,-Gates-Windows-c-5774.html",
            "label": "Doors, Gates & Windows",
            "section": "Building Supplies",
        },
        "tools-home-improvement-ladders-moving-tools": {
            "url": "https://us.shein.com/Ladders-Moving-Tools-c-9306.html",
            "label": "Ladders & Moving Tools",
            "section": "Building Supplies",
        },
        "tools-home-improvement-clothes-drying-racks-poles": {
            "url": "https://us.shein.com/Clothes-Drying-Racks-Poles-c-9334.html",
            "label": "Clothes Drying Racks & " "Poles",
            "section": "Building Supplies",
        },
        "tools-home-improvement-millwork": {
            "url": "https://us.shein.com/Millwork-c-9305.html",
            "label": "Millwork",
            "section": "Building Supplies",
        },
        "tools-home-improvement-flooring-accessories": {
            "url": "https://us.shein.com/Flooring-Accessories-c-9320.html",
            "label": "Flooring Accessories",
            "section": "Building Supplies",
        },
        "tools-home-improvement-gutters-accessories": {
            "url": "https://us.shein.com/Gutters-Accessories-c-9319.html",
            "label": "Gutters & Accessories",
            "section": "Building Supplies",
        },
        "tools-home-improvement-strapping-tape": {
            "url": "https://us.shein.com/Strapping-Tape-c-9317.html",
            "label": "Strapping Tape",
            "section": "Building Supplies",
        },
        "tools-home-improvement-patio-boards-fence-material": {
            "url": "https://us.shein.com/Patio-Boards-Fence-Material-c-9304.html",
            "label": "Patio Boards & Fence " "Material",
            "section": "Building Supplies",
        },
        "tools-home-improvement-environmental-deodorization-maintenance": {
            "url": "https://us.shein.com/Environmental/Deodorization/Maintenance-c-11521.html",
            "label": "Environmental/Deodorization/Maintenance",
            "section": "Building " "Supplies",
        },
        "tools-home-improvement-outdoor-furniture": {
            "url": "https://us.shein.com/Outdoor-Furniture-c-5034.html",
            "label": "Outdoor Furniture",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-patio-seating": {
            "url": "https://us.shein.com/Patio-Seating-c-5017.html",
            "label": "Patio Seating",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-deck-boxes": {
            "url": "https://us.shein.com/Deck-Boxes-c-5047.html",
            "label": "Deck Boxes",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-patio-tables": {
            "url": "https://us.shein.com/Patio-Tables-c-4964.html",
            "label": "Patio Tables",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-umbrellas-shade": {
            "url": "https://us.shein.com/Umbrellas-Shade-c-4937.html",
            "label": "Umbrellas & Shade",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-canopies-gazebos-pergolas": {
            "url": "https://us.shein.com/Canopies,-Gazebos-Pergolas-c-5054.html",
            "label": "Canopies, Gazebos & " "Pergolas",
            "section": "Patio Furniture & " "Accessories",
        },
        "tools-home-improvement-outdoor-heating": {
            "url": "https://us.shein.com/Outdoor-Heating-c-4927.html",
            "label": "Outdoor Heating",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-hammocks-stands-accessories": {
            "url": "https://us.shein.com/Hammocks,-Stands-Accessories-c-5041.html",
            "label": "Hammocks, Stands & " "Accessories",
            "section": "Patio Furniture & " "Accessories",
        },
        "tools-home-improvement-patio-furniture-covers": {
            "url": "https://us.shein.com/Patio-Furniture-Covers-c-5025.html",
            "label": "Patio Furniture Covers",
            "section": "Patio Furniture & " "Accessories",
        },
        "tools-home-improvement-patio-cushions": {
            "url": "https://us.shein.com/Patio-Cushions-c-5051.html",
            "label": "Patio Cushions",
            "section": "Patio Furniture & Accessories",
        },
        "tools-home-improvement-picnic-baskets-tables-accessories": {
            "url": "https://us.shein.com/Picnic-Baskets,-Tables-Accessories-c-5006.html",
            "label": "Picnic Baskets, " "Tables & " "Accessories",
            "section": "Patio Furniture & " "Accessories",
        },
        "tools-home-improvement-privacy-screens-protection": {
            "url": "https://us.shein.com/Privacy-Screens-Protection-c-4990.html",
            "label": "Privacy Screens & " "Protection",
            "section": "Patio Furniture & " "Accessories",
        },
        "tools-home-improvement-patio-cushion-storage-bags": {
            "url": "https://us.shein.com/Patio-Cushion-Storage-Bags-c-5052.html",
            "label": "Patio Cushion Storage Bags",
            "section": "Patio Furniture & " "Accessories",
        },
        "tools-home-improvement-welding-soldering-supplies": {
            "url": "https://us.shein.com/Welding-Soldering-Supplies-c-5599.html",
            "label": "Welding & Soldering " "Supplies",
            "section": "Welding",
        },
        "tools-home-improvement-welding-equipment": {
            "url": "https://us.shein.com/Welding-Equipment-c-14245.html",
            "label": "Welding Equipment",
            "section": "Welding",
        },
        "tools-home-improvement-songmicshome": {
            "url": "https://us.shein.com/recommend/SONGMICSHOME-sc-10050009162.html",
            "label": "SONGMICSHOME",
            "section": "Brands We Love",
        },
        "tools-home-improvement-homcom": {
            "url": "https://us.shein.com/Brands/Homcom-sc-014278110.html",
            "label": "Homcom",
            "section": "Brands We Love",
        },
        "tools-home-improvement-costway": {
            "url": "https://us.shein.com/Brands/Costway-sc-014278118.html",
            "label": "Costway",
            "section": "Brands We Love",
        },
        "tools-home-improvement-yitahome": {
            "url": "https://us.shein.com/recommend/YITAHOME-sc-10050009163.html",
            "label": "YITAHOME",
            "section": "Brands We Love",
        },
        "tools-home-improvement-teckwe": {
            "url": "https://us.shein.com/other/TECKWE-sc-0071743372.html",
            "label": "Teckwe",
            "section": "Brands We Love",
        },
    },
    "office-school-supplies": {
        "office-school-supplies": {
            "url": "https://us.shein.com/RecommendSelection/Office-School-Supplies-sc-017185552.html",
            "label": "Office & School Supplies",
            "section": "Top category",
        },
        "office-school-supplies-view-all": {
            "url": "https://us.shein.com/Office-School-Supplies-c-2297.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "office-school-supplies-new-in": {
            "url": "https://us.shein.com/recommend/Office-School-Supplies-New-In-sc-10050001037.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "office-school-supplies-sale": {
            "url": "https://us.shein.com/recommend/sale-Office-PL-FR-DE-sc-10050001111.html",
            "label": "Sale",
            "section": "Shop by Category",
        },
        "office-school-supplies-top-rated": {
            "url": "https://us.shein.com/recommend/office-top-rated-sc-10050027893.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "office-school-supplies-happy-halloween": {
            "url": "https://us.shein.com/recommend/Happy-Halloween-sc-10050103837.html",
            "label": "Happy Halloween",
            "section": "Shop by Category",
        },
        "office-school-supplies-writing-correction-supplies": {
            "url": "https://us.shein.com/Writing-Correction-Supplies-c-3654.html",
            "label": "Writing & Correction " "Supplies",
            "section": "Shop by Category",
        },
        "office-school-supplies-notebooks-writing-pads": {
            "url": "https://us.shein.com/Notebooks-Writing-Pads-c-3921.html",
            "label": "Notebooks & Writing Pads",
            "section": "Shop by Category",
        },
        "office-school-supplies-art-supplies": {
            "url": "https://us.shein.com/Art-Supplies-c-3904.html",
            "label": "Art Supplies",
            "section": "Shop by Category",
        },
        "office-school-supplies-stationery-stickers": {
            "url": "https://us.shein.com/Stationery-Stickers-c-4123.html",
            "label": "Stationery Stickers",
            "section": "Shop by Category",
        },
        "office-school-supplies-filing-products": {
            "url": "https://us.shein.com/Filing-Products-c-4153.html",
            "label": "Filing Products",
            "section": "Shop by Category",
        },
        "office-school-supplies-desk-accessories": {
            "url": "https://us.shein.com/Desk-Accessories-c-3653.html",
            "label": "Desk Accessories",
            "section": "Shop by Category",
        },
        "office-school-supplies-labels-indexes-stamps": {
            "url": "https://us.shein.com/Labels,Indexes-Stamps-c-3912.html",
            "label": "Labels, Indexes & Stamps",
            "section": "Shop by Category",
        },
        "office-school-supplies-calendars-cards": {
            "url": "https://us.shein.com/Calendars-Cards-c-4168.html",
            "label": "Calendars & Cards",
            "section": "Shop by Category",
        },
        "office-school-supplies-paper": {
            "url": "https://us.shein.com/Paper-c-4138.html",
            "label": "Paper",
            "section": "Shop by Category",
        },
        "office-school-supplies-tapes-adhesives-fasteners": {
            "url": "https://us.shein.com/Tapes,Adhesives-Fasteners-c-4120.html",
            "label": "Tapes, Adhesives & " "Fasteners",
            "section": "Shop by Category",
        },
        "office-school-supplies-office-furniture-accessories": {
            "url": "https://us.shein.com/Office-Furniture-Accessories-c-8299.html",
            "label": "Office Furniture & " "Accessories",
            "section": "Shop by Category",
        },
        "office-school-supplies-office-binding-supplies": {
            "url": "https://us.shein.com/Office-Binding-Supplies-c-4142.html",
            "label": "Office Binding Supplies",
            "section": "Shop by Category",
        },
        "office-school-supplies-mail-shipping-supplies": {
            "url": "https://us.shein.com/Mail-Shipping-Supplies-c-4150.html",
            "label": "Mail & Shipping Supplies",
            "section": "Shop by Category",
        },
        "office-school-supplies-carrying-cases": {
            "url": "https://us.shein.com/Carrying-Cases-c-8289.html",
            "label": "Carrying Cases",
            "section": "Shop by Category",
        },
        "office-school-supplies-presentation-supplies": {
            "url": "https://us.shein.com/Presentation-Supplies-c-4133.html",
            "label": "Presentation Supplies",
            "section": "Shop by Category",
        },
        "office-school-supplies-school-educational-supplies": {
            "url": "https://us.shein.com/School-Educational-Supplies-c-4125.html",
            "label": "School & Educational " "Supplies",
            "section": "Shop by Category",
        },
        "office-school-supplies-cutting-office-tools": {
            "url": "https://us.shein.com/Cutting-Supplies-c-4164.html",
            "label": "Cutting Office Tools",
            "section": "Shop by Category",
        },
        "office-school-supplies-cultural-creations-and-gifts": {
            "url": "https://us.shein.com/Cultural-Creations-And-Gifts-c-12203.html",
            "label": "Cultural Creations And " "Gifts",
            "section": "Shop by Category",
        },
        "office-school-supplies-markers-highlighters": {
            "url": "https://us.shein.com/Markers-Highlighters-c-4113.html",
            "label": "Markers & Highlighters",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-pens-refills": {
            "url": "https://us.shein.com/Pens-Refills-c-4115.html",
            "label": "Pens & Refills",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-pencils": {
            "url": "https://us.shein.com/Pencils-c-4108.html",
            "label": "Pencils",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-erasers-correction-products": {
            "url": "https://us.shein.com/Erasers-Correction-Products-c-4111.html",
            "label": "Erasers & Correction " "Products",
            "section": "Writing & Correction " "Supplies",
        },
        "office-school-supplies-pencil-sharpener": {
            "url": "https://us.shein.com/Pencil-Sharpeners-c-3919.html",
            "label": "Pencil Sharpener",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-multi-function-pens": {
            "url": "https://us.shein.com/Multi-Function-Pens-c-6814.html",
            "label": "Multi-function Pens",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-fineliner-pens": {
            "url": "https://us.shein.com/Fineliner-Pens-c-6815.html",
            "label": "Fineliner Pens",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-smart-pens": {
            "url": "https://us.shein.com/Smart-Pens-c-6812.html",
            "label": "Smart Pens",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-electric-pencil-sharpeners": {
            "url": "https://us.shein.com/Electric-Pencil-Sharpeners-c-6816.html",
            "label": "Electric Pencil Sharpeners",
            "section": "Writing & Correction " "Supplies",
        },
        "office-school-supplies-pen-cover-pen-grip": {
            "url": "https://us.shein.com/Pen-Cover-Pen-Grip-c-3920.html",
            "label": "Pen Cover & Pen Grip",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-rollerball-pens": {
            "url": "https://us.shein.com/Rollerball-Pens-c-6813.html",
            "label": "Rollerball Pens",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-drawing-tablets": {
            "url": "https://us.shein.com/Drawing-Tablets-c-6084.html",
            "label": "Drawing Tablets",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-ink-supplies": {
            "url": "https://us.shein.com/Ink-Supplies-c-5071.html",
            "label": "Ink Supplies",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-electric-erasers": {
            "url": "https://us.shein.com/Electric-Erasers-c-6817.html",
            "label": "Electric Erasers",
            "section": "Writing & Correction Supplies",
        },
        "office-school-supplies-notebooks": {
            "url": "https://us.shein.com/Notebooks-c-1965.html",
            "label": "Notebooks",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-binders": {
            "url": "https://us.shein.com/Binders-c-4149.html",
            "label": "Binders",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-planners": {
            "url": "https://us.shein.com/Planners-c-4148.html",
            "label": "Planners",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-sticky-notes": {
            "url": "https://us.shein.com/Sticky-Notes-c-2272.html",
            "label": "Sticky Notes",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-customized-notebooks": {
            "url": "https://us.shein.com/Customized-Notebooks-c-9827.html",
            "label": "Customized Notebooks",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-memo-pads": {
            "url": "https://us.shein.com/Memo-Pads-c-3922.html",
            "label": "Memo Pads",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-filler-paper": {
            "url": "https://us.shein.com/Filler-Paper-c-4147.html",
            "label": "Filler Paper",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-account-books": {
            "url": "https://us.shein.com/Account-Books-c-8319.html",
            "label": "Account Books",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-padfolio": {
            "url": "https://us.shein.com/Padfolio-c-6418.html",
            "label": "Padfolio",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-notebook-sets": {
            "url": "https://us.shein.com/Notebook-Sets-c-8321.html",
            "label": "Notebook Sets",
            "section": "Notebooks & Writing Pads",
        },
        "office-school-supplies-painting-drawing-supplies": {
            "url": "https://us.shein.com/Painting-Drawing-Supplies-c-4171.html",
            "label": "Painting & Drawing Supplies",
            "section": "Art Supplies",
        },
        "office-school-supplies-photo-album": {
            "url": "https://us.shein.com/Photo-Albums-c-4184.html",
            "label": "Photo Album",
            "section": "Art Supplies",
        },
        "office-school-supplies-scrapbooking-stamping-suppliers": {
            "url": "https://us.shein.com/Scrapbooking-Stamping-c-4170.html",
            "label": "Scrapbooking & " "Stamping Suppliers",
            "section": "Art Supplies",
        },
        "office-school-supplies-cards-card-stock": {
            "url": "https://us.shein.com/Cards-Card-Stock-c-8268.html",
            "label": "Cards & Card Stock",
            "section": "Art Supplies",
        },
        "office-school-supplies-palette-tools": {
            "url": "https://us.shein.com/Palette-Tools-c-6432.html",
            "label": "Palette Tools",
            "section": "Art Supplies",
        },
        "office-school-supplies-arts-accessories": {
            "url": "https://us.shein.com/Arts-Accessories-c-8278.html",
            "label": "Arts Accessories",
            "section": "Art Supplies",
        },
        "office-school-supplies-stationery-gift-sets": {
            "url": "https://us.shein.com/Stationery-Gift-Sets-c-4183.html",
            "label": "Stationery Gift Sets",
            "section": "Art Supplies",
        },
        "office-school-supplies-pastel-paper": {
            "url": "https://us.shein.com/Pastel-Paper-c-6832.html",
            "label": "Pastel Paper",
            "section": "Art Supplies",
        },
        "office-school-supplies-watercolor-paper": {
            "url": "https://us.shein.com/Watercolor-Paper-c-6826.html",
            "label": "Watercolor Paper",
            "section": "Art Supplies",
        },
        "office-school-supplies-classroom-decoration": {
            "url": "https://us.shein.com/Classroom-Decoration-c-8284.html",
            "label": "Classroom Decoration",
            "section": "Art Supplies",
        },
        "office-school-supplies-sketch-charcoal-pencils": {
            "url": "https://us.shein.com/Sketch-Charcoal-Pencils-c-6828.html",
            "label": "Sketch Charcoal Pencils",
            "section": "Art Supplies",
        },
        "office-school-supplies-electric-spray-pens": {
            "url": "https://us.shein.com/Electric-Spray-Pens-c-6835.html",
            "label": "Electric Spray Pens",
            "section": "Art Supplies",
        },
        "office-school-supplies-chinese-painting-pigment": {
            "url": "https://us.shein.com/Chinese-Painting-Pigment-c-6837.html",
            "label": "Chinese Painting Pigment",
            "section": "Art Supplies",
        },
        "office-school-supplies-penholders": {
            "url": "https://us.shein.com/Penholders-c-6430.html",
            "label": "Penholders",
            "section": "Art Supplies",
        },
        "office-school-supplies-textured-paper-tape": {
            "url": "https://us.shein.com/Textured-Paper-Tape-c-11502.html",
            "label": "Textured Paper Tape",
            "section": "Art Supplies",
        },
        "office-school-supplies-stretched-canvas": {
            "url": "https://us.shein.com/Stretched-Canvas-c-6428.html",
            "label": "Stretched Canvas",
            "section": "Art Supplies",
        },
        "office-school-supplies-plaster-models": {
            "url": "https://us.shein.com/Plaster-Models-c-6831.html",
            "label": "Plaster Models",
            "section": "Art Supplies",
        },
        "office-school-supplies-calligraphy-supplies": {
            "url": "https://us.shein.com/Calligraphy-Supplies-c-6473.html",
            "label": "Calligraphy Supplies",
            "section": "Art Supplies",
        },
        "office-school-supplies-painting-paper": {
            "url": "https://us.shein.com/Painting-Paper-c-6833.html",
            "label": "Painting Paper",
            "section": "Art Supplies",
        },
        "office-school-supplies-felt-pads": {
            "url": "https://us.shein.com/Felt-Pads-c-8267.html",
            "label": "Felt Pads",
            "section": "Art Supplies",
        },
        "office-school-supplies-assorted-stickers": {
            "url": "https://us.shein.com/Assorted-Stickers-c-3908.html",
            "label": "Assorted Stickers",
            "section": "Stationery Stickers",
        },
        "office-school-supplies-label-stickers": {
            "url": "https://us.shein.com/Label-Stickers-c-4124.html",
            "label": "Label Stickers",
            "section": "Stationery Stickers",
        },
        "office-school-supplies-customized-stationery-stickers": {
            "url": "https://us.shein.com/Customized-Stationery-Stickers-c-13525.html",
            "label": "Customized Stationery " "Stickers",
            "section": "Stationery Stickers",
        },
        "office-school-supplies-pen-pencil-marker-cases": {
            "url": "https://us.shein.com/Pen,Pencil-Marker-Cases-c-4154.html",
            "label": "Pen, Pencil & Marker Cases",
            "section": "Filing Products",
        },
        "office-school-supplies-file-jackets-file-pockets": {
            "url": "https://us.shein.com/File-Jackets-File-Pockets-c-2271.html",
            "label": "File Jackets & File Pockets",
            "section": "Filing Products",
        },
        "office-school-supplies-loose-leaf-covers": {
            "url": "https://us.shein.com/Loose-leaf-Covers-c-4159.html",
            "label": "Loose-leaf Covers",
            "section": "Filing Products",
        },
        "office-school-supplies-customized-pen-pencil-marker-cases": {
            "url": "https://us.shein.com/Customized-Pen,Pencil-Marker-Cases-c-9163.html",
            "label": "Customized " "Pen,Pencil & " "Marker Cases",
            "section": "Filing Products",
        },
        "office-school-supplies-customized-file-jackets-file-pockets": {
            "url": "https://us.shein.com/Customized-File-Jackets-File-Pockets-c-9825.html",
            "label": "Customized File " "Jackets & File " "Pockets",
            "section": "Filing " "Products",
        },
        "office-school-supplies-expandable-files": {
            "url": "https://us.shein.com/Expandable-Files-c-4160.html",
            "label": "Expandable Files",
            "section": "Filing Products",
        },
        "office-school-supplies-files-box-rack": {
            "url": "https://us.shein.com/Files-Box-Rack-c-11505.html",
            "label": "Files Box & Rack",
            "section": "Filing Products",
        },
        "office-school-supplies-book-covers": {
            "url": "https://us.shein.com/Book-Covers-c-4158.html",
            "label": "Book Covers",
            "section": "Filing Products",
        },
        "office-school-supplies-hanging-file-folders": {
            "url": "https://us.shein.com/Hanging-File-Folders-c-6422.html",
            "label": "Hanging File Folders",
            "section": "Filing Products",
        },
        "office-school-supplies-mouse-mat": {
            "url": "https://us.shein.com/Mouse-Mat-c-5147.html",
            "label": "Mouse Mat",
            "section": "Desk Accessories",
        },
        "office-school-supplies-stationery-storage-boxes": {
            "url": "https://us.shein.com/Stationery-Storage-Boxes-c-3916.html",
            "label": "Stationery Storage Boxes",
            "section": "Desk Accessories",
        },
        "office-school-supplies-desktop-decorations": {
            "url": "https://us.shein.com/Desktop-Decorations-c-11496.html",
            "label": "Desktop Decorations",
            "section": "Desk Accessories",
        },
        "office-school-supplies-desktop-bookshelf": {
            "url": "https://us.shein.com/Desktop-Bookshelf-c-6091.html",
            "label": "Desktop Bookshelf",
            "section": "Desk Accessories",
        },
        "office-school-supplies-cable-organizers": {
            "url": "https://us.shein.com/Cable-Organizers-c-6425.html",
            "label": "Cable Organizers",
            "section": "Desk Accessories",
        },
        "office-school-supplies-desk-mat": {
            "url": "https://us.shein.com/Desk-Mat-c-5146.html",
            "label": "Desk Mat",
            "section": "Desk Accessories",
        },
        "office-school-supplies-desk-sets": {
            "url": "https://us.shein.com/Desk-Sets-c-8288.html",
            "label": "Desk Sets",
            "section": "Desk Accessories",
        },
        "office-school-supplies-office-desk-accessories": {
            "url": "https://us.shein.com/Office-Desk-Accessories-c-11495.html",
            "label": "Office Desk Accessories",
            "section": "Desk Accessories",
        },
        "office-school-supplies-customized-bookends-book-stands": {
            "url": "https://us.shein.com/Customized-Bookends-Book-Stands-c-12510.html",
            "label": "Customized Bookends & " "Book Stands",
            "section": "Desk Accessories",
        },
        "office-school-supplies-file-trays": {
            "url": "https://us.shein.com/File-Trays-c-4162.html",
            "label": "File Trays",
            "section": "Desk Accessories",
        },
        "office-school-supplies-key-holder-keychain-organizers": {
            "url": "https://us.shein.com/Key-Holder-Keychain-Organizers-c-6424.html",
            "label": "Key Holder & Keychain " "Organizers",
            "section": "Desk Accessories",
        },
        "office-school-supplies-bookends-book-stands": {
            "url": "https://us.shein.com/Bookends-Book-Stands-c-3913.html",
            "label": "Bookends & Book Stands",
            "section": "Desk Accessories",
        },
        "office-school-supplies-customized-desk-mat-mouse-mat": {
            "url": "https://us.shein.com/Customized-Desk-Mat-Mouse-Mat-c-13526.html",
            "label": "Customized Desk Mat & " "Mouse Mat",
            "section": "Desk Accessories",
        },
        "office-school-supplies-business-card-holders": {
            "url": "https://us.shein.com/Business-Card-Holders-c-3915.html",
            "label": "Business Card Holders",
            "section": "Desk Accessories",
        },
        "office-school-supplies-wastepaper-baskets": {
            "url": "https://us.shein.com/Wastepaper-Baskets-c-8298.html",
            "label": "Wastepaper Baskets",
            "section": "Desk Accessories",
        },
        "office-school-supplies-copyholders-book-stands": {
            "url": "https://us.shein.com/Copyholders-Book-Stands-c-6825.html",
            "label": "Copyholders & Book Stands",
            "section": "Desk Accessories",
        },
        "office-school-supplies-handing-storage-bag": {
            "url": "https://us.shein.com/Handing-Storage-Bag-c-11493.html",
            "label": "Handing Storage Bag",
            "section": "Desk Accessories",
        },
        "office-school-supplies-office-accessories": {
            "url": "https://us.shein.com/Office-Accessories-c-8291.html",
            "label": "Office Accessories",
            "section": "Desk Accessories",
        },
        "office-school-supplies-letter-holders": {
            "url": "https://us.shein.com/Letter-Holders-c-8286.html",
            "label": "Letter Holders",
            "section": "Desk Accessories",
        },
        "office-school-supplies-badge-holder-accessories": {
            "url": "https://us.shein.com/Badge-Holder-Accessories-c-3923.html",
            "label": "Badge Holder & Accessories",
            "section": "Labels, Indexes & Stamps",
        },
        "office-school-supplies-bookmarks": {
            "url": "https://us.shein.com/Bookmarks-c-3914.html",
            "label": "Bookmarks",
            "section": "Labels, Indexes & Stamps",
        },
        "office-school-supplies-customized-bookmarks": {
            "url": "https://us.shein.com/Customized-Bookmarks-c-12509.html",
            "label": "Customized Bookmarks",
            "section": "Labels, Indexes & Stamps",
        },
        "office-school-supplies-file-folder-labels": {
            "url": "https://us.shein.com/File-Folder-Labels-c-4152.html",
            "label": "File Folder Labels",
            "section": "Labels, Indexes & Stamps",
        },
        "office-school-supplies-universal-label": {
            "url": "https://us.shein.com/Universal-Label-c-11494.html",
            "label": "Universal Label",
            "section": "Labels, Indexes & Stamps",
        },
        "office-school-supplies-inkpads": {
            "url": "https://us.shein.com/Inkpads-c-6420.html",
            "label": "Inkpads",
            "section": "Labels, Indexes & Stamps",
        },
        "office-school-supplies-calendars": {
            "url": "https://us.shein.com/Calendars-c-3917.html",
            "label": "Calendars",
            "section": "Calendars & Cards",
        },
        "office-school-supplies-greeting-cards": {
            "url": "https://us.shein.com/Greeting-Cards-c-8272.html",
            "label": "Greeting Cards",
            "section": "Calendars & Cards",
        },
        "office-school-supplies-postcards": {
            "url": "https://us.shein.com/Postcards-c-8269.html",
            "label": "Postcards",
            "section": "Calendars & Cards",
        },
        "office-school-supplies-business-cards": {
            "url": "https://us.shein.com/Business-Cards-c-4169.html",
            "label": "Business Cards",
            "section": "Calendars & Cards",
        },
        "office-school-supplies-card-holder": {
            "url": "https://us.shein.com/Card-Holder-c-6426.html",
            "label": "Card Holder",
            "section": "Calendars & Cards",
        },
        "office-school-supplies-material-paper": {
            "url": "https://us.shein.com/Material-Paper-c-3907.html",
            "label": "Material Paper",
            "section": "Paper",
        },
        "office-school-supplies-copy-multipurpose-paper": {
            "url": "https://us.shein.com/Copy-Multipurpose-Paper-c-4141.html",
            "label": "Copy & Multipurpose Paper",
            "section": "Paper",
        },
        "office-school-supplies-self-adhesive-paper": {
            "url": "https://us.shein.com/Self-Adhesive-Paper-c-6408.html",
            "label": "Self-adhesive Paper",
            "section": "Paper",
        },
        "office-school-supplies-photo-paper": {
            "url": "https://us.shein.com/Photo-Paper-c-6410.html",
            "label": "Photo Paper",
            "section": "Paper",
        },
        "office-school-supplies-letter-paper": {
            "url": "https://us.shein.com/Letter-Paper-c-4140.html",
            "label": "Letter Paper",
            "section": "Paper",
        },
        "office-school-supplies-kraft-paper": {
            "url": "https://us.shein.com/Kraft-paper-c-6411.html",
            "label": "Kraft paper",
            "section": "Paper",
        },
        "office-school-supplies-a4-paper": {
            "url": "https://us.shein.com/A4-Paper-c-6416.html",
            "label": "A4 Paper",
            "section": "Paper",
        },
        "office-school-supplies-transfer-paper": {
            "url": "https://us.shein.com/Transfer-Paper-c-6406.html",
            "label": "Transfer Paper",
            "section": "Paper",
        },
        "office-school-supplies-scratch-paper": {
            "url": "https://us.shein.com/Scratch-Paper-c-4139.html",
            "label": "Scratch Paper",
            "section": "Paper",
        },
        "office-school-supplies-thermal-fax-paper": {
            "url": "https://us.shein.com/Thermal-Fax-Paper-c-6407.html",
            "label": "Thermal Fax Paper",
            "section": "Paper",
        },
        "office-school-supplies-carbonless-paper": {
            "url": "https://us.shein.com/Carbonless-Paper-c-6414.html",
            "label": "Carbonless Paper",
            "section": "Paper",
        },
        "office-school-supplies-carbon-paper": {
            "url": "https://us.shein.com/Carbon-Paper-c-6415.html",
            "label": "Carbon Paper",
            "section": "Paper",
        },
        "office-school-supplies-rubbing-paper": {
            "url": "https://us.shein.com/Rubbing-Paper-c-6409.html",
            "label": "Rubbing Paper",
            "section": "Paper",
        },
        "office-school-supplies-cash-register-paper": {
            "url": "https://us.shein.com/Cash-Register-Paper-c-6413.html",
            "label": "Cash Register Paper",
            "section": "Paper",
        },
        "office-school-supplies-masking-tape": {
            "url": "https://us.shein.com/Masking-Tape-c-3906.html",
            "label": "Masking Tape",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-liquid-glue": {
            "url": "https://us.shein.com/Liquid-Glue-c-6819.html",
            "label": "Liquid Glue",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-double-sided-tape": {
            "url": "https://us.shein.com/Double-Sided-Tape-c-6820.html",
            "label": "Double Sided Tape",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-tape-dispenser": {
            "url": "https://us.shein.com/Tape-Dispenser-c-4122.html",
            "label": "Tape Dispenser",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-office-adhesive-tape": {
            "url": "https://us.shein.com/Office-Adhesive-Tape-c-4121.html",
            "label": "Office Adhesive Tape",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-solid-gum": {
            "url": "https://us.shein.com/Solid-Gum-c-4450.html",
            "label": "Solid Gum",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-nano-tape": {
            "url": "https://us.shein.com/Nano-Tape-c-6818.html",
            "label": "Nano Tape",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-rubber-bands": {
            "url": "https://us.shein.com/Rubber-Bands-c-6386.html",
            "label": "Rubber Bands",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-twine": {
            "url": "https://us.shein.com/Twine-c-13477.html",
            "label": "Twine",
            "section": "Tapes, Adhesives & Fasteners",
        },
        "office-school-supplies-office-furniture": {
            "url": "https://us.shein.com/Office-Furniture-c-8300.html",
            "label": "Office Furniture",
            "section": "Office Furniture & Accessories",
        },
        "office-school-supplies-office-supplies-accessories": {
            "url": "https://us.shein.com/Office-Supplies-Accessories-c-8322.html",
            "label": "Office Supplies " "Accessories",
            "section": "Office Furniture & " "Accessories",
        },
        "office-school-supplies-hole-puncher": {
            "url": "https://us.shein.com/Hole-Puncher-c-4144.html",
            "label": "Hole Puncher",
            "section": "Office Binding Supplies",
        },
        "office-school-supplies-clips": {
            "url": "https://us.shein.com/Clips-c-3918.html",
            "label": "Clips",
            "section": "Office Binding Supplies",
        },
        "office-school-supplies-stapler-staples": {
            "url": "https://us.shein.com/Stapler-Staples-c-1966.html",
            "label": "Stapler & Staples",
            "section": "Office Binding Supplies",
        },
        "office-school-supplies-pins-tacks": {
            "url": "https://us.shein.com/Pins-Tacks-c-6823.html",
            "label": "Pins & Tacks",
            "section": "Office Binding Supplies",
        },
        "office-school-supplies-book-rings-loose-leaf-binders": {
            "url": "https://us.shein.com/Book-Rings-Loose-Leaf-Binders-c-4146.html",
            "label": "Book Rings & Loose Leaf " "Binders",
            "section": "Office Binding " "Supplies",
        },
        "office-school-supplies-plastic-packaging-supplies": {
            "url": "https://us.shein.com/Plastic-Packaging-Supplies-c-11507.html",
            "label": "Plastic Packaging Supplies",
            "section": "Office Binding Supplies",
        },
        "office-school-supplies-staple-remover": {
            "url": "https://us.shein.com/Staple-Remover-c-4143.html",
            "label": "Staple Remover",
            "section": "Office Binding Supplies",
        },
        "office-school-supplies-paper-envelopes": {
            "url": "https://us.shein.com/Paper-Envelopes-c-3655.html",
            "label": "Paper Envelopes",
            "section": "Mail & Shipping Supplies",
        },
        "office-school-supplies-bubble-mailers": {
            "url": "https://us.shein.com/Bubble-Mailers-c-4151.html",
            "label": "Bubble Mailers",
            "section": "Mail & Shipping Supplies",
        },
        "office-school-supplies-gift-packaging-accessories": {
            "url": "https://us.shein.com/Gift-Packaging-Accessories-c-11504.html",
            "label": "Gift Packaging Accessories",
            "section": "Mail & Shipping " "Supplies",
        },
        "office-school-supplies-box-mailers": {
            "url": "https://us.shein.com/Box-Mailers-c-8334.html",
            "label": "Box Mailers",
            "section": "Mail & Shipping Supplies",
        },
        "office-school-supplies-mail-document-bags": {
            "url": "https://us.shein.com/Mail-Document-Bags-c-8333.html",
            "label": "Mail Document Bags",
            "section": "Mail & Shipping Supplies",
        },
        "office-school-supplies-backpacks": {
            "url": "https://us.shein.com/Backpacks-c-8295.html",
            "label": "Backpacks",
            "section": "Carrying Cases",
        },
        "office-school-supplies-laptop-storage": {
            "url": "https://us.shein.com/Laptop-Storage-c-4920.html",
            "label": "Laptop Storage",
            "section": "Carrying Cases",
        },
        "office-school-supplies-shoulder-bags": {
            "url": "https://us.shein.com/Shoulder-Bags-c-8293.html",
            "label": "Shoulder Bags",
            "section": "Carrying Cases",
        },
        "office-school-supplies-student-lunch-bag": {
            "url": "https://us.shein.com/Student-Lunch-Bag-c-11503.html",
            "label": "Student Lunch Bag",
            "section": "Carrying Cases",
        },
        "office-school-supplies-electronics-organizers": {
            "url": "https://us.shein.com/Electronics-Organizers-c-8292.html",
            "label": "Electronics Organizers",
            "section": "Carrying Cases",
        },
        "office-school-supplies-document-bags": {
            "url": "https://us.shein.com/Document-Bags-c-4161.html",
            "label": "Document Bags",
            "section": "Carrying Cases",
        },
        "office-school-supplies-office-calculators": {
            "url": "https://us.shein.com/Office-Calculators-c-5148.html",
            "label": "Office Calculators",
            "section": "School & Educational Supplies",
        },
        "office-school-supplies-drafting-supplies": {
            "url": "https://us.shein.com/Drafting-Supplies-c-4130.html",
            "label": "Drafting Supplies",
            "section": "School & Educational Supplies",
        },
        "office-school-supplies-teaching-resources-accessories": {
            "url": "https://us.shein.com/Teaching-Resources-Accessories-c-6387.html",
            "label": "Teaching Resources & " "Accessories",
            "section": "School & Educational " "Supplies",
        },
        "office-school-supplies-copybook": {
            "url": "https://us.shein.com/Copybook-c-6438.html",
            "label": "Copybook",
            "section": "School & Educational Supplies",
        },
        "office-school-supplies-laboratory-supplies-equipment": {
            "url": "https://us.shein.com/Laboratory-Supplies-Equipment-c-6390.html",
            "label": "Laboratory Supplies & " "Equipment",
            "section": "School & Educational " "Supplies",
        },
        "office-school-supplies-chalk": {
            "url": "https://us.shein.com/Chalk-c-6397.html",
            "label": "Chalk",
            "section": "School & Educational Supplies",
        },
        "office-school-supplies-educational-equipment": {
            "url": "https://us.shein.com/Educational-Equipment-c-6396.html",
            "label": "Educational Equipment",
            "section": "School & Educational " "Supplies",
        },
        "office-school-supplies-geometry-templates": {
            "url": "https://us.shein.com/Geometry-Templates-c-6822.html",
            "label": "Geometry Templates",
            "section": "School & Educational Supplies",
        },
        "office-school-supplies-protractor": {
            "url": "https://us.shein.com/Protractor-c-6821.html",
            "label": "Protractor",
            "section": "School & Educational Supplies",
        },
        "office-school-supplies-cutting-mat": {
            "url": "https://us.shein.com/Cutting-Mats-c-4165.html",
            "label": "Cutting Mat",
            "section": "Cutting Office Tools",
        },
        "office-school-supplies-scissors": {
            "url": "https://us.shein.com/Scissors-c-4167.html",
            "label": "Scissors",
            "section": "Cutting Office Tools",
        },
        "office-school-supplies-utility-knife": {
            "url": "https://us.shein.com/Utility-Knife-c-4166.html",
            "label": "Utility Knife",
            "section": "Cutting Office Tools",
        },
        "office-school-supplies-customized-tape-measure": {
            "url": "https://us.shein.com/Customized-Tape-Measure-c-12505.html",
            "label": "Customized Tape Measure",
            "section": "Cutting Office Tools",
        },
        "office-school-supplies-letter-knife": {
            "url": "https://us.shein.com/Letter-Knife-c-11509.html",
            "label": "Letter Knife",
            "section": "Cutting Office Tools",
        },
        "office-school-supplies-arts-and-crafts-ornaments": {
            "url": "https://us.shein.com/Arts-And-Crafts-Ornaments-c-12210.html",
            "label": "Arts And Crafts Ornaments",
            "section": "Cultural Creations And " "Gifts",
        },
        "office-school-supplies-medals-trophies-certificates": {
            "url": "https://us.shein.com/Medals,-Trophies,-Certificates-c-12219.html",
            "label": "Medals, Trophies, " "Certificates",
            "section": "Cultural Creations And " "Gifts",
        },
        "office-school-supplies-advertising-fan": {
            "url": "https://us.shein.com/Advertising-Fan-c-12211.html",
            "label": "Advertising Fan",
            "section": "Cultural Creations And Gifts",
        },
    },
    "pet-supplies": {
        "pet-supplies": {
            "url": "https://us.shein.com/RecommendSelection/Pet-Supplies-sc-017172974.html",
            "label": "Pet Supplies",
            "section": "Top category",
        },
        "pet-supplies-view-all": {
            "url": "https://us.shein.com/Pet-Supplies-c-2400.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "pet-supplies-fall-winter": {
            "url": "https://us.shein.com/recommend/Fall-Winter-sc-10050050289.html",
            "label": "Fall & Winter",
            "section": "Shop by Category",
        },
        "pet-supplies-new-in": {
            "url": "https://us.shein.com/new/New-pet-products-sc-0021155119.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-clothing": {
            "url": "https://us.shein.com/Pet-Clothing-c-2875.html",
            "label": "Pet Clothing",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-bedding": {
            "url": "https://us.shein.com/Pet-Bedding-c-2894.html",
            "label": "Pet Bedding",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-toys": {
            "url": "https://us.shein.com/Pet-Toys-c-2893.html",
            "label": "Pet Toys",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-furniture": {
            "url": "https://us.shein.com/Pet-Furniture-c-4056.html",
            "label": "Pet Furniture",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-collars-leashes-harnesses-sets": {
            "url": "https://us.shein.com/Pet-Collars,-Leashes-Harnesses-c-2949.html",
            "label": "Pet Collars, Leashes & Harnesses Sets",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-cleaning": {
            "url": "https://us.shein.com/Pet-Cleaning-c-2946.html",
            "label": "Pet Cleaning",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-accessories": {
            "url": "https://us.shein.com/Pet-Accessories-c-2892.html",
            "label": "Pet Accessories",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-bowls-feeders": {
            "url": "https://us.shein.com/Pet-Bowls-Feeders-c-2896.html",
            "label": "Pet Bowls & Feeders",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-outdoor-gear": {
            "url": "https://us.shein.com/Pet-Outdoor-Gear-c-2947.html",
            "label": "Pet Outdoor Gear",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-grooming": {
            "url": "https://us.shein.com/Pet-Grooming-c-2951.html",
            "label": "Pet Grooming",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-smart-appliances": {
            "url": "https://us.shein.com/Pet-Appliances-c-3880.html",
            "label": "Pet Smart Appliances",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-food": {
            "url": "https://us.shein.com/Pet-Food-c-9681.html",
            "label": "Pet Food",
            "section": "Shop by Category",
        },
        "pet-supplies-small-animal-supplies": {
            "url": "https://us.shein.com/Small-Animal-Supplies-c-4040.html",
            "label": "Small Animal Supplies",
            "section": "Shop by Category",
        },
        "pet-supplies-bird-supplies": {
            "url": "https://us.shein.com/Bird-Supplies-c-4028.html",
            "label": "Bird Supplies",
            "section": "Shop by Category",
        },
        "pet-supplies-customized-pet-supplies": {
            "url": "https://us.shein.com/Customized-Pet-Supplies-c-9815.html",
            "label": "Customized Pet Supplies",
            "section": "Shop by Category",
        },
        "pet-supplies-fish-aquarium-supplies": {
            "url": "https://us.shein.com/Fish-Aquarium-Supplies-c-4035.html",
            "label": "Fish & Aquarium Supplies",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-memorial": {
            "url": "https://us.shein.com/Pet-Memorial-c-4053.html",
            "label": "Pet Memorial",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-health-care-tools": {
            "url": "https://us.shein.com/Pet-Health-Care-c-2955.html",
            "label": "Pet Health Care Tools",
            "section": "Shop by Category",
        },
        "pet-supplies-horses": {
            "url": "https://us.shein.com/Horses-c-6327.html",
            "label": "Horses",
            "section": "Shop by Category",
        },
        "pet-supplies-reptile-amphibian-supplies": {
            "url": "https://us.shein.com/Reptile-Amphibian-Supplies-c-4043.html",
            "label": "Reptile & Amphibian Supplies",
            "section": "Shop by Category",
        },
        "pet-supplies-farm-animal-supplies": {
            "url": "https://us.shein.com/Farm-Animal-Supplies-c-4047.html",
            "label": "Farm Animal Supplies",
            "section": "Shop by Category",
        },
        "pet-supplies-pet-tops": {
            "url": "https://us.shein.com/Pet-Tops-c-2877.html",
            "label": "Pet Tops",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-dresses": {
            "url": "https://us.shein.com/Pet-Dresses-c-2876.html",
            "label": "Pet Dresses",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-sweatshirts-hoodies": {
            "url": "https://us.shein.com/Pet-Sweatshirts-Hoodies-c-2882.html",
            "label": "Pet Sweatshirts & Hoodies",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-jumpsuits": {
            "url": "https://us.shein.com/Pet-Jumpsuits-c-2884.html",
            "label": "Pet Jumpsuits",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-functional-clothing": {
            "url": "https://us.shein.com/Pet-Functional-Clothing-c-2887.html",
            "label": "Pet Functional Clothing",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-pajamas": {
            "url": "https://us.shein.com/Pet-Pajamas-c-2885.html",
            "label": "Pet Pajamas",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-coats-jackets": {
            "url": "https://us.shein.com/Pet-Coats-Jackets-c-2883.html",
            "label": "Pet Coats & Jackets",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-sweaters": {
            "url": "https://us.shein.com/Pet-Sweaters-c-2881.html",
            "label": "Pet Sweaters",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-costumes": {
            "url": "https://us.shein.com/Pet-Costumes-c-2886.html",
            "label": "Pet Costumes",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-clothing-set": {
            "url": "https://us.shein.com/Pet-Clothing-Set-c-3339.html",
            "label": "Pet Clothing Set",
            "section": "Pet Clothing",
        },
        "pet-supplies-pet-bed-crate-mat": {
            "url": "https://us.shein.com/Pet-Bed-Crate-Mat-c-2921.html",
            "label": "Pet Bed & Crate Mat",
            "section": "Pet Bedding",
        },
        "pet-supplies-pet-blankets-covers": {
            "url": "https://us.shein.com/Pet-Blankets-Covers-c-2922.html",
            "label": "Pet Blankets & Covers",
            "section": "Pet Bedding",
        },
        "pet-supplies-pet-hammock-window-perches": {
            "url": "https://us.shein.com/Pet-Hammock/Window-Perches-c-4059.html",
            "label": "Pet Hammock & Window Perches",
            "section": "Pet Bedding",
        },
        "pet-supplies-cat-teasers": {
            "url": "https://us.shein.com/Cat-Teasers-c-2910.html",
            "label": "Cat Teasers",
            "section": "Pet Toys",
        },
        "pet-supplies-pet-plush-toys": {
            "url": "https://us.shein.com/Pet-Plush-Toys-c-2980.html",
            "label": "Pet Plush Toys",
            "section": "Pet Toys",
        },
        "pet-supplies-pet-chew-toys": {
            "url": "https://us.shein.com/Pet-Chew-Toys-c-2916.html",
            "label": "Pet Chew Toys",
            "section": "Pet Toys",
        },
        "pet-supplies-pet-sound-toys": {
            "url": "https://us.shein.com/Pet-Sound-Toys-c-2918.html",
            "label": "Pet Sound Toys",
            "section": "Pet Toys",
        },
        "pet-supplies-pet-chasing-toys": {
            "url": "https://us.shein.com/Pet-Chasing-Toys-c-2913.html",
            "label": "Pet Chasing Toys",
            "section": "Pet Toys",
        },
        "pet-supplies-pet-training-puzzle-toys": {
            "url": "https://us.shein.com/Pet-Training-Puzzle-Toys-c-2917.html",
            "label": "Pet Training & Puzzle Toys",
            "section": "Pet Toys",
        },
        "pet-supplies-cat-tunnels": {
            "url": "https://us.shein.com/Cat-Tunnels-c-2919.html",
            "label": "Cat Tunnels",
            "section": "Pet Toys",
        },
        "pet-supplies-pet-toy-sets": {
            "url": "https://us.shein.com/Pet-Toy-Sets-c-2979.html",
            "label": "Pet Toy Sets",
            "section": "Pet Toys",
        },
        "pet-supplies-cat-scratchers": {
            "url": "https://us.shein.com/Cat-Scratchers-c-2912.html",
            "label": "Cat Scratchers",
            "section": "Pet Furniture",
        },
        "pet-supplies-pet-furniture-tools": {
            "url": "https://us.shein.com/Pet-Furniture-Tools-c-4057.html",
            "label": "Pet Furniture Tools",
            "section": "Pet Furniture",
        },
        "pet-supplies-pet-furniture-protectors": {
            "url": "https://us.shein.com/Pet-Furniture-Protectors-c-2923.html",
            "label": "Pet Furniture Protectors",
            "section": "Pet Furniture",
        },
        "pet-supplies-cat-trees-condos": {
            "url": "https://us.shein.com/Cat-Trees-Condos-c-3848.html",
            "label": "Cat Trees & Condos",
            "section": "Pet Furniture",
        },
        "pet-supplies-pet-houses-cages": {
            "url": "https://us.shein.com/Pet-Houses-Cages-c-4058.html",
            "label": "Pet Houses & Cages",
            "section": "Pet Furniture",
        },
        "pet-supplies-pet-collars": {
            "url": "https://us.shein.com/Pet-Collars-c-2963.html",
            "label": "Pet Collars",
            "section": "Pet Collars, Leashes & Harnesses Sets",
        },
        "pet-supplies-pet-leashes": {
            "url": "https://us.shein.com/Pet-Leashes-c-2964.html",
            "label": "Pet Leashes",
            "section": "Pet Collars, Leashes & Harnesses Sets",
        },
        "pet-supplies-pet-harnesses": {
            "url": "https://us.shein.com/Pet-Harnesses-c-2965.html",
            "label": "Pet Harnesses",
            "section": "Pet Collars, Leashes & Harnesses Sets",
        },
        "pet-supplies-pet-muzzles": {
            "url": "https://us.shein.com/Pet-Muzzles-c-2966.html",
            "label": "Pet Muzzles",
            "section": "Pet Collars, Leashes & Harnesses Sets",
        },
        "pet-supplies-pet-id-tags": {
            "url": "https://us.shein.com/Pet-ID-Tags-c-2967.html",
            "label": "Pet ID Tags",
            "section": "Pet Collars, Leashes & Harnesses Sets",
        },
        "pet-supplies-pet-collars-leashes-harnesses-sets-2982": {
            "url": "https://us.shein.com/Pet-Collars,-Leashes-Harnesses-Sets-c-2982.html",
            "label": "Pet Collars, Leashes & Harnesses " "Sets",
            "section": "Pet Collars, Leashes & " "Harnesses Sets",
        },
        "pet-supplies-pet-cleaning-accessories": {
            "url": "https://us.shein.com/Pet-Cleaning-Accessories-c-2959.html",
            "label": "Pet Cleaning Accessories",
            "section": "Pet Cleaning",
        },
        "pet-supplies-pet-poopbags": {
            "url": "https://us.shein.com/Pet-Poopbags-c-2957.html",
            "label": "Pet Poopbags",
            "section": "Pet Cleaning",
        },
        "pet-supplies-pet-toilet": {
            "url": "https://us.shein.com/Litter-Boxes-Litter-Mats-c-2958.html",
            "label": "Pet Toilet",
            "section": "Pet Cleaning",
        },
        "pet-supplies-pet-stain-odor-removers": {
            "url": "https://us.shein.com/Pet-Stain-Odor-Removers-c-4065.html",
            "label": "Pet Stain & Odor Removers",
            "section": "Pet Cleaning",
        },
        "pet-supplies-cat-litter": {
            "url": "https://us.shein.com/Cat-Litter-c-5102.html",
            "label": "Cat Litter",
            "section": "Pet Cleaning",
        },
        "pet-supplies-pet-glasses": {
            "url": "https://us.shein.com/Pet-Glasses-c-2907.html",
            "label": "Pet Glasses",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-shoes-socks": {
            "url": "https://us.shein.com/Pet-Shoes-Socks-c-2897.html",
            "label": "Pet Shoes & Socks",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-hats": {
            "url": "https://us.shein.com/Pet-Hats-c-4063.html",
            "label": "Pet Hats",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-scarves": {
            "url": "https://us.shein.com/Pet-Scarves-c-2900.html",
            "label": "Pet Scarves",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-storage-organization": {
            "url": "https://us.shein.com/Pet-Storage-Organization-c-2908.html",
            "label": "Pet Storage & Organization",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-hair-accessories": {
            "url": "https://us.shein.com/Pet-Hair-Accessories-c-2901.html",
            "label": "Pet Hair Accessories",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-accessories-sets": {
            "url": "https://us.shein.com/Pet-Accessories-Sets-c-2978.html",
            "label": "Pet Accessories Sets",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-bows-ties": {
            "url": "https://us.shein.com/Pet-Bows-Ties-c-2902.html",
            "label": "Pet Bows & Ties",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-bags": {
            "url": "https://us.shein.com/Pet-Bags-c-2903.html",
            "label": "Pet Bags",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-necklaces": {
            "url": "https://us.shein.com/Pet-Necklaces-c-2904.html",
            "label": "Pet Necklaces",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-headwear": {
            "url": "https://us.shein.com/Pet-Headwear-c-2906.html",
            "label": "Pet Headwear",
            "section": "Pet Accessories",
        },
        "pet-supplies-pet-bowls-feeders-2924": {
            "url": "https://us.shein.com/Pet-Bowls-c-2924.html",
            "label": "Pet Bowls & Feeders",
            "section": "Pet Bowls & Feeders",
        },
        "pet-supplies-pet-food-storage-containers-scoops": {
            "url": "https://us.shein.com/Pet-Food-Storage-Containers-Scoops-c-2928.html",
            "label": "Pet Food Storage Containers & Scoops",
            "section": "Pet Bowls & Feeders",
        },
        "pet-supplies-pet-feeders": {
            "url": "https://us.shein.com/Pet-Feeders-c-2925.html",
            "label": "Pet Feeders",
            "section": "Pet Bowls & Feeders",
        },
        "pet-supplies-pet-waterers-fountains": {
            "url": "https://us.shein.com/Pet-Waterers-Fountains-c-2926.html",
            "label": "Pet Waterers & Fountains",
            "section": "Pet Bowls & Feeders",
        },
        "pet-supplies-pet-placemats": {
            "url": "https://us.shein.com/Pet-Placemats-c-2927.html",
            "label": "Pet Placemats",
            "section": "Pet Bowls & Feeders",
        },
        "pet-supplies-pet-vehicle-accessories": {
            "url": "https://us.shein.com/Pet-Vehicle-Accessories-c-2961.html",
            "label": "Pet Vehicle Accessories",
            "section": "Pet Outdoor Gear",
        },
        "pet-supplies-pet-carrier": {
            "url": "https://us.shein.com/Pet-Carrier-c-2960.html",
            "label": "Pet Carrier",
            "section": "Pet Outdoor Gear",
        },
        "pet-supplies-pet-travel-bowls-bottles": {
            "url": "https://us.shein.com/Pet-Travel-Bowls-Bottles-c-2929.html",
            "label": "Pet Travel Bowls & Bottles",
            "section": "Pet Outdoor Gear",
        },
        "pet-supplies-pet-treat-pouch": {
            "url": "https://us.shein.com/Pet-Treat-Pouch-c-2962.html",
            "label": "Pet Treat Pouch",
            "section": "Pet Outdoor Gear",
        },
        "pet-supplies-pet-seat-belts": {
            "url": "https://us.shein.com/Pet-Seat-Belts-c-5997.html",
            "label": "Pet Seat Belts",
            "section": "Pet Outdoor Gear",
        },
        "pet-supplies-pet-outdoor-gear-sets": {
            "url": "https://us.shein.com/Pet-Outdoor-Gear-Sets-c-2981.html",
            "label": "Pet Outdoor Gear Sets",
            "section": "Pet Outdoor Gear",
        },
        "pet-supplies-pet-shower-bath-accessories": {
            "url": "https://us.shein.com/Pet-Shower-Bath-Accessories-c-4061.html",
            "label": "Pet Shower & Bath Accessories",
            "section": "Pet Grooming",
        },
        "pet-supplies-pet-grooming-tools": {
            "url": "https://us.shein.com/Pet-Grooming-Tools-c-4060.html",
            "label": "Pet Grooming Tools",
            "section": "Pet Grooming",
        },
        "pet-supplies-pet-automatic-feeders-water-fountains": {
            "url": "https://us.shein.com/Pet-Feeders-Appliances-c-3882.html",
            "label": "Pet Automatic Feeders & Water " "Fountains",
            "section": "Pet Smart Appliances",
        },
        "pet-supplies-aquarium-appliances": {
            "url": "https://us.shein.com/Aquarium-Appliances-c-5998.html",
            "label": "Aquarium Appliances",
            "section": "Pet Smart Appliances",
        },
        "pet-supplies-pet-grooming-appliances": {
            "url": "https://us.shein.com/Pet-Grooming-Appliances-c-6001.html",
            "label": "Pet Grooming Appliances",
            "section": "Pet Smart Appliances",
        },
        "pet-supplies-electronic-pet-training-behavior": {
            "url": "https://us.shein.com/Electronic-Pet-Training-Behavior-c-6002.html",
            "label": "Electronic Pet Training & Behavior",
            "section": "Pet Smart Appliances",
        },
        "pet-supplies-electronic-pet-collars-leashes-harnesses": {
            "url": "https://us.shein.com/Electronic-Pet-Collars,-Leashes-Harnesses-c-6004.html",
            "label": "Electronic Pet Collars, Leashes " "& Harnesses",
            "section": "Pet Smart Appliances",
        },
        "pet-supplies-view-all-9682": {
            "url": "https://us.shein.com/Pet-Treats-c-9682.html",
            "label": "View All",
            "section": "Pet Treats",
        },
        "pet-supplies-dog-treats": {
            "url": "https://us.shein.com/Dog-Treats-c-9685.html",
            "label": "Dog Treats",
            "section": "Pet Treats",
        },
        "pet-supplies-cat-treats": {
            "url": "https://us.shein.com/Cat-Treats-c-9686.html",
            "label": "Cat Treats",
            "section": "Pet Treats",
        },
        "pet-supplies-dog-food": {
            "url": "https://us.shein.com/Dog-Food-c-9683.html",
            "label": "Dog Food",
            "section": "Pet Food",
        },
        "pet-supplies-cat-food": {
            "url": "https://us.shein.com/Cat-Food-c-9684.html",
            "label": "Cat Food",
            "section": "Pet Food",
        },
        "pet-supplies-small-animal-cages-houses": {
            "url": "https://us.shein.com/Small-Animal-Cages-Accessories-c-4041.html",
            "label": "Small Animal Cages & Houses",
            "section": "Small Animal Supplies",
        },
        "pet-supplies-small-pet-toys": {
            "url": "https://us.shein.com/Small-Pet-Toys-c-4042.html",
            "label": "Small Pet Toys",
            "section": "Small Animal Supplies",
        },
        "pet-supplies-small-pet-accessories": {
            "url": "https://us.shein.com/Small-Pet-Accessories-c-5994.html",
            "label": "Small Pet Accessories",
            "section": "Small Animal Supplies",
        },
        "pet-supplies-small-pet-feeders": {
            "url": "https://us.shein.com/Small-Pet-Feeders-c-5995.html",
            "label": "Small Pet Feeders",
            "section": "Small Animal Supplies",
        },
        "pet-supplies-bird-toys": {
            "url": "https://us.shein.com/Bird-Toys-c-4031.html",
            "label": "Bird Toys",
            "section": "Bird Supplies",
        },
        "pet-supplies-bird-feeding": {
            "url": "https://us.shein.com/Bird-Feeding-c-4030.html",
            "label": "Bird Feeding",
            "section": "Bird Supplies",
        },
        "pet-supplies-bird-houses-nests": {
            "url": "https://us.shein.com/Bird-Houses-Nests-c-4034.html",
            "label": "Bird Houses & Nests",
            "section": "Bird Supplies",
        },
        "pet-supplies-bird-cages-accessories": {
            "url": "https://us.shein.com/Bird-Cages-Accessories-c-4033.html",
            "label": "Bird Cages & Accessories",
            "section": "Bird Supplies",
        },
        "pet-supplies-bird-grooming-baths": {
            "url": "https://us.shein.com/Bird-Grooming-Baths-c-4029.html",
            "label": "Bird Grooming & Baths",
            "section": "Bird Supplies",
        },
        "pet-supplies-tank-accessories": {
            "url": "https://us.shein.com/Tank-Accessories-c-4036.html",
            "label": "Tank & Accessories",
            "section": "Fish & Aquarium Supplies",
        },
        "pet-supplies-fish-cleaning-tools": {
            "url": "https://us.shein.com/Fish-Cleaning-Tools-c-4038.html",
            "label": "Fish Cleaning Tools",
            "section": "Fish & Aquarium Supplies",
        },
        "pet-supplies-aquarium-decorations": {
            "url": "https://us.shein.com/Aquarium-Decorations-c-5999.html",
            "label": "Aquarium Decorations",
            "section": "Fish & Aquarium Supplies",
        },
        "pet-supplies-feeders": {
            "url": "https://us.shein.com/Feeders-c-4039.html",
            "label": "Feeders",
            "section": "Fish & Aquarium Supplies",
        },
        "pet-supplies-equipment-maintenance": {
            "url": "https://us.shein.com/Equipment-Maintenance-c-4037.html",
            "label": "Equipment & Maintenance",
            "section": "Fish & Aquarium Supplies",
        },
        "pet-supplies-aquarium-substrate": {
            "url": "https://us.shein.com/Aquarium-Substrate-c-6000.html",
            "label": "Aquarium Substrate",
            "section": "Fish & Aquarium Supplies",
        },
        "pet-supplies-commemorative-pet-necklaces": {
            "url": "https://us.shein.com/Commemorative-Pet-Necklaces-c-6003.html",
            "label": "Commemorative Pet Necklaces",
            "section": "Pet Memorial",
        },
        "pet-supplies-pet-picture-frames": {
            "url": "https://us.shein.com/Pet-Picture-Frames-c-6005.html",
            "label": "Pet Picture Frames",
            "section": "Pet Memorial",
        },
        "pet-supplies-pet-health-care-tools-2984": {
            "url": "https://us.shein.com/Pet-Health-Care-Tools-c-2984.html",
            "label": "Pet Health Care Tools",
            "section": "Pet Health Care Tools",
        },
        "pet-supplies-pet-recovery-collars": {
            "url": "https://us.shein.com/Pet-Recovery-Collars-c-2972.html",
            "label": "Pet Recovery Collars",
            "section": "Pet Health Care Tools",
        },
        "pet-supplies-pet-first-aid": {
            "url": "https://us.shein.com/Pet-First-Aid-c-2973.html",
            "label": "Pet First Aid",
            "section": "Pet Health Care Tools",
        },
        "pet-supplies-horse-blankets-sheets": {
            "url": "https://us.shein.com/Horse-Blankets-Sheets-c-6330.html",
            "label": "Horse Blankets & Sheets",
            "section": "Horses",
        },
        "pet-supplies-horse-boots-wraps": {
            "url": "https://us.shein.com/Horse-Boots-Wraps-c-6331.html",
            "label": "Horse Boots & Wraps",
            "section": "Horses",
        },
        "pet-supplies-horse-farrier-supplies": {
            "url": "https://us.shein.com/Horse-Farrier-Supplies-c-6332.html",
            "label": "Horse Farrier Supplies",
            "section": "Horses",
        },
        "pet-supplies-horse-grooming-bathing-supplies": {
            "url": "https://us.shein.com/Horse-Grooming-Bathing-Supplies-c-6333.html",
            "label": "Horse Grooming & Bathing Supplies",
            "section": "Horses",
        },
        "pet-supplies-horse-stable-supplies": {
            "url": "https://us.shein.com/Horse-Stable-Supplies-c-6334.html",
            "label": "Horse Stable Supplies",
            "section": "Horses",
        },
        "pet-supplies-habitat-accessories": {
            "url": "https://us.shein.com/Habitat-Accessories-c-4044.html",
            "label": "Habitat & Accessories",
            "section": "Reptile & Amphibian Supplies",
        },
        "pet-supplies-reptile-feeding-watering-supplies": {
            "url": "https://us.shein.com/Reptile-Feeding-Watering-Supplies-c-4045.html",
            "label": "Reptile Feeding & Watering Supplies",
            "section": "Reptile & Amphibian Supplies",
        },
        "pet-supplies-reptile-cleaning-tools": {
            "url": "https://us.shein.com/Reptile-Cleaning-Tools-c-4046.html",
            "label": "Reptile Cleaning Tools",
            "section": "Reptile & Amphibian Supplies",
        },
        "pet-supplies-reptile-amphibian-clothing": {
            "url": "https://us.shein.com/Reptile-Amphibian-Clothing-c-13483.html",
            "label": "Reptile & Amphibian Clothing",
            "section": "Reptile & Amphibian Supplies",
        },
        "pet-supplies-farm-animal-carriers": {
            "url": "https://us.shein.com/Farm-Animal-Carriers-c-4049.html",
            "label": "Farm Animal Carriers",
            "section": "Farm Animal Supplies",
        },
        "pet-supplies-farm-animal-feeding-watering-supplies": {
            "url": "https://us.shein.com/Farm-Animal-Feeding-Watering-Supplies-c-4050.html",
            "label": "Farm Animal Feeding & Watering " "Supplies",
            "section": "Farm Animal Supplies",
        },
        "pet-supplies-farm-cages-accessories": {
            "url": "https://us.shein.com/Farm-Cages-Accessories-c-4048.html",
            "label": "Farm Cages & Accessories",
            "section": "Farm Animal Supplies",
        },
        "pet-supplies-petsin": {
            "url": "https://us.shein.com/Brands/PETSIN-sc-01442544.html",
            "label": "PETSIN",
            "section": "Brands We Love",
        },
    },
    "home-appliances": {
        "home-appliances": {
            "url": "https://us.shein.com/RecommendSelection/Appliances-sc-017172977.html",
            "label": "Appliances",
            "section": "Top category",
        },
        "home-appliances-view-all": {
            "url": "https://us.shein.com/Home-Appliances-c-3650.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "home-appliances-new-in": {
            "url": "https://us.shein.com/recommend/Appliances-New-In-sc-100121319.html",
            "label": "New In",
            "section": "Shop by Category",
        },
        "home-appliances-top-rated": {
            "url": "https://us.shein.com/recommend/Top-Rated-sc-10050008998.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "home-appliances-heater-cooler": {
            "url": "https://us.shein.com/Heater-Cooler-c-5209.html",
            "label": "Heater & Cooler",
            "section": "Shop by Category",
        },
        "home-appliances-hair-styling-care-appliances": {
            "url": "https://us.shein.com/Hair-Styling-Care-Appliances-c-9108.html",
            "label": "Hair Styling Care Appliances",
            "section": "Shop by Category",
        },
        "home-appliances-juicer-food-processor": {
            "url": "https://us.shein.com/Juicer-Food-Processor-c-8660.html",
            "label": "Juicer & Food Processor",
            "section": "Shop by Category",
        },
        "home-appliances-cooking-appliances": {
            "url": "https://us.shein.com/Cooking-Appliances-c-4631.html",
            "label": "Cooking Appliances",
            "section": "Shop by Category",
        },
        "home-appliances-laundry-appliances": {
            "url": "https://us.shein.com/Laundry-Appliances-c-4566.html",
            "label": "Laundry Appliances",
            "section": "Shop by Category",
        },
        "home-appliances-nail-art-equipments": {
            "url": "https://us.shein.com/Nail-Art-Equipments-c-9120.html",
            "label": "Nail Art Equipments",
            "section": "Shop by Category",
        },
        "home-appliances-beauty-care-appliances": {
            "url": "https://us.shein.com/Beauty-Care-Appliances-c-9109.html",
            "label": "Beauty Care Appliances",
            "section": "Shop by Category",
        },
        "home-appliances-coffee-tea-appliances": {
            "url": "https://us.shein.com/Coffee-Tea-Appliances-c-5451.html",
            "label": "Coffee & Tea Appliances",
            "section": "Shop by Category",
        },
        "home-appliances-cleaning-appliances": {
            "url": "https://us.shein.com/Cleaning-Appliances-c-4555.html",
            "label": "Cleaning Appliances",
            "section": "Shop by Category",
        },
        "home-appliances-portable-air-conditioner": {
            "url": "https://us.shein.com/Portable-Air-Conditioner-c-14151.html",
            "label": "Portable Air Conditioner",
            "section": "Picks for You",
        },
        "home-appliances-electric-fireplaces": {
            "url": "https://us.shein.com/Electric-Fireplaces-c-5445.html",
            "label": "Electric Fireplaces",
            "section": "Picks for You",
        },
        "home-appliances-crepe-makers": {
            "url": "https://us.shein.com/Crepe-Makers-c-5409.html",
            "label": "Crepe Makers",
            "section": "Picks for You",
        },
        "home-appliances-beverage-centers": {
            "url": "https://us.shein.com/Beverage-Centers-c-12225.html",
            "label": "Beverage Centers",
            "section": "Picks for You",
        },
        "home-appliances-carpet-cleaning-machines": {
            "url": "https://us.shein.com/Carpet-Cleaning-Machines-c-14154.html",
            "label": "Carpet Cleaning Machines",
            "section": "Picks for You",
        },
        "home-appliances-humidifier": {
            "url": "https://us.shein.com/Humidifier-c-3877.html",
            "label": "Humidifier",
            "section": "Picks for You",
        },
        "home-appliances-refrigerators": {
            "url": "https://us.shein.com/Refrigerators-c-5402.html",
            "label": "Refrigerators",
            "section": "Picks for You",
        },
        "home-appliances-aroma-diffuser": {
            "url": "https://us.shein.com/Aroma-Diffuser-c-8658.html",
            "label": "Aroma Diffuser",
            "section": "Picks for You",
        },
        "home-appliances-vacuum-cleaners": {
            "url": "https://us.shein.com/Vacuum-Cleaners-c-4562.html",
            "label": "Vacuum Cleaners",
            "section": "Picks for You",
        },
        "home-appliances-stick-vacuum-cleaners": {
            "url": "https://us.shein.com/Stick-Vacuum-Cleaners-c-8692.html",
            "label": "Stick Vacuum Cleaners",
            "section": "Picks for You",
        },
        "home-appliances-portable-fans": {
            "url": "https://us.shein.com/Portable-Fans-c-3687.html",
            "label": "Portable Fans",
            "section": "Picks for You",
        },
        "home-appliances-hand-warmers": {
            "url": "https://us.shein.com/Hand-Warmers-c-5441.html",
            "label": "Hand Warmers",
            "section": "Picks for You",
        },
        "home-appliances-refrigerator-storage-box": {
            "url": "https://us.shein.com/Refrigerator-Storage-Box-c-12882.html",
            "label": "Refrigerator Storage Box",
            "section": "Picks for You",
        },
        "home-appliances-robotic-vacuums": {
            "url": "https://us.shein.com/Robotic-Vacuums-c-8693.html",
            "label": "Robotic Vacuums",
            "section": "Picks for You",
        },
        "home-appliances-electric-skillets-wok": {
            "url": "https://us.shein.com/Electric-Skillets-Wok-c-5417.html",
            "label": "Electric Skillets & Wok",
            "section": "Picks for You",
        },
        "home-appliances-air-fryers": {
            "url": "https://us.shein.com/Air-Fryers-c-4629.html",
            "label": "Air Fryers",
            "section": "Picks for You",
        },
        "home-appliances-electric-blankets": {
            "url": "https://us.shein.com/Electric-Blankets-c-8667.html",
            "label": "Electric Blankets",
            "section": "Picks for You",
        },
        "home-appliances-waffle-makers": {
            "url": "https://us.shein.com/Waffle-Makers-c-4649.html",
            "label": "Waffle Makers",
            "section": "Picks for You",
        },
    },
    "automotive": {
        "automotive": {
            "url": "https://us.shein.com/RecommendSelection/Automotive-sc-017172975.html",
            "label": "Automotive",
            "section": "Top category",
        },
        "automotive-view-all": {
            "url": "https://us.shein.com/Automotive-c-3657.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "automotive-new-in": {
            "url": "https://us.shein.com/recommend/Automotive-New-In-sc-100121185.html",
            "label": "New in",
            "section": "Shop by Category",
        },
        "automotive-top-rated": {
            "url": "https://us.shein.com/recommend/Top-Rated-sc-10050007875.html",
            "label": "Top Rated",
            "section": "Shop by Category",
        },
        "automotive-automotive-interior-accessories": {
            "url": "https://us.shein.com/Automotive-Interior-Accessories-c-3883.html",
            "label": "Automotive Interior Accessories",
            "section": "Shop by Category",
        },
        "automotive-car-seats-accessories": {
            "url": "https://us.shein.com/Car-Seats-Accessories-c-3886.html",
            "label": "Car Seats & Accessories",
            "section": "Shop by Category",
        },
        "automotive-car-storage": {
            "url": "https://us.shein.com/Car-Storage-c-3885.html",
            "label": "Car Storage",
            "section": "Shop by Category",
        },
        "automotive-car-electronics": {
            "url": "https://us.shein.com/Car-Electronics-c-2998.html",
            "label": "Car Electronics",
            "section": "Shop by Category",
        },
        "automotive-automotive-exterior-accessories": {
            "url": "https://us.shein.com/Automotive-Exterior-Accessories-c-3900.html",
            "label": "Automotive Exterior Accessories",
            "section": "Shop by Category",
        },
        "automotive-car-wash-maintenance": {
            "url": "https://us.shein.com/Car-Wash-Maintenance-c-13528.html",
            "label": "Car Wash & Maintenance",
            "section": "Shop by Category",
        },
        "automotive-motorcycle-accessories-parts": {
            "url": "https://us.shein.com/Motorcycle-Accessories-Parts-c-4877.html",
            "label": "Motorcycle Accessories & Parts",
            "section": "Shop by Category",
        },
        "automotive-car-lights": {
            "url": "https://us.shein.com/Car-Lights-c-4686.html",
            "label": "Car Lights",
            "section": "Shop by Category",
        },
        "automotive-car-repair-tools-equipment": {
            "url": "https://us.shein.com/Car-Repair-Tools-Equipment-c-13529.html",
            "label": "Car Repair Tools & Equipment",
            "section": "Shop by Category",
        },
        "automotive-car-sun-protection": {
            "url": "https://us.shein.com/Car-Sun-Protection-c-11929.html",
            "label": "Car Sun Protection",
            "section": "Automotive Interior Accessories",
        },
        "automotive-customized-automotive-interior-accessories": {
            "url": "https://us.shein.com/Customized-Automotive-Interior-Accessories-c-13641.html",
            "label": "Customized Automotive Interior " "Accessories",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-coasters": {
            "url": "https://us.shein.com/Car-Coasters-c-3888.html",
            "label": "Car Coasters",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-interior-stickers": {
            "url": "https://us.shein.com/Car-Interior-Stickers-c-3889.html",
            "label": "Car Interior Stickers",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-air-outlet-accessories": {
            "url": "https://us.shein.com/Car-Air-Outlet-Accessories-c-3890.html",
            "label": "Car Air Outlet Accessories",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-key-case": {
            "url": "https://us.shein.com/Car-Key-Case-c-3892.html",
            "label": "Car Key Case",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-keychain": {
            "url": "https://us.shein.com/Car-Keychain-c-13527.html",
            "label": "Car Keychain",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-hanging-decorations": {
            "url": "https://us.shein.com/Car-Hanging-Decorations-c-13894.html",
            "label": "Car Hanging Decorations",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-parking-number-plate": {
            "url": "https://us.shein.com/Car-Parking-Number-Plate-c-13895.html",
            "label": "Car Parking Number Plate",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-sun-visor-mirror": {
            "url": "https://us.shein.com/Car-Sun-Visor-Mirror-c-13898.html",
            "label": "Car Sun Visor Mirror",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-air-freshener": {
            "url": "https://us.shein.com/Car-Air-Freshener-c-3664.html",
            "label": "Car Air Freshener",
            "section": "Automotive Interior Accessories",
        },
        "automotive-car-ornaments": {
            "url": "https://us.shein.com/Car-Ornaments-c-3891.html",
            "label": "Car Ornaments",
            "section": "Automotive Interior Accessories",
        },
        "automotive-steering-wheel-cover-accs": {
            "url": "https://us.shein.com/Steering-Wheel-Cover-Accs-c-3003.html",
            "label": "Steering Wheel Cover & Accs",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-seat-cushion": {
            "url": "https://us.shein.com/Car-Seat-Cushion-c-3673.html",
            "label": "Car Seat Cushion",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-armrest-pad": {
            "url": "https://us.shein.com/Car-Armrest-Pad-c-3896.html",
            "label": "Car Armrest Pad",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-neck-lumbar-pillow": {
            "url": "https://us.shein.com/Car-Neck-Lumbar-Pillow-c-3897.html",
            "label": "Car Neck & Lumbar Pillow",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-floor-mat": {
            "url": "https://us.shein.com/Car-Floor-Mat-c-3898.html",
            "label": "Car Floor Mat",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-seat-cover": {
            "url": "https://us.shein.com/Car-Seat-Cover-c-3899.html",
            "label": "Car Seat Cover",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-pet-accessories": {
            "url": "https://us.shein.com/Car-Pet-Accessories-c-9749.html",
            "label": "Car Pet Accessories",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-interior-kits": {
            "url": "https://us.shein.com/Car-Interior-Kits-c-9750.html",
            "label": "Car Interior Kits",
            "section": "Car Seats & Accessories",
        },
        "automotive-seatbelt-cover": {
            "url": "https://us.shein.com/Seatbelt-Cover-c-13889.html",
            "label": "Seatbelt Cover",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-inflatable-bed": {
            "url": "https://us.shein.com/Car-Inflatable-Bed-c-13883.html",
            "label": "Car Inflatable Bed",
            "section": "Car Seats & Accessories",
        },
        "automotive-gear-shift-handbrake-cover": {
            "url": "https://us.shein.com/Gear-Shift-Handbrake-Cover-c-13897.html",
            "label": "Gear Shift & Handbrake Cover",
            "section": "Car Seats & Accessories",
        },
        "automotive-car-seat-organization": {
            "url": "https://us.shein.com/Car-Seat-Organization-c-13881.html",
            "label": "Car Seat Organization",
            "section": "Car Storage",
        },
        "automotive-car-tissue-box": {
            "url": "https://us.shein.com/Car-Tissue-Box-c-3894.html",
            "label": "Car Tissue Box",
            "section": "Car Storage",
        },
        "automotive-car-trash-can": {
            "url": "https://us.shein.com/Car-Trash-Can-c-3895.html",
            "label": "Car Trash Can",
            "section": "Car Storage",
        },
        "automotive-car-ashtray": {
            "url": "https://us.shein.com/Car-Ashtray-c-11936.html",
            "label": "Car Ashtray",
            "section": "Car Storage",
        },
        "automotive-car-coin-storage": {
            "url": "https://us.shein.com/Car-Coin-Storage-c-13892.html",
            "label": "Car Coin Storage",
            "section": "Car Storage",
        },
        "automotive-car-air-outlet-storage": {
            "url": "https://us.shein.com/Car-Air-Outlet-Storage-c-13901.html",
            "label": "Car Air Outlet Storage",
            "section": "Car Storage",
        },
        "automotive-car-trunk-organizers": {
            "url": "https://us.shein.com/Car-Trunk-Organizers-c-13899.html",
            "label": "Car Trunk Organizers",
            "section": "Car Storage",
        },
        "automotive-car-sun-visor-storage": {
            "url": "https://us.shein.com/Car-Sun-Visor-Storage-c-13880.html",
            "label": "Car Sun Visor Storage",
            "section": "Car Storage",
        },
        "automotive-car-trays": {
            "url": "https://us.shein.com/Car-Trays-c-13891.html",
            "label": "Car Trays",
            "section": "Car Storage",
        },
        "automotive-car-dashboard-storage": {
            "url": "https://us.shein.com/Car-Dashboard-Storage-c-13893.html",
            "label": "Car Dashboard Storage",
            "section": "Car Storage",
        },
        "automotive-car-center-console-armrest-storage": {
            "url": "https://us.shein.com/Car-Center-Console-Armrest-Storage-c-13900.html",
            "label": "Car Center Console & Armrest Storage",
            "section": "Car Storage",
        },
        "automotive-car-electrical-appliances": {
            "url": "https://us.shein.com/Car-Electrical-Appliances-c-9490.html",
            "label": "Car Electrical Appliances",
            "section": "Car Electronics",
        },
        "automotive-car-dashcam-video": {
            "url": "https://us.shein.com/Car-Dashcam-Video-c-13706.html",
            "label": "Car Dashcam & Video",
            "section": "Car Electronics",
        },
        "automotive-car-intelligence-system": {
            "url": "https://us.shein.com/Car-Intelligence-System-c-13708.html",
            "label": "Car Intelligence System",
            "section": "Car Electronics",
        },
        "automotive-car-audio": {
            "url": "https://us.shein.com/Car-Audio-c-9498.html",
            "label": "Car Audio",
            "section": "Car Electronics",
        },
        "automotive-automotive-cellphone-accessories": {
            "url": "https://us.shein.com/Automotive-Cellphone-Accessories-c-13882.html",
            "label": "Automotive Cellphone Accessories",
            "section": "Car Electronics",
        },
        "automotive-electric-vehicle-charging-equipment": {
            "url": "https://us.shein.com/Electric-Vehicle-Charging-Equipment-c-8067.html",
            "label": "Electric Vehicle Charging Equipment",
            "section": "Car Electronics",
        },
        "automotive-car-electronics-accessories": {
            "url": "https://us.shein.com/Car-Electronics-Accessories-c-2999.html",
            "label": "Car Electronics Accessories",
            "section": "Car Electronics",
        },
        "automotive-car-security-alarms": {
            "url": "https://us.shein.com/Car-Security-Alarms-c-13707.html",
            "label": "Car Security & Alarms",
            "section": "Car Electronics",
        },
        "automotive-exterior-sticker": {
            "url": "https://us.shein.com/Exterior-Sticker-c-3002.html",
            "label": "Exterior Sticker",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-exterior-decorative-accessories": {
            "url": "https://us.shein.com/Exterior-Decorative-Accessories-c-3903.html",
            "label": "Exterior Decorative Accessories",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-rearview-mirror-accessories": {
            "url": "https://us.shein.com/Rearview-Mirror-Accessories-c-3902.html",
            "label": "Rearview Mirror Accessories",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-travel-roadway-product": {
            "url": "https://us.shein.com/Travel-Roadway-Product-c-3005.html",
            "label": "Travel & Roadway Product",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-car-replacement-parts": {
            "url": "https://us.shein.com/Car-Replacement-Parts-c-9182.html",
            "label": "Car Replacement Parts",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-car-license-plate": {
            "url": "https://us.shein.com/Car-License-Plate-c-13533.html",
            "label": "Car License Plate",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-exterior-practical-accessories": {
            "url": "https://us.shein.com/Exterior-Practical-Accessories-c-13536.html",
            "label": "Exterior Practical Accessories",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-ice-and-snow-products": {
            "url": "https://us.shein.com/Ice-and-Snow-Products-c-13535.html",
            "label": "Ice and Snow Products",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-traction-products-and-winches": {
            "url": "https://us.shein.com/Traction-Products-and-Winches-c-13534.html",
            "label": "Traction Products and Winches",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-trunk-and-tailgate-accessories": {
            "url": "https://us.shein.com/Trunk-and-Tailgate-Accessories-c-13537.html",
            "label": "Trunk and Tailgate Accessories",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-safety-products": {
            "url": "https://us.shein.com/Reflective-Warning-Signs-c-13579.html",
            "label": "Safety Products",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-customized-exterior-decorative-accessories": {
            "url": "https://us.shein.com/Customized-Exterior-Decorative-Accessories-c-13644.html",
            "label": "Customized Exterior Decorative " "Accessories",
            "section": "Automotive Exterior Accessories",
        },
        "automotive-car-wash-kit": {
            "url": "https://us.shein.com/Car-Wash-Kit-c-3001.html",
            "label": "Car Wash Kit",
            "section": "Car Wash & Maintenance",
        },
        "automotive-car-cleaning-cloth": {
            "url": "https://us.shein.com/Car-Cleaning-Cloth-c-13546.html",
            "label": "Car Cleaning Cloth",
            "section": "Car Wash & Maintenance",
        },
        "automotive-wiper": {
            "url": "https://us.shein.com/Wiper-c-13541.html",
            "label": "Wiper",
            "section": "Car Wash & Maintenance",
        },
        "automotive-car-cleaning-brush": {
            "url": "https://us.shein.com/Car-Cleaning-Brush-c-13552.html",
            "label": "Car Cleaning Brush",
            "section": "Car Wash & Maintenance",
        },
        "automotive-cleaning-care-agents": {
            "url": "https://us.shein.com/Cleaning-Care-Agents-c-13554.html",
            "label": "Cleaning & Care Agents",
            "section": "Car Wash & Maintenance",
        },
        "automotive-car-polishing-machine": {
            "url": "https://us.shein.com/Car-Polishing-Machine-c-4672.html",
            "label": "Car Polishing Machine",
            "section": "Car Wash & Maintenance",
        },
        "automotive-rust-preventive-rust-remover": {
            "url": "https://us.shein.com/Rust-Preventive-Rust-Remover-c-13544.html",
            "label": "Rust Preventive & Rust Remover",
            "section": "Car Wash & Maintenance",
        },
        "automotive-blower": {
            "url": "https://us.shein.com/Blower-c-13542.html",
            "label": "Blower",
            "section": "Car Wash & Maintenance",
        },
        "automotive-polishing-pads-sponges": {
            "url": "https://us.shein.com/Polishing-Pads-Sponges-c-13547.html",
            "label": "Polishing Pads & Sponges",
            "section": "Car Wash & Maintenance",
        },
        "automotive-paint-spray-guns-and-accessories": {
            "url": "https://us.shein.com/Paint-Spray-Guns-and-Accessories-c-13548.html",
            "label": "Paint Spray Guns and Accessories",
            "section": "Car Wash & Maintenance",
        },
        "automotive-car-paint-and-touch-up": {
            "url": "https://us.shein.com/Car-Paint-and-Touch-Up-c-13553.html",
            "label": "Car Paint and Touch-Up",
            "section": "Car Wash & Maintenance",
        },
        "automotive-car-wash-gun": {
            "url": "https://us.shein.com/Car-Wash-Gun-c-13551.html",
            "label": "Car Wash Gun",
            "section": "Car Wash & Maintenance",
        },
        "automotive-car-washing-gloves": {
            "url": "https://us.shein.com/Car-Washing-Gloves-c-13550.html",
            "label": "Car Washing Gloves",
            "section": "Car Wash & Maintenance",
        },
        "automotive-adhesives-sealants": {
            "url": "https://us.shein.com/Adhesives-Sealants-c-13549.html",
            "label": "Adhesives & Sealants",
            "section": "Car Wash & Maintenance",
        },
        "automotive-motorcycle-accessories": {
            "url": "https://us.shein.com/Motorcycle-Accessories-c-3004.html",
            "label": "Motorcycle Accessories",
            "section": "Motorcycle Accessories & Parts",
        },
        "automotive-motorcycle-protective-gear": {
            "url": "https://us.shein.com/Motorcycle-Protective-Gear-c-13945.html",
            "label": "Motorcycle Protective Gear",
            "section": "Motorcycle Accessories & Parts",
        },
        "automotive-motorcycle-replacement-parts": {
            "url": "https://us.shein.com/Motorcycle-Replacement-Parts-c-5094.html",
            "label": "Motorcycle Replacement Parts",
            "section": "Motorcycle Accessories & Parts",
        },
        "automotive-motorcycle-storage": {
            "url": "https://us.shein.com/Motorcycle-Storage-c-5096.html",
            "label": "Motorcycle Storage",
            "section": "Motorcycle Accessories & Parts",
        },
        "automotive-motorcycle-electronics": {
            "url": "https://us.shein.com/Motorcycle-Electronics-c-5097.html",
            "label": "Motorcycle Electronics",
            "section": "Motorcycle Accessories & Parts",
        },
        "automotive-decorative-lamp": {
            "url": "https://us.shein.com/Decorative-Lamp-c-3000.html",
            "label": "Decorative Lamp",
            "section": "Car Lights",
        },
        "automotive-bulbs": {
            "url": "https://us.shein.com/Bulbs-c-9454.html",
            "label": "Bulbs",
            "section": "Car Lights",
        },
        "automotive-lighting-assemblies": {
            "url": "https://us.shein.com/Lighting-Assemblies-c-9483.html",
            "label": "Lighting Assemblies",
            "section": "Car Lights",
        },
        "automotive-light-bars": {
            "url": "https://us.shein.com/Light-Bars-c-9491.html",
            "label": "Light Bars",
            "section": "Car Lights",
        },
        "automotive-work-lights": {
            "url": "https://us.shein.com/Work-Lights-c-9487.html",
            "label": "Work Lights",
            "section": "Car Lights",
        },
        "automotive-towing-trailer-lighting": {
            "url": "https://us.shein.com/Towing-Trailer-Lighting-c-9488.html",
            "label": "Towing & Trailer Lighting",
            "section": "Car Lights",
        },
        "automotive-warning-emergency-lights": {
            "url": "https://us.shein.com/Warning-Emergency-Lights-c-9489.html",
            "label": "Warning & Emergency Lights",
            "section": "Car Lights",
        },
        "automotive-car-jump-starter": {
            "url": "https://us.shein.com/Car-Jump-Starter-c-4679.html",
            "label": "Car Jump Starter",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-car-diagnostic-tools": {
            "url": "https://us.shein.com/Car-Diagnostic-Tools-c-4673.html",
            "label": "Car Diagnostic Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-car-air-compressors": {
            "url": "https://us.shein.com/Car-Air-Compressors-c-9496.html",
            "label": "Car Air Compressors",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-car-body-repair-tools": {
            "url": "https://us.shein.com/Car-Body-Repair-Tools-c-13532.html",
            "label": "Car Body Repair Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-vehicle-repair-workshop-equipment": {
            "url": "https://us.shein.com/Vehicle-Repair-Workshop-Equipment-c-13540.html",
            "label": "Vehicle Repair Workshop Equipment",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-puller": {
            "url": "https://us.shein.com/Puller-c-13597.html",
            "label": "Puller",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-tire-repair-tools": {
            "url": "https://us.shein.com/Tire-Repair-Tools-c-13608.html",
            "label": "Tire Repair Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-automotive-tool-kits": {
            "url": "https://us.shein.com/Automotive-Tool-Kits-c-13607.html",
            "label": "Automotive Tool Kits",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-car-jack": {
            "url": "https://us.shein.com/Car-Jack-c-13606.html",
            "label": "Car Jack",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-jack-stand": {
            "url": "https://us.shein.com/Jack-Stand-c-13605.html",
            "label": "Jack Stand",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-brake-tools": {
            "url": "https://us.shein.com/Brake-Tools-c-13531.html",
            "label": "Brake Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-engine-tools": {
            "url": "https://us.shein.com/Engine-Tools-c-13538.html",
            "label": "Engine Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-fuel-delivery-lubrication-products": {
            "url": "https://us.shein.com/Fuel-Delivery-Lubrication-Products-c-13539.html",
            "label": "Fuel Delivery & Lubrication Products",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-electrical-system-tools": {
            "url": "https://us.shein.com/Electrical-System-Tools-c-13598.html",
            "label": "Electrical System Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-tool-organizer-tray": {
            "url": "https://us.shein.com/Tool-Organizer/Tray-c-13602.html",
            "label": "Tool Organizer/Tray",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-spark-plugs-and-ignition-tools": {
            "url": "https://us.shein.com/Spark-Plugs-and-Ignition-Tools-c-13599.html",
            "label": "Spark Plugs and Ignition Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-oil-filter-tools": {
            "url": "https://us.shein.com/Oil-Filter-Tools-c-13600.html",
            "label": "Oil Filter Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-thread-repair-kit": {
            "url": "https://us.shein.com/Thread-Repair-Kit-c-13610.html",
            "label": "Thread Repair Kit",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-car-air-conditioning-repair-tools": {
            "url": "https://us.shein.com/Car-Air-Conditioning-Repair-Tools-c-13609.html",
            "label": "Car Air Conditioning Repair Tools",
            "section": "Car Repair Tools & Equipment",
        },
        "automotive-steering-and-suspension-tools": {
            "url": "https://us.shein.com/Steering-and-Suspension-Tools-c-13611.html",
            "label": "Steering and Suspension Tools",
            "section": "Car Repair Tools & Equipment",
        },
    },
    "books-magazines": {
        "books-magazines": {
            "url": "https://us.shein.com/RecommendSelection/Books-Magazines-sc-0175086797.html",
            "label": "Books & Magazine",
            "section": "Top category",
        },
        "books-magazines-view-all": {
            "url": "https://us.shein.com/Books-Magazines-c-13087.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "books-magazines-literature-fiction": {
            "url": "https://us.shein.com/Literature-Fiction-c-13098.html",
            "label": "Literature & Fiction",
            "section": "Shop by Category",
        },
        "books-magazines-kids-books": {
            "url": "https://us.shein.com/Kids-Books-c-13097.html",
            "label": "Kids Books",
            "section": "Shop by Category",
        },
        "books-magazines-life-lifestyle": {
            "url": "https://us.shein.com/Life-Lifestyle-c-13103.html",
            "label": "Life & Lifestyle",
            "section": "Shop by Category",
        },
        "books-magazines-education-teaching": {
            "url": "https://us.shein.com/Education-Teaching-c-13102.html",
            "label": "Education & Teaching",
            "section": "Shop by Category",
        },
        "books-magazines-medical-books": {
            "url": "https://us.shein.com/Medical-Books-c-13104.html",
            "label": "Medical Books",
            "section": "Shop by Category",
        },
        "books-magazines-science-nature-technology": {
            "url": "https://us.shein.com/Humanities-Social-Science-c-13101.html",
            "label": "Science, Nature & Technology",
            "section": "Shop by Category",
        },
        "books-magazines-magazines-newspaper": {
            "url": "https://us.shein.com/Magazines-Newspaper-c-13105.html",
            "label": "Magazines & Newspaper",
            "section": "Shop by Category",
        },
        "books-magazines-romance-novel": {
            "url": "https://us.shein.com/Romance-Novel-c-13140.html",
            "label": "Romance Novel",
            "section": "Literature & Fiction",
        },
        "books-magazines-mystery-detective-suspense": {
            "url": "https://us.shein.com/Mystery-Detective-Suspense-c-13147.html",
            "label": "Mystery & Detective Suspense",
            "section": "Literature & Fiction",
        },
        "books-magazines-thriller-horror-novel": {
            "url": "https://us.shein.com/Thriller-Horror-Novel-c-13144.html",
            "label": "Thriller Horror Novel",
            "section": "Literature & Fiction",
        },
        "books-magazines-biography-memoirs": {
            "url": "https://us.shein.com/Biography-Memoirs-c-13141.html",
            "label": "Biography & Memoirs",
            "section": "Literature & Fiction",
        },
        "books-magazines-science-fiction-fantasy": {
            "url": "https://us.shein.com/Science-Fiction-Fantasy-c-13146.html",
            "label": "Science Fiction & Fantasy",
            "section": "Literature & Fiction",
        },
        "books-magazines-light-novel": {
            "url": "https://us.shein.com/Light-Novel-c-13148.html",
            "label": "Light Novel",
            "section": "Literature & Fiction",
        },
        "books-magazines-ancient-medieval-literature": {
            "url": "https://us.shein.com/Ancient-Medieval-Literature-c-13142.html",
            "label": "Ancient & Medieval Literature",
            "section": "Literature & Fiction",
        },
        "books-magazines-kids-literature-fiction": {
            "url": "https://us.shein.com/Kids-Literature-Fiction-c-13120.html",
            "label": "Kids Literature & Fiction",
            "section": "Kids Books",
        },
        "books-magazines-kids-comics": {
            "url": "https://us.shein.com/Kids-Comics-c-13116.html",
            "label": "Kids Comics",
            "section": "Kids Books",
        },
        "books-magazines-kids-fairy-tales-folk-tales-myths": {
            "url": "https://us.shein.com/Kids-Fairy-Tales,-Folk-Tales-Myths-c-13123.html",
            "label": "Kids Fairy Tales, Folk Tales & " "Myths",
            "section": "Kids Books",
        },
        "books-magazines-kids-coloring-books": {
            "url": "https://us.shein.com/Kids-Coloring-Books-c-13119.html",
            "label": "Kids Coloring Books",
            "section": "Kids Books",
        },
        "books-magazines-kids-sticker-book": {
            "url": "https://us.shein.com/Kids-Sticker-Book-c-13122.html",
            "label": "Kids Sticker Book",
            "section": "Kids Books",
        },
        "books-magazines-other-books": {
            "url": "https://us.shein.com/Other-Kids-Books-c-13118.html",
            "label": "Other Books",
            "section": "Kids Books",
        },
        "books-magazines-cookbooks-food-wine": {
            "url": "https://us.shein.com/Cookbooks,-Food-Wine-c-13132.html",
            "label": "Cookbooks, Food & Wine",
            "section": "Life & Lifestyle",
        },
        "books-magazines-health-fitness-dieting-books": {
            "url": "https://us.shein.com/Health,-Fitness-Dieting-Books-c-13139.html",
            "label": "Health, Fitness & Dieting Books",
            "section": "Life & Lifestyle",
        },
        "books-magazines-crafts-hobbies-home": {
            "url": "https://us.shein.com/Crafts,-Hobbies-Home-c-14376.html",
            "label": "Crafts, Hobbies & Home",
            "section": "Life & Lifestyle",
        },
        "books-magazines-parenting-relationships": {
            "url": "https://us.shein.com/Parenting-Relationships-c-13137.html",
            "label": "Parenting & Relationships",
            "section": "Life & Lifestyle",
        },
        "books-magazines-career-development-books": {
            "url": "https://us.shein.com/Career-Development-Books-c-13117.html",
            "label": "Career Development Books",
            "section": "Education & Teaching",
        },
        "books-magazines-test-preparation": {
            "url": "https://us.shein.com/Test-Preparation-c-13130.html",
            "label": "Test Preparation",
            "section": "Education & Teaching",
        },
        "books-magazines-words-language-grammar": {
            "url": "https://us.shein.com/Words,-Language-Grammar-c-13127.html",
            "label": "Words, Language & Grammar",
            "section": "Education & Teaching",
        },
        "books-magazines-reference-books": {
            "url": "https://us.shein.com/Reference-c-14377.html",
            "label": "Reference Books",
            "section": "Education & Teaching",
        },
        "books-magazines-study-guides-and-workbooks": {
            "url": "https://us.shein.com/Study-Guides-Workbooks-c-13121.html",
            "label": "Study Guides and Workbooks",
            "section": "Education & Teaching",
        },
        "books-magazines-education-theory-instruction-methods": {
            "url": "https://us.shein.com/Education-Theory-Instruction-Methods-c-14401.html",
            "label": "Education Theory & Instruction " "Methods",
            "section": "Education & Teaching",
        },
        "books-magazines-clinical-medical-books": {
            "url": "https://us.shein.com/Clinical-Medical-Books-c-13151.html",
            "label": "Clinical Medical Books",
            "section": "Medical Books",
        },
        "books-magazines-basic-medical-books": {
            "url": "https://us.shein.com/Basic-Medical-Books-c-13154.html",
            "label": "Basic Medical Books",
            "section": "Medical Books",
        },
        "books-magazines-chinese-medicine-books": {
            "url": "https://us.shein.com/Chinese-Medicine-Books-c-13152.html",
            "label": "Chinese Medicine Books",
            "section": "Medical Books",
        },
        "books-magazines-pharmacology-books": {
            "url": "https://us.shein.com/Pharmacology-Books-c-14407.html",
            "label": "Pharmacology Books",
            "section": "Medical Books",
        },
        "books-magazines-nature-ecology": {
            "url": "https://us.shein.com/Nature-Ecology-c-14400.html",
            "label": "Nature & Ecology",
            "section": "Science, Nature & Technology",
        },
        "books-magazines-computer-science-technology": {
            "url": "https://us.shein.com/Computer-Science-Technology-c-13125.html",
            "label": "Computer Science & Technology",
            "section": "Science, Nature & Technology",
        },
        "books-magazines-agricultural-sciences": {
            "url": "https://us.shein.com/Agricultural-Sciences-c-13131.html",
            "label": "Agricultural Sciences",
            "section": "Science, Nature & Technology",
        },
        "books-magazines-fashion-magazines": {
            "url": "https://us.shein.com/Fashion-Magazines-c-13149.html",
            "label": "Fashion Magazines",
            "section": "Magazines & Newspaper",
        },
        "books-magazines-life-magazines": {
            "url": "https://us.shein.com/Life-Magazines-c-13153.html",
            "label": "Life Magazines",
            "section": "Magazines & Newspaper",
        },
        "books-magazines-business-magazines": {
            "url": "https://us.shein.com/Business-Magazines-c-13150.html",
            "label": "Business Magazines",
            "section": "Magazines & Newspaper",
        },
        "books-magazines-newspaper": {
            "url": "https://us.shein.com/Newspaper-c-13156.html",
            "label": "Newspaper",
            "section": "Magazines & Newspaper",
        },
        "books-magazines-cosmic-magazines": {
            "url": "https://us.shein.com/Cosmic-Magazines-c-13155.html",
            "label": "Cosmic Magazines",
            "section": "Magazines & Newspaper",
        },
        "books-magazines-history": {
            "url": "https://us.shein.com/History-c-13138.html",
            "label": "History",
            "section": "Humanities & Social Science",
        },
        "books-magazines-political-science": {
            "url": "https://us.shein.com/Political-Science-c-13135.html",
            "label": "Political Science",
            "section": "Humanities & Social Science",
        },
        "books-magazines-religion-spirituality": {
            "url": "https://us.shein.com/Religion-Spirituality-c-13136.html",
            "label": "Religion & Spirituality",
            "section": "Humanities & Social Science",
        },
        "books-magazines-psychology-books": {
            "url": "https://us.shein.com/Psychology-Books-c-13126.html",
            "label": "Psychology Books",
            "section": "Humanities & Social Science",
        },
        "books-magazines-self-help": {
            "url": "https://us.shein.com/Self-Help-c-13128.html",
            "label": "Self-Help",
            "section": "Humanities & Social Science",
        },
        "books-magazines-law": {
            "url": "https://us.shein.com/Law-c-13133.html",
            "label": "Law",
            "section": "Humanities & Social Science",
        },
    },
    "food-beverages": {
        "food-beverages": {
            "url": "https://us.shein.com/RecommendSelection/Food-Beverages-sc-0175086791.html",
            "label": "Food & Beverages",
            "section": "Top category",
        },
        "food-beverages-view-all": {
            "url": "https://us.shein.com/Food-Beverages-c-13086.html",
            "label": "View All",
            "section": "Shop by Category",
        },
        "food-beverages-water-juices-drinks": {
            "url": "https://us.shein.com/Water/Juices/Drinks-c-13095.html",
            "label": "Water/Juices/Drinks",
            "section": "Shop by Category",
        },
        "food-beverages-snacks-candies": {
            "url": "https://us.shein.com/Snacks-Candies-c-13091.html",
            "label": "Snacks & Candies",
            "section": "Shop by Category",
        },
        "food-beverages-breakfast-foods": {
            "url": "https://us.shein.com/Breakfast-Foods-c-13088.html",
            "label": "Breakfast Foods",
            "section": "Shop by Category",
        },
        "food-beverages-cooking-essentials": {
            "url": "https://us.shein.com/Cooking-Essentials-c-13090.html",
            "label": "Cooking Essentials",
            "section": "Shop by Category",
        },
        "food-beverages-baking-foods-materials": {
            "url": "https://us.shein.com/Baking-Foods-Materials-c-13093.html",
            "label": "Baking Foods & Materials",
            "section": "Shop by Category",
        },
        "food-beverages-food-staples": {
            "url": "https://us.shein.com/Food-Staples-c-13089.html",
            "label": "Food Staples",
            "section": "Shop by Category",
        },
        "food-beverages-convenience-ready-to-eat": {
            "url": "https://us.shein.com/Convenience/Ready-to-eat-c-13094.html",
            "label": "Convenience/Ready-to-eat",
            "section": "Shop by Category",
        },
    },
}
