from __future__ import annotations

import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.ebay_bootstrap_utils import (
    extract_marko_products,
)
from common.spiders.ebay_listing_spider import EbayListingSpider


class EbayEcommerceExtractionTests(unittest.TestCase):
    def test_laptop_fixture_extracts_marko_listing_products(self):
        fixture_path = (
            Path(__file__).resolve().parents[1] / "sample" / "ebay-laptops-sample.html"
        )

        items = extract_marko_products(fixture_path.read_text(encoding="utf-8"))

        self.assertEqual(len(items), 60)
        self.assertEqual(items[0]["productId"], "377497902082")
        self.assertEqual(items[0]["price"], 197.1)
        self.assertEqual(items[0]["currency"], "USD")
        self.assertEqual(items[0]["originalPrice"], 219.0)
        self.assertEqual(items[0]["discountPercentage"], 10.0)
        self.assertEqual(len(items[0]["imageUrls"]), 4)
        self.assertEqual(items[0]["condition"], "Pre-Owned")
        self.assertEqual(items[0]["brand"], "Lenovo")
        self.assertEqual(items[0]["quantityAvailable"], 12)
        self.assertEqual(items[0]["shippingCost"], 0.0)
        self.assertEqual(items[0]["purchaseOptions"], "or Best Offer")
        self.assertTrue(items[0]["acceptsBestOffer"])
        self.assertTrue(items[0]["isNewListing"])
        self.assertEqual(items[0]["position"], 1)
        self.assertEqual(sum(item["isSponsored"] for item in items), 14)

    def test_listing_spider_uses_only_html_card_route(self):
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
        html = """
        <script type="application/ld+json">
          {"@type":"Product","name":"JSON-LD item","url":"https://www.ebay.com/itm/111111111111","offers":{"price":"10.00","priceCurrency":"USD"}}
        </script>
        <li class="s-card">
          <a class="s-card__link" href="https://www.ebay.com/itm/222222222222"></a>
          <div class="s-card__title"><span>HTML item</span></div>
          <span class="s-card__price">$20.00</span>
        </li>
        """
        request = Request(
            url="https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276",
            meta={"page": 1},
        )
        response = TextResponse(
            url=request.url, body=html.encode(), encoding="utf-8", request=request
        )

        items = [item for item in spider.parse(response) if isinstance(item, dict)]

        self.assertEqual([item["itemId"] for item in items], ["222222222222"])

    def test_fixture_follows_all_browse_tile_links(self):
        fixture_path = (
            Path(__file__).resolve().parents[1] / "sample" / "ebay-antiques-sample.html"
        )
        html = fixture_path.read_text(encoding="utf-8")
        url = "https://www.ebay.com/b/Antiques/20081/bn_1851017"
        spider = EbayListingSpider(category="Collectibles & Art", max_pages=1)
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
            url=url, body=html.encode(), encoding="utf-8", request=request
        )

        requests = [
            output for output in spider.parse(response) if isinstance(output, Request)
        ]

        self.assertEqual(len(requests), 18)
        self.assertEqual(requests[0].meta["category_name"], "Collectibles & Art")
        self.assertEqual(requests[0].meta["subcategory_name"], "Antique Furniture")
        self.assertEqual(requests[0].meta["page"], 1)
        self.assertEqual(requests[0].meta["category_url"], requests[0].url)


if __name__ == "__main__":
    unittest.main()
