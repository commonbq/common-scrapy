"""Current crawlable Sephora US categories, grouped by storefront department.

The leaf key is the canonical ``/shop/<slug>`` route segment; the spider passes
it to the catalogue API as ``/api/v2/catalog/categories/<slug>/seo``.
Captured from the live Sephora mega-navigation on the US homepage
(verified 2026-10-14); every slug is globally unique across departments, so the
bare leaf name is a safe Airflow task / GCS output path (see listing_dag_factory).
"""

SEPHORA_CATEGORIES = {
    'Makeup': {
        'makeup-cosmetics': {
            "url": "https://www.sephora.com/shop/makeup-cosmetics",
            "slug": 'makeup-cosmetics',
            "label": 'Makeup',
        },
        'face-makeup': {
            "url": "https://www.sephora.com/shop/face-makeup",
            "slug": 'face-makeup',
            "label": 'Face',
        },
        'foundation-makeup': {
            "url": "https://www.sephora.com/shop/foundation-makeup",
            "slug": 'foundation-makeup',
            "label": 'Foundation',
        },
        'bb-cc-cream-face-makeup': {
            "url": "https://www.sephora.com/shop/bb-cc-cream-face-makeup",
            "slug": 'bb-cc-cream-face-makeup',
            "label": 'BB & CC Cream',
        },
        'tinted-moisturizer': {
            "url": "https://www.sephora.com/shop/tinted-moisturizer",
            "slug": 'tinted-moisturizer',
            "label": 'Tinted Moisturizer',
        },
        'concealer': {
            "url": "https://www.sephora.com/shop/concealer",
            "slug": 'concealer',
            "label": 'Concealer',
        },
        'makeup-primer-face-primer': {
            "url": "https://www.sephora.com/shop/makeup-primer-face-primer",
            "slug": 'makeup-primer-face-primer',
            "label": 'Face Primer',
        },
        'setting-powder-face-powder': {
            "url": "https://www.sephora.com/shop/setting-powder-face-powder",
            "slug": 'setting-powder-face-powder',
            "label": 'Setting Spray & Powder',
        },
        'luminizer-luminous-makeup': {
            "url": "https://www.sephora.com/shop/luminizer-luminous-makeup",
            "slug": 'luminizer-luminous-makeup',
            "label": 'Highlighter',
        },
        'contour-palette-brush': {
            "url": "https://www.sephora.com/shop/contour-palette-brush",
            "slug": 'contour-palette-brush',
            "label": 'Contour',
        },
        'color-correcting': {
            "url": "https://www.sephora.com/shop/color-correcting",
            "slug": 'color-correcting',
            "label": 'Color Correct',
        },
        'complexion-sets': {
            "url": "https://www.sephora.com/shop/complexion-sets",
            "slug": 'complexion-sets',
            "label": 'Face Sets',
        },
        'eye-makeup': {
            "url": "https://www.sephora.com/shop/eye-makeup",
            "slug": 'eye-makeup',
            "label": 'Eye',
        },
        'eyeshadow-palettes': {
            "url": "https://www.sephora.com/shop/eyeshadow-palettes",
            "slug": 'eyeshadow-palettes',
            "label": 'Eye Palettes',
        },
        'mascara': {
            "url": "https://www.sephora.com/shop/mascara",
            "slug": 'mascara',
            "label": 'Mascara',
        },
        'eyeliner': {
            "url": "https://www.sephora.com/shop/eyeliner",
            "slug": 'eyeliner',
            "label": 'Eyeliner',
        },
        'eyebrow-makeup-pencils': {
            "url": "https://www.sephora.com/shop/eyebrow-makeup-pencils",
            "slug": 'eyebrow-makeup-pencils',
            "label": 'Eyebrow',
        },
        'fake-eyelashes-false-eyelashes': {
            "url": "https://www.sephora.com/shop/fake-eyelashes-false-eyelashes",
            "slug": 'fake-eyelashes-false-eyelashes',
            "label": 'False Eyelashes',
        },
        'eyeshadow': {
            "url": "https://www.sephora.com/shop/eyeshadow",
            "slug": 'eyeshadow',
            "label": 'Eyeshadow',
        },
        'eyeshadow-primer-eye-primer': {
            "url": "https://www.sephora.com/shop/eyeshadow-primer-eye-primer",
            "slug": 'eyeshadow-primer-eye-primer',
            "label": 'Eye Primer',
        },
        'eye-sets': {
            "url": "https://www.sephora.com/shop/eye-sets",
            "slug": 'eye-sets',
            "label": 'Eye Sets',
        },
        'lips-makeup': {
            "url": "https://www.sephora.com/shop/lips-makeup",
            "slug": 'lips-makeup',
            "label": 'Lip',
        },
        'lip-gloss': {
            "url": "https://www.sephora.com/shop/lip-gloss",
            "slug": 'lip-gloss',
            "label": 'Lip Gloss',
        },
        'lipstick': {
            "url": "https://www.sephora.com/shop/lipstick",
            "slug": 'lipstick',
            "label": 'Lipstick',
        },
        'lip-oil': {
            "url": "https://www.sephora.com/shop/lip-oil",
            "slug": 'lip-oil',
            "label": 'Lip Oil',
        },
        'lip-plumper': {
            "url": "https://www.sephora.com/shop/lip-plumper",
            "slug": 'lip-plumper',
            "label": 'Lip Plumper',
        },
        'lip-balm-treatments-lips-makeup': {
            "url": "https://www.sephora.com/shop/lip-balm-treatments-lips-makeup",
            "slug": 'lip-balm-treatments-lips-makeup',
            "label": 'Lip Balms & Treatments',
        },
        'liquid-lipstick': {
            "url": "https://www.sephora.com/shop/liquid-lipstick",
            "slug": 'liquid-lipstick',
            "label": 'Liquid Lipstick',
        },
        'lip-liner-lip-pencils': {
            "url": "https://www.sephora.com/shop/lip-liner-lip-pencils",
            "slug": 'lip-liner-lip-pencils',
            "label": 'Lip Liner',
        },
        'lip-stain': {
            "url": "https://www.sephora.com/shop/lip-stain",
            "slug": 'lip-stain',
            "label": 'Lip Stain',
        },
        'lip-palettes-gloss-sets': {
            "url": "https://www.sephora.com/shop/lip-palettes-gloss-sets",
            "slug": 'lip-palettes-gloss-sets',
            "label": 'Lip Sets',
        },
        'cheek-makeup': {
            "url": "https://www.sephora.com/shop/cheek-makeup",
            "slug": 'cheek-makeup',
            "label": 'Cheek',
        },
        'blush': {
            "url": "https://www.sephora.com/shop/blush",
            "slug": 'blush',
            "label": 'Blush',
        },
        'bronzer-makeup': {
            "url": "https://www.sephora.com/shop/bronzer-makeup",
            "slug": 'bronzer-makeup',
            "label": 'Bronzer',
        },
        'cheek-palettes': {
            "url": "https://www.sephora.com/shop/cheek-palettes",
            "slug": 'cheek-palettes',
            "label": 'Cheek Palettes',
        },
        'makeup-kits-makeup-sets': {
            "url": "https://www.sephora.com/shop/makeup-kits-makeup-sets",
            "slug": 'makeup-kits-makeup-sets',
            "label": 'Value & Gift Sets',
        },
        'makeup-palettes': {
            "url": "https://www.sephora.com/shop/makeup-palettes",
            "slug": 'makeup-palettes',
            "label": 'Makeup Palettes',
        },
        'pedicure-tools-manicure-tools': {
            "url": "https://www.sephora.com/shop/pedicure-tools-manicure-tools",
            "slug": 'pedicure-tools-manicure-tools',
            "label": 'Nail',
        },
        'makeup-brushes': {
            "url": "https://www.sephora.com/shop/makeup-brushes",
            "slug": 'makeup-brushes',
            "label": 'Brushes & Applicators',
        },
        'makeup-brush-sets': {
            "url": "https://www.sephora.com/shop/makeup-brush-sets",
            "slug": 'makeup-brush-sets',
            "label": 'Brush Sets',
        },
        'foundation-brushes-face-brushes': {
            "url": "https://www.sephora.com/shop/foundation-brushes-face-brushes",
            "slug": 'foundation-brushes-face-brushes',
            "label": 'Face Brushes',
        },
        'makeup-sponges': {
            "url": "https://www.sephora.com/shop/makeup-sponges",
            "slug": 'makeup-sponges',
            "label": 'Sponges & Applicators',
        },
        'eyeliner-brushes-eyeshadow-brushes': {
            "url": "https://www.sephora.com/shop/eyeliner-brushes-eyeshadow-brushes",
            "slug": 'eyeliner-brushes-eyeshadow-brushes',
            "label": 'Eye Brushes',
        },
        'lip-brushes-lipstick-brushes': {
            "url": "https://www.sephora.com/shop/lip-brushes-lipstick-brushes",
            "slug": 'lip-brushes-lipstick-brushes',
            "label": 'Lip Brushes',
        },
        'makeup-brush-cleaner': {
            "url": "https://www.sephora.com/shop/makeup-brush-cleaner",
            "slug": 'makeup-brush-cleaner',
            "label": 'Brush Cleaners',
        },
        'makeup-tools': {
            "url": "https://www.sephora.com/shop/makeup-tools",
            "slug": 'makeup-tools',
            "label": 'Accessories',
        },
        'eyelash-curlers': {
            "url": "https://www.sephora.com/shop/eyelash-curlers",
            "slug": 'eyelash-curlers',
            "label": 'Eyelash Curlers',
        },
        'makeup-pencil-sharpeners': {
            "url": "https://www.sephora.com/shop/makeup-pencil-sharpeners",
            "slug": 'makeup-pencil-sharpeners',
            "label": 'Sharpeners',
        },
        'tweezers-eyebrow-shapers': {
            "url": "https://www.sephora.com/shop/tweezers-eyebrow-shapers",
            "slug": 'tweezers-eyebrow-shapers',
            "label": 'Tweezers & Eyebrow Tools',
        },
        'makeup-bags-cosmetic-bags': {
            "url": "https://www.sephora.com/shop/makeup-bags-cosmetic-bags",
            "slug": 'makeup-bags-cosmetic-bags',
            "label": 'Makeup & Travel Cases',
        },
        'clean-makeup': {
            "url": "https://www.sephora.com/shop/clean-makeup",
            "slug": 'clean-makeup',
            "label": 'Clean Makeup',
        },
        'vegan-makeup': {
            "url": "https://www.sephora.com/shop/vegan-makeup",
            "slug": 'vegan-makeup',
            "label": 'Vegan Makeup',
        },
        'mini-makeup': {
            "url": "https://www.sephora.com/shop/mini-makeup",
            "slug": 'mini-makeup',
            "label": 'Mini Size',
        },
        'luxury-makeup': {
            "url": "https://www.sephora.com/shop/luxury-makeup",
            "slug": 'luxury-makeup',
            "label": 'Luxury Makeup',
        },
        'korean-makeup-products': {
            "url": "https://www.sephora.com/shop/korean-makeup-products",
            "slug": 'korean-makeup-products',
            "label": 'Korean Makeup',
        },
    },
    'Skincare': {
        'skincare': {
            "url": "https://www.sephora.com/shop/skincare",
            "slug": 'skincare',
            "label": 'Skincare',
        },
        'moisturizing-cream-oils-mists': {
            "url": "https://www.sephora.com/shop/moisturizing-cream-oils-mists",
            "slug": 'moisturizing-cream-oils-mists',
            "label": 'Moisturizers',
        },
        'face-creams': {
            "url": "https://www.sephora.com/shop/face-creams",
            "slug": 'face-creams',
            "label": 'Face Creams',
        },
        'night-cream': {
            "url": "https://www.sephora.com/shop/night-cream",
            "slug": 'night-cream',
            "label": 'Night Creams',
        },
        'cleansing-oil-face-oil': {
            "url": "https://www.sephora.com/shop/cleansing-oil-face-oil",
            "slug": 'cleansing-oil-face-oil',
            "label": 'Face Oils',
        },
        'face-mist-face-spray': {
            "url": "https://www.sephora.com/shop/face-mist-face-spray",
            "slug": 'face-mist-face-spray',
            "label": 'Mists & Essences',
        },
        'bb-cream-cc-cream': {
            "url": "https://www.sephora.com/shop/bb-cream-cc-cream",
            "slug": 'bb-cream-cc-cream',
            "label": 'BB & CC Cream',
        },
        'cleanser': {
            "url": "https://www.sephora.com/shop/cleanser",
            "slug": 'cleanser',
            "label": 'Cleansers',
        },
        'face-wash-facial-cleanser': {
            "url": "https://www.sephora.com/shop/face-wash-facial-cleanser",
            "slug": 'face-wash-facial-cleanser',
            "label": 'Face Wash & Cleansers',
        },
        'exfoliating-scrub-exfoliator': {
            "url": "https://www.sephora.com/shop/exfoliating-scrub-exfoliator",
            "slug": 'exfoliating-scrub-exfoliator',
            "label": 'Exfoliators',
        },
        'makeup-remover-skincare': {
            "url": "https://www.sephora.com/shop/makeup-remover-skincare",
            "slug": 'makeup-remover-skincare',
            "label": 'Makeup Removers',
        },
        'face-wipes': {
            "url": "https://www.sephora.com/shop/face-wipes",
            "slug": 'face-wipes',
            "label": 'Face Wipes',
        },
        'facial-toner-skin-toner': {
            "url": "https://www.sephora.com/shop/facial-toner-skin-toner",
            "slug": 'facial-toner-skin-toner',
            "label": 'Toners',
        },
        'facial-treatments': {
            "url": "https://www.sephora.com/shop/facial-treatments",
            "slug": 'facial-treatments',
            "label": 'Treatments',
        },
        'face-serum': {
            "url": "https://www.sephora.com/shop/face-serum",
            "slug": 'face-serum',
            "label": 'Face Serums',
        },
        'acne-products-acne-cream': {
            "url": "https://www.sephora.com/shop/acne-products-acne-cream",
            "slug": 'acne-products-acne-cream',
            "label": 'Acne & Blemish Treatments',
        },
        'facial-peels': {
            "url": "https://www.sephora.com/shop/facial-peels",
            "slug": 'facial-peels',
            "label": 'Facial Peels',
        },
        'face-mask': {
            "url": "https://www.sephora.com/shop/face-mask",
            "slug": 'face-mask',
            "label": 'Masks',
        },
        'facial-treatment-masks': {
            "url": "https://www.sephora.com/shop/facial-treatment-masks",
            "slug": 'facial-treatment-masks',
            "label": 'Face Masks',
        },
        'sheet-masks': {
            "url": "https://www.sephora.com/shop/sheet-masks",
            "slug": 'sheet-masks',
            "label": 'Sheet Masks',
        },
        'eye-mask': {
            "url": "https://www.sephora.com/shop/eye-mask",
            "slug": 'eye-mask',
            "label": 'Eye Masks',
        },
        'eye-treatment-dark-circle-treatment': {
            "url": "https://www.sephora.com/shop/eye-treatment-dark-circle-treatment",
            "slug": 'eye-treatment-dark-circle-treatment',
            "label": 'Eye Care',
        },
        'eye-cream-dark-circles': {
            "url": "https://www.sephora.com/shop/eye-cream-dark-circles",
            "slug": 'eye-cream-dark-circles',
            "label": 'Eye Creams & Treatments',
        },
        'lip-balm-lip-care': {
            "url": "https://www.sephora.com/shop/lip-balm-lip-care",
            "slug": 'lip-balm-lip-care',
            "label": 'Lip Balms & Treatments',
        },
        'sunscreen-sun-protection': {
            "url": "https://www.sephora.com/shop/sunscreen-sun-protection",
            "slug": 'sunscreen-sun-protection',
            "label": 'Sunscreen',
        },
        'face-sunscreen': {
            "url": "https://www.sephora.com/shop/face-sunscreen",
            "slug": 'face-sunscreen',
            "label": 'Face Sunscreen',
        },
        'sunscreen': {
            "url": "https://www.sephora.com/shop/sunscreen",
            "slug": 'sunscreen',
            "label": 'Body Sunscreen',
        },
        'skin-care-sets-travel-value': {
            "url": "https://www.sephora.com/shop/skin-care-sets-travel-value",
            "slug": 'skin-care-sets-travel-value',
            "label": 'Value & Gift Sets',
        },
        'skin-care-tools': {
            "url": "https://www.sephora.com/shop/skin-care-tools",
            "slug": 'skin-care-tools',
            "label": 'High Tech Tools',
        },
        'anti-aging-tools': {
            "url": "https://www.sephora.com/shop/anti-aging-tools",
            "slug": 'anti-aging-tools',
            "label": 'Anti-Aging',
        },
        'mens-facial-products': {
            "url": "https://www.sephora.com/shop/mens-facial-products",
            "slug": 'mens-facial-products',
            "label": "Men's Grooming",
        },
        'wellness-skincare': {
            "url": "https://www.sephora.com/shop/wellness-skincare",
            "slug": 'wellness-skincare',
            "label": 'Wellness',
        },
        'vitamins-for-hair-skin-nails': {
            "url": "https://www.sephora.com/shop/vitamins-for-hair-skin-nails",
            "slug": 'vitamins-for-hair-skin-nails',
            "label": 'Supplements',
        },
        'feminine-care': {
            "url": "https://www.sephora.com/shop/feminine-care",
            "slug": 'feminine-care',
            "label": 'Feminine Care',
        },
        'oral-care': {
            "url": "https://www.sephora.com/shop/oral-care",
            "slug": 'oral-care',
            "label": 'Oral Care',
        },
        'acne-treatment-blemish-remover': {
            "url": "https://www.sephora.com/shop/acne-treatment-blemish-remover",
            "slug": 'acne-treatment-blemish-remover',
            "label": 'Acne & Blemishes',
        },
        'anti-aging-skin-care': {
            "url": "https://www.sephora.com/shop/anti-aging-skin-care",
            "slug": 'anti-aging-skin-care',
            "label": 'Anti-Aging',
        },
        'dark-spot-remover': {
            "url": "https://www.sephora.com/shop/dark-spot-remover",
            "slug": 'dark-spot-remover',
            "label": 'Dark Spots',
        },
        'pore-minimizing-products': {
            "url": "https://www.sephora.com/shop/pore-minimizing-products",
            "slug": 'pore-minimizing-products',
            "label": 'Pores',
        },
        'dry-skin-treatment': {
            "url": "https://www.sephora.com/shop/dry-skin-treatment",
            "slug": 'dry-skin-treatment',
            "label": 'Dryness',
        },
        'wrinkle-cream-wrinkle-remover': {
            "url": "https://www.sephora.com/shop/wrinkle-cream-wrinkle-remover",
            "slug": 'wrinkle-cream-wrinkle-remover',
            "label": 'Fine Lines & Wrinkles',
        },
        'skin-brighteners-dull-skin-treatments': {
            "url": "https://www.sephora.com/shop/skin-brighteners-dull-skin-treatments",
            "slug": 'skin-brighteners-dull-skin-treatments',
            "label": 'Dullness',
        },
        'clean-skin-care': {
            "url": "https://www.sephora.com/shop/clean-skin-care",
            "slug": 'clean-skin-care',
            "label": 'Clean Skincare',
        },
        'vegan-skin-care': {
            "url": "https://www.sephora.com/shop/vegan-skin-care",
            "slug": 'vegan-skin-care',
            "label": 'Vegan Skincare',
        },
        'mini-skincare': {
            "url": "https://www.sephora.com/shop/mini-skincare",
            "slug": 'mini-skincare',
            "label": 'Mini Size',
        },
        'fsa-eligible-products': {
            "url": "https://www.sephora.com/shop/fsa-eligible-products",
            "slug": 'fsa-eligible-products',
            "label": 'FSA & HSA Eligible',
        },
        'luxury-skincare': {
            "url": "https://www.sephora.com/shop/luxury-skincare",
            "slug": 'luxury-skincare',
            "label": 'Luxury Skincare',
        },
        'korean-skincare-products': {
            "url": "https://www.sephora.com/shop/korean-skincare-products",
            "slug": 'korean-skincare-products',
            "label": 'Korean Skincare',
        },
    },
    'Fragrance': {
        'fragrance': {
            "url": "https://www.sephora.com/shop/fragrance",
            "slug": 'fragrance',
            "label": 'Fragrance',
        },
        'fragrances-for-women': {
            "url": "https://www.sephora.com/shop/fragrances-for-women",
            "slug": 'fragrances-for-women',
            "label": 'Women',
        },
        'perfume': {
            "url": "https://www.sephora.com/shop/perfume",
            "slug": 'perfume',
            "label": 'Perfume',
        },
        'rollerball-perfume-roll-on-perfume': {
            "url": "https://www.sephora.com/shop/rollerball-perfume-roll-on-perfume",
            "slug": 'rollerball-perfume-roll-on-perfume',
            "label": 'Rollerballs & Travel Size',
        },
        'body-mist-hair-mist': {
            "url": "https://www.sephora.com/shop/body-mist-hair-mist",
            "slug": 'body-mist-hair-mist',
            "label": 'Body Mist & Hair Mist',
        },
        'fragrances-for-men': {
            "url": "https://www.sephora.com/shop/fragrances-for-men",
            "slug": 'fragrances-for-men',
            "label": 'Men',
        },
        'cologne': {
            "url": "https://www.sephora.com/shop/cologne",
            "slug": 'cologne',
            "label": 'Cologne',
        },
        'travel-size-mini-cologne': {
            "url": "https://www.sephora.com/shop/travel-size-mini-cologne",
            "slug": 'travel-size-mini-cologne',
            "label": 'Travel Size & Mini Cologne',
        },
        'unisex-perfume-cologne': {
            "url": "https://www.sephora.com/shop/unisex-perfume-cologne",
            "slug": 'unisex-perfume-cologne',
            "label": 'Unisex / Genderless',
        },
        'fragrance-value-sets-gifts': {
            "url": "https://www.sephora.com/shop/fragrance-value-sets-gifts",
            "slug": 'fragrance-value-sets-gifts',
            "label": 'Value & Gift Sets',
        },
        'perfume-gift-sets': {
            "url": "https://www.sephora.com/shop/perfume-gift-sets",
            "slug": 'perfume-gift-sets',
            "label": 'Perfume Gift Sets',
        },
        'cologne-gift-sets': {
            "url": "https://www.sephora.com/shop/cologne-gift-sets",
            "slug": 'cologne-gift-sets',
            "label": 'Cologne Gift Sets',
        },
        'home-fragrance-candle-gift-sets': {
            "url": "https://www.sephora.com/shop/home-fragrance-candle-gift-sets",
            "slug": 'home-fragrance-candle-gift-sets',
            "label": 'Home Gift Sets',
        },
        'home-fragrance': {
            "url": "https://www.sephora.com/shop/home-fragrance",
            "slug": 'home-fragrance',
            "label": 'Candles & Home Scents',
        },
        'candles': {
            "url": "https://www.sephora.com/shop/candles",
            "slug": 'candles',
            "label": 'Candles',
        },
        'diffusers': {
            "url": "https://www.sephora.com/shop/diffusers",
            "slug": 'diffusers',
            "label": 'Diffusers',
        },
        'floral-fragrances': {
            "url": "https://www.sephora.com/shop/floral-fragrances",
            "slug": 'floral-fragrances',
            "label": 'Floral',
        },
        'spicy-warm-fragrances': {
            "url": "https://www.sephora.com/shop/spicy-warm-fragrances",
            "slug": 'spicy-warm-fragrances',
            "label": 'Warm & Spicy',
        },
        'fresh-fragrances': {
            "url": "https://www.sephora.com/shop/fresh-fragrances",
            "slug": 'fresh-fragrances',
            "label": 'Fresh',
        },
        'woody-earthy-fragrances': {
            "url": "https://www.sephora.com/shop/woody-earthy-fragrances",
            "slug": 'woody-earthy-fragrances',
            "label": 'Earthy & Woody',
        },
        'clean-fragrance': {
            "url": "https://www.sephora.com/shop/clean-fragrance",
            "slug": 'clean-fragrance',
            "label": 'Clean Fragrance',
        },
        'vegan-fragrance': {
            "url": "https://www.sephora.com/shop/vegan-fragrance",
            "slug": 'vegan-fragrance',
            "label": 'Vegan Fragrance',
        },
        'mini-perfume': {
            "url": "https://www.sephora.com/shop/mini-perfume",
            "slug": 'mini-perfume',
            "label": 'Mini Size',
        },
        'luxury-fragrance': {
            "url": "https://www.sephora.com/shop/luxury-fragrance",
            "slug": 'luxury-fragrance',
            "label": 'Luxury Fragrance',
        },
    },
    'Hair': {
        'hair-products': {
            "url": "https://www.sephora.com/shop/hair-products",
            "slug": 'hair-products',
            "label": 'Hair',
        },
        'shampoo-conditioner': {
            "url": "https://www.sephora.com/shop/shampoo-conditioner",
            "slug": 'shampoo-conditioner',
            "label": 'Shampoo & Conditioner',
        },
        'shampoo-sulfate-free-shampoo': {
            "url": "https://www.sephora.com/shop/shampoo-sulfate-free-shampoo",
            "slug": 'shampoo-sulfate-free-shampoo',
            "label": 'Shampoo',
        },
        'conditioner-hair': {
            "url": "https://www.sephora.com/shop/conditioner-hair",
            "slug": 'conditioner-hair',
            "label": 'Conditioner',
        },
        'hair-products-treatments': {
            "url": "https://www.sephora.com/shop/hair-products-treatments",
            "slug": 'hair-products-treatments',
            "label": 'Treatments',
        },
        'hair-masks': {
            "url": "https://www.sephora.com/shop/hair-masks",
            "slug": 'hair-masks',
            "label": 'Hair Masks',
        },
        'leave-in-conditioner': {
            "url": "https://www.sephora.com/shop/leave-in-conditioner",
            "slug": 'leave-in-conditioner',
            "label": 'Leave-in Conditioner',
        },
        'hair-oil-treatment': {
            "url": "https://www.sephora.com/shop/hair-oil-treatment",
            "slug": 'hair-oil-treatment',
            "label": 'Hair Oil',
        },
        'hair-styling-products': {
            "url": "https://www.sephora.com/shop/hair-styling-products",
            "slug": 'hair-styling-products',
            "label": 'Hair Serums',
        },
        'hair-treatment-dry-scalp-treatment': {
            "url": "https://www.sephora.com/shop/hair-treatment-dry-scalp-treatment",
            "slug": 'hair-treatment-dry-scalp-treatment',
            "label": 'Scalp Treatments',
        },
        'hair-supplements': {
            "url": "https://www.sephora.com/shop/hair-supplements",
            "slug": 'hair-supplements',
            "label": 'Hair Supplements',
        },
        'thinning-hair-loss': {
            "url": "https://www.sephora.com/shop/thinning-hair-loss",
            "slug": 'thinning-hair-loss',
            "label": 'Hair Thinning & Hair Loss',
        },
        'dry-shampoo': {
            "url": "https://www.sephora.com/shop/dry-shampoo",
            "slug": 'dry-shampoo',
            "label": 'Dry Shampoo',
        },
        'hair-primers': {
            "url": "https://www.sephora.com/shop/hair-primers",
            "slug": 'hair-primers',
            "label": 'Hair Primers & Heat Protectants',
        },
        'hair-spray': {
            "url": "https://www.sephora.com/shop/hair-spray",
            "slug": 'hair-spray',
            "label": 'Hair Spray',
        },
        'hair-clips-hair-bands': {
            "url": "https://www.sephora.com/shop/hair-clips-hair-bands",
            "slug": 'hair-clips-hair-bands',
            "label": 'Accessories',
        },
        'hair-clips-claw-clips': {
            "url": "https://www.sephora.com/shop/hair-clips-claw-clips",
            "slug": 'hair-clips-claw-clips',
            "label": 'Hair Clips & Claw Clips',
        },
        'scrunchies-hair-ties': {
            "url": "https://www.sephora.com/shop/scrunchies-hair-ties",
            "slug": 'scrunchies-hair-ties',
            "label": 'Scrunchies & Hair Ties',
        },
        'hair-towels': {
            "url": "https://www.sephora.com/shop/hair-towels",
            "slug": 'hair-towels',
            "label": 'Hair Towels',
        },
        'scalp-massagers-rollers': {
            "url": "https://www.sephora.com/shop/scalp-massagers-rollers",
            "slug": 'scalp-massagers-rollers',
            "label": 'Scalp Massagers & Rollers',
        },
        'showerheads-filters': {
            "url": "https://www.sephora.com/shop/showerheads-filters",
            "slug": 'showerheads-filters',
            "label": 'Showerheads & Filters',
        },
        'hair-care-sets': {
            "url": "https://www.sephora.com/shop/hair-care-sets",
            "slug": 'hair-care-sets',
            "label": 'Value & Gift Sets',
        },
        'hair-styling-tools': {
            "url": "https://www.sephora.com/shop/hair-styling-tools",
            "slug": 'hair-styling-tools',
            "label": 'Hair Styling Tools',
        },
        'hair-dryers-blow-dryers': {
            "url": "https://www.sephora.com/shop/hair-dryers-blow-dryers",
            "slug": 'hair-dryers-blow-dryers',
            "label": 'Hair Dryers',
        },
        'hair-straightener-curling-iron-flat-iron': {
            "url": "https://www.sephora.com/shop/hair-straightener-curling-iron-flat-iron",
            "slug": 'hair-straightener-curling-iron-flat-iron',
            "label": 'Hair Straighteners & Flat Irons',
        },
        'blow-dry-brush': {
            "url": "https://www.sephora.com/shop/blow-dry-brush",
            "slug": 'blow-dry-brush',
            "label": 'Blow Dry Brushes',
        },
        'curling-wands-curling-irons': {
            "url": "https://www.sephora.com/shop/curling-wands-curling-irons",
            "slug": 'curling-wands-curling-irons',
            "label": 'Curling Irons',
        },
        'hair-tool-attachments-diffusers': {
            "url": "https://www.sephora.com/shop/hair-tool-attachments-diffusers",
            "slug": 'hair-tool-attachments-diffusers',
            "label": 'Hair Tool Attachments & Diffusers',
        },
        'hair-brushes': {
            "url": "https://www.sephora.com/shop/hair-brushes",
            "slug": 'hair-brushes',
            "label": 'Brushes & Combs',
        },
        'curly-hair-products': {
            "url": "https://www.sephora.com/shop/curly-hair-products",
            "slug": 'curly-hair-products',
            "label": 'Curly, Coily, Textured Hair Care',
        },
        'damaged-hair-treatment': {
            "url": "https://www.sephora.com/shop/damaged-hair-treatment",
            "slug": 'damaged-hair-treatment',
            "label": 'Damaged Hair',
        },
        'dry-hair-treatments': {
            "url": "https://www.sephora.com/shop/dry-hair-treatments",
            "slug": 'dry-hair-treatments',
            "label": 'Dryness',
        },
        'best-anti-frizz-products': {
            "url": "https://www.sephora.com/shop/best-anti-frizz-products",
            "slug": 'best-anti-frizz-products',
            "label": 'Frizz',
        },
        'best-volumizing-shampoo-hair-products': {
            "url": "https://www.sephora.com/shop/best-volumizing-shampoo-hair-products",
            "slug": 'best-volumizing-shampoo-hair-products',
            "label": 'Volume',
        },
        'hair-color-treatment': {
            "url": "https://www.sephora.com/shop/hair-color-treatment",
            "slug": 'hair-color-treatment',
            "label": 'Color Care',
        },
        'clean-hair-care': {
            "url": "https://www.sephora.com/shop/clean-hair-care",
            "slug": 'clean-hair-care',
            "label": 'Clean Hair Care',
        },
        'vegan-hair-care': {
            "url": "https://www.sephora.com/shop/vegan-hair-care",
            "slug": 'vegan-hair-care',
            "label": 'Vegan Hair Care',
        },
        'mini-hair-products': {
            "url": "https://www.sephora.com/shop/mini-hair-products",
            "slug": 'mini-hair-products',
            "label": 'Mini Size',
        },
        'luxury-haircare': {
            "url": "https://www.sephora.com/shop/luxury-haircare",
            "slug": 'luxury-haircare',
            "label": 'Luxury Hair',
        },
        'korean-hair-products': {
            "url": "https://www.sephora.com/shop/korean-hair-products",
            "slug": 'korean-hair-products',
            "label": 'Korean Hair',
        },
    },
    'Bath & Body': {
        'bath-body': {
            "url": "https://www.sephora.com/shop/bath-body",
            "slug": 'bath-body',
            "label": 'Bath & Body',
        },
        'bath-and-body-soap': {
            "url": "https://www.sephora.com/shop/bath-and-body-soap",
            "slug": 'bath-and-body-soap',
            "label": 'Bath & Shower',
        },
        'body-wash-shower-gel': {
            "url": "https://www.sephora.com/shop/body-wash-shower-gel",
            "slug": 'body-wash-shower-gel',
            "label": 'Body Wash & Shower Gel',
        },
        'body-scrub-exfoliant': {
            "url": "https://www.sephora.com/shop/body-scrub-exfoliant",
            "slug": 'body-scrub-exfoliant',
            "label": 'Scrubs & Exfoliants',
        },
        'bubble-bath-oil': {
            "url": "https://www.sephora.com/shop/bubble-bath-oil",
            "slug": 'bubble-bath-oil',
            "label": 'Bath Soaks & Bubble Bath',
        },
        'hand-sanitizer-soap': {
            "url": "https://www.sephora.com/shop/hand-sanitizer-soap",
            "slug": 'hand-sanitizer-soap',
            "label": 'Hand Sanitizer & Hand Soap',
        },
        'body-moisturizers': {
            "url": "https://www.sephora.com/shop/body-moisturizers",
            "slug": 'body-moisturizers',
            "label": 'Body Moisturizers',
        },
        'body-lotion-body-oil': {
            "url": "https://www.sephora.com/shop/body-lotion-body-oil",
            "slug": 'body-lotion-body-oil',
            "label": 'Body Lotions & Body Oils',
        },
        'hand-lotion-foot-cream': {
            "url": "https://www.sephora.com/shop/hand-lotion-foot-cream",
            "slug": 'hand-lotion-foot-cream',
            "label": 'Hand Cream & Foot Cream',
        },
        'deodorant-antiperspirant': {
            "url": "https://www.sephora.com/shop/deodorant-antiperspirant",
            "slug": 'deodorant-antiperspirant',
            "label": 'Deodorant & Antiperspirant',
        },
        'self-tanning-products': {
            "url": "https://www.sephora.com/shop/self-tanning-products",
            "slug": 'self-tanning-products',
            "label": 'Self Tanners',
        },
        'wellness-products': {
            "url": "https://www.sephora.com/shop/wellness-products",
            "slug": 'wellness-products',
            "label": 'Wellness',
        },
        'beauty-supplements-bath-body': {
            "url": "https://www.sephora.com/shop/beauty-supplements-bath-body",
            "slug": 'beauty-supplements-bath-body',
            "label": 'Supplements',
        },
        'intimate-care': {
            "url": "https://www.sephora.com/shop/intimate-care",
            "slug": 'intimate-care',
            "label": 'Intimate Care & Vibrators',
        },
        'home-scents-candles': {
            "url": "https://www.sephora.com/shop/home-scents-candles",
            "slug": 'home-scents-candles',
            "label": 'Candles & Home Scents',
        },
        'body-care-by-concern': {
            "url": "https://www.sephora.com/shop/body-care-by-concern",
            "slug": 'body-care-by-concern',
            "label": 'Shop By Concern',
        },
        'body-stretch-mark-firming-cream': {
            "url": "https://www.sephora.com/shop/body-stretch-mark-firming-cream",
            "slug": 'body-stretch-mark-firming-cream',
            "label": 'Stretch Marks & Firming',
        },
        'body-dry-skin-products': {
            "url": "https://www.sephora.com/shop/body-dry-skin-products",
            "slug": 'body-dry-skin-products',
            "label": 'Dryness / Dry Skin',
        },
        'body-texture-kp-products': {
            "url": "https://www.sephora.com/shop/body-texture-kp-products",
            "slug": 'body-texture-kp-products',
            "label": 'Smooth Texture',
        },
        'mini-bath-products': {
            "url": "https://www.sephora.com/shop/mini-bath-products",
            "slug": 'mini-bath-products',
            "label": 'Mini Size',
        },
        'bath-gift-sets': {
            "url": "https://www.sephora.com/shop/bath-gift-sets",
            "slug": 'bath-gift-sets',
            "label": 'Bath Gift Sets',
        },
    },
    'Mini Size': {
        'travel-size-toiletries': {
            "url": "https://www.sephora.com/shop/travel-size-toiletries",
            "slug": 'travel-size-toiletries',
            "label": 'Mini Size',
        },
        'shop-travel-size-makeup': {
            "url": "https://www.sephora.com/shop/shop-travel-size-makeup",
            "slug": 'shop-travel-size-makeup',
            "label": 'Makeup',
        },
        'shop-travel-size-skincare': {
            "url": "https://www.sephora.com/shop/shop-travel-size-skincare",
            "slug": 'shop-travel-size-skincare',
            "label": 'Skincare',
        },
        'shop-travel-size-perfume': {
            "url": "https://www.sephora.com/shop/shop-travel-size-perfume",
            "slug": 'shop-travel-size-perfume',
            "label": 'Fragrance',
        },
        'shop-travel-size-bath-products': {
            "url": "https://www.sephora.com/shop/shop-travel-size-bath-products",
            "slug": 'shop-travel-size-bath-products',
            "label": 'Bath & Body',
        },
        'shop-travel-size-gifts-sets': {
            "url": "https://www.sephora.com/shop/shop-travel-size-gifts-sets",
            "slug": 'shop-travel-size-gifts-sets',
            "label": 'Value & Gift Sets',
        },
        'travel-size-minis-under-25': {
            "url": "https://www.sephora.com/shop/travel-size-minis-under-25",
            "slug": 'travel-size-minis-under-25',
            "label": '$25 and Under',
        },
        'travel-size-minis-under-35': {
            "url": "https://www.sephora.com/shop/travel-size-minis-under-35",
            "slug": 'travel-size-minis-under-35',
            "label": '$35 and Under',
        },
        'luxury-beauty': {
            "url": "https://www.sephora.com/shop/luxury-beauty",
            "slug": 'luxury-beauty',
            "label": 'Luxe Minis',
        },
    },
    'Gifts & Value Sets': {
        'gifts': {
            "url": "https://www.sephora.com/shop/gifts",
            "slug": 'gifts',
            "label": 'Gifts & Value Sets',
        },
        'value-sets': {
            "url": "https://www.sephora.com/shop/value-sets",
            "slug": 'value-sets',
            "label": 'Value & Gift Sets',
        },
        'gifts-under-15': {
            "url": "https://www.sephora.com/shop/gifts-under-15",
            "slug": 'gifts-under-15',
            "label": '$15 and under',
        },
        'gifts-under-25': {
            "url": "https://www.sephora.com/shop/gifts-under-25",
            "slug": 'gifts-under-25',
            "label": '$25 and under',
        },
        'gifts-value-sets-under-35': {
            "url": "https://www.sephora.com/shop/gifts-value-sets-under-35",
            "slug": 'gifts-value-sets-under-35',
            "label": '$35 and under',
        },
        'gifts-under-50': {
            "url": "https://www.sephora.com/shop/gifts-under-50",
            "slug": 'gifts-under-50',
            "label": '$50 and under',
        },
        'gifts-under-75': {
            "url": "https://www.sephora.com/shop/gifts-under-75",
            "slug": 'gifts-under-75',
            "label": '$75 and under',
        },
        'gifts-under-100': {
            "url": "https://www.sephora.com/shop/gifts-under-100",
            "slug": 'gifts-under-100',
            "label": '$100 and under',
        },
        'makeup-gift-sets': {
            "url": "https://www.sephora.com/shop/makeup-gift-sets",
            "slug": 'makeup-gift-sets',
            "label": 'Makeup',
        },
        'skin-care-gift-sets': {
            "url": "https://www.sephora.com/shop/skin-care-gift-sets",
            "slug": 'skin-care-gift-sets',
            "label": 'Skincare',
        },
        'hair-gift-sets': {
            "url": "https://www.sephora.com/shop/hair-gift-sets",
            "slug": 'hair-gift-sets',
            "label": 'Hair',
        },
        'fragrance-gift-sets': {
            "url": "https://www.sephora.com/shop/fragrance-gift-sets",
            "slug": 'fragrance-gift-sets',
            "label": 'Fragrance',
        },
        'beauty-tool-gifts': {
            "url": "https://www.sephora.com/shop/beauty-tool-gifts",
            "slug": 'beauty-tool-gifts',
            "label": 'Tools',
        },
        'makeup-bags-accessories-by-category-gifts': {
            "url": "https://www.sephora.com/shop/makeup-bags-accessories-by-category-gifts",
            "slug": 'makeup-bags-accessories-by-category-gifts',
            "label": 'Brush Sets & Accessories',
        },
        'bath-set-gifts': {
            "url": "https://www.sephora.com/shop/bath-set-gifts",
            "slug": 'bath-set-gifts',
            "label": 'Bath & Body',
        },
        'gifts-for-her': {
            "url": "https://www.sephora.com/shop/gifts-for-her",
            "slug": 'gifts-for-her',
            "label": 'For Her',
        },
        'gifts-for-mom': {
            "url": "https://www.sephora.com/shop/gifts-for-mom",
            "slug": 'gifts-for-mom',
            "label": 'For Mom',
        },
        'gifts-for-men': {
            "url": "https://www.sephora.com/shop/gifts-for-men",
            "slug": 'gifts-for-men',
            "label": 'For Him',
        },
        'gifts-for-them': {
            "url": "https://www.sephora.com/shop/gifts-for-them",
            "slug": 'gifts-for-them',
            "label": 'For Them',
        },
        'top-beauty-gifts': {
            "url": "https://www.sephora.com/shop/top-beauty-gifts",
            "slug": 'top-beauty-gifts',
            "label": 'Top Rated Gifts',
        },
        'exclusive-products': {
            "url": "https://www.sephora.com/shop/exclusive-products",
            "slug": 'exclusive-products',
            "label": 'Only at Sephora',
        },
    },
}
