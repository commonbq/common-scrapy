import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.fashionnova_listing_spider import FashionnovaListingSpider


def response_with(products, *, page=1):
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "item": product}
                for i, product in enumerate(products, 1)
            ],
        },
    }
    body = f'<script type="application/ld+json">{json.dumps(data)}</script>'
    request = Request(
        f"https://www.fashionnova.com/collections/dresses?page={page}",
        meta={
            "page": page,
            "category": "dresses",
            "subcategory": "all",
            "listing_url": "https://www.fashionnova.com/collections/dresses",
        },
    )
    return HtmlResponse(request.url, request=request, body=body, encoding="utf-8")


class FashionnovaListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = FashionnovaListingSpider(category="dresses", max_pages=2)

    def test_feed_export_fields_are_stable(self):
        self.assertEqual(
            self.spider.custom_settings["FEED_EXPORT_FIELDS"],
            [
                "item_id", "title", "brand", "description", "price", "price_max",
                "currency", "availability", "url", "image_url", "product_category",
                "category", "subcategory", "page", "source", "raw",
            ],
        )

    def test_parse_collection_product(self):
        product = {
            "@type": "Product",
            "sku": "DR123",
            "name": "Test Dress",
            "brand": {"@type": "Brand", "name": "Fashion Nova"},
            "url": "https://www.fashionnova.com/products/test-dress",
            "image": ["https://cdn.shopify.com/test.jpg"],
            "category": "Dresses",
            "offers": {
                "lowPrice": "19.99",
                "highPrice": "29.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
            },
        }
        results = list(self.spider.parse(response_with([product])))
        item = results[0]
        self.assertEqual(item["item_id"], "DR123")
        self.assertEqual(item["price"], 19.99)
        self.assertEqual(item["availability"], "InStock")
        self.assertEqual(item["source"], "fashionnova_collection_json_ld")

    def test_deduplicates_and_paginates(self):
        product = {"sku": "DR123", "name": "Test", "url": "https://example.test/p"}
        results = list(self.spider.parse(response_with([product, product])))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["item_id"], "DR123")
        self.assertIsInstance(results[1], Request)
        self.assertEqual(
            results[1].url,
            "https://www.fashionnova.com/collections/dresses?page=2",
        )


if __name__ == "__main__":
    unittest.main()
