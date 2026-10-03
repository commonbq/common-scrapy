from __future__ import annotations

"""Tractor Supply Co. listing spider (issue #181).

This spider is currently BLOCKED due to proxy and API limitations.

The /gtwy/SiteSearch/catalogSearch XHR endpoint requires a 'channel' header
which is stripped by the ScrapeOps proxy. Attempts to pass this header via
query parameters or other proxy services (BrightData, ScraperAPI) have failed
due to IP whitelisting or invalid API keys.

Neither the PLP __NEXT_DATA__ nor any other identified Next.js data routes
server-side render product information. The GraphQL /gtwy/catalog/allBrandsAndCat
endpoint is also 404.

Therefore, product data extraction is not currently feasible with available tools.
"""

import scrapy

class TractorsupplyListingSpider(scrapy.Spider):
    name = "tractorsupply_listing"
    allowed_domains = ["tractorsupply.com", "www.tractorsupply.com"]

    def start_requests(self):
        raise NotImplementedError(
            "TractorsupplyListingSpider is currently BLOCKED. "
            "Product data extraction is not feasible due to proxy limitations. "
            "See spider comments for details."
        )
