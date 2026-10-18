"""Viator's Popular Cities inventory, grouped by the live destination taxonomy.

Sourced from the homepage ``Popular Cities`` wordcloud
(``__PRELOADED_DATA__``/Apollo ``wordcloud`` rehydrate block) on 2026-10-19:
**35 destination pages in 23 groups**. Every link is stored exactly as the
homepage emits it (``/City/d<id>``), which is the form the spider's
``__PRELOADED_DATA__.pageModel.topActivities`` hydration expects.

The groups are the destination regions the site itself shows in each city
page's ``geo-hub-breadcrumbs`` trail: for US destinations the state
(``/USA/d77`` -> ``/Texas/d296`` -> Austin), and for the non-US destinations
the country or first-level region (``/France/d51`` ->
``/Ile-de-France/d5636`` -> Paris). The three state hub pages that also appear
in the wordcloud (``Arizona``, ``Colorado``, ``Florida``) are grouped with the
cities inside that state and scheduled first.

``VIATOR_CATEGORIES`` uses the grouped mapping contract consumed by
``BaseListingSpider``: ``{region: {leaf: url}}``. Leaf keys stay the bare city
slug, so the documented ``-a category=nashville`` command is unchanged; the
DAG groups the tasks by region.
"""

VIATOR_CATEGORIES = {
    # --- United States: grouped by the state in each city's breadcrumb trail.
    "arizona": {
        "arizona": "https://www.viator.com/Arizona/d271",
        "phoenix": "https://www.viator.com/Phoenix/d639",
    },
    "california": {
        "los-angeles": "https://www.viator.com/Los-Angeles/d645",
        "san-diego": "https://www.viator.com/San-Diego/d736",
        "san-francisco": "https://www.viator.com/San-Francisco/d651",
    },
    "colorado": {
        "colorado": "https://www.viator.com/Colorado/d273",
        "denver": "https://www.viator.com/Denver/d4837",
    },
    "florida": {
        "florida": "https://www.viator.com/Florida/d276",
        "key-west": "https://www.viator.com/Key-West/d661",
        "miami": "https://www.viator.com/Miami/d662",
        "orlando": "https://www.viator.com/Orlando/d663",
        "tampa": "https://www.viator.com/Tampa/d666",
    },
    "georgia": {
        "atlanta": "https://www.viator.com/Atlanta/d784",
    },
    "hawaii": {
        "maui": "https://www.viator.com/Maui/d671",
        "oahu": "https://www.viator.com/Oahu/d672",
    },
    "illinois": {
        "chicago": "https://www.viator.com/Chicago/d673",
    },
    "louisiana": {
        "new-orleans": "https://www.viator.com/New-Orleans/d675",
    },
    "massachusetts": {
        "boston": "https://www.viator.com/Boston/d678",
    },
    "nevada": {
        "las-vegas": "https://www.viator.com/Las-Vegas/d684",
    },
    "new-york": {
        "new-york-city": "https://www.viator.com/New-York-City/d687",
    },
    "pennsylvania": {
        "philadelphia": "https://www.viator.com/Philadelphia/d906",
    },
    "south-carolina": {
        "myrtle-beach": "https://www.viator.com/Myrtle-Beach/d5217",
    },
    "tennessee": {
        "nashville": "https://www.viator.com/Nashville/d799",
    },
    "texas": {
        "austin": "https://www.viator.com/Austin/d5021",
        "dallas": "https://www.viator.com/Dallas/d918",
        "houston": "https://www.viator.com/Houston/d5186",
        "san-antonio": "https://www.viator.com/San-Antonio/d910",
    },
    "washington": {
        "seattle": "https://www.viator.com/Seattle/d704",
    },
    "washington-dc": {
        "washington-dc": "https://www.viator.com/Washington-DC/d657",
    },
    # --- Non-US destinations: grouped by country / first-level region.
    "catalonia": {
        "barcelona": "https://www.viator.com/Barcelona/d562",
    },
    "england": {
        "london": "https://www.viator.com/London/d737",
    },
    "ile-de-france": {
        "paris": "https://www.viator.com/Paris/d479",
    },
    "italy": {
        "rome": "https://www.viator.com/Rome/d511",
    },
    "portugal": {
        "lisbon": "https://www.viator.com/Lisbon/d538",
    },
    "tuscany": {
        "florence": "https://www.viator.com/Florence/d519",
    },
}
