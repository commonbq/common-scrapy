from __future__ import annotations

"""Deprecated alias: `target_listing`.

Use `target_search` instead.
"""

from typing import Iterable

from common.spiders.target_search_spider import TargetSearchSpider


class TargetListingSpider(TargetSearchSpider):
    name = "target_listing"

    def start_requests(self) -> Iterable[object]:
        self.logger.warning("`target_listing` is deprecated; use `target_search` instead")
        yield from super().start_requests()
