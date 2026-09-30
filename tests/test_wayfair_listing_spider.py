from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse
from scrapy.selector import Selector

from common.spiders.wayfair_categories import (
    WAYFAIR_CATEGORIES,
    WAYFAIR_CATEGORY_INVENTORY,
)
from common.spiders.wayfair_listing_spider import WayfairListingSpider


class WayfairListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = WayfairListingSpider(category="sofas", max_pages=2)
        self.sample = Path("sample/wayfair-sofas-sample.html").read_text(encoding="utf-8")

    def response(self, body: str, page: int = 1) -> TextResponse:
        url = "https://www.wayfair.com/furniture/sb0/sofas-c413892.html"
        if page > 1:
            url += f"?curpage={page}"
        request = Request(
            url,
            meta={"category": "sofas", "department": "Furniture", "page": page},
        )
        return TextResponse(url, request=request, body=body, encoding="utf-8")

    def test_complete_inventory_is_flattened_and_deduplicated(self):
        self.assertEqual(len(WAYFAIR_CATEGORY_INVENTORY), 15)
        self.assertEqual(
            sum(len(group["subcategories"]) for group in WAYFAIR_CATEGORY_INVENTORY.values()),
            668,
        )
        urls = [entry["url"] for entry in WAYFAIR_CATEGORIES]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(
            next(entry["url"] for entry in WAYFAIR_CATEGORIES if entry["category"] == "sofas"),
            "https://www.wayfair.com/furniture/sb0/sofas-c413892.html",
        )

    def test_fixture_card_extracts_all_normalized_fields(self):
        card = Selector(text=self.sample).xpath('//*[@data-test-id="ListingCard"]')[0]
        item = self.spider._extract_card(card, "https://www.wayfair.com/furniture/")
        self.assertEqual(item["item_id"], "W117645758")
        self.assertEqual(item["variant_id"], "W117645758_1924516003_1924516004")
        self.assertTrue(item["title"].startswith('Boneless 96" Sectional'))
        self.assertEqual(item["brand"], "Latitude Run®")
        self.assertEqual(item["price"], 399.99)
        self.assertEqual(item["original_price"], 419.99)
        self.assertEqual(item["rating"], 4.23)
        self.assertEqual(item["reviews_count"], 513)
        self.assertEqual(item["selected_options"], "Black Corduroy, Left Hand Facing")
        self.assertEqual(item["availability"], "672 Left in Stock")
        self.assertEqual(item["delivery"], "FREE Delivery")

    def test_parse_excludes_placeholders_paginates_and_deduplicates(self):
        placeholder = '<div data-test-id="ListingCard"><span>Loading</span></div>'
        body = f'<main data-test-id="Browse-Grid">{placeholder}{self.sample}</main>'
        outputs = list(self.spider.parse(self.response(body)))
        items = [output for output in outputs if isinstance(output, dict)]
        requests = [output for output in outputs if isinstance(output, Request)]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_id"], "W117645758")
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, "https://www.wayfair.com/furniture/sb0/sofas-c413892.html?curpage=2")
        self.assertEqual(list(self.spider.parse(self.response(body, page=2))), [])

    def test_hub_page_without_browse_grid_fails_visibly(self):
        with self.assertRaisesRegex(ValueError, "hub or blocked"):
            list(self.spider.parse(self.response("<html><title>Furniture</title></html>")))

    def test_feed_export_fields_are_explicit(self):
        fields = self.spider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertEqual(fields[:4], ["category", "department", "item_id", "variant_id"])
        self.assertIn("raw", fields)


if __name__ == "__main__":
    unittest.main()
