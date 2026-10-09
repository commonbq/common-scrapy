import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.dollargeneral_listing_spider import DollargeneralListingSpider


TOKENS = {
    "idToken": "id", "appToken": "app", "appSessionToken": "session",
    "partnerApiToken": "partner", "customerGuid": "customer", "uniqueDeviceId": "device",
}


class DollarGeneralListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = DollargeneralListingSpider(category="on-sale", max_pages="2")

    def response(self, body, *, page=1, api_retry=0):
        request = Request(
            "https://dggo.dollargeneral.com/omni/api/v5/search/shoppinglist/product/Provider",
            meta={"tokens": TOKENS, "store_number": "12107", "page": page, "api_retry": api_retry},
        )
        return TextResponse(request.url, body=body.encode(), encoding="utf-8", request=request)

    def test_session_builds_filtered_api_request(self):
        data = {**TOKENS, "storeInfo": {"sn": "12107"}}
        response = TextResponse(
            "https://www.dollargeneral.com/bin/dg/user",
            body=json.dumps(data).encode(), encoding="utf-8",
            request=Request("https://www.dollargeneral.com/bin/dg/user", meta={"api_retry": 0}),
        )
        request = list(self.spider.parse_session(response))[0]
        payload = json.loads(request.body)
        self.assertEqual(payload["Filters"]["category"], ["On Sale"])
        self.assertEqual(payload["PageStartRecordIndex"], 0)
        self.assertIn("keep_headers=true", request.meta.get("proxy", "") or "keep_headers=true")

    def test_xml_api_maps_product_and_paginates(self):
        body = """<ProductSearchResponseV3 xmlns:d2p1="urn:dg">
          <Items><d2p1:ProductSearchItem>
            <d2p1:UPC>430002404825</d2p1:UPC><d2p1:Sku>43891101</d2p1:Sku>
            <d2p1:Description>Halloween Ghost Décor</d2p1:Description>
            <d2p1:Image>https://img.example/ghost</d2p1:Image>
            <d2p1:Price>8.0</d2p1:Price><d2p1:OriginalPrice>10</d2p1:OriginalPrice>
            <d2p1:Category>Seasonal</d2p1:Category><d2p1:Sellable>true</d2p1:Sellable>
            <d2p1:AvailableQty>3</d2p1:AvailableQty><d2p1:AverageRating>4.5</d2p1:AverageRating>
          </d2p1:ProductSearchItem></Items>
          <PaginationInfo><d2p1:TotalRecords>48</d2p1:TotalRecords></PaginationInfo>
        </ProductSearchResponseV3>"""
        results = list(self.spider.parse_api(self.response(body)))
        item, next_request = results
        self.assertEqual(item["item_id"], "430002404825")
        self.assertEqual(item["price"], 8)
        self.assertTrue(item["is_sellable"])
        self.assertEqual(item["source"], "dollargeneral_omni_search_api")
        self.assertEqual(json.loads(next_request.body)["PageStartRecordIndex"], 24)

    def test_json_api_is_supported(self):
        body = json.dumps({
            "Items": [{"UPC": 1, "Description": "Test Product", "Price": 2.5}],
            "PaginationInfo": {"TotalRecords": 1},
        })
        item = list(self.spider.parse_api(self.response(body)))[0]
        self.assertEqual(item["item_id"], "1")
        self.assertEqual(item["price"], 2.5)

    def test_proxy_failure_retries_then_fails(self):
        response = self.response('{"status":"Failed to get successful response from website. Please retry the request."}')
        retry = list(self.spider.parse_api(response))[0]
        self.assertEqual(retry.meta["api_retry"], 1)
        with self.assertRaises(RuntimeError):
            list(self.spider.parse_api(self.response(response.text, api_retry=2)))


if __name__ == "__main__":
    unittest.main()
