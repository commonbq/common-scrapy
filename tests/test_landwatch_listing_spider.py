from __future__ import annotations

import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.landwatch_categories import LANDWATCH_CATEGORIES
from common.spiders.landwatch_listing_spider import LandwatchListingSpider


URL = "https://www.landwatch.com/texas-land-for-sale"


def _response(*, products=None, next_link=None, status=200):
    state = {
        "searchPage": {
            "searchResults": {
                "propertyResults": products if products is not None else [_product()],
                "totalCount": 99,
                "paginationData": {"nextLink": next_link},
            }
        }
    }
    body = (
        '<script id="__SERVER_STATE__" type="application/json">'
        + json.dumps(state)
        + "</script>"
    )
    request = Request(URL, meta={"page": 1, "category": "texas"})
    return HtmlResponse(URL, body=body, encoding="utf-8", status=status, request=request)


def _product():
    return {
        "siteListingId": 427783557,
        "id": 28381042,
        "title": "Superior Views, Better Hunting",
        "canonicalUrl": "/edwards-county-texas-farms-and-ranches-for-sale/pid/427783557",
        "thumbnailDocumentId": 6406409951,
        "price": 769950,
        "pricePerAcre": 7122.57,
        "priceChangeAmount": -10000,
        "acres": 108.1,
        "acresDisplay": "108 acres",
        "types": ["Farms and Ranches", "Hunting Property", "House"],
        "address": "7997 SD 5200",
        "city": "Rocksprings",
        "county": "Edwards County",
        "state": "Texas",
        "stateAbbreviation": "TX",
        "zip": "78880",
        "latitude": 30.1,
        "longitude": -100.2,
        "beds": 3,
        "baths": 1,
        "halfBaths": 0,
        "homesqft": 934,
        "brokerName": "Glynn Hendley",
        "brokerCompany": "Western Hill Country Realty",
        "brokerPhone": "(830) 532-7205",
        "brokerCanonicalUrl": "/profile/glynn-hendley/4657",
        "hasHouse": True,
        "hasVideo": True,
        "hasVirtualTour": False,
        "imageCount": 91,
        "lastUpdated": "2026-10-07T10:44:06.903",
    }


def test_categories_are_the_twenty_unique_state_seeds():
    assert len(LANDWATCH_CATEGORIES) == 20
    assert len({entry["url"] for entry in LANDWATCH_CATEGORIES}) == 20
    assert LANDWATCH_CATEGORIES[0]["category"] == "texas"


def test_bootstrap_maps_rich_property_fields():
    spider = LandwatchListingSpider(category="texas")
    output = list(spider.parse(_response()))
    assert len(output) == 1
    item = output[0]
    assert item["item_id"] == "427783557"
    assert item["title"] == "Superior Views, Better Hunting"
    assert item["price"] == 769950
    assert item["acres"] == 108.1
    assert item["beds"] == 3
    assert item["broker_company"] == "Western Hill Country Realty"
    assert item["url"].endswith("/pid/427783557")
    assert item["source"] == "landwatch_server_state_bootstrap"


def test_export_fields_match_item_contract_except_middleware_timestamp():
    spider = LandwatchListingSpider(category="texas")
    item = list(spider.parse(_response()))[0]
    fields = set(spider.custom_settings["FEED_EXPORT_FIELDS"])
    assert set(item) == fields - {"timestamp"}


def test_pagination_uses_hydrated_next_link():
    spider = LandwatchListingSpider(category="texas", max_pages=2)
    output = list(spider.parse(_response(next_link="/texas-land-for-sale/page-2")))
    assert output[-1].url == "https://www.landwatch.com/texas-land-for-sale/page-2"
    assert output[-1].meta["page"] == 2


def test_duplicate_ids_are_suppressed():
    spider = LandwatchListingSpider(category="texas")
    assert len(list(spider.parse(_response()))) == 1
    assert list(spider.parse(_response())) == []


def test_missing_bootstrap_fails_loudly():
    request = Request(URL, meta={"page": 1, "category": "texas"})
    response = HtmlResponse(URL, body=b"<html>blocked</html>", request=request)
    with pytest.raises(RuntimeError, match="__SERVER_STATE__"):
        list(LandwatchListingSpider(category="texas").parse(response))
