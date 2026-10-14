import json

import pytest
from scrapy.http import Request, TextResponse

from common.spiders.hm_listing_spider import HmListingSpider


def response(payload, *, page=1):
    html = '<script id="__NEXT_DATA__" type="application/json">' + json.dumps({"props": {"pageProps": {"plpProps": {"productListingSectionProps": {"productListingData": payload}}}}}) + "</script>"
    req = Request("https://www2.hm.com/en_us/ladies/new-arrivals.html", meta={"page": page, "category": "women-new-arrivals", "category_url": "https://www2.hm.com/en_us/ladies/new-arrivals.html"})
    return TextResponse(req.url, request=req, body=html, encoding="utf-8")


def product(code="1345672001"):
    return {"title": "Scarf-Detail Jacket", "articleCode": code, "pdpUrl": f"/en_us/productpage.{code}.html", "brandName": "H&M", "category": "ladies_jackets", "imageProductSrc": "https://image.hm.com/jacket.jpg", "prices": [{"priceType": "whitePrice", "price": 59.99}], "productColor": {"colorName": "Dark taupe", "hexColor": "#7B7164"}, "sizes": [{"name": "S", "stock": 2}]}


def test_extracts_hydrated_product_and_export_fields():
    spider = HmListingSpider(category="women-new-arrivals")
    results = list(spider.parse_listing(response({"hits": [product()], "pagination": {"currentPage": 1, "totalPages": 1}})))
    assert len(results) == 1
    item = results[0]
    assert item["item_id"] == "1345672001"
    assert item["price"] == 59.99
    assert item["color"] == "Dark taupe"
    assert item["availability"] == "in_stock"
    assert item["timestamp"] == spider.job_timestamp
    assert set(spider.custom_settings["FEED_EXPORT_FIELDS"]) <= set(item)


def test_sale_price_and_pagination():
    p = product()
    p["prices"].append({"priceType": "redPrice", "price": 39.99})
    spider = HmListingSpider(category="women-new-arrivals", max_pages=2)
    results = list(spider.parse_listing(response({"hits": [p], "pagination": {"currentPage": 1, "nextPageNum": 2, "totalPages": 3}})))
    assert results[0]["price"] == 39.99
    assert results[0]["regular_price"] == 59.99
    assert isinstance(results[1], Request)
    assert results[1].url.endswith("new-arrivals.html?page=2")


def test_repeated_ids_stop_without_next_request():
    spider = HmListingSpider(category="women-new-arrivals", max_pages=3)
    list(spider.parse_listing(response({"hits": [product()], "pagination": {"totalPages": 3}})))
    assert list(spider.parse_listing(response({"hits": [product()], "pagination": {"totalPages": 3}}, page=2))) == []


def test_missing_or_malformed_hydration_fails_loudly():
    spider = HmListingSpider(category="women-new-arrivals")
    req = Request("https://www2.hm.com/en_us/ladies/new-arrivals.html", meta={"page": 1, "category": "women-new-arrivals", "category_url": "x"})
    empty = TextResponse(req.url, request=req, body=b"<html></html>", encoding="utf-8")
    with pytest.raises(RuntimeError, match="missing __NEXT_DATA__"):
        list(spider.parse_listing(empty))


def test_url_override_and_all_category_mode():
    assert HmListingSpider(category="men-new-arrivals").resolve_target_url().endswith("/men/new-arrivals.html")
    spider = HmListingSpider()
    total = len(spider.available_categories())
    assert total == 122
    requests = list(spider.start_requests())
    assert len(requests) == total


def test_grouped_mapping_and_parent_selector():
    from collections.abc import Mapping
    from common.spiders.hm_categories import HM_CATEGORIES

    assert isinstance(HM_CATEGORIES, Mapping)
    assert all(isinstance(v, Mapping) for v in HM_CATEGORIES.values())
    leaves = [leaf for group in HM_CATEGORIES.values() for leaf in group]
    assert len(leaves) == len(set(leaves)) == 122
    assert all("url" in leaf_entry for group in HM_CATEGORIES.values() for leaf_entry in group.values())

    spider = HmListingSpider(category="women-categories-dresses")
    assert spider.resolve_target_url().endswith("/ladies/shop-by-product/dresses.html")
    # Department selector expands to every leaf in that group.
    entry = spider.category_entry("men-new-arrivals")
    assert entry is not None and entry["group"] == "Men"
