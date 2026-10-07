import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.loopnet_listing_spider import LoopnetListingSpider


class LoopnetListingSpiderTests(unittest.TestCase):
    def test_bootstrap_extracts_criteria(self):
        state = {"criteria": {"PageNumber": 9, "PageSize": 25}}
        actual = LoopnetListingSpider._bootstrap("<script>viewdata.set(" + json.dumps(state) + ");</script>")
        self.assertEqual(actual["criteria"]["PageSize"], 25)

    def test_structured_api_mapping_only(self):
        spider = LoopnetListingSpider(category="commercial-real-estate-for-sale")
        request = Request("https://www.loopnet.com/services/search", meta={"page": 1, "criteria": {}, "referer": "https://www.loopnet.com/search/x"})
        payload = {"data": {"MetaState": {"TotalResultCount": 1}, "Map": {"Pins": [{
            "ListingId": 42, "Title": "Commerce Center", "ListingUrl": "/Listing/x/42/",
            "Latitude": 30.1, "Longitude": -97.7, "Price": 1200000,
        }]}}}
        response = TextResponse(request=request, url=request.url, body=json.dumps(payload).encode(), encoding="utf-8")
        items = list(spider.parse_api(response))
        self.assertEqual(items[0]["item_id"], "42")
        self.assertEqual(items[0]["title"], "Commerce Center")
        self.assertEqual(items[0]["source"], "loopnet_search_api")

    def test_api_placard_fragment_mapping(self):
        html = """<div placard-event-model='{"ListingSearchResultItems":[{"ListingID":1,"Latitude":2,"Longitude":3}]}'></div>
        <article class='placard' data-id='1' gtm-listing-city='Austin' gtm-listing-state='TX'>
        <a class='left-h4' href='/Listing/x/1/'>Main St</a><ul class='data-points-a'><li name='Price'>$1,250,000</li></ul></article>"""
        row = LoopnetListingSpider._records({"Placards": {"HTML": html}})[0]
        self.assertEqual(row["ListingId"], "1")
        self.assertEqual(row["Price"], 1250000.0)
        self.assertEqual(row["Latitude"], 2)

    def test_challenge_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "challenge"):
            LoopnetListingSpider._bootstrap('{"Concurrency":"This request exceeded your accounts concurrency limit."}')
