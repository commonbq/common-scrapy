"""Saks Fifth Avenue storefront category inventory, from the live main navigation.

Source: the ``<nav class="navbar ...">`` block serialized into
https://www.saksfifthavenue.com/ on 2026-10-18. Each ``li.nav-item.l1-menu`` is
one department flyout and every ``/c/...`` anchor inside it is a listing route.

Only real product-listing paths are kept. Dropped: query-only refinements
(``?pmid=``, ``?prefn1=``, ``?srule=``, ``?sre=``), editorial and campaign pages
(``/c/content/``, ``/c/custom/``, ``/c/the-edit``), the designer index
(``/designers``), ``visual-nav`` shells, live-stream and lookbook pages, and the
hidden utility ``li`` blocks whose ids are bare numbers.

Grouped ``{department: {leaf: {url, label, subcategory}}}`` mapping as required by
the base listing spider contract. ``leaf`` is the full ``/c``-relative path slug,
so leaves that repeat across departments stay globally unique for the DAG output
paths and the ``-a category=`` selector. Verified 2026-10-18: 429 unique listing
paths, 429 unique leaf slugs, 12 departments. Entries are ordered shallowest
first so each department root PLP leads its group.

``url`` is the query-free canonical PLP; the spider appends ``start``/``sz`` for
pagination. ``label`` is the nav text and ``subcategory`` the path below the
department segment, exported with every row so it can be traced to its nav slot.

Saks sits behind DataDome, so a live crawl can still return a challenge page; the
inventory itself is what this module pins down.
"""

from __future__ import annotations


