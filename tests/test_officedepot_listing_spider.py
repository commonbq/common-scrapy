import json
import unittest
from pathlib import Path
from urllib.parse import urljoin

from scrapy.http import Request, TextResponse
from scrapy.settings import Settings

from common.spiders.officedepot_listing_spider import (
    CATEGORY_API_URL,
    SITE_BASE,
    OfficedepotListingSpider,
    _extract_js_object,
    _match_braces,
    _parse_price,
    _slugify,
)

HEADER_FIXTURE = Path("sample/officedepot-header.json")
CATEGORY_PAGE_FIXTURE = Path("sample/officedepot-category-page.html")


class OfficedepotListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.settings.set("PROXY", "http://scrapeops.country=us:secret@proxy.scrapeops.io:5353")
        self.spider = OfficedepotListingSpider(settings=self.settings, max_pages=2)

        self.header_json = HEADER_FIXTURE.read_text()
        self.category_page_html = CATEGORY_PAGE_FIXTURE.read_text()

    def response(self, request, body, status=200, url=None):
        if not isinstance(body, str):
            body = json.dumps(body)
        return TextResponse(
            url=url or request.url,
            request=request,
            body=body.encode("utf-8"),
            status=status,
            encoding="utf-8",
        )

    def _resolve_categories(self, category=None):
        spider = OfficedepotListingSpider(settings=self.settings, category=category, max_pages=2)
        request = Request(CATEGORY_API_URL)
        response = self.response(request, self.header_json)
        requests = list(spider.parse_categories_json(response))
        return spider, requests

    # ------------------------------------------------------------- category resolution

    def test_initial_request_fetches_categories_json(self):
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), 1)
        req = requests[0]
        self.assertEqual(req.url, CATEGORY_API_URL)
        self.assertEqual(req.callback, self.spider.parse_categories_json)
        self.assertIn("proxy", req.meta)

    def test_parse_categories_builds_browse_index_and_listing_requests(self):
        spider, requests = self._resolve_categories()

        # Only /b/ browse PLPs are crawled; /l/ editorial landing pages are skipped.
        self.assertEqual(len(spider._categories_to_resolve), 388)
        self.assertEqual(len([r for r in requests if r.callback == spider.parse_listing_page]), 388)

        self.assertEqual(spider._slug_index["furniture"]["url"], "/b/furniture/N-917")
        self.assertEqual(spider._slug_index["office-chairs"]["url"], "/b/office-chairs/N-593067")
        # Qualified alias disambiguates duplicate leaf names.
        self.assertEqual(
            spider._slug_index["furniture-office-chairs"]["url"], "/b/office-chairs/N-593067"
        )
        self.assertFalse(spider._category_resolution_in_progress)

    def test_duplicate_leaf_names_resolve_by_department_qualifier(self):
        spider, _ = self._resolve_categories()

        # "Sheet Protectors" exists under Office Supplies and School Supplies with
        # different nav ids; the plain slug keeps the first, the qualified alias
        # keeps each distinct URL.
        self.assertEqual(spider._slug_index["sheet-protectors"]["url"], "/b/sheet-protectors/N-2310")
        self.assertEqual(
            spider._slug_index["school-supplies-sheet-protectors"]["url"],
            "/b/sheet-protectors/N-1461717",
        )

    def test_category_arg_limits_resolution_to_one_entry(self):
        spider, requests = self._resolve_categories(category="office-chairs")
        self.assertEqual(len(spider._categories_to_resolve), 1)
        self.assertEqual(spider._categories_to_resolve[0]["name"], "Office Chairs")
        self.assertEqual(len(requests), 1)
        self.assertIn("/b/office-chairs/N-593067", requests[0].url)
        self.assertIn("page=1", requests[0].url)

    def test_unknown_category_yields_no_requests(self):
        spider = OfficedepotListingSpider(settings=self.settings, category="does-not-exist", max_pages=1)
        request = Request(CATEGORY_API_URL)
        response = self.response(request, self.header_json)
        requests = list(spider.parse_categories_json(response))
        self.assertEqual(requests, [])
        self.assertTrue(spider.available_categories())

    # ------------------------------------------------------------- product extraction

    def _product_response(self, spider=None, page=1, max_pages=2, url=None):
        spider = spider or self.spider
        entry = {
            "department": "Furniture",
            "sub_category": "",
            "name": "Furniture",
            "url": "/b/furniture/N-917",
        }
        default_url = urljoin(SITE_BASE, f"/b/furniture/N-917?page={page}")
        request = Request(
            url or default_url,
            meta={
                "page": page,
                "metadata": entry,
                "max_pages": max_pages,
            },
        )
        response = self.response(request, self.category_page_html, url=request.url)
        return list(spider.parse_listing_page(response))

    def test_parse_listing_page_extracts_products_and_paginates(self):
        results = self._product_response()
        # 3 products + 1 next-page request (total=4944 > 1 page of 3, max_pages=2)
        self.assertEqual(len(results), 4)

        first = results[0]
        self.assertEqual(first["item_id"], "9003237")
        self.assertEqual(first["item_number"], "9003237")
        self.assertEqual(first["department"], "Furniture")
        self.assertIsNone(first["sub_category"])
        self.assertEqual(first["category"], "Furniture")
        self.assertEqual(first["brand"], "Serta")
        self.assertIn("Serta", first["title"])
        self.assertEqual(
            first["url"],
            "https://www.officedepot.com/a/products/9003237/Serta-Smart-Layers-Brinkley-Ergonomic-Bonded/",
        )
        self.assertTrue(first["image_url"].startswith("https://media.officedepot.com/"))
        self.assertEqual(first["price"], 299.99)
        self.assertEqual(first["original_price"], 299.99)
        self.assertEqual(first["list_price"], 586.81)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["availability"], "InStock")
        self.assertEqual(first["rating"], 4.5169)
        self.assertEqual(first["reviews_count"], 178)
        self.assertEqual(first["category_id"], "593061")
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["category_url"], urljoin(SITE_BASE, "/b/furniture/N-917?page=1"))
        self.assertEqual(first["breadcrumbs"], ["Home", "Furniture"])
        self.assertEqual(first["source"], "officedepot_bootstrap")
        self.assertIn("raw", first)

        # HTML entity in the source shortDescription must be decoded.
        third = results[2]
        self.assertEqual(third["item_id"], "9181888")
        self.assertIn("\u201d", third["title"])
        self.assertNotIn("&rdquo;", third["title"])
        self.assertEqual(third["availability"], "OutOfStock")

        # Last element is the next-page request.
        next_page = results[-1]
        self.assertEqual(next_page.callback, self.spider.parse_listing_page)
        self.assertEqual(next_page.meta["page"], 2)
        self.assertIn("page=2", next_page.url)

    def test_undefined_token_is_tolerated(self):
        # The live page embeds bare `undefined` tokens (invalid JSON); the spider
        # rewrites them to null rather than failing the page.
        results = self._product_response()
        self.assertEqual(len(results), 4)
        self.assertIsNone(results[0]["raw"]["swatches"])

    def test_max_pages_stops_pagination(self):
        spider = OfficedepotListingSpider(settings=self.settings, max_pages=1)
        results = self._product_response(spider=spider, max_pages=1)
        self.assertEqual(len(results), 3)
        self.assertFalse(any(isinstance(r, Request) for r in results))

    def test_deduplication_across_pages(self):
        # Re-parsing the same page must not re-emit already-seen ids.
        first_pass = self._product_response()
        self.assertEqual(len(first_pass), 4)
        second_pass = self._product_response()
        # No new items on a repeat parse (dedup), only the pagination request.
        self.assertEqual([r for r in second_pass if isinstance(r, dict)], [])

    # ------------------------------------------------------------- helpers

    def test_match_braces_basic(self):
        text = 'prefix {key: "value", nested: {a:1}} suffix'
        start = text.find("{")
        end = _match_braces(text, start)
        self.assertEqual(text[start:end + 1], '{key: "value", nested: {a:1}}')

    def test_match_braces_ignores_braces_in_strings(self):
        text = 'pre {a:1, b: undefined, c: "str with } brace", d:{}} post'
        start = text.find("{")
        end = _match_braces(text, start)
        self.assertEqual(text[start:end + 1], '{a:1, b: undefined, c: "str with } brace", d:{}}')

    def test_match_braces_handles_escaped_quote(self):
        text = 'pre {a:"foo\\"bar}", b: {c:1}} post'
        start = text.find("{")
        end = _match_braces(text, start)
        self.assertEqual(text[start:end + 1], '{a:"foo\\"bar}", b: {c:1}}')

    def test_match_braces_unmatched_returns_minus_one(self):
        text = "prefix {key: value, nested: {a:1} suffix"
        start = text.find("{")
        self.assertEqual(_match_braces(text, start), -1)

    def test_extract_js_object(self):
        blob = 'x = 1; window.STATE = {"a": {"b": 2}}; y = 2;'
        self.assertEqual(
            _extract_js_object(blob, "window.STATE"), '{"a": {"b": 2}}'
        )
        self.assertIsNone(_extract_js_object(blob, "window.MISSING"))

    def test_parse_price(self):
        self.assertEqual(_parse_price("$1,234.50"), 1234.50)
        self.assertIsNone(_parse_price(None))
        self.assertIsNone(_parse_price(""))

    def test_slugify(self):
        self.assertEqual(_slugify("Chairs & Seating"), "chairs-seating")


if __name__ == "__main__":
    unittest.main()
