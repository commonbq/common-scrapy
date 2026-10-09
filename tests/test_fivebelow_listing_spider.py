import json

import pytest
from scrapy.http import Request, TextResponse

from common.spiders.fivebelow_listing_spider import FiveBelowListingSpider


CONFIG = {
    "indexName": "prod-ct-products",
    "batchSize": 24,
    "appId": "TESTAPP",
    "searchApiKey": "test-key",
}


def discovery_response():
    flight = f'0:{{"algoliaConfig":{json.dumps(CONFIG)}}}'
    state = {
        "prod-ct-products": {
            "requestParams": [{
                "facetFilters": [["categories.en-US.lvl0:New & Now"]],
                "facets": ["categories.en-US.lvl0"],
                "hitsPerPage": 24,
            }]
        }
    }
    html = (
        f"<script>self.__next_f.push([1,{json.dumps(flight)}])</script>"
        '<script>window[Symbol.for("InstantSearchInitialResults")] = '
        f"{json.dumps(state)}</script>"
    )
    request = Request(
        "https://www.fivebelow.com/categories/new-and-now",
        meta={"category": "new-and-now", "listing_url": "https://www.fivebelow.com/categories/new-and-now"},
    )
    return TextResponse(request.url, request=request, body=html, encoding="utf-8")


def api_response(*, page=0, pages=2):
    hit = {
        "objectID": "product-1",
        "name": {"en-US": "Squishy Duck Cube"},
        "description": {"en-US": "<p>A squishy duck.</p>"},
        "slug": {"en-US": "squishy-duck-cube-9259448"},
        "categories": {"en-US": {"lvl0": ["New & Now"], "lvl1": ["New & Now > Toys"]}},
        "variants": [{
            "id": 1,
            "sku": "9259449",
            "images": ["https://www.fivebelow.com/v3/assets/9259449_01.jpg"],
            "inventory": {"100": 2, "101": 1},
            "prices": {"USD": {"priceValues": [{"value": 300}], "min": 300, "max": 500}},
            "attributes": {
                "styleNumber": "9259448", "fmBrand": ["Five Below"],
                "productState": "available", "department": "GAMES & TOYS",
                "subDepartment": "IMPULSE", "class": "NOVELTY",
                "subclass": "Squishies", "localDelivery": "true",
                "orderLimitQuantity": 5, "releaseDateTime": "2026-09-18",
            },
        }],
    }
    request = Request(
        "https://TESTAPP-dsn.algolia.net/1/indexes/*/queries",
        method="POST",
        meta={
            "category": "new-and-now",
            "listing_url": "https://www.fivebelow.com/categories/new-and-now",
            "config": CONFIG,
            "params": {"hitsPerPage": 24},
        },
    )
    body = {"results": [{"hits": [hit], "page": page, "nbPages": pages, "nbHits": 30}]}
    return TextResponse(request.url, request=request, body=json.dumps(body), encoding="utf-8")


def test_discovery_builds_first_api_request():
    spider = FiveBelowListingSpider(category="new-and-now")
    request = list(spider.parse_discovery(discovery_response()))[0]
    assert request.url == "https://testapp-dsn.algolia.net/1/indexes/*/queries"
    body = json.loads(request.body)
    assert body["requests"][0]["indexName"] == "prod-ct-products"
    assert "page=0" in body["requests"][0]["params"]


def test_maps_variant_and_feed_contract():
    spider = FiveBelowListingSpider(category="new-and-now", max_pages=1)
    output = list(spider.parse_api(api_response()))
    assert len(output) == 1
    item = output[0]
    assert item["item_id"] == "9259449"
    assert item["price"] == 3.0
    assert item["max_price"] == 5.0
    assert item["brand"] == "Five Below"
    assert item["in_stock"] is True
    assert item["inventory_store_count"] == 2
    assert item["url"].endswith("/products/squishy-duck-cube-9259448")
    assert set(item) | {"timestamp"} == set(spider.custom_settings["FEED_EXPORT_FIELDS"])


def test_paginates_algolia_load_more():
    spider = FiveBelowListingSpider(category="new-and-now", max_pages=2)
    output = list(spider.parse_api(api_response()))
    assert output[-1].meta["page"] == 1
    assert "page=1" in json.loads(output[-1].body)["requests"][0]["params"]


def test_unknown_category_fails_loudly():
    with pytest.raises(ValueError, match="Unknown category"):
        FiveBelowListingSpider(category="missing")._selected_category()


def test_defaults_to_first_category():
    assert FiveBelowListingSpider()._selected_category()["category"] == "new-and-now"


def test_missing_hydration_fails_loudly():
    response = TextResponse("https://www.fivebelow.com/categories/new-and-now", body=b"<html></html>", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Algolia config"):
        list(FiveBelowListingSpider(category="new-and-now").parse_discovery(response))
