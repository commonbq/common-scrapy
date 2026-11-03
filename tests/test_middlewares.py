import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from scrapy import Request
from scrapy.settings import Settings

from common.middlewares import CommonDownloaderMiddleware


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


if __name__ == "__main__":
    unittest.main()
