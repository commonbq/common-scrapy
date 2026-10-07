import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.hobbylobby_categories import HOBBY_LOBBY_CATEGORIES
from common.spiders.hobbylobby_listing_spider import HobbylobbyListingSpider

URL = HOBBY_LOBBY_CATEGORIES["art-supplies-painting-supplies"]


def hit(object_id="80968391"):
    return {
        "objectID": object_id,
        "sku": "636449",
        "productID": "product-uuid",
        "productKey": "RS52220-80968391",
        "name": "Master's Touch Oil Paint - 12 Piece Set",
        "variantUrl": "/art-supplies/painting-supplies/oil-painting/set/p/80968391",
        "pdpUrl": "/art-supplies/painting-supplies/oil-painting/set/p/rs52220-80968391",
        "brand": "Master's Touch",
        "variant.price": 6.99,
        "product.lowestPrice": 6.99,
        "product.highestPrice": 6.99,
        "product.lowestOriginalPrice": 8.99,
        "product.highestOriginalPrice": 8.99,
        "isInStock": True,
        "availability": "BOTH",
        "onlineStatus": "ACTIVE",
        "department": "Art Supplies",
        "category": "Painting Supplies",
        "subcategory": "Oil Painting",
        "categoryNames": ["Art Supplies", "Painting Supplies", "Oil Painting"],
        "categories": {"lvl0": ["Art Supplies"]},
        "categoryKeys": ["8", "8-168", "8-168-1310"],
        "quantity": "12 Count",
        "medium": ["Oil"],
        "color": "Assorted Colors",
        "color-family": "multi",
        "material": ["Paint"],
        "ratings.average": 3.8571,
        "ratings.count": 7,
        "images": [{"url": "https://cdn.example/636449"}],
        "product.description": "<p>Student-grade oil paint.</p>",
    }


def response_for(hits=None, page=0, pages=2):
    payload = {
        "HLNextGenEcommIndex_prd": {
            "state": {"index": "HLNextGenEcommIndex_prd"},
            "results": [{"hits": hits or [hit()], "nbHits": 24, "page": page,
                         "nbPages": pages, "hitsPerPage": 12}],
        }
    }
    body = (
        '<script>window[Symbol.for("InstantSearchInitialResults")] = '
        + json.dumps(payload)
        + ';</script>'
    )
    return HtmlResponse(URL, request=Request(URL), body=body.encode(), encoding="utf-8")


class HobbyLobbyListingSpiderTests(unittest.TestCase):
    def test_categories_have_twenty_product_bearing_seeds(self):
        self.assertEqual(len(HOBBY_LOBBY_CATEGORIES), 20)
        self.assertTrue(all("/c/" in url for url in HOBBY_LOBBY_CATEGORIES.values()))

    def test_brace_matched_bootstrap_and_item_contract(self):
        spider = HobbylobbyListingSpider(
            category="art-supplies-painting-supplies", max_pages="2"
        )
        outputs = list(spider.parse(response_for(), URL, URL, 1))
        item = outputs[0]
        self.assertEqual(set(item), set(spider.custom_settings["FEED_EXPORT_FIELDS"]))
        self.assertEqual(item["item_id"], "80968391")
        self.assertEqual(item["title"], "Master's Touch Oil Paint - 12 Piece Set")
        self.assertEqual(item["price"], 6.99)
        self.assertTrue(item["in_stock"])
        self.assertEqual(item["source"], "hobbylobby_instantsearch_bootstrap")
        self.assertEqual(outputs[1].url, f"{URL}?page=2")

    def test_semicolon_inside_hit_does_not_truncate_json(self):
        record = hit()
        record["product.description"] = "<p>Oil; acrylic &amp; more</p>"
        payload = HobbylobbyListingSpider._extract_bootstrap(response_for([record]).text, URL)
        result = HobbylobbyListingSpider._search_result(payload, URL)
        self.assertEqual(result["hits"][0]["product.description"], record["product.description"])

    def test_missing_bootstrap_fails_without_fallback(self):
        with self.assertRaisesRegex(RuntimeError, "no HTML-card or JSON-LD fallback"):
            HobbylobbyListingSpider._extract_bootstrap("<html></html>", URL)

    def test_pagination_stops_at_max_pages(self):
        spider = HobbylobbyListingSpider(
            category="art-supplies-painting-supplies", max_pages="1"
        )
        outputs = list(spider.parse(response_for(), URL, URL, 1))
        self.assertEqual(len(outputs), 1)


if __name__ == "__main__":
    unittest.main()
