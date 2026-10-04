import json
import unittest
import urllib.parse as urlparse
from pathlib import Path

from scrapy.http import Request, TextResponse
from scrapy.settings import Settings

from common.spiders.dickssportinggoods_listing_spider import (
    DickssportinggoodsListingSpider,
)


def _query(response_or_request) -> dict:
    query = urlparse.parse_qs(urlparse.urlparse(response_or_request.url).query)
    return query


class DickssportinggoodsListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = DickssportinggoodsListingSpider(
            category="soccer-gear-equipment", max_pages=2
        )
        self.payload = json.loads(
            Path("sample/dickssportinggoods-listing-products.json").read_text()
        )

    def response(self, request, payload=None, status=200, body=None):
        if body is None:
            body = json.dumps(payload if payload is not None else self.payload).encode()
        return TextResponse(
            request.url,
            request=request,
            body=body,
            status=status,
            encoding="utf-8",
        )

    def first_request(self, spider=None):
        spider = spider or self.spider
        return next(spider.start_requests())

    # --------------------------------------------------------------- requests

    def test_category_builds_selected_category_search_request(self):
        request = self.first_request()
        self.assertTrue(
            request.url.startswith(
                "https://prod-catalog-product-api.dickssportinggoods.com/v2/search"
            )
        )
        search_vo = json.loads(_query(request)["searchVO"][0])
        self.assertEqual(search_vo["selectedCategory"], "12301_201847")
        self.assertEqual(search_vo["storeId"], 15108)
        self.assertEqual(search_vo["pageNumber"], 0)
        self.assertEqual(search_vo["pageSize"], 48)
        self.assertEqual(search_vo["searchTypes"], ["COLOR_PINNING"])
        self.assertEqual(request.meta["category"], "soccer-gear-equipment")

    def test_product_request_adds_scrapeops_bypass_to_proxy(self):
        spider = DickssportinggoodsListingSpider(category="soccer-gear-equipment")
        spider.settings = Settings(
            {"PROXY": "http://scrapeops.country=us:tok@proxy.scrapeops.io:5353"}
        )
        proxy = self.first_request(spider).meta.get("proxy")
        self.assertIn("scrapeops.country=us.bypass=5", proxy)
        self.assertIn("tok@proxy.scrapeops.io:5353", proxy)

    def test_proxy_helper_preserves_existing_bypass(self):
        spider = DickssportinggoodsListingSpider(category="soccer-gear-equipment")
        spider.settings = Settings(
            {"PROXY": "http://scrapeops.country=us.bypass=7:tok@proxy.scrapeops.io:5353"}
        )
        proxy = self.first_request(spider).meta.get("proxy")
        self.assertIn("bypass=7", proxy)
        self.assertNotIn("bypass=5", proxy)

    def test_default_run_targets_every_inventory_category(self):
        spider = DickssportinggoodsListingSpider()
        targets = [request.meta["category"] for request in spider.start_requests()]
        self.assertEqual(len(targets), len(spider.categories))
        self.assertEqual(len(set(targets)), len(spider.categories))

    def test_url_input_resolves_to_inventory_entry(self):
        spider = DickssportinggoodsListingSpider(
            url="https://www.dickssportinggoods.com/c/soccer-gear-equipment"
        )
        request = self.first_request(spider)
        search_vo = json.loads(_query(request)["searchVO"][0])
        self.assertEqual(search_vo["selectedCategory"], "12301_201847")

    def test_unknown_category_raises_with_inventory_hint(self):
        spider = DickssportinggoodsListingSpider(category="not-a-real-category")
        with self.assertRaises(ValueError):
            self.first_request(spider)

    # ------------------------------------------------------------------ parse

    def test_maps_product_fields_from_api_payload(self):
        request = self.first_request()
        outputs = list(self.spider.parse_search(self.response(request)))
        item, next_request = outputs[0], outputs[-1]
        self.assertEqual(item["item_id"], "13286436")
        self.assertEqual(item["title"], "adidas FIFA World Cup Historical Mini Soccer Ball Set")
        self.assertEqual(item["brand"], "adidas")
        self.assertEqual(item["partnumber"], "26968873")
        self.assertEqual(item["parent_partnumber"], "25ADIUSOCCWC26HSTMFAA")
        self.assertTrue(item["url"].startswith("https://www.dickssportinggoods.com/p/"))
        self.assertTrue(item["image_url"].startswith("https://dks.scene7.com/is/image/dkscdn/"))
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["rating"], 4.72)
        self.assertEqual(item["reviews_count"], 125)
        self.assertEqual(item["discount_percent"], 43.39)
        self.assertEqual(item["primary_category"], "SoccerBalls-253295")
        self.assertEqual(item["product_attributes"]["X_BRAND"], "adidas")
        self.assertEqual(item["source"], "dickssportinggoods_search_api")
        self.assertEqual(item["source_url"], request.url)
        self.assertIsInstance(item["raw"], dict)
        self.assertEqual(item["raw"]["catentryId"], 13286436)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["page"], 1)
        self.assertEqual(next_request.meta["page"], 2)

    def test_price_uses_the_active_offer_window(self):
        # 141.52 is the offer active in the sample's third window
        # (start 1790740800000, end 1791010739999); 148.97 windows are past.
        self.spider._now_ms = 1790800000000
        request = self.first_request()
        item = list(self.spider.parse_search(self.response(request)))[0]
        self.assertEqual(item["price"], 141.52)
        self.assertEqual(item["list_price"], 250.0)

    def test_price_falls_back_to_list_when_no_offer_window_active(self):
        self.spider._now_ms = 1000
        request = self.first_request()
        item = list(self.spider.parse_search(self.response(request)))[0]
        self.assertEqual(item["price"], 250.0)
        self.assertEqual(item["list_price"], 250.0)

    def test_deduplicates_products_across_pages(self):
        request = self.first_request()
        first = list(self.spider.parse_search(self.response(request)))
        self.assertTrue(first[0]["item_id"])
        # Re-parsing the identical page must not re-emit any product.
        second = list(self.spider.parse_search(self.response(request)))
        self.assertFalse(any(isinstance(entry, dict) for entry in second))

    def test_pagination_stops_when_total_is_exhausted(self):
        payload = dict(self.payload)
        payload["totalCount"] = 48
        outputs = list(self.spider.parse_search(self.response(self.first_request(), payload)))
        self.assertTrue(all(isinstance(entry, dict) for entry in outputs))
        self.assertEqual(len(outputs), 48)

    def test_max_pages_one_stops_after_first_page(self):
        spider = DickssportinggoodsListingSpider(category="soccer-gear-equipment")
        request = next(spider.start_requests())
        outputs = list(spider.parse_search(self.response(request)))
        self.assertTrue(all(isinstance(entry, dict) for entry in outputs))

    # --------------------------------------------------------------- failures

    def test_rejects_bot_challenge_page(self):
        request = self.first_request()
        response = self.response(
            request, body=b"<html><title>Site Unavailable</title></html>"
        )
        with self.assertRaises(RuntimeError):
            list(self.spider.parse_search(response))

    def test_rejects_non_json_body(self):
        request = self.first_request()
        response = self.response(request, body=b"<html>not json</html>")
        with self.assertRaises(RuntimeError):
            list(self.spider.parse_search(response))

    def test_rejects_http_error_status(self):
        request = self.first_request()
        response = self.response(request, status=403, body=b"{}")
        with self.assertRaises(RuntimeError):
            list(self.spider.parse_search(response))

    # -------------------------------------------------------------- inventory

    def test_inventory_has_unique_urls_and_complete_taxonomy(self):
        urls = [entry["url"] for entry in self.spider.categories]
        self.assertEqual(len(urls), len(set(urls)))
        # 1685 nodes collapse to 1287 unique URLs in the captured inventory.
        self.assertEqual(len(urls), 1287)
        departments = {dept for entry in self.spider.categories for dept in entry["departments"]}
        self.assertEqual(len(departments), 10)

    def test_inventory_entries_are_well_formed(self):
        for entry in self.spider.categories:
            self.assertIsInstance(entry["category"], str)
            self.assertTrue(entry["category"])
            self.assertIsInstance(entry["url"], str)
            self.assertTrue(entry["url"].startswith("https://www.dickssportinggoods.com/c/"))
            self.assertIsInstance(entry["catgroupId"], int)
            self.assertTrue(entry["departments"])
        # category slugs are unique because they key the inventory entries.
        slugs = [entry["category"] for entry in self.spider.categories]
        self.assertEqual(len(slugs), len(set(slugs)))


if __name__ == "__main__":
    unittest.main()
