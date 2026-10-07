import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.homes_listing_spider import (
    HomesListingSpider,
    decode_gstate,
    parse_price,
)


class HomesListingSpiderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = Path("sample/homes-new-york-ny.html").read_bytes()

    def response(self):
        url = "https://www.homes.com/new-york-ny/"
        request = Request(
            url,
            meta={"category": "new-york-ny", "category_url": url},
        )
        return HtmlResponse(url=url, body=self.html, encoding="utf-8", request=request)

    def test_decodes_bootstrap(self):
        search = decode_gstate(self.html.decode())["as"]
        self.assertEqual(search["count"], 23209)
        self.assertEqual(search["sc"]["pagingCriteria"]["resultSize"], 700)
        self.assertGreater(len(search["p"].split("~")), 600)

    def test_emits_bootstrap_records_and_contract(self):
        spider = HomesListingSpider(category="new-york-ny")
        items = list(spider.parse(self.response()))
        self.assertEqual(len(items), 632)
        self.assertEqual(len({item["item_id"] for item in items}), 632)
        first = items[0]
        self.assertEqual(first["item_id"], "4b215f8nkz79f")
        self.assertEqual(first["listing_key"], "lfbykfb6tllzk")
        self.assertEqual(first["price"], 785000.0)
        self.assertEqual(first["latitude"], 40.84279)
        self.assertEqual(first["source"], "homes_gstate_map_bootstrap")
        self.assertEqual(
            set(spider.custom_settings["FEED_EXPORT_FIELDS"]), set(first)
        )

    def test_grouped_marker_and_price_parser(self):
        spider = HomesListingSpider(category="new-york-ny")
        items = list(spider.parse(self.response()))
        self.assertTrue(any(item["grouped_listings"] for item in items))
        self.assertEqual(parse_price("1.55M"), 1550000.0)
        self.assertEqual(parse_price("785K"), 785000.0)
        self.assertIsNone(parse_price("Contact"))

    def test_missing_bootstrap_fails(self):
        with self.assertRaisesRegex(ValueError, "window.gState"):
            decode_gstate("<html></html>")


if __name__ == "__main__":
    unittest.main()
