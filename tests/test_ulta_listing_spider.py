import json
import unittest

from scrapy.http import TextResponse
from scrapy.utils.request import fingerprint
from twisted.python.failure import Failure

from common.spiders.ulta_listing_spider import UltaListingSpider


class UltaListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = UltaListingSpider(category="makeup", max_pages=3)
        self.first = next(self.spider.start_requests())

    def response(self, request, content=None, *, body=None, status=200):
        if body is None:
            body = json.dumps({"data": {"Page": {"content": content}}})
        return TextResponse(
            request.url,
            request=request,
            body=body.encode(),
            encoding="utf-8",
            status=status,
        )

    def discover(self, request=None, content_id="live-module"):
        request = request or self.first
        content = {
            "modules": [
                {"type": "Banner", "id": "wrong"},
                {"children": [{"type": "ProductListingResults", "id": content_id}]},
            ]
        }
        return next(self.spider.parse_page_definition(self.response(request, content)))

    def card(self, sku="123"):
        return {
            "productId": "pimprod1",
            "skuId": sku,
            "brandName": "Brand",
            "productName": "Mascara",
            "action": {"url": "/p/mascara-pimprod1?sku=" + sku},
            "image": {"imageUrl": "https://media.ultainc.com/i/ulta/123"},
            "listPrice": "$20",
            "salePrice": "$15",
            "rating": "4.5",
            "reviewCount": "1,234",
            "sponsored": False,
        }

    def test_dictionary_categories_resolve_and_preserve_url_overrides(self):
        from common_scrapy.cli import _available_categories

        self.assertEqual(
            _available_categories(UltaListingSpider), self.spider.available_categories()
        )
        for category, url in UltaListingSpider.categories.items():
            self.assertEqual(
                UltaListingSpider(category=category).resolve_target_url(), url
            )
        with self.assertRaisesRegex(ValueError, "Available categories:.*makeup"):
            UltaListingSpider()
        with self.assertRaisesRegex(ValueError, "Unknown category"):
            UltaListingSpider(category="unknown").resolve_target_url()
        spider = UltaListingSpider(
            category="custom",
            category_url="https://www.ulta.com/shop/custom",
            url="https://www.ulta.com/shop/override",
        )
        self.assertEqual(
            spider.resolve_target_url(), "https://www.ulta.com/shop/override"
        )
        spider.url = None
        self.assertEqual(
            spider.resolve_target_url(), "https://www.ulta.com/shop/custom"
        )

    def test_discovery_uses_full_url_and_empty_runtime_parameters(self):
        payload = json.loads(self.first.body)
        self.assertEqual(self.first.method, "POST")
        self.assertEqual(payload["operationName"], "Page")
        self.assertEqual(
            payload["variables"],
            {
                "moduleParams": {},
                "url": {"path": "https://www.ulta.com/shop/makeup/all"},
            },
        )
        self.assertEqual(self.first.headers["x-ulta-dxl-query-id"], b"Page")
        listing = self.discover()
        self.assertEqual(listing.meta["content_id"], "live-module")
        self.assertEqual(
            json.loads(listing.body)["variables"]["moduleParams"],
            {"breakpoint": "XL", "loginStatus": "anonymous"},
        )
        self.assertIn('contentId: "live-module"', json.loads(listing.body)["query"])
        self.assertEqual(listing.headers["x-ulta-dxl-query-id"], b"NonCachedPage")

    def test_parsing_and_distinct_pagination_preserve_context(self):
        self.first.meta.update(cookiejar="session", proxy="http://localhost:8080")
        listing = self.discover()
        item, following = list(
            self.spider.parse_listing(self.response(listing, {"items": [self.card()]}))
        )
        self.assertEqual(item, {**self.card(), "category": "makeup"})
        self.assertEqual(following.meta["page"], 2)
        self.assertEqual(following.meta["cookiejar"], "session")
        self.assertNotIn("proxy", following.meta)
        self.assertEqual(following.meta["content_id"], "live-module")
        self.assertIn("?page=2", json.loads(following.body)["query"])
        self.assertNotEqual(fingerprint(listing), fingerprint(following))
        outputs = list(
            self.spider.parse_listing(
                self.response(following, {"items": [self.card("456")]})
            )
        )
        self.assertEqual(outputs[0]["skuId"], "456")
        self.assertEqual(outputs[1].meta["page"], 3)
        self.assertEqual(
            list(
                self.spider.parse_listing(
                    self.response(outputs[1], {"items": [self.card("789")]})
                )
            )[0]["skuId"],
            "789",
        )

    def test_followup_reapplies_authenticated_proxy(self):
        from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
        from scrapy.settings import Settings
        from common.middlewares import CommonDownloaderMiddleware

        self.spider.settings = Settings(
            {"PROXY": "http://user:password@localhost:8080"}
        )
        project_proxy = CommonDownloaderMiddleware()
        http_proxy = HttpProxyMiddleware()
        project_proxy.process_request(self.first, self.spider)
        http_proxy.process_request(self.first, self.spider)
        self.assertEqual(self.first.meta["proxy"], "http://localhost:8080")
        authorization = self.first.headers["Proxy-Authorization"]
        following = self.discover()
        self.assertNotIn("_auth_proxy", following.meta)
        project_proxy.process_request(following, self.spider)
        http_proxy.process_request(following, self.spider)
        self.assertEqual(following.headers["Proxy-Authorization"], authorization)

    def test_repeated_products_stop_pagination(self):
        listing = self.discover()
        _, following = list(
            self.spider.parse_listing(self.response(listing, {"items": [self.card()]}))
        )
        self.assertEqual(
            list(
                self.spider.parse_listing(
                    self.response(following, {"items": [self.card()]})
                )
            ),
            [],
        )

    def test_empty_first_page_rediscovers_once(self):
        listing = self.discover()
        retry = next(self.spider.parse_listing(self.response(listing, {"items": []})))
        self.assertEqual(json.loads(retry.body)["operationName"], "Page")
        self.assertTrue(retry.dont_filter)
        self.assertTrue(retry.meta["dont_cache"])
        self.assertTrue(retry.meta["dont_retry"])
        renewed = self.discover(retry, "renewed-module")
        self.assertEqual(renewed.meta["content_id"], "renewed-module")
        self.assertEqual(
            list(self.spider.parse_listing(self.response(renewed, {"items": []}))), []
        )

    def test_empty_later_page_terminates(self):
        listing = self.discover()
        listing.meta["page"] = 2
        self.assertEqual(
            list(self.spider.parse_listing(self.response(listing, {"items": []}))), []
        )

    def test_invalid_and_blocked_responses_never_request_html(self):
        for request in (self.first, self.discover()):
            for body, status in (
                ("Access denied", 403),
                ("<html></html>", 200),
                ('{"data": null}', 200),
                ("[]", 200),
                ('{"errors": [{"message": "bad"}]}', 200),
                ('{"data":{"Page":{"content": {}}}}', 200),
            ):
                with self.subTest(callback=request.callback, body=body):
                    response = self.response(request, body=body, status=status)
                    self.assertEqual(list(request.callback(response)), [])

    def test_network_failure_terminates(self):
        failure = Failure(TimeoutError("timeout"))
        failure.request = self.first
        self.assertIsNone(self.spider._request_failed(failure))

    def test_page_query_parameters_and_escaping(self):
        path = "https://www.ulta.com/shop/makeup/all?sort=new&page=8&filter="
        self.assertEqual(
            self.spider._with_page(path, 1),
            "https://www.ulta.com/shop/makeup/all?sort=new&filter=",
        )
        self.assertEqual(
            self.spider._with_page(path, 2),
            "https://www.ulta.com/shop/makeup/all?sort=new&filter=&page=2",
        )
        self.assertIn(
            json.dumps('id"quoted'),
            self.spider._build_payload(path, 'id"quoted')["query"],
        )


if __name__ == "__main__":
    unittest.main()
