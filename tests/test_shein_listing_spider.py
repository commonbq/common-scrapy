import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.shein_listing_spider import SheinListingSpider


class SheinListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = SheinListingSpider(category="women", max_pages=1)

    def response(self, body):
        request = Request(
            "https://us.shein.com/Women-c-2030.html",
            meta={"category": "women", "page": 1},
        )
        return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_feed_contract_and_itemlist_extraction(self):
        body = Path("sample/shein-listing-product.html").read_text(encoding="utf-8")
        items = list(self.spider.parse(self.response(body)))

        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "12345678")
        self.assertEqual(items[0]["price"], 19.99)
        self.assertEqual(items[0]["availability"], "InStock")
        self.assertEqual(items[0]["source"], "shein_itemlist_jsonld")

    def test_missing_itemlist_fails_visibly(self):
        body = f'<script type="application/ld+json">{json.dumps({"@type": "WebPage"})}</script>'
        with self.assertRaisesRegex(RuntimeError, "No SHEIN ItemList JSON-LD"):
            list(self.spider.parse(self.response(body)))


if __name__ == "__main__":
    unittest.main()
