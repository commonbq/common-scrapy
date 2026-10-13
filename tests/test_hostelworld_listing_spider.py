import json

from scrapy.http import Request, TextResponse

from common.spiders.hostelworld_categories import HOSTELWORLD_CATEGORIES
from common.spiders.hostelworld_listing_spider import HostelworldListingSpider


def response_for(properties, *, page=1, pages=1, success=True):
    payload = {"success": success, "data": {
        "name": "London", "country": "England", "continent": "Europe",
        "totalPropertiesCount": 31, "numberOfPages": pages, "page": page,
        "properties": properties,
    }}
    request = Request("https://prod.apigee.hostelworld.com/api", meta={
        "category": "london-england", "city_id": 3, "page": page,
    })
    return TextResponse(request.url, request=request, status=200, encoding="utf-8", body=json.dumps(payload).encode())


def property_record(item_id):
    return {
        "id": item_id, "name": "Generator London", "type": "HOSTEL",
        "urlFriendlyName": "generator-london", "address": "Compton Place",
        "avgRating": 7, "numberReviews": 9468, "cityCenterDistance": 2.97,
        "hasAvailability": True, "image": {"medium": "img.example/hostel.jpg"},
        "sharedMinPrice": {"value": 23.2, "currency": "USD"},
        "privateMinPrice": {"value": 27.77, "currency": "USD"},
        "geoCoordinates": {"latitude": 51.52, "longitude": -0.12},
        "badges": [{"badgeName": "Free WiFi"}],
    }


def test_categories_mapping_contract():
    from collections.abc import Mapping

    assert isinstance(HOSTELWORLD_CATEGORIES, Mapping)
    assert all(isinstance(v, Mapping) for v in HOSTELWORLD_CATEGORIES.values())
    # 6 continent groups, every leaf rich (url + numeric city_id).
    assert len(HOSTELWORLD_CATEGORIES) == 6
    leaves = [leaf for group in HOSTELWORLD_CATEGORIES.values() for leaf in group]
    assert len(leaves) == len(set(leaves)) == 3520
    assert all({"url", "city_id"} <= set(leaf) for group in HOSTELWORLD_CATEGORIES.values()
               for leaf in group.values())

    spider = HostelworldListingSpider(category="london-england")
    assert len(spider.available_categories()) == 3520
    assert spider.custom_settings["FEED_EXPORT_FIELDS"][0:3] == ["item_id", "url", "name"]
    assert "raw" in spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert "timestamp" in spider.custom_settings["FEED_EXPORT_FIELDS"]


def test_leaf_lookup_across_groups_and_all_expansion():
    spider = HostelworldListingSpider(category="london-england")
    entry = spider.category_entry("london-england")
    assert entry["group"] == "Europe" and entry["city_id"] == 3

    all_spider = HostelworldListingSpider(category="all")
    requests = list(all_spider.start_requests())
    assert len(requests) == 3520


def test_unknown_category_is_rejected_visibly():
    import pytest

    with pytest.raises(ValueError, match="Unknown category 'new-york'"):
        HostelworldListingSpider(category="new-york")
    spider = HostelworldListingSpider(category="london-england")
    assert spider.category_entry("new-york") is None


def test_api_only_start_request_has_required_headers_and_no_proxy():
    request = next(HostelworldListingSpider(category="new-york-usa").start_requests())
    assert "/13/properties/" in request.url and "page=1" in request.url
    assert request.headers["Accept"] == b"application/json"
    assert request.meta["dont_proxy"] is True


def test_custom_url_resolves_to_known_city():
    spider = HostelworldListingSpider(
        url="https://www.hostelworld.com/hostels/europe/england/london/"
    )
    request = next(spider.start_requests())
    assert "/3/properties/" in request.url


def test_mapping_dedup_and_paging():
    spider = HostelworldListingSpider(category="london-england", max_pages="2")
    records = [property_record(510), property_record(510)] + [property_record(i) for i in range(511, 539)]
    output = list(spider.parse(response_for(records, pages=2)))
    items = [value for value in output if isinstance(value, dict)]
    requests = [value for value in output if isinstance(value, Request)]
    assert len(items) == 29
    assert items[0]["item_id"] == "510"
    assert items[0]["price_shared"] == 23.2 and items[0]["badges"] == ["Free WiFi"]
    assert items[0]["source"] == "hostelworld_city_properties_api"
    assert items[0]["raw"]["id"] == 510
    assert "timestamp" in items[0]
    assert len(requests) == 1 and "page=2" in requests[0].url


def test_error_and_short_page_stop_without_false_items():
    spider = HostelworldListingSpider(category="london-england", max_pages="4")
    assert list(spider.parse(response_for([], pages=4))) == []
    assert list(spider.parse(response_for([property_record(1)], pages=4, success=False))) == []
