import json

from scrapy.http import HtmlResponse, Request

from common.spiders.zumper_listing_spider import ZumperListingSpider


def response_for(state):
    request = Request("https://www.zumper.com/apartments-for-rent/new-york-ny", meta={"page": 1, "base_url": "https://www.zumper.com/apartments-for-rent/new-york-ny"})
    html = "<script>window.__PRELOADED_STATE__ = " + json.dumps(state) + "</script>" + (" " * 5000)
    return HtmlResponse(request=request, url=request.url, body=html.encode(), encoding="utf-8")


def test_bootstrap_only_mapping():
    state = {
        "currentSearch": {"hasMoreListables": False, "firstPageCount": 1, "listables": {"featured": [{"listing_id": 7, "pb_id": 42, "building_name": "Tower", "url": "/apartment-buildings/p42/tower", "min_price": 2000, "image_ids": [9]}]}},
        "geo": {"cities": [{"city_id": 2185, "name": "New York", "state": "NY", "listing_count": 10}]},
    }
    spider = ZumperListingSpider(category="new-york-ny")
    items = list(spider.parse(response_for(state)))
    assert len(items) == 1
    assert items[0]["item_id"] == "42"
    assert items[0]["title"] == "Tower"
    assert items[0]["image_urls"] == ["https://img.zumpercdn.com/9/1280x960"]
    assert items[0]["source"] == "zumper_preloaded_state"


def test_page_url_preserves_query():
    assert ZumperListingSpider._page_url("https://www.zumper.com/x?beds=1", 2).endswith("beds=1&page=2")


def test_challenge_fails_loudly():
    spider = ZumperListingSpider(category="new-york-ny")
    request = Request("https://www.zumper.com/x", meta={"page": 1})
    response = HtmlResponse(request=request, url=request.url, body=b"Access Denied", encoding="utf-8")
    try:
        list(spider.parse(response))
    except RuntimeError as exc:
        assert "challenge" in str(exc)
    else:
        raise AssertionError("challenge response did not fail")
