import unittest
from collections.abc import Mapping
from urllib.parse import parse_qs, urlparse

from common.spiders.macys_listing_spider import MacysListingSpider


class MacysListingSpiderCategoriesTest(unittest.TestCase):
    def test_categories_use_grouped_mapping_contract(self):
        self.assertIsInstance(MacysListingSpider.categories, Mapping)
        self.assertEqual(list(MacysListingSpider.categories), ["beauty"])
        self.assertEqual(len(MacysListingSpider.categories["beauty"]), 14)

    def test_rich_category_fields_build_the_api_request(self):
        spider = MacysListingSpider(category="mens-cologne-grooming")

        entry = spider.category_entry("mens-cologne-grooming")
        self.assertEqual(entry["group"], "beauty")
        self.assertEqual(entry["id"], "392472")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.macys.com/shop/mens/cologne-grooming",
        )

        query = parse_qs(urlparse(spider._build_macys_api_url(1)).query)
        self.assertEqual(query["id"], ["392472"])
        self.assertEqual(query["pathname"], ["/shop/mens/cologne-grooming"])


if __name__ == "__main__":
    unittest.main()
