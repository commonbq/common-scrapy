import json
import unittest

from scrapy.http import HtmlResponse, Request, TextResponse

from common.spiders.barnesandnoble_listing_spider import BarnesandnobleListingSpider


PRODUCT = {
    "id": "gid://shopify/Product/8827283734769", "title": "Projecting Politics",
    "handle": "9780765635969", "description": "An interdisciplinary exploration.",
    "vendor": "Taylor & Francis", "productType": "Hardcover", "availableForSale": True,
    "createdAt": "2025-06-09T19:34:48Z", "updatedAt": "2026-09-19T10:30:54Z",
    "publishedAt": "2025-07-30T20:47:42Z", "tags": ["PDS_WorkId:1120010465"],
    "onlineStoreUrl": "https://shop.barnesandnoble.com/products/9780765635969",
    "featuredImage": {"url": "https://cdn.shopify.com/book.jpg", "altText": "cover"},
    "images": {"nodes": [{"url": "https://cdn.shopify.com/book.jpg"}]},
    "options": [{"name": "Title", "values": ["Default Title"]}],
    "priceRange": {"minVariantPrice": {"amount": "237.61", "currencyCode": "USD"}, "maxVariantPrice": {"amount": "240.00", "currencyCode": "USD"}},
    "compareAtPriceRange": {"maxVariantPrice": {"amount": "250.00", "currencyCode": "USD"}},
    "variants": {"nodes": [{"id": "gid://shopify/ProductVariant/46222109016305", "title": "Default Title", "sku": "9780765635969", "availableForSale": True, "price": {"amount": "237.61", "currencyCode": "USD"}, "compareAtPrice": None, "selectedOptions": []}]},
}


def api_response(products, *, page=1, next_page=False):
    body = json.dumps({"data": {"products": {"nodes": products, "pageInfo": {"hasNextPage": next_page, "endCursor": "cursor-2"}}}})
    request = Request("https://store.myshopify.com/api/2025-07/graphql.json", meta={"category": "fiction", "search_query": "fiction", "api_url": "https://store.myshopify.com/api/2025-07/graphql.json", "token": "public", "page": page})
    return TextResponse(request.url, request=request, body=body, encoding="utf-8")


class BarnesandnobleListingSpiderTest(unittest.TestCase):
    def test_bootstraps_rotating_api_configuration_without_parsing_cards(self):
        spider = BarnesandnobleListingSpider(category="fiction")
        document = r'<script>window.x=[\"publicStoreDomain\",\"store.myshopify.com\",\"publicStorefrontApiVersion\",\"2025-07\",\"storefrontAccessToken\",\"public-token\"]</script>'
        request = Request("https://www.barnesandnoble.com/collections/books/fiction", meta={"category": "fiction", "search_query": "fiction"})
        response = HtmlResponse(request.url, request=request, body=document, encoding="utf-8")
        [api_request] = list(spider.parse_bootstrap(response))
        self.assertEqual(api_request.url, "https://store.myshopify.com/api/2025-07/graphql.json")
        self.assertEqual(api_request.headers[b"x-shopify-storefront-access-token"], b"public-token")

    def test_maps_api_product_and_feed_contract(self):
        spider = BarnesandnobleListingSpider(category="fiction")
        [item] = list(spider.parse_api(api_response([PRODUCT])))
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual((item["item_id"], item["variant_id"], item["ean"]), ("8827283734769", "46222109016305", "9780765635969"))
        self.assertEqual((item["price"], item["compare_price"], item["currency"]), (237.61, 250.0, "USD"))
        self.assertEqual(item["source"], "barnesandnoble_storefront_graphql_api")

    def test_cursor_pagination_and_deduplication(self):
        spider = BarnesandnobleListingSpider(category="fiction", max_pages=2)
        first = list(spider.parse_api(api_response([PRODUCT], next_page=True)))
        self.assertEqual(first[1].meta["page"], 2)
        self.assertEqual(json.loads(first[1].body)["variables"]["after"], "cursor-2")
        self.assertEqual(list(spider.parse_api(api_response([PRODUCT], page=2))), [])

    def test_missing_bootstrap_and_graphql_errors_fail_loudly(self):
        spider = BarnesandnobleListingSpider(category="fiction")
        request = Request("https://www.barnesandnoble.com/collections/books/fiction")
        response = HtmlResponse(request.url, request=request, body=b"<html></html>", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "bootstrap is missing"):
            list(spider.parse_bootstrap(response))
        error = TextResponse(
            "https://store.myshopify.com/api/2025-07/graphql.json",
            request=Request("https://store.myshopify.com/api/2025-07/graphql.json", meta={"page": 1}),
            body=b'{"errors":[{"message":"bad token"}]}', encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "GraphQL errors"):
            list(spider.parse_api(error))
