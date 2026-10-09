from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.gymshark_categories import GYMSHARK_CATEGORIES
from common.spiders.gymshark_listing_spider import GymsharkListingSpider


HIT = {
    "id": 6806409347274,
    "sku": "A4B9W",
    "title": "Power T-Shirt",
    "type": "Mens>Apparel>SS Tops>t_shirt",
    "handle": "gymshark-power-t-shirt-black",
    "featuredMedia": {"src": "https://cdn.shopify.com/power.jpg", "alt": "Power T-Shirt"},
    "colour": "Black/Red",
    "canonicalColour": "black",
    "gender": ["m"],
    "fit": "oversized fit",
    "activities": ["lifting"],
    "price": 36,
    "compareAtPrice": 45,
    "discountPercentage": 20,
    "inStock": True,
    "sizeInStock": ["s", "m"],
    "availableSizes": [
        {"id": 1, "size": "s", "sku": "A4B9W-S", "inStock": True, "inventoryQuantity": 2, "price": 36},
        {"id": 2, "size": "m", "sku": "A4B9W-M", "inStock": True, "inventoryQuantity": 3, "price": 36},
    ],
    "rating": {"average": 4.25, "count": 12, "range": 5},
    "labels": ["popular"],
}


def response_for(query: dict, *, page_index: int = 0) -> TextResponse:
    payload = {"props": {"pageProps": {"ssrQuery": query}}}
    html = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'
    url = "https://www.gymshark.com/collections/all-products"
    request = Request(url, meta={"page_index": page_index, "base_url": url, "category": "all-products"})
    return TextResponse(url, request=request, body=html, encoding="utf-8")


class GymsharkListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = GymsharkListingSpider(category="all-products", max_pages=2)

    def test_top_twenty_category_inventory(self):
        self.assertEqual(len(GYMSHARK_CATEGORIES), 20)
        self.assertEqual(len({row["category"] for row in GYMSHARK_CATEGORIES}), 20)

    def test_hydration_mapping_feed_contract_and_pagination(self):
        query = {"hits": [HIT], "nbHits": 121, "hitsPerPage": 60, "page": 0, "nbPages": 17, "queryID": "qid"}
        outputs = list(self.spider.parse(response_for(query)))
        item = next(row for row in outputs if isinstance(row, dict))
        request = next(row for row in outputs if not isinstance(row, dict))
        self.assertEqual(item["item_id"], "6806409347274")
        self.assertEqual(item["price"], 36)
        self.assertEqual(item["inventory_quantity"], 5)
        self.assertEqual(item["rating"], 4.25)
        self.assertEqual(item["total_pages"], 3)
        self.assertEqual(item["source"], "gymshark_next_data_ssr_query")
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(request.url, "https://www.gymshark.com/collections/all-products?page=1")

    def test_hydrated_total_not_capped_nbpages_drives_pagination(self):
        query = {"hits": [HIT], "nbHits": 2471, "hitsPerPage": 60, "page": 0, "nbPages": 17}
        item = next(row for row in self.spider.parse(response_for(query)) if isinstance(row, dict))
        self.assertEqual(item["total_pages"], 42)

    def test_no_html_or_json_ld_fallback(self):
        url = "https://www.gymshark.com/collections/all-products"
        html = '<article role="listitem">Power T-Shirt</article><script type="application/ld+json">{}</script>'
        response = TextResponse(url, request=Request(url), body=html, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "no #__NEXT_DATA__"):
            list(self.spider.parse(response))

    def test_duplicate_ids_are_suppressed(self):
        query = {"hits": [HIT, HIT], "nbHits": 2, "hitsPerPage": 60, "page": 0}
        items = [row for row in self.spider.parse(response_for(query)) if isinstance(row, dict)]
        self.assertEqual(len(items), 1)


if __name__ == "__main__":
    unittest.main()
