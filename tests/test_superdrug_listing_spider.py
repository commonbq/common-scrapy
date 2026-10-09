import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.superdrug_categories import SUPERDRUG_CATEGORIES
from common.spiders.superdrug_listing_spider import SuperdrugListingSpider


class SuperdrugListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = SuperdrugListingSpider(category="health-winter", max_pages=2)

    @staticmethod
    def response(model, page=1):
        body = (
            '<html><script id="spartacus-app-state" type="application/json">'
            + json.dumps({"mp-product-list.model$": model})
            + "</script></html>"
        ).encode()
        request = Request(
            "https://www.superdrug.com/health/cough-cold-flu/c/health-winter"
            f"?pageSize=8&currentPage={page - 1}",
            meta={
                "category": "health-winter",
                "base_url": SUPERDRUG_CATEGORIES["health-winter"],
                "page": page,
            },
        )
        return HtmlResponse(request.url, request=request, body=body, encoding="utf-8")

    @staticmethod
    def model(current_page=0):
        return {
            "products": [{
                "code": "406503",
                "baseProduct": "BP_406503",
                "ean": "04065036",
                "name": "Superdrug Max Day and Night Capsules x 16",
                "masterBrand": {"name": "Superdrug"},
                "url": "/cold-and-flu/p/406503",
                "images": {"PRIMARY": {"thumbnail": {"url": "https://media.superdrug.com/item.jpg"}}},
                "price": {"value": 1.99, "oldValue": 2.39, "currencyIso": "GBP"},
                "stock": {"stockLevelStatus": "inStock"},
                "averageRating": 4.6,
                "numberOfReviews": 11,
                "ageRestricted": True,
                "licensedType": "GSL",
                "categoryNameHierarchy": "Health/Cough, Cold & Flu",
                "promotions": [{"promotionUrl": "/a/offer"}],
            }],
            "pagination": {
                "currentPage": current_page,
                "pageSize": 8,
                "totalPages": 24,
                "totalResults": 189,
            },
        }

    def test_categories_are_a_dict(self):
        self.assertIsInstance(SUPERDRUG_CATEGORIES, dict)
        self.assertEqual(
            self.spider.resolve_target_url(), SUPERDRUG_CATEGORIES["health-winter"]
        )

    def test_parses_bootstrap_and_schedules_next_page(self):
        response = self.response(self.model())
        response.request.meta.update({"proxy": "http://proxy", "_auth_proxy": "secret"})
        output = list(self.spider.parse(response))
        item = output[0]
        self.assertEqual(item["item_id"], "406503")
        self.assertEqual(item["price"], 1.99)
        self.assertEqual(item["brand"], "Superdrug")
        self.assertEqual(item["total_count"], 189)
        self.assertEqual(item["source"], "superdrug_spartacus_bootstrap")
        self.assertEqual(output[1].url, SUPERDRUG_CATEGORIES["health-winter"] + "?pageSize=8&currentPage=1")
        self.assertNotIn("proxy", output[1].meta)
        self.assertNotIn("_auth_proxy", output[1].meta)

    def test_feed_contract_is_complete(self):
        item = list(self.spider.parse(self.response(self.model())))[0]
        fields = self.spider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertEqual(set(fields), set(item))

    def test_missing_bootstrap_fails_loudly(self):
        response = HtmlResponse(
            "https://www.superdrug.com/category",
            request=Request(
                "https://www.superdrug.com/category",
                meta={"category": "custom", "base_url": "https://www.superdrug.com/category", "page": 1},
            ),
            body=b"<html></html>",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "Spartacus app state"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
