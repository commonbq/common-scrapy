import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.dell_listing_spider import DellListingSpider


def response(body):
    request = Request("https://www.dell.com/list", meta={"category": "view-all-laptops"})
    return HtmlResponse(request.url, body=body.encode(), encoding="utf-8", request=request)


def test_bootstrap_items_and_duplicate_suppression():
    spider = DellListingSpider(category="view-all-laptops")
    products = {
        "p1": {"productId": "p1", "title": "Dell 16 Plus", "dellPrice": "$1,559.99",
               "marketPrice": "$1,799.99", "pdUrl": "/en-us/shop/p1",
               "image": "https://i.dell.com/p1.png", "badges": {"ShowHotDeal": True}},
        "alias": {"productId": "p1", "title": "duplicate", "dellPrice": "$1"},
    }
    encoded = json.dumps(products).replace('"', "&quot;")
    body = f'<div id="ps-wrapper" data-product-detail-info="{encoded}"></div><script>window.TotalItem = "85";</script>'
    items = list(spider.parse_bootstrap(response(body)))
    assert len(items) == 1
    assert items[0]["item_id"] == "p1"
    assert items[0]["price"] == 1559.99
    assert items[0]["regular_price"] == 1799.99
    assert items[0]["source"] == "dell_product_stack_bootstrap"
    assert items[0]["total_count"] == 85


def test_missing_bootstrap_fails_loudly():
    spider = DellListingSpider(category="view-all-laptops")
    with pytest.raises(RuntimeError, match="no Product Stack bootstrap"):
        list(spider.parse_bootstrap(response("<html></html>")))


def test_export_fields_are_ordered():
    fields = DellListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
    assert fields[:6] == ["category", "item_id", "offer_id", "title", "url", "image"]
    assert fields[-3:] == ["source_url", "raw", "timestamp"]
