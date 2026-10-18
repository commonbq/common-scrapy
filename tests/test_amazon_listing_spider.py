from __future__ import annotations

import unittest
from collections.abc import Mapping
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.amazon_listing_spider import AmazonListingSpider


class AmazonListingSpiderTests(unittest.TestCase):
    def test_categories_use_grouped_mapping_with_live_departments(self):
        categories = AmazonListingSpider.categories
        self.assertIsInstance(categories, Mapping)
        self.assertEqual(len(categories), 58)
        self.assertNotIn("departments", categories)
        # A sample of the live department aliases must all be present as groups.
        for department in (
            "alexa-skills",
            "beauty",
            "electronics",
            "fashion",
            "grocery",
            "pets",
            "tools",
            "toys-and-games",
            "videogames",
        ):
            self.assertIn(department, categories)

        # The department search alias stays runnable as a hub leaf.
        spider = AmazonListingSpider(category="electronics")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.amazon.com/s?i=electronics",
        )
        self.assertEqual(
            spider.category_entry("electronics")["label"],
            "Electronics",
        )

    def test_category_leaves_are_grouped_by_department(self):
        categories = AmazonListingSpider.categories
        leaves = [leaf for group in categories.values() for leaf in group]
        self.assertEqual(len(leaves), len(set(leaves)))

        for department, group in categories.items():
            # Hub leaf sits last so the first three scheduled tasks per group
            # are real subcategory PLPs.
            self.assertEqual(list(group)[-1], department)
            for leaf, entry in group.items():
                self.assertTrue(entry["url"].startswith("https://www.amazon.com/s?"))
                if leaf == department:
                    self.assertEqual(
                        entry["url"], f"https://www.amazon.com/s?i={department}"
                    )
                    continue
                self.assertTrue(leaf.startswith(f"{department}-"), leaf)
                self.assertTrue(entry["node"].isdigit(), entry["node"])
                self.assertIn(f"%2Cn%3A{entry['node']}", entry["url"])

    def test_department_leaf_resolves_to_subcategory_search_url(self):
        spider = AmazonListingSpider(category="electronics-accessories-supplies")
        entry = spider.category_entry("electronics-accessories-supplies")
        self.assertEqual(entry["group"], "electronics")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.amazon.com/s?i=electronics"
            "&rh=n%3A172282%2Cn%3A281407",
        )

    def test_category_fixture_follows_shop_by_category_carousel(self):
        fixture_path = (
            Path(__file__).resolve().parents[1] / "sample" / "amazon-home-kitchen.html"
        )
        url = "https://www.amazon.com/b?node=1055398"
        request = Request(
            url=url,
            meta={"page": 1, "category": "Home & Kitchen"},
        )
        response = HtmlResponse(
            url=url,
            body=fixture_path.read_bytes(),
            encoding="utf-8",
            request=request,
        )

        spider = AmazonListingSpider(category="garden", max_pages=1)
        outputs = list(spider.parse(response))
        requests = [output for output in outputs if isinstance(output, Request)]

        self.assertEqual(len(requests), 7)
        self.assertEqual(requests[0].meta["category"], "Home & Kitchen")
        self.assertEqual(requests[0].meta["sub_category"], "Bed & bath")
        self.assertIn("node=1057792", requests[0].url)
        self.assertNotIn("pf_rd_", requests[0].url)
        self.assertNotIn("ref_", requests[0].url)
        self.assertNotIn(
            "Shopbop", {request.meta["sub_category"] for request in requests}
        )

    def test_category_urls_are_canonicalized_by_node(self):
        tracked_url = (
            "https://www.amazon.com/b/home-products?node=1057792"
            "&pf_rd_p=tracking-token&pf_rd_r=request-token&ref_=nav"
        )

        canonical = AmazonListingSpider._canonicalize_category_url(tracked_url)

        self.assertEqual(canonical, "https://www.amazon.com/b?node=1057792")

    def test_crawl_depth_is_limited_to_four(self):
        self.assertEqual(AmazonListingSpider.custom_settings["DEPTH_LIMIT"], 4)


if __name__ == "__main__":
    unittest.main()
