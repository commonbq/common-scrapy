import json
import unittest

from scrapy.http import JsonResponse, Request

from common.spiders.toolstation_listing_spider import ToolstationListingSpider


class ToolstationListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = ToolstationListingSpider(category="kitchen-cabinets", max_pages=2)

    def response(self, *, start=0, total=49):
        product = {
            "pid": "12145", "slug": "kitchen-kit-base-end", "title": "Kitchen Kit Base End",
            "group_title": "Kitchen Kit Base End", "brand": "Kitchen Kit",
            "url": "https://www.toolstation.com/kitchen-kit-base-end/p12145",
            "thumb_image": "https://cdn.aws.toolstation.com/images/12145.jpg",
            "prices": json.dumps({"net": 37.12, "gross": 44.54, "was": 49.49, "priceperunit": None}),
            "ts_reviews": 3.75, "numberofreviews": 4, "channel": 3,
            "name_type": "900mm", "name_qty": "Each", "variations": 3,
        }
        request = Request("https://www.toolstation.com/api/search/crs", meta={"page": start // 48 + 1})
        body = json.dumps({"response": {"numFound": total, "start": start, "docs": [product]}}).encode()
        return JsonResponse(request.url, request=request, body=body, encoding="utf-8")

    def test_api_request_uses_category_and_offset(self):
        request = self.spider._api_request(2)
        self.assertIn("q=c1468", request.url)
        self.assertIn("start=48", request.url)
        self.assertIn("groupby=variant_group", request.url)

    def test_parse_maps_prices_and_rich_fields(self):
        outputs = list(self.spider.parse(self.response(total=1)))
        item = outputs[0]
        self.assertEqual(item["item_id"], "12145")
        self.assertEqual(item["price"], 44.54)
        self.assertEqual(item["original_price"], 49.49)
        self.assertEqual(item["availability"], "direct_ship")
        self.assertEqual(item["source"], "toolstation_bloomreach_crs_api")

    def test_parse_paginates_by_api_total(self):
        outputs = list(self.spider.parse(self.response(total=49)))
        requests = [value for value in outputs if isinstance(value, Request)]
        self.assertEqual(len(requests), 1)
        self.assertIn("start=48", requests[0].url)

    def test_feed_contract_is_ordered_and_complete(self):
        fields = self.spider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertEqual(fields[0:5], ["category", "category_name", "category_id", "department", "category_url"])
        self.assertIn("raw", fields)
        self.assertEqual(fields[-1], "timestamp")


if __name__ == "__main__":
    unittest.main()
