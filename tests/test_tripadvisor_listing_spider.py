import json
import unittest
from urllib.parse import quote

from scrapy.http import HtmlResponse, Request

from common.spiders.tripadvisor_listing_spider import TripadvisorListingSpider


def hotel(item_id=545823):
    return {
        "locationId": item_id,
        "location": {
            "url": f"/Hotel_Review-g1-d{item_id}-Reviews-Test.html",
            "reviewSummary": {"rating": 4.8, "count": 123},
            "thumbnail": {"photoSizeDynamic": {"urlTemplate": "https://img.test/a.jpg?w={width}&h={height}"}},
            "locationV2": {
                "locationId": item_id, "names": {"name": "Test Hotel", "parentGeo": "Bali"},
                "geocode": {"latitude": -8.7, "longitude": 115.2},
                "contact": {"telephone": "+62 1", "streetAddress": {"fullAddress": "Bali, Indonesia", "city": "Sanur", "country": "Indonesia", "postalCode": "80227"}},
                "accommodationType": {"name": "Resort"}, "starRating": 5,
                "hotelHierarchicalPopIndex": {"rank": 3},
            },
        },
        "resultDetail": {
            "amenities": {"highlightedAmenities": [{"amenityName": "Pool"}]},
            "merchandisingLabels": [{"text": "Breakfast included"}],
            "hotelMetaResult": {"lowestPrice": "$160"},
        },
    }


def response(hotels, page=1):
    result = {"list": {"results": hotels, "isComplete": True}}
    outer = {"urqlSsrData": {"results": {"key": {"data": json.dumps(result)}}}}
    js = f'(this.$WP=this.$WP||[]).push(function(e){{}}(JSON.parse({json.dumps(json.dumps(outer))})));'
    body = '<html><body>' + ('x' * 5000) + f'<script src="data:text/javascript,{quote(js)}"></script></body></html>'
    request = Request("https://www.tripadvisor.com/Hotels-g294226-Bali-Hotels.html", meta={"page": page, "base_url": "https://www.tripadvisor.com/Hotels-g294226-Bali-Hotels.html"})
    return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)


class TripadvisorListingSpiderTest(unittest.TestCase):
    def test_maps_urql_bootstrap_and_feed_contract(self):
        spider = TripadvisorListingSpider(category="bali")
        item = list(spider.parse(response([hotel()])))[0]
        self.assertEqual(item["item_id"], "545823")
        self.assertEqual(item["title"], "Test Hotel")
        self.assertEqual(item["price"], 160.0)
        self.assertEqual(item["amenities"], ["Pool"])
        self.assertEqual(item["source"], "tripadvisor_urql_bootstrap")
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_deduplicates_and_builds_offset_pages(self):
        spider = TripadvisorListingSpider(category="bali")
        self.assertEqual(len(list(spider.parse(response([hotel(), hotel()])))), 1)
        self.assertIn("-oa30-", spider._page_url(spider.categories[0]["url"], 2))

    def test_rejects_challenge_or_missing_bootstrap(self):
        spider = TripadvisorListingSpider(category="bali")
        for body in ("captcha", "<html>missing state</html>"):
            page = HtmlResponse("https://www.tripadvisor.com/x", body=body, encoding="utf-8")
            with self.assertRaises(RuntimeError):
                list(spider.parse(page))


if __name__ == "__main__":
    unittest.main()
