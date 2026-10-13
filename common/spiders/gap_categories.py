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


GAP_CATEGORIES = _qualified(
    {
        "women": {
            "dresses": "https://www.gap.com/browse/category.do?cid=13658",
            "new-arrivals": "https://www.gap.com/browse/category.do?cid=8792",
            "jeans": "https://www.gap.com/browse/category.do?cid=5664",
            "tops": "https://www.gap.com/browse/category.do?cid=17076",
            "pants": "https://www.gap.com/browse/category.do?cid=5736",
            "sweaters": "https://www.gap.com/browse/category.do?cid=5745",
        },
        "men": {
            "all": "https://www.gap.com/browse/category.do?cid=6998",
            "new-arrivals": "https://www.gap.com/browse/category.do?cid=1127938",
            "jeans": "https://www.gap.com/browse/category.do?cid=34524",
            "pants": "https://www.gap.com/browse/category.do?cid=34608",
        },
        "girls": {"all": "https://www.gap.com/browse/category.do?cid=14257"},
    }
)
