import unittest
from collections.abc import Mapping

from common.spiders.sephora_listing_spider import SephoraListingSpider


class SephoraListingSpiderTest(unittest.TestCase):
    def test_categories_match_current_crawlable_primary_navigation(self):
        spider = SephoraListingSpider(category="hair")

        self.assertIsInstance(spider.categories, Mapping)
        self.assertTrue(
            all(isinstance(group, Mapping) for group in spider.categories.values())
        )
        self.assertEqual(
            spider.available_categories(),
            [
                "bath-body",
                "fragrance",
                "hair",
                "makeup",
                "skincare",
                "tools-brushes",
            ],
        )
        self.assertEqual(spider._resolve_slug(), "hair-products")
        self.assertEqual(
            spider.category_entry("tools-brushes")["url"],
            "https://www.sephora.com/shop/makeup-tools",
        )

    def test_api_url_uses_rich_mapping_slug(self):
        spider = SephoraListingSpider(category="bath-body")

        self.assertIn(
            "/api/v2/catalog/categories/bath-body/seo?",
            spider._build_api_url(page=1),
        )
        self.assertEqual(spider._current_category_name(), "bath-body")


if __name__ == "__main__":
    unittest.main()
