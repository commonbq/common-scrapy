import unittest
from pathlib import Path

from scrapy.http import HtmlResponse

from common.spiders.bathandbodyworks_listing_spider import (
    BathandbodyworksListingSpider,
)


FIXTURE = Path(__file__).parents[1] / "sample" / "bathandbodyworks-listing-sample.html"


class BathandbodyworksListingSpiderTests(unittest.TestCase):
    def response(self, request, *, body=None, status=200):
        content = FIXTURE.read_bytes() if body is None else body.encode()
        return HtmlResponse(
            request.url, request=request, body=content, encoding="utf-8", status=status
        )

    def test_category_expands_to_every_child(self):
        spider = BathandbodyworksListingSpider(category="candles")
        requests = list(spider.start_requests())
        self.assertEqual(len(requests), 4)
        self.assertEqual(
            {request.meta["subcategory"] for request in requests},
            {"3-wick-candles", "4-wick-candles", "single-wick-candles", "candle-holders"},
        )

    def test_unknown_category_is_rejected(self):
        spider = BathandbodyworksListingSpider(category="unknown")
        with self.assertRaisesRegex(ValueError, "Available categories:.*body-care"):
            list(spider.start_requests())

    def test_jsonld_fixture_yields_complete_products_and_paginates(self):
        spider = BathandbodyworksListingSpider(category="body-care", max_pages=2)
        request = next(spider.start_requests())
        outputs = list(spider.parse(self.response(request)))
        items = [output for output in outputs if isinstance(output, dict)]
        following = outputs[-1]

        self.assertEqual(len(items), 48)
        self.assertEqual(
            items[0],
            {
                "item_id": "028005116",
                "title": "A Thousand Wishes Ultimate Hydration Body Cream",
                "url": "https://www.bathandbodyworks.com/p/a-thousand-wishes-ultimate-hydration-body-cream-028005116",
                "price": 4.95,
                "original_price": 18.95,
                "currency": "USD",
                "brand": "Bath & Body Works",
                "availability": "https://schema.org/InStock",
                "image_url": "https://www.bathandbodyworks.com/on/demandware.static/-/Sites-master-catalog/default/dwba22d9a1/crop/028005116_crop.jpg",
                "raw": None,
                "category": "body-care",
                "subcategory": "all-fragrance",
                "listing_url": "https://www.bathandbodyworks.com/c/body-care/all-fragrance",
                "page": 1,
                "source": "bathandbodyworks_jsonld_itemlist",
                "mode": "category",
            },
        )
        self.assertIn("page=2", following.url)

    def test_duplicate_only_and_blocked_pages_stop(self):
        spider = BathandbodyworksListingSpider(category="candles", max_pages=2)
        first = next(spider.start_requests())
        following = list(spider.parse(self.response(first)))[-1]
        self.assertEqual(list(spider.parse(self.response(following))), [])

        blocked_spider = BathandbodyworksListingSpider(category="candles")
        blocked = next(blocked_spider.start_requests())
        self.assertEqual(
            list(blocked_spider.parse(self.response(blocked, body="Access denied", status=403))),
            [],
        )


if __name__ == "__main__":
    unittest.main()
