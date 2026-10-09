from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import Mock

from scrapy.http import Request, TextResponse

from common.spiders.nike_categories import NIKE_CATEGORIES
from common.spiders.nike_listing_spider import NikeListingSpider, category_slug

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample"


def make_response(
    url: str,
    body: str | bytes,
    *,
    status: int = 200,
    content_type: str = "text/html",
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


def wall_html(payload: dict) -> str:
    """Wrap a Wall object in the __NEXT_DATA__ script a real PLP carries."""
    return (
        '<!doctype html><html><body><script id="__NEXT_DATA__" '
        'type="application/json">' + json.dumps({"props": {"pageProps": {"initialState": {"Wall": payload}}}}) + "</script></body></html>"
    )


class NikeListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = NikeListingSpider(category="mens-shoes-nik1zy7ok", max_pages=3)
        self.fixture_html_raw = (SAMPLE_DIR / "nike-listing-next-data.html").read_text()
        self.fixture_api = json.loads((SAMPLE_DIR / "nike-product-wall-page.json").read_text())
        # Extract the Wall content from the raw fixture HTML once
        match = self.spider.NEXT_DATA_RE.search(self.fixture_html_raw)
        self.fixture_wall_content = json.loads(match.group(1))["props"]["pageProps"]["initialState"]["Wall"]

    def listing_response(self, page: int = 1, category_url: str = "https://www.nike.com/w/mens-shoes-nik1zy7ok", next_path: str | None = None):
        wall_payload = self.fixture_wall_content.copy()
        if next_path is not None:
            wall_payload["pageData"]["next"] = next_path
        else: # ensure next is empty for single page test by default if not overridden
             if "pageData" in wall_payload and "next" in wall_payload["pageData"]:
                wall_payload["pageData"]["next"] = self.fixture_wall_content["pageData"].get("next","")

        return make_response(
            category_url,
            wall_html(wall_payload),
            meta={
                "page": page,
                "category_url": category_url,
                "category": "mens-shoes-nik1zy7ok",
            },
        )

    def api_response(self, page: int = 2, payload: dict | None = None, proxy_user: str | None = None):
        response_payload = payload if payload is not None else self.fixture_api
        return make_response(
            "https://api.nike.com/discover/product_wall/v1",
            json.dumps(response_payload),
            content_type="application/json",
            meta={
                "page": page,
                "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok",
                "category": "mens-shoes-nik1zy7ok",
            },
        )

    # ------------------------------------------------------------- inventory

    def test_categories_are_unique_and_cover_the_inventory(self):
        names = [entry["category"] for entry in self.spider.iter_categories()]
        self.assertEqual(len(names), len(set(names)))

        expected = {
            url
            for groups in NIKE_CATEGORIES.values()
            for subcategories in groups.values()
            for url in subcategories.values()
        }
        self.assertEqual({entry["url"] for entry in self.spider.iter_categories()}, expected)

    def test_duplicate_nav_names_resolve_to_one_entry(self):
        # "Shoes"/"All Shoes" and "New & Featured"/"New Arrivals" are the same page.
        urls = [entry["url"] for entry in self.spider.iter_categories()]
        self.assertEqual(len(urls), len(set(urls)))
        shoes = [e for e in self.spider.iter_categories() if e["category"] == "mens-shoes-nik1zy7ok"]
        self.assertEqual(len(shoes), 1)
        self.assertEqual(shoes[0]["name"], "Shoes")

    def test_category_slug_drops_the_w_prefix_and_normalizes(self):
        self.assertEqual(
            category_slug("https://www.nike.com/w/mens-shoes-nik1zy7ok"),
            "mens-shoes-nik1zy7ok",
        )
        self.assertEqual(
            category_slug("https://www.nike.com/w/womens-shoes-5e1x6zy7ok"),
            "womens-shoes-5e1x6zy7ok",
        )

    def test_inventory_preserves_department_and_group_hierarchy(self):
        entry = self.spider.category_entry("mens-shoes-nik1zy7ok")
        self.assertEqual(entry["department"], "Men")
        self.assertEqual(entry["group"], "Shoes")

    # ------------------------------------------------------- hydration parse

    def test_parse_listing_emits_items_from_next_data(self):
        results = list(self.spider.parse_listing(self.listing_response()))
        items = [r for r in results if isinstance(r, dict)]
        requests = [r for r in results if isinstance(r, Request)]

        self.assertEqual(len(items), 4)
        first = items[0]
        self.assertEqual(first["item_id"], "IX3952-600")
        self.assertEqual(first["title"], "Nike Moon Shoe OG")
        self.assertEqual(first["subtitle"], "Men's Shoes")
        self.assertEqual(first["price"], 105)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["color"], "Red")
        self.assertEqual(first["color_hex"], "B40033")
        self.assertEqual(first["product_type"], "FOOTWEAR")
        self.assertEqual(first["category"], "mens-shoes-nik1zy7ok")
        self.assertEqual(first["department"], "Men")
        self.assertEqual(first["group"], "Shoes")
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["source"], "nike_next_data")
        self.assertIn("IX3952-600", first["url"])
        self.assertTrue(first["image_url"].startswith("https://static.nike.com/"))
        self.assertTrue(first["raw"])
        self.assertEqual(len(requests), 1)
        self.assertTrue(requests[0].url.startswith("https://api.nike.com/discover/product_wall/v1/"))

    def test_every_item_carries_every_export_field(self):
        results = list(self.spider.parse_listing(self.listing_response()))
        items = [r for r in results if isinstance(r, dict)]
        for item in items:
            for field in self.spider.custom_settings["FEED_EXPORT_FIELDS"]:
                self.assertIn(field, item, field)

    def test_multi_color_group_expands_to_one_item_per_product_code(self):
        payload = {
            "productGroupings": [
                {
                    "products": [
                        {"productCode": "CW2289-111", "copy": {"title": "AF1 Mid '07"}, "prices": {"currentPrice": 125, "currency": "USD"}},
                        {"productCode": "CW2289-170", "copy": {"title": "AF1 Mid '07"}, "prices": {"currentPrice": 125, "currency": "USD"}},
                    ]
                }
            ],
            "pageData": {"next": "", "totalPages": 1, "totalResources": 2},
        }
        items = list(self.spider.parse_listing(make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            wall_html(payload),
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )))
        self.assertEqual([i["item_id"] for i in items if isinstance(i, dict)], ["CW2289-111", "CW2289-170"])

    def test_missing_next_data_raises(self):
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            "<html><body>no hydration here</body></html>",
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_listing(response))
        self.assertIn("__NEXT_DATA__", str(ctx.exception))

    def test_missing_wall_state_raises(self):
        html = '<script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{}}}</script>'
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            html,
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_listing(response))
        self.assertIn("Wall", str(ctx.exception))

    def test_malformed_next_data_json_raises(self):
        html = '<script id="__NEXT_DATA__" type="application/json">{not json</script>'
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            html,
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_listing(response))
        self.assertIn("malformed", str(ctx.exception))

    def test_wall_without_product_groupings_raises(self):
        html = wall_html({"pageData": {"next": ""}})
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            html,
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_listing(response))
        self.assertIn("productGroupings", str(ctx.exception))

    def test_product_without_product_code_raises(self):
        html = wall_html({"productGroupings": [{"products": [{"copy": {"title": "x"}}]}]})
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            html,
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_listing(response))
        self.assertIn("productCode", str(ctx.exception))

    def test_single_page_category_schedules_no_api_request(self):
        # Use a listing_response that has no next_path
        results = list(self.spider.parse_listing(self.listing_response(next_path="")))
        items = [r for r in results if isinstance(r, dict)]
        requests = [r for r in results if isinstance(r, Request)]

        self.assertEqual(len(items), 4)  # Expect items from the fixture
        self.assertEqual(len(requests), 0)

    def test_no_next_page_in_page_data_stops_after_page_one(self):
        payload = {
            "productGroupings": [{"products": [{"productCode": "AA0001-100"}]}],
            "pageData": {"next": "", "totalPages": 1, "totalResources": 1},
        }
        out = list(self.spider.parse_listing(make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            wall_html(payload),
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )))
        self.assertEqual(len([r for r in out if isinstance(r, dict)]), 1)
        self.assertEqual(len([r for r in out if isinstance(r, Request)]), 0)

    # ------------------------------------------------------------ API leg

    def test_parse_api_emits_items_and_follows_pages_next(self):
        out = list(self.spider.parse_api(self.api_response()))
        items = [r for r in out if isinstance(r, dict)]
        requests = [r for r in out if isinstance(r, Request)]
        self.assertEqual(len(items), 3) # Fixture has 3 products
        self.assertEqual(len(requests), 1)
        self.assertEqual(items[0]["source"], "nike_product_wall_api")
        self.assertEqual(items[0]["page"], 2)
        self.assertTrue(requests[0].url.startswith("https://api.nike.com/discover/product_wall/v1/"))

    def test_api_request_sends_the_required_caller_header(self):
        spider = NikeListingSpider(category="mens-shoes-nik1zy7ok", max_pages=3)
        # Mock the proxy to return a value that doesn't have the username quoted
        spider.settings = Mock()
        spider.settings.get.return_value = "http://scrapeops.country=us:***@proxy.scrapeops.io:5353"
        request = spider._api_request(
            "/discover/product_wall/v1/x",
            page=2,
            category_url="https://www.nike.com/w/mens-shoes-nik1zy7ok",
            category="mens-shoes-nik1zy7ok",
        )
        self.assertEqual(request.headers[b"nike-api-caller-id"], b"nike:dotcom:browse:wall.client:2.0")

    def test_last_api_page_stops(self):
        payload = {
            "productGroupings": [{"products": [{"productCode": "ZZ0001-100"}]}],
            "pages": {"next": "", "prev": ""},
        }
        out = list(self.spider.parse_api(self.api_response(page=9, payload=payload)))
        self.assertEqual(len([r for r in out if isinstance(r, dict)]), 1)
        self.assertEqual(len([r for r in out if isinstance(r, Request)]), 0)

    def test_max_pages_is_honored(self):
        spider = NikeListingSpider(category="mens-shoes-nik1zy7ok", max_pages=2)
        # page 2 is the API leg, so no page-3 request may be scheduled.
        out = list(spider.parse_api(self.api_response(page=2)))
        self.assertEqual(len([r for r in out if isinstance(r, dict)]), 3)
        self.assertEqual(len([r for r in out if isinstance(r, Request)]), 0)

    def test_malformed_api_json_raises(self):
        response = make_response(
            "https://api.nike.com/discover/product_wall/v1",
            "{not json",
            content_type="application/json",
            meta={"page": 2, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api(response))
        self.assertIn("non-JSON", str(ctx.exception))

    def test_api_missing_product_groupings_raises(self):
        payload = {"pages": {"next": ""}}
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api(self.api_response(payload=payload)))
        self.assertIn("productGroupings", str(ctx.exception))

    def test_stripped_caller_id_error_body_raises_instead_of_silently_ending(self):
        # Nike answers HTTP 200 with an errors array, so a status check alone
        # would read this as a valid empty last page.
        payload = {
            "errors": [{"code": "NIKE_API_CALLER_ID_HEADER_NOT_PRESENT", "message": "Request header nike-api-caller-id must be present"}],
            "productGroupings": [],
        }
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api(self.api_response(payload=payload)))
        self.assertIn("NIKE_API_CALLER_ID_HEADER_NOT_PRESENT", str(ctx.exception))

    def test_http_error_status_raises(self):
        response = make_response(
            "https://api.nike.com/discover/product_wall/v1",
            "forbidden",
            status=403,
            content_type="application/json",
            meta={"page": 2, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_api(response))
        self.assertIn("403", str(ctx.exception))

    def test_challenge_body_is_rejected(self):
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            "<html><body>Access Denied</body></html>",
            content_type="text/plain",
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_listing(response))
        self.assertIn("access-denied", str(ctx.exception))

    # ------------------------------------------------------------ dedupe

    def test_repeated_product_code_is_emitted_once(self):
        payload = {
            "productGroupings": [
                {"products": [{"productCode": "AA0001-100"}, {"productCode": "AA0001-100"}]},
                {"products": [{"productCode": "AA0001-100"}]},
            ],
            "pageData": {"next": ""},
        }
        response = make_response(
            "https://www.nike.com/w/mens-shoes-nik1zy7ok",
            wall_html(payload),
            meta={"page": 1, "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok", "category": "mens-shoes-nik1zy7ok"},
        )
        items = list(self.spider.parse_listing(response))
        self.assertEqual(len([i for i in items if isinstance(i, dict)]), 1)
        self.assertEqual([i["item_id"] for i in items if isinstance(i, dict)], ["AA0001-100"])

    # ------------------------------------------------------ price mapping

    def test_discounted_item_keeps_initial_price_as_list_price(self):
        product = {
            "productCode": "DD0001-100",
            "prices": {"currency": "USD", "currentPrice": 86.97, "initialPrice": 125.0, "discountPercentage": 30},
        }
        item = self.spider._product_item(
            product, category="mens-shoes-nik1zy7ok",
            category_url="https://www.nike.com/w/mens-shoes-nik1zy7ok", page=1, source="nike_next_data",
        )
        self.assertEqual(item["price"], 86.97)
        self.assertEqual(item["list_price"], 125.0)
        self.assertEqual(item["discount_percent"], 30)

    def test_undiscounted_item_has_no_list_price(self):
        product = {
            "productCode": "DD0002-100",
            "prices": {"currency": "USD", "currentPrice": 105, "initialPrice": 105, "discountPercentage": 0},
        }
        item = self.spider._product_item(
            product, category="mens-shoes-nik1zy7ok",
            category_url="https://www.nike.com/w/mens-shoes-nik1zy7ok", page=1, source="nike_next_data",
        )
        self.assertEqual(item["price"], 105)
        self.assertIsNone(item["list_price"])
        self.assertIsNone(item["discount_percent"])

    def test_availability_from_featured_attributes(self):
        self.assertEqual(
            NikeListingSpider._availability({"featuredAttributes": ["COMING_SOON"]}), "PreOrder"
        )
        self.assertEqual(NikeListingSpider._availability({}), "InStock")

    def test_promotion_title_is_read_from_the_product_wall_visibility(self):
        promotions = {
            "promotionId": "25P_DPMUS677",
            "visibilities": [
                {"visibilityType": "PW", "title": "See Price in Bag", "subtitle": ""}
            ],
        }
        self.assertEqual(NikeListingSpider._promotion(promotions), "See Price in Bag")
        self.assertIsNone(NikeListingSpider._promotion(None))

    # --------------------------------------------------------- proxy rewrite

    def test_scrapeops_proxy_gains_keep_headers(self):
        self.spider.settings = Mock()
        self.spider.settings.get.return_value = "http://scrapeops.country=us:***@proxy.scrapeops.io:5353"
        self.assertEqual(
            self.spider._api_proxy(),
            "http://scrapeops.country=us.keep_headers=true:%2A%2A%2A@proxy.scrapeops.io:5353", # Python's quote encodes '*' as %2A
        )

    def test_existing_keep_headers_is_not_duplicated(self):
        self.spider.settings = Mock()
        self.spider.settings.get.return_value = "http://scrapeops.country=us.keep_headers=true:***@proxy.scrapeops.io:5353"
        proxy = self.spider._api_proxy()
        self.assertEqual(proxy.count("keep_headers=true"), 1)

    def test_non_scrapeops_proxy_is_left_to_project_middleware(self):
        self.spider.settings = Mock()
        self.spider.settings.get.return_value = "http://localhost:8080"
        self.assertIsNone(self.spider._api_proxy())

    def test_api_request_carries_the_rewritten_proxy(self):
        self.spider.settings = Mock()
        self.spider.settings.get.return_value = "http://scrapeops.country=us:***@proxy.scrapeops.io:5353"
        request = self.spider._api_request(
            "/discover/product_wall/v1/x",
            page=2,
            category_url="https://www.nike.com/w/mens-shoes-nik1zy7ok",
            category="mens-shoes-nik1zy7ok",
        )
        self.assertIn("keep_headers=true", request.meta["proxy"])

    def test_listing_page_keeps_the_project_proxy(self):
        # Only the API leg needs keep_headers; the HTML leg must not be rewritten
        # so project-wide proxy behaviour stays in one place.
        self.spider.settings = Mock()
        self.spider.settings.get.return_value = "http://scrapeops.country=us:***@proxy.scrapeops.io:5353"
        request = self.spider._listing_request("https://www.nike.com/w/mens-shoes-nik1zy7ok", page=1)
        self.assertNotIn("proxy", request.meta)


if __name__ == "__main__":
    unittest.main()