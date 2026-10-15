# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from datetime import datetime

from scrapy import signals

from common.settings import PROXY

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CommonSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for item_or_request in result:
            yield self._ensure_timestamp(item_or_request, spider)

    async def process_spider_output_async(self, response, result, spider):
        async for item_or_request in result:
            yield self._ensure_timestamp(item_or_request, spider)

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield self._ensure_timestamp(item_or_request, None)

    @staticmethod
    def _ensure_timestamp(item_or_request, spider):
        if not ItemAdapter.is_item(item_or_request):
            return item_or_request

        adapter = ItemAdapter(item_or_request)
        if "timestamp" in adapter:
            return item_or_request

        get_timestamp = getattr(spider, "get_timestamp", None)
        adapter["timestamp"] = (
            get_timestamp() if callable(get_timestamp) else datetime.utcnow()
        )
        return item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CommonDownloaderMiddleware:
    """Project-wide downloader middleware.

    Enforces routing through settings.PROXY when configured.
    """

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Spiders opt individual requests out of proxy routing with
        # meta["disable_proxy"] = True (first-party JSON APIs reachable directly,
        # e.g. Target RedSky and the Barnes & Noble Storefront API). Honour that
        # opt-out instead of forcing PROXY onto the request: a tunnel through
        # ScrapeOps for those hosts is rejected with a 407 and the spider then
        # scrapes 0 items, so `item_scraped_count` is missing from the run logs.
        if request.meta.get("disable_proxy"):
            request.meta.pop("proxy", None)
            return None

        if not request.meta.get("proxy"):
            proxy = spider.settings.get("PROXY") if "PROXY" in spider.settings else PROXY
            if proxy:
                request.meta["proxy"] = proxy

        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        return None

    def spider_opened(self, spider):
        if spider.settings.get("PROXY", PROXY):
            spider.logger.info("Spider opened: %s (proxy enabled)", spider.name)
        else:
            spider.logger.info("Spider opened: %s (proxy disabled)", spider.name)
