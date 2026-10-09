import json

from scrapy.http import HtmlResponse, Request

from common.spiders.zoro_listing_spider import ZoroListingSpider


def response_for(state, url="https://www.zoro.com/aluminum-angles/c/7577/", meta=None):
    encoded = json.dumps(json.dumps(state))
    body = f"<script>window.INITIAL_STATE = {encoded};</script>".encode()
    request = Request(url, meta=meta or {"page": 1, "base_url": url, "department": "raw-materials"})
    return HtmlResponse(url, request=request, body=body, encoding="utf-8")


PRODUCT = {
    "brand": "Zoro Select",
    "title": "Aluminum Angle",
    "product": {
        "zoroNo": "G3109732", "erpId": "293830", "mfrNo": "61A.125X2-48",
        "title": "Aluminum Angle", "brand": "Zoro Select", "slug": "angle",
        "primaryCategoryPaths": [
            {"1": "37", "2": "Raw Materials"}, {"1": "7577", "2": "Aluminum Angles"}
        ],
        "price": 17.39, "originalPrice": 20.0, "priceUnit": "EA",
        "minRetailQty": 1, "packageQty": 1,
        "attributes": [{"name": "Material", "value": "Aluminum"}],
        "media": [{"name": "product image.JPG", "type": "image/jpeg"}],
        "leadTime": 1, "isLTL": False,
    },
}


def test_extracts_products_and_schedules_hydrated_pagination():
    spider = ZoroListingSpider(category_url="https://www.zoro.com/aluminum-angles/c/7577/", max_pages=2)
    state = {"search": {"response": {
        "records": [PRODUCT], "pagination": {"totalSize": 37, "pageSize": 36}
    }}}
    output = list(spider.parse(response_for(state)))
    item = next(value for value in output if isinstance(value, dict))
    request = next(value for value in output if isinstance(value, Request))
    assert item["item_id"] == "G3109732"
    assert item["taxonomy_path"] == "Raw Materials > Aluminum Angles"
    assert item["attributes"] == {"Material": "Aluminum"}
    assert item["image_url"].endswith("product%20image.JPG")
    assert item["source"] == "zoro_initial_state_search_records"
    assert request.url.endswith("?page=2")
    assert spider.custom_settings["FEED_EXPORT_FIELDS"][-3:] == ["source", "raw", "timestamp"]


def test_department_bootstrap_resolves_only_leaf_categories():
    spider = ZoroListingSpider(category="raw-materials")
    state = {
        "category": {"categoryData": {"37": {
            "1": "37", "2": "Raw Materials", "3": "raw-materials", "b": [
                {"1": "9055", "2": "Aluminum", "3": "aluminum", "b": [
                    {"1": "7577", "2": "Aluminum Angles", "3": "aluminum-angles", "b": []}
                ]}
            ]
        }}},
        "search": {"response": {"records": []}},
    }
    requests = list(spider.parse(response_for(
        state,
        "https://www.zoro.com/raw-materials/c/37/",
        {"page": 1, "base_url": "https://www.zoro.com/raw-materials/c/37/", "department": "raw-materials"},
    )))
    assert [request.url for request in requests] == [
        "https://www.zoro.com/aluminum-angles/c/7577/"
    ]
    assert requests[0].meta["category_id"] == "7577"


def test_group_record_uses_group_url_and_fields():
    spider = ZoroListingSpider(category_url="https://www.zoro.com/socket-head-cap-screws/c/4951/")
    grouped = {**PRODUCT, "group": {
        "groupHash": "abc123", "groupName": "Socket Head Screws", "groupSkus": ["G1", "G2"]
    }}
    state = {"search": {"response": {
        "records": [grouped], "pagination": {"totalSize": 1, "pageSize": 36}
    }}}
    item = next(value for value in spider.parse(response_for(state)) if isinstance(value, dict))
    assert item["url"] == "https://www.zoro.com/angle/g/abc123/"
    assert item["group_sku_count"] == 2


def test_missing_bootstrap_fails_visibly():
    spider = ZoroListingSpider(category_url="https://www.zoro.com/test/c/1/")
    request = Request(spider.category_url, meta={"page": 1, "base_url": spider.category_url})
    response = HtmlResponse(request.url, request=request, body=b"<html>challenge</html>")
    try:
        list(spider.parse(response))
    except RuntimeError as exc:
        assert "INITIAL_STATE missing" in str(exc)
    else:
        raise AssertionError("missing bootstrap was accepted")
