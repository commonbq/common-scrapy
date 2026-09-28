import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.stockx_listing_spider import StockxListingSpider


def response_with(products, *, page=1, page_count=1):
    browse = {
        "results": {
            "edges": [{"node": product} for product in products],
            "pageInfo": {"page": page, "pageCount": page_count},
        }
    }
    state = {
        "props": {
            "pageProps": {
                "req": {
                    "appContext": {
                        "states": {
                            "query": {
                                "value": {
                                    "queries": [
                                        {"state": {"data": {"menuCollection": []}}},
                                        {"state": {"data": {"browse": browse}}},
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(state)}</script>'
    request = Request(
        f"https://stockx.com/sneakers?page={page}",
        meta={
            "page": page,
            "category": "sneakers",
            "subcategory": "all",
            "listing_url": "https://stockx.com/sneakers",
        },
    )
    return HtmlResponse(request.url, request=request, body=body, encoding="utf-8")


class StockxListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = StockxListingSpider(category="sneakers", max_pages=2)

    def test_feed_export_fields_are_stable(self):
        fields = self.spider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertEqual(fields[0:4], ["item_id", "title", "brand", "price"])
        self.assertEqual(fields[-4:], ["subcategory", "page", "source", "raw"])

    def test_parse_authoritative_browse_product(self):
        product = {
            "id": "product-1",
            "title": "Jordan 4 Retro Test",
            "urlKey": "air-jordan-4-retro-test",
            "brand": "Jordan",
            "productCategory": "sneakers",
            "media": {"smallImageUrl": "https://images.stockx.com/test.jpg"},
            "market": {
                "state": {
                    "lowestAsk": {"amount": 155},
                    "highestBid": {"amount": 140},
                },
                "statistics": {"lastSale": {"amount": 150}},
            },
        }
        results = list(self.spider.parse(response_with([product])))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["item_id"], "product-1")
        self.assertEqual(results[0]["price"], 155)
        self.assertEqual(results[0]["highest_bid"], 140)
        self.assertEqual(results[0]["last_sale_price"], 150)
        self.assertEqual(results[0]["source"], "stockx_next_data_browse")

    def test_sponsored_product_shape_and_deduplication(self):
        product = {"id": "product-1", "title": "Test", "urlKey": "test"}
        response = response_with([{"product": product}, {"product": product}])
        results = list(self.spider.parse(response))
        self.assertEqual(len(results), 1)

    def test_paginates_with_page_query_parameter(self):
        results = list(self.spider.parse(response_with([], page=1, page_count=3)))
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Request)
        self.assertEqual(results[0].url, "https://stockx.com/sneakers?page=2")


if __name__ == "__main__":
    unittest.main()
