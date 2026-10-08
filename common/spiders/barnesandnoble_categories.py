"""Stable Barnes & Noble collection seeds used to bootstrap Storefront API access."""

BASE_URL = "https://www.barnesandnoble.com/collections"

_PATHS = (
    ("books", "books"),
    ("fiction", "books/fiction"),
    ("nonfiction", "books/nonfiction"),
    ("bestselling-books", "books/bestselling-books"),
    ("new-releases", "books/new-releases"),
    ("kids", "books/kids"),
    ("teens-ya", "books/teens-ya"),
    ("romance", "books/romance"),
    ("mystery-thrillers", "books/mystery-thrillers"),
    ("science-fiction-fantasy", "books/science-fiction-fantasy"),
    ("history", "books/history"),
    ("biography", "books/biography"),
    ("business", "books/business"),
    ("cookbooks-food-wine", "books/cookbooks-food-wine"),
    ("graphic-novels-comics", "books/graphic-novels-comics"),
    ("ebooks-nook", "ebooks-nook"),
    ("audiobooks", "audiobooks"),
    ("toys-games", "toys-games"),
    ("stationery-gifts", "stationery-gifts"),
    ("movies-tv", "movies-tv"),
)

BARNESANDNOBLE_CATEGORIES = [
    {
        "category": category,
        "url": f"{BASE_URL}/{path}",
        "search_query": category.replace("-", " "),
    }
    for category, path in _PATHS
]
