from __future__ import annotations

import re
import json
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class WalmartListingSpider(BaseListingSpider):
    name = "walmart_listing"
    allowed_domains = ["walmart.com", "www.walmart.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
        "DOWNLOAD_DELAY": 0,
        "FEED_EXPORT_FIELDS": [
            "url",
            "page",
            "position",
            "productId",
            "usItemId",
            "offerId",
            "title",
            "brand",
            "description",
            "productType",
            "itemType",
            "classType",
            "salesUnitType",
            "url",
            "sellerId",
            "sellerName",
            "sellerType",
            "hasSellerBadge",
            "imageUrl",
            "imageId",
            "imageName",
            "thumbnailUrl",
            "allImages",
            "imageMaps",
            "currency",
            "price",
            "currentPrice",
            "wasPrice",
            "unitPrice",
            "minimumPrice",
            "variantMinimumPrice",
            "priceRange",
            "shippingPrice",
            "savings",
            "savingsAmount",
            "discountPercent",
            "memberPrice",
            "subscriptionPrice",
            "subscriptionDiscount",
            "finalCostByWeight",
            "priceInfo",
            "rating",
            "reviewsCount",
            "availabilityStatus",
            "isOutOfStock",
            "conditionCode",
            "conditionGroupCode",
            "canAddToCart",
            "fulfillmentType",
            "fulfillmentSpeed",
            "fulfillmentSummary",
            "fulfillmentBadges",
            "fulfillmentBadgeGroups",
            "deliverySla",
            "unitQuantity",
            "averageWeight",
            "weightIncrement",
            "showBuyWithWalmartPlus",
            "isWalmartPlusMember",
            "annualEvent",
            "earlyAccessEvent",
            "showSubscription",
            "subscriptionEligible",
            "subscriptionTransactable",
            "isPreorder",
            "streetDate",
            "preorderMessage",
            "badgeText",
            "badgeKey",
            "badgeType",
            "badges",
            "badgeGroups",
            "flag",
            "specialBuy",
            "priceFlip",
            "promotionMessages",
            "promoDiscount",
            "promoData",
            "rewards",
            "isSponsored",
            "sponsoredProduct",
            "variantCount",
            "variants",
            "raw",
        ]
    }

    categories = [
        {
            "category": "electronics",
            "url": "https://www.walmart.com/cp/electronics/3944",
        },
        {
            "category": "home",
            "url": "https://www.walmart.com/cp/home/4044",
        },
        {
            "category": "clothing",
            "url": "https://www.walmart.com/cp/clothing/5438",
        },
        {
            "category": "beauty",
            "url": "https://www.walmart.com/cp/beauty/1085666",
        },
        {
            "category": "toys",
            "url": "https://www.walmart.com/cp/toys/4171",
        },
        {
            "category": "sports-and-outdoors",
            "url": "https://www.walmart.com/cp/sports-outdoors/4125",
        },
        {
            "category": "grocery",
            "url": "https://www.walmart.com/cp/food/976759",
        },
    ]

    def start_requests(self):
        category_url = self.resolve_target_url()
        category_url = self._with_page(category_url, page=1)
        meta = {"page": 1}
        yield scrapy.Request(category_url, callback=self.parse, meta=meta)

    def html_parse(self, response: scrapy.http.Response):
        if self._is_blocked(response):
            self.logger.warning("Walmart blocked direct request (status=%s) for %s", response.status, response.url)
            return

        cards = response.css("[data-item-id][data-type='items'], div[data-item-id]")
        seen_ids: set[str] = set()

        for card in cards:
            product_id = (card.attrib.get("data-item-id") or "").strip()
            if not product_id or product_id in seen_ids:
                continue
            seen_ids.add(product_id)

            title = (
                card.css("[data-automation-id='product-title']::text").get()
                or card.css("a[link-identifier='linkText']::text").get()
                or ""
            ).strip()

            product_href = (
                card.css("a[data-automation-id='product-title']::attr(href)").get()
                or card.css("a[href*='/ip/']::attr(href)").get()
                or ""
            )
            product_url = response.urljoin(product_href)

            image_url = (
                card.css("img[data-testid='productTileImage']::attr(src)").get()
                or card.css("img::attr(src)").get()
            )

            price_text = " ".join(
                card.css("[data-automation-id='product-price'] *::text").getall()
            )
            price = self._extract_price(
                card.css("[itemprop='price']::attr(content)").get() or price_text
            )

            rating_text = (
                card.css("span[role='img'][aria-label*='out of 5']::attr(aria-label)").get()
                or ""
            ).strip()
            reviews_text = (
                card.css("span[data-automation-id='product-review-count']::text").get()
                or ""
            ).strip()

            yield {
                "productDd": product_id,
                "title": title,
                "url": product_url,
                "imageUrl": image_url,
                "price": price,
                "rating": self._extract_float(rating_text),
                "reviewsCount": self._extract_int(reviews_text),
                "isSponsored": bool(
                    card.xpath('.//*[contains(translate(normalize-space(.), "SPONSORED", "sponsored"), "sponsored")]')
                ),
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        next_href = (
            response.css(
                "nav[aria-label='pagination'] "
                "a[aria-label='Next Page']::attr(href)"
            ).get()
            or response.css(
                "nav[aria-label='pagination'] "
                "a[link-identifier='next-page']::attr(href)"
            ).get()
        )

        # Walmart's sample has href="#" because navigation is performed by
        # client-side JavaScript. Generate the next page URL in that case.
        if next_href and not next_href.strip().startswith(("#", "javascript:")):
            next_url = response.urljoin(next_href)
        else:
            next_url = self._with_page(response.url, current_page + 1)

        if not next_url:
            return

        meta = {
            "page": current_page + 1,
        }

        yield scrapy.Request(
            next_url,
            callback=self.html_parse,
            meta=meta,
        )

    def _is_blocked(self, response: scrapy.http.Response) -> bool:
        body_lower = (response.text or "").lower()
        return (
            response.status in {307, 412, 418, 429, 503}
            or "robot or human" in body_lower
            or "access denied" in body_lower
            or "/blocked" in body_lower
        )

    def _with_page(self, url: str, page: int) -> str:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query["page"] = [str(page)]
        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    def _extract_price(self, text: str) -> float | None:
        cleaned = (text or "").replace(",", "")
        match = re.search(r"(?:\$|Now\s*\$|From\s*\$)\s*(\d+(?:\.\d{1,2})?)", cleaned, flags=re.I)
        if not match:
            match = re.search(r"(\d+(?:\.\d{1,2})?)", cleaned)
        if not match:
            return None
        return float(match.group(1))

    def _extract_float(self, text: str) -> float | None:
        match = re.search(r"(\d+(?:\.\d+)?)\s*out of 5", text or "", flags=re.I)
        if not match:
            match = re.search(r"(\d+(?:\.\d+)?)", text or "")
        if not match:
            return None
        return float(match.group(1))

    def _extract_int(self, text: str) -> int | None:
        cleaned = re.sub(r"[^\d]", "", text or "")
        if not cleaned:
            return None
        return int(cleaned)

    def parse(self, response: scrapy.http.Response):
        if self._is_blocked(response):
            self.logger.warning(
                "Walmart blocked direct request (status=%s) for %s",
                response.status,
                response.url,
            )
            return

        products = self._extract_embedded_products(response)

        if products:
            for position, product in enumerate(products, start=1):
                yield self._build_product_item(
                    response=response,
                    product=product,
                    position=position,
                )
        else:
            self.logger.warning(
                "__NEXT_DATA__ products unavailable; using DOM fallback for %s",
                response.url,
            )
            yield from self._parse_dom_cards(response)

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        next_href = (
            response.css(
                "nav[aria-label='pagination'] "
                "a[aria-label='Next Page']::attr(href)"
            ).get()
            or response.css(
                "nav[aria-label='pagination'] "
                "a[link-identifier='next-page']::attr(href)"
            ).get()
        )

        if next_href and not next_href.strip().startswith(("#", "javascript:")):
            next_url = response.urljoin(next_href)
        else:
            next_url = self._with_page(response.url, current_page + 1)

        if not next_url:
            return

        meta = {
            "page": current_page + 1,
        }

        yield scrapy.Request(
            next_url,
            callback=self.parse,
            meta=meta,
        )

    def _extract_embedded_products(
        self,
        response: scrapy.http.Response,
    ) -> list[dict]:
        raw_json = response.css("script#__NEXT_DATA__::text").get()
        if not raw_json:
            return []

        try:
            page_data = json.loads(raw_json)
        except (TypeError, json.JSONDecodeError) as exc:
            self.logger.warning("Could not decode __NEXT_DATA__: %s", exc)
            return []

        candidates: list[dict] = []

        def walk(value):
            if isinstance(value, dict):
                # Avoid treating entries inside variantList as products.
                if (
                    value.get("usItemId")
                    and value.get("name")
                    and (
                        "priceInfo" in value
                        or "availabilityStatus" in value
                        or "offerId" in value
                    )
                ):
                    candidates.append(value)

                for child in value.values():
                    walk(child)

            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(page_data)

        # Preserve page order while removing duplicate product representations.
        products_by_id: dict[str, dict] = {}

        for product in candidates:
            item_id = str(
                product.get("usItemId")
                or product.get("id")
                or ""
            ).strip()

            if not item_id:
                continue

            existing = products_by_id.get(item_id)

            # Prefer whichever representation contains more populated fields.
            if existing is None or self._product_score(product) > self._product_score(existing):
                products_by_id[item_id] = product

        return list(products_by_id.values())


    @staticmethod
    def _product_score(product: dict) -> int:
        return sum(
            value not in (None, "", [], {})
            for value in product.values()
        )

    def _build_product_item(
        self,
        response: scrapy.http.Response,
        product: dict,
        position: int,
    ) -> dict:
        price_info = product.get("priceInfo") or {}
        rating_info = product.get("rating") or {}
        image_info = product.get("imageInfo") or {}
        condition = product.get("conditionV2") or {}
        preorder = product.get("preOrder") or {}
        subscription = product.get("subscription") or {}
        badge = product.get("badge") or {}
        fulfillment_icon = product.get("fulfillmentIcon") or {}
        event_attributes = product.get("eventAttributes") or {}

        canonical_url = product.get("canonicalUrl")
        image_url = (
            product.get("image")
            or image_info.get("thumbnailUrl")
        )

        current_price = product.get("price")
        if current_price is None:
            current_price = price_info.get("itemPrice")
        if current_price is None:
            current_price = self._extract_price(
                price_info.get("linePrice")
                or price_info.get("linePriceDisplay")
                or ""
            )

        was_price = self._extract_price(price_info.get("wasPrice") or "")
        savings_amount = price_info.get("savingsAmt")

        if savings_amount is None and current_price and was_price:
            savings_amount = round(was_price - current_price, 2)

        discount_percent = None
        if current_price is not None and was_price:
            discount_percent = round(
                (was_price - current_price) / was_price * 100,
                2,
            )

        variants = []
        for variant in product.get("variantList") or []:
            if not variant:
                continue

            variant_url = variant.get("canonicalUrl")

            variants.append({
                **variant,
                "url": response.urljoin(variant_url) if variant_url else None,
                "image_url": variant.get("image"),
                "swatch_image_url": variant.get("swatchImageUrl"),
            })

        # Add consistently named/normalized fields for downstream use.
        item = {
            # Crawl metadata
            "url": response.url,
            "page": int(response.meta.get("page", 1)),
            "position": position,

            # Identity
            "productId": product.get("id"),
            "usItemId": product.get("usItemId"),
            "offerId": product.get("offerId"),

            # Product
            "title": product.get("name"),
            "brand": product.get("brand"),
            "description": product.get("description"),
            "productType": product.get("productType"),
            "itemType": product.get("itemType"),
            "classType": product.get("classType"),
            "salesUnitType": product.get("salesUnitType"),
            "url": response.urljoin(canonical_url) if canonical_url else None,

            # Seller
            "sellerId": product.get("sellerId"),
            "sellerName": product.get("sellerName"),
            "sellerType": product.get("sellerType"),
            "hasSellerBadge": product.get("hasSellerBadge"),

            # Images
            "imageUrl": image_url,
            "imageId": (
                product.get("imageId")
                or image_info.get("id")
            ),
            "imageName": (
                product.get("imageName")
                or image_info.get("name")
            ),
            "thumbnailUrl": image_info.get("thumbnailUrl"),
            "allImages": image_info.get("allImages"),
            "imageMaps": image_info.get("imageMaps"),

            # Price
            "currency": "USD",
            "price": current_price,
            "currentPrice": current_price,
            "wasPrice": was_price,
            "unitPrice": price_info.get("unitPrice"),
            "minimumPrice": price_info.get("minPrice"),
            "variantMinimumPrice": price_info.get("minPriceForVariant"),
            "priceRange": price_info.get("priceRangeString"),
            "shippingPrice": price_info.get("shipPrice"),
            "savings": price_info.get("savings"),
            "savingsAmount": savings_amount,
            "discountPercent": discount_percent,
            "memberPrice": price_info.get("memberPriceString"),
            "subscriptionPrice": price_info.get("subscriptionPrice"),
            "subscriptionDiscount": price_info.get("subscriptionPercentage"),
            "finalCostByWeight": price_info.get("finalCostByWeight"),
            "priceInfo": price_info,

            # Rating
            "rating": (
                product.get("averageRating")
                or rating_info.get("averageRating")
            ),
            "reviewsCount": (
                product.get("numberOfReviews")
                or rating_info.get("numberOfReviews")
            ),

            # Availability and condition
            "availabilityStatus": product.get("availabilityStatus"),
            "isOutOfStock": product.get("isOutOfStock"),
            "conditionCode": condition.get("code"),
            "conditionGroupCode": condition.get("groupCode"),
            "canAddToCart": product.get("canAddToCart"),

            # Fulfillment
            "fulfillmentType": product.get("fulfillmentType"),
            "fulfillmentSpeed": product.get("fulfillmentSpeed"),
            "fulfillmentSummary": product.get("fulfillmentSummary"),
            "fulfillmentBadges": product.get("fulfillmentBadges"),
            "fulfillmentBadgeGroups": product.get(
                "fulfillmentBadgeGroups"
            ),
            "deliverySla": product.get("unsheduled_Delivery_SLA"),

            # Quantity and weight
            "unitQuantity": product.get("unitQuantity"),
            "averageWeight": product.get("averageWeight"),
            "weightIncrement": product.get("weightIncrement"),

            # Programs and eligibility
            "showBuyWithWalmartPlus": product.get("showBuyWithWplus"),
            "isWalmartPlusMember": product.get("isWplusMember"),
            "annualEvent": product.get("annualEventV2"),
            "earlyAccessEvent": product.get("earlyAccessEvent"),

            # Subscription
            "showSubscription": product.get("showSubscribe"),
            "subscriptionEligible": subscription.get(
                "subscriptionEligible"
            ),
            "subscriptionTransactable": subscription.get(
                "subscriptionTransactable"
            ),

            # Preorder
            "isPreorder": preorder.get("isPreOrder"),
            "streetDate": preorder.get("streetDate"),
            "preorderMessage": preorder.get("preOrderMessage"),

            # Promotions and badges
            "badgeText": badge.get("text"),
            "badgeKey": badge.get("key"),
            "badgeType": badge.get("type"),
            "badges": product.get("badges"),
            "badgeGroups": product.get("badgeGroups"),
            "flag": product.get("flag"),
            "specialBuy": (
                product.get("specialBuy")
                or event_attributes.get("specialBuy")
            ),
            "priceFlip": (
                product.get("priceFlip")
                or event_attributes.get("priceFlip")
            ),
            "promotionMessages": product.get("promotionMessages"),
            "promoDiscount": product.get("promoDiscount"),
            "promoData": product.get("promoData"),
            "rewards": product.get("rewards"),

            # Advertising
            "isSponsored": bool(
                product.get("isSponsoredFlag")
                or product.get("sponsoredProduct")
            ),
            "sponsoredProduct": product.get("sponsoredProduct"),

            # Variants
            "variantCount": len(variants),
            "variants": variants,

            # Miscellaneous
            "raw": product,
        }

        return item
