from __future__ import annotations

import json
import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.gamestop_listing_spider import (
    GamestopListingSpider,
    category_slug,
)
from common.spiders.gamestop_categories import GAMESTOP_CATEGORIES

SAMPLE_DIR = Path(__file__).resolve().parents[1] / "sample"


def make_response(
    url: str,
    body: str | bytes,
    *,
    status: int = 200,
    content_type: str = "text/html",
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


class GamestopListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = GamestopListingSpider(category="consoles-hardware", max_pages=3)
        self.grid_html = (SAMPLE_DIR / "gamestop-listing-grid.html").read_text()
        self.tiles_json = (SAMPLE_DIR / "gamestop-tile-products.json").read_text()

    # ------------------------------------------------------------ inventory

    def test_categories_are_unique_and_cover_the_inventory(self):
        names = [entry["category"] for entry in self.spider.categories]
        self.assertEqual(len(names), len(set(names)))

        expected = {url for urls in GAMESTOP_CATEGORIES.values() for url in urls}
        self.assertEqual({entry["url"] for entry in self.spider.categories}, expected)

    def test_category_slug_disambiguates_repeated_leaf_slugs(self):
        # `nintendo-switch` exists under both departments, so leaf-only slugs would
        # collide and drop a department.
        self.assertEqual(
            category_slug("https://www.gamestop.com/consoles-hardware/nintendo-switch"),
            "consoles-hardware-nintendo-switch",
        )
        self.assertEqual(
            category_slug("https://www.gamestop.com/video-games/nintendo-switch"),
            "video-games-nintendo-switch",
        )

    def test_category_slug_normalizes_encoded_characters(self):
        self.assertEqual(
            category_slug(
                "https://www.gamestop.com/consoles-hardware/xbox-series-x%7Cs"
            ),
            "consoles-hardware-xbox-series-x-s",
        )

    # ------------------------------------------------------- grid extraction

    def test_parse_grid_extracts_pids_and_schedules_tile_request(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            f'<div id="product-grid-wrapper" data-cnstrc-num-results="821">'
            f"{self.grid_html}</div>",
            meta={"page": 1, "category_url": url, "cgid": None},
        )

        requests = list(self.spider.parse_grid(response))

        self.assertTrue(requests)
        first = requests[0]
        self.assertIn("Tile-GetProductsJSON", first.url)
        # The storefront controller reads `data`/`pid`; `pids=` returns an empty
        # productsJSON.
        self.assertIn("data=229049", first.url)
        self.assertNotIn("pids=", first.url)
        self.assertEqual(first.meta["allow_next_page"], True)

    def test_parse_grid_chunks_pids_at_tile_batch_size(self):
        pids = "".join(f'<div data-pid="{i}"></div>' for i in range(1, 46))
        response = make_response(
            "https://www.gamestop.com/consoles-hardware",
            pids,
            meta={"page": 1, "category_url": "https://www.gamestop.com/consoles-hardware", "cgid": None},
        )

        requests = list(self.spider.parse_grid(response))

        # 45 pids at 20 per batch -> 3 requests, and only the first may paginate.
        self.assertEqual(len(requests), 3)
        self.assertEqual(
            [r.meta["allow_next_page"] for r in requests], [True, False, False]
        )

    def test_parse_grid_without_tiles_raises(self):
        response = make_response(
            "https://www.gamestop.com/does-not-exist",
            '<div id="product-grid-wrapper" data-cnstrc-num-results="0"></div>',
            meta={"page": 1, "category_url": "https://www.gamestop.com/does-not-exist", "cgid": None},
        )

        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_grid(response))
        self.assertIn("no [data-pid] tiles", str(ctx.exception))

    def test_total_results_read_from_grid_attribute(self):
        response = make_response(
            "https://www.gamestop.com/consoles-hardware",
            '<div data-cnstrc-num-results="821"></div>',
        )
        self.assertEqual(GamestopListingSpider._total_results(response), 821)

    def test_cgid_is_read_from_the_pages_own_grid_link(self):
        # The friendly slug is not the cgid, and the mapping is not derivable
        # offline, so it must come from the rendered page.
        html = (
            '<a href="/on/demandware.store/Sites-gamestop-us-Site/default/'
            'Search-UpdateGrid?cgid=toys-and-collectibles-funko&amp;start=0&amp;sz=20"></a>'
        )
        response = make_response(
            "https://www.gamestop.com/collectibles/funko", html
        )
        self.assertEqual(
            GamestopListingSpider._cgid_from(response), "toys-and-collectibles-funko"
        )

    # ------------------------------------------------------ tile JSON parsing

    def test_parse_tiles_emits_normalized_items_from_real_payload(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            self.tiles_json,
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["106429"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        results = list(self.spider.parse_tiles(response))
        items = [r for r in results if isinstance(r, dict)]

        self.assertEqual(len(items), 20)
        # 20 items plus a single page-2 grid request.
        self.assertEqual(len(results), 21)
        first = items[0]
        self.assertEqual(first["item_id"], "106429")
        self.assertEqual(
            first["title"],
            "Nintendo Wii Original Console with Wii Remote - Super Mario Bros. "
            "25th Anniversary Edition Red",
        )
        self.assertTrue(first["url"].startswith("https://www.gamestop.com/"))
        self.assertTrue(first["image_url"].startswith("https://media.gamestop.com/"))
        self.assertEqual(first["availability"], "InStock")
        self.assertEqual(first["badge"], "BUY CONSOLE, SAVE 10% PO ACC.")
        self.assertEqual(first["rating"], "83.85")
        self.assertEqual(first["reviews_count"], "654")
        self.assertEqual(first["category"], "consoles-hardware")
        self.assertEqual(first["department"], "consoles-hardware")
        self.assertEqual(first["source"], "gamestop_tile_json")
        self.assertEqual(first["currency"], "USD")
        # `raw` is required on every exported item.
        self.assertEqual(first["raw"]["id"], "106429")

    def test_sale_price_wins_and_base_is_kept_separately(self):
        url = "https://www.gamestop.com/consoles-hardware"
        payload = {
            "action": "Tile-GetProductsJSON",
            "productsJSON": {
                "119149": {
                    "id": "119149",
                    "name": "Xbox One",
                    "url": "/x/119149.html",
                    "price": {"base": "109.99", "sale": "89.99", "pro": None},
                    "availability": {"available": True},
                    "ratings": {"percentage": "74.71", "count": "3662"},
                    "image": {"base": "https://media.gamestop.com/i/gamestop/10129112?"},
                }
            },
        }
        response = make_response(
            url,
            json.dumps(payload),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["119149"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        item = list(self.spider.parse_tiles(response))[0]

        self.assertEqual(item["price"], "89.99")
        self.assertEqual(item["list_price"], "109.99")
        self.assertIsNone(item["pro_price"])

    def test_base_price_used_when_no_sale_price(self):
        url = "https://www.gamestop.com/consoles-hardware"
        payload = {
            "productsJSON": {
                "1": {
                    "id": "1",
                    "name": "Plain",
                    "url": "/p/1.html",
                    "price": {"base": "10.00", "sale": None, "pro": None},
                    "availability": {"available": True},
                }
            }
        }
        response = make_response(
            url,
            json.dumps(payload),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "total": 1,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        item = list(self.spider.parse_tiles(response))[0]
        self.assertEqual(item["price"], "10.00")

    def test_empty_products_json_is_skipped_without_crashing(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            json.dumps({"action": "Tile-GetProductsJSON", "productsJSON": {}}),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["9", "8"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        self.assertEqual(list(self.spider.parse_tiles(response)), [])

    def test_missing_products_json_key_raises(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            json.dumps({"action": "Tile-GetProductsJSON"}),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "total": 1,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_tiles(response))
        self.assertIn("productsJSON", str(ctx.exception))

    def test_tile_entry_without_id_raises(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            json.dumps({"productsJSON": {"k": {"name": "no id"}}}),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["k"],
                "total": 1,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        with self.assertRaises(RuntimeError):
            list(self.spider.parse_tiles(response))

    # ----------------------------------------------------------- pagination

    def test_pagination_continues_until_total_is_reached(self):
        url = "https://www.gamestop.com/consoles-hardware"
        payload = {
            "productsJSON": {
                "1": {
                    "id": "1",
                    "name": "A",
                    "url": "/a/1.html",
                    "price": {"base": "1.00"},
                    "availability": {"available": True},
                }
            }
        }
        response = make_response(
            url,
            json.dumps(payload),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        results = list(self.spider.parse_tiles(response))

        self.assertEqual(len(results), 2)  # one item, one next-page request
        next_request = results[1]
        self.assertIn("Search-UpdateGrid", next_request.url)
        self.assertIn("cgid=consoles", next_request.url)
        self.assertEqual(next_request.meta["page"], 2)
        # Offset must follow the pid count actually served, not page * PAGE_SIZE:
        # the friendly category URL renders the storefront default of 20 tiles.
        self.assertIn("start=1", next_request.url)

    def test_pagination_stops_when_start_reaches_total(self):
        url = "https://www.gamestop.com/consoles-hardware"
        page_size = GamestopListingSpider.PAGE_SIZE
        payload = {
            "productsJSON": {
                "1": {
                    "id": "1",
                    "name": "A",
                    "url": "/a/1.html",
                    "price": {"base": "1.00"},
                    "availability": {"available": True},
                }
            }
        }
        response = make_response(
            url,
            json.dumps(payload),
            content_type="application/json",
            meta={
                # Already on the last page: start (60) >= total (60).
                "page": 2,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "grid_start": page_size - 1,
                "grid_size": 1,
                "total": page_size,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        results = list(self.spider.parse_tiles(response))
        self.assertEqual(len(results), 1)

    def test_pagination_offset_accumulates_across_batches(self):
        """A grid bigger than TILE_BATCH_SIZE must not re-request the same offset."""
        url = "https://www.gamestop.com/consoles-hardware"
        pids = [str(i) for i in range(1, 26)]
        products = {
            pid: {
                "id": pid,
                "name": f"P{pid}",
                "url": f"/p/{pid}.html",
                "price": {"base": "1.00"},
                "availability": {"available": True},
            }
            for pid in pids
        }
        response = make_response(
            url,
            json.dumps({"productsJSON": products}),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": pids,
                "grid_start": 0,
                "grid_size": 25,
                "total": 818,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        results = list(self.spider.parse_tiles(response))
        items = [r for r in results if isinstance(r, dict)]
        next_request = [r for r in results if not isinstance(r, dict)]

        self.assertEqual(len(items), 25)
        self.assertEqual(len(next_request), 1)
        self.assertIn("start=25", next_request[0].url)

    def test_next_offset_skips_past_the_whole_grid_not_just_the_batch(self):
        """Regression: a 60-pid grid sent as 3 batches must advance by 60.

        Advancing by the batch length re-requested the middle of the grid and
        produced 40 duplicate items instead of new ones.
        """
        url = "https://www.gamestop.com/consoles-hardware"
        products = {
            pid: {
                "id": pid,
                "name": f"P{pid}",
                "url": f"/p/{pid}.html",
                "price": {"base": "1.00"},
                "availability": {"available": True},
            }
            for pid in ("5", "6")
        }
        response = make_response(
            url,
            json.dumps({"productsJSON": products}),
            content_type="application/json",
            meta={
                "page": 2,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["5", "6"],
                "grid_start": 20,
                "grid_size": 60,
                "total": 818,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        results = list(self.spider.parse_tiles(response))
        next_request = [r for r in results if not isinstance(r, dict)][0]

        self.assertIn("start=80", next_request.url)

    def test_pagination_stops_at_max_pages(self):
        spider = GamestopListingSpider(category="consoles-hardware", max_pages=1)
        url = "https://www.gamestop.com/consoles-hardware"
        payload = {
            "productsJSON": {
                "1": {
                    "id": "1",
                    "name": "A",
                    "url": "/a/1.html",
                    "price": {"base": "1.00"},
                    "availability": {"available": True},
                }
            }
        }
        response = make_response(
            url,
            json.dumps(payload),
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        self.assertEqual(len(list(spider.parse_tiles(response))), 1)

    def test_duplicate_ids_across_pages_are_dropped(self):
        url = "https://www.gamestop.com/consoles-hardware"
        payload = {
            "productsJSON": {
                "1": {
                    "id": "1",
                    "name": "A",
                    "url": "/a/1.html",
                    "price": {"base": "1.00"},
                    "availability": {"available": True},
                }
            }
        }
        response = make_response(
            url,
            json.dumps(payload),
            content_type="application/json",
            meta={
                "page": 2,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        # First call emits the item, second call must not repeat it.
        list(self.spider.parse_tiles(response))
        second_pass = list(self.spider.parse_tiles(response))

        self.assertEqual(second_pass, [])

    # ------------------------------------------------------- challenge/guard

    def test_access_denied_body_raises(self):
        response = make_response(
            "https://www.gamestop.com/consoles-hardware",
            "<html><body>Access Denied</body></html>",
            meta={"page": 1, "category_url": "https://www.gamestop.com/consoles-hardware"},
        )

        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_grid(response))
        self.assertIn("challenge", str(ctx.exception))

    def test_non_200_raises(self):
        response = make_response(
            "https://www.gamestop.com/consoles-hardware",
            "<html></html>",
            status=503,
            meta={"page": 1, "category_url": "https://www.gamestop.com/consoles-hardware"},
        )

        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_grid(response))
        self.assertIn("HTTP 503", str(ctx.exception))

    def test_non_json_tile_body_raises(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            "<html><body>not json</body></html>",
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["1"],
                "total": 1,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        with self.assertRaises(RuntimeError) as ctx:
            list(self.spider.parse_tiles(response))
        self.assertIn("non-JSON", str(ctx.exception))

    def test_category_arg_resolution(self):
        spider = GamestopListingSpider(category="collectibles-funko")
        self.assertEqual(
            spider.resolve_target_url(), "https://www.gamestop.com/collectibles/funko"
        )

    def test_every_exported_field_has_a_key_on_produced_items(self):
        url = "https://www.gamestop.com/consoles-hardware"
        response = make_response(
            url,
            self.tiles_json,
            content_type="application/json",
            meta={
                "page": 1,
                "category_url": url,
                "cgid": "consoles",
                "pids": ["106429"],
                "total": 821,
                "allow_next_page": True,
                "category": "consoles-hardware",
            },
        )

        item = list(self.spider.parse_tiles(response))[0]
        for field in GamestopListingSpider.custom_settings["FEED_EXPORT_FIELDS"]:
            self.assertIn(field, item, f"missing FEED_EXPORT_FIELDS key: {field}")


if __name__ == "__main__":
    unittest.main()