"""Current crawlable departments from Sephora's primary site navigation.

The navigation's separate ``/sale`` landing page is excluded because it is not a
catalog category and ``/api/v2/catalog/categories/sale/seo`` returns 404.
"""

SEPHORA_CATEGORIES = {
    "beauty": {
        "makeup": {
            "url": "https://www.sephora.com/shop/makeup-cosmetics",
            "slug": "makeup-cosmetics",
        },
        "skincare": {
            "url": "https://www.sephora.com/shop/skincare",
            "slug": "skincare",
        },
        "hair": {
            "url": "https://www.sephora.com/shop/hair-products",
            "slug": "hair-products",
        },
        "fragrance": {
            "url": "https://www.sephora.com/shop/fragrance",
            "slug": "fragrance",
        },
        "tools-brushes": {
            "url": "https://www.sephora.com/shop/makeup-tools",
            "slug": "makeup-tools",
        },
        "bath-body": {
            "url": "https://www.sephora.com/shop/bath-body",
            "slug": "bath-body",
        },
    },
}
