"""Twenty deterministic high-volume Apartments.com rental markets."""

APARTMENTS_CATEGORIES = [
    {"category": slug, "url": f"https://www.apartments.com/{slug}/"}
    for slug in (
        "new-york-ny",
        "los-angeles-ca",
        "chicago-il",
        "houston-tx",
        "phoenix-az",
        "philadelphia-pa",
        "san-antonio-tx",
        "san-diego-ca",
        "dallas-tx",
        "san-jose-ca",
        "austin-tx",
        "jacksonville-fl",
        "fort-worth-tx",
        "columbus-oh",
        "charlotte-nc",
        "indianapolis-in",
        "san-francisco-ca",
        "seattle-wa",
        "denver-co",
        "boston-ma",
    )
]
