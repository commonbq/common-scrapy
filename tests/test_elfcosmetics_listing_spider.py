from pathlib import Path
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.elfcosmetics_listing_spider import ElfcosmeticsListingSpider


class ElfcosmeticsListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = ElfcosmeticsListingSpider(category="face", max_pages=2)

    def response(self):
        url = "https://www.elfcosmetics.com/collections/face"
        request = Request(url, meta={"page": 1, "origin": url})
        body = (Path(__file__).parents[1] / "sample" / "elfcosmetics-face.html").read_bytes()
        return HtmlResponse(url, request=request, body=body, encoding="utf-8")

    def test_feed_export_fields_include_bootstrap_product_data(self):
        fields = self.spider.custom_settings["FEED_EXPORT_FIELDS"]
        for field in (
            "variant_id",
            "compare_at_price",
            "available_for_sale",
            "images",
            "selected_options",
            "swatches",
            "raw",
        ):
            self.assertIn(field, fields)

    def test_bootstrap_items_include_rich_data_and_pagination(self):
        output = list(self.spider.parse(self.response()))
        items, requests = (
            [value for value in output if isinstance(value, dict)],
            [value for value in output if isinstance(value, Request)],
        )

        self.assertEqual(len(items), 9)
        self.assertEqual(items[0]["item_id"], "8949173813336")
        self.assertEqual(items[0]["variant_id"], "44556751241304")
        self.assertEqual(items[0]["title"], "Sheer For It Bronzer Tint")
        self.assertEqual(items[0]["price"], 6.0)
        self.assertEqual(items[0]["currency"], "USD")
        self.assertFalse(items[0]["available_for_sale"])
        self.assertEqual(items[0]["selected_options"][0]["value"], "Fair/Light Neutral")
        self.assertEqual(len(items[0]["images"]), 2)
        self.assertEqual(len(items[0]["swatches"]), 4)
        self.assertEqual(items[0]["source"], "elfcosmetics_hydrogen_bootstrap")
        self.assertEqual(requests[0].url, "https://www.elfcosmetics.com/collections/face?page=2")

    def test_missing_bootstrap_data_does_not_fall_back(self):
        url = "https://www.elfcosmetics.com/collections/face"
        request = Request(url, meta={"page": 1, "origin": url})
        response = HtmlResponse(url, request=request, body=b"<html></html>", encoding="utf-8")
        self.assertEqual(list(self.spider.parse(response)), [])


if __name__ == "__main__":
    unittest.main()
