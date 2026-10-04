from __future__ import annotations

import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.williams_sonoma_categories import (
    NON_CATEGORY_TYPES,
    build_index,
    group_id_from_url,
    parse_category_tree,
)
from common.spiders.williams_sonoma_listing_spider import WilliamsSonomaListingSpider

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample"


def make_response(
    url: str,
    body: str | bytes,
    *,
    status: int = 200,
    content_type: str = "application/json",
    meta: dict | None = None,
) -> TextResponse:
    if isinstance(body, str):
        body = body.encode("utf-8")
    request = Request(url, meta=meta or {})
    return TextResponse(
        url,
        request=request,
        body=body,
        encoding="utf-8",
        status=status,
        headers={"Content-Type": content_type},
    )


TEST_KEY = "key_TESTfixture0000000"


def load_all(spider, response):
    """Everything `parse_browse` yields: items plus any follow-up Requests."""
    return list(spider.parse_browse(response))


def load_items(spider, response):
    """Only the emitted items (pagination Requests are not items)."""
    return [
        out
        for out in spider.parse_browse(response)
        if isinstance(out, dict) and "item_id" in out
    ]


def next_requests(spider, response):
    """Only the pagination Requests `parse_browse` schedules."""
    return [out for out in spider.parse_browse(response) if isinstance(out, Request)]


def tree_response(spider, *, status=200, body=None):
    if body is None:
        body = (SAMPLE_DIR / "williams-sonoma-category-tree.json").read_text()
    url = "https://www.williams-sonoma.com/api/catalog/v1/category/categorytree/shop/data.json"
    return make_response(url, body, status=status, meta={})


def browse_response(spider, category, page=1, *, body=None, status=200):
    if body is None:
        body = (SAMPLE_DIR / "williams-sonoma-browse-items.json").read_text()
    url = f"https://ac.cnstrc.com/browse/group_id/{category.group_id}?key=k&page={page}"
    return make_response(url, body, status=status, meta={"category": category, "page": page})


class CategoryTreeTests(unittest.TestCase):
    def setUp(self):
        self.tree = (SAMPLE_DIR / "williams-sonoma-category-tree.json").read_text()

    def test_parse_tree_flattens_and_dedupes_group_ids(self):
        categories = parse_category_tree(self.tree)
        ids = [c.group_id for c in categories]
        self.assertEqual(len(ids), len(set(ids)), "group_ids must be unique crawl targets")
        self.assertIn("cookware", ids)
        self.assertIn("cookware-sets", ids)
        self.assertGreater(len(categories), 2)

    def test_headers_and_leftheaders_are_excluded(self):
        categories = parse_category_tree(self.tree)
        types = {c.node_type for c in categories}
        self.assertFalse(types & NON_CATEGORY_TYPES)
        # `cookware-stovetop-view-all` sits behind a `header` node's
        # referenceCategoryPath; the header itself must not become a target.
        self.assertNotIn(
            "stovetop-cookware",
            [c.group_id for c in categories],
        )

    def test_category_names_are_html_unescaped(self):
        index = build_index(parse_category_tree(self.tree))
        self.assertEqual(index["fry-pans-skillets"].name, "Fry Pans & Skillets")

    def test_urls_and_parents_are_built_from_the_tree_path(self):
        index = build_index(parse_category_tree(self.tree))
        cookware_sets = index["cookware-sets"]
        self.assertEqual(
            cookware_sets.url,
            "https://www.williams-sonoma.com/shop/cookware/cookware-sets/",
        )
        self.assertEqual(cookware_sets.parent_id, "cookware")
        self.assertEqual(cookware_sets.parent_name, "Cookware")

    def test_index_lookup_covers_every_category(self):
        categories = parse_category_tree(self.tree)
        self.assertEqual(len(build_index(categories)), len(categories))

    def test_group_id_from_url(self):
        self.assertEqual(
            group_id_from_url("https://www.williams-sonoma.com/shop/cookware/cookware-sets/"),
            "cookware-sets",
        )
        self.assertEqual(
            group_id_from_url("https://www.williams-sonoma.com/shop/sale-special-offer/?page=2"),
            "sale-special-offer",
        )

    def test_group_id_from_url_rejects_non_category_urls(self):
        # A product URL has no category segment; guessing the last segment would
        # browse an unrelated Constructor group instead of failing.
        with self.assertRaises(ValueError):
            group_id_from_url(
                "https://www.williams-sonoma.com/products/flat-tinned-pan/"
            )


class WilliamsSonomaListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = WilliamsSonomaListingSpider(
            category="cookware-sets", max_pages=2
        )
        # Load the taxonomy so `_resolve_targets` has an index to validate against.
        list(self.spider.parse_category_tree(tree_response(self.spider)))
        self.category = self.spider._index["cookware-sets"]
        self.browse_json = (SAMPLE_DIR / "williams-sonoma-browse-items.json").read_text()
        # The real flow reads the key off the page before browsing; these tests
        # exercise parse_browse directly, so prime that invariant here.
        self.spider._constructor_key = TEST_KEY

    def prime(self, **kwargs):
        """A spider with the taxonomy loaded and the key already read."""
        kwargs.setdefault("category", "cookware-sets")
        kwargs.setdefault("max_pages", 2)
        spider = WilliamsSonomaListingSpider(**kwargs)
        list(spider.parse_category_tree(tree_response(spider)))
        spider._constructor_key = TEST_KEY
        return spider

    # ----------------------------------------------------------------- targets

    def test_category_arg_selects_one_target(self):
        spider = WilliamsSonomaListingSpider(category="cookware", max_pages=1)
        list(spider.parse_category_tree(tree_response(spider)))
        targets = spider._resolve_targets()
        self.assertEqual([t.group_id for t in targets], ["cookware"])

    def test_category_url_arg_derives_the_group_id(self):
        spider = WilliamsSonomaListingSpider(
            category_url="https://www.williams-sonoma.com/shop/cookware/cookware-sets/",
            max_pages=1,
        )
        list(spider.parse_category_tree(tree_response(spider)))
        self.assertEqual([t.group_id for t in spider._resolve_targets()], ["cookware-sets"])

    def test_all_categories_expands_to_the_whole_inventory(self):
        spider = WilliamsSonomaListingSpider(all_categories="true", max_pages=1)
        list(spider.parse_category_tree(tree_response(spider)))
        targets = spider._resolve_targets()
        self.assertEqual(len(targets), len(spider._index))
        self.assertIn("cookware-sets", [t.group_id for t in targets])

    def test_unknown_category_fails_loudly(self):
        spider = WilliamsSonomaListingSpider(category="not-a-real-cat", max_pages=1)
        with self.assertRaises(ValueError):
            list(spider.parse_category_tree(tree_response(spider)))

    def test_no_selector_raises(self):
        spider = WilliamsSonomaListingSpider(max_pages=1)
        with self.assertRaises(ValueError):
            list(spider.parse_category_tree(tree_response(spider)))

    # ------------------------------------------------------------ key reading

    def test_constructor_key_is_read_from_page_state(self):
        context = (SAMPLE_DIR / "williams-sonoma-context.html").read_text()
        spider = WilliamsSonomaListingSpider(category="cookware-sets", max_pages=1)
        list(spider.parse_category_tree(tree_response(spider)))
        category = spider._index["cookware-sets"]
        response = make_response(
            category.url,
            context,
            content_type="text/html",
            meta={"targets": [category]},
        )
        requests = list(spider.parse_context(response))
        self.assertIsNotNone(spider._constructor_key)
        self.assertTrue(spider._constructor_key.startswith("key_"))
        self.assertEqual(len(requests), 1)
        self.assertIn("/browse/group_id/cookware-sets", requests[0].url)
        self.assertIn("key=", requests[0].url)

    def test_missing_constructor_key_raises_instead_of_using_a_constant(self):
        spider = WilliamsSonomaListingSpider(category="cookware-sets", max_pages=1)
        list(spider.parse_category_tree(tree_response(spider)))
        category = spider._index["cookware-sets"]
        response = make_response(
            category.url,
            "<html><body>no state here</body></html>",
            content_type="text/html",
            meta={"targets": [category]},
        )
        with self.assertRaises(RuntimeError):
            list(spider.parse_context(response))

    # ------------------------------------------------------------ item parsing

    def test_items_carry_the_full_feed_contract(self):
        items = load_items(self.spider, browse_response(self.spider, self.category))
        self.assertTrue(items)
        for item in items:
            self.assertEqual(
                list(item), list(self.spider.custom_settings["FEED_EXPORT_FIELDS"])
            )
            self.assertTrue(item["raw"], "every item must carry raw")

    def test_field_extraction(self):
        item = load_items(self.spider, browse_response(self.spider, self.category))[0]
        raw = item["raw"]
        self.assertEqual(item["item_id"], raw["id"])
        self.assertEqual(item["title"], raw["title"])
        self.assertEqual(item["url"], raw["url"])
        self.assertEqual(item["sku"], raw["skuid"])
        self.assertEqual(item["price"], raw["salePriceMin"])
        self.assertEqual(item["regular_price"], raw["regularPriceMin"])
        self.assertEqual(item["price_min"], raw["lowestPrice"])
        self.assertEqual(item["price_type"], raw["productPriceType"])
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["source"], "williams_sonoma_constructor_browse")
        self.assertEqual(item["category"], "cookware-sets")
        self.assertEqual(item["category_name"], "Cookware Sets")
        self.assertEqual(item["parent_category"], "Cookware")
        self.assertEqual(item["category_url"], self.category.url)
        self.assertEqual(item["page"], 1)
        self.assertIn("freeShip", item["flags"])
        # The fixture truncates the comma/`~` joined lists, so derive the counts
        # from the fixture itself rather than hardcoding a magic number.
        self.assertEqual(
            item["alt_images_count"],
            len([p for p in raw["altImages"].split(",") if p.strip()]),
        )
        self.assertEqual(
            item["swatches_count"],
            len([p for p in raw["swatchPrices"].split("~") if p.strip()]),
        )
        self.assertEqual(item["group_ids"], raw["group_ids"][:4])

    def test_price_prefers_sale_then_lowest(self):
        item = self.spider._product_item(
            {
                "id": "x",
                "salePriceMin": 10.0,
                "lowestPrice": 12.0,
                "regularPriceMin": 20.0,
            },
            self.category,
            1,
        )
        self.assertEqual(item["price"], 10.0)
        self.assertEqual(item["regular_price"], 20.0)

        # A non-discounted item has no sale price; the lowest price is next best.
        item = self.spider._product_item(
            {"id": "y", "lowestPrice": 49.5, "regularPriceMin": 49.5}, self.category, 1
        )
        self.assertEqual(item["price"], 49.5)
        self.assertIsNone(item["sale_price_min"])

        # Regular-price-only fallback keeps an item from losing its price.
        item = self.spider._product_item(
            {"id": "z", "regularPriceMin": 7.0}, self.category, 1
        )
        self.assertEqual(item["price"], 7.0)

    def test_missing_optional_fields_do_not_crash(self):
        item = self.spider._product_item({"id": "bare"}, self.category, 1)
        self.assertIsNone(item["price"])
        self.assertIsNone(item["url"])
        self.assertEqual(item["flags"], [])
        self.assertEqual(item["alt_images_count"], 0)

    def test_result_without_id_is_a_contract_break(self):
        response = make_response(
            "https://ac.cnstrc.com/browse/group_id/cookware-sets?key=k",
            json.dumps({"response": {"total_num_results": 1, "results": [{"data": {}}]}}),
            meta={"category": self.category, "page": 1},
        )
        with self.assertRaises(RuntimeError):
            load_items(self.spider, response)

    # -------------------------------------------------------------- pagination

    def test_pagination_advances_until_max_pages(self):
        requests = next_requests(
            self.spider, browse_response(self.spider, self.category, page=1)
        )
        self.assertTrue(requests)
        self.assertIn("page=2", requests[-1].url)
        self.assertIn("num_results_per_page=100", requests[-1].url)
        self.assertIn("section=Products", requests[-1].url)

    def test_pagination_stops_at_total_num_results(self):
        spider = self.prime(max_pages=50)
        category = self.category
        # total 227 / page_size 100 -> page 3 is the last one that can hold items.
        body = json.dumps(
            {"response": {"total_num_results": 227, "results": [{"data": {"id": "a"}}]}}
        )
        for page, expect_next in ((1, True), (2, True), (3, False)):
            response = make_response(
                "https://ac.cnstrc.com/browse/group_id/cookware-sets",
                body,
                meta={"category": category, "page": page},
            )
            requests = list(spider.parse_browse(response))
            self.assertEqual(bool(requests), expect_next, f"page {page}")

    def test_max_pages_is_respected(self):
        spider = self.prime(max_pages=1)
        category = self.category
        response = make_response(
            "https://ac.cnstrc.com/browse/group_id/cookware-sets",
            json.dumps(
                {"response": {"total_num_results": 5000, "results": [{"data": {"id": "a"}}]}}
            ),
            meta={"category": category, "page": 1},
        )
        self.assertEqual(next_requests(spider, response), [])

    def test_duplicate_ids_across_pages_are_dropped(self):
        spider = self.prime()
        category = self.category
        body = json.dumps(
            {
                "response": {
                    "total_num_results": 200,
                    "results": [{"data": {"id": "a"}}, {"data": {"id": "b"}}],
                }
            }
        )
        first = load_items(
            spider,
            make_response(
                "https://ac.cnstrc.com/x", body, meta={"category": category, "page": 1}
            ),
        )
        second = load_items(
            spider,
            make_response(
                "https://ac.cnstrc.com/x", body, meta={"category": category, "page": 2}
            ),
        )
        items = first + second
        ids = [i["item_id"] for i in items]
        self.assertEqual(ids, ["a", "b"])

    # --------------------------------------------------------- zero + failures

    def test_zero_result_category_is_a_log_line_not_a_crash(self):
        body = json.dumps({"response": {"total_num_results": 0, "results": []}})
        response = make_response(
            "https://ac.cnstrc.com/browse/group_id/gift-cards",
            body,
            meta={"category": self.spider._index["cookware-sets"], "page": 1},
        )
        with self.assertLogs(self.spider.logger.name, level="WARNING") as logs:
            self.assertEqual(load_items(self.spider, response), [])
        self.assertIn("0 products", " ".join(logs.output))

    def test_non_json_browse_body_raises(self):
        response = make_response(
            "https://ac.cnstrc.com/browse/group_id/cookware-sets",
            "<html>we are sorry</html>",
            content_type="text/html",
            meta={"category": self.category, "page": 1},
        )
        with self.assertRaises(RuntimeError):
            load_items(self.spider, response)

    def test_challenge_page_is_rejected(self):
        response = make_response(
            "https://ac.cnstrc.com/browse/group_id/cookware-sets",
            "<html><body>Please verify you are a human</body></html>",
            content_type="text/html",
            meta={"category": self.category, "page": 1},
        )
        with self.assertRaises(RuntimeError):
            load_items(self.spider, response)

    def test_non_200_is_rejected(self):
        with self.assertRaises(RuntimeError):
            load_items(
                self.spider,
                browse_response(self.spider, self.category, status=403),
            )

    def test_malformed_envelope_is_rejected(self):
        for body in ('{"response": []}', '{"response": {}}', "[]"):
            response = make_response(
                "https://ac.cnstrc.com/browse/group_id/cookware-sets",
                body,
                meta={"category": self.category, "page": 1},
            )
            with self.assertRaises(RuntimeError):
                load_items(self.spider, response)

    def test_category_tree_failure_is_reported(self):
        spider = WilliamsSonomaListingSpider(category="cookware-sets", max_pages=1)
        with self.assertRaises(RuntimeError):
            list(spider.parse_category_tree(tree_response(spider, body="<html>nope</html>")))


if __name__ == "__main__":
    unittest.main()