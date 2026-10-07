from __future__ import annotations

"""Tripadvisor hotels from its server-rendered URQL bootstrap cache only."""

import json
import re
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.tripadvisor_categories import TRIPADVISOR_CATEGORIES


class TripadvisorListingSpider(BaseListingSpider):
    name = "tripadvisor_listing"
    allowed_domains = ["tripadvisor.com", "www.tripadvisor.com"]
    categories = TRIPADVISOR_CATEGORIES
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "category", "item_id", "title", "url", "rating", "review_count",
            "price", "currency", "address", "city", "country", "postal_code",
            "latitude", "longitude", "phone", "image_url", "accommodation_type",
            "star_rating", "rank", "amenities", "labels", "page", "position",
            "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }
    _hotel_id_re = re.compile(r"-d(\d+)-")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen: set[str] = set()

    def start_requests(self):
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url: str, page: int):
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta={"proxy": self._proxy(), "base_url": base_url, "page": page},
            dont_filter=True,
        )

    def _proxy(self):
        proxy = self.settings.get("PROXY")
        if not isinstance(proxy, str) or not proxy or "scrapeops" not in proxy.lower():
            return proxy or None
        parts = urlsplit(proxy)
        if not parts.hostname or parts.password is None:
            return proxy
        options = (parts.username or "").split(".")
        if "residential=true" not in options:
            options.append("residential=true")
        host = f"{'.'.join(options)}:{quote(parts.password, safe='')}@{parts.hostname}"
        if parts.port:
            host += f":{parts.port}"
        return urlunsplit((parts.scheme, host, parts.path, parts.query, parts.fragment))

    @staticmethod
    def _page_url(url: str, page: int) -> str:
        parts = urlsplit(url)
        path = re.sub(r"-oa\d+-", "-", parts.path)
        if page > 1:
            path = path.replace("-Hotels.html", f"-oa{(page - 1) * 30}-Hotels.html")
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))

    @classmethod
    def _bootstrap(cls, text: str, url: str = "response") -> tuple[list[dict], dict]:
        lowered = text[:250000].lower()
        markers = ("captcha", "access denied", "failed to get successful response", "px-captcha")
        if len(text) < 5000 or any(marker in lowered for marker in markers):
            raise RuntimeError(f"Tripadvisor challenge/proxy response at {url}")
        selector = scrapy.Selector(text=text)
        decoder = json.JSONDecoder()
        for src in selector.css('script[src^="data:text/javascript,"]::attr(src)').getall():
            decoded = unquote(src.split(",", 1)[1])
            marker = "JSON.parse("
            offset = decoded.find(marker)
            if offset < 0:
                continue
            try:
                encoded, _ = decoder.raw_decode(decoded[offset + len(marker):])
                outer = json.loads(encoded)
            except (json.JSONDecodeError, TypeError):
                continue
            results = ((outer.get("urqlSsrData") or {}).get("results") or {})
            for value in results.values():
                try:
                    payload = json.loads(value["data"])
                except (KeyError, TypeError, json.JSONDecodeError):
                    continue
                listing = payload.get("list")
                if isinstance(listing, dict) and isinstance(listing.get("results"), list):
                    return listing["results"], listing
        raise RuntimeError(f"Tripadvisor response has no hotel URQL bootstrap at {url}")

    @staticmethod
    def _price(value):
        if not value:
            return None
        match = re.search(r"[\d,.]+", str(value))
        return float(match.group().replace(",", "")) if match else None

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Tripadvisor returned HTTP {response.status}: {response.url}")
        hotels, listing = self._bootstrap(response.text, response.url)
        page = int(response.meta.get("page", 1))
        new_count = 0
        for position, hotel in enumerate(hotels, 1):
            location = hotel.get("location") or {}
            detail = location.get("locationV2") or {}
            item_id = str(hotel.get("locationId") or detail.get("locationId") or "").strip()
            if not item_id or item_id in self.seen:
                continue
            self.seen.add(item_id)
            new_count += 1
            names = detail.get("names") or {}
            contact = detail.get("contact") or {}
            address = contact.get("streetAddress") or {}
            geo = detail.get("geocode") or {}
            reviews = location.get("reviewSummary") or {}
            thumbnail = ((location.get("thumbnail") or {}).get("photoSizeDynamic") or {})
            result_detail = hotel.get("resultDetail") or {}
            meta = result_detail.get("hotelMetaResult") or {}
            rank = (detail.get("hotelHierarchicalPopIndex") or {}).get("rank")
            amenities = [x.get("amenityName") for x in
                         (result_detail.get("amenities") or {}).get("highlightedAmenities") or []
                         if x.get("amenityName")]
            labels = [x.get("text") for x in result_detail.get("merchandisingLabels") or [] if x.get("text")]
            image = thumbnail.get("urlTemplate")
            if image:
                image = image.replace("{width}", "1200").replace("{height}", "-1")
            yield {
                "category": self.category, "item_id": item_id,
                "title": names.get("name"), "url": urljoin("https://www.tripadvisor.com", location.get("url") or ""),
                "rating": reviews.get("rating"), "review_count": reviews.get("count"),
                "price": self._price(meta.get("lowestPrice")), "currency": "USD",
                "address": address.get("fullAddress"), "city": address.get("city") or names.get("parentGeo"),
                "country": address.get("country"), "postal_code": address.get("postalCode"),
                "latitude": geo.get("latitude"), "longitude": geo.get("longitude"),
                "phone": contact.get("telephone"), "image_url": image,
                "accommodation_type": (detail.get("accommodationType") or {}).get("name"),
                "star_rating": detail.get("starRating"), "rank": rank,
                "amenities": amenities, "labels": labels, "page": page, "position": position,
                "source": "tripadvisor_urql_bootstrap", "raw": hotel, "timestamp": self.job_timestamp,
            }
        if page < self.max_pages and hotels and new_count:
            yield self._request(response.meta["base_url"], page + 1)
