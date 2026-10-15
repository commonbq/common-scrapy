"""Regression tests for the project-wide downloader proxy policy."""

from __future__ import annotations

import unittest

from scrapy import Request, Spider
from scrapy.settings import Settings

from common.middlewares import CommonDownloaderMiddleware


class DownloaderMiddlewareProxyTests(unittest.TestCase):
    def make_spider(self, proxy: str | None) -> Spider:
        spider = Spider(name="proxy-test")
        settings = Settings()
        settings.set("PROXY", proxy)
        spider.settings = settings
        return spider

    def test_applies_configured_proxy_by_default(self):
        middleware = CommonDownloaderMiddleware()
        spider = self.make_spider("http://proxy.example:9999")
        request = Request("https://example.com/plain")
        middleware.process_request(request, spider)
        self.assertEqual(request.meta.get("proxy"), "http://proxy.example:9999")

    def test_disable_proxy_opts_out_of_the_configured_proxy(self):
        middleware = CommonDownloaderMiddleware()
        spider = self.make_spider("http://proxy.example:9999")
        request = Request("https://example.com/api", meta={"disable_proxy": True})
        middleware.process_request(request, spider)
        self.assertNotIn("proxy", request.meta)

    def test_disable_proxy_drops_a_pre_existing_proxy_meta(self):
        middleware = CommonDownloaderMiddleware()
        spider = self.make_spider("http://proxy.example:9999")
        request = Request(
            "https://example.com/api",
            meta={"disable_proxy": True, "proxy": "http://proxy.example:9999"},
        )
        middleware.process_request(request, spider)
        self.assertNotIn("proxy", request.meta)

    def test_explicit_request_proxy_is_preserved(self):
        middleware = CommonDownloaderMiddleware()
        spider = self.make_spider("http://proxy.example:9999")
        request = Request(
            "https://example.com/plain", meta={"proxy": "http://direct.example:1"}
        )
        middleware.process_request(request, spider)
        self.assertEqual(request.meta.get("proxy"), "http://direct.example:1")


if __name__ == "__main__":
    unittest.main()
