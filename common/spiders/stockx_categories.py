"""StockX product categories from the live primary navigation.

Source: ``Product Category Switcher`` on https://stockx.com/, checked
2026-10-18.  Promotional navigation entries (Trending, New, Deals) and audience
browse pages (Men, Women, Kids) are not product categories.

Each live product category is its own group because StockX exposes these as peer
top-level departments, not as children of one synthetic navigation parent.
"""

STOCKX_CATEGORIES = {
    "Sneakers": {
        "sneakers": "https://stockx.com/category/sneakers",
    },
    "Shoes": {
        "shoes": "https://stockx.com/category/shoes",
    },
    "Apparel": {
        "apparel": "https://stockx.com/category/apparel",
    },
    "Accessories": {
        "accessories": "https://stockx.com/category/accessories",
    },
    "Collectibles": {
        "collectibles": "https://stockx.com/category/collectibles",
    },
    "Trading Cards": {
        "trading-cards": "https://stockx.com/category/trading-cards",
    },
    "Mystery Boxes": {
        "mystery-boxes": "https://stockx.com/category/mystery-boxes",
    },
    "Electronics": {
        "electronics": "https://stockx.com/category/electronics?sort=most-active",
    },
}
