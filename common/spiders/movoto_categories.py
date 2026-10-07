from __future__ import annotations


CATEGORIES = {
    slug: f"https://www.movoto.com/{slug}/"
    for slug in (
        "new-york-ny", "los-angeles-ca", "chicago-il", "houston-tx",
        "phoenix-az", "philadelphia-pa", "san-antonio-tx", "san-diego-ca",
        "dallas-tx", "san-jose-ca", "austin-tx", "jacksonville-fl",
        "fort-worth-tx", "columbus-oh", "charlotte-nc", "indianapolis-in",
        "seattle-wa", "denver-co", "boston-ma", "las-vegas-nv",
    )
}

MOVOTO_CATEGORIES = [
    {"category": category, "url": url} for category, url in CATEGORIES.items()
]
