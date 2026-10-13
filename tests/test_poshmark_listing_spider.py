import json
import unittest
from collections.abc import Mapping

from scrapy.http import HtmlResponse, Request

from common.spiders.poshmark_listing_spider import PoshmarkListingSpider


class PoshmarkListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = PoshmarkListingSpider(category="women", max_pages=1)

    def test_full_category_inventory_uses_grouped_mapping(self):
        self.assertIsInstance(self.spider.categories, Mapping)
        self.assertEqual(set(self.spider.categories), {
            "women", "men", "kids", "home", "electronics", "pets"
        })
        self.assertTrue(
            all(isinstance(categories, Mapping) for categories in self.spider.categories.values())
        )
        entries = list(self.spider.iter_categories())
        self.assertEqual(len(entries), 91)
        self.assertEqual(len({entry["category"] for entry in entries}), 91)
        self.assertEqual(
            self.spider.category_entry("women-bath-and-body")["url"],
            "https://poshmark.com/category/Women-Bath_&_Body",
        )
        self.assertEqual(
            self.spider.category_entry("pets-dog-collars-leashes-and-harnesses")["url"],
            "https://poshmark.com/category/Pets-Dog-Collars,_Leashes_&_Harnesses",
        )

    def test_feed_contract_and_bootstrap_extraction(self):
        product = {
            "id": "abc123",
            "title": "Test Dress",
            "brand": "Example",
            "price_amount": {"val": "35.0", "currency_code": "USD"},
            "original_price_amount": {"val": "80.0"},
            "cover_shot": {"url_large": "https://img.example/dress.jpg"},
            "size": "M",
        }
        state = {"$_category": {"gridData": {"data": [product]}}}
        body = f"<script>window.__INITIAL_STATE__={json.dumps(state)};</script>"
        request = Request("https://poshmark.com/category/Women", meta={"category": "women", "page": 1})
        response = HtmlResponse(request.url, body=body, encoding="utf-8", request=request)

        item = list(self.spider.parse(response))[0]

        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "abc123")
        self.assertEqual(item["price"], 35.0)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["url"], "https://poshmark.com/listing/Test-Dress-abc123")
        self.assertEqual(item["raw"], product)

    def test_missing_bootstrap_products_fails_visibly(self):
        request = Request("https://poshmark.com/category/Women", meta={"category": "women", "page": 1})
        response = HtmlResponse(request.url, body="<html></html>", encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "No Poshmark bootstrap listings"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
