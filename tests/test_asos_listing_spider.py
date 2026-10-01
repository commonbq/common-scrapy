from pathlib import Path
import json
import re
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.asos_categories import (
    ASOS_CATEGORIES,
    ASOS_CATEGORY_INVENTORY,
    ASOS_DEPARTMENT_TARGETS,
)
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
        self.assertEqual(sum(len(entries) for entries in ASOS_CATEGORY_INVENTORY.values()), 571)
        self.assertEqual(len(ASOS_CATEGORIES), 412)
        self.assertIn("cid=53315", self.spider.resolve_target_url())
        self.assertEqual(len({entry["cid"] for entry in ASOS_CATEGORIES}), len(ASOS_CATEGORIES))
        self.assertEqual(len({entry["category"] for entry in ASOS_CATEGORIES}), len(ASOS_CATEGORIES))
        self.assertTrue(all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["category"])
                            for entry in ASOS_CATEGORIES))

    def test_documented_department_aliases_resolve(self):
        # The department landing pages serve no PLP hydration, so these shortcuts
        # must stay pinned to explicit department-wide listings.
        for department, target in ASOS_DEPARTMENT_TARGETS.items():
            with self.subTest(department=department):
                spider = AsosListingSpider(category=department, max_pages=2)
                self.assertEqual(spider.resolve_target_url(), target["url"])
        women = AsosListingSpider(category="women", max_pages=2)
        men = AsosListingSpider(category="men", max_pages=2)
        self.assertIn("/us/women/", women.resolve_target_url())
        self.assertIn("/us/men/", men.resolve_target_url())
        self.assertNotEqual(women.resolve_target_url(), AsosListingSpider(
            category="women-fall-occasionwear").resolve_target_url())

    def test_hydration_mapping_feed_contract_and_proxy_handoff(self):
        outputs = list(self.spider.parse(self.response()))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "211160390")
        self.assertEqual(item["style_id"], "158157966")
        self.assertEqual(item["price"], 69.99)
        self.assertEqual(item["original_price"], 99.99)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["title"], "ASOS DESIGN stretch chiffon scarf detail plunge draped maxi dress in chocolate")
        self.assertTrue(item["url"].startswith("https://www.asos.com/us/"))
        self.assertTrue(item["image_url"].startswith("https://"))
        self.assertIsNotNone(item["raw"])
        self.assertEqual(item["raw"]["id"], 211160390)
        follow = outputs[-1]
        self.assertIn("/categories/53315?", follow.url)
        self.assertIn("keyStoreDataversion=fixture-version", follow.url)
        self.assertIn("offset=2", follow.url)
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")

    def test_legacy_flat_hydration_shape_is_still_supported(self):
        # ASOS previously hydrated a flat {products, itemCount, query} object; the
        # search API still returns that shape, so both must keep working.
        state = {"products": [{"id": 1, "name": "Legacy", "price": {"current": {"value": 10.0}, "currency": "USD"},
                               "url": "x/prd/1", "imageUrl": "images.example/a.jpg"}],
                 "itemCount": 5, "query": {"cid": "53315", "offset": 0, "limit": 1}}
        body = ("<script>window.asos.plp._data=JSON.parse(" +
                json.dumps(json.dumps(state)) + ")</script>")
        item = list(self.spider.parse(self.response(body)))[0]
        self.assertEqual(item["item_id"], "1")
        self.assertEqual(item["price"], 10.0)
        self.assertEqual(item["currency"], "USD")

    def test_api_mapping_deduplication_and_pagination(self):
        first_page = list(self.spider.parse(self.response()))
        seen = first_page[0]["item_id"]
        query = {"offset": 2, "limit": 2, "store": "US", "country": "US"}
        payload = {
            "itemCount": 5,
            "products": [
                {"id": int(seen), "name": "duplicate"},
                {"id": 210638193, "name": "new", "price": {"current": {"value": 10}, "currency": "USD"}},
            ],
        }
        outputs = list(self.spider.parse_api(self.response(json.dumps(payload), page=2, api_query=query)))
        self.assertEqual(outputs[0]["item_id"], "210638193")
        self.assertEqual(outputs[0]["source"], "asos_search_api")
        self.assertEqual(outputs[-1].meta["api_query"]["offset"], 4)

    def search_state(self):
        """Return a mutable copy of the fixture's `search` listing node."""
        return self.spider._search_state(json.loads(json.dumps(
            AsosListingSpider._extract_hydration(self.sample))))

    def test_hydration_does_not_handoff_when_page_is_complete_or_empty(self):
        state = self.search_state()
        state["itemCount"] = len(state["products"])
        body = (
            "<script>window.asos.plp._data=JSON.parse(" +
            json.dumps(json.dumps({"search": state})) + ")</script>"
        )
        self.assertTrue(all(isinstance(output, dict) for output in self.spider.parse(self.response(body))))

        state["products"] = []
        state["itemCount"] = 10
        body = (
            "<script>window.asos.plp._data=JSON.parse(" +
            json.dumps(json.dumps({"search": state})) + ")</script>"
        )
        self.assertEqual(list(self.spider.parse(self.response(body))), [])

    def test_hydration_handoff_preserves_nonzero_offset(self):
        state = self.search_state()
        state["query"]["offset"] = 10
        state["itemCount"] = 20
        body = (
            "<script>window.asos.plp._data=JSON.parse(" +
            json.dumps(json.dumps({"search": state})) + ")</script>"
        )
        outputs = list(self.spider.parse(self.response(body)))
        self.assertEqual(outputs[-1].meta["api_query"]["offset"], 12)

    def test_hydration_missing_item_count_fails_before_handoff(self):
        state = self.search_state()
        state.pop("itemCount")
        body = (
            "<script>window.asos.plp._data=JSON.parse(" +
            json.dumps(json.dumps({"search": state})) + ")</script>"
        )
        with self.assertRaisesRegex(RuntimeError, "numeric itemCount"):
            list(self.spider.parse(self.response(body)))

    def test_api_handoff_preserves_refinement_filters(self):
        """Refined categories must keep their filters on the page-2 API handoff."""
        state = self.search_state()
        state["query"].update({"offset": 0, "sizeFilter": ["12"], "brand": ["Adidas"]})
        state["itemCount"] = 100
        body = (
            "<script>window.asos.plp._data=JSON.parse(" +
            json.dumps(json.dumps({"search": state})) + ")</script>"
        )
        api_query = list(self.spider.parse(self.response(body)))[-1].meta["api_query"]
        self.assertEqual(api_query["brand"], '["Adidas"]')
        self.assertEqual(api_query["sizeFilter"], '["12"]')
        self.assertEqual(api_query["offset"], 2)

    def test_url_normalization(self):
        self.assertEqual(AsosListingSpider._https_url("//images.example/a.jpg"), "https://images.example/a.jpg")
        self.assertEqual(AsosListingSpider._https_url("images.example/a.jpg"), "https://images.example/a.jpg")

    def test_malformed_hydration_and_api_fail_visibly(self):
        for body in ("<html></html>", "<script>window.asos.plp._data=JSON.parse('bad')</script>"):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "No valid ASOS"):
                list(self.spider.parse(self.response(body)))
        with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
            list(self.spider.parse_api(self.response("not json", page=2, api_query={"offset": 2, "limit": 2})))
        payload = {"products": []}
        with self.assertRaisesRegex(RuntimeError, "numeric itemCount"):
            list(self.spider.parse_api(self.response(json.dumps(payload), page=2, api_query={"offset": 2, "limit": 2})))

    def test_challenge_page_fails_with_targeted_error(self):
        with self.assertRaisesRegex(RuntimeError, "Akamai access-denied/challenge"):
            list(self.spider.parse(self.response("<html><title>Access Denied</title>Reference #18.</html>")))


if __name__ == "__main__":
    unittest.main()
