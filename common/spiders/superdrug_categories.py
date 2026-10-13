"""Stable Superdrug UK product-listing categories, grouped by department.

Every leaf is a crawlable ``/{breadcrumb...}/c/{slug}`` product-listing route.
The Airflow DAG schedules one task per leaf and the GCS output path is the bare
leaf name, so leaf keys are globally unique (the sample already keys them by the
storefront ``c/<slug>`` code, which is unique across departments).

The grouping is the storefront top-level department (first URL path segment);
each leaf value keeps its canonical ``url``. Captured 2026-10-09 from the
Superdrug storefront navigation (``sample/superdrug-category-dict.json``,
163 categories across 63 departments).
"""
from __future__ import annotations

SUPERDRUG_CATEGORIES: dict[str, dict[str, str]] = {
    '5-friday-deals': {
        'five-pound-friday': 'https://www.superdrug.com/5-friday-deals/c/five-pound-friday',
    },
    'accessories-and-lifestyle': {
        'accessories-and-lifestyle': 'https://www.superdrug.com/accessories-and-lifestyle/c/accessories-and-lifestyle',
        'pt-stationery': 'https://www.superdrug.com/accessories-and-lifestyle/stationery/c/pt-stationery',
    },
    'arabian-fragrance': {
        'ouds': 'https://www.superdrug.com/arabian-fragrance/c/ouds',
    },
    'b-menopause': {
        'b-menopause': 'https://www.superdrug.com/b-menopause/c/b-menopause',
    },
    'b-skincare-age-define': {
        'bskincare-age-define': 'https://www.superdrug.com/b-skincare-age-define/c/bskincare-age-define',
    },
    'b-skincare-cleanse': {
        'bskincare-cleanse': 'https://www.superdrug.com/b-skincare-cleanse/c/bskincare-cleanse',
    },
    'b-skincare-glow': {
        'bskincare-glow': 'https://www.superdrug.com/b-skincare-glow/c/bskincare-glow',
    },
    'b-skincare-hydrate': {
        'bskincare-hydrate': 'https://www.superdrug.com/b-skincare-hydrate/c/bskincare-hydrate',
    },
    'bundles-supersize': {
        'bundles': 'https://www.superdrug.com/bundles-supersize/c/bundles',
    },
    'electricals': {
        'audio-technology': 'https://www.superdrug.com/electricals/audio-technology/c/audio-technology',
        'beauty-electricals-hair-styling': 'https://www.superdrug.com/electricals/beauty-electricals-hair-styling/c/beauty-electricals-hair-styling',
        'electrical-wellbeing': 'https://www.superdrug.com/electricals/electrical-wellbeing/c/electrical-wellbeing',
        'heating-cooling': 'https://www.superdrug.com/electricals/fans-heaters-dehumidifiers/c/heating-cooling',
        'new-electricals': 'https://www.superdrug.com/electricals/new-electricals/c/new-electricals',
        'tech-accessories': 'https://www.superdrug.com/electricals/tech-accessories/c/tech-accessories',
    },
    'energy-hydration-and-electrolytes': {
        'energy-hydration-and-electrolytes': 'https://www.superdrug.com/energy-hydration-and-electrolytes/c/energy-hydration-and-electrolytes',
    },
    'exclusive-members-only-offers': {
        'members-only-offers': 'https://www.superdrug.com/exclusive-members-only-offers/c/members-only-offers',
    },
    'exclusive-to-superdrug': {
        'view_all_exclusives': 'https://www.superdrug.com/exclusive-to-superdrug/c/view_all_exclusives',
    },
    'extracts-body-cream': {
        'superdrug-extracts-body-cream': 'https://www.superdrug.com/extracts-body-cream/c/superdrug-extracts-body-cream',
    },
    'extracts-body-scrub': {
        'superdrug-extracts-body-scrub': 'https://www.superdrug.com/extracts-body-scrub/c/superdrug-extracts-body-scrub',
    },
    'extracts-hand-care': {
        'superdrug-extracts-hand-care': 'https://www.superdrug.com/extracts-hand-care/c/superdrug-extracts-hand-care',
    },
    'fashion': {
        'childrenswear': 'https://www.superdrug.com/fashion/childrenswear/c/childrenswear',
        'menswear': 'https://www.superdrug.com/fashion/menswear/c/menswear',
        'pt_mens_accessories': 'https://www.superdrug.com/fashion/menswear/mens-accessories/c/pt_mens_accessories',
        'pt_mens_coats_and_jackets': 'https://www.superdrug.com/fashion/menswear/mens-coats-jackets/c/pt_mens_coats_and_jackets',
        'pt_mens_footwear': 'https://www.superdrug.com/fashion/menswear/mens-footwear/c/pt_mens_footwear',
        'pt_mens_jeans': 'https://www.superdrug.com/fashion/menswear/mens-jeans/c/pt_mens_jeans',
        'pt_mens_joggers': 'https://www.superdrug.com/fashion/menswear/mens-joggers/c/pt_mens_joggers',
        'pt_mens_jumpers_and_cardigans': 'https://www.superdrug.com/fashion/menswear/mens-jumpers-cardigans/c/pt_mens_jumpers_and_cardigans',
        'pt_mens_shirts': 'https://www.superdrug.com/fashion/menswear/mens-shirts/c/pt_mens_shirts',
        'pt_mens_shorts': 'https://www.superdrug.com/fashion/menswear/mens-shorts/c/pt_mens_shorts',
        'pt_mens_socks': 'https://www.superdrug.com/fashion/menswear/mens-socks/c/pt_mens_socks',
        'pt_mens_sportswear': 'https://www.superdrug.com/fashion/menswear/mens-sportswear/c/pt_mens_sportswear',
        'pt_mens_swimwear': 'https://www.superdrug.com/fashion/menswear/mens-swimwear/c/pt_mens_swimwear',
        'pt_mens_tops': 'https://www.superdrug.com/fashion/menswear/mens-tops/c/pt_mens_tops',
        'pt_mens_trousers': 'https://www.superdrug.com/fashion/menswear/mens-trousers/c/pt_mens_trousers',
        'pt_mens_underwear': 'https://www.superdrug.com/fashion/menswear/mens-underwear/c/pt_mens_underwear',
        'womenswear': 'https://www.superdrug.com/fashion/womenswear/c/womenswear',
        'pt_womens_fashion_accessories': 'https://www.superdrug.com/fashion/womenswear/womens-accessories/c/pt_womens_fashion_accessories',
        'pt_womens_co_ords': 'https://www.superdrug.com/fashion/womenswear/womens-co-ords/c/pt_womens_co_ords',
        'pt_womens_coats_and_jackets': 'https://www.superdrug.com/fashion/womenswear/womens-coats-and-jackets/c/pt_womens_coats_and_jackets',
        'pt_womens_dresses': 'https://www.superdrug.com/fashion/womenswear/womens-dresses/c/pt_womens_dresses',
        'pt_womens_fancy_dress': 'https://www.superdrug.com/fashion/womenswear/womens-fancy-dress/c/pt_womens_fancy_dress',
        'pt_womens_footwear': 'https://www.superdrug.com/fashion/womenswear/womens-footwear/c/pt_womens_footwear',
        'pt_womens_jeans': 'https://www.superdrug.com/fashion/womenswear/womens-jeans/c/pt_womens_jeans',
        'pt_womens_jumpsuits_and_playsuits': 'https://www.superdrug.com/fashion/womenswear/womens-jumpsuits-playsuits/c/pt_womens_jumpsuits_and_playsuits',
        'pt_womens_knitwear': 'https://www.superdrug.com/fashion/womenswear/womens-knitwear/c/pt_womens_knitwear',
        'pt_womens_lingerie': 'https://www.superdrug.com/fashion/womenswear/womens-lingerie/c/pt_womens_lingerie',
        'pt_womens_pyjamas_and_nightwear': 'https://www.superdrug.com/fashion/womenswear/womens-pyjamas-nightwear/c/pt_womens_pyjamas_and_nightwear',
        'pt_womens_shorts': 'https://www.superdrug.com/fashion/womenswear/womens-shorts/c/pt_womens_shorts',
        'pt_womens_skirts': 'https://www.superdrug.com/fashion/womenswear/womens-skirts/c/pt_womens_skirts',
        'pt_womens_socks_and_tights': 'https://www.superdrug.com/fashion/womenswear/womens-socks-tights/c/pt_womens_socks_and_tights',
        'pt_womens_sportswear': 'https://www.superdrug.com/fashion/womenswear/womens-sportswear/c/pt_womens_sportswear',
        'pt_womens_sweatshirts_and_hoodies': 'https://www.superdrug.com/fashion/womenswear/womens-sweatshirts-hoodies/c/pt_womens_sweatshirts_and_hoodies',
        'pt_womens_swim_and_beachwear': 'https://www.superdrug.com/fashion/womenswear/womens-swim-beachwear/c/pt_womens_swim_and_beachwear',
        'pt_womens_tops': 'https://www.superdrug.com/fashion/womenswear/womens-tops/c/pt_womens_tops',
        'pt_womens_trousers': 'https://www.superdrug.com/fashion/womenswear/womens-trousers/c/pt_womens_trousers',
    },
    'fitness-equipment-and-scales': {
        'fitness-equipment-and-scales': 'https://www.superdrug.com/fitness-equipment-and-scales/c/fitness-equipment-and-scales',
    },
    'fragrance': {
        'gift-sets-fragrance': 'https://www.superdrug.com/fragrance/fragrance-gift-sets/c/gift-sets-fragrance',
        'fragranceforher': 'https://www.superdrug.com/fragrance/perfume-for-women/c/fragranceforher',
        'pt_fragrance_fragrance_gift_sets_for_her': 'https://www.superdrug.com/fragrance/perfume-for-women/fragrance-gift-sets-for-her/c/pt_fragrance_fragrance_gift_sets_for_her',
    },
    'free-next-day-delivery-across-healthcare': {
        'free-next-day-delivery-across-healthcare': 'https://www.superdrug.com/free-next-day-delivery-across-healthcare/c/free-next-day-delivery-across-healthcare',
    },
    'gifts': {
        'web-gifts': 'https://www.superdrug.com/gifts/c/web-gifts',
    },
    'hair': {
        'pt-hair-everyday-conditioner': 'https://www.superdrug.com/hair/everyday-conditioner/c/pt-hair-everyday-conditioner',
        'pt_hair_hair_brushes': 'https://www.superdrug.com/hair/hair-brushes/c/pt_hair_hair_brushes',
        'hair-treatments': 'https://www.superdrug.com/hair/hair-treatments/c/hair-treatments',
        'pt_health_medicated_hair_treatments': 'https://www.superdrug.com/hair/hair-treatments/medicated-hair-treatments/c/pt_health_medicated_hair_treatments',
        'pt_hair_anti_dandruff_shampoo': 'https://www.superdrug.com/hair/shampoo/anti-dandruff-shampoo/c/pt_hair_anti_dandruff_shampoo',
        'pt_hair_dry_shampoo': 'https://www.superdrug.com/hair/shampoo/dry-shampoo/c/pt_hair_dry_shampoo',
    },
    'health': {
        'health-allergy': 'https://www.superdrug.com/health/allergy-hayfever/c/health-allergy',
        'health': 'https://www.superdrug.com/health/c/health',
        'health-winter': 'https://www.superdrug.com/health/cough-cold-flu/c/health-winter',
        'health-dietfitness': 'https://www.superdrug.com/health/diet-fitness/c/health-dietfitness',
        'pt-electrolytes-and-hydration': 'https://www.superdrug.com/health/diet-fitness/electrolytes-and-hydration/c/pt-electrolytes-and-hydration',
        'protein': 'https://www.superdrug.com/health/diet-fitness/protein/c/protein',
        'pt-slimming-pills': 'https://www.superdrug.com/health/diet-fitness/weight-management/appetite-suppressant/c/pt-slimming-pills',
        'health-eyecare': 'https://www.superdrug.com/health/eye-care/c/health-eyecare',
        'health-1staid': 'https://www.superdrug.com/health/first-aid/c/health-1staid',
        'pt-health-joint-support': 'https://www.superdrug.com/health/first-aid/injury-and-joint-support/c/pt-health-joint-support',
        'health-footcare': 'https://www.superdrug.com/health/foot-care/c/health-footcare',
        'health-heartburn': 'https://www.superdrug.com/health/heartburn-indigestion/c/health-heartburn',
        'pt-health-test-kits': 'https://www.superdrug.com/health/home-testing-kits/c/pt-health-test-kits',
        'pt-medicated-acne-treatments': 'https://www.superdrug.com/health/medicated-skin/acne-spots-treatment/c/pt-medicated-acne-treatments',
        'health-skintreatments': 'https://www.superdrug.com/health/medicated-skin/c/health-skintreatments',
        'pt-medicated-eczema-treatments': 'https://www.superdrug.com/health/medicated-skin/eczema/c/pt-medicated-eczema-treatments',
        'pt-medicated-dry-skin-treatments': 'https://www.superdrug.com/health/medicated-skin/medicated-dry-skin/c/pt-medicated-dry-skin-treatments',
        'pt-medicated-psoriasis-treatments': 'https://www.superdrug.com/health/medicated-skin/psoriasis-treatment/c/pt-medicated-psoriasis-treatments',
        'pt-sensitive-skin-treatments': 'https://www.superdrug.com/health/medicated-skin/sensitive-skin-treatment/c/pt-sensitive-skin-treatments',
        'health-painrelief': 'https://www.superdrug.com/health/pain-relief/c/health-painrelief',
        'sexual-health': 'https://www.superdrug.com/health/sexual-health/c/sexual-health',
        'pt-erectile-dysfunction': 'https://www.superdrug.com/health/sexual-health/erectile-dysfunction/c/pt-erectile-dysfunction',
        'pt_health_sexual_enhancement_supplements': 'https://www.superdrug.com/health/sexual-health/male-enhancement-pills/c/pt_health_sexual_enhancement_supplements',
        'smoking-control': 'https://www.superdrug.com/health/smoking-control/c/smoking-control',
        'stomach-digestive': 'https://www.superdrug.com/health/stomach-digestive-care/c/stomach-digestive',
        'stomach-digestive%20': 'https://www.superdrug.com/health/stomach-digestive-care/c/stomach-digestive%20',
        'stomach-probiotic': 'https://www.superdrug.com/health/stomach-digestive-care/probiotics/c/stomach-probiotic',
        'pt-creatine': 'https://www.superdrug.com/health/trending-ingredients/creatine/c/pt-creatine',
        'health-vitamins': 'https://www.superdrug.com/health/vitamins-supplements/c/health-vitamins',
        'pt-health-vitamin-collagen': 'https://www.superdrug.com/health/vitamins-supplements/collagen/c/pt-health-vitamin-collagen',
        'pt_health_digestive_care': 'https://www.superdrug.com/health/vitamins-supplements/digestive-care/c/pt_health_digestive_care',
        'pt-health-vitamin-magnesium': 'https://www.superdrug.com/health/vitamins-supplements/energy-supplements/magnesium/c/pt-health-vitamin-magnesium',
        'pt_health_mens_health': 'https://www.superdrug.com/health/vitamins-supplements/vitamins-for-men/c/pt_health_mens_health',
        'pt_health_womens_health': 'https://www.superdrug.com/health/womens-intimate-health-care/c/pt_health_womens_health',
    },
    'healthy-foods-and-teas': {
        'healthy-foods-and-teas': 'https://www.superdrug.com/healthy-foods-and-teas/c/healthy-foods-and-teas',
    },
    'holiday-shop': {
        'luggage-packing': 'https://www.superdrug.com/holiday-shop/luggage-packing/c/luggage-packing',
    },
    'home-kitchen-appliances': {
        'home-appliances': 'https://www.superdrug.com/home-kitchen-appliances/c/home-appliances',
    },
    'in-your-prime': {
        'in-your-prime': 'https://www.superdrug.com/in-your-prime/c/in-your-prime',
    },
    'jewellery': {
        'jewellery': 'https://www.superdrug.com/jewellery/c/jewellery',
        'pt-watches': 'https://www.superdrug.com/jewellery/watches/c/pt-watches',
    },
    'make-up': {
        'pt_beauty_advent_calendars': 'https://www.superdrug.com/make-up/advent-calendars/c/pt_beauty_advent_calendars',
        'makeup': 'https://www.superdrug.com/make-up/c/makeup',
        'pt-eyebrow-tints': 'https://www.superdrug.com/make-up/eye-makeup/eyebrows/eyebrow-dye-and-tinting/c/pt-eyebrow-tints',
        'pt_make_up_false_eyelashes': 'https://www.superdrug.com/make-up/eye-makeup/false-eyelashes/c/pt_make_up_false_eyelashes',
        'bronzer': 'https://www.superdrug.com/make-up/face/bronzer-and-palettes/c/bronzer',
        'kj-beauty': 'https://www.superdrug.com/make-up/korean-japanese-makeup/c/kj-beauty',
        'pt_make_up_false_nails': 'https://www.superdrug.com/make-up/nails/false-nails/c/pt_make_up_false_nails',
        'new-make-up': 'https://www.superdrug.com/make-up/new-make-up/c/new-make-up',
    },
    'meal-replacement': {
        'meal-replacement-shakes-and-bars': 'https://www.superdrug.com/meal-replacement/c/meal-replacement-shakes-and-bars',
    },
    'mens': {
        'mens': 'https://www.superdrug.com/mens/c/mens',
        'pt_mens_mens_moisturisers': 'https://www.superdrug.com/mens/mens-skin-care/mens-face-moisturisers/c/pt_mens_mens_moisturisers',
        'pt_mens_mens_face_wash': 'https://www.superdrug.com/mens/mens-skin-care/mens-face-wash/c/pt_mens_mens_face_wash',
    },
    'mielle-organics-pomegranate-honey': {
        'mielle-organics-pomegranate-honey': 'https://www.superdrug.com/mielle-organics-pomegranate-honey/c/mielle-organics-pomegranate-honey',
    },
    'new-e-l-f-glow-reviver-melting-lip-balm-collection': {
        'elf-lip-balms': 'https://www.superdrug.com/new-e-l-f-glow-reviver-melting-lip-balm-collection/c/elf-lip-balms',
    },
    'new-in-baby-essentials': {
        'new-in-baby-essentials': 'https://www.superdrug.com/new-in-baby-essentials/c/new-in-baby-essentials',
    },
    'new-in-for-men': {
        'new-in-for-men': 'https://www.superdrug.com/new-in-for-men/c/new-in-for-men',
    },
    'new-in-health-care': {
        'new-in-health-care': 'https://www.superdrug.com/new-in-health-care/c/new-in-health-care',
    },
    'new-personal-care': {
        'new-personal-care': 'https://www.superdrug.com/new-personal-care/c/new-personal-care',
    },
    'new-revolution-wrap-lash-collection': {
        'revolution-wrap-lash': 'https://www.superdrug.com/new-revolution-wrap-lash-collection/c/revolution-wrap-lash',
    },
    'new-valentino-born-in-roma-purple-melancholia': {
        'new-valentino-born-in-roma-purple': 'https://www.superdrug.com/new-valentino-born-in-roma-purple-melancholia/c/new-valentino-born-in-roma-purple',
    },
    'pharmacy-medicines': {
        'pharmacy-medicines': 'https://www.superdrug.com/pharmacy-medicines/c/pharmacy-medicines',
    },
    'premium-fragrance-gift-sets': {
        'premium-fragrance-gift-sets': 'https://www.superdrug.com/premium-fragrance-gift-sets/c/premium-fragrance-gift-sets',
    },
    'premium-haircare': {
        'premium-hair': 'https://www.superdrug.com/premium-haircare/c/premium-hair',
    },
    'running-essentials': {
        'running-essentials': 'https://www.superdrug.com/running-essentials/c/running-essentials',
    },
    'save-up-to-30': {
        'coty-save': 'https://www.superdrug.com/save-up-to-30/c/coty-save',
    },
    'shower-routines': {
        'shower-routines': 'https://www.superdrug.com/shower-routines/c/shower-routines',
    },
    'skin': {
        'pt-eye-masks': 'https://www.superdrug.com/skin/eye-skincare/eye-masks/c/pt-eye-masks',
        'pt_skin_facial_serums': 'https://www.superdrug.com/skin/face-skin-care/face-serums/c/pt_skin_facial_serums',
        'k-beauty': 'https://www.superdrug.com/skin/korean-japanese-beauty/c/k-beauty',
        'pure-seoul': 'https://www.superdrug.com/skin/korean-japanese-beauty/pureseoul/c/pure-seoul',
    },
    'solait-after-sun': {
        'solait-aftersun': 'https://www.superdrug.com/solait-after-sun/c/solait-aftersun',
    },
    'solait-fake-tan': {
        'solait-fake-tan': 'https://www.superdrug.com/solait-fake-tan/c/solait-fake-tan',
    },
    'solait-sun-cream': {
        'solait-sun-cream': 'https://www.superdrug.com/solait-sun-cream/c/solait-sun-cream',
    },
    'solait-travel': {
        'solait-travel': 'https://www.superdrug.com/solait-travel/c/solait-travel',
    },
    'star-buy-weeklies': {
        'star-buy-weeklies': 'https://www.superdrug.com/star-buy-weeklies/c/star-buy-weeklies',
    },
    'superdrug-hair-care': {
        'superdrug-hair-care': 'https://www.superdrug.com/superdrug-hair-care/c/superdrug-hair-care',
    },
    'superdrug-halloween': {
        'superdrug-halloween': 'https://www.superdrug.com/superdrug-halloween/c/superdrug-halloween',
    },
    'superdrug-health-wellbeing': {
        'superdrug-health-and-wellbeing': 'https://www.superdrug.com/superdrug-health-wellbeing/c/superdrug-health-and-wellbeing',
    },
    'superdrug-own-brand': {
        'superdrug-own-brand': 'https://www.superdrug.com/superdrug-own-brand/c/superdrug-own-brand',
    },
    'superdrug-q10-skincare': {
        'superdrug-q10-skincare': 'https://www.superdrug.com/superdrug-q10-skincare/c/superdrug-q10-skincare',
    },
    'superdrug-skincare-essentials': {
        'superdrug-skin-essentials': 'https://www.superdrug.com/superdrug-skincare-essentials/c/superdrug-skin-essentials',
    },
    'superdrug-skincare': {
        'superdrug-skincare': 'https://www.superdrug.com/superdrug-skincare/c/superdrug-skincare',
    },
    'superdrug-toiletries': {
        'superdrug-toiletries': 'https://www.superdrug.com/superdrug-toiletries/c/superdrug-toiletries',
    },
    'superdrug-vitamins': {
        'superdrug-vitamins': 'https://www.superdrug.com/superdrug-vitamins/c/superdrug-vitamins',
    },
    'toiletries': {
        'pt_toiletries_toothbrushes_electrical': 'https://www.superdrug.com/toiletries/dental/electrical-toothbrush/c/pt_toiletries_toothbrushes_electrical',
        'teeth-whitening': 'https://www.superdrug.com/toiletries/dental/teeth-whitening/c/teeth-whitening',
        'toil-deodorants': 'https://www.superdrug.com/toiletries/deodorants/c/toil-deodorants',
        'mens-deodorants': 'https://www.superdrug.com/toiletries/deodorants/mens-deodorants/c/mens-deodorants',
        'pt_mens_mens_body_sprays': 'https://www.superdrug.com/toiletries/deodorants/mens-deodorants/mens-body-sprays/c/pt_mens_mens_body_sprays',
        'pt_mens_mens_deodrant_sticks': 'https://www.superdrug.com/toiletries/deodorants/mens-deodorants/mens-deodorant-sticks/c/pt_mens_mens_deodrant_sticks',
        'more-tissues': 'https://www.superdrug.com/toiletries/tissues/c/more-tissues',
    },
    'trending-on-marketplace': {
        'trending-on-marketplace': 'https://www.superdrug.com/trending-on-marketplace/c/trending-on-marketplace',
    },
    'trending-right-now': {
        'trends': 'https://www.superdrug.com/trending-right-now/c/trends',
    },
}
