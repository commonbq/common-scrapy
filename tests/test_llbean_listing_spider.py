from pathlib import Path
import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.llbean_categories import LLBEAN_CATEGORIES
from common.spiders.llbean_listing_spider import LlbeanListingSpider, category_id_from_url

SAMPLE_DIR = Path("sample")


class LlbeanListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = LlbeanListingSpider(category="Gift Shop", max_pages=2)
        self.page1 = json.loads(
            (SAMPLE_DIR / "llbean-listing-products-page1.json").read_text(encoding="utf-8")
        )
        self.page2 = json.loads(
            (SAMPLE_DIR / "llbean-listing-products-page2.json").read_text(encoding="utf-8")
        )

    def response(self, body, start=0, page=1, status=200):
        url = (
            "https://www.llbean.com/api/udal/product-discovery/search"
            f"?categoryId=509870&pageSize=48&start={start}"
        )
        request = Request(
            url,
            meta={
                "category_id": "509870",
                "category": "Gift Shop",
                "department": "Gift Shop",
                "page": page,
            },
        )
        raw = body if isinstance(body, str) else json.dumps(body)
        return TextResponse(url, request=request, body=raw, encoding="utf-8", status=status)

    @staticmethod
    def split(outputs):
        """`parse()` yields items and follow-up requests; split them apart."""
        items = [o for o in outputs if isinstance(o, dict)]
        return items, [o for o in outputs if isinstance(o, Request)]

    def test_category_inventory_is_unique_and_addressable(self):
        self.assertEqual(len(_FLAT(LLBEAN_CATEGORIES)), 500)
        self.assertEqual(len({c["category"] for c in _FLAT(LLBEAN_CATEGORIES)}), 500)
        self.assertEqual(len({c["url"] for c in _FLAT(LLBEAN_CATEGORIES)}), 500)
        # Ambiguous leaf names are qualified so `-a category=` stays unambiguous.
        self.assertIn("Gift Shop", self.spider.available_categories())
        self.assertIn("Clothing / Sweaters [611]", self.spider.available_categories())
        self.assertEqual(
            category_id_from_url(self.spider.resolve_target_url()), "509870"
        )

    def test_category_id_is_read_from_the_url(self):
        self.assertEqual(
            category_id_from_url("https://www.llbean.com/llb/shop/12"), "12"
        )
        self.assertIsNone(category_id_from_url("https://www.llbean.com/llb/shop/"))

    def test_start_request_targets_the_udal_api(self):
        request = next(iter(self.spider.start_requests()))
        self.assertEqual(
            request.url,
            "https://www.llbean.com/api/udal/product-discovery/search"
            "?categoryId=509870&pageSize=48&start=0",
        )
        self.assertIn(b"application/json", request.headers["Accept"])

    def test_field_mapping_feed_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.response(self.page1)))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["category"], "Gift Shop")
        self.assertEqual(item["department"], "Gift Shop")
        self.assertEqual(item["brand"], "L.L.Bean")
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["source"], "llbean_udal_product_discovery")
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], 626)
        # docs are one row per SKU; the SKU is the item identity
        self.assertEqual(item["sku_id"], self.page1["response"]["docs"][0]["skuID_s"])
        self.assertEqual(item["item_id"], item["sku_id"])
        # sale price wins, and the full price is only carried when it differs
        self.assertEqual(item["price"], 49.99)
        self.assertEqual(item["original_price"], 69.95)
        self.assertTrue(item["on_sale"])
        self.assertEqual(
            item["url"],
            "https://www.llbean.com/llb/shop/20010334"
            "?page=The-Original-Double-L-Crewneck-Novely-Sweater-Womens-Petite",
        )
        self.assertEqual(
            item["image_url"],
            "https://cdni.llbean.net/is/image/wim/527356_49104_44?wid=302&hei=352",
        )
        self.assertEqual(item["color"], "Classic Navy")
        self.assertEqual(item["size"], "X-Small")
        self.assertEqual(item["availability"], "IN")
        self.assertEqual(item["rating"], 4.4)
        self.assertEqual(item["reviews_count"], 359)
        # raw is mandatory on every exported item
        self.assertEqual(item["raw"], self.page1["response"]["docs"][0])

        follow = outputs[-1]
        self.assertTrue(
            follow.url.endswith("categoryId=509870&pageSize=48&start=48"), follow.url
        )
        self.assertEqual(follow.meta["page"], 2)

    def test_every_item_carries_raw_and_maps_all_fields(self):
        items, _ = self.split(self.spider.parse(self.response(self.page1)))
        self.assertEqual(len(items), 48)
        for item in items:
            self.assertTrue(item["raw"])
            self.assertTrue(item["url"].startswith("https://www.llbean.com/llb/shop/"))
            self.assertEqual(item["currency"], "USD")
            if item["on_sale"]:
                self.assertLess(item["price"], item["original_price"])
            else:
                self.assertIsNone(item["original_price"])

    def test_page_two_is_disjoint_and_deduplicated(self):
        first, _ = self.split(self.spider.parse(self.response(self.page1)))
        second, _ = self.split(self.spider.parse(self.response(self.page2, start=48, page=2)))
        self.assertEqual(len(first), 48)
        self.assertEqual(len(second), 48)
        first_skus = {item["sku_id"] for item in first}
        self.assertEqual(len(first_skus & {item["sku_id"] for item in second}), 0)
        self.assertEqual({item["page"] for item in second}, {2})

    def test_repeated_skus_are_dropped(self):
        doc = self.page1["response"]["docs"][0]
        body = {"response": {"docs": [doc, dict(doc)], "numFound": 1, "start": 0}}
        items, _ = self.split(self.spider.parse(self.response(body)))
        self.assertEqual(len(items), 1)

    def test_pagination_stops_at_max_pages(self):
        spider = LlbeanListingSpider(category="Gift Shop", max_pages=1)
        _, requests = self.split(spider.parse(self.response(self.page1)))
        self.assertEqual(requests, [])

    def test_pagination_stops_at_num_found(self):
        docs = self.page1["response"]["docs"][:5]
        body = {"response": {"docs": docs, "numFound": 5, "start": 0}}
        items, requests = self.split(self.spider.parse(self.response(body)))
        self.assertEqual(len(items), 5)
        self.assertEqual(requests, [])

    def test_http_error_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "HTTP 503"):
            list(self.spider.parse(self.response(self.page1, status=503)))

    def test_malformed_payload_fails_visibly(self):
        for body in ({"response": {}}, {"response": {"docs": {}}}, {"nope": True}):
            with self.subTest(body=body), self.assertRaisesRegex(
                RuntimeError, "no response.docs list"
            ):
                list(self.spider.parse(self.response(body)))

    def test_non_category_url_fails_visibly(self):
        # `url` wins over `category` in resolve_target_url(), so pass both.
        spider = LlbeanListingSpider(
            category="Gift Shop", url="https://www.llbean.com/help"
        )
        with self.assertRaisesRegex(ValueError, "Cannot read a category id"):
            list(spider.start_requests())


if __name__ == "__main__":
    unittest.main()


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]
