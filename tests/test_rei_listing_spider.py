import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.rei_listing_spider import ReiListingSpider


def response(payload, *, page=1):
    body = '<script type="application/json" id="initial-props">' + json.dumps(payload) + "</script>"
    request = Request("https://www.rei.com/c/hiking-footwear", meta={"category": "hiking-footwear", "page": page})
    return HtmlResponse(request.url, request=request, body=body, encoding="utf-8")


def payload(products, next_query=None):
    return {"ProductSearch": {"products": {"searchResults": {
        "results": products,
        "query": {"totalResults": 754},
        "pagination": {"nextPage": {"queryString": next_query}},
    }}}}


PRODUCT = {
    "prodId": "202126", "brand": "Merrell", "title": "Moab 3 Hiking Shoes - Women's",
    "link": "/product/202126/merrell-moab-3-hiking-shoes-womens",
    "thumbnailImageLink": "https://www.rei.com/media/product/202126", "regularPrice": "145.0",
    "sale": False, "partialClearance": True, "clearance": False, "available": True,
    "rating": "4.6481", "reviewCount": "2296", "displayPrice": {"min": 71.83, "max": 145},
}


def test_maps_hydrated_product_and_feed_contract():
    spider = ReiListingSpider(category="hiking-footwear", max_pages=1)
    items = list(spider.parse(response(payload([PRODUCT]))))
    assert len(items) == 1
    item = items[0]
    assert list(item) == spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert (item["item_id"], item["brand"], item["price"], item["reviews_count"]) == ("202126", "Merrell", 71.83, 2296)
    assert item["source"] == "rei_initial_props_bootstrap"


def test_follows_hydrated_next_page_and_deduplicates():
    spider = ReiListingSpider(category="hiking-footwear", max_pages=2)
    output = list(spider.parse(response(payload([PRODUCT], "?page=2"))))
    assert output[1].url.endswith("?page=2")
    assert list(spider.parse(response(payload([PRODUCT]), page=2))) == []


def test_missing_bootstrap_fails_loudly():
    spider = ReiListingSpider(category="hiking-footwear")
    request = Request("https://www.rei.com/c/hiking-footwear", meta={"category": "hiking-footwear", "page": 1})
    blocked = HtmlResponse(request.url, request=request, body=b"<html></html>", encoding="utf-8")
    with pytest.raises(RuntimeError, match="initial-props"):
        list(spider.parse(blocked))
