"""adidas.com US category inventory captured from the HTML sitemap.

Source: https://www.adidas.com/glass/sitemaps/adidas/US/en/html-sitemap/index.html
Captured: 2026-10-02 (US / en).

The sitemap renders one `<h*>` heading per browse section followed by the
section's `/us/...` anchors. Section labels with no direct link (`Shoes`,
`Clothing`, `Accessories`) and the non-catalog buckets (`Help`, `Resources`,
`About Us`, `All Countries & Regions`) are omitted, so every entry below is a
real, crawlable category URL.
"""

from __future__ import annotations

import re


ADIDAS_CATEGORY_SECTIONS: dict[str, list[dict[str, str]]] = {
    "Sales & Promotions": [
        {"name": "Top Deal", "url": "https://www.adidas.com/us/top_deal"},
        {"name": "Basketball Shoes Under $100", "url": "https://www.adidas.com/us/under_100-shoes"},
    ],
    "MEN'S SALE": [
        {"name": "Men's Shoes on Sale", "url": "https://www.adidas.com/us/men-shoes-sale"},
        {"name": "Men's Clothing on Sale", "url": "https://www.adidas.com/us/men-clothing-sale"},
        {"name": "Men's Accessories on Sale", "url": "https://www.adidas.com/us/men-accessories-sale"},
    ],
    "WOMEN'S SALE": [
        {"name": "Women's Shoes on Sale", "url": "https://www.adidas.com/us/women-shoes-sale"},
        {"name": "Women's Clothing on Sale", "url": "https://www.adidas.com/us/women-clothing-sale"},
        {"name": "Women's Accessories on Sale", "url": "https://www.adidas.com/us/women-accessories-sale"},
    ],
    "KIDS SALE": [
        {"name": "Boys' Shoes On Sale", "url": "https://www.adidas.com/us/boys-shoes-sale"},
        {"name": "Boys' Clothing on Sale", "url": "https://www.adidas.com/us/boys-clothing-sale"},
        {"name": "Boys' Accessories on Sale", "url": "https://www.adidas.com/us/boys-accessories-sale"},
        {"name": "Girls' Shoes On Sale", "url": "https://www.adidas.com/us/girls-shoes-sale"},
        {"name": "Girls' Clothing on Sale", "url": "https://www.adidas.com/us/girls-clothing-sale"},
        {"name": "Girls' Accessories on Sale", "url": "https://www.adidas.com/us/girls-accessories-sale"},
    ],
    "Holiday & Seasonal": [
        {"name": "Back To School", "url": "https://www.adidas.com/us/back_to_school"},
        {"name": "Back To Campus", "url": "https://www.adidas.com/us/back_to_school-campus"},
        {"name": "Cozy Deals", "url": "https://www.adidas.com/us/cozy_deals"},
        {"name": "Halloween", "url": "https://www.adidas.com/us/halloween"},
        {"name": "Black Friday", "url": "https://www.adidas.com/us/black_friday"},
        {"name": "Cyber Monday", "url": "https://www.adidas.com/us/cyber_monday"},
        {"name": "Valentine's Day", "url": "https://www.adidas.com/us/valentines_day"},
        {"name": "Mother's Day", "url": "https://www.adidas.com/us/mothers_day_gifts"},
        {"name": "Father's Day", "url": "https://www.adidas.com/us/fathers_day_gifts"},
        {"name": "Pride Collection", "url": "https://www.adidas.com/us/pride"},
    ],
    "New & Trending": [
        {"name": "New Arrivals", "url": "https://www.adidas.com/us/new_arrivals"},
        {"name": "Best Sellers", "url": "https://www.adidas.com/us/best_sellers"},
        {"name": "Trending Products", "url": "https://www.adidas.com/us/trending"},
    ],
    "MEN": [
        {"name": "New Men's Shoes", "url": "https://www.adidas.com/us/men-shoes-new_arrivals"},
        {"name": "New Men's Clothing", "url": "https://www.adidas.com/us/men-clothing-new_arrivals"},
        {"name": "New Men's Accessories", "url": "https://www.adidas.com/us/men-accessories-new_arrivals"},
    ],
    "WOMEN": [
        {"name": "New Women's Shoes", "url": "https://www.adidas.com/us/women-shoes-new_arrivals"},
        {"name": "New Women's Clothing", "url": "https://www.adidas.com/us/women-clothing-new_arrivals"},
        {"name": "New Women's Accessories", "url": "https://www.adidas.com/us/women-accessories-new_arrivals"},
    ],
    "KIDS": [
        {"name": "New Kids' Shoes", "url": "https://www.adidas.com/us/kids-shoes-new_arrivals"},
        {"name": "New Kids' Clothing", "url": "https://www.adidas.com/us/kids-clothing-new_arrivals"},
        {"name": "New Kids' Accessories", "url": "https://www.adidas.com/us/kids-accessories-new_arrivals"},
        {"name": "Upcoming Releases", "url": "https://www.adidas.com/us/release-dates"},
    ],
    "COLLECTIONS": [
        {"name": "Samba", "url": "https://www.adidas.com/us/samba"},
        {"name": "Gazelle", "url": "https://www.adidas.com/us/gazelle"},
        {"name": "Spezial", "url": "https://www.adidas.com/us/spezial"},
        {"name": "Ultraboost", "url": "https://www.adidas.com/us/ultraboost"},
        {"name": "Predator", "url": "https://www.adidas.com/us/predator"},
        {"name": "Copa", "url": "https://www.adidas.com/us/copa"},
        {"name": "F50", "url": "https://www.adidas.com/us/f50"},
        {"name": "Five Ten", "url": "https://www.adidas.com/us/five_ten"},
        {"name": "Supernova", "url": "https://www.adidas.com/us/supernova"},
        {"name": "TERREX", "url": "https://www.adidas.com/us/terrex"},
        {"name": "Tiro", "url": "https://www.adidas.com/us/tiro"},
        {"name": "Adizero Primeknit Cleats", "url": "https://www.adidas.com/us/adizero"},
    ],
    "MEN'S SHOES": [
        {"name": "Men's Athletic Sneakers", "url": "https://www.adidas.com/us/men-athletic_sneakers"},
        {"name": "Men's Running Shoes", "url": "https://www.adidas.com/us/men-running-shoes"},
        {"name": "Men's Soccer Cleats", "url": "https://www.adidas.com/us/men-soccer-shoes"},
        {"name": "Men's Walking Shoes", "url": "https://www.adidas.com/us/men-walking-shoes"},
        {"name": "Men's Soccer Slides", "url": "https://www.adidas.com/us/men-slides"},
        {"name": "Men's Trail Running Shoes", "url": "https://www.adidas.com/us/men-trail_running-shoes"},
        {"name": "Men's Workout Shoes", "url": "https://www.adidas.com/us/men-workout-shoes"},
        {"name": "Men's Shoes Under $100", "url": "https://www.adidas.com/us/men-under_100-shoes"},
        {"name": "Men's Basketball Shoes", "url": "https://www.adidas.com/us/men-basketball-shoes"},
        {"name": "Men's Golf Shoes", "url": "https://www.adidas.com/us/men-golf-shoes"},
        {"name": "Men's Football Cleats", "url": "https://www.adidas.com/us/men-football-cleats"},
    ],
    "WOMEN'S SHOES": [
        {"name": "Women's Athletic Shoes", "url": "https://www.adidas.com/us/women-athletic_sneakers"},
        {"name": "Women's Running Shoes", "url": "https://www.adidas.com/us/women-running-shoes"},
        {"name": "Women's Slides", "url": "https://www.adidas.com/us/women-slides"},
        {"name": "Women's Walking Shoes", "url": "https://www.adidas.com/us/women-walking-shoes"},
        {"name": "Women's Workout Shoes", "url": "https://www.adidas.com/us/women-workout-shoes"},
        {"name": "Women's Trail Running Shoes", "url": "https://www.adidas.com/us/women-trail_running-shoes"},
        {"name": "Women's Shoes Under $100", "url": "https://www.adidas.com/us/women-under_100-shoes"},
        {"name": "Women's Platform Shoes", "url": "https://www.adidas.com/us/women-platform"},
        {"name": "Women's Soccer Cleats", "url": "https://www.adidas.com/us/women-soccer-shoes"},
        {"name": "Women's Tennis Shoes", "url": "https://www.adidas.com/us/women-tennis-shoes"},
        {"name": "Women's Basketball Shoes", "url": "https://www.adidas.com/us/women-basketball-shoes"},
        {"name": "Women's Golf Shoes", "url": "https://www.adidas.com/us/women-golf-shoes"},
    ],
    "BOYS' SHOES": [
        {"name": "Boys' Athletic Sneakers", "url": "https://www.adidas.com/us/boys-athletic_sneakers"},
        {"name": "Boys' Soccer Shoes", "url": "https://www.adidas.com/us/boys-soccer-shoes"},
        {"name": "Boys' Slides", "url": "https://www.adidas.com/us/boys-slides"},
        {"name": "Boys' Hook and Loop Shoes", "url": "https://www.adidas.com/us/boys-hook_loop-shoes"},
        {"name": "Boys' Running Shoes", "url": "https://www.adidas.com/us/boys-running-shoes"},
        {"name": "Boys' Basketball Shoes", "url": "https://www.adidas.com/us/boys-basketball-shoes"},
    ],
    "GIRLS' SHOES": [
        {"name": "Girls' Athletic Sneakers", "url": "https://www.adidas.com/us/girls-athletic_sneakers"},
        {"name": "Girls' Soccer Shoes", "url": "https://www.adidas.com/us/girls-soccer-shoes"},
        {"name": "Girls' Slides", "url": "https://www.adidas.com/us/girls-slides"},
        {"name": "Girls 'Hook and Loop Shoes", "url": "https://www.adidas.com/us/girls-hook_loop-shoes"},
        {"name": "Girls' Running Shoes", "url": "https://www.adidas.com/us/girls-running-shoes"},
        {"name": "Girls' Basketball Shoes", "url": "https://www.adidas.com/us/girls-basketball-shoes"},
    ],
    "MEN'S CLOTHING": [
        {"name": "Men's Gym Shorts", "url": "https://www.adidas.com/us/men-shorts"},
        {"name": "Men's Hoodies", "url": "https://www.adidas.com/us/men-hoodies_sweatshirts"},
        {"name": "Men's Swimwear", "url": "https://www.adidas.com/us/men-swimwear"},
        {"name": "Men's Pants", "url": "https://www.adidas.com/us/men-pants"},
        {"name": "Men's Jackets", "url": "https://www.adidas.com/us/men-jackets"},
        {"name": "Men's Track Suits", "url": "https://www.adidas.com/us/men-track_suits"},
        {"name": "Men's Matching Sets", "url": "https://www.adidas.com/us/men-matching_sets"},
        {"name": "Men's Jerseys", "url": "https://www.adidas.com/us/men-jerseys"},
    ],
    "WOMEN'S CLOTHING": [
        {"name": "Women's Shorts", "url": "https://www.adidas.com/us/women-shorts"},
        {"name": "Women's Skirts and Dresses", "url": "https://www.adidas.com/us/women-skirts_dresses"},
        {"name": "Women's Plus Size Clothes & Shoes", "url": "https://www.adidas.com/us/women-plus_size"},
        {"name": "Women's Tights and Leggings", "url": "https://www.adidas.com/us/women-tights_leggings"},
        {"name": "Women's Hoodies", "url": "https://www.adidas.com/us/women-hoodies_sweatshirts"},
        {"name": "Women's Swimwear", "url": "https://www.adidas.com/us/women-swimwear"},
        {"name": "Women's Pants", "url": "https://www.adidas.com/us/women-pants"},
        {"name": "Women's Sports Bras", "url": "https://www.adidas.com/us/women-sports_bras"},
        {"name": "Women's Jackets", "url": "https://www.adidas.com/us/women-jackets"},
        {"name": "Women's Track Suits", "url": "https://www.adidas.com/us/women-track_suits"},
        {"name": "Women's Matching Sets", "url": "https://www.adidas.com/us/women-matching_sets"},
    ],
    "BOYS' CLOTHING": [
        {"name": "Boys' Shorts", "url": "https://www.adidas.com/us/boys-shorts"},
        {"name": "Boys' Sweatshirts", "url": "https://www.adidas.com/us/boys-hoodies_sweatshirts"},
        {"name": "Boys' Pants", "url": "https://www.adidas.com/us/boys-pants"},
        {"name": "Boys' Jackets", "url": "https://www.adidas.com/us/boys-jackets"},
        {"name": "Boys' Tracksuits", "url": "https://www.adidas.com/us/boys-track_suits"},
        {"name": "Boys' Matching Sets", "url": "https://www.adidas.com/us/boys-matching_sets"},
    ],
    "GIRLS' CLOTHING": [
        {"name": "Girls' Shorts", "url": "https://www.adidas.com/us/girls-shorts"},
        {"name": "Girls' Hoodies & Sweatshirts", "url": "https://www.adidas.com/us/girls-hoodies_sweatshirts"},
        {"name": "Girls' Pants", "url": "https://www.adidas.com/us/girls-pants"},
        {"name": "Girls' Jackets", "url": "https://www.adidas.com/us/girls-jackets"},
        {"name": "Girls' Tights and Leggings", "url": "https://www.adidas.com/us/girls-tights_leggings"},
        {"name": "Girls' Matching Sets", "url": "https://www.adidas.com/us/girls-matching_sets"},
        {"name": "Girls' Track Suits", "url": "https://www.adidas.com/us/girls-track_suits"},
    ],
    "MEN'S ACCESSORIES": [
        {"name": "Men's Bags", "url": "https://www.adidas.com/us/men-bags"},
        {"name": "Men's Soccer Balls", "url": "https://www.adidas.com/us/men-soccer-balls"},
        {"name": "Men's Basketballs", "url": "https://www.adidas.com/us/men-basketball-balls"},
        {"name": "Men's Gloves for Sports", "url": "https://www.adidas.com/us/men-gloves"},
        {"name": "Men's Hats", "url": "https://www.adidas.com/us/men-hats"},
        {"name": "Men's Socks", "url": "https://www.adidas.com/us/men-socks"},
        {"name": "Men's Underwear", "url": "https://www.adidas.com/us/men-underwear"},
    ],
    "WOMEN'S ACCESSORIES": [
        {"name": "Women's Bags", "url": "https://www.adidas.com/us/women-bags"},
        {"name": "Women's Soccer Balls", "url": "https://www.adidas.com/us/women-soccer-balls"},
        {"name": "Women's Sport Gloves", "url": "https://www.adidas.com/us/women-gloves"},
        {"name": "Women's Hats", "url": "https://www.adidas.com/us/women-hats"},
        {"name": "Women's Socks", "url": "https://www.adidas.com/us/women-socks"},
    ],
    "KIDS' ACCESSORIES": [
        {"name": "Kids' Backpacks", "url": "https://www.adidas.com/us/kids-backpacks"},
        {"name": "Kids' Hats", "url": "https://www.adidas.com/us/kids-hats"},
        {"name": "Kids' Socks", "url": "https://www.adidas.com/us/kids-socks"},
    ],
    "OTHER ACCESSORIES": [
        {"name": "Socks", "url": "https://www.adidas.com/us/socks"},
        {"name": "Gloves", "url": "https://www.adidas.com/us/gloves"},
        {"name": "Bags", "url": "https://www.adidas.com/us/bags"},
        {"name": "Hats", "url": "https://www.adidas.com/us/hats"},
        {"name": "Backpacks", "url": "https://www.adidas.com/us/backpacks"},
        {"name": "Water Bottles", "url": "https://www.adidas.com/us/water_bottles"},
    ],
    "Soccer": [
        {"name": "Men's Soccer Jerseys", "url": "https://www.adidas.com/us/men-soccer-jerseys"},
        {"name": "Soccer Balls", "url": "https://www.adidas.com/us/soccer-balls"},
        {"name": "Kids' Soccer Cleats & Shoes", "url": "https://www.adidas.com/us/kids-soccer-shoes"},
        {"name": "Soccer Shoes", "url": "https://www.adidas.com/us/soccer-shoes"},
        {"name": "Goalkeeper Gloves", "url": "https://www.adidas.com/us/soccer-gloves"},
        {"name": "Custom Soccer Jerseys", "url": "https://www.adidas.com/us/soccer-jerseys-personalisable"},
        {"name": "Replica Soccer Jerseys", "url": "https://www.adidas.com/us/soccer-jerseys"},
        {"name": "Kids' Soccer Jerseys", "url": "https://www.adidas.com/us/kids-soccer-jerseys"},
        {"name": "Soccer Bags", "url": "https://www.adidas.com/us/soccer-bags"},
        {"name": "Soccer Socks", "url": "https://www.adidas.com/us/soccer-socks"},
        {"name": "Men's Soccer Cleats Sale", "url": "https://www.adidas.com/us/men-soccer-shoes-sale"},
        {"name": "Soccer Outfits", "url": "https://www.adidas.com/us/soccer-clothing"},
        {"name": "Women's Soccer Shorts", "url": "https://www.adidas.com/us/women-soccer-shorts"},
        {"name": "Youth Turf Soccer Shoes", "url": "https://www.adidas.com/us/kids-soccer-shoes-turf"},
        {"name": "Men's Soccer Shorts", "url": "https://www.adidas.com/us/men-soccer-shorts"},
        {"name": "Leo Messi Soccer Shoes & Cleats", "url": "https://www.adidas.com/us/lionel_messi-soccer-shoes"},
        {"name": "Men's Soccer Pants", "url": "https://www.adidas.com/us/men-soccer-pants"},
        {"name": "Soccer Shorts", "url": "https://www.adidas.com/us/soccer-shorts"},
        {"name": "Soccer Jerseys Sale", "url": "https://www.adidas.com/us/men-soccer-jerseys-sale"},
        {"name": "Samba Soccer Shoes", "url": "https://www.adidas.com/us/samba-soccer-shoes"},
        {"name": "Men's Artificial Grass Soccer Cleats", "url": "https://www.adidas.com/us/men-soccer-shoes-artificial_grass"},
        {"name": "Kids' Soccer Shorts", "url": "https://www.adidas.com/us/kids-soccer-shorts"},
        {"name": "Turf Soccer Shoes", "url": "https://www.adidas.com/us/soccer-shoes-turf"},
    ],
    "Sports": [
        {"name": "Baseball", "url": "https://www.adidas.com/us/baseball"},
        {"name": "Basketball", "url": "https://www.adidas.com/us/basketball"},
        {"name": "Cricket", "url": "https://www.adidas.com/us/cricket"},
        {"name": "Football", "url": "https://www.adidas.com/us/football"},
        {"name": "Golf", "url": "https://www.adidas.com/us/golf"},
        {"name": "Outdoors", "url": "https://www.adidas.com/us/outdoor"},
        {"name": "Rugby", "url": "https://www.adidas.com/us/rugby"},
        {"name": "Running", "url": "https://www.adidas.com/us/running"},
        {"name": "Soccer", "url": "https://www.adidas.com/us/soccer"},
        {"name": "Skateboarding", "url": "https://www.adidas.com/us/skateboarding"},
        {"name": "Tennis", "url": "https://www.adidas.com/us/tennis"},
        {"name": "Training & Workout", "url": "https://www.adidas.com/us/workout"},
        {"name": "Volleyball Gear", "url": "https://www.adidas.com/us/volleyball"},
        {"name": "Weightlifting", "url": "https://www.adidas.com/us/weightlifting"},
        {"name": "Yoga", "url": "https://www.adidas.com/us/yoga"},
        {"name": "Motorsport", "url": "https://www.adidas.com/us/sport_motorsport"},
    ],
    "Popular Categories": [
        {"name": "Men's Turf Shoes", "url": "https://www.adidas.com/us/men-soccer-shoes-turf"},
        {"name": "Women's White Samba Shoes", "url": "https://www.adidas.com/us/women-white-samba-shoes"},
        {"name": "Tyshawn Men's Skate Shoes", "url": "https://www.adidas.com/us/men-tyshawn-skateboarding-shoes"},
        {"name": "Men's Running Shoes on Sale", "url": "https://www.adidas.com/us/men-running-shoes-sale"},
        {"name": "Anthony Edwards Basketball Shoes", "url": "https://www.adidas.com/us/men-anthony_edwards-basketball-shoes"},
        {"name": "Pink Gazelle Shoes", "url": "https://www.adidas.com/us/women-pink-gazelle-shoes"},
        {"name": "Women's Black Sambas", "url": "https://www.adidas.com/us/women-black-samba-shoes"},
        {"name": "Men's Basketball Shoes on Sale", "url": "https://www.adidas.com/us/men-basketball-shoes-sale"},
        {"name": "Shop All Tennis Shoes", "url": "https://www.adidas.com/us/tennis-shoes"},
        {"name": "Messi Jersey", "url": "https://www.adidas.com/us/lionel_messi-jerseys"},
        {"name": "Pink Gazelle Platform Shoes", "url": "https://www.adidas.com/us/women-pink-gazelle-platform"},
        {"name": "Black Shoes", "url": "https://www.adidas.com/us/black-shoes"},
        {"name": "White Athletic Sneakers", "url": "https://www.adidas.com/us/women-white-athletic_sneakers"},
        {"name": "White Shoes", "url": "https://www.adidas.com/us/white-shoes"},
        {"name": "Women's Running Shoes Sale", "url": "https://www.adidas.com/us/women-running-shoes-sale"},
        {"name": "Original Laced Sambas", "url": "https://www.adidas.com/us/originals-laces-samba-shoes"},
        {"name": "Women's Pink Sambas", "url": "https://www.adidas.com/us/women-pink-samba-shoes"},
        {"name": "Women's Pink adidas Originals", "url": "https://www.adidas.com/us/women-pink-originals-shoes"},
        {"name": "Women's Ultraboost Running Shoes", "url": "https://www.adidas.com/us/women-ultraboost-running-shoes"},
        {"name": "Men's Golf Shoes on Sale", "url": "https://www.adidas.com/us/men-golf-shoes-sale"},
    ],
}


def _slug(label: str) -> str:
    text = str(label or "").lower().replace("&", " and ").replace("'", "").replace("\u2019", "")
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return slug or "category"


def _flatten_categories() -> list[dict[str, str]]:
    """Flatten the sitemap sections into the base spider's category contract."""
    categories: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    used_names: set[str] = set()
    for section, entries in ADIDAS_CATEGORY_SECTIONS.items():
        for entry in entries:
            url = entry["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            base = _slug(entry["name"])
            name = base
            if name in used_names:
                name = f"{_slug(section)}-{base}"
            suffix = 2
            while name in used_names:
                name = f"{_slug(section)}-{base}-{suffix}"
                suffix += 1
            used_names.add(name)
            categories.append(
                {"category": name, "department": section, "subcategory": entry["name"], "url": url}
            )
    return categories


ADIDAS_CATEGORIES = _flatten_categories()
