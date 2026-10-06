import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.getyourguide_categories import GETYOURGUIDE_CATEGORIES
from common.spiders.getyourguide_listing_spider import GetYourGuideListingSpider


def product(item_id=1220349, **updates):
    value = {
        "id": item_id,
        "tour_id": item_id,
        "title": "Perito Moreno Glacier Boat Tour",
        "activity_abstract": "Cruise beside the glacier.",
        "url": f"/el-calafate-l544/example-t{item_id}/?ranking_uuid=track",
        "review_statistics": {"quantity": 18, "rating": 4.877572},
        "price": {
            "base_price": 50,
            "starting_price": 49.5,
            "currency": "USD",
            "currency_symbol": "$",
            "price_category": "individual",
            "price_category_label": "per person",
        },
        "category": "guidedTour",
        "activity_type": "guidedTour",
        "attributes": [{"type": "duration", "label": "1 hour"}],
        "availability": {"message": "Available tomorrow", "next_available_date_time": "2026-10-06T11:45:00-03:00"},
        "photos": [{"urls": [{"url": "https://cdn.getyourguide.com/one.jpg", "size": "thumb"}]}],
    }
    value.update(updates)
    return value


class GetYourGuideListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = GetYourGuideListingSpider(category="argentina")

    def response(self, state, status=200):
        body = f"<script>window.__INITIAL_STATE__ = {json.dumps(state)};</script>"
        request = Request(
            "https://www.getyourguide.com/argentina-l168992/",
            meta={"category": "argentina", "page": 1},
        )
        return HtmlResponse(request.url, status=status, body=body, encoding="utf-8", request=request)

    def test_categories_are_verified_twenty_entry_schema(self):
        self.assertEqual(len(GETYOURGUIDE_CATEGORIES), 20)
        self.assertEqual(GETYOURGUIDE_CATEGORIES[0]["category"], "argentina")
        self.assertEqual(GETYOURGUIDE_CATEGORIES[-1]["category"], "brunei")

    def test_maps_hydrated_product_and_feed_contract(self):
        fixture = Path(__file__).parents[1] / "sample" / "getyourguide-argentina-sample.html"
        request = Request(
            "https://www.getyourguide.com/argentina-l168992/",
            meta={"category": "argentina", "page": 1},
        )
        response = HtmlResponse(
            request.url, body=fixture.read_bytes(), encoding="utf-8", request=request
        )
        item = list(self.spider.parse(response))[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], 1220349)
        self.assertEqual(item["starting_price"], 49.5)
        self.assertEqual(item["rating"], 4.877572)
        self.assertEqual(item["reviews_count"], 18)
        self.assertEqual(item["url"], "https://www.getyourguide.com/el-calafate-l544/example-t1220349/")
        self.assertEqual(item["image_url"], "https://cdn.getyourguide.com/one.jpg")

    def test_recursive_traversal_deduplicates_tracking_copy(self):
        original = product()
        duplicate = product(title="Tracking copy")
        other = product(2)
        items = list(self.spider.parse(self.response({"sdui": {"a": [original], "tracking": [duplicate, other]}})))
        self.assertEqual([item["item_id"] for item in items], [1220349, 2])
        self.assertEqual(items[0]["title"], original["title"])

    def test_optional_photos_and_availability_are_empty(self):
        item = list(self.spider.parse(self.response({"sdui": [product(photos=None, availability=None)]})))[0]
        self.assertIsNone(item["image_url"])
        self.assertEqual(item["image_urls"], [])
        self.assertIsNone(item["availability_message"])

    def test_missing_state_fails_loudly(self):
        response = HtmlResponse("https://example.test", body="<html></html>", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "assignment is absent"):
            list(self.spider.parse(response))

    def test_malformed_state_fails_loudly(self):
        response = HtmlResponse("https://example.test", body="<script>window.__INITIAL_STATE__ = {bad};</script>", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            list(self.spider.parse(response))

    def test_missing_sdui_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "no SDUI contract"):
            list(self.spider.parse(self.response({"other": {}})))

    def test_empty_products_fail_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "No GetYourGuide SDUI products"):
            list(self.spider.parse(self.response({"sdui": {"cards": []}})))


if __name__ == "__main__":
    unittest.main()
