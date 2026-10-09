from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.abercrombie_categories import ABERCROMBIE_CATEGORIES
from common.spiders.abercrombie_listing_spider import AbercrombieListingSpider


def state(page=1, total_pages=2):
    product_key = "Product:63617023"
    query_key = (
        'category({"categoryId":"12203","rows":"90",'
        f'"start":"{(page - 1) * 90}"}})'
    )
    return {
        "CACHE": {
            "ROOT_QUERY": {
                "__typename": "Query",
                query_key: {
                    "__typename": "Category",
                    "categoryId": "12203",
                    "productTotalCount": 91,
                    "pagination": {"currentPage": page, "totalPages": total_pages},
                    'products({"cacheEmpty":false})': [{"__ref": product_key}],
                },
            },
            product_key: {
                "__typename": "Product",
                "id": "63617023",
                "partNumber": "ANF_KIC_144-6328-00243-480",
                "kic": "KIC_144-6328-00243-480",
                "name": "A&F Carrie Wool-Blend Trench Coat",
                "gender": "F",
                "departmentName": "women's",
                "productPageUrl": "/shop/us/p/carrie-trench-63616417?categoryId=12203",
                "imageSet": {"primaryFaceOutImage": "KIC_144-6328-00243-480_life1"},
                "price": {
                    "description": "$200", "originalPrice": "$250",
                    "discountPrice": "$200", "discountText": "20% Off",
                    "priceFlag": "sale",
                },
                "badges": [{"text": "New!", "theme": "newArrival"}],
                "collection": "707489",
                "onlineAvailability": True,
                "memberPrice": {"description": "$180"},
                "promoMessaging": {"message": "Limited time"},
                "swatchList": [
                    {"__ref": "ProductSwatch:KIC_144-6328-00243-480"},
                    {"__ref": "ProductSwatch:KIC_144-6325-00250-428"},
                ],
            },
            "ProductSwatch:KIC_144-6328-00243-480": {
                "__typename": "ProductSwatch", "id": "KIC_144-6328-00243-480",
                "name": "Dark Navy",
            },
            "ProductSwatch:KIC_144-6325-00250-428": {
                "__typename": "ProductSwatch", "id": "KIC_144-6325-00250-428",
                "name": "Light Brown Houndstooth",
            },
        }
    }


def response(payload, page=1):
    base = "https://www.abercrombie.com/shop/us/womens"
    url = AbercrombieListingSpider._page_url(base, page)
    request = Request(
        url, meta={"page": page, "base_url": base, "department": "Women's"},
    )
    body = (
        "<script type=\"application/ld+json\">{\"@type\":\"ItemList\"}</script>"
        f"<script>{AbercrombieListingSpider._marker}"
        f"{json.dumps(payload, separators=(',', ':'))};</script>"
        "<li data-aui=\"product-card\">ignored card</li>"
    )
    return TextResponse(url, request=request, body=body, encoding="utf-8")


class AbercrombieListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = AbercrombieListingSpider(category="womens", max_pages=2)

    def test_complete_category_inventory(self):
        self.assertEqual(len(ABERCROMBIE_CATEGORIES), 37)
        self.assertEqual(len({row["category"] for row in ABERCROMBIE_CATEGORIES}), 37)
        self.assertTrue(all(
            row["url"].startswith("https://www.abercrombie.com/shop/us/")
            for row in ABERCROMBIE_CATEGORIES
        ))

    def test_maps_apollo_product_and_feed_contract(self):
        outputs = list(self.spider.parse(response(state())))
        item = next(value for value in outputs if isinstance(value, dict))
        next_request = next(value for value in outputs if not isinstance(value, dict))
        self.assertEqual(item["item_id"], "ANF_KIC_144-6328-00243-480")
        self.assertEqual(item["product_id"], "63617023")
        self.assertEqual(item["color"], "Dark Navy")
        self.assertEqual(item["colors"], ["Dark Navy", "Light Brown Houndstooth"])
        self.assertEqual(item["price"], 200.0)
        self.assertEqual(item["original_price"], 250.0)
        self.assertEqual(item["member_price"], 180.0)
        self.assertEqual(item["badges"], ["New!"])
        self.assertEqual(item["source"], "abercrombie_catalog_apollo_bootstrap")
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(
            next_request.url,
            "https://www.abercrombie.com/shop/us/womens?start=90",
        )

    def test_second_page_does_not_schedule_beyond_max_pages(self):
        outputs = list(self.spider.parse(response(state(page=2), page=2)))
        self.assertEqual(len(outputs), 1)
        self.assertIsInstance(outputs[0], dict)
        self.assertEqual(outputs[0]["page"], 2)

    def test_deduplicates_part_numbers(self):
        self.assertEqual(len(list(self.spider.parse(response(state())))), 2)
        self.assertEqual(list(self.spider.parse(response(state()))), [])

    def test_no_html_or_json_ld_fallback(self):
        url = "https://www.abercrombie.com/shop/us/womens"
        request = Request(
            url, meta={"page": 1, "base_url": url, "department": "Women's"},
        )
        body = (
            '<script type="application/ld+json">{"@type":"Product"}</script>'
            '<li data-aui="product-card">card</li>'
        )
        missing = TextResponse(url, request=request, body=body, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "no catalog Apollo bootstrap"):
            list(self.spider.parse(missing))


if __name__ == "__main__":
    unittest.main()
