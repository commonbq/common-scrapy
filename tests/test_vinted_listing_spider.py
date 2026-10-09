from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.vinted_listing_spider import VintedListingSpider


URL = "https://www.vinted.com/catalog/1918-home"


def document(records, pagination=None):
    state = {"items": {"items": records, "pagination": pagination or {}}}
    flight = "7b:" + json.dumps(state, separators=(",", ":"))
    return f"<script>self.__next_f.push([1,{json.dumps(flight)}])</script>"


def record(item_id=10287111268):
    return {
        "id": item_id,
        "productItem": {
            "id": item_id,
            "title": "Handmade Patriotic Rice Heating Bag",
            "url": f"/items/{item_id}-handmade-patriotic-rice-heating-bag",
            "favouriteCount": 7,
            "priceWithDiscount": None,
            "price": {"amount": "6.00", "currencyCode": "USD"},
            "serviceFee": {"amount": "1.00", "currencyCode": "USD"},
            "totalItemPrice": {"amount": "7.00", "currencyCode": "USD"},
            "isPromoted": False,
            "thumbnailUrl": "https://images1.vinted.net/example.webp",
            "thumbnailUrls": ["https://images1.vinted.net/example.webp"],
            "user": {"id": 3195669312, "isBusiness": False},
            "itemBox": {
                "firstLine": "US",
                "secondLine": "Other · New without tags",
                "accessibilityLabel": "Handmade Patriotic Rice Heating Bag, Brand: US, Condition: New without tags, Size: Other, 6.00 $, 7.00 $",
                "exposure": "$undefined",
            },
        },
        "catalogTracking": {"contentSource": "catalog_items", "searchScore": 0.75},
    }


class VintedListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = VintedListingSpider(category="home", max_pages=2)

    def response(self, body, page=1):
        request = Request(URL, meta={"category_entry": self.spider.categories[0], "page": page})
        return TextResponse(URL, request=request, body=body, encoding="utf-8")

    def test_inventory_has_twenty_unique_categories(self):
        self.assertEqual(len(self.spider.categories), 20)
        self.assertEqual(len({entry["category"] for entry in self.spider.categories}), 20)
        self.assertEqual(len({entry["url"] for entry in self.spider.categories}), 20)

    def test_rsc_item_contract_and_hydrated_pagination(self):
        outputs = list(self.spider.parse(self.response(document(
            [record()],
            {"current_page": 1, "per_page": 96, "total_entries": 960, "total_pages": 10},
        ))))
        items = [value for value in outputs if isinstance(value, dict)]
        requests = [value for value in outputs if not isinstance(value, dict)]

        self.assertEqual(len(items), 1)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, URL + "?page=2")
        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "10287111268")
        self.assertEqual(item["brand"], "US")
        self.assertEqual(item["condition"], "New without tags")
        self.assertEqual(item["size"], "Other")
        self.assertEqual(item["price"], 6)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["total_pages"], 10)
        self.assertEqual(item["source"], "vinted_nextjs_rsc_catalog_items")
        self.assertIsNone(item["raw"]["productItem"]["itemBox"]["exposure"])

    def test_no_html_or_json_ld_fallback(self):
        with self.assertRaisesRegex(RuntimeError, "no Next.js RSC flight chunks"):
            list(self.spider.parse(self.response('<div data-testid="grid-item"></div>')))

    def test_duplicate_ids_do_not_emit_or_paginate(self):
        body = document([record(), record()], {"current_page": 1, "total_pages": 1})
        outputs = list(self.spider.parse(self.response(body)))
        self.assertEqual(len(outputs), 1)

    def test_proxy_error_envelope_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "proxy error"):
            list(self.spider.parse(self.response('{"API Credits":"consumed"}')))


if __name__ == "__main__":
    unittest.main()
