import json
import unittest

import scrapy
from scrapy.http import HtmlResponse, Request

from common.spiders.backcountry_categories import (
    BACKCOUNTRY_CATEGORIES,
    BACKCOUNTRY_CATEGORY_INVENTORY,
    BACKCOUNTRY_SLUG_LABELS,
)
from common.spiders.backcountry_listing_spider import (
    BackcountryListingSpider,
    absolute_url,
    to_float,
    to_int,
)

LISTING_URL = "https://www.backcountry.com/cat/mens-shirts"
RC_URL = "https://www.backcountry.com/rc/mens-upf-apparel"
# The header taxonomy stores this filter with literal quotes; the spider must
# copy such a query verbatim instead of re-escaping it.
BRAND_URL = 'https://www.backcountry.com/brand/patagonia?p=gender_uFilter:"male"'


def product(product_id="FJRZ133", **overrides):
    node = {
        "__typename": "Product",
        "id": product_id,
        "name": "Fjallglim Regular Shirt - Men's",
        "url": "/fjallraven-fjallglim-regular-shirt-mens",
        "stockStatus": "IN_STOCK",
        "brand": {"__typename": "ProductBrand", "name": "Fjallraven"},
        "aggregates": {
            "__typename": "ProductAggregates",
            "totalColors": 3,
            "totalVariations": 10,
            "variationsOnSale": 0,
            "minDiscount": 0,
            "minListPrice": 124.95,
            "minSalePrice": 124.95,
            "maxDiscount": 0,
            "maxListPrice": 124.95,
            "maxSalePrice": 124.95,
            "pastSeasonColors": ["DANACHWH", "DARNAVMAR", "WOBRBLOA"],
        },
        "flags": {
            "__typename": "ProductFlags",
            "isExclusive": False,
            "isNewArrival": False,
            "isPastSeason": True,
            "isGearheadPick": False,
        },
        "reviewAggregates": {
            "__typename": "ProductReviewAggregates",
            "totalReviews": 0,
            "averageRating": 0,
        },
        "colors": [
            {
                "__typename": "ProductColor",
                "colorId": "DANACHWH",
                "name": "Dark Navy/Chalk White",
                "tileImage": "/images/items/160/FJR/FJRZ133/DANACHWH.jpg",
                "pliImage": "/images/items/large/FJR/FJRZ133/DANACHWH.jpg",
            }
        ],
    }
    node.update(overrides)
    return node


def page_props(nodes, total_pages=36, total_count=1490, has_next=True, has_prev=False,
               category_id="bc-mens-shirts", page_type="plp-cat", apollo=True):
    block_key = {
        "plp-cat": "category",
        "plp-collection": "collection",
        "plp-brand": "brand",
    }.get(page_type, "category")
    props = {
        "type": page_type,
        "totalCount": total_count,
        "totalPages": total_pages,
        "plpData": {
            "data": {
                block_key: {
                    "__typename": block_key.title(),
                    "edges": [{"__typename": "ProductEdge", "node": node} for node in nodes],
                    "pageInfo": {
                        "__typename": "ProductListingPageInfo",
                        "hasNextPage": has_next,
                        "hasPreviousPage": has_prev,
                    },
                }
            },
            "loading": False,
            "networkStatus": 7,
        },
    }
    if page_type == "plp-collection":
        props["collectionId"] = category_id
    elif page_type == "plp-brand":
        props["brandSlug"] = category_id
    else:
        props["categoryId"] = category_id
    if apollo:
        props["__APOLLO_STATE__"] = {
            f"Product:{node['id']}": node for node in nodes
        }
        props["__APOLLO_STATE__"][f"Category:{category_id}"] = {
            "__typename": "Category",
            "id": category_id,
            "name": "Men's Shirts",
        }
    return props


def response_for(props, url=LISTING_URL, status=200):
    payload = {"props": {"pageProps": props}, "buildId": "5.33.0"}
    body = (
        '<!DOCTYPE html><html><head><title>Men&#x27;s Shirts</title></head><body>'
        f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(payload)}</script>'
        "</body></html>"
    )
    return HtmlResponse(
        url, request=Request(url), body=body.encode(), encoding="utf-8", status=status
    )


