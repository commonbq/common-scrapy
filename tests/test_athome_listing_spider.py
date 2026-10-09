from pathlib import Path

import pytest
from scrapy.http import HtmlResponse

from common.spiders.athome_listing_spider import AthomeListingSpider


FIXTURE = Path(__file__).parents[1] / "sample" / "athome-search-updategrid-xhr-sample.html"


def response(spider=None, *, page=1, offset=0, status=200):
    spider = spider or AthomeListingSpider()
    entry = next(iter(spider.iter_categories()))
    request = spider._api_request(entry, page=page, offset=offset)
    return HtmlResponse(
        request.url,
        request=request,
        status=status,
        body=FIXTURE.read_bytes(),
        encoding="utf-8",
    )


def test_maps_updategrid_payload_and_feed_contract():
    spider = AthomeListingSpider()
    output = list(spider.parse_api(response(spider)))
    assert len(output) == 1
    item = output[0]
    assert item["item_id"] == "125043763"
    assert item["title"] == '50-Count Burgundy Ornaments, 2.4"'
    assert item["price"] == 11.99
    assert item["url"].endswith("/125043763.html")
    assert item["source"] == "athome_sfra_search_updategrid_api"
    assert set(item) == set(spider.custom_settings["FEED_EXPORT_FIELDS"])


def test_paginates_the_ajax_api_by_offset():
    spider = AthomeListingSpider(max_pages=2)
    output = list(spider.parse_api(response(spider)))
    request = output[-1]
    assert "start=24" in request.url
    assert "sz=24" in request.url
    assert request.meta["page"] == 2


def test_default_named_and_url_categories():
    assert AthomeListingSpider()._selected_category()["category"] == "christmas"
    assert AthomeListingSpider(category="Area Rugs")._selected_category()["category"] == "area-rugs"
    assert (
        AthomeListingSpider(url="https://www.athome.com/vases/")._selected_category()["category"]
        == "vases"
    )


def test_invalid_category_fails_loudly():
    with pytest.raises(ValueError, match="Unknown At Home category"):
        AthomeListingSpider(category="missing")._selected_category()


def test_api_errors_fail_loudly():
    with pytest.raises(RuntimeError, match="HTTP 403"):
        list(AthomeListingSpider().parse_api(response(status=403)))
