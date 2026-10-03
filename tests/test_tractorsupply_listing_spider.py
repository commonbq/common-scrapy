import json
import unittest

from scrapy.http import HtmlResponse, Request, XmlResponse

from common.spiders.tractorsupply_listing_spider import TractorsupplyListingSpider


class TractorsupplyListingSpiderTest(unittest.TestCase):
    def test_sitemap_is_bounded(self):
        spider = TractorsupplyListingSpider(category="products-1", max_pages=1)
        request = next(spider.start_requests())
        xml = "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>" + "".join(
            f"<url><loc>https://www.tractorsupply.com/tsc/product/item-{n}</loc></url>" for n in range(30)
        ) + "</urlset>"
        response = XmlResponse(request.url, request=request, body=xml.encode())
        self.assertEqual(len(list(spider.parse_sitemap(response))), 24)

    def test_next_data_mapping(self):
        spider = TractorsupplyListingSpider(category="products-1")
        payload = {"props": {"pageProps": {"pageProps": {"pdpData": {"productDetails": {
            "productDetailsById": {"catalogEntryView": [{"uniqueID": "867", "partNumber": "100001199", "name": "Trailer Lift", "manufacturer": "Gorilla-Lift", "xf_thumbnail": "1000011", "attributes": [{"identifier": "_BazaarVoiceReviewRating", "values": [{"value": "4.7"}]}]}]},
            "inventoryAvailabilityData": {"inventoryStatus": "AVL"},
            "breadcrumb": {"breadCrumbTrailEntryView": [{"label": "Trailer Dollies"}]},
        }}}}}}
        request = Request("https://www.tractorsupply.com/tsc/product/trailer-lift", meta={"entry": spider.categories[0]})
        html = f'<script id="__NEXT_DATA__">{json.dumps(payload)}</script>'
        item = list(spider.parse_product(HtmlResponse(request.url, request=request, body=html.encode(), encoding="utf-8")))[0]
        self.assertEqual(item["item_id"], "867")
        self.assertEqual(item["rating"], 4.7)
        self.assertEqual(item["primary_category"], "Trailer Dollies")
        self.assertEqual(item["raw"]["partNumber"], "100001199")

    def test_feed_contract(self):
        fields = TractorsupplyListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertIn("raw", fields)
        self.assertIn("source_url", fields)
