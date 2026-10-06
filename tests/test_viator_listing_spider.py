import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.viator_listing_spider import ViatorListingSpider


def response_for(payload=None, body=None):
    if body is None:
        body = f'<script type="mime/invalid">{json.dumps(payload)}</script>'
    request = Request("https://www.viator.com/Nashville/d799", meta={"category": "nashville"})
    return HtmlResponse(request.url, request=request, body=body.encode(), encoding="utf-8")


def product(code="5046NASH_OTT"):
    return {
        "code": code, "title": "Nashville Hop On Hop Off Trolley Tour",
        "description": "See Nashville's highlights.", "location": "Nashville, Tennessee",
        "category": "Private and Luxury", "url": "/tours/Nashville/example",
        "images": [{"url": "https://media.example/tour.jpg", "srcset": "tour-2x.jpg 2x"}],
        "rating": {"score": 4.5, "exactScore": 4.55, "reviewCount": 6173},
        "price": {
            "retailPrice": {"currencyCode": "USD", "currencySymbol": "$", "amount": 60.0},
            "discountedPrice": {"currencyCode": "USD", "currencySymbol": "$", "amount": 53.72},
            "discountAmount": {"amount": 6.28}, "isDiscounted": True,
        },
        "languages": ["en"],
        "displayDuration": {"duration": {"days": 0, "hours": 1, "minutes": 50}},
        "behaviours": {"hasFreeCancellation": True, "isPrivateTour": False},
        "badges": ["Likely to Sell Out"], "geolocation": {"latitude": 36.1613, "longitude": -86.7785},
    }


def payload(products):
    return {"__PRELOADED_DATA__": {"pageModel": {"topActivities": products}}}


def test_parses_preload_exact_price_and_normalizes_url():
    spider = ViatorListingSpider(category="nashville")
    items = list(spider.parse(response_for(payload([product()]))))
    assert len(items) == 1
    item = items[0]
    assert item["price"] == 53.72
    assert item["original_price"] == 60.0
    assert item["url"] == "https://www.viator.com/tours/Nashville/example"
    assert item["duration"] == "1 hours 50 minutes"
    assert item["rating"] == 4.55
    assert list(item) == spider.custom_settings["FEED_EXPORT_FIELDS"]


def test_optional_fields_and_duplicates():
    first = product()
    for key in ("description", "images", "badges", "geolocation"):
        first.pop(key)
    spider = ViatorListingSpider(category="nashville")
    items = list(spider.parse(response_for(payload([first, product()]))))
    assert len(items) == 1
    assert items[0]["description"] is None
    assert items[0]["image_url"] is None


@pytest.mark.parametrize("body, message", [
    ("<html></html>", "is absent"),
    ('<script type="mime/invalid">{"__PRELOADED_DATA__":</script>', "malformed JSON"),
    ('<script type="mime/invalid">{"__PRELOADED_DATA__": {}}</script>', "missing pageModel.topActivities"),
])
def test_bad_preload_fails(body, message):
    spider = ViatorListingSpider(category="nashville")
    with pytest.raises(RuntimeError, match=message):
        list(spider.parse(response_for(body=body)))


def test_empty_top_activities_fails():
    spider = ViatorListingSpider(category="nashville")
    with pytest.raises(RuntimeError, match="no topActivities records"):
        list(spider.parse(response_for(payload([]))))
