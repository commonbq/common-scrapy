from __future__ import annotations

import re

#: Victoria's Secret / PINK navigation taxonomy.
#:
#: Grouped mapping ``{brand: {leaf: rich}}``. The leaf key is the canonical
#: ``-a category=<leaf>`` slug and the DAG scheduling unit; each rich value keeps
#: the ``brand`` / ``top_category`` / ``department`` / ``url`` (and optional
#: ``sub_category``) the spider reads at runtime.
VICTORIASSECRET_CATEGORIES: dict[str, dict[str, dict[str, object]]] = {
    "vs": {
        "vs-new": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/newarrivals"
        },
        "vs-new-new-vs-icon-shoppe": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/newarrivals/vs-icon-shoppe",
            "sub_category": "New: VS Icon Shoppe"
        },
        "vs-new-bombshell-shine": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/beauty/all-bombshell-shine",
            "sub_category": "Bombshell Shine"
        },
        "vs-new-the-gift-shop": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/giftguide/shop-all",
            "sub_category": "The Gift Shop"
        },
        "vs-new-the-halloween-edit": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/halloween",
            "sub_category": "The Halloween Edit"
        },
        "vs-new-the-lacie-shop": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/bras/the-lacie-shop",
            "sub_category": "The Lacie Shop"
        },
        "vs-new-sexy-night-out": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/night-out",
            "sub_category": "Sexy Night Out"
        },
        "vs-new-as-seen-on-social": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/newarrivals/as-seen-on-tiktok",
            "sub_category": "As Seen on Social"
        },
        "vs-new-bestsellers": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/best-sellers",
            "sub_category": "Bestsellers\u200b"
        },
        "vs-new-our-collections": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/collections",
            "sub_category": "Our Collections"
        },
        "vs-new-brand-boutique": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/brands",
            "sub_category": "Brand Boutique"
        },
        "vs-new-gift-cards": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "vs-new-fashion-show": {
            "brand": "vs",
            "top_category": "New!",
            "department": "vs-new",
            "url": "https://www.victoriassecret.com/us/vs/vsinsider/fashionshow",
            "sub_category": "FASHION SHOW"
        },
        "vs-bras": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras"
        },
        "vs-bras-bestsellers": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/bestsellers",
            "sub_category": "BESTSELLERS"
        },
        "vs-bras-push-up": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/push-up",
            "sub_category": "Push-Up"
        },
        "vs-bras-full-coverage": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/full-coverage",
            "sub_category": "Full Coverage"
        },
        "vs-bras-wireless": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/lounge-and-wireless",
            "sub_category": "Wireless"
        },
        "vs-bras-lightly-lined": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/lightly-lined-and-demi",
            "sub_category": "Lightly Lined"
        },
        "vs-bras-strapless-solutions": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/strapless-and-backless",
            "sub_category": "Strapless & Solutions"
        },
        "vs-bras-t-shirt": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/t-shirt-bra",
            "sub_category": "T-Shirt"
        },
        "vs-bras-demi": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/demi",
            "sub_category": "Demi"
        },
        "vs-bras-unlined": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/unlined",
            "sub_category": "Unlined"
        },
        "vs-bras-balconette": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/balconette",
            "sub_category": "Balconette"
        },
        "vs-bras-plunge": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/plunge",
            "sub_category": "Plunge"
        },
        "vs-bras-sports-bras": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/sports-bras",
            "sub_category": "Sports Bras"
        },
        "vs-bras-bralettes": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/bralette",
            "sub_category": "Bralettes"
        },
        "vs-bras-corset-tops": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/corsets-and-bustiers",
            "sub_category": "Corset Tops"
        },
        "vs-bras-body-by-victoria": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/body-by-victoria-collection",
            "sub_category": "Body By Victoria"
        },
        "vs-bras-dream-angels": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/dream-angels",
            "sub_category": "Dream Angels"
        },
        "vs-bras-very-sexy": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/very-sexy",
            "sub_category": "Very Sexy"
        },
        "vs-bras-vs-signature": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/signature-collection",
            "sub_category": "VS Signature"
        },
        "vs-bras-lacie-collection": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/the-lacie-shop",
            "sub_category": "Lacie Collection"
        },
        "vs-bras-love-cloud": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/love-cloud-collection",
            "sub_category": "Love Cloud"
        },
        "vs-bras-adore-me": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/adore-me",
            "sub_category": "Adore Me"
        },
        "vs-bras-specialty-bras": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/specialty",
            "sub_category": "SPECIALTY BRAS"
        },
        "vs-bras-matching-sets": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/panties/bra-and-panty-sets",
            "sub_category": "Matching Sets"
        },
        "vs-bras-shine-bras-panties": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/panties/shine-collection",
            "sub_category": "Shine Bras & Panties"
        },
        "vs-bras-front-close-bras": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/front-close",
            "sub_category": "Front Close Bras"
        },
        "vs-bras-peekaboo-bras": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/open-cup-bra",
            "sub_category": "Peekaboo Bras"
        },
        "vs-bras-bra-fit-guide": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/bra-fitting-guide",
            "sub_category": "Bra Fit Guide"
        },
        "vs-bras-how-to-measure-bra-size": {
            "brand": "vs",
            "top_category": "BRAS",
            "department": "vs-bras",
            "url": "https://www.victoriassecret.com/us/vs/bras/how-to-measure-bras",
            "sub_category": "How to Measure Bra Size"
        },
        "vs-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties"
        },
        "vs-panties-8-38-panty-party": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/panties-offer",
            "sub_category": "8/$38 Panty Party"
        },
        "vs-panties-3-39-luxe-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/styles-specials",
            "sub_category": "3/$39 Luxe Panties"
        },
        "vs-panties-30-up-panty-packs": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/panty-packs",
            "sub_category": "$30 & Up Panty Packs"
        },
        "vs-panties-thong-v-string-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/thongs-and-v-strings",
            "sub_category": "Thong & V-String Panties"
        },
        "vs-panties-bikini-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/bikinis",
            "sub_category": "Bikini Panties"
        },
        "vs-panties-brief-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/briefs",
            "sub_category": "Brief Panties"
        },
        "vs-panties-hiphugger-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/hiphuggers",
            "sub_category": "Hiphugger Panties"
        },
        "vs-panties-cheeky-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/cheekies-and-cheekinis",
            "sub_category": "Cheeky Panties"
        },
        "vs-panties-boyshort-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/boyshorts-shorties",
            "sub_category": "Boyshort Panties"
        },
        "vs-panties-high-waist-high-leg-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/high-waisted-panties",
            "sub_category": "High-Waist & High-Leg Panties"
        },
        "vs-panties-brazilian-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/brazilian-panties",
            "sub_category": "Brazilian Panties"
        },
        "vs-panties-shapewear": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/shapewear",
            "sub_category": "Shapewear"
        },
        "vs-panties-panty-packs": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/panty-packs",
            "sub_category": "Panty Packs"
        },
        "vs-panties-peekaboo-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/crotchless-panties",
            "sub_category": "Peekaboo Panties"
        },
        "vs-panties-garters-stockings": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/garters",
            "sub_category": "Garters & Stockings"
        },
        "vs-panties-period-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/period-panties",
            "sub_category": "Period Panties"
        },
        "vs-panties-adaptive-bras-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/adaptive",
            "sub_category": "Adaptive Bras & Panties"
        },
        "vs-panties-bra-and-panty-sets": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/bra-and-panty-sets",
            "sub_category": "Bra and Panty Sets"
        },
        "vs-panties-no-show-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/no-show-panties",
            "sub_category": "No-Show Panties"
        },
        "vs-panties-cotton-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/cotton",
            "sub_category": "Cotton Panties"
        },
        "vs-panties-lace-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/lace",
            "sub_category": "Lace Panties"
        },
        "vs-panties-seamless-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/seamless",
            "sub_category": "Seamless Panties"
        },
        "vs-panties-low-rise": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/shop-by-rise?scroll=true#low",
            "sub_category": "Low Rise"
        },
        "vs-panties-mid-rise": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/shop-by-rise?scroll=true#mid",
            "sub_category": "Mid Rise"
        },
        "vs-panties-high-rise": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/shop-by-rise?scroll=true#high",
            "sub_category": "High Rise"
        },
        "vs-panties-the-lacie-shop": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/the-lacie-shop",
            "sub_category": "The Lacie Shop"
        },
        "vs-panties-shine-bra-panties": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/panties/shine-collection",
            "sub_category": "Shine Bra & Panties"
        },
        "vs-panties-body-by-victoria": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/body-collection",
            "sub_category": "Body By Victoria"
        },
        "vs-panties-dream-angels": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/dream-angels",
            "sub_category": "Dream Angels"
        },
        "vs-panties-very-sexy": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/very-sexy",
            "sub_category": "Very Sexy"
        },
        "vs-panties-vs-signature": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/signature-collection",
            "sub_category": "VS Signature"
        },
        "vs-panties-tease-collection": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/tease",
            "sub_category": "Tease Collection"
        },
        "vs-panties-the-love-cloud-collection": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/love-cloud-collection",
            "sub_category": "The Love Cloud Collection"
        },
        "vs-panties-adore-me": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/bras/adore-me?scroll=true&orderBy=REC&filter=category%3APanties",
            "sub_category": "Adore Me"
        },
        "vs-panties-vs-x-leonisa": {
            "brand": "vs",
            "top_category": "PANTIES",
            "department": "vs-panties",
            "url": "https://www.victoriassecret.com/us/vs/shapewear",
            "sub_category": "VS X Leonisa"
        },
        "vs-beauty": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty"
        },
        "vs-beauty-all-beauty": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/shop-all",
            "sub_category": "ALL BEAUTY"
        },
        "vs-beauty-12-fine-fragrance-mists-and-lotions": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/mist-and-lotion-offer",
            "sub_category": "$12 Fine Fragrance Mists and Lotions"
        },
        "vs-beauty-2-28-or-3-33-mists-lotions": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/the-mist-collection",
            "sub_category": "2/$28 or 3/$33 Mists & Lotions"
        },
        "vs-beauty-2-20-body-care": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/body-care-offer",
            "sub_category": "2/$20 Body Care"
        },
        "vs-beauty-12-under-home-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/home-fragrances/offer",
            "sub_category": "$12 & Under Home Fragrance"
        },
        "vs-beauty-all-fine-fragrances": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/all-fragrance",
            "sub_category": "ALL FINE FRAGRANCES"
        },
        "vs-beauty-all-mists-lotions": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/all-body-care",
            "sub_category": "ALL MISTS & LOTIONS"
        },
        "vs-beauty-all-body-care": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/natural-beauty-body-care",
            "sub_category": "ALL BODY CARE"
        },
        "vs-beauty-all-bombshell-shine": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/all-bombshell-shine",
            "sub_category": "ALL BOMBSHELL SHINE"
        },
        "vs-beauty-perfumes": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/perfume",
            "sub_category": "Perfumes"
        },
        "vs-beauty-body-mists-hair-mists": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/mists",
            "sub_category": "Body Mists & Hair Mists"
        },
        "vs-beauty-lotions-oils-glazes": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/body-lotions-and-moisturizers",
            "sub_category": "Lotions, Oils, & Glazes"
        },
        "vs-beauty-lips": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/lip",
            "sub_category": "Lips"
        },
        "vs-beauty-bath-shower-hair": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/body-wash",
            "sub_category": "Bath, Shower, & Hair"
        },
        "vs-beauty-travel": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/rollerballs-and-travel-size",
            "sub_category": "Travel"
        },
        "vs-beauty-gift-sets": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/giftguide/beauty-gift-sets",
            "sub_category": "Gift Sets"
        },
        "vs-beauty-candles-home-fragrances": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/home-fragrances",
            "sub_category": "Candles & Home Fragrances"
        },
        "vs-beauty-men-s-fine-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/mens-fine-fragrance",
            "sub_category": "Men's Fine Fragrance"
        },
        "vs-beauty-makeup-bags": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/accessories/cosmetic-bags",
            "sub_category": "Makeup Bags"
        },
        "vs-beauty-bombshell-no-1-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/fragrances-bombshell-shop",
            "sub_category": "Bombshell No. 1 Fragrance"
        },
        "vs-beauty-bare-fine-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/fragrances-bare-collection",
            "sub_category": "Bare Fine Fragrance"
        },
        "vs-beauty-tease-fine-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/tease",
            "sub_category": "Tease Fine Fragrance"
        },
        "vs-beauty-very-sexy-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/very-sexy-collection",
            "sub_category": "Very Sexy Fragrance"
        },
        "vs-beauty-dream-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/heavenly-dream-angels-fragrances",
            "sub_category": "Dream Fragrance"
        },
        "vs-beauty-love-fragrance": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/love-fragrance-collection",
            "sub_category": "Love Fragrance"
        },
        "vs-beauty-scent-finder": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/fragrance-finder",
            "sub_category": "Scent Finder"
        },
        "vs-beauty-shimmer": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/shimmer-shop",
            "sub_category": "Shimmer"
        },
        "vs-beauty-vanilla-fragrances": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/vanilla-perfume",
            "sub_category": "Vanilla Fragrances"
        },
        "vs-beauty-fashion-show": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/beauty/trending-now",
            "sub_category": "Fashion Show"
        },
        "vs-beauty-gift-cards": {
            "brand": "vs",
            "top_category": "BEAUTY",
            "department": "vs-beauty",
            "url": "https://www.victoriassecret.com/us/vs/gift-cards",
            "sub_category": "Gift Cards"
        },
        "vs-sleep": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear"
        },
        "vs-sleep-pajama-sets": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/pajama-sets",
            "sub_category": "Pajama Sets"
        },
        "vs-sleep-sleepshirts-nightgowns": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/sleepshirts",
            "sub_category": "Sleepshirts & Nightgowns"
        },
        "vs-sleep-robes": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/slippers-and-robes",
            "sub_category": "Robes"
        },
        "vs-sleep-cami-sets": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/camisoles",
            "sub_category": "Cami Sets"
        },
        "vs-sleep-slips": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/slips",
            "sub_category": "Slips"
        },
        "vs-sleep-sleep-separates": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/separates",
            "sub_category": "Sleep Separates"
        },
        "vs-sleep-long-pajama-sets": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/long-pajama-sets",
            "sub_category": "Long Pajama Sets"
        },
        "vs-sleep-short-pajama-sets": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/pajama-shorts-sets",
            "sub_category": "Short Pajama Sets"
        },
        "vs-sleep-slippers": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/slippers",
            "sub_category": "Slippers"
        },
        "vs-sleep-loungewear": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/loungewear",
            "sub_category": "Loungewear"
        },
        "vs-sleep-sosoft-modal": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/modal",
            "sub_category": "SoSoft\u2122 Modal"
        },
        "vs-sleep-signature-satin": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/satin",
            "sub_category": "Signature Satin"
        },
        "vs-sleep-flannel": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/flannel",
            "sub_category": "Flannel"
        },
        "vs-sleep-cotton": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/cotton",
            "sub_category": "Cotton"
        },
        "vs-sleep-new-silk": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/washable-silk",
            "sub_category": "New Silk"
        },
        "vs-sleep-printed-pajamas": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/printed-pajamas",
            "sub_category": "Printed Pajamas"
        },
        "vs-sleep-lunya": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/lunya",
            "sub_category": "Lunya"
        },
        "vs-sleep-adore-me": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/bras/adore-me?scroll=true&orderBy=REC&filter=category%3ASleep+%26+Lingerie",
            "sub_category": "Adore Me"
        },
        "vs-sleep-papinelle": {
            "brand": "vs",
            "top_category": "SLEEP",
            "department": "vs-sleep",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/papinelle",
            "sub_category": "Papinelle"
        },
        "vs-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie"
        },
        "vs-lingerie-slips": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/slips",
            "sub_category": "Slips"
        },
        "vs-lingerie-babydolls": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/babydolls",
            "sub_category": "Babydolls"
        },
        "vs-lingerie-cami-sets": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/camisoles",
            "sub_category": "Cami Sets"
        },
        "vs-lingerie-teddy-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/teddies-and-bodysuits",
            "sub_category": "Teddy Lingerie"
        },
        "vs-lingerie-robes": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/kimonos",
            "sub_category": "Robes"
        },
        "vs-lingerie-matching-sets": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/bras-and-panties",
            "sub_category": "Matching Sets"
        },
        "vs-lingerie-bodysuits-rompers": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/bodysuits",
            "sub_category": "Bodysuits & Rompers"
        },
        "vs-lingerie-corset-tops": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/corsets-and-bustiers",
            "sub_category": "Corset Tops"
        },
        "vs-lingerie-wear-out-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/very-sexy-collection",
            "sub_category": "Wear-Out Lingerie"
        },
        "vs-lingerie-shapewear": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/shapewear",
            "sub_category": "Shapewear"
        },
        "vs-lingerie-garters-stockings": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/panties/garters",
            "sub_category": "Garters & Stockings"
        },
        "vs-lingerie-bridal-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/bridal",
            "sub_category": "Bridal Lingerie"
        },
        "vs-lingerie-push-up-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/push-up",
            "sub_category": "Push-Up Lingerie"
        },
        "vs-lingerie-satin-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/satin",
            "sub_category": "Satin Lingerie"
        },
        "vs-lingerie-lace-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/lace",
            "sub_category": "Lace Lingerie"
        },
        "vs-lingerie-the-halloween-edit": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/halloween",
            "sub_category": "The Halloween Edit"
        },
        "vs-lingerie-tease-collection": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/bras/tease",
            "sub_category": "Tease Collection"
        },
        "vs-lingerie-after-hours-lingerie": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/after-hours",
            "sub_category": "After Hours Lingerie"
        },
        "vs-lingerie-new-silk-collection": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/sleepwear/washable-silk",
            "sub_category": "New Silk Collection"
        },
        "vs-lingerie-bluebella": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/bluebella",
            "sub_category": "Bluebella"
        },
        "vs-lingerie-adore-me": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/bras/adore-me",
            "sub_category": "Adore Me"
        },
        "vs-lingerie-vs-x-leonisa": {
            "brand": "vs",
            "top_category": "LINGERIE",
            "department": "vs-lingerie",
            "url": "https://www.victoriassecret.com/us/vs/shapewear",
            "sub_category": "VS X Leonisa"
        },
        "vs-clothing": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel"
        },
        "vs-clothing-2-59-sexy-swim-separates": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/swimwear/offer",
            "sub_category": "2/$59 Sexy Swim Separates"
        },
        "vs-clothing-angel-essentials-loungewear": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/angel-essentials",
            "sub_category": "ANGEL ESSENTIALS LOUNGEWEAR"
        },
        "vs-clothing-matching-sets": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/activewear/matching-sets",
            "sub_category": "Matching Sets"
        },
        "vs-clothing-dresses": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/dresses",
            "sub_category": "Dresses"
        },
        "vs-clothing-loungewear": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear",
            "sub_category": "Loungewear"
        },
        "vs-clothing-tees-tanks": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/tees-and-tank-tops",
            "sub_category": "Tees & Tanks"
        },
        "vs-clothing-sweatpants-leggings": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/joggers-and-sweatpants",
            "sub_category": "Sweatpants & Leggings"
        },
        "vs-clothing-sweatshirts": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/hoodies-and-sweatshirts",
            "sub_category": "Sweatshirts"
        },
        "vs-clothing-sweaters-cardigans": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/sweaters",
            "sub_category": "Sweaters & Cardigans"
        },
        "vs-clothing-jeans": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/denim",
            "sub_category": "Jeans"
        },
        "vs-clothing-shorts-skirts": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/shorts",
            "sub_category": "Shorts & Skirts"
        },
        "vs-clothing-jackets-coats": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/jackets",
            "sub_category": "Jackets & Coats"
        },
        "vs-clothing-bodysuits": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/bodysuits",
            "sub_category": "Bodysuits"
        },
        "vs-clothing-swim-cover-ups": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/swimwear",
            "sub_category": "Swim & Cover-ups"
        },
        "vs-clothing-maternity": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/maternity",
            "sub_category": "Maternity"
        },
        "vs-clothing-the-halloween-edit": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/halloween",
            "sub_category": "The Halloween Edit"
        },
        "vs-clothing-sexy-night-out": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/lingerie/night-out",
            "sub_category": "Sexy Night Out"
        },
        "vs-clothing-bridal-shop": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/wedding-shop",
            "sub_category": "Bridal Shop"
        },
        "vs-clothing-wedding-guest-dresses": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/wedding-guest-dresses",
            "sub_category": "Wedding Guest Dresses"
        },
        "vs-clothing-little-black-dresses": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/little-black-dresses",
            "sub_category": "Little Black Dresses"
        },
        "vs-clothing-featherweight-knit": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/activewear/featherweight-knit",
            "sub_category": "Featherweight Knit"
        },
        "vs-clothing-bardot": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/bardot",
            "sub_category": "Bardot"
        },
        "vs-clothing-summer-away": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/summer-away",
            "sub_category": "Summer Away"
        },
        "vs-clothing-nia": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/nia",
            "sub_category": "Nia"
        },
        "vs-clothing-lulus": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/lulus",
            "sub_category": "Lulus"
        },
        "vs-clothing-afrm": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/afrm",
            "sub_category": "AFRM"
        },
        "vs-clothing-astr-the-label": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/astr-the-label",
            "sub_category": "ASTR the Label"
        },
        "vs-clothing-avec-les-filles": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/apparel/avec-les-filles",
            "sub_category": "Avec Les Filles"
        },
        "vs-clothing-gift-cards": {
            "brand": "vs",
            "top_category": "CLOTHING",
            "department": "vs-clothing",
            "url": "https://www.victoriassecret.com/us/vs/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "vs-activewear": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear"
        },
        "vs-activewear-all-activewear": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/vs-sport",
            "sub_category": "ALL ACTIVEWEAR"
        },
        "vs-activewear-new-arrivals": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/new-arrivals",
            "sub_category": "NEW ARRIVALS"
        },
        "vs-activewear-up-to-50-off-vsx": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/offer",
            "sub_category": "Up to 50% Off VSX"
        },
        "vs-activewear-buy-2-bras-get-1-free": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/bras/sports-bras",
            "sub_category": "Buy 2 Bras, Get 1 Free"
        },
        "vs-activewear-sports-bras": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/bras/sports-bras",
            "sub_category": "Sports Bras"
        },
        "vs-activewear-leggings": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/leggings",
            "sub_category": "Leggings"
        },
        "vs-activewear-matching-sets": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/matching-sets",
            "sub_category": "Matching Sets"
        },
        "vs-activewear-bottoms": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/bottoms",
            "sub_category": "Bottoms"
        },
        "vs-activewear-tops": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/tops",
            "sub_category": "Tops"
        },
        "vs-activewear-shorts": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/biker-shorts",
            "sub_category": "Shorts"
        },
        "vs-activewear-jackets-coats": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/jackets",
            "sub_category": "Jackets & Coats"
        },
        "vs-activewear-dresses-and-jumpsuits": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/dresses-and-jumpsuits",
            "sub_category": "Dresses and Jumpsuits"
        },
        "vs-activewear-sneakers": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/shoes/sneakers",
            "sub_category": "Sneakers"
        },
        "vs-activewear-sport-panties": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/panties/sport-panties",
            "sub_category": "Sport Panties"
        },
        "vs-activewear-vsx-elevate": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/the-elevate-collection",
            "sub_category": "VSX Elevate\u2122"
        },
        "vs-activewear-vsx-new-essential": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/the-luxmarl-collection",
            "sub_category": "VSX New Essential"
        },
        "vs-activewear-featherweight-knit": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/featherweight-knit",
            "sub_category": "Featherweight Knit"
        },
        "vs-activewear-vsx-glossytech": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/trending-now",
            "sub_category": "VSX GlossyTech\u2122"
        },
        "vs-activewear-featherweight-sports-bras": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/activewear/featherweight-max-sports-bra",
            "sub_category": "Featherweight Sports Bras"
        },
        "vs-activewear-angel-essentials-loungewear": {
            "brand": "vs",
            "top_category": "Activewear",
            "department": "vs-activewear",
            "url": "https://www.victoriassecret.com/us/vs/loungewear/angel-essentials",
            "sub_category": "Angel Essentials Loungewear"
        },
        "vs-accessories": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories"
        },
        "vs-accessories-tote-bags": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/tote-bags",
            "sub_category": "Tote Bags"
        },
        "vs-accessories-fall-s-favorite-uggs": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/ugg",
            "sub_category": "Fall's Favorite UGGs"
        },
        "vs-accessories-bags": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/all-bags",
            "sub_category": "Bags"
        },
        "vs-accessories-makeup-bags": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/cosmetic-bags",
            "sub_category": "Makeup Bags"
        },
        "vs-accessories-keychains-charms": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/charms-and-keychains",
            "sub_category": "Keychains & Charms"
        },
        "vs-accessories-luggage-travel": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/luggage-and-travel",
            "sub_category": "Luggage & Travel"
        },
        "vs-accessories-socks-stockings": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/socks",
            "sub_category": "Socks & Stockings"
        },
        "vs-accessories-wallets-card-cases": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/wallets",
            "sub_category": "Wallets & Card Cases"
        },
        "vs-accessories-jewelry": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/jewelry",
            "sub_category": "Jewelry"
        },
        "vs-accessories-hats-hair-accessories": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/hats",
            "sub_category": "Hats & Hair Accessories"
        },
        "vs-accessories-sunglasses": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/sunglasses",
            "sub_category": "Sunglasses"
        },
        "vs-accessories-candles": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/beauty/candles",
            "sub_category": "Candles"
        },
        "vs-accessories-all-shoes": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/footwear",
            "sub_category": "ALL SHOES"
        },
        "vs-accessories-boots": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/boots",
            "sub_category": "Boots"
        },
        "vs-accessories-sandals": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/sandals",
            "sub_category": "Sandals"
        },
        "vs-accessories-slippers": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/slippers",
            "sub_category": "Slippers"
        },
        "vs-accessories-sneakers": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/sneakers",
            "sub_category": "Sneakers"
        },
        "vs-accessories-heels": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/heels",
            "sub_category": "Heels"
        },
        "vs-accessories-clogs-slides": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/clogs",
            "sub_category": "Clogs & Slides"
        },
        "vs-accessories-the-heritage-stripe-shop": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/accessories/heritage-stripe-shop",
            "sub_category": "The Heritage Stripe Shop"
        },
        "vs-accessories-ugg": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/ugg",
            "sub_category": "UGG"
        },
        "vs-accessories-hunter": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/hunter",
            "sub_category": "Hunter"
        },
        "vs-accessories-birkenstock": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/birkenstock",
            "sub_category": "Birkenstock"
        },
        "vs-accessories-puma": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/puma",
            "sub_category": "PUMA"
        },
        "vs-accessories-steve-madden": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/steve-madden",
            "sub_category": "Steve Madden"
        },
        "vs-accessories-dolce-vita": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/shoes/dolce-vita",
            "sub_category": "Dolce Vita"
        },
        "vs-accessories-gift-cards": {
            "brand": "vs",
            "top_category": "ACCESSORIES",
            "department": "vs-accessories",
            "url": "https://www.victoriassecret.com/us/vs/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "vs-fashion-show": {
            "brand": "vs",
            "top_category": "FASHION SHOW",
            "department": "vs-fashion-show",
            "url": "https://www.victoriassecret.com/us/vs/vsinsider/fashionshow"
        },
        "vs-fashion-show-shop-backstage-fashion-show-merch": {
            "brand": "vs",
            "top_category": "FASHION SHOW",
            "department": "vs-fashion-show",
            "url": "https://www.victoriassecret.com/us/vs/newarrivals/vs-icon-shoppe",
            "sub_category": "Shop Backstage Fashion Show Merch"
        },
        "vs-sale": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale"
        },
        "vs-sale-bras": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-bras",
            "sub_category": "Bras"
        },
        "vs-sale-panties": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-panties",
            "sub_category": "Panties"
        },
        "vs-sale-sleep": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-sleep",
            "sub_category": "Sleep"
        },
        "vs-sale-activewear": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-sport",
            "sub_category": "Activewear"
        },
        "vs-sale-beauty": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-beauty",
            "sub_category": "Beauty"
        },
        "vs-sale-lingerie": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-lingerie",
            "sub_category": "Lingerie"
        },
        "vs-sale-clothing": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-clothing",
            "sub_category": "Clothing"
        },
        "vs-sale-swim": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-swim",
            "sub_category": "Swim"
        },
        "vs-sale-accessories": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-accessories",
            "sub_category": "Accessories"
        },
        "vs-sale-home-fragrance": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/clearance-home-fragrance",
            "sub_category": "Home Fragrance"
        },
        "vs-sale-brands-we-love": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/brands-we-love-sale",
            "sub_category": "Brands We Love"
        },
        "vs-sale-adore-me": {
            "brand": "vs",
            "top_category": "SALE",
            "department": "vs-sale",
            "url": "https://www.victoriassecret.com/us/vs/sale/adore-me",
            "sub_category": "Adore Me"
        }
    },
    "pink": {
        "pink-pink-halftime-show": {
            "brand": "pink",
            "top_category": "PINK HALFTIME SHOW",
            "department": "pink-pink-halftime-show",
            "url": "https://www.victoriassecret.com/us/pink/fashion-show"
        },
        "pink-pink-halftime-show-the-pregame": {
            "brand": "pink",
            "top_category": "PINK HALFTIME SHOW",
            "department": "pink-pink-halftime-show",
            "url": "https://www.victoriassecret.com/us/pink/fashion-show/shop-the-show",
            "sub_category": "THE PREGAME"
        },
        "pink-new": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals"
        },
        "pink-new-pink-wednesday-drop": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/wednesday-drop",
            "sub_category": "PINK Wednesday Drop"
        },
        "pink-new-best-sellers": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/best-sellers",
            "sub_category": "Best Sellers"
        },
        "pink-new-secret-menu": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/online-exclusives",
            "sub_category": "Secret Menu"
        },
        "pink-new-halloween": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/halloween-shop",
            "sub_category": "Halloween"
        },
        "pink-new-pink-college-collection": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/collabs/collegiate-collection",
            "sub_category": "PINK College Collection"
        },
        "pink-new-pink-logo-shop": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/classic-pink-shop",
            "sub_category": "PINK Logo Shop"
        },
        "pink-new-bling-sparkle-shine": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/sparkle-and-shine",
            "sub_category": "Bling, Sparkle & Shine"
        },
        "pink-new-as-seen-on-social": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/as-seen-on-tiktok",
            "sub_category": "As Seen on Social"
        },
        "pink-new-game-day": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/game-day",
            "sub_category": "Game Day"
        },
        "pink-new-ugg": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/shoes/ugg-boots",
            "sub_category": "UGG"
        },
        "pink-new-birkenstock": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/shoes/birkenstock",
            "sub_category": "Birkenstock"
        },
        "pink-new-puma": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/shoes/puma",
            "sub_category": "Puma"
        },
        "pink-new-steve-madden": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/shoes/steve-madden",
            "sub_category": "Steve Madden"
        },
        "pink-new-hunter": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/shoes/hunter",
            "sub_category": "Hunter"
        },
        "pink-new-gifts": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/gifts",
            "sub_category": "GIFTS"
        },
        "pink-new-gift-cards": {
            "brand": "pink",
            "top_category": "NEW!",
            "department": "pink-new",
            "url": "https://www.victoriassecret.com/us/pink/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "pink-clothing": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms"
        },
        "pink-clothing-foldover-faves": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/foldover-faves",
            "sub_category": "Foldover Faves"
        },
        "pink-clothing-going-out-clothes": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/going-out-clothes",
            "sub_category": "Going Out Clothes"
        },
        "pink-clothing-secret-menu": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/new-arrivals/online-exclusives",
            "sub_category": "Secret Menu"
        },
        "pink-clothing-matching-sets": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/matching-sets",
            "sub_category": "Matching Sets"
        },
        "pink-clothing-new-waffle-lounge": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/cozy",
            "sub_category": "NEW: Waffle Lounge"
        },
        "pink-clothing-pink-college-collection": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/collabs/collegiate-collection",
            "sub_category": "PINK College Collection"
        },
        "pink-clothing-nfl-collection": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/collabs/nfl-collection",
            "sub_category": "NFL Collection"
        },
        "pink-clothing-sweatshirts-hoodies": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/sweatshirts",
            "sub_category": "Sweatshirts & Hoodies"
        },
        "pink-clothing-t-shirts": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/tees",
            "sub_category": "T-Shirts"
        },
        "pink-clothing-tank-tops": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/tank-tops",
            "sub_category": "Tank Tops"
        },
        "pink-clothing-going-out-tops": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/going-out",
            "sub_category": "Going Out Tops"
        },
        "pink-clothing-sweaters": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/sweaters",
            "sub_category": "Sweaters"
        },
        "pink-clothing-outerwear": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/outerwear",
            "sub_category": "Outerwear"
        },
        "pink-clothing-dresses": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/dresses",
            "sub_category": "DRESSES"
        },
        "pink-clothing-sweatpants-joggers": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/sweatpants",
            "sub_category": "Sweatpants & Joggers"
        },
        "pink-clothing-leggings": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/leggings",
            "sub_category": "Leggings"
        },
        "pink-clothing-flares": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/flares",
            "sub_category": "Flares"
        },
        "pink-clothing-denim": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/denim",
            "sub_category": "Denim"
        },
        "pink-clothing-shorts": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/shorts",
            "sub_category": "Shorts"
        },
        "pink-clothing-skirts": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/skirts",
            "sub_category": "Skirts"
        },
        "pink-clothing-pants": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/pants",
            "sub_category": "Pants"
        },
        "pink-clothing-capris": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/capris",
            "sub_category": "Capris"
        },
        "pink-clothing-campus-fleece-campus-cotton": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/campus-cotton",
            "sub_category": "Campus Fleece\u2122 & Campus Cotton\u2122"
        },
        "pink-clothing-all-day-cotton": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/all-day-cotton",
            "sub_category": "All Day Cotton\u2122"
        },
        "pink-clothing-pink-base-stretch": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/base-stretch",
            "sub_category": "PINK Base Stretch\u2122"
        },
        "pink-clothing-35-sweatshirts-sweatpants": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/apparel-offer",
            "sub_category": "$35 Sweatshirts & Sweatpants"
        },
        "pink-clothing-25-tees": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/offer",
            "sub_category": "$25 Tees"
        },
        "pink-clothing-40-off-denim": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/special-offer",
            "sub_category": "40% off Denim"
        },
        "pink-clothing-35-cotton-foldover-flare": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/select-styles",
            "sub_category": "$35 Cotton Foldover Flare"
        },
        "pink-clothing-gift-cards": {
            "brand": "pink",
            "top_category": "CLOTHING",
            "department": "pink-clothing",
            "url": "https://www.victoriassecret.com/us/pink/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "pink-bras": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras"
        },
        "pink-bras-push-up": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/push-up",
            "sub_category": "Push-Up"
        },
        "pink-bras-super-push-up": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/super-push-up",
            "sub_category": "Super Push-Up"
        },
        "pink-bras-t-shirt-lightly-lined": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/lightly-lined",
            "sub_category": "T-Shirt & Lightly Lined"
        },
        "pink-bras-wireless": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/wireless-styles",
            "sub_category": "Wireless"
        },
        "pink-bras-strapless-backless": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/strapless",
            "sub_category": "Strapless & Backless"
        },
        "pink-bras-bralettes": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/bralette",
            "sub_category": "Bralettes"
        },
        "pink-bras-sports-bras": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/sport-bras-collection",
            "sub_category": "Sports Bras"
        },
        "pink-bras-unlined": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/unlined",
            "sub_category": "Unlined"
        },
        "pink-bras-bra-tops": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/bra-tops",
            "sub_category": "Bra Tops"
        },
        "pink-bras-balconette": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/balconette",
            "sub_category": "Balconette"
        },
        "pink-bras-bra-panty-sets": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/matching-sets",
            "sub_category": "Bra & Panty Sets"
        },
        "pink-bras-adaptive-bras-panties": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/adaptive",
            "sub_category": "Adaptive Bras & Panties"
        },
        "pink-bras-marshmallow-bras-comfy-cute": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/comfy-marshmallow",
            "sub_category": "Marshmallow Bras: Comfy & Cute"
        },
        "pink-bras-wear-everywhere-everyday-faves": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/all-wear-everywhere-special-pink",
            "sub_category": "Wear Everywhere\u2122: Everyday Faves"
        },
        "pink-bras-pink-wink-fun-flirty": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/the-wink",
            "sub_category": "PINK Wink\u2122: Fun & Flirty"
        },
        "pink-bras-pink-relay-sporty-faves": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/sport/relay-collection?scroll=true&orderBy=REC&filter=subclass%3ASports%20Bras",
            "sub_category": "PINK Relay\u2122: Sporty Faves"
        },
        "pink-bras-meet-our-bras": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/meet-our-bras",
            "sub_category": "Meet Our Bras"
        },
        "pink-bras-how-to-measure-bra-size": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/how-to-measure",
            "sub_category": "How to Measure Bra Size"
        },
        "pink-bras-bras-from-25": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/offer",
            "sub_category": "Bras from $25"
        },
        "pink-bras-2-42-sports-bras": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/bras/sport-bra-offer",
            "sub_category": "2/$42 Sports Bras"
        },
        "pink-bras-gift-cards": {
            "brand": "pink",
            "top_category": "BRAS",
            "department": "pink-bras",
            "url": "https://www.victoriassecret.com/us/pink/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "pink-panties": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear"
        },
        "pink-panties-thongs-v-strings": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/thong-underwear",
            "sub_category": "Thongs & V-Strings"
        },
        "pink-panties-cheekies": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/cheekster-underwear",
            "sub_category": "Cheekies"
        },
        "pink-panties-boyshorts": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/boyshort-underwear",
            "sub_category": "Boyshorts"
        },
        "pink-panties-hiphuggers": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/hipster-underwear",
            "sub_category": "Hiphuggers"
        },
        "pink-panties-bikinis": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/bikini-underwear",
            "sub_category": "Bikinis"
        },
        "pink-panties-panty-packs": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/underwear-packs",
            "sub_category": "Panty Packs"
        },
        "pink-panties-brazilians": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/brazilian-underwear",
            "sub_category": "Brazilians"
        },
        "pink-panties-period-panties": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/leak-proof-period-underwear",
            "sub_category": "Period Panties"
        },
        "pink-panties-bra-panty-sets": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/bras/matching-sets",
            "sub_category": "Bra & Panty Sets"
        },
        "pink-panties-adaptive-bras-panties": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/bras/adaptive",
            "sub_category": "Adaptive Bras & Panties"
        },
        "pink-panties-our-1-collection-no-show": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/no-show-underwear",
            "sub_category": "Our #1 Collection: No-Show"
        },
        "pink-panties-cotton": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/cotton-underwear",
            "sub_category": "Cotton"
        },
        "pink-panties-lace": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/lace-underwear",
            "sub_category": "Lace"
        },
        "pink-panties-seamless": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/seamless-collection",
            "sub_category": "Seamless"
        },
        "pink-panties-ultra-low-rise": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#ultra-low",
            "sub_category": "Ultra-Low Rise"
        },
        "pink-panties-low-rise": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#low",
            "sub_category": "Low Rise"
        },
        "pink-panties-mid-rise": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#mid",
            "sub_category": "Mid Rise"
        },
        "pink-panties-high-rise": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#high",
            "sub_category": "High Rise"
        },
        "pink-panties-8-38-panties": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/underwear-offer",
            "sub_category": "8/$38 Panties"
        },
        "pink-panties-panty-packs-from-35": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/underwear/underwear-packs",
            "sub_category": "Panty Packs from $35"
        },
        "pink-panties-gift-cards": {
            "brand": "pink",
            "top_category": "PANTIES",
            "department": "pink-panties",
            "url": "https://www.victoriassecret.com/us/pink/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "pink-sleep": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear"
        },
        "pink-sleep-mix-match-pajamas": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/mix-and-match",
            "sub_category": "Mix & Match Pajamas"
        },
        "pink-sleep-pajama-sets": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/sets",
            "sub_category": "Pajama Sets"
        },
        "pink-sleep-pajama-tops": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/tops",
            "sub_category": "Pajama Tops"
        },
        "pink-sleep-pajama-bottoms": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/bottoms",
            "sub_category": "Pajama Bottoms"
        },
        "pink-sleep-robes-slippers-socks": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/robes-socks-and-slippers",
            "sub_category": "Robes, Slippers, & Socks"
        },
        "pink-sleep-new-flannel": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/flannel",
            "sub_category": "New: Flannel"
        },
        "pink-sleep-modal": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/modal",
            "sub_category": "Modal"
        },
        "pink-sleep-cotton": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/cotton",
            "sub_category": "Cotton"
        },
        "pink-sleep-2-45-sleep": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/sleepwear/special-offer",
            "sub_category": "2/$45 Sleep"
        },
        "pink-sleep-gift-cards": {
            "brand": "pink",
            "top_category": "SLEEP",
            "department": "pink-sleep",
            "url": "https://www.victoriassecret.com/us/pink/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "pink-activewear": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/sport"
        },
        "pink-activewear-leggings": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/leggings",
            "sub_category": "Leggings"
        },
        "pink-activewear-sports-bras": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/bras/sport-bras-collection",
            "sub_category": "Sports Bras"
        },
        "pink-activewear-flare-leggings": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/yoga-pants",
            "sub_category": "Flare Leggings"
        },
        "pink-activewear-athletic-shorts": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/biker-shorts",
            "sub_category": "Athletic Shorts"
        },
        "pink-activewear-sport-jackets": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/sport/jackets",
            "sub_category": "Sport Jackets"
        },
        "pink-activewear-workout-tops": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/sport/workout-tops",
            "sub_category": "Workout Tops"
        },
        "pink-activewear-sneakers": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/accessories/sneakers",
            "sub_category": "Sneakers"
        },
        "pink-activewear-sport-panties": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/underwear/sport-underwear",
            "sub_category": "Sport Panties"
        },
        "pink-activewear-pink-relay": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/sport/relay-collection",
            "sub_category": "PINK Relay\u2122"
        },
        "pink-activewear-all-day-cotton": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/all-day-cotton",
            "sub_category": "All-Day Cotton\u2122"
        },
        "pink-activewear-2-42-sports-bras": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/bras/sport-bra-offer",
            "sub_category": "2/$42 Sports Bras"
        },
        "pink-activewear-gift-cards": {
            "brand": "pink",
            "top_category": "ACTIVEWEAR",
            "department": "pink-activewear",
            "url": "https://www.victoriassecret.com/us/pink/gift-cards",
            "sub_category": "GIFT CARDS"
        },
        "pink-accessories": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories"
        },
        "pink-accessories-all-shoes": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/footwear",
            "sub_category": "ALL SHOES"
        },
        "pink-accessories-slipper-szn": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/slippers",
            "sub_category": "Slipper Szn"
        },
        "pink-accessories-hot-rn-ugg": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/ugg-boots",
            "sub_category": "Hot RN: UGG"
        },
        "pink-accessories-the-pink-pup-shop": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/pet-accessories",
            "sub_category": "The PINK Pup Shop"
        },
        "pink-accessories-travel-accessories": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/travel",
            "sub_category": "Travel Accessories"
        },
        "pink-accessories-bags": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/bags",
            "sub_category": "BAGS"
        },
        "pink-accessories-totes": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/tote-bags",
            "sub_category": "Totes\u200b"
        },
        "pink-accessories-backpacks": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/backpacks",
            "sub_category": "Backpacks"
        },
        "pink-accessories-shoulder-crossbody": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/crossbody-bags",
            "sub_category": "Shoulder & Crossbody"
        },
        "pink-accessories-travel-bags": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/travel-bags",
            "sub_category": "Travel Bags"
        },
        "pink-accessories-makeup-beauty-bags": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/makeup-bags",
            "sub_category": "Makeup & Beauty Bags"
        },
        "pink-accessories-keychains-bag-charms": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/keychains",
            "sub_category": "Keychains & Bag Charms"
        },
        "pink-accessories-stackable-jewelry": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/jewelry",
            "sub_category": "Stackable Jewelry"
        },
        "pink-accessories-socks": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/socks-and-slippers",
            "sub_category": "Socks"
        },
        "pink-accessories-hats-hair-accessories": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/hats",
            "sub_category": "Hats & Hair Accessories"
        },
        "pink-accessories-sunglasses": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/sunglasses",
            "sub_category": "Sunglasses"
        },
        "pink-accessories-shoes": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/footwear",
            "sub_category": "SHOES"
        },
        "pink-accessories-boots": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/boots",
            "sub_category": "Boots"
        },
        "pink-accessories-slippers": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/slippers",
            "sub_category": "Slippers"
        },
        "pink-accessories-sneakers": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/sneakers",
            "sub_category": "Sneakers"
        },
        "pink-accessories-clogs": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/clogs",
            "sub_category": "Clogs"
        },
        "pink-accessories-flats": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/flats-and-loafers",
            "sub_category": "Flats"
        },
        "pink-accessories-sandals-flip-flops": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/sandals",
            "sub_category": "Sandals & Flip-Flops"
        },
        "pink-accessories-birkenstock": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/birkenstock",
            "sub_category": "Birkenstock"
        },
        "pink-accessories-ugg": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/ugg-boots",
            "sub_category": "UGG"
        },
        "pink-accessories-puma": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/puma",
            "sub_category": "PUMA"
        },
        "pink-accessories-hunter": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/hunter",
            "sub_category": "Hunter"
        },
        "pink-accessories-crocs": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/crocs",
            "sub_category": "Crocs"
        },
        "pink-accessories-steve-madden": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/shoes/steve-madden",
            "sub_category": "Steve Madden"
        },
        "pink-accessories-bags-from-30": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/offer",
            "sub_category": "Bags from $30"
        },
        "pink-accessories-2-30-bag-charms-more": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/keychains",
            "sub_category": "2/$30 Bag Charms & More\u200b"
        },
        "pink-accessories-socks-from-7": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/accessories-offer",
            "sub_category": "Socks from $7"
        },
        "pink-accessories-2-40-little-words-project-bracelets": {
            "brand": "pink",
            "top_category": "ACCESSORIES",
            "department": "pink-accessories",
            "url": "https://www.victoriassecret.com/us/pink/accessories/little-words-project",
            "sub_category": "2/$40 Little Words Project Bracelets"
        },
        "pink-beauty": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty"
        },
        "pink-beauty-perfume": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/perfume",
            "sub_category": "Perfume"
        },
        "pink-beauty-hair-body-mists": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/mists",
            "sub_category": "Hair & Body Mists"
        },
        "pink-beauty-lotions-oils": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/body-lotion",
            "sub_category": "Lotions & Oils"
        },
        "pink-beauty-scrubs-washes": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/beauty-body-wash",
            "sub_category": "Scrubs & Washes"
        },
        "pink-beauty-body-oil": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/body-oil",
            "sub_category": "Body Oil"
        },
        "pink-beauty-lip": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/lip",
            "sub_category": "Lip"
        },
        "pink-beauty-minis-travel-size": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/beauty-on-the-go",
            "sub_category": "Minis & Travel-Size"
        },
        "pink-beauty-fruity": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#fruity",
            "sub_category": "Fruity"
        },
        "pink-beauty-vanilla": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#vanilla",
            "sub_category": "Vanilla"
        },
        "pink-beauty-warm": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#warm",
            "sub_category": "Warm"
        },
        "pink-beauty-fresh": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#fresh",
            "sub_category": "Fresh"
        },
        "pink-beauty-10-full-sized": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/select-styles",
            "sub_category": "$10 Full-Sized"
        },
        "pink-beauty-build-your-routine": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/build-your-routine",
            "sub_category": "Build Your Routine"
        },
        "pink-beauty-new-arrivals": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/limited-edition",
            "sub_category": "New Arrivals"
        },
        "pink-beauty-scent-finder": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists",
            "sub_category": "Scent Finder"
        },
        "pink-beauty-shimmer-shop": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/body-spray-and-shimmer",
            "sub_category": "Shimmer Shop"
        },
        "pink-beauty-body-care-shop": {
            "brand": "pink",
            "top_category": "BEAUTY",
            "department": "pink-beauty",
            "url": "https://www.victoriassecret.com/us/pink/beauty/body-care",
            "sub_category": "Body Care Shop"
        },
        "pink-gifts": {
            "brand": "pink",
            "top_category": "GIFTS",
            "department": "pink-gifts",
            "url": "https://www.victoriassecret.com/us/pink/gifts"
        },
        "pink-sale": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink"
        },
        "pink-sale-clothing": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/apparel-sale",
            "sub_category": "Clothing"
        },
        "pink-sale-bras": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/bras-sale",
            "sub_category": "Bras"
        },
        "pink-sale-panties": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/underwear-sale",
            "sub_category": "Panties"
        },
        "pink-sale-sleep": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/sleep-sale",
            "sub_category": "Sleep"
        },
        "pink-sale-activewear": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/activewear-sale",
            "sub_category": "Activewear"
        },
        "pink-sale-swim": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/swim-sale",
            "sub_category": "Swim"
        },
        "pink-sale-shoes-accessories": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/accessories-sale",
            "sub_category": "Shoes & Accessories"
        },
        "pink-sale-beauty": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/beauty-sale",
            "sub_category": "Beauty"
        },
        "pink-sale-brands-we-love": {
            "brand": "pink",
            "top_category": "SALE",
            "department": "pink-sale",
            "url": "https://www.victoriassecret.com/us/pink/all-sale-pink/brands-we-love",
            "sub_category": "Brands We Love"
        }
    }
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_categories() -> list[dict[str, str]]:
    """Flatten the grouped taxonomy into canonical listing categories.

    Order is preserved (brand, then leaf) so the flattened rows match the DAG's
    ``_spider_category_groups`` output and the legacy inventory exactly.
    """
    return [
        dict(leaf, category=leaf_name)
        for group in VICTORIASSECRET_CATEGORIES.values()
        for leaf_name, leaf in group.items()
    ]


if __name__ == "__main__":
    """Print flattened crawl targets, or resolve a single ``--category``.

    Usage:
        python -m common.spiders.victoriassecret_categories
        python -m common.spiders.victoriassecret_categories --category vs-bras
    """
    import argparse
    import json as _json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", help="show the single matching category")
    options = parser.parse_args()

    targets = load_categories()
    if options.category:
        matches = [t for t in targets if t["category"] == options.category]
        if not matches:
            parser.error(
                f"Unknown category '{options.category}'. "
                f"Available: {', '.join(t['category'] for t in targets)}"
            )
        print(_json.dumps(matches, indent=2))
    else:
        for target in targets:
            print(f"{target['category']}\t{target['url']}")
