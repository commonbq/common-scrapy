"""iHerb (iherb.com) mega-menu category inventory.

Captured 2026-10-04 from the server-rendered homepage mega-menu on
`https://www.iherb.com/` (issue #226). Tracking query strings and
logo-only brand pills were dropped; the `Shop all ...` department landing
pages are kept because they are valid PLPs.

The inventory is only the *crawl key*: no listing document is ever fetched
from these HTML URLs. `iherb_listing` resolves every entry to its storefront
`urlName` (the path segment(s) after `/c/`) and POSTs to the first-party
catalog API (`catalog.app.iherb.com/category/{urlName}/products`) -- the same
service the storefront PLP calls for its own filter/pagination XHRs.
"""

from __future__ import annotations

import re

IHERB_CATEGORY_INVENTORY = {
    "Supplements": {
        "url": "https://www.iherb.com/c/supplements",
        "subcategories": {
            "Amino Acids": "https://www.iherb.com/c/amino-acids",
            "Amino Acid Blends": "https://www.iherb.com/c/amino-acids-blends",
            "Glycine": "https://www.iherb.com/c/glycine",
            "L-Arginine": "https://www.iherb.com/c/l-arginine",
            "L-Theanine": "https://www.iherb.com/c/l-theanine",
            "Antioxidants": "https://www.iherb.com/c/antioxidants",
            "Alpha Lipoic Acid": "https://www.iherb.com/c/alpha-lipoic-acid",
            "Astaxanthin": "https://www.iherb.com/c/astaxanthin",
            "CoQ10": "https://www.iherb.com/c/coenzyme-q10-coq10",
            "Glutathione": "https://www.iherb.com/c/l-glutathione",
            "Lutein & Zeaxanthin": "https://www.iherb.com/c/lutein",
            "NAC": "https://www.iherb.com/c/n-acetyl-cysteine-nac",
            "Resveratrol": "https://www.iherb.com/c/resveratrol",
            "Turmeric & Curcumin": "https://www.iherb.com/c/turmeric-curcumin",
            "Bee Products": "https://www.iherb.com/c/bee-products",
            "Bone, Joint & Cartilage": "https://www.iherb.com/c/bone-joint-cartilage",
            "Collagen Supplements": "https://www.iherb.com/c/collagen-supplements",
            "Glucosamine": "https://www.iherb.com/c/glucosamine-chondroitin-formulas",
            "Brain & Cognitive": "https://www.iherb.com/c/brain-cognitive",
            "Creatine": "https://www.iherb.com/c/creatine",
            "NAD+": "https://www.iherb.com/c/nad-nicotinamide-adenine-dinucleotide-",
            "NMN": "https://www.iherb.com/c/nmn-nicotinamide-mononucleotide",
            "Detox & Cleanse": "https://www.iherb.com/c/detox-cleanse",
            "Fish Oils & Omegas": "https://www.iherb.com/c/fish-oil-omegas-epa-dha",
            "Krill Oil": "https://www.iherb.com/c/krill-oil",
            "Omega-3 Fish Oil": "https://www.iherb.com/c/omega-3-fish-oil",
            "Greens & Superfoods": "https://www.iherb.com/c/greens-superfoods",
            "Chlorophyll": "https://www.iherb.com/c/chlorophyll",
            "Gut Health": "https://www.iherb.com/c/gut-health",
            "Digestive Enzymes": "https://www.iherb.com/c/digestive-enzymes",
            "Fiber": "https://www.iherb.com/c/fiber",
            "Intestinal Formulas": "https://www.iherb.com/c/intestinal-formulas",
            "Probiotics": "https://www.iherb.com/c/probiotics",
            "Hair, Skin & Nails": "https://www.iherb.com/c/hair-skin-nails",
            "Hyaluronic Acid": "https://www.iherb.com/c/hyaluronic-acid",
            "Herbs": "https://www.iherb.com/c/herbs",
            "Adaptogens": "https://www.iherb.com/c/adaptogens",
            "Ashwagandha": "https://www.iherb.com/c/ashwagandha",
            "Berberine": "https://www.iherb.com/c/berberine-barberry",
            "Elderberry": "https://www.iherb.com/c/elderberry-sambucus",
            "Herbal Formulas": "https://www.iherb.com/c/herbal-formulas",
            "Maca": "https://www.iherb.com/c/maca",
            "Milk Thistle": "https://www.iherb.com/c/milk-thistle-silymarin",
            "Men's Health": "https://www.iherb.com/c/mens-health",
            "Minerals": "https://www.iherb.com/c/minerals",
            "Calcium": "https://www.iherb.com/c/calcium",
            "Iron": "https://www.iherb.com/c/iron",
            "Lithium": "https://www.iherb.com/c/lithium",
            "Magnesium": "https://www.iherb.com/c/magnesium",
            "Sea Moss": "https://www.iherb.com/c/sea-moss",
            "Zinc": "https://www.iherb.com/c/zinc",
            "Mushrooms": "https://www.iherb.com/c/mushrooms",
            "Lions Mane": "https://www.iherb.com/c/lions-mane",
            "Reishi": "https://www.iherb.com/c/reishi",
            "Organ Meats": "https://www.iherb.com/c/organ-meats",
            "Phospholipids": "https://www.iherb.com/c/phospholipids",
            "Sleep": "https://www.iherb.com/c/sleep",
            "Vitamins": "https://www.iherb.com/c/vitamins",
            "Multivitamins": "https://www.iherb.com/c/multivitamins",
            "Vitamin B": "https://www.iherb.com/c/vitamin-b",
            "Vitamin C": "https://www.iherb.com/c/vitamin-c",
            "Vitamin D": "https://www.iherb.com/c/vitamin-d",
            "Vitamin E": "https://www.iherb.com/c/vitamin-e",
            "Vitamin K": "https://www.iherb.com/c/vitamin-k",
            "Weight Management": "https://www.iherb.com/c/weight-management",
            "Women's Health": "https://www.iherb.com/c/womens-health",
            "Shop Professional Brands": "https://www.iherb.com/c/professional-brands",
            "Shop all Supplements": "https://www.iherb.com/c/supplements"
        }
    },
    "Sports": {
        "url": "https://www.iherb.com/c/sports",
        "subcategories": {
            "Amino Acids": "https://www.iherb.com/c/amino-acids",
            "BCAAs": "https://www.iherb.com/c/bcaa",
            "Essential Amino Acids (EAA)": "https://www.iherb.com/c/essential-amino-acids-eaa",
            "L-Carnitine": "https://www.iherb.com/c/l-carnitine",
            "L-Glutamine": "https://www.iherb.com/c/l-glutamine",
            "L-Taurine": "https://www.iherb.com/c/l-taurine",
            "Creatine": "https://www.iherb.com/c/creatine",
            "Buffered Creatine": "https://www.iherb.com/c/buffered-creatine",
            "Creatine Monohydrate": "https://www.iherb.com/c/creatine-monohydrate",
            "Creatine HCl": "https://www.iherb.com/c/creatine-hcl",
            "Electrolytes & Hydration": "https://www.iherb.com/c/electrolytes-hydration",
            "Fitness Accessories": "https://www.iherb.com/c/exercise-fitness-accessories",
            "Shaker Cups": "https://www.iherb.com/c/shaker-cups",
            "Water Bottles": "https://www.iherb.com/c/water-bottles",
            "Trimmers & Belts": "https://www.iherb.com/c/trimmers-belts",
            "Muscle Recovery": "https://www.iherb.com/c/muscle-recovery-supplements",
            "Carbohydrate Powders": "https://www.iherb.com/c/carbohydrate-powders",
            "HMB": "https://www.iherb.com/c/hmb",
            "Zinc Magnesium Aspartate": "https://www.iherb.com/c/zinc-magnesium-aspartate",
            "Nitric Oxide Supplements": "https://www.iherb.com/c/nitric-oxide-supplements",
            "Beets": "https://www.iherb.com/c/beet",
            "Citrulline Malate": "https://www.iherb.com/c/citrulline-malate",
            "L-Arginine": "https://www.iherb.com/c/l-arginine",
            "L-Arginine L-Citrulline Complex": "https://www.iherb.com/c/l-arginine-l-citrulline-complex",
            "L-Citrulline": "https://www.iherb.com/c/l-citrulline",
            "Pre-Workout Supplements": "https://www.iherb.com/c/pre-workout-supplements",
            "Caffeine": "https://www.iherb.com/c/caffeine",
            "Non-Stim Pre-Workout": "https://www.iherb.com/c/non-stim-pre-workout",
            "Stimulant Pre-Workout": "https://www.iherb.com/c/stimulant-pre-workout",
            "Protein": "https://www.iherb.com/c/protein",
            "Casein Protein": "https://www.iherb.com/c/casein-protein",
            "Mass Gainers": "https://www.iherb.com/c/mass-gainers",
            "Meal Replacements": "https://www.iherb.com/c/meal-replacements",
            "Plant Based Protein": "https://www.iherb.com/c/plant-based-protein",
            "Ready-to-Drink Protein": "https://www.iherb.com/c/ready-to-drink-protein",
            "Whey Protein": "https://www.iherb.com/c/whey-protein",
            "Sports Bars & Snacks": "https://www.iherb.com/c/sports-bars-snacks",
            "Protein Bars": "https://www.iherb.com/c/protein-bars",
            "Protein Snacks": "https://www.iherb.com/c/protein-snacks",
            "Sports Supplements": "https://www.iherb.com/c/sports-supplements",
            "Fat Burners": "https://www.iherb.com/c/fat-burners",
            "Sports Fish Oil & Omegas": "https://www.iherb.com/c/sports-fish-oil-omegas",
            "Sports Multivitamins": "https://www.iherb.com/c/sports-multivitamins",
            "Sport Certified": "https://www.iherb.com/c/sportcertified/store",
            "Shop all Sports": "https://www.iherb.com/c/sports"
        }
    },
    "Bath": {
        "url": "https://www.iherb.com/c/bath-personal-care",
        "subcategories": {
            "Bath & Shower": "https://www.iherb.com/c/bath-shower",
            "Bar Soap": "https://www.iherb.com/c/bar-soap",
            "Bath Soaks": "https://www.iherb.com/c/bath-soaks",
            "Body Scrubs": "https://www.iherb.com/c/body-scrubs",
            "Body Wash & Shower Gel": "https://www.iherb.com/c/body-wash-shower-gel",
            "Body Care": "https://www.iherb.com/c/body-care",
            "Body & Massage Oils": "https://www.iherb.com/c/body-massage-oil",
            "Hand Cream": "https://www.iherb.com/c/hand-cream",
            "Lotion": "https://www.iherb.com/c/lotion",
            "Self-Tanner": "https://www.iherb.com/c/self-tanner",
            "Skin Treatment": "https://www.iherb.com/c/skin-treatment",
            "Essential Oils": "https://www.iherb.com/c/essential-oils-aromatherapy",
            "Essential Oil Blends": "https://www.iherb.com/c/essential-oil-blends",
            "Essential Oil Diffusers": "https://www.iherb.com/c/essential-oil-diffusers",
            "Essential Oil Sets": "https://www.iherb.com/c/essential-oil-sets",
            "Essential Oil Spray": "https://www.iherb.com/c/essential-oil-spray",
            "Single Essential Oils": "https://www.iherb.com/c/single-essential-oils",
            "Eye Care": "https://www.iherb.com/c/eye-care",
            "Eye Drops": "https://www.iherb.com/c/eye-drops",
            "Foot Care": "https://www.iherb.com/c/foot-care",
            "Foot Cream & Treatments": "https://www.iherb.com/c/foot-cream-treatments",
            "Hair Care": "https://www.iherb.com/c/hair-care",
            "Conditioner": "https://www.iherb.com/c/hair-conditioners",
            "Detangler": "https://www.iherb.com/c/detangler",
            "Hair Accessories": "https://www.iherb.com/c/hair-accessories",
            "Hair Color": "https://www.iherb.com/c/hair-color",
            "Hair Styling": "https://www.iherb.com/c/hair-styling",
            "Hair Treatments": "https://www.iherb.com/c/hair-treatments",
            "K-Beauty Hair Care": "https://www.iherb.com/c/k-beauty-hair-care",
            "Shampoo": "https://www.iherb.com/c/shampoo",
            "Lip Care": "https://www.iherb.com/c/lip-care",
            "Lip Balm": "https://www.iherb.com/c/lip-balm",
            "Medicine Cabinet": "https://www.iherb.com/c/medicine-cabinet",
            "Allergy, Sinus & Nasal Care": "https://www.iherb.com/c/allergy-sinus-nasal-care",
            "First Aid": "https://www.iherb.com/c/first-aid",
            "Homeopathy": "https://www.iherb.com/c/homeopathy",
            "Sore Throat & Cough Lozenges": "https://www.iherb.com/c/sore-throat-cough-lozenges",
            "Men's Grooming": "https://www.iherb.com/c/mens-grooming",
            "Oral Care": "https://www.iherb.com/c/oral-care",
            "Teeth Whitening Strips": "https://www.iherb.com/c/teeth-whitening-strips",
            "Toothpaste": "https://www.iherb.com/c/toothpaste",
            "Mouthwash, Rinse & Spray": "https://www.iherb.com/c/mouthwash-rinse-spray",
            "Personal Care": "https://www.iherb.com/c/personal-care",
            "Deodorant": "https://www.iherb.com/c/deodorant",
            "Feminine Hygiene": "https://www.iherb.com/c/feminine-hygiene",
            "Shaving & Hair Removal": "https://www.iherb.com/c/shaving-hair-removal",
            "Sunscreen": "https://www.iherb.com/c/sunscreen",
            "Baby & Kids Sunscreen": "https://www.iherb.com/c/baby-kids-sunscreen",
            "Face Sunscreen": "https://www.iherb.com/c/face-sunscreen",
            "K-Beauty Sunscreen": "https://www.iherb.com/c/k-beauty-sunscreen",
            "Shop all Bath": "https://www.iherb.com/c/bath-personal-care"
        }
    },
    "Beauty": {
        "url": "https://www.iherb.com/c/beauty",
        "subcategories": {
            "Beauty by Ingredient": "https://www.iherb.com/c/beauty-by-ingredient",
            "Centella": "https://www.iherb.com/c/centella-skin-care",
            "Ceramides": "https://www.iherb.com/c/ceramides",
            "Coconut": "https://www.iherb.com/c/coconut-skin-care",
            "Collagen": "https://www.iherb.com/c/collagen-skin-care",
            "Glycolic Acid": "https://www.iherb.com/c/glycolic-acid-skin-care",
            "Hyaluronic Acid": "https://www.iherb.com/c/hyaluronic-acid-skin-care",
            "Niacinamide": "https://www.iherb.com/c/niacinamide-skin-care",
            "Retinol": "https://www.iherb.com/c/retinol-skin-care",
            "Rice": "https://www.iherb.com/c/rice-skin-care",
            "Salicylic Acid": "https://www.iherb.com/c/salicylic-acid-skin-care",
            "Vitamin C": "https://www.iherb.com/c/vitamin-c-skin-care",
            "Beauty Face Masks": "https://www.iherb.com/c/beauty-face-masks-peels",
            "Eye Masks": "https://www.iherb.com/c/eye-masks",
            "Lip Masks": "https://www.iherb.com/c/lip-mask",
            "Pimple Patches": "https://www.iherb.com/c/pimple-patches",
            "Sheet Masks": "https://www.iherb.com/c/sheet-masks1",
            "Wash-off Face Masks": "https://www.iherb.com/c/wash-off-face-masks",
            "Cleansers": "https://www.iherb.com/c/cleansers",
            "Face Scrubs & Exfoliators": "https://www.iherb.com/c/face-scrubs-exfoliators",
            "Face Washes": "https://www.iherb.com/c/face-washes",
            "Face Wipes & Towelettes": "https://www.iherb.com/c/face-wipes-towelettes",
            "Toners": "https://www.iherb.com/c/toners",
            "Face Moisturizers": "https://www.iherb.com/c/face-moisturizers-creams",
            "Eye Creams": "https://www.iherb.com/c/eye-creams",
            "Face Mist": "https://www.iherb.com/c/face-mist",
            "Face Oils": "https://www.iherb.com/c/face-oil-care",
            "Night Moisturizers & Creams": "https://www.iherb.com/c/night-moisturizers-creams",
            "K-Beauty": "https://www.iherb.com/c/k-beauty",
            "K-Beauty Cleansers": "https://www.iherb.com/c/k-beauty-cleansers",
            "K-Beauty Face Masks": "https://www.iherb.com/c/k-beauty-face-masks",
            "K-Beauty Toners": "https://www.iherb.com/c/k-beauty-toners",
            "K-Beauty Moisturizers": "https://www.iherb.com/c/k-beauty-moisturizers-creams",
            "K-Beauty Treatments & Serums": "https://www.iherb.com/c/k-beauty-treatments-serums",
            "Makeup": "https://www.iherb.com/c/makeup",
            "Eyes": "https://www.iherb.com/c/eye",
            "Face": "https://www.iherb.com/c/face",
            "Lips": "https://www.iherb.com/c/lips",
            "Makeup Removers": "https://www.iherb.com/c/makeup-remover",
            "Nails": "https://www.iherb.com/c/nail",
            "Makeup Accessories": "https://www.iherb.com/c/makeup-brushes-accessories",
            "Makeup Brushes": "https://www.iherb.com/c/makeup-brushes",
            "Makeup Tools": "https://www.iherb.com/c/makeup-tools",
            "Makeup & Skincare Gifts": "https://www.iherb.com/c/makeup-skin-care-gifts",
            "Sunscreen": "https://www.iherb.com/c/sunscreen",
            "Baby & Kids Sunscreen": "https://www.iherb.com/c/baby-kids-sunscreen",
            "Face Sunscreen": "https://www.iherb.com/c/face-sunscreen",
            "K-Beauty Sunscreen": "https://www.iherb.com/c/k-beauty-sunscreen",
            "Treatments & Serums": "https://www.iherb.com/c/treatments-serums",
            "Acne & Blemish Treatments": "https://www.iherb.com/c/acne-blemish-treatments",
            "Anti-Aging & Firming Serums": "https://www.iherb.com/c/anti-aging-firming-serums",
            "Hydrating Serums": "https://www.iherb.com/c/hydrating-serums",
            "Vitamin C Serums": "https://www.iherb.com/c/vitamin-c-serums",
            "Shop all Beauty": "https://www.iherb.com/c/beauty"
        }
    },
    "Grocery": {
        "url": "https://www.iherb.com/c/grocery",
        "subcategories": {
            "Baking, Flour & Mixes": "https://www.iherb.com/c/baking-flour-mixes",
            "Almond Flour & Meal": "https://www.iherb.com/c/almond-flour-meal",
            "Extracts & Food Coloring": "https://www.iherb.com/c/extracts-food-coloring",
            "Pancake & Waffle Mix": "https://www.iherb.com/c/pancake-waffle-mix",
            "Bars": "https://www.iherb.com/c/bars",
            "Energy Bars": "https://www.iherb.com/c/energy-bars",
            "Plant Based Protein Bars": "https://www.iherb.com/c/plant-based-protein-bars",
            "Protein Bars": "https://www.iherb.com/c/protein-bars",
            "Snack Bars": "https://www.iherb.com/c/snack-bars",
            "Cereals & Breakfast Foods": "https://www.iherb.com/c/cereals-breakfast-foods",
            "Baby Cereal": "https://www.iherb.com/c/baby-cereal",
            "Granola": "https://www.iherb.com/c/granola",
            "Oatmeal": "https://www.iherb.com/c/oatmeal",
            "Chocolate & Candy": "https://www.iherb.com/c/chocolate-candy",
            "Candy": "https://www.iherb.com/c/candy",
            "Chocolate": "https://www.iherb.com/c/chocolate",
            "Gum & Mints": "https://www.iherb.com/c/gum-mints",
            "Condiments, Sauces & Spreads": "https://www.iherb.com/c/condiments-sauces-spreads",
            "Nut Butters & Spreads": "https://www.iherb.com/c/nut-butters-spreads",
            "Sauces & Marinades": "https://www.iherb.com/c/sauces-marinades",
            "Herbs & Spices": "https://www.iherb.com/c/herb-spices",
            "Cinnamon Spices": "https://www.iherb.com/c/cinnamon-spices",
            "Garlic Powder & Seasoning": "https://www.iherb.com/c/garlic-powder-seasoning",
            "Salt": "https://www.iherb.com/c/salt",
            "Spice Blends": "https://www.iherb.com/c/spice-blends",
            "Honey & Sweeteners": "https://www.iherb.com/c/honey-sweeteners",
            "Allulose": "https://www.iherb.com/c/allulose",
            "Erythritol": "https://www.iherb.com/c/erythritol",
            "Honey": "https://www.iherb.com/c/honey",
            "Manuka Honey": "https://www.iherb.com/c/manuka-honey",
            "Maple Syrup": "https://www.iherb.com/c/maple-syrup",
            "Monk Fruit": "https://www.iherb.com/c/monk-fruit",
            "Stevia": "https://www.iherb.com/c/stevia",
            "Oils & Vinegar": "https://www.iherb.com/c/oils-vinegar",
            "Apple Cider Vinegar": "https://www.iherb.com/c/apple-cider-vinegar-grocery",
            "Avocado Oil": "https://www.iherb.com/c/avocado-oil",
            "Coconut Oil": "https://www.iherb.com/c/coconut-oil",
            "Ghee": "https://www.iherb.com/c/ghee",
            "Olive Oil": "https://www.iherb.com/c/olive-oil",
            "Packaged Foods": "https://www.iherb.com/c/packaged-prepared-foods",
            "Beans & Lentils": "https://www.iherb.com/c/beans-lentils",
            "Bread & Wraps": "https://www.iherb.com/c/bread-wraps",
            "Pasta & Noodles": "https://www.iherb.com/c/pasta-noodles",
            "Ready-to-Eat Meals": "https://www.iherb.com/c/ready-to-eat-meals",
            "Seafood": "https://www.iherb.com/c/seafood",
            "Soup & Broth": "https://www.iherb.com/c/soup-broth",
            "Snacks": "https://www.iherb.com/c/snacks",
            "Chips": "https://www.iherb.com/c/chips",
            "Cookies": "https://www.iherb.com/c/cookies",
            "Crackers": "https://www.iherb.com/c/crackers",
            "Dried Fruits & Vegetables": "https://www.iherb.com/c/dried-fruits-vegetables",
            "Nuts & Seeds": "https://www.iherb.com/c/nuts-seeds",
            "Seaweed Snacks": "https://www.iherb.com/c/seaweed-snacks",
            "Tea & Beverages": "https://www.iherb.com/c/tea-beverages",
            "Black Tea": "https://www.iherb.com/c/black-tea",
            "Chamomile Tea": "https://www.iherb.com/c/chamomile-tea",
            "Coffee": "https://www.iherb.com/c/coffee",
            "Cocoa Powder & Hot Chocolate": "https://www.iherb.com/c/cocoa-powder-hot-chocolate",
            "Fruit Tea": "https://www.iherb.com/c/fruit-tea",
            "Green Tea": "https://www.iherb.com/c/green-tea",
            "Instant Coffee": "https://www.iherb.com/c/instant-coffee",
            "Herbal Tea": "https://www.iherb.com/c/herbal-tea",
            "Matcha": "https://www.iherb.com/c/matcha",
            "Medicinal Teas": "https://www.iherb.com/c/medicinal-teas",
            "Tea & Coffee Accessories": "https://www.iherb.com/c/tea-coffee-accessories",
            "Shop all Grocery": "https://www.iherb.com/c/grocery"
        }
    },
    "Home": {
        "url": "https://www.iherb.com/c/healthy-home",
        "subcategories": {
            "Cleaning": "https://www.iherb.com/c/cleaning",
            "Dishwashing": "https://www.iherb.com/c/dishwashing",
            "Household Surface Cleaners": "https://www.iherb.com/c/household-surface-cleaners",
            "Laundry": "https://www.iherb.com/c/laundry",
            "Drinkware": "https://www.iherb.com/c/drinkware",
            "Shaker Cups": "https://www.iherb.com/c/shaker-cups",
            "Water Bottles": "https://www.iherb.com/c/water-bottles",
            "Essential Oils": "https://www.iherb.com/c/essential-oils-aromatherapy",
            "Essential Oil Diffusers": "https://www.iherb.com/c/essential-oil-diffusers",
            "Incense": "https://www.iherb.com/c/incense",
            "Single Essential Oils": "https://www.iherb.com/c/single-essential-oils",
            "Home Fragrance": "https://www.iherb.com/c/home-fragrance",
            "Air & Fabric Fresheners": "https://www.iherb.com/c/air-fresheners-deodorizer",
            "Candles": "https://www.iherb.com/c/candles",
            "Kitchen Supplies": "https://www.iherb.com/c/kitchen-supplies",
            "Food Storage & Containers": "https://www.iherb.com/c/food-storage-containers",
            "Produce & Food Wash": "https://www.iherb.com/c/produce-food-wash",
            "Tea & Coffee Accessories": "https://www.iherb.com/c/tea-coffee-accessories",
            "Home Accessories": "https://www.iherb.com/c/home-accessories",
            "Shop all Home": "https://www.iherb.com/c/healthy-home"
        }
    },
    "Baby": {
        "url": "https://www.iherb.com/c/baby-kids",
        "subcategories": {
            "Bath, Skin & Hair": "https://www.iherb.com/c/baby-kids-bath-skin-hair",
            "All-in-One Shampoo & Wash": "https://www.iherb.com/c/baby-kids-all-in-one-shampoo-wash",
            "Lotion & Cream": "https://www.iherb.com/c/baby-kids-lotion-cream",
            "Skin Treatments": "https://www.iherb.com/c/baby-kids-skin-treatments",
            "Conditioners & Detanglers": "https://www.iherb.com/c/baby-kids-conditioners-detanglers",
            "Shampoo": "https://www.iherb.com/c/baby-kids-shampoo",
            "Feeding": "https://www.iherb.com/c/baby-kids-feeding",
            "Snacks": "https://www.iherb.com/c/baby-kids-snacks",
            "Cereal": "https://www.iherb.com/c/baby-cereal",
            "Pouches, Purees & Meals": "https://www.iherb.com/c/pouches-purees-meals",
            "Formula": "https://www.iherb.com/c/baby-formula",
            "Home": "https://www.iherb.com/c/baby-kids-home",
            "Detergent": "https://www.iherb.com/c/baby-detergent",
            "Dish Soaps": "https://www.iherb.com/c/baby-dish-soaps",
            "Safety": "https://www.iherb.com/c/baby-kids-safety",
            "Nasal Care": "https://www.iherb.com/c/baby-kids-nasal-care",
            "Sunscreen": "https://www.iherb.com/c/baby-kids-sunscreen",
            "Lice Prevention & Treatment": "https://www.iherb.com/c/lice-prevention-treatment",
            "Bug Repellents": "https://www.iherb.com/c/baby-kids-bug-repellents",
            "Baby & Kid's Toys": "https://www.iherb.com/c/baby-kids-toys",
            "Bath Toys": "https://www.iherb.com/c/bath-toys",
            "Health": "https://www.iherb.com/c/childrens-health",
            "DHA & Omegas": "https://www.iherb.com/c/childrens-dha-omega",
            "Herbs": "https://www.iherb.com/c/childrens-herbs",
            "Melatonin & Sleep Aids": "https://www.iherb.com/c/childrens-melatonin-sleep-aids",
            "Multivitamins": "https://www.iherb.com/c/childrens-multivitamins",
            "Probiotics": "https://www.iherb.com/c/childrens-probiotics",
            "Cold, Flu & Cough": "https://www.iherb.com/c/childrens-cold-flu-cough",
            "Vitamin D": "https://www.iherb.com/c/childrens-vitamin-d",
            "Minerals": "https://www.iherb.com/c/childrens-minerals",
            "Calcium": "https://www.iherb.com/c/childrens-calcium",
            "Vitamin C": "https://www.iherb.com/c/childrens-vitamin-c",
            "Teen Health": "https://www.iherb.com/c/teen-health",
            "Diapering": "https://www.iherb.com/c/diapering",
            "Moms & Maternity": "https://www.iherb.com/c/moms-maternity",
            "Lactation Support": "https://www.iherb.com/c/lactation-support",
            "Pregnancy & Ovulation Tests": "https://www.iherb.com/c/pregnancy-ovulation-tests",
            "Women's Fertility": "https://www.iherb.com/c/womens-fertility",
            "Pacifiers & Clips": "https://www.iherb.com/c/pacifiers-clips",
            "Teething & Oral Care": "https://www.iherb.com/c/teething-oral-care",
            "Shop all Baby & Kids": "https://www.iherb.com/c/baby-kids"
        }
    },
    "Pets": {
        "url": "https://www.iherb.com/c/pets",
        "subcategories": {
            "Pet Grooming": "https://www.iherb.com/c/pet-grooming",
            "Cat Grooming": "https://www.iherb.com/c/cat-grooming",
            "Dog Grooming": "https://www.iherb.com/c/dog-grooming",
            "Pet Supplies": "https://www.iherb.com/c/pet-supplies",
            "Pet Stain & Odor Removers": "https://www.iherb.com/c/pet-stain-odor-removers",
            "Dog Waste Bags & Pads": "https://www.iherb.com/c/dog-waste-bags-pads",
            "Pet Supplements": "https://www.iherb.com/c/pet-supplements",
            "Cat Supplements": "https://www.iherb.com/c/cat-supplements",
            "Dog Supplements": "https://www.iherb.com/c/dog-supplements",
            "Pet Food & Treats": "https://www.iherb.com/c/pet-food-treats",
            "Cat Treats": "https://www.iherb.com/c/cat-treats",
            "Dog Treats": "https://www.iherb.com/c/dog-treats",
            "Pet Health": "https://www.iherb.com/c/pet-health",
            "Cat Treatments & Remedies": "https://www.iherb.com/c/cat-treatments-remedies",
            "Dog Treatments & Remedies": "https://www.iherb.com/c/dog-treatments-remedies",
            "Pet Toys": "https://www.iherb.com/c/pet-toys",
            "Dog Toys": "https://www.iherb.com/c/dog-toys",
            "Shop all Pets": "https://www.iherb.com/c/pets"
        }
    },
    "Health Topics": {
        "url": "https://www.iherb.com/c/health-topics",
        "subcategories": {
            "Anti-Aging & Longevity": "https://www.iherb.com/c/anti-aging-longevity",
            "Arthritis": "https://www.iherb.com/c/arthritis",
            "Biohacking": "https://www.iherb.com/c/biohacking",
            "Eye & Vision": "https://www.iherb.com/c/eye-vision",
            "Memory": "https://www.iherb.com/c/brain-cognitive",
            "Metabolism": "https://www.iherb.com/c/metabolism",
            "GLP-1 Support": "https://www.iherb.com/c/glp-1-support",
            "Hydration": "https://www.iherb.com/c/electrolytes-hydration",
            "High Protein": "https://www.iherb.com/c/high-protein",
            "Recovery": "https://www.iherb.com/c/muscle-recovery-supplements",
            "Bone, Joint & Cartilage": "https://www.iherb.com/c/bone-joint-cartilage",
            "Cardiovascular Support": "https://www.iherb.com/c/cardiovascular-support",
            "Colon": "https://www.iherb.com/c/colon",
            "Ears, Nose & Throat": "https://www.iherb.com/c/ear-nose-throat",
            "Gut Health": "https://www.iherb.com/c/gut-health",
            "Heart": "https://www.iherb.com/c/heart",
            "Hormonal Health": "https://www.iherb.com/c/hormonal-health",
            "Liver Support": "https://www.iherb.com/c/liver-formulas",
            "Prostate": "https://www.iherb.com/c/prostate",
            "Respiratory": "https://www.iherb.com/c/respiratory-support",
            "Sexual Health": "https://www.iherb.com/c/sexual-health",
            "Urinary Tract": "https://www.iherb.com/c/urinary-tract",
            "Acne": "https://www.iherb.com/c/acne-blemish-treatments",
            "Body": "https://www.iherb.com/c/body-care",
            "Energy": "https://www.iherb.com/c/energy",
            "Hair Treatments": "https://www.iherb.com/c/hair-treatments",
            "Hair, Skin & Nails Support": "https://www.iherb.com/c/hair-skin-nails",
            "Lip Care": "https://www.iherb.com/c/lip-care",
            "Massage": "https://www.iherb.com/c/body-massage-oil",
            "Oral Care": "https://www.iherb.com/c/oral-care",
            "Personal Care": "https://www.iherb.com/c/personal-care",
            "Skin Care": "https://www.iherb.com/c/skin-care-1",
            "Sunscreen": "https://www.iherb.com/c/sunscreen",
            "Weight Management": "https://www.iherb.com/c/weight-management",
            "Baby & Toddler": "https://www.iherb.com/c/childrens-health",
            "Mens": "https://www.iherb.com/c/mens-health",
            "Seniors": "https://www.iherb.com/c/supplements",
            "Teens": "https://www.iherb.com/c/teen-health",
            "Womens": "https://www.iherb.com/c/womens-wellness/store",
            "Greens & Superfoods": "https://www.iherb.com/c/greens-superfoods",
            "Healthy Fats": "https://www.iherb.com/c/healthy-fats",
            "Healthy Snacking": "https://www.iherb.com/c/healthy-snacking",
            "Meal Replacements": "https://www.iherb.com/c/meal-replacements",
            "Adaptogens": "https://www.iherb.com/c/adaptogens",
            "Blood Sugar Balance": "https://www.iherb.com/c/blood-sugar-balance",
            "Cold & Flu": "https://www.iherb.com/c/common-cold-flu",
            "Detox & Cleanse": "https://www.iherb.com/c/detox-cleanse",
            "Focus": "https://www.iherb.com/c/focus-memory-formulas",
            "Immune Support": "https://www.iherb.com/c/immune-support",
            "Mood Balance & Anxiety": "https://www.iherb.com/c/mood-balance-anxiety",
            "Pain Relief": "https://www.iherb.com/c/pain-relief",
            "Seasonal Allergies": "https://www.iherb.com/c/seasonal-allergies",
            "Sleep": "https://www.iherb.com/c/sleep",
            "Stress": "https://www.iherb.com/c/stress-relief-formulas",
            "Travel": "https://www.iherb.com/c/travel/store",
            "Derm Skincare": "https://www.iherb.com/c/dermatological-beauty/store",
            "Professional Brands": "https://www.iherb.com/c/professional-brands"
        }
    }
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def url_name_for(url: str) -> str:
    """Return the storefront ``urlName`` for an iHerb PLP path.

    ``https://www.iherb.com/c/magnesium``            -> ``magnesium``
    ``https://www.iherb.com/c/sportcertified/store`` -> ``sportcertified/store``
    """
    path = re.sub(r"^https?://[^/]+", "", (url or "").strip())
    path = path.split("?", 1)[0].split("#", 1)[0].strip("/")
    parts = [segment for segment in path.split("/") if segment]
    if parts and parts[0] == "c":
        parts = parts[1:]
    return "/".join(parts)


def _flatten_categories() -> list[dict[str, str]]:
    """Flatten the inventory into ``BaseListingSpider`` category entries.

    Entries are deduplicated on the API ``urlName`` (not the HTML URL) so a
    storefront path is never requested twice, and category names that collide
    across departments are prefixed with their department.
    """
    categories: list[dict[str, str]] = []
    seen_url_names: set[str] = set()
    used_names: set[str] = set()
    for root, group in IHERB_CATEGORY_INVENTORY.items():
        entries = [(root, group["url"]), *group["subcategories"].items()]
        for label, url in entries:
            url_name = url_name_for(url)
            if not url_name or url_name in seen_url_names:
                continue
            seen_url_names.add(url_name)
            base = _slug(label)
            name = base
            if name in used_names:
                name = f"{_slug(root)}-{base}"
            suffix = 2
            while name in used_names:
                name = f"{_slug(root)}-{base}-{suffix}"
                suffix += 1
            used_names.add(name)
            categories.append(
                {
                    "category": name,
                    "department": root,
                    "subcategory": label,
                    "url": url,
                    "url_name": url_name,
                }
            )
    return categories


IHERB_CATEGORIES = _flatten_categories()
