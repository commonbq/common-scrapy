from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.zappos_categories import ZAPPOS_CATEGORIES, ZAPPOS_CATEGORY_INVENTORY
from common.spiders.zappos_listing_spider import ZapposListingSpider


class ZapposListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = ZapposListingSpider(category="women", max_pages=2)
        self.sample = Path("sample/zappos-listing-sample.html").read_text(encoding="utf-8")

    def response(self, body=None, page=1):
        url = "https://www.zappos.com/women/wAEB4gIBGA.zso" + ("?p=1" if page == 2 else "")
        request = Request(url, meta={"category": "women", "department": "Women", "page": page, "proxy": "http://proxy.invalid:8080"})
        return TextResponse(url, request=request, body=body or self.sample, encoding="utf-8")

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(ZAPPOS_CATEGORY_INVENTORY), 4)
        self.assertEqual(len(ZAPPOS_CATEGORIES), 50)
        spider = ZapposListingSpider(category="women-shoes")
        self.assertIn("women-shoes", spider.resolve_target_url())

    def test_state_mapping_feed_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.response()))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "8910671")
        self.assertEqual(item["brand"], "Fjällräven")
        self.assertEqual(item["price"], 300.0)
        self.assertEqual(item["original_price"], 375.0)
        self.assertTrue(item["image_url"].endswith("4036549-t-THUMBNAIL.jpg"))
        self.assertTrue(item["on_sale"])
        self.assertEqual(item["total_count"], 29543)
        follow = outputs[1]
        self.assertEqual(follow.url, "https://www.zappos.com/women/wAEB4gIBGA.zso?p=1")
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")

    def test_page_two_is_followed_and_deduplicated(self):
        list(self.spider.parse(self.response()))
        page_two = self.sample.replace('"productId":"8910671"', '"productId":"9999999"').replace('<link rel="next" href="/women/wAEB4gIBGA.zso?p=1">', "")
        items = list(self.spider.parse(self.response(page_two, page=2)))
        self.assertEqual([item["item_id"] for item in items], ["9999999"])
        self.assertEqual(items[0]["page"], 2)

    def test_missing_and_malformed_state_fail_visibly(self):
        for body in ("<html></html>", "<script>window.__INITIAL_STATE__ = {bad};</script>"):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "No valid Zappos"):
                list(self.spider.parse(self.response(body)))

    def test_non_list_products_fail_visibly(self):
        body = '<script>window.__INITIAL_STATE__ = {"products":{"list":{}}};</script>'
        with self.assertRaisesRegex(RuntimeError, "list-valued products.list"):
            list(self.spider.parse(self.response(body)))


if __name__ == "__main__":
    unittest.main()
