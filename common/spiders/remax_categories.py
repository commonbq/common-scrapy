"""RE/MAX crawl inventory: every US state sale-search route, grouped by region.

The state list is the ``homes-for-sale/<state>`` navigation published on
https://www.remax.com/ (captured live on 2026-10-19: 50 states, unchanged from
the previous flat inventory). The District of Columbia is added explicitly:
``/homes-for-sale/dc`` is not in the desktop navigation, but it is a real state
page (verified live 2026-10-19, 3,839 sale listings), so the inventory covers all
51 sale-search state routes RE/MAX serves.

Leaf keys are the values accepted by ``-a category=``. The
``northeast``/``midwest``/``south``/``west`` groups are the four US Census
regions, matching the convention already used by ``landwatch_categories.py`` and
``realtor_categories.py``; the grouping is editorial and the leaf slugs are
unchanged from the flat inventory this file used to hold.
"""


def _state_urls(*names: str) -> dict[str, str]:
    return {
        name.lower(): f"https://www.remax.com/homes-for-sale/{_STATE_CODES[name]}"
        for name in names
    }


# RE/MAX state route segments. The site uses the postal abbreviation for every
# state, which is not mechanically derivable from the full state name.
_STATE_CODES = {
    "Alabama": "al",
    "Alaska": "ak",
    "Arizona": "az",
    "Arkansas": "ar",
    "California": "ca",
    "Colorado": "co",
    "Connecticut": "ct",
    "Delaware": "de",
    "District-of-Columbia": "dc",
    "Florida": "fl",
    "Georgia": "ga",
    "Hawaii": "hi",
    "Idaho": "id",
    "Illinois": "il",
    "Indiana": "in",
    "Iowa": "ia",
    "Kansas": "ks",
    "Kentucky": "ky",
    "Louisiana": "la",
    "Maine": "me",
    "Maryland": "md",
    "Massachusetts": "ma",
    "Michigan": "mi",
    "Minnesota": "mn",
    "Mississippi": "ms",
    "Missouri": "mo",
    "Montana": "mt",
    "Nebraska": "ne",
    "Nevada": "nv",
    "New-Hampshire": "nh",
    "New-Jersey": "nj",
    "New-Mexico": "nm",
    "New-York": "ny",
    "North-Carolina": "nc",
    "North-Dakota": "nd",
    "Ohio": "oh",
    "Oklahoma": "ok",
    "Oregon": "or",
    "Pennsylvania": "pa",
    "Rhode-Island": "ri",
    "South-Carolina": "sc",
    "South-Dakota": "sd",
    "Tennessee": "tn",
    "Texas": "tx",
    "Utah": "ut",
    "Vermont": "vt",
    "Virginia": "va",
    "Washington": "wa",
    "West-Virginia": "wv",
    "Wisconsin": "wi",
    "Wyoming": "wy",
}


REMAX_CATEGORIES = {
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
