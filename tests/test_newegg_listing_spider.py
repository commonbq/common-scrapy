import json
import unittest

import scrapy
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
    second_product = {
        "ProductNumber": "19-113-737",
        "ItemCell": {
            "Item": "19-113-737",
            "FinalPrice": 99,
            "UnitCost": 109.0,
            "Model": "BX8070110100F",
            "Instock": True,
            "ShippingCharge": 0.0,
            "ShipFromCountryName": "United States",
            "Description": {"Title": "Intel Core i3-10100F", "UrlKeywords": "intel-core-i3-10100f"},
            "NewImage": {"ImageName": "19-113-737-01.png"},
            "Image": {"ImagePathPattern": [{"Size": 1280, "PathPattern": "https://img.test/{ImageName}"}]},
            "ItemManufactory": {"Manufactory": "Intel"},
            "Review": {"RatingOneDecimal": 4.7, "HumanRating": 388},
            "Seller": {"SellerName": "Newegg"},
            "Category": {"RealCategoryName": "CPU"},
            "Subcategory": {"SubcategoryDescription": "Desktop CPU Processor"},
        },
    }

    def test_hydration_mapping_feed_fields_and_pagination(self):
        spider = NeweggListingSpider(category="desktop-cpu-processors", max_pages=2)
        output = list(spider.parse(
            response_for({"Products": [self.product, self.second_product], "TotalItemCount": 40}),
            "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343", 1))
        items, request = output[:-1], output[-1]
        self.assertEqual(len(items), 2)
        first, second = items
        self.assertEqual(list(first), spider.custom_settings["FEED_EXPORT_FIELDS"])
        self.assertEqual(first["item_id"], "19-113-877")
        self.assertEqual(first["title"], "AMD Ryzen 7 9800X3D")
        self.assertEqual(first["brand"], "AMD")
        self.assertEqual(first["price"], 469)
        self.assertEqual(first["original_price"], 497.49)
        self.assertEqual(first["url"], "https://www.newegg.com/amd-ryzen-7-9800x3d/p/N82E16819113877")
        self.assertEqual(first["image"], "https://img.test/19-113-877-01.png")
        self.assertEqual(first["rating"], 4.8)
        self.assertEqual(first["reviews_count"], 727)
        self.assertEqual(first["page"], 1)
        self.assertEqual(second["item_id"], "19-113-737")
        self.assertEqual(second["title"], "Intel Core i3-10100F")
        self.assertEqual(second["brand"], "Intel")
        self.assertEqual(second["rating"], 4.7)
        self.assertEqual(second["reviews_count"], 388)
        self.assertEqual(second["url"], "https://www.newegg.com/intel-core-i3-10100f/p/N82E16819113737")
        self.assertEqual(second["image"], "https://img.test/19-113-737-01.png")
        # Every exported item carries the verbatim hydration entry in ``raw``.
        self.assertEqual(first["raw"], self.product)
        self.assertEqual(second["raw"], self.second_product)
        self.assertEqual(first["raw"]["ItemCell"]["FinalPrice"], 469)
        self.assertEqual(request.url, "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343/Page-2")

    def test_partial_final_page_keeps_first_page_size(self):
        # 40 products, 36 on page 1, 4 on page 2 must not schedule a phantom page 3.
        spider = NeweggListingSpider(category="desktop-cpu-processors", max_pages=10)
        page1 = list(spider.parse(
            response_for({"Products": [self.product] * 36, "TotalItemCount": 40}),
            "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343", 1))
        request = page1[-1]
        self.assertEqual(request.cb_kwargs["page_size"], 36)
        # The second page is partial (4 items) but reuses the first-page size.
        page2 = list(spider.parse(
            response_for({"Products": [self.second_product] * 4, "TotalItemCount": 40}, page=2),
            "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343", 2,
            page_size=request.cb_kwargs["page_size"]))
        # No out-of-range page 3 may be scheduled; all outputs are deduplicated items.
        self.assertTrue(all(isinstance(output, dict) for output in page2))
        self.assertFalse([o for o in page2 if isinstance(o, scrapy.Request)])

    def test_direct_url_modes_construct_and_http_errors_pass_through(self):
        url = "https://www.newegg.com/Desktop-CPU-Processor/SubCategory/ID-343"
        self.assertEqual(NeweggListingSpider(url=url).resolve_target_url(), url)
        self.assertEqual(NeweggListingSpider(category_url=url).resolve_target_url(), url)
        self.assertTrue(NeweggListingSpider.custom_settings["HTTPERROR_ALLOW_ALL"])
        # The base-class gate must stay disabled or direct-URL runs cannot construct.
        self.assertFalse(NeweggListingSpider.require_category_arg)
        with self.assertRaisesRegex(ValueError, "Provide -a category"):
            NeweggListingSpider()

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

    def test_custom_link_overrides_generic_url_field(self):
        custom = "https://www.newegg.com/AMD-Processors/Category/ID-10"
        generic = "https://www.newegg.com/Computers/Category/ID-1"
        payload = {"Menu": [{"url": generic, "CustomLink": custom}]}
        self.assertEqual(NeweggListingSpider._inventory_urls(payload), [custom])

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
