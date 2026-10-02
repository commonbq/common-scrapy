from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.petsmart_categories import (
    PETSMART_CATEGORIES,
    PETSMART_CATEGORY_INVENTORY,
)
from common.spiders.petsmart_listing_spider import PetsmartListingSpider


class PetsmartListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = PetsmartListingSpider(category="dog/food", max_pages=2)
        self.sample = Path("sample/petsmart-dog-food.html").read_text(encoding="utf-8")
        self.sample_page2 = Path("sample/petsmart-dog-food-page2.html").read_text(encoding="utf-8")

    def response(self, body=None, page=1):
        url = "https://www.petsmart.com/dog/food/" + (f"?page={page}" if page > 1 else "")
        request = Request(
            url,
            meta={
                "category": "dog/food",
                "department": "dog",
                "page": page,
                "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(url, request=request, body=body or self.sample, encoding="utf-8")

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(PETSMART_CATEGORY_INVENTORY), 7)
        self.assertEqual(len(PETSMART_CATEGORIES), 113)
        spider = PetsmartListingSpider(category="dog/food/dry-food")
        self.assertEqual(
            spider.resolve_target_url(), "https://www.petsmart.com/dog/food/dry-food/"
        )
        spider = PetsmartListingSpider(category="small-pet")
        self.assertEqual(spider.resolve_target_url(), "https://www.petsmart.com/small-pet")

    def test_algolia_hydration_mapping_and_feed_contract(self):
        outputs = list(self.spider.parse(self.response()))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(len([o for o in outputs if isinstance(o, dict)]), 40)
        self.assertEqual(item["item_id"], "5252900")
        self.assertEqual(item["master_product_id"], 36648)
        self.assertEqual(item["sku"], "5252900")
        self.assertEqual(item["upc"], "038100175526")
        self.assertEqual(item["brand"], "Purina Pro Plan")
        self.assertEqual(item["manufacturer"], "NESTLE PURINA DRY")
        self.assertEqual(item["url"], "https://www.petsmart.com/-36648.html")
        self.assertIn("5252900", item["image_url"])
        self.assertEqual(item["price"], 77.99)
        self.assertEqual(item["list_price"], 77.99)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["availability"], "in_stock")
        self.assertTrue(item["in_stock_in_store"])
        self.assertTrue(item["is_subscription_enabled"])
        self.assertEqual(item["rating"], 4.5)
        self.assertEqual(item["reviews_count"], 9116)
        self.assertEqual(item["category_path"], "Dog > Food > Dry Food")
        self.assertEqual(item["primary_category"], "Dry Food")
        self.assertEqual(item["pet_type"], ["Dog"])
        self.assertEqual(item["total_count"], 1795)
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["source"], "petsmart_instantsearch_algolia")
        self.assertEqual(item["raw"]["objectID"], "5252900")
        follow = outputs[-1]
        self.assertEqual(follow.url, "https://www.petsmart.com/dog/food/?page=2")
        self.assertEqual(follow.meta["page"], 2)
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")

    def test_page_two_has_no_overlap_and_is_followed(self):
        list(self.spider.parse(self.response()))
        page_two = list(self.spider.parse(self.response(self.sample_page2, page=2)))
        item = page_two[0]
        self.assertEqual(item["item_id"], "5348097")
        self.assertEqual(item["url"], "https://www.petsmart.com/-80289.html")
        self.assertEqual(item["brand"], "Authority")
        self.assertEqual(item["page"], 2)
        self.assertEqual(item["position"], 1)

    def test_duplicates_across_pages_are_dropped(self):
        list(self.spider.parse(self.response()))
        page_two = list(self.spider.parse(self.response(self.sample_page2, page=2)))
        # Replaying page 1 with a fresh page number must not re-emit seen products.
        replay = [i for i in self.spider.parse(self.response(self.sample, page=3)) if isinstance(i, dict)]
        self.assertEqual(replay, [])
        self.assertEqual(page_two[0]["item_id"], "5348097")

    def test_max_pages_stops_pagination(self):
        single = PetsmartListingSpider(category="dog/food", max_pages=1)
        outputs = list(single.parse(self.response()))
        self.assertFalse([o for o in outputs if not isinstance(o, dict)])

    def test_price_falls_back_to_range_low_end(self):
        body = self.sample.replace('"current":77.99,"listRange"', '"current":null,"listRange"')
        item = list(self.spider.parse(self.response(body)))[0]
        self.assertEqual(item["price"], 20.68)

    def test_missing_and_malformed_hydration_fail_visibly(self):
        for body in ("<html></html>", '<script>window[Symbol.for("InstantSearchInitialResults")] = {bad};</script>'):
            with self.subTest(body=body), self.assertRaisesRegex(RuntimeError, "No Algolia InstantSearch"):
                list(self.spider.parse(self.response(body)))

    def test_non_200_and_challenge_pages_fail_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "HTTP 503"):
            list(self.spider.parse(self.response(page=1).replace(status=503, body=b"nope")))
        with self.assertRaisesRegex(RuntimeError, "anti-bot challenge"):
            list(self.spider.parse(self.response("<html>Access Denied</html>")))


if __name__ == "__main__":
    unittest.main()
