"""Stable Superdrug UK product-listing categories.

Keys match the final ``/c/<code>`` path segment used by the storefront and by
the Angular listing bootstrap.  A dictionary is intentional: it keeps CLI
lookup deterministic and makes duplicate category codes impossible.
"""

SUPERDRUG_CATEGORIES: dict[str, str] = {
    "health-winter": "https://www.superdrug.com/health/cough-cold-flu/c/health-winter",
    "health-allergy": "https://www.superdrug.com/health/allergy-hayfever/c/health-allergy",
    "health-painrelief": "https://www.superdrug.com/health/pain-relief/c/health-painrelief",
    "health-vitamins": "https://www.superdrug.com/health/vitamins-supplements/c/health-vitamins",
    "health-skintreatments": "https://www.superdrug.com/health/medicated-skin/c/health-skintreatments",
    "makeup": "https://www.superdrug.com/make-up/c/makeup",
    "k-beauty": "https://www.superdrug.com/skin/korean-japanese-beauty/c/k-beauty",
    "kj-beauty": "https://www.superdrug.com/make-up/korean-japanese-makeup/c/kj-beauty",
    "fragranceforher": "https://www.superdrug.com/fragrance/perfume-for-women/c/fragranceforher",
    "gift-sets-fragrance": "https://www.superdrug.com/fragrance/fragrance-gift-sets/c/gift-sets-fragrance",
    "hair-treatments": "https://www.superdrug.com/hair/hair-treatments/c/hair-treatments",
    "toil-deodorants": "https://www.superdrug.com/toiletries/deodorants/c/toil-deodorants",
    "teeth-whitening": "https://www.superdrug.com/toiletries/dental/teeth-whitening/c/teeth-whitening",
    "womenswear": "https://www.superdrug.com/fashion/womenswear/c/womenswear",
    "menswear": "https://www.superdrug.com/fashion/menswear/c/menswear",
    "childrenswear": "https://www.superdrug.com/fashion/childrenswear/c/childrenswear",
    "pharmacy-medicines": "https://www.superdrug.com/pharmacy-medicines/c/pharmacy-medicines",
    "mens": "https://www.superdrug.com/mens/c/mens",
    "beauty-electricals-hair-styling": (
        "https://www.superdrug.com/electricals/beauty-electricals-hair-styling/"
        "c/beauty-electricals-hair-styling"
    ),
    "audio-technology": "https://www.superdrug.com/electricals/audio-technology/c/audio-technology",
    "jewellery": "https://www.superdrug.com/jewellery/c/jewellery",
    "pt-watches": "https://www.superdrug.com/jewellery/watches/c/pt-watches",
    "web-gifts": "https://www.superdrug.com/gifts/c/web-gifts",
    "bundles": "https://www.superdrug.com/bundles-supersize/c/bundles",
    "trends": "https://www.superdrug.com/trending-right-now/c/trends",
    "new-personal-care": "https://www.superdrug.com/new-personal-care/c/new-personal-care",
    "new-in-health-care": "https://www.superdrug.com/new-in-health-care/c/new-in-health-care",
    "members-only-offers": "https://www.superdrug.com/exclusive-members-only-offers/c/members-only-offers",
}
