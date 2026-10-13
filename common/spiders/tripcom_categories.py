"""Trip.com popular hotel destinations, grouped by country.

Source: the ``us.trip.com`` home page ``seoLinksContent.data.tabList``
"Popular Hotels" tab. The full tab currently advertises **21** destination
links (captured 2026-10-13); each link carries both the city slug and the
numeric city id, e.g. ``https://us.trip.com/hotels/<slug>-hotels-list-<id>/``.

The inventory is a **grouped mapping** ``{country: {leaf: url}}``, matching the
base-listing-spider contract: the leaf name is what ``-a category=<leaf>``
selects and what the DAG schedules one task per. Trip.com has no public
"all cities" JSON endpoint (the ``/hotels/all-cities/`` page renders only one
alphabetical page of ~1,000 links and paginates client-side with no reachable
data URL), so this curated popular-destination set is the deterministic source.
"""

TRIPCOM_CATEGORIES = {
    "China": {
        "shanghai": "https://us.trip.com/hotels/shanghai-hotels-list-2/",
        "beijing": "https://us.trip.com/hotels/beijing-hotels-list-1/",
        "guangzhou": "https://us.trip.com/hotels/guangzhou-hotels-list-32/",
        "hong-kong": "https://us.trip.com/hotels/hong-kong-hotels-list-58/",
    },
    "United States": {
        "las-vegas": "https://us.trip.com/hotels/las-vegas-hotels-list-26282/",
        "new-york": "https://us.trip.com/hotels/new-york-hotels-list-633/",
        "chicago": "https://us.trip.com/hotels/chicago-hotels-list-549/",
        "san-diego": "https://us.trip.com/hotels/san-diego-hotels-list-698/",
        "miami": "https://us.trip.com/hotels/miami-hotels-list-25773/",
        "new-orleans": "https://us.trip.com/hotels/new-orleans-hotels-list-1186/",
        "nashville": "https://us.trip.com/hotels/nashville-hotels-list-3228/",
        "boston": "https://us.trip.com/hotels/boston-hotels-list-26848/",
        "orlando": "https://us.trip.com/hotels/orlando-hotels-list-1187/",
        "savannah": "https://us.trip.com/hotels/savannah-hotels-list-26631/",
        "charleston": "https://us.trip.com/hotels/charleston-hotels-list-4188/",
        "los-angeles": "https://us.trip.com/hotels/los-angeles-hotels-list-347/",
    },
    "Thailand": {
        "bangkok": "https://us.trip.com/hotels/bangkok-hotels-list-359/",
    },
    "Malaysia": {
        "kuala-lumpur": "https://us.trip.com/hotels/kuala-lumpur-hotels-list-315/",
    },
    "United Arab Emirates": {
        "dubai": "https://us.trip.com/hotels/dubai-hotels-list-220/",
    },
    "Singapore": {
        "singapore": "https://us.trip.com/hotels/singapore-hotels-list-73/",
    },
    "Vietnam": {
        "da-nang": "https://us.trip.com/hotels/da-nang-hotels-list-1356/",
    },
}