def raw_response(body, url=LISTING_URL, status=200):
    return HtmlResponse(
        url, request=Request(url), body=body.encode(), encoding="utf-8", status=status
    )


class BackcountryTaxonomyTests(unittest.TestCase):
    def test_inventory_slugs_are_unique_and_labelled(self):
        slugs = [entry["slug"] for entry in BACKCOUNTRY_CATEGORY_INVENTORY]
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertEqual(len(slugs), 469)
        for entry in BACKCOUNTRY_CATEGORY_INVENTORY:
            self.assertEqual(entry["slug"], BACKCOUNTRY_SLUG_LABELS[entry["slug"]]["slug"])
            self.assertTrue(entry["department"])
            self.assertTrue(entry["section"])
            self.assertTrue(entry["name"])
            self.assertTrue(entry["url"].startswith("https://www.backcountry.com/"))

    def test_inventory_counts_match_the_captured_header(self):
        departments = {e["department"] for e in BACKCOUNTRY_CATEGORY_INVENTORY}
        sections = {(e["department"], e["section"]) for e in BACKCOUNTRY_CATEGORY_INVENTORY}
        # The header has 14 departments / 109 sections; "Guides" and 49 sections
        # carry no links, so 12 departments / 60 sections reach the inventory.
        self.assertEqual(len(departments), 12)
        self.assertEqual(len(sections), 60)
        # 71 links are cross-listed under a second department/section.
        self.assertEqual(len({e["url"] for e in BACKCOUNTRY_CATEGORY_INVENTORY}), 398)

    def test_links_without_category_id_are_kept(self):
        without_id = [e for e in BACKCOUNTRY_CATEGORY_INVENTORY if not e["category_id"]]
        self.assertEqual(len(without_id), 469 - 230)
        # /rc/ redirect endpoints and brand-filtered URLs must survive.
        self.assertTrue(any("/rc/" in e["url"] for e in without_id))
        self.assertTrue(any("/brand/" in e["url"] for e in without_id))

    def test_category_map_matches_base_spider_schema(self):
        self.assertEqual(len(BACKCOUNTRY_CATEGORIES), len(BACKCOUNTRY_CATEGORY_INVENTORY))
        for entry in BACKCOUNTRY_CATEGORIES:
            self.assertEqual(set(entry), {"category", "url"})
        shirts = next(
            e for e in BACKCOUNTRY_CATEGORIES if e["category"] == "men/clothing/shirts"
        )
        self.assertEqual(shirts["url"], LISTING_URL)

    def test_taxonomy_slugs_are_derived_from_labels(self):
        slug = BACKCOUNTRY_SLUG_LABELS["men/clothing/hoodies-sweatshirts"]
        self.assertEqual(slug["name"], "Hoodies & Sweatshirts")
        self.assertEqual(slug["category_id"], "bc-mens-hoodies-sweatshirts")


class BackcountryHelperTests(unittest.TestCase):
    def test_to_float_accepts_strings_and_rejects_junk(self):
        self.assertEqual(to_float("$1,249.95"), 1249.95)
        self.assertEqual(to_float(35), 35.0)
        self.assertIsNone(to_float("n/a"))
        self.assertIsNone(to_float(""))
        self.assertIsNone(to_float(None))
        # bool is an int subclass; it must not become 1.0
        self.assertIsNone(to_float(True))

    def test_to_int(self):
        self.assertEqual(to_int("42"), 42)
        self.assertIsNone(to_int("many"))

    def test_absolute_url(self):
        self.assertEqual(
            absolute_url("/fjallraven-fjallglim-regular-shirt-mens"),
            "https://www.backcountry.com/fjallraven-fjallglim-regular-shirt-mens",
        )
        self.assertEqual(
            absolute_url("//www.backcountry.com/x"),
            "https://www.backcountry.com/x",
        )
        self.assertEqual(
            absolute_url("https://www.backcountry.com/y"),
            "https://www.backcountry.com/y",
        )
        self.assertIsNone(absolute_url(""))
        self.assertIsNone(absolute_url(None))
        self.assertIsNone(absolute_url(123))


