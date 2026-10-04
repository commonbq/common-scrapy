from pathlib import Path
import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.belk_categories import BELK_CATEGORIES, BELK_CATEGORY_INVENTORY
from common.spiders.belk_listing_spider import BelkListingSpider


CATEGORY = "shoes/womens-shoes/flats"
API_URL = "https://www.belk.com/ecom/cio/v1/web/category/" + CATEGORY + "?v2=true"
SAMPLE_DIR = Path("sample")


class BelkListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = BelkListingSpider(category=CATEGORY, max_pages=2)
        self.page1 = (SAMPLE_DIR / "belk-listing-flats-p1.json").read_text(encoding="utf-8")
        self.page2 = (SAMPLE_DIR / "belk-listing-flats-p2.json").read_text(encoding="utf-8")
        self.tiles1 = json.loads(self.page1)["product_tiles"]

    def response(self, body=None, *, page=1, url=None):
        if url is None:
            url = API_URL + (f"&start={60 * (page - 1)}&sz=60" if page > 1 else "")
        request = Request(url, meta={"page": page, **self.spider._meta()})
        return TextResponse(
            url,
            request=request,
            body=self.page1 if body is None else body,
            encoding="utf-8",
        )

    def items(self, body=None, *, page=1, url=None):
        return [
            out for out in self.spider.parse(self.response(body, page=page, url=url))
            if isinstance(out, dict)
        ]

    def tile(self, item_id):
        return next(t for t in self.tiles1 if t["id"] == item_id)

    # ---------------------------------------------------------------- taxonomy

    def test_inventory_shape_and_first_url(self):
        self.assertEqual(len(BELK_CATEGORY_INVENTORY), 13)
        self.assertEqual(len(BELK_CATEGORIES), 427)
        self.assertEqual(len({entry["category"] for entry in BELK_CATEGORIES}), 427)
        self.assertEqual(len({entry["url"] for entry in BELK_CATEGORIES}), 427)
        self.assertTrue(all(entry["url"].startswith(
            "https://www.belk.com/ecom/cio/v1/web/category/") for entry in BELK_CATEGORIES
        ))
        self.assertEqual(self.spider._first_api_url(), API_URL)
        self.assertEqual(self.spider._meta()["department"], "Shoes")

    def test_cross_linked_paths_report_the_shallowest_department(self):
        """/fan-gear/ is linked 30 times; the department itself must win."""
        entry = next(e for e in BELK_CATEGORIES if e["category"] == "fan-gear")
        self.assertEqual(entry["department"], "Fan Gear")
        self.assertEqual(entry["cgid"], "fan-gear")
        home = next(e for e in BELK_CATEGORIES if e["category"] == "home/home-decor")
        self.assertEqual(home["department"], "Home")
        self.assertEqual(len({e["department"] for e in BELK_CATEGORIES}), 13)

    def test_search_shortcuts_are_not_categories_but_their_children_are(self):
        categories = {entry["category"] for entry in BELK_CATEGORIES}
        self.assertNotIn("search", categories)
        self.assertNotIn("shopbybrand", categories)
        self.assertIn("home/home-decor", categories)  # lives under a /search/ mega-menu node

    def test_category_accepts_path_unique_leaf_and_site_url(self):
        expected = "https://www.belk.com/ecom/cio/v1/web/category/home/home-decor?v2=true"
        for spider in (
            BelkListingSpider(category="home/home-decor"),
            BelkListingSpider(category="home-decor"),
            BelkListingSpider(category_url="https://www.belk.com/home/home-decor/"),
            BelkListingSpider(url=expected),
        ):
            self.assertEqual(spider._first_api_url(), expected)

    def test_taxonomy_context_is_resolved_for_every_argument_form(self):
        for spider in (
            BelkListingSpider(category="home/home-decor"),
            BelkListingSpider(category_url="https://www.belk.com/home/home-decor/"),
            BelkListingSpider(url=API_URL.replace("shoes/womens-shoes/flats", "home/home-decor")),
        ):
            meta = spider._meta()
            self.assertEqual(meta["category"], "home/home-decor")
            self.assertEqual(meta["department"], "Home")
            self.assertEqual(meta["subcategory"], "Home Decor")
            self.assertEqual(meta["site_url"], "https://www.belk.com/home/home-decor/")

    def test_browse_path_is_extracted_from_both_url_shapes(self):
        self.assertEqual(
            self.spider.browse_path("https://www.belk.com/home/home-decor/"),
            "home/home-decor",
        )
        self.assertEqual(self.spider.browse_path(API_URL), CATEGORY)

    def test_ambiguous_leaf_and_unknown_category_fail_loudly(self):
        tails = {}
        for entry in BELK_CATEGORIES:
            tails.setdefault(entry["category"].rsplit("/", 1)[-1], []).append(entry["category"])
        ambiguous = next(name for name, paths in sorted(tails.items()) if len(paths) > 1)
        with self.assertRaises(ValueError) as ctx:
            BelkListingSpider(category=ambiguous)._first_api_url()
        self.assertIn("Ambiguous category", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            BelkListingSpider(category="nope/nope")._first_api_url()
        self.assertIn("Unknown category", str(ctx.exception))

        with self.assertRaises(ValueError):
            BelkListingSpider()

    # ----------------------------------------------------------------- parsing

    def test_first_page_yields_60_items_matching_feed_contract(self):
        items = self.items()
        self.assertEqual(len(items), 60)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

        first = items[0]
        self.assertEqual(first["item_id"], "2900965MULANEYW")
        self.assertEqual(first["title"], "Mulaney Flats")
        self.assertEqual(first["brand"], "DV Dolce Vita")
        self.assertEqual(
            first["url"],
            "https://www.belk.com/p/dv-dolce-vita-mulaney-flats/2900965MULANEYW.html",
        )
        self.assertEqual(first["price"], 45.5)
        self.assertEqual(first["original_price"], 65.0)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["discount_percent"], 30.0)
        self.assertEqual(first["total_count"], 1637)
        self.assertEqual(first["items_per_page"], 60)
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["source"], "belk_cio_category_api")
        self.assertEqual(first["badge"], "badge-db-buys")
        self.assertEqual(first["category_id"], "shoes-womens-shoes-flats")
        self.assertEqual(first["category_title"], "Women's Flats")
        self.assertEqual(first["breadcrumb"], ["Belk", "Shoes", "Women's Shoes", "Flats"])
        self.assertEqual(first["color"], "IVORY")
        self.assertIn("IVORY", first["swatches"])
        self.assertTrue(first["image_url"].startswith("https://belk.scene7.com/"))
        self.assertIsNotNone(first["raw"])

    def test_price_range_tile_uses_the_minimum(self):
        item = next(i for i in self.items() if i["item_id"] == "2900868MARCI")
        self.assertEqual(item["price"], 27.49)
        self.assertEqual(item["original_price"], 54.99)

    def test_sale_price_equal_to_original_reports_no_discount(self):
        item = next(i for i in self.items() if i["item_id"] == "2900053KIKIBK")
        self.assertEqual(item["price"], 60.0)
        self.assertEqual(item["original_price"], 60.0)
        self.assertIsNone(item["discount_percent"])

    def test_coupon_fields_are_exported(self):
        item = next(i for i in self.items() if i["item_id"] == "290001511775519")
        self.assertEqual(item["coupon_code"], "NEWFORFALL")
        self.assertEqual(item["coupon_discount_percent"], 30.0)
        self.assertEqual(item["coupon_price"], 48.3)
        self.assertEqual(item["coupon_end_date"], "2026-10-05T03:59:00.000Z")

    def test_promotions_are_exported(self):
        item = next(i for i in self.items() if i["item_id"] == "2900053BELLEVUE2")
        self.assertEqual(item["promotions"], ["BOGO: Buy 1, Get 1 Free"])

    def test_rating_and_reviews_are_parsed(self):
        item = next(i for i in self.items() if i["rating"] is not None)
        self.assertEqual(item["rating"], 3.0)
        self.assertEqual(item["reviews_count"], 1)
        self.assertIs(item["marketplace"], False)  # mirakl=False, not a marketplace tile

    def test_capped_total_count_is_normalised(self):
        body = json.dumps({"header": {"count": "10,000+"}, "product_tiles": [
            {"id": "1", "title": "x", "url": "/p/x/1.html", "price": {"orig": {"min": 1}}}
        ]})
        self.assertEqual(self.items(body)[0]["total_count"], 10000)

    # -------------------------------------------------------------- pagination

    def test_next_page_uses_api_offset_params_and_stops_at_max_pages(self):
        first = list(self.spider.parse(self.response()))[-1]
        self.assertEqual(first.url, API_URL + "&start=60&sz=60")
        self.assertEqual(first.meta["page"], 2)

        single = BelkListingSpider(category=CATEGORY, max_pages=1)
        outputs = list(single.parse(self.response()))
        self.assertFalse([o for o in outputs if not isinstance(o, dict)])

    def test_second_page_yields_items_without_page_one_duplicates(self):
        first_ids = {i["item_id"] for i in self.items()}
        second = [
            out for out in self.spider.parse(self.response(self.page2, page=2))
            if isinstance(out, dict)
        ]
        # the live capture repeats one promoted item across the page boundary
        self.assertEqual(len(second), 59)
        self.assertFalse({i["item_id"] for i in second} & first_ids)
        self.assertTrue(all(i["page"] == 2 for i in second))
        self.assertEqual(second[0]["position"], 1)

    def test_pagination_falls_back_to_stepped_offset_without_navs(self):
        body = json.dumps({
            "header": {"count": "130"},
            "pagination": {"navs": []},
            "product_tiles": [{"id": "1", "title": "x"}],
        })
        request = next(o for o in self.spider.parse(self.response(body)) if not isinstance(o, dict))
        for needle in ("start=60", "sz=60", "v2=true"):
            self.assertIn(needle, request.url)

    def test_pagination_stops_at_reported_total(self):
        body = json.dumps({
            "header": {"count": "60"},
            "pagination": {"navs": []},
            "product_tiles": [{"id": "1", "title": "x"}],
        })
        self.assertFalse([o for o in self.spider.parse(self.response(body))
                          if not isinstance(o, dict)])

    def test_duplicate_tiles_within_a_page_are_collapsed(self):
        body = json.dumps({"product_tiles": [
            {"id": "9", "title": "a"}, {"id": "9", "title": "a"}, {"id": "10", "title": "b"},
        ]})
        self.assertEqual([i["item_id"] for i in self.items(body)], ["9", "10"])

    # ---------------------------------------------------------------- failures

    def test_non_json_challenge_body_fails_visibly(self):
        for body, needle in [
            ("<html><body>Access denied</body></html>", "did not return JSON"),
            ("", "did not return JSON"),
            ('{"header": ', "did not return JSON"),
            ("[1, 2, 3]", "expected an object"),
        ]:
            with self.assertRaises(RuntimeError) as ctx:
                list(self.spider.parse(self.response(body)))
            self.assertIn(needle, str(ctx.exception))

    def test_missing_and_empty_product_tiles_fail_visibly(self):
        for payload, needle in [
            ({"header": {"count": "1"}}, "no list-valued 'product_tiles'"),
            ({"product_tiles": []}, "zero product tiles"),
        ]:
            with self.assertRaises(RuntimeError) as ctx:
                list(self.spider.parse(self.response(json.dumps(payload))))
            self.assertIn(needle, str(ctx.exception))

    def test_landing_page_redirect_is_reported_not_swallowed(self):
        body = json.dumps({"metaData": {"redirectUrl": "/search/?pmid=BelkClearance"}})
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.response(body)))
        self.assertIn("landing page", str(ctx.exception))
        self.assertIn("/search/?pmid=BelkClearance", str(ctx.exception))

    def test_unknown_category_404_is_reported(self):
        body = json.dumps({"status": 404, "message": "Category not found belkdigitalbooks"})
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.response(body)))
        self.assertIn("does not know category", str(ctx.exception))

    def test_non_200_status_fails_visibly(self):
        response = self.response()
        response.status = 403
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(response))
        self.assertIn("HTTP 403", str(ctx.exception))

    def test_tiles_without_id_are_skipped(self):
        body = json.dumps({"product_tiles": [
            {"title": "no id"}, {"id": "", "title": "blank"}, {"id": "5", "title": "ok"},
        ]})
        self.assertEqual([i["item_id"] for i in self.items(body)], ["5"])

    def test_requests_carry_the_api_url_and_json_headers(self):
        request = next(iter(self.spider.start_requests()))
        self.assertEqual(request.url, API_URL)
        self.assertIn("application/json", request.headers["Accept"].decode())
        self.assertEqual(request.headers["Referer"].decode(), "https://www.belk.com/")
        self.assertEqual(request.meta["page"], 1)


if __name__ == "__main__":
    unittest.main()