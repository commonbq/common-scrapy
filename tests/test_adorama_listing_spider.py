from pathlib import Path
import json
import re
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.adorama_categories import (
    ADORAMA_CATEGORIES,
    ADORAMA_CATEGORY_INVENTORY,
    ADORAMA_PAGE_SIZE,
)
from common.spiders.adorama_listing_spider import AdoramaListingSpider


CATEGORY = "audio-audio-bags-and-cases-microphone-cases"
LISTING_URL = "https://www.adorama.com/l/Audio/Audio-Bags-and-Cases/Microphone-Cases"


class AdoramaListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = AdoramaListingSpider(category=CATEGORY, max_pages=2)
        self.sample = Path("sample/adorama-listing-sample.html").read_text(encoding="utf-8")

    def response(self, body=None, *, status=200, page=1, listing_url=LISTING_URL):
        url = AdoramaListingSpider._page_url(listing_url, page)
        meta = {
            "category": "Microphone Cases",
            "subcategory": "Audio Bags and Cases",
            "department": "Audio",
            "page": page,
            "listing_url": listing_url,
        }
        return TextResponse(
            url, request=Request(url, meta=meta), body=body or self.sample,
            encoding="utf-8", status=status,
        )

    def state(self):
        props = AdoramaListingSpider._page_props(
            AdoramaListingSpider._extract_hydration(self.sample)
        )
        return json.loads(json.dumps(props))

    def body_with(self, props):
        state = {"props": {"pageProps": props}}
        return (
            '<html><script id="__NEXT_DATA__" type="application/json">'
            + json.dumps(state) + "</script></html>"
        )

    # --- inventory -----------------------------------------------------

    def test_inventory_covers_every_crawlable_category(self):
        self.assertEqual(len(ADORAMA_CATEGORY_INVENTORY), 11)
        self.assertEqual(len(ADORAMA_CATEGORIES), 1079)
        # 1090 sitemap URLs minus the 11 depth-1 CMS landing pages.
        self.assertEqual(len(ADORAMA_CATEGORIES), 1090 - 11)
        self.assertEqual(len({c["category"] for c in ADORAMA_CATEGORIES}), 1079)
        self.assertEqual(len({c["url"] for c in ADORAMA_CATEGORIES}), 1079)
        self.assertTrue(all(c["depth"] >= 2 for c in ADORAMA_CATEGORIES))
        self.assertTrue(all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", c["category"])
                            for c in ADORAMA_CATEGORIES))
        # Adorama reuses labels across branches, so path-keyed slugs must not collide.
        self.assertEqual(len([c for c in ADORAMA_CATEGORIES if c["label"] == "Microphone Cases"]), 2)

    def test_documented_category_resolves(self):
        self.assertEqual(self.spider.resolve_target_url(), LISTING_URL)
        cameras = AdoramaListingSpider(category="photography-cameras", max_pages=1)
        self.assertEqual(cameras.resolve_target_url(), "https://www.adorama.com/l/Photography/Cameras")

    def test_direct_url_and_category_url_are_accepted(self):
        for arg in ("url", "category_url"):
            with self.subTest(arg=arg):
                spider = AdoramaListingSpider(**{arg: LISTING_URL}, max_pages=1)
                self.assertEqual(spider.resolve_target_url(), LISTING_URL)
        with self.assertRaisesRegex(ValueError, "Provide -a category"):
            AdoramaListingSpider(max_pages=1)
        with self.assertRaisesRegex(ValueError, "Unknown category"):
            AdoramaListingSpider(category="not-a-department", max_pages=1)

    # --- hydration mapping ----------------------------------------------

    def test_hydration_mapping_and_feed_contract(self):
        outputs = list(self.spider.parse(self.response()))
        self.assertEqual(len(outputs), 24 + 1)  # 24 items + the page-2 request
        item = outputs[0]
        self.assertEqual(list(item), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(item["item_id"], "GCGWPTRODEC4")
        self.assertEqual(item["sku"], "GCGWPTRODEC4")
        self.assertEqual(item["title"],
                         "Gator Cases Titan Case for Rodecaster Pro, 4 Mics and 4 Headsets")
        self.assertEqual(item["brand"], "Gator Cases")
        self.assertEqual(item["manufacturer"], "GWP-TITANRODECASTER4")
        self.assertEqual(item["price"], 539.99)
        self.assertEqual(item["original_price"], 863.99)
        self.assertEqual(item["currency"], "USD")
        self.assertEqual(item["savings"], 324)
        self.assertEqual(item["url"], "https://www.adorama.com/gator-cases-titan-rodecaster-pro-4-mics-4-headsets/p/gcgwptrodec4")
        self.assertEqual(item["image"], "https://www.adorama.com/images/product/GCGWPTRODEC4.jpg")
        self.assertTrue(item["in_stock"])
        self.assertEqual(item["stock_status"], "In Stock")
        self.assertEqual(item["condition"], "new")
        self.assertEqual(item["badge"], "38% Off")
        self.assertEqual(item["shipping"], "FREE 2-Day Shipping")
        self.assertEqual(item["category"], "Microphone Cases")
        self.assertEqual(item["subcategory"], "Audio Bags and Cases")
        self.assertEqual(item["department"], "Audio")
        self.assertEqual(item["page"], 1)
        self.assertEqual(item["position"], 1)
        self.assertEqual(item["total_count"], 129)
        self.assertEqual(item["source"], "adorama_next_data_products")
        self.assertEqual(item["raw"]["sku"], "GCGWPTRODEC4")

    def test_condition_and_stock_flags(self):
        props = self.state()
        product = props["products"][1]
        product["flags"].update({"isUsed": True, "isAvailableForPurchase": False})
        product["stock"] = "Out"
        product["subStatus"] = {"name": "Backordered"}
        item = list(self.spider.parse(self.response(self.body_with(props))))[1]
        self.assertEqual(item["condition"], "used")
        self.assertFalse(item["in_stock"])
        self.assertEqual(item["stock_status"], "Backordered")

    def test_badge_falls_back_to_persuasion_message(self):
        props = self.state()
        props["products"][0].pop("badgeText")
        item = list(self.spider.parse(self.response(self.body_with(props))))[0]
        self.assertEqual(item["badge"], "Limited Quantity Available \u2013 Buy Now")

    # --- pagination ------------------------------------------------------

    def test_pagination_follows_next_page_url_and_dedupes(self):
        outputs = list(self.spider.parse(self.response()))
        follow = outputs[-1]
        self.assertTrue(hasattr(follow, "url"))
        self.assertEqual(follow.url, f"{LISTING_URL}?startAt=24")
        self.assertEqual(follow.cb_kwargs["page"], 2)

        # Replaying page 1 must not emit anything new and must not loop.
        self.assertEqual([o for o in outputs if hasattr(o, "url")], [follow])
        self.assertEqual(list(self.spider.parse(self.response(page=2))), [])

    def test_max_pages_caps_pagination(self):
        spider = AdoramaListingSpider(category=CATEGORY, max_pages=1)
        outputs = list(spider.parse(self.response()))
        self.assertTrue(all(not hasattr(o, "url") for o in outputs))

    def test_pagination_stops_without_next_page_url(self):
        props = self.state()
        props["nextPageUrl"] = None
        outputs = list(self.spider.parse(self.response(self.body_with(props))))
        self.assertEqual(len(outputs), 24)
        self.assertTrue(all(not hasattr(o, "url") for o in outputs))

    def test_empty_products_stops_pagination(self):
        props = self.state()
        props["products"] = []
        self.assertEqual(list(self.spider.parse(self.response(self.body_with(props)))), [])

    def test_page_url_builder(self):
        self.assertEqual(AdoramaListingSpider._page_url(LISTING_URL, 1), LISTING_URL)
        self.assertEqual(AdoramaListingSpider._page_url(LISTING_URL, 2), f"{LISTING_URL}?startAt=24")
        self.assertEqual(AdoramaListingSpider._page_url(LISTING_URL, 3), f"{LISTING_URL}?startAt=48")
        # Existing refinements survive the pagination hand-off.
        refined = f"{LISTING_URL}?sel=Filter-By_BRAND-Sony"
        self.assertEqual(
            AdoramaListingSpider._page_url(refined, 2),
            f"{refined}&startAt=24",
        )

    # --- failure modes ---------------------------------------------------

    def test_non_200_fails_with_proxy_guidance(self):
        with self.assertRaisesRegex(RuntimeError, "HTTP 403.*DataDome"):
            list(self.spider.parse(self.response("<html></html>", status=403)))

    def test_missing_or_malformed_hydration_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "no <script id="):
            list(self.spider.parse(self.response("<html><body>no state</body></html>")))
        broken = '<html><script id="__NEXT_DATA__" type="application/json">{"props":</script></html>'
        with self.assertRaisesRegex(RuntimeError, "not valid JSON"):
            list(self.spider.parse(self.response(broken)))
        with self.assertRaisesRegex(RuntimeError, "no props.pageProps"):
            list(self.spider.parse(self.response(
                '<html><script id="__NEXT_DATA__" type="application/json">{"props":{}}</script></html>')))

    def test_schema_drift_fails_visibly(self):
        props = self.state()
        props.pop("products")
        with self.assertRaisesRegex(RuntimeError, "no props.pageProps.products list"):
            list(self.spider.parse(self.response(self.body_with(props))))

    def test_department_landing_page_is_rejected(self):
        props = self.state()
        props["pageInfo"]["pageType"] = "bcmsSitePage"
        with self.assertRaisesRegex(RuntimeError, "pageType='bcmsSitePage'"):
            list(self.spider.parse(self.response(self.body_with(props))))

    def test_hydration_extraction_ignores_other_inline_scripts(self):
        """A greedy regex over <script> blocks would splice these into the payload."""
        injected = (
            "<script>window.__OTHER__ = {\"products\": [{\"sku\": \"SPOOF\"}]};</script>"
            '<script id="__NEXT_DATA__" type="application/json">'
            + json.dumps({"props": {"pageProps": {"products": [{"sku": "REAL"}]}}})
            + "</script>"
            '<script>window.__TRAILING__ = "products";</script>'
        )
        outputs = list(self.spider.parse(self.response(injected)))
        self.assertEqual([o["item_id"] for o in outputs], ["REAL"])

    def test_page_size_constant_matches_hydration_contract(self):
        self.assertEqual(ADORAMA_PAGE_SIZE, 24)
        props = self.state()
        self.assertEqual(props["defaultPerPage"], ADORAMA_PAGE_SIZE)
        self.assertEqual(len(props["products"]), ADORAMA_PAGE_SIZE)
        self.assertEqual(props["nextPageUrl"], f"/l/Audio/Audio-Bags-and-Cases/Microphone-Cases?startAt=24")


if __name__ == "__main__":
    unittest.main()