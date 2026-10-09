from pathlib import Path
import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.containerstore_categories import CONTAINERSTORE_CATEGORIES
from common.spiders.containerstore_listing_spider import ContainerStoreListingSpider

PAGE1_URL = "https://www.containerstore.com/s/kitchen/pantry-organizers/12"


def hydrate(page_props: dict) -> str:
    """Wrap a pageProps object back into the `__NEXT_DATA__` script the spider reads."""
    payload = {"props": {"pageProps": page_props}}
    return (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(payload)
        + "</script></body></html>"
    )


def page_props(path: str) -> dict:
    document = Path(path).read_text(encoding="utf-8")
    marker = '<script id="__NEXT_DATA__" type="application/json">'
    start = document.index(marker) + len(marker)
    return json.JSONDecoder().raw_decode(document, start)[0]["props"]["pageProps"]


def load(path: str) -> dict:
    return page_props(path)


class ContainerStoreListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = ContainerStoreListingSpider(category="Kitchen > Pantry Organizers", max_pages=2)
        self.page1 = load("sample/containerstore-listing-page1.html")
        self.page2 = load("sample/containerstore-listing-page2.html")

    def response(self, body=None, url=PAGE1_URL, page=1, meta=None):
        request_meta = {
            "category": "Kitchen > Pantry Organizers",
            "department": "Kitchen",
            "subcategory": "Pantry Organizers",
            "leaf": None,
            "page": page,
            "proxy": "http://proxy.invalid:8080",
        }
        request_meta.update(meta or {})
        return TextResponse(url, request=Request(url, meta=request_meta), body=body, encoding="utf-8")

    # ---------------------------------------------------------------- taxonomy

    def test_inventory_is_unique_and_crawlable(self):
        self.assertEqual(len(_FLAT(CONTAINERSTORE_CATEGORIES)), 295)
        self.assertEqual(len({e["category"] for e in _FLAT(CONTAINERSTORE_CATEGORIES)}), 295)
        self.assertEqual(len({e["url"] for e in _FLAT(CONTAINERSTORE_CATEGORIES)}), 295)
        self.assertTrue(all(e["url"].startswith("https://www.containerstore.com/s/") for e in _FLAT(CONTAINERSTORE_CATEGORIES)))
        # 14 department + 189 L2 + 159 L3 = 362 hydrated nodes, 295 unique catalogue URLs.
        self.assertEqual(len({e["department"] for e in _FLAT(CONTAINERSTORE_CATEGORIES)}), 14)

    def test_category_lookup_returns_the_hydrated_url(self):
        self.assertEqual(
            ContainerStoreListingSpider(category="Kitchen > Pantry Organizers").resolve_target_url(),
            PAGE1_URL,
        )
        self.assertEqual(
            ContainerStoreListingSpider(category="Storage > Plastic Bins & Baskets").resolve_target_url(),
            "https://www.containerstore.com/s/storage/plastic-bins-baskets/12",
        )

    def test_missing_category_arg_raises_with_available_names(self):
        with self.assertRaisesRegex(ValueError, "Available categories"):
            ContainerStoreListingSpider()

    # ---------------------------------------------------------------- parsing

    def test_feed_contract_and_item_mapping(self):
        items = [out for out in self.spider.parse(self.response(body=hydrate(self.page1))) if isinstance(out, dict)]
        self.assertEqual(len(items), 8)
        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["department"], "Kitchen")
        self.assertEqual(item["subcategory"], "Pantry Organizers")
        self.assertEqual(item["leaf"], None)
        self.assertTrue(item["url"].startswith("https://www.containerstore.com/"))
        self.assertTrue(item["image_url"].startswith("https://images.containerstore.com/"))
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], 325)
        self.assertEqual(item["last_page"], 6)
        self.assertEqual(item["source"], "containerstore_next_data_products_entities")
        self.assertIsInstance(item["raw"], dict)
        self.assertTrue(item["title"])
        self.assertTrue(item["item_id"])
        self.assertIsNotNone(item["price"])

    def test_page_two_uses_its_own_page_no_and_never_page_one(self):
        body = hydrate(self.page2)
        items = [out for out in self.spider.parse(self.response(body=body, page=2)) if isinstance(out, dict)]
        self.assertTrue(items)
        self.assertEqual({item["page"] for item in items}, {2})
        # the hydrated grid for page 2 is disjoint from page 1
        page1_ids = {
            e["id"]
            for e in self.page1["initialState"]["products"]["entities"].values()
        }
        self.assertFalse({int(item["item_id"]) for item in items} & page1_ids)

    def test_breadcrumbs_fill_taxonomy_when_driven_by_url(self):
        response = self.response(
            body=hydrate(self.page1),
            url="https://www.containerstore.com/s/other/thing/12",
            meta={"category": "custom", "department": None, "subcategory": None, "leaf": None},
        )
        items = [out for out in self.spider.parse(response) if isinstance(out, dict)]
        crumbs = self.page1["initialState"]["plp"]["data"]["breadcrumbs"]
        # the fixture sits two levels deep (a `/12` subcategory): dept + subcategory, no leaf
        self.assertEqual(len(crumbs), 2)
        self.assertEqual(items[0]["department"], crumbs[0]["name"])
        self.assertEqual(items[0]["subcategory"], crumbs[1]["name"])
        self.assertIsNone(items[0]["leaf"])

    def test_prismic_template_is_parsed_despite_its_page_type(self):
        # `pageType` is not a usable signal: this fixture hydrates as PrismicTemplate
        # yet carries a full product grid.
        self.assertEqual(self.page1["pageType"], "PrismicTemplate")
        items = [out for out in self.spider.parse(self.response(body=hydrate(self.page1))) if isinstance(out, dict)]
        self.assertTrue(items)

    # ---------------------------------------------------------------- pricing

    def test_discount_mapping(self):
        items = [out for out in self.spider.parse(self.response(body=hydrate(self.page1))) if isinstance(out, dict)]
        for item in items:
            if item["original_price"]:
                self.assertGreater(item["original_price"], item["price"])
                self.assertAlmostEqual(
                    item["discount_percentage"],
                    round((item["original_price"] - item["price"]) / item["original_price"] * 100, 2),
                    places=2,
                )
            else:
                self.assertIsNone(item["discount_percentage"])

    def test_zero_saving_sale_falls_back_to_the_retail_price(self):
        # `isOnSale` is frequently true while minSalePrice == minRetailPrice; that must not
        # produce a bogus original_price / discount_percentage pair.
        props = json.loads(json.dumps(self.page1))
        entity_id = next(iter(props["initialState"]["products"]["entities"]))
        entity = props["initialState"]["products"]["entities"][entity_id]
        entity["price"] = {"minSalePrice": 10.0, "minRetailPrice": 10.0, "isOnSale": True}
        items = [out for out in self.spider.parse(self.response(body=hydrate(props))) if isinstance(out, dict)]
        self.assertEqual(items[0]["price"], 10.0)
        self.assertIsNone(items[0]["original_price"])
        self.assertIsNone(items[0]["discount_percentage"])

    def test_non_numeric_and_missing_prices_are_none(self):
        props = json.loads(json.dumps(self.page1))
        entity_id = next(iter(props["initialState"]["products"]["entities"]))
        props["initialState"]["products"]["entities"][entity_id]["price"] = {"minSalePrice": "n/a"}
        items = [out for out in self.spider.parse(self.response(body=hydrate(props))) if isinstance(out, dict)]
        self.assertIsNone(items[0]["price"])

    # ---------------------------------------------------------------- variants

    def test_color_variant_options(self):
        props = json.loads(json.dumps(self.page1))
        entities = props["initialState"]["products"]["entities"]
        entity_id = next(iter(entities))
        entities[entity_id]["colorSwatcheInfo"] = {
            "variant": "COLOR",
            "values": [{"value": "Peacock", "swatchValue": "#22c8d1"}, {"value": "Aqua"}],
        }
        items = [out for out in self.spider.parse(self.response(body=hydrate(props))) if isinstance(out, dict)]
        self.assertEqual(items[0]["color_option_count"], 2)
        self.assertEqual(items[0]["color_options"], "Peacock, Aqua")

    def test_badges_and_flags(self):
        items = [out for out in self.spider.parse(self.response(body=hydrate(self.page1))) if isinstance(out, dict)]
        self.assertTrue(all(isinstance(item["on_sale"], bool) for item in items))
        self.assertTrue(all(isinstance(item["out_of_stock"], bool) for item in items))
        self.assertTrue(any(item["badge"] for item in items))

    # ---------------------------------------------------------------- pagination

    def test_next_page_follows_the_hydrated_url(self):
        outputs = list(self.spider.parse(self.response(body=hydrate(self.page1))))
        follow = [out for out in outputs if not isinstance(out, dict)]
        self.assertEqual(len(follow), 1)
        self.assertEqual(
            follow[0].url, "https://www.containerstore.com/s/kitchen/pantry-organizers/12?p=60&ps=60"
        )
        self.assertEqual(follow[0].callback, self.spider.parse)
        self.assertEqual(follow[0].meta["page"], 2)

    def test_max_pages_one_stops_pagination(self):
        spider = ContainerStoreListingSpider(category="Kitchen > Pantry Organizers", max_pages=1)
        outputs = list(spider.parse(self.response(body=hydrate(self.page1))))
        self.assertEqual([out for out in outputs if not isinstance(out, dict)], [])

    def test_last_page_stops_pagination(self):
        props = json.loads(json.dumps(self.page1))
        props["initialState"]["plp"]["data"]["currentPage"] = 6
        props["initialState"]["plp"]["data"]["lastPage"] = 6
        props["initialState"]["plp"]["entities"] = {"6": props["initialState"]["plp"]["entities"]["1"]}
        spider = ContainerStoreListingSpider(category="Kitchen > Pantry Organizers", max_pages=10)
        outputs = list(spider.parse(self.response(body=hydrate(props), page=6)))
        self.assertTrue([out for out in outputs if isinstance(out, dict)])
        self.assertEqual([out for out in outputs if not isinstance(out, dict)], [])

    def test_missing_next_url_falls_back_to_the_paging_contract(self):
        props = json.loads(json.dumps(self.page1))
        props["initialState"]["plp"]["data"]["nextPageUrl"] = ""
        props["initialState"]["plp"]["data"]["pageSize"] = 60
        outputs = list(self.spider.parse(self.response(body=hydrate(props))))
        follow = [out for out in outputs if not isinstance(out, dict)]
        self.assertEqual(len(follow), 1)
        self.assertIn("p=60&ps=60", follow[0].url)

    # ---------------------------------------------------------------- landings

    def test_department_landing_page_is_logged_not_scraped(self):
        body = Path("sample/containerstore-department-landing.html").read_text(encoding="utf-8")
        with self.assertLogs("containerstore_listing", level="INFO") as logs:
            outputs = list(self.spider.parse(self.response(body=body, url="https://www.containerstore.com/s/kitchen/1")))
        self.assertEqual(outputs, [])
        self.assertTrue(any("No product grid" in line for line in logs.output))
        self.assertTrue(any("subcategory tile" in line for line in logs.output))

    def test_category_landing_without_plp_entities_is_logged(self):
        body = Path("sample/containerstore-category-landing.html").read_text(encoding="utf-8")
        with self.assertLogs("containerstore_listing", level="INFO") as logs:
            outputs = list(self.spider.parse(self.response(body=body, url="https://www.containerstore.com/s/all-products")))
        self.assertEqual(outputs, [])
        self.assertTrue(any("No product grid" in line for line in logs.output))

    def test_empty_page_two_stops_quietly(self):
        props = json.loads(json.dumps(self.page1))
        props["initialState"]["plp"]["data"]["currentPage"] = 2
        props["initialState"]["plp"]["entities"] = {"2": {"pageNo": 2, "products": []}}
        with self.assertLogs("containerstore_listing", level="INFO") as logs:
            outputs = list(self.spider.parse(self.response(body=hydrate(props), page=2)))
        self.assertEqual(outputs, [])
        self.assertTrue(any("empty product grid" in line for line in logs.output))

    # ---------------------------------------------------------------- robustness

    def test_missing_hydration_blob_raises(self):
        with self.assertRaisesRegex(RuntimeError, "No containerstore __NEXT_DATA__"):
            list(self.spider.parse(self.response(body="<html><body>nope</body></html>")))

    def test_malformed_hydration_json_raises(self):
        with self.assertRaisesRegex(RuntimeError, "no props.pageProps"):
            list(self.spider.parse(self.response(body='<script id="__NEXT_DATA__" type="application/json">{oops</script>')))

    def test_missing_page_props_raises(self):
        with self.assertRaisesRegex(RuntimeError, "no props.pageProps"):
            list(self.spider.parse(self.response(body='<script id="__NEXT_DATA__" type="application/json">{"props":{}}</script>')))

    def test_missing_initial_state_raises(self):
        with self.assertRaisesRegex(RuntimeError, "no props.pageProps.initialState"):
            list(self.spider.parse(self.response(body=hydrate({"pageType": "PLP"}))))

    def test_missing_plp_state_raises(self):
        with self.assertRaisesRegex(RuntimeError, "no plp state"):
            list(self.spider.parse(self.response(body=hydrate({"pageType": "PLP", "initialState": {}}))))

    def test_product_id_without_an_entity_is_skipped(self):
        props = json.loads(json.dumps(self.page1))
        entities = props["initialState"]["products"]["entities"]
        grid = props["initialState"]["plp"]["entities"]["1"]["products"]
        orphaned = grid[0]
        del entities[str(orphaned)]
        with self.assertLogs("containerstore_listing", level="WARNING") as logs:
            items = [out for out in self.spider.parse(self.response(body=hydrate(props))) if isinstance(out, dict)]
        self.assertEqual(len(items), len(grid) - 1)
        self.assertTrue(any("no matching products.entities record" in line for line in logs.output))

    def test_duplicate_products_across_pages_are_emitted_once(self):
        props = json.loads(json.dumps(self.page1))
        props["initialState"]["plp"]["data"]["currentPage"] = 2
        # page 2 reuses page 1's grid verbatim
        props["initialState"]["plp"]["entities"] = {"2": props["initialState"]["plp"]["entities"]["1"]}
        first = [out for out in self.spider.parse(self.response(body=hydrate(self.page1))) if isinstance(out, dict)]
        second = [out for out in self.spider.parse(self.response(body=hydrate(props), page=2)) if isinstance(out, dict)]
        self.assertEqual(second, [])
        self.assertEqual(len(first), 8)

    def test_non_200_raises(self):
        response = self.response(body="")
        response.status = 503
        with self.assertRaisesRegex(RuntimeError, "HTTP 503"):
            list(self.spider.parse(response))

    def test_start_requests_carry_taxonomy_meta(self):
        request = next(iter(self.spider.start_requests()))
        self.assertEqual(request.url, PAGE1_URL)
        self.assertEqual(request.meta["category"], "Kitchen > Pantry Organizers")
        self.assertEqual(request.meta["department"], "Kitchen")
        self.assertEqual(request.meta["page"], 1)


if __name__ == "__main__":
    unittest.main()


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]
