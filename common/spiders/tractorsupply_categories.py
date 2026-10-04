"""Product sitemap inventory for Tractor Supply Co."""

TRACTORSUPPLY_CATEGORIES = [
    {
        "category": f"products-{number}",
        "name": f"Product sitemap {number}",
        "department": "All products",
        "url": f"https://www.tractorsupply.com/sitemap_product_{number}.xml",
    }
    for number in range(1, 5)
]
