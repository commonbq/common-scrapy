"""Offline tests for `michaels_listing` (issue #185).

Every test here runs against committed fixtures in `sample/` and touches no
network: the RSC fixtures are re-wrapped into the exact
`self.__next_f.push([1,"..."])` document shape Michaels streams, so the spider's
real regex/raw_decode path is what gets exercised.
"""

from __future__ import annotations

import json
from pathlib import Path

import unittest

from scrapy.http import Request, TextResponse

from common.spiders.michaels_categories import (
    MICHAELS_CATEGORY_SITEMAP_URL,
    category_path_parts,
    parse_category_sitemap,
    resolve_category,
)
from common.spiders.michaels_listing_spider import MichaelsListingSpider

SITEMAP_FIXTURE = Path("sample/michaels-category-sitemap.xml")
PAGE1_FIXTURE = Path("sample/michaels-listing-rsc-page1.json")
PAGE2_FIXTURE = Path("sample/michaels-listing-rsc-page2.json")

PLP_URL = "https://www.michaels.com/shop/home-decor/floral-arrangements/"


def rsc_document(props: dict) -> str:
    """Render props the way a Next.js App Router page streams them."""
    buffer = json.dumps(props, separators=(",", ":"), ensure_ascii=False)
    chunk = json.dumps(buffer, ensure_ascii=False)
    return (
        "<!DOCTYPE html><html><body><h1>Floral Arrangements</h1>"
        f"<script>self.__next_f.push([1,{chunk}])</script>"
        "</body></html>"
    )


def props_from(fixture: Path, **overrides) -> dict:
    props = json.loads(fixture.read_text(encoding="utf-8"))["props"]
    props.update(overrides)
    return props


class MichaelsListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = MichaelsListingSpider(category="floral-arrangements", max_pages=2)
        self.sitemap = parse_category_sitemap(SITEMAP_FIXTURE.read_text(encoding="utf-8"))

    def listing_response(self, document: str, url: str = PLP_URL, page: int = 1):
        target = next(
            entry for entry in self.sitemap if entry["url"] == PLP_URL
        )
        request = Request(
            url,
            meta={
                "category": target,
                "page": page,
                "base_url": PLP_URL,
                "proxy": "http://proxy.invalid:8080",
            },
        )
        return TextResponse(url, request=request, body=document, encoding="utf-8")

    def split(self, outputs):
        items = [entry for entry in outputs if isinstance(entry, dict)]
        requests = [entry for entry in outputs if not isinstance(entry, dict)]
        return items, requests

    # ------------------------------------------------------------- inventory

    def test_sitemap_inventory_shape(self):
        self.assertEqual(len(self.sitemap), 60)
        self.assertEqual(len({e["category"] for e in self.sitemap}), 60)
        self.assertEqual(len({e["url"] for e in self.sitemap}), 60)
        self.assertTrue(all(e["url"].startswith("https://www.michaels.com/shop/") for e in self.sitemap))

        by_url = {e["url"]: e for e in self.sitemap}
        floral = by_url["https://www.michaels.com/shop/home-decor/floral-arrangements/"]
        self.assertEqual(floral["category"], "floral-arrangements")
        self.assertEqual(floral["department"], "home-decor")
        self.assertEqual(floral["subcategory"], "floral-arrangements")

        deep = by_url[
            "https://www.michaels.com/shop/craft-machines/cricut/cricut-materials-tools-accessories/"
            "mats-tools-accessories/cricut-storage/"
        ]
        self.assertEqual(deep["department"], "craft-machines")
        self.assertEqual(deep["subcategory"], "cricut/cricut-materials-tools-accessories/mats-tools-accessories/cricut-storage")

    def test_repeated_leaf_slugs_are_disambiguated_by_department(self):
        # `art-storage` appears under kids/ and under art-supplies/ in the
        # fixture, and `bead-jewelry-storage` under beads-jewelry/ and storage/.
        arts = sorted(e["category"] for e in self.sitemap if e["url"].endswith("art-storage/"))
        self.assertEqual(arts, ["art-supplies-art-storage", "kids-art-storage"])
        beads = sorted(
            e["category"] for e in self.sitemap if e["url"].endswith("/bead-jewelry-storage/")
        )
        self.assertEqual(beads, ["beads-jewelry-bead-jewelry-storage", "storage-bead-jewelry-storage"])

    def test_category_path_parts_ignores_scheme_query_and_non_shop_urls(self):
        self.assertEqual(
            category_path_parts("https://www.michaels.com/shop/kids/art-supplies/art-storage/"),
            ["kids", "art-supplies", "art-storage"],
        )
        self.assertEqual(category_path_parts("/shop/fabric/"), ["fabric"])
        self.assertEqual(category_path_parts("/shop/kids?page=2#top"), ["kids"])
        self.assertEqual(category_path_parts("https://www.michaels.com/product/xyz-10809872"), [])
        self.assertEqual(category_path_parts(""), [])

    def test_resolve_category_by_slug_and_by_url(self):
        by_slug = resolve_category(self.sitemap, category="floral-arrangements")
        self.assertEqual(by_slug["department"], "home-decor")

        for url in (
            "https://www.michaels.com/shop/home-decor/floral-arrangements",
            "https://www.michaels.com/shop/home-decor/floral-arrangements/",
            "/shop/home-decor/floral-arrangements/",
            "https://www.michaels.com/shop/home-decor/floral-arrangements?page=3",
        ):
            with self.subTest(url=url):
                self.assertEqual(
                    resolve_category(self.sitemap, category_url=url)["category"],
                    "floral-arrangements",
                )

        self.assertIsNone(resolve_category(self.sitemap, category="nope-not-a-category"))
        self.assertIsNone(resolve_category(self.sitemap, category_url="https://www.michaels.com/help"))
        self.assertIsNone(resolve_category(self.sitemap))

    def test_category_arg_may_be_a_shop_path(self):
        entry = resolve_category(self.sitemap, category="/shop/home-decor/floral-arrangements/")
        self.assertEqual(entry["category"], "floral-arrangements")

    # -------------------------------------------------------------- hydration

    def test_flight_payload_is_reassembled_from_chunks(self):
        buffer = self.spider._flight_payload(rsc_document(props_from(PAGE1_FIXTURE)))
        self.assertIn('"initialProducts":[', buffer)
        self.assertIn('"initialTotal":3315', buffer)

    def test_page_one_item_contract_and_pagination(self):
        outputs = list(self.spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE)))))
        items, requests = self.split(outputs)

        self.assertEqual(len(items), 4)
        self.assertEqual(len(requests), 1)
        follow = requests[0]
        self.assertEqual(follow.url, PLP_URL + "?page=2")
        self.assertEqual(follow.meta["page"], 2)
        self.assertEqual(follow.meta["proxy"], "http://proxy.invalid:8080")
        self.assertEqual(follow.callback, self.spider.parse)

        item = items[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["category"], "floral-arrangements")
        self.assertEqual(item["department"], "home-decor")
        self.assertEqual(item["subcategory"], "floral-arrangements")
        self.assertEqual(item["item_id"], "10809872")
        self.assertEqual(item["sku"], "10809872")
        self.assertIsNone(item["master_sku"])
        self.assertEqual(item["title"], '11" Pink Peony & Cream Rose Mix Bouquet by Ashland®')
        self.assertEqual(item["brand"], "Michaels")
        self.assertEqual(item["product_category"], "Fall Stem Bundles")
        self.assertEqual(
            item["url"],
            "https://www.michaels.com/product/11-pink-peony-cream-rose-mix-bouquet-by-ashland-10809872",
        )
        self.assertTrue(item["image_url"].startswith("https://imgs.michaels.com/"))
        self.assertEqual(item["image_count"], 3)
        self.assertEqual(item["price"], 9.99)
        self.assertIsNone(item["original_price"])
        self.assertEqual(item["currency"], "USD")
        self.assertFalse(item["on_sale"])
        self.assertEqual(item["rating"], 4.5)
        self.assertEqual(item["reviews_count"], 16)
        self.assertTrue(item["store_pickup"])
        self.assertTrue(item["same_day_delivery"])
        self.assertTrue(item["in_stock"])
        self.assertIn("Same Day Delivery", item["badges"])
        self.assertEqual(
            item["promotion_message"],
            "30% off every regular price purchase with code GETMY30",
        )
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], 3315)
        self.assertEqual(item["source_url"], PLP_URL)
        self.assertEqual(item["source"], "michaels_nextjs_rsc_initial_products")
        self.assertIsInstance(item["raw"], dict)

    def test_rsc_sentinels_are_stripped_from_raw(self):
        item = next(
            entry
            for entry in self.spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE))))
            if isinstance(entry, dict)
        )
        self.assertNotIn("$undefined", json.dumps(item["raw"]))
        self.assertIsNone(item["raw"]["originalPrice"])
        self.assertIsNone(item["raw"]["availability"]["stockCount"])
        self.assertEqual(item["raw"]["price"], 9.99)

    def test_discounted_item_maps_original_price_and_badges(self):
        item = next(
            entry
            for entry in self.spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE))))
            if isinstance(entry, dict) and entry["sku"] == "10809896"
        )
        self.assertEqual(item["price"], 14.99)
        self.assertEqual(item["original_price"], 29.99)
        self.assertTrue(item["on_sale"])
        self.assertIn("Sale", item["badges"])
        self.assertIsNone(item["promotion_message"])

    def test_page_two_yields_distinct_ids_and_no_pagination_further(self):
        outputs = list(
            self.spider.parse(
                self.listing_response(
                    rsc_document(props_from(PAGE2_FIXTURE)),
                    url=PLP_URL + "?page=2",
                    page=2,
                )
            )
        )
        items, requests = self.split(outputs)
        self.assertEqual(len(items), 4)
        self.assertEqual(requests, [])  # max_pages=2 reached
        page_one = {
            entry["sku"]
            for entry in self.spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE))))
            if isinstance(entry, dict)
        }
        self.assertEqual(page_one & {entry["sku"] for entry in items}, set())

    def test_two_pages_chain_through_the_real_follow_request(self):
        """Drive page 1 -> follow -> page 2 the way the scheduler would."""
        page_one = list(
            self.spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE))))
        )
        follow = [entry for entry in page_one if not isinstance(entry, dict)][0]
        self.assertEqual(follow.url, PLP_URL + "?page=2")

        # Replay the follow request: same meta, page-2 document as the body.
        request = Request(follow.url, meta=follow.meta)
        page_two_response = TextResponse(
            follow.url,
            request=request,
            body=rsc_document(props_from(PAGE2_FIXTURE)),
            encoding="utf-8",
        )
        page_two = list(self.spider.parse(page_two_response))

        items = [entry for entry in page_one + page_two if isinstance(entry, dict)]
        requests = [entry for entry in page_one + page_two if not isinstance(entry, dict)]
        self.assertEqual(len(items), 8)
        self.assertEqual(len({entry["item_id"] for entry in items}), 8)
        self.assertEqual([entry["page"] for entry in items[:4]], [1, 1, 1, 1])
        self.assertEqual([entry["page"] for entry in items[4:]], [2, 2, 2, 2])
        self.assertEqual([entry["position"] for entry in items[4:]], [1, 2, 3, 4])
        # max_pages=2 ends the crawl after the second window.
        self.assertEqual(len(requests), 1)

    def test_max_pages_one_stops_after_first_page(self):
        spider = MichaelsListingSpider(category="floral-arrangements", max_pages=1)
        outputs = list(spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE)))))
        _, requests = self.split(outputs)
        self.assertEqual(requests, [])

    def test_duplicate_ids_across_pages_are_dropped(self):
        # Page 1 first, so its ids are already in the spider's dedupe set.
        list(self.spider.parse(self.listing_response(rsc_document(props_from(PAGE1_FIXTURE)))))
        outputs = list(
            self.spider.parse(
                self.listing_response(
                    rsc_document(props_from(PAGE1_FIXTURE)),
                    url=PLP_URL + "?page=2",
                    page=2,
                )
            )
        )
        items, _ = self.split(outputs)
        self.assertEqual(items, [])

    def test_page_past_the_end_stops_without_error(self):
        outputs = list(
            self.spider.parse(
                self.listing_response(
                    rsc_document(props_from(PAGE1_FIXTURE, initialProducts=[], initialTotal=0)),
                    url=PLP_URL + "?page=200",
                    page=200,
                )
            )
        )
        self.assertEqual(list(outputs), [])

    def test_first_page_with_no_products_raises(self):
        with self.assertRaises(RuntimeError) as ctx:
            list(
                self.spider.parse(
                    self.listing_response(
                        rsc_document(props_from(PAGE1_FIXTURE, initialProducts=[], initialTotal=0))
                    )
                )
            )
        self.assertIn("No initialProducts", str(ctx.exception))

    # ---------------------------------------------------------------- failure

    def test_non_200_is_reported(self):
        response = self.listing_response(rsc_document(props_from(PAGE1_FIXTURE)))
        response.status = 503
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(response))
        self.assertIn("HTTP 503", str(ctx.exception))

    def test_akamai_challenge_body_is_reported(self):
        body = "<html><body>Access Denied - Reference #18.1 ref</body></html>"
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.listing_response(body)))
        self.assertIn("challenge body", str(ctx.exception))

    def test_document_without_flight_chunks_is_reported(self):
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.listing_response("<html><body>hello</body></html>")))
        self.assertIn("self.__next_f", str(ctx.exception))

    def test_payload_without_initial_products_is_reported(self):
        document = rsc_document({"initialTotal": 12, "initialFilters": []})
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse(self.listing_response(document)))
        self.assertIn("initialProducts", str(ctx.exception))

    def test_empty_sitemap_is_reported(self):
        response = TextResponse(
            MICHAELS_CATEGORY_SITEMAP_URL,
            request=Request(MICHAELS_CATEGORY_SITEMAP_URL),
            body="<?xml version='1.0'?><urlset></urlset>",
            encoding="utf-8",
        )
        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_category_sitemap(response))
        self.assertIn("No /shop/ category URLs", str(ctx.exception))

    def test_unknown_category_lists_available_slugs(self):
        spider = MichaelsListingSpider(category="not-a-real-category", max_pages=1)
        response = TextResponse(
            MICHAELS_CATEGORY_SITEMAP_URL,
            request=Request(MICHAELS_CATEGORY_SITEMAP_URL),
            body=SITEMAP_FIXTURE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError) as ctx:
            list(spider.parse_category_sitemap(response))
        message = str(ctx.exception)
        self.assertIn("not-a-real-category", message)
        self.assertIn("floral-arrangements", message)

    def test_spider_requires_a_target(self):
        with self.assertRaises(ValueError) as ctx:
            MichaelsListingSpider()
        self.assertIn("-a category=", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()