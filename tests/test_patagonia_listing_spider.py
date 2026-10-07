import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.patagonia_listing_spider import PatagoniaListingSpider


class PatagoniaListingSpiderTest(unittest.TestCase):
    def response(self, body):
        request = Request(
            "https://www.patagonia.com/api?cgid=new-arrivals",
            meta={"page": 1, "start": 0, "listing_url": "https://www.patagonia.com/shop/new-arrivals"},
        )
        body = body + (" " * max(0, 501 - len(body)))
        return HtmlResponse(request.url, request=request, body=body.encode(), encoding="utf-8")

    def test_parses_sfcc_api_tile_attributes_and_gtm(self):
        spider = PatagoniaListingSpider(category="new-arrivals", max_pages=1)
        response = self.response('''
        <product-tile-simple name="M's Jacket" url="/product/jacket/30355.html"
          image="/30355.jpg" hover-image="/30355-back.jpg" number-of-swatches="4.0"
          data-gtm='[{"ecommerce":{"items":[{"item_id":"30355","item_variation_id":"199346089197","item_brand":"Patagonia","item_color":"Blue","price":369}]}}]'>
          <product-tile-pricing primary-category="Snow Jackets" currency="USD"
            sale-price="369.0" list-price="399.0"></product-tile-pricing>
        </product-tile-simple>''')

        item = list(spider.parse_api(response))[0]
        self.assertEqual(item["item_id"], "30355")
        self.assertEqual(item["variant_id"], "199346089197")
        self.assertEqual(item["title"], "M's Jacket")
        self.assertEqual(item["price"], 369.0)
        self.assertEqual(item["original_price"], 399.0)
        self.assertEqual(item["swatch_count"], 4)
        self.assertEqual(item["image_url"], "https://www.patagonia.com/30355.jpg")

    def test_malformed_gtm_keeps_attribute_data(self):
        spider = PatagoniaListingSpider(category="new-arrivals", max_pages=1)
        response = self.response('''
        <product-tile-simple name="Fallback Tee" url="/product/tee/123.html"
          product-id="123" data-gtm="not-json">
          <product-tile-pricing currency="USD" sale-price="49"></product-tile-pricing>
        </product-tile-simple>''')
        item = list(spider.parse_api(response))[0]
        self.assertEqual((item["item_id"], item["title"], item["price"]), ("123", "Fallback Tee", 49.0))

    def test_api_request_uses_offset_and_api_source(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        request = next(spider.start_requests())
        self.assertIn("AsyncComponents-ProductList", request.url)
        self.assertIn("cgid=new-arrivals", request.url)
        self.assertIn("start=0", request.url)
        self.assertEqual(request.headers["X-Requested-With"], b"XMLHttpRequest")

    def test_challenge_page_emits_no_items(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        response = self.response("<html><title>Hang Tight! Routing to checkout...</title>" + " " * 600 + "</html>")
        self.assertEqual(list(spider.parse_api(response)), [])


if __name__ == "__main__":
    unittest.main()
