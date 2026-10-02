import json
import unittest
import urllib.parse as urlparse
from pathlib import Path
from urllib.parse import urljoin

from scrapy.http import Request, TextResponse
from scrapy.settings import Settings

from common.spiders.footlocker_listing_spider import (
    FootlockerListingSpider, API_BASE, SITE_BASE, RESIDENTIAL_PROXY, _iter_nav_nodes
)

def _query(response_or_request) -> dict:
    query = urlparse.parse_qs(urlparse.urlparse(response_or_request.url).query)
    return query

class FootlockerListingSpiderTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.settings.set("PROXY", "http://scrapeops.country=us:test_key@proxy.scrapeops.io:5353")
        self.spider = FootlockerListingSpider(category="all-men-s-shoes", settings=self.settings, max_pages=2)

        self.header_json = json.loads(Path("sample/footlocker-header.json").read_text())
        self.mens_shoes_html = Path("sample/footlocker-mens-shoes.html").read_text()
        self.api_page0_json = json.loads(Path("sample/footlocker-mens-shoes-api-page0.json").read_text())

    def response(self, request, body, status=200, headers=None, url=None):
        return TextResponse(
            url=url or request.url,
            request=request,
            body=body.encode('utf-8') if isinstance(body, str) else json.dumps(body).encode('utf-8'),
            status=status,
            encoding="utf-8",
            headers=headers
        )

    # --------------------------------------------------------------- Initial Category Resolution

    def test_initial_request_fetches_header_json(self):
        requests = list(self.spider.start_requests())
        self.assertEqual(len(requests), 1)
        req = requests[0]
        self.assertIn("/api/content/en/header.public.json", req.url)
        self.assertEqual(req.callback, self.spider.parse_header_json_for_categories)
        self.assertIn('proxy', req.meta)
        self.assertNotIn(RESIDENTIAL_PROXY, req.meta['proxy'])
    
    def test_parse_header_json_for_categories_populates_categories_to_resolve(self):
        initial_request = Request(urljoin(SITE_BASE, "/api/content/en/header.public.json"), meta={'initial': True})
        response = self.response(initial_request, self.header_json)
        requests = list(self.spider.parse_header_json_for_categories(response))

        # After parsing header, _categories_to_resolve should be populated
        # and _resolved_categories should start getting populated either by query or HTML fetches
        self.assertTrue(len(self.spider._categories_to_resolve) > 0)
        self.assertEqual(self.spider._category_resolution_in_progress, True)

        # Verify some requests to get searchParams from HTML are generated
        html_requests_count = 0
        for req in requests:
            if req.callback == self.spider.parse_search_params_from_html:
                html_requests_count += 1
                self.assertIn(SITE_BASE, req.url)
                self.assertNotIn(RESIDENTIAL_PROXY, req.meta['proxy'])
        self.assertTrue(html_requests_count > 0)

    def test_extract_search_params_from_html(self):
        request = Request(urljoin(SITE_BASE, "/category/mens/shoes.html"), meta={'entry': {'url': '/category/mens/shoes.html'}})
        response = self.response(request, self.mens_shoes_html)
        search_params = self.spider._extract_search_params_from_html(response)
        self.assertEqual(search_params, "::collection_id:men-s-shoes")

    def test_parse_search_params_from_html_resolves_category(self):
        entry = {"band": "Men's", "sub_category": "Shoes", "name": "All Men's Shoes", "url": "/category/mens/shoes.html"}
        request = Request(urljoin(SITE_BASE, "/category/mens/shoes.html"), meta={'entry': entry})
        response = self.response(request, self.mens_shoes_html)
        requests = list(self.spider.parse_search_params_from_html(response))

        # One category should be resolved
        self.assertEqual(len(self.spider._resolved_categories), 1)
        resolved_entry = self.spider._resolved_categories[0]
        self.assertEqual(resolved_entry["category_slug"], "all-men-s-shoes")
        self.assertEqual(resolved_entry["searchParams"], "::collection_id:men-s-shoes")

        # If this was the last category to resolve, it should trigger API crawls
        # For this test, we mock _categories_to_resolve to have only one entry
        self.spider._categories_to_resolve = [entry]
        requests = list(self.spider.parse_search_params_from_html(response))
        # After this, it should trigger _start_api_crawls which will yield API requests
        self.assertTrue(any(req.callback == self.spider.parse_api_products for req in requests))
        self.assertFalse(self.spider._category_resolution_in_progress)

    # --------------------------------------------------------------- API Product Crawl

    def test_api_request_construction(self):
        entry = {"band": "Men's", "sub_category": "Shoes", "name": "All Men's Shoes", "url": "/category/mens/shoes.html", "searchParams": "::collection_id:men-s-shoes", "category_slug": "all-men-s-shoes"}
        req = self.spider._api_request(entry["searchParams"], entry["url"], page=0, metadata=entry)

        self.assertIn(API_BASE, req.url)
        self.assertIn("currentPage=0", req.url)
        self.assertIn(RESIDENTIAL_PROXY, req.meta['proxy'])
        self.assertEqual(req.callback, self.spider.parse_api_products)
        self.assertEqual(req.headers.get('Referer').decode(), entry["url"])

    def test_parse_api_products_yields_items_and_next_page(self):
        entry = {"band": "Men's", "sub_category": "Shoes", "name": "All Men's Shoes", "url": "/category/mens/shoes.html", "searchParams": "::collection_id:men-s-shoes", "category_slug": "all-men-s-shoes"}
        request = Request(API_BASE, meta={
            "category_url": entry["url"],
            "search_params": entry["searchParams"],
            "page": 0,
            "metadata": entry
        })
        response = self.response(request, self.api_page0_json, url=API_BASE)
        results = list(self.spider.parse_api_products(response))

        # Expecting 48 items + 1 next page request
        self.assertEqual(len(results), 48 + 1)

        first_item = results[0]
        self.assertIsInstance(first_item, dict)
        self.assertEqual(first_item["item_id"], "T8013103")
        self.assertEqual(first_item["title"], "Jordan Retro 12 - Men's")
        self.assertIn("EBFL2/T8013103", first_item["image_url"])
        self.assertEqual(first_item["price"], 215.0)
        self.assertEqual(first_item["currency"], "USD")
        self.assertEqual(first_item["band"], "Men's")
        self.assertEqual(first_item["sub_category"], "Shoes")
        self.assertEqual(first_item["category"], "all-men-s-shoes")
        self.assertEqual(first_item["brand"], "Jordan")
        self.assertEqual(first_item["page"], 1)
        self.assertEqual(first_item["source"], "footlocker_api")
        self.assertIn("raw", first_item)

        # Test brand derivation from title if product.brand is missing
        self.spider._seen_ids = set()  # allow the same fixture products to be re-parsed
        product_no_brand = self.api_page0_json["products"][1].copy()
        product_no_brand["brand"] = None
        request_no_brand = Request(API_BASE, meta={
            "category_url": entry["url"],
            "search_params": entry["searchParams"],
            "page": 0,
            "metadata": entry
        })
        response_no_brand = self.response(request_no_brand, {"products": [product_no_brand], "pagination": self.api_page0_json["pagination"]}, url=API_BASE)
        results_no_brand = list(self.spider.parse_api_products(response_no_brand))
        self.assertEqual(results_no_brand[0]["brand"], "Jordan") # "Jordan Retro 8" should derive "Jordan"

        # Last item should be the next page request
        next_page_request = results[-1]
        self.assertEqual(next_page_request.callback, self.spider.parse_api_products)
        self.assertEqual(next_page_request.meta["page"], 1)

    def test_max_pages_stops_pagination(self):
        self.spider.max_pages = 1 # Only one page
        entry = {"band": "Men's", "sub_category": "Shoes", "name": "All Men's Shoes", "url": "/category/mens/shoes.html", "searchParams": "::collection_id:men-s-shoes", "category_slug": "all-men-s-shoes"}
        request = Request(API_BASE, meta={
            "category_url": entry["url"],
            "search_params": entry["searchParams"],
            "page": 0,
            "metadata": entry
        })
        response = self.response(request, self.api_page0_json, url=API_BASE)
        results = list(self.spider.parse_api_products(response))

        # Expect 48 items, no next page request because max_pages is 1 (currentPage + 1 < max_pages is False)
        self.assertEqual(len(results), 48)
        self.assertFalse(any(req.callback == self.spider.parse_api_products for req in results[48:]))

    def test_no_products_stops_pagination(self):
        entry = {"band": "Men's", "sub_category": "Shoes", "name": "All Men's Shoes", "url": "/category/mens/shoes.html", "searchParams": "::collection_id:men-s-shoes", "category_slug": "all-men-s-shoes"}
        request = Request(API_BASE, meta={
            "category_url": entry["url"],
            "search_params": entry["searchParams"],
            "page": 0,
            "metadata": entry
        })
        empty_api_response = {"products": [], "pagination": {"currentPage": 0, "pageSize": 48, "sort": "relevance-descending", "totalPages": 0, "totalResults": 0}}
        response = self.response(request, empty_api_response, url=API_BASE)
        results = list(self.spider.parse_api_products(response))

        # Expect no items and no next page request
        self.assertEqual(len(results), 0)

    def test_explicit_category_arg_triggers_api_crawl(self):
        # Mock _resolved_categories to simulate resolution complete
        self.spider._resolved_categories = [{
            "band": "Men's",
            "sub_category": "Shoes",
            "name": "All Men's Shoes",
            "url": "/category/mens/shoes.html",
            "searchParams": "::collection_id:men-s-shoes",
            "category_slug": "all-men-s-shoes",
        }]
        self.spider._category_resolution_in_progress = False

        # Re-initialize spider with specific category
        spider_with_category = FootlockerListingSpider(category="all-men-s-shoes", settings=self.settings, max_pages=1)
        # Manually set resolved categories (this is normally done by earlier stages)
        spider_with_category._resolved_categories = self.spider._resolved_categories
        # ``start_requests`` only fetches the header when there is nothing to
        # resolve yet; with categories already resolved it goes straight to the
        # API crawl.
        spider_with_category._categories_to_resolve = self.spider._resolved_categories
        spider_with_category._category_resolution_in_progress = False

        requests = list(spider_with_category.start_requests())
        self.assertEqual(len(requests), 1)
        req = requests[0]
        self.assertIn(API_BASE, req.url)
        self.assertIn("currentPage=0", req.url)
        self.assertIn(RESIDENTIAL_PROXY, req.meta['proxy'])
        self.assertEqual(req.callback, spider_with_category.parse_api_products)
        self.assertEqual(req.meta["metadata"]["category_slug"], "all-men-s-shoes")

