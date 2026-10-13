from __future__ import annotations


def _qualified(
    groups: dict[str, dict[str, str]],
) -> dict[str, dict[str, dict[str, str]]]:
    return {
        group: {
            f"{group}-{leaf}": {"url": url, "subcategory": leaf}
            for leaf, url in leaves.items()
        }
        for group, leaves in groups.items()
    }


TARGET_CATEGORIES = _qualified(
    {
        "grocery": {
            "all": "https://www.target.com/c/grocery/-/N-5xt1a",
            "bakery-bread": "https://www.target.com/c/bakery-bread-grocery/-/N-5xt19",
            "beverages": "https://www.target.com/c/beverages-grocery/-/N-5xt0r",
            "breakfast-cereal": "https://www.target.com/c/breakfast-cereal-grocery/-/N-wo2mp",
            "candy": "https://www.target.com/c/candy-grocery/-/N-5xt0d",
            "coffee": "https://www.target.com/c/coffee-beverages-grocery/-/N-4yi5p",
            "dairy-eggs-cheese": "https://www.target.com/c/dairy-eggs-cheese-grocery/-/N-5xszm",
            "deli": "https://www.target.com/c/deli-grocery/-/N-5hp74",
            "fresh-meat-seafood": "https://www.target.com/c/fresh-meat-seafood-grocery/-/N-5xsyh",
            "frozen-foods": "https://www.target.com/c/frozen-foods-grocery/-/N-5xszd",
            "pantry": "https://www.target.com/c/pantry-grocery/-/N-5xt13",
            "produce": "https://www.target.com/c/produce-grocery/-/N-u7fty",
            "snacks": "https://www.target.com/c/snacks-grocery/-/N-5xsy9",
            "wine-beer-liquor": "https://www.target.com/c/wine-beer-liquor-beverages/-/N-5n5q6",
        },
        "women": {"all": "https://www.target.com/c/women/-/N-5xtd3"},
        "men": {"all": "https://www.target.com/c/men/-/N-18y1l"},
        "kids": {"all": "https://www.target.com/c/kids/-/N-xcoz4"},
        "baby": {"all": "https://www.target.com/c/baby/-/N-5xtly"},
        "home": {"all": "https://www.target.com/c/home/-/N-5xtvd"},
        "kitchen-dining": {"all": "https://www.target.com/c/kitchen-dining/-/N-hz89j"},
        "patio-garden": {"all": "https://www.target.com/c/patio-lawn-garden/-/N-5xtq9"},
        "beauty": {"all": "https://www.target.com/c/beauty/-/N-55r1x"},
        "personal-care": {"all": "https://www.target.com/c/personal-care/-/N-5xtzq"},
        "health": {"all": "https://www.target.com/c/health/-/N-5xu1n"},
        "household-essentials": {
            "all": "https://www.target.com/c/household-essentials/-/N-5xsz1"
        },
        "pets": {"all": "https://www.target.com/c/pets/-/N-5xt44"},
        "toys": {"all": "https://www.target.com/c/toys/-/N-5xtb0"},
        "electronics": {"all": "https://www.target.com/c/electronics/-/N-5xtg6"},
        "video-games": {"all": "https://www.target.com/c/video-games/-/N-5xtg5"},
        "sports-outdoors": {
            "all": "https://www.target.com/c/sports-outdoors/-/N-5xt85"
        },
        "school-office": {
            "all": "https://www.target.com/c/school-office-supplies/-/N-5xsxr"
        },
        "movies-music-books": {
            "all": "https://www.target.com/c/movies-music-books/-/N-5xsxe"
        },
        "gift-cards": {"all": "https://www.target.com/c/gift-cards/-/N-5xsxu"},
        "clearance": {"all": "https://www.target.com/c/clearance/-/N-5q0ga"},
    }
)
