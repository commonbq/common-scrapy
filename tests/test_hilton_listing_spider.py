import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.hilton_listing_spider import HiltonListingSpider


def response(hotels, status=200):
    state = {"props": {"pageProps": {"pageData": {"hotelSummaryOptions": {"hotels": hotels}}}}}
    url = "https://www.hilton.com/en/locations/usa/new-york/new-york/"
    request = Request(url)
    body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(state)}</script>'
    return HtmlResponse(url, body=body, status=status, encoding="utf-8", request=request)


def hotel(item_id="NYCTEPO"):
    return {
        "ctyhocn": item_id, "name": "Tempo by Hilton New York Times Square",
        "brandCode": "PO", "facilityOverview": {"homeUrlTemplate": "/en/hotels/nyctepo-tempo/"},
        "address": {"addressFmt": "1568 Broadway", "city": "New York", "state": "NY", "postalCode": "10036"},
        "localization": {"currencyCode": "USD", "coordinate": {"latitude": 40.76, "longitude": -73.98}},
        "leadRate": {"lowest": {"rateAmount": 299, "rateAmountFmt": "$299", "ratePlan": {"ratePlanName": "Flexible"}}},
        "images": {"master": {"ratios": [{"size": "threeByTwo", "url": "https://img.test/hotel.jpg"}]}},
        "amenityIds": ["free-wifi"], "display": {"open": True},
    }


def test_maps_next_data_hotel_and_feed_contract():
    spider = HiltonListingSpider(category="new-york-ny")
    item = list(spider.parse(response([hotel()])))[0]
    assert item["item_id"] == "NYCTEPO"
    assert item["url"] == "https://www.hilton.com/en/hotels/nyctepo-tempo/"
    assert item["price"] == 299
    assert item["photo"] == "https://img.test/hotel.jpg"
    assert item["source"] == "hilton_next_data"
    assert list(item) == spider.custom_settings["FEED_EXPORT_FIELDS"]


def test_deduplicates_by_property_code():
    spider = HiltonListingSpider(category="new-york-ny")
    assert len(list(spider.parse(response([hotel(), hotel()])))) == 1


@pytest.mark.parametrize("body", ["<html></html>", "captcha", '<script id="__NEXT_DATA__">{}</script>'])
def test_rejects_missing_invalid_or_challenge_payload(body):
    spider = HiltonListingSpider(category="new-york-ny")
    page = HtmlResponse("https://www.hilton.com/x", body=body, encoding="utf-8")
    with pytest.raises(RuntimeError):
        list(spider.parse(page))
