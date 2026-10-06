import json

import pytest
from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.agoda_listing_spider import AgodaListingSpider


def response(url, body, *, meta=None, html=False, status=200):
    request = Request(url, meta=meta or {})
    cls = HtmlResponse if html else TextResponse
    return cls(url=url, body=body.encode(), encoding="utf-8", request=request, status=status)


def test_config_builds_cronos_request():
    spider = AgodaListingSpider(category="bali")
    body = '<script>geoPageParams = JSON.parse("{\\"pageTypeId\\":5,\\"objectId\\":17193,\\"accommodationTypeId\\":0}");</script>'
    req = list(spider.parse_config(response("https://www.agoda.com/city/bali-id.html", body, meta={"category": "bali"}, html=True)))[0]
    assert "pageTypeId=5&objectId=17193&accommodationType=0&accommodationFeaturesType=1" in req.url
    assert req.headers["Referer"] == b"https://www.agoda.com/city/bali-id.html"


def test_cards_map_normalize_and_deduplicate():
    spider = AgodaListingSpider(category="bali")
    card = {"hotelId": 489045, "hotelUrl": "/rimba/hotel/bali-id.html", "name": "RIMBA", "translatedName": "RIMBA", "imgUrl": "//pix8.agoda.net/a.jpg", "reviewScore": 9.1, "reviewScoreText": "Exceptional", "numberOfReviews": 15617, "starRating": 5, "reviewSnippet": "Great", "customerName": "Sujata", "customerCountry": "United Kingdom"}
    meta = {"category": "bali", "source_url": "https://www.agoda.com/city/bali-id.html", "page_type_id": 5, "object_id": 17193, "accommodation_type_id": 0}
    first = list(spider.parse(response("https://www.agoda.com/api/cronos/geo/accommodations/", json.dumps({"hotelcards": [card]}), meta=meta)))
    second = list(spider.parse(response("https://www.agoda.com/api/cronos/geo/accommodations/", json.dumps({"hotelcards": [card]}), meta=meta)))
    assert first[0]["item_id"] == "489045"
    assert first[0]["url"].startswith("https://www.agoda.com/")
    assert first[0]["image_url"] == "https://pix8.agoda.net/a.jpg"
    assert list(first[0]) == spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert first[0]["timestamp"] is not None
    assert second == []


@pytest.mark.parametrize("body", ["", "Pardon the Interruption", "<html>captcha</html>"])
def test_challenge_and_empty_responses_fail(body):
    spider = AgodaListingSpider(category="bali")
    with pytest.raises(RuntimeError):
        list(spider.parse_config(response("https://www.agoda.com/city/bali-id.html", body, meta={"category": "bali"}, html=True)))


def test_malformed_hydration_and_empty_cards_fail():
    spider = AgodaListingSpider(category="bali")
    with pytest.raises(RuntimeError, match="malformed"):
        spider.extract_geo_params('geoPageParams = JSON.parse("nope")')
    meta = {"category": "bali", "source_url": "x", "page_type_id": 5, "object_id": 17193, "accommodation_type_id": 0}
    with pytest.raises(RuntimeError, match="empty"):
        list(spider.parse(response("https://www.agoda.com/api/cronos/geo/accommodations/", '{"hotelcards":[]}', meta=meta)))

