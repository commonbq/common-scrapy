from __future__ import annotations

import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.ssense_categories import SSENSE_CATEGORIES
from common.spiders.ssense_listing_spider import SsenseListingSpider


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]


def document(payload: str) -> str:
    return f"<script>self.__next_f.push([1,{json.dumps(payload)}])</script>"


PAYLOAD = r'''b:["$","x",null,{"fields":{"itemListId":"product_listing_page","products":[{"productId":"15856491","productName":"Gray Cargo Pants","brandId":"238","brandName":"Rick Owens","allCategoryIds":["3","191"],"gender":"men","finalPrice":980,"regularPrice":1400,"currency":"USD"}]}}]
74:["$","x",null,{"children":[["$","x","15856491",{}]]}]
75:["$","x",null,{"paginationInfo":{"currentPage":1,"totalPages":3}}]
79:["$","x",null,{"href":"/men/product/rick-owens/gray-cargo-pants/15856491","children":[["$","div",null,{"src":"https://res.cloudinary.com/ssenseweb/image/upload/b_white/__IMAGE_PARAMS__/242232M188005_1.jpg"}]]}]
'''


class SsenseListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = SsenseListingSpider(category="men-clothing", max_pages=2)

    def response(self, payload: str = PAYLOAD):
        url = "https://www.ssense.com/en-us/men/clothing"
        request = Request(url, meta={"page": 1, "base_url": url})
        return TextResponse(url, request=request, body=document(payload), encoding="utf-8")

    def test_category_inventory(self):
        rows = _FLAT(SSENSE_CATEGORIES)
        self.assertEqual(len(rows), 20)
        self.assertEqual(len({row["category"] for row in rows}), 20)

    def test_rsc_item_mapping_feed_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.response()))
        item = next(value for value in outputs if isinstance(value, dict))
        request = next(value for value in outputs if not isinstance(value, dict))
        self.assertEqual(item["item_id"], "15856491")
        self.assertEqual(item["sku"], "242232M188005")
        self.assertEqual(item["brand"], "Rick Owens")
        self.assertEqual(item["price"], 980)
        self.assertEqual(item["original_price"], 1400)
        self.assertTrue(item["on_sale"])
        self.assertEqual(item["source"], "ssense_next_rsc_bootstrap")
        self.assertEqual(item["url"], "https://www.ssense.com/en-us/men/product/rick-owens/gray-cargo-pants/15856491")
        self.assertIn("f_auto,q_85,w_640", item["image_url"])
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(request.url, "https://www.ssense.com/en-us/men/clothing?page=2")

    def test_no_html_or_json_ld_fallback(self):
        html_only = '<a href="/product/1"><script type="application/ld+json">{}</script></a>'
        url = "https://www.ssense.com/en-us/men/clothing"
        request = Request(url, meta={"page": 1, "base_url": url})
        response = TextResponse(url, request=request, body=html_only, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "no Next.js RSC"):
            list(self.spider.parse(response))

    def test_duplicate_ids_are_suppressed(self):
        first = [value for value in self.spider.parse(self.response()) if isinstance(value, dict)]
        second = [value for value in self.spider.parse(self.response()) if isinstance(value, dict)]
        self.assertEqual(len(first), 1)
        self.assertEqual(second, [])

    def test_all_analytics_batches_are_collected(self):
        second = PAYLOAD.replace('"15856491"', '"20000002"').replace(
            "gray-cargo-pants/15856491", "second-product/20000002"
        )
        flight = self.spider._flight_payload(document(PAYLOAD + second))
        self.assertEqual(
            [row["productId"] for row in self.spider._products(flight)],
            ["15856491", "20000002"],
        )

    def test_challenge_is_rejected(self):
        response = self.response(PAYLOAD)
        response = TextResponse(
            response.url,
            request=response.request,
            body="<title>Just a moment...</title>",
            encoding="utf-8",
            status=403,
        )
        with self.assertRaisesRegex(RuntimeError, "challenge/proxy"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
