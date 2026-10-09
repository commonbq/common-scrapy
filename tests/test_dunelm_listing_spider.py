import json
from pathlib import Path

from scrapy.http import HtmlResponse, Request

from common.spiders.dunelm_listing_spider import DunelmListingSpider


ROOT = Path(__file__).parents[1]


def make_spider(**kwargs):
    return DunelmListingSpider(category="home-and-furniture", **kwargs)


def response_for(html, url="https://www.dunelm.com/category/home-and-furniture/bedding"):
    request = Request(url, meta={"page": 1, "discovery_depth": 0})
    return HtmlResponse(url, body=html.encode(), encoding="utf-8", request=request)


def test_categories_and_feed_contract():
    spider = make_spider()
    assert len(spider.categories) == 20
    fields = spider.custom_settings["FEED_EXPORT_FIELDS"]
    assert fields[0:4] == ["category", "item_id", "title", "brand"]
    assert fields[-3:] == ["source", "raw", "timestamp"]


def test_extracts_only_redux_bootstrap_products():
    product = json.loads((ROOT / "sample/dunelm-product-sample.json").read_text())
    state = {
        "reduxState": {
            "config": {"imagesCDNUrl": "https://images.dunelm.com"},
            "product": {"partialProductById": {product["id"]: product}},
            "searchProduct": {"results": [{"res": {
                "hits": [{"productId": product["id"], "mostRelevantSkuId": "30145683"}],
                "nbHits": 3457, "nbPages": 58,
            }}]},
        }
    }
    html = f'<script id="ssr-state-data" type="application/json">{json.dumps(state)}</script>'
    output = list(make_spider().parse_listing(response_for(html)))
    assert len(output) == 1
    item = output[0]
    assert item["item_id"] == "1000000601"
    assert item["title"] == "Non Iron Plain Fitted Sheet"
    assert item["price"] == 12
    assert item["price_min"] == 6
    assert item["reviews_count"] == 4324
    assert item["image"] == "https://images.dunelm.com/30145683.jpg"
    assert item["source"] == "dunelm_redux_ssr_bootstrap"


def test_department_page_discovers_leaf_without_parsing_json_ld():
    html = '''
    <script type="application/ld+json">{"@type":"Product","name":"Ignored"}</script>
    <a href="/category/home-and-furniture/bedding">Bedding</a>
    '''
    output = list(make_spider().parse_listing(response_for(html, "https://www.dunelm.com/category/home-and-furniture")))
    assert len(output) == 1
    assert output[0].url == "https://www.dunelm.com/category/home-and-furniture/bedding"


def test_pagination_url_replaces_page():
    assert DunelmListingSpider._with_page("https://www.dunelm.com/category/rugs?page=2", 3).endswith("?page=3")

