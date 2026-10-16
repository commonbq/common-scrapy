"""Anthropologie US category inventory refreshed from live site navigation (2026-10-16).

Captured from the storefront ``llms.txt`` (https://www.anthropologie.com/llms.txt)
which lists the full department tree. Each leaf is a crawlable category page
returned by the Pinia SSR hydration state that ``anthropologie_listing_spider``
parses.

Shape follows the base listing spider contract::

    {
        "<group>": {
            "<leaf>": {
                "name": "<display name>",
                "department": "<group>",
                "category": "<leaf>",
                "url": "https://www.anthropologie.com/<path>",
            },
            ...
        },
        ...
    }
"""

ANTHROPOLOGIE_CATEGORIES = {
    "Clothing": {
        "clothes": {
            "name": "Women's Clothing",
            "department": "Clothing",
            "category": "clothes",
            "url": "https://www.anthropologie.com/clothes",
        },
        "dresses": {
            "name": "Dresses",
            "department": "Clothing",
            "category": "dresses",
            "url": "https://www.anthropologie.com/dresses",
        },
        "tops": {
            "name": "Tops",
            "department": "Clothing",
            "category": "tops",
            "url": "https://www.anthropologie.com/tops",
        },
        "bottoms": {
            "name": "Bottoms",
            "department": "Clothing",
            "category": "bottoms",
            "url": "https://www.anthropologie.com/bottoms",
        },
        "jackets-coats": {
            "name": "Jackets & Coats",
            "department": "Clothing",
            "category": "jackets-coats",
            "url": "https://www.anthropologie.com/jackets-coats",
        },
        "intimates": {
            "name": "Intimates & Lingerie",
            "department": "Clothing",
            "category": "intimates",
            "url": "https://www.anthropologie.com/intimates",
        },
        "sleepwear": {
            "name": "Sleepwear & Loungewear",
            "department": "Clothing",
            "category": "sleepwear",
            "url": "https://www.anthropologie.com/sleepwear",
        },
        "sets": {
            "name": "Matching Sets",
            "department": "Clothing",
            "category": "sets",
            "url": "https://www.anthropologie.com/sets",
        },
        "new-clothes": {
            "name": "New Clothing",
            "department": "Clothing",
            "category": "new-clothes",
            "url": "https://www.anthropologie.com/new-clothes",
        },
    },
    "Shoes": {
        "shoes": {
            "name": "Shoes",
            "department": "Shoes",
            "category": "shoes",
            "url": "https://www.anthropologie.com/shoes",
        },
    },
    "Accessories": {
        "accessories": {
            "name": "Accessories",
            "department": "Accessories",
            "category": "accessories",
            "url": "https://www.anthropologie.com/accessories",
        },
        "jewelry": {
            "name": "Jewelry",
            "department": "Accessories",
            "category": "jewelry",
            "url": "https://www.anthropologie.com/jewelry",
        },
    },
    "Home & Furniture": {
        "house-home": {
            "name": "Home & Furniture",
            "department": "Home & Furniture",
            "category": "house-home",
            "url": "https://www.anthropologie.com/house-home",
        },
    },
    "Beauty": {
        "beauty-wellness": {
            "name": "Beauty & Wellness",
            "department": "Beauty",
            "category": "beauty-wellness",
            "url": "https://www.anthropologie.com/beauty-wellness",
        },
    },
    "Sale": {
        "sale-all": {
            "name": "Sale",
            "department": "Sale",
            "category": "sale-all",
            "url": "https://www.anthropologie.com/sale-all",
        },
    },
    "Gifts & Holiday": {
        "all-gifts": {
            "name": "Gifts & Holiday",
            "department": "Gifts & Holiday",
            "category": "all-gifts",
            "url": "https://www.anthropologie.com/all-gifts",
        },
    },
    "Weddings": {
        "bhldn-weddings": {
            "name": "Weddings",
            "department": "Weddings",
            "category": "bhldn-weddings",
            "url": "https://www.anthropologie.com/bhldn-weddings",
        },
    },
    "maeve": {
        "maeve": {
            "name": "maeve",
            "department": "maeve",
            "category": "maeve",
            "url": "https://www.anthropologie.com/maeve",
        },
    },
    "Top-Rated": {
        "top-rated-products": {
            "name": "Top-Rated",
            "department": "Top-Rated",
            "category": "top-rated-products",
            "url": "https://www.anthropologie.com/top-rated-products",
        },
    },
}
