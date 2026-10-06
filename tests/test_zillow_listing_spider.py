import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.zillow_listing_spider import ZillowListingSpider


def page(items, current=1):
    state = {"props": {"isBot": False, "pageProps": {"searchPageState": {
        "queryState": {"pagination": {"currentPage": current}},
        "regionState": {"regionInfo": [{"regionId": 39051, "displayName": "Houston TX"}]},
        "categoryTotals": {"cat1": {"totalResultCount": 2}},
        "cat1": {"searchResults": {"listResults": items}},
    }}}}
    return f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(state)}</script>'


def response(spider, body, page_number=1):
    request = Request("https://www.zillow.com/homes/for_sale/Houston-TX/", meta={
        "page": page_number, "base_url": "https://www.zillow.com/homes/for_sale/Houston-TX/"
    })
    return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)


def test_maps_hydrated_listing():
    spider = ZillowListingSpider(category="houston-tx")
    product = {"zpid": "123", "detailUrl": "/homedetails/x/123_zpid/", "address": "1 Main St",
               "unformattedPrice": 500000, "beds": 3, "baths": 2, "area": 1500,
               "latLong": {"latitude": 1, "longitude": 2},
               "hdpData": {"homeInfo": {"homeType": "SINGLE_FAMILY"}}}
    outputs = list(spider.parse(response(spider, page([product]))))
    item = outputs[0]
    assert item["item_id"] == "123"
    assert item["url"] == "https://www.zillow.com/homedetails/x/123_zpid/"
    assert item["home_type"] == "SINGLE_FAMILY"
    assert item["region_id"] == 39051


def test_page_url_uses_server_rendered_path():
    url = "https://www.zillow.com/homes/for_sale/Houston-TX/"
    assert ZillowListingSpider._page_url(url, 2).endswith("/Houston-TX/2_p/")
    assert ZillowListingSpider._page_url(ZillowListingSpider._page_url(url, 2), 3).endswith("/Houston-TX/3_p/")


def test_deduplicates_and_stops_repeated_page():
    spider = ZillowListingSpider(category="houston-tx", max_pages=2)
    product = {"zpid": "123", "address": "1 Main St"}
    assert len(list(spider.parse(response(spider, page([product]))))) == 2
    assert list(spider.parse(response(spider, page([product], 2), 2))) == []


@pytest.mark.parametrize("body", ["Pardon the Interruption", "<html></html>"])
def test_rejects_challenge_or_missing_hydration(body):
    spider = ZillowListingSpider(category="houston-tx")
    with pytest.raises(RuntimeError):
        list(spider.parse(response(spider, body)))
