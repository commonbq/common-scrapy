import unittest
from collections.abc import Mapping
from urllib.parse import parse_qs, urlparse

from common.spiders.macys_listing_spider import MacysListingSpider


class MacysListingSpiderCategoriesTest(unittest.TestCase):
    def test_categories_use_grouped_mapping_contract(self):
        categories = MacysListingSpider.categories
        self.assertIsInstance(categories, Mapping)
        self.assertTrue(all(isinstance(group, Mapping) for group in categories.values()))

        leaves = [leaf for group in categories.values() for leaf in group]
        self.assertEqual(len(categories), 13)
        self.assertEqual(len(leaves), 363)
        # Leaf keys are the full /shop path slug, so they are globally unique.
        self.assertEqual(len(set(leaves)), 363)

        # Cross-listed paths resolve to a single department, keeping leaves unique.
        self.assertIn("womens-shoes", categories["Women"])
        self.assertIn("womens-shoes-sneakers", categories["Shoes"])
        self.assertIn("home-bed-bath-bedding", categories["Home"])
        self.assertIn("beauty-fragrance", categories["Beauty"])
        self.assertIn(
            "seasonal-celebrations-holiday-shop-christmas-decorations-outdoor",
            categories["Holiday Shop"],
        )

    def test_rich_category_fields_build_the_api_request(self):
        spider = MacysListingSpider(category="beauty-fragrance-perfume")

        entry = spider.category_entry("beauty-fragrance-perfume")
        self.assertEqual(entry["group"], "Beauty")
        self.assertEqual(entry["id"], "30087")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.macys.com/shop/beauty/fragrance/perfume?id=30087",
        )

        query = parse_qs(urlparse(spider._build_macys_api_url(1)).query)
        self.assertEqual(query["id"], ["30087"])
        self.assertEqual(query["pathname"], ["/shop/beauty/fragrance/perfume"])

    def test_legacy_beauty_leaf_still_resolves(self):
        spider = MacysListingSpider(category="mens-cologne-grooming")
        entry = spider.category_entry("mens-cologne-grooming")
        self.assertEqual(entry["id"], "392472")
        self.assertEqual(
            parse_qs(urlparse(spider._build_macys_api_url(1)).query)["id"],
            ["392472"],
        )


if __name__ == "__main__":
    unittest.main()
