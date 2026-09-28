import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.maccosmetics_listing_spider import MaccosmeticsListingSpider


HTML = '''
<html><head><link rel="next" href="/collections/face?page=2"></head><body>
<script>var meta = {"products":[{"id":123,"vendor":"MAC Cosmetics","type":"Face","handle":"studio-fix","variants":[{"price":3900,"name":"Studio Fix - NC20","public_title":"Studio Fix","sku":"SKU-1"}]}],"page":{"pageType":"collection"}};</script>
<dynamic-product-card data-handle="studio-fix" title="Studio Fix Foundation" image="//cdn.example/studio.png"></dynamic-product-card>
</body></html>
'''


class MaccosmeticsListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = MaccosmeticsListingSpider(category="face", max_pages="1")
        request = Request("https://www.maccosmetics.com/collections/face", meta={"page": 1})
        self.response = HtmlResponse(request.url, request=request, body=HTML, encoding="utf-8")

    def test_feed_export_fields(self):
        self.assertEqual(
            list(self.spider.custom_settings["FEED_EXPORT_FIELDS"]),
            ["category", "item_id", "sku", "title", "brand", "product_type", "url", "image_url", "price", "currency", "page", "source", "raw"],
        )

    def test_parses_shopify_catalog(self):
        item = list(self.spider.parse(self.response))[0]
        self.assertEqual(item["item_id"], "123")
        self.assertEqual(item["sku"], "SKU-1")
        self.assertEqual(item["title"], "Studio Fix Foundation")
        self.assertEqual(item["price"], 39.0)
        self.assertEqual(item["image_url"], "https://cdn.example/studio.png")

    def test_inventory_matches_current_sitemap(self):
        self.assertEqual(len(self.spider.categories), 79)
        self.assertIn("face", {entry["category"] for entry in self.spider.categories})


if __name__ == "__main__":
    unittest.main()
