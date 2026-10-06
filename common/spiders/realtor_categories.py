"""Bounded major-city taxonomy for Realtor.com listings."""

REALTOR_CATEGORIES = {
    "los-angeles-ca": "https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA",
    "new-york-ny": "https://www.realtor.com/realestateandhomes-search/New-York_NY",
    "chicago-il": "https://www.realtor.com/realestateandhomes-search/Chicago_IL",
    "houston-tx": "https://www.realtor.com/realestateandhomes-search/Houston_TX",
    "phoenix-az": "https://www.realtor.com/realestateandhomes-search/Phoenix_AZ",
    "philadelphia-pa": "https://www.realtor.com/realestateandhomes-search/Philadelphia_PA",
    "san-antonio-tx": "https://www.realtor.com/realestateandhomes-search/San-Antonio_TX",
    "san-diego-ca": "https://www.realtor.com/realestateandhomes-search/San-Diego_CA",
    "dallas-tx": "https://www.realtor.com/realestateandhomes-search/Dallas_TX",
    "jacksonville-fl": "https://www.realtor.com/realestateandhomes-search/Jacksonville_FL",
    "austin-tx": "https://www.realtor.com/realestateandhomes-search/Austin_TX",
    "fort-worth-tx": "https://www.realtor.com/realestateandhomes-search/Fort-Worth_TX",
    "san-jose-ca": "https://www.realtor.com/realestateandhomes-search/San-Jose_CA",
    "columbus-oh": "https://www.realtor.com/realestateandhomes-search/Columbus_OH",
    "charlotte-nc": "https://www.realtor.com/realestateandhomes-search/Charlotte_NC",
    "indianapolis-in": "https://www.realtor.com/realestateandhomes-search/Indianapolis_IN",
    "san-francisco-ca": "https://www.realtor.com/realestateandhomes-search/San-Francisco_CA",
    "seattle-wa": "https://www.realtor.com/realestateandhomes-search/Seattle_WA",
    "denver-co": "https://www.realtor.com/realestateandhomes-search/Denver_CO",
    "boston-ma": "https://www.realtor.com/realestateandhomes-search/Boston_MA",
}

CATEGORIES = [{"category": key, "url": url} for key, url in REALTOR_CATEGORIES.items()]
