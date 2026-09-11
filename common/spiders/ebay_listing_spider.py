from __future__ import annotations

"""eBay category listing spider (bootstrap/model-state first).

Usage examples:
  scrapy crawl ebay_listing -a category='laptops' -a max_pages=2
  scrapy crawl ebay_listing -a category_url='https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276' -a max_pages=2
"""

import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.ebay_bootstrap_utils import (
    extract_browse_tiles_from_html,
    extract_items_from_next_data,
    extract_items_from_html_cards,
    extract_json_ld_products,
    extract_next_data,
)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _build_categories() -> list[dict[str, str]]:
    data_path = Path(__file__).resolve().parent / "ebay_category_urls.json"
    with data_path.open("r", encoding="utf-8") as fp:
        category_dict = json.load(fp)

    categories: list[dict[str, str]] = []
    for top_level, section in category_dict.items():
        if not isinstance(top_level, str) or not isinstance(section, dict):
            continue
        top_slug = _slug(top_level)
        for label, url in section.items():
            if not isinstance(label, str) or not isinstance(url, str):
                continue
            categories.append({"category": f"{top_slug}/{_slug(label)}", "url": url})
    return categories


class EbayListingSpider(BaseListingSpider):
    name = "ebay_listing"
    allowed_domains = ["ebay.com", "www.ebay.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    categories: list[dict[str, str]] = []

    categories = _build_categories()

    def start_requests(self):
        target_url = self._with_page(self._resolve_target_url(), 1)
        yield scrapy.Request(
            target_url,
            callback=self.parse,
            meta=self.proxy_meta({"page": 1, "original_url": target_url}),
        )

    def parse(self, response: scrapy.http.Response):
        original_url = response.meta.get("original_url") or response.url
        page = int(response.meta.get("page", 1))

        yielded = 0

        next_data = extract_next_data(response.text or "")
        if next_data:
            for item in extract_items_from_next_data(next_data):
                item.update(
                    {
                        "mode": "category",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yielded += 1
                yield item

        if yielded == 0:
            for item in extract_json_ld_products(response.text or ""):
                item.update(
                    {
                        "mode": "category",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yielded += 1
                yield item

        if yielded == 0:
            for item in extract_items_from_html_cards(response.text or ""):
                item.update(
                    {
                        "mode": "category",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yield item
                yielded += 1

        if yielded == 0:
            for item in extract_browse_tiles_from_html(response.text or ""):
                item.update(
                    {
                        "mode": "category",
                        "category_url": self.category_url or self.url,
                        "page": page,
                        "source_url": response.url,
                    }
                )
                yield item

        if page < self.args.max_pages:
            next_url = self._with_page(original_url, page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta=self.proxy_meta({"page": page + 1, "original_url": next_url}),
            )

    def _resolve_target_url(self) -> str:
        if self.url:
            return self.url
        if self.category_url:
            return self.category_url
        if self.category and self.category.startswith(("http://", "https://")):
            self.category_url = self.category
            return self.category_url
        for entry in self.categories:
            if entry.get("category") == self.category:
                self.category_url = entry.get("url")
                return self.category_url
        names = ", ".join(sorted([c["category"] for c in self.categories]))
        raise ValueError(f"Unknown category '{self.category}'. Use one of: {names}")

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs.setdefault("_ipg", ["60"])
        qs["_pgn"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))
