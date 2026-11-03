import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from scrapy import Request, Spider
from scrapy.http import HtmlResponse
from scrapy.settings import Settings

from common.middlewares import CommonDownloaderMiddleware, CommonSpiderMiddleware
from common.spiders.base_listing_spider import BaseListingSpider


class DummyListingSpider(BaseListingSpider):
    name = "dummy_listing"
    categories = {"all": {"test": "https://example.com"}}


class DummySpider(Spider):
    name = "dummy"


class CommonDownloaderMiddlewareTests(unittest.TestCase):
    def setUp(self):
        self.middleware = CommonDownloaderMiddleware()
        self.spider = SimpleNamespace(settings=Settings({"PROXY": "http://default-proxy"}))

    @patch.dict(os.environ, {"RETRY_PROXY_1": "http://retry-proxy-1"}, clear=False)
    def test_retry_proxy_overrides_existing_proxy(self):
        request = Request(
            "https://example.com",
            meta={"proxy": "http://original-proxy", "retries": 1},
        )

        self.middleware.process_request(request, self.spider)

        self.assertEqual(request.meta["proxy"], "http://retry-proxy-1")

    @patch.dict(os.environ, {}, clear=True)
    def test_retry_without_matching_proxy_preserves_existing_proxy(self):
        request = Request(
            "https://example.com",
            meta={"proxy": "http://original-proxy", "retries": 2},
        )

        self.middleware.process_request(request, self.spider)

        self.assertEqual(request.meta["proxy"], "http://original-proxy")

    @patch.dict(os.environ, {"RETRY_PROXY_2": "http://retry-proxy-2"}, clear=False)
    def test_retry_number_selects_matching_proxy(self):
        request = Request("https://example.com", meta={"retries": 2})

        self.middleware.process_request(request, self.spider)

        self.assertEqual(request.meta["proxy"], "http://retry-proxy-2")

    @patch.dict(os.environ, {"RETRY_PROXY_0": "http://unused-retry-proxy"}, clear=False)
    def test_initial_request_uses_default_proxy(self):
        request = Request("https://example.com", meta={"retries": 0})

        self.middleware.process_request(request, self.spider)

        self.assertEqual(request.meta["proxy"], "http://default-proxy")


class CommonSpiderMiddlewareTests(unittest.TestCase):
    def setUp(self):
        self.middleware = CommonSpiderMiddleware()
        self.spider = DummyListingSpider(category="test")
        self.spider.settings = Settings({"MAX_RETRIES": 0})

    @staticmethod
    def response(meta=None):
        request = Request("https://example.com/products", meta=meta or {})
        return HtmlResponse(request.url, request=request, body=b"<html></html>")

    def test_retries_listing_runtime_error_once(self):
        response = self.response()

        result = self.middleware.process_spider_exception(
            response, RuntimeError("required element missing"), self.spider
        )

        self.assertEqual(len(result), 1)
        retry_request = result[0]
        self.assertEqual(retry_request.url, response.url)
        self.assertTrue(retry_request.dont_filter)
        self.assertTrue(retry_request.meta["dont_cache"])
        self.assertEqual(retry_request.meta[self.middleware.RETRY_KEY], 1)

    def test_second_listing_runtime_error_propagates(self):
        response = self.response({self.middleware.RETRY_KEY: 1})

        result = self.middleware.process_spider_exception(
            response, RuntimeError("still missing"), self.spider
        )

        self.assertIsNone(result)

    def test_uses_spider_max_retries_setting(self):
        self.spider.settings.set("MAX_RETRIES", 2, priority="spider")
        response = self.response({self.middleware.RETRY_KEY: 1})

        result = self.middleware.process_spider_exception(
            response, RuntimeError("still missing"), self.spider
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].meta[self.middleware.RETRY_KEY], 2)

    def test_does_not_retry_other_exception_types(self):
        result = self.middleware.process_spider_exception(
            self.response(), ValueError("invalid input"), self.spider
        )

        self.assertIsNone(result)

    def test_does_not_retry_non_listing_spider(self):
        result = self.middleware.process_spider_exception(
            self.response(), RuntimeError("required element missing"), DummySpider()
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