class BackcountryPageUrlTests(unittest.TestCase):
    def test_first_page_keeps_url_and_filters(self):
        self.assertEqual(BackcountryListingSpider._page_url(BRAND_URL, 1), BRAND_URL)

    def test_page_two_merges_page_into_existing_query(self):
        self.assertEqual(
            BackcountryListingSpider._page_url(BRAND_URL, 2),
            f"{BRAND_URL}&page=2",
        )

    def test_page_two_on_plain_category_url(self):
        self.assertEqual(
            BackcountryListingSpider._page_url(LISTING_URL, 2),
            f"{LISTING_URL}?page=2",
        )

    def test_page_two_replaces_an_existing_page_param(self):
        self.assertEqual(
            BackcountryListingSpider._page_url(f"{LISTING_URL}?page=7", 2),
            f"{LISTING_URL}?page=2",
        )

    def test_page_two_keeps_other_params_while_replacing_page(self):
        url = "https://www.backcountry.com/rc/approach-shoes?p=u_categoryPathId:bc-mens-footwear&page=7"
        self.assertEqual(
            BackcountryListingSpider._page_url(url, 2),
            "https://www.backcountry.com/rc/approach-shoes?p=u_categoryPathId:bc-mens-footwear&page=2",
        )


class BackcountryParseTests(unittest.TestCase):
    def make(self, **kwargs):
        spider = BackcountryListingSpider(category="men/clothing/shirts", **kwargs)
        spider.settings = None
        return spider

    def test_page_one_items_cover_feed_fields(self):
        spider = self.make()
        items = list(
            spider.parse(response_for(page_props([product(), product("PATZBBQ", name="Second Shirt")])), LISTING_URL, 1)
        )
        items = [i for i in items if isinstance(i, dict)]
        self.assertEqual(len(items), 2)
        first = items[0]
        self.assertEqual(list(first), spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(first["item_id"], "FJRZ133")
        self.assertEqual(first["title"], "Fjallglim Regular Shirt - Men's")
        self.assertEqual(first["brand"], "Fjallraven")
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["price"], 124.95)
        self.assertEqual(first["original_price"], 124.95)
        self.assertEqual(first["on_sale"], False)
        self.assertEqual(first["discount_percent"], 0.0)
        self.assertEqual(first["availability"], "IN_STOCK")
        self.assertTrue(first["in_stock"])
        self.assertEqual(first["stock_status"], "IN_STOCK")
        self.assertEqual(
            first["url"],
            "https://www.backcountry.com/fjallraven-fjallglim-regular-shirt-mens",
        )
        self.assertEqual(first["listing_url"], LISTING_URL)
        self.assertEqual(
            first["image_url"],
            "https://www.backcountry.com/images/items/large/FJR/FJRZ133/DANACHWH.jpg",
        )
        self.assertEqual(first["image"], first["image_url"])
        self.assertEqual(first["color"], "Dark Navy/Chalk White")
        self.assertEqual(first["colors"], ["Dark Navy/Chalk White"])
        self.assertEqual(first["color_ids"], ["DANACHWH"])
        self.assertEqual(first["color_count"], 3)
        self.assertEqual(first["total_variations"], 10)
        self.assertEqual(first["past_season_colors"], ["DANACHWH", "DARNAVMAR", "WOBRBLOA"])
        self.assertTrue(first["is_past_season"])
        self.assertFalse(first["is_new_arrival"])
        self.assertEqual(first["page"], 1)
        self.assertEqual(first["source"], "backcountry_next_data")
        self.assertEqual(first["raw"]["id"], "FJRZ133")

    def test_category_labels_are_attached(self):
        spider = self.make()
        item = next(
            i for i in spider.parse(response_for(page_props([product()])), LISTING_URL, 1)
            if isinstance(i, dict)
        )
        self.assertEqual(item["department"], "Men")
        self.assertEqual(item["section"], "Clothing")
        self.assertEqual(item["category_name"], "Shirts")
        self.assertEqual(item["category_slug"], "men/clothing/shirts")
        self.assertEqual(item["category_id"], "bc-mens-shirts")

    def test_sale_price_and_discount(self):
        spider = self.make()
        on_sale = product(
            "BJOC0B1",
            aggregates={
                "totalColors": 4,
                "totalVariations": 7,
                "variationsOnSale": 7,
                "minDiscount": 40,
                "minListPrice": 34.95,
                "minSalePrice": 20.97,
                "maxDiscount": 40,
                "maxListPrice": 34.95,
                "maxSalePrice": 20.97,
                "pastSeasonColors": [],
            },
            reviewAggregates={"totalReviews": 12, "averageRating": 4.5},
        )
        item = next(
            i for i in spider.parse(response_for(page_props([on_sale])), LISTING_URL, 1)
            if isinstance(i, dict)
        )
        self.assertEqual(item["price"], 20.97)
        self.assertEqual(item["original_price"], 34.95)
        self.assertTrue(item["on_sale"])
        self.assertEqual(item["discount_percent"], 40.0)
        self.assertEqual(item["rating"], 4.5)
        self.assertEqual(item["reviews_count"], 12)

    def test_out_of_stock_flag(self):
        spider = self.make()
        item = next(
            i
            for i in spider.parse(
                response_for(page_props([product(stockStatus="OUT_OF_STOCK")])),
                LISTING_URL,
                1,
            )
            if isinstance(i, dict)
        )
        self.assertFalse(item["in_stock"])
        self.assertEqual(item["availability"], "OUT_OF_STOCK")

    def test_page_two_request_is_scheduled(self):
        spider = self.make(max_pages=2)
        output = list(spider.parse(response_for(page_props([product()])), LISTING_URL, 1))
        request = output[-1]
        self.assertIsInstance(request, scrapy.Request)
        self.assertEqual(request.url, f"{LISTING_URL}?page=2")
        self.assertEqual(request.cb_kwargs, {"listing_url": LISTING_URL, "page": 2})

    def test_max_pages_stops_pagination(self):
        spider = self.make(max_pages=1)
        output = list(spider.parse(response_for(page_props([product()])), LISTING_URL, 1))
        self.assertFalse([o for o in output if isinstance(o, scrapy.Request)])

    def test_total_pages_stops_pagination_before_max_pages(self):
        spider = self.make(max_pages=10)
        output = list(
            spider.parse(
                response_for(page_props([product()], total_pages=1)), LISTING_URL, 1
            )
        )
        self.assertFalse([o for o in output if isinstance(o, scrapy.Request)])

    def test_has_next_page_false_stops_when_total_pages_missing(self):
        spider = self.make(max_pages=5)
        props = page_props([product()], total_pages=None, has_next=False)
        output = list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertFalse([o for o in output if isinstance(o, scrapy.Request)])

    def test_has_next_page_true_continues_when_total_pages_missing(self):
        spider = self.make(max_pages=5)
        props = page_props([product()], total_pages=None, has_next=True)
        output = list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertTrue([o for o in output if isinstance(o, scrapy.Request)])

    def test_deduplicates_products_across_pages(self):
        spider = self.make(max_pages=3)
        first_page = product()
        second_page_product = product("ICEZ79D", name="Third Shirt")

        page1 = [
            i for i in spider.parse(response_for(page_props([first_page])), LISTING_URL, 1)
            if isinstance(i, dict)
        ]
        self.assertEqual([i["item_id"] for i in page1], ["FJRZ133"])

        # page 2 repeats the page-1 product and adds one new one
        page2 = [
            i
            for i in spider.parse(
                response_for(page_props([first_page, second_page_product])), LISTING_URL, 2
            )
            if isinstance(i, dict)
        ]
        self.assertEqual([i["item_id"] for i in page2], ["ICEZ79D"])
        self.assertEqual(page2[0]["page"], 2)

        # page 3 repeats only seen ids -> nothing new is emitted
        page3 = [
            i for i in spider.parse(response_for(page_props([first_page])), LISTING_URL, 3)
            if isinstance(i, dict)
        ]
        self.assertEqual(page3, [])

    def test_apollo_state_record_is_joined(self):
        spider = self.make()
        # Edge node lacks the flag; the Apollo record carries it.
        edge_node = product()
        edge_node["flags"] = {}
        props = page_props([edge_node])
        props["__APOLLO_STATE__"]["Product:FJRZ133"]["flags"] = {
            "isNewArrival": True,
            "isPastSeason": False,
            "isExclusive": False,
            "isGearheadPick": True,
        }
        item = next(
            i for i in spider.parse(response_for(props), LISTING_URL, 1)
            if isinstance(i, dict)
        )
        self.assertTrue(item["is_new_arrival"])
        self.assertTrue(item["is_gearhead_pick"])

    def test_edges_still_parse_without_apollo_state(self):
        spider = self.make()
        item = next(
            i
            for i in spider.parse(
                response_for(page_props([product()], apollo=False)), LISTING_URL, 1
            )
            if isinstance(i, dict)
        )
        self.assertEqual(item["item_id"], "FJRZ133")

    def test_absolute_urls_for_relative_and_protocol_relative_paths(self):
        spider = self.make()
        item = next(
            i
            for i in spider.parse(
                response_for(page_props([product(url="//www.backcountry.com/rel-prod")])), LISTING_URL, 1
            )
            if isinstance(i, dict)
        )
        self.assertEqual(item["url"], "https://www.backcountry.com/rel-prod")

    def test_image_falls_back_to_tile_image(self):
        spider = self.make()
        node = product()
        node["colors"] = [{"colorId": "X", "name": "Blue", "tileImage": "/images/items/160/x.jpg"}]
        item = next(
            i for i in spider.parse(response_for(page_props([node])), LISTING_URL, 1)
            if isinstance(i, dict)
        )
        self.assertEqual(item["image_url"], "https://www.backcountry.com/images/items/160/x.jpg")

    def test_missing_colors_do_not_break_extraction(self):
        spider = self.make()
        node = product()
        node["colors"] = []
        item = next(
            i for i in spider.parse(response_for(page_props([node])), LISTING_URL, 1)
            if isinstance(i, dict)
        )
        self.assertIsNone(item["color"])
        self.assertEqual(item["colors"], [])

    def test_direct_url_run_still_gets_labels_from_the_taxonomy(self):
        spider = BackcountryListingSpider(url=LISTING_URL)
        spider.settings = None
        item = next(
            i for i in spider.parse(response_for(page_props([product()])), LISTING_URL, 1)
            if isinstance(i, dict)
        )
        self.assertEqual(item["category_slug"], "men/clothing/shirts")
        self.assertEqual(item["category_id"], "bc-mens-shirts")


