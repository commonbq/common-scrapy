import json

from scrapy.http import Request, TextResponse

from common.spiders.klook_categories import KLOOK_CATEGORIES
from common.spiders.klook_listing_spider import KlookListingSpider


def response(url, body, **meta):
    request = Request(url, meta=meta)
    if not isinstance(body, bytes):
        body = body.encode()
    return TextResponse(url, request=request, body=body, encoding="utf-8")


def test_categories_and_xhr_discovery():
    assert len(KLOOK_CATEGORIES) == 20
    spider = KlookListingSpider(category="japan")
    html = '<script>window.__KLOOK__=' + json.dumps({"data": [{"pageData": {"page": {"body": {"sections": [
        {"data_type": "other"}, {"body": {"content": {"data_type": "ttd_acts", "src": "/v1/acts?dest_id=1012"}}}
    ]}}}}]}) + ';</script>'
    req = list(spider.parse_destination(response("https://www.klook.com/en-US/destination/co1012-japan/", html, category="japan")))[0]
    assert req.url == "https://www.klook.com/v1/acts?dest_id=1012"
    assert req.headers["Accept"] == b"application/json"


def test_item_export_and_currency():
    spider = KlookListingSpider(category="japan")
    data = {"vertical_id": 46604, "vertical_type": 100, "title": "Universal Studios Japan Studio Pass",
            "category": "Theme parks", "city_name": "Osaka", "deep_link": "https://www.klook.com/activity/46604",
            "cover_url": "https://res.klook.com/a.jpg", "price": {"selling_price": "HK$ 683", "market_price": "HK$ 700"},
            "review_obj": {"star": "4.8", "count": "89.6K+ reviews", "booked": "6M+ booked"}, "sold_out": False}
    payload = {"success": True, "result": {"total": 1000, "has_more": True, "corner_button_deep_link": "https://www.klook.com/more", "items": [{"data": data}]}}
    item = list(spider.parse_activities(response("https://www.klook.com/v1/acts", json.dumps(payload), category="japan", listing_url="https://www.klook.com/japan")))[0]
    assert list(item) == spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert (item["item_id"], item["price"], item["currency"], item["rating"]) == ("46604", 683.0, "HKD", 4.8)


def test_hydration_errors_are_loud():
    try:
        KlookListingSpider._state("<html></html>")
    except RuntimeError as error:
        assert "missing" in str(error)
    else:
        raise AssertionError("missing hydration accepted")
