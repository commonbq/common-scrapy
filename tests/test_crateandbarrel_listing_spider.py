import json

from common.spiders.crateandbarrel_listing_spider import CrateandbarrelListingSpider


def make_spider(category="furniture-sofas"):
    return CrateandbarrelListingSpider(category=category)


def test_categories_are_grouped_and_unique():
    spider = make_spider()
    # Grouped {department: {leaf: url}} mapping built from the full sitemap
    # taxonomy: 35 departments / 1884 crawlable leaves.
    assert len(spider._all_category_entries()) == 35
    assert len(list(spider.iter_categories())) == 1884
    # A department-prefixed leaf is globally unique (DAG/GCS output paths use
    # the bare leaf name); a bare label resolves across every group.
    assert spider.category_entry("furniture-sofas")["url"].endswith("/furniture/sofas/1")
    assert spider.category_entry("kids-beds")["url"].endswith("/kids/beds/1")
    assert spider.category_entry("furniture-beds")["url"].endswith("/furniture/beds/1")
    assert spider.category_entry("does-not-exist") is None


def test_resolve_target_url_uses_grouped_leaf():
    spider = make_spider("kids-beds")
    assert spider.resolve_target_url() == "https://www.crateandbarrel.com/kids/beds/1"


def test_extract_product_listing_and_js_escapes():
    payload = {"productData": [{"sku": 123, "name": "Kid's Sofa"}], "hasMoreItems": False}
    encoded = json.dumps(payload).replace("'", "\\'")
    html = "ReactDOM.hydrate(React.createElement(ProductListing, JSON.parse('" + encoded + "')), document.getElementById(\"root\"));"
    assert CrateandbarrelListingSpider.extract_product_listing(html) == payload


def test_page_url_replaces_plp_page_and_preserves_query():
    url = "https://www.crateandbarrel.com/furniture/sofas/1?sort=price"
    assert CrateandbarrelListingSpider._page_url(url, 2).endswith("/sofas/2?sort=price")
