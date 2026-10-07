from urllib.parse import parse_qs, urlsplit

import pytest
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, TextResponse

from common.spiders.worldmarket_listing_spider import WorldmarketListingSpider


CATEGORY_HTML = """
<html><body><a href="/on/demandware.store/Sites-World_Market-Site/en_US/Search-UpdateGrid?cgid=116745&amp;start=60&amp;sz=60">more</a></body></html>
"""

API_HTML = """
<html><body>
<option data-url="https://www.worldmarket.com/on/demandware.store/Sites-World_Market-Site/en_US/Search-UpdateGrid?cgid=116745&amp;count=121&amp;start=60&amp;sz=60"></option>
<div class="product js-a-tile-data" data-pid="null" data-collection-id="SET135122"
 data-id="SET135122" data-sku="135122" data-online-status="in stock"
 data-rating="5.00" data-reviews="2" data-sale-tag="true"
 data-product-name="Isaiah Seating Collection" data-image-url="https://img.example/item.jpg">
 <a class="js-a-product-click" href="/p/isaiah-seating-collection-SET135122.html"></a>
 <div class="price"><span class="value" content="299.99"></span><span class="value" content="799.99"></span></div>
</div>
<div class="product js-a-tile-data" data-id="137944" data-sku="137944"
 data-product-name="Clive Swivel Chair" data-online-status="out of stock">
 <a href="/p/clive-chair-137944.html"></a><div class="price"><span class="value">$249.99</span></div>
</div>
</body></html>
"""


def response(url, body, meta=None, status=200):
    request = Request(url, meta=meta or {})
    return TextResponse(url=url, request=request, body=body.encode(), encoding="utf-8", status=status)


def spider(max_pages=2):
    return WorldmarketListingSpider(category="furniture-shop-all-furniture", max_pages=max_pages)


def test_start_and_category_handoff_use_api_start_zero():
    subject = spider()
    initial = list(subject.start_requests())[0]
    result = list(subject.parse_category(response(initial.url, CATEGORY_HTML, initial.meta)))
    assert len(result) == 1
    assert parse_qs(urlsplit(result[0].url).query) == {"cgid": ["116745"], "start": ["0"], "sz": ["60"]}
    assert result[0].headers["X-Requested-With"] == b"XMLHttpRequest"


def test_api_extracts_contract_and_paginates():
    subject = spider()
    meta = {"category": "furniture-shop-all-furniture", "category_url": "https://www.worldmarket.com/c/furniture/shop-all-furniture/", "category_id": "116745", "start": 0}
    results = list(subject.parse_api(response("https://www.worldmarket.com/api", API_HTML, meta)))
    assert len(results) == 3
    first = results[0]
    assert first["item_id"] == "SET135122"
    assert first["price"] == 299.99
    assert first["original_price"] == 799.99
    assert first["is_sale"] is True
    assert first["rating"] == 5.0
    assert first["reviews_count"] == 2
    assert first["source"] == "worldmarket_sfcc_search_update_grid_api"
    assert set(subject.custom_settings["FEED_EXPORT_FIELDS"]) == set(first)
    assert parse_qs(urlsplit(results[-1].url).query)["start"] == ["60"]


def test_max_pages_and_duplicate_suppression():
    subject = spider(max_pages=1)
    meta = {"category": "furniture-shop-all-furniture", "category_url": "x", "category_id": "116745", "start": 0}
    first = list(subject.parse_api(response("https://www.worldmarket.com/api", API_HTML, meta)))
    second = list(subject.parse_api(response("https://www.worldmarket.com/api", API_HTML, meta)))
    assert len(first) == 2
    assert second == []


@pytest.mark.parametrize("status,body", [(403, "denied"), (200, "Pardon Our Interruption")])
def test_fail_loudly_on_error_or_challenge(status, body):
    with pytest.raises(CloseSpider):
        list(spider().parse_category(response("https://www.worldmarket.com/c/furniture/", body, status=status)))


def test_api_fails_loudly_on_empty_product_payload():
    meta = {"category": "furniture", "category_url": "x", "category_id": "116745", "start": 0}
    with pytest.raises(CloseSpider):
        list(spider().parse_api(response("https://www.worldmarket.com/api", "<html></html>", meta)))
