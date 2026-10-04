from pathlib import Path
import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.adorama_categories import ADORAMA_CATEGORIES, ADORAMA_CATEGORY_INVENTORY
from common.spiders.adorama_listing_spider import AdoramaListingSpider


def _hydration(page_props: dict) -> str:
    payload = {"props": {"pageProps": page_props}}
    return f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'


class AdoramaListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = AdoramaListingSpider(category="cameras", max_pages=2)
        self.page1 = Path("sample/adorama-listing-cameras-p1.html").read_text(encoding="utf-8")
        self.page2 = Path("sample/adorama-listing-cameras-p2.html").read_text(encoding="utf-8")

    def response(self, body=None, *, page=1):
        url = "https://www.adorama.com/l/Photography/Cameras" + ("?startAt=24" if page == 2 else "")
        request = Request(
            url,
            meta={
                "category": "cameras", "department": "Photography",
                "subcategory": "Cameras", "category_path": "/l/Photography/Cameras",
                "page": page, "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(url, request=request, body=body or self.page1, encoding="utf-8")

    @staticmethod
    def split(outputs):
        # Materialize once: `parse` returns a generator that a single pass exhausts.
        outputs = list(outputs)
        items = [o for o in outputs if isinstance(o, dict)]
        requests = [o for o in outputs if not isinstance(o, dict)]
        return items, requests

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(ADORAMA_CATEGORY_INVENTORY), 11)
        self.assertEqual(len(ADORAMA_CATEGORIES), 1079)
        self.assertEqual(len({entry["url"] for entry in ADORAMA_CATEGORIES}), 1079)
        self.assertEqual(len({entry["category"] for entry in ADORAMA_CATEGORIES}), 1079)
        self.assertEqual(self.spider.resolve_target_url(), "https://www.adorama.com/l/Photography/Cameras")
        # Depth-1 department landings have no product grid and must not be crawlable.
        self.assertNotIn("https://www.adorama.com/l/Photography", {e["url"] for e in ADORAMA_CATEGORIES})
        leaf = next(e for e in ADORAMA_CATEGORIES if e["category"] == "microphone-cases")
        self.assertEqual(leaf["url"], "https://www.adorama.com/l/Audio/Audio-Bags-and-Cases/Microphone-Cases")

    def test_hydration_yields_24_items_and_feed_contract(self):
        items, requests = self.split(self.spider.parse(self.response()))
        self.assertEqual(len(items), 24)
        self.assertEqual(len(requests), 1)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        first = items[0]
        self.assertEqual(first["item_id"], "KKRK0603A")
        self.assertEqual(
            first["title"],
            "Kodak Charmera Millenium Edition 1.6MP Keychain Digital Camera, w/32GB Card",
        )
        self.assertEqual(first["brand"], "Kodak")
        self.assertEqual(first["url"], "https://www.adorama.com/kodak-charmera-millenium-edition-keychain-camera-1-6-mp/p/kkrk0603a")
        self.assertEqual(first["image_url"], "https://www.adorama.com/images/product/KKRK0603A.JPG")
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["price"], 54.94)
        self.assertTrue(first["in_stock"])
        self.assertEqual(first["total_count"], 3077)
        self.assertEqual(first["items_per_page"], 24)
        self.assertEqual(first["page_type"], "listPage")
        self.assertEqual(first["source"], "adorama_next_data")
        self.assertEqual(first["category_id"], "239101")
        self.assertEqual(first["category_path"], "/l/Photography/Cameras")
        self.assertEqual(first["category_path_hierarchy"], "Photography/Cameras/Digital Point & Shoot Cameras")

    def test_next_page_url_and_max_pages(self):
        _, requests = self.split(self.spider.parse(self.response()))
        self.assertEqual(len(requests), 1)
        first = requests[0]
        self.assertEqual(first.url, "https://www.adorama.com/l/Photography/Cameras?startAt=24")
        self.assertEqual(first.meta["page"], 2)
        self.assertEqual(first.meta["proxy"], "http://proxy.invalid:8080")
        self.assertEqual(first.meta["category_path"], "/l/Photography/Cameras")

        items, requests = self.split(self.spider.parse(self.response(self.page2, page=2)))
        self.assertEqual(len(items), 24)
        self.assertEqual(items[0]["page"], 2)
        self.assertEqual(items[0]["position"], 1)
        # max_pages=2 is reached, so the page-2 `nextPageUrl` is not followed.
        self.assertEqual(requests, [])

    def test_pagination_does_not_duplicate_skus(self):
        page1_skus = [i["item_id"] for i in self.split(self.spider.parse(self.response()))[0]]
        page2_skus = [i["item_id"] for i in self.split(self.spider.parse(self.response(self.page2, page=2)))[0]]
        self.assertEqual(len(page1_skus), 24)
        self.assertEqual(len(page2_skus), 24)
        self.assertEqual(set(page1_skus) & set(page2_skus), set())

        # Replaying page 1 against an already-populated dedupe set yields nothing new.
        replayed, _ = self.split(self.spider.parse(self.response()))
        self.assertEqual(replayed, [])

    def test_max_pages_one_skips_follow(self):
        spider = AdoramaListingSpider(category="cameras", max_pages=1)
        items, requests = self.split(spider.parse(self.response()))
        self.assertEqual(len(items), 24)
        self.assertEqual(requests, [])

    def test_malformed_missing_and_empty_hydration_fail_visibly(self):
        cases = [
            ("<html></html>", "No valid Adorama"),
            ('<script id="__NEXT_DATA__">bad</script>', "No valid Adorama"),
            ('<script id="__NEXT_DATA__">[]</script>', "No valid Adorama"),
            ('<script id="__NEXT_DATA__">{}</script>', "no props.pageProps"),
            (_hydration({"pageInfo": {"pageType": "listPage"}}), "no list-valued products"),
            (_hydration({"pageInfo": {"pageType": "listPage"}, "products": []}), "zero products"),
            (_hydration({"pageInfo": {"pageType": "bcmsSitePage"}, "products": [{"sku": "X1"}]}), "CMS landing page"),
        ]
        for body, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(RuntimeError, message):
                list(self.spider.parse(self.response(body)))

    def test_non_200_fails_visibly(self):
        request = Request("https://www.adorama.com/l/Photography/Cameras", meta={"page": 1})
        blocked = TextResponse(
            "https://www.adorama.com/l/Photography/Cameras", request=request,
            body="<html>blocked</html>", status=403, encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
            list(self.spider.parse(blocked))

    def test_rating_and_savings_mapping(self):
        items = self.split(self.spider.parse(self.response()))[0]
        rated = [i for i in items if i["rating"] is not None]
        self.assertTrue(rated, "fixture should contain rated products")
        self.assertEqual(rated[0]["rating"], 5)
        self.assertEqual(rated[0]["reviews_count"], 5)

        saved = [i for i in items if i["savings_amount"] is not None]
        self.assertTrue(saved, "fixture should contain discounted products")
        self.assertGreater(saved[0]["list_price"], saved[0]["price"])
        self.assertEqual(saved[0]["savings_amount"], round(saved[0]["list_price"] - saved[0]["price"], 2))

        # `in_stock` reflects physical stock; pre-order SKUs stay purchasable but
        # are not in stock, so the two flags must be reported independently.
        self.assertEqual({i["stock"] for i in items}, {"In", "Out"})
        for item in items:
            self.assertEqual(item["in_stock"], item["stock"] == "In")
        preorder = [i for i in items if i["stock"] == "Out"]
        self.assertTrue(preorder)
        self.assertTrue(any(i["is_available_for_purchase"] for i in preorder))

    def test_url_or_category_arg_required(self):
        with self.assertRaisesRegex(ValueError, "Provide -a category"):
            AdoramaListingSpider()

    def test_leaves_raw_source_entry_untouched(self):
        item = list(self.spider.parse(self.response()))[0]
        self.assertEqual(item["raw"]["sku"], "KKRK0603A")
        self.assertEqual(item["source_url"], "https://www.adorama.com/l/Photography/Cameras")
