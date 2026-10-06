"""Booking.com city destinations exposed by the homepage."""

BOOKING_CATEGORIES = [
    {"category": slug, "url": f"https://www.booking.com/city/us/{path}.html"}
    for slug, path in [
        ("las-vegas", "las-vegas"),
        ("new-york", "new-york"),
        ("los-angeles", "los-angeles"),
        ("orlando", "orlando"),
        ("san-diego", "san-diego"),
        ("san-francisco", "san-francisco"),
        ("fort-lauderdale", "fort-lauderdale"),
        ("south-lake-tahoe", "south-lake-tahoe"),
        ("breckenridge", "breckenridge"),
        ("miami", "miami"),
        ("houston", "houston"),
        ("atlanta", "atlanta"),
        ("denver", "denver"),
        ("new-orleans", "new-orleans"),
        ("chicago", "chicago"),
        ("washington", "washington"),
        ("columbus", "columbus"),
        ("seattle", "seattle"),
        ("myrtle-beach", "myrtle-beach"),
        ("daytona-beach", "daytona-beach"),
    ]
]
