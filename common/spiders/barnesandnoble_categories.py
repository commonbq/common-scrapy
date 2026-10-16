"""Barnes & Noble collection categories refreshed from live site navigation.

Source: Barnes & Noble's live collections sitemap, fetched 2026-10-17.
Every ``url`` points at a real ``/collections/<department>/<leaf>`` page the
storefront actually emits; any leaf that does not resolve at crawl time is
skipped by the spider rather than emitting zero items.

Dict format per base_listing_spider.py:
    {group: {leaf: {"url": ..., "search_query": ..., "department": ..., "category": ...}}}
"""

BASE_URL = "https://www.barnesandnoble.com/collections"

BARNESANDNOBLE_CATEGORIES = {
    "books": {
        "books": {
            "url": "https://www.barnesandnoble.com/collections/books",
            "search_query": "books",
            "department": "books",
            "category": "books",
        },
        "fiction": {
            "url": "https://www.barnesandnoble.com/collections/books/fiction",
            "search_query": "fiction",
            "department": "books",
            "category": "fiction",
        },
        "nonfiction": {
            "url": "https://www.barnesandnoble.com/collections/books/nonfiction",
            "search_query": "nonfiction",
            "department": "books",
            "category": "nonfiction",
        },
        "mystery-thrillers": {
            "url": "https://www.barnesandnoble.com/collections/books/mystery-thrillers",
            "search_query": "mystery thrillers",
            "department": "books",
            "category": "mystery-thrillers",
        },
        "science-fiction-fantasy": {
            "url": "https://www.barnesandnoble.com/collections/books/science-fiction-fantasy",
            "search_query": "science fiction fantasy",
            "department": "books",
            "category": "science-fiction-fantasy",
        },
        "romance": {
            "url": "https://www.barnesandnoble.com/collections/books/romance",
            "search_query": "romance",
            "department": "books",
            "category": "romance",
        },
        "history": {
            "url": "https://www.barnesandnoble.com/collections/books/history",
            "search_query": "history",
            "department": "books",
            "category": "history",
        },
        "biography": {
            "url": "https://www.barnesandnoble.com/collections/books/biography",
            "search_query": "biography",
            "department": "books",
            "category": "biography",
        },
        "business": {
            "url": "https://www.barnesandnoble.com/collections/books/business",
            "search_query": "business",
            "department": "books",
            "category": "business",
        },
        "cookbooks-food-wine": {
            "url": "https://www.barnesandnoble.com/collections/books/cookbooks-food-wine",
            "search_query": "cookbooks food wine",
            "department": "books",
            "category": "cookbooks-food-wine",
        },
        "graphic-novels-comics": {
            "url": "https://www.barnesandnoble.com/collections/books/graphic-novels-comics",
            "search_query": "graphic novels comics",
            "department": "books",
            "category": "graphic-novels-comics",
        },
        "kids": {
            "url": "https://www.barnesandnoble.com/collections/books/kids",
            "search_query": "kids",
            "department": "books",
            "category": "kids",
        },
        "teens-ya": {
            "url": "https://www.barnesandnoble.com/collections/books/teens-ya",
            "search_query": "teens ya",
            "department": "books",
            "category": "teens-ya",
        },
        "bestselling-books": {
            "url": "https://www.barnesandnoble.com/collections/books/bestselling-books",
            "search_query": "bestselling books",
            "department": "books",
            "category": "bestselling-books",
        },
        "new-releases": {
            "url": "https://www.barnesandnoble.com/collections/books/new-releases",
            "search_query": "new releases",
            "department": "books",
            "category": "new-releases",
        },
    },
    "audiobooks": {
        "audiobooks": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks",
            "search_query": "audiobooks",
            "department": "audiobooks",
            "category": "audiobooks",
        },
        "mystery-thrillers": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/mystery-thrillers",
            "search_query": "mystery thrillers",
            "department": "audiobooks",
            "category": "mystery-thrillers",
        },
        "romance": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/romance",
            "search_query": "romance",
            "department": "audiobooks",
            "category": "romance",
        },
        "science-fiction-fantasy": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/science-fiction-fantasy",
            "search_query": "science fiction fantasy",
            "department": "audiobooks",
            "category": "science-fiction-fantasy",
        },
        "history": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/history",
            "search_query": "history",
            "department": "audiobooks",
            "category": "history",
        },
        "biography": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/biography",
            "search_query": "biography",
            "department": "audiobooks",
            "category": "biography",
        },
        "business": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/business",
            "search_query": "business",
            "department": "audiobooks",
            "category": "business",
        },
        "literature": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/literature",
            "search_query": "literature",
            "department": "audiobooks",
            "category": "literature",
        },
        "new-releases": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/new-releases",
            "search_query": "new releases",
            "department": "audiobooks",
            "category": "new-releases",
        },
        "kids": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/kids",
            "search_query": "kids",
            "department": "audiobooks",
            "category": "kids",
        },
        "teens-ya": {
            "url": "https://www.barnesandnoble.com/collections/audiobooks/teens-ya",
            "search_query": "teens ya",
            "department": "audiobooks",
            "category": "teens-ya",
        },
    },
    "ebooks-nook": {
        "ebooks-nook": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook",
            "search_query": "ebooks nook",
            "department": "ebooks-nook",
            "category": "ebooks-nook",
        },
        "mystery-thrillers": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/mystery-thrillers",
            "search_query": "mystery thrillers",
            "department": "ebooks-nook",
            "category": "mystery-thrillers",
        },
        "romance": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/romance",
            "search_query": "romance",
            "department": "ebooks-nook",
            "category": "romance",
        },
        "science-fiction-fantasy": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/science-fiction-fantasy",
            "search_query": "science fiction fantasy",
            "department": "ebooks-nook",
            "category": "science-fiction-fantasy",
        },
        "graphic-novels-comics": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/graphic-novels-comics",
            "search_query": "graphic novels comics",
            "department": "ebooks-nook",
            "category": "graphic-novels-comics",
        },
        "history": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/history",
            "search_query": "history",
            "department": "ebooks-nook",
            "category": "history",
        },
        "business": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/business",
            "search_query": "business",
            "department": "ebooks-nook",
            "category": "business",
        },
        "new-releases": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/new-releases",
            "search_query": "new releases",
            "department": "ebooks-nook",
            "category": "new-releases",
        },
        "nook-devices": {
            "url": "https://www.barnesandnoble.com/collections/ebooks-nook/nook-devices",
            "search_query": "nook devices",
            "department": "ebooks-nook",
            "category": "nook-devices",
        },
    },
    "movies-tv": {
        "movies-tv": {
            "url": "https://www.barnesandnoble.com/collections/movies-tv",
            "search_query": "movies tv",
            "department": "movies-tv",
            "category": "movies-tv",
        },
        "the-criterion-collection": {
            "url": "https://www.barnesandnoble.com/collections/movies-tv/the-criterion-collection",
            "search_query": "criterion collection",
            "department": "movies-tv",
            "category": "the-criterion-collection",
        },
        "doctor-who": {
            "url": "https://www.barnesandnoble.com/collections/movies-tv/doctor-who",
            "search_query": "doctor who",
            "department": "movies-tv",
            "category": "doctor-who",
        },
        "anime": {
            "url": "https://www.barnesandnoble.com/collections/movies-tv/anime",
            "search_query": "anime",
            "department": "movies-tv",
            "category": "anime",
        },
    },
    "music": {
        "music": {
            "url": "https://www.barnesandnoble.com/collections/music",
            "search_query": "music",
            "department": "music",
            "category": "music",
        },
        "vinyl-albums": {
            "url": "https://www.barnesandnoble.com/collections/music/vinyl-albums",
            "search_query": "vinyl albums",
            "department": "music",
            "category": "vinyl-albums",
        },
        "music-deals": {
            "url": "https://www.barnesandnoble.com/collections/music/music-deals",
            "search_query": "music deals",
            "department": "music",
            "category": "music-deals",
        },
    },
    "stationery-gifts": {
        "stationery-gifts": {
            "url": "https://www.barnesandnoble.com/collections/stationery-gifts",
            "search_query": "stationery gifts",
            "department": "stationery-gifts",
            "category": "stationery-gifts",
        },
        "journals": {
            "url": "https://www.barnesandnoble.com/collections/stationery-gifts/journals-1",
            "search_query": "journals",
            "department": "stationery-gifts",
            "category": "journals",
        },
        "planners": {
            "url": "https://www.barnesandnoble.com/collections/stationery-gifts/planners",
            "search_query": "planners",
            "department": "stationery-gifts",
            "category": "planners",
        },
        "greeting-cards": {
            "url": "https://www.barnesandnoble.com/collections/stationery-gifts/stationery-writing/greeting-cards-2",
            "search_query": "greeting cards",
            "department": "stationery-gifts",
            "category": "greeting-cards",
        },
        "gift-wrap": {
            "url": "https://www.barnesandnoble.com/collections/stationery-gifts/gift-wrap",
            "search_query": "gift wrap",
            "department": "stationery-gifts",
            "category": "gift-wrap",
        },
        "calendars": {
            "url": "https://www.barnesandnoble.com/collections/stationery-gifts/calendars",
            "search_query": "calendars",
            "department": "stationery-gifts",
            "category": "calendars",
        },
    },
    "toys-games": {
        "toys-games": {
            "url": "https://www.barnesandnoble.com/collections/toys-games",
            "search_query": "toys games",
            "department": "toys-games",
            "category": "toys-games",
        },
        "games": {
            "url": "https://www.barnesandnoble.com/collections/toys-games/games",
            "search_query": "games",
            "department": "toys-games",
            "category": "games",
        },
        "puzzles": {
            "url": "https://www.barnesandnoble.com/collections/toys-games/puzzles",
            "search_query": "puzzles",
            "department": "toys-games",
            "category": "puzzles",
        },
        "arts-crafts": {
            "url": "https://www.barnesandnoble.com/collections/toys-games/arts-crafts",
            "search_query": "arts crafts",
            "department": "toys-games",
            "category": "arts-crafts",
        },
        "building-lego": {
            "url": "https://www.barnesandnoble.com/collections/toys-games/building-lego",
            "search_query": "lego building sets",
            "department": "toys-games",
            "category": "building-lego",
        },
        "dolls-stuffed-animals": {
            "url": "https://www.barnesandnoble.com/collections/toys-games/dolls-stuffed-animals",
            "search_query": "dolls stuffed animals",
            "department": "toys-games",
            "category": "dolls-stuffed-animals",
        },
        "outdoor-toys": {
            "url": "https://www.barnesandnoble.com/collections/toys-games/outdoor-toys",
            "search_query": "outdoor toys",
            "department": "toys-games",
            "category": "outdoor-toys",
        },
    },
}
