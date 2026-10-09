import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, TextResponse

from common.spiders.ikea_listing_spider import IkeaListingSpider


class IkeaListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = IkeaListingSpider(category="st004", max_pages=2)
        capture = json.loads(Path("sample/ikea-sik-sample.json").read_text())
        self.product = capture["requests"][0]["response"]["first_item"]

    def response(self, request, *, start=0, end=24, total=147):
        payload = {
            "component": "PRIMARY_AREA",
            "items": [self.product, {"type": "OFFERS"}],
            "metadata_window": {
                "start": start,
                "end": end,
                "max": total,
                "itemsPerType": {"PRODUCT": total},
            },
        }
        return TextResponse(
            request.url,
            request=request,
            body=json.dumps(payload).encode(),
            encoding="utf-8",
        )

    def test_maps_product_and_requests_second_window(self):
        first = next(self.spider.start_requests())
        self.assertEqual(json.loads(first.body)["components"][0]["window"], {"size": 24, "offset": 0})
        outputs = list(self.spider.parse(self.response(first)))
        item, second = outputs
        self.assertEqual(item["item_id"], "60561248")
        self.assertEqual(item["title"], "STORKLINTA")
        self.assertEqual(item["product_type"], "6-drawer dresser")
        self.assertEqual(item["price"], 249.99)
        self.assertEqual(item["rating"], 3.9)
        self.assertEqual(item["reviews_count"], 319)
        self.assertEqual(item["raw"], self.product["product"])
        self.assertEqual(json.loads(second.body)["components"][0]["window"], {"size": 24, "offset": 24})

    def test_exports_api_derived_enrichment_fields(self):
        first = next(self.spider.start_requests())
        item = list(self.spider.parse(self.response(first)))[0]
        raw = self.product["product"]
        # Each new field is read straight from the API payload, not invented.
        self.assertEqual(item["item_no_global"], raw["itemNoGlobal"])
        self.assertEqual(item["product_class"], raw["filterClass"])
        self.assertEqual(item["department"], raw["categoryPath"][0]["name"])
        self.assertEqual(
            item["category_path"], [entry["name"] for entry in raw["categoryPath"]]
        )
        self.assertEqual(
            item["business_area"], raw["businessStructure"]["productAreaName"]
        )
        self.assertEqual(item["product_type_tag"], raw["optimizelyAttributes"]["PRODUCT_TYPE"])
        self.assertEqual(item["variant_count"], raw["gprDescription"]["numberOfVariants"])
        self.assertEqual(item["colors"], [c["name"] for c in raw["colors"]])
        self.assertEqual(item["image_alt"], raw["mainImageAlt"])
        self.assertEqual(item["quick_facts"], [f["name"] for f in raw["quickFacts"]])

    def test_enrichment_fields_tolerate_missing_optional_keys(self):
        first = next(self.spider.start_requests())
        payload = {
            "component": "PRIMARY_AREA",
            "items": [{"type": "PRODUCT", "product": {"itemNo": "1", "name": "Sparse"}}],
            "metadata": {"start": 0, "end": 24, "max": 1, "itemsPerType": {"PRODUCT": 1}},
        }
        item = list(self.spider.parse(self.response_from(first, payload)))[0]
        self.assertIsNone(item["department"])
        self.assertIsNone(item["category_path"])
        self.assertIsNone(item["business_area"])
        self.assertIsNone(item["variant_count"])
        self.assertIsNone(item["quick_facts"])
        self.assertEqual(item["colors"], [])
        self.assertEqual(item["item_id"], "1")

    def test_accepts_url_only_input(self):
        spider = IkeaListingSpider(url="https://www.ikea.com/us/en/cat/dressers-chests-of-drawers-st004/")
        request = next(spider.start_requests())
        self.assertEqual(request.meta["category_id"], "st004")
        with self.assertRaises(ValueError):
            next(IkeaListingSpider().start_requests())

    def test_deduplicates_products_between_pages(self):
        first = next(self.spider.start_requests())
        list(self.spider.parse(self.response(first)))
        second = self.spider._api_request("st004", first.meta["category_url"], page=2)
        self.assertEqual(list(self.spider.parse(self.response(second, start=24, end=48))), [])

    def test_inventory_has_unique_urls(self):
        urls = [entry["url"] for entry in self.spider.iter_categories()]
        self.assertEqual(len(urls), len(set(urls)))
        # Exact count from the captured inventory, not a loose lower bound: the
        # issue requires the complete concrete inventory.
        self.assertEqual(len(urls), 221)

    def test_inventory_entries_pass_schema_validation(self):
        # require_category_arg=False makes BaseListingSpider skip its
        # `_validate_categories_schema_if_needed` check, so the spider validates
        # the inventory itself. Every entry must still be a well-formed dict.
        for entry in self.spider.iter_categories():
            self.assertIsInstance(entry["category"], str)
            self.assertTrue(entry["category"])
            self.assertIsInstance(entry["url"], str)
            self.assertTrue(entry["url"])
            # The category token has to be recoverable from the url, since that
            # is what resolve_target_url() feeds to the SIK request.
            self.assertEqual(
                IkeaListingSpider._category_id(entry["url"]), entry["category"]
            )
        # The default construction path runs the same validation.
        self.assertEqual(
            len(list(IkeaListingSpider(category="st004").iter_categories())), 221
        )

    def test_malformed_inventory_is_rejected(self):
        # A bad entry must fail at construction, not later as a confusing
        # "Unknown category" error at crawl time.
        with self.assertRaisesRegex(ValueError, "missing string 'category'"):
            self._spider_with_inventory(
                {"all": {"": {"url": "https://www.ikea.com/us/en/cat/x-st999/"}}}
            )
        with self.assertRaisesRegex(ValueError, "does not match the token"):
            self._spider_with_inventory(
                {
                    "all": {
                        "st004": {
                            "url": "https://www.ikea.com/us/en/cat/other-st001/"
                        }
                    }
                }
            )
        with self.assertRaisesRegex(ValueError, "'url' must be a non-empty string"):
            self._spider_with_inventory({"all": {"st004": {"url": ""}}})
        with self.assertRaisesRegex(ValueError, "missing string 'url'"):
            self._spider_with_inventory({"all": {"st004": {}}})

    @staticmethod
    def _spider_with_inventory(categories):
        class _Spider(IkeaListingSpider):
            pass

        _Spider.categories = categories
        return _Spider(category="st004")

    def test_unknown_mode_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown -a mode"):
            IkeaListingSpider(category="st004", mode="jsonld")

    def test_html_fallback_parses_server_rendered_cards(self):
        # Reduced capture of the live st004 PLP (2026-10-02 UTC): the
        # `.js-product-list[data-category]` state plus the first two of the 24
        # server-rendered `.plp-fragment-wrapper` cards.
        spider = IkeaListingSpider(category="st004", max_pages=2, mode="html")
        request = next(spider.start_requests())
        self.assertEqual(request.url, spider.resolve_target_url())
        self.assertEqual(request.callback.__func__, IkeaListingSpider.parse_html)
        items = list(spider.parse_html(self.html_response(request)))
        self.assertEqual(len(items), 2)
        first = items[0]
        self.assertEqual(first["item_id"], "60561248")
        self.assertEqual(first["title"], "STORKLINTA")
        self.assertEqual(first["product_type"], "6-drawer dresser")
        self.assertEqual(first["design"], "white/anchor/unlock function")
        self.assertEqual(first["dimensions"], '55 1/8x18 7/8x29 1/2 "')
        self.assertEqual(first["price"], 249.99)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["rating"], 3.9)
        self.assertEqual(first["reviews_count"], 320)
        self.assertEqual(first["badge"], "Best seller")
        self.assertEqual(first["availability"], "InStock")
        self.assertEqual(first["source"], "ikea_plp_html")
        self.assertEqual(first["page"], 1)
        self.assertTrue(first["url"].endswith("-60561248/"))
        self.assertTrue(first["image_url"].endswith("_s5.jpg?f=xxs"))
        self.assertEqual(len(first["image_urls"]), 2)
        self.assertIn("Modern white chest of drawers", first["image_alt"])
        # Every exported item carries `raw` in both modes.
        self.assertTrue(all("raw" in item and item["raw"] for item in items))
        self.assertEqual(first["raw"]["itemNo"], "60561248")
        # The HTML path is page 1 only: it must not chain a second request.
        self.assertNotIn("data-category", {k for k in first["raw"]})

    def test_html_fallback_hub_url_is_rejected_clearly(self):
        # Issue #114: a hub-only URL must be rejected, not silently empty.
        spider = IkeaListingSpider(
            url="https://www.ikea.com/us/en/cat/storage-organization-st001/", mode="html"
        )
        request = next(spider.start_requests())
        body = b"<html><body><div class='plp-main-container'></div></body></html>"
        response = HtmlResponse(
            request.url, request=request, body=body, encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "category hub"):
            list(spider.parse_html(response))

    def test_html_fallback_requires_product_cards(self):
        spider = IkeaListingSpider(category="st004", mode="html")
        request = next(spider.start_requests())
        body = b"<html><body><div class='js-product-list' data-category='{}'></div></body></html>"
        response = HtmlResponse(
            request.url, request=request, body=body, encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "plp-fragment-wrapper"):
            list(spider.parse_html(response))

    def test_api_mode_does_not_request_the_html_page(self):
        # mode=html is opt-in; the default run must hit SIK only.
        first = next(self.spider.start_requests())
        self.assertIn("sik.search.blue.cdtapps.com", first.url)
        self.assertEqual(first.callback.__func__, IkeaListingSpider.parse)

    def test_sik_version_is_configurable(self):
        self.assertIn("v=20250507", self.spider.api_url)
        overridden = IkeaListingSpider(category="st004", sik_version="20990101")
        self.assertIn("v=20990101", overridden.api_url)
        self.assertTrue(overridden.api_url.startswith(IkeaListingSpider.SIK_BASE_URL))

    def test_bad_sik_version_error_suggests_override(self):
        spider = IkeaListingSpider(category="st004", sik_version="99999999")
        request = next(spider.start_requests())
        # Verified live: the API answers an unknown version with
        # {"status":400,...,"detail":"Invalid API version"} and no PRIMARY_AREA.
        body = json.dumps(
            {"status": 400, "title": "Bad Request", "detail": "Invalid API version"}
        ).encode()
        response = TextResponse(request.url, request=request, body=body, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "sik_version=<current value>"):
            list(spider.parse(response))

    def test_live_results_wrapped_shape_is_parsed(self):
        # Verified live 2026-10-01: the storefront returns
        # {"usergroup","results","testActivationTriggers","metadata"} where
        # results[0] is the PRIMARY_AREA and carries the window under `metadata`.
        payload = {
            "usergroup": "USERGROUP",
            "results": [
                {
                    "component": "PRIMARY_AREA",
                    "viewMode": "GRID",
                    "items": [self.product, {"type": "NEW_PRODUCT"}],
                    "metadata": {
                        "start": 0,
                        "end": 24,
                        "max": 150,
                        "itemsPerType": {"PRODUCT": 148, "NEW_PRODUCT": 1},
                    },
                }
            ],
            "metadata": {"categoryPage": {"categoryKey": "st004"}},
        }
        request = next(self.spider.start_requests())
        outputs = list(self.spider.parse(self.response_from(request, payload)))
        item, second = outputs
        self.assertEqual(item["item_id"], "60561248")
        # itemsPerType.PRODUCT (148) > end (24), so page 2 must be requested.
        self.assertEqual(json.loads(second.body)["components"][0]["window"]["offset"], 24)

    def test_missing_primary_area_fails_loudly(self):
        request = next(self.spider.start_requests())
        response = TextResponse(
            request.url, request=request, body=b'{"results": []}', encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "missing PRIMARY_AREA"):
            list(self.spider.parse(response))

    def test_product_without_identifier_fails_loudly(self):
        request = next(self.spider.start_requests())
        payload = {
            "component": "PRIMARY_AREA",
            "items": [{"type": "PRODUCT", "product": {"name": "No id product"}}],
            "metadata_window": {"start": 0, "end": 24, "max": 147, "itemsPerType": {"PRODUCT": 147}},
        }
        response = TextResponse(
            request.url, request=request, body=json.dumps(payload).encode(), encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "missing itemNo/id"):
            list(self.spider.parse(response))

    def test_captured_top_level_shape_is_parsed(self):
        # The bundled capture is a reduced single PRIMARY_AREA object with `items`
        # and `metadata_window`; it has no `results` array.
        capture = json.loads(Path("sample/ikea-sik-sample.json").read_text())
        captured = capture["requests"][0]["response"]
        payload = {
            "component": captured["component"],
            "items": [captured["first_item"], {"type": "OFFERS"}],
            "metadata_window": captured["metadata_window"],
        }
        request = next(self.spider.start_requests())
        outputs = list(self.spider.parse(self.response_from(request, payload)))
        item, second = outputs
        self.assertEqual(item["item_id"], "60561248")
        self.assertEqual(item["title"], "STORKLINTA")
        # metadata_window.itemsPerType.PRODUCT = 147 > end (24), so page 2 follows.
        self.assertEqual(json.loads(second.body)["components"][0]["window"]["offset"], 24)

    def response_from(self, request, payload):
        return TextResponse(
            request.url, request=request, body=json.dumps(payload).encode(), encoding="utf-8"
        )

    def html_response(self, request, name="ikea-plp-sample.html"):
        return HtmlResponse(
            request.url,
            request=request,
            body=Path("sample", name).read_bytes(),
            encoding="utf-8",
        )
