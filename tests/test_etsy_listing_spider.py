import json
import unittest

from scrapy.http import Request, TextResponse

from common.spiders.etsy_listing_spider import EtsyListingSpider


PAGE_HTML = """
<html><body>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"ItemList","itemListElement":[
  {"@type":"ListItem","position":1,"item":{"@type":"Product",
   "image":"https://i.etsystatic.com/x.jpg",
   "name":"Handmade Example",
   "url":"https://www.etsy.com/listing/123/example?ref=pagination",
   "brand":{"@type":"Brand","name":"ExampleShop"},
   "offers":{"@type":"Offer","price":"29.40","priceCurrency":"USD",
             "priceSpecification":{"@type":"UnitPriceSpecification","price":"42.00","priceCurrency":"USD"}}}},
  {"@type":"ListItem","position":2,"item":{"@type":"Product",
   "image":["https://i.etsystatic.com/y.jpg"],
   "name":"Second Product",
   "url":"https://www.etsy.com/listing/456/second",
   "brand":{"@type":"Brand","name":"SecondShop"},
   "offers":{"@type":"Offer","price":"10.00","priceCurrency":"USD"}}}
]}</script>
<div class="v2-listing-card" data-listing-id="123" data-shop-id="789">
 <a href="https://www.etsy.com/listing/123/example?ref=x" title="Example"><img src="https://i.etsystatic.com/x.jpg"></a>
 <h3> Handmade Example </h3><input type="hidden" name="rating" value="4.8">
 <span class="reviews">(1.2k)</span><span class="currency-value">29.40</span>
 <p data-seller-name-container>ExampleShop <span>From shop ExampleShop</span></p>
 <span>FREE shipping</span>
</div>
<div class="v2-listing-card" data-listing-id="456" data-shop-id="987">
 <a href="https://www.etsy.com/listing/456/second"><h3>Second Product</h3></a>
 <span class="currency-value">10.00</span>
 <p data-seller-name-container>Ad by SecondShop</p>
</div>
<nav class="search-pagination">
  <a href="https://www.etsy.com/c/jewelry?ref=pagination&page=2" data-page="2">Next</a>
</nav>
</body></html>
"""


def _response(body: str, url: str = "https://www.etsy.com/c/jewelry") -> TextResponse:
    request = Request(url, meta={"category": "jewelry", "category_url": url, "page": 1})
    return TextResponse(request=request, url=url, body=body, encoding="utf-8")


class EtsyListingSpiderTest(unittest.TestCase):
    def spider(self):
        return EtsyListingSpider(category="jewelry", max_pages=1)

    def test_parses_itemlist_jsonld(self):
        rows = list(self.spider().parse(_response(PAGE_HTML)))
        self.assertEqual(len(rows), 2)
        first = rows[0]
        self.assertEqual(first["item_id"], "123")
        self.assertEqual(first["shop_id"], "789")
        self.assertEqual(first["title"], "Handmade Example")
        self.assertEqual(first["shop"], "ExampleShop")
        self.assertEqual(first["url"], "https://www.etsy.com/listing/123/example")
        self.assertEqual(first["price"], 29.4)
        self.assertEqual(first["original_price"], 42.0)
        self.assertEqual(first["currency"], "USD")
        self.assertEqual(first["rating"], 4.8)
        self.assertEqual(first["reviews_count"], 1200)
        self.assertTrue(first["free_shipping"])
        self.assertFalse(first["is_ad"])
        self.assertEqual(first["position"], 1)
        self.assertEqual(first["source"], "etsy_itemlist_jsonld")

    def test_ad_card_is_flagged_and_shop_suppressed(self):
        rows = list(self.spider().parse(_response(PAGE_HTML)))
        ad_row = rows[1]
        self.assertEqual(ad_row["item_id"], "456")
        self.assertTrue(ad_row["is_ad"])
        self.assertIsNone(ad_row["shop"])
        self.assertEqual(ad_row["position"], 2)

    def test_deduplicates_listing_ids(self):
        spider = self.spider()
        rows = list(spider.parse(_response(PAGE_HTML)))
        self.assertEqual(len(rows), 2)
        more = list(spider.parse(_response(PAGE_HTML.replace('data-page="2"', 'data-page="3"'))))
        self.assertEqual(more, [])

    def test_follows_pagination_link(self):
        spider = EtsyListingSpider(category="jewelry", max_pages=2)
        requests = [r for r in spider.parse(_response(PAGE_HTML)) if isinstance(r, Request)]
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].url, "https://www.etsy.com/c/jewelry?ref=pagination&page=2")
        self.assertEqual(requests[0].meta["page"], 2)

    def test_max_pages_one_yields_no_followup(self):
        requests = [r for r in self.spider().parse(_response(PAGE_HTML)) if isinstance(r, Request)]
        self.assertEqual(requests, [])

    def test_empty_page_closes_spider(self):
        from scrapy.exceptions import CloseSpider

        spider = self.spider()
        with self.assertRaises(CloseSpider):
            list(spider.parse(_response("<html><body><p>no products</p></body></html>")))

    def test_custom_settings_keep_field_contract(self):
        fields = EtsyListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
        self.assertIn("raw", fields)
        self.assertIn("timestamp", fields)
        self.assertLess(fields.index("raw"), fields.index("timestamp"))


if __name__ == "__main__":
    unittest.main()
