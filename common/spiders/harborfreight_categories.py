"""Stable Harbor Freight department/category seeds."""

BASE_URL = "https://www.harborfreight.com"

# The public department navigation.  Department names are accepted as aliases
# for their first product-bearing category so the documented `Automotive` smoke
# command produces inventory rather than crawling a taxonomy landing page.
_CATEGORY_PATHS = {
    "Automotive": "automotive/jacks-jack-stands.html",
    "Generators & Engines": "generators-engines/generators.html",
    "Tool Storage & Organization": "tool-storage-organization/tool-storage.html",
    "Welding": "welding/welders.html",
    "Power Tools": "power-tools/drills-drivers.html",
    "Air Tools & Compressors": "air-tools-compressors/air-tools.html",
    "Hand Tools": "hand-tools/sockets-ratchets.html",
    "Lawn & Garden": "lawn-garden/gardening-garden-tools.html",
    "Lighting": "lighting/flashlights.html",
    "Safety": "safety/gloves.html",
    "Electrical": "electrical/extension-cords-power-strips.html",
    "Material Handling": "material-handling/hand-trucks-carts-dollies.html",
    "Pumps & Plumbing": "plumbing/pumps.html",
    "Painting": "painting/paint-sprayers.html",
    "Home & Security": "home/security-safes.html",
    "Building & Construction": "building-construction/masonry-tile-stone.html",
    "Hardware": "hardware/nuts-bolts.html",
}

HARBORFREIGHT_CATEGORIES = [
    {"category": name, "department": name, "subcategory": path.rsplit("/", 1)[-1].removesuffix(".html"),
     "url": f"{BASE_URL}/{path}"}
    for name, path in _CATEGORY_PATHS.items()
]
