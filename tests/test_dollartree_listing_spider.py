import json

import pytest
from scrapy.http import TextResponse

from common.spiders.dollartree_listing_spider import DollartreeListingSpider


def response(payload, *, page=1, status=200):
    request = DollartreeListingSpider()._api_request(
        {"category": "food-candy-drinks", "dimension_id": "477714525"},
        page,
        (page - 1) * 24,
    )
    return TextResponse(
        request.url,
        request=request,
        status=status,
        body=json.dumps(payload),
        encoding="utf-8",
    )


def payload(total=1, records=True):
    attrs = {
        "product.id": ["354662"],
        "sku.repositoryId": ["354662"],
        "product.displayName": ["Lil' Dutch Maid Duplex Crème Cookies."],
        "product.brand": ["Lil Dutch Maid"],
        "product.route": ["/cookies/354662"],
        "product.primaryFullImageURL": ["/ccstore/v1/images/cookie.jpg"],
        "product.longDescription": ["Cream-filled cookies"],
        "product.category": ["Cookies"],
        "sku.activePrice": ["1.250000"],
        "sku.availabilityStatus": ["INSTOCK"],
        "product.minimumQuantity": ["12"],
        "DollarProductType.casePackSize": ["12"],
        "DollarProductType.averageRating": ["5.0"],
        "DollarProductType.numberOfReviews": ["10"],
    }
    rows = [
        {
            "attributes": {
                "sku.minActivePrice": ["1.250000"],
                "sku.maxActivePrice": ["1.500000"],
            },
            "records": [{"attributes": attrs}],
        }
    ] if records else []
    return {
        "resultsList": {
            "records": rows,
            "totalNumRecs": total,
            "recsPerPage": 24,
        }
    }


def test_maps_occ_record_and_feed_contract():
    spider = DollartreeListingSpider()
    output = list(spider.parse_api(response(payload())))
    assert len(output) == 1
    item = output[0]
    assert item["item_id"] == "354662"
    assert item["price"] == 1.25
    assert item["min_price"] == 1.25
    assert item["max_price"] == 1.5
    assert item["in_stock"] is True
    assert item["url"] == "https://www.dollartree.com/cookies/354662"
    assert item["source"] == "dollartree_occ_guided_search_api"
    assert set(item) == set(spider.custom_settings["FEED_EXPORT_FIELDS"])


def test_paginates_by_offset():
    spider = DollartreeListingSpider(max_pages=2)
    output = list(spider.parse_api(response(payload(total=30))))
    assert output[-1].url.endswith("N=477714525&Nrpp=24&No=24")


def test_default_and_named_categories():
    assert DollartreeListingSpider()._selected_category()["category"] == "food-candy-drinks"
    assert (
        DollartreeListingSpider(category="christmas")._selected_category()["dimension_id"]
        == "2506507028"
    )


def test_invalid_category_fails_loudly():
    with pytest.raises(ValueError, match="Unknown category"):
        DollartreeListingSpider(category="missing")._selected_category()


def test_missing_results_fails_loudly():
    with pytest.raises(RuntimeError, match="resultsList"):
        list(DollartreeListingSpider().parse_api(response({})))
