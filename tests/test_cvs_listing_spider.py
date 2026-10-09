import json
import unittest

from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.cvs_listing_spider import CvsListingSpider
from common.spiders.cvs_categories import CVS_CATEGORY_INVENTORY

LISTING_URL = "https://www.cvs.com/shop/health-medicine"


def product(
    product_id="702568",
    title="Nature's Truth Melatonin 12mg & Magnesium Gummies, 60 CT",
    brand="Nature's Truth",
    list_price="21.99",
    sale_price="21.99",
    carepass="0.0",
    promo="",
    rating=None,
    reviews=None,
    ship_status="IN_STOCK",
    ship_qty=2052,
    pick_status="OUT_OF_STOCK",
    sdd_status="OUT_OF_STOCK",
    store_pickup=True,
    is_new=True,
    image="/bizcontent/merchandising/productimages/high_res/84009312838.jpg",
):
    variant = {
        "id": product_id,
        "displayName": title,
        "skuImageUrl": image,
        "skuSize": "60.00 Ct",
        "skuCount": None,
        "averageOverallRating": rating,
        "totalReviewCount": reviews,
        "storePickUpIndicator": store_pickup,
        "fsaIndicator": True,
        "hotDealsIndicator": False,
        "inventoryInfo": {
            "shipInv": {
                "locationAvailabilityStatus": ship_status,
                "locationAvailableToPromiseQuantity": ship_qty,
            },
            "pickInv": {"locationAvailabilityStatus": pick_status, "locationAvailableToPromiseQuantity": 0},
            "sddInv": {"locationAvailabilityStatus": sdd_status, "locationAvailableToPromiseQuantity": 0},
        },
        "coupons": {"promoDescription": None},
    }
    return {
        "id": product_id,
        "title": title,
        "url": f"/shop/some-slug-prodid-{product_id}",
        "brand": brand,
        "isNewProduct": is_new,
        "isFeatured": False,
        "isSponsored": False,
        "skuDynamicImageUrl": None,
        "priceInfo": {
            "listPrice": list_price,
            "salePrice": sale_price,
            "carepassPrice": carepass,
            "unitPrice": "$36.65/ea.",
            "promoDescription": promo,
        },
        "defaultVariant": variant,
        "variants": [variant],
    }


def response_for(payload, url=LISTING_URL, status=200, prefix="var productIndexData ="):
    body = f"<script>{prefix} {json.dumps(payload)};</script>"
    cls = HtmlResponse if status == 200 else TextResponse
    return cls(url, request=Request(url), body=body.encode(), encoding="utf-8", status=status)


def index(products, num_found=40, start=0, limit=20, page=1):
    return {
        "numFound": num_found,
        "start": start,
        "limit": limit,
        "page": page,
        "products": products,
        "refinements": [],
        "breadCrumbs": [{"title": "Health & Medicine", "href": "/shop/health-medicine"}],
    }


class CvsCategoryInventoryTests(unittest.TestCase):
    def test_inventory_is_nested_shop_urls_with_ids(self):
        self.assertGreaterEqual(len(CVS_CATEGORY_INVENTORY), 10)
        for department, node in CVS_CATEGORY_INVENTORY.items():
            self.assertTrue(node["url"].startswith("/shop/"), department)
            self.assertTrue(node["id"], department)

    def test_non_shop_navigation_is_excluded(self):
        blob = json.dumps(CVS_CATEGORY_INVENTORY)
        self.assertNotIn("/shop/brand-directory", blob)
        self.assertNotIn("/shop/content/", blob)

    def test_categories_flatten_to_unique_rows(self):
        spider = CvsListingSpider(category="allergy-medicine")
        slugs = [entry["category"] for entry in spider.iter_categories()]
        urls = [entry["url"] for entry in spider.iter_categories()]
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(len(urls), len(set(urls)))
        self.assertGreaterEqual(len(urls), 700)
        self.assertIn("health-medicine", slugs)
        self.assertIn("allergy-sinus", slugs)

    def test_categories_cover_subcategory_paths(self):
        entry = CvsListingSpider(category="allergy-medicine").category_entry("allergy-medicine")
        self.assertEqual(
            entry["url"],
            "https://www.cvs.com/shop/health-medicine/allergy-sinus/allergy-medicine",
        )
        self.assertEqual(entry["department"], "Health & Medicine")
        self.assertEqual(
            entry["breadcrumb"], ["Health & Medicine", "Allergy & Sinus", "Allergy Medicine"]
        )
        self.assertEqual(entry["category_id"], "cat510010")

    def test_cross_listed_labels_get_unique_slugs(self):
        rows = [
            e
            for e in CvsListingSpider(category="allergy-medicine").iter_categories()
            if "bar-soap" in e["category"]
        ]
        self.assertGreaterEqual(len(rows), 2)
        self.assertEqual(len({r["category"] for r in rows}), len(rows))


