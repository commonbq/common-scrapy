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


FASHIONNOVA_CATEGORIES = _qualified(
    {
        "new": {"all": "https://www.fashionnova.com/collections/new"},
        "women": {"all": "https://www.fashionnova.com/collections/women"},
        "novadeals": {
            "all": "https://www.fashionnova.com/collections/womens-novadeals"
        },
        "halloween": {"all": "https://www.fashionnova.com/collections/halloween"},
        "jeans": {"all": "https://www.fashionnova.com/collections/jeans"},
        "dresses": {
            "all": "https://www.fashionnova.com/collections/dresses",
            "going-out": "https://www.fashionnova.com/collections/club-dresses",
            "birthday": "https://www.fashionnova.com/collections/birthday-dresses",
            "office": "https://www.fashionnova.com/collections/wear-to-work-dresses",
            "cocktail": "https://www.fashionnova.com/collections/cocktail-dresses",
            "fall": "https://www.fashionnova.com/collections/fall-dresses",
            "formal": "https://www.fashionnova.com/collections/formal-shop",
            "luxe": "https://www.fashionnova.com/collections/womens-nova-luxe-dresses",
            "deals": "https://www.fashionnova.com/collections/everyday-dresses",
        },
        "matching-sets": {
            "all": "https://www.fashionnova.com/collections/matching-sets"
        },
        "tops": {"all": "https://www.fashionnova.com/collections/all-tops"},
        "graphic-tops": {"all": "https://www.fashionnova.com/collections/graphic-tops"},
        "jackets-and-sweaters": {
            "all": "https://www.fashionnova.com/collections/jackets"
        },
        "shoes": {"all": "https://www.fashionnova.com/collections/shoes"},
        "formal": {"all": "https://www.fashionnova.com/collections/formal-shop"},
        "jumpsuits": {
            "all": "https://www.fashionnova.com/collections/rompers-and-jumpsuits"
        },
        "bottoms": {"all": "https://www.fashionnova.com/collections/bottoms"},
        "lingerie-and-sleep": {
            "all": "https://www.fashionnova.com/collections/lingerie"
        },
        "accessories": {"all": "https://www.fashionnova.com/collections/accessories"},
        "sale": {"all": "https://www.fashionnova.com/collections/sale"},
        "nova-luxe": {"all": "https://www.fashionnova.com/collections/luxe"},
    }
)
