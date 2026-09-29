import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.homedepot_listing_spider import HomeDepotListingSpider


class HomeDepotListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = HomeDepotListingSpider(category="tools", max_pages=1)

    def response(self, body=None):
        body = body if body is not None else Path("sample/homedepot-listing-products.html").read_bytes()
        request = Request("https://www.homedepot.com/b/Tools/N-5yc1vZc1xy", meta={"category": "tools", "page": 1})
        return TextResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_apollo_state_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "100000001")
        self.assertEqual(items[0]["price"], 14.97)
        self.assertEqual(items[0]["image_url"], "https://images.thdstatic.com/productImages/hammer_300.jpg")
        self.assertEqual(items[1]["reviews_count"], 1542)

    def test_missing_contract_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "did not contain __APOLLO_STATE__"):
            list(self.spider.parse(self.response(b"<html></html>")))


if __name__ == "__main__":
    unittest.main()
