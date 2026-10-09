import json
import unittest
from pathlib import Path

from scrapy.exceptions import CloseSpider
from scrapy.http import Request, TextResponse
from scrapy.settings import Settings

from common.spiders.basspro_categories import (
    BASSPRO_CATEGORIES,
    BASSPRO_COVEO_ORGANIZATION_ID,
    BASSPRO_COVEO_SEARCH_HUB,
    BASSPRO_DEPARTMENTS,
    BASSPRO_TOKEN_URL,
)
from common.spiders.basspro_listing_spider import (
    BassproListingSpider,
    as_int,
    first_image,
    flag,
    parse_number,
)

PLP_FIXTURE = Path("sample/basspro-plp.html")
TOKEN_FIXTURE = Path("sample/basspro-token.json")
PAGE1_FIXTURE = Path("sample/basspro-coveo-page1.json")
PAGE2_FIXTURE = Path("sample/basspro-coveo-page2.json")
LAST_PAGE_FIXTURE = Path("sample/basspro-coveo-lastpage.json")
ERROR_FIXTURE = Path("sample/basspro-coveo-error.json")
CHALLENGE_FIXTURE = Path("sample/basspro-challenge.html")


class BassproListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.settings.set("PROXY", "http://scrapeops.example:secret@proxy.example:5353")
        self.spider = BassproListingSpider(
            settings=self.settings, category="rod-reel-combos", max_pages=3
        )
        self.plp_html = PLP_FIXTURE.read_text()
        self.page1 = PAGE1_FIXTURE.read_text()
        self.page2 = PAGE2_FIXTURE.read_text()
        self.entry = next(e for e in BASSPRO_CATEGORIES if e["slug"] == "rod-reel-combos")

    def response(self, request, body, status=200):
        if not isinstance(body, str):
            body = json.dumps(body)
        return TextResponse(
            url=request.url,
            request=request,
            body=body.encode("utf-8"),
            status=status,
            encoding="utf-8",
        )

    # ----------------------------------------------------------------- taxonomy

    def test_taxonomy_inventory(self):
        levels = {}
        for entry in BASSPRO_CATEGORIES:
            levels[entry["level"]] = levels.get(entry["level"], 0) + 1
        self.assertEqual(len(BASSPRO_DEPARTMENTS), 11)
        self.assertEqual(levels, {1: 11, 2: 116, 3: 782})
        self.assertEqual(len(BASSPRO_CATEGORIES), 909)

    def test_taxonomy_entries_are_complete_and_unique_per_path(self):
        paths = [entry["category"] for entry in BASSPRO_CATEGORIES]
        self.assertEqual(len(paths), len(set(paths)))
        for entry in BASSPRO_CATEGORIES:
            self.assertTrue(entry["url"].startswith("https://www.basspro.com/"))
            self.assertEqual(entry["url"], "https://www.basspro.com" + "/" + entry["url_type"] + "/" + entry["slug"])
            self.assertTrue(entry["department"])

    def test_duplicate_urls_keep_every_navigation_path(self):
        # /l/life-jackets is linked from two departments; both stay addressable.
        slugs = [e["slug"] for e in BASSPRO_CATEGORIES if e["slug"] == "life-jackets"]
        self.assertGreater(len(slugs), 1)
        self.assertEqual(len(set(e["category"] for e in BASSPRO_CATEGORIES if e["slug"] == "life-jackets")), len(slugs))

    def test_resolve_by_slug(self):
        entry = self.spider.resolve_entry()
        self.assertEqual(entry["category"], "Fishing/Rod & Reel Combos")
        self.assertEqual(entry["url"], "https://www.basspro.com/l/rod-reel-combos")
        self.assertEqual(entry["category_id"], "3074457345616732396")

    def test_resolve_by_full_navigation_path(self):
        spider = BassproListingSpider(
            settings=self.settings, category="Fishing/Rod & Reel Combos/Baitcast Combos"
        )
        entry = spider.resolve_entry()
        self.assertEqual(entry["slug"], "baitcast-combos")
        self.assertEqual(entry["department"], "Fishing")
        self.assertEqual(entry["category_name"], "Rod & Reel Combos")
        self.assertEqual(entry["subcategory"], "Baitcast Combos")

    def test_resolve_by_url(self):
        for value in (
            "https://www.basspro.com/l/fishing-rods",
            "https://www.basspro.com/c/marine-electronics",
            "/l/fishing-rods",
        ):
            spider = BassproListingSpider(settings=self.settings, url=value)
            self.assertEqual(spider.resolve_entry()["slug"], value.rstrip("/").split("/")[-1])

    def test_duplicate_slugs_resolve_to_one_browse_url(self):
        # 119 slugs are cross-linked between departments but point at the same
        # browse URL, so the bare slug stays usable; the full path stays available
        # for callers that want a specific department label.
        entry = BassproListingSpider(
            settings=self.settings, category="trailer-accessories"
        ).resolve_entry()
        self.assertEqual(entry["url"], "https://www.basspro.com/l/trailer-accessories")
        qualified = BassproListingSpider(
            settings=self.settings, category="Outdoor Rec/Trailer Accessories"
        ).resolve_entry()
        self.assertEqual(qualified["department"], "Outdoor Rec")
        self.assertEqual(qualified["url"], entry["url"])

    def test_ambiguous_slug_with_different_urls_is_rejected(self):
        spider = BassproListingSpider(settings=self.settings, category="life-jackets")
        # Simulate a taxonomy regression: two paths, two different URLs.
        boat = spider.category_entry("Boating/Water Sports/Life Jackets")
        outdoor = spider.category_entry("Outdoor Rec/Water Sports/Life Jackets")
        boat, outdoor = dict(boat), dict(outdoor)
        boat["slug"] = "life-jackets"
        outdoor["slug"] = "life-jackets"
        outdoor["url"] = "https://www.basspro.com/l/life-jackets-alt"
        spider.categories = {
            "all": {
                "Boating/Water Sports/Life Jackets": boat,
                "Outdoor Rec/Water Sports/Life Jackets": outdoor,
            }
        }
        spider._category_cache = None  # rebuilt after the taxonomy mutation
        with self.assertRaises(ValueError) as ctx:
            spider.resolve_entry()
        self.assertIn("Ambiguous category", str(ctx.exception))

    def test_resolve_unknown_category_is_rejected(self):
        spider = BassproListingSpider(settings=self.settings, category="nope-nope")
        with self.assertRaises(ValueError) as ctx:
            spider.resolve_entry()
        self.assertIn("Unknown category", str(ctx.exception))

    def test_missing_category_argument_is_rejected(self):
        with self.assertRaises(ValueError):
            BassproListingSpider(settings=self.settings)

    def test_unsafe_slug_is_refused(self):
        with self.assertRaises(ValueError):
            BassproListingSpider.validate_slug('rod" OR @isgun==1')
        self.assertEqual(BassproListingSpider.validate_slug("rod-reel-combos"), "rod-reel-combos")

    # ----------------------------------------------------------------- routing

    def test_start_request_targets_the_category_page_through_the_proxy(self):
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, "https://www.basspro.com/l/rod-reel-combos")
        self.assertEqual(requests[0].callback, self.spider.parse_plp)
        self.assertEqual(requests[0].meta["proxy"], self.settings.get("PROXY"))

    def test_storefront_legs_are_proxied_but_the_coveo_search_is_direct(self):
        requests = list(self.spider.parse_plp(self._plp_response()))
        token_request = requests[0]
        self.assertEqual(token_request.url, BASSPRO_TOKEN_URL)
        self.assertEqual(token_request.meta["proxy"], self.settings.get("PROXY"))

        search_requests = list(self.spider.parse_token(self._token_response()))
        search = search_requests[0]
        self.assertIn(BASSPRO_COVEO_ORGANIZATION_ID, search.url)
        self.assertEqual(search.method, "POST")
        # The Coveo edge ignores the body of a proxied POST, so this leg must
        # not inherit the storefront leg's proxy.
        self.assertIsNone(search.meta.get("proxy"))
        self.assertTrue(search.headers["Authorization"].decode().startswith("Bearer "))
        self.assertEqual(search.meta["page"], 1)

    def test_downloader_middleware_is_disabled_so_routing_is_explicit(self):
        self.assertIsNone(
            self.spider.custom_settings["DOWNLOADER_MIDDLEWARES"][
                "common.middlewares.CommonDownloaderMiddleware"
            ]
        )

    # ----------------------------------------------------------------- request body

    def test_search_body_filters_by_slug_and_excludes_restricted_skus(self):
        body = self.spider.search_body(48, "rod-reel-combos")
        self.assertEqual(body["firstResult"], 48)
        self.assertEqual(body["numberOfResults"], 48)
        self.assertEqual(body["searchHub"], BASSPRO_COVEO_SEARCH_HUB)
        self.assertIn('@groupurlkeywords=="rod-reel-combos"', body["aq"])
        self.assertIn("@isgun==1", body["aq"])
        self.assertIn("fieldsToInclude", body)

    def test_include_restricted_drops_the_storefront_safety_query(self):
        spider = BassproListingSpider(
            settings=self.settings, category="rod-reel-combos", include_restricted="1"
        )
        self.assertEqual(spider.search_body(0, "rod-reel-combos")["aq"], '@groupurlkeywords=="rod-reel-combos"')

    def test_page_size_override(self):
        spider = BassproListingSpider(settings=self.settings, category="rod-reel-combos", page_size="24")
        self.assertEqual(spider.page_size, 24)
        self.assertEqual(spider.search_body(24, "x")["numberOfResults"], 24)

    # ----------------------------------------------------------------- parsing

    def _plp_response(self, html=None, status=200, spider=None):
        spider = spider or self.spider
        request = Request(
            "https://www.basspro.com/l/rod-reel-combos",
            meta={"entry": self.entry},
        )
        return self.response(request, html or self.plp_html, status=status)

    def _token_response(self):
        request = Request(BASSPRO_TOKEN_URL, meta={"slug": "rod-reel-combos", "entry": self.entry})
        return self.response(request, TOKEN_FIXTURE.read_text())

    def _search_response(self, body, page=1, spider=None):
        spider = spider or self.spider
        request = Request(f"https://platform.cloud.coveo.com/rest/search/v2?x=1", method="POST")
        request.meta.update(
            {
                "page": page,
                "slug": "rod-reel-combos",
                "entry": self.entry,
                "page_id": "3074457345616732396",
                "page_identifier": "Rod and Reel Combos",
                "store_id": "715838534",
                "breadcrumbs": ["Fishing", "Rod & Reel Combos"],
                "token": "fixture-token",
            }
        )
        return self.response(request, body)

    def test_parse_plp_reads_page_metadata_and_requests_the_token(self):
        meta = list(self.spider.parse_plp(self._plp_response()))[0].meta
        self.assertEqual(meta["slug"], "rod-reel-combos")
        self.assertEqual(meta["page_id"], "3074457345616732396")
        self.assertEqual(meta["page_identifier"], "Rod and Reel Combos")
        self.assertEqual(meta["store_id"], "715838534")
        self.assertEqual(meta["breadcrumbs"], ["Fishing", "Rod & Reel Combos"])
        # `srchattridentifier` is "_cat.<Coveo field>" on the storefront.
        self.assertIn("Subcategory", meta["facets"])
        self.assertIn("Brand", meta["facets"])

    def test_parse_plp_rejects_challenge_pages(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_plp(self._plp_response(CHALLENGE_FIXTURE.read_text())))
        self.assertIn("block/challenge page", ctx.exception.reason)

    def test_parse_plp_rejects_non_200(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_plp(self._plp_response(status=403)))
        self.assertIn("HTTP 403", ctx.exception.reason)

    def test_parse_plp_rejects_missing_next_data(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_plp(self._plp_response("<html><body>hello</body></html>")))
        self.assertIn("__NEXT_DATA__", ctx.exception.reason)

    def test_parse_plp_rejects_page_without_page_values(self):
        payload = json.dumps({"props": {"pageProps": {}}, "page": "/l/[pageName]"})
        html = f'<script id="__NEXT_DATA__" type="application/json">{payload}</script>'
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_plp(self._plp_response(html)))
        self.assertIn("pageValues is empty", ctx.exception.reason)

    def test_parse_plp_rejects_invalid_json(self):
        html = '<script id="__NEXT_DATA__" type="application/json">{oops}</script>'
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_plp(self._plp_response(html)))
        self.assertIn("not valid JSON", ctx.exception.reason)

    def test_parse_token_requires_a_token_field(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_token(self.response(Request(BASSPRO_TOKEN_URL), '{"error":"nope"}')))
        self.assertIn("no `token` field", ctx.exception.reason)

    def test_parse_token_rejects_non_200(self):
        response = self._token_response()
        response.status = 500
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_token(response))
        self.assertIn("HTTP 500", ctx.exception.reason)

    # ----------------------------------------------------------------- results

    def test_parse_search_maps_results_and_paginates(self):
        # page_size=3 makes the 3-result fixture a *full* page, so the spider must
        # keep paginating instead of treating it as the last page.
        spider = BassproListingSpider(
            settings=self.settings, category="rod-reel-combos", max_pages=3, page_size="3"
        )
        results = list(spider.parse_search(self._search_response(self.page1, spider=spider)))
        items = [r for r in results if isinstance(r, dict)]
        next_page = [r for r in results if isinstance(r, Request)]
        self.assertEqual(len(items), 3)
        self.assertEqual(len(next_page), 1)
        self.assertEqual(json.loads(next_page[0].body)["firstResult"], 3)

        first = items[0]
        self.assertEqual(first["category"], "Fishing/Rod & Reel Combos")
        self.assertEqual(first["department"], "Fishing")
        self.assertEqual(first["category_id"], "3074457345616732396")
        self.assertEqual(first["page_id"], "3074457345616732396")
        self.assertEqual(first["category_slug"], "rod-reel-combos")
        self.assertEqual(first["breadcrumb"], ["Fishing", "Rod & Reel Combos"])
        self.assertEqual(first["item_id"], "3472884")
        self.assertEqual(first["sku"], "3472884")
        self.assertEqual(first["title"], "Bass Pro Shops Megacast Baitcast Combo")
        self.assertEqual(first["brand"], "Bass Pro Shops")
        self.assertEqual(first["url"], "https://www.basspro.com/p/bass-pro-shops-megacast-baitcast-combo")
        self.assertTrue(first["image_url"].startswith("https://assets.basspro.com/"))
        self.assertEqual(first["price"], 69.99)
        self.assertIsNone(first["original_price"])
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["rating"], 3.6241)
        self.assertEqual(first["reviews_count"], 133)
        self.assertEqual(first["availability"], "InStock")
        self.assertEqual(first["quantity"], 624)
        self.assertEqual(first["gear_ratio"], "6.6:1")
        self.assertEqual(first["country_of_origin"], "CHINA")
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["total_count"], 478)
        self.assertEqual(first["source"], "basspro_coveo")
        self.assertIn("thecategories", first["raw"])

    def test_export_fields_match_the_item_dict(self):
        items = [
            r for r in self.spider.parse_search(self._search_response(self.page1))
            if isinstance(r, dict)
        ]
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_max_pages_stops_pagination(self):
        spider = BassproListingSpider(
            settings=self.settings, category="rod-reel-combos", max_pages=1, page_size="3"
        )
        results = list(spider.parse_search(self._search_response(self.page1, spider=spider)))
        self.assertEqual(len([r for r in results if isinstance(r, dict)]), 3)
        self.assertFalse([r for r in results if isinstance(r, Request)])

    def test_second_page_keeps_its_own_page_and_position(self):
        items = [
            r for r in self.spider.parse_search(self._search_response(self.page2, page=2))
            if isinstance(r, dict)
        ]
        self.assertEqual(len(items), 3)
        self.assertEqual({i["page"] for i in items}, {2})
        self.assertEqual([i["position"] for i in items], [1, 2, 3])

    def test_short_page_stops_pagination(self):
        results = list(
            self.spider.parse_search(
                self._search_response(LAST_PAGE_FIXTURE.read_text(), page=10)
            )
        )
        self.assertFalse([r for r in results if isinstance(r, Request)])
        self.assertEqual(len([r for r in results if isinstance(r, dict)]), 2)

    def test_empty_results_stop_pagination_without_items(self):
        body = json.dumps({"totalCount": 0, "results": []})
        results = list(self.spider.parse_search(self._search_response(body)))
        self.assertEqual(results, [])

    def test_duplicate_results_are_dropped(self):
        body = json.loads(self.page1)
        body["results"] = body["results"] + body["results"][:1]
        items = [
            r for r in self.spider.parse_search(self._search_response(json.dumps(body)))
            if isinstance(r, dict)
        ]
        self.assertEqual(len(items), 3)
        self.assertEqual(len({i["item_id"] for i in items}), 3)

    def test_coveo_error_payload_raises(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_search(self._search_response(ERROR_FIXTURE.read_text())))
        self.assertIn("Coveo error", ctx.exception.reason)

    def test_unexpected_response_shape_raises(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_search(self._search_response({"foo": "bar"})))
        self.assertIn("unexpected Coveo response shape", ctx.exception.reason)

    def test_non_json_response_raises(self):
        with self.assertRaises(CloseSpider) as ctx:
            list(self.spider.parse_search(self._search_response("<html>nope</html>")))
        self.assertIn("not JSON", ctx.exception.reason)

    def test_result_without_identifier_is_skipped(self):
        body = json.loads(self.page1)
        for key in ("sku", "product_catentry_id", "catentry_id"):
            body["results"][0]["raw"].pop(key)
        items = [
            r for r in self.spider.parse_search(self._search_response(json.dumps(body)))
            if isinstance(r, dict)
        ]
        self.assertEqual(len(items), 2)

    def test_markdown_price_mapping(self):
        body = json.loads(self.page1)
        raw = body["results"][0]["raw"]
        raw["listprice"] = "99.99"
        raw["maxsavings"] = "30.00"
        raw["percentsavings"] = "30"
        raw["isclearance"] = "1"
        raw["buyable"] = "0"
        items = [
            r for r in self.spider.parse_search(self._search_response(json.dumps(body)))
            if isinstance(r, dict)
        ]
        first = items[0]
        self.assertEqual(first["price"], 69.99)
        self.assertEqual(first["original_price"], 99.99)
        self.assertEqual(first["savings"], 30.0)
        self.assertEqual(first["discount_percent"], 30.0)
        self.assertTrue(first["is_clearance"])
        self.assertEqual(first["availability"], "OutOfStock")

    # ----------------------------------------------------------------- helpers

    def test_parse_number(self):
        self.assertEqual(parse_number("69.99"), 69.99)
        self.assertEqual(parse_number("1,234.50"), 1234.5)
        self.assertEqual(parse_number("$8-17 lbs."), 8.0)
        self.assertEqual(parse_number(12), 12.0)
        self.assertIsNone(parse_number(None))
        self.assertIsNone(parse_number(""))
        self.assertIsNone(parse_number("n/a"))
        self.assertIsNone(parse_number(True))

    def test_as_int(self):
        self.assertEqual(as_int("133.0"), 133)
        self.assertEqual(as_int("3"), 3)
        self.assertIsNone(as_int(None))

    def test_flag(self):
        self.assertTrue(flag("1"))
        self.assertTrue(flag(True))
        self.assertFalse(flag("0"))
        self.assertFalse(flag(None))
        self.assertFalse(flag(""))

    def test_first_image_prefers_the_plp_thumbnail(self):
        raw = {
            "thumbnail": "https://assets.basspro.com/a.json?$Prod_PLPThumb$",
            "fullimage": "https://assets.basspro.com/a.json",
        }
        self.assertIn("$Prod_PLPThumb$", first_image(raw))
        self.assertEqual(first_image({"fullimage": "https://x/y.json"}), "https://x/y.json")
        self.assertIsNone(first_image({}))


if __name__ == "__main__":
    unittest.main()