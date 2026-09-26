from __future__ import annotations

import json
import unittest
from pathlib import Path

from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.ae_listing_spider import AeListingSpider


class AeListingSpiderTests(unittest.TestCase):
    def test_real_fastboot_shoebox_id_prefix_is_decoded(self):
        self.assertEqual(
            AeListingSpider._decode_shoebox_id(
                "shoebox-L2Jyb3dzZS92MS9jYXRlZ29yeS93b21lbnM"
            ),
            "/browse/v1/category/womens",
        )

    def test_navigation_shoebox_is_skipped_before_product_payload(self):
        navigation_id = "shoebox-L2Jyb3dzZS92MS9jYXRlZ29yeS93b21lbnMvbmF2aWdhdGlvbg"
        browse_id = "shoebox-L2Jyb3dzZS92MS9jYXRlZ29yeS93b21lbnM"
        html = f'''<html><body>
          <script type="fastboot/shoebox" id="{navigation_id}">
            {{"data": [], "included": []}}
          </script>
          <script type="fastboot/shoebox" id="{browse_id}">
            {{"data": {{}}, "included": [{{"type": "product"}}]}}
          </script>
        </body></html>'''
        response = HtmlResponse(
            url="https://www.ae.com/us/en/c/women/womens",
            body=html.encode(),
            encoding="utf-8",
        )

        path, payload = AeListingSpider._extract_shoebox_payload(response)

        self.assertEqual(path, "/browse/v1/category/womens")
        self.assertEqual(payload["included"][0]["type"], "product")

    def setUp(self):
        self.spider = AeListingSpider(category="women-tops", max_pages=3)
        self.sample_dir = Path(__file__).resolve().parents[1] / "sample"

    def response(self, request: Request, body: str | bytes, *, status: int = 200):
        if isinstance(body, str):
            body = body.encode("utf-8")
        return TextResponse(
            request.url,
            request=request,
            body=body,
            encoding="utf-8",
            status=status,
        )

    def test_category_dictionary_and_overrides(self):
        self.assertEqual(len(self.spider.categories), 29)
        self.assertEqual(
            self.spider.categories["women-tops"],
            "https://www.ae.com/us/en/c/women/tops/cat10049",
        )
        self.assertEqual(
            self.spider.categories["men-clearance"],
            "https://www.ae.com/us/en/c/men/clearance/clrmens",
        )
        self.assertEqual(
            self.spider.categories["aerie-all"],
            "https://www.ae.com/us/en/c/aerie/clothing-accessories/cat870009",
        )
        self.assertEqual(
            AeListingSpider(category="women-tops").resolve_target_url(),
            "https://www.ae.com/us/en/c/women/tops/cat10049",
        )
        self.assertEqual(
            AeListingSpider(
                category="women-tops", category_url="https://www.ae.com/custom"
            ).resolve_target_url(),
            "https://www.ae.com/custom",
        )
        self.assertEqual(
            AeListingSpider(
                category="women-tops", url="https://www.ae.com/override"
            ).resolve_target_url(),
            "https://www.ae.com/override",
        )
        with self.assertRaisesRegex(
            ValueError, r"Provide only one of -a url or -a category_url"
        ):
            AeListingSpider(
                category="women-tops",
                url="https://www.ae.com/override",
                category_url="https://www.ae.com/custom",
            ).resolve_target_url()

    def test_parse_html_uses_fastboot_payload_and_schedules_browse_page(self):
        body = (self.sample_dir / "ae-listing-sample.html").read_text(encoding="utf-8")
        request = Request(
            url="https://www.ae.com/us/en/c/women/tops/cat10049",
            meta={
                "page": 1,
                "category": "women-tops",
                "category_url": "https://www.ae.com/us/en/c/women/tops/cat10049",
            },
        )
        response = self.response(request, body)
        outputs = list(self.spider.parse_html(response))

        items = [x for x in outputs if isinstance(x, dict)]
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["item_id"], "1457_2980_808")
        self.assertEqual(items[0]["title"], "AE Big Hug V-Neck Sweatshirt")
        self.assertEqual(
            items[0]["url"],
            "https://www.ae.com/us/en/p/women/hoodies-sweatshirts/crew-neck-sweatshirts/ae-big-hug-v-neck-sweatshirt/1457_2980_808",
        )
        self.assertEqual(items[0]["price"], 38.97)
        self.assertEqual(items[0]["original_price"], 64.95)
        self.assertEqual(items[0]["rating"], 4.7)
        self.assertEqual(items[0]["reviews_count"], 123)
        self.assertEqual(items[0]["category"], "women-tops")

        follow = next(x for x in outputs if isinstance(x, Request))
        self.assertIn("/browse/v1/category/womens", follow.url)
        self.assertIn("offset=2", follow.url)
        self.assertIn("rows=2", follow.url)
        self.assertEqual(follow.meta["page"], 2)
        self.assertEqual(follow.meta["browse_path"], "/browse/v1/category/womens")

    def test_parse_browse_deduplicates_and_stops_at_total_products(self):
        page2_body = (self.sample_dir / "ae-listing-browse-page2.json").read_text(
            encoding="utf-8"
        )
        page2_request = Request(
            url="https://www.ae.com/browse/v1/category/womens?offset=2&rows=2",
            meta={
                "page": 2,
                "category": "women-tops",
                "category_url": "https://www.ae.com/us/en/c/women/tops/cat10049",
                "browse_path": "/browse/v1/category/womens",
            },
        )
        # Seed product seen on the initial shoebox payload.
        self.spider._seen_products.add("1457_1111_100")
        page2_outputs = list(self.spider.parse_browse(self.response(page2_request, page2_body)))
        page2_items = [x for x in page2_outputs if isinstance(x, dict)]
        self.assertEqual(len(page2_items), 1)
        self.assertEqual(page2_items[0]["item_id"], "1457_2222_200")
        self.assertEqual(page2_items[0]["reviews_count"], 1234)

        page3_request = next(x for x in page2_outputs if isinstance(x, Request))
        page3_payload = {
            "data": [],
            "included": [
                {
                    "type": "product",
                    "id": "prod-004",
                    "attributes": {
                        "id": "1457_3333_300",
                        "displayName": "AE Hoodie",
                        "url": "/us/en/p/women/tops/hoodies-sweatshirts/ae-hoodie/1457_3333_300",
                        "salePrice": 39.95,
                        "listPrice": 49.95,
                    },
                }
            ],
            "meta": {"offset": 4, "rows": 2, "totalProducts": 5},
        }
        page3_outputs = list(
            self.spider.parse_browse(
                self.response(page3_request, json.dumps(page3_payload))
            )
        )
        self.assertEqual(len(page3_outputs), 1)
        self.assertEqual(page3_outputs[0]["item_id"], "1457_3333_300")

    def test_start_requests_resets_seen_products_for_new_run(self):
        self.spider._seen_products.add("1457_1111_100")
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), 1)
        self.assertEqual(self.spider._seen_products, set())

    def test_zero_product_and_blocked_pages_yield_no_results(self):
        empty_body = (self.sample_dir / "ae-listing-empty.html").read_text(encoding="utf-8")
        blocked_body = (self.sample_dir / "ae-listing-blocked.html").read_text(
            encoding="utf-8"
        )
        request = Request(
            url="https://www.ae.com/us/en/c/women/tops/cat10049",
            meta={
                "page": 1,
                "category": "women-tops",
                "category_url": "https://www.ae.com/us/en/c/women/tops/cat10049",
            },
        )
        self.assertEqual(list(self.spider.parse_html(self.response(request, empty_body))), [])
        self.assertEqual(list(self.spider.parse_html(self.response(request, blocked_body))), [])


if __name__ == "__main__":
    unittest.main()
