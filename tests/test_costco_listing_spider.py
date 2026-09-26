from __future__ import annotations

import json
import unittest
from pathlib import Path

from scrapy.http import TextResponse

from common.spiders.costco_listing_spider import CostcoListingSpider


class CostcoListingSpiderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_html = (
            Path(__file__).resolve().parents[1] / "sample" / "costco-coffee.html"
        ).read_text(encoding="utf-8")

    def setUp(self):
        self.spider = CostcoListingSpider(category="coffee", max_pages=2)
        self.first = next(self.spider.start_requests())

    def response(self, request, body, *, status=200):
        return TextResponse(
            request.url,
            request=request,
            body=body.encode("utf-8"),
            encoding="utf-8",
            status=status,
        )

    def listing_request(self):
        outputs = list(self.spider.parse(self.response(self.first, self.fixture_html)))
        self.assertEqual(len(outputs), 1)
        return outputs[0]

    def search_payload(self, result_ids, *, total_size=20):
        results = []
        for item_id in result_ids:
            results.append(
                {
                    "id": item_id,
                    "product": {
                        "title": f"Coffee {item_id}",
                        "uri": f"https://www.costco.com/test-{item_id}.product.{item_id}.html",
                        "brands": ["Kirkland Signature"],
                        "rating": {"averageRating": 4.7, "ratingCount": 123},
                        "images": [
                            {"url": f"https://images.costco-static.com/{item_id}.jpg"}
                        ],
                    },
                    "variantRollupValues": {
                        "price": [14.99],
                        "originalPrice": [19.99],
                    },
                }
            )
        return json.dumps(
            {"searchResult": {"results": results, "totalSize": total_size}}
        )

    def test_category_mapping_expands_from_inventory(self):
        self.assertIn("coffee/single-serve", self.spider.available_categories())
        self.assertEqual(
            CostcoListingSpider(category="coffee/tea").resolve_target_url(),
            "https://www.costco.com/tea.html",
        )

    def test_fixture_discovers_subcategories_and_builds_api_request(self):
        request = self.listing_request()
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            request.url, "https://gdx-api.costco.com/catalog/search/api/v1/search"
        )
        payload = json.loads(request.body)
        self.assertEqual(payload["pageSize"], 24)
        self.assertEqual(payload["offset"], 0)
        self.assertEqual(payload["pageCategories"], ["coffee-sweeteners"])
        self.assertEqual(
            payload["filterBy"], ['attributes.category_uri: ANY("coffee-sweeteners")']
        )
        self.assertEqual(request.meta["category_name"], "Coffee")
        self.assertEqual(request.meta["category_id"], "512120")
        self.assertEqual(
            {entry["url"] for entry in request.meta["subcategories"]},
            {
                "https://www.costco.com/single-serve-coffee.html",
                "https://www.costco.com/whole-bean-coffee.html",
                "https://www.costco.com/ground-coffee.html",
                "https://www.costco.com/instant-coffee.html",
                "https://www.costco.com/creamer-sweeteners.html",
                "https://www.costco.com/tea.html",
            },
        )

    def test_search_results_are_normalized_and_paginated(self):
        request = self.listing_request()
        item, follow_up = list(
            self.spider.parse_search(
                self.response(request, self.search_payload(["100361434"], total_size=25))
            )
        )
        self.assertEqual(item["item_id"], "100361434")
        self.assertEqual(item["title"], "Coffee 100361434")
        self.assertEqual(item["price"], 14.99)
        self.assertEqual(item["original_price"], 19.99)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["brand"], "Kirkland Signature")
        self.assertEqual(
            item["url"],
            "https://www.costco.com/test-100361434.product.100361434.html",
        )
        self.assertEqual(item["category_name"], "Coffee")
        self.assertEqual(item["page"], 1)
        self.assertEqual(follow_up.meta["page"], 2)
        self.assertEqual(json.loads(follow_up.body)["offset"], 24)
        duplicate_page = list(
            self.spider.parse_search(
                self.response(
                    follow_up, self.search_payload(["100361434"], total_size=25)
                )
            )
        )
        self.assertEqual(duplicate_page, [])

    def test_escaped_flight_strings_are_decoded(self):
        rows = [
            '1:["$","$L0",null,{"serviceConfigurationGRSSearch":{"endpoint":"https://gdx-api.costco.com/catalog/search/api/v1/search","method":"POST","required_request_headers":{"client-identifier":"cid","client_id":{"USBC":"USBC"},"locale":{"en-us":"en-US"},"searchResultProvider":"GRS","Content-Type":"application/json"},"required_request_parameters":{"pageSize":20,"offset":0,"deliveryLocations":[],"filterBy":[]}}}]',
            '2:["$","$L0",null,{"specificPageEntry":{"category_id":{"category_title":"Coffee","category_id":"512120"},"page_id":"coffee-sweeteners","title":"Coffee"}}]',
            '3:["$","$L0",null,{"pageType":"category","resultsPerPage":24,"categoryTitle":"Coffee"}]',
            '4:["$","$L0",null,{"productTileConfigData":{"translationsConfig":{"keys":{"productApiWarehouseNumber":"847"}}}}]',
            '5:["$","$L18",null,{"title":"Shop by Category","ads":[["$","$L450",null,{"categoryData":{"title":"Tea","hrefUrl":"/tea.html?deliveryFacetFlag=true\\u0026refine=x"}}]]}]',
        ]
        html = (
            "<script>(self.__next_f=self.__next_f||[]).push([0])</script>"
            f"<script>self.__next_f.push([1,{json.dumps(chr(10).join(rows))}])</script>"
        )
        flight = self.spider._extract_flight_context(html, "https://www.costco.com/coffee.html")
        self.assertIsNotNone(flight)
        self.assertEqual(flight["page_size"], 24)
        self.assertEqual(
            flight["subcategories"][0]["url"],
            "https://www.costco.com/tea.html?deliveryFacetFlag=true&refine=x",
        )

    def test_empty_and_blocked_responses_do_not_yield_requests_or_items(self):
        self.assertEqual(list(self.spider.parse(self.response(self.first, "Access denied", status=403))), [])
        self.assertEqual(list(self.spider.parse(self.response(self.first, "<html></html>"))), [])
        request = self.listing_request()
        self.assertEqual(list(self.spider.parse_search(self.response(request, "[]"))), [])
        self.assertEqual(
            list(self.spider.parse_search(self.response(request, '{"searchResult":{}}'))),
            [],
        )


if __name__ == "__main__":
    unittest.main()
