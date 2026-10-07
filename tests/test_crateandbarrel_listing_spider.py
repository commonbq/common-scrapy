import json

from common.spiders.crateandbarrel_listing_spider import CrateandbarrelListingSpider


def test_extract_product_listing_and_js_escapes():
    payload = {"productData": [{"sku": 123, "name": "Kid's Sofa"}], "hasMoreItems": False}
    encoded = json.dumps(payload).replace("'", "\\'")
    html = "ReactDOM.hydrate(React.createElement(ProductListing, JSON.parse('" + encoded + "')), document.getElementById(\"root\"));"
    assert CrateandbarrelListingSpider.extract_product_listing(html) == payload


def test_page_url_replaces_plp_page_and_preserves_query():
    url = "https://www.crateandbarrel.com/furniture/sofas/1?sort=price"
    assert CrateandbarrelListingSpider._page_url(url, 2).endswith("/sofas/2?sort=price")
