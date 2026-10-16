import unittest
from collections.abc import Mapping

from scrapy.http import HtmlResponse, Request

from common.spiders.patagonia_listing_spider import PatagoniaListingSpider


class PatagoniaListingSpiderTest(unittest.TestCase):
    def response(self, body, *, url="https://www.patagonia.com/grid", meta=None):
        request = Request(
            url,
            meta=meta
            or {
                "page": 1,
                "start": 0,
                "cgid": "collections-new-arrivals",
                "listing_url": "https://www.patagonia.com/shop/new-arrivals",
            },
        )
        body = body + (" " * max(0, 501 - len(body)))
        return HtmlResponse(request.url, request=request, body=body.encode(), encoding="utf-8")

    def test_parses_grid_tile_attributes_and_gtm(self):
        spider = PatagoniaListingSpider(category="new-arrivals", max_pages=1)
        response = self.response('''
        <product-tile data-pid="28442" data-gtm='[{"ecommerce":{"items":[{"item_id":"28442","item_variation_id":"195699994546","item_name":"Womens Parka","item_brand":"Patagonia","price":365}]}}]'>
          <meta itemprop="image" content="https://dis.patagonia.com/28442_BLSG.jpg">
          <a href="/product/womens-parka/28442.html"></a>
          <product-tile-pricing primary-category="Womens Parkas" currency="USD"
            sale-price="365.0" list-price="399.0"></product-tile-pricing>
        </product-tile>''')

        item = list(spider.parse_api(response))[0]
        self.assertEqual(item["item_id"], "28442")
        self.assertEqual(item["variant_id"], "195699994546")
        self.assertEqual(item["title"], "Womens Parka")
        self.assertEqual(item["price"], 365.0)
        self.assertEqual(item["original_price"], 399.0)
        self.assertEqual(item["url"], "https://www.patagonia.com/product/womens-parka/28442.html")
        self.assertEqual(item["image_url"], "https://dis.patagonia.com/28442_BLSG.jpg")
        self.assertEqual(item["source"], "patagonia_sfcc_search_grid")

    def test_parses_legacy_simple_tile(self):
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

    def test_skips_lazy_placeholder_image(self):
        spider = PatagoniaListingSpider(category="new-arrivals", max_pages=1)
        response = self.response('''
        <product-tile data-pid="1" data-gtm='[{"ecommerce":{"items":[{"item_id":"1","price":10}]}}]'>
          <img class="product-tile__cover-image"
            src="https://www.patagonia.com/on/demandware.static/Sites-patagonia-us-Site/-/default/dw238ef249/images/1x1.png">
          <product-tile-image base="https://dis.patagonia.com/real_1.jpg"></product-tile-image>
          <product-tile-pricing currency="USD" sale-price="10"></product-tile-pricing>
        </product-tile>''')
        item = list(spider.parse_api(response))[0]
        self.assertEqual(item["image_url"], "https://dis.patagonia.com/real_1.jpg")

    def test_categories_are_grouped_full_navigation_inventory(self):
        categories = PatagoniaListingSpider.categories
        self.assertIsInstance(categories, Mapping)
        self.assertTrue(all(isinstance(leaves, Mapping) for leaves in categories.values()))
        self.assertEqual(len(categories), 7)
        self.assertEqual(sum(len(leaves) for leaves in categories.values()), 144)
        self.assertEqual(
            PatagoniaListingSpider(category="new-arrivals").resolve_target_url(),
            "https://www.patagonia.com/shop/new-arrivals",
        )
        self.assertEqual(
            PatagoniaListingSpider(category="packs-gear").resolve_target_url(),
            "https://www.patagonia.com/shop/gear",
        )

    def test_malformed_gtm_keeps_attribute_data(self):
        spider = PatagoniaListingSpider(category="new-arrivals", max_pages=1)
        response = self.response('''
        <product-tile-simple name="Fallback Tee" url="/product/tee/123.html"
          product-id="123" data-gtm="not-json">
          <product-tile-pricing currency="USD" sale-price="49"></product-tile-pricing>
        </product-tile-simple>''')
        item = list(spider.parse_api(response))[0]
        self.assertEqual((item["item_id"], item["title"], item["price"]), ("123", "Fallback Tee", 49.0))

    def test_start_requests_fetch_listing_page_then_grid(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        request = next(spider.start_requests())
        self.assertEqual(request.url, "https://www.patagonia.com/shop/new-arrivals")

        grid = spider._api_request(
            request.url, cgid="collections-new-arrivals", page=1, start=0
        )
        self.assertIn("Search-UpdateGrid", grid.url)
        self.assertIn("cgid=collections-new-arrivals", grid.url)
        self.assertIn("start=0", grid.url)
        self.assertEqual(grid.headers["X-Requested-With"], b"XMLHttpRequest")

    def test_extracts_cgid_from_listing_page(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        response = self.response(
            '<a href="/shop/new-arrivals?cgid=collections-new-arrivals">x</a>',
            url="https://www.patagonia.com/shop/new-arrivals",
        )
        self.assertEqual(spider._extract_cgid(response), "collections-new-arrivals")

    def test_extract_cgid_ignores_root(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        response = self.response('<a href="/?cgid=root">x</a>')
        self.assertIsNone(spider._extract_cgid(response))

    def test_challenge_page_emits_no_items(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        response = self.response("<html><title>Hang Tight! Routing to checkout...</title>" + " " * 600 + "</html>")
        self.assertEqual(list(spider.parse_api(response)), [])

    def test_recaptcha_config_is_not_a_challenge(self):
        spider = PatagoniaListingSpider(category="new-arrivals")
        response = self.response(
            '<script>{"recaptcha":{"enabled":true}}</script>'
            '<a href="/shop/new-arrivals?cgid=collections-new-arrivals">x</a>',
            url="https://www.patagonia.com/shop/new-arrivals",
        )
        self.assertFalse(spider._blocked(response))


if __name__ == "__main__":
    unittest.main()
