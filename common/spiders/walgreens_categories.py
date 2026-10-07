"""Checked-in Walgreens navigation snapshot (issue #189).

The names below are stable CLI-friendly leaves captured from Walgreens' header
and ``/productapi/v1/categories/{id}/children`` taxonomy.  The spider never
calls the taxonomy API while crawling products.
"""

BASE = "https://www.walgreens.com"


def _category(name: str, category_id: str, slug: str) -> dict[str, str]:
    return {
        "category": name,
        "category_id": category_id,
        "url": f"{BASE}/store/c/{slug}/ID={category_id}-tier2general",
    }


WALGREENS_CATEGORIES = [
    _category("Allergy & Sinus", "360545", "allergy-and-sinus"),
    _category("Snacks", "360665", "snacks"),
    _category("Beverages", "360663", "beverages"),
    _category("Candy & Chocolate", "360667", "candy-and-chocolate"),
    _category("Skin Care", "360323", "skin-care"),
    _category("Makeup", "360337", "makeup"),
    _category("Hair Care", "360339", "hair-care"),
    _category("Bath & Body", "360341", "bath-and-body"),
    _category("Oral Care", "360523", "oral-care"),
    _category("Incontinence", "360513", "incontinence"),
    _category("Shaving & Grooming", "360521", "shaving-and-grooming"),
    _category("Home Tests & Monitoring", "360517", "home-tests-and-monitoring"),
    _category("Feminine Care", "360515", "feminine-care"),
    _category("Eye Care", "360509", "eye-care"),
    _category("Foot Care", "360511", "foot-care"),
    _category("Cleaning Supplies", "20000911", "cleaning-supplies"),
    _category("Laundry Care", "20000924", "laundry-care"),
    _category("Pet Supplies", "20000613", "pet-supplies"),
    _category("Cough, Cold & Flu", "360549", "cough-cold-and-flu"),
    _category("First Aid", "360533", "first-aid"),
    _category("Pain Relief & Management", "360547", "pain-relief-and-management"),
    _category("Digestive Health & Nausea", "360543", "digestive-health-and-nausea"),
    _category("Condoms & Contraceptives", "360609", "condoms-and-contraceptives"),
    _category("Multivitamins", "360567", "multivitamins"),
    _category("Supplements", "360559", "supplements"),
    _category("Fish Oil & Omegas", "360557", "fish-oil-and-omegas"),
    _category("Diapering", "360645", "diapering"),
    _category("Baby Food & Formula", "360643", "baby-food-and-formula"),
    _category("Games & Puzzles", "20001434", "games-and-puzzles"),
    _category("Arts & Crafts", "20001042", "arts-and-crafts"),
    _category("Bathroom Safety", "360585", "bathroom-safety"),
    _category("Walkers & Rollators", "360591", "walkers-and-rollators"),
    _category("Weight Management", "360625", "weight-management"),
    _category("Sports Nutrition", "360623", "sports-nutrition"),
    _category("Specialty Gift Cards", "20001460", "specialty-gift-cards"),
]
