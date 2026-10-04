import json
import re
from pathlib import Path
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.newegg_categories import (
    NEWEGG_CATEGORIES,
    NEWEGG_LISTING_CATEGORIES,
    NEWEGG_SITE_BASE,
    url_kind,
)
from common.spiders.newegg_listing_spider import DEFAULT_IMAGE_SIZE, NeweggListingSpider

CPU_URL = "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343"
CPU_CATEGORY = "components-storage-core-component-cpu-processor-desktop-cpu-processor"


def load_state(name: str) -> dict:
    document = Path(f"sample/{name}").read_text(encoding="utf-8")
    match = re.search(r"window\.__initialState__\s*=\s*", document)
    return json.JSONDecoder().raw_decode(document, document.find("{", match.end()))[0]


class NeweggListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = NeweggListingSpider(category=CPU_CATEGORY, max_pages=2)
        self.page_one = Path("sample/newegg-desktop-cpu-sample.html").read_text(encoding="utf-8")
        self.page_two = Path("sample/newegg-desktop-cpu-page2.html").read_text(encoding="utf-8")

    def response(self, body, url=CPU_URL, page=1):
        request = Request(
            url,
            meta={
                "category": CPU_CATEGORY,
                "department": "Components & Storage",
                "subcategory": (
                    "Components & Storage > Core Component > CPU / Processor > Desktop CPU Processor"
                ),
                "base_url": CPU_URL,
                "page": page,
            },
        )
        return TextResponse(url, request=request, body=body, encoding="utf-8")

    def test_inventory_shape_and_category_selection(self):
        self.assertGreater(len(NEWEGG_CATEGORIES), 1000)
        names = [entry["category"] for entry in NEWEGG_CATEGORIES]
        urls = [entry["url"] for entry in NEWEGG_CATEGORIES]
        self.assertEqual(len(set(names)), len(names))
        self.assertEqual(len(set(urls)), len(urls))
        self.assertTrue(all(url.startswith(NEWEGG_SITE_BASE + "/") for url in urls))
        self.assertTrue(all(re.search(r"/(Store|Category|SubCategory)/ID-\d+$", url) for url in urls))

        selected = NeweggListingSpider(category=CPU_CATEGORY)
        self.assertEqual(selected.resolve_target_url(), CPU_URL)
        self.assertIn(CPU_CATEGORY, selected.available_categories())

    def test_inventory_contains_no_grouping_nodes(self):
        """StoreType=0 nodes carry no listing and must not be crawlable."""
        self.assertTrue(all(entry["url"] for entry in NEWEGG_CATEGORIES))

    def test_listing_categories_are_subcategory_leaves(self):
        """Only SubCategory nodes render products; Store/Category are hubs."""
        self.assertTrue(NEWEGG_LISTING_CATEGORIES)
        self.assertTrue(all(e["kind"] == "SubCategory" for e in NEWEGG_LISTING_CATEGORIES))
        self.assertLess(len(NEWEGG_LISTING_CATEGORIES), len(NEWEGG_CATEGORIES))
        self.assertEqual(url_kind(CPU_URL), "SubCategory")
        self.assertIn("kind", NEWEGG_CATEGORIES[0])

    def test_hub_category_logs_a_diagnostic(self):
        state = load_state("newegg-desktop-cpu-sample.html")
        state["Products"] = []
        body = "<script>window.__initialState__ = " + json.dumps(state) + ";</script>"
        url = "https://www.newegg.com/Laptops/Category/ID-702"
        with self.assertLogs(NeweggListingSpider.name, level="INFO") as logs:
            self.assertEqual(list(self.spider.parse(self.response(body, url=url))), [])
        self.assertTrue(any("navigation hubs" in line for line in logs.output))

    def test_image_size_is_configurable(self):
        small = NeweggListingSpider(category=CPU_CATEGORY, image_size=100)
        large = NeweggListingSpider(category=CPU_CATEGORY, image_size=1280)
        self.assertEqual(small.image_size, 100)
        self.assertEqual(NeweggListingSpider(category=CPU_CATEGORY).image_size, DEFAULT_IMAGE_SIZE)
        body = self.page_one
        urls = {}
        for label, spider in (("small", small), ("large", large)):
            items = [
                entry for entry in spider.parse(self.response(body)) if isinstance(entry, dict)
            ]
            urls[label] = items[0]["image_url"]
        self.assertIn("ProductImageCompressAll100", urls["small"])
        self.assertIn("ProductImageOriginal", urls["large"])
        # Both renditions must be real URLs derived from Newegg's own patterns.
        for url in urls.values():
            self.assertTrue(url.startswith("https://c1.neweggimages.com/"))
            self.assertTrue(url.endswith("/19-113-877-01.png"))

    def test_hydration_mapping_and_pagination_request(self):
        outputs = list(self.spider.parse(self.response(self.page_one)))
        items = [entry for entry in outputs if isinstance(entry, dict)]
        requests = [entry for entry in outputs if not isinstance(entry, dict)]

        self.assertEqual(len(items), 2)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, CPU_URL + "/Page-2")

        first = items[0]
        self.assertEqual(first["item_id"], "19-113-877")
        self.assertEqual(first["department"], "Components & Storage")
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["total_count"], 1181)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["source"], "newegg_initial_state_products")
        self.assertEqual(first["source_url"], CPU_URL)

        self.assertTrue(first["title"].startswith("AMD Ryzen 7 9800X3D"))
        self.assertEqual(first["brand"], "AMD")
        self.assertEqual(first["model"], "100-100001084WOF")
        self.assertEqual(first["price"], 469.0)
        self.assertEqual(first["original_price"], 497.49)
        self.assertTrue(first["on_sale"])
        self.assertAlmostEqual(first["discount_pct"], 5.73, places=2)
        self.assertEqual(first["rating"], 4.8)
        self.assertEqual(first["reviews_count"], 729)
        self.assertTrue(first["in_stock"])
        self.assertEqual(first["ships_from"], "United States")
        self.assertEqual(first["shipping_charge"], 0.01)
        self.assertEqual(first["seller"], "Newegg")
        self.assertIn("Promotion", str(first["promotional_badge"]))
        self.assertEqual(first["group_item_count"], 142)
        self.assertEqual(first["subcategory_name"], "Desktop CPU Processor")

        self.assertEqual(
            first["url"],
            f"{NEWEGG_SITE_BASE}/amd-ryzen-7-9000-series-ryzen-7-9800x3d-granite-ridge-"
            "zen-5-socket-am5-desktop-cpu-processor/p/19-113-877",
        )
        self.assertEqual(
            first["image_url"],
            "https://c1.neweggimages.com/NeweggImage/ProductImageCompressAll200/19-113-877-01.png",
        )

        fields = set(self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertTrue(fields.issuperset(first))
        self.assertEqual(fields, set(items[1]))

    def test_max_pages_2_follows_page_2_without_duplicate_skus(self):
        page_one_items = {
            entry["item_id"]
            for entry in self.spider.parse(self.response(self.page_one))
            if isinstance(entry, dict)
        }
        follow = [
            entry
            for entry in self.spider.parse(self.response(self.page_one))
            if not isinstance(entry, dict)
        ][0]

        outputs = list(self.spider.parse(self.response(self.page_two, url=follow.url, page=2)))
        items = [entry for entry in outputs if isinstance(entry, dict)]
        requests = [entry for entry in outputs if not isinstance(entry, dict)]

        self.assertEqual(len(items), 2)
        self.assertTrue(all(item["page"] == 2 for item in items))
        self.assertTrue(page_one_items.isdisjoint({item["item_id"] for item in items}))
        # total_count implies 33 pages, so max_pages=2 must stop the crawl.
        self.assertEqual(requests, [])

    def test_deduplicates_repeated_sku_within_a_page(self):
        state = load_state("newegg-desktop-cpu-sample.html")
        state["Products"] = [state["Products"][0], state["Products"][0]]
        body = "<script>window.__initialState__ = " + json.dumps(state) + ";</script>"
        items = [
            entry
            for entry in self.spider.parse(self.response(body))
            if isinstance(entry, dict)
        ]
        self.assertEqual(len(items), 1)

    def test_with_page_helper(self):
        with_page = NeweggListingSpider._with_page
        self.assertEqual(with_page(CPU_URL, 1), CPU_URL)
        self.assertEqual(with_page(CPU_URL, 3), CPU_URL + "/Page-3")
        self.assertEqual(with_page(CPU_URL + "/Page-3", 4), CPU_URL + "/Page-4")
        self.assertEqual(with_page(CPU_URL + "/", 2), CPU_URL + "/Page-2")

    def test_zero_item_page_stops_pagination(self):
        state = load_state("newegg-desktop-cpu-sample.html")
        state["Products"] = []
        body = "<script>window.__initialState__ = " + json.dumps(state) + ";</script>"
        self.assertEqual(list(self.spider.parse(self.response(body))), [])

    def test_missing_hydration_state_raises(self):
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.response("<html><body>no state here</body></html>")))
        self.assertIn("__initialState__", str(ctx.exception))

    def test_schema_drift_raises(self):
        body = "<script>window.__initialState__ = {\"Products\": \"nope\"};</script>"
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.response(body)))
        self.assertIn("Products", str(ctx.exception))

    def test_non_200_raises(self):
        response = self.response(self.page_one)
        response.status = 503
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(response))
        self.assertIn("503", str(ctx.exception))

    def test_extraction_ignores_decoy_scripts(self):
        """Balanced decoding must not latch onto unrelated JSON in the document."""
        document = (
            '<script>window.__routing = {"Products": [{"bogus": true}]};</script>'
            '<script>var ld = {"@type":"Product"};</script>' + self.page_one
        )
        items = [
            entry
            for entry in self.spider.parse(self.response(document))
            if isinstance(entry, dict)
        ]
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["item_id"], "19-113-877")

    def test_requires_a_target(self):
        with self.assertRaises(ValueError):
            NeweggListingSpider()


if __name__ == "__main__":
    unittest.main()
