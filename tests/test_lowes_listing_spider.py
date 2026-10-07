import json

from scrapy.http import HtmlResponse, Request

from common.spiders.lowes_listing_spider import LowesListingSpider
from common.spiders.retail_bootstrap_utils import extract_preloaded_state


def test_bracket_preloaded_state_and_product_mapping():
    state = {"plp": {"items": [{"omniItemId": "123", "description": "Cooler", "brand": "Acme", "imageUrl": "/a.jpg", "rating": "4.5", "reviewCount": "7"}]}}
    html = f"<script>window['__PRELOADED_STATE__'] = {json.dumps(state)}</script>"
    assert extract_preloaded_state(html) == state
    products = LowesListingSpider._product_records(state)
    assert products[0]["item_id"] == "123"
    assert products[0]["title"] == "Cooler"
    assert products[0]["rating"] == "4.5"


def test_page_url_preserves_query():
    assert LowesListingSpider._page_url("https://www.lowes.com/pl/x/1?sort=top", 2).endswith("sort=top&page=2")


def test_challenge_fails_loudly():
    spider = LowesListingSpider(category="beverage-wine-chillers")
    request = Request("https://www.lowes.com/pl/x", meta={"page": 1})
    response = HtmlResponse(request=request, url=request.url, status=200, body=b"Access Denied", encoding="utf-8")
    try:
        list(spider.parse(response))
    except RuntimeError as exc:
        assert "challenge" in str(exc)
    else:
        raise AssertionError("challenge response did not fail")
