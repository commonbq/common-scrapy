import unittest
from pathlib import Path

from scrapy.http import HtmlResponse

from common.spiders.anthropologie_listing_spider import AnthropologieListingSpider


FIXTURE = Path(__file__).parents[1] / "sample" / "anthropologie-listing-sample.html"


class AnthropologieListingSpiderTests(unittest.TestCase):
    def response(self, request, *, body=None, status=200):
        if body is None:
            body = FIXTURE.read_bytes()
        elif isinstance(body, str):
            body = body.encode()
        return HtmlResponse(
            request.url,
            request=request,
            body=body,
            encoding="utf-8",
            status=status,
        )

    def test_category_expands_to_every_configured_subcategory(self):
        spider = AnthropologieListingSpider(category="clothing")
        requests = list(spider.start_requests())

        self.assertEqual(spider.available_categories(), sorted(spider.categories))
        self.assertEqual(len(requests), len(spider.categories["clothing"]))
        self.assertEqual(
            {request.meta["subcategory"] for request in requests},
            {"all", "shop-all"},
        )
        self.assertTrue(all(request.meta["category"] == "clothing" for request in requests))

    def test_unknown_category_is_rejected(self):
        spider = AnthropologieListingSpider(category="unknown")
        with self.assertRaisesRegex(ValueError, "Available categories:.*clothing"):
            list(spider.start_requests())

    def test_fixture_extracts_authoritative_jsonld_products(self):
        spider = AnthropologieListingSpider(category="clothing", max_pages=2)
        request = list(spider.start_requests())[1]
        outputs = list(spider.parse(self.response(request)))
        items = [output for output in outputs if isinstance(output, dict)]
        requests = [output for output in outputs if not isinstance(output, dict)]

        self.assertEqual(len(items), 36)
        self.assertEqual(len(requests), 1)
        self.assertEqual(
            items[0],
            {
                "item_id": "by-anthropologie-goldie-100-cashmere-sweater",
                "title": "By Anthropologie Goldie 100% Cashmere Sweater",
                "url": "https://www.anthropologie.com/shop/by-anthropologie-goldie-100-cashmere-sweater?color=702&type=STANDARD",
                "price": 138.0,
                "original_price": None,
                "currency": "USD",
                "brand": "Anthropologie",
                "rating": None,
                "reviews_count": None,
                "image_url": "https://images.urbndata.com/is/image/Anthropologie/4114086690121_702_b14?$an-category$&qlt=80&fit=constrain",
                "raw": None,
                "category": "clothing",
                "subcategory": "shop-all",
                "listing_url": "https://www.anthropologie.com/womens-clothing",
                "page": 1,
                "source": "anthropologie_jsonld_itemlist",
                "mode": "category",
            },
        )
        self.assertIn("page=2", requests[0].url)
        self.assertEqual(requests[0].meta["subcategory"], "shop-all")

    def test_duplicates_stop_pagination_and_blocked_pages_are_ignored(self):
        spider = AnthropologieListingSpider(category="new", max_pages=3)
        first = next(spider.start_requests())
        outputs = list(spider.parse(self.response(first)))
        following = outputs[-1]
        self.assertEqual(list(spider.parse(self.response(following))), [])

        blocked_spider = AnthropologieListingSpider(category="new")
        blocked = next(blocked_spider.start_requests())
        self.assertEqual(
            list(blocked_spider.parse(self.response(blocked, body="Access denied", status=403))),
            [],
        )


if __name__ == "__main__":
    unittest.main()
