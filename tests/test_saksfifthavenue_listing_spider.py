from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.saksfifthavenue_listing_spider import SaksfifthavenueListingSpider


class SaksListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = SaksfifthavenueListingSpider(category="women", max_pages=2)

    def test_feed_fields(self):
        self.assertEqual(len(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), 15)
        self.assertEqual(self.spider.custom_settings["FEED_EXPORT_FIELDS"][0:3], ["category", "subcategory", "item_id"])

    def test_server_rendered_grid(self):
        body = Path("sample/saksfifthavenue-listing.html").read_bytes()
        request = Request("https://www.saksfifthavenue.com/c/women-s-apparel?start=0&sz=24", meta={
            "category": "women", "subcategory": "apparel", "category_url": "https://www.saksfifthavenue.com/c/women-s-apparel", "page": 1,
        })
        response = TextResponse(request.url, request=request, body=body, encoding="utf-8")
        outputs = list(self.spider.parse(response))
        self.assertEqual(len(outputs), 3)
        self.assertEqual(outputs[0]["item_id"], "0400021044812")
        self.assertEqual(outputs[0]["title"], "FARM Rio Floral Midi Dress")
        self.assertEqual(outputs[0]["price"], 195.0)
        self.assertEqual(outputs[0]["original_price"], 280.0)
        self.assertEqual(outputs[-1].meta["page"], 2)


if __name__ == "__main__":
    unittest.main()
