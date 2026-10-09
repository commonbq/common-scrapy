import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.apartments_categories import APARTMENTS_CATEGORIES
from common.spiders.apartments_listing_spider import ApartmentsListingSpider


def response(state, *, page=1):
    url = "https://www.apartments.com/new-york-ny/" if page == 1 else f"https://www.apartments.com/new-york-ny/{page}/"
    body = f"<html><script>window.aptsState = {json.dumps(state)};</script></html>"
    request = Request(url, meta={"category": "new-york-ny", "page": page})
    return HtmlResponse(url, request=request, body=body.encode(), encoding="utf-8")


class ApartmentsListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = ApartmentsListingSpider(category="new-york-ny", max_pages=2)
        self.state = {
            "as": {
                "p": [
                    {"k": "1j2c5h6", "lat": 40.7766, "lng": -73.93585, "t": 5,
                     "f": 184, "nr": 5075, "xr": 6483, "mu": 1,
                     "sl": [{"k": "child1"}]},
                    {"k": "2vjnkfb", "lat": 40.88934, "lng": -73.89894, "t": 4,
                     "f": 152, "nr": 1750, "xr": 2300},
                ],
                "ic": {"g": {"t": 2, "v": 30699, "id": "6zxdpbt", "d": "New York, NY",
                               "a": {"ci": "New York", "st": "NY", "co": "New York",
                                     "cc": "USA", "mn": "New York", "dma": "New York, NY-NJ-PA-CT"}}},
                "nc": 896, "ac": 7350, "lc": 700,
                "pg": {"page": 1, "totalPages": 18,
                       "nextUrl": "https://www.apartments.com/new-york-ny/2/"},
            }
        }

    def test_taxonomy_has_exact_twenty_markets(self):
        self.assertEqual(20, len(APARTMENTS_CATEGORIES))
        self.assertEqual("new-york-ny", APARTMENTS_CATEGORIES[0]["category"])
        self.assertEqual("boston-ma", APARTMENTS_CATEGORIES[-1]["category"])

    def test_bootstrap_item_mapping_and_pagination(self):
        output = list(self.spider.parse(response(self.state)))
        items = [row for row in output if isinstance(row, dict)]
        requests = [row for row in output if isinstance(row, Request)]
        self.assertEqual(2, len(items))
        self.assertEqual("1j2c5h6", items[0]["item_id"])
        self.assertEqual(5075, items[0]["rent_min"])
        self.assertEqual(["child1"], items[0]["related_listing_ids"])
        self.assertEqual("New York", items[0]["city"])
        self.assertEqual("apartments_apts_state_bootstrap", items[0]["source"])
        self.assertEqual(1, len(requests))
        self.assertEqual("https://www.apartments.com/new-york-ny/2/", requests[0].url)

    def test_deduplicates_inventory_across_pages(self):
        list(self.spider.parse(response(self.state)))
        second = json.loads(json.dumps(self.state))
        second["as"]["p"] = [second["as"]["p"][0], {"k": "new-id", "lat": 1, "lng": 2}]
        second["as"]["pg"] = {"page": 2, "totalPages": 18}
        items = list(self.spider.parse(response(second, page=2)))
        self.assertEqual(["new-id"], [row["item_id"] for row in items])

    def test_rejects_challenge_and_missing_bootstrap(self):
        with self.assertRaisesRegex(RuntimeError, "challenge/proxy"):
            self.spider._bootstrap('{"API Credits":"You have consumed all your API credits"}')
        with self.assertRaisesRegex(RuntimeError, "no window.aptsState"):
            self.spider._bootstrap("<html>ordinary shell</html>")


if __name__ == "__main__":
    unittest.main()
