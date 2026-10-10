"""Checked-in Walgreens navigation snapshot (issue #189).

The names below are stable CLI-friendly leaves captured from Walgreens' header
and ``/productapi/v1/categories/{id}/children`` taxonomy.  The spider never
calls the taxonomy API while crawling products.
"""

BASE = "https://www.walgreens.com"

WALGREENS_CATEGORIES = {
    "health": {
        "Allergy & Sinus": {
            "category_id": "360545",
            "url": "https://www.walgreens.com/store/c/allergy-and-sinus/ID=360545-tier2general",
            "department": "health",
            "category": "Allergy & Sinus",
        },
        "Incontinence": {
            "category_id": "360513",
            "url": "https://www.walgreens.com/store/c/incontinence/ID=360513-tier2general",
            "department": "health",
            "category": "Incontinence",
        },
        "Home Tests & Monitoring": {
            "category_id": "360517",
            "url": "https://www.walgreens.com/store/c/home-tests-and-monitoring/ID=360517-tier2general",
            "department": "health",
            "category": "Home Tests & Monitoring",
        },
        "Eye Care": {
            "category_id": "360509",
            "url": "https://www.walgreens.com/store/c/eye-care/ID=360509-tier2general",
            "department": "health",
            "category": "Eye Care",
        },
        "Foot Care": {
            "category_id": "360511",
            "url": "https://www.walgreens.com/store/c/foot-care/ID=360511-tier2general",
            "department": "health",
            "category": "Foot Care",
        },
        "Cough, Cold & Flu": {
            "category_id": "360549",
            "url": "https://www.walgreens.com/store/c/cough-cold-and-flu/ID=360549-tier2general",
            "department": "health",
            "category": "Cough, Cold & Flu",
        },
        "First Aid": {
            "category_id": "360533",
            "url": "https://www.walgreens.com/store/c/first-aid/ID=360533-tier2general",
            "department": "health",
            "category": "First Aid",
        },
        "Pain Relief & Management": {
            "category_id": "360547",
            "url": "https://www.walgreens.com/store/c/pain-relief-and-management/ID=360547-tier2general",
            "department": "health",
            "category": "Pain Relief & Management",
        },
        "Digestive Health & Nausea": {
            "category_id": "360543",
            "url": "https://www.walgreens.com/store/c/digestive-health-and-nausea/ID=360543-tier2general",
            "department": "health",
            "category": "Digestive Health & Nausea",
        },
        "Bathroom Safety": {
            "category_id": "360585",
            "url": "https://www.walgreens.com/store/c/bathroom-safety/ID=360585-tier2general",
            "department": "health",
            "category": "Bathroom Safety",
        },
        "Walkers & Rollators": {
            "category_id": "360591",
            "url": "https://www.walgreens.com/store/c/walkers-and-rollators/ID=360591-tier2general",
            "department": "health",
            "category": "Walkers & Rollators",
        },
    },
    "grocery": {
        "Snacks": {
            "category_id": "360665",
            "url": "https://www.walgreens.com/store/c/snacks/ID=360665-tier2general",
            "department": "grocery",
            "category": "Snacks",
        },
        "Beverages": {
            "category_id": "360663",
            "url": "https://www.walgreens.com/store/c/beverages/ID=360663-tier2general",
            "department": "grocery",
            "category": "Beverages",
        },
        "Candy & Chocolate": {
            "category_id": "360667",
            "url": "https://www.walgreens.com/store/c/candy-and-chocolate/ID=360667-tier2general",
            "department": "grocery",
            "category": "Candy & Chocolate",
        },
    },
    "beauty": {
        "Skin Care": {
            "category_id": "360323",
            "url": "https://www.walgreens.com/store/c/skin-care/ID=360323-tier2general",
            "department": "beauty",
            "category": "Skin Care",
        },
        "Makeup": {
            "category_id": "360337",
            "url": "https://www.walgreens.com/store/c/makeup/ID=360337-tier2general",
            "department": "beauty",
            "category": "Makeup",
        },
        "Hair Care": {
            "category_id": "360339",
            "url": "https://www.walgreens.com/store/c/hair-care/ID=360339-tier2general",
            "department": "beauty",
            "category": "Hair Care",
        },
        "Bath & Body": {
            "category_id": "360341",
            "url": "https://www.walgreens.com/store/c/bath-and-body/ID=360341-tier2general",
            "department": "beauty",
            "category": "Bath & Body",
        },
        "Oral Care": {
            "category_id": "360523",
            "url": "https://www.walgreens.com/store/c/oral-care/ID=360523-tier2general",
            "department": "beauty",
            "category": "Oral Care",
        },
        "Shaving & Grooming": {
            "category_id": "360521",
            "url": "https://www.walgreens.com/store/c/shaving-and-grooming/ID=360521-tier2general",
            "department": "beauty",
            "category": "Shaving & Grooming",
        },
        "Feminine Care": {
            "category_id": "360515",
            "url": "https://www.walgreens.com/store/c/feminine-care/ID=360515-tier2general",
            "department": "beauty",
            "category": "Feminine Care",
        },
    },
    "household": {
        "Cleaning Supplies": {
            "category_id": "20000911",
            "url": "https://www.walgreens.com/store/c/cleaning-supplies/ID=20000911-tier2general",
            "department": "household",
            "category": "Cleaning Supplies",
        },
        "Laundry Care": {
            "category_id": "20000924",
            "url": "https://www.walgreens.com/store/c/laundry-care/ID=20000924-tier2general",
            "department": "household",
            "category": "Laundry Care",
        },
        "Pet Supplies": {
            "category_id": "20000613",
            "url": "https://www.walgreens.com/store/c/pet-supplies/ID=20000613-tier2general",
            "department": "household",
            "category": "Pet Supplies",
        },
    },
    "sexual-wellness": {
        "Condoms & Contraceptives": {
            "category_id": "360609",
            "url": "https://www.walgreens.com/store/c/condoms-and-contraceptives/ID=360609-tier2general",
            "department": "sexual-wellness",
            "category": "Condoms & Contraceptives",
        },
    },
    "vitamins": {
        "Multivitamins": {
            "category_id": "360567",
            "url": "https://www.walgreens.com/store/c/multivitamins/ID=360567-tier2general",
            "department": "vitamins",
            "category": "Multivitamins",
        },
        "Supplements": {
            "category_id": "360559",
            "url": "https://www.walgreens.com/store/c/supplements/ID=360559-tier2general",
            "department": "vitamins",
            "category": "Supplements",
        },
        "Fish Oil & Omegas": {
            "category_id": "360557",
            "url": "https://www.walgreens.com/store/c/fish-oil-and-omegas/ID=360557-tier2general",
            "department": "vitamins",
            "category": "Fish Oil & Omegas",
        },
        "Weight Management": {
            "category_id": "360625",
            "url": "https://www.walgreens.com/store/c/weight-management/ID=360625-tier2general",
            "department": "vitamins",
            "category": "Weight Management",
        },
        "Sports Nutrition": {
            "category_id": "360623",
            "url": "https://www.walgreens.com/store/c/sports-nutrition/ID=360623-tier2general",
            "department": "vitamins",
            "category": "Sports Nutrition",
        },
    },
    "baby": {
        "Diapering": {
            "category_id": "360645",
            "url": "https://www.walgreens.com/store/c/diapering/ID=360645-tier2general",
            "department": "baby",
            "category": "Diapering",
        },
        "Baby Food & Formula": {
            "category_id": "360643",
            "url": "https://www.walgreens.com/store/c/baby-food-and-formula/ID=360643-tier2general",
            "department": "baby",
            "category": "Baby Food & Formula",
        },
    },
    "toys": {
        "Games & Puzzles": {
            "category_id": "20001434",
            "url": "https://www.walgreens.com/store/c/games-and-puzzles/ID=20001434-tier2general",
            "department": "toys",
            "category": "Games & Puzzles",
        },
        "Arts & Crafts": {
            "category_id": "20001042",
            "url": "https://www.walgreens.com/store/c/arts-and-crafts/ID=20001042-tier2general",
            "department": "toys",
            "category": "Arts & Crafts",
        },
    },
    "gifts": {
        "Specialty Gift Cards": {
            "category_id": "20001460",
            "url": "https://www.walgreens.com/store/c/specialty-gift-cards/ID=20001460-tier2general",
            "department": "gifts",
            "category": "Specialty Gift Cards",
        },
    },
}
