import json
import unittest

from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.target_listing_spider import TargetListingSpider


class TargetListingSpiderTests(unittest.TestCase):
    def test_named_category_expands_to_all_children(self):
        spider = TargetListingSpider(category="grocery")
        requests = list(spider.start_requests())

        self.assertEqual(len(requests), len(spider.categories["grocery"]))
        self.assertEqual(requests[0].meta["category"], "grocery")
        self.assertEqual(requests[0].meta["subcategory"], "all")
        self.assertEqual(requests[0].meta["category_id"], "5xt1a")

    def test_direct_category_id_remains_supported(self):
        spider = TargetListingSpider(category="5xtc0")
        request = next(spider.start_requests())
        self.assertEqual(request.meta["category_id"], "5xtc0")
        self.assertIn("/N-5xtc0", request.url)

    def test_redsky_products_match_feed_contract_and_deduplicate(self):
        spider = TargetListingSpider(category="grocery", max_pages=1)
        payload = {
            "data": {
                "search": {
                    "products": [
                        {
                            "tcin": "123",
                            "item": {
                                "product_description": {"title": "Coffee"},
                                "primary_brand": {"name": "Good & Gather"},
                                "enrichment": {
                                    "buy_url": "/p/coffee/-/A-123",
                                    "image_info": {
                                        "primary_image": {
                                            "url": "https://example.test/123.jpg"
                                        }
                                    },
                                },
                            },
                            "price": {
                                "formatted_current_price": "$8.99",
                                "formatted_comparison_price": "$10.99",
                            },
                            "ratings_and_reviews": {
                                "statistics": {
                                    "rating": {"average": 4.5, "count": 42}
                                }
                            },
                        },
                        {"tcin": "123", "title": "duplicate"},
                    ]
                }
            }
        }
        request = Request(
            "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?offset=0",
            meta={"category": "grocery", "subcategory": "coffee", "page": 1},
        )
        response = TextResponse(
            request.url,
            request=request,
            body=json.dumps(payload).encode(),
            encoding="utf-8",
        )

        items = list(spider.parse_redsky(response))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["product_id"], "123")
        self.assertEqual(items[0]["brand"], "Good & Gather")
        self.assertEqual(items[0]["image"], "https://example.test/123.jpg")
        self.assertEqual(items[0]["rating"], 4.5)
        self.assertEqual(items[0]["reviews_count"], 42)
        self.assertEqual(items[0]["category"], "grocery")
        self.assertEqual(items[0]["source"], "target_redsky_plp_search_v2")
        self.assertEqual(
            list(spider.custom_settings["FEED_EXPORT_FIELDS"]),
            [
                "product_id",
                "name",
                "brand",
                "price",
                "original_price",
                "currency",
                "url",
                "image",
                "rating",
                "reviews_count",
                "category",
                "subcategory",
                "page",
                "source",
                "raw",
            ],
        )

    def test_html_discovers_current_redsky_key(self):
        spider = TargetListingSpider(category="grocery")
        request = next(spider.start_requests())
        response = HtmlResponse(
            request.url,
            request=request,
            body=b'<script>apiKey\\\":\\\"0123456789abcdef0123456789abcdef0000</script>',
            encoding="utf-8",
        )
        redsky = next(spider.parse_search_html(response))
        self.assertIn("key=0123456789abcdef0123456789abcdef", redsky.url)
        self.assertEqual(redsky.meta["category_id"], "5xt1a")


if __name__ == "__main__":
    unittest.main()
