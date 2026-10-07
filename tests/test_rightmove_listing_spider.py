import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.rightmove_categories import RIGHTMOVE_CATEGORIES
from common.spiders.rightmove_listing_spider import RightmoveListingSpider


class RightmoveListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = RightmoveListingSpider(category="london", max_pages=2)

    def response(self, properties=None, *, page=1, body=None):
        properties = properties if properties is not None else [{
            "id": 89825950,
            "displayAddress": "Tottenham Street, Fitzrovia, W1",
            "propertyUrl": "/properties/89825950#/?channel=RES_BUY",
            "price": {"amount": 680000, "currencyCode": "GBP", "displayPrices": [{"displayPrice": "£680,000"}]},
            "bedrooms": 1, "bathrooms": 1, "propertySubType": "Flat",
            "propertyTypeFullDescription": "1 bedroom flat for sale",
            "tenure": {"tenureType": "LEASEHOLD"}, "displaySize": "526 sq. ft.",
            "location": {"latitude": 51.52055, "longitude": -0.13503},
            "summary": "A central London flat.",
            "keyFeatures": [{"description": "Central Fitzrovia Location"}],
            "images": [{"srcUrl": "https://media.rightmove.co.uk/property.jpeg"}],
            "numberOfImages": 12, "numberOfFloorplans": 1, "numberOfVirtualTours": 1,
            "customer": {"branchId": 129667, "branchDisplayName": "Leo Newman, London Sales", "contactTelephone": "020 3910 0880"},
            "firstVisibleDate": "2021-03-15T13:00:06Z", "addedOrReduced": "Added on 15/03/2021",
            "transactionType": "buy", "tags": ["FEATURED_PROPERTY"],
            "productLabel": {"productLabelText": "Featured Property"},
        }]
        payload = {"props": {"pageProps": {"searchResults": {
            "properties": properties, "resultCount": "60,714",
            "pagination": {"total": "42", "last": "984", "next": "24" if page == 1 else "48", "page": str(page)},
            "location": {"id": "REGION^87490"},
            "searchParameters": {"locationIdentifier": "REGION^87490"},
        }}}}
        html = body or (" " * 5000 + f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>')
        url = "https://www.rightmove.co.uk/property-for-sale/London.html" + ("?index=24" if page == 2 else "")
        request = Request(url, meta={"category": "london", "page": page})
        return TextResponse(url, request=request, body=html, encoding="utf-8")

    def test_categories_are_complete_and_unique(self):
        self.assertEqual(len(RIGHTMOVE_CATEGORIES), 20)
        self.assertEqual(len({entry["category"] for entry in RIGHTMOVE_CATEGORIES}), 20)
        self.assertEqual(self.spider.resolve_target_url(), "https://www.rightmove.co.uk/property-for-sale/London.html")
        self.assertEqual(len(list(RightmoveListingSpider(category="all").start_requests())), 20)
        custom = RightmoveListingSpider(category_url="https://www.rightmove.co.uk/property-for-sale/York.html")
        self.assertEqual(next(custom.start_requests()).meta["category"], "custom")

    def test_hydration_item_and_feed_contract(self):
        outputs = list(self.spider.parse(self.response()))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "89825950")
        self.assertEqual(item["price"], 680000)
        self.assertEqual(item["result_count"], 60714)
        self.assertEqual(item["source"], "rightmove_next_data")
        self.assertEqual(outputs[1].url, "https://www.rightmove.co.uk/property-for-sale/London.html?index=24")

    def test_deduplication_and_max_pages(self):
        list(self.spider.parse(self.response()))
        self.assertEqual(list(self.spider.parse(self.response(page=2))), [])

    def test_invalid_payloads_fail_visibly(self):
        cases = [
            ("tiny", "challenge or proxy-error"),
            (" " * 5000 + "<html></html>", "no searchResults"),
            (" " * 5000 + '<script id="__NEXT_DATA__">{}</script>', "no searchResults"),
        ]
        for body, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(RuntimeError, message):
                list(self.spider.parse(self.response(body=body)))


if __name__ == "__main__":
    unittest.main()
