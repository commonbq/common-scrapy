import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.elfcosmetics_listing_spider import ElfcosmeticsListingSpider


class ElfcosmeticsListingSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = ElfcosmeticsListingSpider(category="face", max_pages=2)

    def response(self):
        request = Request(
            "https://www.elfcosmetics.com/collections/face",
            meta={"page": 1, "origin": "https://www.elfcosmetics.com/collections/face"},
        )
        body = b"""<html><body>
          <a href='/products/banner-product'>Promotional banner</a>
          <article><a aria-label='View details for Halo Glow Setting Powder'
            href='/products/halo-glow-setting-powder?Color=Light'>
            <img src='https://cdn.example/powder.jpg'/><span>Halo Glow Setting Powder</span>
            <span>$8.00</span></a></article>
          <a rel='next' href='/collections/face?page=2'>Next</a>
        </body></html>"""
        return HtmlResponse(request.url, request=request, body=body, encoding="utf-8")

    def test_feed_export_fields_are_stable(self):
        self.assertEqual(
            self.spider.custom_settings["FEED_EXPORT_FIELDS"],
            ["item_id", "title", "url", "price", "currency", "brand", "rating",
             "reviews_count", "image_url", "category", "category_url", "page", "source",
             "source_url", "raw"],
        )

    def test_html_items_include_export_context_and_pagination(self):
        output = list(self.spider.parse_html(self.response()))
        item, request = output
        self.assertEqual(item["item_id"], "halo-glow-setting-powder")
        self.assertEqual(item["title"], "Halo Glow Setting Powder")
        self.assertEqual(item["price"], 8.0)
        self.assertEqual(item["category"], "face")
        self.assertEqual(item["source"], "elfcosmetics_html")
        self.assertEqual(request.url, "https://www.elfcosmetics.com/collections/face?page=2")


if __name__ == "__main__":
    unittest.main()
