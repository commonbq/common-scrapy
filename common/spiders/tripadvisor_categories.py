"""Tripadvisor 2026 Travelers' Choice top destinations, grouped by region."""

TRIPADVISOR_CATEGORIES = {
    "asia": {
        "bali": {
            "url": "https://www.tripadvisor.com/Hotels-g294226-Bali-Hotels.html",
            "country": "Indonesia",
            "rank": 1,
        },
        "dubai": {
            "url": "https://www.tripadvisor.com/Hotels-g295424-Dubai_Emirate_of_Dubai-Hotels.html",
            "country": "United Arab Emirates",
            "rank": 3,
        },
        "hanoi": {
            "url": "https://www.tripadvisor.com/Hotels-g293924-Hanoi-Hotels.html",
            "country": "Vietnam",
            "rank": 4,
        },
        "bangkok": {
            "url": "https://www.tripadvisor.com/Hotels-g293916-Bangkok-Hotels.html",
            "country": "Thailand",
            "rank": 8,
        },
        "siem-reap": {
            "url": "https://www.tripadvisor.com/Hotels-g297390-Siem_Reap_Siem_Reap_Province-Hotels.html",
            "country": "Cambodia",
            "rank": 11,
        },
        "istanbul": {
            "url": "https://www.tripadvisor.com/Hotels-g293974-Istanbul-Hotels.html",
            "country": "Turkey",
            "rank": 12,
        },
        "tokyo": {
            "url": "https://www.tripadvisor.com/Hotels-g298184-Tokyo_Tokyo_Prefecture_Kanto-Hotels.html",
            "country": "Japan",
            "rank": 16,
        },
        "kathmandu": {
            "url": "https://www.tripadvisor.com/Hotels-g293890-Kathmandu_Kathmandu_Valley_Bagmati_Zone_Central_Region-Hotels.html",
            "country": "Nepal",
            "rank": 17,
        },
        "maldives": {
            "url": "https://www.tripadvisor.com/Hotels-g293953-Maldives-Hotels.html",
            "country": "Maldives",
            "rank": 21,
        },
        "new-delhi": {
            "url": "https://www.tripadvisor.com/Hotels-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Hotels.html",
            "country": "India",
            "rank": 22,
        },
        "seoul": {
            "url": "https://www.tripadvisor.com/Hotels-g294197-Seoul-Hotels.html",
            "country": "South Korea",
            "rank": 24,
        },
        "abu-dhabi": {
            "url": "https://www.tripadvisor.com/Hotels-g294013-Abu_Dhabi_Emirate_of_Abu_Dhabi-Hotels.html",
            "country": "United Arab Emirates",
            "rank": 25,
        },
    },
    "europe": {
        "london": {
            "url": "https://www.tripadvisor.com/Hotels-g186338-London_England-Hotels.html",
            "country": "United Kingdom",
            "rank": 2,
        },
        "paris": {
            "url": "https://www.tripadvisor.com/Hotels-g187147-Paris_Ile_de_France-Hotels.html",
            "country": "France",
            "rank": 5,
        },
        "rome": {
            "url": "https://www.tripadvisor.com/Hotels-g187791-Rome_Lazio-Hotels.html",
            "country": "Italy",
            "rank": 6,
        },
        "crete": {
            "url": "https://www.tripadvisor.com/Hotels-g189413-Crete-Hotels.html",
            "country": "Greece",
            "rank": 9,
        },
        "barcelona": {
            "url": "https://www.tripadvisor.com/Hotels-g187497-Barcelona_Catalonia-Hotels.html",
            "country": "Spain",
            "rank": 14,
        },
        "lisbon": {
            "url": "https://www.tripadvisor.com/Hotels-g189158-Lisbon_Lisbon_District_Central_Portugal-Hotels.html",
            "country": "Portugal",
            "rank": 15,
        },
        "edinburgh": {
            "url": "https://www.tripadvisor.com/Hotels-g186525-Edinburgh_Scotland-Hotels.html",
            "country": "United Kingdom",
            "rank": 18,
        },
        "budapest": {
            "url": "https://www.tripadvisor.com/Hotels-g274887-Budapest_Central_Hungary-Hotels.html",
            "country": "Hungary",
            "rank": 23,
        },
    },
    "africa": {
        "marrakech": {
            "url": "https://www.tripadvisor.com/Hotels-g293734-Marrakech_Marrakech_Safi-Hotels.html",
            "country": "Morocco",
            "rank": 7,
        },
        "hurghada": {
            "url": "https://www.tripadvisor.com/Hotels-g297549-Hurghada_Red_Sea_and_Sinai-Hotels.html",
            "country": "Egypt",
            "rank": 19,
        },
    },
    "north-america": {
        "new-york-city": {
            "url": "https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html",
            "country": "United States",
            "rank": 10,
        },
        "cabo-san-lucas": {
            "url": "https://www.tripadvisor.com/Hotels-g152515-Cabo_San_Lucas_Los_Cabos_Baja_California-Hotels.html",
            "country": "Mexico",
            "rank": 20,
        },
    },
    "south-america": {
        "cusco": {
            "url": "https://www.tripadvisor.com/Hotels-g294314-Cusco_Cusco_Region-Hotels.html",
            "country": "Peru",
            "rank": 13,
        },
    },
}
