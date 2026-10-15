from __future__ import annotations

import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.ebay_bootstrap_utils import (
    extract_marko_products,
    extract_subcategories_from_html,
)
from common.spiders.ebay_listing_spider import EbayListingSpider


class EbayListingSpiderTests(unittest.TestCase):
    def test_category_dictionary_loaded(self):
        self.assertEqual(len(EbayListingSpider.categories), 18)
        self.assertEqual(
            sum(len(section) for section in EbayListingSpider.categories.values()), 209
        )
        self.assertIn(
            "collectibles-art-antiques",
            EbayListingSpider.categories["Collectibles & Art"],
        )
        self.assertEqual(
            EbayListingSpider.categories["Collectibles & Art"]
            ["collectibles-art-antiques"]["url"],
            "https://www.ebay.com/b/Antiques/20081/bn_1851017",
        )

    def test_leaf_category_selects_one_listing(self):
        spider = EbayListingSpider(
            category="collectibles-art-antiques", max_pages=1
        )
        requests = list(spider.start_requests())
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].meta["subCategory"], "Antiques")

    def test_antique_fixture_parses_non_zero_subcategories(self):
        fixture_path = (
            Path(__file__).resolve().parents[1] / "sample" / "ebay-antiques-sample.html"
        )
        html = fixture_path.read_text(encoding="utf-8")
        items = extract_subcategories_from_html(html)

        self.assertGreater(len(items), 0)
        first = items[0]
        self.assertEqual(set(first), {"subCategory", "url"})
        self.assertIsInstance(first.get("subCategory"), str)
        self.assertTrue(first.get("url", "").startswith("https://www.ebay.com/"))

    def test_parse_follows_browse_tile_links_with_subcategory_context(self):
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
        html = """
        <section class="dp-browse-destinations-module">
          <div class="su-card-container">
            <a class="su-item-card__title" href="/b/Antique-Furniture/20091/bn_1865102">
              Antique Furniture
            </a>
          </div>
        </section>
        """
        request = Request(
            url="https://www.ebay.com/b/Antiques/20081/bn_1851017",
            meta={
                "page": 1,
                "original_url": "https://www.ebay.com/b/Antiques/20081/bn_1851017",
                "category_name": "Collectibles & Art",
                "subcategory_name": "Antiques",
                "category_url": "https://www.ebay.com/b/Antiques/20081/bn_1851017",
            },
        )
        response = TextResponse(
            url=request.url, body=html.encode(), encoding="utf-8", request=request
        )

        outputs = list(spider.parse(response))

        self.assertEqual(len(outputs), 1)
        follow_request = outputs[0]
        self.assertIsInstance(follow_request, Request)
        self.assertEqual(
            follow_request.url,
            "https://www.ebay.com/b/Antique-Furniture/20091/bn_1865102",
        )
        self.assertEqual(follow_request.meta["subcategory_name"], "Antique Furniture")
        self.assertEqual(follow_request.meta["page"], 1)
        self.assertEqual(follow_request.meta["original_url"], follow_request.url)
        self.assertEqual(follow_request.meta["category_url"], follow_request.url)

    def test_parse_skips_json_body_with_http_200(self):
        """A proxy/anti-bot envelope served as HTTP 200 must not crash parse.

        The proxy can return a JSON body with HTTP 200; calling parsel's
        ``.css()`` on it raised ``ValueError: Cannot use css on a Selector of
        type 'json'``, so the callback errored and the run exported 0 items
        with no ``item_scraped_count`` (#375).
        """
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
        request = Request(
            url="https://www.ebay.com/b/Antiques/20081/bn_1851017",
            meta={"page": 1, "category": "Collectibles & Art"},
        )
        body = json.dumps(
            {"message": "We couldn't retrieve a successful response"}
        ).encode()
        response = TextResponse(
            url=request.url,
            body=body,
            encoding="utf-8",
            request=request,
            headers={"Content-Type": "application/json"},
        )

        outputs = list(spider.parse(response))

        self.assertEqual(outputs, [])

    def test_parse_skips_small_proxy_envelope_and_logs(self):
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
        request = Request(
            url="https://www.ebay.com/b/Antiques/20081/bn_1851017",
            meta={"page": 1, "category": "Collectibles & Art"},
        )
        body = b"<html><body>request unsuccessful</body></html>"
        response = TextResponse(
            url=request.url,
            body=body,
            encoding="utf-8",
            request=request,
            headers={"Content-Type": "text/html"},
        )

        with self.assertLogs("ebay_listing", level="WARNING") as captured:
            outputs = list(spider.parse(response))

        self.assertEqual(outputs, [])
        self.assertTrue(any("non-HTML body" in line for line in captured.output))

    def test_extract_helpers_tolerate_json_body(self):
        """The extraction helpers must not raise on a non-HTML body."""
        envelope = '{"errors":[{"message":"No query string was present"}]}'
        self.assertEqual(extract_marko_products(envelope), [])
        self.assertEqual(extract_subcategories_from_html(envelope), [])

    def test_start_requests_covers_subcategories_with_context(self):
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
        requests = list(spider.start_requests())
        self.assertEqual(len(requests), 10)
        antique_request = next(
            request
            for request in requests
            if request.meta["subcategory_name"] == "Antiques"
        )
        self.assertEqual(antique_request.meta["category_name"], "Collectibles & Art")
        self.assertEqual(antique_request.meta["page"], 1)

    def test_parse_pagination_request_keeps_category_context(self):
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=2)
        url = "https://www.ebay.com/b/Antiques/20081/bn_1851017?_ipg=60&_pgn=1"
        request = Request(
            url=url,
            meta={
                "page": 1,
                "original_url": url,
                "category_name": "Collectibles & Art",
                "subcategory_name": "Antiques",
                "category_url": url,
            },
        )
        response = TextResponse(
            url=request.url, body=b"", encoding="utf-8", request=request
        )

        follow_up_requests = [
            x for x in spider.parse(response) if isinstance(x, Request)
        ]
        self.assertEqual(len(follow_up_requests), 1)
        self.assertEqual(follow_up_requests[0].meta.get("subcategory_name"), "Antiques")
        self.assertEqual(follow_up_requests[0].meta.get("page"), 2)

    def test_browse_tile_fallback_not_used_when_listing_items_exist(self):
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
        html = """
        <html><body>
          <ul>
            <li class="s-card">
              <a class="s-card__link" href="https://www.ebay.com/itm/123456789012"></a>
              <div class="s-card__title"><span>Vintage Clock</span></div>
              <span class="s-card__price">$42.00</span>
            </li>
          </ul>
          <section class="dp-browse-destinations-module">
            <div class="su-card-container">
              <a class="su-item-card__title" href="https://www.ebay.com/b/Antique-Furniture/20091/bn_1865102">Antique Furniture</a>
            </div>
          </section>
        </body></html>
        """
        req = Request(
            url="https://www.ebay.com/b/Antiques/20081/bn_1851017?_ipg=60&_pgn=1",
            meta={
                "page": 1,
                "original_url": "https://www.ebay.com/b/Antiques/20081/bn_1851017?_ipg=60&_pgn=1",
            },
        )
        response = TextResponse(
            url=req.url, body=html.encode("utf-8"), encoding="utf-8", request=req
        )

        outputs = [x for x in spider.parse(response) if isinstance(x, dict)]
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0]["itemId"], "123456789012")
        self.assertEqual(outputs[0]["url"], "https://www.ebay.com/itm/123456789012")
        self.assertEqual(outputs[0]["source"], "ebay_html_cards_fallback")


if __name__ == "__main__":
    unittest.main()
