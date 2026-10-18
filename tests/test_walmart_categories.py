import unittest
from collections.abc import Mapping
from urllib.parse import urlparse

from common.spiders.walmart_categories import WALMART_CATEGORIES
from common.spiders.walmart_listing_spider import WalmartListingSpider


class WalmartCategoriesTest(unittest.TestCase):
    def test_inventory_uses_grouped_department_mapping(self):
        self.assertIsInstance(WALMART_CATEGORIES, Mapping)
        self.assertEqual(len(WALMART_CATEGORIES), 23)

        # Every group is a mapping of leaf -> rich entry with a live PLP url.
        for department, leaves in WALMART_CATEGORIES.items():
            self.assertIsInstance(leaves, Mapping, department)
            self.assertTrue(leaves, department)
            for leaf, entry in leaves.items():
                self.assertIsInstance(entry, Mapping, f"{department}/{leaf}")
                self.assertTrue(
                    entry["url"].startswith("https://www.walmart.com/"),
                    f"{department}/{leaf}",
                )

        leaves = [leaf for group in WALMART_CATEGORIES.values() for leaf in group]
        self.assertEqual(len(leaves), 296)
        # Leaves are globally unique so the per-group DAG output paths cannot collide.
        self.assertEqual(len(set(leaves)), 296)

    def test_every_target_url_is_distinct(self):
        urls = [
            entry["url"]
            for group in WALMART_CATEGORIES.values()
            for entry in group.values()
        ]
        # A PLP linked from two departments is stored once, so no task repeats.
        self.assertEqual(len(urls), len(set(urls)))

    def test_legacy_department_slug_still_resolves_to_its_hub(self):
        spider = WalmartListingSpider(category="electronics")

        entry = spider.category_entry("electronics")
        self.assertEqual(entry["group"], "electronics")
        self.assertEqual(entry["url"], "https://www.walmart.com/cp/electronics/3944")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.walmart.com/cp/electronics/3944",
        )

    def test_subcategory_leaf_resolves_inside_its_department(self):
        spider = WalmartListingSpider(category="furniture")

        entry = spider.category_entry("furniture")
        self.assertEqual(entry["group"], "home")
        self.assertEqual(entry["url"], "https://www.walmart.com/cp/furniture/103150")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.walmart.com/cp/furniture/103150",
        )

    def test_cross_listed_plp_is_owned_by_one_department(self):
        # "Kids Clothing" is linked from both Clothing and Baby & Kids.
        self.assertIn("kids", WALMART_CATEGORIES["clothing"])
        self.assertNotIn("kids-clothing", WALMART_CATEGORIES["baby-and-kids"])
        # "Video Games" is a department hub, so it stays with its own group.
        self.assertIn("video-games", WALMART_CATEGORIES["video-games"])
        self.assertNotIn("video-games", WALMART_CATEGORIES["electronics"])

    def test_every_department_hub_leaf_is_last_in_its_group(self):
        # The DAG schedules only the first three leaves per group, so the hub
        # must not occupy one of those slots.
        for department, leaves in WALMART_CATEGORIES.items():
            self.assertEqual(list(leaves)[-1], department)


if __name__ == "__main__":
    unittest.main()
