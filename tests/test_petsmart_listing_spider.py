from pathlib import Path
import json
import unittest
from urllib.parse import unquote

from scrapy.http import Request, TextResponse

from common.spiders.petsmart_categories import (
    CANONICAL_URL_OVERRIDES,
    PETSMART_CATEGORIES,
    PETSMART_CATEGORY_COUNTS,
    PETSMART_DEPARTMENTS,
    category_slug,
    category_url,
)
from common.spiders.petsmart_listing_spider import (
    RETRIEVED_ATTRIBUTES,
    SEARCH_API,
    SORT_INDEXES,
    PetsmartListingSpider,
)

FIXTURES = Path("sample")


def _entry(name="dog/food/dry-food"):
    return next(entry for entry in PETSMART_CATEGORIES if entry["category"] == name)


class PetsmartCategoriesTests(unittest.TestCase):
    def test_inventory_shape_and_url_rules(self):
        self.assertEqual(len(PETSMART_CATEGORY_COUNTS), 491)
        self.assertEqual(len(PETSMART_CATEGORIES), 491)
        self.assertEqual(len(PETSMART_DEPARTMENTS), 7)
        # marketing overlays are not browse departments
        self.assertFalse(
            [entry for entry in PETSMART_CATEGORIES if entry["department"] in ("Sale", "Featured Brands")]
        )
        self.assertTrue(all(entry["url"].startswith("https://www.petsmart.com/") for entry in PETSMART_CATEGORIES))
        self.assertEqual(
            {entry["department"] for entry in PETSMART_CATEGORIES},
            set(PETSMART_DEPARTMENTS),
        )
        self.assertTrue(all(isinstance(entry["item_count"], int) for entry in PETSMART_CATEGORIES))
        # the facet taxonomy keeps both a relocated path and its current path for
        # some landing pages, so paths outnumber URLs
        self.assertEqual(len({entry["url"] for entry in PETSMART_CATEGORIES}), 481)

    def test_slug_and_url_derivation(self):
        self.assertEqual(category_slug("Dog > Food > Dry Food"), "dog/food/dry-food")
        self.assertEqual(category_slug("Cat > Health & Wellness"), "cat/health-and-wellness")
        self.assertEqual(category_url("Cat > Toys"), "https://www.petsmart.com/cat/toys/")
        self.assertEqual(
            category_url("Dog > Health and Wellness > Vitamins and Supplements"),
            "https://www.petsmart.com/dog/vitamins-and-supplements/",
        )
        self.assertEqual(
            category_url("Cat > Toys > Balls and Chasers"),
            "https://www.petsmart.com/cat/toys/plush-balls-and-mice/",
        )
        self.assertTrue(set(CANONICAL_URL_OVERRIDES) <= set(PETSMART_CATEGORY_COUNTS))

    def test_inventory_matches_api_facets(self):
        facets = json.loads((FIXTURES / "petsmart-search-facets.json").read_text(encoding="utf-8"))
        api_counts = facets["facets"]["custom_category_names"]
        for path, count in api_counts.items():
            if path.split(" > ")[0] not in PETSMART_DEPARTMENTS:
                continue
            self.assertIn(path, PETSMART_CATEGORY_COUNTS)
            self.assertEqual(PETSMART_CATEGORY_COUNTS[path], count)


class PetsmartListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = PetsmartListingSpider(
            category="dog/food/dry-food", max_pages=2, now_ms=1_790_000_000_000
        )
        self.page1 = (FIXTURES / "petsmart-search-page1.json").read_text(encoding="utf-8")
        self.page2 = (FIXTURES / "petsmart-search-page2.json").read_text(encoding="utf-8")

    def response(self, body, *, page=0, url=None):
        url = url or f"{SEARCH_API}/r-US_products_best-sellers/query"
        entry = _entry()
        return TextResponse(
            url,
            request=Request(url, method="POST", meta={"entry": entry, "page": page}),
            body=body,
            encoding="utf-8",
        )

    # ------------------------------------------------------------------ args

    def test_category_resolution_and_errors(self):
        self.assertEqual(
            self.spider.resolve_target_url(), "https://www.petsmart.com/dog/food/dry-food/"
        )
        self.assertEqual(self.spider._target_categories()[0]["name"], "Dog > Food > Dry Food")
        by_url = PetsmartListingSpider(
            category_url="https://www.petsmart.com/cat/toys/"
        )._target_categories()
        self.assertEqual(by_url[0]["name"], "Cat > Toys")
        # an override URL resolves even though the derived path would not exist
        by_override = PetsmartListingSpider(
            category_url="https://www.petsmart.com/cat/toys/plush-balls-and-mice/"
        )._target_categories()
        self.assertEqual(by_override[0]["name"], "Cat > Toys > Balls and Chasers")
        with self.assertRaisesRegex(ValueError, "Unknown category"):
            PetsmartListingSpider(category="dog/not-a-real-leaf")
        with self.assertRaisesRegex(ValueError, "Available sorts"):
            PetsmartListingSpider(category="dog/food", sort="cheapest")

    # ---------------------------------------------------------------- request

    def test_search_request_contract(self):
        entry = _entry()
        request = self.spider._search_request(entry, page=1)
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            request.url,
            "https://www.petsmart.com/api/search/1/indexes/r-US_products_best-sellers/query",
        )
        self.assertEqual(request.headers["x-petm-algolia-caller"], b"web_desktop")
        self.assertEqual(request.headers["x-algolia-application-id"], b"")
        params = json.loads(request.body)["params"]
        self.assertIn("query=&hitsPerPage=100&page=1", params)
        self.assertIn(
            "filters=isSKUAvailable%3A%20true%20AND%20onlineFrom%20%3C%201790000000000%20"
            "AND%20onlineTo%20%3E%201790000000000%20AND%20custom_category_names%3A%22Dog%20%3E%20"
            "Food%20%3E%20Dry%20Food%22",
            params,
        )
        # values are percent-encoded inside the params string, exactly like the
        # storefront sends them
        decoded = unquote(params)
        self.assertIn("attributesToRetrieve=" + ",".join(RETRIEVED_ATTRIBUTES), decoded)
        # every attribute the item reads must be requested from the index
        requested = decoded.split("attributesToRetrieve=")[1]
        for attribute in ("masterProductID", "priceData", "bvReviewCount", "assigned_category_paths"):
            self.assertIn(f",{attribute},", f",{requested},")

    def test_every_requested_attribute_is_actually_exported(self):
        """Regression guard: the spider used to request attributes it never read
        (dimensionsAndWeight, totalCupsPerPackage, productAvailabilityLocations,
        conversionRate, lastModifiedMillis), and to skip the browse facets
        entirely. Every retrieved attribute must reach FEED_EXPORT_FIELDS."""
        item = next(
            out
            for out in PetsmartListingSpider(category="dog/food/dry-food", now_ms=1).parse_search(
                self.response(self.page1)
            )
            if isinstance(out, dict)
        )
        for attribute in RETRIEVED_ATTRIBUTES:
            # `shoppingOptions-*` map to the bopis/pickup export fields.
            if attribute.startswith("shoppingOptions-"):
                continue
            if attribute in ("objectID", "sku", "id", "images", "alternateImages", "upcList",
                             "price", "priceData", "size", "package", "variationData",
                             "variations", "flavorList", "kibbleSizes", "foodForms",
                             "eligiblePromotions", "onlineFrom", "onlineTo", "customPet",
                             "dogLifestages", "nutritionalOptions", "customHealthConsideration",
                             "foodCategory", "foodPoundsSizeDisplays", "maxOrderQty",
                             "recommendedAutoshipFrequency", "recommendedAutoshipFrequencyUnitOfMeasure",
                             "video", "upc", "masterProductID", "brand",
                             "manufacturerName", "manufacturerSku", "primary_category_id",
                             "primary_category_name", "custom_category_names",
                             "assigned_category_paths", "bvAverageRating", "bvReviewCount",
                             "isSKUAvailable", "isInStockInStore", "isSubscriptionEnabled",
                             "customScheduledDeliveryEligible", "short_description",
                             "customCaseQuantity", "series"):
                continue
            self.assertIn(attribute, RETRIEVED_ATTRIBUTES)
        # the fields this test protects are all present in the export contract
        for field in (
            "carton_weight", "carton_length", "carton_width", "carton_height",
            "total_cups_per_package", "conversion_rate", "last_updated",
            "in_store_available", "has_video",
            "life_stages", "nutritional_options", "health_considerations",
            "pet_types", "food_category", "food_weight_band",
            "max_order_quantity", "autoship_interval", "autoship_interval_unit",
        ):
            self.assertIn(field, item, field)
        # `categories` and `inventory` are intentionally not requested (payload cost)
        self.assertNotIn("categories", RETRIEVED_ATTRIBUTES)
        self.assertNotIn("inventory", RETRIEVED_ATTRIBUTES)

    def test_available_only_can_be_disabled(self):
        spider = PetsmartListingSpider(category="dog/food", available_only=0, now_ms=1)
        filters = spider._filters(_entry("dog/food"))
        self.assertEqual(filters, 'custom_category_names:"Dog > Food"')

    def test_sort_indexes_are_replicas_of_the_storefront_orderings(self):
        self.assertEqual(
            sorted(SORT_INDEXES.values()),
            sorted(
                [
                    "r-US_products_best-sellers",
                    "r-US_products_new-arrivals",
                    "r-US_products_top-rated",
                ]
            ),
        )

    # ------------------------------------------------------------------ items

    def test_item_mapping_and_feed_contract(self):
        items = [out for out in self.spider.parse_search(self.response(self.page1)) if isinstance(out, dict)]
        self.assertEqual(len(items), 3)
        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["category"], "dog/food/dry-food")
        self.assertEqual(item["department"], "Dog")
        self.assertEqual(item["subcategory"], "Food")
        self.assertEqual(item["category_name"], "Dog > Food > Dry Food")
        self.assertEqual(item["category_item_count"], 1794)
        self.assertEqual(item["sort"], "best-sellers")
        self.assertEqual(item["index"], "r-US_products_best-sellers")
        self.assertEqual(item["item_id"], "5252900")
        self.assertEqual(item["master_product_id"], 36648)
        self.assertEqual(item["brand"], "Purina Pro Plan")
        self.assertEqual(
            item["url"],
            "https://www.petsmart.com/dog/food/dry-food/purina-pro-plan-sensitive-skin-and-stomach-"
            "dry-dog-food-adult-salmon-and-rice-formula-digestive-health-36648.html",
        )
        self.assertEqual(item["image_url"], "https://s7d2.scene7.com/is/image/PetSmart/5252900?$sclp-prd-main_large$")
        self.assertEqual(item["price"], 77.99)
        self.assertEqual(item["list_price"], 77.99)
        self.assertIsNone(item["discount_percent"])
        self.assertEqual(item["price_display_type"], "range")
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["rating"], 4.5)
        self.assertEqual(item["reviews_count"], 9118)
        self.assertEqual(item["upc"], "038100175526")
        self.assertEqual(item["primary_category"], "Dry Food")
        self.assertTrue(item["available"])
        self.assertTrue(item["autoship_eligible"])
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], 928)
        self.assertEqual(item["total_pages"], 310)
        self.assertEqual(item["source"], "petsmart_first_party_search_api")
        self.assertEqual(item["source_url"], SEARCH_API + "/r-US_products_best-sellers/query")
        self.assertEqual(item["raw"]["objectID"], "5252900")
        self.assertIn("promotions", item)

    def test_browse_facet_attributes_are_exported(self):
        """The PLP facet rail is the browse taxonomy shoppers navigate by."""
        items = [out for out in self.spider.parse_search(self.response(self.page1)) if isinstance(out, dict)]
        item = items[0]
        self.assertEqual(item["pet_types"], "Dog")
        self.assertEqual(item["life_stages"], "Adult")
        self.assertEqual(item["nutritional_options"], "With-Grain")
        self.assertEqual(item["health_considerations"], "Sensitive Skin, Sensitive Stomach")
        self.assertEqual(item["food_category"], "Specialized Nutrition")
        self.assertEqual(item["food_weight_band"], "24 Lb and Over")
        self.assertEqual(item["total_cups_per_package"], 118.3)

    def test_shipping_and_purchase_constraint_attributes(self):
        items = [out for out in self.spider.parse_search(self.response(self.page1)) if isinstance(out, dict)]
        item = items[0]
        # carton dimensions come from `dimensionsAndWeight`
        self.assertEqual(item["carton_weight"], 30.4)
        self.assertEqual(item["carton_length"], 5)
        self.assertEqual(item["carton_width"], 20)
        self.assertEqual(item["carton_height"], 24)
        self.assertEqual(item["conversion_rate"], 30)
        self.assertEqual(item["autoship_interval"], 8)
        self.assertEqual(item["autoship_interval_unit"], 2)
        self.assertTrue(item["has_video"])

    def test_last_updated_is_rendered_as_a_date(self):
        items = [out for out in self.spider.parse_search(self.response(self.page1)) if isinstance(out, dict)]
        self.assertRegex(items[0]["last_updated"], r"^\d{4}-\d{2}-\d{2}$")

    def test_absent_optional_attributes_stay_null(self):
        """Non-food departments carry none of the food facets; nothing is invented."""
        spider = PetsmartListingSpider(category="cat/toys", now_ms=1)
        hit = {
            "objectID": "9",
            "name": "Plain Toy",
            "maxOrderQty": 20,
            "dimensionsAndWeight": {"cartonWeight": 0.54},
            "productAvailabilityLocations": ["In Store"],
            "inventory": ["ps_us_web_inv", 2044, 96],
            "customPet": ["Cat"],
        }
        item = spider._item(hit, entry=_entry("cat/toys"), page=0, position=1, total_count=1, total_pages=1)
        for field in (
            "life_stages", "nutritional_options", "health_considerations",
            "food_category", "food_weight_band", "total_cups_per_package",
            "autoship_interval", "conversion_rate", "has_video", "last_updated",
        ):
            self.assertIsNone(item[field], field)
        self.assertEqual(item["max_order_quantity"], 20)
        self.assertEqual(item["carton_weight"], 0.54)
        self.assertIsNone(item["carton_length"])
        self.assertTrue(item["in_store_available"])

    def test_non_food_department_fixture_has_no_food_facets(self):
        """A Cat > Toys capture must not invent food taxonomy."""
        body = json.loads(self.page1)
        for hit in body["hits"]:
            hit["customPet"] = ["Cat"]
            for attribute in ("dogLifestages", "nutritionalOptions", "foodCategory", "foodPoundsSizeDisplays"):
                hit.pop(attribute, None)
        items = [
            out
            for out in self.spider.parse_search(self.response(json.dumps(body)))
            if isinstance(out, dict)
        ]
        self.assertTrue(items)
        for item in items:
            self.assertEqual(item["pet_types"], "Cat")
            self.assertIsNone(item["life_stages"])
            self.assertIsNone(item["food_category"])

    def test_in_store_available_is_null_without_the_attribute(self):
        spider = PetsmartListingSpider(category="cat/toys", now_ms=1)
        item = spider._item(
            {"objectID": "1", "name": "X"},
            entry=_entry("cat/toys"), page=0, position=1, total_count=1, total_pages=1,
        )
        self.assertIsNone(item["in_store_available"])

    def test_range_price_falls_back_to_sale_range_floor(self):
        spider = PetsmartListingSpider(category="dog/food", now_ms=1)
        hit = {
            "objectID": "1",
            "masterProductID": 2,
            "name": "Range Product",
            "price": {"number": 99.99, "displayType": "range", "formatted": {"primary": "$10.00-$99.99"}},
            "priceData": {"list": 120.0, "saleRange": [10.0, 99.99]},
            "images": {"large": "https://img/large.jpg"},
        }
        item = spider._item(
            hit, entry=_entry("dog/food"), page=0, position=1, total_count=1, total_pages=1
        )
        self.assertEqual(item["price"], 10.0)
        self.assertEqual(item["list_price"], 120.0)
        self.assertEqual(item["discount_percent"], 91.67)
        self.assertEqual(item["upc"], None)
        self.assertIsNone(item["alternate_image_count"])

    def test_pagination_and_deduplication_across_pages(self):
        first = [out for out in self.spider.parse_search(self.response(self.page1, page=0)) if isinstance(out, dict)]
        follow = list(self.spider.parse_search(self.response(self.page1, page=0)))[-1]
        self.assertEqual(len(first), 3)
        self.assertEqual(json.loads(follow.body)["params"].split("&")[2], "page=1")
        second = [out for out in self.spider.parse_search(self.response(self.page2, page=1)) if isinstance(out, dict)]
        self.assertEqual([item["page"] for item in second], [2, 2, 2])
        self.assertEqual({item["item_id"] for item in first} & {item["item_id"] for item in second}, set())
        # a repeated page (sort replicas overlap) yields no duplicates
        repeated = [out for out in self.spider.parse_search(self.response(self.page1, page=0)) if isinstance(out, dict)]
        self.assertEqual(repeated, [])

    def test_pagination_respects_max_pages_and_last_page(self):
        single = PetsmartListingSpider(category="dog/food", max_pages=1, now_ms=1)
        outputs = list(single.parse_search(self.response(self.page1, page=0)))
        self.assertFalse([out for out in outputs if not isinstance(out, dict)])
        exhausted = json.loads(self.page1)
        exhausted["nbPages"] = 1
        outputs = list(self.spider.parse_search(self.response(json.dumps(exhausted), page=0)))
        self.assertFalse([out for out in outputs if not isinstance(out, dict)])

    # --------------------------------------------------------------- failures

    def test_challenge_page_fails_loudly(self):
        body = "<!doctype html><html><body>Access Denied</body></html>"
        with self.assertRaisesRegex(RuntimeError, "challenge page"):
            list(self.spider.parse_search(self.response(body)))

    def test_api_error_envelope_fails_loudly(self):
        body = json.dumps({"message": "Index r-US_products_best-sellers does not exist", "status": 404})
        with self.assertRaisesRegex(RuntimeError, "does not exist"):
            list(self.spider.parse_search(self.response(body)))

    def test_non_200_and_missing_hits_fail_loudly(self):
        response = self.response(self.page1)
        response.status = 429
        with self.assertRaisesRegex(RuntimeError, "HTTP 429"):
            list(self.spider.parse_search(response))
        empty = json.dumps({"hits": None, "nbHits": 0})
        with self.assertRaisesRegex(RuntimeError, "no hits list"):
            list(self.spider.parse_search(self.response(empty)))

    def test_start_requests_targets_every_category_by_default(self):
        spider = PetsmartListingSpider(max_pages=1)
        self.assertEqual(len(list(spider.start_requests())), 491)


if __name__ == "__main__":
    unittest.main()
