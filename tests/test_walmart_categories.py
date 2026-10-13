import unittest
from collections.abc import Mapping

from common.spiders.walmart_categories import WALMART_CATEGORIES
from common.spiders.walmart_listing_spider import WalmartListingSpider


class WalmartCategoriesTest(unittest.TestCase):
    def test_inventory_uses_grouped_mapping_contract(self):
        self.assertIsInstance(WALMART_CATEGORIES, Mapping)
        self.assertEqual(set(WALMART_CATEGORIES), {"departments"})
        self.assertEqual(len(WALMART_CATEGORIES["departments"]), 23)

    def test_every_department_resolves_by_leaf_name(self):
        spider = WalmartListingSpider(category="electronics")
        entries = list(spider.iter_categories())

        self.assertEqual(len(entries), 23)
        self.assertTrue(all(entry["group"] == "departments" for entry in entries))
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.walmart.com/cp/electronics/3944",
        )


if __name__ == "__main__":
    unittest.main()
