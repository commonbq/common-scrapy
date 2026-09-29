import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.newegg_listing_spider import NeweggListingSpider


def response_for(state, page=1):
    url = "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343"
    body = f'<script>window.__initialState__ = {json.dumps(state)};</script>'
    return HtmlResponse(
        url, request=Request(url), body=body.encode(), encoding="utf-8"
    )


class NeweggListingSpiderTests(unittest.TestCase):
    product = {
        "ProductNumber": "19-113-877",
        "ItemCell": {
            "Item": "19-113-877",
            "FinalPrice": 469,
            "UnitCost": 497.49,
            "Model": "100-100001084WOF",
            "Instock": True,
            "ShippingCharge": 0.01,
            "ShipFromCountryName": "United States",
            "Description": {"Title": "AMD Ryzen 7 9800X3D", "UrlKeywords": "amd-ryzen-7-9800x3d"},
            "NewImage": {"ImageName": "19-113-877-01.png"},
            "Image": {"ImagePathPattern": [{"Size": 1280, "PathPattern": "https://img.test/{ImageName}"}]},
            "ItemManufactory": {"Manufactory": "AMD"},
            "Review": {"RatingOneDecimal": 4.8, "HumanRating": 727},
            "Seller": {"SellerName": None},
            "Category": {"RealCategoryName": "CPU"},
            "Subcategory": {"SubcategoryDescription": "Desktop CPU Processor"},
            "PromotionInfo": {"PromotionText": "$20 off"},
            "CustomTags": {"Save": "Save 5%"},
        },
    }

    def test_hydration_mapping_feed_fields_and_pagination(self):
        spider = NeweggListingSpider(category="desktop-cpu-processors", max_pages=2)
        output = list(spider.parse(response_for({"Products": [self.product], "TotalItemCount": 2}),
                                   "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343", 1))
        item, request = output
        self.assertEqual(item["item_id"], "19-113-877")
        self.assertEqual(item["brand"], "AMD")
        self.assertEqual(item["price"], 469)
        self.assertEqual(item["rating"], 4.8)
        self.assertEqual(item["reviews_count"], 727)
        self.assertEqual(request.url, "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343/Page-2")
        self.assertEqual(list(item), spider.custom_settings["FEED_EXPORT_FIELDS"])

    def test_duplicate_ids_are_not_emitted(self):
        spider = NeweggListingSpider(category="desktop-cpu-processors")
        state = {"Products": [self.product, self.product], "TotalItemCount": 2}
        self.assertEqual(len(list(spider.parse(response_for(state), response_for(state).url, 1))), 1)

    def test_balanced_decoder_ignores_later_scripts(self):
        text = '<script>window.__initialState__={"Products":[]};</script><script>{bad}</script>'
        self.assertEqual(NeweggListingSpider._extract_initial_state(text), {"Products": []})

    def test_inventory_flattens_and_deduplicates_concrete_urls(self):
        url = "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343"
        payload = {"Menu": [{"url": url}, {"children": [{"CustomLink": url}]}]}
        self.assertEqual(NeweggListingSpider._inventory_urls(payload), [url])

    def test_inventory_builds_urls_from_store_contract(self):
        payload = {"StoreType": 3, "StoreId": 343, "StoreName": "Desktop CPU Processor"}
        self.assertEqual(
            NeweggListingSpider._inventory_urls(payload),
            ["https://www.newegg.com/desktop-cpu-processor/SubCategory/ID-343"],
        )

    def test_schema_drift_fails_loudly(self):
        spider = NeweggListingSpider(category="desktop-cpu-processors")
        with self.assertRaisesRegex(RuntimeError, "no Products list"):
            list(spider.parse(response_for({"Wrong": []}), response_for({}).url, 1))


if __name__ == "__main__":
    unittest.main()
