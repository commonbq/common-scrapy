import unittest
from pathlib import Path

import scrapy
from scrapy.http import HtmlResponse, Request

from common.spiders.sallybeauty_listing_spider import SallybeautyListingSpider


class SallybeautyListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = SallybeautyListingSpider(category="hair-care", max_pages="2")
        url = "https://www.sallybeauty.com/hair-care/shop-by-product/shampoo/"
        request = Request(url, meta={"page": 1, "category_url": url})
        body = Path("sample/sallybeauty-listing-product.html").read_bytes()
        self.response = HtmlResponse(url, request=request, body=body, encoding="utf-8")

    def test_feed_contract_and_items(self):
        results = list(self.spider.parse(self.response))
        items = [result for result in results if not isinstance(result, scrapy.Request)]
        requests = [result for result in results if isinstance(result, scrapy.Request)]
        self.assertEqual(list(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), list(items[0]))
        self.assertEqual(items[0]["item_id"], "SBS-539230")
        self.assertEqual(items[0]["price"], 11.99)
        self.assertEqual(items[0]["reviews_count"], 29)
        self.assertEqual(len(items), 2)
        self.assertEqual(len(requests), 1)
        self.assertIn("Search-UpdateGrid?cgid=shampoo&start=12&sz=12", requests[0].url)
        self.assertEqual(requests[0].headers[b"X-Requested-With"], b"XMLHttpRequest")

        body = Path("sample/sallybeauty-listing-product-page-2.html").read_bytes()
        response = HtmlResponse(
            requests[0].url,
            request=requests[0],
            body=body,
            encoding="utf-8",
        )
        page_two = list(self.spider.parse(response))
        self.assertEqual(len(page_two), 1)
        self.assertEqual(page_two[0]["item_id"], "SBS-539240")
        self.assertEqual(page_two[0]["page"], 2)
        self.assertEqual(page_two[0]["source"], "sallybeauty_sfcc_search_update_grid")

    def test_category_inventory(self):
        self.assertEqual(len(self.spider.categories), 12)
        self.assertIn("salon-supplies", self.spider.available_categories())


if __name__ == "__main__":
    unittest.main()
