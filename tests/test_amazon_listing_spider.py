from __future__ import annotations

import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.amazon_listing_spider import AmazonListingSpider


class AmazonListingSpiderTests(unittest.TestCase):
    def test_category_fixture_follows_shop_by_category_carousel(self):
        fixture_path = (
            Path(__file__).resolve().parents[1]
            / "sample"
            / "amazon-home-kitchen.html"
        )
        url = "https://www.amazon.com/b?node=1055398"
        request = Request(
            url=url,
            meta={"page": 1, "category": "Home & Kitchen"},
        )
        response = HtmlResponse(
            url=url,
            body=fixture_path.read_bytes(),
            encoding="utf-8",
            request=request,
        )

        spider = AmazonListingSpider(category="Home & Kitchen", max_pages=1)
        outputs = list(spider.parse(response))
        requests = [output for output in outputs if isinstance(output, Request)]

        self.assertEqual(len(requests), 7)
        self.assertEqual(requests[0].meta["category"], "Home & Kitchen")
        self.assertEqual(requests[0].meta["sub_category"], "Bed & bath")
        self.assertIn("node=1057792", requests[0].url)
        self.assertNotIn("pf_rd_", requests[0].url)
        self.assertNotIn("ref_", requests[0].url)
        self.assertNotIn(
            "Shopbop", {request.meta["sub_category"] for request in requests}
        )

    def test_category_urls_are_canonicalized_by_node(self):
        tracked_url = (
            "https://www.amazon.com/b/home-products?node=1057792"
            "&pf_rd_p=tracking-token&pf_rd_r=request-token&ref_=nav"
        )

        canonical = AmazonListingSpider._canonicalize_category_url(tracked_url)

        self.assertEqual(canonical, "https://www.amazon.com/b?node=1057792")

    def test_crawl_depth_is_limited_to_four(self):
        self.assertEqual(AmazonListingSpider.custom_settings["DEPTH_LIMIT"], 4)


if __name__ == "__main__":
    unittest.main()
