"""Viator Popular Cities inventory verified from the homepage (issue #247)."""

VIATOR_CATEGORIES = [
    {"category": slug, "url": f"https://www.viator.com/{city}/d{destination_id}"}
    for slug, city, destination_id in (
        ("nashville", "Nashville", "799"),
        ("chicago", "Chicago", "673"),
        ("houston", "Houston", "5186"),
        ("san-diego", "San-Diego", "736"),
        ("atlanta", "Atlanta", "784"),
        ("denver", "Denver", "4837"),
        ("las-vegas", "Las-Vegas", "684"),
        ("miami", "Miami", "662"),
        ("orlando", "Orlando", "663"),
        ("dallas", "Dallas", "918"),
        ("new-orleans", "New-Orleans", "675"),
        ("san-antonio", "San-Antonio", "910"),
        ("san-francisco", "San-Francisco", "651"),
        ("seattle", "Seattle", "704"),
        ("austin", "Austin", "5021"),
        ("boston", "Boston", "678"),
        ("rome", "Rome", "511"),
        ("los-angeles", "Los-Angeles", "645"),
        ("myrtle-beach", "Myrtle-Beach", "5217"),
        ("philadelphia", "Philadelphia", "906"),
    )
]
