"""Complete US state-level taxonomy for Realtor.com sale listings."""


def _state_urls(*names: str) -> dict[str, str]:
    return {
        name.lower(): f"https://www.realtor.com/realestateandhomes-search/{name}"
        for name in names
    }


# Census regions keep the inventory grouped while the leaf keys remain the values
# accepted by ``-a category=``. District of Columbia is included with the South.
REALTOR_CATEGORIES = {
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

# Backward-compatible import name used by older callers.
CATEGORIES = REALTOR_CATEGORIES
