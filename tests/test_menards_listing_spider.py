import json

from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.menards_listing_spider import MenardsListingSpider


def response(url, body, *, meta=None, content_type="application/json"):
    request = Request(url, meta=meta or {})
    cls = HtmlResponse if content_type == "text/html" else TextResponse
    return cls(url, request=request, body=body.encode(), encoding="utf-8",
               headers={"Content-Type": content_type})


def test_category_get_builds_api_request():
    spider = MenardsListingSpider(category="halloween-animated-decorations")
    first = next(spider.start_requests())
    request = next(spider.parse_category(response(first.url, "<html></html>", meta=first.meta, content_type="text/html")))
    assert request.method == "POST"
    assert json.loads(request.body) == {"categoryId": "19081", "firstRequest": True, "page": 1,
                                        "sortBy": "BEST_MATCH", "selectedFacets": [], "inStockToday": False}
    assert request.headers["Referer"].decode() == first.url


def test_api_items_deduplicate_and_paginate():
    spider = MenardsListingSpider(category="halloween-animated-decorations", max_pages="2")
    meta = {"category_id": "19081", "category": spider.category,
            "category_url": spider.resolve_target_url(), "page": 1}
    product = {"productId": "123", "sku": "SKU123", "name": "Animated Dragon", "brandName": "Enchanted Forest",
               "productUrl": "/main/p-123.htm", "imageUrl": "https://img/123.jpg",
               "price": {"current": "$99.99", "regular": "129.99", "currency": "USD"},
               "availability": "IN_STOCK", "rating": {"value": 4.5, "count": 12}}
    out = list(spider.parse_api(response(spider.api_url,
        json.dumps({"searchResult": {"items": [product, product], "totalItems": 4}}), meta=meta)))
    assert out[0]["item_id"] == "123"
    assert out[0]["price"] == 99.99
    assert out[0]["reviews_count"] == 12
    assert out[0]["raw"] == product
    assert out[0]["timestamp"] == spider.job_timestamp
    assert "timestamp" in MenardsListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
    assert "raw" in MenardsListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
    assert out[1].meta["page"] == 2
    assert json.loads(out[1].body)["firstRequest"] is False


def test_challenge_and_missing_contract_fail_loudly():
    spider = MenardsListingSpider(category="halloween-animated-decorations")
    blocked = response(spider.api_url, "<html>Incapsula captcha</html>", content_type="text/html")
    try:
        list(spider.parse_api(blocked))
        assert False
    except RuntimeError as exc:
        assert "blocked" in str(exc)

