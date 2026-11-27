"""Mango US product listings from the Next.js React Flight bootstrap state."""

from __future__ import annotations

import json
import re

import scrapy
from dotenv import dotenv_values

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.mango_categories import MANGO_CATEGORIES


class MangoListingSpider(BaseListingSpider):
    name = "mango_listing"
    allowed_domains = ["shop.mango.com"]
    categories = MANGO_CATEGORIES
    custom_settings = {
        "FEED_EXPORT_FIELDS": [
            "product_id", "title", "url", "image_url", "color", "price",
            "currency", "category", "category_url", "page", "position",
            "source", "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = dotenv_values(".env").get("SCRAPEOPS_PROXY")
        if not self.proxy:
            raise ValueError("SCRAPEOPS_PROXY must be configured in .env")

    async def start(self):
        entry = self.category_entry(self.category)
        target = self.url or self.category_url or (entry["url"] if isinstance(entry, dict) else entry)
        if not target:
            raise ValueError(f"Unknown category {self.category!r}; choose one of {self.available_categories()}")
        yield scrapy.Request(
            target, callback=self.parse,
            meta={"proxy": self.proxy, "category": self.category, "category_url": target},
            headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
                     "accept-language": "en-US,en;q=0.9"},
        )

    @staticmethod
    def _catalog_items(response):
        # Next.js serializes React Flight rows as JSON strings inside script calls.
        for script in response.xpath('//script[contains(., "__next_f.push")]/text()').getall():
            match = re.search(r"__next_f\.push\((\[.*\])\)", script, re.S)
            if not match:
                continue
            try:
                flight = json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
            payload = flight[1] if len(flight) > 1 and isinstance(flight[1], str) else ""
            marker = '"catalogItemsData":'
            start = payload.find(marker)
            if start < 0:
                continue
            start += len(marker)
            while start < len(payload) and payload[start].isspace():
                start += 1
            if start >= len(payload) or payload[start] != '[':
                continue
            # Find the JSON array boundary while honoring strings and escapes.
            depth, quoted, escaped, end = 0, False, False, None
            for index in range(start, len(payload)):
                char = payload[index]
                if quoted:
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        quoted = False
                elif char == '"':
                    quoted = True
                elif char == '[':
                    depth += 1
                elif char == ']':
                    depth -= 1
                    if depth == 0:
                        end = index + 1
                        break
            if end:
                encoded = payload[start:end]
                try:
                    return json.loads(encoded)
                except (json.JSONDecodeError, TypeError):
                    continue
        return None

    def parse(self, response):
        items = self._catalog_items(response)
        if not isinstance(items, list) or not items:
            raise scrapy.exceptions.CloseSpider("Mango Next.js bootstrap contained no catalogItemsData")
        for position, row in enumerate(items, 1):
            ref = row.get("reference") or row.get("id")
            if not ref:
                continue
            colors = row.get("colors") or []
            color = colors[0] if colors else {}
            looks = color.get("looks") or {}
            image = next((
                image_data.get("img")
                for look in looks.values()
                for image_data in (look.get("images") or {}).values()
                if image_data.get("img")
            ), None)
            image_url = f"https://media.mango.com{image}" if image else None
            yield {
                "product_id": ref,
                "title": row.get("nameEn") or row.get("name"),
                "url": response.urljoin(row.get("url") or ""),
                "image_url": image_url,
                "color": color.get("labelEn") or color.get("label"),
                "price": None,
                "currency": "USD",
                "category": response.meta["category"],
                "category_url": response.meta["category_url"],
                "page": 1,
                "position": position,
                "source": "mango_next_flight_bootstrap",
                "timestamp": self.job_timestamp,
            }
