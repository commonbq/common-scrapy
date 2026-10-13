import unittest
from collections.abc import Mapping
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.kroger_listing_spider import KrogerListingSpider


class KrogerListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = KrogerListingSpider(category="cereal", max_pages=1)

    def response(self, body=None):
        request = Request(
            "https://www.kroger.com/pl/cereal/09002?page=1",
            meta={"category": "cereal", "page": 1},
        )
        body = body if body is not None else Path("sample/kroger-listing-products.html").read_bytes()
        return TextResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_initial_state_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "0001111012345")
        self.assertEqual(items[0]["price"], 3.99)
        self.assertEqual(items[0]["regular_price"], 4.49)
        self.assertEqual(items[1]["price"], 5.29)

    def test_categories_use_grouped_mapping_contract(self):
        self.assertIsInstance(self.spider.categories, Mapping)
        self.assertGreaterEqual(sum(map(len, self.spider.categories.values())), 25)
        self.assertTrue(
            all(isinstance(group, Mapping) for group in self.spider.categories.values())
        )
        self.assertEqual(
            self.spider.category_entry("cereal")["url"],
            "https://www.kroger.com/pl/cereal/09002",
        )

    def test_missing_contract_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "No Kroger __INITIAL_STATE__ JSON"):
            list(self.spider.parse(self.response(b"<html></html>")))

    def test_empty_products_fail_visibly(self):
        body = b"<script>window.__INITIAL_STATE__ = JSON.parse('{\"search\":{\"searchAll\":{\"response\":{\"products\":[]}}}}');</script>"
        with self.assertRaisesRegex(RuntimeError, "No Kroger Redux search products"):
            list(self.spider.parse(self.response(body)))


if __name__ == "__main__":
    unittest.main()
