from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.iherb_categories import IHERB_CATEGORIES
from common.spiders.iherb_listing_spider import IherbListingSpider


def response_for(payload, *, page=1):
    request = Request(
        "https://catalog.app.iherb.com/category/magnesium/products",
        meta={
            "page": page,
            "category": "magnesium",
            "department": "Supplements",
            "subcategory": "Magnesium",
            "category_url_name": "magnesium",
            "listing_url": "https://www.iherb.com/c/magnesium",
        },
    )
    body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    return TextResponse(request.url, request=request, body=body, encoding="utf-8")


PRODUCT = {
    "productId": 16567,
    "displayName": "Doctor's Best, Magnesium, 240 Tablets",
    "name": "Magnesium, 240 Tablets",
    "url": "https://ua.iherb.com/pr/doctor-s-best-magnesium/16567",
    "partNumber": "DRB-00087",
    "listPrice": "$29.99",
    "discountPrice": "$23.99",
    "discountPriceValue": "23.99",
    "currencySymbol": "$",
    "showDiscount": True,
    "rating": 4.8,
    "ratingCount": 215219,
    "isOutOfStock": False,
    "brandCode": "DRB",
    "brandName": "Doctor's Best",
    "primaryImageIndex": 214,
    "promoCode": "SAVE20",
    "discountMessage": "20% off code: SAVE20",
    "isNew": False,
    "isShippingSaver": True,
    "isFeaturedBrand": False,
    "isIherbPick": True,
    "isExpressDelivery": False,
    "isAutoship": True,
    "productForm": "Tablet",
    "potency": "100 mg",
    "packageQuantity": "240 count",
    "pricePerServing": "$0.20/serving",
    "productStatus": 0,
    "groupId": 0,
}


class IherbListingSpiderTests(unittest.TestCase):
    def spider(self, **kwargs):
        return IherbListingSpider(category="magnesium", **kwargs)

    def test_taxonomy_is_unique_and_complete(self):
        self.assertEqual(len(IHERB_CATEGORIES), 380)
        self.assertEqual(len({entry["url"] for entry in IHERB_CATEGORIES}), 380)
        self.assertEqual(len({entry["category"] for entry in IHERB_CATEGORIES}), 380)
        self.assertTrue(all("?" not in entry["url"] for entry in IHERB_CATEGORIES))
        self.assertEqual({entry["department"] for entry in IHERB_CATEGORIES}, {
            "Supplements", "Sports", "Bath", "Beauty", "Grocery", "Home",
            "Baby", "Pets", "Health Topics",
        })

    def test_request_uses_only_catalog_api(self):
        spider = self.spider(max_pages=2)
        request = next(spider.start_requests())
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url, "https://catalog.app.iherb.com/category/magnesium/products")
        self.assertEqual(json.loads(request.body), {"page": 1, "pageSize": 50})
        self.assertEqual(request.meta["page"], 1)

    def test_item_and_export_contract(self):
        spider = self.spider()
        item = list(spider.parse(response_for({"totalSize": 857, "products": [PRODUCT]})))[0]
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "16567")
        self.assertEqual(item["price"], 23.99)
        self.assertEqual(item["list_price"], 29.99)
        self.assertEqual(item["discount_percent"], 20.01)
        self.assertEqual(item["currency"], "USD")
        self.assertTrue(item["in_stock"])
        self.assertEqual(item["url"], "https://www.iherb.com/pr/doctor-s-best-magnesium/16567")
        self.assertEqual(
            item["image_url"],
            "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/drb/drb00087/u/214.jpg",
        )
        self.assertEqual(item["raw"], PRODUCT)

    def test_hidden_price_and_availability(self):
        product = {**PRODUCT, "hidePrice": True, "isOutOfStock": True}
        item = list(self.spider().parse(response_for({"totalSize": 1, "products": [product]})))[0]
        self.assertIsNone(item["price"])
        self.assertIsNone(item["list_price"])
        self.assertFalse(item["in_stock"])
        self.assertEqual(item["availability"], "out_of_stock")

    def test_second_page_request_and_duplicate_stop(self):
        spider = self.spider(max_pages=3)
        outputs = list(spider.parse(response_for({"totalSize": 120, "products": [PRODUCT]})))
        self.assertEqual(len(outputs), 2)
        self.assertEqual(outputs[-1].meta["page"], 2)
        duplicate_page = response_for({"totalSize": 120, "products": [PRODUCT]}, page=2)
        self.assertEqual(list(spider.parse(duplicate_page)), [])

    def test_last_page_stops(self):
        spider = self.spider(max_pages=4, page_size=50)
        outputs = list(spider.parse(response_for({"totalSize": 50, "products": [PRODUCT]})))
        self.assertEqual(len(outputs), 1)

    def test_page_size_is_capped(self):
        self.assertEqual(self.spider(page_size=999).page_size, 50)
        self.assertEqual(self.spider(page_size=0).page_size, 1)

    def test_contract_and_challenge_fail_loudly(self):
        spider = self.spider()
        with self.assertRaisesRegex(RuntimeError, "no products array"):
            list(spider.parse(response_for({"message": "unknown category"})))
        challenge = response_for(b"<html>Just a moment...</html>")
        with self.assertRaisesRegex(RuntimeError, "non-JSON"):
            list(spider.parse(challenge))

    def test_empty_first_page_fails(self):
        with self.assertRaisesRegex(RuntimeError, "empty first page"):
            list(self.spider().parse(response_for({"totalSize": 0, "products": []})))


if __name__ == "__main__":
    unittest.main()
