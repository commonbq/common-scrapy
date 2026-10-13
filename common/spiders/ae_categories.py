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


AE_CATEGORIES = _qualified(
    {
        "women": {
            "all": "https://www.ae.com/us/en/c/women/womens",
            "jeans": "https://www.ae.com/us/en/c/women/bottoms/jeans/cat6430042",
            "tops": "https://www.ae.com/us/en/c/women/tops/cat10049",
            "bottoms": "https://www.ae.com/us/en/c/women/bottoms/cat10051",
            "pants-sweatpants": "https://www.ae.com/us/en/c/women/bottoms/pants-sweatpants/cat90034",
            "t-shirts": "https://www.ae.com/us/en/c/women/tops/t-shirts/cat90030",
            "hoodies-sweatshirts": "https://www.ae.com/us/en/c/women/tops/hoodies-sweatshirts/cat90048",
            "sweaters-cardigans": "https://www.ae.com/us/en/c/women/tops/sweaters-cardigans/cat1410002",
            "dresses-jumpsuits": "https://www.ae.com/us/en/c/women/dresses/cat1320034",
            "loungewear-pjs": "https://www.ae.com/us/en/c/women/loungewear-pjs/cat730011",
            "jackets-vests": "https://www.ae.com/us/en/c/women/tops/jackets-vests/cat4260032",
            "accessories-socks": "https://www.ae.com/us/en/c/women/accessories-socks/cat4840018",
            "shoes": "https://www.ae.com/us/en/c/women/shoes/cat4840020",
            "clearance": "https://www.ae.com/us/en/c/women/clearance/clrwomens",
        },
        "men": {
            "all": "https://www.ae.com/us/en/c/men/mens",
            "jeans": "https://www.ae.com/us/en/c/men/bottoms/jeans/cat6430041",
            "tops": "https://www.ae.com/us/en/c/men/tops/cat10025",
            "bottoms": "https://www.ae.com/us/en/c/men/bottoms/cat10027",
            "hoodies-sweatshirts": "https://www.ae.com/us/en/c/men/tops/hoodies-sweatshirts/cat90020",
            "t-shirts": "https://www.ae.com/us/en/c/men/tops/t-shirts/cat90012",
            "shirts-flannels": "https://www.ae.com/us/en/c/men/tops/shirts-flannels/cat40005",
            "underwear": "https://www.ae.com/us/en/c/men/underwear/cat10032",
            "activewear": "https://www.ae.com/us/en/c/men/activewear/cat1100008",
            "loungewear-pjs": "https://www.ae.com/us/en/c/men/loungewear-pjs/cat130005",
            "jackets": "https://www.ae.com/us/en/c/men/tops/jackets-vests/cat380145",
            "accessories-socks": "https://www.ae.com/us/en/c/men/accessories-socks/cat4840022",
            "shoes": "https://www.ae.com/us/en/c/men/shoes/cat4840024",
            "clearance": "https://www.ae.com/us/en/c/men/clearance/clrmens",
        },
        "aerie": {
            "all": "https://www.ae.com/us/en/c/aerie/clothing-accessories/cat870009"
        },
    }
)
