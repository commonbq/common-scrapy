import json

import pytest

from common.spiders.harborfreight_listing_spider import HarborfreightListingSpider


class Response:
    status = 200
    url = "https://www.harborfreight.com/automotive/jacks-jack-stands.html"

    def __init__(self, state, page=1):
        self.text = f"<script>window.__APOLLO_STATE__ = {json.dumps(state)};</script>"
        self.meta = {"page": page, "base_url": self.url, "category": "Automotive",
                     "department": "Automotive", "subcategory": "jacks-jack-stands"}


def state(page=1, refs=("SimpleProduct:13354",), total_pages=1):
    result = {"items": [{"__ref": ref} for ref in refs], "total_count": 63,
              "page_info": {"current_page": page, "page_size": 36, "total_pages": total_pages}}
    data = {"ROOT_QUERY": {f'products({{"currentPage":{page},"pageSize":36}})': result}}
    data["SimpleProduct:13354"] = {
        "id": 13354, "sku": "64784",
        "name": "3 Ton Low-Profile Professional Floor Jack with RAPID PUMP, Green",
        "Brand": "DAYTONA", "canonical_url": "3-ton-floor-jack-64784.html",
        "small_image": {"url": "https://example.com/jack.jpg"},
        "price_range": {"minimum_price": {"final_price": {"value": 199.99},
                                             "regular_price": {"value": 219.99}}},
    }
    return data


def test_maps_apollo_reference_and_feed_contract():
    spider = HarborfreightListingSpider(category="Automotive")
    output = list(spider.parse(Response(state())))
    assert len(output) == 1
    item = output[0]
    assert item["sku"] == "64784"
    assert item["price"] == 199.99
    assert item["brand"] == "DAYTONA"
    assert item["source"] == "harborfreight_apollo_bootstrap"
    assert set(item) == set(spider.custom_settings["FEED_EXPORT_FIELDS"])


def test_paginates_with_magento_p_parameter():
    spider = HarborfreightListingSpider(category="Automotive", max_pages=2)
    output = list(spider.parse(Response(state(total_pages=2))))
    assert output[-1].url.endswith("?p=2")


def test_deduplicates_skus():
    spider = HarborfreightListingSpider(category="Automotive")
    assert len(list(spider.parse(Response(state())))) == 1
    assert list(spider.parse(Response(state()))) == []


def test_missing_hydration_fails_loudly():
    response = Response(state())
    response.text = "<html><title>Access denied</title></html>"
    with pytest.raises(RuntimeError, match="hydration"):
        list(HarborfreightListingSpider(category="Automotive").parse(response))


def test_page_url_preserves_query():
    url = HarborfreightListingSpider._page_url("https://example.com/cat.html?order=name", 2)
    assert url == "https://example.com/cat.html?order=name&p=2"
