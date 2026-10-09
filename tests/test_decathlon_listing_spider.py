import json
import unittest

from scrapy.http import TextResponse

from common.spiders.decathlon_listing_spider import DecathlonListingSpider


def response(payload, *, page=1, status=200):
    spider = DecathlonListingSpider(category="camp-hike")
    request = spider._api_request(
        "https://www.decathlon.com/collections/camp-hike", page=page
    )
    return TextResponse(
        request.url,
        request=request,
        status=status,
        body=json.dumps(payload),
        encoding="utf-8",
    )


def product():
    return {
        "id": 8209731190846,
        "title": "Simond Men’s Xplore Hooded Down Jacket",
        "handle": "men-s-lightweight-down-trekking-jacket-3-c-xplore-khaki",
        "body_html": "Compact and lightweight.",
        "published_at": "2026-08-14T07:45:42-07:00",
        "vendor": "Simond",
        "product_type": "Down jacket",
        "tags": ["Down Jackets", "SPORT: mountain trekking"],
        "variants": [
            {
                "id": 43182121386046,
                "sku": "5787754",
                "available": True,
                "price": "119.00",
                "compare_at_price": "139.00",
            }
        ],
        "images": [{"src": "https://cdn.shopify.com/jacket.jpg"}],
    }


class DecathlonListingSpiderTest(unittest.TestCase):
    def test_maps_shopify_product_and_feed_contract(self):
        spider = DecathlonListingSpider(category="camp-hike")
        output = list(spider.parse_api(response({"products": [product()]})))
        self.assertEqual(len(output), 1)
        item = output[0]
        self.assertEqual(item["item_id"], "8209731190846")
        self.assertEqual(item["variant_id"], "43182121386046")
        self.assertEqual(item["sku"], "5787754")
        self.assertEqual(item["price"], 119.0)
        self.assertEqual(item["compare_at_price"], 139.0)
        self.assertIs(item["in_stock"], True)
        self.assertEqual(item["available_variant_count"], 1)
        self.assertEqual(item["source"], "decathlon_shopify_collection_api")
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_paginates_only_when_api_page_is_full(self):
        spider = DecathlonListingSpider(category="camp-hike", max_pages=2)
        rows = [dict(product(), id=index) for index in range(spider.page_size)]
        output = list(spider.parse_api(response({"products": rows})))
        self.assertTrue(output[-1].url.endswith("limit=250&page=2"))

    def test_default_category_and_api_url(self):
        spider = DecathlonListingSpider()
        request = next(spider.start_requests())
        self.assertIn("/collections/shop-all/products.json", request.url)
        self.assertIn("limit=250&page=1", request.url)

    def test_missing_products_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "products list"):
            list(DecathlonListingSpider().parse_api(response({})))
