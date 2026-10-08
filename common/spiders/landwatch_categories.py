"""Stable, high-inventory LandWatch state listing seeds."""

LANDWATCH_CATEGORIES = [
    {"category": state, "url": f"https://www.landwatch.com/{state}-land-for-sale"}
    for state in (
        "texas",
        "florida",
        "georgia",
        "north-carolina",
        "california",
        "michigan",
        "tennessee",
        "arkansas",
        "arizona",
        "missouri",
        "virginia",
        "new-york",
        "south-carolina",
        "oklahoma",
        "colorado",
        "kentucky",
        "wisconsin",
        "louisiana",
        "pennsylvania",
        "indiana",
    )
]
