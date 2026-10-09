from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.mediamarkt_categories import MEDIAMARKT_CATEGORIES
from common.spiders.mediamarkt_listing_spider import MediamarktListingSpider


def document(state: dict, *, undefined: bool = False) -> str:
    payload = json.dumps(state, separators=(",", ":"))
    if undefined:
        payload = payload.replace('"optional":null', '"optional":undefined')
    return f'<script type="application/ld+json">{{"@type":"ItemList"}}</script>' \
           f'<script>window.__PRELOADED_STATE__ = {payload};</script>'


STATE = {
    "optional": None,
    "apolloState": {
        "ProductList:test": {
            "__typename": "ProductList", "maxPage": 3, "totalProducts": 25,
            "endPage": 1, "loadedPages": [1], "pageSize": 12,
        },
        "ProductListPage:test": {
            "__typename": "ProductListPage",
            "products": [{"__typename": "ProductListProduct", "productId": "3037446"}],
        },
        "GraphqlProduct:Media:de-DE:3037446": {
            "__typename": "GraphqlProduct", "id": "3037446", "title": "Galaxy Book",
            "manufacturer": "SAMSUNG", "url": "/de/product/_galaxy-book-3037446.html",
            "breadcrumbs": [
                {"categoryId": "CAT_DE_MM_344", "name": "Computer & Büro"},
                {"categoryId": "CAT_DE_MM_362", "name": "Laptops & Notebooks"},
            ],
        },
        "CofrCoreFeature:Media:de:3037446": {
            "__typename": "CofrCoreFeature", "id": "Media:de:3037446",
            "ean": "8806099213626", "isProductOfTypeMarketplace": False,
            "reviewStatistics": {"averageOverallRating": 4.8333, "totalReviewCount": 30},
            "highlightedFeatures": [{"__ref": "feature:processor"}],
        },
        "feature:processor": {
            "__typename": "CofrCoreFeatureProductFeature", "id": "feature:processor",
            "name": "Prozessor", "values": "Snapdragon X",
        },
        "CofrPriceFeature:test": {
            "__typename": "CofrPriceFeature", "id": "Media:de:3037446", "currency": "EUR",
            "price": {"amount": 629, "discount": 390, "discountPercentage": 38, "shippingCost": 0},
            "strikePrice": {"amount": 1019}, "marketplaceSeller": None,
        },
        "CofrMediaAssetsFeature:Media:de:3037446": {
            "__typename": "CofrMediaAssetsFeature", "id": "Media:de:3037446",
            "productMainImage": {"link": "https://assets.example/3037446", "altText": "Laptop"},
        },
        "CofrOnlineStatusFeature:Media:de:3037446": {
            "__typename": "CofrOnlineStatusFeature", "id": "Media:de:3037446",
            "onlineStatus": "AVAILABLE", "isAvailableAndBuyable": True,
        },
        "CofrBadgesFeature:Media:de:3037446": {
            "__typename": "CofrBadgesFeature", "id": "Media:de:3037446",
            "computedBadges": [{"name": "Aus unserer Werbung"}],
        },
    },
}


class MediamarktListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = MediamarktListingSpider(category="Computer & Büro", max_pages=2)

    def response(self, state: dict = STATE, *, undefined: bool = False):
        url = MEDIAMARKT_CATEGORIES[0]["url"]
        request = Request(url, meta={"page": 1, "base_url": url})
        return TextResponse(
            url, request=request, body=document(state, undefined=undefined), encoding="utf-8"
        )

    def test_category_inventory(self):
        self.assertEqual(len(MEDIAMARKT_CATEGORIES), 20)
        self.assertEqual(len({row["category"] for row in MEDIAMARKT_CATEGORIES}), 20)
        self.assertTrue(all(row["url"].startswith("https://www.mediamarkt.de/") for row in MEDIAMARKT_CATEGORIES))

    def test_bootstrap_mapping_feed_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.response(undefined=True)))
        item = next(value for value in outputs if isinstance(value, dict))
        request = next(value for value in outputs if not isinstance(value, dict))
        self.assertEqual(item["item_id"], "3037446")
        self.assertEqual(item["ean"], "8806099213626")
        self.assertEqual(item["title"], "Galaxy Book")
        self.assertEqual(item["brand"], "SAMSUNG")
        self.assertEqual(item["price"], 629)
        self.assertEqual(item["original_price"], 1019)
        self.assertEqual(item["currency"], "EUR")
        self.assertEqual(item["rating"], 4.8333)
        self.assertEqual(item["category_path"], ["Computer & Büro", "Laptops & Notebooks"])
        self.assertEqual(item["features"], {"Prozessor": "Snapdragon X"})
        self.assertEqual(item["source"], "mediamarkt_preloaded_apollo_bootstrap")
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(request.url, MEDIAMARKT_CATEGORIES[0]["url"] + "?page=2")

    def test_uses_listing_product_order_not_all_hydrated_products(self):
        state = json.loads(json.dumps(STATE))
        state["apolloState"]["GraphqlProduct:Media:de-DE:999"] = {
            "__typename": "GraphqlProduct", "id": "999", "title": "Teaser product"
        }
        items = [value for value in self.spider.parse(self.response(state)) if isinstance(value, dict)]
        self.assertEqual([item["item_id"] for item in items], ["3037446"])

    def test_no_json_ld_or_html_fallback(self):
        url = MEDIAMARKT_CATEGORIES[0]["url"]
        request = Request(url, meta={"page": 1, "base_url": url})
        response = TextResponse(
            url,
            request=request,
            body='<script type="application/ld+json">{"@type":"ItemList"}</script><article>card</article>',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "no __PRELOADED_STATE__"):
            list(self.spider.parse(response))

    def test_duplicate_ids_are_suppressed(self):
        first = [value for value in self.spider.parse(self.response()) if isinstance(value, dict)]
        second = [value for value in self.spider.parse(self.response()) if isinstance(value, dict)]
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])

    def test_challenge_is_rejected(self):
        response = self.response()
        response = TextResponse(
            response.url, request=response.request, body="<title>Just a moment...</title>",
            encoding="utf-8", status=403,
        )
        with self.assertRaisesRegex(RuntimeError, "challenge/proxy"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
