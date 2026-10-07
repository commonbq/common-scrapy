import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.movoto_categories import MOVOTO_CATEGORIES
from common.spiders.movoto_listing_spider import MovotoListingSpider


ROOT = Path(__file__).parents[1]


class MovotoListingSpiderTest(unittest.TestCase):
    def response(self, name="movoto-new-york-ny.html", page=1):
        url = "https://www.movoto.com/new-york-ny/" if page == 1 else f"https://www.movoto.com/new-york-ny/p-{page}/"
        request = Request(url, meta={"category": "new-york-ny", "page": page, "base_url": "https://www.movoto.com/new-york-ny/"})
        body = (ROOT / "sample" / name).read_bytes()
        return HtmlResponse(url, request=request, body=body, encoding="utf-8")

    def test_categories_are_ordered_and_complete(self):
        self.assertEqual(20, len(MOVOTO_CATEGORIES))
        self.assertEqual("new-york-ny", MOVOTO_CATEGORIES[0]["category"])
        self.assertEqual("las-vegas-nv", MOVOTO_CATEGORIES[-1]["category"])

    def test_maps_initial_state_and_feed_fields(self):
        spider = MovotoListingSpider(category="new-york-ny", max_pages=1)
        output = list(spider.parse(self.response()))
        self.assertEqual(50, len(output))
        first = output[0]
        self.assertEqual("movoto_initial_state", first["source"])
        self.assertTrue(first["item_id"])
        self.assertTrue(first["title"])
        self.assertTrue(first["url"].startswith("https://www.movoto.com/"))
        self.assertIsInstance(first["price"], int)
        self.assertEqual(1, first["page"])
        self.assertEqual(50, len({item["item_id"] for item in output}))
        self.assertEqual(list(first), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_paginates_with_p_segment_and_deduplicates(self):
        spider = MovotoListingSpider(category="new-york-ny", max_pages=2)
        first_page = list(spider.parse(self.response()))
        next_request = first_page.pop()
        self.assertEqual("https://www.movoto.com/new-york-ny/p-2/", next_request.url)
        second_page = list(spider.parse(self.response("movoto-new-york-ny-p-2.html", 2)))
        self.assertEqual(50, len(first_page))
        self.assertEqual(50, len(second_page))
        self.assertFalse({item["item_id"] for item in first_page} & {item["item_id"] for item in second_page})

    def test_rejects_missing_bootstrap_without_html_fallback(self):
        spider = MovotoListingSpider(category="new-york-ny")
        body = b"<html><body>" + (b"x" * 6000) + b"</body></html>"
        request = Request("https://www.movoto.com/new-york-ny/", meta={"category": "new-york-ny", "page": 1, "base_url": "https://www.movoto.com/new-york-ny/"})
        response = HtmlResponse(request.url, request=request, body=body, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "bootstrap has no listings"):
            list(spider.parse(response))

    def test_rejects_challenge(self):
        spider = MovotoListingSpider(category="new-york-ny")
        body = ("<html>px-captcha" + "x" * 6000 + "</html>").encode()
        response = HtmlResponse("https://www.movoto.com/new-york-ny/", body=body, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "challenge or proxy-error"):
            list(spider.parse(response))


if __name__ == "__main__":
    unittest.main()
