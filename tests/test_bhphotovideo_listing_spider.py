import html
import json

from scrapy.http import HtmlResponse, Request

from common.spiders.bhphotovideo_listing_spider import BhphotovideoListingSpider


def response_for(data):
    state = {"ListingStore": {"state": {"response": {"data": data}}}}
    body = f'<div class="bh-preloaded-data" data-data="{html.escape(json.dumps(state), quote=True)}"></div>'
    request = Request("https://www.bhphotovideo.com/c/buy/x", meta={
        "page": 1, "category": "Mirrorless Lenses", "department": "Photography",
        "category_url": "https://www.bhphotovideo.com/c/buy/x",
    })
    return HtmlResponse(request.url, body=body, encoding="utf-8", request=request)


def test_hydration_item_and_pagination():
    product = {
        "itemKey": {"skuNo": 123},
        "core": {"itemCode": "SONY1", "shortDescription": "Sony Lens", "detailsUrl": "/c/product/123", "manufacturerCatalogNumber": "SEL1"},
        "priceInfo": {"price": 99.5, "addToCartButton": "ADD_TO_CART"},
        "mainImage": {"listing": {"url": "https://img/123.jpg"}},
        "reviewsStats": {"reviewRating": 4.5, "reviewCount": 8},
        "stockInfo": {"status": "IN_STOCK"},
        "categoryInfo": {"primaryCategoryPath": [{"name": "Photography"}, {"name": "Lenses"}]},
    }
    spider = BhphotovideoListingSpider(category="Mirrorless Lenses", max_pages=2)
    output = list(spider.parse(response_for({"items": [product], "count": 2, "itemsPerPage": 1, "pageNumber": 1, "mainCategory": {"id": 7}})))
    assert output[0]["product_id"] == 123
    assert output[0]["price"] == 99.5
    assert output[0]["category_path"] == "Photography > Lenses"
    assert output[1].url.endswith("/pn/2")


def test_category_and_override_resolution():
    spider = BhphotovideoListingSpider(category="Mirrorless Lenses")
    assert "/ci/17912/" in spider.resolve_target_url()
    override = BhphotovideoListingSpider(category="Mirrorless Lenses", url="https://www.bhphotovideo.com/custom")
    assert override.resolve_target_url().endswith("/custom")
