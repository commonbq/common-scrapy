from __future__ import annotations

import re

VICTORIASSECRET_CATEGORIES: dict[str, dict[str, dict[str, dict[str, str]]]] = {
    "vs": {
        "Pink Color": {
            "path": "",
            "subcategories": {
                "Group 1": {
                    "Gifts": "https://www.victoriassecret.com/us/vs/giftguide/shop-all"
                }
            }
        },
        "New!": {
            "path": "https://www.victoriassecret.com/us/vs/newarrivals",
            "subcategories": {
                "Group 1": {
                    "ALL NEW ARRIVALS": "https://www.victoriassecret.com/us/vs/newarrivals"
                },
                "Group 2": {
                    "New: VS Icon Shoppe": "https://www.victoriassecret.com/us/vs/newarrivals/vs-icon-shoppe",
                    "Bombshell Shine": "https://www.victoriassecret.com/us/vs/beauty/all-bombshell-shine",
                    "The Gift Shop": "https://www.victoriassecret.com/us/vs/giftguide/shop-all",
                    "The Halloween Edit": "https://www.victoriassecret.com/us/vs/lingerie/halloween",
                    "The Lacie Shop": "https://www.victoriassecret.com/us/vs/bras/the-lacie-shop",
                    "Sexy Night Out": "https://www.victoriassecret.com/us/vs/lingerie/night-out",
                    "As Seen on Social": "https://www.victoriassecret.com/us/vs/newarrivals/as-seen-on-tiktok"
                },
                "Group 3": {
                    "Bestsellers\u200b": "https://www.victoriassecret.com/us/vs/best-sellers",
                    "Our Collections": "https://www.victoriassecret.com/us/vs/collections",
                    "Brand Boutique": "https://www.victoriassecret.com/us/vs/brands",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/vs/gift-cards",
                    "FASHION SHOW": "https://www.victoriassecret.com/us/vs/vsinsider/fashionshow"
                }
            }
        },
        "BRAS": {
            "path": "https://www.victoriassecret.com/us/vs/bras",
            "subcategories": {
                "Group 1": {
                    "ALL BRAS: A-F CUPS": "https://www.victoriassecret.com/us/vs/bras",
                    "BESTSELLERS": "https://www.victoriassecret.com/us/vs/bras/bestsellers",
                    "Buy 2 Bras, Get 1 Free": "https://www.victoriassecret.com/us/vs/bras"
                },
                "Group 2": {
                    "Push-Up": "https://www.victoriassecret.com/us/vs/bras/push-up",
                    "Full Coverage": "https://www.victoriassecret.com/us/vs/bras/full-coverage",
                    "Wireless": "https://www.victoriassecret.com/us/vs/bras/lounge-and-wireless",
                    "Lightly Lined": "https://www.victoriassecret.com/us/vs/bras/lightly-lined-and-demi",
                    "Strapless & Solutions": "https://www.victoriassecret.com/us/vs/bras/strapless-and-backless",
                    "T-Shirt": "https://www.victoriassecret.com/us/vs/bras/t-shirt-bra",
                    "Demi": "https://www.victoriassecret.com/us/vs/bras/demi",
                    "Unlined": "https://www.victoriassecret.com/us/vs/bras/unlined",
                    "Balconette": "https://www.victoriassecret.com/us/vs/bras/balconette",
                    "Plunge": "https://www.victoriassecret.com/us/vs/bras/plunge",
                    "Sports Bras": "https://www.victoriassecret.com/us/vs/bras/sports-bras",
                    "Bralettes": "https://www.victoriassecret.com/us/vs/bras/bralette",
                    "Corset Tops": "https://www.victoriassecret.com/us/vs/lingerie/corsets-and-bustiers"
                },
                "Group 3": {
                    "Body By Victoria": "https://www.victoriassecret.com/us/vs/bras/body-by-victoria-collection",
                    "Dream Angels": "https://www.victoriassecret.com/us/vs/bras/dream-angels",
                    "Very Sexy": "https://www.victoriassecret.com/us/vs/bras/very-sexy",
                    "VS Signature": "https://www.victoriassecret.com/us/vs/bras/signature-collection",
                    "Lacie Collection": "https://www.victoriassecret.com/us/vs/bras/the-lacie-shop",
                    "Love Cloud": "https://www.victoriassecret.com/us/vs/bras/love-cloud-collection",
                    "Adore Me": "https://www.victoriassecret.com/us/vs/bras/adore-me",
                    "SPECIALTY BRAS": "https://www.victoriassecret.com/us/vs/bras/specialty"
                },
                "Group 4": {
                    "Matching Sets": "https://www.victoriassecret.com/us/vs/panties/bra-and-panty-sets",
                    "Shine Bras & Panties": "https://www.victoriassecret.com/us/vs/panties/shine-collection",
                    "Front Close Bras": "https://www.victoriassecret.com/us/vs/bras/front-close",
                    "Peekaboo Bras": "https://www.victoriassecret.com/us/vs/bras/open-cup-bra",
                    "Bra Fit Guide": "https://www.victoriassecret.com/us/vs/bras/bra-fitting-guide",
                    "How to Measure Bra Size": "https://www.victoriassecret.com/us/vs/bras/how-to-measure-bras"
                }
            }
        },
        "PANTIES": {
            "path": "https://www.victoriassecret.com/us/vs/panties",
            "subcategories": {
                "Group 1": {
                    "All Panties: XS-XXXL": "https://www.victoriassecret.com/us/vs/panties",
                    "8/$38 Panty Party": "https://www.victoriassecret.com/us/vs/panties/panties-offer",
                    "3/$39 Luxe Panties": "https://www.victoriassecret.com/us/vs/panties/styles-specials",
                    "$30 & Up Panty Packs": "https://www.victoriassecret.com/us/vs/panties/panty-packs"
                },
                "Group 2": {
                    "Thong & V-String Panties": "https://www.victoriassecret.com/us/vs/panties/thongs-and-v-strings",
                    "Bikini Panties": "https://www.victoriassecret.com/us/vs/panties/bikinis",
                    "Brief Panties": "https://www.victoriassecret.com/us/vs/panties/briefs",
                    "Hiphugger Panties": "https://www.victoriassecret.com/us/vs/panties/hiphuggers",
                    "Cheeky Panties": "https://www.victoriassecret.com/us/vs/panties/cheekies-and-cheekinis",
                    "Boyshort Panties": "https://www.victoriassecret.com/us/vs/panties/boyshorts-shorties",
                    "High-Waist & High-Leg Panties": "https://www.victoriassecret.com/us/vs/panties/high-waisted-panties",
                    "Brazilian Panties": "https://www.victoriassecret.com/us/vs/panties/brazilian-panties",
                    "Shapewear": "https://www.victoriassecret.com/us/vs/shapewear",
                    "Panty Packs": "https://www.victoriassecret.com/us/vs/panties/panty-packs",
                    "Peekaboo Panties": "https://www.victoriassecret.com/us/vs/panties/crotchless-panties",
                    "Garters & Stockings": "https://www.victoriassecret.com/us/vs/panties/garters",
                    "Period Panties": "https://www.victoriassecret.com/us/vs/panties/period-panties",
                    "Adaptive Bras & Panties": "https://www.victoriassecret.com/us/vs/bras/adaptive",
                    "Bra and Panty Sets": "https://www.victoriassecret.com/us/vs/panties/bra-and-panty-sets"
                },
                "Group 3": {
                    "No-Show Panties": "https://www.victoriassecret.com/us/vs/panties/no-show-panties",
                    "Cotton Panties": "https://www.victoriassecret.com/us/vs/panties/cotton",
                    "Lace Panties": "https://www.victoriassecret.com/us/vs/panties/lace",
                    "Seamless Panties": "https://www.victoriassecret.com/us/vs/panties/seamless",
                    "Low Rise": "https://www.victoriassecret.com/us/vs/panties/shop-by-rise?scroll=true#low",
                    "Mid Rise": "https://www.victoriassecret.com/us/vs/panties/shop-by-rise?scroll=true#mid",
                    "High Rise": "https://www.victoriassecret.com/us/vs/panties/shop-by-rise?scroll=true#high"
                },
                "Group 4": {
                    "The Lacie Shop": "https://www.victoriassecret.com/us/vs/bras/the-lacie-shop",
                    "Shine Bra & Panties": "https://www.victoriassecret.com/us/vs/panties/shine-collection",
                    "Body By Victoria": "https://www.victoriassecret.com/us/vs/bras/body-collection",
                    "Dream Angels": "https://www.victoriassecret.com/us/vs/bras/dream-angels",
                    "Very Sexy": "https://www.victoriassecret.com/us/vs/bras/very-sexy",
                    "VS Signature": "https://www.victoriassecret.com/us/vs/bras/signature-collection",
                    "Tease Collection": "https://www.victoriassecret.com/us/vs/bras/tease",
                    "The Love Cloud Collection": "https://www.victoriassecret.com/us/vs/bras/love-cloud-collection",
                    "Adore Me": "https://www.victoriassecret.com/us/vs/bras/adore-me?scroll=true&orderBy=REC&filter=category%3APanties",
                    "VS X Leonisa": "https://www.victoriassecret.com/us/vs/shapewear"
                }
            }
        },
        "BEAUTY": {
            "path": "https://www.victoriassecret.com/us/vs/beauty",
            "subcategories": {
                "Group 1": {
                    "ALL BEAUTY": "https://www.victoriassecret.com/us/vs/beauty/shop-all",
                    "$12 Fine Fragrance Mists and Lotions": "https://www.victoriassecret.com/us/vs/beauty/mist-and-lotion-offer",
                    "2/$28 or 3/$33 Mists & Lotions": "https://www.victoriassecret.com/us/vs/beauty/the-mist-collection",
                    "2/$20 Body Care": "https://www.victoriassecret.com/us/vs/beauty/body-care-offer",
                    "$12 & Under Home Fragrance": "https://www.victoriassecret.com/us/vs/home-fragrances/offer"
                },
                "Group 2": {
                    "ALL FINE FRAGRANCES": "https://www.victoriassecret.com/us/vs/beauty/all-fragrance",
                    "ALL MISTS & LOTIONS": "https://www.victoriassecret.com/us/vs/beauty/all-body-care",
                    "ALL BODY CARE": "https://www.victoriassecret.com/us/vs/beauty/natural-beauty-body-care",
                    "ALL BOMBSHELL SHINE": "https://www.victoriassecret.com/us/vs/beauty/all-bombshell-shine"
                },
                "Group 3": {
                    "Perfumes": "https://www.victoriassecret.com/us/vs/beauty/perfume",
                    "Body Mists & Hair Mists": "https://www.victoriassecret.com/us/vs/beauty/mists",
                    "Lotions, Oils, & Glazes": "https://www.victoriassecret.com/us/vs/beauty/body-lotions-and-moisturizers",
                    "Lips": "https://www.victoriassecret.com/us/vs/beauty/lip",
                    "Bath, Shower, & Hair": "https://www.victoriassecret.com/us/vs/beauty/body-wash",
                    "Travel": "https://www.victoriassecret.com/us/vs/beauty/rollerballs-and-travel-size",
                    "Gift Sets": "https://www.victoriassecret.com/us/vs/giftguide/beauty-gift-sets",
                    "Candles & Home Fragrances": "https://www.victoriassecret.com/us/vs/home-fragrances",
                    "Men's Fine Fragrance": "https://www.victoriassecret.com/us/vs/beauty/mens-fine-fragrance",
                    "Makeup Bags": "https://www.victoriassecret.com/us/vs/accessories/cosmetic-bags"
                },
                "Group 4": {
                    "Bombshell No. 1 Fragrance": "https://www.victoriassecret.com/us/vs/beauty/fragrances-bombshell-shop",
                    "Bare Fine Fragrance": "https://www.victoriassecret.com/us/vs/beauty/fragrances-bare-collection",
                    "Tease Fine Fragrance": "https://www.victoriassecret.com/us/vs/beauty/tease",
                    "Very Sexy Fragrance": "https://www.victoriassecret.com/us/vs/beauty/very-sexy-collection",
                    "Dream Fragrance": "https://www.victoriassecret.com/us/vs/beauty/heavenly-dream-angels-fragrances",
                    "Love Fragrance": "https://www.victoriassecret.com/us/vs/beauty/love-fragrance-collection",
                    "Scent Finder": "https://www.victoriassecret.com/us/vs/beauty/fragrance-finder",
                    "Shimmer": "https://www.victoriassecret.com/us/vs/beauty/shimmer-shop",
                    "Vanilla Fragrances": "https://www.victoriassecret.com/us/vs/beauty/vanilla-perfume",
                    "Fashion Show": "https://www.victoriassecret.com/us/vs/beauty/trending-now",
                    "Gift Cards": "https://www.victoriassecret.com/us/vs/gift-cards"
                }
            }
        },
        "SLEEP": {
            "path": "https://www.victoriassecret.com/us/vs/sleepwear",
            "subcategories": {
                "Group 1": {
                    "ALL SLEEP": "https://www.victoriassecret.com/us/vs/sleepwear"
                },
                "Group 2": {
                    "Pajama Sets": "https://www.victoriassecret.com/us/vs/sleepwear/pajama-sets",
                    "Sleepshirts & Nightgowns": "https://www.victoriassecret.com/us/vs/sleepwear/sleepshirts",
                    "Robes": "https://www.victoriassecret.com/us/vs/sleepwear/slippers-and-robes",
                    "Cami Sets": "https://www.victoriassecret.com/us/vs/sleepwear/camisoles",
                    "Slips": "https://www.victoriassecret.com/us/vs/lingerie/slips",
                    "Sleep Separates": "https://www.victoriassecret.com/us/vs/sleepwear/separates",
                    "Long Pajama Sets": "https://www.victoriassecret.com/us/vs/sleepwear/long-pajama-sets",
                    "Short Pajama Sets": "https://www.victoriassecret.com/us/vs/sleepwear/pajama-shorts-sets",
                    "Slippers": "https://www.victoriassecret.com/us/vs/sleepwear/slippers",
                    "Loungewear": "https://www.victoriassecret.com/us/vs/sleepwear/loungewear"
                },
                "Group 3": {
                    "SoSoft\u2122 Modal": "https://www.victoriassecret.com/us/vs/sleepwear/modal",
                    "Signature Satin": "https://www.victoriassecret.com/us/vs/sleepwear/satin",
                    "Flannel": "https://www.victoriassecret.com/us/vs/sleepwear/flannel",
                    "Cotton": "https://www.victoriassecret.com/us/vs/sleepwear/cotton",
                    "New Silk": "https://www.victoriassecret.com/us/vs/sleepwear/washable-silk"
                },
                "Group 4": {
                    "Printed Pajamas": "https://www.victoriassecret.com/us/vs/sleepwear/printed-pajamas",
                    "Lunya": "https://www.victoriassecret.com/us/vs/sleepwear/lunya",
                    "Adore Me": "https://www.victoriassecret.com/us/vs/bras/adore-me?scroll=true&orderBy=REC&filter=category%3ASleep+%26+Lingerie",
                    "Papinelle": "https://www.victoriassecret.com/us/vs/sleepwear/papinelle"
                }
            }
        },
        "LINGERIE": {
            "path": "https://www.victoriassecret.com/us/vs/lingerie",
            "subcategories": {
                "Group 1": {
                    "ALL LINGERIE": "https://www.victoriassecret.com/us/vs/lingerie"
                },
                "Group 2": {
                    "Slips": "https://www.victoriassecret.com/us/vs/lingerie/slips",
                    "Babydolls": "https://www.victoriassecret.com/us/vs/lingerie/babydolls",
                    "Cami Sets": "https://www.victoriassecret.com/us/vs/lingerie/camisoles",
                    "Teddy Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/teddies-and-bodysuits",
                    "Robes": "https://www.victoriassecret.com/us/vs/lingerie/kimonos",
                    "Matching Sets": "https://www.victoriassecret.com/us/vs/lingerie/bras-and-panties",
                    "Bodysuits & Rompers": "https://www.victoriassecret.com/us/vs/lingerie/bodysuits",
                    "Corset Tops": "https://www.victoriassecret.com/us/vs/lingerie/corsets-and-bustiers",
                    "Wear-Out Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/very-sexy-collection",
                    "Shapewear": "https://www.victoriassecret.com/us/vs/shapewear",
                    "Garters & Stockings": "https://www.victoriassecret.com/us/vs/panties/garters",
                    "Bridal Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/bridal"
                },
                "Group 3": {
                    "Push-Up Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/push-up",
                    "Satin Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/satin",
                    "Lace Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/lace"
                },
                "Group 4": {
                    "The Halloween Edit": "https://www.victoriassecret.com/us/vs/lingerie/halloween",
                    "Tease Collection": "https://www.victoriassecret.com/us/vs/bras/tease",
                    "After Hours Lingerie": "https://www.victoriassecret.com/us/vs/lingerie/after-hours",
                    "New Silk Collection": "https://www.victoriassecret.com/us/vs/sleepwear/washable-silk",
                    "Bluebella": "https://www.victoriassecret.com/us/vs/lingerie/bluebella",
                    "Adore Me": "https://www.victoriassecret.com/us/vs/bras/adore-me",
                    "VS X Leonisa": "https://www.victoriassecret.com/us/vs/shapewear"
                }
            }
        },
        "CLOTHING": {
            "path": "https://www.victoriassecret.com/us/vs/apparel",
            "subcategories": {
                "Group 1": {
                    "ALL CLOTHING": "https://www.victoriassecret.com/us/vs/apparel",
                    "2/$59 Sexy Swim Separates": "https://www.victoriassecret.com/us/vs/swimwear/offer",
                    "ANGEL ESSENTIALS LOUNGEWEAR": "https://www.victoriassecret.com/us/vs/loungewear/angel-essentials",
                    "Matching Sets": "https://www.victoriassecret.com/us/vs/activewear/matching-sets"
                },
                "Group 2": {
                    "Dresses": "https://www.victoriassecret.com/us/vs/apparel/dresses",
                    "Loungewear": "https://www.victoriassecret.com/us/vs/loungewear",
                    "Tees & Tanks": "https://www.victoriassecret.com/us/vs/loungewear/tees-and-tank-tops",
                    "Sweatpants & Leggings": "https://www.victoriassecret.com/us/vs/loungewear/joggers-and-sweatpants",
                    "Sweatshirts": "https://www.victoriassecret.com/us/vs/loungewear/hoodies-and-sweatshirts",
                    "Sweaters & Cardigans": "https://www.victoriassecret.com/us/vs/loungewear/sweaters",
                    "Jeans": "https://www.victoriassecret.com/us/vs/apparel/denim",
                    "Shorts & Skirts": "https://www.victoriassecret.com/us/vs/loungewear/shorts",
                    "Jackets & Coats": "https://www.victoriassecret.com/us/vs/loungewear/jackets",
                    "Bodysuits": "https://www.victoriassecret.com/us/vs/loungewear/bodysuits",
                    "Swim & Cover-ups": "https://www.victoriassecret.com/us/vs/swimwear",
                    "Maternity": "https://www.victoriassecret.com/us/vs/apparel/maternity"
                },
                "Group 3": {
                    "The Halloween Edit": "https://www.victoriassecret.com/us/vs/lingerie/halloween",
                    "Sexy Night Out": "https://www.victoriassecret.com/us/vs/lingerie/night-out",
                    "Bridal Shop": "https://www.victoriassecret.com/us/vs/wedding-shop",
                    "Wedding Guest Dresses": "https://www.victoriassecret.com/us/vs/apparel/wedding-guest-dresses",
                    "Little Black Dresses": "https://www.victoriassecret.com/us/vs/apparel/little-black-dresses",
                    "Featherweight Knit": "https://www.victoriassecret.com/us/vs/activewear/featherweight-knit"
                },
                "Group 4": {
                    "Bardot": "https://www.victoriassecret.com/us/vs/apparel/bardot",
                    "Summer Away": "https://www.victoriassecret.com/us/vs/apparel/summer-away",
                    "Nia": "https://www.victoriassecret.com/us/vs/apparel/nia",
                    "Lulus": "https://www.victoriassecret.com/us/vs/apparel/lulus",
                    "AFRM": "https://www.victoriassecret.com/us/vs/apparel/afrm",
                    "ASTR the Label": "https://www.victoriassecret.com/us/vs/apparel/astr-the-label",
                    "Avec Les Filles": "https://www.victoriassecret.com/us/vs/apparel/avec-les-filles",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/vs/gift-cards"
                }
            }
        },
        "Activewear": {
            "path": "https://www.victoriassecret.com/us/vs/activewear",
            "subcategories": {
                "Group 1": {
                    "ALL ACTIVEWEAR": "https://www.victoriassecret.com/us/vs/activewear/vs-sport",
                    "NEW ARRIVALS": "https://www.victoriassecret.com/us/vs/activewear/new-arrivals",
                    "Up to 50% Off VSX": "https://www.victoriassecret.com/us/vs/activewear/offer",
                    "Buy 2 Bras, Get 1 Free": "https://www.victoriassecret.com/us/vs/bras/sports-bras"
                },
                "Group 2": {
                    "Sports Bras": "https://www.victoriassecret.com/us/vs/bras/sports-bras",
                    "Leggings": "https://www.victoriassecret.com/us/vs/activewear/leggings",
                    "Matching Sets": "https://www.victoriassecret.com/us/vs/activewear/matching-sets",
                    "Bottoms": "https://www.victoriassecret.com/us/vs/activewear/bottoms",
                    "Tops": "https://www.victoriassecret.com/us/vs/activewear/tops",
                    "Shorts": "https://www.victoriassecret.com/us/vs/activewear/biker-shorts",
                    "Jackets & Coats": "https://www.victoriassecret.com/us/vs/activewear/jackets",
                    "Dresses and Jumpsuits": "https://www.victoriassecret.com/us/vs/activewear/dresses-and-jumpsuits",
                    "Sneakers": "https://www.victoriassecret.com/us/vs/shoes/sneakers",
                    "Sport Panties": "https://www.victoriassecret.com/us/vs/panties/sport-panties"
                },
                "Group 3": {
                    "VSX Elevate\u2122": "https://www.victoriassecret.com/us/vs/activewear/the-elevate-collection",
                    "VSX New Essential": "https://www.victoriassecret.com/us/vs/activewear/the-luxmarl-collection",
                    "Featherweight Knit": "https://www.victoriassecret.com/us/vs/activewear/featherweight-knit",
                    "VSX GlossyTech\u2122": "https://www.victoriassecret.com/us/vs/activewear/trending-now",
                    "Featherweight Sports Bras": "https://www.victoriassecret.com/us/vs/activewear/featherweight-max-sports-bra",
                    "Angel Essentials Loungewear": "https://www.victoriassecret.com/us/vs/loungewear/angel-essentials"
                }
            }
        },
        "ACCESSORIES": {
            "path": "https://www.victoriassecret.com/us/vs/accessories",
            "subcategories": {
                "Group 1": {
                    "ALL ACCESSORIES": "https://www.victoriassecret.com/us/vs/accessories",
                    "Tote Bags": "https://www.victoriassecret.com/us/vs/accessories/tote-bags",
                    "Fall's Favorite UGGs": "https://www.victoriassecret.com/us/vs/shoes/ugg"
                },
                "Group 2": {
                    "Bags": "https://www.victoriassecret.com/us/vs/accessories/all-bags",
                    "Makeup Bags": "https://www.victoriassecret.com/us/vs/accessories/cosmetic-bags",
                    "Keychains & Charms": "https://www.victoriassecret.com/us/vs/accessories/charms-and-keychains",
                    "Luggage & Travel": "https://www.victoriassecret.com/us/vs/accessories/luggage-and-travel",
                    "Socks & Stockings": "https://www.victoriassecret.com/us/vs/accessories/socks",
                    "Wallets & Card Cases": "https://www.victoriassecret.com/us/vs/accessories/wallets",
                    "Jewelry": "https://www.victoriassecret.com/us/vs/accessories/jewelry",
                    "Hats & Hair Accessories": "https://www.victoriassecret.com/us/vs/accessories/hats",
                    "Sunglasses": "https://www.victoriassecret.com/us/vs/accessories/sunglasses",
                    "Candles": "https://www.victoriassecret.com/us/vs/beauty/candles"
                },
                "Group 3": {
                    "ALL SHOES": "https://www.victoriassecret.com/us/vs/shoes/footwear",
                    "Boots": "https://www.victoriassecret.com/us/vs/shoes/boots",
                    "Sandals": "https://www.victoriassecret.com/us/vs/shoes/sandals",
                    "Slippers": "https://www.victoriassecret.com/us/vs/shoes/slippers",
                    "Sneakers": "https://www.victoriassecret.com/us/vs/shoes/sneakers",
                    "Heels": "https://www.victoriassecret.com/us/vs/shoes/heels",
                    "Clogs & Slides": "https://www.victoriassecret.com/us/vs/shoes/clogs"
                },
                "Group 4": {
                    "The Heritage Stripe Shop": "https://www.victoriassecret.com/us/vs/accessories/heritage-stripe-shop",
                    "UGG": "https://www.victoriassecret.com/us/vs/shoes/ugg",
                    "Hunter": "https://www.victoriassecret.com/us/pink/shoes/hunter",
                    "Birkenstock": "https://www.victoriassecret.com/us/vs/shoes/birkenstock",
                    "PUMA": "https://www.victoriassecret.com/us/vs/shoes/puma",
                    "Steve Madden": "https://www.victoriassecret.com/us/vs/shoes/steve-madden",
                    "Dolce Vita": "https://www.victoriassecret.com/us/vs/shoes/dolce-vita",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/vs/gift-cards"
                }
            }
        },
        "FASHION SHOW": {
            "path": "https://www.victoriassecret.com/us/vs/vsinsider/fashionshow",
            "subcategories": {
                "Group 1": {
                    "Shop Backstage Fashion Show Merch": "https://www.victoriassecret.com/us/vs/newarrivals/vs-icon-shoppe",
                    "Learn More": "https://www.victoriassecret.com/us/vs/vsinsider/fashionshow"
                }
            }
        },
        "SALE": {
            "path": "https://www.victoriassecret.com/us/vs/sale",
            "subcategories": {
                "Group 1": {
                    "UP TO 50% OFF SALE": "https://www.victoriassecret.com/us/vs/sale"
                },
                "Group 2": {
                    "Bras": "https://www.victoriassecret.com/us/vs/sale/clearance-bras",
                    "Panties": "https://www.victoriassecret.com/us/vs/sale/clearance-panties",
                    "Sleep": "https://www.victoriassecret.com/us/vs/sale/clearance-sleep",
                    "Activewear": "https://www.victoriassecret.com/us/vs/sale/clearance-sport",
                    "Beauty": "https://www.victoriassecret.com/us/vs/sale/clearance-beauty",
                    "Lingerie": "https://www.victoriassecret.com/us/vs/sale/clearance-lingerie",
                    "Clothing": "https://www.victoriassecret.com/us/vs/sale/clearance-clothing",
                    "Swim": "https://www.victoriassecret.com/us/vs/sale/clearance-swim",
                    "Accessories": "https://www.victoriassecret.com/us/vs/sale/clearance-accessories",
                    "Home Fragrance": "https://www.victoriassecret.com/us/vs/sale/clearance-home-fragrance",
                    "Brands We Love": "https://www.victoriassecret.com/us/vs/sale/brands-we-love-sale",
                    "Adore Me": "https://www.victoriassecret.com/us/vs/sale/adore-me"
                }
            }
        }
    },
    "pink": {
        "PINK HALFTIME SHOW": {
            "path": "https://www.victoriassecret.com/us/pink/fashion-show",
            "subcategories": {
                "Group 1": {
                    "LEARN MORE": "https://www.victoriassecret.com/us/pink/fashion-show",
                    "THE PREGAME": "https://www.victoriassecret.com/us/pink/fashion-show/shop-the-show"
                }
            }
        },
        "NEW!": {
            "path": "https://www.victoriassecret.com/us/pink/new-arrivals",
            "subcategories": {
                "Group 1": {
                    "NEW ARRIVALS": "https://www.victoriassecret.com/us/pink/new-arrivals",
                    "PINK Wednesday Drop": "https://www.victoriassecret.com/us/pink/new-arrivals/wednesday-drop",
                    "Best Sellers": "https://www.victoriassecret.com/us/pink/best-sellers"
                },
                "Group 2": {
                    "Secret Menu": "https://www.victoriassecret.com/us/pink/new-arrivals/online-exclusives",
                    "Halloween": "https://www.victoriassecret.com/us/pink/new-arrivals/halloween-shop",
                    "PINK College Collection": "https://www.victoriassecret.com/us/pink/collabs/collegiate-collection",
                    "PINK Logo Shop": "https://www.victoriassecret.com/us/pink/new-arrivals/classic-pink-shop",
                    "Bling, Sparkle & Shine": "https://www.victoriassecret.com/us/pink/new-arrivals/sparkle-and-shine",
                    "As Seen on Social": "https://www.victoriassecret.com/us/pink/new-arrivals/as-seen-on-tiktok",
                    "Game Day": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/game-day"
                },
                "Group 3": {
                    "UGG": "https://www.victoriassecret.com/us/pink/shoes/ugg-boots",
                    "Birkenstock": "https://www.victoriassecret.com/us/pink/shoes/birkenstock",
                    "Puma": "https://www.victoriassecret.com/us/pink/shoes/puma",
                    "Steve Madden": "https://www.victoriassecret.com/us/pink/shoes/steve-madden",
                    "Hunter": "https://www.victoriassecret.com/us/pink/shoes/hunter",
                    "GIFTS": "https://www.victoriassecret.com/us/pink/gifts",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/pink/gift-cards"
                }
            }
        },
        "CLOTHING": {
            "path": "https://www.victoriassecret.com/us/pink/tops-and-bottoms",
            "subcategories": {
                "Group 1": {
                    "ALL CLOTHING": "https://www.victoriassecret.com/us/pink/tops-and-bottoms"
                },
                "Group 2": {
                    "Foldover Faves": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/foldover-faves",
                    "Going Out Clothes": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/going-out-clothes",
                    "Secret Menu": "https://www.victoriassecret.com/us/pink/new-arrivals/online-exclusives",
                    "Matching Sets": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/matching-sets",
                    "NEW: Waffle Lounge": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/cozy",
                    "PINK College Collection": "https://www.victoriassecret.com/us/pink/collabs/collegiate-collection",
                    "NFL Collection": "https://www.victoriassecret.com/us/pink/collabs/nfl-collection"
                },
                "Group 3": {
                    "Sweatshirts & Hoodies": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/sweatshirts",
                    "T-Shirts": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/tees",
                    "Tank Tops": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/tank-tops",
                    "Going Out Tops": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/going-out",
                    "Sweaters": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/sweaters",
                    "Outerwear": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/outerwear",
                    "DRESSES": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/dresses"
                },
                "Group 4": {
                    "Sweatpants & Joggers": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/sweatpants",
                    "Leggings": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/leggings",
                    "Flares": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/flares",
                    "Denim": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/denim",
                    "Shorts": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/shorts",
                    "Skirts": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/skirts",
                    "Pants": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/pants",
                    "Capris": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/capris"
                },
                "Group 5": {
                    "Campus Fleece\u2122 & Campus Cotton\u2122": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/campus-cotton",
                    "All Day Cotton\u2122": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/all-day-cotton",
                    "PINK Base Stretch\u2122": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/base-stretch",
                    "$35 Sweatshirts & Sweatpants": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/apparel-offer",
                    "$25 Tees": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/offer",
                    "40% off Denim": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/special-offer",
                    "$35 Cotton Foldover Flare": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/select-styles",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/pink/gift-cards"
                }
            }
        },
        "BRAS": {
            "path": "https://www.victoriassecret.com/us/pink/bras",
            "subcategories": {
                "Group 1": {
                    "ALL BRAS: AA-G CUPS": "https://www.victoriassecret.com/us/pink/bras"
                },
                "Group 2": {
                    "Push-Up": "https://www.victoriassecret.com/us/pink/bras/push-up",
                    "Super Push-Up": "https://www.victoriassecret.com/us/pink/bras/super-push-up",
                    "T-Shirt & Lightly Lined": "https://www.victoriassecret.com/us/pink/bras/lightly-lined",
                    "Wireless": "https://www.victoriassecret.com/us/pink/bras/wireless-styles",
                    "Strapless & Backless": "https://www.victoriassecret.com/us/pink/bras/strapless",
                    "Bralettes": "https://www.victoriassecret.com/us/pink/bras/bralette",
                    "Sports Bras": "https://www.victoriassecret.com/us/pink/bras/sport-bras-collection",
                    "Unlined": "https://www.victoriassecret.com/us/pink/bras/unlined",
                    "Bra Tops": "https://www.victoriassecret.com/us/pink/bras/bra-tops",
                    "Balconette": "https://www.victoriassecret.com/us/pink/bras/balconette",
                    "Bra & Panty Sets": "https://www.victoriassecret.com/us/pink/bras/matching-sets",
                    "Adaptive Bras & Panties": "https://www.victoriassecret.com/us/pink/bras/adaptive"
                },
                "Group 3": {
                    "Marshmallow Bras: Comfy & Cute": "https://www.victoriassecret.com/us/pink/bras/comfy-marshmallow",
                    "Wear Everywhere\u2122: Everyday Faves": "https://www.victoriassecret.com/us/pink/bras/all-wear-everywhere-special-pink",
                    "PINK Wink\u2122: Fun & Flirty": "https://www.victoriassecret.com/us/pink/bras/the-wink",
                    "PINK Relay\u2122: Sporty Faves": "https://www.victoriassecret.com/us/pink/sport/relay-collection?scroll=true&orderBy=REC&filter=subclass%3ASports%20Bras",
                    "Meet Our Bras": "https://www.victoriassecret.com/us/pink/bras/meet-our-bras",
                    "How to Measure Bra Size": "https://www.victoriassecret.com/us/pink/bras/how-to-measure"
                },
                "Group 4": {
                    "Bras from $25": "https://www.victoriassecret.com/us/pink/bras/offer",
                    "2/$42 Sports Bras": "https://www.victoriassecret.com/us/pink/bras/sport-bra-offer",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/pink/gift-cards"
                }
            }
        },
        "PANTIES": {
            "path": "https://www.victoriassecret.com/us/pink/underwear",
            "subcategories": {
                "Group 1": {
                    "ALL PANTIES: XXS-XXL": "https://www.victoriassecret.com/us/pink/underwear"
                },
                "Group 2": {
                    "Thongs & V-Strings": "https://www.victoriassecret.com/us/pink/underwear/thong-underwear",
                    "Cheekies": "https://www.victoriassecret.com/us/pink/underwear/cheekster-underwear",
                    "Boyshorts": "https://www.victoriassecret.com/us/pink/underwear/boyshort-underwear",
                    "Hiphuggers": "https://www.victoriassecret.com/us/pink/underwear/hipster-underwear",
                    "Bikinis": "https://www.victoriassecret.com/us/pink/underwear/bikini-underwear",
                    "Panty Packs": "https://www.victoriassecret.com/us/pink/underwear/underwear-packs",
                    "Brazilians": "https://www.victoriassecret.com/us/pink/underwear/brazilian-underwear",
                    "Period Panties": "https://www.victoriassecret.com/us/pink/underwear/leak-proof-period-underwear",
                    "Bra & Panty Sets": "https://www.victoriassecret.com/us/pink/bras/matching-sets",
                    "Adaptive Bras & Panties": "https://www.victoriassecret.com/us/pink/bras/adaptive"
                },
                "Group 3": {
                    "Our #1 Collection: No-Show": "https://www.victoriassecret.com/us/pink/underwear/no-show-underwear",
                    "Cotton": "https://www.victoriassecret.com/us/pink/underwear/cotton-underwear",
                    "Lace": "https://www.victoriassecret.com/us/pink/underwear/lace-underwear",
                    "Seamless": "https://www.victoriassecret.com/us/pink/underwear/seamless-collection",
                    "Ultra-Low Rise": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#ultra-low",
                    "Low Rise": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#low",
                    "Mid Rise": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#mid",
                    "High Rise": "https://www.victoriassecret.com/us/pink/underwear/low-mid-high-rise-underwear?scroll=true#high"
                },
                "Group 4": {
                    "8/$38 Panties": "https://www.victoriassecret.com/us/pink/underwear/underwear-offer",
                    "Panty Packs from $35": "https://www.victoriassecret.com/us/pink/underwear/underwear-packs",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/pink/gift-cards"
                }
            }
        },
        "SLEEP": {
            "path": "https://www.victoriassecret.com/us/pink/sleepwear",
            "subcategories": {
                "Group 1": {
                    "ALL SLEEP": "https://www.victoriassecret.com/us/pink/sleepwear"
                },
                "Group 2": {
                    "Mix & Match Pajamas": "https://www.victoriassecret.com/us/pink/sleepwear/mix-and-match",
                    "Pajama Sets": "https://www.victoriassecret.com/us/pink/sleepwear/sets",
                    "Pajama Tops": "https://www.victoriassecret.com/us/pink/sleepwear/tops",
                    "Pajama Bottoms": "https://www.victoriassecret.com/us/pink/sleepwear/bottoms",
                    "Robes, Slippers, & Socks": "https://www.victoriassecret.com/us/pink/sleepwear/robes-socks-and-slippers"
                },
                "Group 3": {
                    "New: Flannel": "https://www.victoriassecret.com/us/pink/sleepwear/flannel",
                    "Modal": "https://www.victoriassecret.com/us/pink/sleepwear/modal",
                    "Cotton": "https://www.victoriassecret.com/us/pink/sleepwear/cotton"
                },
                "Group 4": {
                    "2/$45 Sleep": "https://www.victoriassecret.com/us/pink/sleepwear/special-offer",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/pink/gift-cards"
                }
            }
        },
        "ACTIVEWEAR": {
            "path": "https://www.victoriassecret.com/us/pink/sport",
            "subcategories": {
                "Group 1": {
                    "All Activewear": "https://www.victoriassecret.com/us/pink/sport"
                },
                "Group 2": {
                    "Leggings": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/leggings",
                    "Sports Bras": "https://www.victoriassecret.com/us/pink/bras/sport-bras-collection",
                    "Flare Leggings": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/yoga-pants",
                    "Athletic Shorts": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/biker-shorts",
                    "Sport Jackets": "https://www.victoriassecret.com/us/pink/sport/jackets",
                    "Workout Tops": "https://www.victoriassecret.com/us/pink/sport/workout-tops",
                    "Sneakers": "https://www.victoriassecret.com/us/pink/accessories/sneakers",
                    "Sport Panties": "https://www.victoriassecret.com/us/pink/underwear/sport-underwear"
                },
                "Group 3": {
                    "PINK Relay\u2122": "https://www.victoriassecret.com/us/pink/sport/relay-collection",
                    "All-Day Cotton\u2122": "https://www.victoriassecret.com/us/pink/tops-and-bottoms/all-day-cotton"
                },
                "Group 4": {
                    "2/$42 Sports Bras": "https://www.victoriassecret.com/us/pink/bras/sport-bra-offer",
                    "GIFT CARDS": "https://www.victoriassecret.com/us/pink/gift-cards"
                }
            }
        },
        "ACCESSORIES": {
            "path": "https://www.victoriassecret.com/us/pink/accessories",
            "subcategories": {
                "Group 1": {
                    "ALL ACCESSORIES": "https://www.victoriassecret.com/us/pink/accessories",
                    "ALL SHOES": "https://www.victoriassecret.com/us/pink/shoes/footwear",
                    "Slipper Szn": "https://www.victoriassecret.com/us/pink/shoes/slippers",
                    "Hot RN: UGG": "https://www.victoriassecret.com/us/pink/shoes/ugg-boots",
                    "The PINK Pup Shop": "https://www.victoriassecret.com/us/pink/accessories/pet-accessories",
                    "Travel Accessories": "https://www.victoriassecret.com/us/pink/accessories/travel"
                },
                "Group 2": {
                    "BAGS": "https://www.victoriassecret.com/us/pink/accessories/bags",
                    "Totes\u200b": "https://www.victoriassecret.com/us/pink/accessories/tote-bags",
                    "Backpacks": "https://www.victoriassecret.com/us/pink/accessories/backpacks",
                    "Shoulder & Crossbody": "https://www.victoriassecret.com/us/pink/accessories/crossbody-bags",
                    "Travel Bags": "https://www.victoriassecret.com/us/pink/accessories/travel-bags",
                    "Makeup & Beauty Bags": "https://www.victoriassecret.com/us/pink/accessories/makeup-bags",
                    "Keychains & Bag Charms": "https://www.victoriassecret.com/us/pink/accessories/keychains",
                    "Stackable Jewelry": "https://www.victoriassecret.com/us/pink/accessories/jewelry",
                    "Socks": "https://www.victoriassecret.com/us/pink/accessories/socks-and-slippers",
                    "Hats & Hair Accessories": "https://www.victoriassecret.com/us/pink/accessories/hats",
                    "Sunglasses": "https://www.victoriassecret.com/us/pink/accessories/sunglasses"
                },
                "Group 3": {
                    "SHOES": "https://www.victoriassecret.com/us/pink/shoes/footwear",
                    "Boots": "https://www.victoriassecret.com/us/pink/shoes/boots",
                    "Slippers": "https://www.victoriassecret.com/us/pink/shoes/slippers",
                    "Sneakers": "https://www.victoriassecret.com/us/pink/shoes/sneakers",
                    "Clogs": "https://www.victoriassecret.com/us/pink/shoes/clogs",
                    "Flats": "https://www.victoriassecret.com/us/pink/shoes/flats-and-loafers",
                    "Sandals & Flip-Flops": "https://www.victoriassecret.com/us/pink/shoes/sandals",
                    "Birkenstock": "https://www.victoriassecret.com/us/pink/shoes/birkenstock",
                    "UGG": "https://www.victoriassecret.com/us/pink/shoes/ugg-boots",
                    "PUMA": "https://www.victoriassecret.com/us/pink/shoes/puma",
                    "Hunter": "https://www.victoriassecret.com/us/pink/shoes/hunter",
                    "Crocs": "https://www.victoriassecret.com/us/pink/shoes/crocs",
                    "Steve Madden": "https://www.victoriassecret.com/us/pink/shoes/steve-madden"
                },
                "Group 4": {
                    "Bags from $30": "https://www.victoriassecret.com/us/pink/accessories/offer",
                    "2/$30 Bag Charms & More\u200b": "https://www.victoriassecret.com/us/pink/accessories/keychains",
                    "Socks from $7": "https://www.victoriassecret.com/us/pink/accessories/accessories-offer",
                    "2/$40 Little Words Project Bracelets": "https://www.victoriassecret.com/us/pink/accessories/little-words-project"
                }
            }
        },
        "BEAUTY": {
            "path": "https://www.victoriassecret.com/us/pink/beauty",
            "subcategories": {
                "Group 1": {
                    "All Beauty": "https://www.victoriassecret.com/us/pink/beauty"
                },
                "Group 2": {
                    "Perfume": "https://www.victoriassecret.com/us/pink/beauty/perfume",
                    "Hair & Body Mists": "https://www.victoriassecret.com/us/pink/beauty/mists",
                    "Lotions & Oils": "https://www.victoriassecret.com/us/pink/beauty/body-lotion",
                    "Scrubs & Washes": "https://www.victoriassecret.com/us/pink/beauty/beauty-body-wash",
                    "Body Oil": "https://www.victoriassecret.com/us/pink/beauty/body-oil",
                    "Lip": "https://www.victoriassecret.com/us/pink/beauty/lip",
                    "Minis & Travel-Size": "https://www.victoriassecret.com/us/pink/beauty/beauty-on-the-go"
                },
                "Group 3": {
                    "Fruity": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#fruity",
                    "Vanilla": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#vanilla",
                    "Warm": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#warm",
                    "Fresh": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists#fresh"
                },
                "Group 4": {
                    "$10 Full-Sized": "https://www.victoriassecret.com/us/pink/beauty/select-styles",
                    "Build Your Routine": "https://www.victoriassecret.com/us/pink/beauty/build-your-routine",
                    "New Arrivals": "https://www.victoriassecret.com/us/pink/beauty/limited-edition",
                    "Scent Finder": "https://www.victoriassecret.com/us/pink/beauty/fragrances-and-body-mists",
                    "Shimmer Shop": "https://www.victoriassecret.com/us/pink/beauty/body-spray-and-shimmer",
                    "Body Care Shop": "https://www.victoriassecret.com/us/pink/beauty/body-care"
                }
            }
        },
        "GIFTS": {
            "path": "https://www.victoriassecret.com/us/pink/gifts"
        },
        "SALE": {
            "path": "https://www.victoriassecret.com/us/pink/all-sale-pink",
            "subcategories": {
                "Group 1": {
                    "All Sale": "https://www.victoriassecret.com/us/pink/all-sale-pink"
                },
                "Group 2": {
                    "Clothing": "https://www.victoriassecret.com/us/pink/all-sale-pink/apparel-sale",
                    "Bras": "https://www.victoriassecret.com/us/pink/all-sale-pink/bras-sale",
                    "Panties": "https://www.victoriassecret.com/us/pink/all-sale-pink/underwear-sale",
                    "Sleep": "https://www.victoriassecret.com/us/pink/all-sale-pink/sleep-sale",
                    "Activewear": "https://www.victoriassecret.com/us/pink/all-sale-pink/activewear-sale",
                    "Swim": "https://www.victoriassecret.com/us/pink/all-sale-pink/swim-sale",
                    "Shoes & Accessories": "https://www.victoriassecret.com/us/pink/all-sale-pink/accessories-sale",
                    "Beauty": "https://www.victoriassecret.com/us/pink/all-sale-pink/beauty-sale",
                    "Brands We Love": "https://www.victoriassecret.com/us/pink/all-sale-pink/brands-we-love"
                }
            }
        }
    }
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def load_categories() -> list[dict[str, str]]:
    """Flatten the navigation tree into canonical listing categories."""
    flat: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(
        slug: str,
        brand: str,
        top: str,
        sub: str | None,
        url: str,
    ) -> None:
        if not url or not url.startswith("http") or slug in seen:
            return
        seen.add(slug)
        entry = {
            "category": slug,
            "brand": brand,
            "top_category": top,
            "department": f"{brand}-{slugify(top)}",
            "url": url,
        }
        if sub:
            entry["sub_category"] = sub
        flat.append(entry)

    for brand, tops in VICTORIASSECRET_CATEGORIES.items():
        for top_name, top_data in tops.items():
            top_url = top_data.get("path") or ""
            if not top_url:
                continue
            top_slug = f"{brand}-{slugify(top_name)}"
            add(top_slug, brand, top_name, None, top_url)
            for group_name, group_data in top_data.get(
                "subcategories", {}
            ).items():
                if not isinstance(group_data, dict):
                    group_data = {group_name: group_data}
                for sub_name, sub_url in group_data.items():
                    if not isinstance(sub_url, str) or sub_url == top_url:
                        continue
                    add(
                        f"{top_slug}-{slugify(sub_name)}",
                        brand,
                        top_name,
                        sub_name,
                        sub_url,
                    )

    return flat


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
