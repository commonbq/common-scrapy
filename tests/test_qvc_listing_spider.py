import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.qvc_listing_spider import QVC_CATEGORIES, QvcListingSpider


class QvcListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = QvcListingSpider(category="fashion", max_pages=2)
        html = Path("sample/qvc-fashion-sample.html").read_text()
        request = Request(
            QVC_CATEGORIES["fashion"][0], meta={"category": "fashion", "page": 1}
        )
        self.response = HtmlResponse(request.url, request=request, body=html, encoding="utf-8")

    def test_parse_exports_observed_gallery_contract_and_pagination(self):
        first, second, next_request = list(self.spider.parse(self.response))

        self.assertEqual(list(self.spider.custom_settings["FEED_EXPORT_FIELDS"]), list(first))
        self.assertEqual("NAV6285", first["category_id"])
        self.assertEqual("A740517", first["item_id"])
        self.assertEqual(59.98, first["price"])
        self.assertEqual(73.0, first["original_price"])
        self.assertEqual("Today's Special Value", first["badge"])
        self.assertEqual("Free Standard S&H", first["shipping_promo"])
        self.assertEqual("TSV", first["special_price_code"])
        self.assertEqual(3, first["installment_count"])
        self.assertEqual(5326, first["total_products"])
        self.assertEqual(4.3, second["rating"])
        self.assertEqual(2419, second["reviews_count"])
        self.assertEqual(1, second["colors_count"])
        self.assertEqual(
            "https://www.qvc.com/c/fashion/-/lglt/c.html?currentPage=2",
            next_request.url,
        )

    def test_bootstrap_state_is_optional_when_cards_are_present(self):
        response = self.response.replace(
            body=self.response.text.replace("var utag_data", "var unavailable_state").encode()
        )
        first = list(self.spider.parse(response))[0]
        self.assertIsNone(first["category_id"])
        self.assertEqual(1, first["page"])

    def test_missing_grid_has_no_fallback_items(self):
        blocked = self.response.replace(body=b"<html><body>blocked</body></html>")
        self.assertEqual([], list(self.spider.parse(blocked)))


if __name__ == "__main__":
    unittest.main()
