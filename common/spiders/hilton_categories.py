"""Major US Hilton destination pages."""

HILTON_CATEGORIES = [
    {"category": slug, "url": f"https://www.hilton.com/en/locations/usa/{state}/{city}/"}
    for slug, state, city in [
        ("new-york-ny", "new-york", "new-york"),
        ("los-angeles-ca", "california", "los-angeles"),
        ("chicago-il", "illinois", "chicago"),
        ("miami-fl", "florida", "miami"),
        ("las-vegas-nv", "nevada", "las-vegas"),
        ("orlando-fl", "florida", "orlando"),
        ("san-francisco-ca", "california", "san-francisco"),
        ("washington-dc", "district-of-columbia", "washington"),
        ("boston-ma", "massachusetts", "boston"),
        ("seattle-wa", "washington", "seattle"),
        ("houston-tx", "texas", "houston"),
        ("dallas-tx", "texas", "dallas"),
        ("atlanta-ga", "georgia", "atlanta"),
        ("phoenix-az", "arizona", "phoenix"),
        ("san-diego-ca", "california", "san-diego"),
        ("denver-co", "colorado", "denver"),
        ("new-orleans-la", "louisiana", "new-orleans"),
        ("nashville-tn", "tennessee", "nashville"),
        ("austin-tx", "texas", "austin"),
        ("honolulu-hi", "hawaii", "honolulu"),
    ]
]
