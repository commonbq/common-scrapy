from __future__ import annotations


COLLECTION_HANDLES = (
    "best-sellers", "eye-lip-treatments", "multi-use", "serums-treatments",
    "eye-makeup", "turquatic", "spf", "matte-lipstick", "tools-accessories",
    "dazzle", "waterproof", "lip-brushes", "moisturizers",
    "removers-cleansers", "makeup-sponges-applicators", "eye-primers",
    "blue-shades", "purple-shades", "lip-balm-primer", "skincare",
    "mixing-mediums", "liquid-lipstick", "lip", "pro-palettes", "face-kits",
    "berry-lip", "eye-brushes", "lip-liners", "face-brushes",
    "false-eyelashes", "primers", "highlighting-contour", "eyebrow",
    "fragrance", "pink-lipstick", "mascaras", "bestselling-lipstick-shades",
    "face", "eyeliner", "eye-shadow-palettes", "lip-gloss",
    "lip-palettes-kits", "concealer", "blush-bronzer", "eye-shadow",
    "brushes", "foundation", "lipstick", "winter-essentials",
    "mothers-day-gift-guide", "spring-essentials", "pride-looks",
    "refer-a-friend", "fall-favourites", "subscription", "sale",
    "lip-pairings", "minimalist-makeup", "wedding", "gift-by-price",
    "fall-lip-colours", "lip-sale", "setting-spray", "makeup-bags",
    "eye-accessories", "glow-play", "minis", "glitter-pigments", "tools",
    "value-sets", "double-denim", "all-pro", "new", "nudes", "red-lips",
    "haute-chocolates", "face-powders", "mac-in-sepia",
    "must-haves-halloween",
)


# MAC exposes these as a flat collection inventory with no parent taxonomy.
# Keep one explicit group so the constant follows BaseListingSpider's canonical
# ``{group: {leaf: url}}`` schema without inventing a hierarchy.
MACCOSMETICS_CATEGORIES = {
    "collections": {
        handle: f"https://www.maccosmetics.com/collections/{handle}"
        for handle in COLLECTION_HANDLES
    }
}
