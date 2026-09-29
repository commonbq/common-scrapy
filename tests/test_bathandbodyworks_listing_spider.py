import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.bathandbodyworks_categories import BATHANDBODYWORKS_CATEGORIES
from common.spiders.bathandbodyworks_listing_spider import BathAndBodyWorksListingSpider


class BathAndBodyWorksListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = BathAndBodyWorksListingSpider(category="body-care", max_pages=2)

    @staticmethod
    def response(body):
        request = Request(
            "https://www.bathandbodyworks.com/c/body-care",
            meta={"category": "body-care", "page": 1},
        )
        return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_hydrated_products_feed_contract_and_pagination(self):
        body = Path("sample/bathandbodyworks-listing-products.html").read_text()
        output = list(self.spider.parse(self.response(body)))
        items, requests = output[:-1], output[-1:]

        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "028005116")
        self.assertEqual(items[0]["price"], 4.95)
        self.assertEqual(items[0]["regular_price"], 18.95)
        self.assertEqual(items[0]["reviews_count"], 5132)
        self.assertEqual(items[0]["availability"], "InStock")
        self.assertEqual(requests[0].url, "https://www.bathandbodyworks.com/c/body-care?start=2")

    def test_missing_hydration_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "mobify-data hydration"):
            list(self.spider.parse(self.response("<html></html>")))

    def test_navigation_inventory_is_nested_and_complete(self):
        self.assertEqual(len(BATHANDBODYWORKS_CATEGORIES), 9)
        self.assertEqual(sum(map(len, BATHANDBODYWORKS_CATEGORIES.values())), 65)
        self.assertIn("3-wick-candles", BATHANDBODYWORKS_CATEGORIES["candles"])


if __name__ == "__main__":
    unittest.main()
