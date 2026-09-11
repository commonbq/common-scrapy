from __future__ import annotations

import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.ebay_bootstrap_utils import (
    extract_browse_tiles_from_html,
    extract_items_from_html_cards,
)
from common.spiders.ebay_listing_spider import EbayListingSpider


class EbayListingSpiderTests(unittest.TestCase):
    def test_category_dictionary_loaded(self):
        self.assertEqual(len(EbayListingSpider.categories), 209)
        category_map = {entry["category"]: entry["url"] for entry in EbayListingSpider.categories}
        self.assertIn("collectibles-art/antiques", category_map)
        self.assertEqual(
            category_map["collectibles-art/antiques"],
            "https://www.ebay.com/b/Antiques/20081/bn_1851017",
        )

    def test_category_accepts_dictionary_url(self):
        url = "https://www.ebay.com/b/Antiques/20081/bn_1851017"
        spider = EbayListingSpider(category=url, max_pages=1)
        self.assertEqual(spider._resolve_target_url(), url)

    def test_antique_fixture_parses_non_zero_browse_tiles(self):
        fixture_path = Path(__file__).resolve().parents[1] / "sample" / "ebay-antiques-sample.html"
        html = fixture_path.read_text(encoding="utf-8")
        items = extract_browse_tiles_from_html(html)

        self.assertGreater(len(items), 0)
        first = items[0]
        self.assertIsInstance(first.get("title"), str)
        self.assertTrue(first.get("url", "").startswith("https://www.ebay.com/"))
        self.assertEqual(first.get("source"), "ebay_html_browse_tiles_fallback")

    def test_antique_fixture_has_no_item_cards(self):
        fixture_path = Path(__file__).resolve().parents[1] / "sample" / "ebay-antiques-sample.html"
        html = fixture_path.read_text(encoding="utf-8")
        self.assertEqual(extract_items_from_html_cards(html), [])

    def test_start_requests_uses_proxy_meta(self):
        import common.spiders.base_listing_spider as base_listing_spider

        original_proxy = base_listing_spider.PROXY
        base_listing_spider.PROXY = "http://proxy.local:8080"
        try:
            spider = EbayListingSpider(category="collectibles-art/antiques", max_pages=1)
            request = next(spider.start_requests())
            self.assertEqual(request.meta.get("proxy"), "http://proxy.local:8080")
            self.assertEqual(request.meta.get("page"), 1)
        finally:
            base_listing_spider.PROXY = original_proxy

    def test_parse_pagination_request_keeps_proxy_meta(self):
        import common.spiders.base_listing_spider as base_listing_spider

        original_proxy = base_listing_spider.PROXY
        base_listing_spider.PROXY = "http://proxy.local:8080"
        try:
            spider = EbayListingSpider(category="collectibles-art/antiques", max_pages=2)
            spider.category_url = spider._resolve_target_url()
            request = Request(
                url="https://www.ebay.com/b/Antiques/20081/bn_1851017?_ipg=60&_pgn=1",
                meta={"page": 1, "original_url": "https://www.ebay.com/b/Antiques/20081/bn_1851017?_ipg=60&_pgn=1"},
            )
            response = TextResponse(url=request.url, body=b"", encoding="utf-8", request=request)

            follow_up_requests = [x for x in spider.parse(response) if isinstance(x, Request)]
            self.assertEqual(len(follow_up_requests), 1)
            self.assertEqual(follow_up_requests[0].meta.get("proxy"), "http://proxy.local:8080")
            self.assertEqual(follow_up_requests[0].meta.get("page"), 2)
        finally:
            base_listing_spider.PROXY = original_proxy


if __name__ == "__main__":
    unittest.main()
