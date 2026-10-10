import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse
from scrapy.settings import Settings

from common.spiders.etsy_categories import ETSY_CATEGORIES
from common.spiders.etsy_listing_spider import CONTEXT_MARKER, EtsyListingSpider


def response(body, page=1):
    url = f"https://www.etsy.com/c/jewelry?explicit=1&page={page}&ref=pagination"
    request = Request(url, meta={
        "category": "jewelry", "category_url": "https://www.etsy.com/c/jewelry?explicit=1", "page": page,
    })
    return TextResponse(request=request, url=url, body=body, encoding="utf-8")


class EtsyListingSpiderTest(unittest.TestCase):
    def spider(self, max_pages=1):
        spider = EtsyListingSpider(category="jewelry", max_pages=max_pages)
        spider.settings = Settings({"PROXY": ""})
        return spider

    def fixture(self):
        return Path("sample/etsy_context_bootstrap_page1.html").read_text()

    def test_extracts_context_json_without_card_or_jsonld_parsing(self):
        state = self.spider()._context_state(response(self.fixture()))
        self.assertEqual(state["total_pages"], 250)
        self.assertEqual(state["organic_listings_count"], 179687)
        self.assertEqual(len(self.spider()._impression_records(state)), 2)

    def test_maps_encoded_impressions_to_feed_contract(self):
        spider = self.spider()
        rows = list(spider.parse(response(self.fixture())))
        self.assertEqual([row["item_id"] for row in rows], ["1001", "1002"])
        first = rows[0]
        self.assertEqual(first["shop_id"], "501")
        self.assertEqual(first["url"], "https://www.etsy.com/listing/1001")
        self.assertEqual(first["price"], 24.5)
        self.assertEqual(first["original_price"], 49.0)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["discount_percent"], 50)
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["total_pages"], 250)
        self.assertEqual(first["source"], "etsy_context_bootstrap")
        self.assertEqual(list(first), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_paginates_using_bootstrap_total_pages(self):
        outputs = list(self.spider(max_pages=2).parse(response(self.fixture())))
        request = next(value for value in outputs if isinstance(value, Request))
        self.assertIn("page=2", request.url)
        self.assertIn("ref=pagination", request.url)
        self.assertEqual(request.meta["page"], 2)

    def test_deduplicates_listing_ids_between_pages(self):
        spider = self.spider()
        self.assertEqual(len(list(spider.parse(response(self.fixture())))), 2)
        self.assertEqual(list(spider.parse(response(self.fixture(), page=2))), [])

    def test_malformed_bootstrap_fails_visibly(self):
        from scrapy.exceptions import CloseSpider

        body = f"<script>{CONTEXT_MARKER}{{not-json}});</script>"
        with self.assertRaises(CloseSpider):
            list(self.spider().parse(response(body)))

    def test_complete_taxonomy(self):
        departments = {entry["department"] for entry in _FLAT(ETSY_CATEGORIES)}
        top_level = [entry for entry in _FLAT(ETSY_CATEGORIES) if "/" not in entry["category"]]
        self.assertEqual(len(departments), 17)
        self.assertEqual(len(top_level), 17)
        self.assertEqual(len(_FLAT(ETSY_CATEGORIES)) - len(top_level), 175)
        self.assertEqual(len({entry["category"] for entry in _FLAT(ETSY_CATEGORIES)}), 192)


if __name__ == "__main__":
    unittest.main()


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]
