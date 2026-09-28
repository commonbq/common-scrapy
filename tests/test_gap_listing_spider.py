from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.gap_listing_spider import GapListingSpider


class GapListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = GapListingSpider(category="women", max_pages=2)

    def response(self, payload, page=1):
        request = Request(
            "https://api.gap.com/commerce/search/products/v2/cc?cid=13658&page=0",
            meta={
                "page": page,
                "category": "women",
                "subcategory": "dresses",
                "listing_url": "https://www.gap.com/browse/category.do?cid=13658",
            },
        )
        return TextResponse(
            request.url,
            request=request,
            body=json.dumps(payload).encode(),
            encoding="utf-8",
        )

    def test_feed_fields_match_item_order(self):
        self.assertEqual(
            self.spider.custom_settings["FEED_EXPORT_FIELDS"],
            [
                "category", "subcategory", "item_id", "style_id", "title",
                "brand", "url", "image_url", "color", "price",
                "original_price", "currency", "availability", "rating",
                "reviews_count", "page", "source", "raw",
            ],
        )

    def test_api_product_parsing_and_pagination(self):
        payload = {
            "pagination": {"pageNumberTotal": "3"},
            "products": [{
                "styleId": "912593", "styleName": "Denim Mini Shift Dress",
                "reviewScore": 4.5, "reviewCount": 12,
                "styleColors": [{
                    "ccId": "909364002", "ccName": "Blue",
                    "ccShortDescription": "dark wash", "effectivePrice": "44.0",
                    "regularPrice": "89.95", "inventoryStatus": "In Stock",
                    "images": [{"type": "P01", "path": "/webcontent/dress.jpg"}],
                }],
            }],
        }
        outputs = list(self.spider.parse_api(self.response(payload)))
        item = outputs[0]
        self.assertEqual(item["item_id"], "909364002")
        self.assertEqual(item["price"], 44.0)
        self.assertEqual(item["image_url"], "https://www.gap.com/webcontent/dress.jpg")
        self.assertEqual(outputs[1].meta["page"], 2)
        self.assertIn("page=1", outputs[1].url)

    def test_start_requests_cover_selected_category(self):
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), len(self.spider.categories["women"]))
        self.assertTrue(all("api.gap.com" in request.url for request in requests))


if __name__ == "__main__":
    unittest.main()
