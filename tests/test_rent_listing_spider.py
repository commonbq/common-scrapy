import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.rent_listing_spider import RentListingSpider


def response(listings, page=1, total=30):
    state = {"props": {"pageProps": {"pageData": {"location": {"listingSearch": {
        "listings": listings, "total": total,
    }}}}}}
    url = "https://www.rent.com/california/los-angeles-apartments"
    request = Request(url, meta={"page": page, "base_url": url})
    body = f'<script id="__NEXT_DATA__">{json.dumps(state)}</script>'
    return HtmlResponse(url, body=body, encoding="utf-8", request=request)


def test_maps_hydrated_listing():
    spider = RentListingSpider(category="los-angeles-ca")
    listing = {
        "id": "lc1", "name": "Example Apartments", "urlPathname": "/apartment/example-lc1",
        "location": {"city": "Los Angeles", "stateAbbr": "CA", "zip": "90001", "lat": 1, "lng": 2},
        "priceText": "$1,500", "priceRange": {"min": 1500, "max": 1800},
        "bedRange": {"min": 1, "max": 2},
        "floorPlans": [{"bathCount": 1, "sqFtRange": {"min": 600, "max": 800}}],
        "optimizedPhotos": [{"id": "photo-1"}],
    }
    item = list(spider.parse(response([listing])))[0]
    assert item["item_id"] == "lc1"
    assert item["url"] == "https://www.rent.com/apartment/example-lc1"
    assert item["price_min"] == 1500
    assert item["baths"] == [1]
    assert item["square_feet_max"] == 800


def test_paginates_with_server_rendered_path():
    spider = RentListingSpider(category="los-angeles-ca", max_pages=2)
    request = list(spider.parse(response([{"id": "lc1"}])))[-1]
    assert request.url.endswith("/los-angeles-apartments/page-2")


def test_deduplicates_and_stops_repeated_page():
    spider = RentListingSpider(category="los-angeles-ca", max_pages=2)
    assert len(list(spider.parse(response([{"id": "lc1"}])))) == 2
    assert list(spider.parse(response([{"id": "lc1"}], page=2))) == []


@pytest.mark.parametrize("body", ["<html></html>", '<script id="__NEXT_DATA__">{}</script>'])
def test_rejects_missing_or_invalid_hydration(body):
    spider = RentListingSpider(category="los-angeles-ca")
    request = Request("https://www.rent.com/x", meta={"page": 1, "base_url": "https://www.rent.com/x"})
    page = HtmlResponse(request.url, body=body, encoding="utf-8", request=request)
    with pytest.raises(RuntimeError):
        list(spider.parse(page))
