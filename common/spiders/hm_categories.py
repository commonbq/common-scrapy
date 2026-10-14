"""Current crawlable H&M US category inventory, grouped by storefront department.

Source of truth: the server-rendered ``siteStructure`` block in the H&M US
homepage ``#__NEXT_DATA__`` hydration (https://www2.hm.com/en_us/index.html),
which is the storefront's own navigation taxonomy. Captured and refreshed
2026-10-14.

The mapping is ``{department: {leaf: {name, url, slug}}}``. Leaf keys are
group-qualified (``<department>-<section>-<slug>``) so the bare leaf name used as
the Airflow task id / GCS output path is globally unique across departments.
Each URL is the canonical ``/en_us/...`` product-listing route the spider sends
to the storefront; ``-a category=<department>`` still expands to every leaf in
that department through the base class parent-selector support.
"""

HM_CATEGORIES = {
    "Women": {
        "women-new-arrivals": {
            "name": "New in",
            "url": "https://www2.hm.com/en_us/ladies/new-arrivals.html",
            "slug": "new-arrivals",
        },
        "women-categories-view-all": {
            "name": "View All",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/view-all.html",
            "slug": "view-all",
        },
        "women-categories-bestsellers-redirect": {
            "name": "Best Sellers",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/bestsellers-redirect.html",
            "slug": "bestsellers-redirect",
        },
        "women-categories-dresses": {
            "name": "Dresses",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/dresses.html",
            "slug": "dresses",
        },
        "women-categories-tops": {
            "name": "Tops & T-Shirts",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/tops.html",
            "slug": "tops",
        },
        "women-categories-jeans": {
            "name": "Jeans",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/jeans.html",
            "slug": "jeans",
        },
        "women-categories-trousers": {
            "name": "Pants",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/trousers.html",
            "slug": "trousers",
        },
        "women-categories-shirts-and-blouses": {
            "name": "Blouses & Shirts",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/shirts-and-blouses.html",
            "slug": "shirts-and-blouses",
        },
        "women-categories-basics": {
            "name": "Basics",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/basics.html",
            "slug": "basics",
        },
        "women-categories-sweatpants": {
            "name": "Sweatpants",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/sweatpants.html",
            "slug": "sweatpants",
        },
        "women-categories-cardigans-and-jumpers": {
            "name": "Sweaters & Cardigans",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/cardigans-and-jumpers.html",
            "slug": "cardigans-and-jumpers",
        },
        "women-categories-hoodies-sweatshirts": {
            "name": "Hoodies & Sweatshirts",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/hoodies-sweatshirts.html",
            "slug": "hoodies-sweatshirts",
        },
        "women-categories-jackets-and-coats": {
            "name": "Coats & Jackets",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/jackets-and-coats.html",
            "slug": "jackets-and-coats",
        },
        "women-categories-shorts": {
            "name": "Shorts",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/shorts.html",
            "slug": "shorts",
        },
        "women-categories-skirts": {
            "name": "Skirts",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/skirts.html",
            "slug": "skirts",
        },
        "women-categories-maternity-wear": {
            "name": "Maternity Clothes",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/maternity-wear.html",
            "slug": "maternity-wear",
        },
        "women-categories-blazers-and-waistcoats": {
            "name": "Blazers & Vests",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/blazers-and-waistcoats.html",
            "slug": "blazers-and-waistcoats",
        },
        "women-categories-linen-clothing": {
            "name": "Linen Layers",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/linen-clothing.html",
            "slug": "linen-clothing",
        },
        "women-categories-swimwear": {
            "name": "Swimwear & Beachwear",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/swimwear.html",
            "slug": "swimwear",
        },
        "women-categories-nightwear": {
            "name": "Sleepwear",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/nightwear.html",
            "slug": "nightwear",
        },
        "women-categories-lingerie": {
            "name": "Lingerie",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/lingerie.html",
            "slug": "lingerie",
        },
        "women-categories-loungewear": {
            "name": "Loungewear",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/loungewear.html",
            "slug": "loungewear",
        },
        "women-categories-socks-and-tights": {
            "name": "Socks & Tights",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/socks-and-tights.html",
            "slug": "socks-and-tights",
        },
        "women-categories-jumpsuits": {
            "name": "Jumpsuits & Overalls",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/jumpsuits.html",
            "slug": "jumpsuits",
        },
        "women-categories-care-products": {
            "name": "Care Products",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/care-products.html",
            "slug": "care-products",
        },
        "women-collections-hm-studio": {
            "name": "H&M Studio",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/hm-studio.html",
            "slug": "hm-studio",
        },
        "women-collections-athleisure": {
            "name": "Athleisure Edit",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/athleisure.html",
            "slug": "athleisure",
        },
        "women-collections-functional-essentials": {
            "name": "Functional Essentials",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/functional-essentials.html",
            "slug": "functional-essentials",
        },
        "women-collections-premium-selection": {
            "name": "Premium Selection",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/premium-selection.html",
            "slug": "premium-selection",
        },
        "women-occasions-regional-redirect-collections-1": {
            "name": "Night Out Edit",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/regional-redirect-collections-1.html",
            "slug": "regional-redirect-collections-1",
        },
        "women-occasions-office-wear": {
            "name": "Workwear",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/office-wear.html",
            "slug": "office-wear",
        },
        "women-occasions-party": {
            "name": "Party Wear",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/party.html",
            "slug": "party",
        },
        "women-occasions-wedding": {
            "name": "Wedding Guest",
            "url": "https://www2.hm.com/en_us/ladies/shop-by-product/wedding.html",
            "slug": "wedding",
        },
    },
    "Men": {
        "men-new-arrivals": {
            "name": "New in",
            "url": "https://www2.hm.com/en_us/men/new-arrivals.html",
            "slug": "new-arrivals",
        },
        "men-categories-view-all": {
            "name": "View All",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/view-all.html",
            "slug": "view-all",
        },
        "men-categories-bestsellers-redirect": {
            "name": "Best Sellers",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/bestsellers-redirect.html",
            "slug": "bestsellers-redirect",
        },
        "men-categories-t-shirts-and-tanks": {
            "name": "T-shirts & Tops",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/t-shirts-and-tanks.html",
            "slug": "t-shirts-and-tanks",
        },
        "men-categories-trousers": {
            "name": "Pants",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/trousers.html",
            "slug": "trousers",
        },
        "men-categories-jeans": {
            "name": "Jeans",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/jeans.html",
            "slug": "jeans",
        },
        "men-categories-hoodies-and-sweatshirts": {
            "name": "Hoodies & Sweatshirts",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/hoodies-and-sweatshirts.html",
            "slug": "hoodies-and-sweatshirts",
        },
        "men-categories-sweatpants": {
            "name": "Sweatpants",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/sweatpants.html",
            "slug": "sweatpants",
        },
        "men-categories-blazers-and-suits": {
            "name": "Suits & Blazers",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/blazers-and-suits.html",
            "slug": "blazers-and-suits",
        },
        "men-categories-shirts": {
            "name": "Shirts",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/shirts.html",
            "slug": "shirts",
        },
        "men-categories-jackets-and-coats": {
            "name": "Jackets & Coats",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/jackets-and-coats.html",
            "slug": "jackets-and-coats",
        },
        "men-categories-cardigans-and-jumpers": {
            "name": "Sweaters & Cardigans",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/cardigans-and-jumpers.html",
            "slug": "cardigans-and-jumpers",
        },
        "men-categories-polos": {
            "name": "Polos",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/polos.html",
            "slug": "polos",
        },
        "men-categories-knitwear": {
            "name": "Knitwear",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/knitwear.html",
            "slug": "knitwear",
        },
        "men-categories-shorts": {
            "name": "Shorts",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/shorts.html",
            "slug": "shorts",
        },
        "men-categories-linen-clothing": {
            "name": "Linen Clothing",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/linen-clothing.html",
            "slug": "linen-clothing",
        },
        "men-categories-swimwear": {
            "name": "Swimwear",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/swimwear.html",
            "slug": "swimwear",
        },
        "men-categories-underwear": {
            "name": "Underwear",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/underwear.html",
            "slug": "underwear",
        },
        "men-categories-basics": {
            "name": "Basics",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/basics.html",
            "slug": "basics",
        },
        "men-categories-socks": {
            "name": "Socks",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/socks.html",
            "slug": "socks",
        },
        "men-categories-nightwear-loungewear": {
            "name": "Sleepwear & Loungewear",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/nightwear-loungewear.html",
            "slug": "nightwear-loungewear",
        },
        "men-collections-collections-redirect-1": {
            "name": "Band tees & fits",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/collections-redirect-1.html",
            "slug": "collections-redirect-1",
        },
        "men-collections-athleisure-redirect": {
            "name": "ATHLEISURE EDIT",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/athleisure-redirect.html",
            "slug": "athleisure-redirect",
        },
        "men-collections-atelier": {
            "name": "Atelier",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/atelier.html",
            "slug": "atelier",
        },
        "men-collections-occasion-wear-redirect": {
            "name": "WELL DRESSED EDIT",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/occasion-wear-redirect.html",
            "slug": "occasion-wear-redirect",
        },
        "men-collections-functional-essentials": {
            "name": "Functional Essentials",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/functional-essentials.html",
            "slug": "functional-essentials",
        },
        "men-collections-merch-graphics": {
            "name": "Merch & Graphics",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/merch-graphics.html",
            "slug": "merch-graphics",
        },
        "men-collections-premium-selection": {
            "name": "Premium Selection",
            "url": "https://www2.hm.com/en_us/men/shop-by-product/premium-selection.html",
            "slug": "premium-selection",
        },
    },
    "Kids": {
        "kids-newborn-newborn": {
            "name": "Sale",
            "url": "https://www2.hm.com/en_us/baby/sale/newborn.html",
            "slug": "newborn",
        },
        "kids-newborn-clothing": {
            "name": "Clothing",
            "url": "https://www2.hm.com/en_us/baby/newborn/clothing.html",
            "slug": "clothing",
        },
        "kids-newborn-nightwear": {
            "name": "Pajamas",
            "url": "https://www2.hm.com/en_us/baby/newborn/nightwear.html",
            "slug": "nightwear",
        },
        "kids-newborn-outerwear": {
            "name": "Outerwear",
            "url": "https://www2.hm.com/en_us/baby/newborn/outerwear.html",
            "slug": "outerwear",
        },
        "kids-newborn-shoes": {
            "name": "Shoes",
            "url": "https://www2.hm.com/en_us/baby/newborn/shoes.html",
            "slug": "shoes",
        },
        "kids-newborn-accessories": {
            "name": "Accessories",
            "url": "https://www2.hm.com/en_us/baby/newborn/accessories.html",
            "slug": "accessories",
        },
        "kids-newborn-baby-essentials": {
            "name": "Baby Essentials",
            "url": "https://www2.hm.com/en_us/baby/baby-essentials.html",
            "slug": "baby-essentials",
        },
        "kids-baby-baby": {
            "name": "Sale",
            "url": "https://www2.hm.com/en_us/baby/sale/baby.html",
            "slug": "baby",
        },
        "kids-baby-clothing": {
            "name": "Clothing",
            "url": "https://www2.hm.com/en_us/baby/shop-by-product/clothing.html",
            "slug": "clothing",
        },
        "kids-baby-bestsellers": {
            "name": "Best Sellers from $9.99",
            "url": "https://www2.hm.com/en_us/baby/shop-by-product/bestsellers.html",
            "slug": "bestsellers",
        },
        "kids-baby-nightwear": {
            "name": "Pajamas",
            "url": "https://www2.hm.com/en_us/baby/shop-by-product/nightwear.html",
            "slug": "nightwear",
        },
        "kids-baby-outerwear": {
            "name": "Outerwear",
            "url": "https://www2.hm.com/en_us/baby/shop-by-product/outerwear.html",
            "slug": "outerwear",
        },
        "kids-baby-shoes": {
            "name": "Shoes",
            "url": "https://www2.hm.com/en_us/baby/shop-by-product/shoes.html",
            "slug": "shoes",
        },
        "kids-baby-accessories": {
            "name": "Accessories",
            "url": "https://www2.hm.com/en_us/baby/shop-by-product/accessories.html",
            "slug": "accessories",
        },
        "kids-baby-baby-essentials": {
            "name": "Baby Essentials",
            "url": "https://www2.hm.com/en_us/baby/baby-essentials.html",
            "slug": "baby-essentials",
        },
        "kids-2-8-years-new-arrivals": {
            "name": "New In",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/new-arrivals.html",
            "slug": "new-arrivals",
        },
        "kids-2-8-years-clothing": {
            "name": "Clothing",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/clothing.html",
            "slug": "clothing",
        },
        "kids-2-8-years-the-character-shop": {
            "name": "The Character Shop",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/the-character-shop.html",
            "slug": "the-character-shop",
        },
        "kids-2-8-years-bestsellers": {
            "name": "Bestsellers from $9.99",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/bestsellers.html",
            "slug": "bestsellers",
        },
        "kids-2-8-years-nightwear": {
            "name": "Pajamas",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/nightwear.html",
            "slug": "nightwear",
        },
        "kids-2-8-years-outerwear": {
            "name": "Outerwear",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/outerwear.html",
            "slug": "outerwear",
        },
        "kids-2-8-years-shoes": {
            "name": "Shoes",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/shoes.html",
            "slug": "shoes",
        },
        "kids-2-8-years-accessories": {
            "name": "Accessories",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/accessories.html",
            "slug": "accessories",
        },
        "kids-2-8-years-sportswear": {
            "name": "Activewear",
            "url": "https://www2.hm.com/en_us/kids/shop-by-product/sportswear.html",
            "slug": "sportswear",
        },
        "kids-2-8-years-kids-room": {
            "name": "Kids Room & Toys",
            "url": "https://www2.hm.com/en_us/kids/kids-room.html",
            "slug": "kids-room",
        },
        "kids-2-8-years-2-8y": {
            "name": "Sale",
            "url": "https://www2.hm.com/en_us/kids/sale/2-8y.html",
            "slug": "2-8y",
        },
        "kids-9-14-years-new-arrivals-9-14y": {
            "name": "New In",
            "url": "https://www2.hm.com/en_us/kids/9-14y/new-arrivals-9-14y.html",
            "slug": "new-arrivals-9-14y",
        },
        "kids-9-14-years-clothing": {
            "name": "Clothing",
            "url": "https://www2.hm.com/en_us/kids/9-14y/clothing.html",
            "slug": "clothing",
        },
        "kids-9-14-years-the-character-shop": {
            "name": "The Character Shop",
            "url": "https://www2.hm.com/en_us/kids/9-14y/the-character-shop.html",
            "slug": "the-character-shop",
        },
        "kids-9-14-years-bestsellers-9-14y": {
            "name": "Bestsellers from $14.99",
            "url": "https://www2.hm.com/en_us/kids/9-14y/bestsellers-9-14y.html",
            "slug": "bestsellers-9-14y",
        },
        "kids-9-14-years-outerwear": {
            "name": "Outerwear",
            "url": "https://www2.hm.com/en_us/kids/9-14y/outerwear.html",
            "slug": "outerwear",
        },
        "kids-9-14-years-shoes": {
            "name": "Shoes",
            "url": "https://www2.hm.com/en_us/kids/9-14y/shoes.html",
            "slug": "shoes",
        },
        "kids-9-14-years-accessories": {
            "name": "Accessories",
            "url": "https://www2.hm.com/en_us/kids/9-14y/accessories.html",
            "slug": "accessories",
        },
        "kids-9-14-years-sportswear": {
            "name": "Sportswear",
            "url": "https://www2.hm.com/en_us/kids/9-14y/sportswear.html",
            "slug": "sportswear",
        },
        "kids-9-14-years-9-14y": {
            "name": "Sale",
            "url": "https://www2.hm.com/en_us/kids/sale/9-14y.html",
            "slug": "9-14y",
        },
    },
    "Home": {
        "home-new-arrivals": {
            "name": "New In",
            "url": "https://www2.hm.com/en_us/home/new-arrivals.html",
            "slug": "new-arrivals",
        },
        "home-all-view-all": {
            "name": "View all products",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/view-all.html",
            "slug": "view-all",
        },
        "home-all-best-sellers-shop-redirect": {
            "name": "Best Sellers",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/best-sellers-shop-redirect.html",
            "slug": "best-sellers-shop-redirect",
        },
        "home-all-cooking-dining": {
            "name": "Cooking & Dining",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/cooking-dining.html",
            "slug": "cooking-dining",
        },
        "home-all-bed-linen": {
            "name": "Bedding & Blankets",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/bed-linen.html",
            "slug": "bed-linen",
        },
        "home-all-decorations": {
            "name": "Decorations",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/decorations.html",
            "slug": "decorations",
        },
        "home-all-bath-shower": {
            "name": "Bath & Shower",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/bath-shower.html",
            "slug": "bath-shower",
        },
        "home-all-textiles": {
            "name": "Interior textiles",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/textiles.html",
            "slug": "textiles",
        },
        "home-all-room-fragrance": {
            "name": "Home Fragrance",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/room-fragrance.html",
            "slug": "room-fragrance",
        },
        "home-all-kids": {
            "name": "Kids & Baby",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/kids.html",
            "slug": "kids",
        },
        "home-all-storage": {
            "name": "Storage",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/storage.html",
            "slug": "storage",
        },
        "home-all-furnitures": {
            "name": "Furniture",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/furnitures.html",
            "slug": "furnitures",
        },
        "home-all-lighting": {
            "name": "Lighting",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/lighting.html",
            "slug": "lighting",
        },
        "home-all-sleepwear": {
            "name": "Sleep & Loungewear",
            "url": "https://www2.hm.com/en_us/home/shop-by-product/sleepwear.html",
            "slug": "sleepwear",
        },
    },
    "Beauty": {
        "beauty-new-arrivals": {
            "name": "New In",
            "url": "https://www2.hm.com/en_us/beauty/new-arrivals.html",
            "slug": "new-arrivals",
        },
        "beauty-all-view-all": {
            "name": "View all products",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/view-all.html",
            "slug": "view-all",
        },
        "beauty-all-best-sellers-shop-redirect": {
            "name": "Best Sellers",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/best-sellers-shop-redirect.html",
            "slug": "best-sellers-shop-redirect",
        },
        "beauty-all-fragrance": {
            "name": "Fragrance & Perfume",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/fragrance.html",
            "slug": "fragrance",
        },
        "beauty-all-makeup": {
            "name": "Makeup",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/makeup.html",
            "slug": "makeup",
        },
        "beauty-all-nails": {
            "name": "Nails",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/nails.html",
            "slug": "nails",
        },
        "beauty-all-skin-care": {
            "name": "Skin Care",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/skin-care.html",
            "slug": "skin-care",
        },
        "beauty-all-hair-care": {
            "name": "Hair Care",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/hair-care.html",
            "slug": "hair-care",
        },
        "beauty-all-makeup-bags-cases": {
            "name": "Makeup Bags & Cases",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/makeup-bags-cases.html",
            "slug": "makeup-bags-cases",
        },
        "beauty-all-mini-size": {
            "name": "Mini Size",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/mini-size.html",
            "slug": "mini-size",
        },
        "beauty-all-sets": {
            "name": "Beauty Sets",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/sets.html",
            "slug": "sets",
        },
        "beauty-all-brushes-tools": {
            "name": "Brushes & Tools",
            "url": "https://www2.hm.com/en_us/beauty/shop-by-product/brushes-tools.html",
            "slug": "brushes-tools",
        },
    },
}
