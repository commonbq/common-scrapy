import json

from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.redfin_categories import REDFIN_CATEGORIES
from common.spiders.redfin_listing_spider import RedfinListingSpider


def gis(homes):
    return {"resultCode": 0, "payload": {"homes": homes}}


def test_categories_and_feed_contract():
    spider = RedfinListingSpider(category="los-angeles-ca")
    assert len(REDFIN_CATEGORIES) == 20
    assert spider.custom_settings["FEED_EXPORT_FIELDS"][-2:] == ["source", "raw"]


def test_hydration_discovers_cached_api_response():
    payload = "{}&&" + json.dumps(gis([{"propertyId": 12}]))
    state = {"ReactServerAgent.cache": {"dataCache": {
        "/stingray/api/gis?region_id=11203&page_number=1&start=0": {"res": {"text": payload}}
    }}}
    html = f"<script>root.__reactServerState.InitialContext = {json.dumps(state)};</script>"
    decoded = RedfinListingSpider._initial_context(html)
    url, response = RedfinListingSpider._cached_gis(decoded)
    assert "region_id=11203" in url
    assert response["payload"]["homes"][0]["propertyId"] == 12


def test_parse_maps_items_and_builds_second_page_request():
    spider = RedfinListingSpider(category="los-angeles-ca", max_pages="2")
    payload = gis([{
        "propertyId": 5196541, "listingId": 224110415,
        "mlsId": {"value": "SR1"}, "streetLine": "13229 Margate St",
        "city": "Sherman Oaks", "state": "CA", "zip": "91401",
        "price": {"value": 1399000}, "beds": 3, "baths": 2.5,
        "sqFt": {"value": 1905}, "url": "/home/5196541",
    }])
    state = {"cache": {"/stingray/api/gis?region_id=11203&page_number=1&start=0": {"text": "{}&&" + json.dumps(payload)}}}
    request = Request("https://www.redfin.com/city/11203/CA/Los-Angeles", meta={
        "category": "los-angeles-ca", "page": 1,
        "listing_url": "https://www.redfin.com/city/11203/CA/Los-Angeles",
    })
    response = HtmlResponse(request.url, request=request, encoding="utf-8", body=(
        "root.__reactServerState.InitialContext = " + json.dumps(state) + ";"
    ).encode())
    output = list(spider.parse(response))
    assert output[0]["item_id"] == "5196541"
    assert output[0]["price"] == 1399000
    assert output[0]["source"] == "redfin_stingray_api"
    assert output[1].url.endswith("page_number=2&start=1")


def test_api_prefix_and_deduplication():
    spider = RedfinListingSpider(category="los-angeles-ca")
    meta = {"category": "los-angeles-ca", "page": 1}
    response = TextResponse("https://www.redfin.com/stingray/api/gis", encoding="utf-8")
    home = {"propertyId": 1, "url": "/home/1"}
    assert len(list(spider._emit(gis([home, home]), meta, response))) == 1
    assert RedfinListingSpider._decode_gis("{}&&" + json.dumps(gis([])))["resultCode"] == 0


def test_missing_hydration_fails_loudly():
    try:
        RedfinListingSpider._initial_context("<html></html>")
    except RuntimeError as exc:
        assert "missing" in str(exc)
    else:
        raise AssertionError("missing state did not fail")
