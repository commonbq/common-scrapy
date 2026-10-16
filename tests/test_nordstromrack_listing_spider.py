import unittest
from pathlib import Path

from collections.abc import Mapping

from scrapy.http import HtmlResponse, Request

from common.spiders.nordstromrack_listing_spider import NordstromrackListingSpider


class NordstromrackListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = NordstromrackListingSpider(category="women-clothing-dresses")

    def test_fixture_and_feed_contract(self):
        request = Request(
            "https://www.nordstromrack.com/c/women",
            meta={
                "category": "women-clothing-dresses",
                "page": 1,
                "listing_url": "https://www.nordstromrack.com/c/women",
            },
        )
        response = HtmlResponse(
            request.url,
            request=request,
            body=Path("sample/nordstromrack-listing.html").read_bytes(),
            encoding="utf-8",
        )
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["item_id"], "7788991")
        self.assertEqual(items[0]["price"], 34.97)
        self.assertEqual(items[0]["raw"]["sku"], "7788991")
        self.assertEqual(items[0]["raw"]["@type"], "Product")
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_categories_are_grouped_mapping(self):
        categories = NordstromrackListingSpider.categories
        self.assertIsInstance(categories, Mapping)
        self.assertTrue(all(isinstance(leaves, Mapping) for leaves in categories.values()))
        # The navigation sitemap taxonomy: 18 departments / 1335 crawlable leaves.
        self.assertEqual(len(categories), 18)
        self.assertEqual(sum(len(leaves) for leaves in categories.values()), 1335)
        self.assertIn("women", categories)
        self.assertIn("clearance", categories)

    def test_leaf_resolution_across_groups(self):
        spider = NordstromrackListingSpider(category="women-clothing-dresses")
        entry = spider.category_entry("women-clothing-dresses")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["group"], "women")
        self.assertEqual(entry["url"], "https://www.nordstromrack.com/shop/women/clothing/dresses")
        # A leaf that only exists under clearance resolves too.
        clearance = spider.category_entry("clearance-women")
        self.assertEqual(clearance["group"], "clearance")

    def test_unknown_category_is_rejected(self):
        with self.assertRaises(ValueError):
            NordstromrackListingSpider(category="not-a-real-category")

    def test_initial_config_products_are_exported(self):
        request = Request(
            "https://www.nordstromrack.com/shop/accessories",
            meta={
                "category": "accessories",
                "page": 1,
                "listing_url": "https://www.nordstromrack.com/shop/accessories",
            },
        )
        response = HtmlResponse(
            request.url,
            request=request,
            body=Path("sample/nordstromrack-initial-config.html").read_bytes(),
            encoding="utf-8",
        )
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 2)
        first = items[0]
        self.assertEqual(first["item_id"], "3287827")
        self.assertEqual(first["title"], "'Wayfarer' 58mm Sunglasses")
        self.assertEqual(first["brand"], "Ray-Ban")
        self.assertEqual(first["price"], 89.97)
        self.assertEqual(first["price_max"], 89.97)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["availability"], "Sellable")
        self.assertEqual(first["source"], "nordstromrack_initial_config")
        self.assertEqual(
            first["url"],
            "https://www.nordstromrack.com/s/ray-ban-wayfarer-58mm-sunglasses/3287827",
        )
        self.assertEqual(
            first["image_url"], "https://n.nordstrommedia.com/it/9ae2c565.jpeg"
        )
        # ``timestamp`` is injected by the middleware, so the item matches the
        # export contract up to that trailing field.
        self.assertEqual(
            list(first), self.spider.custom_settings["FEED_EXPORT_FIELDS"][:-1]
        )

    def test_proxy_envelope_is_retried_then_fails_visibly(self):
        request = Request(
            "https://www.nordstromrack.com/shop/accessories",
            meta={
                "category": "accessories",
                "page": 1,
                "listing_url": "https://www.nordstromrack.com/shop/accessories",
                "proxy_retries": 0,
            },
        )
        envelope = '{"status": "We could not retrieve a successful response"}'.encode()
        response = HtmlResponse(
            request.url, request=request, body=envelope, encoding="utf-8"
        )
        self.assertTrue(self.spider._is_proxy_payload(response))
        # First hits re-request instead of silently emitting nothing.
        retried = list(self.spider.parse(response))
        self.assertEqual(len(retried), 1)
        from scrapy import Request as ScrapyRequest

        self.assertIsInstance(retried[0], ScrapyRequest)
        # At the retry cap the failure surfaces instead of a zero-item run.
        request.meta["proxy_retries"] = 3
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(response))

if __name__ == "__main__":
    unittest.main()
