from pathlib import Path

from scrapy.http import HtmlResponse

from common.spiders.tesco_listing_spider import TescoListingSpider


def test_apollo_fixture_contains_product_listing_and_normalized_product():
    fixture = Path(__file__).parent / "fixtures" / "tesco_apollo_listing.html"
    response = HtmlResponse(
        url="https://www.tesco.com/shop/en-GB/browse/groceries-and-essentials/fresh-food/all",
        body=fixture.read_bytes(),
        encoding="utf-8",
    )

    cache = TescoListingSpider._apollo_cache(response)
    listing = TescoListingSpider._listing(cache, 1)
    ref = listing["results"][0]["node"]["__ref"]

    assert listing["info"]["total"] == 1
    assert cache[ref]["title"] == "Muller Light Yogurt 6x140g"
