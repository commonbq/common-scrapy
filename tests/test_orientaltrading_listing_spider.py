from __future__ import annotations

import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.orientaltrading_listing_spider import OrientaltradingListingSpider


LISTING = """
<html><head><link rel="next" href="?pg=2"></head><body>
<a class="js_quickview" href="/web/browse/productQuickView?sku=13913005&amp;categoryId=90000%2b1604">Quick View</a>
<a class="js_quickview" href="/web/browse/productQuickView?sku=13913005&amp;categoryId=90000%2b1604">duplicate</a>
</body></html>
"""

API = """
<div id="quickview_item" data-sku="13913005">
  <div class="c_sku_image"><img data-src="https://i.example/main.jpg"><img data-src="https://i.example/second.jpg"></div>
  <div id="pdp_main_item_details">
    <a class="c_module_hover_text" href="/bulk-candy-a2-13913005.fltr?sku=x">Bulk Candy</a>
    <div class="c_rating" title="4.5/5.0 Stars"><span class="c_rating_count">(122)</span></div>
    <div class="c_sku_description_trimmed">A large candy assortment.</div>
    <input name="sku" value="13913005"><input name="price" value="169.98">
    <input name="stock_status" value="IN"><input name="rating" value="4.50">
    <input name="reviews" value="122"><input name="brand" value="OTC">
    <input name="category_id" value="553760"><input name="category_name" value="Candy">
    <input name="badge" value="FLOS_DEALS"><input name="uom" value="3000 Piece(s)">
  </div>
</div>
<!-- item_was_price = 184.99 WAS PRICE -->
"""


def response(url: str, body: str, meta=None):
    request = Request(url, meta=meta or {})
    return HtmlResponse(url=url, request=request, body=body.encode(), encoding="utf-8")


class OrientaltradingListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = OrientaltradingListingSpider(category="sale", max_pages=2)

    def test_listing_discovers_api_once_and_paginates(self):
        result = list(self.spider.parse_listing(response(
            "https://www.orientaltrading.com/sale-a1-90000+1604-1.fltr",
            LISTING,
            {"category": "sale", "category_url": "https://example/category", "page": 1},
        )))
        self.assertEqual(2, len(result))
        self.assertIn("productQuickView", result[0].url)
        self.assertEqual(2, result[1].meta["page"])

    def test_api_maps_rich_product_contract(self):
        item = next(self.spider.parse_api(response(
            "https://www.orientaltrading.com/web/browse/productQuickView?sku=13913005",
            API,
            {"category": "sale", "category_url": "https://example/category", "discovery_url": "https://example/page", "page": 1, "position": 1, "sku": "13913005"},
        )))
        self.assertEqual("13913005", item["item_id"])
        self.assertEqual("Bulk Candy", item["title"])
        self.assertEqual(169.98, item["price"])
        self.assertEqual(184.99, item["original_price"])
        self.assertEqual(2, len(item["image_urls"]))
        self.assertEqual("in_stock", item["availability"])
        self.assertEqual("orientaltrading_quick_view_api", item["source"])

    def test_feed_fields_match_item(self):
        item = next(self.spider.parse_api(response(
            "https://www.orientaltrading.com/web/browse/productQuickView?sku=13913005",
            API,
            {"category": "sale", "category_url": "x", "discovery_url": "y", "page": 1, "position": 1, "sku": "13913005"},
        )))
        self.assertEqual(self.spider.custom_settings["FEED_EXPORT_FIELDS"], list(item))

    def test_api_limit_bounds_live_smoke_runs(self):
        spider = OrientaltradingListingSpider(category="sale", api_limit=1)
        result = list(spider.parse_listing(response(
            "https://www.orientaltrading.com/sale-a1-90000+1604-1.fltr",
            LISTING,
            {"category": "sale", "category_url": "x", "page": 1},
        )))
        self.assertEqual(1, len(result))


if __name__ == "__main__":
    unittest.main()
