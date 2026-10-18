from scrapy.http import HtmlResponse, Request

from common.spiders.oreilly_categories import OREILLY_CATEGORIES, child_categories
from common.spiders.oreilly_listing_spider import OreillyListingSpider


HTML = """
<script>
window._ost.totalResults = 1; window._ost.totalPages = 1;
var broadleafProductId = 7946016; var itemId = 'BBR|3512RGS';
window[`_7946016_name`] = 'BrakeBest Select Front Brake Rotor ';
window[`_7946016_primaryImage`] = 'https://img.example/rotor.jpg';
window[`_7946016_pricing`] = {'currency': {'currencyCode':'USD'}, 'price':89.99,
 'retailPrice':99.99, 'salePrice':89.99};
window._ost.products[itemId] = {item_id: itemId,
 item_name: 'BrakeBest Select Front Brake Rotor  - 3512RGS', price: 89.99,
 currency: 'USD', index: 1};
</script>
<a data-id="7946016" href="/detail/rotor"></a>
"""


def test_bootstrap_product_and_export_contract():
    spider = OreillyListingSpider(category_url="https://www.oreillyauto.com/shop/b/brakes/x")
    request = Request(spider.category_url, meta={"page": 1, "category_path": "Brakes"})
    response = HtmlResponse(request.url, request=request, body=HTML.encode())
    items = [x for x in spider.parse(response) if isinstance(x, dict)]
    assert items[0]["item_id"] == "BBR|3512RGS"
    assert items[0]["price"] == 89.99
    assert items[0]["url"] == "https://www.oreillyauto.com/detail/rotor"
    assert "source" in spider.custom_settings["FEED_EXPORT_FIELDS"]


def test_child_category_hydration_and_page_url():
    html = """<script>window._ost.childCategories = [
      {'hierarchyDescription':'Rotors','url':'/shop/b/rotors/x'}];</script>"""
    assert child_categories(html) == [
        {"name": "Rotors", "url": "https://www.oreillyauto.com/shop/b/rotors/x"}
    ]
    assert OreillyListingSpider._page_url("https://example.test/cat?x=1", 2).endswith("x=1&page=2")


def test_categories_use_grouped_mapping_contract():
    assert len(OREILLY_CATEGORIES) == 34
    assert all(isinstance(leaves, dict) for leaves in OREILLY_CATEGORIES.values())

    leaves = [
        leaf for group in OREILLY_CATEGORIES.values() for leaf in group
    ]
    assert len(leaves) == sum(len(g) for g in OREILLY_CATEGORIES.values())
    # GCS output paths use the bare leaf name, so leaves stay globally unique.
    assert len(leaves) == len(set(leaves))
    assert "brakes" in OREILLY_CATEGORIES
    assert "brake-drums-rotors" in OREILLY_CATEGORIES["brakes"]

    spider = OreillyListingSpider(category="brake-drums-rotors")
    entry = spider.category_entry("brake-drums-rotors")
    assert entry == {
        "group": "brakes",
        "url": (
            "https://www.oreillyauto.com/shop/b/brakes/"
            "brake-drums---rotors/7145c118aa8d"
        ),
        "category_path": "Brake Drums & Rotors",
        "subcategory": "brake-drums-rotors",
        "department": "Brakes",
        "category": "brake-drums-rotors",
    }
    assert spider.resolve_target_url() == entry["url"]


def test_repeated_child_slug_keeps_department_prefix():
    """`brakes` is both a department key and a child of Performance."""
    spider = OreillyListingSpider(category="performance-brakes")
    entry = spider.category_entry("performance-brakes")
    assert entry["group"] == "performance"
    assert entry["subcategory"] == "brakes"
    assert entry["url"].startswith(
        "https://www.oreillyauto.com/shop/b/performance/brakes/"
    )
