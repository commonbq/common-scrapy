"""LandWatch crawl inventory: property-type searches plus every US state market.

Leaf keys are the values accepted by ``-a category=``. Two groups are exposed:

* ``land-types`` -- the property-type search links LandWatch publishes in its
  homepage navigation (captured live on 2026-10-19).
* ``northeast``/``midwest``/``south``/``west`` -- all 50 states plus the
  District of Columbia, split by US Census region so the DAG can schedule them
  as TaskGroups. The grouping is editorial; the leaf slugs are unchanged from
  the flat inventory this file used to hold.
"""


def _state_urls(*names: str) -> dict[str, str]:
    return {
        name.lower(): f"https://www.landwatch.com/{name.lower()}-land-for-sale"
        for name in names
    }


# Property-type landing pages linked from https://www.landwatch.com/ (homepage
# search navigation + the sitemap's property-type block).
LAND_TYPES = {
    "land-for-sale": "https://www.landwatch.com/land",
    "hunting-property": "https://www.landwatch.com/hunting-property",
    "farms-ranches": "https://www.landwatch.com/farms-ranches",
    "homes": "https://www.landwatch.com/homes",
    "timberland-property": "https://www.landwatch.com/timberland-property",
    "commercial-property": "https://www.landwatch.com/commercial-property",
    "homesites": "https://www.landwatch.com/homesites",
    "recreational-property": "https://www.landwatch.com/recreational-property",
    "horse-property": "https://www.landwatch.com/horse-property",
    "undeveloped-land": "https://www.landwatch.com/undeveloped-land",
    "waterfront-property": "https://www.landwatch.com/waterfront-property",
}


LANDWATCH_CATEGORIES = {
    "land-types": LAND_TYPES,
    # District of Columbia is grouped with the South, matching the convention
    # already used by ``realtor_categories.py``.
    "northeast": _state_urls(
        "Connecticut",
        "Maine",
        "Massachusetts",
        "New-Hampshire",
        "Rhode-Island",
        "Vermont",
        "New-Jersey",
        "New-York",
        "Pennsylvania",
    ),
    "midwest": _state_urls(
        "Indiana",
        "Illinois",
        "Michigan",
        "Ohio",
        "Wisconsin",
        "Iowa",
        "Kansas",
        "Minnesota",
        "Missouri",
        "Nebraska",
        "North-Dakota",
        "South-Dakota",
    ),
    "south": _state_urls(
        "Delaware",
        "District-of-Columbia",
        "Florida",
        "Georgia",
        "Maryland",
        "North-Carolina",
        "South-Carolina",
        "Virginia",
        "West-Virginia",
        "Alabama",
        "Kentucky",
        "Mississippi",
        "Tennessee",
        "Arkansas",
        "Louisiana",
        "Oklahoma",
        "Texas",
    ),
    "west": _state_urls(
        "Arizona",
        "Colorado",
        "Idaho",
        "Montana",
        "Nevada",
        "New-Mexico",
        "Utah",
        "Wyoming",
        "Alaska",
        "California",
        "Hawaii",
        "Oregon",
        "Washington",
    ),
}
