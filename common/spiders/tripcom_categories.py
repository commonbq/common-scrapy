"""Trip.com popular hotel destinations."""

TRIPCOM_CATEGORIES = [
    {"category": slug, "url": f"https://us.trip.com/hotels/{path}/"}
    for slug, path in (
        ("shanghai", "shanghai-hotels-list-2"), ("hong-kong", "hong-kong-hotels-list-58"),
        ("las-vegas", "las-vegas-hotels-list-26282"), ("bangkok", "bangkok-hotels-list-359"),
        ("beijing", "beijing-hotels-list-1"), ("guangzhou", "guangzhou-hotels-list-32"),
        ("new-york", "new-york-hotels-list-633"), ("singapore", "singapore-hotels-list-73"),
        ("kuala-lumpur", "kuala-lumpur-hotels-list-315"), ("dubai", "dubai-hotels-list-220"),
        ("chicago", "chicago-hotels-list-549"), ("san-diego", "san-diego-hotels-list-698"),
        ("miami", "miami-hotels-list-25773"), ("new-orleans", "new-orleans-hotels-list-1186"),
        ("nashville", "nashville-hotels-list-3228"), ("boston", "boston-hotels-list-26848"),
        ("orlando", "orlando-hotels-list-1187"), ("savannah", "savannah-hotels-list-26631"),
        ("charleston", "charleston-hotels-list-4188"), ("los-angeles", "los-angeles-hotels-list-347"),
    )
]
