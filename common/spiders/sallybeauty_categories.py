"""Sally Beauty's complete crawlable storefront category inventory.

The storefront's ``Find it by category`` navigation was checked on 2026-10-12.
It exposes the product departments below plus three non-listing destinations
(``Free Hair Color Advice``, ``Brands``, and ``DIY University``); those content
and index pages are intentionally excluded because this spider requires an SFCC
product grid.  ``new`` remains as the crawlable New Arrivals collection linked
from the current home-page category rail.
"""

SALLYBEAUTY_CATEGORIES = {
    "hair-color": {
        "hair-color": "https://www.sallybeauty.com/hair-color/",
    },
    "hair-care": {
        "hair-care": "https://www.sallybeauty.com/hair-care/shop-by-product/",
    },
    "textured-curly-hair": {
        "textured-curly-hair": "https://www.sallybeauty.com/hair-care/textured-and-curly-hair-care/",
    },
    "hair-extensions": {
        "hair-extensions": "https://www.sallybeauty.com/hair-care/hair-care-accessories-and-styling-products/hair-extensions/",
    },
    "tools-brushes": {
        "tools-brushes": "https://www.sallybeauty.com/tools-and-brushes/",
    },
    "nails": {
        "nails": "https://www.sallybeauty.com/nails/",
    },
    "cosmetics-skin-care": {
        "cosmetics-skin-care": "https://www.sallybeauty.com/cosmetics-and-skin-care/",
    },
    "fragrances": {
        "fragrances": "https://www.sallybeauty.com/cosmetics-and-skin-care/fragrances/",
    },
    "mens-grooming": {
        "mens-grooming": "https://www.sallybeauty.com/mens-grooming/",
    },
    "salon-supplies": {
        "salon-supplies": "https://www.sallybeauty.com/salon-supplies/",
    },
    "featured": {
        "featured": "https://www.sallybeauty.com/featured/",
        "new": "https://www.sallybeauty.com/sally-new/",
    },
    "deals": {
        "deals": "https://www.sallybeauty.com/deals/",
    },
    "clearance": {
        "clearance": "https://www.sallybeauty.com/clearance/",
    },
}
