from datetime import datetime

import scrapy
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings

from common.middlewares import CommonSpiderMiddleware
from common.spiders.base_listing_spider import BaseListingSpider


class TimestampSpider(scrapy.Spider):
    name = "timestamp_test"

    def get_timestamp(self):
        return datetime(2026, 10, 5, 12, 30)


class DirectYieldSpider(BaseListingSpider):
    name = "direct_yield_test"
    categories = [{"category": "test", "url": "https://example.com"}]

    def parse(self, response):
        yield {"name": "direct"}


def test_every_spider_exports_timestamp():
    loader = SpiderLoader.from_settings(get_project_settings())

    for spider_name in loader.list():
        custom_settings = loader.load(spider_name).custom_settings or {}
        assert "FEED_EXPORT_FIELDS" in custom_settings, spider_name
        assert "timestamp" in custom_settings["FEED_EXPORT_FIELDS"], spider_name


def test_spider_middleware_adds_timestamp_to_every_item():
    spider = TimestampSpider()
    request = scrapy.Request("https://example.com")
    original_timestamp = datetime(2025, 1, 1)
    outputs = list(
        CommonSpiderMiddleware().process_spider_output(
            None,
            [
                {"name": "new"},
                {"name": "existing", "timestamp": original_timestamp},
                request,
            ],
            spider,
        )
    )

    assert outputs[0]["timestamp"] == spider.get_timestamp()
    assert outputs[1]["timestamp"] == original_timestamp
    assert outputs[2] is request


def test_direct_spider_callback_yields_timestamp():
    spider = DirectYieldSpider(category="test")

    item = next(spider.parse(None))

    assert item["timestamp"] == spider.job_timestamp
