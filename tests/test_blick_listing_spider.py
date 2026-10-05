import json
import unittest
import urllib.parse as urlparse
from pathlib import Path

from scrapy.http import TextResponse

from common.spiders.blick_categories import (
    BLICK_CATEGORY_COUNTS,
    BLICK_CATEGORY_TREE,
    crawlable_categories,
    flatten_categories,
)
from common.spiders.blick_listing_spider import API_BASE, BlickListingSpider

ACRYLIC_CATEGORY = "paint-and-mediums/acrylic-paint"
ACRYLIC_URL = "https://www.dickblick.com/categories/painting/acrylic-paint/"
ACRYLIC_ENTRY_ID = "64h0nGCpZmASYWykoCaM4E"


def _query(response_or_request) -> dict:
    return urlparse.parse_qs(urlparse.urlparse(response_or_request.url).query)


def _load(name):
    return json.loads(Path(f"sample/{name}").read_text())


class BlickCategoriesTest(unittest.TestCase):
    def setUp(self):
        self.rows = flatten_categories()
        self.crawlable = crawlable_categories()

    def test_taxonomy_counts_match_the_capture(self):
        self.assertEqual(len(BLICK_CATEGORY_TREE), 17)
        self.assertEqual(len(self.crawlable), 899)
        self.assertEqual(BLICK_CATEGORY_COUNTS["category_urls"], 899)
        self.assertEqual(BLICK_CATEGORY_COUNTS["departments"], 17)

    def test_category_urls_are_unique(self):
        urls = [row["url"] for row in self.crawlable]
        self.assertEqual(len(urls), len(set(urls)))

    def test_every_crawlable_url_is_a_dickblick_category_page(self):
        for row in self.crawlable:
            self.assertTrue(row["url"].startswith("https://www.dickblick.com/categories/"), row)
            self.assertTrue(row["url"].endswith("/"), row)

    def test_category_slugs_are_unique_and_present(self):
        slugs = [row["category"] for row in self.rows]
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertIn(ACRYLIC_CATEGORY, slugs)

    def test_acrylic_paint_is_a_leaf_under_paint_and_mediums(self):
        row = next(r for r in self.crawlable if r["url"] == ACRYLIC_URL)
        self.assertEqual(row["category"], ACRYLIC_CATEGORY)
        self.assertEqual(row["name"], "Acrylic Paint")
        self.assertEqual(row["path"], "Paint and Mediums > Acrylic Paint")
        self.assertEqual(row["depth"], 2)

    def test_structural_group_nodes_have_no_url(self):
        structural = [row for row in self.rows if not row["url"]]
        self.assertEqual(len(structural), BLICK_CATEGORY_COUNTS["structural_group_nodes"])
        self.assertEqual(len(self.rows), 899 + len(structural))
        names = {row["name"] for row in structural}
        # Verified live: these are path segments only, not landing pages.
        self.assertIn("Acrylics", names)

    def test_cross_listed_urls_are_collapsed_to_one_node(self):
        # The CMS lists /categories/canvas/primers/ as both "Primers" and
        # "Primers and Gessoes"; exactly one node must own that URL.
        owners = [
            row for row in self.crawlable
            if row["url"] == "https://www.dickblick.com/categories/canvas/primers/"
        ]
        self.assertEqual(len(owners), 1)
        self.assertEqual(owners[0]["name"], "Primers and Gessoes")

    def test_tree_matches_the_captured_index_fixture(self):
        fixture = _load("blick-categories-next-data.json")
        self.assertEqual(fixture["uniqueNamedUrls"], 899)
        self.assertEqual(fixture["recordCount"], 2697)
        for record in fixture["records"]:
            url = "https://www.dickblick.com/" + record["url"].strip("/") + "/"
            self.assertIn(url, {row["url"] for row in self.crawlable}, url)


class BlickListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = BlickListingSpider(category=ACRYLIC_CATEGORY, max_pages=2)
        self.entry = next(
            entry for entry in self.spider.categories if entry["category"] == ACRYLIC_CATEGORY
        )
        self.next_data = _load("blick-acrylic-next-data.json")
        self.page0 = _load("blick-acrylic-api-page0.json")
        self.page1 = _load("blick-acrylic-api-page1.json")
        self.last_page = _load("blick-acrylic-api-lastpage.json")

    # ----------------------------------------------------------------- helpers

    def html_response(self, request, payload=None, status=200, body=None):
        if body is None:
            # The real page ships the hydration inside a __NEXT_DATA__ script tag.
            body = (
                '<html><body><script id="__NEXT_DATA__" type="application/json">'
                + json.dumps(payload if payload is not None else self.next_data)
                + "</script></body></html>"
            ).encode()
        return TextResponse(
            request.url, request=request, body=body, status=status, encoding="utf-8"
        )

    def api_response(self, request, payload=None, status=200, body=None):
        if body is None:
            body = json.dumps(payload if payload is not None else self.page0).encode()
        return TextResponse(
            request.url, request=request, body=body, status=status, encoding="utf-8"
        )

    def entry_request(self):
        return next(self.spider.start_requests())

    def api_request(self, page=0, entry=None):
        entry = entry or self.entry
        return self.spider._api_request(entry, ACRYLIC_ENTRY_ID, page=page)

    def _items(self, request, payload):
        return [
            out
            for out in self.spider.parse_api_page(self.api_response(request, payload))
            if isinstance(out, dict)
        ]

    # --------------------------------------------------------------- requests

    def test_starts_from_the_category_landing_page(self):
        request = self.entry_request()
        self.assertEqual(request.url, ACRYLIC_URL)
        self.assertEqual(request.callback, self.spider.parse_entry_id)

    def test_api_request_uses_the_first_party_collection_endpoint(self):
        request = self.api_request(page=1)
        self.assertTrue(request.url.startswith(f"{API_BASE}/{ACRYLIC_ENTRY_ID}?"))
        query = _query(request)
        self.assertEqual(query["pageNumber"], ["1"])
        self.assertEqual(query["pageSize"], ["30"])
        self.assertEqual(query["includeFacets"], ["false"])

    def test_api_request_sends_the_required_portal_header(self):
        request = self.api_request()
        self.assertEqual(request.headers["X-blick-portal"].decode(), "blick")
        self.assertEqual(request.headers["Accept"].decode().split(",")[0], "application/json")
        self.assertEqual(request.headers["Referer"].decode(), ACRYLIC_URL)
        self.assertEqual(request.headers["Origin"].decode(), "https://www.dickblick.com")

    def test_allowed_domains_cover_the_api_host(self):
        self.assertIn("api.dickblick.com", self.spider.allowed_domains)

    # ------------------------------------------------------------------ parse

    def test_entry_id_is_read_from_the_next_data_hydration(self):
        request = self.entry_request()
        outputs = list(self.spider.parse_entry_id(self.html_response(request)))
        self.assertEqual(len(outputs), 1)
        self.assertEqual(
            outputs[0].url.split("?")[0], f"{API_BASE}/{ACRYLIC_ENTRY_ID}"
        )
        # Page 1 of the crawl is API pageNumber=0 (zero-based API).
        self.assertEqual(_query(outputs[0])["pageNumber"], ["0"])

    def test_html_page_is_not_used_as_a_product_source(self):
        request = self.entry_request()
        outputs = list(self.spider.parse_entry_id(self.html_response(request)))
        self.assertFalse(
            [out for out in outputs if isinstance(out, dict)],
            "the category HTML must only yield the collection id, never items",
        )

    def test_page0_items_are_typed_from_the_api_payload(self):
        items = self._items(self.api_request(page=0), self.page0)
        self.assertEqual(len(items), len(self.page0["items"]))
        first = items[0]
        self.assertEqual(first["item_id"], "00711")
        self.assertEqual(first["title"], "Blickrylic Student Acrylic Paints and Sets")
        self.assertEqual(first["brand"], "Blick")
        self.assertEqual(first["url"], "https://www.dickblick.com/products/blickrylic-student-acrylics/")
        self.assertTrue(first["image_url"].startswith("https://cld-assets.dick-blick.com/"))
        self.assertEqual(first["price"], 7.45)
        self.assertEqual(first["price_max"], 183.4)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["rating"], 4.6)
        self.assertEqual(first["reviews_count"], 2140)
        self.assertEqual(first["sku_count"], 123)
        self.assertEqual(first["savings_text"], "SAVE up to 43%")
        self.assertIs(first["is_sale"], True)
        self.assertEqual(first["collection_id"], ACRYLIC_ENTRY_ID)
        self.assertEqual(first["source"], "blick_product_search_api")
        self.assertEqual(first["category"], ACRYLIC_CATEGORY)
        self.assertEqual(first["department"], "Paint and Mediums")
        self.assertEqual(first["category_name"], "Acrylic Paint")
        self.assertEqual(first["total_count"], 168)
        self.assertEqual(first["page"], 0)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["raw"], self.page0["items"][0])

    def test_api_page_numbering_is_zero_based(self):
        page0_items = self._items(self.api_request(page=0), self.page0)
        page1_items = self._items(self.api_request(page=1), self.page1)
        self.assertEqual(page0_items[0]["page"], 0)
        self.assertEqual(page1_items[0]["page"], 1)
        self.assertEqual(page0_items[0]["position"], 1)
        self.assertNotEqual(page0_items[0]["item_id"], page1_items[0]["item_id"])

    def test_pagination_follows_page_number_increment(self):
        request = self.api_request(page=0)
        outputs = [
            out
            for out in self.spider.parse_api_page(self.api_response(request, self.page0))
            if not isinstance(out, dict)
        ]
        self.assertEqual(len(outputs), 1)
        self.assertEqual(_query(outputs[0])["pageNumber"], ["1"])

    def test_pagination_stops_at_total_pages(self):
        spider = BlickListingSpider(category=ACRYLIC_CATEGORY, max_pages=99)
        entry = next(e for e in spider.categories if e["category"] == ACRYLIC_CATEGORY)
        spider._seen_items.update(
            {item["itemId"] for item in self.page0["items"] + self.page1["items"]}
        )
        # API pageNumber=5 is the last of totalPages=6, so page 6 must not be requested.
        request = spider._api_request(entry, ACRYLIC_ENTRY_ID, page=5)
        payload = dict(self.last_page, pageNumber=5, totalPages=6)
        outputs = [
            out
            for out in spider.parse_api_page(TextResponse(
                request.url, request=request, body=json.dumps(payload).encode(),
                status=200, encoding="utf-8"))
            if not isinstance(out, dict)
        ]
        self.assertEqual(outputs, [], "must not request page 7 of a 6-page collection")

    def test_pagination_stops_on_empty_page(self):
        spider = BlickListingSpider(category=ACRYLIC_CATEGORY, max_pages=99)
        entry = next(e for e in spider.categories if e["category"] == ACRYLIC_CATEGORY)
        request = spider._api_request(entry, ACRYLIC_ENTRY_ID, page=6)
        payload = dict(self.page1, items=[], pageNumber=6, totalPages=None)
        outputs = [
            out
            for out in spider.parse_api_page(TextResponse(
                request.url, request=request, body=json.dumps(payload).encode(),
                status=200, encoding="utf-8"))
            if not isinstance(out, dict)
        ]
        self.assertEqual(outputs, [])

    def test_pagination_respects_max_pages(self):
        spider = BlickListingSpider(category=ACRYLIC_CATEGORY, max_pages=1)
        entry = next(e for e in spider.categories if e["category"] == ACRYLIC_CATEGORY)
        spider._seen_items.update({item["itemId"] for item in self.page0["items"]})
        request = spider._api_request(entry, ACRYLIC_ENTRY_ID, page=0)
        outputs = [
            out
            for out in spider.parse_api_page(TextResponse(
                request.url, request=request, body=json.dumps(self.page0).encode(),
                status=200, encoding="utf-8"))
            if not isinstance(out, dict)
        ]
        self.assertEqual(outputs, [])

    def test_total_count_is_a_backstop_when_total_pages_is_missing(self):
        spider = BlickListingSpider(category=ACRYLIC_CATEGORY, max_pages=99)
        entry = next(e for e in spider.categories if e["category"] == ACRYLIC_CATEGORY)
        request = spider._api_request(entry, ACRYLIC_ENTRY_ID, page=5)
        payload = dict(self.last_page, totalPages=None, totalCount=168)
        spider._seen_items.update({item["itemId"] for item in self.last_page["items"]})
        outputs = [
            out
            for out in spider.parse_api_page(TextResponse(
                request.url, request=request, body=json.dumps(payload).encode(),
                status=200, encoding="utf-8"))
            if not isinstance(out, dict)
        ]
        # 6 * 30 = 180 >= 168 -> stop even without totalPages.
        self.assertEqual(outputs, [])

    def test_items_are_deduped_across_pages(self):
        # Emit page 0 first so its products are in the dedupe set.
        self._items(self.api_request(page=0), self.page0)
        request = self.api_request(page=1)
        # Replaying page 0's products on page 1 must not double-emit them.
        payload = dict(self.page1, items=self.page0["items"] + self.page1["items"])
        items = self._items(request, payload)
        self.assertEqual(len(items), 2, "only the not-yet-seen products may be emitted")
        self.assertEqual(items[0]["item_id"], self.page1["items"][0]["itemId"])

    def test_duplicate_item_within_a_page_is_dropped(self):
        request = self.api_request(page=0)
        payload = dict(self.page0, items=[self.page0["items"][0], self.page0["items"][0]])
        items = self._items(request, payload)
        self.assertEqual(len(items), 1)

    # ------------------------------------------------------------ fail loudly

    def test_missing_entry_id_raises(self):
        spider = BlickListingSpider(category=ACRYLIC_CATEGORY, max_pages=1)
        request = next(spider.start_requests())
        payload = {"props": {"pageProps": {"contentType": "department"}}}
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_entry_id(self.html_response(request, payload)))
        self.assertIn("entryId", str(ctx.exception))

    def test_category_page_without_next_data_raises(self):
        request = self.entry_request()
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_entry_id(self.html_response(request, body=b"<html></html>")))
        self.assertIn("__NEXT_DATA__", str(ctx.exception))

    def test_challenge_body_on_category_page_raises(self):
        request = self.entry_request()
        body = b"<html><head><title>Just a moment...</title></head><body></body></html>"
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_entry_id(self.html_response(request, body=body)))
        self.assertIn("challenge", str(ctx.exception).lower())

    def test_real_category_page_is_not_treated_as_a_challenge(self):
        """A live Blick PLP is ~370 KB and its feature-flag JSON contains the
        string "ff-checkout-captcha-enabled"; scanning the whole body would
        reject every real category page. On the live page that blob sits far
        past the <head>, so reproduce that layout here."""
        request = self.entry_request()
        flags = json.dumps({"ff-checkout-captcha-enabled": {"defaultvalue": False}})
        padding = "<!--" + ("x" * 20_000) + "-->"
        body = (
            "<html><head>" + padding + "</head><body>"
            '<script id="feature-flags" type="application/json">' + flags + "</script>"
            '<script id="__NEXT_DATA__" type="application/json">'
            + json.dumps(self.next_data)
            + "</script></body></html>"
        ).encode()
        outputs = list(self.spider.parse_entry_id(self.html_response(request, body=body)))
        self.assertEqual(len(outputs), 1)
        self.assertTrue(outputs[0].url.startswith(API_BASE))

    def test_challenge_body_on_api_raises(self):
        request = self.api_request()
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api_page(self.api_response(request, body=b"<html>Access Denied</html>")))
        self.assertIn("challenge", str(ctx.exception).lower())

    def test_api_http_error_raises(self):
        request = self.api_request()
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api_page(self.api_response(request, payload={}, status=503)))
        self.assertIn("503", str(ctx.exception))

    def test_api_payload_without_items_raises(self):
        request = self.api_request()
        payload = {"totalCount": 10, "totalPages": 1}
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api_page(self.api_response(request, payload)))
        self.assertIn("items", str(ctx.exception))

    def test_unknown_alias_string_payload_raises(self):
        # The API answers 200 with a bare JSON string for an unknown alias.
        request = self.api_request()
        body = json.dumps("Collection with external ID 'x' not found").encode()
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api_page(self.api_response(request, body=body)))
        self.assertIn("non-object", str(ctx.exception))

    def test_unknown_category_raises_with_examples(self):
        spider = BlickListingSpider(category="does-not-exist", max_pages=1)
        with self.assertRaises(ValueError) as ctx:
            list(spider.start_requests())
        self.assertIn("Available categories", str(ctx.exception))

    # ------------------------------------------------------------------ args

    def test_category_url_arg_resolves_a_bundled_category(self):
        spider = BlickListingSpider(category_url=ACRYLIC_URL, max_pages=1)
        self.assertEqual(next(spider.start_requests()).url, ACRYLIC_URL)

    def test_export_fields_are_ordered_and_complete(self):
        fields = BlickListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertEqual(fields[0], "category")
        self.assertEqual(fields[-1], "raw")
        for required in (
            "item_id", "title", "brand", "url", "image_url", "price", "price_max",
            "currency", "rating", "reviews_count", "sku_count", "savings_text",
            "page", "position", "total_count", "source_url", "source",
        ):
            self.assertIn(required, fields)
        item = self._items(self.api_request(page=0), self.page0)[0]
        self.assertEqual(set(item), set(fields), "every emitted key must be exported")


if __name__ == "__main__":
    unittest.main()
