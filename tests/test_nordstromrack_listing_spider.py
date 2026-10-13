import unittest
from pathlib import Path

from collections.abc import Mapping

from scrapy.http import HtmlResponse, Request

from common.spiders.nordstromrack_listing_spider import NordstromrackListingSpider


class NordstromrackListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = NordstromrackListingSpider(category="women-clothing-dresses")

    def test_fixture_and_feed_contract(self):
        request = Request(
            "https://www.nordstromrack.com/c/women",
            meta={
                "category": "women-clothing-dresses",
                "page": 1,
                "listing_url": "https://www.nordstromrack.com/c/women",
            },
        )
        response = HtmlResponse(
            request.url,
            request=request,
            body=Path("sample/nordstromrack-listing.html").read_bytes(),
            encoding="utf-8",
        )
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["item_id"], "7788991")
        self.assertEqual(items[0]["price"], 34.97)
        self.assertEqual(items[0]["raw"]["sku"], "7788991")
        self.assertEqual(items[0]["raw"]["@type"], "Product")
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_categories_are_grouped_mapping(self):
        categories = NordstromrackListingSpider.categories
        self.assertIsInstance(categories, Mapping)
        self.assertTrue(all(isinstance(leaves, Mapping) for leaves in categories.values()))
        # The navigation sitemap taxonomy: 18 departments / 1335 crawlable leaves.
        self.assertEqual(len(categories), 18)
        self.assertEqual(sum(len(leaves) for leaves in categories.values()), 1335)
        self.assertIn("women", categories)
        self.assertIn("clearance", categories)

    def test_leaf_resolution_across_groups(self):
        spider = NordstromrackListingSpider(category="women-clothing-dresses")
        entry = spider.category_entry("women-clothing-dresses")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["group"], "women")
        self.assertEqual(entry["url"], "https://www.nordstromrack.com/shop/women/clothing/dresses")
        # A leaf that only exists under clearance resolves too.
        clearance = spider.category_entry("clearance-women")
        self.assertEqual(clearance["group"], "clearance")

    def test_unknown_category_is_rejected(self):
        with self.assertRaises(ValueError):
            NordstromrackListingSpider(category="not-a-real-category")


if __name__ == "__main__":
    unittest.main()
