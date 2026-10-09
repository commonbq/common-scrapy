from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.shopbop_categories import SHOPBOP_CATEGORIES
from common.spiders.shopbop_listing_spider import (
    HYDRATE_MARKER,
    IMAGE_CDN,
    IMAGE_SUFFIX,
    ShopbopListingSpider,
)


PAGE1_URL = "https://www.shopbop.com/whats-new/br/v=1/13198.htm"
PAGE2_URL = "https://www.shopbop.com/whats-new/br/v=1/13198.htm?offset=100"
SALE_URL = "https://www.shopbop.com/sale/br/v=1/13594.htm"


def load(name: str) -> str:
    return Path("sample", name).read_text(encoding="utf-8")


def navigation() -> dict:
    """Rebuild the taxonomy the way the builder did, straight from the saved homepage."""
    hydrate = ShopbopListingSpider._hydrate(load("shopbop-home-navigation.html"), PAGE1_URL)
    slots = hydrate["dehydratedState"]["frameworkState"]["dd"]["renderTree"]["topLevelSlots"]
    props = slots["top-nav-1"]["content"]["slotConfiguration"]["squareState"]["props"]
    return props["unfilteredNavigationData"]["navigationCategoryGroupList"]


class ShopbopListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = ShopbopListingSpider(category="Women > What's New", max_pages=2)
        self.page1 = load("shopbop-listing-page1.html")
        self.page2 = load("shopbop-listing-page2.html")
        self.sale = load("shopbop-listing-sale.html")
        self.lastpage = load("shopbop-listing-lastpage.html")

    def response(self, body, url=PAGE1_URL, page=1, offset=0, meta=None):
        request_meta = {
            "category": "Women > What's New",
            "department": "Women",
            "subcategory": "What's New",
            "leaf": None,
            "page": page,
            "offset": offset,
        }
        request_meta.update(meta or {})
        return TextResponse(url, request=Request(url, meta=request_meta), body=body, encoding="utf-8")

    def results(self, body, **kwargs):
        return list(self.spider.parse(self.response(body, **kwargs)))

    def items(self, body, **kwargs):
        return [i for i in self.results(body, **kwargs) if isinstance(i, dict)]

    def follow_ups(self, body, **kwargs):
        return [r for r in self.results(body, **kwargs) if isinstance(r, Request)]

    # ------------------------------------------------------------------ taxonomy

    def test_inventory_is_unique_and_crawlable(self):
        self.assertEqual(len(_FLAT(SHOPBOP_CATEGORIES)), 266)
        self.assertEqual(len({e["category"] for e in _FLAT(SHOPBOP_CATEGORIES)}), 266)
        self.assertEqual(len({e["url"] for e in _FLAT(SHOPBOP_CATEGORIES)}), 266)
        self.assertTrue(all(e["url"].startswith("https://www.shopbop.com/") for e in _FLAT(SHOPBOP_CATEGORIES)))
        # Only PLP routes survive; the storefront's editorial and designer-index links carry
        # no folderId and are filtered out.
        self.assertTrue(all(e["folder_id"] for e in _FLAT(SHOPBOP_CATEGORIES)))
        self.assertFalse([e for e in _FLAT(SHOPBOP_CATEGORIES) if "/ci/" in e["url"]])
        self.assertFalse([e for e in _FLAT(SHOPBOP_CATEGORIES) if "/vp/" in e["url"]])

    def test_taxonomy_covers_the_three_navigation_groups(self):
        groups = {e["department"] for e in _FLAT(SHOPBOP_CATEGORIES)}
        self.assertEqual(groups, {"Women", "Men", "Beauty"})
        counts = {g: sum(1 for e in _FLAT(SHOPBOP_CATEGORIES) if e["department"] == g) for g in groups}
        self.assertEqual(counts, {"Women": 183, "Men": 70, "Beauty": 13})

    def test_category_lookup_returns_the_hydrated_url(self):
        self.assertEqual(
            ShopbopListingSpider(category="Women > What's New").resolve_target_url(), PAGE1_URL
        )
        self.assertEqual(
            ShopbopListingSpider(category="Men > Shoes").resolve_target_url(),
            "https://www.shopbop.com/men-shoes/br/v=1/19186.htm",
        )
        self.assertEqual(
            ShopbopListingSpider(category="Beauty > Beauty > Makeup").resolve_target_url(),
            "https://www.shopbop.com/beauty-makeup/br/v=1/69288.htm",
        )

    def test_taxonomy_matches_the_saved_navigation_payload(self):
        """Rebuild the inventory from the homepage fixture: 335 nodes -> 266 unique URLs."""
        rows = []
        for group in navigation():
            for category in group["categories"]:
                rows.append((0, group["title"], category.get("title"), None, None,
                             category.get("link"), category.get("folderId")))
                for section in category.get("sectionList") or []:
                    if section.get("link"):
                        rows.append((1, group["title"], category.get("title"), section.get("title"),
                                     None, section.get("link"), section.get("folderId")))
                    for item in section.get("itemList") or []:
                        rows.append((2, group["title"], category.get("title"),
                                     section.get("title") or None, item.get("title"),
                                     item.get("link"), item.get("folderId")))

        self.assertEqual(len(rows), 335, "the homepage ships 335 navigation link nodes")
        kept = [r for r in rows if r[6]]
        self.assertEqual(len(kept), 315, "20 nodes carry no folderId and are not category pages")

        shallowest = {}
        for row in kept:
            if row[5] not in shallowest or row[0] < shallowest[row[5]][0]:
                shallowest[row[5]] = row
        self.assertEqual(len(shallowest), 266, "49 nodes repeat a shallower URL")

        expected = {
            "https://www.shopbop.com" + url: row[6] for url, row in shallowest.items()
        }
        actual = {e["url"]: e["folder_id"] for e in _FLAT(SHOPBOP_CATEGORIES)}
        self.assertEqual(actual, expected)

    def test_deepest_duplicate_keeps_the_shallow_placement(self):
        """/whats-new is shipped three times; the primary category node must win."""
        entries = [e for e in _FLAT(SHOPBOP_CATEGORIES) if e["folder_id"] == "13198"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["category"], "Women > What's New")

    def test_non_product_navigation_links_are_excluded(self):
        urls = {e["url"] for e in _FLAT(SHOPBOP_CATEGORIES)}
        self.assertNotIn("https://www.shopbop.com/designers", urls)
        self.assertNotIn("https://www.shopbop.com/shop-men", urls)
        self.assertNotIn("https://www.shopbop.com/giftcard", urls)

    # ------------------------------------------------------------------ hydration

    def test_hydration_is_read_with_balanced_json(self):
        """The blob is megabytes of nested JSON; a greedy regex would truncate it."""
        hydrate = ShopbopListingSpider._hydrate(self.page1, PAGE1_URL)
        self.assertEqual(hydrate["pageType"], "PLP")
        self.assertIn("dehydratedState", hydrate)
        self.assertIn(HYDRATE_MARKER, self.page1)

    def test_hydration_survives_braces_inside_strings(self):
        document = (
            "<script>window.__shopbop_sca_hydrate__ = "
            + '{"pageType": "PLP", "note": "a }; b ; \\" still inside", "n": 2};'
            + "</script>"
        )
        self.assertEqual(
            ShopbopListingSpider._hydrate(document, PAGE1_URL),
            {"pageType": "PLP", "note": 'a }; b ; " still inside', "n": 2},
        )

    def test_missing_hydration_raises(self):
        with self.assertRaises(RuntimeError) as ctx:
            ShopbopListingSpider._hydrate("<html><body>captcha</body></html>", PAGE1_URL)
        self.assertIn("No shopbop", str(ctx.exception))

    def test_unbalanced_hydration_raises(self):
        with self.assertRaises(RuntimeError) as ctx:
            ShopbopListingSpider._hydrate(
                "<script>window.__shopbop_sca_hydrate__ = {\"pageType\": \"PLP\"", PAGE1_URL
            )
        self.assertIn("not a decodable JSON object", str(ctx.exception))

    def test_products_query_is_found_regardless_of_slot_depth(self):
        """The products result is located by shape, not by slot id or component name."""
        hydrate = ShopbopListingSpider._hydrate(self.sale, SALE_URL)
        plp = ShopbopListingSpider._products_query(hydrate)
        self.assertIsInstance(plp, dict)
        self.assertEqual(len(plp["products"]), 6)
        self.assertEqual(plp["resultsTitle"], "Sale")
        # The masthead child slot carries its own queries list; the search must not stop early.
        containers = ShopbopListingSpider._query_containers(hydrate)
        self.assertGreaterEqual(len(containers), 2)

    def test_nested_products_query_is_still_found(self):
        hydrate = ShopbopListingSpider._hydrate(self.page1, PAGE1_URL)
        slots = hydrate["dehydratedState"]["frameworkState"]["dd"]["renderTree"]["topLevelSlots"]
        main = slots["plp-main"]["content"]["slotConfiguration"]["squareState"]["props"]["dehydratedState"]
        moved = slots["plp-main"]["content"]["children"] = {}
        deep = {"content": {"slotConfiguration": {"squareState": {"props": {"dehydratedState": main}}}}}
        slots["plp-main"]["content"]["children"] = {"buried": deep}
        self.assertEqual(len(ShopbopListingSpider._products_query(hydrate)["products"]), 6)
        self.assertIsNotNone(moved)

    def test_non_plp_document_reports_no_products_query(self):
        """`/designers` hydrates pageType="Designer" and carries no products query at all."""
        designer = load("shopbop-designer-index.html")
        hydrate = ShopbopListingSpider._hydrate(designer, "https://www.shopbop.com/designers")
        self.assertEqual(hydrate["pageType"], "Designer")
        self.assertIsNone(ShopbopListingSpider._products_query(hydrate))
        self.assertEqual(
            self.items(designer, url="https://www.shopbop.com/designers",
                       meta={"department": None, "subcategory": None, "leaf": None}),
            [],
        )

    def test_homepage_carries_navigation_but_no_products(self):
        hydrate = ShopbopListingSpider._hydrate(load("shopbop-home-navigation.html"), PAGE1_URL)
        self.assertEqual(hydrate["pageType"], "Homepage")
        self.assertIsNone(ShopbopListingSpider._products_query(hydrate))

    def test_empty_product_grid_raises_instead_of_returning_nothing(self):
        with self.assertRaises(RuntimeError) as ctx:
            self.items(load("shopbop-listing-empty.html"))
        self.assertIn("hydrated no product records", str(ctx.exception))

    def test_non_plp_page_type_with_products_raises(self):
        hydrate = ShopbopListingSpider._hydrate(self.page1, PAGE1_URL)
        hydrate["pageType"] = "Designer"
        document = (
            "<script>window.__shopbop_sca_hydrate__ = " + __import__("json").dumps(hydrate) + ";</script>"
        )
        with self.assertRaises(RuntimeError) as ctx:
            self.items(document)
        self.assertIn("expected 'PLP'", str(ctx.exception))

    def test_http_error_raises(self):
        response = self.response(self.page1)
        response.status = 503
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(response))
        self.assertIn("HTTP 503", str(ctx.exception))

    # ------------------------------------------------------------------ items

    def test_items_carry_the_required_fields(self):
        items = self.items(self.page1)
        self.assertEqual(len(items), 6)
        for item in items:
            self.assertTrue(item["item_id"], "productSin is the item id")
            self.assertTrue(item["sku_id"])
            self.assertTrue(item["title"])
            self.assertTrue(item["brand"])
            self.assertTrue(item["url"].startswith("https://www.shopbop.com/"))
            self.assertTrue(item["image_url"].startswith(IMAGE_CDN))
            self.assertTrue(item["price"])
            self.assertEqual(item["currency"], "USD")
            self.assertEqual(item["folder_id"], "13198")
            self.assertEqual(item["page"], 1)
            self.assertEqual(item["offset"], 0)
            self.assertIsInstance(item["position"], int)

    def test_export_fields_match_the_item_keys(self):
        fields = set(ShopbopListingSpider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(fields, set(self.items(self.page1)[0].keys()))

    def test_placeholder_export_fields_are_always_present(self):
        item = self.items(self.page1)[0]
        for key in ("original_price", "discount_percentage", "rating", "reviews_count",
                    "color_options", "size_options", "attribute_icons", "leaf",
                    "final_sale", "size_scale", "brand_url"):
            self.assertIn(key, item)

    def test_rating_is_not_reported_without_reviews(self):
        """`reviews.average` hydrates as 0 even for unrated products."""
        import json as _json
        hydrate = ShopbopListingSpider._hydrate(self.sale, SALE_URL)
        for container in ShopbopListingSpider._query_containers(hydrate):
            for query in container:
                if query.get("queryKey", [None])[0] == "products":
                    products = query["state"]["data"]["data"]["products"]
                    products[0]["product"]["reviews"] = {"count": 4, "average": 4.5}
                    products[1]["product"]["reviews"] = {"count": 0, "average": 0}
        document = "<script>window.__shopbop_sca_hydrate__ = " + _json.dumps(hydrate) + ";</script>"
        items = self.items(document, url=SALE_URL, meta={"subcategory": "Sale", "leaf": None})
        self.assertEqual(items[0]["rating"], 4.5)
        self.assertEqual(items[0]["reviews_count"], 4)
        self.assertIsNone(items[1]["rating"])
        self.assertEqual(items[1]["reviews_count"], 0)

    def test_image_url_resolves_the_storefront_relative_path(self):
        item = self.items(self.page1)[0]
        self.assertTrue(item["image_url"].startswith(IMAGE_CDN + "/prod/products/"))
        # The raw `.jpg` path from the payload 404s on the CDN, so the storefront's own
        # transform suffix is applied to the filename stem.
        self.assertTrue(item["image_url"].endswith(IMAGE_SUFFIX))

    def test_image_transform_is_only_applied_to_jpg_media(self):
        self.assertEqual(
            ShopbopListingSpider._sized("/prod/products/a/b_1.jpg"),
            "/prod/products/a/b_1" + IMAGE_SUFFIX,
        )
        self.assertEqual(ShopbopListingSpider._sized("/prod/products/a/b_1.webp"), "/prod/products/a/b_1.webp")

    def test_media_paths_use_the_image_cdn_not_the_site_host(self):
        self.assertEqual(
            ShopbopListingSpider._absolute("/prod/products/a/b.jpg", PAGE1_URL),
            IMAGE_CDN + "/prod/products/a/b" + IMAGE_SUFFIX,
        )
        # The `p` path segment is part of the CDN base; without it the CDN answers Not Found.
        self.assertIn("/Shopbop/p/prod/", ShopbopListingSpider._absolute("/prod/x.jpg", PAGE1_URL))

    def test_variant_detail_is_retained_in_raw(self):
        item = self.items(self.page1)[0]
        raw = item["raw"]
        self.assertIn("colors", raw)
        self.assertIn("sizes", raw)
        self.assertEqual(item["item_id"], raw["productSin"])
        self.assertEqual(item["sku_id"], raw["productCode"])
        # One item per productSin; colorways stay inside `raw`.
        self.assertEqual(item["color_option_count"], len(raw["colors"]))
        self.assertEqual(item["size_option_count"], len(raw["sizes"]))

    def test_color_and_size_names_are_deduplicated(self):
        item = self.items(self.page1)[0]
        names = [n.strip() for n in item["color_options"].split(",")]
        self.assertEqual(len(names), len(set(names)))
        self.assertIn(item["color"], names)

    def test_sale_items_carry_a_real_markdown(self):
        items = self.items(self.sale, url=SALE_URL, meta={"subcategory": "Sale", "leaf": None})
        self.assertTrue(items)
        for item in items:
            self.assertTrue(item["on_sale"])
            self.assertLess(item["price"], item["original_price"])
            self.assertGreater(item["discount_percentage"], 0)
            # The percentage is applied to the numeric `retailPrice.usdPrice`, never to the
            # formatted `lowPrice.price` string.
            self.assertAlmostEqual(
                item["original_price"] * (1 - item["discount_percentage"] / 100),
                item["price"],
                places=2,
            )

    def test_non_sale_items_have_no_original_price(self):
        for item in self.items(self.page1):
            self.assertFalse(item["on_sale"])
            self.assertIsNone(item["original_price"])
            self.assertIsNone(item["discount_percentage"])

    def test_url_driven_crawl_fills_the_category_from_results_title(self):
        items = self.items(
            self.page1,
            url="https://www.shopbop.com/clothing-dresses/br/v=1/13351.htm",
            meta={"category": "custom", "department": None, "subcategory": None, "leaf": None},
        )
        self.assertTrue(items)
        self.assertEqual(items[0]["subcategory"], "What's New")
        self.assertEqual(items[0]["folder_id"], "13198")
        self.assertIsNone(items[0]["department"], "the group is unknown for a bare -a url= run")

    # ------------------------------------------------------------------ pagination

    def test_page_two_is_requested_from_the_authoritative_next_offset(self):
        follow_up = self.follow_ups(self.page1)
        self.assertEqual(len(follow_up), 1)
        self.assertEqual(follow_up[0].url, PAGE2_URL)
        self.assertEqual(follow_up[0].meta["page"], 2)
        self.assertEqual(follow_up[0].meta["offset"], 100)

    def test_page_two_products_do_not_repeat_page_one(self):
        first = {i["item_id"] for i in self.items(self.page1)}
        second = self.items(self.page2, url=PAGE2_URL, page=2, offset=100)
        self.assertTrue(second)
        self.assertEqual(first & {i["item_id"] for i in second}, set())
        self.assertTrue(all(i["page"] == 2 and i["offset"] == 100 for i in second))

    def test_pagination_stops_at_max_pages(self):
        spider = ShopbopListingSpider(category="Women > What's New", max_pages=1)
        results = list(spider.parse(self.response(self.page1)))
        self.assertTrue([r for r in results if isinstance(r, dict)])
        self.assertEqual([r for r in results if isinstance(r, Request)], [])

    def test_natural_last_page_has_no_next_request(self):
        """A category with fewer than 100 items hydrates `nextOffset: null`."""
        results = self.results(
            self.lastpage,
            url="https://www.shopbop.com/beauty-suncare/br/v=1/71917.htm",
            meta={"subcategory": "Suncare", "leaf": None},
        )
        self.assertTrue([r for r in results if isinstance(r, dict)])
        self.assertEqual([r for r in results if isinstance(r, Request)], [])

    def test_pagination_preserves_existing_query_parameters(self):
        """Facet/sort state lives in the query string; only `offset` may change."""
        filtered = "https://www.shopbop.com/sale/br/v=1/13594.htm?productSort=price-asc&f=13064%2C1"
        url = ShopbopListingSpider._next_page_url(filtered, 100)
        self.assertEqual(
            url,
            "https://www.shopbop.com/sale/br/v=1/13594.htm?productSort=price-asc&f=13064%2C1&offset=100",
        )

    def test_pagination_replaces_an_existing_offset(self):
        self.assertEqual(
            ShopbopListingSpider._next_page_url(PAGE2_URL, 200), PAGE1_URL + "?offset=200"
        )

    def test_duplicate_products_are_emitted_once_across_pages(self):
        spider = ShopbopListingSpider(category="Women > What's New", max_pages=2)
        first = [i for i in spider.parse(self.response(self.page1)) if isinstance(i, dict)]
        self.assertEqual(len(first), 6)
        # Replaying page 1's grid as page 2 must not re-yield the same items.
        again = [
            i
            for i in spider.parse(self.response(self.page1, page=2, offset=100))
            if isinstance(i, dict)
        ]
        self.assertEqual(again, [])

    def test_entries_without_a_product_sin_are_skipped(self):
        import json as _json
        hydrate = ShopbopListingSpider._hydrate(self.page1, PAGE1_URL)
        for container in ShopbopListingSpider._query_containers(hydrate):
            for query in container:
                if query.get("queryKey", [None])[0] == "products":
                    data = query["state"]["data"]["data"]
                    data["products"][0] = {"colorSin": "1"}
                    data["products"][1] = {"colorSin": "2", "product": {}}
                    document = "<script>window.__shopbop_sca_hydrate__ = " + _json.dumps(hydrate) + ";</script>"
        items = self.items(document)
        self.assertEqual(len(items), 4)
        self.assertTrue(all(i["item_id"] for i in items))

    # ------------------------------------------------------------------ helpers

    def test_absolute_leaves_absolute_urls_alone(self):
        self.assertEqual(
            ShopbopListingSpider._absolute("https://cdn.example/x.jpg", PAGE1_URL),
            "https://cdn.example/x.jpg",
        )
        self.assertEqual(
            ShopbopListingSpider._absolute("/kyla-coat/vp/v=1/1.htm", PAGE1_URL),
            "https://www.shopbop.com/kyla-coat/vp/v=1/1.htm",
        )
        self.assertIsNone(ShopbopListingSpider._absolute("", PAGE1_URL))
        self.assertIsNone(ShopbopListingSpider._absolute(None, PAGE1_URL))

    def test_taxonomy_is_required_unless_a_url_is_given(self):
        with self.assertRaises(ValueError) as ctx:
            ShopbopListingSpider()
        self.assertIn("Provide -a category=", str(ctx.exception))

    def test_number_and_integer_reject_booleans(self):
        self.assertIsNone(ShopbopListingSpider._number(True))
        self.assertIsNone(ShopbopListingSpider._integer(False))
        self.assertEqual(ShopbopListingSpider._number("12.5"), 12.5)
        self.assertIsNone(ShopbopListingSpider._number("$1,495.00"))


if __name__ == "__main__":
    unittest.main()


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]
