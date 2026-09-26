from __future__ import annotations

import unittest
from pathlib import Path

from scrapy.http import Request, TextResponse

from common.spiders.bloomingdales_listing_spider import (
    BLOOMINGDALES_CATEGORIES,
    BloomingdalesListingSpider,
)


class BloomingdalesListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = BloomingdalesListingSpider(category="women", max_pages=2)
        self.sample_dir = Path(__file__).resolve().parents[1] / "sample"

    def _fixture(self, name: str) -> str:
        return (self.sample_dir / name).read_text(encoding="utf-8")

    def _response(self, url: str, body: str, *, page: int = 1, resolved_leaf: bool = False):
        request = Request(
            url,
            meta={
                "page": page,
                "resolved_leaf": resolved_leaf,
                "seed_category_url": BLOOMINGDALES_CATEGORIES["women"],
            },
        )
        return TextResponse(
            url=url,
            request=request,
            body=body.encode("utf-8"),
            encoding="utf-8",
            status=200,
        )

    def test_full_stable_seed_categories_are_exposed(self):
        expected = sorted(BLOOMINGDALES_CATEGORIES)
        self.assertEqual(self.spider.available_categories(), expected)
        for category, url in BLOOMINGDALES_CATEGORIES.items():
            self.assertEqual(
                BloomingdalesListingSpider(category=category).resolve_target_url(),
                url,
            )

    def test_splash_response_redirects_to_leaf_browse_page(self):
        response = self._response(
            BLOOMINGDALES_CATEGORIES["women"],
            self._fixture("bloomingdales-women-splash.html"),
        )

        outputs = list(self.spider.parse(response))

        self.assertEqual(len(outputs), 1)
        follow = outputs[0]
        self.assertIsInstance(follow, Request)
        self.assertEqual(
            follow.url,
            "https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683",
        )
        self.assertEqual(follow.meta["page"], 1)
        self.assertTrue(follow.meta["resolved_leaf"])

    def test_leaf_contract_parsing_extracts_fields_and_paginates(self):
        response = self._response(
            "https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683",
            self._fixture("bloomingdales-dresses-leaf-page1.html"),
            resolved_leaf=True,
        )

        outputs = list(self.spider.parse(response))
        products = [obj for obj in outputs if isinstance(obj, dict)]
        next_requests = [obj for obj in outputs if isinstance(obj, Request)]

        self.assertEqual(len(products), 2)
        self.assertEqual(len(next_requests), 1)

        first = products[0]
        self.assertEqual(first["item_id"], "111111")
        self.assertEqual(first["title"], "Floral Dress")
        self.assertEqual(
            first["url"],
            "https://www.bloomingdales.com/shop/product/aqua-floral-dress?ID=111111",
        )
        self.assertEqual(first["price"], 120.0)
        self.assertEqual(first["original_price"], 150.0)
        self.assertEqual(first["image"], "https://img.example/a.jpg")
        self.assertEqual(first["brand"], "AQUA")
        self.assertEqual(first["rating"], 4.6)
        self.assertEqual(first["review_count"], 12)
        self.assertEqual(first["category"], "women")
        self.assertIn(
            "https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683",
            first["subcategory_urls"],
        )
        self.assertIn(
            "https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683&prefn1=COLOR_NORMAL&prefv1=Blue",
            first["facet_urls"],
        )

        self.assertEqual(next_requests[0].meta["page"], 2)
        self.assertEqual(
            next_requests[0].url,
            "https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683&pageindex=2",
        )

    def test_reference_resolution_and_deduplication_stop_follow_up_pagination(self):
        first_page = self._response(
            "https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683",
            self._fixture("bloomingdales-dresses-leaf-page1.html"),
            resolved_leaf=True,
        )
        first_outputs = list(self.spider.parse(first_page))
        page_two_request = next(obj for obj in first_outputs if isinstance(obj, Request))

        second_page = TextResponse(
            url=page_two_request.url,
            request=page_two_request,
            body=self._fixture("bloomingdales-dresses-leaf-page2.html").encode("utf-8"),
            encoding="utf-8",
            status=200,
        )

        second_outputs = list(self.spider.parse(second_page))
        self.assertEqual(second_outputs, [])

    def test_block_page_raises_runtime_error(self):
        request = Request(BLOOMINGDALES_CATEGORIES["women"], meta={"page": 1})
        blocked = TextResponse(
            url=request.url,
            request=request,
            body=b"Access denied",
            encoding="utf-8",
            status=403,
        )
        with self.assertRaisesRegex(RuntimeError, "blocked"):
            list(self.spider.parse(blocked))


if __name__ == "__main__":
    unittest.main()
