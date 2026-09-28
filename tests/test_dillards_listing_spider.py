import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.dillards_listing_spider import DILLARDS_CATEGORIES, DillardsListingSpider


class DillardsListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = DillardsListingSpider(category="women", max_pages=2)
        html = Path("sample/dillards-listing-sample.html").read_text()
        request = Request("https://www.dillards.com/c/women-dresses", meta={"category": "women", "subcategory": "women-dresses", "page": 1})
        self.response = HtmlResponse(request.url, request=request, body=html, encoding="utf-8")

    def test_category_inventory_has_all_departments_and_children(self):
        self.assertEqual(10, len(DILLARDS_CATEGORIES))
        self.assertEqual(124, sum(len(urls) for urls in DILLARDS_CATEGORIES.values()))
        self.assertEqual(len(DILLARDS_CATEGORIES["women"]), len(set(DILLARDS_CATEGORIES["women"])))

    def test_parse_exports_contract_and_next_page(self):
        output = list(self.spider.parse(self.response))
        item, request = output
        self.assertEqual(list(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), list(item))
        self.assertEqual("520620253", item["item_id"])
        self.assertEqual(208.0, item["price"])
        self.assertEqual(20, item["reviews_count"])
        self.assertEqual("20619482", item["raw"]["partNumber"])
        self.assertEqual("https://www.dillards.com/c/women-dresses?pageNumber=2", request.url)

    def test_deduplicates_items(self):
        list(self.spider.parse(self.response))
        self.assertFalse(any(isinstance(value, dict) for value in self.spider.parse(self.response)))

    def test_missing_bootstrap_fails_without_speculative_fallback(self):
        response = self.response.replace(body=b"<html>blocked</html>")
        self.assertEqual([], list(self.spider.parse(response)))


if __name__ == "__main__":
    unittest.main()
