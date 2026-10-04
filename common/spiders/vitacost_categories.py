from __future__ import annotations

"""Vitacost (vitacost.com) category inventory.
Extracted from the desktop `Categories` mega-menu (`.mega-menu__sidebar-item`) on
2026-10-04 and flattened into the repository listing-spider schema:

    [
        {"category": "Supplements", "url": ".../collections/supplements",
         "department": "Supplements", "subcategory": None},
        {"category": "Supplements > Vitamins", "url": ".../collections/vitamins",
         "department": "Supplements", "subcategory": "Vitamins"},
    ]

Duplicate leaf labels exist across departments (`Sunscreen` under both *Bath & Personal
Care* and *Beauty*, `Essential Oils & Aromatherapy` under both *Bath & Personal Care* and
*Home*), so `category` is qualified with the parent department. The `handle` is the
Shopify collection handle that keys the Boost `collection_scope` lookup.
"""

BASE_URL = "https://www.vitacost.com"
COLLECTION_URL = BASE_URL + "/collections/{handle}"
SHOP_DOMAIN = "icost.myshopify.com"
FILTER_API_URL = "https://services.mybcapps.com/bc-sf-filter/filter"


def build_vitacost_categories(tree: dict) -> list[dict]:
    """Flatten the mega-menu tree into listing-spider category entries."""
    entries: list[dict] = []
    for department, node in tree.items():
        handle = node["url"].rsplit("/", 1)[-1]
        entries.append({
            "category": department,
            "url": node["url"],
            "department": department,
            "subcategory": None,
            "handle": handle,
        })
        for label, url in node.get("subcategories", {}).items():
            entries.append({
                "category": f"{department} > {label}",
                "url": url,
                "department": department,
                "subcategory": label,
                "handle": url.rsplit("/", 1)[-1],
            })
    return entries


