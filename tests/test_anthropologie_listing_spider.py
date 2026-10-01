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
        self.assertEqual(output[0]["currency"], "USD")
        self.assertEqual(output[1].url, "https://www.anthropologie.com/womens-clothing?page=2")

    def test_missing_hydration_fails_visibly(self):
        request = Request("https://www.anthropologie.com/womens-clothing")
        response = HtmlResponse(request.url, body="<html></html>", encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "No Anthropologie urbnInitialPiniaState"):
            list(self.spider.parse(response))

    def test_page_2_category_preserves_starting_page(self):
        spider = AnthropologieListingSpider(category="womens-clothing-page-2", max_pages=3)
        request = list(spider.start_requests())[0]
        self.assertIn("page=2", request.url)
        self.assertEqual(request.meta["page"], 2)

    def test_direct_url_and_category_url_modes_construct(self):
        url = "https://www.anthropologie.com/womens-clothing"
        self.assertEqual(AnthropologieListingSpider(url=url).resolve_target_url(), url)
        self.assertEqual(AnthropologieListingSpider(category_url=url).resolve_target_url(), url)
        with self.assertRaisesRegex(ValueError, "Provide -a category"):
            AnthropologieListingSpider()

    def test_every_exported_item_carries_a_non_empty_raw(self):
        tiles = [
            {
                "recordType": "PRODUCT",
                "faceOutColorCode": str(index),
                "faceOutImage": f"img_{index}",
                "product": {"productId": f"AN-{index:013d}-000", "productSlug": f"item-{index}"},
                "skuInfo": {"hasAvailableSku": True, "listPriceLow": 10 * index},
            }
            for index in range(1, 4)
        ]
        state = {"category": {"currentPage": 1, "totalPages": 1,
                               "pages": {"1": {"wrapper": {"tiles": tiles}}}}}
        items = [out for out in self.spider.parse(self.response(state)) if isinstance(out, dict)]
        self.assertEqual(len(items), 3)
        for item in items:
            self.assertIn("raw", item)
            self.assertIsInstance(item["raw"], dict)
            self.assertTrue(item["raw"], "raw must not be an empty placeholder")
            self.assertEqual(item["raw"]["recordType"], "PRODUCT")

    def test_currency_follows_the_crawled_storefront(self):
        ca = "https://www.anthropologie.com/en-ca/womens-clothing"
        us = "https://www.anthropologie.com/womens-clothing"
        # Locale fallback when the hydration carries no explicit currency.
        self.assertEqual(AnthropologieListingSpider._currency(ca, {}, {}, {}), "CAD")
        self.assertEqual(AnthropologieListingSpider._currency(us, {}, {}, {}), "USD")
        # An explicit hydrated currency always wins over the locale fallback.
        self.assertEqual(
            AnthropologieListingSpider._currency(us, {}, {}, {"currencyCode": "cad"}), "CAD")
        self.assertEqual(
            AnthropologieListingSpider._currency(ca, {"currency": "USD"}, {}, {}), "USD")
        self.assertEqual(
            AnthropologieListingSpider._currency(us, {"currency": " "}, {}, {}), "USD")

    def test_locale_is_preserved_in_product_urls(self):
        self.assertEqual(
            AnthropologieListingSpider._product_url(
                "https://www.anthropologie.com/en-ca/womens-clothing", "goldie-sweater", "702"),
            "https://www.anthropologie.com/en-ca/shop/goldie-sweater?color=702&type=STANDARD",
        )
        self.assertEqual(
            AnthropologieListingSpider._product_url(
                "https://www.anthropologie.com/womens-clothing", "goldie-sweater", "702"),
            "https://www.anthropologie.com/shop/goldie-sweater?color=702&type=STANDARD",
        )


if __name__ == "__main__":
    unittest.main()