SAKS_CATEGORY_SECTIONS: dict[str, dict[str, dict[str, str]]] = {
    "Women's Apparel": {
        "women-s-apparel": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel",
            "label": "Clothing",
            "subcategory": "women-s-apparel",
        },
        "women-s-apparel-akris-punto": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/akris-punto",
            "label": "Akris punto",
            "subcategory": "akris-punto",
        },
        "women-s-apparel-alice-olivia": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/alice-olivia",
            "label": "ALICE + OLIVIA",
            "subcategory": "alice-olivia",
        },
        "women-s-apparel-altuzarra": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/altuzarra",
            "label": "Altuzarra",
            "subcategory": "altuzarra",
        },
        "women-s-apparel-burberry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/burberry",
            "label": "Burberry",
            "subcategory": "burberry",
        },
        "women-s-apparel-cinq-c3-a0-sept": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/cinq-%C3%A0-sept",
            "label": "Cinq à Sept",
            "subcategory": "cinq-%C3%A0-sept",
        },
        "women-s-apparel-coats": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/coats",
            "label": "Coats",
            "subcategory": "coats",
        },
        "women-s-apparel-d-c3-b4en": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/d%C3%B4en",
            "label": "DÔEN",
            "subcategory": "d%C3%B4en",
        },
        "women-s-apparel-dresses": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses",
            "label": "Dresses",
            "subcategory": "dresses",
        },
        "women-s-apparel-jackets-blazers": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/jackets-blazers",
            "label": "Jackets & Blazers",
            "subcategory": "jackets-blazers",
        },
        "women-s-apparel-jeans": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/jeans",
            "label": "Jeans",
            "subcategory": "jeans",
        },
        "women-s-apparel-l-agence": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/l-agence",
            "label": "L'AGENCE",
            "subcategory": "l-agence",
        },
        "women-s-apparel-lingerie-shapewear": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/lingerie-shapewear",
            "label": "Lingerie",
            "subcategory": "lingerie-shapewear",
        },
        "women-s-apparel-matching-sets": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/matching-sets",
            "label": "Matching Sets",
            "subcategory": "matching-sets",
        },
        "women-s-apparel-moncler": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/moncler",
            "label": "Moncler",
            "subcategory": "moncler",
        },
        "women-s-apparel-nili-lotan": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/nili-lotan",
            "label": "Nili Lotan",
            "subcategory": "nili-lotan",
        },
        "women-s-apparel-pajamas-robes": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/pajamas-robes",
            "label": "Pajamas & Robes",
            "subcategory": "pajamas-robes",
        },
        "women-s-apparel-pants": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/pants",
            "label": "Pants",
            "subcategory": "pants",
        },
        "women-s-apparel-polo-ralph-lauren": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/polo-ralph-lauren",
            "label": "Polo Ralph Lauren",
            "subcategory": "polo-ralph-lauren",
        },
        "women-s-apparel-ralph-lauren-collection": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/ralph-lauren-collection",
            "label": "Ralph Lauren Collection",
            "subcategory": "ralph-lauren-collection",
        },
        "women-s-apparel-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/sale",
            "label": "Sale",
            "subcategory": "sale",
        },
        "women-s-apparel-skirts": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/skirts",
            "label": "Skirts",
            "subcategory": "skirts",
        },
        "women-s-apparel-sweaters": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/sweaters",
            "label": "Novelty Knits",
            "subcategory": "sweaters",
        },
        "women-s-apparel-swimsuits-beach-cover-ups": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/swimsuits-beach-cover-ups",
            "label": "Swimsuits & Cover-Ups",
            "subcategory": "swimsuits-beach-cover-ups",
        },
        "women-s-apparel-tops": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/tops",
            "label": "Tops",
            "subcategory": "tops",
        },
        "women-s-apparel-toteme": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/toteme",
            "label": "Toteme",
            "subcategory": "toteme",
        },
        "women-s-apparel-veronica-beard": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/veronica-beard",
            "label": "Veronica Beard",
            "subcategory": "veronica-beard",
        },
        "women-s-apparel-zimmermann": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/zimmermann",
            "label": "Zimmermann",
            "subcategory": "zimmermann",
        },
        "women-s-apparel-coats-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/coats/sale",
            "label": "Coats",
            "subcategory": "coats/sale",
        },
        "women-s-apparel-coats-wool-coats": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/coats/wool-coats",
            "label": "Wool Coats",
            "subcategory": "coats/wool-coats",
        },
        "women-s-apparel-dresses-brown": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/brown",
            "label": "Chocolate Brown Dresses",
            "subcategory": "dresses/brown",
        },
        "women-s-apparel-dresses-carolina-herrera": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/carolina-herrera",
            "label": "Carolina Herrera",
            "subcategory": "dresses/carolina-herrera",
        },
        "women-s-apparel-dresses-chiara-boni-la-petite-robe": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/chiara-boni-la-petite-robe",
            "label": "Chiara Boni La Petite Robe",
            "subcategory": "dresses/chiara-boni-la-petite-robe",
        },
        "women-s-apparel-dresses-cocktail": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/cocktail",
            "label": "Cocktail & Party Dresses",
            "subcategory": "dresses/cocktail",
        },
        "women-s-apparel-dresses-day-casual": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/day-casual",
            "label": "Day & Casual",
            "subcategory": "dresses/day-casual",
        },
        "women-s-apparel-dresses-dress-the-population": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/dress-the-population",
            "label": "Dress The Population",
            "subcategory": "dresses/dress-the-population",
        },
        "women-s-apparel-dresses-evening-gowns": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/evening-gowns",
            "label": "Evening Gowns",
            "subcategory": "dresses/evening-gowns",
        },
        "women-s-apparel-dresses-florals-prints": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/florals-prints-",
            "label": "Florals & Prints",
            "subcategory": "dresses/florals-prints-",
        },
        "women-s-apparel-dresses-mac-duggal": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/mac-duggal",
            "label": "Mac Duggal",
            "subcategory": "dresses/mac-duggal",
        },
        "women-s-apparel-dresses-maxi": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/maxi",
            "label": "Maxi",
            "subcategory": "dresses/maxi",
        },
        "women-s-apparel-dresses-midi": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/midi",
            "label": "Midi",
            "subcategory": "dresses/midi",
        },
        "women-s-apparel-dresses-milly": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/milly",
            "label": "Milly",
            "subcategory": "dresses/milly",
        },
        "women-s-apparel-dresses-mini": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/mini",
            "label": "Mini",
            "subcategory": "dresses/mini",
        },
        "women-s-apparel-dresses-mother-of-the-bride": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/mother-of-the-bride",
            "label": "Mother of the Bride",
            "subcategory": "dresses/mother-of-the-bride",
        },
        "women-s-apparel-dresses-oscar-de-la-renta": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/oscar-de-la-renta",
            "label": "Oscar de la Renta",
            "subcategory": "dresses/oscar-de-la-renta",
        },
        "women-s-apparel-dresses-sachin-babi": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/sachin-babi",
            "label": "SACHIN BABI",
            "subcategory": "dresses/sachin-babi",
        },
        "women-s-apparel-dresses-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/sale",
            "label": "Sale",
            "subcategory": "dresses/sale",
        },
        "women-s-apparel-dresses-sequin": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/sequin",
            "label": "Sequin Dresses",
            "subcategory": "dresses/sequin",
        },
        "women-s-apparel-dresses-shoshanna": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/shoshanna",
            "label": "Shoshanna",
            "subcategory": "dresses/shoshanna",
        },
        "women-s-apparel-dresses-silvia-tcherassi": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/silvia-tcherassi",
            "label": "Silvia Tcherassi",
            "subcategory": "dresses/silvia-tcherassi",
        },
        "women-s-apparel-dresses-tadashi-shoji": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/tadashi-shoji",
            "label": "Tadashi Shoji",
            "subcategory": "dresses/tadashi-shoji",
        },
        "women-s-apparel-dresses-teri-jon-by-rickie-freeman": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/teri-jon-by-rickie-freeman",
            "label": "Teri Jon by Rickie Freeman",
            "subcategory": "dresses/teri-jon-by-rickie-freeman",
        },
        "women-s-apparel-dresses-theia": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/theia",
            "label": "Theia",
            "subcategory": "dresses/theia",
        },
        "women-s-apparel-dresses-velvet": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/velvet",
            "label": "Velvet Dresses",
            "subcategory": "dresses/velvet",
        },
        "women-s-apparel-dresses-workwear": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/workwear",
            "label": "Work",
            "subcategory": "dresses/workwear",
        },
        "women-s-apparel-jackets-blazers-leather-jackets": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/jackets-blazers/leather-jackets",
            "label": "Leather & Suede Jackets",
            "subcategory": "jackets-blazers/leather-jackets",
        },
        "women-s-apparel-jackets-blazers-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/jackets-blazers/sale",
            "label": "Jackets & Blazers",
            "subcategory": "jackets-blazers/sale",
        },
        "women-s-apparel-jeans-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/jeans/sale",
            "label": "Jeans",
            "subcategory": "jeans/sale",
        },
        "women-s-apparel-pants-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/pants/sale",
            "label": "Pants",
            "subcategory": "pants/sale",
        },
        "women-s-apparel-shorts-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/shorts/sale",
            "label": "Shorts",
            "subcategory": "shorts/sale",
        },
        "women-s-apparel-skirts-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/skirts/sale",
            "label": "Skirts",
            "subcategory": "skirts/sale",
        },
        "women-s-apparel-sweaters-cashmere": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/sweaters/cashmere",
            "label": "Cashmere Sweaters",
            "subcategory": "sweaters/cashmere",
        },
        "women-s-apparel-sweaters-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/sweaters/sale",
            "label": "Sweaters",
            "subcategory": "sweaters/sale",
        },
        "women-s-apparel-swimsuits-beach-cover-ups-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/swimsuits-beach-cover-ups/sale",
            "label": "Swimsuits & Coverups",
            "subcategory": "swimsuits-beach-cover-ups/sale",
        },
        "women-s-apparel-tops-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/tops/sale",
            "label": "Tops",
            "subcategory": "tops/sale",
        },
        "women-s-apparel-dresses-cocktail-black": {
            "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses/cocktail/black",
            "label": "Little Black Dresses",
            "subcategory": "dresses/cocktail/black",
        },
    },
    "Women's Jewelry": {
        "women-s-jewelry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry",
            "label": "Jewelry",
            "subcategory": "women-s-jewelry",
        },
        "women-s-jewelry-boucheron": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/boucheron",
            "label": "Boucheron",
            "subcategory": "boucheron",
        },
        "women-s-jewelry-bracelets": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/bracelets",
            "label": "Bracelets",
            "subcategory": "bracelets",
        },
        "women-s-jewelry-bvlgari": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/bvlgari",
            "label": "BVLGARI",
            "subcategory": "bvlgari",
        },
        "women-s-jewelry-chopard": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/chopard",
            "label": "Chopard",
            "subcategory": "chopard",
        },
        "women-s-jewelry-david-yurman": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/david-yurman",
            "label": "David Yurman",
            "subcategory": "david-yurman",
        },
        "women-s-jewelry-diamonds-at-saks-fifth-avenue": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/diamonds-at-saks-fifth-avenue",
            "label": "Diamonds at Saks Fifth Avenue",
            "subcategory": "diamonds-at-saks-fifth-avenue",
        },
        "women-s-jewelry-earrings": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/earrings",
            "label": "Earrings",
            "subcategory": "earrings",
        },
        "women-s-jewelry-fashion-jewelry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/fashion-jewelry",
            "label": "Fashion Jewelry",
            "subcategory": "fashion-jewelry",
        },
        "women-s-jewelry-fine-jewelry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/fine-jewelry",
            "label": "Fine Jewelry",
            "subcategory": "fine-jewelry",
        },
        "women-s-jewelry-gabriel-co": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/gabriel-co",
            "label": "Gabriel & Co",
            "subcategory": "gabriel-co",
        },
        "women-s-jewelry-ippolita": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/ippolita",
            "label": "Ippolita",
            "subcategory": "ippolita",
        },
        "women-s-jewelry-lana": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/lana",
            "label": "LANA",
            "subcategory": "lana",
        },
        "women-s-jewelry-marco-bicego": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/marco-bicego",
            "label": "Marco Bicego",
            "subcategory": "marco-bicego",
        },
        "women-s-jewelry-necklaces": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/necklaces",
            "label": "Necklaces",
            "subcategory": "necklaces",
        },
        "women-s-jewelry-one-of-a-kind-jewelry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/one-of-a-kind-jewelry",
            "label": "One Of A Kind Jewelry",
            "subcategory": "one-of-a-kind-jewelry",
        },
        "women-s-jewelry-oradina": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/oradina",
            "label": "Oradina",
            "subcategory": "oradina",
        },
        "women-s-jewelry-repossi": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/repossi",
            "label": "Repossi",
            "subcategory": "repossi",
        },
        "women-s-jewelry-rings": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/rings",
            "label": "Rings",
            "subcategory": "rings",
        },
        "women-s-jewelry-roberto-coin": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/roberto-coin",
            "label": "Roberto Coin",
            "subcategory": "roberto-coin",
        },
        "women-s-jewelry-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/sale",
            "label": "Sale",
            "subcategory": "sale",
        },
        "women-s-jewelry-temple-st-clair": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/temple-st.-clair",
            "label": "Temple St. Clair",
            "subcategory": "temple-st.-clair",
        },
        "women-s-jewelry-watches": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/watches",
            "label": "Watches",
            "subcategory": "watches",
        },
        "women-s-jewelry-earrings-hoops": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/earrings/hoops",
            "label": "Hoops",
            "subcategory": "earrings/hoops",
        },
        "women-s-jewelry-earrings-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/earrings/sale",
            "label": "Earrings",
            "subcategory": "earrings/sale",
        },
        "women-s-jewelry-necklaces-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/necklaces/sale",
            "label": "Necklaces",
            "subcategory": "necklaces/sale",
        },
        "women-s-jewelry-watches-fine": {
            "url": "https://www.saksfifthavenue.com/c/women-s-jewelry/watches/fine",
            "label": "Fine Watches",
            "subcategory": "watches/fine",
        },
    },
    "Women's Accessories": {
        "women-s-accessories": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories",
            "label": "Accessories",
            "subcategory": "women-s-accessories",
        },
        "women-s-accessories-belts": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/belts",
            "label": "Belts",
            "subcategory": "belts",
        },
        "women-s-accessories-bottega-veneta": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/bottega-veneta",
            "label": "Bottega Veneta",
            "subcategory": "bottega-veneta",
        },
        "women-s-accessories-brunello-cucinelli": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/brunello-cucinelli",
            "label": "Brunello Cucinelli",
            "subcategory": "brunello-cucinelli",
        },
        "women-s-accessories-burberry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/burberry",
            "label": "Burberry",
            "subcategory": "burberry",
        },
        "women-s-accessories-cartier": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/cartier",
            "label": "Cartier Eyewear",
            "subcategory": "cartier",
        },
        "women-s-accessories-celine": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/celine",
            "label": "CELINE Eyewear",
            "subcategory": "celine",
        },
        "women-s-accessories-cold-weather-accessories": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/cold-weather-accessories",
            "label": "Cold Weather Accessories",
            "subcategory": "cold-weather-accessories",
        },
        "women-s-accessories-dior": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/dior",
            "label": "Dior Eyewear",
            "subcategory": "dior",
        },
        "women-s-accessories-gloves": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/gloves",
            "label": "Gloves & Mittens",
            "subcategory": "gloves",
        },
        "women-s-accessories-gucci": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/gucci",
            "label": "Gucci Eyewear",
            "subcategory": "gucci",
        },
        "women-s-accessories-hair-accessories": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/hair-accessories",
            "label": "Hair Accessories",
            "subcategory": "hair-accessories",
        },
        "women-s-accessories-hats": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/hats",
            "label": "Hats",
            "subcategory": "hats",
        },
        "women-s-accessories-loewe": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/loewe",
            "label": "LOEWE",
            "subcategory": "loewe",
        },
        "women-s-accessories-max-mara": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/max-mara",
            "label": "Max Mara",
            "subcategory": "max-mara",
        },
        "women-s-accessories-miu-miu": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/miu-miu",
            "label": "Miu Miu",
            "subcategory": "miu-miu",
        },
        "women-s-accessories-not-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/not-sale",
            "label": "Accessories Gifts Under $400",
            "subcategory": "not-sale",
        },
        "women-s-accessories-prada": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/prada",
            "label": "Prada",
            "subcategory": "prada",
        },
        "women-s-accessories-saint-laurent": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/saint-laurent",
            "label": "SAINT LAURENT",
            "subcategory": "saint-laurent",
        },
        "women-s-accessories-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/sale",
            "label": "Sale",
            "subcategory": "sale",
        },
        "women-s-accessories-scarves": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/scarves",
            "label": "Scarves & Wraps",
            "subcategory": "scarves",
        },
        "women-s-accessories-sunglasses": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/sunglasses",
            "label": "Sunglasses",
            "subcategory": "sunglasses",
        },
        "women-s-accessories-tom-ford": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/tom-ford",
            "label": "TOM FORD",
            "subcategory": "tom-ford",
        },
        "women-s-accessories-belts-logo": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/belts/logo",
            "label": "Iconic Belts",
            "subcategory": "belts/logo",
        },
        "women-s-accessories-cold-weather-accessories-burberry": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/cold-weather-accessories/burberry",
            "label": "Burberry Cold Weather Accessories",
            "subcategory": "cold-weather-accessories/burberry",
        },
        "women-s-accessories-sunglasses-sale": {
            "url": "https://www.saksfifthavenue.com/c/women-s-accessories/sunglasses/sale",
            "label": "Sunglasses",
            "subcategory": "sunglasses/sale",
        },
    },
    "Shoes": {
        "shoes-shoes": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes",
            "label": "Shoes",
            "subcategory": "shoes",
        },
        "shoes-shoes-boots": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/boots",
            "label": "Boots",
            "subcategory": "shoes/boots",
        },
        "shoes-shoes-christian-louboutin": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/christian-louboutin",
            "label": "Christian Louboutin",
            "subcategory": "shoes/christian-louboutin",
        },
        "shoes-shoes-evening": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/evening",
            "label": "Evening Shoes",
            "subcategory": "shoes/evening",
        },
        "shoes-shoes-fendi": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/fendi",
            "label": "Fendi",
            "subcategory": "shoes/fendi",
        },
        "shoes-shoes-flats": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/flats",
            "label": "Flats",
            "subcategory": "shoes/flats",
        },
        "shoes-shoes-gianvito-rossi": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/gianvito-rossi",
            "label": "Gianvito Rossi",
            "subcategory": "shoes/gianvito-rossi",
        },
        "shoes-shoes-gucci": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/gucci",
            "label": "Gucci",
            "subcategory": "shoes/gucci",
        },
        "shoes-shoes-heels": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/heels",
            "label": "Heels",
            "subcategory": "shoes/heels",
        },
        "shoes-shoes-jimmy-choo": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/jimmy-choo",
            "label": "Jimmy Choo",
            "subcategory": "shoes/jimmy-choo",
        },
        "shoes-shoes-loewe": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/loewe",
            "label": "LOEWE",
            "subcategory": "shoes/loewe",
        },
        "shoes-shoes-manolo-blahnik": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/manolo-blahnik",
            "label": "Manolo Blahnik",
            "subcategory": "shoes/manolo-blahnik",
        },
        "shoes-shoes-miu-miu": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/miu-miu",
            "label": "Miu Miu",
            "subcategory": "shoes/miu-miu",
        },
        "shoes-shoes-not-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/not-sale",
            "label": "Shoe Gifts Under $500",
            "subcategory": "shoes/not-sale",
        },
        "shoes-shoes-oxfords-loafers": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/oxfords-loafers",
            "label": "Loafers",
            "subcategory": "shoes/oxfords-loafers",
        },
        "shoes-shoes-prada": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/prada",
            "label": "Prada",
            "subcategory": "shoes/prada",
        },
        "shoes-shoes-saint-laurent": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/saint-laurent",
            "label": "SAINT LAURENT",
            "subcategory": "shoes/saint-laurent",
        },
        "shoes-shoes-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/sale",
            "label": "Sale",
            "subcategory": "shoes/sale",
        },
        "shoes-shoes-sandals": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/sandals",
            "label": "Sandals",
            "subcategory": "shoes/sandals",
        },
        "shoes-shoes-sneakers": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/sneakers",
            "label": "Sneakers",
            "subcategory": "shoes/sneakers",
        },
        "shoes-shoes-stuart-weitzman": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/stuart-weitzman",
            "label": "Stuart Weitzman",
            "subcategory": "shoes/stuart-weitzman",
        },
        "shoes-shoes-suede": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/suede",
            "label": "Suede Shoes",
            "subcategory": "shoes/suede",
        },
        "shoes-shoes-valentino-garavani": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/valentino-garavani",
            "label": "Valentino Garavani",
            "subcategory": "shoes/valentino-garavani",
        },
        "shoes-shoes-veronica-beard": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/veronica-beard",
            "label": "Veronica Beard",
            "subcategory": "shoes/veronica-beard",
        },
        "shoes-shoes-boots-booties": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/boots/booties",
            "label": "Booties",
            "subcategory": "shoes/boots/booties",
        },
        "shoes-shoes-boots-cold-weather": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/boots/cold-weather",
            "label": "Cold Weather Boots",
            "subcategory": "shoes/boots/cold-weather",
        },
        "shoes-shoes-boots-knee-high": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/boots/knee-high",
            "label": "Statement Boots",
            "subcategory": "shoes/boots/knee-high",
        },
        "shoes-shoes-boots-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/boots/sale",
            "label": "Boots",
            "subcategory": "shoes/boots/sale",
        },
        "shoes-shoes-boots-staud": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/boots/staud",
            "label": "STAUD Wally Boots",
            "subcategory": "shoes/boots/staud",
        },
        "shoes-shoes-flats-ballet-flats": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/flats/ballet-flats",
            "label": "Ballet Flats",
            "subcategory": "shoes/flats/ballet-flats",
        },
        "shoes-shoes-flats-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/flats/sale",
            "label": "Flats",
            "subcategory": "shoes/flats/sale",
        },
        "shoes-shoes-heels-pumps": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/heels/pumps",
            "label": "Pumps",
            "subcategory": "shoes/heels/pumps",
        },
        "shoes-shoes-heels-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/heels/sale",
            "label": "Heels",
            "subcategory": "shoes/heels/sale",
        },
        "shoes-shoes-sandals-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/sandals/sale",
            "label": "Sandals",
            "subcategory": "shoes/sandals/sale",
        },
        "shoes-shoes-sneakers-sale": {
            "url": "https://www.saksfifthavenue.com/c/shoes/shoes/sneakers/sale",
            "label": "Sneakers",
            "subcategory": "shoes/sneakers/sale",
        },
    },
    "Handbags": {
        "handbags-handbags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags",
            "label": "Bags",
            "subcategory": "handbags",
        },
        "handbags-handbags-balenciaga": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/balenciaga",
            "label": "Balenciaga",
            "subcategory": "handbags/balenciaga",
        },
        "handbags-handbags-beach-straw-bags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/beach-straw-bags",
            "label": "Straw & Raffia Bags",
            "subcategory": "handbags/beach-straw-bags",
        },
        "handbags-handbags-bottega-veneta": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/bottega-veneta",
            "label": "Bottega Veneta",
            "subcategory": "handbags/bottega-veneta",
        },
        "handbags-handbags-burberry": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/burberry",
            "label": "Burberry",
            "subcategory": "handbags/burberry",
        },
        "handbags-handbags-chlo-c3-a9": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/chlo%C3%A9",
            "label": "Chloé",
            "subcategory": "handbags/chlo%C3%A9",
        },
        "handbags-handbags-christian-louboutin": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/christian-louboutin",
            "label": "Christian Louboutin",
            "subcategory": "handbags/christian-louboutin",
        },
        "handbags-handbags-clutches-pouches": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/clutches-pouches",
            "label": "Clutches & Pouches",
            "subcategory": "handbags/clutches-pouches",
        },
        "handbags-handbags-crossbody-bags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/crossbody-bags",
            "label": "Crossbody Bags",
            "subcategory": "handbags/crossbody-bags",
        },
        "handbags-handbags-evening-bags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/evening-bags",
            "label": "Evening Bags",
            "subcategory": "handbags/evening-bags",
        },
        "handbags-handbags-hobo-bags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/hobo-bags",
            "label": "Hobo Bags",
            "subcategory": "handbags/hobo-bags",
        },
        "handbags-handbags-jimmy-choo": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/jimmy-choo",
            "label": "Jimmy Choo",
            "subcategory": "handbags/jimmy-choo",
        },
        "handbags-handbags-loewe": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/loewe",
            "label": "LOEWE",
            "subcategory": "handbags/loewe",
        },
        "handbags-handbags-mini-bags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/mini-bags",
            "label": "Mini Bags",
            "subcategory": "handbags/mini-bags",
        },
        "handbags-handbags-miu-miu": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/miu-miu",
            "label": "Miu Miu",
            "subcategory": "handbags/miu-miu",
        },
        "handbags-handbags-not-sale": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/not-sale",
            "label": "Handbag Gifts Under $1,000",
            "subcategory": "handbags/not-sale",
        },
        "handbags-handbags-polo-ralph-lauren": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/polo-ralph-lauren",
            "label": "Marc Jacobs",
            "subcategory": "handbags/polo-ralph-lauren",
        },
        "handbags-handbags-prada": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/prada",
            "label": "Prada",
            "subcategory": "handbags/prada",
        },
        "handbags-handbags-red": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/red",
            "label": "Burgundy Bags",
            "subcategory": "handbags/red",
        },
        "handbags-handbags-saint-laurent": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/saint-laurent",
            "label": "SAINT LAURENT",
            "subcategory": "handbags/saint-laurent",
        },
        "handbags-handbags-sale": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/sale",
            "label": "Sale",
            "subcategory": "handbags/sale",
        },
        "handbags-handbags-shoulder-bags": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/shoulder-bags",
            "label": "Shoulder Bags",
            "subcategory": "handbags/shoulder-bags",
        },
        "handbags-handbags-suede": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/suede",
            "label": "Suede Bags",
            "subcategory": "handbags/suede",
        },
        "handbags-handbags-top-handles-satchels": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/top-handles-satchels",
            "label": "Top Handles & Satchels",
            "subcategory": "handbags/top-handles-satchels",
        },
        "handbags-handbags-totes": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/totes",
            "label": "Tote Bags",
            "subcategory": "handbags/totes",
        },
        "handbags-handbags-valentino-garavani": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/valentino-garavani",
            "label": "Valentino Garavani",
            "subcategory": "handbags/valentino-garavani",
        },
        "handbags-handbags-wallets-card-cases": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/wallets-card-cases",
            "label": "Wallets & Card Cases",
            "subcategory": "handbags/wallets-card-cases",
        },
        "handbags-handbags-crossbody-bags-sale": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/crossbody-bags/sale",
            "label": "Crossbody Bags",
            "subcategory": "handbags/crossbody-bags/sale",
        },
        "handbags-handbags-shoulder-bags-sale": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/shoulder-bags/sale",
            "label": "Shoulder Bags",
            "subcategory": "handbags/shoulder-bags/sale",
        },
        "handbags-handbags-top-handles-satchels-sale": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/top-handles-satchels/sale",
            "label": "Top Handles & Satchels",
            "subcategory": "handbags/top-handles-satchels/sale",
        },
        "handbags-handbags-totes-sale": {
            "url": "https://www.saksfifthavenue.com/c/handbags/handbags/totes/sale",
            "label": "Totes",
            "subcategory": "handbags/totes/sale",
        },
    },
    "Beauty": {
        "beauty-view-all-beauty": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty",
            "label": "Beauty",
            "subcategory": "view-all-beauty",
        },
        "beauty-view-all-beauty-balenciaga": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/balenciaga",
            "label": "Balenciaga",
            "subcategory": "view-all-beauty/balenciaga",
        },
        "beauty-view-all-beauty-bath-body": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/bath-body",
            "label": "Bath & Body",
            "subcategory": "view-all-beauty/bath-body",
        },
        "beauty-view-all-beauty-bond-no-9-new-york": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/bond-no.9-new-york",
            "label": "Bond No.9 New York",
            "subcategory": "view-all-beauty/bond-no.9-new-york",
        },
        "beauty-view-all-beauty-bottega-veneta": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/bottega-veneta",
            "label": "NEW: Bottega Veneta",
            "subcategory": "view-all-beauty/bottega-veneta",
        },
        "beauty-view-all-beauty-byredo": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/byredo",
            "label": "Byredo",
            "subcategory": "view-all-beauty/byredo",
        },
        "beauty-view-all-beauty-cl-c3-a9-de-peau-beaut-c3-a9": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/cl%C3%A9-de-peau-beaut%C3%A9",
            "label": "Clé de Peau Beauté",
            "subcategory": "view-all-beauty/cl%C3%A9-de-peau-beaut%C3%A9",
        },
        "beauty-view-all-beauty-dior": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/dior",
            "label": "Dior",
            "subcategory": "view-all-beauty/dior",
        },
        "beauty-view-all-beauty-fragrance": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/fragrance",
            "label": "Fragrance & Perfume",
            "subcategory": "view-all-beauty/fragrance",
        },
        "beauty-view-all-beauty-gifts-gift-sets": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/gifts-gift-sets",
            "label": "Gifts & Gift Sets",
            "subcategory": "view-all-beauty/gifts-gift-sets",
        },
        "beauty-view-all-beauty-guerlain": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/guerlain",
            "label": "GUERLAIN",
            "subcategory": "view-all-beauty/guerlain",
        },
        "beauty-view-all-beauty-hair-care": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/hair-care",
            "label": "Hair Care & Styling Tools",
            "subcategory": "view-all-beauty/hair-care",
        },
        "beauty-view-all-beauty-la-mer": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/la-mer",
            "label": "La Mer",
            "subcategory": "view-all-beauty/la-mer",
        },
        "beauty-view-all-beauty-la-prairie": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/la-prairie",
            "label": "La Prairie",
            "subcategory": "view-all-beauty/la-prairie",
        },
        "beauty-view-all-beauty-loewe-perfumes": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/loewe-perfumes",
            "label": "LOEWE Perfumes",
            "subcategory": "view-all-beauty/loewe-perfumes",
        },
        "beauty-view-all-beauty-maison-francis-kurkdjian": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/maison-francis-kurkdjian",
            "label": "Maison Francis Kurkdjian",
            "subcategory": "view-all-beauty/maison-francis-kurkdjian",
        },
        "beauty-view-all-beauty-makeup": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/makeup",
            "label": "Makeup",
            "subcategory": "view-all-beauty/makeup",
        },
        "beauty-view-all-beauty-parfums-de-marly": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/parfums-de-marly",
            "label": "Parfums de Marly",
            "subcategory": "view-all-beauty/parfums-de-marly",
        },
        "beauty-view-all-beauty-sisley-paris": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/sisley-paris",
            "label": "Sisley-Paris",
            "subcategory": "view-all-beauty/sisley-paris",
        },
        "beauty-view-all-beauty-skin-care": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/skin-care",
            "label": "Skin Care",
            "subcategory": "view-all-beauty/skin-care",
        },
        "beauty-view-all-beauty-makeup-eyes": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/makeup/eyes",
            "label": "Eyes",
            "subcategory": "view-all-beauty/makeup/eyes",
        },
        "beauty-view-all-beauty-makeup-face": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/makeup/face",
            "label": "Face",
            "subcategory": "view-all-beauty/makeup/face",
        },
        "beauty-view-all-beauty-makeup-lips": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/makeup/lips",
            "label": "Lips",
            "subcategory": "view-all-beauty/makeup/lips",
        },
        "beauty-view-all-beauty-skin-care-eye-creams-treatments": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/skin-care/eye-creams-treatments",
            "label": "Eye Creams & Treatments",
            "subcategory": "view-all-beauty/skin-care/eye-creams-treatments",
        },
        "beauty-view-all-beauty-skin-care-moisturizers": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/skin-care/moisturizers",
            "label": "Moisturizers",
            "subcategory": "view-all-beauty/skin-care/moisturizers",
        },
        "beauty-view-all-beauty-skin-care-serums-essences": {
            "url": "https://www.saksfifthavenue.com/c/beauty/view-all-beauty/skin-care/serums-essences",
            "label": "Serums & Essences",
            "subcategory": "view-all-beauty/skin-care/serums-essences",
        },
    },
    "Men": {
        "men-accessories": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories",
            "label": "Accessories",
            "subcategory": "accessories",
        },
        "men-amiri": {
            "url": "https://www.saksfifthavenue.com/c/men/amiri",
            "label": "Amiri",
            "subcategory": "amiri",
        },
        "men-apparel": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel",
            "label": "Clothing",
            "subcategory": "apparel",
        },
        "men-balenciaga": {
            "url": "https://www.saksfifthavenue.com/c/men/balenciaga",
            "label": "Balenciaga",
            "subcategory": "balenciaga",
        },
        "men-brunello-cucinelli": {
            "url": "https://www.saksfifthavenue.com/c/men/brunello-cucinelli",
            "label": "Brunello Cucinelli",
            "subcategory": "brunello-cucinelli",
        },
        "men-burberry": {
            "url": "https://www.saksfifthavenue.com/c/men/burberry",
            "label": "Burberry",
            "subcategory": "burberry",
        },
        "men-canali": {
            "url": "https://www.saksfifthavenue.com/c/men/canali",
            "label": "Canali",
            "subcategory": "canali",
        },
        "men-casablanca": {
            "url": "https://www.saksfifthavenue.com/c/men/casablanca",
            "label": "Casablanca",
            "subcategory": "casablanca",
        },
        "men-christian-louboutin": {
            "url": "https://www.saksfifthavenue.com/c/men/christian-louboutin",
            "label": "Christian Louboutin",
            "subcategory": "christian-louboutin",
        },
        "men-dolce-gabbana": {
            "url": "https://www.saksfifthavenue.com/c/men/dolce-gabbana",
            "label": "Dolce&Gabbana",
            "subcategory": "dolce-gabbana",
        },
        "men-ferragamo": {
            "url": "https://www.saksfifthavenue.com/c/men/ferragamo",
            "label": "FERRAGAMO",
            "subcategory": "ferragamo",
        },
        "men-grooming-cologne": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne",
            "label": "Men's Grooming & Cologne",
            "subcategory": "grooming-cologne",
        },
        "men-gucci": {
            "url": "https://www.saksfifthavenue.com/c/men/gucci",
            "label": "Gucci",
            "subcategory": "gucci",
        },
        "men-ksubi": {
            "url": "https://www.saksfifthavenue.com/c/men/ksubi",
            "label": "Ksubi",
            "subcategory": "ksubi",
        },
        "men-loewe": {
            "url": "https://www.saksfifthavenue.com/c/men/loewe",
            "label": "LOEWE",
            "subcategory": "loewe",
        },
        "men-moncler": {
            "url": "https://www.saksfifthavenue.com/c/men/moncler",
            "label": "Moncler",
            "subcategory": "moncler",
        },
        "men-polo-ralph-lauren": {
            "url": "https://www.saksfifthavenue.com/c/men/polo-ralph-lauren",
            "label": "Polo Ralph Lauren",
            "subcategory": "polo-ralph-lauren",
        },
        "men-prada": {
            "url": "https://www.saksfifthavenue.com/c/men/prada",
            "label": "Prada",
            "subcategory": "prada",
        },
        "men-purple-brand": {
            "url": "https://www.saksfifthavenue.com/c/men/purple-brand",
            "label": "Purple Brand",
            "subcategory": "purple-brand",
        },
        "men-ralph-lauren-purple-label": {
            "url": "https://www.saksfifthavenue.com/c/men/ralph-lauren-purple-label",
            "label": "Ralph Lauren Purple Label",
            "subcategory": "ralph-lauren-purple-label",
        },
        "men-rhude": {
            "url": "https://www.saksfifthavenue.com/c/men/rhude",
            "label": "Rhude",
            "subcategory": "rhude",
        },
        "men-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/sale",
            "label": "Men's",
            "subcategory": "sale",
        },
        "men-shoes": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes",
            "label": "Shoes",
            "subcategory": "shoes",
        },
        "men-versace": {
            "url": "https://www.saksfifthavenue.com/c/men/versace",
            "label": "Versace",
            "subcategory": "versace",
        },
        "men-zegna": {
            "url": "https://www.saksfifthavenue.com/c/men/zegna",
            "label": "ZEGNA",
            "subcategory": "zegna",
        },
        "men-accessories-amiri": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/amiri",
            "label": "Amiri",
            "subcategory": "accessories/amiri",
        },
        "men-accessories-bags": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/bags",
            "label": "Bags",
            "subcategory": "accessories/bags",
        },
        "men-accessories-belts": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/belts",
            "label": "Belts",
            "subcategory": "accessories/belts",
        },
        "men-accessories-bottega-veneta": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/bottega-veneta",
            "label": "Bottega Veneta",
            "subcategory": "accessories/bottega-veneta",
        },
        "men-accessories-burberry": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/burberry",
            "label": "Burberry",
            "subcategory": "accessories/burberry",
        },
        "men-accessories-cartier": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/cartier",
            "label": "Cartier",
            "subcategory": "accessories/cartier",
        },
        "men-accessories-cold-weather-shop": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/cold-weather-shop",
            "label": "Cold Weather Accessories",
            "subcategory": "accessories/cold-weather-shop",
        },
        "men-accessories-david-yurman": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/david-yurman",
            "label": "David Yurman",
            "subcategory": "accessories/david-yurman",
        },
        "men-accessories-ferragamo": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/ferragamo",
            "label": "FERRAGAMO",
            "subcategory": "accessories/ferragamo",
        },
        "men-accessories-hats": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/hats",
            "label": "Hats",
            "subcategory": "accessories/hats",
        },
        "men-accessories-jewelry": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/jewelry",
            "label": "Jewelry for Him",
            "subcategory": "accessories/jewelry",
        },
        "men-accessories-montblanc": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/montblanc",
            "label": "Montblanc",
            "subcategory": "accessories/montblanc",
        },
        "men-accessories-prada": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/prada",
            "label": "Prada",
            "subcategory": "accessories/prada",
        },
        "men-accessories-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/sale",
            "label": "Accessories",
            "subcategory": "accessories/sale",
        },
        "men-accessories-sunglasses": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/sunglasses",
            "label": "Sunglasses",
            "subcategory": "accessories/sunglasses",
        },
        "men-accessories-tag-heuer": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/tag-heuer",
            "label": "TAG Heuer",
            "subcategory": "accessories/tag-heuer",
        },
        "men-accessories-ties-formal-accessories": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/ties-formal-accessories",
            "label": "Ties & Formal Accessories",
            "subcategory": "accessories/ties-formal-accessories",
        },
        "men-accessories-tom-ford": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/tom-ford",
            "label": "TOM FORD",
            "subcategory": "accessories/tom-ford",
        },
        "men-accessories-wallets-card-cases": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/wallets-card-cases",
            "label": "Wallets & Card Cases",
            "subcategory": "accessories/wallets-card-cases",
        },
        "men-accessories-watches": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/watches",
            "label": "Watches",
            "subcategory": "accessories/watches",
        },
        "men-apparel-amiri": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/amiri",
            "label": "Amiri",
            "subcategory": "apparel/amiri",
        },
        "men-apparel-brunello-cucinelli": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/brunello-cucinelli",
            "label": "Brunello Cucinelli",
            "subcategory": "apparel/brunello-cucinelli",
        },
        "men-apparel-canada-goose": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/canada-goose",
            "label": "Canada Goose",
            "subcategory": "apparel/canada-goose",
        },
        "men-apparel-casablanca": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/casablanca",
            "label": "Casablanca",
            "subcategory": "apparel/casablanca",
        },
        "men-apparel-casual-button-down-shirts": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/casual-button-down-shirts",
            "label": "Casual Button-Down Shirts",
            "subcategory": "apparel/casual-button-down-shirts",
        },
        "men-apparel-coats-jackets": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/coats-jackets",
            "label": "Coats & Jackets",
            "subcategory": "apparel/coats-jackets",
        },
        "men-apparel-denim-jeans": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/denim-jeans",
            "label": "Jeans",
            "subcategory": "apparel/denim-jeans",
        },
        "men-apparel-dress-shirts": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/dress-shirts",
            "label": "Dress Shirts",
            "subcategory": "apparel/dress-shirts",
        },
        "men-apparel-ksubi": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/ksubi",
            "label": "Ksubi",
            "subcategory": "apparel/ksubi",
        },
        "men-apparel-matching-sets": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/matching-sets",
            "label": "Matching Sets",
            "subcategory": "apparel/matching-sets",
        },
        "men-apparel-moncler": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/moncler",
            "label": "Moncler",
            "subcategory": "apparel/moncler",
        },
        "men-apparel-pajamas-loungewear-robes": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/pajamas--loungewear-robes",
            "label": "Pajamas & Loungewear",
            "subcategory": "apparel/pajamas--loungewear-robes",
        },
        "men-apparel-pants": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/pants",
            "label": "Pants",
            "subcategory": "apparel/pants",
        },
        "men-apparel-polo-ralph-lauren": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/polo-ralph-lauren",
            "label": "Polo Ralph Lauren",
            "subcategory": "apparel/polo-ralph-lauren",
        },
        "men-apparel-polos": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/polos",
            "label": "Polos",
            "subcategory": "apparel/polos",
        },
        "men-apparel-prada": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/prada",
            "label": "Prada",
            "subcategory": "apparel/prada",
        },
        "men-apparel-purple-brand": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/purple-brand",
            "label": "Purple Brand",
            "subcategory": "apparel/purple-brand",
        },
        "men-apparel-ralph-lauren-purple-label": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/ralph-lauren-purple-label",
            "label": "Ralph Lauren Purple Label",
            "subcategory": "apparel/ralph-lauren-purple-label",
        },
        "men-apparel-rhude": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/rhude",
            "label": "Rhude",
            "subcategory": "apparel/rhude",
        },
        "men-apparel-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/sale",
            "label": "Clothing",
            "subcategory": "apparel/sale",
        },
        "men-apparel-shorts": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/shorts",
            "label": "Shorts",
            "subcategory": "apparel/shorts",
        },
        "men-apparel-sportscoats-blazers": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/sportscoats-blazers",
            "label": "Blazers & Sportcoats",
            "subcategory": "apparel/sportscoats-blazers",
        },
        "men-apparel-suits-suit-separates": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/suits-suit-separates",
            "label": "Suits & Suit Separates",
            "subcategory": "apparel/suits-suit-separates",
        },
        "men-apparel-sweaters": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/sweaters",
            "label": "Sweaters",
            "subcategory": "apparel/sweaters",
        },
        "men-apparel-sweatshirts-hoodies": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/sweatshirts-hoodies",
            "label": "Sweatshirts & Hoodies",
            "subcategory": "apparel/sweatshirts-hoodies",
        },
        "men-apparel-swimwear": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/swimwear",
            "label": "Swimwear",
            "subcategory": "apparel/swimwear",
        },
        "men-apparel-t-shirts": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/t-shirts",
            "label": "T-Shirts",
            "subcategory": "apparel/t-shirts",
        },
        "men-apparel-tuxedos-formal-wear": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/tuxedos-formal-wear",
            "label": "Tuxedos & Formal Wear",
            "subcategory": "apparel/tuxedos-formal-wear",
        },
        "men-apparel-underwear-socks": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/underwear-socks",
            "label": "Underwear & Socks",
            "subcategory": "apparel/underwear-socks",
        },
        "men-best-sellers-accessories": {
            "url": "https://www.saksfifthavenue.com/c/men/best-sellers/accessories",
            "label": "Best Sellers",
            "subcategory": "best-sellers/accessories",
        },
        "men-best-sellers-apparel": {
            "url": "https://www.saksfifthavenue.com/c/men/best-sellers/apparel",
            "label": "Best Sellers",
            "subcategory": "best-sellers/apparel",
        },
        "men-best-sellers-grooming-cologne": {
            "url": "https://www.saksfifthavenue.com/c/men/best-sellers/grooming-cologne",
            "label": "Best Sellers",
            "subcategory": "best-sellers/grooming-cologne",
        },
        "men-best-sellers-men-s-shoes": {
            "url": "https://www.saksfifthavenue.com/c/men/best-sellers/men-s-shoes",
            "label": "Best Sellers",
            "subcategory": "best-sellers/men-s-shoes",
        },
        "men-canali-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/canali/sale",
            "label": "Canali",
            "subcategory": "canali/sale",
        },
        "men-grooming-cologne-acqua-di-parma": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/acqua-di-parma",
            "label": "Acqua di Parma",
            "subcategory": "grooming-cologne/acqua-di-parma",
        },
        "men-grooming-cologne-balenciaga": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/balenciaga",
            "label": "Balenciaga",
            "subcategory": "grooming-cologne/balenciaga",
        },
        "men-grooming-cologne-bath-body": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/bath-body",
            "label": "Bath & Body",
            "subcategory": "grooming-cologne/bath-body",
        },
        "men-grooming-cologne-bond-no-9-new-york": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/bond-no.9-new-york",
            "label": "Bond No.9 New York",
            "subcategory": "grooming-cologne/bond-no.9-new-york",
        },
        "men-grooming-cologne-cologne": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/cologne",
            "label": "Cologne",
            "subcategory": "grooming-cologne/cologne",
        },
        "men-grooming-cologne-creed": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/creed",
            "label": "CREED",
            "subcategory": "grooming-cologne/creed",
        },
        "men-grooming-cologne-dior": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/dior",
            "label": "Dior",
            "subcategory": "grooming-cologne/dior",
        },
        "men-grooming-cologne-guerlain": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/guerlain",
            "label": "GUERLAIN",
            "subcategory": "grooming-cologne/guerlain",
        },
        "men-grooming-cologne-herm-c3-a8s": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/herm%C3%A8s",
            "label": "HERMÈS",
            "subcategory": "grooming-cologne/herm%C3%A8s",
        },
        "men-grooming-cologne-jo-malone-london": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/jo-malone-london",
            "label": "Jo Malone London",
            "subcategory": "grooming-cologne/jo-malone-london",
        },
        "men-grooming-cologne-kits-gift-sets": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/kits-gift-sets",
            "label": "Gifts & Gift Sets",
            "subcategory": "grooming-cologne/kits-gift-sets",
        },
        "men-grooming-cologne-le-labo": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/le-labo",
            "label": "Le Labo",
            "subcategory": "grooming-cologne/le-labo",
        },
        "men-grooming-cologne-loewe-perfumes": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/loewe-perfumes",
            "label": "LOEWE Perfumes",
            "subcategory": "grooming-cologne/loewe-perfumes",
        },
        "men-grooming-cologne-maison-francis-kurkdjian": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/maison-francis-kurkdjian",
            "label": "Maison Francis Kurkdjian",
            "subcategory": "grooming-cologne/maison-francis-kurkdjian",
        },
        "men-grooming-cologne-parfums-de-marly": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/parfums-de-marly",
            "label": "Parfums de Marly",
            "subcategory": "grooming-cologne/parfums-de-marly",
        },
        "men-grooming-cologne-skin-care": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/skin-care",
            "label": "Skin Care",
            "subcategory": "grooming-cologne/skin-care",
        },
        "men-grooming-cologne-tom-ford": {
            "url": "https://www.saksfifthavenue.com/c/men/grooming-cologne/tom-ford",
            "label": "TOM FORD",
            "subcategory": "grooming-cologne/tom-ford",
        },
        "men-polo-ralph-lauren-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/polo-ralph-lauren/sale",
            "label": "Polo Ralph Lauren",
            "subcategory": "polo-ralph-lauren/sale",
        },
        "men-purple-brand-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/purple-brand/sale",
            "label": "Purple Brand",
            "subcategory": "purple-brand/sale",
        },
        "men-ralph-lauren-purple-label-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/ralph-lauren-purple-label/sale",
            "label": "Ralph Lauren Purple Label",
            "subcategory": "ralph-lauren-purple-label/sale",
        },
        "men-shoes-amiri": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/amiri",
            "label": "Amiri",
            "subcategory": "shoes/amiri",
        },
        "men-shoes-balenciaga": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/balenciaga",
            "label": "Balenciaga",
            "subcategory": "shoes/balenciaga",
        },
        "men-shoes-boots": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/boots",
            "label": "Boots",
            "subcategory": "shoes/boots",
        },
        "men-shoes-bottega-veneta": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/bottega-veneta",
            "label": "Bottega Veneta",
            "subcategory": "shoes/bottega-veneta",
        },
        "men-shoes-christian-louboutin": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/christian-louboutin",
            "label": "Christian Louboutin",
            "subcategory": "shoes/christian-louboutin",
        },
        "men-shoes-dress-shoes": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/dress-shoes",
            "label": "Dress Shoes",
            "subcategory": "shoes/dress-shoes",
        },
        "men-shoes-ferragamo": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/ferragamo",
            "label": "FERRAGAMO",
            "subcategory": "shoes/ferragamo",
        },
        "men-shoes-golden-goose": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/golden-goose",
            "label": "Golden Goose",
            "subcategory": "shoes/golden-goose",
        },
        "men-shoes-gucci": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/gucci",
            "label": "Gucci",
            "subcategory": "shoes/gucci",
        },
        "men-shoes-loafers-slip-ons": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/loafers-slip-ons",
            "label": "Loafers & Slip Ons",
            "subcategory": "shoes/loafers-slip-ons",
        },
        "men-shoes-maison-margiela": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/maison-margiela",
            "label": "Maison Margiela",
            "subcategory": "shoes/maison-margiela",
        },
        "men-shoes-mcqueen": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/mcqueen",
            "label": "McQueen",
            "subcategory": "shoes/mcqueen",
        },
        "men-shoes-prada": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/prada",
            "label": "Prada",
            "subcategory": "shoes/prada",
        },
        "men-shoes-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/sale",
            "label": "Shoes",
            "subcategory": "shoes/sale",
        },
        "men-shoes-santoni": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/santoni",
            "label": "Santoni",
            "subcategory": "shoes/santoni",
        },
        "men-shoes-slides-sandals": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/slides-sandals",
            "label": "Slides & Sandals",
            "subcategory": "shoes/slides-sandals",
        },
        "men-shoes-sneakers": {
            "url": "https://www.saksfifthavenue.com/c/men/shoes/sneakers",
            "label": "Sneakers",
            "subcategory": "shoes/sneakers",
        },
        "men-valentino-garavani-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/valentino-garavani/sale",
            "label": "Valentino Garavani",
            "subcategory": "valentino-garavani/sale",
        },
        "men-accessories-jewelry-bracelets": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/jewelry/bracelets",
            "label": "Bracelets",
            "subcategory": "accessories/jewelry/bracelets",
        },
        "men-accessories-watches-fine-watches": {
            "url": "https://www.saksfifthavenue.com/c/men/accessories/watches/fine-watches",
            "label": "Fine Watches",
            "subcategory": "accessories/watches/fine-watches",
        },
        "men-apparel-casual-button-down-shirts-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/casual-button-down-shirts/sale",
            "label": "Casual Button Down Shirts",
            "subcategory": "apparel/casual-button-down-shirts/sale",
        },
        "men-apparel-coats-jackets-leather-shearling": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/coats-jackets/leather-shearling",
            "label": "Leather & Suede Jackets",
            "subcategory": "apparel/coats-jackets/leather-shearling",
        },
        "men-apparel-coats-jackets-peacoats-overcoats-topcoats": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/coats-jackets/peacoats--overcoats-topcoats",
            "label": "Peacoats, Overcoats, & Topcoats",
            "subcategory": "apparel/coats-jackets/peacoats--overcoats-topcoats",
        },
        "men-apparel-coats-jackets-puffer-down-jackets": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/coats-jackets/puffer-down-jackets",
            "label": "Puffer & Down Jackets",
            "subcategory": "apparel/coats-jackets/puffer-down-jackets",
        },
        "men-apparel-coats-jackets-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/coats-jackets/sale",
            "label": "Coats & Jackets",
            "subcategory": "apparel/coats-jackets/sale",
        },
        "men-apparel-coats-jackets-vests": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/coats-jackets/vests",
            "label": "Vests",
            "subcategory": "apparel/coats-jackets/vests",
        },
        "men-apparel-sweaters-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/sweaters/sale",
            "label": "Sweaters",
            "subcategory": "apparel/sweaters/sale",
        },
        "men-apparel-sweatshirts-hoodies-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/sweatshirts-hoodies/sale",
            "label": "Sweatshirts & Hoodies",
            "subcategory": "apparel/sweatshirts-hoodies/sale",
        },
        "men-apparel-t-shirts-sale": {
            "url": "https://www.saksfifthavenue.com/c/men/apparel/t-shirts/sale",
            "label": "T-Shirts",
            "subcategory": "apparel/t-shirts/sale",
        },
    },
    "Kids": {
        "kids": {
            "url": "https://www.saksfifthavenue.com/c/kids",
            "label": "All Kids",
            "subcategory": "kids",
        },
        "kids-amiri": {
            "url": "https://www.saksfifthavenue.com/c/kids/amiri",
            "label": "Amiri",
            "subcategory": "amiri",
        },
        "kids-baby": {
            "url": "https://www.saksfifthavenue.com/c/kids/baby",
            "label": "Baby (Sizes 0-24 M)",
            "subcategory": "baby",
        },
        "kids-boys": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys",
            "label": "Boys",
            "subcategory": "boys",
        },
        "kids-burberry": {
            "url": "https://www.saksfifthavenue.com/c/kids/burberry",
            "label": "Burberry",
            "subcategory": "burberry",
        },
        "kids-dolce-gabbana": {
            "url": "https://www.saksfifthavenue.com/c/kids/dolce-gabbana",
            "label": "Dolce&Gabbana",
            "subcategory": "dolce-gabbana",
        },
        "kids-girls": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls",
            "label": "Girls",
            "subcategory": "girls",
        },
        "kids-golden-goose": {
            "url": "https://www.saksfifthavenue.com/c/kids/golden-goose",
            "label": "Golden Goose",
            "subcategory": "golden-goose",
        },
        "kids-molo": {
            "url": "https://www.saksfifthavenue.com/c/kids/molo",
            "label": "Molo",
            "subcategory": "molo",
        },
        "kids-moncler": {
            "url": "https://www.saksfifthavenue.com/c/kids/moncler",
            "label": "Moncler",
            "subcategory": "moncler",
        },
        "kids-polo-ralph-lauren": {
            "url": "https://www.saksfifthavenue.com/c/kids/polo-ralph-lauren",
            "label": "Polo Ralph Lauren",
            "subcategory": "polo-ralph-lauren",
        },
        "kids-sale": {
            "url": "https://www.saksfifthavenue.com/c/kids/sale",
            "label": "Sale",
            "subcategory": "sale",
        },
        "kids-tulleen": {
            "url": "https://www.saksfifthavenue.com/c/kids/tulleen",
            "label": "Tulleen",
            "subcategory": "tulleen",
        },
        "kids-versace": {
            "url": "https://www.saksfifthavenue.com/c/kids/versace",
            "label": "Versace",
            "subcategory": "versace",
        },
        "kids-baby-baby-boy-0-24-months": {
            "url": "https://www.saksfifthavenue.com/c/kids/baby/baby-boy--0-24-months-",
            "label": "Baby Boy",
            "subcategory": "baby/baby-boy--0-24-months-",
        },
        "kids-baby-baby-girl-0-24-months": {
            "url": "https://www.saksfifthavenue.com/c/kids/baby/baby-girl--0-24-months-",
            "label": "Baby Girl",
            "subcategory": "baby/baby-girl--0-24-months-",
        },
        "kids-baby-shoes": {
            "url": "https://www.saksfifthavenue.com/c/kids/baby/shoes",
            "label": "Baby Shoes",
            "subcategory": "baby/shoes",
        },
        "kids-boys-bottoms": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/bottoms",
            "label": "Bottoms",
            "subcategory": "boys/bottoms",
        },
        "kids-boys-boys-clothing-sizes-7-20": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/boys--clothing--sizes-7-20-",
            "label": "Boys' Clothing (Sizes 7-20)",
            "subcategory": "boys/boys--clothing--sizes-7-20-",
        },
        "kids-boys-boys-coats-jackets": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/boys-coats-jackets",
            "label": "Coats & Jackets",
            "subcategory": "boys/boys-coats-jackets",
        },
        "kids-boys-shoes": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/shoes",
            "label": "Boys' Shoes",
            "subcategory": "boys/shoes",
        },
        "kids-boys-suits-separates": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/suits-separates",
            "label": "Suits & Separates",
            "subcategory": "boys/suits-separates",
        },
        "kids-boys-toddler-boys-clothing-sizes-2-6": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/toddler-boys--clothing--sizes-2-6-",
            "label": "Toddler Boys' Clothing (Sizes 2-6)",
            "subcategory": "boys/toddler-boys--clothing--sizes-2-6-",
        },
        "kids-boys-tops": {
            "url": "https://www.saksfifthavenue.com/c/kids/boys/tops",
            "label": "Tops",
            "subcategory": "boys/tops",
        },
        "kids-girls-accessories": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/accessories",
            "label": "Accessories",
            "subcategory": "girls/accessories",
        },
        "kids-girls-bottoms": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/bottoms",
            "label": "Bottoms",
            "subcategory": "girls/bottoms",
        },
        "kids-girls-dresses": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/dresses",
            "label": "Dresses",
            "subcategory": "girls/dresses",
        },
        "kids-girls-girls-2-6": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/girls--2-6-",
            "label": "Toddler Girls' Clothing (Sizes 2-6)",
            "subcategory": "girls/girls--2-6-",
        },
        "kids-girls-girls-clothing-sizes-7-20": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/girls--clothing--sizes-7-20-",
            "label": "Girls' Clothing (Sizes 7-16)",
            "subcategory": "girls/girls--clothing--sizes-7-20-",
        },
        "kids-girls-girls-coats-jackets": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/girls-coats-jackets",
            "label": "Coats & Jackets",
            "subcategory": "girls/girls-coats-jackets",
        },
        "kids-girls-shoes": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/shoes",
            "label": "Girls' Shoes",
            "subcategory": "girls/shoes",
        },
        "kids-girls-tops": {
            "url": "https://www.saksfifthavenue.com/c/kids/girls/tops",
            "label": "Tops",
            "subcategory": "girls/tops",
        },
    },
    "Home": {
        "home": {
            "url": "https://www.saksfifthavenue.com/c/home",
            "label": "Home",
            "subcategory": "home",
        },
        "home-assouline": {
            "url": "https://www.saksfifthavenue.com/c/home/assouline",
            "label": "Assouline",
            "subcategory": "assouline",
        },
        "home-bath": {
            "url": "https://www.saksfifthavenue.com/c/home/bath",
            "label": "Bath",
            "subcategory": "bath",
        },
        "home-bedding": {
            "url": "https://www.saksfifthavenue.com/c/home/bedding",
            "label": "Bedding",
            "subcategory": "bedding",
        },
        "home-best-sellers": {
            "url": "https://www.saksfifthavenue.com/c/home/best-sellers",
            "label": "Best Sellers",
            "subcategory": "best-sellers",
        },
        "home-dining-entertaining": {
            "url": "https://www.saksfifthavenue.com/c/home/dining-entertaining",
            "label": "Dining & Entertaining",
            "subcategory": "dining-entertaining",
        },
        "home-dolce-gabbana": {
            "url": "https://www.saksfifthavenue.com/c/home/dolce-gabbana",
            "label": "Dolce&Gabbana",
            "subcategory": "dolce-gabbana",
        },
        "home-fornasetti": {
            "url": "https://www.saksfifthavenue.com/c/home/fornasetti",
            "label": "Fornasetti",
            "subcategory": "fornasetti",
        },
        "home-ginori-1735": {
            "url": "https://www.saksfifthavenue.com/c/home/ginori-1735",
            "label": "Ginori 1735",
            "subcategory": "ginori-1735",
        },
        "home-holiday-christmas": {
            "url": "https://www.saksfifthavenue.com/c/home/holiday-christmas",
            "label": "Home Holiday Shop",
            "subcategory": "holiday-christmas",
        },
        "home-home-decor": {
            "url": "https://www.saksfifthavenue.com/c/home/home-decor",
            "label": "Home Décor",
            "subcategory": "home-decor",
        },
        "home-jonathan-adler": {
            "url": "https://www.saksfifthavenue.com/c/home/jonathan-adler",
            "label": "Jonathan Adler",
            "subcategory": "jonathan-adler",
        },
        "home-kitchen": {
            "url": "https://www.saksfifthavenue.com/c/home/kitchen",
            "label": "Kitchen",
            "subcategory": "kitchen",
        },
        "home-luggage-travel-gear": {
            "url": "https://www.saksfifthavenue.com/c/home/luggage-travel-gear",
            "label": "Luggage & Travel",
            "subcategory": "luggage-travel-gear",
        },
        "home-mackenzie-childs": {
            "url": "https://www.saksfifthavenue.com/c/home/mackenzie-childs",
            "label": "MacKenzie-Childs",
            "subcategory": "mackenzie-childs",
        },
        "home-michael-aram": {
            "url": "https://www.saksfifthavenue.com/c/home/michael-aram",
            "label": "Michael Aram",
            "subcategory": "michael-aram",
        },
        "home-ralph-lauren": {
            "url": "https://www.saksfifthavenue.com/c/home/ralph-lauren",
            "label": "Ralph Lauren",
            "subcategory": "ralph-lauren",
        },
        "home-sale": {
            "url": "https://www.saksfifthavenue.com/c/home/sale",
            "label": "Sale & Limited Time Offers",
            "subcategory": "sale",
        },
        "home-tech-accessories": {
            "url": "https://www.saksfifthavenue.com/c/home/tech-accessories",
            "label": "Household Tech",
            "subcategory": "tech-accessories",
        },
        "home-wolf": {
            "url": "https://www.saksfifthavenue.com/c/home/wolf",
            "label": "WOLF",
            "subcategory": "wolf",
        },
        "home-dining-entertaining-drinkware-glassware": {
            "url": "https://www.saksfifthavenue.com/c/home/dining-entertaining/drinkware-glassware",
            "label": "Drinkware & Glassware",
            "subcategory": "dining-entertaining/drinkware-glassware",
        },
        "home-holiday-christmas-christmas-ornaments-tree-decorations": {
            "url": "https://www.saksfifthavenue.com/c/home/holiday-christmas/christmas-ornaments-tree-decorations",
            "label": "Ornaments",
            "subcategory": "holiday-christmas/christmas-ornaments-tree-decorations",
        },
        "home-holiday-christmas-holiday-decor": {
            "url": "https://www.saksfifthavenue.com/c/home/holiday-christmas/holiday-decor",
            "label": "Holiday Decor",
            "subcategory": "holiday-christmas/holiday-decor",
        },
        "home-holiday-christmas-holiday-dining-entertaining": {
            "url": "https://www.saksfifthavenue.com/c/home/holiday-christmas/holiday-dining-entertaining",
            "label": "Holiday Dining & Entertaining",
            "subcategory": "holiday-christmas/holiday-dining-entertaining",
        },
        "home-holiday-christmas-holiday-gourmet-food-candy": {
            "url": "https://www.saksfifthavenue.com/c/home/holiday-christmas/holiday-gourmet-food-candy",
            "label": "Gourmet Food & Candy",
            "subcategory": "holiday-christmas/holiday-gourmet-food-candy",
        },
        "home-home-decor-candles-diffusers": {
            "url": "https://www.saksfifthavenue.com/c/home/home-decor/candles-diffusers",
            "label": "Candles & Diffusers",
            "subcategory": "home-decor/candles-diffusers",
        },
        "home-home-decor-picture-frames": {
            "url": "https://www.saksfifthavenue.com/c/home/home-decor/picture-frames",
            "label": "Picture Frames",
            "subcategory": "home-decor/picture-frames",
        },
        "home-holiday-christmas-holiday-decor-wreaths-garlands-ribbons": {
            "url": "https://www.saksfifthavenue.com/c/home/holiday-christmas/holiday-decor/wreaths--garlands-ribbons",
            "label": "Wreaths & Garlands",
            "subcategory": "holiday-christmas/holiday-decor/wreaths--garlands-ribbons",
        },
    },
    "Gifts": {
        "gifts-gifting": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting",
            "label": "Holiday Gifts",
            "subcategory": "gifting",
        },
        "gifts-gifting-beauty-gifts": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting/beauty-gifts",
            "label": "Beauty Gifts",
            "subcategory": "gifting/beauty-gifts",
        },
        "gifts-gifting-best-selling-gifts": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting/best-selling-gifts",
            "label": "Best Selling Gifts",
            "subcategory": "gifting/best-selling-gifts",
        },
        "gifts-gifting-gifts-for-her": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting/gifts-for-her",
            "label": "Gifts for Her",
            "subcategory": "gifting/gifts-for-her",
        },
        "gifts-gifting-gifts-for-him": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting/gifts-for-him",
            "label": "Gifts for Him",
            "subcategory": "gifting/gifts-for-him",
        },
        "gifts-gifting-gifts-under-200": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting/gifts-under--200",
            "label": "Gifts Under $200",
            "subcategory": "gifting/gifts-under--200",
        },
        "gifts-gifting-stocking-stuffers": {
            "url": "https://www.saksfifthavenue.com/c/gifts/gifting/stocking-stuffers",
            "label": "Stocking Stuffers",
            "subcategory": "gifting/stocking-stuffers",
        },
        "gifts-our-favorite-gifts-baby-shower-gifts": {
            "url": "https://www.saksfifthavenue.com/c/gifts/our-favorite-gifts/baby-shower-gifts",
            "label": "Baby Shower Gifts",
            "subcategory": "our-favorite-gifts/baby-shower-gifts",
        },
        "gifts-our-favorite-gifts-wedding-gifts": {
            "url": "https://www.saksfifthavenue.com/c/gifts/our-favorite-gifts/wedding-gifts",
            "label": "Wedding Gifts",
            "subcategory": "our-favorite-gifts/wedding-gifts",
        },
    },
    "Wedding Shop": {
        "the-wedding-shop": {
            "url": "https://www.saksfifthavenue.com/c/the-wedding-shop",
            "label": "Wedding",
            "subcategory": "the-wedding-shop",
        },
        "the-wedding-shop-bride-attire": {
            "url": "https://www.saksfifthavenue.com/c/the-wedding-shop/bride-attire",
            "label": "Bride Attire",
            "subcategory": "bride-attire",
        },
        "the-wedding-shop-bride-attire-bridal-dresses": {
            "url": "https://www.saksfifthavenue.com/c/the-wedding-shop/bride-attire/bridal-dresses",
            "label": "Bride Attire",
            "subcategory": "bride-attire/bridal-dresses",
        },
        "the-wedding-shop-bride-attire-bridal-shoes": {
            "url": "https://www.saksfifthavenue.com/c/the-wedding-shop/bride-attire/bridal-shoes",
            "label": "Bridal Shoes",
            "subcategory": "bride-attire/bridal-shoes",
        },
        "the-wedding-shop-wedding-guest-attire-men-s-wedding-guest-attire": {
            "url": "https://www.saksfifthavenue.com/c/the-wedding-shop/wedding-guest-attire/men-s-wedding-guest-attire",
            "label": "Wedding Guest",
            "subcategory": "wedding-guest-attire/men-s-wedding-guest-attire",
        },
        "the-wedding-shop-wedding-guest-attire-women-s-wedding-guest-attire": {
            "url": "https://www.saksfifthavenue.com/c/the-wedding-shop/wedding-guest-attire/women-s-wedding-guest-attire",
            "label": "Wedding Guest",
            "subcategory": "wedding-guest-attire/women-s-wedding-guest-attire",
        },
    },
    "Sale": {
        "sale-2-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/sale",
            "label": "Sale",
            "subcategory": "sale",
        },
        "sale-2-akris-punto-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/akris-punto/sale",
            "label": "Akris punto",
            "subcategory": "akris-punto/sale",
        },
        "sale-2-alice-olivia-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/alice-olivia/sale",
            "label": "ALICE + OLIVIA",
            "subcategory": "alice-olivia/sale",
        },
        "sale-2-cinq-c3-a0-sept-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/cinq-%C3%A0-sept/sale",
            "label": "Cinq à Sept",
            "subcategory": "cinq-%C3%A0-sept/sale",
        },
        "sale-2-favorite-daughter-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/favorite-daughter/sale",
            "label": "Favorite Daughter",
            "subcategory": "favorite-daughter/sale",
        },
        "sale-2-frame-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/frame/sale",
            "label": "FRAME",
            "subcategory": "frame/sale",
        },
        "sale-2-l-agence-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/l-agence/sale",
            "label": "L'AGENCE",
            "subcategory": "l-agence/sale",
        },
        "sale-2-milly-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/milly/sale",
            "label": "Milly",
            "subcategory": "milly/sale",
        },
        "sale-2-rag-bone-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/rag-bone/sale",
            "label": "rag & bone",
            "subcategory": "rag-bone/sale",
        },
        "sale-2-ramy-brook-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/ramy-brook/sale",
            "label": "Ramy Brook",
            "subcategory": "ramy-brook/sale",
        },
        "sale-2-simkhai-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/simkhai/sale",
            "label": "SIMKHAI",
            "subcategory": "simkhai/sale",
        },
        "sale-2-staud-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/staud/sale",
            "label": "STAUD",
            "subcategory": "staud/sale",
        },
        "sale-2-stuart-weitzman-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/stuart-weitzman/sale",
            "label": "Stuart Weitzman",
            "subcategory": "stuart-weitzman/sale",
        },
        "sale-2-valentino-garavani-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/valentino-garavani/sale",
            "label": "Valentino Garavani",
            "subcategory": "valentino-garavani/sale",
        },
        "sale-2-veronica-beard-sale": {
            "url": "https://www.saksfifthavenue.com/c/sale-2/veronica-beard/sale",
            "label": "Veronica Beard",
            "subcategory": "veronica-beard/sale",
        },
    },
}
