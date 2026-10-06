from pathlib import Path

import pytest
from scrapy.http import HtmlResponse, Request

from common.spiders.trulia_categories import TRULIA_CATEGORIES
from common.spiders.trulia_listing_spider import TruliaListingSpider

SAMPLE = Path(__file__).parents[1] / "sample" / "trulia-next-data-sample.html"


def response(body=None, page=1):
    request = Request("https://www.trulia.com/CO/Colorado_Springs/", meta={"page": page, "category": "colorado-springs-co"})
    return HtmlResponse(request.url, request=request, body=(body or SAMPLE.read_text()).encode(), encoding="utf-8")


def test_exact_category_inventory():
    assert len(TRULIA_CATEGORIES) == 20
    assert TRULIA_CATEGORIES["colorado-springs-co"].endswith("/CO/Colorado_Springs/")


def test_hydration_mapping_and_export_contract():
    spider = TruliaListingSpider(category="colorado-springs-co", max_pages=1)
    items = list(spider.parse(response()))
    assert len(items) == 1
    item = items[0]
    assert set(item) == set(spider.custom_settings["FEED_EXPORT_FIELDS"])
    assert item["item_id"] == "465800506"
    assert item["price"] == 2500000
    assert item["beds"] == 5 and item["baths"] == 5.5
    assert item["sqft"] == 6885
    assert item["latitude"] == 38.781754
    assert item["source"] == "trulia_next_data"


def test_follows_canonical_next_page():
    out = list(TruliaListingSpider(category="colorado-springs-co", max_pages=2).parse(response()))
    assert out[-1].url == "https://www.trulia.com/CO/Colorado_Springs/2_p/"
    assert out[-1].meta["page"] == 2


def test_deduplicates_property_ids():
    spider = TruliaListingSpider(category="colorado-springs-co")
    assert len(list(spider.parse(response()))) == 1
    assert list(spider.parse(response())) == []


@pytest.mark.parametrize("body,message", [
    ("<html></html>", "no __NEXT_DATA__"),
    ('<script id="__NEXT_DATA__">{bad}</script>', "malformed"),
    ('<script id="__NEXT_DATA__" type="application/json">{"props":{}}</script>', "props.searchData"),
])
def test_missing_or_malformed_state_fails(body, message):
    with pytest.raises(RuntimeError, match=message):
        list(TruliaListingSpider(category="colorado-springs-co").parse(response(body)))


def test_scrapeops_options_are_idempotent():
    spider = TruliaListingSpider(category="colorado-springs-co")
    spider.settings = {"PROXY": "http://scrapeops.country=us:key@proxy.scrapeops.io:5353"}
    mutated = spider._proxy()
    assert "residential=true" in mutated and "bypass=5" in mutated
    spider.settings = {"PROXY": mutated}
    assert spider._proxy() == mutated
