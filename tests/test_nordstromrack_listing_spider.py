import unittest
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from common.spiders.nordstromrack_listing_spider import NordstromrackListingSpider

class NordstromrackListingSpiderTests(unittest.TestCase):
    def setUp(self): self.spider = NordstromrackListingSpider(category="women")
    def test_fixture_and_feed_contract(self):
        request = Request("https://www.nordstromrack.com/c/women", meta={"category":"women","page":1,"listing_url":"https://www.nordstromrack.com/c/women"})
        response = HtmlResponse(request.url, request=request, body=Path("sample/nordstromrack-listing.html").read_bytes(), encoding="utf-8")
        items = list(self.spider.parse(response))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["item_id"], "7788991")
        self.assertEqual(items[0]["price"], 34.97)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])

if __name__ == "__main__": unittest.main()
