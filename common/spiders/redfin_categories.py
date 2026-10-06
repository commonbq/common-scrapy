"""Popular Redfin city markets linked by the first-party homepage."""

REDFIN_CATEGORIES = [
    {"category": slug, "url": url}
    for slug, url in {
        "los-angeles-ca": "https://www.redfin.com/city/11203/CA/Los-Angeles",
        "new-york-ny": "https://www.redfin.com/city/30749/NY/New-York",
        "chicago-il": "https://www.redfin.com/city/29470/IL/Chicago",
        "houston-tx": "https://www.redfin.com/city/8903/TX/Houston",
        "phoenix-az": "https://www.redfin.com/city/14240/AZ/Phoenix",
        "philadelphia-pa": "https://www.redfin.com/city/15502/PA/Philadelphia",
        "san-antonio-tx": "https://www.redfin.com/city/16657/TX/San-Antonio",
        "san-diego-ca": "https://www.redfin.com/city/16904/CA/San-Diego",
        "dallas-tx": "https://www.redfin.com/city/30794/TX/Dallas",
        "jacksonville-fl": "https://www.redfin.com/city/8907/FL/Jacksonville",
        "austin-tx": "https://www.redfin.com/city/30818/TX/Austin",
        "fort-worth-tx": "https://www.redfin.com/city/30827/TX/Fort-Worth",
        "san-jose-ca": "https://www.redfin.com/city/17420/CA/San-Jose",
        "columbus-oh": "https://www.redfin.com/city/4664/OH/Columbus",
        "charlotte-nc": "https://www.redfin.com/city/3105/NC/Charlotte",
        "indianapolis-in": "https://www.redfin.com/city/9170/IN/Indianapolis",
        "san-francisco-ca": "https://www.redfin.com/city/17151/CA/San-Francisco",
        "seattle-wa": "https://www.redfin.com/city/16163/WA/Seattle",
        "denver-co": "https://www.redfin.com/city/5155/CO/Denver",
        "boston-ma": "https://www.redfin.com/city/1826/MA/Boston",
    }.items()
]
