"""Featured Marriott city destinations exposed by the destinations catalogue."""

MARRIOTT_CATEGORIES = [
    {"category": slug, "url": f"https://www.marriott.com/en-us/destinations/{path}.mi"}
    for slug, path in [
        ("new-york-city", "united-states/new-york/new-york-city"),
        ("las-vegas", "united-states/nevada/las-vegas"),
        ("miami", "united-states/florida/miami"),
        ("orlando", "united-states/florida/orlando"),
        ("chicago", "united-states/illinois/chicago"),
        ("san-francisco", "united-states/california/san-francisco"),
        ("san-diego", "united-states/california/san-diego"),
        ("washington-dc", "united-states/district-of-columbia/washington-dc"),
        ("boston", "united-states/massachusetts/boston"),
        ("seattle", "united-states/washington/seattle"),
        ("denver", "united-states/colorado/denver"),
        ("maui", "united-states/hawaii/maui"),
        ("nashville", "united-states/tennessee/nashville"),
        ("charleston", "united-states/south-carolina/charleston"),
        ("london", "united-kingdom/london"),
        ("paris", "france/paris"),
        ("rome", "italy/rome"),
        ("barcelona", "spain/barcelona"),
        ("tokyo", "japan/tokyo"),
        ("toronto", "canada/toronto"),
    ]
]
