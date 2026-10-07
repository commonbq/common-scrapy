"""Major US HotPads rental markets in deterministic order."""

HOTPADS_CATEGORIES = [
    {"category": slug, "url": f"https://hotpads.com/{slug}/apartments-for-rent"}
    for slug in [
        "new-york-ny", "los-angeles-ca", "chicago-il", "houston-tx",
        "phoenix-az", "philadelphia-pa", "san-antonio-tx", "san-diego-ca",
        "dallas-tx", "san-jose-ca", "austin-tx", "jacksonville-fl",
        "fort-worth-tx", "columbus-oh", "charlotte-nc", "indianapolis-in",
        "san-francisco-ca", "seattle-wa", "denver-co", "boston-ma",
    ]
]