class CvsPageUrlTests(unittest.TestCase):
    def test_first_page_has_no_page_parameter(self):
        self.assertEqual(CvsListingSpider._page_url(LISTING_URL, 1), LISTING_URL)

    def test_page_parameter_is_appended(self):
        self.assertEqual(
            CvsListingSpider._page_url(LISTING_URL, 2), f"{LISTING_URL}?page=2"
        )

    def test_other_query_parameters_are_preserved(self):
        self.assertEqual(
            CvsListingSpider._page_url(f"{LISTING_URL}?sort=price", 3),
            f"{LISTING_URL}?sort=price&page=3",
        )
        self.assertEqual(
            CvsListingSpider._page_url(f"{LISTING_URL}?page=7", 1), LISTING_URL
        )


class CvsHydrationExtractionTests(unittest.TestCase):
    def test_missing_assignment_raises_actionable_error(self):
        spider = CvsListingSpider(category="health-medicine")
        response = HtmlResponse(
            LISTING_URL,
            request=Request(LISTING_URL),
            body=b"<html><body>no hydration here</body></html>",
            encoding="utf-8",
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response, LISTING_URL, 1))
        self.assertIn("productIndexData", str(ctx.exception))
        self.assertIn("no markup fallback", str(ctx.exception))

    def test_invalid_json_raises(self):
        spider = CvsListingSpider(category="health-medicine")
        body = b"<script>var productIndexData = {numFound: 3,</script>"
        response = HtmlResponse(
            LISTING_URL, request=Request(LISTING_URL), body=body, encoding="utf-8"
        )
        with self.assertRaises(RuntimeError):
            list(spider.parse(response, LISTING_URL, 1))

    def test_non_200_raises(self):
        spider = CvsListingSpider(category="health-medicine")
        response = response_for(index([product()]), status=503)
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response, LISTING_URL, 1))
        self.assertIn("503", str(ctx.exception))

    def test_missing_products_list_raises(self):
        spider = CvsListingSpider(category="health-medicine")
        response = response_for({"numFound": 3, "start": 0})
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response, LISTING_URL, 1))
        self.assertIn("no products list", str(ctx.exception))

    def test_string_whitespace_before_assignment_is_tolerated(self):
        spider = CvsListingSpider(category="health-medicine")
        response = response_for(index([product()]), prefix="var  productIndexData =")
        items = list(spider.parse(response, LISTING_URL, 1))
        self.assertEqual(len(items), 1)


