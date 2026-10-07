import html
import json

from scrapy.http import HtmlResponse, Request

from common.spiders.tripcom_listing_spider import TripcomListingSpider


def test_city_bootstrap_items():
    state = {"cityId": 359, "cityName": "Bangkok", "hotels": [
        {"hotelName": "Example Hotel", "price": "$15", "priceUnit": "1 night"}]}
    data = html.escape(json.dumps(state), quote=True)
    body = f'<div data-type="template-comp" data-name="City" data-jsondata="{data}"></div>' + (" " * 5000)
    request = Request("https://us.trip.com/hotels/bangkok-hotels-list-359/")
    response = HtmlResponse(request.url, body=body.encode(), encoding="utf-8", request=request)
    item = list(TripcomListingSpider(category="bangkok").parse(response))[0]
    assert (item["title"], item["price"], item["currency"], item["city_id"]) == ("Example Hotel", 15, "USD", 359)
    assert item["source"] == "tripcom_city_component_bootstrap"
    assert item["raw"] == state["hotels"][0]
    assert item["timestamp"]
    assert list(item) == TripcomListingSpider.custom_settings["FEED_EXPORT_FIELDS"]


def test_price_parser():
    assert TripcomListingSpider._price("$1,234") == (1234, "USD")
    assert TripcomListingSpider._price("") == (None, None)
