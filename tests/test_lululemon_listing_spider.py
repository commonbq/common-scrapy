import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.lululemon_listing_spider import LululemonListingSpider


class LululemonListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = LululemonListingSpider(category="women-leggings", max_pages=1)

    def response(self):
        body = Path("sample/lululemon-listing-product.html").read_text()
        request = Request("https://shop.lululemon.com/c/womens-leggings/_/N-8r6?page=1", meta={"category": "women-leggings", "page": 1})
        return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_next_data_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "prod11860112")
        self.assertEqual(items[0]["price"], 98.0)
        self.assertEqual(items[0]["original_price"], 118.0)
        self.assertEqual(items[0]["color_count"], 2)

    def test_missing_contract_fails_visibly(self):
        request = Request("https://shop.lululemon.com/c/womens-leggings/_/N-8r6")
        response = HtmlResponse(request.url, body="<html></html>", encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "No Lululemon __NEXT_DATA__"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
