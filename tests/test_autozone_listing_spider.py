import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.autozone_listing_spider import AutozoneListingSpider


def response(payload, page=1):
    url = "https://www.autozone.com/filters-and-pcv/oil-filter"
    body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'
    request = Request(url, meta={"category": "oil-filter", "page": page, "listing_url": url})
    return HtmlResponse(url, request=request, body=body.encode(), encoding="utf-8")


def payload(last=24, total=30):
    records = [{"itemId": "1117175", "itemDescription": "STP Oil Filter S45023",
                "brandName": "STP", "partNumber": "S45023",
                "productDetailsPageUrl": "/p/stp-engine-oil-filter-s45023/1117175",
                "productImageUrl": "https://img.test/filter.jpg", "sponsoredProductFlag": False}]
    shelf = {"queryKey": ["productshelf-results"], "state": {"data": {"pages": [
        {"productShelfResults": {"skuRecords": records, "lastRecordNumber": last,
                                  "totalNumberOfRecords": total}}
    ]}}}
    details = {"queryKey": ["productSkuDetails"], "state": {"data": {"items": [
        {"itemId": "1117175", "price": {"value": 9.99},
         "availability": "IN_STOCK", "inStock": True}
    ]}}}
    return {"props": {"pageProps": {"dehydratedState": {"queries": [shelf, details]}}}}


def test_maps_hydration_and_paginates():
    spider = AutozoneListingSpider(category="oil-filter", max_pages=2)
    output = list(spider.parse(response(payload())))
    item, request = output
    assert list(item) == spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert item["item_id"] == "1117175"
    assert item["price"] == 9.99
    assert item["url"].endswith("/1117175")
    assert request.url.endswith("?page=2")


def test_stops_at_total_and_deduplicates():
    spider = AutozoneListingSpider(category="oil-filter", max_pages=3)
    assert len(list(spider.parse(response(payload(last=30, total=30))))) == 1
    assert list(spider.parse(response(payload(last=30, total=30)))) == []


@pytest.mark.parametrize("mutator,message", [
    (lambda p: p["props"]["pageProps"]["dehydratedState"]["queries"].pop(0), "productshelf"),
    (lambda p: p["props"]["pageProps"]["dehydratedState"]["queries"].pop(), "SKU details"),
])
def test_missing_queries_fail_loudly(mutator, message):
    data = payload(); mutator(data)
    with pytest.raises(RuntimeError, match=message):
        list(AutozoneListingSpider(category="oil-filter").parse(response(data)))


def test_missing_or_malformed_next_data_fails_loudly():
    url = "https://www.autozone.com/filters-and-pcv/oil-filter"
    blank = HtmlResponse(url, request=Request(url), body=b"", encoding="utf-8")
    with pytest.raises(RuntimeError, match="no __NEXT_DATA__"):
        AutozoneListingSpider._next_data(blank)


def test_proxy_options_are_idempotent():
    spider = AutozoneListingSpider(category="oil-filter")
    spider.settings = {"PROXY": "http://scrapeops.country=us.residential=true:key@proxy.scrapeops.io:5353"}
    proxy = spider._residential_proxy()
    assert proxy.count("country=us") == 1
    assert proxy.count("residential=true") == 1


def test_category_discovery():
    data = {"props": {"pageProps": {"topNavProductData": {"rootCategories": [
        {"name": "Brakes", "url": "/brakes-and-traction-control"}]}}}}
    assert AutozoneListingSpider.discover_categories(data) == [{
        "category": "Brakes", "url": "https://www.autozone.com/brakes-and-traction-control"}]
