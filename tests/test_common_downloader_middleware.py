"""Regression tests for the project-wide proxy downloader middleware."""

from __future__ import annotations

import unittest

import scrapy

from common.middlewares import CommonDownloaderMiddleware


class _FakeSettings:
    def __init__(self, values: dict) -> None:
        self._values = values

    def get(self, key, default=None):
        return self._values.get(key, default)

    def __contains__(self, key) -> bool:
        return key in self._values


class _FakeSpider:
    name = "fake"

    def __init__(self, proxy: str | None = "http://proxy.example:5353") -> None:
        self.settings = _FakeSettings({"PROXY": proxy} if proxy is not None else {})


class CommonDownloaderMiddlewareTests(unittest.TestCase):
    def setUp(self) -> None:
        self.middleware = CommonDownloaderMiddleware()

    def test_configured_proxy_applied_by_default(self) -> None:
        request = scrapy.Request("https://example.com/")
        self.middleware.process_request(request, _FakeSpider())
        self.assertEqual(request.meta["proxy"], "http://proxy.example:5353")

    def test_disable_proxy_opts_out_of_configured_proxy(self) -> None:
        request = scrapy.Request("https://redsky.target.com/", meta={"disable_proxy": True})
        self.middleware.process_request(request, _FakeSpider())
        self.assertNotIn("proxy", request.meta)

    def test_disable_proxy_drops_preset_proxy_meta(self) -> None:
        # A re-used response meta can carry the downloader's proxy URL; a
        # disable_proxy request must not inherit it and hit a 407.
        request = scrapy.Request(
            "https://redsky.target.com/",
            meta={"disable_proxy": True, "proxy": "http://proxy.example:5353"},
        )
        self.middleware.process_request(request, _FakeSpider())
        self.assertNotIn("proxy", request.meta)

    def test_explicit_request_proxy_is_preserved(self) -> None:
        request = scrapy.Request(
            "https://example.com/", meta={"proxy": "http://custom.example:8080"}
        )
        self.middleware.process_request(request, _FakeSpider())
        self.assertEqual(request.meta["proxy"], "http://custom.example:8080")

    def test_spider_settings_proxy_takes_precedence(self) -> None:
        request = scrapy.Request("https://example.com/")
        self.middleware.process_request(
            request, _FakeSpider(proxy="http://spider.example:9090")
        )
        self.assertEqual(request.meta["proxy"], "http://spider.example:9090")


if __name__ == "__main__":
    unittest.main()
