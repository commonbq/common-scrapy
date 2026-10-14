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

    def test_inventory_matches_live_navigation_sitemap(self):
        categories = NordstromListingSpider.categories
        # Refreshed from https://www.nordstrom.com/navigation-sitemap.xml on
        # 2026-10-14: 30 shopping departments / 1887 crawlable leaves.
        self.assertEqual(len(categories), 30)
        self.assertEqual(sum(len(leaves) for leaves in categories.values()), 1887)
        for department in ("women", "men", "kids", "beauty", "designer", "home", "sale"):
            self.assertIn(department, categories)

    def test_leaf_keys_are_globally_unique(self):
        leaves = [
            leaf
            for group in NordstromListingSpider.categories.values()
            for leaf in group
        ]
        self.assertEqual(len(leaves), len(set(leaves)))

    def test_new_department_resolves_to_site_url(self):
        spider = NordstromListingSpider(category="new")
        self.assertEqual(
            spider.resolve_target_url(), "https://www.nordstrom.com/browse/new"
        )

    def test_parent_department_still_resolves(self):
        spider = NordstromListingSpider(category="women")
        self.assertEqual(
            spider.resolve_target_url(), "https://www.nordstrom.com/browse/women"
        )
        targets = spider.category_targets("women")
        self.assertEqual(targets["women"], "https://www.nordstrom.com/browse/women")
        self.assertEqual(
            targets["women-maternity-nursing-clothing"],
            "https://www.nordstrom.com/browse/women/maternity/nursing-clothing",
        )

    def test_leaf_lookup_across_groups(self):
        spider = NordstromListingSpider(category="women-maternity-nursing-clothing")
        entry = spider.category_entry("women-maternity-nursing-clothing")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["group"], "women")
        self.assertEqual(
            entry["url"],
            "https://www.nordstrom.com/browse/women/maternity/nursing-clothing",
        )

    def test_unknown_category_is_rejected(self):
        spider = NordstromListingSpider(category="not-a-real-category")
        with self.assertRaises(ValueError):
            list(spider.start_requests())


if __name__ == "__main__":
    unittest.main()
