from pathlib import Path
import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.staples_categories import STAPLES_CATEGORIES, STAPLES_CATEGORY_INVENTORY
from common.spiders.staples_listing_spider import StaplesListingSpider


class StaplesListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = StaplesListingSpider(category="binders", max_pages=2)
        self.sample = Path("sample/staples-listing-sample.html").read_text(encoding="utf-8")

    def response(self, body=None, *, page=1):
        url = f"https://www.staples.com/Binders/cat_CL167205{'?pn=2' if page == 2 else ''}"
        request = Request(
            url,
            meta={
                "category": "binders", "department": "Office Supplies",
                "subcategory": "Binders", "page": page,
                "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(url, request=request, body=body or self.sample, encoding="utf-8")

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(STAPLES_CATEGORY_INVENTORY), 34)
        self.assertEqual(sum(len(group["subcategories"]) for group in STAPLES_CATEGORY_INVENTORY.values()), 208)
        self.assertEqual(len(STAPLES_CATEGORIES), 242)
        self.assertEqual(len({entry["url"] for entry in STAPLES_CATEGORIES}), 242)
        self.assertEqual(self.spider.resolve_target_url(), "https://www.staples.com/Binders/cat_CL167205")

    def test_hydration_yields_40_items_and_feed_contract(self):
        outputs = list(self.spider.parse(self.response()))
        items = outputs[:-1]
        self.assertEqual(len(items), 40)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "82656")
        self.assertEqual(items[0]["url"], "https://www.staples.com/product_82656")
        self.assertEqual(items[0]["price"], 10.09)
        self.assertTrue(items[0]["in_stock"])
        self.assertEqual(items[0]["available_quantity"], 10749)
        self.assertEqual(items[0]["class_id"], "CL167205")

    def test_next_link_preserves_metadata_and_stops_at_max_pages(self):
        first = list(self.spider.parse(self.response()))[-1]
        self.assertEqual(first.url, "https://www.staples.com/Binders/cat_CL167205?pn=2")
        self.assertEqual(first.meta["page"], 2)
        self.assertEqual(first.meta["proxy"], "http://proxy.invalid:8080")
        payload = {
            "props": {"initialStateOrStore": {"searchState": {
                "productTileData": [{"itemId": "90001", "title": "Page two"}],
                "pageNumber": 2, "totalCount": 41, "itemsPerPage": 40,
            }}}
        }
        page_two = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'
        outputs = list(self.spider.parse(self.response(page_two, page=2)))
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0]["item_id"], "90001")

    def test_deduplicates_item_ids(self):
        list(self.spider.parse(self.response()))
        outputs = list(self.spider.parse(self.response(page=2)))
        self.assertFalse(any(isinstance(output, dict) for output in outputs))

    def test_malformed_missing_and_empty_hydration_fail_visibly(self):
        cases = [
            ("<html></html>", "No valid Staples"),
            ('<script id="__NEXT_DATA__">bad</script>', "No valid Staples"),
            ('<script id="__NEXT_DATA__">{}</script>', "no searchState"),
            ('<script id="__NEXT_DATA__">{"props":{"initialStateOrStore":{"searchState":{}}}}</script>', "no list-valued"),
            ('<script id="__NEXT_DATA__">{"props":{"initialStateOrStore":{"searchState":{"productTileData":[]}}}}</script>', "zero products"),
        ]
        for body, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(RuntimeError, message):
                list(self.spider.parse(self.response(body)))


if __name__ == "__main__":
    unittest.main()
