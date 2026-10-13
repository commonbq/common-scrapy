from __future__ import annotations

import re


# Full category navigation captured from https://poshmark.com/ on 2026-10-12.
# Keep the site path spelling intact because Poshmark uses it as its route key.
_POSHMARK_CATEGORY_PATHS = {
    "women": (
        "Women",
        "Women-Accessories",
        "Women-Bags",
        "Women-Bath_&_Body",
        "Women-Dresses",
        "Women-Hair",
        "Women-Handbags",
        "Women-Intimates_&_Sleepwear",
        "Women-Jackets_&_Coats",
        "Women-Jeans",
        "Women-Jewelry",
        "Women-Makeup",
        "Women-Other",
        "Women-Pants_&_Jumpsuits",
        "Women-Shoes",
        "Women-Shorts",
        "Women-Skincare",
        "Women-Skirts",
        "Women-Sweaters",
        "Women-Swim",
        "Women-Tops",
    ),
    "men": (
        "Men",
        "Men-Accessories",
        "Men-Bags",
        "Men-Grooming",
        "Men-Jackets_&_Coats",
        "Men-Jeans",
        "Men-Other",
        "Men-Pants",
        "Men-Shirts",
        "Men-Shoes",
        "Men-Shorts",
        "Men-Suits_&_Blazers",
        "Men-Sweaters",
        "Men-Swim",
        "Men-Underwear_&_Socks",
    ),
    "kids": (
        "Kids",
        "Kids-Accessories",
        "Kids-Bath,_Skin_&_Hair",
        "Kids-Bottoms",
        "Kids-Costumes",
        "Kids-Dresses",
        "Kids-Jackets_&_Coats",
        "Kids-Matching_Sets",
        "Kids-One_Pieces",
        "Kids-Other",
        "Kids-Pajamas",
        "Kids-Shirts_&_Tops",
        "Kids-Shoes",
        "Kids-Swim",
        "Kids-Toys",
    ),
    "home": (
        "Home",
        "Home-Accents",
        "Home-Art",
        "Home-Bath",
        "Home-Bedding",
        "Home-Design",
        "Home-Dining",
        "Home-Games",
        "Home-Holiday",
        "Home-Kitchen",
        "Home-Office",
        "Home-Other",
        "Home-Party_Supplies",
        "Home-Storage_&_Organization",
        "Home-Wall_Decor",
    ),
    "electronics": (
        "Electronics",
        "Electronics-Cameras,_Photo_&_Video",
        "Electronics-Car_Audio,_Video_&_GPS",
        "Electronics-Cell_Phones_&_Accessories",
        "Electronics-Computers,_Laptops_&_Parts",
        "Electronics-Headphones",
        "Electronics-Media",
        "Electronics-Networking",
        "Electronics-Other",
        "Electronics-Portable_Audio_&_Video",
        "Electronics-Tablets_&_Accessories",
        "Electronics-VR,_AR_&_Accessories",
        "Electronics-Video_Games_&_Consoles",
        "Electronics-Wearables",
    ),
    "pets": (
        "Pets",
        "Pets-Bird",
        "Pets-Cat",
        "Pets-Cat-Toys",
        "Pets-Dog",
        "Pets-Dog-Clothing_&_Accessories",
        "Pets-Dog-Collars,_Leashes_&_Harnesses",
        "Pets-Fish",
        "Pets-Other",
        "Pets-Reptile",
        "Pets-Small_Pets",
    ),
}


def _category_slug(path: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.lower().replace("&", "and")).strip("-")


POSHMARK_CATEGORIES = {
    department: {
        _category_slug(path): f"https://poshmark.com/category/{path}"
        for path in paths
    }
    for department, paths in _POSHMARK_CATEGORY_PATHS.items()
}