class CvsItemMappingTests(unittest.TestCase):
    def test_fields_match_the_feed_contract(self):
        spider = CvsListingSpider(category="health-medicine")
        items = list(spider.parse(response_for(index([product()])), LISTING_URL, 1))
        self.assertEqual(list(items[0]), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_core_mapping(self):
        spider = CvsListingSpider(category="health-medicine")
        item = next(iter(spider.parse(response_for(index([product()])), LISTING_URL, 1)))
        self.assertEqual(item["item_id"], "702568")
        self.assertEqual(item["brand"], "Nature's Truth")
        self.assertEqual(
            item["url"],
            "https://www.cvs.com/shop/some-slug-prodid-702568",
        )
        self.assertEqual(
            item["image"],
            "https://www.cvs.com/bizcontent/merchandising/productimages/high_res/84009312838.jpg",
        )
        self.assertEqual(item["price"], 21.99)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["category"], "health-medicine")
        self.assertEqual(item["category_name"], "Health & Medicine")
        self.assertEqual(item["category_id"], "cat1")
        self.assertEqual(item["department"], "Health & Medicine")
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], 40)
        self.assertEqual(item["source"], "cvs_product_index_hydration")
        self.assertEqual(item["source_url"], LISTING_URL)

    def test_sale_pricing_is_only_reported_when_marked_down(self):
        spider = CvsListingSpider(category="health-medicine")
        items = list(
            spider.parse(
                response_for(
                    index(
                        [
                            product(),
                            product(
                                product_id="631451",
                                list_price="10.49",
                                sale_price="7.99",
                            ),
                        ]
                    )
                ),
                LISTING_URL,
                1,
            )
        )
        plain, sale = items
        self.assertEqual(plain["price"], 21.99)
        self.assertIsNone(plain["original_price"])
        self.assertIsNone(plain["sale_price"])
        self.assertEqual(sale["price"], 7.99)
        self.assertEqual(sale["original_price"], 10.49)
        self.assertEqual(sale["sale_price"], 7.99)

    def test_zero_carepass_price_is_reported_as_absent(self):
        spider = CvsListingSpider(category="health-medicine")
        item = next(
            iter(
                spider.parse(
                    response_for(index([product(carepass="0.0")])), LISTING_URL, 1
                )
            )
        )
        self.assertIsNone(item["carepass_price"])
        item = next(
            iter(
                spider.parse(
                    response_for(
                        index([product(product_id="1", carepass="9.99")])
                    ),
                    LISTING_URL,
                    1,
                )
            )
        )
        self.assertEqual(item["carepass_price"], 9.99)

    def test_inventory_and_fulfilment_flags(self):
        spider = CvsListingSpider(category="health-medicine")
        item = next(
            iter(
                spider.parse(
                    response_for(
                        index(
                            [
                                product(
                                    rating=3.8945,
                                    reviews=436,
                                    ship_status="OUT_OF_STOCK",
                                    ship_qty=0,
                                    pick_status="IN_STOCK",
                                    sdd_status="IN_STOCK",
                                )
                            ]
                        )
                    ),
                    LISTING_URL,
                    1,
                )
            )
        )
        self.assertEqual(item["rating"], 3.8945)
        self.assertEqual(item["reviews_count"], 436)
        self.assertFalse(item["in_stock"])
        self.assertEqual(item["stock_quantity"], 0)
        self.assertTrue(item["pickup_in_stock"])
        self.assertTrue(item["same_day_in_stock"])
        self.assertTrue(item["store_pickup"])
        self.assertTrue(item["fsa_eligible"])
        self.assertFalse(item["hot_deals"])

    def test_promo_message_and_optional_values(self):
        spider = CvsListingSpider(category="health-medicine")
        item = next(
            iter(
                spider.parse(
                    response_for(index([product(promo="Buy 1, Get 1 Free")])),
                    LISTING_URL,
                    1,
                )
            )
        )
        self.assertEqual(item["promo_message"], "Buy 1, Get 1 Free")
        self.assertIsNone(item["count"])
        self.assertEqual(item["unit_price"], "$36.65/ea.")
        self.assertEqual(item["size"], "60.00 Ct")

    def test_placeholder_zero_quantity_stays_zero(self):
        spider = CvsListingSpider(category="health-medicine")
        item = next(
            iter(
                spider.parse(
                    response_for(index([product(ship_qty=0)])), LISTING_URL, 1
                )
            )
        )
        self.assertEqual(item["stock_quantity"], 0)

    def test_absolute_url_handling(self):
        spider = CvsListingSpider(category="health-medicine")
        self.assertEqual(
            spider._absolute("//images.cvs.com/a.jpg"), "https://images.cvs.com/a.jpg"
        )
        self.assertEqual(
            spider._absolute("https://cdn.cvs.com/b.jpg"), "https://cdn.cvs.com/b.jpg"
        )
        self.assertEqual(spider._absolute("bizcontent/x.jpg"), "https://www.cvs.com/bizcontent/x.jpg")
        self.assertIsNone(spider._absolute(None))

    def test_raw_keeps_variants_for_downstream_rederivation(self):
        spider = CvsListingSpider(category="health-medicine")
        item = next(iter(spider.parse(response_for(index([product()])), LISTING_URL, 1)))
        self.assertEqual(set(item["raw"]), {"product", "variants"})
        self.assertEqual(item["raw"]["variants"][0]["id"], "702568")


