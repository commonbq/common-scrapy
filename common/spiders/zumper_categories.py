"""Deterministic major-market categories for Zumper listing pages."""

ZUMPER_CATEGORIES = [
    {"category": slug, "url": f"https://www.zumper.com/apartments-for-rent/{slug}"}
    for slug in (
        "new-york-ny", "los-angeles-ca", "san-francisco-ca", "chicago-il",
        "boston-ma", "seattle-wa", "washington-dc", "miami-fl", "atlanta-ga",
        "philadelphia-pa", "houston-tx", "dallas-tx", "austin-tx", "denver-co",
        "phoenix-az", "san-diego-ca", "portland-or", "minneapolis-mn",
        "las-vegas-nv", "nashville-tn",
    )
]
