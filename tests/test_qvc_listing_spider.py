import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.qvc_listing_spider import QVC_CATEGORIES, QvcListingSpider


class QvcListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = QvcListingSpider(category="fashion", max_pages=2)
        html = Path("sample/qvc-fashion-sample.html").read_text()
        request = Request(
            QVC_CATEGORIES["fashion"][0], meta={"category": "fashion", "page": 1}
        )
        self.response = HtmlResponse(request.url, request=request, body=html, encoding="utf-8")

    def test_parse_exports_feed_contract_and_pagination(self):
        output = list(self.spider.parse(self.response))
        first, second, next_request = output
        self.assertEqual(list(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), list(first))
        self.assertEqual("A702781", first["item_id"])
        self.assertEqual(49.98, first["price"])
        self.assertEqual(58.0, first["original_price"])
        self.assertEqual(127, first["reviews_count"])
        self.assertEqual("Denim & Co.", second["brand"])
        self.assertEqual("https://www.qvc.com/c/fashion/-/lglt/c.html?currentPage=2", next_request.url)

    def test_missing_grid_has_no_fallback_items(self):
        blocked = self.response.replace(body=b"<html><body>blocked</body></html>")
        self.assertEqual([], list(self.spider.parse(blocked)))


if __name__ == "__main__":
    unittest.main()
