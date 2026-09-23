from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.ulta_listing_spider import UltaListingSpider


class UltaListingSpiderTests(unittest.TestCase):
    def _json_response(self, request: Request, payload: dict) -> TextResponse:
        return TextResponse(
            url=request.url,
            body=json.dumps(payload).encode("utf-8"),
            encoding="utf-8",
            request=request,
        )

    def test_start_requests_uses_page_discovery(self):
        spider = UltaListingSpider(category="makeup", max_pages=1)

        request = next(spider.start_requests())
        payload = json.loads(request.body.decode("utf-8"))

        self.assertEqual(request.url, spider.GRAPHQL_URL)
        self.assertEqual(request.method, "POST")
        self.assertEqual(payload["operationName"], "Page")
        self.assertEqual(
            payload["variables"]["url"]["path"],
            "https://www.ulta.com/shop/makeup/all",
        )
        self.assertEqual(request.meta["page"], 1)

    def test_parse_page_definition_uses_discovered_content_id(self):
        spider = UltaListingSpider(category="makeup", max_pages=1)
        page_request = spider._build_page_request("https://www.ulta.com/shop/makeup/all")
        response = self._json_response(
            page_request,
            {
                "data": {
                    "Page": {
                        "content": {
                            "modules": [
                                {"type": "HeroBanner", "id": "ignore-me"},
                                {
                                    "type": "ProductListingResults",
                                    "id": "live-content-id",
                                },
                            ]
                        }
                    }
                }
            },
        )

        outputs = list(spider.parse_page_definition(response))

        self.assertEqual(len(outputs), 1)
        listing_request = outputs[0]
        self.assertIsInstance(listing_request, Request)
        payload = json.loads(listing_request.body.decode("utf-8"))
        self.assertEqual(payload["operationName"], "NonCachedPage")
        self.assertIn('contentId: "live-content-id"', payload["query"])
        self.assertEqual(listing_request.meta["content_id"], "live-content-id")
        self.assertEqual(listing_request.meta["category_url"], "https://www.ulta.com/shop/makeup/all")

    def test_parse_listing_normalizes_items_and_paginates(self):
        spider = UltaListingSpider(category="makeup", max_pages=2)
        request = Request(
            url=spider.GRAPHQL_URL,
            method="POST",
            meta={
                "page": 1,
                "category_url": "https://www.ulta.com/shop/makeup/all",
                "content_id": "live-content-id",
            },
        )
        response = self._json_response(
            request,
            {
                "data": {
                    "Page": {
                        "content": {
                            "items": [
                                {
                                    "productId": "prod-1",
                                    "skuId": "sku-1",
                                    "brandName": "Ulta Beauty Collection",
                                    "productName": "Hydrating Foundation",
                                    "action": {"url": "/p/hydrating-foundation?sku=sku-1"},
                                    "image": {"imageUrl": "https://images.example/sku-1.jpg"},
                                    "listPrice": "$20.00",
                                    "salePrice": "$15.00",
                                    "rating": "4.5",
                                    "reviewCount": "123",
                                    "sponsored": True,
                                }
                            ]
                        }
                    }
                }
            },
        )

        outputs = list(spider.parse_listing(response))

        self.assertEqual(len(outputs), 2)
        item = outputs[0]
        self.assertEqual(
            item,
            {
                "category": "makeup",
                "item_id": "prod-1",
                "sku_id": "sku-1",
                "brand": "Ulta Beauty Collection",
                "title": "Hydrating Foundation",
                "url": "https://www.ulta.com/p/hydrating-foundation?sku=sku-1",
                "image_url": "https://images.example/sku-1.jpg",
                "list_price": "$20.00",
                "sale_price": "$15.00",
                "rating": 4.5,
                "reviews_count": 123,
                "is_sponsored": True,
                "source": "ulta_dxl_graphql",
                "mode": "category",
                "page": 1,
                "category_url": "https://www.ulta.com/shop/makeup/all",
            },
        )

        next_request = outputs[1]
        self.assertIsInstance(next_request, Request)
        self.assertEqual(next_request.meta["page"], 2)
        next_payload = json.loads(next_request.body.decode("utf-8"))
        self.assertIn(
            'url: {path: "https://www.ulta.com/shop/makeup/all?page=2"}',
            next_payload["query"],
        )
        self.assertIn('contentId: "live-content-id"', next_payload["query"])

    def test_parse_listing_empty_first_page_rediscovery_then_html_fallback(self):
        spider = UltaListingSpider(category="makeup", max_pages=1)
        request = Request(
            url=spider.GRAPHQL_URL,
            method="POST",
            meta={
                "page": 1,
                "category_url": "https://www.ulta.com/shop/makeup/all",
                "content_id": "expired-id",
            },
        )
        response = self._json_response(request, {"data": {"Page": {"content": {"items": []}}}})

        first_outputs = list(spider.parse_listing(response))

        self.assertEqual(len(first_outputs), 1)
        rediscovery_request = first_outputs[0]
        self.assertIsInstance(rediscovery_request, Request)
        self.assertEqual(rediscovery_request.meta["rediscovery_attempted"], True)
        self.assertEqual(rediscovery_request.callback.__name__, "parse_page_definition")

        retry_request = Request(
            url=spider.GRAPHQL_URL,
            method="POST",
            meta={
                "page": 1,
                "category_url": "https://www.ulta.com/shop/makeup/all",
                "content_id": "expired-id",
                "rediscovery_attempted": True,
            },
        )
        retry_response = self._json_response(
            retry_request, {"data": {"Page": {"content": {"items": []}}}}
        )

        second_outputs = list(spider.parse_listing(retry_response))

        self.assertEqual(len(second_outputs), 1)
        fallback_request = second_outputs[0]
        self.assertEqual(fallback_request.url, "https://www.ulta.com/shop/makeup/all")
        self.assertEqual(fallback_request.callback.__name__, "parse_html_listing")

    def test_parse_listing_rediscovery_when_next_page_content_id_missing(self):
        spider = UltaListingSpider(category="makeup", max_pages=2)
        request = Request(
            url=spider.GRAPHQL_URL,
            method="POST",
            meta={
                "page": 1,
                "category_url": "https://www.ulta.com/shop/makeup/all",
            },
        )
        response = self._json_response(
            request,
            {
                "data": {
                    "Page": {
                        "content": {
                            "items": [
                                {
                                    "productId": "prod-1",
                                    "skuId": "sku-1",
                                    "brandName": "Ulta Beauty Collection",
                                    "productName": "Hydrating Foundation",
                                    "action": {"url": "/p/hydrating-foundation?sku=sku-1"},
                                }
                            ]
                        }
                    }
                }
            },
        )

        outputs = list(spider.parse_listing(response))

        self.assertEqual(len(outputs), 2)
        rediscovery_request = outputs[1]
        self.assertIsInstance(rediscovery_request, Request)
        self.assertEqual(rediscovery_request.callback.__name__, "parse_page_definition")
        self.assertEqual(rediscovery_request.meta["page"], 2)
        payload = json.loads(rediscovery_request.body.decode("utf-8"))
        self.assertEqual(payload["operationName"], "Page")
        self.assertEqual(
            payload["variables"]["url"]["path"],
            "https://www.ulta.com/shop/makeup/all",
        )

    def test_parse_listing_non_json_after_rediscovery_stops_retry_loop(self):
        spider = UltaListingSpider(category="makeup", max_pages=1)
        request = Request(
            url=spider.GRAPHQL_URL,
            method="POST",
            meta={
                "page": 1,
                "category_url": "https://www.ulta.com/shop/makeup/all",
                "content_id": "live-content-id",
                "rediscovery_attempted": True,
            },
        )
        response = TextResponse(
            url=request.url,
            body=b"<html>blocked</html>",
            encoding="utf-8",
            request=request,
        )

        outputs = list(spider.parse_listing(response))

        self.assertEqual(len(outputs), 1)
        fallback_request = outputs[0]
        self.assertEqual(fallback_request.callback.__name__, "parse_html_listing")


if __name__ == "__main__":
    unittest.main()
