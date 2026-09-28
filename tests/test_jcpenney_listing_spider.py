import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.jcpenney_listing_spider import JCPenneyListingSpider


class JCPenneyListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = JCPenneyListingSpider(category="womens_tops", max_pages=1)

    def response(self, body=None):
        request = Request(
            "https://search-api.jcpenney.com/v1/search-service/g/women/tops?page=1",
            meta={
                "category": "womens_tops",
                "target_url": "https://www.jcpenney.com/g/women/tops?id=cat100210006",
                "page": 1,
            },
        )
        if body is None:
            body = Path("sample/jcpenney-listing-products.json").read_bytes()
        return TextResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_search_service_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "ppr5008584232")
        self.assertEqual(items[0]["price"], 12.99)
        self.assertEqual(items[0]["reviews_count"], 118)
        self.assertEqual(items[1]["brand"], "Liz Claiborne")

    def test_missing_json_contract_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "No JCPenney search-service JSON"):
            list(self.spider.parse(self.response(b"<html>Access Denied</html>")))

    def test_empty_products_fail_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "No JCPenney organicZoneInfo products"):
            list(self.spider.parse(self.response(json.dumps({"organicZoneInfo": {"products": []}}).encode())))


if __name__ == "__main__":
    unittest.main()
