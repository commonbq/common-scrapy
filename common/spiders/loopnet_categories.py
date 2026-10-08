"""Stable LoopNet property-type searches exposed by the site navigation."""

LOOPNET_CATEGORIES = [
    {"category": slug, "url": f"https://www.loopnet.com/search/{path}/usa/{transaction}/"}
    for slug, path, transaction in (
        ("commercial-real-estate-for-sale", "commercial-real-estate", "for-sale"),
        ("commercial-real-estate-for-lease", "commercial-real-estate", "for-lease"),
        ("commercial-real-estate-auctions", "commercial-real-estate", "auctions"),
        ("apartment-buildings-for-sale", "apartment-buildings", "for-sale"),
        ("multifamily-properties-for-sale", "multifamily-properties", "for-sale"),
        ("office-buildings-for-sale", "office-buildings", "for-sale"),
        ("office-space-for-lease", "office-space", "for-lease"),
        ("industrial-properties-for-sale", "industrial-properties", "for-sale"),
        ("industrial-space-for-lease", "industrial-space", "for-lease"),
        ("retail-properties-for-sale", "retail-properties", "for-sale"),
        ("retail-space-for-lease", "retail-space", "for-lease"),
        ("land-for-lease", "land", "for-lease"),
        ("warehouses-for-sale", "warehouses", "for-sale"),
        ("flex-space-for-sale", "flex-space", "for-sale"),
        ("flex-space-for-lease", "flex-space", "for-lease"),
        ("shopping-centers-for-sale", "shopping-centers", "for-sale"),
        ("self-storage-facilities-for-sale", "self-storage-facilities", "for-sale"),
        ("hotels-for-sale", "hotels", "for-sale"),
        ("medical-offices-for-lease", "medical-offices", "for-lease"),
        ("restaurants-for-sale", "restaurants", "for-sale"),
    )
]
