"""Sally Beauty complete crawlable storefront category inventory.

Captured 2026-10-15 from the server-rendered ``Find it by category`` /
department mega-navigation on the US homepage (https://www.sallybeauty.com/).
Every URL below was fetched through the configured proxy and confirmed to render
an SFCC product grid (a ``data-pid`` product tile), so each is a runnable crawl
target. The storefront's brand-index flyouts, ``explore-*`` editorial links
(how-to / ``*-101`` guides), and other content-only destinations are dropped
because this spider requires an SFCC product grid.

Grouped ``{department: {leaf: {name, department, url}}}`` mapping as required by
the base listing-spider contract. Leaf keys are the full path slug
(``<department>-...-<slug>``), so the bare leaf name used as the Airflow task id
and GCS output path stays globally unique across departments (see
listing_dag_factory). ``-a category=<department-slug>`` still expands to every
leaf in that department through the base-class parent-selector support.
"""

SALLYBEAUTY_CATEGORIES = {
    "Hair Color": {
        "hair-color": {
            "name": "Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/",
        },
        "hair-color-other-products-and-applications": {
            "name": "Other Products and Applications",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/",
        },
        "hair-color-other-products-and-applications-bleach-and-lightener": {
            "name": "Bleach & Lightener",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/bleach-and-lightener/",
        },
        "hair-color-other-products-and-applications-bond-repair": {
            "name": "Bond Repair",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/bond-repair/",
        },
        "hair-color-other-products-and-applications-developer": {
            "name": "Developer",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/developer/",
        },
        "hair-color-other-products-and-applications-fillers-and-additives": {
            "name": "Fillers & Additives",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/fillers-and-additives/",
        },
        "hair-color-other-products-and-applications-gloves": {
            "name": "Gloves",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/gloves/",
        },
        "hair-color-other-products-and-applications-hair-color-accessories": {
            "name": "Hair Color Accessories",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/hair-color-accessories/",
        },
        "hair-color-other-products-and-applications-hair-color-removers-and-correctors": {
            "name": "Hair Color Removers & Correctors",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/hair-color-removers-and-correctors/",
        },
        "hair-color-other-products-and-applications-mixing-tools": {
            "name": "Mixing Tools",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/mixing-tools/",
        },
        "hair-color-other-products-and-applications-perms-and-straighteners": {
            "name": "Perms & Straighteners",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/perms-and-straighteners/",
        },
        "hair-color-other-products-and-applications-toner": {
            "name": "Toner",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/other-products-and-applications/toner/",
        },
        "hair-color-shop-all-hair-color": {
            "name": "Shop All Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-all-hair-color/",
        },
        "hair-color-shop-by-color": {
            "name": "Shop by Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/",
        },
        "hair-color-shop-by-color-black-hair-color": {
            "name": "Black Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/black-hair-color/",
        },
        "hair-color-shop-by-color-blonde-hair-color": {
            "name": "Blonde Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/blonde-hair-color/",
        },
        "hair-color-shop-by-color-brunette-hair-color": {
            "name": "Brunette Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/brunette-hair-color/",
        },
        "hair-color-shop-by-color-red-hair-color": {
            "name": "Red Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/red-hair-color/",
        },
        "hair-color-shop-by-color-silver-and-gray-hair-color": {
            "name": "Silver & Gray Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/silver-and-gray-hair-color/",
        },
        "hair-color-shop-by-color-vibrant-and-bright-hair-color": {
            "name": "Vibrant and Bright Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-color/vibrant-and-bright-hair-color/",
        },
        "hair-color-shop-by-type": {
            "name": "Shop by Type",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/",
        },
        "hair-color-shop-by-type-demi-permanent-hair-color": {
            "name": "Demi-Permanent Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/demi-permanent-hair-color/",
        },
        "hair-color-shop-by-type-gloss-hair-color": {
            "name": "Gloss Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/gloss-hair-color/",
        },
        "hair-color-shop-by-type-hair-color-for-natural-hair": {
            "name": "Hair Color for Natural Hair",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/hair-color-for-natural-hair/",
        },
        "hair-color-shop-by-type-hair-color-kits": {
            "name": "Hair Color Kits",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/hair-color-kits/",
        },
        "hair-color-shop-by-type-mens-hair-color": {
            "name": "Men's Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/mens-hair-color/",
        },
        "hair-color-shop-by-type-permanent-hair-color": {
            "name": "Permanent Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/permanent-hair-color/",
        },
        "hair-color-shop-by-type-root-touch-up": {
            "name": "Root Touch-Up",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/root-touch-up/",
        },
        "hair-color-shop-by-type-semi-permanent-hair-color": {
            "name": "Semi-Permanent Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/semi-permanent-hair-color/",
        },
        "hair-color-shop-by-type-temporary-hair-color": {
            "name": "Temporary Hair Color",
            "department": "Hair Color",
            "url": "https://www.sallybeauty.com/hair-color/shop-by-type/temporary-hair-color/",
        },
    },
    "Hair Care": {
        "hair-care": {
            "name": "Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/",
        },
        "hair-care-hair-care-accessories-and-styling-products": {
            "name": "Hair Care Accessories & Styling Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/hair-care-accessories-and-styling-products/",
        },
        "hair-care-hair-care-accessories-and-styling-products-hair-accessories": {
            "name": "Hair Accessories",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/hair-care-accessories-and-styling-products/hair-accessories/",
        },
        "hair-care-hair-care-accessories-and-styling-products-hair-extensions": {
            "name": "Hair Extensions",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/hair-care-accessories-and-styling-products/hair-extensions/",
        },
        "hair-care-hair-care-accessories-and-styling-products-perms-and-straighteners": {
            "name": "Perms & Straighteners",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/hair-care-accessories-and-styling-products/perms-and-straighteners/",
        },
        "hair-care-hair-care-accessories-and-styling-products-shears-and-hair-shapers": {
            "name": "Shears & Hair Shapers",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/hair-care-accessories-and-styling-products/shears-and-hair-shapers/",
        },
        "hair-care-other-products-and-accessories-mens-hair-tools-and-accessories": {
            "name": "Men\u2019s Hair Tools & Grooming Accessories",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/other-products-and-accessories/mens-hair-tools-and-accessories/",
        },
        "hair-care-shop-all-hair-care-products": {
            "name": "Shop All Hair Care Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-all-hair-care-products/",
        },
        "hair-care-shop-by-product": {
            "name": "Shop by Product",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/",
        },
        "hair-care-shop-by-product-conditioner": {
            "name": "Conditioner",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/conditioner/",
        },
        "hair-care-shop-by-product-hair-sprays": {
            "name": "Hair Sprays",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/hair-sprays/",
        },
        "hair-care-shop-by-product-hair-styling-products": {
            "name": "Hair Styling Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/hair-styling-products/",
        },
        "hair-care-shop-by-product-hair-treatments": {
            "name": "Hair Treatments",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/hair-treatments/",
        },
        "hair-care-shop-by-product-kids-hair-care-products": {
            "name": "Kids Hair Care Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/kids-hair-care-products/",
        },
        "hair-care-shop-by-product-mens-hair": {
            "name": "Men's Hair",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/mens-hair/",
        },
        "hair-care-shop-by-product-shampoo": {
            "name": "Shampoo",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/shampoo/",
        },
        "hair-care-shop-by-product-shop-all-hair-care-products": {
            "name": "Shop All Hair Care Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/shop-all-hair-care-products/",
        },
        "hair-care-shop-by-product-travel-size-hair-care-products": {
            "name": "Travel Size Hair Care Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-product/travel-size-hair-care-products/",
        },
        "hair-care-shop-by-solution": {
            "name": "Shop by Solution",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/",
        },
        "hair-care-shop-by-solution-anti-frizz-hair-care": {
            "name": "Anti-Frizz Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/anti-frizz-hair-care/",
        },
        "hair-care-shop-by-solution-blonde-hair-care": {
            "name": "Blonde Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/blonde-hair-care/",
        },
        "hair-care-shop-by-solution-bond-repair": {
            "name": "Bond Repair",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/bond-repair/",
        },
        "hair-care-shop-by-solution-brunette-hair-care": {
            "name": "Brunette Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/brunette-hair-care/",
        },
        "hair-care-shop-by-solution-clarifying-hair-products": {
            "name": "Clarifying Hair Products",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/clarifying-hair-products/",
        },
        "hair-care-shop-by-solution-color-protection": {
            "name": "Color Protection",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/color-protection/",
        },
        "hair-care-shop-by-solution-hair-repair": {
            "name": "Hair Repair",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/hair-repair/",
        },
        "hair-care-shop-by-solution-hair-thinning-and-hair-loss-solutions": {
            "name": "Hair Thinning & Hair Loss Solutions",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/hair-thinning-and-hair-loss-solutions/",
        },
        "hair-care-shop-by-solution-heat-protection": {
            "name": "Heat Protection",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/heat-protection/",
        },
        "hair-care-shop-by-solution-moisturizing-hair-care": {
            "name": "Moisturizing Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/moisturizing-hair-care/",
        },
        "hair-care-shop-by-solution-scalp-care": {
            "name": "Scalp Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/scalp-care/",
        },
        "hair-care-shop-by-solution-shop-all-hair-care-solutions": {
            "name": "Shop All Hair Care Solutions",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/shop-by-solution/shop-all-hair-care-solutions/",
        },
        "hair-care-textured-and-curly-hair-care": {
            "name": "Textured and Curly Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/",
        },
        "hair-care-textured-and-curly-hair-care-coily-hair": {
            "name": "Coily Hair",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/coily-hair/",
        },
        "hair-care-textured-and-curly-hair-care-conditioner": {
            "name": "Conditioner",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/conditioner/",
        },
        "hair-care-textured-and-curly-hair-care-curly-hair": {
            "name": "Curly Hair",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/curly-hair/",
        },
        "hair-care-textured-and-curly-hair-care-gels-and-edge-controls": {
            "name": "Gels & Edge Controls",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/gels-and-edge-controls/",
        },
        "hair-care-textured-and-curly-hair-care-growth-aids-and-hair-oils": {
            "name": "Growth Aids & Hair Oils",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/growth-aids-and-hair-oils/",
        },
        "hair-care-textured-and-curly-hair-care-leave-in-conditioners": {
            "name": "Leave-in Conditioners",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/leave-in-conditioners/",
        },
        "hair-care-textured-and-curly-hair-care-scalp-care": {
            "name": "Scalp Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/scalp-care/",
        },
        "hair-care-textured-and-curly-hair-care-shampoo": {
            "name": "Shampoo",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/shampoo/",
        },
        "hair-care-textured-and-curly-hair-care-shop-all-textured-and-curly-hair-care": {
            "name": "Shop All Textured and Curly Hair Care",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/shop-all-textured-and-curly-hair-care/",
        },
        "hair-care-textured-and-curly-hair-care-wavy-hair": {
            "name": "Wavy Hair",
            "department": "Hair Care",
            "url": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/wavy-hair/",
        },
    },
    "Textured & Curly Hair Care": {
        "textured-and-curly-hair-care": {
            "name": "Textured and Curly Hair Care",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/",
        },
        "textured-and-curly-hair-care-coily-hair": {
            "name": "Coily Hair",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/coily-hair/",
        },
        "textured-and-curly-hair-care-conditioner": {
            "name": "Conditioner",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/conditioner/",
        },
        "textured-and-curly-hair-care-curly-hair": {
            "name": "Curly Hair",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/curly-hair/",
        },
        "textured-and-curly-hair-care-gels-and-edge-controls": {
            "name": "Gels & Edge Controls",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/gels-and-edge-controls/",
        },
        "textured-and-curly-hair-care-growth-aids-and-hair-oils": {
            "name": "Growth Aids & Hair Oils",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/growth-aids-and-hair-oils/",
        },
        "textured-and-curly-hair-care-leave-in-conditioners": {
            "name": "Leave-in Conditioners",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/leave-in-conditioners/",
        },
        "textured-and-curly-hair-care-scalp-care": {
            "name": "Scalp Care",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/scalp-care/",
        },
        "textured-and-curly-hair-care-shampoo": {
            "name": "Shampoo",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/shampoo/",
        },
        "textured-and-curly-hair-care-shop-all-textured-and-curly-hair-care": {
            "name": "Shop all Textured and Curly Hair Care",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/shop-all-textured-and-curly-hair-care/",
        },
        "textured-and-curly-hair-care-wavy-hair": {
            "name": "Wavy Hair",
            "department": "Textured & Curly Hair Care",
            "url": "https://www.sallybeauty.com/textured-and-curly-hair-care/wavy-hair/",
        },
    },
    "Hair Extensions": {
        "hair-extensions": {
            "name": "Hair Extensions",
            "department": "Hair Extensions",
            "url": "https://www.sallybeauty.com/hair-extensions/",
        },
    },
    "Tools & Brushes": {
        "tools-and-brushes": {
            "name": "Tools & Brushes",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/",
        },
        "tools-and-brushes-brushes-and-combs": {
            "name": "Brushes & Combs",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/brushes-and-combs/",
        },
        "tools-and-brushes-brushes-and-combs-combs": {
            "name": "Combs",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/brushes-and-combs/combs/",
        },
        "tools-and-brushes-brushes-and-combs-hair-brushes": {
            "name": "Hair Brushes",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/brushes-and-combs/hair-brushes/",
        },
        "tools-and-brushes-brushes-and-combs-hair-picks": {
            "name": "Hair Picks",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/brushes-and-combs/hair-picks/",
        },
        "tools-and-brushes-curling-irons-and-wands": {
            "name": "Shop All Curling Irons & Wands",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/curling-irons-and-wands/",
        },
        "tools-and-brushes-curling-irons-and-wands-crimpers-and-wavers": {
            "name": "Crimpers & Wavers",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/curling-irons-and-wands/crimpers-and-wavers/",
        },
        "tools-and-brushes-curling-irons-and-wands-curling-irons": {
            "name": "Curling Irons",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/curling-irons-and-wands/curling-irons/",
        },
        "tools-and-brushes-curling-irons-and-wands-hair-rollers": {
            "name": "Hair Rollers",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/curling-irons-and-wands/hair-rollers/",
        },
        "tools-and-brushes-flat-irons-and-hair-straighteners": {
            "name": "Flat Irons & Hair Straighteners",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/flat-irons-and-hair-straighteners/",
        },
        "tools-and-brushes-flat-irons-and-hair-straighteners-flat-irons": {
            "name": "Flat Irons",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/flat-irons-and-hair-straighteners/flat-irons/",
        },
        "tools-and-brushes-flat-irons-and-hair-straighteners-straightening-brush": {
            "name": "Straightening Brush",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/flat-irons-and-hair-straighteners/straightening-brush/",
        },
        "tools-and-brushes-hair-cutting-tools": {
            "name": "Hair Cutting Tools",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-cutting-tools/",
        },
        "tools-and-brushes-hair-cutting-tools-clipper-comb-attachments": {
            "name": "Clipper Comb Attachments",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-cutting-tools/clipper-comb-attachments/",
        },
        "tools-and-brushes-hair-cutting-tools-clippers-and-trimmers": {
            "name": "Clippers & Trimmers",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-cutting-tools/clippers-and-trimmers/",
        },
        "tools-and-brushes-hair-cutting-tools-combos-and-sets": {
            "name": "Combos & Sets",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-cutting-tools/combos-and-sets/",
        },
        "tools-and-brushes-hair-cutting-tools-shears": {
            "name": "Shears",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-cutting-tools/shears/",
        },
        "tools-and-brushes-hair-dryers-diffusers-and-attachments-classic-dryer": {
            "name": "Classic Blow Dryers",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-dryers-diffusers-and-attachments/classic-dryer/",
        },
        "tools-and-brushes-hair-dryers-diffusers-and-attachments-multi-use-tools": {
            "name": "Multi-Use Tools",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-dryers-diffusers-and-attachments/multi-use-tools/",
        },
        "tools-and-brushes-hair-dryers": {
            "name": "Hair Dryers, Diffusers, & Attachments",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-dryers/",
        },
        "tools-and-brushes-hair-dryers-bonnet-dryer": {
            "name": "Bonnet Hair Dryers",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-dryers/bonnet-dryer/",
        },
        "tools-and-brushes-hair-dryers-hot-air-brush": {
            "name": "Hot Air Blowout Brushes",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/hair-dryers/hot-air-brush/",
        },
        "tools-and-brushes-shop-all-curling-irons-and-wands-curling-wands": {
            "name": "Curling Wands",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/shop-all-curling-irons-and-wands/curling-wands/",
        },
        "tools-and-brushes-shop-all-curling-irons-and-wands-hot-curl-set": {
            "name": "Hot Curl Set",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/shop-all-curling-irons-and-wands/hot-curl-set/",
        },
        "tools-and-brushes-shop-all-hair-styling-tools-and-brushes": {
            "name": "Shop All Hair Styling Tools & Brushes",
            "department": "Tools & Brushes",
            "url": "https://www.sallybeauty.com/tools-and-brushes/shop-all-hair-styling-tools-and-brushes/",
        },
    },
    "Nails": {
        "nails": {
            "name": "Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/",
        },
        "nails-acrylic-nails": {
            "name": "Acrylic Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/",
        },
        "nails-acrylic-nails-acrylic-nail-powder-and-monomer-liquids": {
            "name": "Acrylic Nail Powder & Monomer Liquids",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/acrylic-nail-powder-and-monomer-liquids/",
        },
        "nails-acrylic-nails-drills-acrylic-brushes-and-accessories": {
            "name": "Drills, Acrylic Brushes & Accessories",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/drills-acrylic-brushes-and-accessories/",
        },
        "nails-acrylic-nails-nail-extension-kits": {
            "name": "Nail Extension Kits",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/nail-extension-kits/",
        },
        "nails-acrylic-nails-nail-glue": {
            "name": "Nail Glue",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/nail-glue/",
        },
        "nails-acrylic-nails-nail-tips-and-forms": {
            "name": "Nail Tips & Forms",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/nail-tips-and-forms/",
        },
        "nails-acrylic-nails-polygel-hard-gel-and-builder-gel-nails": {
            "name": "PolyGel, Hard Gel & Builder Gel Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/polygel-hard-gel-and-builder-gel-nails/",
        },
        "nails-acrylic-nails-shop-all-nail-extensions": {
            "name": "Shop All Nail Extensions",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/acrylic-nails/shop-all-nail-extensions/",
        },
        "nails-nail-care-and-accessories": {
            "name": "Nail Care & Accessories",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/",
        },
        "nails-nail-care-and-accessories-cuticle-tools-and-treatments": {
            "name": "Cuticle Tools & Treatments",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/cuticle-tools-and-treatments/",
        },
        "nails-nail-care-and-accessories-nail-art-and-stickers": {
            "name": "Nail Art & Stickers",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/nail-art-and-stickers/",
        },
        "nails-nail-care-and-accessories-nail-files-and-buffers": {
            "name": "Nail Files & Buffers",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/nail-files-and-buffers/",
        },
        "nails-nail-care-and-accessories-nail-treatments-and-strengtheners": {
            "name": "Nail Treatments & Strengtheners",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/nail-treatments-and-strengtheners/",
        },
        "nails-nail-care-and-accessories-pedicure-and-manicure-tools": {
            "name": "Pedicure & Manicure Tools",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/pedicure-and-manicure-tools/",
        },
        "nails-nail-care-and-accessories-shop-all-nail-care-and-accessories": {
            "name": "Shop All Nail Care & Accessories",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/shop-all-nail-care-and-accessories/",
        },
        "nails-nail-care-and-accessories-uv-and-led-nail-lights": {
            "name": "UV & LED Nail Lights",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-care-and-accessories/uv-and-led-nail-lights/",
        },
        "nails-nail-color": {
            "name": "Nail Color",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/",
        },
        "nails-nail-color-dip-powder-nails": {
            "name": "Dip Powder Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/dip-powder-nails/",
        },
        "nails-nail-color-gel-nail-polish": {
            "name": "Gel Nail Polish",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/gel-nail-polish/",
        },
        "nails-nail-color-nail-polish-and-lacquer": {
            "name": "Nail Polish & Lacquer",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/nail-polish-and-lacquer/",
        },
        "nails-nail-color-nail-polish-remover-and-thinner": {
            "name": "Nail Polish Remover & Thinner",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/nail-polish-remover-and-thinner/",
        },
        "nails-nail-color-shop-all-nail-color": {
            "name": "Shop All Nail Color",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/shop-all-nail-color/",
        },
        "nails-nail-color-shop-by-color": {
            "name": "Shop by Color",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/shop-by-color/",
        },
        "nails-nail-color-top-and-base-coat-nail-polish": {
            "name": "Top & Base Coat Nail Polish",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/nail-color/top-and-base-coat-nail-polish/",
        },
        "nails-press-on-nails": {
            "name": "Press-On Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/",
        },
        "nails-press-on-nails-french-tip-press-on-nails": {
            "name": "French Tip Press-On Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/french-tip-press-on-nails/",
        },
        "nails-press-on-nails-semi-cured-gel-nail-strips": {
            "name": "Semi-Cured Gel Nail Strips",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/semi-cured-gel-nail-strips/",
        },
        "nails-press-on-nails-shop-all-press-on-nails": {
            "name": "Shop All Press-On Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/shop-all-press-on-nails/",
        },
        "nails-press-on-nails-shop-by-color": {
            "name": "Shop By Color",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/shop-by-color/",
        },
        "nails-press-on-nails-shop-by-shape": {
            "name": "Shop By Shape",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/shop-by-shape/",
        },
        "nails-press-on-nails-toe-press-on-nails": {
            "name": "Toe Press-On Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/press-on-nails/toe-press-on-nails/",
        },
        "nails-shop-all-nails": {
            "name": "Shop All Nails",
            "department": "Nails",
            "url": "https://www.sallybeauty.com/nails/shop-all-nails/",
        },
    },
    "Cosmetics & Skin Care": {
        "cosmetics-and-skin-care": {
            "name": "Cosmetics & Skin Care",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/",
        },
        "cosmetics-and-skin-care-fragrances": {
            "name": "Fragrances",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/fragrances/",
        },
        "cosmetics-and-skin-care-makeup": {
            "name": "Makeup",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/",
        },
        "cosmetics-and-skin-care-makeup-eye-makeup": {
            "name": "Eye Makeup",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/eye-makeup/",
        },
        "cosmetics-and-skin-care-makeup-eyelashes": {
            "name": "Eyelashes",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/eyelashes/",
        },
        "cosmetics-and-skin-care-makeup-face": {
            "name": "Face",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/face/",
        },
        "cosmetics-and-skin-care-makeup-lips": {
            "name": "Lips",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/lips/",
        },
        "cosmetics-and-skin-care-makeup-organizers-and-travel": {
            "name": "Organizers & Travel",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/organizers-and-travel/",
        },
        "cosmetics-and-skin-care-makeup-shop-all-makeup": {
            "name": "Shop All Makeup",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/shop-all-makeup/",
        },
        "cosmetics-and-skin-care-makeup-tools-and-brushes": {
            "name": "Tools & Brushes",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/makeup/tools-and-brushes/",
        },
        "cosmetics-and-skin-care-mens-grooming": {
            "name": "Men's Grooming",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/mens-grooming/",
        },
        "cosmetics-and-skin-care-mens-grooming-mens-hair-care": {
            "name": "Men's Hair Care",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/mens-grooming/mens-hair-care/",
        },
        "cosmetics-and-skin-care-mens-grooming-mens-hair-tools-and-accessories": {
            "name": "Men's Hair Tools & Accessories",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/mens-grooming/mens-hair-tools-and-accessories/",
        },
        "cosmetics-and-skin-care-mens-grooming-pomades-and-oils": {
            "name": "Pomades & Oils",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/mens-grooming/pomades-and-oils/",
        },
        "cosmetics-and-skin-care-mens-grooming-shaving": {
            "name": "Shaving",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/mens-grooming/shaving/",
        },
        "cosmetics-and-skin-care-shop-all-cosmetics-and-skin-care": {
            "name": "Shop All Cosmetics & Skin Care",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/shop-all-cosmetics-and-skin-care/",
        },
        "cosmetics-and-skin-care-skin-care": {
            "name": "Skin Care",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/",
        },
        "cosmetics-and-skin-care-skin-care-body-care": {
            "name": "Body Care",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/body-care/",
        },
        "cosmetics-and-skin-care-skin-care-cleansers-and-toners": {
            "name": "Cleansers & Toners",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/cleansers-and-toners/",
        },
        "cosmetics-and-skin-care-skin-care-exfoliators": {
            "name": "Exfoliators",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/exfoliators/",
        },
        "cosmetics-and-skin-care-skin-care-face-masks": {
            "name": "Face Masks",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/face-masks/",
        },
        "cosmetics-and-skin-care-skin-care-makeup-remover": {
            "name": "Makeup Remover",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/makeup-remover/",
        },
        "cosmetics-and-skin-care-skin-care-moisturizers": {
            "name": "Moisturizers",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/moisturizers/",
        },
        "cosmetics-and-skin-care-skin-care-piercing-and-jewelry": {
            "name": "Piercing & Jewelry",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/piercing-and-jewelry/",
        },
        "cosmetics-and-skin-care-skin-care-shop-all-skincare": {
            "name": "Shop All Skincare",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/shop-all-skincare/",
        },
        "cosmetics-and-skin-care-skin-care-skincare-accessories-and-tools": {
            "name": "Skincare Accessories & Tools",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/skincare-accessories-and-tools/",
        },
        "cosmetics-and-skin-care-skin-care-tattoos-and-tattoo-care": {
            "name": "Tattoos & Tattoo Care",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/tattoos-and-tattoo-care/",
        },
        "cosmetics-and-skin-care-skin-care-treatments-and-serums": {
            "name": "Treatments & Serums",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/skin-care/treatments-and-serums/",
        },
        "cosmetics-and-skin-care-waxing-and-tanning-1": {
            "name": "Waxing & Tanning",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/waxing-and-tanning-1/",
        },
        "cosmetics-and-skin-care-waxing-and-tanning-self-tanning": {
            "name": "Self Tanning",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/waxing-and-tanning/self-tanning/",
        },
        "cosmetics-and-skin-care-waxing-and-tanning-shop-all-waxing-and-tanning": {
            "name": "Shop All Waxing & Tanning",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/waxing-and-tanning/shop-all-waxing-and-tanning/",
        },
        "cosmetics-and-skin-care-waxing-and-tanning-waxing-and-hair-removal": {
            "name": "Waxing & Hair Removal",
            "department": "Cosmetics & Skin Care",
            "url": "https://www.sallybeauty.com/cosmetics-and-skin-care/waxing-and-tanning/waxing-and-hair-removal/",
        },
    },
    "Fragrances": {
        "fragrances": {
            "name": "Fragrances",
            "department": "Fragrances",
            "url": "https://www.sallybeauty.com/fragrances/",
        },
    },
    "Men's Grooming": {
        "mens-grooming": {
            "name": "Men's Grooming",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/",
        },
        "mens-grooming-beard-and-facial-hair": {
            "name": "Beard & Facial Hair",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/beard-and-facial-hair/",
        },
        "mens-grooming-beard-and-facial-hair-beard-hair-color": {
            "name": "Beard Hair Color",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/beard-and-facial-hair/beard-hair-color/",
        },
        "mens-grooming-beard-and-facial-hair-beard-oils-and-balms": {
            "name": "Beard Oils & Balms",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/beard-and-facial-hair/beard-oils-and-balms/",
        },
        "mens-grooming-beard-and-facial-hair-beard-wash-and-conditioner": {
            "name": "Beard Wash & Conditioner",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/beard-and-facial-hair/beard-wash-and-conditioner/",
        },
        "mens-grooming-mens-hair-care-and-accessories": {
            "name": "Men's Hair Care and Accessories",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/",
        },
        "mens-grooming-mens-hair-care-and-accessories-hair-and-wave-caps": {
            "name": "Hair & Wave Caps",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/hair-and-wave-caps/",
        },
        "mens-grooming-mens-hair-care-and-accessories-mens-combs-and-brushes": {
            "name": "Men's Combs & Brushes",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/mens-combs-and-brushes/",
        },
        "mens-grooming-mens-hair-care-and-accessories-mens-hair-color": {
            "name": "Men's Hair Color",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/mens-hair-color/",
        },
        "mens-grooming-mens-hair-care-and-accessories-mens-hair-styling-products": {
            "name": "Men's Hair Styling Products",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/mens-hair-styling-products/",
        },
        "mens-grooming-mens-hair-care-and-accessories-mens-hair-thinning-and-hair-loss": {
            "name": "Men's Hair Thinning & Hair Loss",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/mens-hair-thinning-and-hair-loss/",
        },
        "mens-grooming-mens-hair-care-and-accessories-shampoo-and-conditioner": {
            "name": "Shampoo & Conditioner",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-hair-care-and-accessories/shampoo-and-conditioner/",
        },
        "mens-grooming-mens-skin-care": {
            "name": "Men's Skin Care",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-skin-care/",
        },
        "mens-grooming-mens-skin-care-aftershave-and-cologne": {
            "name": "Aftershave & Cologne",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-skin-care/aftershave-and-cologne/",
        },
        "mens-grooming-mens-skin-care-mens-lotions-and-powders": {
            "name": "Men's Lotions and Powders",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-skin-care/mens-lotions-and-powders/",
        },
        "mens-grooming-mens-skin-care-mens-soap-and-body-wash": {
            "name": "Men's Soap & Body Wash",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-skin-care/mens-soap-and-body-wash/",
        },
        "mens-grooming-mens-skin-care-shaving-cream-and-gels": {
            "name": "Shaving Cream & Gels",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-skin-care/shaving-cream-and-gels/",
        },
        "mens-grooming-mens-skin-care-tattoo-care": {
            "name": "Tattoo Care",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-skin-care/tattoo-care/",
        },
        "mens-grooming-mens-textured-hair-care": {
            "name": "Men's Textured Hair Care",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/",
        },
        "mens-grooming-mens-textured-hair-care-beard-grooming": {
            "name": "Beard Grooming",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/beard-grooming/",
        },
        "mens-grooming-mens-textured-hair-care-bump-and-ingrown-hair-prevention": {
            "name": "Bump & Ingrown Hair Prevention",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/bump-and-ingrown-hair-prevention/",
        },
        "mens-grooming-mens-textured-hair-care-curl-enhancers-and-styling-products": {
            "name": "Curl Enhancers & Styling Products",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/curl-enhancers-and-styling-products/",
        },
        "mens-grooming-mens-textured-hair-care-hair-loc-maintenance": {
            "name": "Hair Loc Maintenance",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/hair-loc-maintenance/",
        },
        "mens-grooming-mens-textured-hair-care-wave-brushes-and-hair-picks": {
            "name": "Wave Brushes & Hair Picks",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/wave-brushes-and-hair-picks/",
        },
        "mens-grooming-mens-textured-hair-care-wave-caps-and-durags": {
            "name": "Wave Caps & Durags",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/mens-textured-hair-care/wave-caps-and-durags/",
        },
        "mens-grooming-shaving-and-razor-care": {
            "name": "Shaving & Razor Care",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/shaving-and-razor-care/",
        },
        "mens-grooming-shaving-and-razor-care-bump-and-ingrown-hair-prevention": {
            "name": "Bump & Ingrown Hair Prevention",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/shaving-and-razor-care/bump-and-ingrown-hair-prevention/",
        },
        "mens-grooming-shaving-and-razor-care-electric-shavers": {
            "name": "Electric Shavers",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/shaving-and-razor-care/electric-shavers/",
        },
        "mens-grooming-shaving-and-razor-care-razors-and-razor-blades": {
            "name": "Razors & Razor Blades",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/shaving-and-razor-care/razors-and-razor-blades/",
        },
        "mens-grooming-shaving-and-razor-care-shaving-cream-and-gels": {
            "name": "Shaving Cream & Gels",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/shaving-and-razor-care/shaving-cream-and-gels/",
        },
        "mens-grooming-shop-all-mens-grooming": {
            "name": "Shop All Men's Grooming",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/shop-all-mens-grooming/",
        },
        "mens-grooming-tools-and-barber-essentials": {
            "name": "Tools & Barber Essentials",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/",
        },
        "mens-grooming-tools-and-barber-essentials-barber-sanitation-and-disinfecting": {
            "name": "Barber Sanitation & Disinfecting",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/barber-sanitation-and-disinfecting/",
        },
        "mens-grooming-tools-and-barber-essentials-clipper-comb-attachments": {
            "name": "Clipper Comb Attachments",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/clipper-comb-attachments/",
        },
        "mens-grooming-tools-and-barber-essentials-clippers-and-trimmers": {
            "name": "Clippers & Trimmers",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/clippers-and-trimmers/",
        },
        "mens-grooming-tools-and-barber-essentials-combos-and-sets": {
            "name": "Combos & Sets",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/combos-and-sets/",
        },
        "mens-grooming-tools-and-barber-essentials-electric-shavers": {
            "name": "Electric Shavers",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/electric-shavers/",
        },
        "mens-grooming-tools-and-barber-essentials-neck-dusters-and-neck-strips": {
            "name": "Neck Dusters & Neck Strips",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/neck-dusters-and-neck-strips/",
        },
        "mens-grooming-tools-and-barber-essentials-razors-and-razor-blades": {
            "name": "Razors & Razor Blades",
            "department": "Men's Grooming",
            "url": "https://www.sallybeauty.com/mens-grooming/tools-and-barber-essentials/razors-and-razor-blades/",
        },
    },
    "Salon Supplies": {
        "salon-supplies": {
            "name": "Salon Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/",
        },
        "salon-supplies-hair-coloring-tools": {
            "name": "Hair Coloring Tools",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/hair-coloring-tools/",
        },
        "salon-supplies-hair-coloring-tools-capes-smocks-and-aprons": {
            "name": "Capes, Smocks & Aprons",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/hair-coloring-tools/capes-smocks-and-aprons/",
        },
        "salon-supplies-hair-coloring-tools-foils": {
            "name": "Foils",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/hair-coloring-tools/foils/",
        },
        "salon-supplies-hair-coloring-tools-perm-supplies": {
            "name": "Perm Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/hair-coloring-tools/perm-supplies/",
        },
        "salon-supplies-hair-coloring-tools-tint-brushes-bowls-and-applicators": {
            "name": "Tint Brushes, Bowls & Applicators",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/hair-coloring-tools/tint-brushes-bowls-and-applicators/",
        },
        "salon-supplies-other-professional-supplies": {
            "name": "Other Professional Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/other-professional-supplies/",
        },
        "salon-supplies-other-professional-supplies-barber-supplies": {
            "name": "Barber Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/other-professional-supplies/barber-supplies/",
        },
        "salon-supplies-other-professional-supplies-beauty-student-supplies": {
            "name": "Beauty Student Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/other-professional-supplies/beauty-student-supplies/",
        },
        "salon-supplies-other-professional-supplies-nail-salon-supplies": {
            "name": "Nail Salon Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/other-professional-supplies/nail-salon-supplies/",
        },
        "salon-supplies-salon-equipment-and-furniture": {
            "name": "Salon Equipment & Furniture",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/",
        },
        "salon-supplies-salon-equipment-and-furniture-equipment-accessories-and-parts": {
            "name": "Equipment Accessories & Parts",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/equipment-accessories-and-parts/",
        },
        "salon-supplies-salon-equipment-and-furniture-furniture-cabinetry-and-station-area": {
            "name": "Furniture, Cabinetry & Station Area",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/furniture-cabinetry-and-station-area/",
        },
        "salon-supplies-salon-equipment-and-furniture-manicure-and-pedicure-equipment": {
            "name": "Manicure & Pedicure Equipment",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/manicure-and-pedicure-equipment/",
        },
        "salon-supplies-salon-equipment-and-furniture-massage-equipment": {
            "name": "Massage Equipment",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/massage-equipment/",
        },
        "salon-supplies-salon-equipment-and-furniture-salon-chairs-and-stools": {
            "name": "Salon Chairs & Stools",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/salon-chairs-and-stools/",
        },
        "salon-supplies-salon-equipment-and-furniture-shampoo-area": {
            "name": "Shampoo Area",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-equipment-and-furniture/shampoo-area/",
        },
        "salon-supplies-salon-essentials": {
            "name": "Salon Essentials",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/",
        },
        "salon-supplies-salon-essentials-bobby-pins-and-clips": {
            "name": "Bobby Pins & Clips",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/bobby-pins-and-clips/",
        },
        "salon-supplies-salon-essentials-bottles-and-sprayers": {
            "name": "Bottles & Sprayers",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/bottles-and-sprayers/",
        },
        "salon-supplies-salon-essentials-disinfectants-and-cleaners": {
            "name": "Disinfectants & Cleaners",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/disinfectants-and-cleaners/",
        },
        "salon-supplies-salon-essentials-gloves": {
            "name": "Gloves",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/gloves/",
        },
        "salon-supplies-salon-essentials-personal-protective-equipment": {
            "name": "Personal Protective Equipment",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/personal-protective-equipment/",
        },
        "salon-supplies-salon-essentials-professional-hair-care": {
            "name": "Professional Hair Care",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/professional-hair-care/",
        },
        "salon-supplies-salon-essentials-towels": {
            "name": "Towels",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/salon-essentials/towels/",
        },
        "salon-supplies-shop-all-salon-supplies": {
            "name": "Shop All Salon Supplies",
            "department": "Salon Supplies",
            "url": "https://www.sallybeauty.com/salon-supplies/shop-all-salon-supplies/",
        },
    },
    "Deals": {
        "deals": {
            "name": "Deals",
            "department": "Deals",
            "url": "https://www.sallybeauty.com/deals/",
        },
    },
    "Perm Rods": {
        "perm-rods": {
            "name": "Perm Rods",
            "department": "Perm Rods",
            "url": "https://www.sallybeauty.com/perm-rods/",
        },
    },}
