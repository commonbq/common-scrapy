"""SHEIN's complete top-level category inventory.

Sourced from the live US homepage category navigation on 2026-10-12.  SHEIN
publishes these as peer categories, so the base spider's synthetic ``all``
group is represented explicitly here.
"""

SHEIN_CATEGORIES = {
    "all": {
        "women": "https://us.shein.com/RecommendSelection/Women-Clothing-sc-017172961.html",
        "kids": "https://us.shein.com/RecommendSelection/Kids-sc-017185550.html",
        "curve": "https://us.shein.com/RecommendSelection/Curve-sc-017172964.html",
        "men": "https://us.shein.com/RecommendSelection/Men-Clothing-sc-017172963.html",
        "shoes": "https://us.shein.com/RecommendSelection/Shoes-sc-017172966.html",
        "underwear-sleepwear": "https://us.shein.com/RecommendSelection/Underwear-Sleepwear-sc-017172965.html",
        "home": "https://us.shein.com/RecommendSelection/Home-Kitchen-sc-017185546.html",
        "jewelry": "https://us.shein.com/RecommendSelection/Jewelry-Accessories-sc-017291431.html",
        "beauty": "https://us.shein.com/RecommendSelection/Beauty-Health-sc-017172970.html",
        "baby": "https://us.shein.com/RecommendSelection/Baby-Maternity-sc-017172967.html",
        "bags": "https://us.shein.com/RecommendSelection/Bags-Luggage-sc-017174546.html",
        "sports": "https://us.shein.com/RecommendSelection/Sports-Outdoors-sc-017185553.html",
        "home-textile": "https://us.shein.com/RecommendSelection/Home-Textile-sc-017172972.html",
        "cell-phones-accessories": "https://us.shein.com/RecommendSelection/Cell-Phones-Accessories-sc-017706910.html",
        "electronics": "https://us.shein.com/RecommendSelection/Electronics-sc-017706908.html",
        "toys-games": "https://us.shein.com/RecommendSelection/Toys-Games-sc-017172978.html",
        "tools-home-improvement": "https://us.shein.com/RecommendSelection/Tools-Home-Improvement-sc-017185547.html",
        "office-school-supplies": "https://us.shein.com/RecommendSelection/Office-School-Supplies-sc-017185552.html",
        "pet-supplies": "https://us.shein.com/RecommendSelection/Pet-Supplies-sc-017172974.html",
        "home-appliances": "https://us.shein.com/RecommendSelection/Appliances-sc-017172977.html",
        "automotive": "https://us.shein.com/RecommendSelection/Automotive-sc-017172975.html",
        "books-magazines": "https://us.shein.com/RecommendSelection/Books-Magazines-sc-0175086797.html",
        "food-beverages": "https://us.shein.com/RecommendSelection/Food-Beverages-sc-0175086791.html",
    }
}
