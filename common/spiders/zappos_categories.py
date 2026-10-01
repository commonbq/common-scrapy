"""Captured Zappos Department navigation inventory (2026-09-30)."""

ZAPPOS_CATEGORY_INVENTORY = {
    "Women": {
        "url": "https://www.zappos.com/women/wAEB4gIBGA.zso",
        "subcategories": {
            "Shoes": "https://www.zappos.com/women-shoes/CK_XAcABAeICAgEY.zso",
            "Clothing": "https://www.zappos.com/women-clothing/CKvXAcABAeICAgEY.zso",
            "Bags": "https://www.zappos.com/women-bags/COjWAcABAeICAgEY.zso",
            "Accessories": "https://www.zappos.com/women-accessories/COfWAcABAeICAgEY.zso",
            "Jewelry": "https://www.zappos.com/women-jewelry/CK7XAcABAeICAgEY.zso",
            "Sporting Goods": "https://www.zappos.com/women-sporting-goods/CLDXAcABAeICAgEY.zso",
            "Eyewear": "https://www.zappos.com/women-eyewear/CKzXAcABAeICAgEY.zso",
            "Home": "https://www.zappos.com/women-home/CK3XAcABAeICAgEY.zso",
            "Beauty": "https://www.zappos.com/women-beauty/CLPWAcABAeICAgEY.zso",
            "Watches": "https://www.zappos.com/women-watches/CLHXAcABAeICAgEY.zso",
            "Electronics": "https://www.zappos.com/women-electronics/CKjaAcABAeICAgEY.zso",
        },
    },
    "Men": {
        "url": "https://www.zappos.com/men/wAEC4gIBGA.zso",
        "subcategories": {
            "Shoes": "https://www.zappos.com/men-shoes/CK_XAcABAuICAgEY.zso",
            "Clothing": "https://www.zappos.com/men-clothing/CKvXAcABAuICAgEY.zso",
            "Accessories": "https://www.zappos.com/men-accessories/COfWAcABAuICAgEY.zso",
            "Bags": "https://www.zappos.com/men-bags/COjWAcABAuICAgEY.zso",
            "Sporting Goods": "https://www.zappos.com/men-sporting-goods/CLDXAcABAuICAgEY.zso",
            "Eyewear": "https://www.zappos.com/men-eyewear/CKzXAcABAuICAgEY.zso",
            "Home": "https://www.zappos.com/men-home/CK3XAcABAuICAgEY.zso",
            "Watches": "https://www.zappos.com/men-watches/CLHXAcABAuICAgEY.zso",
            "Beauty": "https://www.zappos.com/men-beauty/CLPWAcABAuICAgEY.zso",
            "Electronics": "https://www.zappos.com/men-electronics/CKjaAcABAuICAgEY.zso",
            "Jewelry": "https://www.zappos.com/men-jewelry/CK7XAcABAuICAgEY.zso",
        },
    },
    "Girls": {
        "url": "https://www.zappos.com/girls/wAED4gIBGA.zso",
        "subcategories": {
            "Shoes": "https://www.zappos.com/girls-shoes/CK_XAcABA-ICAgEY.zso",
            "Clothing": "https://www.zappos.com/girls-clothing/CKvXAcABA-ICAgEY.zso",
            "Bags": "https://www.zappos.com/girls-bags/COjWAcABA-ICAgEY.zso",
            "Accessories": "https://www.zappos.com/girls-accessories/COfWAcABA-ICAgEY.zso",
            "Home": "https://www.zappos.com/girls-home/CK3XAcABA-ICAgEY.zso",
            "Baby Essentials": "https://www.zappos.com/girls-baby-essentials/CITaAcABA-ICAgEY.zso",
            "Sporting Goods": "https://www.zappos.com/girls-sporting-goods/CLDXAcABA-ICAgEY.zso",
            "Eyewear": "https://www.zappos.com/girls-eyewear/CKzXAcABA-ICAgEY.zso",
            "Toys and Games": "https://www.zappos.com/girls-toys-and-games/CKjYAcABA-ICAgEY.zso",
            "Watches": "https://www.zappos.com/girls-watches/CLHXAcABA-ICAgEY.zso",
            "Beauty": "https://www.zappos.com/girls-beauty/CLPWAcABA-ICAgEY.zso",
            "Electronics": "https://www.zappos.com/girls-electronics/CKjaAcABA-ICAgEY.zso",
        },
    },
    "Boys": {
        "url": "https://www.zappos.com/boys/wAEE4gIBGA.zso",
        "subcategories": {
            "Shoes": "https://www.zappos.com/boys-shoes/CK_XAcABBOICAgEY.zso",
            "Clothing": "https://www.zappos.com/boys-clothing/CKvXAcABBOICAgEY.zso",
            "Accessories": "https://www.zappos.com/boys-accessories/COfWAcABBOICAgEY.zso",
            "Bags": "https://www.zappos.com/boys-bags/COjWAcABBOICAgEY.zso",
            "Home": "https://www.zappos.com/boys-home/CK3XAcABBOICAgEY.zso",
            "Baby Essentials": "https://www.zappos.com/boys-baby-essentials/CITaAcABBOICAgEY.zso",
            "Sporting Goods": "https://www.zappos.com/boys-sporting-goods/CLDXAcABBOICAgEY.zso",
            "Toys and Games": "https://www.zappos.com/boys-toys-and-games/CKjYAcABBOICAgEY.zso",
            "Eyewear": "https://www.zappos.com/boys-eyewear/CKzXAcABBOICAgEY.zso",
            "Watches": "https://www.zappos.com/boys-watches/CLHXAcABBOICAgEY.zso",
            "Beauty": "https://www.zappos.com/boys-beauty/CLPWAcABBOICAgEY.zso",
            "Electronics": "https://www.zappos.com/boys-electronics/CKjaAcABBOICAgEY.zso",
        },
    },
}


def _slug(value: str) -> str:
    return value.lower().replace(" ", "-")


ZAPPOS_CATEGORIES = []
for department, group in ZAPPOS_CATEGORY_INVENTORY.items():
    ZAPPOS_CATEGORIES.append({"category": _slug(department), "department": department, "url": group["url"]})
    ZAPPOS_CATEGORIES.extend(
        {
            "category": f"{_slug(department)}-{_slug(name)}",
            "department": department,
            "url": url,
        }
        for name, url in group["subcategories"].items()
    )
