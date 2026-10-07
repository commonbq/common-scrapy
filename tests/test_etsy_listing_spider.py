import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.etsy_listing_spider import EtsyListingSpider


CARD = """
<div class="v2-listing-card" data-listing-id="123" data-shop-id="456">
 <a href="https://www.etsy.com/listing/123/example?ref=x" title="Example"><img src="https://i.etsystatic.com/x.jpg"></a>
 <h3> Handmade Example </h3><input name="rating" value="4.8">
 <span class="reviews">(1.2k)</span><span class="currency-value">29.40</span>
 <p data-seller-name-container>Ad by ExampleShop</p><span>FREE shipping</span>
</div>
"""


class EtsyListingSpiderTest(unittest.TestCase):
    def spider(self):
        return EtsyListingSpider(category="jewelry", max_pages=1)

    def test_maps_api_fragment(self):
        item = list(self.spider()._parse_cards(CARD, "jewelry", 1))[0]
        self.assertEqual(item["item_id"], "123")
        self.assertEqual(item["reviews_count"], 1200)
        self.assertEqual(item["price"], 29.4)
        self.assertEqual(item["source"], "etsy_neu_search_api")

    def test_deduplicates_listing_id(self):
        spider = self.spider()
        self.assertEqual(len(list(spider._parse_cards(CARD + CARD, "jewelry", 1))), 1)

    def test_parses_api_envelope(self):
        spider = self.spider()
        request = Request("https://www.etsy.com/api", meta={"page": 1, "category": "jewelry", "category_url": "https://www.etsy.com/c/jewelry"})
        response = TextResponse(request=request, url=request.url, body=json.dumps({"output": {"async_search_results": CARD}}), encoding="utf-8")
        rows = list(spider.parse_api(response))
        self.assertEqual(rows[0]["title"], "Handmade Example")


if __name__ == "__main__":
    unittest.main()
