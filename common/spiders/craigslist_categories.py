"""Craigslist NYC category dictionary.

Source: captured from the Craigslist New York City homepage category navigation
(#sss "for sale" section). URLs normalized to the live working route
/search/<category-code>.

Category codes verified live on 2026-11-20.
"""

CATEGORIES = {
    "all_for_sale": "https://newyork.craigslist.org/search/sss",
    "antiques": "https://newyork.craigslist.org/search/ata",
    "appliances": "https://newyork.craigslist.org/search/ppa",
    "arts_crafts": "https://newyork.craigslist.org/search/ara",
    "atv_utv_sno": "https://newyork.craigslist.org/search/sna",
    "auto_parts": "https://newyork.craigslist.org/search/pta",
    "aviation": "https://newyork.craigslist.org/search/ava",
    "baby_kid": "https://newyork.craigslist.org/search/baa",
    "barter": "https://newyork.craigslist.org/search/bar",
    "beauty_hlth": "https://newyork.craigslist.org/search/haa",
    "bike_parts": "https://newyork.craigslist.org/search/bip",
    "bikes": "https://newyork.craigslist.org/search/bia",
    "boat_parts": "https://newyork.craigslist.org/search/bpa",
    "boats": "https://newyork.craigslist.org/search/boo",
    "books": "https://newyork.craigslist.org/search/bka",
    "business": "https://newyork.craigslist.org/search/bfa",
    "cars_trucks": "https://newyork.craigslist.org/search/cta",
    "cds_dvd_vhs": "https://newyork.craigslist.org/search/ema",
    "cell_phones": "https://newyork.craigslist.org/search/moa",
    "clothes_acc": "https://newyork.craigslist.org/search/cla",
    "collectibles": "https://newyork.craigslist.org/search/cba",
    "computer_parts": "https://newyork.craigslist.org/search/syp",
    "computers": "https://newyork.craigslist.org/search/sya",
    "electronics": "https://newyork.craigslist.org/search/ela",
    "farm_garden": "https://newyork.craigslist.org/search/gra",
    "free": "https://newyork.craigslist.org/search/zip",
    "furniture": "https://newyork.craigslist.org/search/fua",
    "garage_sale": "https://newyork.craigslist.org/search/gms",
    "general": "https://newyork.craigslist.org/search/foa",
    "heavy_equip": "https://newyork.craigslist.org/search/hva",
    "household": "https://newyork.craigslist.org/search/hsa",
    "jewelry": "https://newyork.craigslist.org/search/jwa",
    "materials": "https://newyork.craigslist.org/search/maa",
    "motorcycle_parts": "https://newyork.craigslist.org/search/mpa",
    "motorcycles": "https://newyork.craigslist.org/search/mca",
    "music_instr": "https://newyork.craigslist.org/search/msa",
    "photo_video": "https://newyork.craigslist.org/search/pha",
    "rvs_camp": "https://newyork.craigslist.org/search/rva",
    "sporting": "https://newyork.craigslist.org/search/sga",
    "tickets": "https://newyork.craigslist.org/search/tia",
    "tools": "https://newyork.craigslist.org/search/tla",
    "toys_games": "https://newyork.craigslist.org/search/taa",
    "trailers": "https://newyork.craigslist.org/search/tra",
    "video_gaming": "https://newyork.craigslist.org/search/vga",
    "wanted": "https://newyork.craigslist.org/search/waa",
    "wheels_tires": "https://newyork.craigslist.org/search/wta",
}