class BackcountryFailureTests(unittest.TestCase):
    def make(self, **kwargs):
        spider = BackcountryListingSpider(category="men/clothing/shirts", **kwargs)
        spider.settings = None
        return spider

    def test_non_200_raises(self):
        spider = self.make()
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(page_props([product()]), status=403), LISTING_URL, 1))
        self.assertIn("HTTP 403", str(ctx.exception))

    def test_missing_next_data_raises(self):
        spider = self.make()
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(raw_response("<html><body>no hydration here</body></html>"), LISTING_URL, 1))
        self.assertIn("hydration schema error", str(ctx.exception))

    def test_invalid_next_data_json_raises(self):
        spider = self.make()
        body = '<script id="__NEXT_DATA__" type="application/json">{not json</script>'
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(raw_response(body), LISTING_URL, 1))
        self.assertIn("hydration schema error", str(ctx.exception))

    def test_waf_challenge_raises_actionable_error(self):
        spider = self.make()
        body = (
            '<html><head><script type="text/javascript">window.awsWafCookieDomainList = '
            'window.awsWafCookieDomainList || [];</script></head><body></body></html>'
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(raw_response(body), LISTING_URL, 1))
        message = str(ctx.exception)
        self.assertIn("AWS WAF challenge", message)
        self.assertIn("residential=true", message)

    def test_grecaptcha_badge_in_real_page_is_not_a_challenge(self):
        # The live category page embeds this style block; a generic "captcha"
        # marker would reject every successful response.
        spider = self.make()
        body = (
            "<html><head><style>.grecaptcha-badge { visibility: hidden; }</style>"
            "</head><body>"
            '<script id="__NEXT_DATA__" type="application/json">'
            f"{json.dumps({'props': {'pageProps': page_props([product()])}})}"
            "</script></body></html>"
        )
        items = [
            i for i in spider.parse(raw_response(body), LISTING_URL, 1)
            if isinstance(i, dict)
        ]
        self.assertEqual([i["item_id"] for i in items], ["FJRZ133"])

    def test_deny_page_names_the_proxy_remedy(self):
        spider = self.make()
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(raw_response("<html>Access Denied</html>"), LISTING_URL, 1))
        message = str(ctx.exception)
        self.assertIn("hydration schema error", message)
        self.assertIn("residential=true", message)

    def test_non_plp_page_type_raises(self):
        spider = self.make()
        props = page_props([product()], page_type="pd")
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertIn("not a product listing page", str(ctx.exception))

    def test_rc_collection_page_parses(self):
        # /rc/ redirect endpoints render as plp-collection, keyed under
        # data.collection with a collectionId instead of a categoryId.
        spider = BackcountryListingSpider(category="men/clothing/sun-protection")
        spider.settings = None
        url = RC_URL
        props = page_props(
            [product()], total_pages=10, total_count=382,
            category_id="mens-upf-apparel", page_type="plp-collection",
        )
        items = [
            i
            for i in spider.parse(
                response_for(props, url=url), url, 1
            )
            if isinstance(i, dict)
        ]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category_id"], "mens-upf-apparel")
        self.assertEqual(items[0]["department"], "Men")
        self.assertEqual(items[0]["category_name"], "Sun Protection")

    def test_brand_page_parses(self):
        url = BRAND_URL
        spider = BackcountryListingSpider(url=url)
        spider.settings = None
        props = page_props(
            [product()], total_pages=9, total_count=355,
            category_id="patagonia", page_type="plp-brand",
        )
        items = [
            i for i in spider.parse(response_for(props, url=url), url, 1)
            if isinstance(i, dict)
        ]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category_slug"], "men/top-brands/patagonia")
        self.assertEqual(items[0]["department"], "Men")

    def test_brand_filtered_page_two_keeps_the_filter(self):
        url = BRAND_URL
        spider = BackcountryListingSpider(url=url, max_pages=2)
        spider.settings = None
        output = list(
            spider.parse(
                response_for(page_props([product()], category_id="patagonia",
                                        page_type="plp-brand"), url=url),
                url,
                1,
            )
        )
        request = output[-1]
        # The brand/gender filter must survive pagination. Scrapy normalizes
        # the literal quotes to %22, which is the correct wire form.
        self.assertEqual(
            request.url,
            'https://www.backcountry.com/brand/patagonia'
            "?p=gender_uFilter:%22male%22&page=2",
        )

    def test_missing_plp_data_raises(self):
        spider = self.make()
        props = {"type": "plp-cat", "categoryId": "bc-mens-shirts"}
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertIn("no PLP data", str(ctx.exception))

    def test_unrecognized_plp_block_raises(self):
        spider = self.make()
        props = {
            "type": "plp-cat",
            "categoryId": "bc-mens-shirts",
            "plpData": {"data": {"somethingElse": {}}},
        }
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertIn("no PLP data", str(ctx.exception))

    def test_missing_edges_raises(self):
        spider = self.make()
        props = {
            "type": "plp-cat",
            "categoryId": "bc-mens-shirts",
            "plpData": {"data": {"category": {"pageInfo": {"hasNextPage": False}}}},
        }
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertIn("no product edges", str(ctx.exception))

    def test_empty_edges_raises(self):
        spider = self.make()
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(page_props([])), LISTING_URL, 1))
        self.assertIn("no product edges", str(ctx.exception))

    def test_edges_of_wrong_type_raise(self):
        spider = self.make()
        props = page_props([product()])
        props["plpData"]["data"]["category"]["edges"] = {"nope": True}
        with self.assertRaises(RuntimeError) as ctx:
            list(spider.parse(response_for(props), LISTING_URL, 1))
        self.assertIn("not a list", str(ctx.exception))

    def test_missing_target_raises(self):
        with self.assertRaises(ValueError) as ctx:
            BackcountryListingSpider()
        self.assertIn("men/clothing/shirts", str(ctx.exception))

    def test_unknown_category_raises(self):
        with self.assertRaises(ValueError) as ctx:
            list(
                BackcountryListingSpider(category="nope/nope/nope").start_requests()
            )
        self.assertIn("Unknown category", str(ctx.exception))


