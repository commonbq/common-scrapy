import json
import unittest
from pathlib import Path

from scrapy.http import TextResponse

from common.spiders.zara_categories import (
    category_key,
    is_product_category,
    listing_url,
    load_categories,
    parse_taxonomy,
    seo_category_id_from_url,
)
from common.spiders.zara_listing_spider import ZaraListingSpider


class ZaraTaxonomyTest(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(
            Path("sample/zara-categories.json").read_text()
        )
        self.entries = parse_taxonomy(self.payload)

    def test_only_eligible_nodes_become_categories(self):
        # The fixture nests one eligible node plus decoys: a
        # marketing-content-view node, an irrelevant products-category-view, a
        # srpls-products-category-view, a giftcard-balance-view and a
        # divider-category-view with no seo at all.
        self.assertEqual(len(self.entries), 3)
        for entry in self.entries:
            self.assertEqual(entry["url"], listing_url(entry["keyword"], entry["seo_category_id"]))

    def test_menu_id_is_preserved_for_the_products_endpoint(self):
        entry = next(e for e in self.entries if e["category"] == "WOMAN > NEW ARRIVALS > THE NEW")
        self.assertEqual(entry["category_id"], 2546081)
        self.assertEqual(entry["seo_category_id"], 1180)
        self.assertEqual(entry["keyword"], "woman-new-in")
        self.assertEqual(
            entry["url"], "https://www.zara.com/us/en/woman-new-in-l1180.html"
        )

    def test_repeated_menu_labels_stay_distinguishable_by_path(self):
        # THE NEW is cross-listed under itself in the fixture; the URL dedupe
        # must collapse it while every surviving key keeps its full breadcrumb.
        keys = [entry["category"] for entry in self.entries]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertIn("WOMAN > NEW ARRIVALS > THE NEW > DRESSES", keys)

    def test_section_is_the_top_level_menu_node(self):
        sections = {entry["category"]: entry["section"] for entry in self.entries}
        self.assertEqual(sections["WOMAN > NEW ARRIVALS > THE NEW"], "WOMAN")
        self.assertEqual(sections["PRE-OWNED > SERVICES"], "PRE-OWNED")

    def test_is_product_category_rejects_each_decoy(self):
        node = self.payload["categories"][0]["subcategories"][0]["subcategories"][0]
        by_name = {n["name"]: n for n in node["subcategories"]}
        self.assertTrue(is_product_category(node))
        self.assertFalse(is_product_category(by_name["WOMAN"]))          # marketing layout
        self.assertFalse(is_product_category(by_name["NEW ARRIVALS"]))   # irrelevant=True
        self.assertFalse(is_product_category(by_name["SRPLS FLWRS"]))    # other *-category-view
        self.assertFalse(is_product_category(by_name["View balance"]))   # gift-card layout
        self.assertFalse(is_product_category(by_name["DIVIDER-REFORM-10"]))
        self.assertFalse(is_product_category("not a dict"))

    def test_is_product_category_requires_both_seo_fields(self):
        base = {
            "layout": "products-category-view",
            "irrelevant": False,
            "seo": {"keyword": "k", "seoCategoryId": 1},
        }
        self.assertTrue(is_product_category(dict(base)))
        for missing in ("keyword", "seoCategoryId"):
            seo = {k: v for k, v in base["seo"].items() if k != missing}
            self.assertFalse(is_product_category({**base, "seo": seo}))
        # `irrelevant` must be explicitly False, not merely absent.
        self.assertFalse(is_product_category({**base, "irrelevant": None}))
        self.assertFalse(is_product_category({**base, "layout": "divider-category-view"}))

    def test_category_key_drops_empty_path_segments(self):
        self.assertEqual(category_key(("WOMAN", "", "NEW ARRIVALS")), "WOMAN > NEW ARRIVALS")
        self.assertEqual(category_key(()), "Zara")

    def test_parse_taxonomy_rejects_non_object_payload(self):
        with self.assertRaises(ValueError):
            parse_taxonomy([])
        with self.assertRaises(ValueError):
            parse_taxonomy(None)

    def test_load_categories_returns_flat_schema(self):
        flat = load_categories(self.payload)
        self.assertEqual(len(flat), len(self.entries))
        for entry in flat:
            self.assertEqual(set(entry), {"category", "url"})

    def test_seo_category_id_from_url(self):
        self.assertEqual(
            seo_category_id_from_url("https://www.zara.com/us/en/woman-new-in-l1180.html"),
            "1180",
        )
        self.assertIsNone(seo_category_id_from_url("https://www.zara.com/us/en/woman-new-in.html"))
        self.assertIsNone(seo_category_id_from_url("https://www.zara.com/us/en/x-labc.html"))
        self.assertIsNone(seo_category_id_from_url(""))


class ZaraListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = ZaraListingSpider(
            category="WOMAN > NEW ARRIVALS > THE NEW", max_pages=1
        )
        self.taxonomy = json.loads(Path("sample/zara-categories.json").read_text())
        self.payload = json.loads(
            Path("sample/zara-listing-products.json").read_text()
        )
        self.entries = parse_taxonomy(self.taxonomy)

    def response(self, request, payload=None, status=200, body=None):
        if body is None:
            body = json.dumps(
                payload if payload is not None else self.payload
            ).encode()
        return TextResponse(
            request.url, request=request, body=body, status=status, encoding="utf-8"
        )

    # --------------------------------------------------------------- requests

    def test_first_request_hydrates_the_runtime_taxonomy(self):
        request = next(self.spider.start_requests())
        self.assertEqual(request.url, "https://www.zara.com/us/en/categories")
        self.assertEqual(request.headers["X-Requested-With"], b"XMLHttpRequest")
        self.assertIn(b"Chrome", request.headers["User-Agent"])

    def test_taxonomy_request_is_made_even_with_an_explicit_category(self):
        # The products endpoint needs the numeric menu id, which is absent from
        # the public URL, so the taxonomy is always fetched first.
        spider = ZaraListingSpider(category="anything", max_pages=1)
        self.assertEqual(
            next(spider.start_requests()).url,
            "https://www.zara.com/us/en/categories",
        )

    def test_parse_categories_selects_the_requested_entry(self):
        self.spider.categories = []
        request = next(self.spider.start_requests())
        response = self.response(request, self.taxonomy)
        follow = list(self.spider.parse_categories(response))
        self.assertEqual(len(follow), 1)
        self.assertEqual(
            follow[0].url,
            "https://www.zara.com/us/en/category/2546081/products?ajax=true",
        )
        self.assertEqual(follow[0].meta["entry"]["category"], "WOMAN > NEW ARRIVALS > THE NEW")
        self.assertEqual(len(self.spider.categories), 3)

    def test_products_request_carries_a_plp_referer(self):
        entry = self.entries[0]
        request = self.spider._products_request(entry, page=1)
        self.assertEqual(
            request.headers["Referer"], b"https://www.zara.com/us/en/woman-new-in-l1180.html"
        )
        self.assertEqual(request.meta["page"], 1)

    def test_taxonomy_run_without_a_target_crawls_every_category(self):
        spider = ZaraListingSpider(max_pages=1)
        spider.categories = []
        request = next(spider.start_requests())
        follow = list(spider.parse_categories(self.response(request, self.taxonomy)))
        self.assertEqual(len(follow), 3)
        self.assertEqual(
            {r.meta["entry"]["category_id"] for r in follow}, {2546081, 2420895, 2645257}
        )

    def test_unknown_category_raises_with_a_helpful_message(self):
        spider = ZaraListingSpider(category="NOPE > NOPE", max_pages=1)
        spider.categories = self.entries
        with self.assertRaises(ValueError) as ctx:
            spider._entry_for(spider.resolve_target_url())
        self.assertIn("Available categories", str(ctx.exception))

    def test_bare_url_run_requires_an_explicit_menu_id(self):
        # A URL outside the taxonomy cannot be resolved: the menu id is not in
        # the public URL, so it must be passed explicitly.
        url = "https://www.zara.com/us/en/some-new-category-l9999.html"
        with self.assertRaises(ValueError):
            ZaraListingSpider(url=url, max_pages=1)._entry_for(url)

        ok = ZaraListingSpider(url=url, category_id="12345", max_pages=1)
        entry = ok._entry_for(url)
        self.assertEqual(entry["category_id"], "12345")
        self.assertEqual(entry["seo_category_id"], "9999")

    # ------------------------------------------------------------------ parse

    def items(self, payload=None, spider=None):
        spider = spider or self.spider
        spider.categories = self.entries
        spider._seen_items.clear()
        entry = self.entries[0]
        request = spider._products_request(entry, page=1)
        return list(spider.parse_products(self.response(request, payload)))

    def test_emits_the_sample_product_from_the_ticket(self):
        items = self.items()
        by_id = {item["item_id"]: item for item in items}
        self.assertIn("555844528", by_id)
        jacket = by_id["555844528"]
        self.assertEqual(jacket["title"], "ZW COLLECTION FLORAL JACKET")
        self.assertEqual(jacket["price"], 129.0)
        self.assertEqual(jacket["currency"], "USD")
        self.assertEqual(jacket["partnumber"], "04088260-I2026")
        self.assertEqual(jacket["display_reference"], "4088/260")
        self.assertEqual(jacket["kind"], "Wear")
        self.assertEqual(jacket["brand"], "zara")
        self.assertEqual(jacket["colors"], ["Ecru / Beige"])
        self.assertEqual(jacket["color_count"], 1)
        self.assertEqual(
            jacket["url"],
            "https://www.zara.com/us/en/zw-collection-floral-jacket-p04088260.html",
        )
        self.assertEqual(jacket["category_id"], 2546081)

    def test_item_keys_match_feed_export_fields_exactly(self):
        for item in self.items():
            self.assertEqual(
                list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"]
            )

    def test_editorial_components_are_dropped(self):
        # Element 0 of the fixture holds a Bundle with an empty name; element 4
        # holds a *named* Bundle ("LOOK" outfit). Neither may be emitted.
        items = self.items()
        self.assertNotIn("9884826724", {item["item_id"] for item in items})
        self.assertNotIn("598703028", {item["item_id"] for item in items})
        for item in items:
            self.assertEqual(item["raw"]["type"], "Product")
            self.assertTrue(item["title"])

    def test_duplicate_product_ids_are_emitted_once(self):
        # 571885314 appears in two different merchandising elements.
        ids = [item["item_id"] for item in self.items()]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids.count("571885314"), 1)

    def test_prices_are_converted_from_minor_units(self):
        spider = self.spider
        self.assertEqual(spider._decimal(12900), 129.0)
        self.assertEqual(spider._decimal(3990), 39.9)
        self.assertEqual(spider._decimal(75900), 759.0)
        # Non-numeric, boolean and non-positive prices become None.
        self.assertIsNone(spider._decimal(None))
        self.assertIsNone(spider._decimal("12900"))
        self.assertIsNone(spider._decimal(True))
        self.assertIsNone(spider._decimal(0))
        self.assertIsNone(spider._decimal(-100))

    def test_original_price_is_never_invented(self):
        # A raw grep of the 5.5 MB live payload finds no oldPrice/salePrice/
        # discount key anywhere, so the mapped original price stays None.
        for item in self.items():
            self.assertIsNone(item["original_price"])
            self.assertIsNone(item["discount_percent"])
            self.assertNotIn("oldPrice", item["raw"])

    def test_discount_percent_only_when_a_real_markdown_exists(self):
        spider = self.spider
        component = {
            "id": 1,
            "name": "X",
            "type": "Product",
            "price": 8000,
            "oldPrice": 10000,
            "seo": {"keyword": "k", "seoProductId": "1"},
            "detail": {"colors": []},
            "availableColors": [],
        }
        response = self.response(self.spider._products_request(self.entries[0], page=1))
        item = spider._item(component, response, self.entries[0], 1, 1, 1)
        self.assertEqual(item["price"], 80.0)
        self.assertEqual(item["original_price"], 100.0)
        self.assertEqual(item["discount_percent"], 20.0)

    def test_image_url_prefers_the_absolute_delivery_url(self):
        spider = self.spider
        colors = [
            {
                "xmedia": [
                    {"type": "hls", "path": "/assets/public/vid"},
                    {
                        "type": "image",
                        "set": 2,
                        "path": "/assets/public/aaa/bbb/x-f1",
                        "extraInfo": {
                            "deliveryUrl": "https://static.zara.net/assets/public/aaa/bbb/x-f1/x-f1.jpg?ts=1"
                        },
                    },
                ]
            }
        ]
        self.assertEqual(
            spider._image_url(colors),
            "https://static.zara.net/assets/public/aaa/bbb/x-f1/x-f1.jpg?ts=1",
        )

    def test_image_url_falls_back_to_the_cdn_path_without_doubling_the_prefix(self):
        spider = self.spider
        colors = [{"xmedia": [{"type": "image", "set": 1, "path": "/assets/public/a/b/p"}]}]
        self.assertEqual(
            spider._image_url(colors),
            "https://www.zara.com/assets/public/a/b/p",
        )
        self.assertNotIn("/assets/public/assets/public", spider._image_url(colors))

    def test_image_url_prefers_set_one_and_skips_video(self):
        spider = self.spider
        colors = [
            {
                "xmedia": [
                    {"type": "image", "set": 2, "path": "/assets/public/set2"},
                    {"type": "image", "set": 1, "path": "/assets/public/set1"},
                ]
            }
        ]
        self.assertEqual(spider._image_url(colors), "https://www.zara.com/assets/public/set1")

    def test_image_url_ignores_3d_directory_paths_when_a_still_exists(self):
        spider = self.spider
        colors = [
            {"xmedia": [{"type": "image", "set": 2, "path": "/assets/public/dir/"}]},
            {"xmedia": [{"type": "image", "set": 1, "path": "/assets/public/real-p"}]},
        ]
        self.assertEqual(spider._image_url(colors), "https://www.zara.com/assets/public/real-p")

    def test_image_url_none_when_no_media(self):
        self.assertIsNone(self.spider._image_url([]))
        self.assertIsNone(self.spider._image_url([{"xmedia": []}]))

    def test_color_names_and_count(self):
        spider = self.spider
        self.assertEqual(
            spider._color_names(
                [{"colorName": "Red", "hexColor": "#650614"},
                 {"colorName": "Brown", "hexColor": "#420A0A"}]
            ),
            ["Red", "Brown"],
        )
        self.assertIsNone(spider._color_names([]))
        self.assertIsNone(spider._color_names([{"colorName": "  "}]))

    def test_brand_accepts_object_or_scalar(self):
        spider = self.spider
        self.assertEqual(spider._brand({"brandGroupCode": "zara"}), "zara")
        self.assertEqual(spider._brand("massimodutti"), "massimodutti")
        self.assertIsNone(spider._brand({}))
        self.assertIsNone(spider._brand(None))

    def test_product_url_falls_back_to_the_category_url(self):
        spider = self.spider
        entry = self.entries[0]
        self.assertEqual(spider._product_url({}, entry), entry["url"])
        self.assertEqual(
            spider._product_url({"keyword": "k", "seoProductId": "9"}, entry),
            "https://www.zara.com/us/en/k-p9.html",
        )

    def test_availability_mapping(self):
        spider = self.spider
        for value, coming_soon, in_stock in (
            ("in_stock", False, True),
            ("IN_STOCK", False, True),
            ("coming_soon", True, False),
            ("COMING_SOON", True, False),
            ("sold_out", False, False),
        ):
            component = {
                "id": 7, "name": "T", "type": "Product", "availability": value,
                "seo": {}, "detail": {"colors": []}, "availableColors": [],
            }
            response = self.response(spider._products_request(self.entries[0], page=1))
            spider._seen_items.clear()
            item = spider._item(component, response, self.entries[0], 1, 1, 1)
            self.assertEqual(item["availability"], value)
            self.assertEqual(item["coming_soon"], coming_soon)
            self.assertEqual(item["in_stock"], in_stock)

    def test_position_and_total_count_cover_the_response(self):
        items = self.items()
        self.assertEqual(
            [item["position"] for item in items], list(range(1, len(items) + 1))
        )
        # total_count counts the products in the response (5), not the deduped
        # number emitted (4) -- one id is repeated across merchandising blocks.
        self.assertEqual({item["total_count"] for item in items}, {5})
        for item in items:
            self.assertEqual(item["page"], 1)
            self.assertEqual(item["source"], "zara_api")

    def test_never_follows_a_second_page(self):
        # page/offset/limit/sort are ignored by the endpoint (byte-identical
        # bodies), so the crawl must stop after the single response.
        spider = self.spider
        spider.max_pages = 5
        spider.categories = self.entries
        spider._seen_items.clear()
        request = spider._products_request(self.entries[0], page=1)
        self.assertEqual(list(spider.parse_products(self.response(request))), self.items())

    def test_empty_product_groups_is_an_explicit_failure(self):
        with self.assertRaises(RuntimeError) as ctx:
            self.items(payload={"productGroups": [{"id": 1, "elements": []}]})
        self.assertIn("productGroups", str(ctx.exception))

    def test_a_payload_of_only_bundles_is_an_explicit_failure(self):
        payload = {
            "productGroups": [
                {
                    "id": 1,
                    "elements": [
                        {"commercialComponents": [{"id": 5, "name": "LOOK", "type": "Bundle"}]}
                    ],
                }
            ]
        }
        with self.assertRaises(RuntimeError) as ctx:
            self.items(payload=payload)
        self.assertIn("none of type 'Product'", str(ctx.exception))

    def test_non_200_is_an_explicit_failure(self):
        spider = self.spider
        spider.categories = self.entries
        spider._seen_items.clear()
        request = spider._products_request(self.entries[0], page=1)
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_products(self.response(request, status=403)))
        self.assertIn("HTTP 403", str(ctx.exception))

    def test_html_body_where_json_was_expected_is_rejected(self):
        spider = self.spider
        spider.categories = self.entries
        spider._seen_items.clear()
        request = spider._products_request(self.entries[0], page=1)
        response = self.response(request, body=b"<html>Access Denied</html>")
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_products(response))
        self.assertIn("bot-challenge", str(ctx.exception))

    def test_empty_taxonomy_is_an_explicit_failure(self):
        spider = ZaraListingSpider(category="X", max_pages=1)
        request = next(spider.start_requests())
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_categories(self.response(request, {"categories": []})))
        self.assertIn("no product-category nodes", str(ctx.exception))

    def test_raw_payload_is_preserved(self):
        item = self.items()[0]
        self.assertEqual(item["raw"]["id"], int(item["item_id"]))
        self.assertIn("commercialComponents", json.dumps(self.payload))