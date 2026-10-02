from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.adidas_categories import ADIDAS_CATEGORIES, ADIDAS_CATEGORY_SECTIONS
from common.spiders.adidas_listing_spider import AdidasListingSpider


class AdidasListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = AdidasListingSpider(category="mens-shoes", max_pages=2)
        self.sample = Path("sample/adidas-listing-sample.html").read_text(encoding="utf-8")
        self.page2 = Path("sample/adidas-listing-page2.html").read_text(encoding="utf-8")

    def response(self, body=None, page=1, start=0):
        url = f"https://www.adidas.com/us/men-shoes?start={start}" if start else "https://www.adidas.com/us/men-shoes"
        request = Request(
            url,
            meta={
                "category": "mens-shoes",
                "department": "MEN'S SHOES",
                "subcategory": "Men's Shoes",
                "page": page,
                "start": start,
                "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(url, request=request, body=body or self.sample, encoding="utf-8")

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(ADIDAS_CATEGORY_SECTIONS), 25)
        self.assertEqual(len(ADIDAS_CATEGORIES), 196)
        self.assertEqual(len({entry["url"] for entry in ADIDAS_CATEGORIES}), 196)
        self.assertEqual(
            {entry["category"] for entry in ADIDAS_CATEGORIES if entry["subcategory"] == "Samba"},
            {"samba"},
        )
        self.assertEqual(
            AdidasListingSpider(category="mens-athletic-sneakers").resolve_target_url(),
            "https://www.adidas.com/us/men-athletic_sneakers",
        )
        # every category URL is a real, crawlable /us/ PLP route
        self.assertTrue(all(entry["url"].startswith("https://www.adidas.com/us/") for entry in ADIDAS_CATEGORIES))

    def test_missing_category_arg_raises_with_available_names(self):
        with self.assertRaisesRegex(ValueError, "Available categories"):
            AdidasListingSpider()

    def test_hydration_mapping_feed_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.response()))
        items = [out for out in outputs if isinstance(out, dict)]
        follow = outputs[-1]
        self.assertEqual(len(items), 48)
        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "KK1153")
        self.assertEqual(item["style_id"], "BTP23")
        self.assertEqual(item["title"], "Handball Spezial Shoes")
        self.assertEqual(item["brand"], "Originals")
        self.assertEqual(item["product_category"], "Originals")
        self.assertEqual(item["price"], 110.0)
        self.assertIsNone(item["original_price"])
        self.assertIsNone(item["discount_percentage"])
        self.assertFalse(item["on_sale"])
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["colorway_count"], 52)
        self.assertEqual(item["colorway_ids"].split(", ")[0], "KK1153")
        self.assertEqual(item["rating"], 4.8163)
        self.assertEqual(item["reviews_count"], 10913)
        self.assertEqual(item["badges"], "Best Seller")
        self.assertEqual(item["total_count"], 1596)
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["source"], "adidas_next_data_page_props_products")
        self.assertEqual(item["raw"]["id"], "KK1153")
        self.assertEqual(follow.url, "https://www.adidas.com/us/men-shoes?start=48")
        self.assertEqual(follow.meta["start"], 48)
        self.assertEqual(follow.meta["page"], 2)
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")

    def test_sale_pricing_prefers_sale_over_original(self):
        sale = next(
            item for item in self.spider.parse(self.response())
            if isinstance(item, dict) and item["on_sale"]
        )
        self.assertEqual(sale["item_id"], "KH6893")
        self.assertEqual(sale["price"], 65.0)
        self.assertEqual(sale["original_price"], 130.0)
        self.assertEqual(sale["discount_percentage"], 50)

    def test_negative_review_sentinel_normalizes_to_null(self):
        body = self.sample.replace('"ratingCount":10913', '"ratingCount":-99', 1)
        item = next(out for out in self.spider.parse(self.response(body)) if isinstance(out, dict))
        self.assertEqual(item["item_id"], "KK1153")
        self.assertIsNone(item["reviews_count"])
        self.assertEqual(item["raw"]["ratingCount"], -99)

    def test_page_two_follows_view_size_step_and_dedupes(self):
        three_page = AdidasListingSpider(category="mens-shoes", max_pages=3)
        list(three_page.parse(self.response()))
        outputs = list(three_page.parse(self.response(self.page2, page=2, start=48)))
        items = [out for out in outputs if isinstance(out, dict)]
        self.assertEqual(len(items), 48)
        self.assertTrue(all(item["page"] == 2 for item in items))
        self.assertTrue(all(item["total_count"] == 1596 for item in items))
        # page 2 continues from start=48 with its own window
        self.assertEqual(outputs[-1].url, "https://www.adidas.com/us/men-shoes?start=96")
        self.assertEqual(outputs[-1].meta["start"], 96)

    def test_max_pages_caps_pagination(self):
        single = AdidasListingSpider(category="mens-shoes", max_pages=1)
        outputs = list(single.parse(self.response()))
        self.assertEqual(len(outputs), 48)
        self.assertTrue(all(isinstance(out, dict) for out in outputs))

    def test_out_of_range_page_type_stops_silently(self):
        body = self.sample.replace('"pageType":"ProductListingPage"', '"pageType":"ERROR"')
        self.assertEqual(list(self.spider.parse(self.response(body, page=2, start=5000))), [])

    def test_missing_and_malformed_hydration_fail_visibly(self):
        for body in ("<html></html>", '<script id="__NEXT_DATA__" type="application/json">{bad}</script>'):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "adidas"):
                list(self.spider.parse(self.response(body)))

    def test_non_list_products_fail_visibly(self):
        body = '<script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{"pageType":"ProductListingPage","products":{}}}}</script>'
        with self.assertRaisesRegex(RuntimeError, "list-valued products"):
            list(self.spider.parse(self.response(body)))

    def test_non_listing_page_type_on_first_page_fails_visibly(self):
        body = self.sample.replace('"pageType":"ProductListingPage"', '"pageType":"ERROR"')
        with self.assertRaisesRegex(RuntimeError, "not a ProductListingPage"):
            list(self.spider.parse(self.response(body)))


if __name__ == "__main__":
    unittest.main()