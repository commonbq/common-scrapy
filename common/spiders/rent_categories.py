"""Major US Rent.com apartment markets exposed by the homepage."""

RENT_CATEGORIES = [
    {"category": slug, "url": f"https://www.rent.com/{state}/{city}-apartments"}
    for slug, state, city in [
        ("new-york-ny", "new-york", "new-york"),
        ("los-angeles-ca", "california", "los-angeles"),
        ("chicago-il", "illinois", "chicago"),
        ("houston-tx", "texas", "houston"),
        ("phoenix-az", "arizona", "phoenix"),
        ("philadelphia-pa", "pennsylvania", "philadelphia"),
        ("san-antonio-tx", "texas", "san-antonio"),
        ("san-diego-ca", "california", "san-diego"),
        ("jacksonville-fl", "florida", "jacksonville"),
        ("san-jose-ca", "california", "san-jose"),
        ("austin-tx", "texas", "austin"),
        ("columbus-oh", "ohio", "columbus"),
        ("charlotte-nc", "north-carolina", "charlotte"),
        ("san-francisco-ca", "california", "san-francisco"),
        ("seattle-wa", "washington", "seattle"),
        ("denver-co", "colorado", "denver"),
        ("atlanta-ga", "georgia", "atlanta"),
        ("las-vegas-nv", "nevada", "las-vegas"),
        ("miami-fl", "florida", "miami"),
        ("el-paso-tx", "texas", "el-paso"),
    ]
]
