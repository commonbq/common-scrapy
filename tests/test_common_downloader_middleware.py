import unittest

from scrapy.http import Request
from scrapy.settings import Settings

from common.middlewares import CommonDownloaderMiddleware


class _Spider:
    """Minimal spider stub exposing the settings the middleware reads."""

    def __init__(self, settings):
        self.settings = settings
        self.name = "stub"


class CommonDownloaderMiddlewareTests(unittest.TestCase):
    def test_applies_configured_proxy_by_default(self):
        settings = Settings({"PROXY": "http://user:pass@proxy.test:5353"})
        spider = _Spider(settings)

        request = Request("https://example.test/")
        CommonDownloaderMiddleware().process_request(request, spider)

        self.assertEqual(request.meta["proxy"], "http://user:pass@proxy.test:5353")

    def test_disable_proxy_opts_request_out_of_proxy_routing(self):
        """A request with disable_proxy must reach its host directly.

        Target RedSky and the Barnes & Noble Storefront API are first-party
        JSON endpoints reached directly; tunnelling them through ScrapeOps is
        rejected (407) and the spider previously scraped 0 items because this
        opt-out was ignored. Regression guard for issue #388 / #373.
        """
        settings = Settings({"PROXY": "http://user:pass@proxy.test:5353"})
        spider = _Spider(settings)

        request = Request(
            "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2",
            meta={"disable_proxy": True},
        )
        CommonDownloaderMiddleware().process_request(request, spider)

        self.assertNotIn("proxy", request.meta)

    def test_disable_proxy_does_not_override_an_explicit_proxy(self):
        settings = Settings({"PROXY": "http://user:pass@proxy.test:5353"})
        spider = _Spider(settings)

        request = Request(
            "https://example.test/",
            meta={"disable_proxy": True, "proxy": "http://explicit.test:8080"},
        )
        CommonDownloaderMiddleware().process_request(request, spider)

        self.assertEqual(request.meta["proxy"], "http://explicit.test:8080")


if __name__ == "__main__":
    unittest.main()
