import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.remax_listing_spider import RemaxListingSpider


def listing(item_id="MLS-123"):
    return {
        "uniqueListingId": item_id,
        "listingId": "123",
        "oUID": "MLS",
        "uPI": "property-123",
        "listingAddressFull": "1 Main St, Los Angeles, CA 90001",
        "listingAddress1": "1 Main St",
        "listingUrl": "/ca/los-angeles/home-details/1-main-st/property-123/MLS/123",
        "listingImages": [{"src": "https://images.example/1.jpg", "alt": "Home"}],
        "listPriceRaw": 500000,
        "currencyType": "$undefined",
        "beds": "3",
        "baths": "2.5",
        "livingArea": 1500,
        "listingSize": {"value": "1500", "text": "Sq Ft"},
        "lotSizeAcres": 0.2,
        "propertyType": "Single Family",
        "uiTransactionType": "Sale",
        "isRental": False,
        "banners": ["New Listing"],
        "openHouses": "$undefined",
        "listAgentFullName": "Agent Example",
        "listAgentPreferredPhone": "555-0100",
        "listOfficeName": "RE/MAX Example",
        "listOfficePhone": "555-0200",
        "listOfficeEmail": "office@example.com",
        "displayLogoAlt": "Example MLS",
        "location": {"city": "Los Angeles", "state": "CA", "postalCode": "90001"},
    }


def document(records):
    state = {"totalResults": 48, "results": records, "bounds": {}}
    flight = f'71:["$","$L74",null,{{"listingResultsUnfiltered":{json.dumps(state)}}}]'
    script = f"self.__next_f.push([1,{json.dumps(flight)}])"
    return "<html><body>" + ("x" * 5000) + f"<script>{script}</script></body></html>"


def response(records, page=1):
    url = RemaxListingSpider._page_url("https://www.remax.com/homes-for-sale/ca", page)
    request = Request(
        url,
        meta={"category": "california", "base_url": "https://www.remax.com/homes-for-sale/ca", "page": page},
    )
    return HtmlResponse(url, body=document(records), encoding="utf-8", request=request)


class RemaxListingSpiderTest(unittest.TestCase):
    def test_maps_rsc_bootstrap_and_obeys_feed_contract(self):
        spider = RemaxListingSpider(category="california", max_pages=1)
        item = list(spider.parse(response([listing()])))[0]
        self.assertEqual(item["item_id"], "MLS-123")
        self.assertEqual(item["price"], 500000)
        self.assertEqual(item["beds"], 3)
        self.assertEqual(item["baths"], 2.5)
        self.assertEqual(item["currency"], "USD")
        self.assertIsNone(item["open_houses"])
        self.assertEqual(item["source"], "remax_nextjs_rsc_bootstrap")
        self.assertEqual(set(item), set(spider.custom_settings["FEED_EXPORT_FIELDS"]))

    def test_builds_search_query_pagination_and_preserves_params(self):
        page = RemaxListingSpider._page_url(
            "https://www.remax.com/homes-for-sale/ca?upi=abc", 2
        )
        self.assertIn("upi=abc", page)
        self.assertIn("searchQuery=%7B%22pageNumber%22%3A2%7D", page)

    def test_paginates_and_stops_on_repeated_ids(self):
        spider = RemaxListingSpider(category="california", max_pages=2)
        outputs = list(spider.parse(response([listing()])))
        self.assertEqual(len(outputs), 2)
        self.assertTrue(outputs[1].url.endswith("searchQuery=%7B%22pageNumber%22%3A2%7D"))
        self.assertEqual(list(spider.parse(response([listing()], page=2))), [])

    def test_rejects_missing_bootstrap_or_challenge(self):
        spider = RemaxListingSpider(category="california")
        for body in ("<html></html>", "x" * 6000 + " captcha"):
            with self.subTest(body=body[:20]):
                request = Request(
                    "https://www.remax.com/homes-for-sale/ca",
                    meta={"category": "california", "base_url": "https://www.remax.com/homes-for-sale/ca", "page": 1},
                )
                bad = HtmlResponse(request.url, body=body, encoding="utf-8", request=request)
                with self.assertRaises(RuntimeError):
                    list(spider.parse(bad))


if __name__ == "__main__":
    unittest.main()
