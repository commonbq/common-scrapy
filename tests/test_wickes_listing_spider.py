from __future__ import annotations

import unittest

from scrapy.http import Request, TextResponse

from common.spiders.wickes_categories import WICKES_CATEGORIES
from common.spiders.wickes_listing_spider import WickesListingSpider


BOOTSTRAP = r'''
<script>
var impressionsEvent = {ecommerce: {currencyCode: "GBP", impressions: []}};
var list = "Product Listing Page";
var product = {
  name: "Dulux Matt Emulsion Paint - Egyptian Cotton - 2.5L",
  id: "106974",
  price: "25",
  brand: "Dulux",
  category: "Painting & Decorating\/Interior Paint\/Dulux",
  variant: "not classified"
}
var currentPosition = impressionsEvent.ecommerce.impressions.length;
impressionsEvent.ecommerce.impressions.push($.extend({list: list}, product));
var product = {
  name: "Wickes Collector\'s Matt Emulsion Paint - Subtle Sage NO.806 - 2.5L",
  id: "300591", price: "14.50", brand: "Wickes",
  category: "Painting & Decorating\/Interior Paint\/Wall & Ceiling Emulsion Paint",
  variant: "not classified"
}
var currentPosition = impressionsEvent.ecommerce.impressions.length;
</script>
'''


class WickesListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = WickesListingSpider(category="wall-ceiling-emulsion-paint", max_pages=2)

    def response(self, page=1, body=BOOTSTRAP):
        url = self.spider._target_url if page == 1 else self.spider._results_url(page - 1)
        request = Request(url, meta={"page": page})
        return TextResponse(url, request=request, body=body, encoding="utf-8")

    def test_top_twenty_category_inventory(self):
        self.assertEqual(len(WICKES_CATEGORIES), 20)
        self.assertEqual(len({entry["category"] for entry in WICKES_CATEGORIES}), 20)
        self.assertTrue(all("/c/" in entry["url"] for entry in WICKES_CATEGORIES))

    def test_extracts_only_analytics_bootstrap_records(self):
        records = self.spider.extract_bootstrap_products(BOOTSTRAP)
        self.assertEqual([record["id"] for record in records], ["106974", "300591"])
        self.assertEqual(records[0]["category"], "Painting & Decorating/Interior Paint/Dulux")
        self.assertIn("Collector's", records[1]["name"])

    def test_items_follow_feed_contract_and_schedule_load_more(self):
        output = list(self.spider.parse(self.response()))
        items = [entry for entry in output if isinstance(entry, dict)]
        requests = [entry for entry in output if isinstance(entry, Request)]
        self.assertEqual(len(items), 2)
        self.assertEqual(list(items[0]), self.spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(items[0]["url"], "https://www.wickes.co.uk/p/106974")
        self.assertEqual(items[0]["price"], 25)
        self.assertEqual(items[1]["price"], 14.5)
        self.assertEqual(items[0]["source"], "wickes_analytics_bootstrap")
        self.assertEqual(len(requests), 1)
        self.assertEqual(
            requests[0].url,
            "https://www.wickes.co.uk/c/1001115/results/view?q=%3Arelevance&page=1&sort=relevance",
        )

    def test_empty_first_page_fails_but_empty_later_page_stops(self):
        with self.assertRaisesRegex(RuntimeError, "no analytics product bootstrap"):
            list(self.spider.parse(self.response(body="<html></html>")))
        self.assertEqual(list(self.spider.parse(self.response(page=2, body=""))), [])

    def test_duplicate_ids_are_not_emitted_again(self):
        first = list(self.spider.parse(self.response()))
        self.assertEqual(len([entry for entry in first if isinstance(entry, dict)]), 2)
        second = list(self.spider.parse(self.response(page=2)))
        self.assertEqual(second, [])

    def test_challenge_and_bad_status_fail_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "challenge/proxy"):
            list(self.spider.parse(self.response(body="<html>Access Denied</html>")))
        request = Request(self.spider._target_url, meta={"page": 1})
        response = TextResponse(
            self.spider._target_url, request=request, body=b"nope", status=503, encoding="utf-8"
        )
        with self.assertRaisesRegex(RuntimeError, "HTTP 503"):
            list(self.spider.parse(response))


if __name__ == "__main__":
    unittest.main()
