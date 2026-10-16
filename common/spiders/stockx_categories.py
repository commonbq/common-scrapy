"""StockX product categories from the live primary navigation.

Source: ``Product Category Switcher`` on https://stockx.com/, checked
2026-10-17.  Promotional navigation entries (Trending, New, Deals) and audience
browse pages (Men, Women, Kids) are not product categories.
"""

STOCKX_CATEGORIES = {
    "All products": {
        "sneakers": "https://stockx.com/category/sneakers",
        "shoes": "https://stockx.com/category/shoes",
        "apparel": "https://stockx.com/category/apparel",
        "accessories": "https://stockx.com/category/accessories",
        "collectibles": "https://stockx.com/category/collectibles",
        "trading-cards": "https://stockx.com/category/trading-cards",
        "mystery-boxes": "https://stockx.com/category/mystery-boxes",
        "electronics": "https://stockx.com/category/electronics?sort=most-active",
    },
}
