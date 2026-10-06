import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.booking_listing_spider import BookingListingSpider


def response(payload, *, url="https://www.booking.com/searchresults.html?city=1", meta=None):
    body = f'<script type="application/json">{json.dumps(payload)}</script>'.encode()
    request = Request(url, meta=meta or {})
    return HtmlResponse(url=url, body=body, encoding="utf-8", request=request)


RESULT = {
    "basicPropertyData": {
        "id": 123, "accommodationTypeId": 204, "pageName": "sample-hotel",
        "location": {"city": "Las Vegas", "countryCode": "us", "latitude": 36.1, "longitude": -115.1},
        "photos": {"main": {"highResUrl": {"relativeUrl": "/xdata/hotel.webp"}}},
        "reviews": {"totalScore": 8.7, "reviewsCount": 42},
        "starRating": {"value": 4},
    },
    "displayName": {"text": "Sample Hotel"},
    "location": {"popularFreeDistrictName": "The Strip"},
    "priceDisplayInfoIrene": {
        "displayPrice": {"amountPerStay": {"amountUnformatted": 199.5, "currency": "USD"}},
        "priceBeforeDiscount": {"amountPerStay": {"amountUnformatted": 249}},
    },
}


class BookingListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = BookingListingSpider(category="las-vegas", max_pages=2)

    def test_categories(self):
        self.assertEqual(len(self.spider.categories), 20)
        self.assertEqual(self.spider.categories[0]["category"], "las-vegas")

    def test_city_handoff_uses_apollo(self):
        payload = {"ROOT_QUERY": {"lxAccommodations({})": {"web": {
            "destination": {"identifier": {"destId": 1}},
            "searchResultSnippet": {"seeAllUrl": "/searchresults.html?city=1&"},
        }}}}
        out = list(self.spider.parse_city(response(payload, url=self.spider.categories[0]["url"], meta={"category": "las-vegas"})))
        self.assertEqual(len(out), 1)
        self.assertIn("rows=25", out[0].url)
        self.assertIn("offset=0", out[0].url)

    def test_search_mapping_and_pagination(self):
        payload = {"ROOT_QUERY": {"searchQueries": {"search({})": {
            "results": [RESULT, RESULT],
            "pagination": {"nbResultsPerPage": 25, "nbResultsTotal": 30},
        }}}}
        out = list(self.spider.parse_search(response(payload, meta={"category": "las-vegas", "page": 1, "dest_id": 1})))
        self.assertEqual(len(out), 2)  # one unique item and one next request
        item = out[0]
        self.assertEqual(item["item_id"], "123")
        self.assertEqual(item["title"], "Sample Hotel")
        self.assertEqual(item["url"], "https://www.booking.com/hotel/us/sample-hotel.html")
        self.assertEqual(item["image_url"], "https://cf.bstatic.com/xdata/hotel.webp")
        self.assertEqual(item["price"], 199.5)
        self.assertEqual(item["source"], "booking_apollo_hydration")
        self.assertIn("offset=25", out[1].url)

    def test_page_url_removes_tracking_and_replaces_pagination(self):
        url = self.spider._page_url("https://www.booking.com/searchresults.html?city=1&aid=x&sid=y&offset=9", 3)
        self.assertNotIn("aid=", url)
        self.assertNotIn("sid=", url)
        self.assertIn("offset=50", url)

    def test_missing_contract_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "expected one Apollo"):
            list(self.spider.parse_search(response({"not": "apollo"}, meta={"page": 1})))

    def test_feed_fields_cover_output(self):
        item = self.spider._item(RESULT, response({}, meta={"category": "las-vegas"}), 1, 1, 30)
        self.assertEqual(set(item), set(self.spider.custom_settings["FEED_EXPORT_FIELDS"]))

    def test_saved_search_fixture(self):
        path = Path(__file__).parents[1] / "sample" / "booking-search-sample.html"
        request = Request("https://www.booking.com/searchresults.html?city=1", meta={
            "category": "las-vegas", "page": 1, "dest_id": 1,
        })
        fixture = HtmlResponse(request.url, body=path.read_bytes(), encoding="utf-8", request=request)
        out = list(self.spider.parse_search(fixture))
        self.assertEqual(out[0]["item_id"], "123")


if __name__ == "__main__":
    unittest.main()
