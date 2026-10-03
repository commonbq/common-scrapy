from pathlib import Path
import json
import unittest
from urllib.parse import parse_qs, urlparse

from scrapy.http import Request, TextResponse

from common.spiders.uniqlo_categories import (
    UNIQLO_CATEGORIES,
    UNIQLO_CATEGORY_INVENTORY,
    UNIQLO_CATEGORY_PATHS,
)
from common.spiders.uniqlo_listing_spider import PRODUCTS_API, UniqloListingSpider

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample"
WOMENS_TSHIRTS_URL = "https://www.uniqlo.com/us/en/women/tops/t-shirts"
WOMENS_TSHIRTS_PATH = "22210,23295,23335"


def load_sample(name: str) -> dict:
    return json.loads((SAMPLE_DIR / name).read_text(encoding="utf-8"))


class UniqloListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = UniqloListingSpider(category="t-shirts-and-tank-tops", max_pages=3)
        self.request = next(iter(self.spider.start_requests()))

    def response(self, payload=None, *, page=1, offset=0, status=200, url=None):
        url = url or f"{PRODUCTS_API}?path={WOMENS_TSHIRTS_PATH}&limit=36&offset={offset}"
        body = payload if isinstance(payload, str) else json.dumps(payload or {})
        request = Request(
            url,
            meta={
                **self.request.meta,
                "page": page,
                "offset": offset,
                "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(
            url,
            status=status,
            request=request,
            body=body,
            encoding="utf-8",
        )

    # -- taxonomy -------------------------------------------------------------

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(UNIQLO_CATEGORY_INVENTORY), 4)
        self.assertEqual(len(UNIQLO_CATEGORIES), 2741)
        self.assertEqual(len(UNIQLO_CATEGORY_PATHS), 2741)
        self.assertEqual(len({entry["url"] for entry in UNIQLO_CATEGORIES}), 2741)
        self.assertEqual(
            self.spider.resolve_target_url(),
            "https://www.uniqlo.com/us/en/women/tops/t-shirts",
        )

    def test_every_category_carries_a_unique_slug_and_taxonomy_path(self):
        slugs = [entry["category"] for entry in UNIQLO_CATEGORIES]
        self.assertEqual(len(slugs), len(set(slugs)))
        for entry in UNIQLO_CATEGORIES:
            self.assertTrue(entry["path"], entry["url"])
            self.assertTrue(entry["url"].startswith("https://www.uniqlo.com/us/en/"))
            parts = entry["path"].split(",")
            self.assertTrue(all(part.isdigit() for part in parts), entry["url"])

    def test_parents_are_preserved_for_deep_leaves(self):
        url = "https://www.uniqlo.com/us/en/men/accessories-and-shoes/bags/backpacks"
        entry = next(e for e in UNIQLO_CATEGORIES if e["url"] == url)
        self.assertEqual(entry["path"], "22211,23309,31985,68744")
        self.assertEqual(entry["department"], "Men")
        self.assertEqual(entry["subcategory"], "Accessories")
        self.assertEqual(entry["category_name"], "Backpacks")

    def test_colliding_leaf_slugs_are_disambiguated(self):
        vests = [e for e in UNIQLO_CATEGORIES if e["category_name"] == "Vest"]
        self.assertGreater(len(vests), 1)
        self.assertEqual(len({e["category"] for e in vests}), len(vests))
        self.assertEqual(len({e["url"] for e in vests}), len(vests))

    # -- request construction -------------------------------------------------

    def test_category_resolves_to_the_bff_products_request(self):
        query = parse_qs(urlparse(self.request.url).query)
        self.assertEqual(self.request.url.split("?")[0], PRODUCTS_API)
        self.assertEqual(query["path"], [WOMENS_TSHIRTS_PATH])
        self.assertEqual(query["limit"], ["36"])
        self.assertEqual(query["offset"], ["0"])
        self.assertEqual(self.request.meta["category"], "t-shirts-and-tank-tops")
        self.assertEqual(self.request.meta["category_name"], "T-Shirts and Tank Tops")
        self.assertEqual(self.request.meta["department"], "Women")
        self.assertEqual(self.request.meta["subcategory"], "T-Shirts, Sweats & Fleece")
        self.assertEqual(self.request.meta["taxonomy_path"], WOMENS_TSHIRTS_PATH)
        self.assertEqual(self.request.meta["page"], 1)
        self.assertIn(b"user-agent", self.request.headers)

    def test_category_url_resolves_through_the_inventory(self):
        spider = UniqloListingSpider(category_url=WOMENS_TSHIRTS_URL)
        request = next(iter(spider.start_requests()))
        self.assertEqual(parse_qs(urlparse(request.url).query)["path"], [WOMENS_TSHIRTS_PATH])
        self.assertEqual(request.meta["department"], "Women")

    def test_no_target_raises(self):
        with self.assertRaises(ValueError):
            UniqloListingSpider()

    def test_unknown_category_url_is_rejected(self):
        spider = UniqloListingSpider(category_url="https://www.uniqlo.com/us/en/not-a-real-shelf")
        with self.assertRaises(ValueError) as ctx:
            next(iter(spider.start_requests()))
        self.assertLess(len(str(ctx.exception)), 600)

    # -- item extraction ------------------------------------------------------

    def test_first_page_yields_36_items_and_the_feed_contract(self):
        outputs = list(self.spider.parse(self.response(load_sample("uniqlo-products-womens-tshirts.json"))))
        items = [o for o in outputs if hasattr(o, "get")]
        self.assertEqual(len(items), 36)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

        first = items[0]
        self.assertEqual(first["category"], "t-shirts-and-tank-tops")
        self.assertEqual(first["category_name"], "T-Shirts and Tank Tops")
        self.assertEqual(first["department"], "Women")
        self.assertEqual(first["subcategory"], "T-Shirts, Sweats & Fleece")
        self.assertEqual(first["item_id"], "E424873-000-00")
        self.assertEqual(first["style_id"], "424873")
        self.assertEqual(first["title"], "Crew Neck T-Shirt")
        self.assertEqual(first["brand"], "UNIQLO")
        self.assertEqual(first["gender"], "WOMEN")
        self.assertEqual(first["color"], "White")
        self.assertEqual(first["color_code"], "00")
        self.assertEqual(first["url"], "https://www.uniqlo.com/us/en/products/E424873-000")
        self.assertTrue(first["image_url"].startswith("https://image.uniqlo.com/"))
        self.assertIn("usgoods_00_424873_3x4.jpg", first["image_url"])
        self.assertEqual(first["price"], 19.9)
        self.assertIsNone(first["original_price"])
        self.assertEqual(first["currency"], "USD")
        self.assertFalse(first["on_sale"])
        self.assertEqual(first["rating"], 4.7)
        self.assertEqual(first["reviews_count"], 2858)
        self.assertIn("XXS", first["available_sizes"])
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["total_count"], 69)
        self.assertEqual(first["items_per_page"], 36)
        self.assertEqual(first["taxonomy_path"], WOMENS_TSHIRTS_PATH)
        self.assertEqual(first["source"], "uniqlo_commerce_bff_products")
        self.assertIn("productId", first["raw"])

    def test_every_item_exposes_raw(self):
        outputs = list(self.spider.parse(self.response(load_sample("uniqlo-products-womens-tshirts.json"))))
        items = [o for o in outputs if hasattr(o, "get")]
        self.assertTrue(items)
        for item in items:
            self.assertIsInstance(item["raw"], dict)
            self.assertTrue(item["raw"])
            self.assertTrue(item["item_id"])
            self.assertTrue(item["title"])
            self.assertTrue(item["url"])
            self.assertTrue(item["image_url"])
            self.assertEqual(item["currency"], "USD")

    def test_second_page_positions_continue(self):
        outputs = list(
            self.spider.parse(
                self.response(load_sample("uniqlo-products-womens-tshirts-page2.json"), page=2, offset=36)
            )
        )
        items = [o for o in outputs if hasattr(o, "get")]
        self.assertEqual(len(items), 33)
        self.assertEqual(items[0]["page"], 2)
        self.assertEqual(items[0]["position"], 1)
        self.assertEqual(items[0]["total_count"], 69)

    def test_promotional_item_maps_prices(self):
        """A genuinely discounted row: ``promo`` is the price paid, ``base`` the original."""
        item = self.spider._item(
            {
                "productId": "E999999-000",
                "name": "Sale Jacket",
                "prices": {
                    "base": {"value": 79.9, "currency": {"code": "USD"}},
                    "promo": {"value": 39.95, "currency": {"code": "USD"}},
                    "isDualPrice": True,
                },
                "promotionText": "Limited time offer",
            },
            self.response({}), 1, 1, 10, 10,
        )
        self.assertEqual(item["price"], 39.95)
        self.assertEqual(item["original_price"], 79.9)
        self.assertTrue(item["on_sale"])
        self.assertEqual(item["promotion_text"], "Limited time offer")
        self.assertEqual(item["currency"], "USD")

    def test_non_discounted_item_has_no_original_price(self):
        """``promo`` present but equal to ``base`` (or absent) is not a sale."""
        for prices in (
            {"base": {"value": 9.9}, "promo": {"value": 9.9}, "isDualPrice": False},
            {"base": {"value": 19.9}, "promo": None, "isDualPrice": False},
        ):
            item = self.spider._item(
                {"productId": "E999999-000", "prices": prices},
                self.response({}), 1, 1, 10, 10,
            )
            self.assertEqual(item["price"], 9.9 if prices["base"]["value"] == 9.9 else 19.9)
            self.assertIsNone(item["original_price"])
            self.assertFalse(item["on_sale"])

    def test_committed_fixture_rows_are_all_regular_priced(self):
        """Regression guard: no committed fixture row is actually on sale."""
        for name in ("uniqlo-products-womens-tshirts.json", "uniqlo-products-womens-tshirts-page2.json"):
            payload = load_sample(name)
            for product in payload["result"]["items"]:
                item = self.spider._item(product, self.response(payload), 1, 1, 69, 36)
                self.assertFalse(item["on_sale"], product["productId"])
                self.assertIsNone(item["original_price"], product["productId"])
                self.assertEqual(item["price"], (product["prices"]["base"] or {}).get("value"))

    def test_item_id_appends_the_representative_colour_code(self):
        self.assertEqual(UniqloListingSpider._item_id({"productId": "E424873-000", "representativeColorDisplayCode": "32"}), "E424873-000-32")
        self.assertEqual(UniqloListingSpider._item_id({"productId": "E424873-000"}), "E424873-000")
        self.assertEqual(UniqloListingSpider._item_id({}), "")

    def test_style_id_falls_back_to_none_for_unexpected_ids(self):
        self.assertIsNone(UniqloListingSpider._style_id("not-a-product"))
        self.assertIsNone(UniqloListingSpider._style_id(""))
        self.assertEqual(UniqloListingSpider._style_id("E424873-000"), "424873")

    # -- pagination -----------------------------------------------------------

    def test_pagination_enqueues_the_next_offset(self):
        outputs = list(self.spider.parse(self.response(load_sample("uniqlo-products-womens-tshirts.json"))))
        follow_up = outputs[-1]
        self.assertFalse(hasattr(follow_up, "get"))
        self.assertEqual(parse_qs(urlparse(follow_up.url).query)["offset"], ["36"])
        self.assertEqual(parse_qs(urlparse(follow_up.url).query)["path"], [WOMENS_TSHIRTS_PATH])
        self.assertEqual(follow_up.meta["page"], 2)
        self.assertEqual(follow_up.meta["offset"], 36)

    def test_last_page_does_not_enqueue_another_request(self):
        outputs = list(
            self.spider.parse(
                self.response(load_sample("uniqlo-products-womens-tshirts-page2.json"), page=2, offset=36)
            )
        )
        self.assertTrue(all(hasattr(o, "get") for o in outputs))

    def test_max_pages_caps_pagination(self):
        spider = UniqloListingSpider(category="t-shirts-and-tank-tops", max_pages=1)
        request = next(iter(spider.start_requests()))
        outputs = list(spider.parse(self.response(load_sample("uniqlo-products-womens-tshirts.json"))))
        self.assertTrue(all(hasattr(o, "get") for o in outputs))
        self.assertEqual(len([o for o in outputs if hasattr(o, "get")]), 36)

    def test_duplicate_product_ids_across_colourways_are_kept(self):
        # The BFF returns E424873-000 twice with different colour codes (00 and 32);
        # collapsing on productId alone would silently drop a real colourway.
        items = load_sample("uniqlo-products-womens-tshirts.json")["result"]["items"]
        self.assertEqual(len(items), 36)
        self.assertEqual(len({i["productId"] for i in items}), 34)
        outputs = list(self.spider.parse(self.response(load_sample("uniqlo-products-womens-tshirts.json"))))
        yielded = [o for o in outputs if hasattr(o, "get")]
        self.assertEqual(len(yielded), 36)
        self.assertEqual(len({o["item_id"] for o in yielded}), 36)
        by_id = {o["item_id"]: o for o in yielded}
        self.assertIn("E424873-000-00", by_id)
        self.assertIn("E424873-000-32", by_id)
        self.assertEqual(by_id["E424873-000-00"]["color_code"], "00")
        self.assertEqual(by_id["E424873-000-32"]["color_code"], "32")

    def test_duplicate_product_ids_are_deduplicated(self):
        payload = load_sample("uniqlo-products-womens-tshirts.json")
        items = payload["result"]["items"]
        payload["result"]["items"] = [items[0], items[0], *items[1:5]]
        outputs = list(self.spider.parse(self.response(payload)))
        ids = [o["item_id"] for o in outputs if hasattr(o, "get")]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids[0], "E424873-000-00")

    def test_gender_level_category_pages(self):
        spider = UniqloListingSpider(category_url="https://www.uniqlo.com/us/en/women")
        request = next(iter(spider.start_requests()))
        self.assertEqual(parse_qs(urlparse(request.url).query)["path"], ["22210"])
        self.assertEqual(request.meta["taxonomy_path"], "22210")

    # -- error handling -------------------------------------------------------

    def test_http_error_raises(self):
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(self.response({"status": "ok"}, status=503)))

    def test_non_json_body_raises(self):
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(self.response("<html>blocked</html>")))

    def test_missing_result_raises(self):
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(self.response({"status": "ok"})))

    def test_missing_items_raises(self):
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(self.response({"status": "ok", "result": {}})))


if __name__ == "__main__":
    unittest.main()
