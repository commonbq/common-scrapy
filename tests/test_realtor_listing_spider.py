import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.realtor_categories import REALTOR_CATEGORIES
from common.spiders.realtor_listing_spider import RealtorListingSpider


def streamed_html(properties):
    table = [{"_1": 2}, "loaderData", {"_3": 4}, "srp", {"_5": 6}, "search", ["P", 6]]
    patch_table = []

    def patch_add(value):
        patch_table.append(value)
        return len(table) + len(patch_table) - 1

    def patch_encode(value):
        index = patch_add(None)
        if isinstance(value, dict):
            pairs = []
            for key, entry in value.items():
                key_ref = patch_add(key)
                value_ref = patch_encode(entry)
                pairs.append((key_ref, value_ref))
            patch_table[index - len(table)] = {f"_{key}": ref for key, ref in pairs}
        elif isinstance(value, list):
            patch_table[index - len(table)] = [patch_encode(entry) for entry in value]
        else:
            patch_table[index - len(table)] = value
        return index

    patch_root = patch_encode({"properties": properties, "total": 123})
    assert patch_root == len(table)
    first = json.dumps(json.dumps(table))
    patch = json.dumps("P6:" + json.dumps(patch_table) + "\n")
    return f"<script>streamController.enqueue({first})</script><script>streamController.enqueue({patch})</script>"


SAMPLE = {
    "property_id": "9573322873",
    "listing_id": "2994590506",
    "ldpSlug": "11201-Chalon-Rd_Los-Angeles_CA_90049_M95733-22873",
    "status": "for_sale",
    "statusText": "House for sale",
    "list_price": 400000000,
    "description": {"type": "single_family", "beds": 39, "baths_consolidated": "50.5+", "sqft": 70000, "lot_sqft": 342464},
    "location": {"address": {"line": "11201 Chalon Rd", "city": "Los Angeles", "state_code": "CA", "postal_code": "90049", "coordinate": {"lat": 34.08, "lon": -118.46}}},
    "primary_photo": {"href": "https://ap.rdcpix.com/photo.jpg"},
    "flags": {"is_new_listing": False},
}


class RealtorListingSpiderTests(unittest.TestCase):
    def test_taxonomy_is_exactly_twenty_cities(self):
        self.assertEqual(len(REALTOR_CATEGORIES), 20)

    def test_stream_decode_and_item_mapping(self):
        spider = RealtorListingSpider(category="los-angeles-ca")
        request = Request(REALTOR_CATEGORIES["los-angeles-ca"], meta={"page": 1, "base_url": REALTOR_CATEGORIES["los-angeles-ca"]})
        response = HtmlResponse(request.url, request=request, body=streamed_html([SAMPLE]).encode())
        output = list(spider.parse(response))
        self.assertEqual(len(output), 1)
        item = output[0]
        self.assertEqual(item["item_id"], "9573322873")
        self.assertEqual(item["price"], 400000000)
        self.assertEqual(item["beds"], 39)
        self.assertEqual(item["source"], "realtor_react_router_stream")
        self.assertIn("timestamp", item)
        self.assertIn("raw", item)
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_deduplicates_and_paginates(self):
        spider = RealtorListingSpider(category="los-angeles-ca", max_pages=2)
        request = Request(REALTOR_CATEGORIES["los-angeles-ca"], meta={"page": 1, "base_url": REALTOR_CATEGORIES["los-angeles-ca"]})
        response = HtmlResponse(request.url, request=request, body=streamed_html([SAMPLE, SAMPLE]).encode())
        output = list(spider.parse(response))
        self.assertEqual(sum(isinstance(value, dict) for value in output), 1)
        follow = next(value for value in output if isinstance(value, Request))
        self.assertTrue(follow.url.endswith("/pg-2"))

    def test_proxy_options_are_idempotent(self):
        spider = RealtorListingSpider(category="los-angeles-ca")
        spider.settings = {"PROXY": "http://scrapeops.country=us.residential=true:key@proxy.scrapeops.io:5353"}
        proxy = spider._realtor_proxy()
        self.assertEqual(proxy.count("residential=true"), 1)
        self.assertEqual(proxy.count("bypass=5"), 1)

    def test_missing_stream_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "Missing React Router"):
            RealtorListingSpider._decode_router_stream("<html></html>")


if __name__ == "__main__":
    unittest.main()
