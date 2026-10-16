import json
import unittest
from collections.abc import Mapping
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.lululemon_listing_spider import (
    MAX_PROXY_RETRIES,
    LululemonListingSpider,
)


class LululemonListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = LululemonListingSpider(category="women-leggings", max_pages=1)

    def response(self):
        body = Path("sample/lululemon-listing-product.html").read_text()
        request = Request("https://shop.lululemon.com/c/womens-leggings/_/N-8r6?page=1", meta={"category": "women-leggings", "page": 1})
        return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)

    def test_next_data_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "prod11860112")
        self.assertEqual(items[0]["price"], 98.0)
        self.assertEqual(items[0]["original_price"], 118.0)
        self.assertEqual(items[0]["color_count"], 2)

    def test_missing_contract_fails_visibly(self):
        request = Request("https://shop.lululemon.com/c/womens-leggings/_/N-8r6")
        response = HtmlResponse(request.url, body="<html></html>", encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "No Lululemon __NEXT_DATA__"):
            list(self.spider.parse(response))

    def test_proxy_envelope_retries_then_succeeds(self):
        # A proxy envelope is an HTTP 200 body, so parse() must re-issue the
        # request itself rather than relying on RetryMiddleware.
        spider = self.spider
        url = "https://shop.lululemon.com/c/women-leggings/n1udsq?page=1"
        envelope = b'{"status":"We couldn\'t retrieve a successful response."}'
        request = Request(
            url, meta={"category": "women-leggings", "page": 1, "proxy_retries": 0}
        )
        response = HtmlResponse(url, body=envelope, encoding="utf-8", request=request)
        issued = list(spider.parse(response))
        self.assertEqual(len(issued), 1)
        self.assertEqual(issued[0].meta["proxy_retries"], 1)
        self.assertEqual(issued[0].url, url)

    def test_proxy_envelope_fails_after_the_bound(self):
        spider = self.spider
        url = "https://shop.lululemon.com/c/women-leggings/n1udsq?page=1"
        envelope = b'{"status":"We couldn\'t retrieve a successful response."}'
        request = Request(
            url,
            meta={
                "category": "women-leggings",
                "page": 1,
                "proxy_retries": MAX_PROXY_RETRIES,
            },
        )
        response = HtmlResponse(url, body=envelope, encoding="utf-8", request=request)
        with self.assertRaisesRegex(RuntimeError, "did not return an HTML document"):
            list(spider.parse(response))

    def test_jsonapi_catalog_contract(self):
        # Lululemon re-platformed the grid onto a `catalogPageData` JSON:API
        # document; product entities live in `included` (regression: #380).
        state = {
            "props": {"pageProps": {"dehydratedState": {"queries": [
                {
                    "queryKey": [
                        "catalogPageData", "cdp",
                        {"hash": "n1udsq", "offset": 0, "pageSize": 40},
                    ],
                    "state": {"data": {"pages": [{
                        "data": {"attributes": {"totalCount": 98, "limit": 40, "offset": 0}},
                        "included": [
                            {
                                "id": "ku580lgm9e", "type": "products",
                                "attributes": {
                                    "name": 'Groove High-Rise Tight 25"',
                                    "unifiedId": "Groove-High-Rise-Tight-25",
                                    "url": "/p/groove-high-rise-tight-25/ku580lgm9e",
                                    "colors": [{"id": "75753", "url": "https://img/75753"}],
                                    "styles": [{"colors": [{
                                        "price": {"listPrice": 118, "currencyCode": "USD"},
                                        "images": [{"url": "https://img/LW5IUXS_075753_1"}],
                                        "availability": {"isAvailable": True},
                                    }]}],
                                },
                            },
                            {"id": "cat", "type": "category-page-data", "attributes": {}},
                        ],
                    }]}},
                }
            ]}}},
        }
        request = Request("https://shop.lululemon.com/c/women-leggings/n1udsq?page=1")
        body = f'<html><script id="__NEXT_DATA__" type="application/json">{json.dumps(state)}</script></html>'
        spider = LululemonListingSpider(category="women-leggings", max_pages=1)
        response = HtmlResponse(request.url, body=body.encode(), encoding="utf-8", request=request)
        items = list(spider.parse(response))
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["item_id"], "Groove-High-Rise-Tight-25")
        self.assertEqual(item["url"], "https://shop.lululemon.com/p/groove-high-rise-tight-25/ku580lgm9e")
        self.assertEqual(item["price"], 118.0)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["color_count"], 1)
        self.assertEqual(item["availability"], "InStock")
        self.assertEqual(item["source"], "next_data_category_page_query")

    def test_json_error_envelope_fails_visibly(self):
        # ScrapeOps datacenter route: HTTP 200 with a 55-byte JSON body.
        request = Request(
            "https://shop.lululemon.com/c/women-clothes/n14uwk?page=1",
            meta={"proxy_retries": MAX_PROXY_RETRIES},
        )
        body = '{\n"message": "Bad Request.", \n"errorCode": "GE401001"\n}'
        response = HtmlResponse(
            request.url, body=body.encode(), encoding="utf-8",
            headers={"Content-Type": "application/json"}, request=request,
        )
        with self.assertRaisesRegex(RuntimeError, "did not return an HTML document"):
            list(self.spider.parse(response))

    def test_categories_use_grouped_mapping_contract(self):
        self.assertIsInstance(self.spider.categories, Mapping)
        self.assertTrue(
            all(isinstance(group, Mapping) for group in self.spider.categories.values())
        )
        entries = list(self.spider.iter_categories())
        self.assertEqual(len(entries), 112)
        self.assertEqual(len({entry["category"] for entry in entries}), len(entries))
        self.assertEqual(
            self.spider.category_entry("women-leggings")["url"],
            "https://shop.lululemon.com/c/women-leggings/n1udsq",
        )


if __name__ == "__main__":
    unittest.main()
