import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.flipkart_categories import FLIPKART_CATEGORIES
from common.spiders.flipkart_listing_spider import FlipkartListingSpider


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]


class FlipkartListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = FlipkartListingSpider(category="rings", max_pages=2)

    def response(self):
        state = {"pageDataV4": {"page": {"data": {
            "10004": [{"widget": {"data": {"title": "Rings", "totalProducts": 70450}}}],
            "10003": [
                {"id": "8001000", "widget": {"data": {"products": [{"productInfo": {
                    "value": {
                        "id": "RNGH8KGEJEFTVSQB",
                        "titles": {"title": "Crystal Ring", "subtitle": "Adjustable"},
                        "pricing": {"prices": [
                            {"priceType": "FSP", "value": 599, "currency": "INR"},
                            {"priceType": "SPECIAL_PRICE", "value": 301, "currency": "INR"},
                        ], "totalDiscount": 49},
                        "media": {"images": [{"url": "http://img/{@width}/{@height}?q={@quality}"}]},
                        "rating": {"average": 4.2, "count": 17},
                    },
                    "action": {"url": "/crystal-ring/p/itm123?pid=RNG123"},
                }}]}}},
                {"id": 9, "widget": {"data": {"currentPage": 1, "totalPages": 1762}}},
            ],
        }}}}
        url = _FLAT(FLIPKART_CATEGORIES)[0]["url"]
        body = "<script>window.__INITIAL_STATE__ = " + json.dumps(state) + ";</script>"
        request = Request(url, meta={"category": "rings", "category_name": "Rings", "page": 1})
        return TextResponse(url, request=request, body=body, encoding="utf-8")

    def test_extracts_bootstrap_product_and_prices(self):
        outputs = list(self.spider.parse(self.response()))
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "RNGH8KGEJEFTVSQB")
        self.assertEqual(item["title"], "Crystal Ring")
        self.assertEqual(item["price"], 301.0)
        self.assertEqual(item["was_price"], 599.0)
        self.assertEqual(item["discount_pct"], 49.0)
        self.assertEqual(item["currency"], "INR")
        self.assertEqual(item["total_count"], 70450)
        self.assertEqual(item["total_pages"], 1762)
        self.assertEqual(item["source"], "flipkart_initial_state_product_widgets")

    def test_uses_query_string_pagination(self):
        follow = list(self.spider.parse(self.response()))[-1]
        self.assertEqual(follow.url, _FLAT(FLIPKART_CATEGORIES)[0]["url"] + "&page=2")

    def test_taxonomy_has_20_unique_categories(self):
        rows = _FLAT(FLIPKART_CATEGORIES)
        self.assertEqual(len(rows), 20)
        self.assertEqual(len({row["category"] for row in rows}), 20)

    def test_missing_bootstrap_fails_visibly(self):
        response = self.response().replace(body=b"<html></html>")
        with self.assertRaisesRegex(RuntimeError, "no window.__INITIAL_STATE__"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
