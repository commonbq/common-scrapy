import json

import pytest
from scrapy.http import Request, TextResponse

from common.spiders.argos_categories import ARGOS_CATEGORIES
from common.spiders.argos_listing_spider import ArgosListingSpider


def response(products, *, page=1, total_pages=2):
    state = {"props": {"pageProps": {
        "productData": products,
        "productMetadata": {"currentPage": page, "totalPages": total_pages, "numberOfResults": 61},
    }}}
    body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(state)}</script>'
    base = "https://www.argos.co.uk/browse/technology/laptops/c:1054421/"
    url = ArgosListingSpider._page_url(base, page)
    request = Request(url, meta={"category": "laptops", "page": page, "base_url": base})
    return TextResponse(url, request=request, body=body, encoding="utf-8")


def product(item_id="9547021"):
    return {"id": item_id, "type": "_doc", "attributes": {
        "name": "Lenovo IdeaPad Slim 3", "brand": "Lenovo", "price": 499,
        "wasPrice": 549.99, "productId": item_id, "avgRating": 4.5,
        "reviewsCount": 17, "deliverable": True, "freeDelivery": True,
        "reservable": False, "clearance": False, "hasVariations": False,
        "specialOfferText": "Save 50 pounds", "badge": {"BADGE_VALUE": ["wow_deal"]},
    }}


def split(outputs):
    values = list(outputs)
    return [value for value in values if isinstance(value, dict)], [value for value in values if not isinstance(value, dict)]


def test_top_20_categories_are_unique():
    assert len(ARGOS_CATEGORIES) == 20
    assert len({entry["category"] for entry in ARGOS_CATEGORIES}) == 20
    assert len({entry["url"] for entry in ARGOS_CATEGORIES}) == 20


def test_hydration_mapping_feed_contract_and_path_pagination():
    spider = ArgosListingSpider(category="laptops", max_pages=2)
    items, requests = split(spider.parse(response([product()])))
    assert len(items) == 1
    assert list(items[0]) == spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert items[0]["item_id"] == "9547021"
    assert items[0]["price"] == 499.0
    assert items[0]["was_price"] == 549.99
    assert items[0]["currency"] == "GBP"
    assert items[0]["in_stock"] is True
    assert items[0]["source"] == "argos_next_data_bootstrap"
    assert requests[0].url.endswith("/c:1054421/opt/page:2/")


def test_deduplicates_across_pages_and_stops_at_last_page():
    spider = ArgosListingSpider(category="laptops", max_pages=3)
    list(spider.parse(response([product()], page=1)))
    items, requests = split(spider.parse(response([product()], page=2, total_pages=2)))
    assert items == [] and requests == []


@pytest.mark.parametrize("body,match", [
    ("<html></html>", "no __NEXT_DATA__"),
    ('<script id="__NEXT_DATA__">{bad}</script>', "malformed"),
    ('<script id="__NEXT_DATA__">{}</script>', "malformed"),
])
def test_missing_or_malformed_bootstrap_fails_loudly(body, match):
    spider = ArgosListingSpider(category="laptops")
    request = Request("https://www.argos.co.uk/browse/technology/laptops/c:1054421/", meta={"page": 1})
    result = TextResponse(request.url, request=request, body=body, encoding="utf-8")
    with pytest.raises(RuntimeError, match=match):
        list(spider.parse(result))
