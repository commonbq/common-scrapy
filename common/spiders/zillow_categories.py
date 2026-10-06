"""Top US Zillow sale markets, ordered by live listing volume."""

ZILLOW_CATEGORIES = [
    {"category": slug, "url": f"https://www.zillow.com/homes/for_sale/{path}/"}
    for slug, path in [
        ("houston-tx", "Houston-TX"), ("san-antonio-tx", "San-Antonio-TX"),
        ("los-angeles-ca", "Los-Angeles-CA"), ("las-vegas-nv", "Las-Vegas-NV"),
        ("philadelphia-pa", "Philadelphia-PA"), ("miami-fl", "Miami-FL"),
        ("chicago-il", "Chicago-IL"), ("jacksonville-fl", "Jacksonville-FL"),
        ("phoenix-az", "Phoenix-AZ"), ("austin-tx", "Austin-TX"),
        ("nashville-tn", "Nashville-TN"), ("atlanta-ga", "Atlanta-GA"),
        ("dallas-tx", "Dallas-TX"), ("charlotte-nc", "Charlotte-NC"),
        ("indianapolis-in", "Indianapolis-IN"), ("denver-co", "Denver-CO"),
        ("washington-dc", "Washington-DC"), ("seattle-wa", "Seattle-WA"),
        ("san-diego-ca", "San-Diego-CA"), ("portland-or", "Portland-OR"),
    ]
]
