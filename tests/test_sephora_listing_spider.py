import json
import unittest
from collections.abc import Mapping

from scrapy.http import Request, TextResponse

from common.spiders.sephora_categories import SEPHORA_CATEGORIES
from common.spiders.sephora_listing_spider import SephoraListingSpider


class SephoraListingSpiderTest(unittest.TestCase):
    def test_export_contract_uses_standard_raw_field(self):
        fields = SephoraListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertIn("raw", fields)
        self.assertNotIn("rawProduct", fields)

        product = {"productId": "P1"}
        request = Request("https://www.sephora.com/test", meta={"page": 1})
        response = TextResponse(
            request=request,
            url=request.url,
            body=json.dumps({"products": [product]}).encode(),
            encoding="utf-8",
        )
        item = next(SephoraListingSpider(category="foundation-makeup").parse(response))
        self.assertEqual(json.loads(item["raw"]), product)
        self.assertNotIn("rawProduct", item)

    def test_categories_are_department_grouped_dict(self):
        spider = SephoraListingSpider(category="foundation-makeup")

        self.assertIsInstance(spider.categories, Mapping)
        self.assertTrue(
            all(isinstance(group, Mapping) for group in spider.categories.values())
        )
        self.assertEqual(
            list(spider.categories),
            [
                "Makeup",
                "Skincare",
                "Fragrance",
                "Hair",
                "Bath & Body",
                "Mini Size",
                "Gifts & Value Sets",
            ],
        )
        self.assertEqual(
            sum(len(group) for group in spider.categories.values()),
            len([leaf for group in SEPHORA_CATEGORIES.values() for leaf in group]),
        )

    def test_leaf_names_are_unique_across_groups(self):
        leaves = [leaf for group in SEPHORA_CATEGORIES.values() for leaf in group]
        self.assertEqual(len(leaves), len(set(leaves)))

    def test_available_categories_match_leaf_keys(self):
        spider = SephoraListingSpider(category="foundation-makeup")

        expected = sorted(
            leaf for group in SEPHORA_CATEGORIES.values() for leaf in group
        )
        self.assertEqual(spider.available_categories(), expected)
        self.assertEqual(len(expected), 218)

    def test_resolve_slug_uses_rich_mapping_slug(self):
        spider = SephoraListingSpider(category="perfume")
        self.assertEqual(spider._resolve_slug(), "perfume")
        self.assertEqual(spider._current_category_name(), "perfume")

    def test_api_url_uses_rich_mapping_slug(self):
        spider = SephoraListingSpider(category="body-wash-shower-gel")

        self.assertIn(
            "/api/v2/catalog/categories/body-wash-shower-gel/seo?",
            spider._build_api_url(page=1),
        )
        self.assertEqual(spider._current_category_name(), "body-wash-shower-gel")


if __name__ == "__main__":
    unittest.main()
