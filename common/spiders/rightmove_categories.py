from __future__ import annotations


RIGHTMOVE_CATEGORIES = [
    {"category": slug, "url": f"https://www.rightmove.co.uk/property-for-sale/{location}.html"}
    for slug, location in (
        ("london", "London"),
        ("manchester", "Manchester"),
        ("birmingham", "Birmingham"),
        ("leeds", "Leeds"),
        ("liverpool", "Liverpool"),
        ("bristol", "Bristol"),
        ("leicester", "Leicester"),
        ("sheffield", "Sheffield"),
        ("cardiff", "Cardiff"),
        ("coventry", "Coventry"),
        ("milton-keynes", "Milton-Keynes"),
        ("southampton", "Southampton"),
        ("nottingham", "Nottingham"),
        ("brighton", "Brighton"),
        ("glasgow", "Glasgow"),
        ("norwich", "Norwich"),
        ("edinburgh", "Edinburgh"),
        ("portsmouth", "Portsmouth"),
        ("derby", "Derby"),
        ("plymouth", "Plymouth"),
    )
]