class BackcountryProxyTests(unittest.TestCase):
    def make_with_proxy(self, proxy):
        spider = BackcountryListingSpider(category="men/clothing/shirts")
        spider.settings = _Settings(proxy)
        return spider

    def test_residential_is_appended_to_scrapeops_username(self):
        spider = self.make_with_proxy(
            "http://scrapeops.country=us:test_key@proxy.scrapeops.io:5353"
        )
        proxy = spider._residential_proxy()
        self.assertIn("scrapeops.country=us.residential=true", proxy)
        self.assertIn("test_key@proxy.scrapeops.io:5353", proxy)

    def test_existing_username_options_are_preserved(self):
        spider = self.make_with_proxy(
            "http://scrapeops.country=us.bypass=7:tok@proxy.scrapeops.io:5353"
        )
        proxy = spider._residential_proxy()
        self.assertIn("scrapeops.country=us.bypass=7.residential=true", proxy)
        self.assertIn("tok@proxy.scrapeops.io:5353", proxy)

    def test_residential_is_appended_only_once(self):
        spider = self.make_with_proxy(
            "http://scrapeops.country=us.residential=true:tok@proxy.scrapeops.io:5353"
        )
        proxy = spider._residential_proxy()
        self.assertEqual(proxy.count("residential=true"), 1)

    def test_non_scrapeops_proxy_is_unchanged(self):
        spider = self.make_with_proxy("http://user:pass@proxy.example.com:8080")
        self.assertIsNone(spider._residential_proxy())

    def test_no_proxy_returns_none(self):
        spider = self.make_with_proxy(None)
        self.assertIsNone(spider._residential_proxy())

    def test_requests_carry_the_residential_proxy(self):
        spider = BackcountryListingSpider(category="men/clothing/shirts")
        spider.settings = _Settings("http://scrapeops.country=us:tok@proxy.scrapeops.io:5353")
        request = next(spider.start_requests())
        self.assertIn("residential=true", request.meta["proxy"])

    def test_page_requests_carry_the_residential_proxy(self):
        spider = BackcountryListingSpider(category="men/clothing/shirts", max_pages=2)
        spider.settings = _Settings("http://scrapeops.country=us:tok@proxy.scrapeops.io:5353")
        first = next(spider.start_requests())
        second = spider._page_request(LISTING_URL, 2)
        for request in (first, second):
            self.assertIn("residential=true", request.meta["proxy"])

    def test_requests_omit_proxy_when_not_configured(self):
        spider = BackcountryListingSpider(category="men/clothing/shirts")
        spider.settings = _Settings(None)
        self.assertNotIn("proxy", next(spider.start_requests()).meta)


class _Settings:
    def __init__(self, proxy):
        self._proxy = proxy

    def get(self, key, default=None):
        if key == "PROXY":
            return self._proxy
        return default


if __name__ == "__main__":
    unittest.main()