from __future__ import annotations

import json
import re
from urllib.parse import urljoin

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.wayfair_categories import WAYFAIR_CATEGORIES


class WayfairListingSpider(BaseListingSpider):
    """Wayfair listings from server-rendered semantic product cards."""

    name = "wayfair_listing"
    allowed_domains = ["wayfair.com", "www.wayfair.com", "localhost", "127.0.0.1"]
    categories = WAYFAIR_CATEGORIES
    require_category_arg = False

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_FIELDS": [
            "category", "department", "item_id", "variant_id", "title", "brand",
            "selected_options", "option_ids", "choices_text", "url", "image_url",
            "image_srcset", "price", "original_price", "currency", "rating",
            "reviews_count", "promotion", "promotion_type", "availability",
            "delivery", "is_sponsored", "page", "position", "source_url",
            "source", "raw",
            "timestamp",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            available = ", ".join(self.available_categories())
            raise ValueError(f"Provide -a category=<name>, category_url=<url>, or url=<url>. Available categories: {available}")
        self._seen_products: set[str] = set()

    def start_requests(self):
        self._seen_products.clear()
        target = self.resolve_target_url()
        selected = next((row for row in self.categories if row["url"] == target), {})
        yield scrapy.Request(
            target,
            callback=self.parse,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
            },
            meta={
                "page": 1,
                "category": self.category or "custom",
                "department": selected.get("department"),
            },
        )

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise ValueError(f"Wayfair listing returned HTTP {response.status}: {response.url}")

        grid = response.xpath('//*[@data-test-id="Browse-Grid"]')
        if not grid:
            raise ValueError(
                f"Wayfair Browse-Grid absent; URL may be a hub or blocked response: {response.url}"
            )
        cards = grid.xpath('.//*[@data-test-id="ListingCard"][.//a[contains(@href, "/pdp/")]]')
        if not cards:
            raise ValueError(f"Wayfair Browse-Grid contains no real product cards: {response.url}")

        page = int(response.meta.get("page", 1))
        new_count = 0
        for position, card in enumerate(cards, start=1):
            item = self._extract_card(card, response.url)
            item_id = item.get("item_id")
            if not item_id or item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            new_count += 1
            item.update({
                "category": response.meta.get("category"),
                "department": response.meta.get("department"),
                "page": page,
                "position": position,
                "source_url": response.url,
                "source": "wayfair_server_rendered_listing_card",
            })
            yield item

        if new_count == 0:
            self.logger.warning("Wayfair page produced no new listing IDs: %s", response.url)
            return

        next_href = response.xpath(
            '//*[@data-test-id="Grid-Pagination"]//a[@data-enzyme-id="paginationNextPageLink"]/@href'
        ).get()
        if next_href and page < self.max_pages:
            yield response.follow(
                next_href,
                callback=self.parse,
                headers=response.request.headers,
                meta={**response.meta, "page": page + 1},
            )

    def _extract_card(self, card: scrapy.Selector, base_url: str) -> dict:
        tracking_node = card.xpath('.//*[@data-tracking-metadata][1]')
        tracking = self._json_object(tracking_node.attrib.get("data-tracking-metadata"))
        metadata = tracking.get("metadata") if isinstance(tracking.get("metadata"), dict) else {}
        if not metadata:
            self.logger.warning("Malformed or absent Wayfair tracking metadata")

        context_node = card.xpath('.//*[@data-clio-context and @data-test-id="CardWrapper"][1]')
        context = self._json_object(context_node.attrib.get("data-clio-context"))
        # `isSponsored` lives on the ListingCard's own clio context; the inner
        # CardWrapper context only carries displayListingID/VariantID.
        card_context = self._json_object(card.attrib.get("data-clio-context"))
        href = card.xpath('.//a[contains(@href, "/pdp/")][1]/@href').get()
        image = card.xpath('.//img[@data-name-id="ListingCardImageCarouselLeadImage"][1]')
        if not image:
            image = card.xpath('.//img[1]')

        title = metadata.get("listingCardName") or self._text(
            card.xpath('.//*[@data-name-id="ListingCardName"]//text()').getall()
        )
        brand = metadata.get("manufacturerName") or self._text(
            card.xpath('.//*[@data-name-id="ListingCardManufacturer"]//text()').getall()
        ).removeprefix("By ")
        price = self._money(metadata.get("leadPrice") or self._text(
            card.xpath('.//*[@data-test-id="PricingStandard-leadPrice"]//text()').getall()
        ))
        original_price = self._money(metadata.get("strikethroughPrice") or self._text(
            card.xpath('.//*[@data-test-id="PricingStandard-strikethroughPrice"]//text()').getall()
        ))

        return {
            "item_id": metadata.get("displayListingId") or context.get("displayListingID") or self._id_from_url(href),
            "variant_id": context.get("displayListingVariantID"),
            "title": title or None,
            "brand": brand or None,
            "selected_options": self._text(card.xpath('.//*[@data-name-id="ListingCardSelectedChoices"]//text()').getall()) or None,
            "option_ids": metadata.get("displayedOptionIDs") or [],
            "choices_text": metadata.get("choicesText"),
            "url": urljoin(base_url, href) if href else None,
            "image_url": image.attrib.get("src"),
            "image_srcset": image.attrib.get("srcset"),
            "price": price,
            "original_price": original_price,
            "currency": "USD" if price is not None or original_price is not None else None,
            "rating": self._number(metadata.get("averageRating")),
            "reviews_count": self._integer(metadata.get("totalReviewCount")),
            "promotion": metadata.get("flagText"),
            "promotion_type": metadata.get("flagVariation"),
            "availability": metadata.get("inventoryStatusMessage"),
            "delivery": metadata.get("shippingBadgeText") or self._text(
                card.xpath('.//*[@data-name-id="ShippingWidgetPlainText"]//text()').getall()
            ) or None,
            "is_sponsored": bool(card_context.get("isSponsored", False)),
            "raw": tracking or None,
        }

    @staticmethod
    def _json_object(value: str | None) -> dict:
        try:
            parsed = json.loads(value or "")
        except (TypeError, ValueError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    @staticmethod
    def _text(parts: list[str]) -> str:
        return " ".join(part.strip() for part in parts if part.strip())

    @staticmethod
    def _money(value):
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
        match = re.search(r"[0-9][0-9,]*(?:\.\d+)?", str(value or ""))
        return float(match.group(0).replace(",", "")) if match else None

    @staticmethod
    def _number(value):
        try:
            return float(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value):
        try:
            return int(value) if value is not None and not isinstance(value, bool) else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _id_from_url(url: str | None) -> str | None:
        match = re.search(r"-([a-zA-Z]+\d+)\.html", url or "")
        return match.group(1) if match else None
