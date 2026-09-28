import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.sallybeauty_listing_spider import SallybeautyListingSpider


class SallybeautyListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = SallybeautyListingSpider(category="hair-care", max_pages="1")
        url = "https://www.sallybeauty.com/hair-care/shop-by-product/shampoo/"
        request = Request(url, meta={"page": 1, "category_url": url})
        body = Path("tests/fixtures/sallybeauty_shampoo.html").read_bytes()
        self.response = HtmlResponse(url, request=request, body=body, encoding="utf-8")

    def test_feed_contract_and_items(self):
        items = list(self.spider.parse(self.response))
        self.assertEqual(list(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), list(items[0]))
        self.assertEqual(items[0]["item_id"], "SBS-539230")
        self.assertEqual(items[0]["price"], 11.99)
        self.assertEqual(items[0]["reviews_count"], 29)
        self.assertEqual(len(items), 2)

    def test_category_inventory(self):
        self.assertEqual(len(self.spider.categories), 12)
        self.assertIn("salon-supplies", self.spider.available_categories())


if __name__ == "__main__":
    unittest.main()
