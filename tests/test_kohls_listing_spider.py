import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.kohls_listing_spider import KohlsListingSpider


class KohlsListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = KohlsListingSpider(category="women-clothing", max_pages=1)

    def response(self):
        body = Path("sample/kohls-listing-products.json").read_bytes()
        request = Request("https://www.kohls.com/web/catalog/Gender:Womens%20Department:Clothing", meta={"category": "women-clothing", "page": 1})
        return TextResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_catalog_api_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "4920973")
        self.assertEqual(items[0]["price"], 29.99)
        self.assertEqual(items[0]["regular_price"], 44.0)
        self.assertEqual(items[1]["price"], 20.0)

    def test_missing_contract_fails_visibly(self):
        request = Request("https://www.kohls.com/web/catalog/test", meta={"category": "women-clothing", "page": 1})
        response = TextResponse(request.url, body=b'{"payload": {"products": []}}', encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "No Kohl's catalog API products"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
