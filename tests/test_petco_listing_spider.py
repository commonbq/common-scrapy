import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.petco_categories import PETCO_CATEGORIES, PETCO_CATEGORY_INVENTORY
from common.spiders.petco_listing_spider import PetcoListingSpider

LISTING_URL = "https://www.petco.com/shop/en/petcostore/category/cat/cat-food/dry-cat-food"


def _node_counts(node):
    children = node.get("subcategories", {})
    return 1 + sum(_node_counts(child) for child in children.values())


class PetcoListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = PetcoListingSpider(category="cat-cat-food-dry-cat-food", max_pages=2)
        self.sample = Path("sample/petco-listing-dry-cat-food.html").read_text(encoding="utf-8")

    def response(self, body=None, *, url=LISTING_URL, page=1):
        return TextResponse(
            url,
            request=Request(url, meta={"page": page, "category": "cat-cat-food-dry-cat-food"}),
            body=body or self.sample,
            encoding="utf-8",
        )

    def page_two(self, *, total=433, page=2, item_id="9990001"):
        payload = {
            "props": {
                "pageProps": {
                    "pageData": {
                        "categoryId": "10195",
                        "h1title": "Dry Cat Food & Kibble",
                        "breadcrumbs": [{"label": "Cat Food", "value": "10027"}],
                        "constructorResults": {
                            "response": {
                                "results": [
                                    {
                                        "data": {
                                            "catEntryID": item_id,
                                            "itemname": "Page two product",
                                            "mfName": "Purina",
                                            "rdprice": 10.5,
                                            "listprice": 12.0,
                                            "url": f"/product/page-two-{item_id}",
                                            "PTC_OMNI_BOPUS_FLAG": "Yes",
                                        },
                                        "value": "Page two product, 3 lbs.",
                                        "variations": [],
                                    }
                                ],
                                "total_num_results": total,
                            },
                            "request": {"page": page, "num_results_per_page": 48},
                        },
                    }
                }
            }
        }
        body = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'
        return self.response(body, url=f"{LISTING_URL}?page={page}", page=page)

    def test_inventory_and_category_selection(self):
        self.assertEqual(len(PETCO_CATEGORY_INVENTORY), 22)
        self.assertEqual(
            sum(_node_counts(group) for group in PETCO_CATEGORY_INVENTORY.values()), 286
        )
        self.assertEqual(len(PETCO_CATEGORIES), 264)
        self.assertEqual(len({entry["url"] for entry in PETCO_CATEGORIES}), 264)
        selected = next(
            entry for entry in PETCO_CATEGORIES
            if entry["category"] == "cat-cat-food-dry-cat-food"
        )
        self.assertEqual(selected["url"], LISTING_URL)
        self.assertEqual(selected["department"], "Cat")
        self.assertEqual(self.spider.resolve_target_url(), LISTING_URL)

    def test_requires_a_target(self):
        with self.assertRaises(ValueError):
            PetcoListingSpider()

    def test_hydration_yields_items_and_feed_contract(self):
        outputs = list(self.spider.parse(self.response()))
        items = outputs[:-1]
        self.assertEqual(len(items), 3)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        first = items[0]
        self.assertEqual(first["category"], "cat-cat-food-dry-cat-food")
        self.assertEqual(first["category_id"], "10195")
        self.assertEqual(first["category_name"], "Dry Cat Food & Kibble")
        self.assertEqual(first["breadcrumb_path"], "Cat Supplies > Cat Food > Dry Cat Food & Kibble")
        self.assertEqual(first["item_id"], "6848523")
        self.assertEqual(
            first["url"],
            "https://www.petco.com/product/purina-cat-chow-indoor-hairball-healthy-weight-dry-cat-food-15-lbs-3880710",
        )
        self.assertEqual(first["brand"], "Purina Cat Chow")
        self.assertEqual(first["price"], 18.99)
        self.assertEqual(first["original_price"], 19.99)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["rating"], 4.8141)
        self.assertEqual(first["reviews_count"], 3770)
        self.assertTrue(first["in_stock"])
        self.assertEqual(first["variants_count"], 2)
        self.assertEqual(first["variant_ids"], ["3880710", "3880672"])
        self.assertEqual(first["facets"]["Primary Brand"], ["Purina Cat Chow"])
        self.assertEqual(first["total_count"], 433)
        self.assertEqual(first["items_per_page"], 48)
        self.assertEqual(first["search_engine"], "constructor.io")
        self.assertEqual(first["source"], "petco_next_data")
        self.assertEqual(first["raw"]["data"]["catEntryID"], "6848523")
        self.assertEqual([item["position"] for item in items], [1, 2, 3])

    def test_pagination_follows_page_query_and_stops_at_max_pages(self):
        first = list(self.spider.parse(self.response()))[-1]
        self.assertEqual(first.url, f"{LISTING_URL}?page=2")
        self.assertEqual(first.meta["page"], 2)
        second = list(self.spider.parse(self.page_two()))
        self.assertEqual(len(second), 1)
        self.assertEqual(second[0]["page"], 2)
        self.assertEqual(second[0]["item_id"], "9990001")
        self.assertTrue(second[0]["bopus_available"])
        self.assertEqual(second[0]["breadcrumb_path"], "Cat Food")

    def test_pagination_stops_when_last_page_is_reached(self):
        spider = PetcoListingSpider(category="cat-cat-food-dry-cat-food", max_pages=5)
        outputs = list(spider.parse(self.page_two(total=96)))
        self.assertEqual(len(outputs), 1)
        outputs = list(spider.parse(self.page_two(total=433)))
        self.assertEqual(outputs[-1].url, f"{LISTING_URL}?page=3")

    def test_duplicate_rows_are_dropped_within_a_run(self):
        outputs = list(self.spider.parse(self.response()))
        first_ids = [item["item_id"] for item in outputs[:-1]]
        self.assertEqual(sorted(self.spider._seen_products), sorted(first_ids))
        repeated = list(self.spider.parse(self.page_two(item_id=first_ids[0])))
        self.assertEqual(repeated, [])

    def test_missing_hydration_raises(self):
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(self.response("<html><body>no state</body></html>")))
        empty = self.response(
            '<script id="__NEXT_DATA__" type="application/json">{"props":{}}</script>'
        )
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(empty))
        no_results = self.response(
            '<script id="__NEXT_DATA__" type="application/json">'
            '{"props":{"pageProps":{"pageData":{"constructorResults":{"response":{"results":[]}}}}}}</script>'
        )
        with self.assertRaises(RuntimeError):
            list(self.spider.parse(no_results))
