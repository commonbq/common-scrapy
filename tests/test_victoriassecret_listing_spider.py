from __future__ import annotations

import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.victoriassecret_categories import VICTORIASSECRET_CATEGORIES
from common.spiders.victoriassecret_listing_spider import (
    VictoriassecretListingSpider,
    load_categories,
    parse_money,
    slugify,
)

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample"


def make_response(
    url: str,
    body: str | bytes,
    *,
    status: int = 200,
    content_type: str = "application/json",
    meta: dict | None = None,
) -> TextResponse:
    if isinstance(body, str):
        body = body.encode("utf-8")
    request = Request(url, meta=meta or {})
    return TextResponse(
        url,
        request=request,
        body=body,
        encoding="utf-8",
        status=status,
        headers={"Content-Type": content_type},
    )


class VictoriassecretListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = VictoriassecretListingSpider(category="vs-bras", max_pages=3)
        self.ssr_html = (SAMPLE_DIR / "victoriassecret-vs-bras-ssr.html").read_text()
        self.initial_json = (SAMPLE_DIR / "victoriassecret-stacks-initial.json").read_text()
        self.paginated_json = (SAMPLE_DIR / "victoriassecret-stacks-paginated.json").read_text()

    # ------------------------------------------------------------ taxonomy

    def test_categories_are_unique_and_urls_are_absolute(self):
        names = [entry["category"] for entry in self.spider.categories]
        self.assertEqual(len(names), len(set(names)))
        for entry in self.spider.categories:
            self.assertTrue(entry["url"].startswith("https://www.victoriassecret.com"))

    def test_both_brands_are_represented(self):
        brands = {entry["brand"] for entry in self.spider.categories}
        self.assertEqual(brands, {"vs", "pink"})

    def test_taxonomy_matches_the_source_tree(self):
        # Every reachable top-level path should yield a crawl target.
        tops = {
            f"{brand}-{slugify(name)}"
            for brand, data in VICTORIASSECRET_CATEGORIES.items()
            for name, node in data.items()
            if node.get("path")
        }
        slugs = {entry["category"] for entry in self.spider.categories}
        self.assertTrue(tops.issubset(slugs))

    def test_header_rows_without_path_are_skipped(self):
        # "Pink Color" is a heading row with a placeholder path and must not be a
        # crawl target on its own (its one real child survives).
        slugs = {entry["category"] for entry in load_categories()}
        self.assertNotIn("vs-pink-color", slugs)

    def test_sub_category_labels_are_attached(self):
        push_up = [e for e in self.spider.categories if e["category"] == "vs-bras-push-up"]
        self.assertEqual(len(push_up), 1)
        self.assertEqual(push_up[0]["sub_category"], "Push-Up")
        self.assertEqual(push_up[0]["top_category"], "BRAS")

    # ------------------------------------------------------- helpers

    def test_slugify_normalizes_punctuation(self):
        self.assertEqual(slugify("ALL BRAS: A-F CUPS"), "all-bras-a-f-cups")
        self.assertEqual(slugify("NEW!"), "new")

    def test_parse_money(self):
        self.assertEqual(parse_money("$49.95"), 49.95)
        self.assertEqual(parse_money(59.95), 59.95)
        self.assertIsNone(parse_money(""))
        self.assertIsNone(parse_money(None))

    # ------------------------------------------------- SSR -> collection id

    def test_parse_category_page_extracts_collection_id_and_schedules_api(self):
        response = make_response(
            "https://www.victoriassecret.com/us/vs/bras",
            self.ssr_html,
            content_type="text/html",
            meta={"category": {"category": "vs-bras", "brand": "vs", "top_category": "BRAS",
                               "url": "https://www.victoriassecret.com/us/vs/bras"}},
        )
        requests = list(self.spider.parse_category_page(response))
        self.assertEqual(len(requests), 1)
        api_request = requests[0]
        self.assertIsInstance(api_request, Request)
        # Page 0 must hit the trailing-slash URL; without it the gateway 404s.
        self.assertIn("/stacks/v46/?", api_request.url)
        self.assertIn("collectionId=e88ab444-c093-4a29-a7c9-ef78f2a3e557", api_request.url)
        self.assertIn("brand=vs", api_request.url)
        self.assertEqual(api_request.meta["offset"], 0)

    # --------------------------------------------------- API -> items

    def test_parse_initial_response_emits_items_and_paginates(self):
        response = make_response(
            "https://api.victoriassecret.com/stacks/v46/?collectionId=x",
            self.initial_json,
            meta={"category": {"category": "vs-bras", "brand": "vs", "top_category": "BRAS",
                               "url": "https://www.victoriassecret.com/us/vs/bras"},
                  "collection_id": "e88ab444-c093-4a29-a7c9-ef78f2a3e557",
                  "brand": "vs", "is_bras_or_panties": True, "offset": 0, "total": None},
        )
        results = list(self.spider.parse_api_response(response))
        items = [r for r in results if isinstance(r, dict)]
        requests = [r for r in results if isinstance(r, Request)]
        self.assertEqual(len(items), 2)
        self.assertEqual(len(requests), 1)

        first = items[0]
        self.assertEqual(first["item_id"], "11295563|7I65")
        self.assertEqual(first["price"], 49.95)
        self.assertEqual(first["brand"], "vs")
        self.assertEqual(first["top_category"], "BRAS")
        self.assertIn("raw", first)
        self.assertTrue(first["image_url"].startswith("https://www.victoriassecret.com/p/380x507/"))

        # Total came from the page-0 envelope; the next offset advances by what
        # was actually served (2 in this trimmed fixture), not by PAGE_SIZE.
        self.assertIn("/stacks/v46/stack?", requests[0].url)
        self.assertEqual(requests[0].meta["offset"], 2)
        self.assertEqual(requests[0].meta["total"], 475)

    def test_parse_paginated_response_reads_top_level_product_list(self):
        response = make_response(
            "https://api.victoriassecret.com/stacks/v46/stack?offset=96",
            self.paginated_json,
            meta={"category": {"category": "vs-bras", "brand": "vs", "top_category": "BRAS",
                               "url": "https://www.victoriassecret.com/us/vs/bras"},
                  "collection_id": "e88ab444-c093-4a29-a7c9-ef78f2a3e557",
                  "brand": "vs", "is_bras_or_panties": True, "offset": 96, "total": 475},
        )
        items = [r for r in self.spider.parse_api_response(response) if isinstance(r, dict)]
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["page"], 2)

    def test_last_page_stops_pagination(self):
        # total == offset + len(products) -> no further request.
        response = make_response(
            "https://api.victoriassecret.com/stacks/v46/stack?offset=96",
            self.paginated_json,
            meta={"category": {"category": "vs-bras", "brand": "vs", "top_category": "BRAS",
                               "url": "https://www.victoriassecret.com/us/vs/bras"},
                  "collection_id": "x", "brand": "vs", "is_bras_or_panties": True,
                  "offset": 96, "total": 98},
        )
        self.assertEqual(
            [r for r in self.spider.parse_api_response(response) if isinstance(r, Request)],
            [],
        )

    def test_duplicate_ids_are_dropped(self):
        response = make_response(
            "https://api.victoriassecret.com/stacks/v46/stack?offset=96",
            self.paginated_json,
            meta={"category": {"category": "vs-bras", "brand": "vs", "top_category": "BRAS",
                               "url": "https://www.victoriassecret.com/us/vs/bras"},
                  "collection_id": "x", "brand": "vs", "is_bras_or_panties": True,
                  "offset": 96, "total": 475},
        )
        first = [r for r in self.spider.parse_api_response(response) if isinstance(r, dict)]
        second = [r for r in self.spider.parse_api_response(response) if isinstance(r, dict)]
        self.assertEqual(len(first), 2)
        self.assertEqual(second, [])

    def test_non_json_response_is_ignored(self):
        response = make_response(
            "https://api.victoriassecret.com/stacks/v46/", "404 page not found",
            status=200,
            meta={"category": {"category": "vs-bras", "brand": "vs", "top_category": "BRAS",
                               "url": "x"}, "offset": 0, "total": None},
        )
        self.assertEqual(list(self.spider.parse_api_response(response)), [])


if __name__ == "__main__":
    unittest.main()
