"""Amazon departments from the US storefront search selector.

The selector exposes stable ``search-alias`` values. Keep those aliases as the
category keys so CLI and DAG task names remain URL-safe while retaining the
storefront label in each rich leaf.
"""

AMAZON_CATEGORIES = {
    "departments": {
        "alexa-skills": {
            "url": "https://www.amazon.com/s?i=alexa-skills",
            "label": "Alexa Skills",
        },
        "vehicles": {
            "url": "https://www.amazon.com/s?i=vehicles",
            "label": "Amazon Autos",
        },
        "amazon-devices": {
            "url": "https://www.amazon.com/s?i=amazon-devices",
            "label": "Amazon Devices",
        },
        "amazon-global-store": {
            "url": "https://www.amazon.com/s?i=amazon-global-store",
            "label": "Amazon Global Store",
        },
        "bazaar": {"url": "https://www.amazon.com/s?i=bazaar", "label": "Amazon Haul"},
        "amazon-one-medical": {
            "url": "https://www.amazon.com/s?i=amazon-one-medical",
            "label": "Amazon One Medical",
        },
        "amazon-pharmacy": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy",
            "label": "Amazon Pharmacy",
        },
        "warehouse-deals": {
            "url": "https://www.amazon.com/s?i=warehouse-deals",
            "label": "Amazon Resale",
        },
        "appliances": {
            "url": "https://www.amazon.com/s?i=appliances",
            "label": "Appliances",
        },
        "mobile-apps": {
            "url": "https://www.amazon.com/s?i=mobile-apps",
            "label": "Apps & Games",
        },
        "arts-crafts": {
            "url": "https://www.amazon.com/s?i=arts-crafts",
            "label": "Arts, Crafts & Sewing",
        },
        "audible": {
            "url": "https://www.amazon.com/s?i=audible",
            "label": "Audible Books & Originals",
        },
        "automotive": {
            "url": "https://www.amazon.com/s?i=automotive",
            "label": "Automotive Parts & Accessories",
        },
        "baby-products": {
            "url": "https://www.amazon.com/s?i=baby-products",
            "label": "Baby",
        },
        "beauty": {
            "url": "https://www.amazon.com/s?i=beauty",
            "label": "Beauty & Personal Care",
        },
        "stripbooks": {
            "url": "https://www.amazon.com/s?i=stripbooks",
            "label": "Books",
        },
        "popular": {
            "url": "https://www.amazon.com/s?i=popular",
            "label": "CDs & Vinyl",
        },
        "mobile": {
            "url": "https://www.amazon.com/s?i=mobile",
            "label": "Cell Phones & Accessories",
        },
        "fashion": {
            "url": "https://www.amazon.com/s?i=fashion",
            "label": "Clothing, Shoes & Jewelry",
        },
        "fashion-womens": {
            "url": "https://www.amazon.com/s?i=fashion-womens",
            "label": "Women's Clothing, Shoes & Jewelry",
        },
        "fashion-mens": {
            "url": "https://www.amazon.com/s?i=fashion-mens",
            "label": "Men's Clothing, Shoes & Jewelry",
        },
        "fashion-girls": {
            "url": "https://www.amazon.com/s?i=fashion-girls",
            "label": "Girl's Clothing, Shoes & Jewelry",
        },
        "fashion-boys": {
            "url": "https://www.amazon.com/s?i=fashion-boys",
            "label": "Boy's Clothing, Shoes & Jewelry",
        },
        "fashion-baby": {
            "url": "https://www.amazon.com/s?i=fashion-baby",
            "label": "Baby Clothing, Shoes & Jewelry",
        },
        "collectibles": {
            "url": "https://www.amazon.com/s?i=collectibles",
            "label": "Collectibles & Fine Art",
        },
        "computers": {
            "url": "https://www.amazon.com/s?i=computers",
            "label": "Computers",
        },
        "financial": {
            "url": "https://www.amazon.com/s?i=financial",
            "label": "Credit and Payment Cards",
        },
        "digital-music": {
            "url": "https://www.amazon.com/s?i=digital-music",
            "label": "Digital Music",
        },
        "electronics": {
            "url": "https://www.amazon.com/s?i=electronics",
            "label": "Electronics",
        },
        "lawngarden": {
            "url": "https://www.amazon.com/s?i=lawngarden",
            "label": "Garden & Outdoor",
        },
        "gift-cards": {
            "url": "https://www.amazon.com/s?i=gift-cards",
            "label": "Gift Cards",
        },
        "grocery": {
            "url": "https://www.amazon.com/s?i=grocery",
            "label": "Grocery & Gourmet Food",
        },
        "handmade": {"url": "https://www.amazon.com/s?i=handmade", "label": "Handmade"},
        "hpc": {
            "url": "https://www.amazon.com/s?i=hpc",
            "label": "Health, Household & Baby Care",
        },
        "local-services": {
            "url": "https://www.amazon.com/s?i=local-services",
            "label": "Home & Business Services",
        },
        "garden": {
            "url": "https://www.amazon.com/s?i=garden",
            "label": "Home & Kitchen",
        },
        "industrial": {
            "url": "https://www.amazon.com/s?i=industrial",
            "label": "Industrial & Scientific",
        },
        "prime-exclusive": {
            "url": "https://www.amazon.com/s?i=prime-exclusive",
            "label": "Just for Prime",
        },
        "digital-text": {
            "url": "https://www.amazon.com/s?i=digital-text",
            "label": "Kindle Store",
        },
        "fashion-luggage": {
            "url": "https://www.amazon.com/s?i=fashion-luggage",
            "label": "Luggage & Travel Gear",
        },
        "luxury": {
            "url": "https://www.amazon.com/s?i=luxury",
            "label": "Luxury Stores",
        },
        "magazines": {
            "url": "https://www.amazon.com/s?i=magazines",
            "label": "Magazine Subscriptions",
        },
        "movies-tv": {
            "url": "https://www.amazon.com/s?i=movies-tv",
            "label": "Movies & TV",
        },
        "mi": {"url": "https://www.amazon.com/s?i=mi", "label": "Musical Instruments"},
        "office-products": {
            "url": "https://www.amazon.com/s?i=office-products",
            "label": "Office Products",
        },
        "pets": {"url": "https://www.amazon.com/s?i=pets", "label": "Pet Supplies"},
        "luxury-beauty": {
            "url": "https://www.amazon.com/s?i=luxury-beauty",
            "label": "Premium Beauty",
        },
        "instant-video": {
            "url": "https://www.amazon.com/s?i=instant-video",
            "label": "Prime Video",
        },
        "smart-home": {
            "url": "https://www.amazon.com/s?i=smart-home",
            "label": "Smart Home",
        },
        "software": {"url": "https://www.amazon.com/s?i=software", "label": "Software"},
        "sporting": {
            "url": "https://www.amazon.com/s?i=sporting",
            "label": "Sports & Outdoors",
        },
        "specialty-aps-sns": {
            "url": "https://www.amazon.com/s?i=specialty-aps-sns",
            "label": "Subscribe & Save",
        },
        "subscribe-with-amazon": {
            "url": "https://www.amazon.com/s?i=subscribe-with-amazon",
            "label": "Subscription Boxes",
        },
        "tools": {
            "url": "https://www.amazon.com/s?i=tools",
            "label": "Tools & Home Improvement",
        },
        "toys-and-games": {
            "url": "https://www.amazon.com/s?i=toys-and-games",
            "label": "Toys & Games",
        },
        "under-ten-dollars": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars",
            "label": "Under $10",
        },
        "videogames": {
            "url": "https://www.amazon.com/s?i=videogames",
            "label": "Video Games",
        },
        "wholefoods": {
            "url": "https://www.amazon.com/s?i=wholefoods",
            "label": "Whole Foods Market",
        },
    }
}
