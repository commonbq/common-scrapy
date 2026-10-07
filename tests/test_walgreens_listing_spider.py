import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.walgreens_listing_spider import WalgreensListingSpider

URL = "https://www.walgreens.com/store/c/allergy-and-sinus/ID=360545-tier2general"


def product(product_id="prod6335256"):
    return {
        "prodId": product_id,
        "skuId": "sku6279388",
        "articleId": "585352",
        "upc": "049022585352",
        "productDisplayName": "Walgreens Neti Pot Kit",
        "productURL": f"/store/c/item/ID={product_id}-product",
        "imageUrl450": "//pics.walgreens.com/prodimg/585352/450.jpg",
        "brandName": "Walgreens",
        "averageRating": "4.0",
        "reviewCount": "199",
        "onlineInvStatus": "instock",
        "priceInfo": {"regularPrice": "$14.99", "salePrice": "$11.99"},
    }


def response(products=None, page=1, pages=2):
    state = {"searchResult": {"productList": [{"productInfo": p} for p in (products or [])],
        "summary": {"p": str(page), "totalNumPages": str(pages), "productInfoCount": "48"}}}
    body = f"<script>window.getInitialState = function () {{ return {json.dumps(state)}; }};</script>"
    request = Request(URL)
    return HtmlResponse(URL, request=request, body=body.encode(), encoding="utf-8")


class WalgreensListingTests(unittest.TestCase):
    def test_category_and_url_precedence(self):
        spider = WalgreensListingSpider(category="Allergy & Sinus")
        self.assertEqual(spider.resolve_target_url(), URL)
        direct = WalgreensListingSpider(category="Allergy & Sinus", url="https://www.walgreens.com/store/c/productlist/N=1/1/ShopAll=1")
        self.assertIn("ShopAll=1", direct.resolve_target_url())

    def test_hydration_and_normalization(self):
        spider = WalgreensListingSpider(category="Allergy & Sinus")
        item = next(iter(spider.parse(response([product()]), URL, 1)))
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["product_id"], "prod6335256")
        self.assertEqual(item["price"], 11.99)
        self.assertEqual(item["regular_price"], 14.99)
        self.assertEqual(item["image"], "https://pics.walgreens.com/prodimg/585352/450.jpg")
        self.assertEqual(item["reviews_count"], 199)

    def test_challenge_and_malformed_state_fail(self):
        spider = WalgreensListingSpider(category="Allergy & Sinus")
        blocked = HtmlResponse(URL, request=Request(URL), body=b"bm-verify /_sec/verify", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Akamai challenge"):
            list(spider.parse(blocked, URL, 1))
        malformed = HtmlResponse(URL, request=Request(URL), body=b"window.getInitialState=function(){return {bad", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Invalid"):
            list(spider.parse(malformed, URL, 1))

    def test_pagination_and_repeat_guard(self):
        spider = WalgreensListingSpider(category="Allergy & Sinus", max_pages=2)
        output = list(spider.parse(response([product()], pages=3), URL, 1))
        self.assertEqual(len(output), 2)
        self.assertIsInstance(output[-1], Request)
        self.assertIn("/2/ShopAll=360545", output[-1].url)
        self.assertEqual(list(spider.parse(response([product()], page=2), URL, 2)), [])

    def test_empty_and_max_page_stop(self):
        empty = WalgreensListingSpider(category="Allergy & Sinus", max_pages=3)
        self.assertEqual(list(empty.parse(response([]), URL, 1)), [])
        one = WalgreensListingSpider(category="Allergy & Sinus", max_pages=1)
        self.assertEqual(len(list(one.parse(response([product()]), URL, 1))), 1)

    def test_proxy_options_are_applied_without_secret_constants(self):
        spider = WalgreensListingSpider(category="Allergy & Sinus")
        spider.settings = {"PROXY": "http://user:secret@proxy.scrapeops.io:5353"}
        proxy = spider._render_proxy()
        self.assertIn("render_js=true", proxy)
        self.assertIn("country=us", proxy)
