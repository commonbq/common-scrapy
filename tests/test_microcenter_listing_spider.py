from __future__ import annotations

from scrapy.http import HtmlResponse, Request

from common.spiders.microcenter_categories import MICROCENTER_CATEGORIES, load_categories
from common.spiders.microcenter_listing_spider import MicrocenterListingSpider


URL = "https://www.microcenter.com/search/search_results.aspx?fq=category%3AProcessors%2FCPUs%7C123&storeid=121"
CARD = """
<li class="product_wrapper">
 <a class="productClickItemV2" data-id="706001" data-name="Ryzen 7 9850X3D" data-brand="AMD"
    data-price="459.99" data-position="1" href="/product/706001/ryzen"></a>
 <img class="SearchResultProductImage" src="https://productimages.microcenter.com/0706001.jpg">
 <p class="sku">SKU: 974659</p><div class="highlight">Free game code</div>
 <div class="stock"><span class="inventoryCnt">25+ <span>IN STOCK</span></span><span class="storeName"> at Cambridge Store</span></div>
 <div class="price"><strike>$499.99</strike></div>
 <form><input name="store_id" value="121"><input name="sku" value="974659"></form>
</li>
"""


def response(body=CARD, page=1, status=200):
    request = Request(URL, meta={"page": page})
    return HtmlResponse(URL, body=body.encode(), encoding="utf-8", request=request, status=status)


def collect(spider, page=response()):
    output = list(spider.parse(page))
    return [x for x in output if isinstance(x, dict)], [x for x in output if isinstance(x, Request)]


def test_taxonomy_preserves_full_navigation_and_deduplicates_urls():
    categories = load_categories()
    assert len(categories) == 513
    assert len({x["url"] for x in categories}) == 513
    assert len({x["category"] for x in categories}) == 513
    contexts = [context for item in categories for context in item["navigation_contexts"]]
    assert len(contexts) == 578
    assert len({(x["department"], x["group"]) for x in contexts}) == 118
    assert len({x["department"] for x in contexts}) == 20


def test_structured_card_state_maps_item_and_feed_contract():
    spider = MicrocenterListingSpider(category="processors-cpus", max_pages=1)
    items, requests = collect(spider)
    assert requests == []
    assert items[0] | {} == items[0]
    assert items[0]["item_id"] == "706001"
    assert items[0]["sku"] == "974659"
    assert items[0]["title"] == "Ryzen 7 9850X3D"
    assert items[0]["brand"] == "AMD"
    assert items[0]["price"] == 459.99
    assert items[0]["original_price"] == 499.99
    assert items[0]["stock_count"] == 25
    assert items[0]["store_name"] == "Cambridge Store"
    assert items[0]["source"] == "microcenter_card_state_bootstrap"


def test_pagination_preserves_store_and_stops_at_max_pages():
    body = CARD + '<div id="bottomPagination"><p class="status">1 - 24 of 41 items</p></div>'
    spider = MicrocenterListingSpider(category="processors-cpus", max_pages=2, store_id=121)
    items, requests = collect(spider, response(body))
    assert len(items) == 1 and len(requests) == 1
    assert "page=2" in requests[0].url and "storeid=121" in requests[0].url
    assert items[0]["total_count"] == 41 and items[0]["last_page"] == 2


def test_duplicate_ids_are_not_exported_across_pages():
    spider = MicrocenterListingSpider(category="processors-cpus", max_pages=2)
    first, _ = collect(spider)
    second, _ = collect(spider, response(page=2))
    assert len(first) == 1 and second == []


def test_challenge_and_empty_pages_emit_no_false_items():
    spider = MicrocenterListingSpider(category="processors-cpus")
    assert collect(spider, response("<title>Just a moment...</title>")) == ([], [])
    assert collect(spider, response("<html>normal empty page</html>")) == ([], [])


def test_start_request_adds_configurable_store():
    spider = MicrocenterListingSpider(category="processors-cpus", store_id="115")
    request = next(spider.start_requests())
    assert "storeid=115" in request.url and "page=1" in request.url


def test_feed_export_fields_cover_every_emitted_key():
    spider = MicrocenterListingSpider(category="processors-cpus")
    items, _ = collect(spider)
    assert set(items[0]) == set(spider.custom_settings["FEED_EXPORT_FIELDS"])
