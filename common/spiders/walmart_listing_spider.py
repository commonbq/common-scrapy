from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.settings import PROXY


class WalmartListingSpider(scrapy.Spider):
    name = "walmart_listing"
    allowed_domains = ["walmart.com", "www.walmart.com", "r.jina.ai"]

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
        "DOWNLOAD_DELAY": 0,
    }

    def __init__(
        self,
        q: str | None = None,
        url: str | None = None,
        max_pages: int = 1,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.q = (q or "").strip()
        self.url = (url or "").strip()
        self.max_pages = int(max_pages)

    def start_requests(self):
        target_url = self.url
        if not target_url:
            target_url = f"https://www.walmart.com/search?{urlencode({'q': self.q or 'laptop'})}"

        meta = {"page": 1, "original_url": target_url}
        if PROXY:
            meta["proxy"] = PROXY

        yield scrapy.Request(target_url, callback=self.parse, meta=meta)

    def parse(self, response: scrapy.http.Response):
        if self._is_blocked(response):
            page = int(response.meta.get("page", 1))
            original_url = response.meta.get("original_url") or response.url
            fallback_url = f"https://r.jina.ai/http://{original_url.replace('https://', '').replace('http://', '')}"
            self.logger.info("Walmart blocked direct request. Falling back to %s", fallback_url)
            yield scrapy.Request(
                fallback_url,
                callback=self.parse_jina,
                meta={"page": page, "original_url": original_url},
            )
            return

        cards = response.css("[data-item-id][data-type='items'], div[data-item-id]")
        seen_ids: set[str] = set()

        for card in cards:
            item_id = (card.attrib.get("data-item-id") or "").strip()
            if not item_id or item_id in seen_ids:
                continue
            seen_ids.add(item_id)

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
                "item_id": item_id,
                "title": title,
                "url": product_url,
                "image_url": image_url,
                "price": price,
                "rating": self._extract_float(rating_text),
                "reviews_count": self._extract_int(reviews_text),
                "is_sponsored": bool(
                    card.xpath('.//*[contains(translate(normalize-space(.), "SPONSORED", "sponsored"), "sponsored")]')
                ),
                "source": "walmart_html",
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        next_href = (
            response.css("a[link-identifier='next-page']::attr(href)").get()
            or response.css("a[aria-label='Next Page']::attr(href)").get()
            or response.css("a[data-testid='NextPage']::attr(href)").get()
        )

        next_url = response.urljoin(next_href) if next_href else self._with_page(response.url, current_page + 1)
        if not next_url:
            return

        meta = {"page": current_page + 1, "original_url": next_url}
        if PROXY:
            meta["proxy"] = PROXY

        yield scrapy.Request(next_url, callback=self.parse, meta=meta)

    def parse_jina(self, response: scrapy.http.Response):
        text = response.text

        chunks = re.split(r"\n(?=\[### )", text)
        for chunk in chunks:
            m = re.search(r"\[###\s+(.*?)\]\((https?://[^)]+)\)", chunk)
            if not m:
                continue

            title = (m.group(1) or "").strip()
            url = (m.group(2) or "").strip()
            if "walmart.com" not in url:
                continue

            item_id_match = re.search(r"/ip/[^/]+/(\d+)", url)
            item_id = item_id_match.group(1) if item_id_match else None

            image_match = re.search(r"!\[Image[^\]]*\]\((https?://[^)]+)\)", chunk)
            price = self._extract_price(chunk)
            rating = self._extract_float(chunk)

            reviews_count = None
            reviews_match = re.search(r"(\d[\d,]*)\s+reviews", chunk, flags=re.I)
            if reviews_match:
                reviews_count = self._extract_int(reviews_match.group(1))

            yield {
                "item_id": item_id,
                "title": title,
                "url": url,
                "image_url": image_match.group(1) if image_match else None,
                "price": price,
                "rating": rating,
                "reviews_count": reviews_count,
                "is_sponsored": bool(re.search(r"\bSponsored\b", chunk, flags=re.I)),
                "source": "r.jina.ai_fallback",
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages:
            return

        original_url = response.meta.get("original_url")
        if not original_url:
            return

        next_original = self._with_page(original_url, current_page + 1)
        next_fallback = f"https://r.jina.ai/http://{next_original.replace('https://', '').replace('http://', '')}"
        yield scrapy.Request(
            next_fallback,
            callback=self.parse_jina,
            meta={"page": current_page + 1, "original_url": next_original},
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