class CvsPaginationTests(unittest.TestCase):
    def test_schedules_next_page(self):
        spider = CvsListingSpider(category="health-medicine", max_pages=3)
        output = list(
            spider.parse(
                response_for(index([product(product_id=str(i)) for i in range(1, 4)])),
                LISTING_URL,
                1,
            )
        )
        self.assertEqual(len(output), 4)
        request = output[-1]
        self.assertEqual(request.url, f"{LISTING_URL}?page=2")
        self.assertEqual(request.cb_kwargs["page"], 2)
        self.assertEqual(request.cb_kwargs["listing_url"], LISTING_URL)

    def test_max_pages_caps_the_crawl(self):
        spider = CvsListingSpider(category="health-medicine", max_pages=1)
        output = list(
            spider.parse(
                response_for(index([product()], num_found=3035)), LISTING_URL, 1
            )
        )
        self.assertEqual(len(output), 1)

    def test_last_page_from_num_found_stops_crawl(self):
        spider = CvsListingSpider(category="health-medicine", max_pages=5)
        output = list(
            spider.parse(
                response_for(index([product()], num_found=20, start=0, limit=20, page=1)),
                LISTING_URL,
                1,
            )
        )
        self.assertEqual(len(output), 1)

    def test_empty_products_list_stops_crawl(self):
        spider = CvsListingSpider(category="health-medicine", max_pages=5)
        output = list(
            spider.parse(response_for(index([], num_found=40)), LISTING_URL, 1)
        )
        self.assertEqual(output, [])

    def test_duplicate_page_yields_no_items_and_stops(self):
        spider = CvsListingSpider(category="health-medicine", max_pages=5)
        first = list(
            spider.parse(response_for(index([product()])), LISTING_URL, 1)
        )[0]
        self.assertIsNotNone(first)
        output = list(
            spider.parse(
                response_for(index([product()], start=20, page=2)), LISTING_URL, 2
            )
        )
        self.assertEqual(output, [])


class CvsCategoryResolutionTests(unittest.TestCase):
    def test_category_url_is_resolved_from_the_inventory(self):
        spider = CvsListingSpider(category="allergy-sinus")
        self.assertEqual(
            spider.resolve_target_url(),
            "https://www.cvs.com/shop/health-medicine/allergy-sinus",
        )

    def test_start_requests_target_the_resolved_url(self):
        spider = CvsListingSpider(category="health-medicine")
        request = next(iter(spider.start_requests()))
        self.assertEqual(request.url, LISTING_URL)
        self.assertEqual(request.cb_kwargs["page"], 1)

    def test_explicit_category_url_is_supported(self):
        spider = CvsListingSpider(
            category_url="https://www.cvs.com/shop/vitamins/multivitamins"
        )
        request = next(iter(spider.start_requests()))
        self.assertEqual(
            request.url, "https://www.cvs.com/shop/vitamins/multivitamins"
        )

    def test_unknown_category_is_rejected(self):
        with self.assertRaises(ValueError):
            CvsListingSpider(category="not-a-real-category")

    def test_missing_category_is_rejected(self):
        with self.assertRaises(ValueError):
            CvsListingSpider()

    def test_unlisted_url_falls_back_to_a_derived_slug(self):
        spider = CvsListingSpider(url="https://www.cvs.com/shop/some-new-shelf")
        item = next(
            iter(
                spider.parse(
                    response_for(index([product()]), url="https://www.cvs.com/shop/some-new-shelf"),
                    "https://www.cvs.com/shop/some-new-shelf",
                    1,
                )
            )
        )
        self.assertEqual(item["category"], "some-new-shelf")
        self.assertIsNone(item["category_id"])
        self.assertIsNone(item["department"])


if __name__ == "__main__":
    unittest.main()