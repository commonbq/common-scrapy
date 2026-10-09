from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.hsn_categories import HSN_CATEGORIES
from common.spiders.hsn_listing_spider import HsnListingSpider


def response(url, body, meta=None):
    request = Request(url, meta=meta or {})
    return TextResponse(url, request=request, body=body.encode(), encoding="utf-8")


class HsnListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = HsnListingSpider(category="Electronics", max_pages=2)
        self.spider._constructor_key = "key_fixture123456"
        self.meta = {
            "category": "Electronics",
            "category_url": "https://www.hsn.com/shop/electronics/ec",
            "category_id": "EC",
            "page": 1,
        }

    def test_top_twenty_categories_are_unique(self):
        self.assertEqual(len(HSN_CATEGORIES), 20)
        self.assertEqual(len({x["category"] for x in HSN_CATEGORIES}), 20)

    def test_start_requests_fetches_constructor_client_only(self):
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, "https://cnstrc.com/js/cust/hsn_1oWza0.js")

    def test_client_selects_production_key_and_builds_api_request(self):
        js = '["www.hsn.com","www07.hsn.com"].includes(r)?"key_production123456":"key_qa123456789012"'
        requests = list(self.spider.parse_constructor_client(response("https://cnstrc.com/js/cust/hsn_x.js", js, self.meta)))
        self.assertEqual(self.spider._constructor_key, "key_production123456")
        self.assertIn("/browse/group_id/EC?", requests[0].url)

    def test_api_maps_fields_and_paginates(self):
        payload = {
            "response": {
                "total_num_results": 61,
                "results": [{
                    "value": "Example Laptop",
                    "is_slotted": False,
                    "data": {
                        "id": "23993915", "variation_id": "23993915",
                        "image_name": "944190", "price": 45999,
                        "webp_id": "23993915",
                        "url": "https://www.hsn.com/products/example/23993915",
                        "image_url": "https://i.hsncdn.com/example.jpg",
                        "description": "Example Laptop", "group_ids": ["EC", "EC0033"],
                    },
                }],
            }
        }
        outputs = list(self.spider.parse_api(response("https://ac.cnstrc.com/browse/group_id/EC", json.dumps(payload), self.meta)))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["price"], 459.99)
        self.assertEqual(item["web_product_id"], "23993915")
        self.assertEqual(item["total_pages"], 2)
        self.assertEqual(item["source"], "hsn_constructor_browse_api")
        self.assertIsInstance(outputs[1], Request)


if __name__ == "__main__":
    unittest.main()
