from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.levi_categories import LEVI_CATEGORIES, LEVI_CATEGORY_INVENTORY, LEVI_SITE_BASE
from common.spiders.levis_listing_spider import LevisListingSpider

FIRSTCAT_URL = (
    "https://www.levi.com/US/en_US/new-arrivals/mens-new-arrivals/"
    "c/levi_clothing_men_new_arrivals_us"
)
JEANS_URL = "https://www.levi.com/US/en_US/clothing/men/jeans/c/levi_clothing_men_jeans"


class LevisListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = LevisListingSpider(category="men-s-new-arrivals", max_pages=2)
        self.firstcat = Path("sample/levi-firstcat-sample.html").read_text(encoding="utf-8")
        self.page_two = Path("sample/levi-listing-page2.html").read_text(encoding="utf-8")

    def response(self, body, url=FIRSTCAT_URL, page=1):
        request = Request(
            url,
            meta={
                "category": "men-s-new-arrivals",
                "department": "New",
                "subcategory": "New",
                "base_url": url,
                "page": page,
                "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(url, request=request, body=body, encoding="utf-8")

    def test_inventory_shape_and_category_selection(self):
        self.assertEqual(len(LEVI_CATEGORY_INVENTORY), 5)
        self.assertEqual(len(LEVI_CATEGORIES), 83)
        names = [entry["category"] for entry in LEVI_CATEGORIES]
        urls = [entry["url"] for entry in LEVI_CATEGORIES]
        self.assertEqual(len(set(names)), len(names))
        self.assertEqual(len(set(urls)), len(urls))
        self.assertTrue(all(url.startswith(LEVI_SITE_BASE + "/") for url in urls))
        self.assertTrue(all("/c/" in url for url in urls))
        self.assertIn("men-s-new-arrivals", names)

    def test_state_mapping_feed_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.response(self.firstcat)))
        items = [entry for entry in outputs if isinstance(entry, dict)]
        follows = [entry for entry in outputs if not isinstance(entry, dict)]
        self.assertEqual(len(items), 24)
        self.assertEqual(len(follows), 1)

        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "005013912")
        self.assertEqual(item["title"], "501\u00ae Original Men's Jeans")
        self.assertEqual(item["url"], LEVI_SITE_BASE + "/clothing/men/jeans/straight/501-original-mens-jeans/p/005013912")
        self.assertTrue(item["image_url"].startswith("https://lscoglobal.scene7.com/"))
        self.assertEqual(item["price"], 74.99)
        self.assertEqual(item["original_price"], 84.95)
        self.assertEqual(item["currency"], "USD")
        self.assertTrue(item["on_sale"])
        self.assertEqual(item["rating"], 4.2477)
        self.assertEqual(item["reviews_count"], 11322)
        self.assertEqual(item["category_code"], "levi_clothing_men_new_arrivals_us")
        self.assertEqual(item["total_count"], 197)
        self.assertEqual(item["source"], "levis_lsco_initial_state_products")
        self.assertIsInstance(item["raw"], dict)
        self.assertEqual(item["raw"]["code"], "005013912")

        follow = follows[0]
        self.assertEqual(follow.url, FIRSTCAT_URL + "?page=1")
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")

    def test_page_two_uses_pagination_state(self):
        page_two_spider = LevisListingSpider(category="shop-all-men-s-jeans", max_pages=3)
        outputs = list(page_two_spider.parse(self.response(self.page_two, url=JEANS_URL + "?page=1", page=2)))
        items = [entry for entry in outputs if isinstance(entry, dict)]
        follow = [entry for entry in outputs if not isinstance(entry, dict)]
        self.assertEqual(len(items), 24)
        self.assertEqual(items[0]["item_id"], "295071711")
        self.assertEqual(items[0]["page"], 2)
        self.assertEqual(items[0]["total_count"], 174)
        # currentPage=1 of totalPages=8 -> next page would be ?page=2.
        self.assertEqual(follow[0].url, JEANS_URL + "?page=2")

    def test_dedupe_across_pages(self):
        list(self.spider.parse(self.response(self.firstcat)))
        repeats = list(self.spider.parse(self.response(self.firstcat, url=FIRSTCAT_URL + "?page=1", page=2)))
        self.assertEqual([entry for entry in repeats if isinstance(entry, dict)], [])

    def test_missing_and_malformed_state_fail_visibly(self):
        for body in ("<html></html>", "<script>window.__LSCO_INITIAL_STATE__ = {bad};</script>"):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "No valid Levi's"):
                list(self.spider.parse(self.response(body)))

    def test_state_without_product_list_fails_visibly(self):
        body = (
            '<script>Object.defineProperty(window, "__LSCO_INITIAL_STATE__", '
            '{value: {"foo": 1}});</script>'
        )
        with self.assertRaisesRegex(RuntimeError, "no ssrViewStoreProductList"):
            list(self.spider.parse(self.response(body)))


if __name__ == "__main__":
    unittest.main()