VITACOST_MENU = {
    "Supplements": {
        "url": "https://www.vitacost.com/collections/supplements",
        "subcategories": {
            "Omegas & Fish Oils (EPA DHA)": "https://www.vitacost.com/collections/omegas-fish-oils-epa-dha",
            "Vitamins": "https://www.vitacost.com/collections/vitamins",
            "Bone, Joint & Cartilage": "https://www.vitacost.com/collections/bone-joint-cartilage",
            "Minerals": "https://www.vitacost.com/collections/minerals",
            "Gut Health": "https://www.vitacost.com/collections/gut-health",
            "Herbs": "https://www.vitacost.com/collections/herbs",
            "Hair, Skin & Nails": "https://www.vitacost.com/collections/hair-skin-nails",
            "Phospholipids": "https://www.vitacost.com/collections/phospholipids",
            "Greens & Superfoods": "https://www.vitacost.com/collections/greens-superfoods",
            "Antioxidants": "https://www.vitacost.com/collections/antioxidants",
            "Sleep": "https://www.vitacost.com/collections/sleep",
            "Women's Health": "https://www.vitacost.com/collections/womens-health",
            "Men's Health": "https://www.vitacost.com/collections/mens-health",
            "Weight Management": "https://www.vitacost.com/collections/weight-management",
            "Amino Acids": "https://www.vitacost.com/collections/amino-acids",
            "Brain & Cognitive": "https://www.vitacost.com/collections/brain-cognitive",
            "Eye, Ear & Nose": "https://www.vitacost.com/collections/eye-ear-nose",
            "Detox & Cleanse Formulas": "https://www.vitacost.com/collections/detox-cleanse-formulas",
            "Bee Products": "https://www.vitacost.com/collections/bee-products",
            "Organ Meats": "https://www.vitacost.com/collections/organ-meats",
            "Mushrooms": "https://www.vitacost.com/collections/mushrooms"
        },
    },
    "Sports": {
        "url": "https://www.vitacost.com/collections/sports",
        "subcategories": {
            "Sports Supplements": "https://www.vitacost.com/collections/sports-supplements",
            "Creatine": "https://www.vitacost.com/collections/creatine",
            "Electrolytes & Hydration": "https://www.vitacost.com/collections/electrolytes-hydration",
            "Exercise & Fitness Accessories": "https://www.vitacost.com/collections/exercise-fitness-accessories",
            "Muscle Builders": "https://www.vitacost.com/collections/muscle-builders",
            "Muscle Recovery Supplements": "https://www.vitacost.com/collections/muscle-recovery-supplements",
            "Nitric Oxide Supplements": "https://www.vitacost.com/collections/nitric-oxide-supplements",
            "Pre-Workout Supplements": "https://www.vitacost.com/collections/pre-workout-supplements",
            "Protein": "https://www.vitacost.com/collections/protein",
            "Sports Bars & Snacks": "https://www.vitacost.com/collections/sports-bars-snacks"
        },
    },
    "Bath & Personal Care": {
        "url": "https://www.vitacost.com/collections/bath",
        "subcategories": {
            "Bath & Shower": "https://www.vitacost.com/collections/bath-shower",
            "Body Care": "https://www.vitacost.com/collections/body-care",
            "Essential Oils & Aromatherapy": "https://www.vitacost.com/collections/essential-oils-aromatherapy",
            "Eye Care": "https://www.vitacost.com/collections/eye-care",
            "Hair Care": "https://www.vitacost.com/collections/hair-care",
            "Lip Care": "https://www.vitacost.com/collections/lip-care",
            "Medicine Cabinet": "https://www.vitacost.com/collections/medicine-cabinet",
            "Men's Grooming": "https://www.vitacost.com/collections/mens-grooming",
            "Personal Care": "https://www.vitacost.com/collections/personal-care",
            "Sunscreen": "https://www.vitacost.com/collections/sunscreen"
        },
    },
    "Beauty": {
        "url": "https://www.vitacost.com/collections/beauty",
        "subcategories": {
            "Cleansers": "https://www.vitacost.com/collections/cleansers",
            "Face Moisturizers & Creams": "https://www.vitacost.com/collections/face-moisturizers-creams",
            "K-Beauty": "https://www.vitacost.com/collections/k-beauty",
            "Beauty by Ingredient": "https://www.vitacost.com/collections/beauty-by-ingredient",
            "Makeup": "https://www.vitacost.com/collections/makeup",
            "Makeup & Skin Care Gifts": "https://www.vitacost.com/collections/makeup-skin-care-gifts",
            "Makeup Brushes & Accessories": "https://www.vitacost.com/collections/makeup-brushes-accessories",
            "Sunscreen": "https://www.vitacost.com/collections/sunscreen",
            "Treatments & Serums": "https://www.vitacost.com/collections/treatments-serums"
        },
    },
    "Grocery": {
        "url": "https://www.vitacost.com/collections/grocery",
        "subcategories": {
            "Baking, Flour & Mixes": "https://www.vitacost.com/collections/baking-flour-mixes",
            "Bars": "https://www.vitacost.com/collections/bars",
            "Cereals & Breakfast Foods": "https://www.vitacost.com/collections/cereals-breakfast-foods",
            "Chocolate & Candy": "https://www.vitacost.com/collections/chocolate-candy",
            "Condiments, Sauces & Spreads": "https://www.vitacost.com/collections/condiments-sauces-spreads",
            "Herbs & Spices": "https://www.vitacost.com/collections/herbs-spices",
            "Honey & Sweeteners": "https://www.vitacost.com/collections/honey-sweeteners",
            "Oils & Vinegar": "https://www.vitacost.com/collections/oils-vinegar",
            "Packaged & Prepared Foods": "https://www.vitacost.com/collections/packaged-prepared-foods",
            "Snacks": "https://www.vitacost.com/collections/snacks",
            "Tea & Beverages": "https://www.vitacost.com/collections/tea-beverages"
        },
    },
    "Home": {
        "url": "https://www.vitacost.com/collections/home",
        "subcategories": {
            "Cleaning": "https://www.vitacost.com/collections/cleaning",
            "Drinkware": "https://www.vitacost.com/collections/drinkware",
            "Essential Oils & Aromatherapy": "https://www.vitacost.com/collections/essential-oils-aromatherapy",
            "Home Accessories": "https://www.vitacost.com/collections/home-accessories",
            "Home Fragrance": "https://www.vitacost.com/collections/home-fragrance",
            "Kitchen Supplies": "https://www.vitacost.com/collections/kitchen-supplies"
        },
    },
    "Baby & Kids": {
        "url": "https://www.vitacost.com/collections/baby",
        "subcategories": {
            "Children's Health": "https://www.vitacost.com/collections/childrens-health",
            "Teething & Oral Care": "https://www.vitacost.com/collections/teething-oral-care",
            "Moms & Maternity": "https://www.vitacost.com/collections/moms-maternity",
            "Baby & Kids Feeding": "https://www.vitacost.com/collections/baby-kids-feeding",
            "Baby & Kids Safety": "https://www.vitacost.com/collections/baby-kids-safety",
            "Baby & Kids Bath, Skin & Hair": "https://www.vitacost.com/collections/baby-kids-bath-skin-hair",
            "Baby & Kids Toys": "https://www.vitacost.com/collections/baby-kids-toys",
            "Diapering": "https://www.vitacost.com/collections/diapering",
            "Baby & Kids Home": "https://www.vitacost.com/collections/baby-kids-home",
            "Pacifiers & Clips": "https://www.vitacost.com/collections/pacifiers-clips",
            "Gifts for New Parents": "https://www.vitacost.com/collections/gifts-for-new-parents"
        },
    },
    "Pets": {
        "url": "https://www.vitacost.com/collections/pets",
        "subcategories": {
            "Pet Food & Treats": "https://www.vitacost.com/collections/pet-food-treats",
            "Pet Grooming": "https://www.vitacost.com/collections/pet-grooming",
            "Pet Health": "https://www.vitacost.com/collections/pet-health",
            "Pet Supplements": "https://www.vitacost.com/collections/pet-supplements",
            "Pet Supplies": "https://www.vitacost.com/collections/pet-supplies",
            "Pet Toys": "https://www.vitacost.com/collections/pet-toys"
        },
    },
}

VITACOST_CATEGORIES = build_vitacost_categories(VITACOST_MENU)
