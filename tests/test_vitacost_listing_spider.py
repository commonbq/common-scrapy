import json
import unittest
from pathlib import Path

from scrapy.http import Request, Response, TextResponse

from common.spiders.vitacost_categories import VITACOST_CATEGORIES
from common.spiders.vitacost_listing_spider import VitacostListingSpider

COLLECTION_URL = "https://www.vitacost.com/collections/supplements"
COLLECTION_ID = "457575104827"
API_PREFIX = "https://services.mybcapps.com/bc-sf-filter/filter"


def fixture(name: str) -> str:
    return Path("sample") / name


def load_api(name: str) -> dict:
    return json.loads(Path(fixture(name)).read_text(encoding="utf-8"))


class VitacostListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = VitacostListingSpider(category="Supplements", max_pages=2)
        self.page1 = load_api("vitacost-boost-filter-supplements-page1.json")
        self.page2 = load_api("vitacost-boost-filter-supplements-page2.json")

    def collection_response(self, body: str | None = None):
        meta = {
            "category": "Supplements",
            "department": "Supplements",
            "subcategory": None,
            "handle": "supplements",
            "collection_url": COLLECTION_URL,
            "page": 0,
        }
        url = COLLECTION_URL
        if body is None:
            body = Path(fixture("vitacost-collection-page.html")).read_text(encoding="utf-8")
        return TextResponse(url, request=Request(url, meta=meta), body=body, encoding="utf-8")

    def api_response(self, payload, page=1, status=200, url=None, meta=None):
        url = url or f"{API_PREFIX}?collection_scope={COLLECTION_ID}&page={page}"
        request_meta = {
            "category": "Supplements",
            "department": "Supplements",
            "subcategory": None,
            "handle": "supplements",
            "collection_url": COLLECTION_URL,
            "collection_id": COLLECTION_ID,
            "page": page,
        }
        request_meta.update(meta or {})
        body = payload if isinstance(payload, (str, bytes)) else json.dumps(payload)
        if status == 200:
            return TextResponse(url, request=Request(url, meta=request_meta), body=body, encoding="utf-8")
        return Response(url, request=Request(url, meta=request_meta), status=status)

    def items(self, payload, page=1, **kwargs):
        response = self.api_response(payload, page=page, **kwargs)
        return [out for out in self.spider.parse_filter_api(response) if isinstance(out, dict)]

    def requests(self, payload, page=1):
        response = self.api_response(payload, page=page)
        return [out for out in self.spider.parse_filter_api(response) if hasattr(out, "url")]

    # ------------------------------------------------------------------ taxonomy

    def test_inventory_is_unique_and_crawlable(self):
        self.assertEqual(len(VITACOST_CATEGORIES), 92)
        self.assertEqual(len({e["category"] for e in VITACOST_CATEGORIES}), 92)
        self.assertEqual(len({e["department"] for e in VITACOST_CATEGORIES}), 8)
        self.assertTrue(all(e["url"].startswith("https://www.vitacost.com/collections/") for e in VITACOST_CATEGORIES))
        self.assertTrue(all(e["handle"] == e["url"].rsplit("/", 1)[-1] for e in VITACOST_CATEGORIES))
        # `Sunscreen` and `Essential Oils & Aromatherapy` each exist twice, so 92 labels -> 90 URLs.
        self.assertEqual(len({e["url"] for e in VITACOST_CATEGORIES}), 90)

    def test_category_lookup_returns_the_collection_url(self):
        self.assertEqual(
            VitacostListingSpider(category="Supplements > Vitamins").resolve_target_url(),
            "https://www.vitacost.com/collections/vitamins",
        )
        self.assertEqual(VitacostListingSpider(category="Supplements").resolve_target_url(), COLLECTION_URL)

    def test_missing_category_arg_raises_with_available_names(self):
        with self.assertRaisesRegex(ValueError, "Available categories"):
            VitacostListingSpider()

    def test_unknown_category_lists_the_inventory(self):
        with self.assertRaisesRegex(ValueError, "Unknown category 'Nope'"):
            next(iter(VitacostListingSpider(category="Nope").start_requests()))

    def test_start_request_carries_the_resolved_taxonomy(self):
        request = next(iter(self.spider.start_requests()))
        self.assertEqual(request.url, COLLECTION_URL)
        self.assertEqual(request.meta["handle"], "supplements")
        self.assertEqual(request.meta["department"], "Supplements")
        self.assertEqual(request.callback, self.spider.parse_collection_page)

    def test_url_arg_derives_the_handle(self):
        request = next(iter(VitacostListingSpider(url="https://www.vitacost.com/collections/greens-superfoods/").start_requests()))
        self.assertEqual(request.meta["handle"], "greens-superfoods")
        self.assertEqual(request.meta["department"], None)

    def test_non_collection_url_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Cannot derive a Shopify collection handle"):
            next(iter(VitacostListingSpider(url="https://www.vitacost.com/").start_requests()))

    # ------------------------------------------------------------------ collection id

    def test_collection_id_is_read_from_the_storefront_page(self):
        requests = list(self.spider.parse_collection_page(self.collection_response()))
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].meta["collection_id"], "458194583867")
        self.assertEqual(requests[0].meta["page"], 1)
        self.assertTrue(requests[0].url.startswith(API_PREFIX))
        self.assertIn("collection_scope=458194583867", requests[0].url)
        self.assertIn("page=1", requests[0].url)
        self.assertIn("shop=icost.myshopify.com", requests[0].url)
        self.assertIn("pg=collection_page", requests[0].url)
        # The Boost request must not inherit the storefront proxy.
        self.assertNotIn("proxy", requests[0].meta)
        self.assertEqual(requests[0].headers["Referer"], COLLECTION_URL.encode())

    def test_page_without_a_collection_id_stops_with_an_error_log(self):
        with self.assertLogs("vitacost_listing", level="ERROR") as logs:
            self.assertEqual(list(self.spider.parse_collection_page(self.collection_response("<html></html>"))), [])
        self.assertIn("No numeric collection id", logs.output[0])

    # ------------------------------------------------------------------ item mapping

    def test_feed_contract_and_item_mapping(self):
        items = self.items(self.page1)
        self.assertEqual(len(items), 5)
        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], str(self.page1["products"][0]["id"]))
        self.assertEqual(item["title"], self.page1["products"][0]["title"])
        self.assertEqual(item["brand"], self.page1["products"][0]["vendor"])
        self.assertTrue(item["url"].startswith("https://www.vitacost.com/products/"))
        self.assertTrue(item["url"].endswith("/"))
        self.assertTrue(item["image_url"].startswith("https://cdn.shopify.com/"))
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["price"], self.page1["products"][0]["price_min"])
        self.assertEqual(item["original_price"], self.page1["products"][0]["compare_at_price_min"])
        self.assertEqual(item["discount_percentage"], self.page1["products"][0]["percent_sale_min"])
        self.assertTrue(item["on_sale"])
        self.assertFalse(item["out_of_stock"])
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], self.page1["total_product"])
        self.assertEqual(item["source"], "vitacost_boost_filter_api")
        self.assertIsInstance(item["raw"], dict)
        self.assertNotIn("body_html", item["raw"])

    def test_item_matches_the_feed_export_fields_exactly(self):
        item = self.items(self.page1)[0]
        self.assertEqual(list(item.keys()), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_ratings_come_from_the_judgemetafields(self):
        item = self.items(self.page1)[0]
        self.assertEqual(item["rating"], 4.72)
        self.assertEqual(item["reviews_count"], 484)
        self.assertEqual(item["package_quantity"], "120 - 179 count")
        self.assertEqual(item["form"], "Capsule")
        self.assertEqual(item["strength"], "1000 - 4999 mg")
        self.assertEqual(item["badges"], "Clearance, On Sale")
        self.assertTrue(item["description"].startswith("Description"))
        self.assertLessEqual(len(item["description"]), 400)

    def test_full_price_items_have_no_original_price_or_discount(self):
        product = dict(self.page1["products"][0])
        product["compare_at_price_min"] = product["price_min"]
        product["percent_sale_min"] = 0
        item = self.items({"total_product": 1, "products": [product]})[0]
        self.assertIsNone(item["original_price"])
        self.assertIsNone(item["discount_percentage"])
        self.assertFalse(item["on_sale"])

    def test_discount_is_derived_when_the_api_omits_the_percentage(self):
        product = dict(self.page1["products"][0])
        product["percent_sale_min"] = 0
        item = self.items({"total_product": 1, "products": [product]})[0]
        self.assertAlmostEqual(item["discount_percentage"], 25.0, places=1)

    def test_sold_out_product_flags_stock(self):
        product = dict(self.page1["products"][0])
        product["available"] = False
        product["variants"] = [dict(product["variants"][0], inventory_quantity=0)]
        item = self.items({"total_product": 1, "products": [product]})[0]
        self.assertTrue(item["out_of_stock"])
        self.assertIsNone(item["in_stock_quantity"])

    def test_non_default_options_are_flattened(self):
        product = dict(self.page1["products"][0])
        product["options_with_values"] = [
            {"name": "size", "label": "Size", "values": [{"title": "60 count"}, {"title": "120 count"}]},
            {"name": "title", "label": "Title", "values": [{"title": "Default Title"}]},
        ]
        item = self.items({"total_product": 1, "products": [product]})[0]
        self.assertEqual(item["option_count"], 1)
        self.assertEqual(item["options"], "Size: 60 count, 120 count")

    def test_products_without_an_id_are_skipped(self):
        product = dict(self.page1["products"][0])
        product["id"] = None
        self.assertEqual(self.items({"total_product": 1, "products": [product]}), [])

    # ------------------------------------------------------------------ pagination

    def test_page_two_is_requested_once_and_products_are_deduplicated(self):
        self.spider._seen_products.update(
            str(p["id"]) for p in self.page1["products"][:2]
        )
        items = self.items(self.page2, page=2)
        self.assertTrue(items)
        self.assertEqual({item["page"] for item in items}, {2})
        page1_ids = {str(p["id"]) for p in self.page1["products"][:2]}
        self.assertFalse({item["item_id"] for item in items} & page1_ids)
        self.assertEqual([item["position"] for item in items], list(range(1, len(items) + 1)))

    def test_max_pages_stops_before_the_next_request(self):
        spider = VitacostListingSpider(category="Supplements", max_pages=1)
        response = self.api_response(self.page1, page=1)
        self.assertEqual([out for out in spider.parse_filter_api(response) if hasattr(out, "url")], [])

    def test_pagination_stops_at_total_num_products(self):
        payload = {"total_product": 5, "products": self.page1["products"][:2]}
        self.assertEqual(self.requests(payload), [])

    def test_next_page_request_carries_the_same_scope_and_page(self):
        requests = self.requests(self.page1)
        self.assertEqual(len(requests), 1)
        self.assertIn("page=2", requests[0].url)
        self.assertIn("collection_scope=457575104827", requests[0].url)
        self.assertEqual(requests[0].meta["page"], 2)
        self.assertEqual(requests[0].meta["collection_id"], COLLECTION_ID)

    def test_empty_page_stops_with_an_info_log(self):
        empty = load_api("vitacost-boost-filter-empty.json")
        with self.assertLogs("vitacost_listing", level="INFO") as logs:
            self.assertEqual(self.items(empty), [])
        self.assertIn("No products on page 1", logs.output[0])

    def test_repeated_only_page_stops_pagination(self):
        # Same products on page 2 -> nothing new, so the crawl must stop.
        response = self.api_response(self.page2, page=2)
        list(self.spider.parse_filter_api(response))
        with self.assertLogs("vitacost_listing", level="INFO") as logs:
            requests = [
                out for out in self.spider.parse_filter_api(self.api_response(self.page2, page=2))
                if hasattr(out, "url")
            ]
        self.assertEqual(requests, [])
        self.assertIn("repeated only known products", logs.output[0])

    # ------------------------------------------------------------------ error paths

    def test_non_200_api_response_is_logged_and_skipped(self):
        with self.assertLogs("vitacost_listing", level="ERROR") as logs:
            self.assertEqual(self.items(self.page1, status=403), [])
        self.assertIn("HTTP 403", logs.output[0])

    def test_non_json_api_response_is_logged_and_skipped(self):
        with self.assertLogs("vitacost_listing", level="ERROR") as logs:
            self.assertEqual(self.items("<html>nope</html>"), [])
        self.assertIn("non-JSON", logs.output[0])

    def test_api_error_message_is_logged(self):
        with self.assertLogs("vitacost_listing", level="ERROR") as logs:
            self.assertEqual(self.items({"message": "403 Forbidden: "}), [])
        self.assertIn("403 Forbidden", logs.output[0])

    def test_envelope_without_products_key_is_tolerated(self):
        with self.assertLogs("vitacost_listing", level="INFO"):
            self.assertEqual(self.items({"total_product": 0}), [])

    # ------------------------------------------------------------------ helpers

    def test_page_size_is_clamped_to_the_api_cap(self):
        self.assertEqual(VitacostListingSpider(category="Supplements").page_size, 48)
        self.assertEqual(VitacostListingSpider(category="Supplements", limit=100).page_size, 50)
        self.assertEqual(VitacostListingSpider(category="Supplements", limit=0).page_size, 1)
        self.assertEqual(VitacostListingSpider(category="Supplements", limit="bogus").page_size, 48)

    def test_handle_parsing(self):
        parse = VitacostListingSpider._handle
        self.assertEqual(parse("https://www.vitacost.com/collections/supplements"), "supplements")
        self.assertEqual(parse("https://www.vitacost.com/collections/vitamins/?page=2"), "vitamins")
        self.assertIsNone(parse("https://www.vitacost.com/"))
        self.assertIsNone(parse(None))


if __name__ == "__main__":
    unittest.main()