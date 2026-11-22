import json

import pytest

from common.spiders.jcrew_listing_spider import (
    JcrewListingSpider,
    hydrated_products,
    parse_next_data,
)


def hydration_html(products=None, pagination=None):
    payload = {
        "props": {
            "initialState": {
                "array": {
                    "data": {
                        "productArray": {
                            "productList": [{"products": products or []}],
                            "pagination": pagination or {"pageIndex": 1, "totalPage": 2, "resultsPerPage": 60},
                        }
                    }
                }
            }
        }
    }
    return f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'


def test_extracts_hydrated_product_fields_and_pagination():
    product = {
        "productCode": "CZ324",
        "productDescription": "Fair Isle sweater",
        "primaryCategoryId": "womens|categories|clothing|sweaters",
        "url": "/p/womens/sweater/CZ324",
        "listPrice": {"amount": 168, "formatted": "$168.00"},
        "searchPrice": 168,
        "bvAverageRating": "4.44",
        "bvReviewCount": "9",
    }
    payload = parse_next_data(hydration_html([product]))
    products, pagination = hydrated_products(payload)
    assert products == [product]
    assert pagination == {"pageIndex": 1, "totalPage": 2, "resultsPerPage": 60}
    spider = JcrewListingSpider(category="New Arrivals")
    assert spider._money(product["listPrice"]["amount"]) == 168.0
    assert spider._number(product["bvAverageRating"]) == 4.44
    assert spider._integer(product["bvReviewCount"]) == 9


def test_page_url_preserves_existing_category_query():
    assert JcrewListingSpider._page_url(
        "https://www.jcrew.com/plp/womens?fit=Classic", 2
    ) == "https://www.jcrew.com/plp/womens?fit=Classic&page=2"


@pytest.mark.parametrize(
    "html, message",
    [
        ("<html>not hydrated</html>", "missing the __NEXT_DATA__"),
        ("<html>Access Denied</html>", "challenge page"),
        ('<script id="__NEXT_DATA__">{bad}</script>', "invalid JSON"),
    ],
)
def test_missing_invalid_or_challenged_hydration_fails(html, message):
    with pytest.raises(ValueError, match=message):
        parse_next_data(html)
