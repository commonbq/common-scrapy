import unittest
from collections.abc import Mapping

from common.spiders.nordstrom_listing_spider import NordstromListingSpider


class NordstromListingSpiderCategoryTests(unittest.TestCase):
    def test_categories_use_grouped_mapping_contract(self):
        self.assertIsInstance(NordstromListingSpider.categories, Mapping)
        self.assertTrue(
            all(
                isinstance(leaves, Mapping)
                for leaves in NordstromListingSpider.categories.values()
            )
        )

    def test_current_top_level_shopping_departments_are_available(self):
        spider = NordstromListingSpider()
        self.assertEqual(
            set(spider.available_categories()),
            {
                "new",
                "women",
                "men",
                "beauty",
                "shoes",
                "accessories",
                "kids",
                "designer",
                "home",
                "gifts",
                "sale",
            },
        )

    def test_new_department_resolves_to_site_url(self):
        spider = NordstromListingSpider(category="new")
        self.assertEqual(
            spider.resolve_target_url(), "https://www.nordstrom.com/browse/new"
        )


if __name__ == "__main__":
    unittest.main()
