import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.overstock_listing_spider import OverstockListingSpider


def flight_html(rows):
    chunk = json.dumps("\n".join(rows))
    return f"<html><script>self.__next_f.push([1,{chunk}])</script></html>"


class OverstockListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = OverstockListingSpider(category="furniture", max_pages=2)

    def response(self, body, page=1):
        request = Request(
            "https://www.overstock.com/c/furniture?t=24352",
            meta={"target": self.spider.categories[0], "page": page},
        )
        return HtmlResponse(request.url, request=request, body=body, encoding="utf-8")

    def test_bootstrap_items_feed_contract_and_pagination(self):
        ecommerce = {
            "grs_filter": "attributes.taxonomy_id: ANY(24352)",
            "item_list_id": 24352,
            "item_list_name": "Furniture",
            "search_filter": [],
            "page_number": 1,
            "sort_order": "Best Selling",
            "items": [{
                "product_id": 43594621, "option_id": None, "item_id": "46634829",
                "item_name": "Comfy Cloud Modular Sectional Sofa", "is_spa": False,
                "index": 0, "price": 144.49, "discount": 0,
                "image_url": "https://ak1.ostkcdn.com/cloud.jpg",
                "product_rating": 3.67, "product_num_reviews": 3,
            }],
        }
        article = ["$", "article", "43594621", {
            "data-testid": "product-1",
            "children": ["$", "a", None, {
                "href": "https://www.overstock.com/Home-Garden/cloud/43594621/product.html?ref=x"
            }],
        }]
        rows = [
            "3f:" + json.dumps(["$", "component", None, {"viewItemList": {"ecommerce": ecommerce}}], separators=(",", ":")),
            "81:" + json.dumps(article, separators=(",", ":")),
            "78:" + json.dumps(["$", "pager", None, {"hitsPerPage": 48, "page": 1, "totalPages": 84, "nextPageUrl": "https://www.overstock.com/c/furniture?t=24352&page=2"}], separators=(",", ":")),
        ]

        output = list(self.spider.parse(self.response(flight_html(rows))))
        self.assertEqual(len(output), 2)
        item, request = output
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "43594621")
        self.assertEqual(item["sku"], "46634829")
        self.assertEqual(item["price"], 144.49)
        self.assertEqual(item["rating"], 3.67)
        self.assertEqual(item["url"], "https://www.overstock.com/Home-Garden/cloud/43594621/product.html")
        self.assertEqual(item["source"], "overstock_nextjs_rsc_view_item_list")
        self.assertEqual(request.url, "https://www.overstock.com/c/furniture?t=24352&page=2")

    def test_missing_hydration_and_challenge_fail_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "self.__next_f"):
            list(self.spider.parse(self.response("<html></html>")))
        with self.assertRaisesRegex(RuntimeError, "challenge"):
            list(self.spider.parse(self.response("<html>CAPTCHA</html>")))

    def test_catalog_has_twenty_verified_targets(self):
        self.assertEqual(len(self.spider.categories), 20)
        self.assertEqual(len({entry["url"] for entry in self.spider.categories}), 20)


if __name__ == "__main__":
    unittest.main()
