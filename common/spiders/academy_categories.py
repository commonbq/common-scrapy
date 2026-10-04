"""Academy Sports + Outdoors category inventory (issue #132).

Academy is not Next.js: it server-renders a component registry into
``window.ASOData`` as one assignment per component. The global header carries
the full shop taxonomy, captured once on 2026-10-03 from:

    https://www.academy.com/   ->  window.ASOData['comp-<blt...>'] with
         "rcn":"header240"

and specifically ``cms.shop.shop_navigation[0].l1_level``. Nodes recurse through
``l2_level``, ``l3_level`` and ``l4_level``; the label field varies by level
(``title``, ``name`` or ``display_name``) and the product API key is
``category_id``/``unique_id``.

The tree below holds **12 departments / 97 level-2 / 137 level-3 = 246 nodes**
that carry a ``categoryId``. Nodes without an id cannot be requested from
``/api/category/v3/{categoryId}`` and are dropped (their keyed children are
kept). After collapsing cross-listed nodes the inventory resolves to 228 unique
category ids, 213 of which also expose a canonical ``/c/...`` browse URL.

Each node carries ``name``/``categoryId``/``seoUrl``/``url``; the spider derives
every product request from ``categoryId``.
"""

from __future__ import annotations

import json

ACADEMY_CATEGORY_INVENTORY = json.loads(
    r"""
[
 {
  "name": "Deals + Clearance",
  "categoryId": "210952",
  "subcategories": [
   {
    "name": "Hot Deals",
    "categoryId": "210952",
    "seoUrl": "/c/hot-deals",
    "url": "https://www.academy.com/c/hot-deals",
    "subcategories": [
     {
      "name": "Shoes + Boots",
      "categoryId": "3074457345616921636",
      "seoUrl": "/c/hot-deals/hot-deals-on-shoes-boots",
      "url": "https://www.academy.com/c/hot-deals/hot-deals-on-shoes-boots"
     }
    ]
   },
   {
    "name": "Clearance",
    "categoryId": "3074457345616907229",
    "seoUrl": "/c/academy-clearance",
    "url": "https://www.academy.com/c/academy-clearance",
    "subcategories": [
     {
      "name": "Shoes + Boots",
      "categoryId": "3074457345617127098",
      "seoUrl": "/c/academy-clearance/clothing-shoes-clearance/shoes-clearance",
      "url": "https://www.academy.com/c/academy-clearance/clothing-shoes-clearance/shoes-clearance"
     }
    ]
   }
  ]
 },
 {
  "name": "New + Trending",
  "categoryId": "3074457345617089598",
  "subcategories": [
   {
    "name": "New at Academy",
    "categoryId": "3074457345617089598",
    "seoUrl": "/c/new-at-academy",
    "url": "https://www.academy.com/c/new-at-academy"
   },
   {
    "name": "Trending Shops",
    "categoryId": "12345678902819"
   },
   {
    "name": "Trending Brands",
    "categoryId": "123456316851"
   }
  ]
 },
 {
  "name": "Men's",
  "categoryId": "3074457345616968650",
  "seoUrl": "/c/mens",
  "url": "https://www.academy.com/c/mens",
  "subcategories": [
   {
    "name": "Shirts + Tops",
    "categoryId": "15055",
    "seoUrl": "/c/mens/mens-apparel/mens-shirts--t-shirts",
    "url": "https://www.academy.com/c/mens/mens-apparel/mens-shirts--t-shirts",
    "subcategories": [
     {
      "name": "Fishing Shirts",
      "categoryId": "3074457345616972110",
      "seoUrl": "/c/outdoors/fishing/fishing-shoes-clothing/fishing-shirts--t-shirts/mens-fishing-shirts",
      "url": "https://www.academy.com/c/outdoors/fishing/fishing-shoes-clothing/fishing-shirts--t-shirts/mens-fishing-shirts"
     },
     {
      "name": "T-Shirts",
      "categoryId": "3074457345616993099",
      "seoUrl": "/c/mens/mens-apparel/mens-shirts--t-shirts/mens-tees",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-shirts--t-shirts/mens-tees"
     },
     {
      "name": "Polos",
      "categoryId": "3074457345616968712",
      "seoUrl": "/c/mens/mens-apparel/mens-shirts--t-shirts/mens-polos",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-shirts--t-shirts/mens-polos"
     },
     {
      "name": "Button Up Shirts",
      "categoryId": "3074457345616968707",
      "seoUrl": "/c/mens/mens-apparel/mens-shirts--t-shirts/mens-button-downs",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-shirts--t-shirts/mens-button-downs"
     },
     {
      "name": "Hoodies & Sweatshirts",
      "categoryId": "15060",
      "seoUrl": "/c/mens/mens-apparel/mens-hoodies-and-sweatshirts",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-hoodies-and-sweatshirts"
     }
    ]
   },
   {
    "name": "Bottoms",
    "categoryId": "3074457345617166098",
    "seoUrl": "/c/mens/mens-apparel/mens-bottoms",
    "url": "https://www.academy.com/c/mens/mens-apparel/mens-bottoms",
    "subcategories": [
     {
      "name": "Shorts",
      "categoryId": "15061",
      "seoUrl": "/c/mens/mens-apparel/mens-shorts",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-shorts"
     },
     {
      "name": "Jeans",
      "categoryId": "3074457345616990617",
      "seoUrl": "/c/mens/mens-apparel/mens-pants/mens-jeans",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-pants/mens-jeans"
     },
     {
      "name": "Work Pants",
      "categoryId": "235948",
      "seoUrl": "/c/mens/mens-apparel/workwear/work-pants",
      "url": "https://www.academy.com/c/mens/mens-apparel/workwear/work-pants"
     },
     {
      "name": "Athletic + Workout Pants",
      "categoryId": "3074457345616924122",
      "seoUrl": "/c/mens/mens-apparel/mens-pants/mens-athletic-pants--1",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-pants/mens-athletic-pants--1"
     },
     {
      "name": "Cargo Pants",
      "categoryId": "3074457345616990635",
      "seoUrl": "/c/mens/mens-apparel/mens-pants/mens-cargo-pants",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-pants/mens-cargo-pants"
     }
    ]
   },
   {
    "name": "Shoes + Boots",
    "categoryId": "15646",
    "seoUrl": "/c/mens/mens-footwear",
    "url": "https://www.academy.com/c/mens/mens-footwear"
   },
   {
    "name": "Shoes By Sport",
    "categoryId": "239223",
    "seoUrl": "/c/mens/mens-footwear/mens-shoes-by-sport",
    "url": "https://www.academy.com/c/mens/mens-footwear/mens-shoes-by-sport"
   },
   {
    "name": "Workwear",
    "categoryId": "3074457345616908210",
    "seoUrl": "/c/shops/workwear-clothing-boots",
    "url": "https://www.academy.com/c/shops/workwear-clothing-boots"
   },
   {
    "name": "Outdoor Clothing",
    "categoryId": "3074457345616976598",
    "seoUrl": "/c/shops/trending/top-outdoor-brands",
    "url": "https://www.academy.com/c/shops/trending/top-outdoor-brands",
    "subcategories": [
     {
      "name": "Fishing Clothing",
      "categoryId": "3074457345616986098",
      "seoUrl": "/c/mens/mens-apparel/mens-fishing-clothing-",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-fishing-clothing-"
     },
     {
      "name": "Hiking Clothing",
      "categoryId": "3074457345616972637",
      "seoUrl": "/c/outdoors/camping--outdoors/hiking-gear/hiking-clothes-for-the-family/hiking-clothes-for-men",
      "url": "https://www.academy.com/c/outdoors/camping--outdoors/hiking-gear/hiking-clothes-for-the-family/hiking-clothes-for-men"
     },
     {
      "name": "Hiking Boots",
      "categoryId": "15659",
      "seoUrl": "/c/mens/mens-footwear/mens-boots/mens-hiking",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-boots/mens-hiking"
     }
    ]
   },
   {
    "name": "Active Clothing",
    "categoryId": "3074457345616973144",
    "seoUrl": "/c/shops/trending/top-athletic-brands",
    "url": "https://www.academy.com/c/shops/trending/top-athletic-brands",
    "subcategories": [
     {
      "name": "Golf Clothing",
      "categoryId": "3074457345616970234",
      "seoUrl": "/c/sports/golf/golf-apparel/mens-golf-apparel",
      "url": "https://www.academy.com/c/sports/golf/golf-apparel/mens-golf-apparel"
     },
     {
      "name": "Gym Clothes",
      "categoryId": "3074457345616978598",
      "seoUrl": "/c/mens/mens-apparel/mens-workout-clothing--1/mens-training-clothes",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-workout-clothing--1/mens-training-clothes"
     }
    ]
   },
   {
    "name": "Accessories",
    "categoryId": "216434",
    "seoUrl": "/c/mens/mens-accessories",
    "url": "https://www.academy.com/c/mens/mens-accessories",
    "subcategories": [
     {
      "name": "Hats + Beanies",
      "categoryId": "15079",
      "seoUrl": "/c/mens/mens-accessories/mens-hats",
      "url": "https://www.academy.com/c/mens/mens-accessories/mens-hats"
     },
     {
      "name": "Sunglasses",
      "categoryId": "3074457345616968645",
      "seoUrl": "/c/mens/mens-accessories/mens-sunglasses",
      "url": "https://www.academy.com/c/mens/mens-accessories/mens-sunglasses"
     },
     {
      "name": "Underwear",
      "categoryId": "15073",
      "seoUrl": "/c/mens/mens-apparel/mens-underwear",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-underwear"
     },
     {
      "name": "Gaiters",
      "categoryId": "3074457345616971107",
      "seoUrl": "/c/mens/mens-accessories/mens-gaiters-bandanas",
      "url": "https://www.academy.com/c/mens/mens-accessories/mens-gaiters-bandanas"
     }
    ]
   },
   {
    "name": "All Clothing",
    "categoryId": "15054",
    "seoUrl": "/c/mens/mens-apparel",
    "url": "https://www.academy.com/c/mens/mens-apparel",
    "subcategories": [
     {
      "name": "Clearance",
      "categoryId": "3074457345616921147",
      "seoUrl": "/c/academy-clearance/clothing-shoes-clearance/clothing-clearance/mens-clothing-clearance",
      "url": "https://www.academy.com/c/academy-clearance/clothing-shoes-clearance/clothing-clearance/mens-clothing-clearance"
     },
     {
      "name": "Hot Deals",
      "categoryId": "3074457345616907260",
      "seoUrl": "/c/hot-deals/mens-hot-deals-on-apparel-shoes",
      "url": "https://www.academy.com/c/hot-deals/mens-hot-deals-on-apparel-shoes"
     }
    ]
   },
   {
    "name": "Top Brands + Trending",
    "categoryId": "3074457345616972126",
    "subcategories": [
     {
      "name": "New Men's Clothing",
      "categoryId": "3074457345617259599",
      "seoUrl": "/c/mens/mens-apparel/new-mens-clothing",
      "url": "https://www.academy.com/c/mens/mens-apparel/new-mens-clothing"
     },
     {
      "name": "Denim Shop",
      "categoryId": "3074457345617213098",
      "seoUrl": "/c/mens/mens-apparel/mens-denim-clothing",
      "url": "https://www.academy.com/c/mens/mens-apparel/mens-denim-clothing"
     },
     {
      "name": "Western Wear",
      "categoryId": "3074457345617223599",
      "seoUrl": "/c/shops/the-rodeo-shop/mens-western-wear",
      "url": "https://www.academy.com/c/shops/the-rodeo-shop/mens-western-wear"
     },
     {
      "name": "Carhartt",
      "categoryId": "3074457345616993137",
      "seoUrl": "/c/brands/carhartt-brand-shop/mens-carhartt",
      "url": "https://www.academy.com/c/brands/carhartt-brand-shop/mens-carhartt"
     },
     {
      "name": "Nike",
      "categoryId": "3074457345616978103",
      "seoUrl": "/c/brands/nike-brand-shop/mens-nike",
      "url": "https://www.academy.com/c/brands/nike-brand-shop/mens-nike"
     },
     {
      "name": "adidas",
      "categoryId": "3074457345616979609",
      "seoUrl": "/c/brands/adidas/adidas-men",
      "url": "https://www.academy.com/c/brands/adidas/adidas-men"
     },
     {
      "name": "Magellan",
      "categoryId": "3074457345616979615",
      "seoUrl": "/c/brands/magellan/magellan-men",
      "url": "https://www.academy.com/c/brands/magellan/magellan-men"
     },
     {
      "name": "Under Armour",
      "categoryId": "3074457345616979605",
      "seoUrl": "/c/brands/under-armour/under-armour-men",
      "url": "https://www.academy.com/c/brands/under-armour/under-armour-men"
     },
     {
      "name": "BURLEBO",
      "categoryId": "3074457345616971114",
      "seoUrl": "/c/brands/brands-a-to-d/burlebo/burlebo-apparel",
      "url": "https://www.academy.com/c/brands/brands-a-to-d/burlebo/burlebo-apparel"
     }
    ]
   }
  ]
 },
 {
  "name": "Women's",
  "categoryId": "3074457345616968651",
  "seoUrl": "/c/womens",
  "url": "https://www.academy.com/c/womens",
  "subcategories": [
   {
    "name": "Shirts + Tops",
    "categoryId": "15116",
    "seoUrl": "/c/womens/womens-apparel/womens-shirts--tops",
    "url": "https://www.academy.com/c/womens/womens-apparel/womens-shirts--tops",
    "subcategories": [
     {
      "name": "Polos",
      "categoryId": "3074457345616968750",
      "seoUrl": "/c/womens/womens-apparel/womens-shirts--tops/womens-polos--1",
      "url": "https://www.academy.com/c/womens/womens-apparel/womens-shirts--tops/womens-polos--1"
     },
     {
      "name": "Sports Bras",
      "categoryId": "3074457345616924254",
      "seoUrl": "/c/womens/womens-apparel/womens-sports-bras",
      "url": "https://www.academy.com/c/womens/womens-apparel/womens-sports-bras"
     },
     {
      "name": "Long Sleeve Shirts",
      "categoryId": "3074457345617099598",
      "seoUrl": "/c/womens/womens-apparel/womens-shirts--tops/womens-long-sleeve-shirts",
      "url": "https://www.academy.com/c/womens/womens-apparel/womens-shirts--tops/womens-long-sleeve-shirts"
     }
    ]
   },
   {
    "name": "Bottoms",
    "categoryId": "3074457345617165098",
    "seoUrl": "/c/womens/womens-apparel/womens-bottoms",
    "url": "https://www.academy.com/c/womens/womens-apparel/womens-bottoms",
    "subcategories": [
     {
      "name": "Pants",
      "categoryId": "15119",
      "seoUrl": "/c/womens/womens-apparel/womens-pants",
      "url": "https://www.academy.com/c/womens/womens-apparel/womens-pants"
     }
    ]
   },
   {
    "name": "Shoes + Boots",
    "categoryId": "15630",
    "seoUrl": "/c/womens/womens-footwear",
    "url": "https://www.academy.com/c/womens/womens-footwear",
    "subcategories": [
     {
      "name": "Casual Shoes",
      "categoryId": "15680",
      "seoUrl": "/c/womens/womens-footwear/womens-casual-shoes",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-casual-shoes"
     },
     {
      "name": "Athletic Sneakers",
      "categoryId": "239222",
      "seoUrl": "/c/womens/womens-footwear/womens-athletic-sneakers",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-athletic-sneakers"
     },
     {
      "name": "Slides, Sandals + Flip-Flops",
      "categoryId": "3074457345616932606",
      "seoUrl": "/c/womens/womens-footwear/womens-casual-shoes/women-sandals",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-casual-shoes/women-sandals"
     }
    ]
   },
   {
    "name": "Shoes by Sport",
    "categoryId": "239224",
    "seoUrl": "/c/womens/womens-footwear/womens-shoes-by-sport",
    "url": "https://www.academy.com/c/womens/womens-footwear/womens-shoes-by-sport"
   },
   {
    "name": "Active Clothing",
    "categoryId": "239433",
    "seoUrl": "/c/womens/womens-apparel/womens-workout-clothing",
    "url": "https://www.academy.com/c/womens/womens-apparel/womens-workout-clothing"
   },
   {
    "name": "Outdoor Clothing",
    "categoryId": "3074457345616976598",
    "seoUrl": "/c/shops/trending/top-outdoor-brands",
    "url": "https://www.academy.com/c/shops/trending/top-outdoor-brands"
   },
   {
    "name": "Accessories",
    "categoryId": "216438",
    "seoUrl": "/c/womens/womens-accessories",
    "url": "https://www.academy.com/c/womens/womens-accessories"
   },
   {
    "name": "Workwear",
    "categoryId": "3074457345616970143",
    "seoUrl": "/c/womens/womens-apparel/womens-workwear",
    "url": "https://www.academy.com/c/womens/womens-apparel/womens-workwear"
   },
   {
    "name": "All Clothing",
    "categoryId": "15082",
    "seoUrl": "/c/womens/womens-apparel",
    "url": "https://www.academy.com/c/womens/womens-apparel"
   },
   {
    "name": "Top Brands + Trending",
    "categoryId": "3074457345616968694",
    "subcategories": [
     {
      "name": "Freely",
      "categoryId": "3074457345616971119",
      "seoUrl": "/c/brands/freely/freely-womens",
      "url": "https://www.academy.com/c/brands/freely/freely-womens"
     },
     {
      "name": "Nike",
      "categoryId": "3074457345616978102",
      "seoUrl": "/c/brands/nike-brand-shop/womens-nike",
      "url": "https://www.academy.com/c/brands/nike-brand-shop/womens-nike"
     },
     {
      "name": "adidas",
      "categoryId": "3074457345616979610",
      "seoUrl": "/c/brands/adidas/adidas-women",
      "url": "https://www.academy.com/c/brands/adidas/adidas-women"
     },
     {
      "name": "Brooks",
      "categoryId": "3074457345616919105",
      "seoUrl": "/c/brands/brooks/womens-shoes-by-brooks",
      "url": "https://www.academy.com/c/brands/brooks/womens-shoes-by-brooks"
     },
     {
      "name": "Magellan",
      "categoryId": "3074457345616979616",
      "seoUrl": "/c/brands/magellan/magellan-women",
      "url": "https://www.academy.com/c/brands/magellan/magellan-women"
     },
     {
      "name": "Under Armour",
      "categoryId": "3074457345616979606",
      "seoUrl": "/c/brands/under-armour/under-armour-women",
      "url": "https://www.academy.com/c/brands/under-armour/under-armour-women"
     }
    ]
   },
   {
    "name": "Swimwear",
    "categoryId": "233434",
    "seoUrl": "/c/womens/womens-swimsuits--cover-ups",
    "url": "https://www.academy.com/c/womens/womens-swimsuits--cover-ups",
    "subcategories": [
     {
      "name": "Swim Tops",
      "categoryId": "233437",
      "seoUrl": "/c/womens/womens-swimsuits--cover-ups/womens-swim-tops",
      "url": "https://www.academy.com/c/womens/womens-swimsuits--cover-ups/womens-swim-tops"
     },
     {
      "name": "Swim Bottoms",
      "categoryId": "233436",
      "seoUrl": "/c/womens/womens-swimsuits--cover-ups/womens-swim-bottoms",
      "url": "https://www.academy.com/c/womens/womens-swimsuits--cover-ups/womens-swim-bottoms"
     },
     {
      "name": "One-Piece Swim Suits",
      "categoryId": "233435",
      "seoUrl": "/c/womens/womens-swimsuits--cover-ups/womens-one-piece-swimsuits",
      "url": "https://www.academy.com/c/womens/womens-swimsuits--cover-ups/womens-one-piece-swimsuits"
     },
     {
      "name": "Rashgaurds",
      "categoryId": "239047",
      "seoUrl": "/c/womens/womens-swimsuits--cover-ups/womens-rash-guards",
      "url": "https://www.academy.com/c/womens/womens-swimsuits--cover-ups/womens-rash-guards"
     }
    ]
   }
  ]
 },
 {
  "name": "Kids'",
  "categoryId": "3074457345616931607",
  "seoUrl": "/c/kids",
  "url": "https://www.academy.com/c/kids",
  "subcategories": [
   {
    "name": "Boys' Clothing",
    "categoryId": "15090",
    "seoUrl": "/c/kids/boys-apparel",
    "url": "https://www.academy.com/c/kids/boys-apparel",
    "subcategories": [
     {
      "name": "Shirts + Tops",
      "categoryId": "15091",
      "seoUrl": "/c/kids/boys-apparel/boys-shirts--t-shirts",
      "url": "https://www.academy.com/c/kids/boys-apparel/boys-shirts--t-shirts"
     },
     {
      "name": "Pants + Jeans",
      "categoryId": "15094",
      "seoUrl": "/c/kids/boys-apparel/boys-pants",
      "url": "https://www.academy.com/c/kids/boys-apparel/boys-pants"
     },
     {
      "name": "Shorts",
      "categoryId": "15097",
      "seoUrl": "/c/kids/boys-apparel/boys-shorts",
      "url": "https://www.academy.com/c/kids/boys-apparel/boys-shorts"
     },
     {
      "name": "Hoodies + Sweatshirts",
      "categoryId": "197960",
      "seoUrl": "/c/kids/boys-apparel/boys-hoodies--sweatshirts",
      "url": "https://www.academy.com/c/kids/boys-apparel/boys-hoodies--sweatshirts"
     }
    ]
   },
   {
    "name": "Girls' Clothing",
    "categoryId": "15109",
    "seoUrl": "/c/kids/girls-apparel",
    "url": "https://www.academy.com/c/kids/girls-apparel",
    "subcategories": [
     {
      "name": "Shirts + Tops",
      "categoryId": "15110",
      "seoUrl": "/c/kids/girls-apparel/girls-shirts--t-shirts",
      "url": "https://www.academy.com/c/kids/girls-apparel/girls-shirts--t-shirts"
     },
     {
      "name": "Pants + Leggings",
      "categoryId": "15113",
      "seoUrl": "/c/kids/girls-apparel/girls-pants",
      "url": "https://www.academy.com/c/kids/girls-apparel/girls-pants"
     },
     {
      "name": "Shorts",
      "categoryId": "15158",
      "seoUrl": "/c/kids/girls-apparel/girls-shorts",
      "url": "https://www.academy.com/c/kids/girls-apparel/girls-shorts"
     },
     {
      "name": "Hoodies + Sweatshirts",
      "categoryId": "197571",
      "seoUrl": "/c/kids/girls-apparel/girls-hoodies--sweatshirts",
      "url": "https://www.academy.com/c/kids/girls-apparel/girls-hoodies--sweatshirts"
     }
    ]
   },
   {
    "name": "Kids' Shoes",
    "categoryId": "3074457345616931617",
    "seoUrl": "/c/kids/kids-shoes",
    "url": "https://www.academy.com/c/kids/kids-shoes",
    "subcategories": [
     {
      "name": "Boys' Shoes",
      "categoryId": "15692",
      "seoUrl": "/c/kids/kids-shoes/boys-footwear",
      "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear"
     },
     {
      "name": "Girls' Shoes",
      "categoryId": "15663",
      "seoUrl": "/c/kids/kids-shoes/girls-footwear",
      "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear"
     },
     {
      "name": "Grade School (Size 3.5 - 7)",
      "categoryId": "3074457345617044598",
      "seoUrl": "/c/kids/kids-shoes/big-kids-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/big-kids-shoes"
     },
     {
      "name": "Preschool (Size 11-3)",
      "categoryId": "3074457345617044599",
      "seoUrl": "/c/kids/kids-shoes/little-kids-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/little-kids-shoes"
     },
     {
      "name": "Toddler (Size 5 - 10)",
      "categoryId": "15718",
      "seoUrl": "/c/kids/kids-shoes/toddler-footwear",
      "url": "https://www.academy.com/c/kids/kids-shoes/toddler-footwear"
     },
     {
      "name": "Athletic + Sneakers",
      "categoryId": "3074457345616989602",
      "seoUrl": "/c/kids/kids-shoes/kids-sneakers",
      "url": "https://www.academy.com/c/kids/kids-shoes/kids-sneakers"
     },
     {
      "name": "Sandals, Slides + Flip-Flops",
      "categoryId": "3074457345616989621",
      "seoUrl": "/c/kids/kids-shoes/kids-sandals",
      "url": "https://www.academy.com/c/kids/kids-shoes/kids-sandals"
     },
     {
      "name": "Cleats",
      "categoryId": "3074457345616989601",
      "seoUrl": "/c/kids/kids-shoes/kids-cleats",
      "url": "https://www.academy.com/c/kids/kids-shoes/kids-cleats"
     }
    ]
   },
   {
    "name": "Shoes By Sport",
    "categoryId": "239535",
    "seoUrl": "/c/kids/kids-shoes/kids-shop-by-sport",
    "url": "https://www.academy.com/c/kids/kids-shoes/kids-shop-by-sport"
   },
   {
    "name": "Kids' Accessories",
    "categoryId": "3074457345616971144",
    "seoUrl": "/c/kids/accessories-for-kids",
    "url": "https://www.academy.com/c/kids/accessories-for-kids",
    "subcategories": [
     {
      "name": "Kids Socks",
      "categoryId": "3074457345616971137",
      "seoUrl": "/c/kids/accessories-for-kids/kids-accessories-socks",
      "url": "https://www.academy.com/c/kids/accessories-for-kids/kids-accessories-socks"
     },
     {
      "name": "Hats",
      "categoryId": "15103",
      "seoUrl": "/c/kids/accessories-for-kids/kids-accessories-hats",
      "url": "https://www.academy.com/c/kids/accessories-for-kids/kids-accessories-hats"
     }
    ]
   },
   {
    "name": "Sports Equipment",
    "categoryId": "3074457345616933672",
    "seoUrl": "/c/kids/kids-sports",
    "url": "https://www.academy.com/c/kids/kids-sports"
   },
   {
    "name": "Fun + Play",
    "categoryId": "1234"
   },
   {
    "name": "Trending + Top Brands",
    "categoryId": "12341234",
    "seoUrl": "/c/kids/kids-trending",
    "url": "https://www.academy.com/c/kids/kids-trending",
    "subcategories": [
     {
      "name": "Boys' Jordan Clothing",
      "categoryId": "3074457345617093598",
      "seoUrl": "/c/brands/jordan/boys-jordan",
      "url": "https://www.academy.com/c/brands/jordan/boys-jordan"
     },
     {
      "name": "Girls' Jordan Clothing",
      "categoryId": "3074457345617093599",
      "seoUrl": "/c/brands/jordan/girls-jordan",
      "url": "https://www.academy.com/c/brands/jordan/girls-jordan"
     }
    ]
   }
  ]
 },
 {
  "name": "Shoes + Boots",
  "categoryId": "15645",
  "seoUrl": "/c/footwear",
  "url": "https://www.academy.com/c/footwear",
  "subcategories": [
   {
    "name": "Men's Shoes",
    "categoryId": "15646",
    "seoUrl": "/c/mens/mens-footwear",
    "url": "https://www.academy.com/c/mens/mens-footwear",
    "subcategories": [
     {
      "name": "Athletic + Sneakers",
      "categoryId": "239221",
      "seoUrl": "/c/mens/mens-footwear/mens-athletic-sneakers",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-athletic-sneakers"
     },
     {
      "name": "Casual Shoes",
      "categoryId": "15655",
      "seoUrl": "/c/mens/mens-footwear/mens-casual-shoes",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-casual-shoes"
     },
     {
      "name": "Running Shoes",
      "categoryId": "15660",
      "seoUrl": "/c/mens/mens-footwear/mens-athletic-sneakers/mens-running-shoes",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-athletic-sneakers/mens-running-shoes"
     },
     {
      "name": "Work Boots + Shoes",
      "categoryId": "15654",
      "seoUrl": "/c/mens/mens-footwear/mens-boots/mens-work-boots",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-boots/mens-work-boots"
     },
     {
      "name": "Slides, Sandals + Flip-Flops",
      "categoryId": "3074457345616932605",
      "seoUrl": "/c/mens/mens-footwear/mens-casual-shoes/men-sandals",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-casual-shoes/men-sandals"
     },
     {
      "name": "Cleats",
      "categoryId": "15656",
      "seoUrl": "/c/mens/mens-footwear/mens-cleats",
      "url": "https://www.academy.com/c/mens/mens-footwear/mens-cleats"
     }
    ]
   },
   {
    "name": "Women's Shoes",
    "categoryId": "15630",
    "seoUrl": "/c/womens/womens-footwear",
    "url": "https://www.academy.com/c/womens/womens-footwear",
    "subcategories": [
     {
      "name": "Athletic + Sneakers",
      "categoryId": "239222",
      "seoUrl": "/c/womens/womens-footwear/womens-athletic-sneakers",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-athletic-sneakers"
     },
     {
      "name": "Casual Shoes",
      "categoryId": "15680",
      "seoUrl": "/c/womens/womens-footwear/womens-casual-shoes",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-casual-shoes"
     },
     {
      "name": "Running Shoes",
      "categoryId": "15685",
      "seoUrl": "/c/womens/womens-footwear/womens-athletic-sneakers/womens-running-shoes",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-athletic-sneakers/womens-running-shoes"
     },
     {
      "name": "Work Boots + Shoes",
      "categoryId": "15679",
      "seoUrl": "/c/womens/womens-footwear/womens-boots/womens-work-boots",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-boots/womens-work-boots"
     },
     {
      "name": "Slides, Sandals + Flip-Flops",
      "categoryId": "17429",
      "seoUrl": "/c/womens/womens-footwear/womens-casual-shoes/women-sandals",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-casual-shoes/women-sandals"
     },
     {
      "name": "Cleats",
      "categoryId": "15681",
      "seoUrl": "/c/womens/womens-footwear/womens-cleats",
      "url": "https://www.academy.com/c/womens/womens-footwear/womens-cleats"
     }
    ]
   },
   {
    "name": "Boys' Shoes",
    "categoryId": "15692",
    "seoUrl": "/c/kids/kids-shoes/boys-footwear",
    "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear",
    "subcategories": [
     {
      "name": "Athletic + Sneakers",
      "categoryId": "239533",
      "seoUrl": "/c/kids/kids-shoes/boys-footwear/boys-athletic-sneakers",
      "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear/boys-athletic-sneakers"
     },
     {
      "name": "Grade School (Size 3.5 - 7)",
      "categoryId": "3074457345617044598",
      "seoUrl": "/c/kids/kids-shoes/big-kids-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/big-kids-shoes"
     },
     {
      "name": "Pre School (Size 11 - 3)",
      "categoryId": "3074457345617044599",
      "seoUrl": "/c/kids/kids-shoes/little-kids-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/little-kids-shoes"
     },
     {
      "name": "Toddler (Size 5 - 10)",
      "categoryId": "3074457345616907207",
      "seoUrl": "/c/kids/kids-shoes/boys-footwear/boys-toddler-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear/boys-toddler-shoes"
     },
     {
      "name": "Slides, Sandals + Flip-Flops",
      "categoryId": "3074457345616932607",
      "seoUrl": "/c/kids/kids-shoes/boys-footwear/boys-sandals",
      "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear/boys-sandals"
     },
     {
      "name": "Slippers",
      "categoryId": "17464",
      "seoUrl": "/c/kids/kids-shoes/boys-footwear/boys-slippers",
      "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear/boys-slippers"
     },
     {
      "name": "Cleats",
      "categoryId": "15700",
      "seoUrl": "/c/kids/kids-shoes/boys-footwear/boys-cleats",
      "url": "https://www.academy.com/c/kids/kids-shoes/boys-footwear/boys-cleats"
     }
    ]
   },
   {
    "name": "Girls' Shoes",
    "categoryId": "15663",
    "seoUrl": "/c/kids/kids-shoes/girls-footwear",
    "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear",
    "subcategories": [
     {
      "name": "Athletic + Sneakers",
      "categoryId": "239540",
      "seoUrl": "/c/kids/kids-shoes/girls-footwear/girls-athletic-sneakers",
      "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear/girls-athletic-sneakers"
     },
     {
      "name": "Grade School (Size 3.5 - 7)",
      "categoryId": "3074457345617044598",
      "seoUrl": "/c/kids/kids-shoes/big-kids-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/big-kids-shoes"
     },
     {
      "name": "Pre School (Size 11 - 3)",
      "categoryId": "3074457345617044599",
      "seoUrl": "/c/kids/kids-shoes/little-kids-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/little-kids-shoes"
     },
     {
      "name": "Toddler (Size 5 - 10)",
      "categoryId": "3074457345616907206",
      "seoUrl": "/c/kids/kids-shoes/girls-footwear/girls-toddler-shoes",
      "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear/girls-toddler-shoes"
     },
     {
      "name": "Slides, Sandals + Flip-Flops",
      "categoryId": "3074457345616932608",
      "seoUrl": "/c/kids/kids-shoes/girls-footwear/girls-sandals",
      "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear/girls-sandals"
     },
     {
      "name": "Slippers",
      "categoryId": "17911",
      "seoUrl": "/c/kids/kids-shoes/girls-footwear/girls-slippers",
      "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear/girls-slippers"
     },
     {
      "name": "Cleats",
      "categoryId": "15671",
      "seoUrl": "/c/kids/kids-shoes/girls-footwear/girls-cleats",
      "url": "https://www.academy.com/c/kids/kids-shoes/girls-footwear/girls-cleats"
     }
    ]
   },
   {
    "name": "Shoes by Sport",
    "categoryId": "239148",
    "seoUrl": "/c/footwear/shoes-by-sport",
    "url": "https://www.academy.com/c/footwear/shoes-by-sport",
    "subcategories": [
     {
      "name": "Running Shoes",
      "categoryId": "195950",
      "seoUrl": "/c/footwear/athletic-shoes-sneakers/running-shoes",
      "url": "https://www.academy.com/c/footwear/athletic-shoes-sneakers/running-shoes"
     },
     {
      "name": "Basketball Shoes",
      "categoryId": "183447",
      "seoUrl": "/c/sports/basketball/basketball-shoes",
      "url": "https://www.academy.com/c/sports/basketball/basketball-shoes"
     },
     {
      "name": "Soccer Cleats",
      "categoryId": "16231",
      "seoUrl": "/c/sports/soccer/soccer-cleats",
      "url": "https://www.academy.com/c/sports/soccer/soccer-cleats"
     },
     {
      "name": "Football Cleats",
      "categoryId": "16143",
      "seoUrl": "/c/sports/football/football-cleats",
      "url": "https://www.academy.com/c/sports/football/football-cleats"
     },
     {
      "name": "Baseball Cleats",
      "categoryId": "16179",
      "seoUrl": "/c/sports/baseball/baseball-cleats",
      "url": "https://www.academy.com/c/sports/baseball/baseball-cleats"
     }
    ]
   },
   {
    "name": "Boots",
    "categoryId": "61402",
    "seoUrl": "/c/footwear/boots",
    "url": "https://www.academy.com/c/footwear/boots",
    "subcategories": [
     {
      "name": "Work Boots + Shoes",
      "categoryId": "194521",
      "seoUrl": "/c/footwear/boots/work-boots",
      "url": "https://www.academy.com/c/footwear/boots/work-boots"
     },
     {
      "name": "Western Boots",
      "categoryId": "155808",
      "seoUrl": "/c/footwear/boots/western-boots",
      "url": "https://www.academy.com/c/footwear/boots/western-boots"
     },
     {
      "name": "Steel Toe Boots",
      "categoryId": "3074457345616954131",
      "seoUrl": "/c/footwear/boots/work-boots/steel-toe-boots-shoes",
      "url": "https://www.academy.com/c/footwear/boots/work-boots/steel-toe-boots-shoes"
     },
     {
      "name": "Rain + Rubber Boots",
      "categoryId": "187957",
      "seoUrl": "/c/footwear/boots/rain--rubber-boots",
      "url": "https://www.academy.com/c/footwear/boots/rain--rubber-boots"
     },
     {
      "name": "Hiking Boots",
      "categoryId": "186968",
      "seoUrl": "/c/outdoors/camping--outdoors/hiking-gear/hiking-boots",
      "url": "https://www.academy.com/c/outdoors/camping--outdoors/hiking-gear/hiking-boots"
     },
     {
      "name": "Hunting Boots",
      "categoryId": "38301",
      "seoUrl": "/c/outdoors/hunting/hunting-boots-camo-clothing--1/hunting-boots",
      "url": "https://www.academy.com/c/outdoors/hunting/hunting-boots-camo-clothing--1/hunting-boots"
     },
     {
      "name": "Casual Boots",
      "categoryId": "196131",
      "seoUrl": "/c/footwear/boots/casual-boots",
      "url": "https://www.academy.com/c/footwear/boots/casual-boots"
     },
     {
      "name": "Winter Boots",
      "categoryId": "3074457345616911602",
      "seoUrl": "/c/footwear/boots/winter-boots",
      "url": "https://www.academy.com/c/footwear/boots/winter-boots"
     }
    ]
   },
   {
    "name": "Top Brands",
    "categoryId": "77777788888",
    "subcategories": [
     {
      "name": "Nike",
      "categoryId": "3074457345616909624",
      "seoUrl": "/c/brands/nike-brand-shop/nike-footwear",
      "url": "https://www.academy.com/c/brands/nike-brand-shop/nike-footwear"
     },
     {
      "name": "Jordan",
      "categoryId": "3074457345617094098",
      "seoUrl": "/c/brands/jordan/jordan-shoes",
      "url": "https://www.academy.com/c/brands/jordan/jordan-shoes"
     },
     {
      "name": "Brooks",
      "categoryId": "3074457345616919104",
      "seoUrl": "/c/brands/brooks",
      "url": "https://www.academy.com/c/brands/brooks"
     },
     {
      "name": "Adidas",
      "categoryId": "3074457345616909627",
      "seoUrl": "/c/brands/adidas/adidas-shoes",
      "url": "https://www.academy.com/c/brands/adidas/adidas-shoes"
     },
     {
      "name": "Crocs",
      "categoryId": "3074457345616911120",
      "seoUrl": "/c/brands/crocs-brand-shop",
      "url": "https://www.academy.com/c/brands/crocs-brand-shop"
     },
     {
      "name": "New Balance",
      "categoryId": "3074457345616919108",
      "seoUrl": "/c/brands/brands-m-r/new-balance",
      "url": "https://www.academy.com/c/brands/brands-m-r/new-balance"
     },
     {
      "name": "Birkenstock",
      "categoryId": "3074457345616984148",
      "seoUrl": "/c/brands/brands-a-to-d/birkenstock",
      "url": "https://www.academy.com/c/brands/brands-a-to-d/birkenstock"
     },
     {
      "name": "Converse",
      "categoryId": "3074457345616928601",
      "seoUrl": "/c/brands/converse",
      "url": "https://www.academy.com/c/brands/converse"
     },
     {
      "name": "HEYDUDE",
      "categoryId": "3074457345616974618",
      "seoUrl": "/c/brands/hey-dude-shoes",
      "url": "https://www.academy.com/c/brands/hey-dude-shoes"
     },
     {
      "name": "Skechers",
      "categoryId": "239014",
      "seoUrl": "/c/brands/skechers",
      "url": "https://www.academy.com/c/brands/skechers"
     }
    ]
   },
   {
    "name": "Socks + Accessories",
    "categoryId": "777788881",
    "subcategories": [
     {
      "name": "Socks",
      "categoryId": "15719",
      "seoUrl": "/c/shops/all-accessories/socks",
      "url": "https://www.academy.com/c/shops/all-accessories/socks"
     },
     {
      "name": "Long Sports Socks",
      "categoryId": "217449",
      "seoUrl": "/c/shops/all-accessories/socks/team-socks",
      "url": "https://www.academy.com/c/shops/all-accessories/socks/team-socks"
     },
     {
      "name": "Shoe Accessories",
      "categoryId": "15722",
      "seoUrl": "/c/footwear/socks--shoes-accessories",
      "url": "https://www.academy.com/c/footwear/socks--shoes-accessories"
     },
     {
      "name": "Insoles",
      "categoryId": "17932",
      "seoUrl": "/c/footwear/socks--shoes-accessories/insoles",
      "url": "https://www.academy.com/c/footwear/socks--shoes-accessories/insoles"
     }
    ]
   },
   {
    "name": "Shoes on Sale",
    "categoryId": "3074457345616921636",
    "seoUrl": "/c/hot-deals/hot-deals-on-shoes-boots",
    "url": "https://www.academy.com/c/hot-deals/hot-deals-on-shoes-boots"
   }
  ]
 },
 {
  "name": "Outdoors",
  "categoryId": "220431",
  "seoUrl": "/c/outdoors",
  "url": "https://www.academy.com/c/outdoors",
  "subcategories": [
   {
    "name": "Hunting",
    "categoryId": "15758",
    "seoUrl": "/c/outdoors/hunting",
    "url": "https://www.academy.com/c/outdoors/hunting"
   },
   {
    "name": "Firearms + Ammo",
    "categoryId": "64413",
    "seoUrl": "/c/outdoors/shooting",
    "url": "https://www.academy.com/c/outdoors/shooting"
   },
   {
    "name": "Fishing",
    "categoryId": "15478",
    "seoUrl": "/c/outdoors/fishing",
    "url": "https://www.academy.com/c/outdoors/fishing"
   },
   {
    "name": "Camping + Hiking",
    "categoryId": "15286",
    "seoUrl": "/c/outdoors/camping--outdoors",
    "url": "https://www.academy.com/c/outdoors/camping--outdoors"
   },
   {
    "name": "Boating",
    "categoryId": "15157",
    "seoUrl": "/c/outdoors/boating",
    "url": "https://www.academy.com/c/outdoors/boating"
   },
   {
    "name": "Water Bottles + Tumblers",
    "categoryId": "16290",
    "seoUrl": "/c/outdoors/insulated-drinkware",
    "url": "https://www.academy.com/c/outdoors/insulated-drinkware"
   },
   {
    "name": "Coolers",
    "categoryId": "3074457345616954170",
    "seoUrl": "/c/outdoors/coolers",
    "url": "https://www.academy.com/c/outdoors/coolers",
    "subcategories": [
     {
      "name": "Hard-Sided Coolers",
      "categoryId": "15993",
      "seoUrl": "/c/outdoors/coolers/hard-sided-coolers",
      "url": "https://www.academy.com/c/outdoors/coolers/hard-sided-coolers"
     },
     {
      "name": "Soft-Sided Coolers",
      "categoryId": "15996",
      "seoUrl": "/c/outdoors/coolers/soft-sided-coolers",
      "url": "https://www.academy.com/c/outdoors/coolers/soft-sided-coolers"
     },
     {
      "name": "Wheeled Coolers",
      "categoryId": "3074457345616982103",
      "seoUrl": "/c/outdoors/coolers/wheeled-coolers",
      "url": "https://www.academy.com/c/outdoors/coolers/wheeled-coolers"
     },
     {
      "name": "Backpack Coolers",
      "categoryId": "3074457345616982104",
      "seoUrl": "/c/outdoors/coolers/backpack-coolers",
      "url": "https://www.academy.com/c/outdoors/coolers/backpack-coolers"
     },
     {
      "name": "Coolers on Sale",
      "categoryId": "3074457345617167098",
      "seoUrl": "/c/outdoors/coolers/coolers-on-sale",
      "url": "https://www.academy.com/c/outdoors/coolers/coolers-on-sale"
     }
    ]
   },
   {
    "name": "Knives + Self Defense",
    "categoryId": "123456789"
   },
   {
    "name": "Featured",
    "categoryId": "1234524"
   }
  ]
 },
 {
  "name": "Firearms + Ammo",
  "categoryId": "64413",
  "seoUrl": "/c/outdoors/shooting",
  "url": "https://www.academy.com/c/outdoors/shooting",
  "subcategories": [
   {
    "name": "Handguns",
    "categoryId": "3074457345616968636",
    "seoUrl": "/c/outdoors/shooting/firearms/handguns",
    "url": "https://www.academy.com/c/outdoors/shooting/firearms/handguns",
    "subcategories": [
     {
      "name": "Shop All Handguns",
      "categoryId": "3074457345616968636",
      "seoUrl": "/c/outdoors/shooting/firearms/handguns",
      "url": "https://www.academy.com/c/outdoors/shooting/firearms/handguns"
     }
    ]
   },
   {
    "name": "Rifles",
    "categoryId": "15818",
    "seoUrl": "/c/outdoors/shooting/firearms/rifles",
    "url": "https://www.academy.com/c/outdoors/shooting/firearms/rifles",
    "subcategories": [
     {
      "name": "Shop All Rifles",
      "categoryId": "15818",
      "seoUrl": "/c/outdoors/shooting/firearms/rifles",
      "url": "https://www.academy.com/c/outdoors/shooting/firearms/rifles"
     }
    ]
   },
   {
    "name": "Shotguns",
    "categoryId": "15819",
    "seoUrl": "/c/outdoors/shooting/firearms/shotguns",
    "url": "https://www.academy.com/c/outdoors/shooting/firearms/shotguns",
    "subcategories": [
     {
      "name": "Double Barrel",
      "categoryId": "Double Barrel",
      "seoUrl": "/c/outdoors/shooting/firearms/shotguns/double-barrel-shotguns",
      "url": "https://www.academy.com/c/outdoors/shooting/firearms/shotguns/double-barrel-shotguns"
     },
     {
      "name": "Shop All Shotguns",
      "categoryId": "15819",
      "seoUrl": "/c/outdoors/shooting/firearms/shotguns",
      "url": "https://www.academy.com/c/outdoors/shooting/firearms/shotguns"
     }
    ]
   },
   {
    "name": "Ammo",
    "categoryId": "15759",
    "seoUrl": "/c/outdoors/shooting/ammunition",
    "url": "https://www.academy.com/c/outdoors/shooting/ammunition"
   },
   {
    "name": "Gun Storage + Safety",
    "categoryId": "15832",
    "seoUrl": "/c/outdoors/shooting/gun-storage--safety",
    "url": "https://www.academy.com/c/outdoors/shooting/gun-storage--safety"
   },
   {
    "name": "Featured Brands",
    "categoryId": "1234567"
   },
   {
    "name": "Optics + Scopes",
    "categoryId": "15941",
    "seoUrl": "/c/outdoors/hunting/optics",
    "url": "https://www.academy.com/c/outdoors/hunting/optics"
   },
   {
    "name": "Gun Accessories",
    "categoryId": "15798",
    "seoUrl": "/c/outdoors/shooting/shooting-gear--accessories",
    "url": "https://www.academy.com/c/outdoors/shooting/shooting-gear--accessories"
   },
   {
    "name": "Gun Deals",
    "categoryId": "3074457345617058598",
    "seoUrl": "/c/shops/black-friday/gun-deals",
    "url": "https://www.academy.com/c/shops/black-friday/gun-deals"
   }
  ]
 },
 {
  "name": "Sports",
  "categoryId": "220432",
  "seoUrl": "/c/sports",
  "url": "https://www.academy.com/c/sports",
  "subcategories": [
   {
    "name": "Baseball",
    "categoryId": "16155",
    "seoUrl": "/c/sports/baseball",
    "url": "https://www.academy.com/c/sports/baseball"
   },
   {
    "name": "Softball",
    "categoryId": "16166",
    "seoUrl": "/c/sports/softball",
    "url": "https://www.academy.com/c/sports/softball"
   },
   {
    "name": "Basketball",
    "categoryId": "15725",
    "seoUrl": "/c/sports/basketball",
    "url": "https://www.academy.com/c/sports/basketball"
   },
   {
    "name": "Golf",
    "categoryId": "15733",
    "seoUrl": "/c/sports/golf",
    "url": "https://www.academy.com/c/sports/golf",
    "subcategories": [
     {
      "name": "Golf Shoes",
      "categoryId": "15705",
      "seoUrl": "/c/sports/golf/golf-shoes",
      "url": "https://www.academy.com/c/sports/golf/golf-shoes"
     },
     {
      "name": "Golf Clothes",
      "categoryId": "15707",
      "seoUrl": "/c/sports/golf/golf-apparel",
      "url": "https://www.academy.com/c/sports/golf/golf-apparel"
     }
    ]
   },
   {
    "name": "Football",
    "categoryId": "15732",
    "seoUrl": "/c/sports/football",
    "url": "https://www.academy.com/c/sports/football"
   },
   {
    "name": "Soccer",
    "categoryId": "15743",
    "seoUrl": "/c/sports/soccer",
    "url": "https://www.academy.com/c/sports/soccer"
   },
   {
    "name": "Tennis + Racquet Sports",
    "categoryId": "16101",
    "seoUrl": "/c/sports/tennis-racquet-sports",
    "url": "https://www.academy.com/c/sports/tennis-racquet-sports",
    "subcategories": [
     {
      "name": "Tennis",
      "categoryId": "213479",
      "seoUrl": "/c/sports/tennis-racquet-sports/tennis--1",
      "url": "https://www.academy.com/c/sports/tennis-racquet-sports/tennis--1"
     },
     {
      "name": "Pickleball",
      "categoryId": "15939",
      "seoUrl": "/c/sports/tennis-racquet-sports/pickleball",
      "url": "https://www.academy.com/c/sports/tennis-racquet-sports/pickleball"
     }
    ]
   },
   {
    "name": "More Sports",
    "categoryId": "02"
   },
   {
    "name": "Trending",
    "categoryId": "01",
    "subcategories": [
     {
      "name": "adidas World Cup Soccer Balls",
      "categoryId": "3074457345616907368",
      "seoUrl": "/c/brands/adidas/adidas-sports/adidas-soccer/adidas-world-cup-gear/adidas-world-cup-soccer-balls",
      "url": "https://www.academy.com/c/brands/adidas/adidas-sports/adidas-soccer/adidas-world-cup-gear/adidas-world-cup-soccer-balls"
     }
    ]
   }
  ]
 },
 {
  "name": "Home + Recreation",
  "categoryId": "239455",
  "seoUrl": "/c/home-backyard",
  "url": "https://www.academy.com/c/home-backyard",
  "subcategories": [
   {
    "name": "Outdoor Living",
    "categoryId": "15973",
    "seoUrl": "/c/home-backyard/outdoor-living",
    "url": "https://www.academy.com/c/home-backyard/outdoor-living"
   },
   {
    "name": "Grills + Outdoor Cooking",
    "categoryId": "15999",
    "seoUrl": "/c/outdoors/grills--outdoor-cooking",
    "url": "https://www.academy.com/c/outdoors/grills--outdoor-cooking"
   },
   {
    "name": "Tailgating",
    "categoryId": "234431",
    "seoUrl": "/c/outdoors/tailgate",
    "url": "https://www.academy.com/c/outdoors/tailgate"
   },
   {
    "name": "Outdoor Toys",
    "categoryId": "15877",
    "seoUrl": "/c/home-backyard/toys",
    "url": "https://www.academy.com/c/home-backyard/toys",
    "subcategories": [
     {
      "name": "Playsets + Swing Sets",
      "categoryId": "15989",
      "seoUrl": "/c/home-backyard/outdoor-play/play-sets--swing-sets",
      "url": "https://www.academy.com/c/home-backyard/outdoor-play/play-sets--swing-sets"
     }
    ]
   },
   {
    "name": "Game Room",
    "categoryId": "65653",
    "seoUrl": "/c/home-backyard/indoor-fun",
    "url": "https://www.academy.com/c/home-backyard/indoor-fun"
   },
   {
    "name": "Sunglasses",
    "categoryId": "238983",
    "seoUrl": "/c/shops/all-accessories/sunglasses-and-accessories",
    "url": "https://www.academy.com/c/shops/all-accessories/sunglasses-and-accessories"
   },
   {
    "name": "Bikes + Cycling",
    "categoryId": "15613",
    "seoUrl": "/c/outdoors/bike-shop",
    "url": "https://www.academy.com/c/outdoors/bike-shop"
   },
   {
    "name": "Pools",
    "categoryId": "16028",
    "seoUrl": "/c/home-backyard/pools",
    "url": "https://www.academy.com/c/home-backyard/pools"
   },
   {
    "name": "Trending",
    "categoryId": "3074457345617141098"
   }
  ]
 },
 {
  "name": "Health + Fitness",
  "categoryId": "15609",
  "seoUrl": "/c/fitness",
  "url": "https://www.academy.com/c/fitness",
  "subcategories": [
   {
    "name": "Strength Training",
    "categoryId": "15640",
    "seoUrl": "/c/fitness/weight--strength-training",
    "url": "https://www.academy.com/c/fitness/weight--strength-training"
   },
   {
    "name": "Cardio Equipment",
    "categoryId": "15610",
    "seoUrl": "/c/fitness/cardio-equipment--machines",
    "url": "https://www.academy.com/c/fitness/cardio-equipment--machines"
   },
   {
    "name": "Running Essentials",
    "categoryId": "3074457345616921599",
    "seoUrl": "/c/shops/for-the-runner",
    "url": "https://www.academy.com/c/shops/for-the-runner"
   },
   {
    "name": "Yoga",
    "categoryId": "239059",
    "seoUrl": "/c/fitness/yoga",
    "url": "https://www.academy.com/c/fitness/yoga"
   },
   {
    "name": "Fitness Accessories",
    "categoryId": "15638",
    "seoUrl": "/c/fitness/toning",
    "url": "https://www.academy.com/c/fitness/toning"
   },
   {
    "name": "Cross Training Equipment",
    "categoryId": "15577",
    "seoUrl": "/c/fitness/crossfit-training-equipment",
    "url": "https://www.academy.com/c/fitness/crossfit-training-equipment"
   },
   {
    "name": "Wellness and Recovery",
    "categoryId": "15578",
    "seoUrl": "/c/fitness/sports-medicine",
    "url": "https://www.academy.com/c/fitness/sports-medicine"
   },
   {
    "name": "Performance + Metabolic Supplements",
    "categoryId": "3074457345617186098",
    "seoUrl": "/c/fitness/nutrition--supplements",
    "url": "https://www.academy.com/c/fitness/nutrition--supplements"
   },
   {
    "name": "Trending",
    "categoryId": "15576"
   }
  ]
 },
 {
  "name": "Fan Shop",
  "categoryId": "15415",
  "seoUrl": "/c/fan-shop",
  "url": "https://www.academy.com/c/fan-shop",
  "subcategories": [
   {
    "name": "MLB",
    "categoryId": "15403",
    "seoUrl": "/c/fan-shop/mlb",
    "url": "https://www.academy.com/c/fan-shop/mlb"
   },
   {
    "name": "NCAA",
    "categoryId": "15432",
    "seoUrl": "/c/fan-shop/ncaa",
    "url": "https://www.academy.com/c/fan-shop/ncaa"
   },
   {
    "name": "Soccer",
    "categoryId": "3074457345616941634",
    "seoUrl": "/c/fan-shop/soccer-shop",
    "url": "https://www.academy.com/c/fan-shop/soccer-shop"
   },
   {
    "name": "NBA",
    "categoryId": "15394",
    "seoUrl": "/c/fan-shop/nba",
    "url": "https://www.academy.com/c/fan-shop/nba"
   },
   {
    "name": "NHL",
    "categoryId": "15466",
    "seoUrl": "/c/fan-shop/nhl",
    "url": "https://www.academy.com/c/fan-shop/nhl"
   },
   {
    "name": "NFL",
    "categoryId": "15424",
    "seoUrl": "/c/fan-shop/nfl",
    "url": "https://www.academy.com/c/fan-shop/nfl"
   },
   {
    "name": "Fan Shop Brands",
    "categoryId": "3074457345617237098",
    "seoUrl": "/c/fan-shop/fan-shop-brands",
    "url": "https://www.academy.com/c/fan-shop/fan-shop-brands"
   },
   {
    "name": "Collections",
    "categoryId": "1234598238743"
   },
   {
    "name": "Tailgating",
    "categoryId": "3074457345616962616",
    "seoUrl": "/c/fan-shop/tailgate-for-the-fan",
    "url": "https://www.academy.com/c/fan-shop/tailgate-for-the-fan"
   }
  ]
 }
]
"""
)
