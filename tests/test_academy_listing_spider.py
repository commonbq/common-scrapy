import json
import unittest
import urllib.parse as urlparse
from pathlib import Path

from scrapy.http import TextResponse
from scrapy.settings import Settings

from common.spiders.academy_categories import ACADEMY_CATEGORY_INVENTORY
from common.spiders.academy_listing_spider import (
    AcademyListingSpider,
    _load_categories,
)

HOT_DEALS_URL = "https://www.academy.com/c/hot-deals"
HOT_DEALS_ID = "210952"


def _query(response_or_request) -> dict:
    return urlparse.parse_qs(urlparse.urlparse(response_or_request.url).query)


def _iter(nodes):
    for node in nodes:
        yield node
        for key in ("l2_level", "l3_level", "l4_level"):
            yield from _iter(node.get(key) or [])


def _flatten(nodes, depth=1, out=None):
    out = [] if out is None else out
    for node in nodes:
        out.append((depth, node))
        _flatten(node.get("subcategories") or [], depth + 1, out)
    return out


class AcademyCategoriesTest(unittest.TestCase):
    def test_inventory_shape(self):
        self.assertEqual(len(ACADEMY_CATEGORY_INVENTORY), 12)
        rows = _flatten(ACADEMY_CATEGORY_INVENTORY)
        self.assertEqual(len(rows), 246)
        self.assertEqual(sum(1 for d, _ in rows if d == 1), 12)
        self.assertEqual(sum(1 for d, _ in rows if d == 2), 97)
        self.assertEqual(sum(1 for d, _ in rows if d == 3), 137)

    def test_every_node_is_requestable(self):
        for _, node in _flatten(ACADEMY_CATEGORY_INVENTORY):
            self.assertTrue(str(node.get("categoryId") or "").strip())

    def test_bundled_urls_are_absolute_academy_urls(self):
        for _, node in _flatten(ACADEMY_CATEGORY_INVENTORY):
            url = node.get("url")
            if url:
                self.assertTrue(url.startswith("https://www.academy.com/c/"))

    def test_load_categories_dedupes_cross_listed_ids(self):
        rows = _load_categories()
        ids = [entry["category_id"] for entry in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn(HOT_DEALS_ID, ids)
        hot = next(e for e in rows if e["category_id"] == HOT_DEALS_ID)
        self.assertEqual(hot["url"], HOT_DEALS_URL)
        # Cross-listed under "Deals + Clearance" and "New + Trending".
        self.assertGreaterEqual(len(hot["departments"]), 1)

    def test_hot_deals_category_slug(self):
        rows = _load_categories()
        slugs = {entry["category"] for entry in rows}
        self.assertIn("deals-clearance-hot-deals", slugs)


class AcademyListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = AcademyListingSpider(category="deals-clearance-hot-deals", max_pages=2)
        self.page1 = json.loads(
            Path("sample/academy-hot-deals-api-page1.json").read_text()
        )
        self.page2 = json.loads(
            Path("sample/academy-hot-deals-api-page2.json").read_text()
        )

    def response(self, request, payload=None, status=200, body=None):
        if body is None:
            body = json.dumps(payload if payload is not None else self.page1).encode()
        return TextResponse(
            request.url, request=request, body=body, status=status, encoding="utf-8"
        )

    def first_request(self, spider=None):
        spider = spider or self.spider
        return next(spider.start_requests())

    def _items(self, request, payload):
        """Drain parse_category, keeping only item dicts."""
        return [
            out
            for out in self.spider.parse_category(self.response(request, payload))
            if isinstance(out, dict)
        ]

    # --------------------------------------------------------------- requests

    def test_request_targets_first_party_category_api(self):
        request = self.first_request()
        self.assertTrue(
            request.url.startswith(f"https://www.academy.com/api/category/v3/{HOT_DEALS_ID}?")
        )
        query = _query(request)
        self.assertEqual(query["web"], ["true"])
        self.assertEqual(query["displayFacets"], ["true"])
        self.assertEqual(query["recordsPerPage"], ["48"])
        # pageNumber on this endpoint is 1-based.
        self.assertEqual(query["pageNumber"], ["1"])
        self.assertEqual(request.meta["category"], "deals-clearance-hot-deals")
        self.assertEqual(
            request.headers["Referer"].decode(), HOT_DEALS_URL
        )

    def test_request_adds_scrapeops_bypass_to_proxy(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        spider.settings = Settings(
            {"PROXY": "http://scrapeops.country=us:tok@proxy.scrapeops.io:5353"}
        )
        proxy = self.first_request(spider).meta.get("proxy")
        self.assertIn("scrapeops.country=us.bypass=5", proxy)
        self.assertIn("tok@proxy.scrapeops.io:5353", proxy)

    def test_proxy_helper_preserves_existing_bypass(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        spider.settings = Settings(
            {"PROXY": "http://scrapeops.country=us.bypass=7:tok@proxy.scrapeops.io:5353"}
        )
        proxy = self.first_request(spider).meta.get("proxy")
        self.assertIn("bypass=7", proxy)
        self.assertNotIn("bypass=5", proxy)

    def test_proxy_helper_ignores_foreign_proxy(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        spider.settings = Settings({"PROXY": "http://user:pw@proxy.example.com:8080"})
        self.assertIsNone(self.first_request(spider).meta.get("proxy"))

    def test_default_run_targets_every_inventory_category(self):
        spider = AcademyListingSpider()
        targets = [request.meta["category"] for request in spider.start_requests()]
        self.assertEqual(len(targets), len(spider.categories))
        self.assertEqual(len(set(targets)), len(spider.categories))

    def test_url_input_resolves_to_inventory_entry(self):
        spider = AcademyListingSpider(url=HOT_DEALS_URL)
        request = self.first_request(spider)
        self.assertIn(f"/api/category/v3/{HOT_DEALS_ID}?", request.url)

    def test_unknown_category_raises_with_available_names(self):
        spider = AcademyListingSpider(category="not-a-real-academy-category")
        with self.assertRaises(ValueError) as ctx:
            list(spider.start_requests())
        self.assertIn("Available categories", str(ctx.exception))

    def test_unknown_url_raises_with_available_names(self):
        spider = AcademyListingSpider(url="https://www.academy.com/c/not-real")
        with self.assertRaises(ValueError) as ctx:
            list(spider.start_requests())
        self.assertIn("numeric categoryId", str(ctx.exception))

    # ------------------------------------------------------------------ parse

    def test_parse_emits_normalized_items(self):
        request = self.first_request()
        items = self._items(request, self.page1)
        self.assertEqual(len(items), len(self.page1["hits"]))
        first = items[0]
        self.assertEqual(first["category"], "deals-clearance-hot-deals")
        self.assertEqual(first["category_id"], HOT_DEALS_ID)
        self.assertEqual(first["department"], "Deals + Clearance")
        self.assertEqual(first["item_id"], self.page1["hits"][0]["uniqueId"])
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["source"], "academy_category_api")
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["raw"], self.page1["hits"][0])
        self.assertTrue(first["url"].startswith("https://www.academy.com/p/"))
        self.assertTrue(first["image_url"].startswith("https://academy.scene7.com/"))

    def test_parse_includes_raw_product_payload(self):
        request = self.first_request()
        items = self._items(request, self.page1)
        self.assertTrue(all(item["raw"] for item in items))
        self.assertIn("raw", self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(
            self.spider.custom_settings["FEED_EXPORT_FIELDS"][-1], "raw"
        )

    def test_parse_follows_next_page(self):
        request = self.first_request()
        gen = self.spider.parse_category(self.response(request))
        items = []
        nxt = None
        for out in gen:
            if isinstance(out, dict):
                items.append(out)
            else:
                nxt = out
        self.assertEqual(len(items), 5)
        self.assertIsNotNone(nxt)
        self.assertEqual(_query(nxt)["pageNumber"], ["2"])

    def test_second_page_does_not_duplicate_first(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals", max_pages=2)
        first = self.first_request(spider)
        list(spider.parse_category(self.response(first)))
        second = spider._category_request(first.meta["entry"], page=2)
        items = list(spider.parse_category(self.response(second, self.page2)))
        ids = {item["item_id"] for item in items}
        self.assertEqual(len(ids), len(items))
        self.assertTrue(all(item["page"] == 2 for item in items))

    def test_max_pages_stops_pagination(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals", max_pages=1)
        out = list(spider.parse_category(self.response(self.first_request(spider))))
        self.assertTrue(all(isinstance(o, dict) for o in out))

    def test_nb_pages_stop_condition(self):
        payload = dict(self.page1, nbPages=1, nbHits=5)
        spider = AcademyListingSpider(category="deals-clearance-hot-deals", max_pages=5)
        out = list(spider.parse_category(self.response(self.first_request(spider), payload)))
        self.assertTrue(all(isinstance(o, dict) for o in out))

    def test_empty_page_stops_pagination(self):
        payload = dict(self.page1, hits=[])
        spider = AcademyListingSpider(category="deals-clearance-hot-deals", max_pages=5)
        out = list(spider.parse_category(self.response(self.first_request(spider), payload)))
        self.assertEqual(out, [])

    # ------------------------------------------------------------- robustness

    def test_bot_challenge_body_raises(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        body = b"<html><body>Access Denied - you have been blocked</body></html>"
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_category(self.response(self.first_request(spider), body=body)))
        self.assertIn("bot-challenge", str(ctx.exception))

    def test_scrapeops_error_json_raises_on_non_200(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        response = self.response(self.first_request(spider), status=503, body=b"{}")
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_category(response))
        self.assertIn("HTTP 503", str(ctx.exception))

    def test_non_json_body_raises(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        body = b"not json at all"
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_category(self.response(self.first_request(spider), body=body)))
        self.assertIn("non-JSON", str(ctx.exception))

    def test_missing_hits_key_raises(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse_category(self.response(self.first_request(spider), {"page": 1})))
        self.assertIn("no hits list", str(ctx.exception))

    # ------------------------------------------------------------ item fields

    def test_price_and_promo_fields(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        product = {
            "uniqueId": "1",
            "name": "Test",
            "partNumber": "999",
            "seoURL": "test-product",
            "facet_Brand": "acme",
            "sellable": "true",
            "giftCardFlag": "N",
            "freeShipping": True,
            "defaultSku": {"salePrice": 7.5, "listPrice": 10.0, "color": "Blue"},
            "definingAttributes": {"Size": "Large"},
            "descriptiveAttributes": {"averageRating": "4.5", "reviewcount": "12"},
            "promoMessage": "20% Off",
            "promoCode": "SAVE20",
            "promoPrice": "8.00",
            "minEffectivePrice": 8.0,
        }
        request = self.first_request(spider)
        item = spider._item(product, self.response(request), request.meta["entry"], 1, 1, 100)
        self.assertEqual(item["price"], 7.5)
        self.assertEqual(item["list_price"], 10.0)
        self.assertEqual(item["promo_price"], 8.0)
        self.assertEqual(item["brand"], "acme")
        self.assertEqual(item["color"], "Blue")
        self.assertEqual(item["size"], "Large")
        self.assertEqual(item["rating"], 4.5)
        self.assertEqual(item["reviews_count"], 12)
        self.assertTrue(item["in_stock"])
        self.assertTrue(item["free_shipping"])
        self.assertFalse(item["gift_card"])
        self.assertEqual(item["url"], "https://www.academy.com/p/test-product/999")

    def test_protocol_relative_image_is_absolutized(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        self.assertEqual(
            spider._absolute_image("//academy.scene7.com/is/image/academy/1"),
            "https://academy.scene7.com/is/image/academy/1",
        )
        self.assertEqual(
            spider._absolute_image("21454658"),
            "https://academy.scene7.com/is/image/academy/21454658",
        )
        self.assertIsNone(spider._absolute_image(""))

    def test_duplicate_item_ids_are_dropped(self):
        spider = AcademyListingSpider(category="deals-clearance-hot-deals")
        request = self.first_request(spider)
        response = self.response(request)
        entry = request.meta["entry"]
        product = {"uniqueId": "42", "name": "Dup", "partNumber": "1"}
        first = spider._item(product, response, entry, 1, 1, 10)
        second = spider._item(product, response, entry, 1, 2, 10)
        self.assertIsNotNone(first)
        self.assertIsNone(second)


class AcademyHeaderHydrationTest(unittest.TestCase):
    """The bundled taxonomy was captured from window.ASOData; parse it back."""

    def setUp(self):
        self.html = Path("sample/academy-header.html").read_text()

    def _components(self):
        decoder = json.JSONDecoder()
        found = []
        marker = "window.ASOData['"
        index = self.html.find(marker)
        while index != -1:
            start = index + len(marker)
            end = self.html.index("']=", start)
            key = self.html[start:end]
            try:
                value, _ = decoder.raw_decode(self.html[end + 3 :].lstrip())
            except ValueError:
                index = self.html.find(marker, end)
                continue
            found.append((key, value))
            index = self.html.find(marker, end)
        return found

    def test_header_component_present(self):
        components = dict(self._components())
        headers = [v for v in components.values() if v.get("rcn") == "header240"]
        self.assertEqual(len(headers), 1)
        nav = headers[0]["cms"]["shop"]["shop_navigation"][0]["l1_level"]
        self.assertEqual([n["title"] for n in nav], ["Men's", "Sports"])
        self.assertTrue(all("l2_level" in n for n in nav))

    def test_plp_component_present(self):
        components = dict(self._components())
        plps = [v for v in components.values() if v.get("rcn") == "productListingPage240"]
        self.assertEqual(len(plps), 1)
        self.assertEqual(len(plps[0]["api"]["products"]), 3)

    def test_bundled_inventory_matches_header_capture(self):
        """Every id-bearing node of the captured departments is in the inventory."""
        components = dict(self._components())
        header = next(v for v in components.values() if v.get("rcn") == "header240")
        captured = header["cms"]["shop"]["shop_navigation"][0]["l1_level"]
        captured_ids = {
            str(node.get("category_id") or node.get("unique_id") or "").strip()
            for node in _iter(captured)
        } - {""}
        self.assertTrue(captured_ids)
        self.assertTrue(captured_ids <= {entry["category_id"] for entry in _load_categories()})


if __name__ == "__main__":
    unittest.main()
