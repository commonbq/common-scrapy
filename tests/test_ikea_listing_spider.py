import json
import unittest
from pathlib import Path

from scrapy.http import TextResponse

from common.spiders.ikea_listing_spider import IkeaListingSpider


class IkeaListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = IkeaListingSpider(category="st004", max_pages=2)
        capture = json.loads(Path("sample/ikea-sik-sample.json").read_text())
        self.product = capture["requests"][0]["response"]["first_item"]

    def response(self, request, *, start=0, end=24, total=147):
        payload = {
            "component": "PRIMARY_AREA",
            "items": [self.product, {"type": "OFFERS"}],
            "metadata_window": {
                "start": start,
                "end": end,
                "max": total,
                "itemsPerType": {"PRODUCT": total},
            },
        }
        return TextResponse(
            request.url,
            request=request,
            body=json.dumps(payload).encode(),
            encoding="utf-8",
        )

    def test_maps_product_and_requests_second_window(self):
        first = next(self.spider.start_requests())
        self.assertEqual(json.loads(first.body)["components"][0]["window"], {"size": 24, "offset": 0})
        outputs = list(self.spider.parse(self.response(first)))
        item, second = outputs
        self.assertEqual(item["item_id"], "60561248")
        self.assertEqual(item["title"], "STORKLINTA")
        self.assertEqual(item["product_type"], "6-drawer dresser")
        self.assertEqual(item["price"], 249.99)
        self.assertEqual(item["rating"], 3.9)
        self.assertEqual(item["reviews_count"], 319)
        self.assertEqual(item["raw"], self.product["product"])
        self.assertEqual(json.loads(second.body)["components"][0]["window"], {"size": 24, "offset": 24})

    def test_accepts_url_only_input(self):
        spider = IkeaListingSpider(url="https://www.ikea.com/us/en/cat/dressers-chests-of-drawers-st004/")
        request = next(spider.start_requests())
        self.assertEqual(request.meta["category_id"], "st004")
        with self.assertRaises(ValueError):
            next(IkeaListingSpider().start_requests())

    def test_deduplicates_products_between_pages(self):
        first = next(self.spider.start_requests())
        list(self.spider.parse(self.response(first)))
        second = self.spider._api_request("st004", first.meta["category_url"], page=2)
        self.assertEqual(list(self.spider.parse(self.response(second, start=24, end=48))), [])

    def test_inventory_has_unique_urls(self):
        urls = [entry["url"] for entry in self.spider.categories]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertGreaterEqual(len(urls), 200)

    def test_missing_primary_area_fails_loudly(self):
        request = next(self.spider.start_requests())
        response = TextResponse(
            request.url, request=request, body=b'{"results": []}', encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "missing PRIMARY_AREA"):
            list(self.spider.parse(response))

    def test_product_without_identifier_fails_loudly(self):
        request = next(self.spider.start_requests())
        payload = {
            "component": "PRIMARY_AREA",
            "items": [{"type": "PRODUCT", "product": {"name": "No id product"}}],
            "metadata_window": {"start": 0, "end": 24, "max": 147, "itemsPerType": {"PRODUCT": 147}},
        }
        response = TextResponse(
            request.url, request=request, body=json.dumps(payload).encode(), encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "missing itemNo/id"):
            list(self.spider.parse(response))

    def test_captured_top_level_shape_is_parsed(self):
        # The real SIK response is a single PRIMARY_AREA object with `items` and
        # `metadata_window`; it has no `results` array.
        capture = json.loads(Path("sample/ikea-sik-sample.json").read_text())
        captured = capture["requests"][0]["response"]
        payload = {
            "component": captured["component"],
            "items": [captured["first_item"], {"type": "OFFERS"}],
            "metadata_window": captured["metadata_window"],
        }
        request = next(self.spider.start_requests())
        outputs = list(self.spider.parse(self.response_from(request, payload)))
        item, second = outputs
        self.assertEqual(item["item_id"], "60561248")
        self.assertEqual(item["title"], "STORKLINTA")
        # metadata_window.itemsPerType.PRODUCT = 147 > end (24), so page 2 follows.
        self.assertEqual(json.loads(second.body)["components"][0]["window"]["offset"], 24)

    def response_from(self, request, payload):
        return TextResponse(
            request.url, request=request, body=json.dumps(payload).encode(), encoding="utf-8"
        )
