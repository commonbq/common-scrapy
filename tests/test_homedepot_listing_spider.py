import unittest
from collections.abc import Mapping
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.homedepot_listing_spider import (
    MAX_PROXY_RETRIES,
    HomeDepotListingSpider,
)

FIXTURE = Path("sample/homedepot-listing-products.html")

# Current live Apollo shape: the SearchModel sits under ROOT_QUERY and products
# are BaseProduct nodes referenced from a plain ``products`` list key.
LIVE_SHAPE = b"""<!doctype html><html><body><script>
window.__APOLLO_STATE__={"ROOT_QUERY":{"searchModel({\\"navParam\\":\\"N-5yc1vZc1xy\\"})":{"__typename":"SearchModel","products":[{"__ref":"base-searchNav-100000001"},{"__ref":"base-searchNav-100000002"}]}},"base-searchNav-100000001":{"__typename":"BaseProduct","itemId":"100000001","dataSources":"searchNav","identifiers":{"itemId":"100000001","storeSkuNumber":"1000123456","brandName":"Husky","productLabel":"16 oz. Fiberglass Claw Hammer","modelNumber":"H16F"},"pricing({\\"storeId\\":\\"8119\\"})":{"value":14.97,"original":17.97},"media":{"images":[{"url":"https://images.thdstatic.com/productImages/hammer_<SIZE>.jpg"}]},"reviews":{"ratingsReviews":{"averageRating":"4.7","totalReviews":"238"}}},"base-searchNav-100000002":{"__typename":"BaseProduct","itemId":"100000002","identifiers":{"itemId":"100000002","brandName":"DEWALT","productLabel":"20V MAX Cordless Drill Kit"},"pricing({\\"storeId\\":\\"8119\\"})":{"value":99},"media":{"images":[{"url":"https://images.thdstatic.com/productImages/drill_<SIZE>.jpg"}]},"reviews":{"ratingsReviews":{"averageRating":"4.5","totalReviews":"1542"}}}}
</script></body></html>"""

PROXY_ENVELOPE = (
    b'{"status":"We couldn\'t retrieve a successful response for this request. '
    b'Try stronger proxy settings"}'
)

class HomeDepotListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = HomeDepotListingSpider(category="tools", max_pages=1)

    def response(self, body=None, status=200, meta=None):
        body = body if body is not None else FIXTURE.read_bytes()
        request = Request(
            "https://www.homedepot.com/b/Tools/N-5yc1vZc1xy",
            meta=meta or {"category": "tools", "page": 1},
        )
        return TextResponse(request.url, body=body, encoding="utf-8",
                            status=status, request=request)

    def test_legacy_apollo_state_feed_contract(self):
        items = list(self.spider.parse(self.response()))
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["item_id"], "100000001")
        self.assertEqual(items[0]["price"], 14.97)
        self.assertEqual(items[0]["image_url"], "https://images.thdstatic.com/productImages/hammer_300.jpg")
        self.assertEqual(items[0]["timestamp"], self.spider.job_timestamp)
        self.assertEqual(items[1]["reviews_count"], 1542)

    def test_live_root_query_products_shape(self):
        items = list(self.spider.parse(self.response(LIVE_SHAPE)))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["item_id"], "100000001")
        self.assertEqual(items[0]["price"], 14.97)
        self.assertEqual(items[1]["item_id"], "100000002")

    def test_proxy_envelope_retries_then_fails_visibly(self):
        retry = list(self.spider.parse(self.response(PROXY_ENVELOPE)))
        self.assertEqual(len(retry), 1)
        self.assertEqual(retry[0].meta["proxy_retries"], 1)
        with self.assertRaisesRegex(RuntimeError, "blocked/proxy payload"):
            list(self.spider.parse(self.response(
                PROXY_ENVELOPE, meta={"category": "tools", "page": 1, "proxy_retries": MAX_PROXY_RETRIES})))

    def test_missing_contract_retries_then_fails_visibly(self):
        retry = list(self.spider.parse(self.response(b"<html></html>")))
        self.assertEqual(len(retry), 1)
        self.assertEqual(retry[0].meta["proxy_retries"], 1)
        with self.assertRaisesRegex(RuntimeError, "did not contain __APOLLO_STATE__"):
            list(self.spider.parse(self.response(
                b"<html></html>", meta={"category": "tools", "page": 1, "proxy_retries": MAX_PROXY_RETRIES})))

    def test_categories_use_grouped_department_mapping(self):
        self.assertIsInstance(self.spider.categories, Mapping)
        self.assertEqual(len(self.spider.categories), 26)
        self.assertIn("tools", self.spider.categories)
        self.assertEqual(len(list(self.spider.iter_categories())), 393)
        self.assertEqual(
            self.spider.category_entry("tools")["url"],
            "https://www.homedepot.com/b/Tools/N-5yc1vZc1xy",
        )

    def test_subcategory_leaf_resolves_inside_its_department(self):
        entry = self.spider.category_entry("tools-power-tools")
        self.assertEqual(entry["group"], "tools")
        self.assertEqual(
            entry["url"],
            "https://www.homedepot.com/b/Tools-Power-Tools/N-5yc1vZc298",
        )

    def test_leaf_keys_and_urls_are_globally_unique(self):
        entries = list(self.spider.iter_categories())
        self.assertEqual(len({e["category"] for e in entries}), len(entries))
        self.assertEqual(len({e["url"] for e in entries}), len(entries))

    def test_department_hub_leaf_is_last_in_its_group(self):
        # The DAG schedules only the first three leaves per group, so the hub must
        # sort last for the scheduled tasks to stay real subcategory PLPs.
        for group, leaves in self.spider.categories.items():
            self.assertEqual(list(leaves)[-1], group, group)
            self.assertGreaterEqual(len(leaves), 4, group)


if __name__ == "__main__":
    unittest.main()
