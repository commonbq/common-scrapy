import json

import pytest
from scrapy.http import Request, TextResponse

from common.spiders.chewy_listing_spider import ChewyListingSpider
from common.spiders.chewy_categories import CHEWY_CATEGORIES, CHEWY_CATEGORY_INVENTORY


def response(spider, products, *, page=1, total=3):
    state = {"props": {"pageProps": {"initialState": {"searchSlice": {"plpData": {
        "products": products, "recordSetTotal": total,
    }}}}}}
    body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(state)}</script>'
    url = "https://www.chewy.com/b/food-332" + (f"?page={page}" if page > 1 else "")
    request = Request(url, meta={"category": "dog-food", "page": page, "base_url": "https://www.chewy.com/b/food-332"})
    return TextResponse(url, request=request, body=body, encoding="utf-8")


def product(item_id="3969182", href="/pedigree/dp/3969182"):
    return {"catalogEntryId": item_id, "partNumber": item_id, "name": "Pedigree Dog Food",
            "manufacturer": "Pedigree", "href": href, "displayPrice": "$25.97",
            "advertisedPrice": "25.97", "strikePrice": "$29.99", "autoshipPrice": "24.67",
            "rating": 4.6406, "ratingCount": 11023, "isAd": False, "imageUrl": "https://img.test/a.jpg"}


def split(outputs):
    values = list(outputs)
    return [x for x in values if isinstance(x, dict)], [x for x in values if not isinstance(x, dict)]


def test_complete_navigation_taxonomy():
    assert set(CHEWY_CATEGORY_INVENTORY) == {"dog", "cat", "more-pets-farm"}
    assert len(CHEWY_CATEGORIES) >= 170
    assert len({entry["url"] for entry in CHEWY_CATEGORIES}) == len(CHEWY_CATEGORIES)


def test_hydration_mapping_feed_contract_and_pagination():
    spider = ChewyListingSpider(category="food-332", max_pages=2)
    items, requests = split(spider.parse(response(spider, [product(), {"type": "banner"}])))
    assert len(items) == 1
    assert list(items[0]) == spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert items[0]["item_id"] == "3969182"
    assert items[0]["price"] == 25.97
    assert items[0]["list_price"] == 29.99
    assert items[0]["autoship_price"] == 24.67
    assert items[0]["source"] == "chewy_next_data_bootstrap"
    assert requests[0].url == "https://www.chewy.com/b/food-332?page=2"


def test_scrapeops_proxy_is_upgraded_to_us_residential():
    spider = ChewyListingSpider(category="food-332")
    spider.settings = {"PROXY": "http://scrapeops:key@proxy.scrapeops.io:5353"}
    proxy = spider._residential_proxy()
    assert "scrapeops.residential=true.country=us" in proxy


def test_sponsored_redirect_and_deduplication():
    spider = ChewyListingSpider(category="food-332", max_pages=2)
    href = "/click?redirect=https%3A%2F%2Fwww.chewy.com%2Fcanonical%2Fdp%2F7"
    first, _ = split(spider.parse(response(spider, [product("7", href)], total=2)))
    second, requests = split(spider.parse(response(spider, [product("7", href)], page=2, total=2)))
    assert first[0]["url"] == "https://www.chewy.com/canonical/dp/7"
    assert second == [] and requests == []


@pytest.mark.parametrize("body,match", [
    ("<html></html>", "no __NEXT_DATA__"),
    ('<script id="__NEXT_DATA__">{bad}</script>', "malformed"),
    ('<script id="__NEXT_DATA__">{}</script>', "no searchSlice"),
])
def test_missing_or_malformed_state_fails_loudly(body, match):
    spider = ChewyListingSpider(category="food-332")
    request = Request("https://www.chewy.com/b/food-332", meta={"page": 1, "base_url": "https://www.chewy.com/b/food-332"})
    result = TextResponse(request.url, request=request, body=body, encoding="utf-8")
    with pytest.raises(RuntimeError, match=match):
        list(spider.parse(result))
