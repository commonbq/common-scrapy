"""Amazon department -> subcategory inventory from the live storefront.

Source of truth: the ``Department`` refinement tree Amazon renders on each
department's browse page (``/s?rh=n%3A<node>&fs=true``), captured 2026-10-19
UTC through the repository's configured ScrapeOps US proxy: **58 departments**
and **595 scheduled leaves**.

Grouped ``{department: {leaf: {url, label}}}`` mapping as required by the
``BaseListingSpider`` contract (one top-level key per department), so the spider
and the DAG share one source of truth and
``_spider_category_groups(..., group_by="department")`` can emit one TaskGroup
per department.

Leaf keys are ``<department>-<subcategory>`` so every task id is globally
unique; the department's own search alias (``electronics``) is kept as a leaf
last in its group so the documented ``-a category=electronics`` command keeps
working while the DAG schedules real subcategory PLPs first.

Departments Amazon exposes only as a single page (Amazon Autos, Amazon Global
Store, Handmade, Home & Business Services, Just for Prime, Smart Home,
Subscription Boxes) keep just their hub leaf: their landing pages carry no
browse tree.
"""

AMAZON_CATEGORIES = {
    "alexa-skills": {
        "alexa-skills-business-finance": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284819011",
            "label": "Business & Finance",
            "node": "14284819011",
        },
        "alexa-skills-communication": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284865011",
            "label": "Communication",
            "node": "14284865011",
        },
        "alexa-skills-connected-car": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284820011",
            "label": "Connected Car",
            "node": "14284820011",
        },
        "alexa-skills-education-reference": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284821011",
            "label": "Education & Reference",
            "node": "14284821011",
        },
        "alexa-skills-food-drink": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284822011",
            "label": "Food & Drink",
            "node": "14284822011",
        },
        "alexa-skills-games-trivia": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284827011",
            "label": "Games & Trivia",
            "node": "14284827011",
        },
        "alexa-skills-health-wellness": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284831011",
            "label": "Health & Wellness",
            "node": "14284831011",
        },
        "alexa-skills-home-services": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A17388364011",
            "label": "Home Services",
            "node": "17388364011",
        },
        "alexa-skills-kids": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284832011",
            "label": "Kids",
            "node": "14284832011",
        },
        "alexa-skills-lifestyle": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284837011",
            "label": "Lifestyle",
            "node": "14284837011",
        },
        "alexa-skills-local": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284844011",
            "label": "Local",
            "node": "14284844011",
        },
        "alexa-skills-movies-tv": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284846011",
            "label": "Movies & TV",
            "node": "14284846011",
        },
        "alexa-skills-music-audio": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284851011",
            "label": "Music & Audio",
            "node": "14284851011",
        },
        "alexa-skills-news": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284857011",
            "label": "News",
            "node": "14284857011",
        },
        "alexa-skills-novelty-humor": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284858011",
            "label": "Novelty & Humor",
            "node": "14284858011",
        },
        "alexa-skills-productivity": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284859011",
            "label": "Productivity",
            "node": "14284859011",
        },
        "alexa-skills-shopping": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284862011",
            "label": "Shopping",
            "node": "14284862011",
        },
        "alexa-skills-smart-home": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284863011",
            "label": "Smart Home",
            "node": "14284863011",
        },
        "alexa-skills-social": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284864011",
            "label": "Social",
            "node": "14284864011",
        },
        "alexa-skills-sports": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284869011",
            "label": "Sports",
            "node": "14284869011",
        },
        "alexa-skills-travel-transportation": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284874011",
            "label": "Travel & Transportation",
            "node": "14284874011",
        },
        "alexa-skills-utilities": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284882011",
            "label": "Utilities",
            "node": "14284882011",
        },
        "alexa-skills-weather": {
            "url": "https://www.amazon.com/s?i=alexa-skills&rh=n%3A13727921011%2Cn%3A14284889011",
            "label": "Weather",
            "node": "14284889011",
        },
        "alexa-skills": {
            "url": "https://www.amazon.com/s?i=alexa-skills",
            "label": "Alexa Skills",
        },
    },
    "vehicles": {
        "vehicles": {
            "url": "https://www.amazon.com/s?i=vehicles",
            "label": "Amazon Autos",
        },
    },
    "amazon-devices": {
        "amazon-devices-amazon-devices": {
            "url": "https://www.amazon.com/s?i=amazon-devices&rh=n%3A16333372011%2Cn%3A2102313011",
            "label": "Amazon Devices",
            "node": "2102313011",
        },
        "amazon-devices-amazon-device-accessories": {
            "url": "https://www.amazon.com/s?i=amazon-devices&rh=n%3A16333372011%2Cn%3A370783011",
            "label": "Amazon Device Accessories",
            "node": "370783011",
        },
        "amazon-devices-amazon-device-subscriptions": {
            "url": "https://www.amazon.com/s?i=amazon-devices&rh=n%3A16333372011%2Cn%3A121475272011",
            "label": "Amazon Device Subscriptions",
            "node": "121475272011",
        },
        "amazon-devices": {
            "url": "https://www.amazon.com/s?i=amazon-devices",
            "label": "Amazon Devices",
        },
    },
    "amazon-global-store": {
        "amazon-global-store": {
            "url": "https://www.amazon.com/s?i=amazon-global-store",
            "label": "Amazon Global Store",
        },
    },
    "bazaar": {
        "bazaar-arts-crafts-sewing": {
            "url": "https://www.amazon.com/s?i=bazaar&rh=n%3A121974693011%2Cn%3A2617941011",
            "label": "Arts, Crafts & Sewing",
            "node": "2617941011",
        },
        "bazaar-everything-else": {
            "url": "https://www.amazon.com/s?i=bazaar&rh=n%3A121974693011%2Cn%3A10272111",
            "label": "Everything Else",
            "node": "10272111",
        },
        "bazaar-grocery-gourmet-food": {
            "url": "https://www.amazon.com/s?i=bazaar&rh=n%3A121974693011%2Cn%3A16310101",
            "label": "Grocery & Gourmet Food",
            "node": "16310101",
        },
        "bazaar-handmade-products": {
            "url": "https://www.amazon.com/s?i=bazaar&rh=n%3A121974693011%2Cn%3A11260432011",
            "label": "Handmade Products",
            "node": "11260432011",
        },
        "bazaar": {
            "url": "https://www.amazon.com/s?i=bazaar",
            "label": "Amazon Haul",
        },
    },
    "amazon-one-medical": {
        "amazon-one-medical": {
            "url": "https://www.amazon.com/s?i=amazon-one-medical",
            "label": "Amazon One Medical",
        },
    },
    "amazon-pharmacy": {
        "amazon-pharmacy-baby-child-care": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A10787321",
            "label": "Baby & Child Care",
            "node": "10787321",
        },
        "amazon-pharmacy-health-care": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A3760941",
            "label": "Health Care",
            "node": "3760941",
        },
        "amazon-pharmacy-household-supplies": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A15342811",
            "label": "Household Supplies",
            "node": "15342811",
        },
        "amazon-pharmacy-medical-supplies-equipment": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A3775161",
            "label": "Medical Supplies & Equipment",
            "node": "3775161",
        },
        "amazon-pharmacy-oral-care": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A10079992011",
            "label": "Oral Care",
            "node": "10079992011",
        },
        "amazon-pharmacy-prescription-medications": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A19763358011",
            "label": "Prescription Medications",
            "node": "19763358011",
        },
        "amazon-pharmacy-sexual-wellness": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A3777371",
            "label": "Sexual Wellness",
            "node": "3777371",
        },
        "amazon-pharmacy-stationery-gift-wrapping-supplies": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A723418011",
            "label": "Stationery & Gift Wrapping Supplies",
            "node": "723418011",
        },
        "amazon-pharmacy-vision": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A10079994011",
            "label": "Vision",
            "node": "10079994011",
        },
        "amazon-pharmacy-diet-sports-nutrition": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A3764441",
            "label": "Diet & Sports Nutrition",
            "node": "3764441",
        },
        "amazon-pharmacy-wellness-relaxation": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A10079996011",
            "label": "Wellness & Relaxation",
            "node": "10079996011",
        },
        "amazon-pharmacy-vitamins-minerals-supplements": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A23675621011",
            "label": "Vitamins, Minerals & Supplements",
            "node": "23675621011",
        },
        "amazon-pharmacy-personal-care": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy&rh=n%3A3760901%2Cn%3A3777891",
            "label": "Personal Care",
            "node": "3777891",
        },
        "amazon-pharmacy": {
            "url": "https://www.amazon.com/s?i=amazon-pharmacy",
            "label": "Amazon Pharmacy",
        },
    },
    "warehouse-deals": {
        "warehouse-deals-arts-crafts-sewing": {
            "url": "https://www.amazon.com/s?i=warehouse-deals&rh=n%3A10158976011%2Cn%3A2617941011",
            "label": "Arts, Crafts & Sewing",
            "node": "2617941011",
        },
        "warehouse-deals-everything-else": {
            "url": "https://www.amazon.com/s?i=warehouse-deals&rh=n%3A10158976011%2Cn%3A10272111",
            "label": "Everything Else",
            "node": "10272111",
        },
        "warehouse-deals-grocery-gourmet-food": {
            "url": "https://www.amazon.com/s?i=warehouse-deals&rh=n%3A10158976011%2Cn%3A16310101",
            "label": "Grocery & Gourmet Food",
            "node": "16310101",
        },
        "warehouse-deals": {
            "url": "https://www.amazon.com/s?i=warehouse-deals",
            "label": "Amazon Resale",
        },
    },
    "appliances": {
        "appliances-refrigerators-freezers-ice-makers": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A17921061011",
            "label": "Refrigerators, Freezers & Ice Makers",
            "node": "17921061011",
        },
        "appliances-laundry-appliances": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A18116194011",
            "label": "Laundry Appliances",
            "node": "18116194011",
        },
        "appliances-ranges-ovens-cooktops": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A18116197011",
            "label": "Ranges, Ovens & Cooktops",
            "node": "18116197011",
        },
        "appliances-microwave-ovens": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A289935",
            "label": "Microwave Ovens",
            "node": "289935",
        },
        "appliances-dishwashers": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A3741271",
            "label": "Dishwashers",
            "node": "3741271",
        },
        "appliances-small-kitchen-appliances": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A289913",
            "label": "Small Kitchen Appliances",
            "node": "289913",
        },
        "appliances-vacuums-floor-care": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A18116203011",
            "label": "Vacuums & Floor Care",
            "node": "18116203011",
        },
        "appliances-garbage-disposals-compactors": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A18116205011",
            "label": "Garbage Disposals & Compactors",
            "node": "18116205011",
        },
        "appliances-parts-accessories": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A3741181",
            "label": "Parts & Accessories",
            "node": "3741181",
        },
        "appliances-appliance-warranties": {
            "url": "https://www.amazon.com/s?i=appliances&rh=n%3A2619525011%2Cn%3A2242350011",
            "label": "Appliance Warranties",
            "node": "2242350011",
        },
        "appliances": {
            "url": "https://www.amazon.com/s?i=appliances",
            "label": "Appliances",
        },
    },
    "mobile-apps": {
        "mobile-apps-books-comics": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408444011",
            "label": "Books & Comics",
            "node": "9408444011",
        },
        "mobile-apps-business": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A10298305011",
            "label": "Business",
            "node": "10298305011",
        },
        "mobile-apps-communication": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408466011",
            "label": "Communication",
            "node": "9408466011",
        },
        "mobile-apps-customization": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408481011",
            "label": "Customization",
            "node": "9408481011",
        },
        "mobile-apps-education": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408490011",
            "label": "Education",
            "node": "9408490011",
        },
        "mobile-apps-finance": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408433011",
            "label": "Finance",
            "node": "9408433011",
        },
        "mobile-apps-food-drink": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408523011",
            "label": "Food & Drink",
            "node": "9408523011",
        },
        "mobile-apps-games": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9209902011",
            "label": "Games",
            "node": "9209902011",
        },
        "mobile-apps-health-fitness": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408749011",
            "label": "Health & Fitness",
            "node": "9408749011",
        },
        "mobile-apps-kids": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408582011",
            "label": "Kids",
            "node": "9408582011",
        },
        "mobile-apps-lifestyle": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408710011",
            "label": "Lifestyle",
            "node": "9408710011",
        },
        "mobile-apps-local": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A10298309011",
            "label": "Local",
            "node": "10298309011",
        },
        "mobile-apps-magazines": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408805011",
            "label": "Magazines",
            "node": "9408805011",
        },
        "mobile-apps-medical": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A10298306011",
            "label": "Medical",
            "node": "10298306011",
        },
        "mobile-apps-movies-tv": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408765011",
            "label": "Movies & TV",
            "node": "9408765011",
        },
        "mobile-apps-music-audio": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408771011",
            "label": "Music & Audio",
            "node": "9408771011",
        },
        "mobile-apps-news": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408802011",
            "label": "News",
            "node": "9408802011",
        },
        "mobile-apps-novelty": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408852011",
            "label": "Novelty",
            "node": "9408852011",
        },
        "mobile-apps-photo-video": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408874011",
            "label": "Photo & Video",
            "node": "9408874011",
        },
        "mobile-apps-productivity": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408449011",
            "label": "Productivity",
            "node": "9408449011",
        },
        "mobile-apps-reference": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408491011",
            "label": "Reference",
            "node": "9408491011",
        },
        "mobile-apps-shopping": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408875011",
            "label": "Shopping",
            "node": "9408875011",
        },
        "mobile-apps-social": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408464011",
            "label": "Social",
            "node": "9408464011",
        },
        "mobile-apps-sports": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408876011",
            "label": "Sports",
            "node": "9408876011",
        },
        "mobile-apps-transportation": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A10298308011",
            "label": "Transportation",
            "node": "10298308011",
        },
        "mobile-apps-travel": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408785011",
            "label": "Travel",
            "node": "9408785011",
        },
        "mobile-apps-utilities": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408914011",
            "label": "Utilities",
            "node": "9408914011",
        },
        "mobile-apps-weather": {
            "url": "https://www.amazon.com/s?i=mobile-apps&rh=n%3A2350149011%2Cn%3A9408850011",
            "label": "Weather",
            "node": "9408850011",
        },
        "mobile-apps": {
            "url": "https://www.amazon.com/s?i=mobile-apps",
            "label": "Apps & Games",
        },
    },
    "arts-crafts": {
        "arts-crafts-beading-jewelry-making": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12896081",
            "label": "Beading & Jewelry Making",
            "node": "12896081",
        },
        "arts-crafts-crafting": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A378733011",
            "label": "Crafting",
            "node": "378733011",
        },
        "arts-crafts-fabric": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12899121",
            "label": "Fabric",
            "node": "12899121",
        },
        "arts-crafts-fabric-decorating": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12896841",
            "label": "Fabric Decorating",
            "node": "12896841",
        },
        "arts-crafts-gift-wrapping-supplies": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A723452011",
            "label": "Gift Wrapping Supplies",
            "node": "723452011",
        },
        "arts-crafts-knitting-crochet": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12897221",
            "label": "Knitting & Crochet",
            "node": "12897221",
        },
        "arts-crafts-model-hobby-building": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A23539912011",
            "label": "Model & Hobby Building",
            "node": "23539912011",
        },
        "arts-crafts-needlework": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A2237329011",
            "label": "Needlework",
            "node": "2237329011",
        },
        "arts-crafts-organization-storage-transport": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A2237594011",
            "label": "Organization, Storage & Transport",
            "node": "2237594011",
        },
        "arts-crafts-painting-drawing-art-supplies": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A2747968011",
            "label": "Painting, Drawing & Art Supplies",
            "node": "2747968011",
        },
        "arts-crafts-party-decorations-supplies": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A723469011",
            "label": "Party Decorations & Supplies",
            "node": "723469011",
        },
        "arts-crafts-printmaking": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12898451",
            "label": "Printmaking",
            "node": "12898451",
        },
        "arts-crafts-scrapbooking-stamping": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12898821",
            "label": "Scrapbooking & Stamping",
            "node": "12898821",
        },
        "arts-crafts-sewing": {
            "url": "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011%2Cn%3A12899091",
            "label": "Sewing",
            "node": "12899091",
        },
        "arts-crafts": {
            "url": "https://www.amazon.com/s?i=arts-crafts",
            "label": "Arts, Crafts & Sewing",
        },
    },
    "audible": {
        "audible-arts-entertainment": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18571910011",
            "label": "Arts & Entertainment",
            "node": "18571910011",
        },
        "audible-biographies-memoirs": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18571951011",
            "label": "Biographies & Memoirs",
            "node": "18571951011",
        },
        "audible-business-careers": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18572029011",
            "label": "Business & Careers",
            "node": "18572029011",
        },
        "audible-children-s-audiobooks": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18572091011",
            "label": "Children's Audiobooks",
            "node": "18572091011",
        },
        "audible-comedy-humor": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A24427740011",
            "label": "Comedy & Humor",
            "node": "24427740011",
        },
        "audible-computers-technology": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573211011",
            "label": "Computers & Technology",
            "node": "18573211011",
        },
        "audible-education-learning": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573267011",
            "label": "Education & Learning",
            "node": "18573267011",
        },
        "audible-erotica": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573351011",
            "label": "Erotica",
            "node": "18573351011",
        },
        "audible-health-wellness": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573370011",
            "label": "Health & Wellness",
            "node": "18573370011",
        },
        "audible-history": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573518011",
            "label": "History",
            "node": "18573518011",
        },
        "audible-home-garden": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573701011",
            "label": "Home & Garden",
            "node": "18573701011",
        },
        "audible-lgbtq": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18573743011",
            "label": "LGBTQ+",
            "node": "18573743011",
        },
        "audible-literature-fiction": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18574426011",
            "label": "Literature & Fiction",
            "node": "18574426011",
        },
        "audible-money-finance": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18574547011",
            "label": "Money & Finance",
            "node": "18574547011",
        },
        "audible-mystery-thriller-suspense": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18574597011",
            "label": "Mystery, Thriller & Suspense",
            "node": "18574597011",
        },
        "audible-politics-social-sciences": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18574641011",
            "label": "Politics & Social Sciences",
            "node": "18574641011",
        },
        "audible-relationships-parenting-personal-development": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18574784011",
            "label": "Relationships, Parenting & Personal Development",
            "node": "18574784011",
        },
        "audible-religion-spirituality": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18574839011",
            "label": "Religion & Spirituality",
            "node": "18574839011",
        },
        "audible-romance": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18580518011",
            "label": "Romance",
            "node": "18580518011",
        },
        "audible-science-engineering": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18580540011",
            "label": "Science & Engineering",
            "node": "18580540011",
        },
        "audible-science-fiction-fantasy": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18580606011",
            "label": "Science Fiction & Fantasy",
            "node": "18580606011",
        },
        "audible-sports-outdoors": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18580648011",
            "label": "Sports & Outdoors",
            "node": "18580648011",
        },
        "audible-teen-young-adult": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18580715011",
            "label": "Teen & Young Adult",
            "node": "18580715011",
        },
        "audible-travel-tourism": {
            "url": "https://www.amazon.com/s?i=audible&rh=n%3A18145289011%2Cn%3A18581095011",
            "label": "Travel & Tourism",
            "node": "18581095011",
        },
        "audible": {
            "url": "https://www.amazon.com/s?i=audible",
            "label": "Audible Books & Originals",
        },
    },
    "automotive": {
        "automotive-car-care": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15718271",
            "label": "Car Care",
            "node": "15718271",
        },
        "automotive-car-electronics-accessories": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A2230642011",
            "label": "Car Electronics & Accessories",
            "node": "2230642011",
        },
        "automotive-exterior-accessories": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15857511",
            "label": "Exterior Accessories",
            "node": "15857511",
        },
        "automotive-interior-accessories": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15857501",
            "label": "Interior Accessories",
            "node": "15857501",
        },
        "automotive-lights-bulbs-indicators": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15736321",
            "label": "Lights, Bulbs & Indicators",
            "node": "15736321",
        },
        "automotive-motorcycle-powersports": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A346333011",
            "label": "Motorcycle & Powersports",
            "node": "346333011",
        },
        "automotive-oils-fluids": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15718791",
            "label": "Oils & Fluids",
            "node": "15718791",
        },
        "automotive-paint-paint-supplies": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A13591416011",
            "label": "Paint & Paint Supplies",
            "node": "13591416011",
        },
        "automotive-performance-parts-accessories": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15710351",
            "label": "Performance Parts & Accessories",
            "node": "15710351",
        },
        "automotive-replacement-parts": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15719731",
            "label": "Replacement Parts",
            "node": "15719731",
        },
        "automotive-rv-parts-accessories": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A2258019011",
            "label": "RV Parts & Accessories",
            "node": "2258019011",
        },
        "automotive-tires-wheels": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15706571",
            "label": "Tires & Wheels",
            "node": "15706571",
        },
        "automotive-tools-equipment": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15706941",
            "label": "Tools & Equipment",
            "node": "15706941",
        },
        "automotive-automotive-enthusiast-merchandise": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A2204830011",
            "label": "Automotive Enthusiast Merchandise",
            "node": "2204830011",
        },
        "automotive-heavy-duty-commercial-vehicle-equipment": {
            "url": "https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15682003011",
            "label": "Heavy Duty & Commercial Vehicle Equipment",
            "node": "15682003011",
        },
        "automotive": {
            "url": "https://www.amazon.com/s?i=automotive",
            "label": "Automotive Parts & Accessories",
        },
    },
    "baby-products": {
        "baby-products-activity-entertainment": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A239225011",
            "label": "Activity & Entertainment",
            "node": "239225011",
        },
        "baby-products-baby-toddler-toys": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A196601011",
            "label": "Baby & Toddler Toys",
            "node": "196601011",
        },
        "baby-products-baby-care": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A17720255011",
            "label": "Baby Care",
            "node": "17720255011",
        },
        "baby-products-baby-stationery": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A405369011",
            "label": "Baby Stationery",
            "node": "405369011",
        },
        "baby-products-car-seats-accessories": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A166835011",
            "label": "Car Seats & Accessories",
            "node": "166835011",
        },
        "baby-products-diapering": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A166764011",
            "label": "Diapering",
            "node": "166764011",
        },
        "baby-products-feeding": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A166777011",
            "label": "Feeding",
            "node": "166777011",
        },
        "baby-products-gifts": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A239226011",
            "label": "Gifts",
            "node": "239226011",
        },
        "baby-products-nursery": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A695338011",
            "label": "Nursery",
            "node": "695338011",
        },
        "baby-products-potty-training": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A166887011",
            "label": "Potty Training",
            "node": "166887011",
        },
        "baby-products-pregnancy-maternity": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A166804011",
            "label": "Pregnancy & Maternity",
            "node": "166804011",
        },
        "baby-products-safety": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A166863011",
            "label": "Safety",
            "node": "166863011",
        },
        "baby-products-strollers-accessories": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A8446318011",
            "label": "Strollers & Accessories",
            "node": "8446318011",
        },
        "baby-products-travel-gear": {
            "url": "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011%2Cn%3A17726796011",
            "label": "Travel Gear",
            "node": "17726796011",
        },
        "baby-products": {
            "url": "https://www.amazon.com/s?i=baby-products",
            "label": "Baby",
        },
    },
    "beauty": {
        "beauty-makeup": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A11058281",
            "label": "Makeup",
            "node": "11058281",
        },
        "beauty-skin-care": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A11060451",
            "label": "Skin Care",
            "node": "11060451",
        },
        "beauty-hair-care": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A11057241",
            "label": "Hair Care",
            "node": "11057241",
        },
        "beauty-fragrance": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A11056591",
            "label": "Fragrance",
            "node": "11056591",
        },
        "beauty-foot-hand-nail-care": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A17242866011",
            "label": "Foot, Hand & Nail Care",
            "node": "17242866011",
        },
        "beauty-tools-accessories": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A11062741",
            "label": "Tools & Accessories",
            "node": "11062741",
        },
        "beauty-shave-hair-removal": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A3778591",
            "label": "Shave & Hair Removal",
            "node": "3778591",
        },
        "beauty-personal-care": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A3777891",
            "label": "Personal Care",
            "node": "3777891",
        },
        "beauty-gift-sets": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A211908598011",
            "label": "Gift Sets",
            "node": "211908598011",
        },
        "beauty-salon-spa-equipment": {
            "url": "https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A15144566011",
            "label": "Salon & Spa Equipment",
            "node": "15144566011",
        },
        "beauty": {
            "url": "https://www.amazon.com/s?i=beauty",
            "label": "Beauty & Personal Care",
        },
    },
    "stripbooks": {
        "stripbooks-arts-photography": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A1",
            "label": "Arts & Photography",
            "node": "1",
        },
        "stripbooks-biographies-memoirs": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A2",
            "label": "Biographies & Memoirs",
            "node": "2",
        },
        "stripbooks-business-money": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A3",
            "label": "Business & Money",
            "node": "3",
        },
        "stripbooks-calendars": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A3248857011",
            "label": "Calendars",
            "node": "3248857011",
        },
        "stripbooks-children-s-books": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A4",
            "label": "Children's Books",
            "node": "4",
        },
        "stripbooks-comics-graphic-novels": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A4366",
            "label": "Comics & Graphic Novels",
            "node": "4366",
        },
        "stripbooks-computers-technology": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A5",
            "label": "Computers & Technology",
            "node": "5",
        },
        "stripbooks-cookbooks-food-wine": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A6",
            "label": "Cookbooks, Food & Wine",
            "node": "6",
        },
        "stripbooks-crafts-hobbies-home": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A48",
            "label": "Crafts, Hobbies & Home",
            "node": "48",
        },
        "stripbooks-education-teaching": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A8975347011",
            "label": "Education & Teaching",
            "node": "8975347011",
        },
        "stripbooks-engineering-transportation": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A173507",
            "label": "Engineering & Transportation",
            "node": "173507",
        },
        "stripbooks-health-fitness-dieting": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A10",
            "label": "Health, Fitness & Dieting",
            "node": "10",
        },
        "stripbooks-history": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A9",
            "label": "History",
            "node": "9",
        },
        "stripbooks-humor-entertainment": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A86",
            "label": "Humor & Entertainment",
            "node": "86",
        },
        "stripbooks-law": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A10777",
            "label": "Law",
            "node": "10777",
        },
        "stripbooks-lgbtq-books": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A301889",
            "label": "LGBTQ+ Books",
            "node": "301889",
        },
        "stripbooks-literature-fiction": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A17",
            "label": "Literature & Fiction",
            "node": "17",
        },
        "stripbooks-medical-books": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A173514",
            "label": "Medical Books",
            "node": "173514",
        },
        "stripbooks-mystery-thriller-suspense": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A18",
            "label": "Mystery, Thriller & Suspense",
            "node": "18",
        },
        "stripbooks-parenting-relationships": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A20",
            "label": "Parenting & Relationships",
            "node": "20",
        },
        "stripbooks-politics-social-sciences": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A3377866011",
            "label": "Politics & Social Sciences",
            "node": "3377866011",
        },
        "stripbooks-reference": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A21",
            "label": "Reference",
            "node": "21",
        },
        "stripbooks-religion-spirituality": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A22",
            "label": "Religion & Spirituality",
            "node": "22",
        },
        "stripbooks-romance": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A23",
            "label": "Romance",
            "node": "23",
        },
        "stripbooks-science-math": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A75",
            "label": "Science & Math",
            "node": "75",
        },
        "stripbooks-science-fiction-fantasy": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A25",
            "label": "Science Fiction & Fantasy",
            "node": "25",
        },
        "stripbooks-self-help": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A4736",
            "label": "Self-Help",
            "node": "4736",
        },
        "stripbooks-sports-outdoors": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A26",
            "label": "Sports & Outdoors",
            "node": "26",
        },
        "stripbooks-teen-young-adult": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A28",
            "label": "Teen & Young Adult",
            "node": "28",
        },
        "stripbooks-test-preparation": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A5267710011",
            "label": "Test Preparation",
            "node": "5267710011",
        },
        "stripbooks-travel": {
            "url": "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155%2Cn%3A27",
            "label": "Travel",
            "node": "27",
        },
        "stripbooks": {
            "url": "https://www.amazon.com/s?i=stripbooks",
            "label": "Books",
        },
    },
    "popular": {
        "popular-blues": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A31",
            "label": "Blues",
            "node": "31",
        },
        "popular-broadway-vocalists": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A265640",
            "label": "Broadway & Vocalists",
            "node": "265640",
        },
        "popular-children-s-music": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A173425",
            "label": "Children's Music",
            "node": "173425",
        },
        "popular-christian-gospel": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A173429",
            "label": "Christian & Gospel",
            "node": "173429",
        },
        "popular-classic-rock": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A67204",
            "label": "Classic Rock",
            "node": "67204",
        },
        "popular-classical": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A85",
            "label": "Classical",
            "node": "85",
        },
        "popular-comedy-spoken-word": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A63936",
            "label": "Comedy & Spoken Word",
            "node": "63936",
        },
        "popular-country": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A16",
            "label": "Country",
            "node": "16",
        },
        "popular-dance-electronic": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A7",
            "label": "Dance & Electronic",
            "node": "7",
        },
        "popular-folk": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A32",
            "label": "Folk",
            "node": "32",
        },
        "popular-holiday-wedding": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A292572",
            "label": "Holiday & Wedding",
            "node": "292572",
        },
        "popular-indie-alternative": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A21165438011",
            "label": "Indie & Alternative",
            "node": "21165438011",
        },
        "popular-international-music": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A33",
            "label": "International Music",
            "node": "33",
        },
        "popular-jazz": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A34",
            "label": "Jazz",
            "node": "34",
        },
        "popular-karaoke": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A63945",
            "label": "Karaoke",
            "node": "63945",
        },
        "popular-latin-music": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A289122",
            "label": "Latin Music",
            "node": "289122",
        },
        "popular-metal": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A67207",
            "label": "Metal",
            "node": "67207",
        },
        "popular-new-age": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A36",
            "label": "New Age",
            "node": "36",
        },
        "popular-opera-classical-vocal": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A84",
            "label": "Opera & Classical Vocal",
            "node": "84",
        },
        "popular-pop": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A37",
            "label": "Pop",
            "node": "37",
        },
        "popular-r-b": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A39",
            "label": "R&B",
            "node": "39",
        },
        "popular-rap-hip-hop": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A38",
            "label": "Rap & Hip-Hop",
            "node": "38",
        },
        "popular-reggae": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A63885",
            "label": "Reggae",
            "node": "63885",
        },
        "popular-rock": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A40",
            "label": "Rock",
            "node": "40",
        },
        "popular-soundtracks": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A42",
            "label": "Soundtracks",
            "node": "42",
        },
        "popular-special-interest": {
            "url": "https://www.amazon.com/s?i=popular&rh=n%3A5174%2Cn%3A35",
            "label": "Special Interest",
            "node": "35",
        },
        "popular": {
            "url": "https://www.amazon.com/s?i=popular",
            "label": "CDs & Vinyl",
        },
    },
    "mobile": {
        "mobile-accessories": {
            "url": "https://www.amazon.com/s?i=mobile&rh=n%3A2335752011%2Cn%3A2407755011",
            "label": "Accessories",
            "node": "2407755011",
        },
        "mobile-cases-holsters-sleeves": {
            "url": "https://www.amazon.com/s?i=mobile&rh=n%3A2335752011%2Cn%3A2407760011",
            "label": "Cases, Holsters & Sleeves",
            "node": "2407760011",
        },
        "mobile-cell-phones": {
            "url": "https://www.amazon.com/s?i=mobile&rh=n%3A2335752011%2Cn%3A7072561011",
            "label": "Cell Phones",
            "node": "7072561011",
        },
        "mobile-sim-cards-prepaid-minutes": {
            "url": "https://www.amazon.com/s?i=mobile&rh=n%3A2335752011%2Cn%3A3345523011",
            "label": "SIM Cards & Prepaid Minutes",
            "node": "3345523011",
        },
        "mobile": {
            "url": "https://www.amazon.com/s?i=mobile",
            "label": "Cell Phones & Accessories",
        },
    },
    "fashion": {
        "fashion-novelty-more": {
            "url": "https://www.amazon.com/s?i=fashion&rh=n%3A7141123011%2Cn%3A7147445011",
            "label": "Novelty & More",
            "node": "7147445011",
        },
        "fashion-uniforms-work-safety": {
            "url": "https://www.amazon.com/s?i=fashion&rh=n%3A7141123011%2Cn%3A7586144011",
            "label": "Uniforms, Work & Safety",
            "node": "7586144011",
        },
        "fashion-costumes-accessories": {
            "url": "https://www.amazon.com/s?i=fashion&rh=n%3A7141123011%2Cn%3A7586165011",
            "label": "Costumes & Accessories",
            "node": "7586165011",
        },
        "fashion-shoe-jewelry-watch-accessories": {
            "url": "https://www.amazon.com/s?i=fashion&rh=n%3A7141123011%2Cn%3A7586146011",
            "label": "Shoe, Jewelry & Watch Accessories",
            "node": "7586146011",
        },
        "fashion-sport-specific-clothing": {
            "url": "https://www.amazon.com/s?i=fashion&rh=n%3A7141123011%2Cn%3A23575629011",
            "label": "Sport Specific Clothing",
            "node": "23575629011",
        },
        "fashion": {
            "url": "https://www.amazon.com/s?i=fashion",
            "label": "Clothing, Shoes & Jewelry",
        },
    },
    "fashion-womens": {
        "fashion-womens-clothing": {
            "url": "https://www.amazon.com/s?i=fashion-womens&rh=n%3A7147440011%2Cn%3A1040660",
            "label": "Clothing",
            "node": "1040660",
        },
        "fashion-womens-shoes": {
            "url": "https://www.amazon.com/s?i=fashion-womens&rh=n%3A7147440011%2Cn%3A679337011",
            "label": "Shoes",
            "node": "679337011",
        },
        "fashion-womens-jewelry": {
            "url": "https://www.amazon.com/s?i=fashion-womens&rh=n%3A7147440011%2Cn%3A7192394011",
            "label": "Jewelry",
            "node": "7192394011",
        },
        "fashion-womens-watches": {
            "url": "https://www.amazon.com/s?i=fashion-womens&rh=n%3A7147440011%2Cn%3A6358543011",
            "label": "Watches",
            "node": "6358543011",
        },
        "fashion-womens-handbags-wallets": {
            "url": "https://www.amazon.com/s?i=fashion-womens&rh=n%3A7147440011%2Cn%3A15743631",
            "label": "Handbags & Wallets",
            "node": "15743631",
        },
        "fashion-womens-accessories": {
            "url": "https://www.amazon.com/s?i=fashion-womens&rh=n%3A7147440011%2Cn%3A2474936011",
            "label": "Accessories",
            "node": "2474936011",
        },
        "fashion-womens": {
            "url": "https://www.amazon.com/s?i=fashion-womens",
            "label": "Women's Clothing, Shoes & Jewelry",
        },
    },
    "fashion-mens": {
        "fashion-mens-clothing": {
            "url": "https://www.amazon.com/s?i=fashion-mens&rh=n%3A7147441011%2Cn%3A1040658",
            "label": "Clothing",
            "node": "1040658",
        },
        "fashion-mens-shoes": {
            "url": "https://www.amazon.com/s?i=fashion-mens&rh=n%3A7147441011%2Cn%3A679255011",
            "label": "Shoes",
            "node": "679255011",
        },
        "fashion-mens-jewelry": {
            "url": "https://www.amazon.com/s?i=fashion-mens&rh=n%3A7147441011%2Cn%3A3887881",
            "label": "Jewelry",
            "node": "3887881",
        },
        "fashion-mens-watches": {
            "url": "https://www.amazon.com/s?i=fashion-mens&rh=n%3A7147441011%2Cn%3A6358539011",
            "label": "Watches",
            "node": "6358539011",
        },
        "fashion-mens-accessories": {
            "url": "https://www.amazon.com/s?i=fashion-mens&rh=n%3A7147441011%2Cn%3A2474937011",
            "label": "Accessories",
            "node": "2474937011",
        },
        "fashion-mens-handbags-shoulder-bags": {
            "url": "https://www.amazon.com/s?i=fashion-mens&rh=n%3A7147441011%2Cn%3A14864589011",
            "label": "Handbags & Shoulder Bags",
            "node": "14864589011",
        },
        "fashion-mens": {
            "url": "https://www.amazon.com/s?i=fashion-mens",
            "label": "Men's Clothing, Shoes & Jewelry",
        },
    },
    "fashion-girls": {
        "fashion-girls-clothing": {
            "url": "https://www.amazon.com/s?i=fashion-girls&rh=n%3A7147442011%2Cn%3A1040664",
            "label": "Clothing",
            "node": "1040664",
        },
        "fashion-girls-shoes": {
            "url": "https://www.amazon.com/s?i=fashion-girls&rh=n%3A7147442011%2Cn%3A679217011",
            "label": "Shoes",
            "node": "679217011",
        },
        "fashion-girls-jewelry": {
            "url": "https://www.amazon.com/s?i=fashion-girls&rh=n%3A7147442011%2Cn%3A3880961",
            "label": "Jewelry",
            "node": "3880961",
        },
        "fashion-girls-watches": {
            "url": "https://www.amazon.com/s?i=fashion-girls&rh=n%3A7147442011%2Cn%3A6358547011",
            "label": "Watches",
            "node": "6358547011",
        },
        "fashion-girls-accessories": {
            "url": "https://www.amazon.com/s?i=fashion-girls&rh=n%3A7147442011%2Cn%3A2474938011",
            "label": "Accessories",
            "node": "2474938011",
        },
        "fashion-girls-handbags-shoulder-bags": {
            "url": "https://www.amazon.com/s?i=fashion-girls&rh=n%3A7147442011%2Cn%3A205664993011",
            "label": "Handbags & Shoulder Bags",
            "node": "205664993011",
        },
        "fashion-girls": {
            "url": "https://www.amazon.com/s?i=fashion-girls",
            "label": "Girl's Clothing, Shoes & Jewelry",
        },
    },
    "fashion-boys": {
        "fashion-boys-clothing": {
            "url": "https://www.amazon.com/s?i=fashion-boys&rh=n%3A7147443011%2Cn%3A1040666",
            "label": "Clothing",
            "node": "1040666",
        },
        "fashion-boys-shoes": {
            "url": "https://www.amazon.com/s?i=fashion-boys&rh=n%3A7147443011%2Cn%3A679182011",
            "label": "Shoes",
            "node": "679182011",
        },
        "fashion-boys-watches": {
            "url": "https://www.amazon.com/s?i=fashion-boys&rh=n%3A7147443011%2Cn%3A6358551011",
            "label": "Watches",
            "node": "6358551011",
        },
        "fashion-boys-accessories": {
            "url": "https://www.amazon.com/s?i=fashion-boys&rh=n%3A7147443011%2Cn%3A2474939011",
            "label": "Accessories",
            "node": "2474939011",
        },
        "fashion-boys-jewelry": {
            "url": "https://www.amazon.com/s?i=fashion-boys&rh=n%3A7147443011%2Cn%3A3880611",
            "label": "Jewelry",
            "node": "3880611",
        },
        "fashion-boys": {
            "url": "https://www.amazon.com/s?i=fashion-boys",
            "label": "Boy's Clothing, Shoes & Jewelry",
        },
    },
    "fashion-baby": {
        "fashion-baby-baby-girls": {
            "url": "https://www.amazon.com/s?i=fashion-baby&rh=n%3A7147444011%2Cn%3A7628012011",
            "label": "Baby Girls",
            "node": "7628012011",
        },
        "fashion-baby-baby-boys": {
            "url": "https://www.amazon.com/s?i=fashion-baby&rh=n%3A7147444011%2Cn%3A7628013011",
            "label": "Baby Boys",
            "node": "7628013011",
        },
        "fashion-baby": {
            "url": "https://www.amazon.com/s?i=fashion-baby",
            "label": "Baby Clothing, Shoes & Jewelry",
        },
    },
    "collectibles": {
        "collectibles-advertising": {
            "url": "https://www.amazon.com/s?i=collectibles&rh=n%3A4991425011%2Cn%3A7301170011",
            "label": "Advertising",
            "node": "7301170011",
        },
        "collectibles-collectible-coins": {
            "url": "https://www.amazon.com/s?i=collectibles&rh=n%3A4991425011%2Cn%3A9003130011",
            "label": "Collectible Coins",
            "node": "9003130011",
        },
        "collectibles-entertainment": {
            "url": "https://www.amazon.com/s?i=collectibles&rh=n%3A4991425011%2Cn%3A5088769011",
            "label": "Entertainment",
            "node": "5088769011",
        },
        "collectibles-fine-art": {
            "url": "https://www.amazon.com/s?i=collectibles&rh=n%3A4991425011%2Cn%3A6685269011",
            "label": "Fine Art",
            "node": "6685269011",
        },
        "collectibles-historical-political": {
            "url": "https://www.amazon.com/s?i=collectibles&rh=n%3A4991425011%2Cn%3A5525092011",
            "label": "Historical & Political",
            "node": "5525092011",
        },
        "collectibles-sports": {
            "url": "https://www.amazon.com/s?i=collectibles&rh=n%3A4991425011%2Cn%3A3250697011",
            "label": "Sports",
            "node": "3250697011",
        },
        "collectibles": {
            "url": "https://www.amazon.com/s?i=collectibles",
            "label": "Collectibles & Fine Art",
        },
    },
    "computers": {
        "computers-computer-accessories-peripherals": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A172456",
            "label": "Computer Accessories & Peripherals",
            "node": "172456",
        },
        "computers-computer-components": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A193870011",
            "label": "Computer Components",
            "node": "193870011",
        },
        "computers-computers-tablets": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A13896617011",
            "label": "Computers & Tablets",
            "node": "13896617011",
        },
        "computers-data-storage": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A1292110011",
            "label": "Data Storage",
            "node": "1292110011",
        },
        "computers-laptop-accessories": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A3011391011",
            "label": "Laptop Accessories",
            "node": "3011391011",
        },
        "computers-monitors": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A1292115011",
            "label": "Monitors",
            "node": "1292115011",
        },
        "computers-networking-products": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A172504",
            "label": "Networking Products",
            "node": "172504",
        },
        "computers-servers": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A11036071",
            "label": "Servers",
            "node": "11036071",
        },
        "computers-tablet-accessories": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A2348628011",
            "label": "Tablet Accessories",
            "node": "2348628011",
        },
        "computers-tablet-replacement-parts": {
            "url": "https://www.amazon.com/s?i=computers&rh=n%3A541966%2Cn%3A15524379011",
            "label": "Tablet Replacement Parts",
            "node": "15524379011",
        },
        "computers": {
            "url": "https://www.amazon.com/s?i=computers",
            "label": "Computers",
        },
    },
    "financial": {
        "financial-credit-cards": {
            "url": "https://www.amazon.com/s?i=financial&rh=n%3A3561432011%2Cn%3A5652905011",
            "label": "Credit Cards",
            "node": "5652905011",
        },
        "financial": {
            "url": "https://www.amazon.com/s?i=financial",
            "label": "Credit and Payment Cards",
        },
    },
    "digital-music": {
        "digital-music-blues": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624881011",
            "label": "Blues",
            "node": "624881011",
        },
        "digital-music-broadway-vocalists": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624894011",
            "label": "Broadway & Vocalists",
            "node": "624894011",
        },
        "digital-music-children-s-music": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624899011",
            "label": "Children's Music",
            "node": "624899011",
        },
        "digital-music-christian-gospel": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624905011",
            "label": "Christian & Gospel",
            "node": "624905011",
        },
        "digital-music-classical": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624926011",
            "label": "Classical",
            "node": "624926011",
        },
        "digital-music-classic-rock": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624916011",
            "label": "Classic Rock",
            "node": "624916011",
        },
        "digital-music-country": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624976011",
            "label": "Country",
            "node": "624976011",
        },
        "digital-music-dance-electronic": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A624988011",
            "label": "Dance & Electronic",
            "node": "624988011",
        },
        "digital-music-folk": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625003011",
            "label": "Folk",
            "node": "625003011",
        },
        "digital-music-hard-rock-metal": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625011011",
            "label": "Hard Rock & Metal",
            "node": "625011011",
        },
        "digital-music-holiday": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625065011",
            "label": "Holiday",
            "node": "625065011",
        },
        "digital-music-indie-alternative": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A19387930011",
            "label": "Indie & Alternative",
            "node": "19387930011",
        },
        "digital-music-jazz": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625036011",
            "label": "Jazz",
            "node": "625036011",
        },
        "digital-music-latin-music": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625054011",
            "label": "Latin Music",
            "node": "625054011",
        },
        "digital-music-new-age": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625070011",
            "label": "New Age",
            "node": "625070011",
        },
        "digital-music-opera": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625075011",
            "label": "Opera",
            "node": "625075011",
        },
        "digital-music-r-b": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625105011",
            "label": "R&B",
            "node": "625105011",
        },
        "digital-music-rap-hip-hop": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625117011",
            "label": "Rap & Hip-Hop",
            "node": "625117011",
        },
        "digital-music-rock": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625129011",
            "label": "Rock",
            "node": "625129011",
        },
        "digital-music-soundtracks": {
            "url": "https://www.amazon.com/s?i=digital-music&rh=n%3A163856011%2Cn%3A625144011",
            "label": "Soundtracks",
            "node": "625144011",
        },
        "digital-music": {
            "url": "https://www.amazon.com/s?i=digital-music",
            "label": "Digital Music",
        },
    },
    "electronics": {
        "electronics-accessories-supplies": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A281407",
            "label": "Accessories & Supplies",
            "node": "281407",
        },
        "electronics-camera-photo": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A502394",
            "label": "Camera & Photo",
            "node": "502394",
        },
        "electronics-car-vehicle-electronics": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A3248684011",
            "label": "Car & Vehicle Electronics",
            "node": "3248684011",
        },
        "electronics-cell-phones-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A2811119011",
            "label": "Cell Phones & Accessories",
            "node": "2811119011",
        },
        "electronics-electronic-protection-plans": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A2242348011",
            "label": "Electronic Protection Plans",
            "node": "2242348011",
        },
        "electronics-gps-finders-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A172526",
            "label": "GPS, Finders & Accessories",
            "node": "172526",
        },
        "electronics-home-audio": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A667846011",
            "label": "Home Audio",
            "node": "667846011",
        },
        "electronics-office-electronics": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A172574",
            "label": "Office Electronics",
            "node": "172574",
        },
        "electronics-portable-audio-video": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A172623",
            "label": "Portable Audio & Video",
            "node": "172623",
        },
        "electronics-security-surveillance": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A524136",
            "label": "Security & Surveillance",
            "node": "524136",
        },
        "electronics-service-plans": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A16285901",
            "label": "Service Plans",
            "node": "16285901",
        },
        "electronics-television-video": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A1266092011",
            "label": "Television & Video",
            "node": "1266092011",
        },
        "electronics-video-game-consoles-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A7926841011",
            "label": "Video Game Consoles & Accessories",
            "node": "7926841011",
        },
        "electronics-video-projectors": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A300334",
            "label": "Video Projectors",
            "node": "300334",
        },
        "electronics-wearable-technology": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A10048700011",
            "label": "Wearable Technology",
            "node": "10048700011",
        },
        "electronics-ebook-readers-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A2642125011",
            "label": "eBook Readers & Accessories",
            "node": "2642125011",
        },
        "electronics-headphones-earbuds-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A24046923011",
            "label": "Headphones, Earbuds & Accessories",
            "node": "24046923011",
        },
        "electronics-household-batteries-chargers-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A21608214011",
            "label": "Household Batteries, Chargers & Accessories",
            "node": "21608214011",
        },
        "electronics-power-accessories": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A21608215011",
            "label": "Power Accessories",
            "node": "21608215011",
        },
        "electronics-tablets": {
            "url": "https://www.amazon.com/s?i=electronics&rh=n%3A172282%2Cn%3A1232597011",
            "label": "Tablets",
            "node": "1232597011",
        },
        "electronics": {
            "url": "https://www.amazon.com/s?i=electronics",
            "label": "Electronics",
        },
    },
    "lawngarden": {
        "lawngarden-gardening-lawn-care": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A3610851",
            "label": "Gardening & Lawn Care",
            "node": "3610851",
        },
        "lawngarden-outdoor-d-cor": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A553788",
            "label": "Outdoor Décor",
            "node": "553788",
        },
        "lawngarden-patio-furniture-accessories": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A553824",
            "label": "Patio Furniture & Accessories",
            "node": "553824",
        },
        "lawngarden-grills-outdoor-cooking": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A553760",
            "label": "Grills & Outdoor Cooking",
            "node": "553760",
        },
        "lawngarden-outdoor-lighting": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A495236",
            "label": "Outdoor Lighting",
            "node": "495236",
        },
        "lawngarden-outdoor-power-tools": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A551242",
            "label": "Outdoor Power Tools",
            "node": "551242",
        },
        "lawngarden-pools-hot-tubs-supplies": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A1272941011",
            "label": "Pools, Hot Tubs & Supplies",
            "node": "1272941011",
        },
        "lawngarden-generators-portable-power": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A552808",
            "label": "Generators & Portable Power",
            "node": "552808",
        },
        "lawngarden-pest-control": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A553844",
            "label": "Pest Control",
            "node": "553844",
        },
        "lawngarden-snow-removal": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A3043471",
            "label": "Snow Removal",
            "node": "3043471",
        },
        "lawngarden-outdoor-heating-cooling": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A13638732011",
            "label": "Outdoor Heating & Cooling",
            "node": "13638732011",
        },
        "lawngarden-outdoor-storage-housing": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A13400641",
            "label": "Outdoor Storage & Housing",
            "node": "13400641",
        },
        "lawngarden-farm-ranch": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A4619352011",
            "label": "Farm & Ranch",
            "node": "4619352011",
        },
        "lawngarden-backyard-birding-wildlife": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A553632",
            "label": "Backyard Birding & Wildlife",
            "node": "553632",
        },
        "lawngarden-lawn-plant-care": {
            "url": "https://www.amazon.com/s?i=lawngarden&rh=n%3A2972638011%2Cn%3A215739575011",
            "label": "Lawn & Plant Care",
            "node": "215739575011",
        },
        "lawngarden": {
            "url": "https://www.amazon.com/s?i=lawngarden",
            "label": "Garden & Outdoor",
        },
    },
    "gift-cards": {
        "gift-cards-gift-cards": {
            "url": "https://www.amazon.com/s?i=gift-cards&rh=n%3A2238192011%2Cn%3A2864196011",
            "label": "Gift Cards",
            "node": "2864196011",
        },
        "gift-cards": {
            "url": "https://www.amazon.com/s?i=gift-cards",
            "label": "Gift Cards",
        },
    },
    "grocery": {
        "grocery-alcoholic-beverages": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A2983371011",
            "label": "Alcoholic Beverages",
            "node": "2983371011",
        },
        "grocery-baby-foods": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A16323111",
            "label": "Baby Foods",
            "node": "16323111",
        },
        "grocery-beverages": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A16310231",
            "label": "Beverages",
            "node": "16310231",
        },
        "grocery-breads-bakery": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A16318751",
            "label": "Breads & Bakery",
            "node": "16318751",
        },
        "grocery-breakfast-cereal": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A118518014011",
            "label": "Breakfast Cereal",
            "node": "118518014011",
        },
        "grocery-breakfast-foods": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A16310251",
            "label": "Breakfast Foods",
            "node": "16310251",
        },
        "grocery-dairy-eggs-plant-based-alternatives": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A371460011",
            "label": "Dairy, Eggs & Plant-Based Alternatives",
            "node": "371460011",
        },
        "grocery-deli-prepared-foods": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A18773724011",
            "label": "Deli & Prepared Foods",
            "node": "18773724011",
        },
        "grocery-food-beverage-gifts": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A2255571011",
            "label": "Food & Beverage Gifts",
            "node": "2255571011",
        },
        "grocery-fresh-flowers-live-indoor-plants": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A3745171",
            "label": "Fresh Flowers & Live Indoor Plants",
            "node": "3745171",
        },
        "grocery-fresh-meal-kits": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A15709227011",
            "label": "Fresh Meal Kits",
            "node": "15709227011",
        },
        "grocery-frozen": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A6459122011",
            "label": "Frozen",
            "node": "6459122011",
        },
        "grocery-home-brewing-winemaking": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A979861011",
            "label": "Home Brewing & Winemaking",
            "node": "979861011",
        },
        "grocery-meat-seafood": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A371469011",
            "label": "Meat & Seafood",
            "node": "371469011",
        },
        "grocery-meat-substitutes": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A6518859011",
            "label": "Meat Substitutes",
            "node": "6518859011",
        },
        "grocery-pantry-staples": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A18787303011",
            "label": "Pantry Staples",
            "node": "18787303011",
        },
        "grocery-produce": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A6506977011",
            "label": "Produce",
            "node": "6506977011",
        },
        "grocery-snacks-sweets": {
            "url": "https://www.amazon.com/s?i=grocery&rh=n%3A16310101%2Cn%3A23759921011",
            "label": "Snacks & Sweets",
            "node": "23759921011",
        },
        "grocery": {
            "url": "https://www.amazon.com/s?i=grocery",
            "label": "Grocery & Gourmet Food",
        },
    },
    "handmade": {
        "handmade": {
            "url": "https://www.amazon.com/s?i=handmade",
            "label": "Handmade",
        },
    },
    "hpc": {
        "hpc-baby-child-care": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A10787321",
            "label": "Baby & Child Care",
            "node": "10787321",
        },
        "hpc-health-care": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A3760941",
            "label": "Health Care",
            "node": "3760941",
        },
        "hpc-household-supplies": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A15342811",
            "label": "Household Supplies",
            "node": "15342811",
        },
        "hpc-medical-supplies-equipment": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A3775161",
            "label": "Medical Supplies & Equipment",
            "node": "3775161",
        },
        "hpc-oral-care": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A10079992011",
            "label": "Oral Care",
            "node": "10079992011",
        },
        "hpc-prescription-medications": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A19763358011",
            "label": "Prescription Medications",
            "node": "19763358011",
        },
        "hpc-sexual-wellness": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A3777371",
            "label": "Sexual Wellness",
            "node": "3777371",
        },
        "hpc-stationery-gift-wrapping-supplies": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A723418011",
            "label": "Stationery & Gift Wrapping Supplies",
            "node": "723418011",
        },
        "hpc-vision": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A10079994011",
            "label": "Vision",
            "node": "10079994011",
        },
        "hpc-diet-sports-nutrition": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A3764441",
            "label": "Diet & Sports Nutrition",
            "node": "3764441",
        },
        "hpc-wellness-relaxation": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A10079996011",
            "label": "Wellness & Relaxation",
            "node": "10079996011",
        },
        "hpc-vitamins-minerals-supplements": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A23675621011",
            "label": "Vitamins, Minerals & Supplements",
            "node": "23675621011",
        },
        "hpc-funeral": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A8622234011",
            "label": "Funeral",
            "node": "8622234011",
        },
        "hpc-personal-care": {
            "url": "https://www.amazon.com/s?i=hpc&rh=n%3A3760901%2Cn%3A3777891",
            "label": "Personal Care",
            "node": "3777891",
        },
        "hpc": {
            "url": "https://www.amazon.com/s?i=hpc",
            "label": "Health, Household & Baby Care",
        },
    },
    "local-services": {
        "local-services": {
            "url": "https://www.amazon.com/s?i=local-services",
            "label": "Home & Business Services",
        },
    },
    "garden": {
        "garden-kids-home-store": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A3206325011",
            "label": "Kids' Home Store",
            "node": "3206325011",
        },
        "garden-kitchen-dining": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A284507",
            "label": "Kitchen & Dining",
            "node": "284507",
        },
        "garden-bedding": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A1063252",
            "label": "Bedding",
            "node": "1063252",
        },
        "garden-bath": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A1063236",
            "label": "Bath",
            "node": "1063236",
        },
        "garden-furniture": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A1063306",
            "label": "Furniture",
            "node": "1063306",
        },
        "garden-home-d-cor-products": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A1063278",
            "label": "Home Décor Products",
            "node": "1063278",
        },
        "garden-wall-art": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A3736081",
            "label": "Wall Art",
            "node": "3736081",
        },
        "garden-lighting-ceiling-fans": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A16510975011",
            "label": "Lighting & Ceiling Fans",
            "node": "16510975011",
        },
        "garden-seasonal-d-cor": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A13679381",
            "label": "Seasonal Décor",
            "node": "13679381",
        },
        "garden-event-party-supplies": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A901590",
            "label": "Event & Party Supplies",
            "node": "901590",
        },
        "garden-heating-cooling-air-quality": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A3206324011",
            "label": "Heating, Cooling & Air Quality",
            "node": "3206324011",
        },
        "garden-irons-steamers": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A510240",
            "label": "Irons & Steamers",
            "node": "510240",
        },
        "garden-vacuums-floor-care": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A510106",
            "label": "Vacuums & Floor Care",
            "node": "510106",
        },
        "garden-storage-organization": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A3610841",
            "label": "Storage & Organization",
            "node": "3610841",
        },
        "garden-cleaning-supplies": {
            "url": "https://www.amazon.com/s?i=garden&rh=n%3A1055398%2Cn%3A10802561",
            "label": "Cleaning Supplies",
            "node": "10802561",
        },
        "garden": {
            "url": "https://www.amazon.com/s?i=garden",
            "label": "Home & Kitchen",
        },
    },
    "industrial": {
        "industrial-abrasive-finishing-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A256167011",
            "label": "Abrasive & Finishing Products",
            "node": "256167011",
        },
        "industrial-additive-manufacturing-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A6066126011",
            "label": "Additive Manufacturing Products",
            "node": "6066126011",
        },
        "industrial-adhesives-sealants-lubricants": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A256225011",
            "label": "Adhesives, Sealants & Lubricants",
            "node": "256225011",
        },
        "industrial-commercial-door-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A10773802011",
            "label": "Commercial Door Products",
            "node": "10773802011",
        },
        "industrial-commercial-lighting": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A5772192011",
            "label": "Commercial Lighting",
            "node": "5772192011",
        },
        "industrial-cutting-tools": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A383598011",
            "label": "Cutting Tools",
            "node": "383598011",
        },
        "industrial-digital-signage": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A18746931011",
            "label": "Digital Signage",
            "node": "18746931011",
        },
        "industrial-fasteners": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A383599011",
            "label": "Fasteners",
            "node": "383599011",
        },
        "industrial-filtration": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A3061625011",
            "label": "Filtration",
            "node": "3061625011",
        },
        "industrial-food-service-equipment-supplies": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A6054382011",
            "label": "Food Service Equipment & Supplies",
            "node": "6054382011",
        },
        "industrial-hydraulics-pneumatics-plumbing": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A3021479011",
            "label": "Hydraulics, Pneumatics & Plumbing",
            "node": "3021479011",
        },
        "industrial-industrial-electrical": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A306506011",
            "label": "Industrial Electrical",
            "node": "306506011",
        },
        "industrial-industrial-hardware": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A16412251",
            "label": "Industrial Hardware",
            "node": "16412251",
        },
        "industrial-janitorial-sanitation-supplies": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A317971011",
            "label": "Janitorial & Sanitation Supplies",
            "node": "317971011",
        },
        "industrial-lab-scientific-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A317970011",
            "label": "Lab & Scientific Products",
            "node": "317970011",
        },
        "industrial-material-handling-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A256346011",
            "label": "Material Handling Products",
            "node": "256346011",
        },
        "industrial-occupational-health-safety-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A318135011",
            "label": "Occupational Health & Safety Products",
            "node": "318135011",
        },
        "industrial-packaging-shipping-supplies": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A8553197011",
            "label": "Packaging & Shipping Supplies",
            "node": "8553197011",
        },
        "industrial-power-hand-tools": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A3021459011",
            "label": "Power & Hand Tools",
            "node": "3021459011",
        },
        "industrial-power-transmission-products": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A16310181",
            "label": "Power Transmission Products",
            "node": "16310181",
        },
        "industrial-professional-dental-supplies": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A8297371011",
            "label": "Professional Dental Supplies",
            "node": "8297371011",
        },
        "industrial-professional-medical-supplies": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A8297370011",
            "label": "Professional Medical Supplies",
            "node": "8297370011",
        },
        "industrial-raw-materials": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A16310191",
            "label": "Raw Materials",
            "node": "16310191",
        },
        "industrial-retail-store-fixtures-equipment": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A8615538011",
            "label": "Retail Store Fixtures & Equipment",
            "node": "8615538011",
        },
        "industrial-robotics": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A8498884011",
            "label": "Robotics",
            "node": "8498884011",
        },
        "industrial-science-education": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A393459011",
            "label": "Science Education",
            "node": "393459011",
        },
        "industrial-test-measure-inspect": {
            "url": "https://www.amazon.com/s?i=industrial&rh=n%3A16310091%2Cn%3A256409011",
            "label": "Test, Measure & Inspect",
            "node": "256409011",
        },
        "industrial": {
            "url": "https://www.amazon.com/s?i=industrial",
            "label": "Industrial & Scientific",
        },
    },
    "prime-exclusive": {
        "prime-exclusive": {
            "url": "https://www.amazon.com/s?i=prime-exclusive",
            "label": "Just for Prime",
        },
    },
    "digital-text": {
        "digital-text-kindle-ebooks": {
            "url": "https://www.amazon.com/s?i=digital-text&rh=n%3A133140011%2Cn%3A154606011",
            "label": "Kindle eBooks",
            "node": "154606011",
        },
        "digital-text-kindle-short-reads": {
            "url": "https://www.amazon.com/s?i=digital-text&rh=n%3A133140011%2Cn%3A8584457011",
            "label": "Kindle Short Reads",
            "node": "8584457011",
        },
        "digital-text-kindle-singles": {
            "url": "https://www.amazon.com/s?i=digital-text&rh=n%3A133140011%2Cn%3A2486013011",
            "label": "Kindle Singles",
            "node": "2486013011",
        },
        "digital-text": {
            "url": "https://www.amazon.com/s?i=digital-text",
            "label": "Kindle Store",
        },
    },
    "fashion-luggage": {
        "fashion-luggage-backpacks": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A360832011",
            "label": "Backpacks",
            "node": "360832011",
        },
        "fashion-luggage-briefcases": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A2204831011",
            "label": "Briefcases",
            "node": "2204831011",
        },
        "fashion-luggage-gym-bags": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15743181",
            "label": "Gym Bags",
            "node": "15743181",
        },
        "fashion-luggage-laptop-bags": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A9971584011",
            "label": "Laptop Bags",
            "node": "9971584011",
        },
        "fashion-luggage-luggage": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15743251",
            "label": "Luggage",
            "node": "15743251",
        },
        "fashion-luggage-messenger-bags": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15743231",
            "label": "Messenger Bags",
            "node": "15743231",
        },
        "fashion-luggage-travel-accessories": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15743971",
            "label": "Travel Accessories",
            "node": "15743971",
        },
        "fashion-luggage-travel-duffels": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15743211",
            "label": "Travel Duffels",
            "node": "15743211",
        },
        "fashion-luggage-travel-totes": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15743241",
            "label": "Travel Totes",
            "node": "15743241",
        },
        "fashion-luggage-umbrellas": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A15744111",
            "label": "Umbrellas",
            "node": "15744111",
        },
        "fashion-luggage-waist-packs": {
            "url": "https://www.amazon.com/s?i=fashion-luggage&rh=n%3A9479199011%2Cn%3A2477385011",
            "label": "Waist Packs",
            "node": "2477385011",
        },
        "fashion-luggage": {
            "url": "https://www.amazon.com/s?i=fashion-luggage",
            "label": "Luggage & Travel Gear",
        },
    },
    "luxury": {
        "luxury": {
            "url": "https://www.amazon.com/s?i=luxury",
            "label": "Luxury Stores",
        },
    },
    "magazines": {
        "magazines-kindle-ebooks": {
            "url": "https://www.amazon.com/s?i=magazines&rh=n%3A115961083011%2Cn%3A154606011",
            "label": "Kindle eBooks",
            "node": "154606011",
        },
        "magazines": {
            "url": "https://www.amazon.com/s?i=magazines",
            "label": "Magazine Subscriptions",
        },
    },
    "movies-tv": {
        "movies-tv-movies": {
            "url": "https://www.amazon.com/s?i=movies-tv&rh=n%3A2625373011%2Cn%3A2649512011",
            "label": "Movies",
            "node": "2649512011",
        },
        "movies-tv-tv": {
            "url": "https://www.amazon.com/s?i=movies-tv&rh=n%3A2625373011%2Cn%3A2649513011",
            "label": "TV",
            "node": "2649513011",
        },
        "movies-tv": {
            "url": "https://www.amazon.com/s?i=movies-tv",
            "label": "Movies & TV",
        },
    },
    "mi": {
        "mi-guitars": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11971241",
            "label": "Guitars",
            "node": "11971241",
        },
        "mi-bass-guitars": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11971311",
            "label": "Bass Guitars",
            "node": "11971311",
        },
        "mi-ukuleles-mandolins-banjos": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A14733114011",
            "label": "Ukuleles, Mandolins & Banjos",
            "node": "14733114011",
        },
        "mi-amplifiers-effects": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A8882494011",
            "label": "Amplifiers & Effects",
            "node": "8882494011",
        },
        "mi-drums-percussion": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11970241",
            "label": "Drums & Percussion",
            "node": "11970241",
        },
        "mi-keyboards-midi": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11969981",
            "label": "Keyboards & MIDI",
            "node": "11969981",
        },
        "mi-microphones-accessories": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11974521",
            "label": "Microphones & Accessories",
            "node": "11974521",
        },
        "mi-band-orchestra": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A405758011",
            "label": "Band & Orchestra",
            "node": "405758011",
        },
        "mi-stringed-instruments": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A8882493011",
            "label": "Stringed Instruments",
            "node": "8882493011",
        },
        "mi-wind-woodwind-instruments": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A8882497011",
            "label": "Wind & Woodwind Instruments",
            "node": "8882497011",
        },
        "mi-instrument-accessories": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11965871",
            "label": "Instrument Accessories",
            "node": "11965871",
        },
        "mi-live-sound-stage": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A405757011",
            "label": "Live Sound & Stage",
            "node": "405757011",
        },
        "mi-studio-recording-equipment": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11973111",
            "label": "Studio Recording Equipment",
            "node": "11973111",
        },
        "mi-electronic-music-dj-karaoke": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A11973881",
            "label": "Electronic Music, DJ & Karaoke",
            "node": "11973881",
        },
        "mi-scores-songbooks-lyrics": {
            "url": "https://www.amazon.com/s?i=mi&rh=n%3A11091801%2Cn%3A1821",
            "label": "Scores, Songbooks & Lyrics",
            "node": "1821",
        },
        "mi": {
            "url": "https://www.amazon.com/s?i=mi",
            "label": "Musical Instruments",
        },
    },
    "office-products": {
        "office-products-office-school-supplies": {
            "url": "https://www.amazon.com/s?i=office-products&rh=n%3A1064954%2Cn%3A1069242",
            "label": "Office & School Supplies",
            "node": "1069242",
        },
        "office-products-office-electronics": {
            "url": "https://www.amazon.com/s?i=office-products&rh=n%3A1064954%2Cn%3A172574",
            "label": "Office Electronics",
            "node": "172574",
        },
        "office-products-office-furniture-lighting": {
            "url": "https://www.amazon.com/s?i=office-products&rh=n%3A1064954%2Cn%3A1069102",
            "label": "Office Furniture & Lighting",
            "node": "1069102",
        },
        "office-products": {
            "url": "https://www.amazon.com/s?i=office-products",
            "label": "Office Products",
        },
    },
    "pets": {
        "pets-dogs": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975312011",
            "label": "Dogs",
            "node": "2975312011",
        },
        "pets-cats": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975241011",
            "label": "Cats",
            "node": "2975241011",
        },
        "pets-fish-aquatic-pets": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975446011",
            "label": "Fish & Aquatic Pets",
            "node": "2975446011",
        },
        "pets-birds": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975221011",
            "label": "Birds",
            "node": "2975221011",
        },
        "pets-horses": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975481011",
            "label": "Horses",
            "node": "2975481011",
        },
        "pets-reptiles-amphibians": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975504011",
            "label": "Reptiles & Amphibians",
            "node": "2975504011",
        },
        "pets-small-animals": {
            "url": "https://www.amazon.com/s?i=pets&rh=n%3A2619533011%2Cn%3A2975520011",
            "label": "Small Animals",
            "node": "2975520011",
        },
        "pets": {
            "url": "https://www.amazon.com/s?i=pets",
            "label": "Pet Supplies",
        },
    },
    "luxury-beauty": {
        "luxury-beauty-premium-beauty-us": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A214874358011",
            "label": "Premium Beauty US",
            "node": "214874358011",
        },
        "luxury-beauty-new-arrivals": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A21488580011",
            "label": "New Arrivals",
            "node": "21488580011",
        },
        "luxury-beauty-premium-brands": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A21157564011",
            "label": "Premium Brands",
            "node": "21157564011",
        },
        "luxury-beauty-makeup": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951540011",
            "label": "Makeup",
            "node": "20951540011",
        },
        "luxury-beauty-skin-care": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951542011",
            "label": "Skin Care",
            "node": "20951542011",
        },
        "luxury-beauty-hair-care": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951539011",
            "label": "Hair Care",
            "node": "20951539011",
        },
        "luxury-beauty-fragrance": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951538011",
            "label": "Fragrance",
            "node": "20951538011",
        },
        "luxury-beauty-foot-hand-nail-care": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951537011",
            "label": "Foot, Hand & Nail Care",
            "node": "20951537011",
        },
        "luxury-beauty-tools-accessories": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951543011",
            "label": "Tools & Accessories",
            "node": "20951543011",
        },
        "luxury-beauty-shaving-hair-removal": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951541011",
            "label": "Shaving & Hair Removal",
            "node": "20951541011",
        },
        "luxury-beauty-bath-body": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A20951536011",
            "label": "Bath & Body",
            "node": "20951536011",
        },
        "luxury-beauty-men-s-grooming": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A21150993011",
            "label": "Men's Grooming",
            "node": "21150993011",
        },
        "luxury-beauty-internet-famous": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A23432474011",
            "label": "Internet Famous",
            "node": "23432474011",
        },
        "luxury-beauty-premium-beauty": {
            "url": "https://www.amazon.com/s?i=luxury-beauty&rh=n%3A20951535011%2Cn%3A23372343011",
            "label": "Premium Beauty",
            "node": "23372343011",
        },
        "luxury-beauty": {
            "url": "https://www.amazon.com/s?i=luxury-beauty",
            "label": "Premium Beauty",
        },
    },
    "instant-video": {
        "instant-video-movies": {
            "url": "https://www.amazon.com/s?i=instant-video&rh=n%3A2625373011%2Cn%3A2649512011",
            "label": "Movies",
            "node": "2649512011",
        },
        "instant-video-tv": {
            "url": "https://www.amazon.com/s?i=instant-video&rh=n%3A2625373011%2Cn%3A2649513011",
            "label": "TV",
            "node": "2649513011",
        },
        "instant-video": {
            "url": "https://www.amazon.com/s?i=instant-video",
            "label": "Prime Video",
        },
    },
    "smart-home": {
        "smart-home": {
            "url": "https://www.amazon.com/s?i=smart-home",
            "label": "Smart Home",
        },
    },
    "software": {
        "software-accounting-finance": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A5223260011",
            "label": "Accounting & Finance",
            "node": "5223260011",
        },
        "software-antivirus-security": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229677",
            "label": "Antivirus & Security",
            "node": "229677",
        },
        "software-business-office": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229535",
            "label": "Business & Office",
            "node": "229535",
        },
        "software-children-s": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229548",
            "label": "Children's",
            "node": "229548",
        },
        "software-education-reference": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229563",
            "label": "Education & Reference",
            "node": "229563",
        },
        "software-lifestyle-hobbies": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229624",
            "label": "Lifestyle & Hobbies",
            "node": "229624",
        },
        "software-music": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A497022",
            "label": "Music",
            "node": "497022",
        },
        "software-networking-servers": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229637",
            "label": "Networking & Servers",
            "node": "229637",
        },
        "software-operating-systems": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229653",
            "label": "Operating Systems",
            "node": "229653",
        },
        "software-photography-graphic-design": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229614",
            "label": "Photography & Graphic Design",
            "node": "229614",
        },
        "software-programming-web-development": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A5223262011",
            "label": "Programming & Web Development",
            "node": "5223262011",
        },
        "software-tax-preparation": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229545",
            "label": "Tax Preparation",
            "node": "229545",
        },
        "software-utilities": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A229672",
            "label": "Utilities",
            "node": "229672",
        },
        "software-video": {
            "url": "https://www.amazon.com/s?i=software&rh=n%3A229534%2Cn%3A290542",
            "label": "Video",
            "node": "290542",
        },
        "software": {
            "url": "https://www.amazon.com/s?i=software",
            "label": "Software",
        },
    },
    "sporting": {
        "sporting-outdoor-recreation": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A706814011",
            "label": "Outdoor Recreation",
            "node": "706814011",
        },
        "sporting-fan-shop": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A3386071",
            "label": "Fan Shop",
            "node": "3386071",
        },
        "sporting-clothing": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A23466320011",
            "label": "Clothing",
            "node": "23466320011",
        },
        "sporting-exercise-fitness": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A3407731",
            "label": "Exercise & Fitness",
            "node": "3407731",
        },
        "sporting-hunting-fishing": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A706813011",
            "label": "Hunting & Fishing",
            "node": "706813011",
        },
        "sporting-memorabilia-display-storage": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A2358921011",
            "label": "Memorabilia Display & Storage",
            "node": "2358921011",
        },
        "sporting-sports": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A10971181011",
            "label": "Sports",
            "node": "10971181011",
        },
        "sporting-sports-outdoor-recreation-accessories": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A3394801",
            "label": "Sports & Outdoor Recreation Accessories",
            "node": "3394801",
        },
        "sporting-sports-medicine": {
            "url": "https://www.amazon.com/s?i=sporting&rh=n%3A3375251%2Cn%3A3422351",
            "label": "Sports Medicine",
            "node": "3422351",
        },
        "sporting": {
            "url": "https://www.amazon.com/s?i=sporting",
            "label": "Sports & Outdoors",
        },
    },
    "specialty-aps-sns": {
        "specialty-aps-sns-arts-crafts-sewing": {
            "url": "https://www.amazon.com/s?i=specialty-aps-sns&rh=n%3A5856181011%2Cn%3A2617941011",
            "label": "Arts, Crafts & Sewing",
            "node": "2617941011",
        },
        "specialty-aps-sns-everything-else": {
            "url": "https://www.amazon.com/s?i=specialty-aps-sns&rh=n%3A5856181011%2Cn%3A10272111",
            "label": "Everything Else",
            "node": "10272111",
        },
        "specialty-aps-sns-grocery-gourmet-food": {
            "url": "https://www.amazon.com/s?i=specialty-aps-sns&rh=n%3A5856181011%2Cn%3A16310101",
            "label": "Grocery & Gourmet Food",
            "node": "16310101",
        },
        "specialty-aps-sns-handmade-products": {
            "url": "https://www.amazon.com/s?i=specialty-aps-sns&rh=n%3A5856181011%2Cn%3A11260432011",
            "label": "Handmade Products",
            "node": "11260432011",
        },
        "specialty-aps-sns": {
            "url": "https://www.amazon.com/s?i=specialty-aps-sns",
            "label": "Subscribe & Save",
        },
    },
    "subscribe-with-amazon": {
        "subscribe-with-amazon": {
            "url": "https://www.amazon.com/s?i=subscribe-with-amazon",
            "label": "Subscription Boxes",
        },
    },
    "tools": {
        "tools-appliances": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A13397451",
            "label": "Appliances",
            "node": "13397451",
        },
        "tools-building-supplies": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A551240",
            "label": "Building Supplies",
            "node": "551240",
        },
        "tools-electrical": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A495266",
            "label": "Electrical",
            "node": "495266",
        },
        "tools-hardware": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A511228",
            "label": "Hardware",
            "node": "511228",
        },
        "tools-kitchen-bath-fixtures": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A3754161",
            "label": "Kitchen & Bath Fixtures",
            "node": "3754161",
        },
        "tools-light-bulbs": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A322525011",
            "label": "Light Bulbs",
            "node": "322525011",
        },
        "tools-lighting-ceiling-fans": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A495224",
            "label": "Lighting & Ceiling Fans",
            "node": "495224",
        },
        "tools-measuring-layout-tools": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A553244",
            "label": "Measuring & Layout Tools",
            "node": "553244",
        },
        "tools-paint-wall-treatments-supplies": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A228899",
            "label": "Paint, Wall Treatments & Supplies",
            "node": "228899",
        },
        "tools-plumbing": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A13749581",
            "label": "Plumbing",
            "node": "13749581",
        },
        "tools-power-hand-tools": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A328182011",
            "label": "Power & Hand Tools",
            "node": "328182011",
        },
        "tools-safety-security": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A3180231",
            "label": "Safety & Security",
            "node": "3180231",
        },
        "tools-storage-home-organization": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A13400631",
            "label": "Storage & Home Organization",
            "node": "13400631",
        },
        "tools-welding-soldering": {
            "url": "https://www.amazon.com/s?i=tools&rh=n%3A228013%2Cn%3A8106310011",
            "label": "Welding & Soldering",
            "node": "8106310011",
        },
        "tools": {
            "url": "https://www.amazon.com/s?i=tools",
            "label": "Tools & Home Improvement",
        },
    },
    "toys-and-games": {
        "toys-and-games-arts-crafts": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166057011",
            "label": "Arts & Crafts",
            "node": "166057011",
        },
        "toys-and-games-baby-toddler-toys": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A196601011",
            "label": "Baby & Toddler Toys",
            "node": "196601011",
        },
        "toys-and-games-building-toys": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166092011",
            "label": "Building Toys",
            "node": "166092011",
        },
        "toys-and-games-collectible-toys": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A19431275011",
            "label": "Collectible Toys",
            "node": "19431275011",
        },
        "toys-and-games-dolls-accessories": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166118011",
            "label": "Dolls & Accessories",
            "node": "166118011",
        },
        "toys-and-games-dress-up-pretend-play": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166316011",
            "label": "Dress Up & Pretend Play",
            "node": "166316011",
        },
        "toys-and-games-games-accessories": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166220011",
            "label": "Games & Accessories",
            "node": "166220011",
        },
        "toys-and-games-kids-electronics": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166164011",
            "label": "Kids' Electronics",
            "node": "166164011",
        },
        "toys-and-games-learning-education": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166269011",
            "label": "Learning & Education",
            "node": "166269011",
        },
        "toys-and-games-novelty-gag-toys": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166027011",
            "label": "Novelty & Gag Toys",
            "node": "166027011",
        },
        "toys-and-games-party-supplies": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A1266203011",
            "label": "Party Supplies",
            "node": "1266203011",
        },
        "toys-and-games-puppets-puppet-theaters": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166333011",
            "label": "Puppets & Puppet Theaters",
            "node": "166333011",
        },
        "toys-and-games-puzzles": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166359011",
            "label": "Puzzles",
            "node": "166359011",
        },
        "toys-and-games-remote-app-controlled-vehicles-parts": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A6925830011",
            "label": "Remote & App Controlled Vehicles & Parts",
            "node": "6925830011",
        },
        "toys-and-games-sports-outdoor-play": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166420011",
            "label": "Sports & Outdoor Play",
            "node": "166420011",
        },
        "toys-and-games-stuffed-animals-plush-toys": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A166461011",
            "label": "Stuffed Animals & Plush Toys",
            "node": "166461011",
        },
        "toys-and-games-toy-figures-playsets": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A165993011",
            "label": "Toy Figures & Playsets",
            "node": "165993011",
        },
        "toys-and-games-tricycles-scooters-wagons": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A256994011",
            "label": "Tricycles, Scooters & Wagons",
            "node": "256994011",
        },
        "toys-and-games-vehicles": {
            "url": "https://www.amazon.com/s?i=toys-and-games&rh=n%3A165793011%2Cn%3A23539911011",
            "label": "Vehicles",
            "node": "23539911011",
        },
        "toys-and-games": {
            "url": "https://www.amazon.com/s?i=toys-and-games",
            "label": "Toys & Games",
        },
    },
    "under-ten-dollars": {
        "under-ten-dollars-arts-crafts-sewing": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars&rh=n%3ANone%2Cn%3A2617941011",
            "label": "Arts, Crafts & Sewing",
            "node": "2617941011",
        },
        "under-ten-dollars-everything-else": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars&rh=n%3ANone%2Cn%3A10272111",
            "label": "Everything Else",
            "node": "10272111",
        },
        "under-ten-dollars-grocery-gourmet-food": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars&rh=n%3ANone%2Cn%3A16310101",
            "label": "Grocery & Gourmet Food",
            "node": "16310101",
        },
        "under-ten-dollars-handmade-products": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars&rh=n%3ANone%2Cn%3A11260432011",
            "label": "Handmade Products",
            "node": "11260432011",
        },
        "under-ten-dollars-magazine-subscriptions": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars&rh=n%3ANone%2Cn%3A599858",
            "label": "Magazine Subscriptions",
            "node": "599858",
        },
        "under-ten-dollars": {
            "url": "https://www.amazon.com/s?i=under-ten-dollars",
            "label": "Under $10",
        },
    },
    "videogames": {
        "videogames-playstation-5": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A20972781011",
            "label": "PlayStation 5",
            "node": "20972781011",
        },
        "videogames-playstation-4": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A6427814011",
            "label": "PlayStation 4",
            "node": "6427814011",
        },
        "videogames-xbox-series-x-s": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A20972798011",
            "label": "Xbox Series X & S",
            "node": "20972798011",
        },
        "videogames-xbox-one": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A6469269011",
            "label": "Xbox One",
            "node": "6469269011",
        },
        "videogames-nintendo-switch-2": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A206234609011",
            "label": "Nintendo Switch 2",
            "node": "206234609011",
        },
        "videogames-nintendo-switch": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A16227128011",
            "label": "Nintendo Switch",
            "node": "16227128011",
        },
        "videogames-pc": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A229575",
            "label": "PC",
            "node": "229575",
        },
        "videogames-mac": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A229647",
            "label": "Mac",
            "node": "229647",
        },
        "videogames-legacy-systems": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A294940",
            "label": "Legacy Systems",
            "node": "294940",
        },
        "videogames-online-game-services": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A17596052011",
            "label": "Online Game Services",
            "node": "17596052011",
        },
        "videogames-handheld-game-systems": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A120387867011",
            "label": "Handheld Game Systems",
            "node": "120387867011",
        },
        "videogames-virtual-reality": {
            "url": "https://www.amazon.com/s?i=videogames&rh=n%3A468642%2Cn%3A21479453011",
            "label": "Virtual Reality",
            "node": "21479453011",
        },
        "videogames": {
            "url": "https://www.amazon.com/s?i=videogames",
            "label": "Video Games",
        },
    },
    "wholefoods": {
        "wholefoods-arts-crafts-sewing": {
            "url": "https://www.amazon.com/s?i=wholefoods&rh=n%3A18473610011%2Cn%3A2617941011",
            "label": "Arts, Crafts & Sewing",
            "node": "2617941011",
        },
        "wholefoods-everything-else": {
            "url": "https://www.amazon.com/s?i=wholefoods&rh=n%3A18473610011%2Cn%3A10272111",
            "label": "Everything Else",
            "node": "10272111",
        },
        "wholefoods-grocery-gourmet-food": {
            "url": "https://www.amazon.com/s?i=wholefoods&rh=n%3A18473610011%2Cn%3A16310101",
            "label": "Grocery & Gourmet Food",
            "node": "16310101",
        },
        "wholefoods": {
            "url": "https://www.amazon.com/s?i=wholefoods",
            "label": "Whole Foods Market",
        },
    },
}
