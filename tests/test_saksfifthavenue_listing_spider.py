from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.saksfifthavenue_categories import SAKS_CATEGORY_SECTIONS
from common.spiders.saksfifthavenue_listing_spider import SaksfifthavenueListingSpider


class SaksListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = SaksfifthavenueListingSpider(category="women-s-apparel", max_pages=2)

    def test_feed_fields(self):
        self.assertEqual(len(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), 16)
        self.assertEqual(self.spider.custom_settings["FEED_EXPORT_FIELDS"][0:3], ["category", "subcategory", "item_id"])

    def test_inventory_is_a_grouped_mapping(self):
        self.assertEqual(len(SAKS_CATEGORY_SECTIONS), 13)
        leaves = [
            leaf
            for group in SAKS_CATEGORY_SECTIONS.values()
            for leaf in group
        ]
        self.assertEqual(len(leaves), 430)
        self.assertEqual(len(set(leaves)), 430, "leaf slugs must be globally unique")
        for group in SAKS_CATEGORY_SECTIONS.values():
            for leaf, entry in group.items():
                self.assertTrue(leaf)
                self.assertTrue(entry["url"].startswith("https://www.saksfifthavenue.com/c/"))
                self.assertTrue(entry["label"])
                self.assertTrue(entry["subcategory"])

    def test_category_lookup_spans_every_department(self):
        entry = self.spider.category_entry("men-apparel")
        self.assertEqual(entry["group"], "Men")
        self.assertEqual(
            entry["url"], "https://www.saksfifthavenue.com/c/men/apparel"
        )
        self.assertEqual(len(self.spider.available_categories()), 430)

    def test_unknown_category_lists_available_leaves(self):
        spider = SaksfifthavenueListingSpider(category="women", max_pages=1)
        with self.assertRaises(ValueError) as raised:
            list(spider.start_requests())
        self.assertIn("Unknown category 'women'", str(raised.exception))
        self.assertIn("men-apparel", str(raised.exception))

    def test_server_rendered_grid(self):
        body = Path("sample/saksfifthavenue-listing.html").read_bytes()
        request = Request("https://www.saksfifthavenue.com/c/women-s-apparel?start=0&sz=24", meta={
            "category": "women-s-apparel", "subcategory": "women-s-apparel", "category_url": "https://www.saksfifthavenue.com/c/women-s-apparel", "page": 1,
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
