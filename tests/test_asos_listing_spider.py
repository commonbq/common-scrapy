from pathlib import Path
import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.asos_categories import ASOS_CATEGORIES, ASOS_CATEGORY_INVENTORY
from common.spiders.asos_listing_spider import AsosListingSpider


class AsosListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = AsosListingSpider(category="women-fall-occasionwear", max_pages=3)
        self.sample = Path("sample/asos-listing-sample.html").read_text(encoding="utf-8")

    def response(self, body=None, *, page=1, api_query=None):
        url = "https://www.asos.com/us/women/occasionwear/cat/?cid=53315"
        meta = {
            "category": "women-fall-occasionwear", "subcategory": "Fall occasionwear",
            "page": page, "proxy": "http://proxy.invalid:8080",
        }
        if api_query:
            meta.update({"api_query": api_query, "cid": "53315", "referer": url})
        request = Request(url, meta=meta)
        return TextResponse(url, request=request, body=body or self.sample, encoding="utf-8")

    def test_inventory_and_category_selection(self):
        self.assertEqual(set(ASOS_CATEGORY_INVENTORY), {"women", "men"})
        self.assertGreater(len(ASOS_CATEGORIES), 100)
        self.assertIn("cid=53315", self.spider.resolve_target_url())
        self.assertEqual(len({entry["cid"] for entry in ASOS_CATEGORIES}), len(ASOS_CATEGORIES))

    def test_hydration_mapping_feed_contract_and_proxy_handoff(self):
        outputs = list(self.spider.parse(self.response()))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "210638191")
        self.assertEqual(item["style_id"], "156233978")
        self.assertEqual(item["price"], 99.99)
        self.assertEqual(item["original_price"], 120.0)
        self.assertTrue(item["image_url"].startswith("https://"))
        follow = outputs[-1]
        self.assertIn("/categories/53315?", follow.url)
        self.assertIn("keyStoreDataversion=fixture-version", follow.url)
        self.assertIn("offset=2", follow.url)
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")

    def test_api_mapping_deduplication_and_pagination(self):
        list(self.spider.parse(self.response()))
        query = {"offset": 2, "limit": 2, "store": "US", "country": "US"}
        payload = {
            "itemCount": 5,
            "products": [
                {"id": 210638191, "name": "duplicate"},
                {"id": 210638193, "name": "new", "price": {"current": {"value": 10}, "currency": "USD"}},
            ],
        }
        outputs = list(self.spider.parse_api(self.response(json.dumps(payload), page=2, api_query=query)))
        self.assertEqual(outputs[0]["item_id"], "210638193")
        self.assertEqual(outputs[0]["source"], "asos_search_api")
        self.assertEqual(outputs[-1].meta["api_query"]["offset"], 4)

    def test_url_normalization(self):
        self.assertEqual(AsosListingSpider._https_url("//images.example/a.jpg"), "https://images.example/a.jpg")
        self.assertEqual(AsosListingSpider._https_url("images.example/a.jpg"), "https://images.example/a.jpg")

    def test_malformed_hydration_and_api_fail_visibly(self):
        for body in ("<html></html>", "<script>window.asos.plp._data=JSON.parse('bad')</script>"):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "No valid ASOS"):
                list(self.spider.parse(self.response(body)))
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            list(self.spider.parse_api(self.response("not json", page=2, api_query={"offset": 2, "limit": 2})))


if __name__ == "__main__":
    unittest.main()
