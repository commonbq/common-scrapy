"""Deterministic RE/MAX state listing targets.

RE/MAX publishes one sale-search route per US state.  The spider intentionally
ships the 20 most populous states so its category surface stays consistent with
the other real-estate spiders in this repository.
"""

REMAX_CATEGORIES = [
    {"category": "california", "url": "https://www.remax.com/homes-for-sale/ca"},
    {"category": "texas", "url": "https://www.remax.com/homes-for-sale/tx"},
    {"category": "florida", "url": "https://www.remax.com/homes-for-sale/fl"},
    {"category": "new-york", "url": "https://www.remax.com/homes-for-sale/ny"},
    {"category": "pennsylvania", "url": "https://www.remax.com/homes-for-sale/pa"},
    {"category": "illinois", "url": "https://www.remax.com/homes-for-sale/il"},
    {"category": "ohio", "url": "https://www.remax.com/homes-for-sale/oh"},
    {"category": "georgia", "url": "https://www.remax.com/homes-for-sale/ga"},
    {"category": "north-carolina", "url": "https://www.remax.com/homes-for-sale/nc"},
    {"category": "michigan", "url": "https://www.remax.com/homes-for-sale/mi"},
    {"category": "new-jersey", "url": "https://www.remax.com/homes-for-sale/nj"},
    {"category": "virginia", "url": "https://www.remax.com/homes-for-sale/va"},
    {"category": "washington", "url": "https://www.remax.com/homes-for-sale/wa"},
    {"category": "arizona", "url": "https://www.remax.com/homes-for-sale/az"},
    {"category": "tennessee", "url": "https://www.remax.com/homes-for-sale/tn"},
    {"category": "massachusetts", "url": "https://www.remax.com/homes-for-sale/ma"},
    {"category": "indiana", "url": "https://www.remax.com/homes-for-sale/in"},
    {"category": "missouri", "url": "https://www.remax.com/homes-for-sale/mo"},
    {"category": "maryland", "url": "https://www.remax.com/homes-for-sale/md"},
    {"category": "wisconsin", "url": "https://www.remax.com/homes-for-sale/wi"},
]
