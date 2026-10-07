from __future__ import annotations


# Hostelworld's catalogue taxonomy is continent/country/city. Each city also
# has a numeric city_id, recorded separately below, which the paging API needs.
HOSTELWORLD_CATEGORIES = {
    "london": "https://www.hostelworld.com/hostels/europe/england/london/",
    "paris": "https://www.hostelworld.com/hostels/europe/france/paris/",
    "barcelona": "https://www.hostelworld.com/hostels/europe/spain/barcelona/",
    "rome": "https://www.hostelworld.com/hostels/europe/italy/rome/",
    "amsterdam": "https://www.hostelworld.com/hostels/europe/netherlands/amsterdam/",
    "berlin": "https://www.hostelworld.com/hostels/europe/germany/berlin/",
    "madrid": "https://www.hostelworld.com/hostels/europe/spain/madrid/",
    "prague": "https://www.hostelworld.com/hostels/europe/czech-republic/prague/",
    "lisbon": "https://www.hostelworld.com/hostels/europe/portugal/lisbon/",
    "dublin": "https://www.hostelworld.com/hostels/europe/ireland/dublin/",
    "vienna": "https://www.hostelworld.com/hostels/europe/austria/vienna/",
    "budapest": "https://www.hostelworld.com/hostels/europe/hungary/budapest/",
    "milan": "https://www.hostelworld.com/hostels/europe/italy/milan/",
    "venice": "https://www.hostelworld.com/hostels/europe/italy/venice/",
    "edinburgh": "https://www.hostelworld.com/hostels/europe/scotland/edinburgh/",
    "copenhagen": "https://www.hostelworld.com/hostels/europe/denmark/copenhagen/",
    "krakow": "https://www.hostelworld.com/hostels/europe/poland/krakow/",
    "athens": "https://www.hostelworld.com/hostels/europe/greece/athens/",
    "new-york": "https://www.hostelworld.com/hostels/north-america/usa/new-york/",
    "bangkok": "https://www.hostelworld.com/hostels/asia/thailand/bangkok/",
}

HOSTELWORLD_CITY_IDS = {
    "london": 3, "paris": 14, "barcelona": 83, "rome": 36,
    "amsterdam": 15, "berlin": 26, "madrid": 117, "prague": 19,
    "lisbon": 725, "dublin": 5, "vienna": 38, "budapest": 50,
    "milan": 649, "venice": 68, "edinburgh": 22, "copenhagen": 48,
    "krakow": 285, "athens": 588, "new-york": 13, "bangkok": 149,
}

HostelworldCategory = dict[str, str | int]

HOSTELWORLD_CATEGORY_LIST: list[HostelworldCategory] = [
    {"category": slug, "url": url, "city_id": HOSTELWORLD_CITY_IDS[slug]}
    for slug, url in HOSTELWORLD_CATEGORIES.items()
]
