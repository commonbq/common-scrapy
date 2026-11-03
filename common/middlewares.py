# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
from datetime import datetime

from scrapy import signals

from common.settings import PROXY

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CommonSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    RETRY_KEY = "retries"

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
        # Import lazily so loading project middleware does not introduce a
        # module-level dependency on every listing spider's base class.
        from common.spiders.base_listing_spider import BaseListingSpider

        if not isinstance(spider, BaseListingSpider):
            return None
        if not isinstance(exception, RuntimeError):
            return None

        retry_count = int(response.meta.get(self.RETRY_KEY, 0))
        max_retries = spider.settings.getint("MAX_RETRIES", 2)
        if retry_count > max_retries:
            return None

        retry_request = response.request.copy()
        retry_request.dont_filter = True
        retry_request.meta["dont_cache"] = True
        retry_request.meta[self.RETRY_KEY] = retry_count + 1
        spider.logger.warning(
            "Retrying after RuntimeError (%s): %s",
            exception,
            response.url,
        )
        return [retry_request]

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
        retries = int(request.meta.get("retries", 0))
        retry_proxy = os.environ.get(f"RETRY_PROXY_{retries}") if retries > 0 else None
        if retry_proxy:
            spider.logger.info(
                "Using retry proxy for request %s (retry count: %d)",
                request.url,
                retries,
            )
            request.meta["proxy"] = retry_proxy
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
