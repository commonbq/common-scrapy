import json

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.hotpads_listing_spider import HotPadsListingSpider


def html(buildings, total_pages=2):
    state = {"listings": {"buildings": buildings, "numUnits": 123},
             "totalPages": total_pages,
             "initialParams": {"area": {"areaId": "42", "city": "New York", "state": "NY"}}}
    flight = f'0:["$",{{"initialListingsData":{json.dumps(state)}}}]'
    script = f"self.__next_f.push([1,{json.dumps(flight)}])"
    return "<html><body>" + ("x" * 5000) + f"<script>{script}</script></body></html>"


def response(body, page=1):
    url = "https://hotpads.com/new-york-ny/apartments-for-rent"
    request = Request(url, meta={"page": page, "base_url": url, "category": "new-york-ny"})
    return HtmlResponse(url, body=body, encoding="utf-8", request=request)


def building(item_id="abc"):
    return {"lotIdEncoded": item_id, "geo": {"lat": 1, "lon": 2}, "listings": [{
        "title": "Riverbank", "uriMalone": f"/riverbank-{item_id}/pad",
        "address": {"street": "1 Main", "city": "New York", "state": "NY", "zip": "10001"},
        "summary": {"beds": {"min": 0, "max": 3}, "baths": {"min": 1, "max": 2},
                    "price": {"min": 3000, "max": 5000}},
        "tags": ["active"], "unitCount": 4, "contactPhone": "555-0100",
    }]}


def test_maps_rsc_listing_and_paginates():
    spider = HotPadsListingSpider(category="new-york-ny", max_pages=2)
    outputs = list(spider.parse(response(html([building()]))))
    item = outputs[0]
    assert item["item_id"] == "abc"
    assert item["price_low"] == 3000
    assert item["beds"] == {"min": 0, "max": 3}
    assert item["source"] == "hotpads_rsc_bootstrap"
    assert outputs[1].url.endswith("/page/2")


def test_page_url_replaces_existing_page():
    base = "https://hotpads.com/new-york-ny/apartments-for-rent/page/7"
    assert HotPadsListingSpider._page_url(base, 1).endswith("/apartments-for-rent")
    assert HotPadsListingSpider._page_url(base, 3).endswith("/apartments-for-rent/page/3")


def test_deduplicates_repeated_building():
    spider = HotPadsListingSpider(category="new-york-ny")
    assert len(list(spider.parse(response(html([building()]))))) == 1
    assert list(spider.parse(response(html([building()])))) == []


@pytest.mark.parametrize("body", ["<html></html>", "x" * 6000 + " Pardon the Interruption"])
def test_rejects_missing_or_challenge_bootstrap(body):
    spider = HotPadsListingSpider(category="new-york-ny")
    with pytest.raises(RuntimeError):
        list(spider.parse(response(body)))
