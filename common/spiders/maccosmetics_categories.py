from __future__ import annotations


BASE_URL = "https://www.maccosmetics.com/collections"


# Product-listing collections exposed by the US site's primary navigation on
# 2026-10-13. Product and editorial links are intentionally excluded because
# MaccosmeticsListingSpider parses Shopify collection pages.
MACCOSMETICS_CATEGORIES = {
    "featured": {
        "gift-by-price": f"{BASE_URL}/gift-by-price",
        "new": f"{BASE_URL}/new",
        "sale": f"{BASE_URL}/sale",
    },
    "bestsellers": {
        "best-sellers": f"{BASE_URL}/best-sellers",
        "face-bestsellers": (
            f"{BASE_URL}/best-sellers?fh_f_fhr_product_type="
            "cleansersmakeupremovers,concealers,foundations,highlighters,"
            "makeupsettingsprays,powders"
        ),
        "lips-bestsellers": (
            f"{BASE_URL}/best-sellers?fh_f_fhr_product_type="
            "lipglosses,lipliners,lipsticks"
        ),
        "eyes-bestsellers": (
            f"{BASE_URL}/best-sellers?fh_f_fhr_product_type="
            "eyepalettes,eyeshadows,mascaras"
        ),
    },
    "face": {
        "face": f"{BASE_URL}/face",
        "foundation": f"{BASE_URL}/foundation",
        "concealer": f"{BASE_URL}/concealer",
        "blush-bronzer": f"{BASE_URL}/blush-bronzer",
        "face-powders": f"{BASE_URL}/face-powders",
        "highlighting-contour": f"{BASE_URL}/highlighting-contour",
        "glitter-pigments": f"{BASE_URL}/glitter-pigments",
        "primers": f"{BASE_URL}/primers",
        "setting-spray": f"{BASE_URL}/setting-spray",
        "minis": f"{BASE_URL}/minis",
    },
    "lips": {
        "lip": f"{BASE_URL}/lip",
        "lipstick": f"{BASE_URL}/lipstick",
        "lip-liners": f"{BASE_URL}/lip-liners",
        "lip-gloss": f"{BASE_URL}/lip-gloss",
        "liquid-lipstick": f"{BASE_URL}/liquid-lipstick",
        "lip-balm-primer": f"{BASE_URL}/lip-balm-primer",
    },
    "eyes": {
        "eye-makeup": f"{BASE_URL}/eye-makeup",
        "eye-shadow": f"{BASE_URL}/eye-shadow",
        "eyeliner": f"{BASE_URL}/eyeliner",
        "mascaras": f"{BASE_URL}/mascaras",
        "eyebrow": f"{BASE_URL}/eyebrow",
        "false-eyelashes": f"{BASE_URL}/false-eyelashes",
        "eye-primers": f"{BASE_URL}/eye-primers",
    },
    "brushes-tools": {
        "brushes": f"{BASE_URL}/brushes",
        "face-brushes": f"{BASE_URL}/face-brushes",
        "lip-brushes": f"{BASE_URL}/lip-brushes",
        "eye-brushes": f"{BASE_URL}/eye-brushes",
        "tools-accessories": f"{BASE_URL}/tools-accessories",
        "makeup-sponges-applicators": f"{BASE_URL}/makeup-sponges-applicators",
    },
    "kits-sets": {
        "face-kits": f"{BASE_URL}/face-kits",
        "lip-palettes-kits": f"{BASE_URL}/lip-palettes-kits",
        "eye-shadow-palettes": f"{BASE_URL}/eye-shadow-palettes",
    },
    "skincare": {
        "skincare": f"{BASE_URL}/skincare",
        "moisturizers": f"{BASE_URL}/moisturizers",
        "serums-treatments": f"{BASE_URL}/serums-treatments",
        "removers-cleansers": f"{BASE_URL}/removers-cleansers",
        "eye-lip-treatments": f"{BASE_URL}/eye-lip-treatments",
        "spf": f"{BASE_URL}/spf",
    },
    "fragrance": {
        "fragrance": f"{BASE_URL}/fragrance",
    },
    "pro": {
        "all-pro": f"{BASE_URL}/all-pro",
        "pro-palettes": f"{BASE_URL}/pro-palettes",
        "multi-use": f"{BASE_URL}/multi-use",
        "makeup-bags": f"{BASE_URL}/makeup-bags",
    },
}
