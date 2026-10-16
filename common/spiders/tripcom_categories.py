"""Trip.com popular hotel destinations, grouped by country.

Source: the ``us.trip.com`` home page ``seoLinksContent.data.tabList``
"Popular Hotels" tab, refreshed live on 2026-10-16. The full tab advertises
**29** destination links; each link carries both the city slug and the numeric
city id, e.g. ``https://us.trip.com/hotels/<slug>-hotels-list-<id>/``.

The inventory is a **grouped mapping** ``{country: {leaf: url}}``, matching the
base-listing-spider contract: the leaf name is what ``-a category=<leaf>``
selects and what the DAG schedules one task per. Trip.com has no public
"all cities" JSON endpoint (the ``/hotels/all-cities/`` page renders only one
alphabetical page of ~1,000 links and paginates client-side with no reachable
data URL), so this curated popular-destination set is the deterministic source.
"""

TRIPCOM_CATEGORIES = {
    "China": {
        "beijing": "https://us.trip.com/hotels/beijing-hotels-list-1/",
        "chengdu": "https://us.trip.com/hotels/chengdu-hotels-list-28/",
        "chongqing": "https://us.trip.com/hotels/chongqing-hotels-list-4/",
        "guangzhou": "https://us.trip.com/hotels/guangzhou-hotels-list-32/",
        "hangzhou": "https://us.trip.com/hotels/hangzhou-hotels-list-17/",
        "hong-kong": "https://us.trip.com/hotels/hong-kong-hotels-list-58/",
        "shanghai": "https://us.trip.com/hotels/shanghai-hotels-list-2/",
        "shenzhen": "https://us.trip.com/hotels/shenzhen-hotels-list-30/",
        "xi-an": "https://us.trip.com/hotels/xi-an-hotels-list-10/",
        "zhangjiajie": "https://us.trip.com/hotels/zhangjiajie-hotels-list-27/",
    },
    "United States": {
        "chicago": "https://us.trip.com/hotels/chicago-hotels-list-549/",
        "indianapolis": "https://us.trip.com/hotels/indianapolis-hotels-list-1291/",
        "las-vegas": "https://us.trip.com/hotels/las-vegas-hotels-list-26282/",
        "miami": "https://us.trip.com/hotels/miami-hotels-list-25773/",
        "new-york": "https://us.trip.com/hotels/new-york-hotels-list-633/",
    },
    "Thailand": {
        "bangkok": "https://us.trip.com/hotels/bangkok-hotels-list-359/",
    },
    "Vietnam": {
        "ho-chi-minh-city": "https://us.trip.com/hotels/ho-chi-minh-city-hotels-list-301/",
    },
    "Malaysia": {
        "kuala-lumpur": "https://us.trip.com/hotels/kuala-lumpur-hotels-list-315/",
    },
    "Singapore": {
        "singapore": "https://us.trip.com/hotels/singapore-hotels-list-73/",
    },
    "Japan": {
        "osaka": "https://us.trip.com/hotels/osaka-hotels-list-219/",
        "tokyo": "https://us.trip.com/hotels/tokyo-hotels-list-228/",
    },
    "Australia": {
        "gold-coast": "https://us.trip.com/hotels/gold-coast-hotels-list-1210/",
        "melbourne": "https://us.trip.com/hotels/melbourne-hotels-list-358/",
        "sydney": "https://us.trip.com/hotels/sydney-hotels-list-501/",
    },
    "Turkey": {
        "istanbul": "https://us.trip.com/hotels/istanbul-hotels-list-532/",
    },
    "United Kingdom": {
        "london": "https://us.trip.com/hotels/london-hotels-list-338/",
    },
    "France": {
        "paris": "https://us.trip.com/hotels/paris-hotels-list-192/",
    },
    "South Korea": {
        "seoul": "https://us.trip.com/hotels/seoul-hotels-list-274/",
    },
    "Taiwan": {
        "taipei": "https://us.trip.com/hotels/taipei-hotels-list-617/",
    },
}
