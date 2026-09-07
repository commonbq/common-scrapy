from __future__ import annotations

"""Target search spider."""

from common.spiders.target_listing_spider import TargetListingSpider


class TargetSearchSpider(TargetListingSpider):
    name = "target_search"
