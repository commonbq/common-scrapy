import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.anthropologie_listing_spider import AnthropologieListingSpider


class AnthropologieListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = AnthropologieListingSpider(category="womens-clothing", max_pages=2)

    def response(self, state):
        body = f'<script id="urbnInitialPiniaState">{json.dumps(json.dumps(state))}</script>'
        request = Request(
            "https://www.anthropologie.com/womens-clothing?page=1",
            meta={"category": "womens-clothing", "page": 1},
        )
        return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_pinia_feed_contract_and_pagination(self):
        tile = {
            "recordType": "PRODUCT",
            "faceOutColorCode": "702",
            "faceOutImage": "4114086690121_702_b14",
            "product": {
                "productId": "AN-4114086690121-000",
                "styleNumber": "4114086690121",
                "displayName": "Goldie Cashmere Sweater",
                "brand": "By Anthropologie",
                "productSlug": "goldie-cashmere-sweater",
                "facets": {"colors": [{"colorId": "702"}, {"colorId": "001"}]},
                "badges": [{"type": "A_PLUS"}],
            },
            "reviews": {"averageRating": 4.5, "count": 12},
            "skuInfo": {"hasAvailableSku": True, "listPriceLow": 138, "salePriceLow": 118},
        }
        state = {"category": {"currentPage": 1, "totalPages": 3, "pages": {"1": {"wrapper": {"tiles": [tile]}}}}}
        output = list(self.spider.parse(self.response(state)))
        self.assertEqual(list(output[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(output[0]["item_id"], "AN-4114086690121-000")
        self.assertEqual(output[0]["price"], 118.0)
        self.assertEqual(output[0]["color_count"], 2)
        self.assertEqual(output[0]["source"], "urbn_pinia_hydration")
        self.assertEqual(output[1].url, "https://www.anthropologie.com/womens-clothing?page=2")

    def test_missing_hydration_fails_visibly(self):
        request = Request("https://www.anthropologie.com/womens-clothing")
        response = HtmlResponse(request.url, body="<html></html>", encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "No Anthropologie urbnInitialPiniaState"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
