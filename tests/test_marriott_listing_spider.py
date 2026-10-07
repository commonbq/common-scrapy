import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.marriott_listing_spider import MarriottListingSpider


HOTEL = {
    "id": "MIAJW",
    "brandCode": "JW",
    "titleDetails": {
        "title": "JW Marriott Miami",
        "titleLink": "/en-us/hotels/travel/miajw-jw-marriott-miami",
    },
    "reviewsDetails": {
        "reviewsAvg": 3.7,
        "reviewsText": "(1,715 reviews)",
        "reviewsLink": "/en-us/hotels/miajw-jw-marriott-miami/reviews/",
        "milesText": "0.1 mi from destination",
    },
    "description": "A hotel in Brickell.",
    "images": [{"defaultImageUrl": "https://cache.marriott.com/hotel.jpg", "altText": "Pool"}],
    "footerLinkDetails": {
        "href": "/reservation/availabilitySearch.mi?propertyCode=MIAJW",
        "hasPrice": True,
        "priceValue": 399.0,
        "currency": "USD",
        "isHotelUnavailable": False,
    },
    "isHotelBookable": True,
}


def fixture(hotels=None, *, total=138, page=1):
    processed = {"hotels": hotels if hotels is not None else [HOTEL], "totalProperties": total}
    payload = {"props": {"pageProps": {"model": {
        ":items": {"propertieslist": {"processedData": processed}}
    }}}}
    body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'.encode()
    url = "https://www.marriott.com/en-us/destinations/united-states/florida/miami.mi"
    request = Request(url, meta={"category": "miami", "page": page})
    return HtmlResponse(url=url, body=body, encoding="utf-8", request=request)


class MarriottListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = MarriottListingSpider(category="miami", max_pages=2)

    def test_categories(self):
        self.assertEqual(len(self.spider.categories), 20)
        self.assertEqual(self.spider.categories[2]["category"], "miami")

    def test_bootstrap_mapping_and_pagination(self):
        output = list(self.spider.parse(fixture()))
        self.assertEqual(len(output), 2)
        item, request = output
        self.assertEqual(item["item_id"], "MIAJW")
        self.assertEqual(item["title"], "JW Marriott Miami")
        self.assertEqual(item["rating"], 3.7)
        self.assertEqual(item["reviews_count"], 1715)
        self.assertEqual(item["distance_miles"], 0.1)
        self.assertEqual(item["price"], 399)
        self.assertEqual(item["source"], "marriott_next_data_hydration")
        self.assertEqual(request.url, fixture().url + "?pg=2")

    def test_repeated_id_stops_pagination(self):
        list(self.spider.parse(fixture()))
        self.assertEqual(list(self.spider.parse(fixture(page=2))), [])

    def test_missing_hydration_fails_loudly(self):
        request = Request(fixture().url, meta={"category": "miami", "page": 1})
        response = HtmlResponse(request.url, body=b"<html></html>", request=request)
        with self.assertRaisesRegex(RuntimeError, "__NEXT_DATA__ missing"):
            list(self.spider.parse(response))

    def test_feed_fields_cover_output(self):
        item = next(iter(self.spider.parse(fixture(total=1))))
        self.assertEqual(set(item), set(self.spider.custom_settings["FEED_EXPORT_FIELDS"]))


if __name__ == "__main__":
    unittest.main()
