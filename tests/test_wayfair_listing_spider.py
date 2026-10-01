from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse
from scrapy.selector import Selector

from common.spiders.wayfair_categories import (
    WAYFAIR_CATEGORIES,
    WAYFAIR_CATEGORY_INVENTORY,
    classify_target,
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

    def test_only_listing_targets_are_runnable_categories(self):
        # Hubs and informational pages stay in the inventory but must not be crawl targets.
        self.assertEqual(classify_target("https://www.wayfair.com/m/living-room"), "hub")
        self.assertEqual(classify_target("https://www.wayfair.com/affirm"), "informational")
        self.assertEqual(classify_target("https://www.wayfair.com/help/article/returns/"), "informational")
        self.assertEqual(classify_target("https://www.wayfair.com/design-services/?src=furn"), "informational")
        self.assertEqual(classify_target("https://www.wayfair.com/ideas-and-advice/type/x~M1"), "informational")
        self.assertEqual(classify_target(
            "https://www.wayfair.com/furniture/cat/furniture-c45974.html", is_department_root=True), "hub")
        self.assertEqual(classify_target("https://www.wayfair.com/furniture/sb0/sofas-c413892.html"), "listing")

        urls = {entry["url"] for entry in WAYFAIR_CATEGORIES}
        for bad in (
            "https://www.wayfair.com/help/article/returns/",
            "https://www.wayfair.com/affirm",
            "https://www.wayfair.com/design-services/?src=furn",
            "https://www.wayfair.com/m/motion-upholstery",
            "https://www.wayfair.com/furniture/cat/furniture-c45974.html",
        ):
            with self.subTest(url=bad):
                self.assertNotIn(bad, urls)
        # Real listings, including brand and curated collections, remain exposed.
        self.assertIn("https://www.wayfair.com/furniture/sb0/sofas-c413892.html", urls)
        self.assertIn("https://www.wayfair.com/curated/top-rated-furniture~ev426445.html", urls)

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

    def test_is_sponsored_reads_card_own_clio_context(self):
        # Regression: isSponsored is on the ListingCard, while the inner CardWrapper
        # context carries only listing/variant IDs, so reading it from the wrapper
        # always produced false.
        sponsored = self.sample.replace(
            'data-clio-context=\'{"indexWithinParent":1,"isSponsored":false}\'',
            'data-clio-context=\'{"indexWithinParent":1,"isSponsored":true}\'',
        )
        self.assertNotEqual(sponsored, self.sample)
        card = Selector(text=sponsored).xpath('//*[@data-test-id="ListingCard"]')[0]
        item = self.spider._extract_card(card, "https://www.wayfair.com/furniture/")
        self.assertTrue(item["is_sponsored"])

    def test_hub_page_without_browse_grid_fails_visibly(self):
        with self.assertRaisesRegex(ValueError, "hub or blocked"):
            list(self.spider.parse(self.response("<html><title>Furniture</title></html>")))

    def test_feed_export_fields_are_explicit(self):
        fields = self.spider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertEqual(fields[:4], ["category", "department", "item_id", "variant_id"])
        self.assertIn("raw", fields)


if __name__ == "__main__":
    unittest.main()
