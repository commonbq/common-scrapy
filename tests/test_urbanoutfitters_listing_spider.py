from __future__ import annotations

import json
from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.urbanoutfitters_categories import (
    parse_category_sitemap,
    resolve_category,
)
from common.spiders.urbanoutfitters_listing_spider import UrbanOutfittersListingSpider


SITEMAP = Path("sample/urbanoutfitters-categories-sitemap.xml")
PAGE1 = Path("sample/urbanoutfitters-plp-pinia-page1.html")
PAGE2 = Path("sample/urbanoutfitters-plp-pinia-page2.html")


class UrbanOutfittersListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = UrbanOutfittersListingSpider(category="new-arrivals", max_pages=2)
        self.categories = parse_category_sitemap(SITEMAP.read_text())
        self.target = resolve_category(self.categories, category="new-arrivals")

    def response(self, fixture=PAGE1, page=1, url=None):
        url = url or ("https://www.urbanoutfitters.com/new-arrivals" + ("?page=2" if page == 2 else ""))
        request = Request(url, meta={"category": self.target, "page": page, "base_url": self.target["url"]})
        return TextResponse(url, request=request, body=fixture.read_bytes(), encoding="utf-8")

    def test_full_sitemap_inventory_and_query_categories(self):
        self.assertEqual(len(self.categories), 2162)
        self.assertEqual(len({row["category"] for row in self.categories}), 2162)
        self.assertEqual(len({row["url"] for row in self.categories}), 2162)
        refined = resolve_category(
            self.categories,
            category_url="/dresses?length=Mini&sleeve=Long+Sleeve",
        )
        self.assertEqual(refined["category"], "dresses-length-mini-sleeve-long-sleeve")
        self.assertEqual(refined["query"], "length=Mini&sleeve=Long Sleeve")

    def test_pinia_state_is_double_decoded(self):
        state = self.spider._pinia_state(PAGE1.read_text())
        self.assertEqual(state["category"]["currentPage"], 1)
        self.assertEqual(state["category"]["totalRecordCount"], 1241)
        self.assertEqual(len(self.spider._tiles(state)), 10)

    def test_items_fields_prices_and_page_two_request(self):
        outputs = list(self.spider.parse(self.response()))
        items = [value for value in outputs if isinstance(value, dict)]
        requests = [value for value in outputs if not isinstance(value, dict)]
        self.assertEqual(len(items), 10)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, "https://www.urbanoutfitters.com/new-arrivals?page=2")
        first = items[0]
        self.assertEqual(first["item_id"], "UO-106663735-000")
        self.assertEqual(first["sku_id"], "106663735_000")
        self.assertEqual(first["title"], "Kimchi Blue Ella Flyaway Ruffle Lace Trim Cami")
        self.assertEqual(first["price"], 39)
        self.assertEqual(first["rating"], 4.7308)
        self.assertEqual(first["reviews_count"], 26)
        sale = next(item for item in items if item["on_sale"])
        self.assertEqual((sale["price"], sale["list_price"]), (55.3, 79))
        self.assertEqual(sale["discount_percentage"], 30.0)
        self.assertEqual(first["source"], "urbanoutfitters_pinia_ssr_tiles")
        self.assertIsInstance(first["raw"], dict)

    def test_second_page_uses_hydrated_page_key(self):
        state = self.spider._pinia_state(PAGE2.read_text())
        self.assertEqual(state["category"]["currentPage"], 2)
        self.assertEqual(len(self.spider._tiles(state)), 8)

    def test_query_pagination_preserves_refinements(self):
        url = "https://www.urbanoutfitters.com/dresses?color=green&sleeve=Long+Sleeve"
        self.assertEqual(self.spider._page_url(url, 1), url)
        self.assertEqual(
            self.spider._page_url(url + "&page=9", 2),
            url + "&page=2",
        )

    def test_malformed_and_missing_hydration_fail_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "No #urbnInitialPiniaState"):
            self.spider._pinia_state("<html></html>")
        bad = '<script id="urbnInitialPiniaState" type="mime/invalid">"nope</script>'
        with self.assertRaisesRegex(RuntimeError, "not decodable JSON"):
            self.spider._pinia_state(bad)

    def test_404_stub_is_rejected(self):
        request = Request("https://www.urbanoutfitters.com/nope")
        response = TextResponse(
            request.url,
            request=request,
            body=Path("sample/urbanoutfitters-404-stub.html").read_bytes(),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "404 stub"):
            self.spider._reject_challenge(response, "category page")

    def test_feed_fields_cover_every_item_key(self):
        item = next(value for value in self.spider.parse(self.response()) if isinstance(value, dict))
        self.assertEqual(set(item), set(self.spider.custom_settings["FEED_EXPORT_FIELDS"]))


if __name__ == "__main__":
    unittest.main()
