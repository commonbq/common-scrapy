from __future__ import annotations

"""Zillow sale listings from server-rendered Next.js hydration only."""

import json
from urllib.parse import urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider
from common.spiders.zillow_categories import ZILLOW_CATEGORIES


class ZillowListingSpider(BaseListingSpider):
    name = "zillow_listing"
    allowed_domains = ["zillow.com", "www.zillow.com"]
    categories = ZILLOW_CATEGORIES
    require_category_arg = False
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id", "title", "url", "image_url", "price", "price_display",
            "currency", "address", "street", "city", "state", "postal_code",
            "beds", "baths", "area", "status", "status_text", "home_type",
            "latitude", "longitude", "zestimate", "rent_zestimate", "broker",
            "days_on_zillow", "time_on_zillow", "listing_sub_type", "has_3d_model",
            "category", "region_id", "region_name", "page", "position",
            "total_count", "source", "raw", "timestamp",
        ],
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError("Provide category, category_url, or url")
        self.seen = set()

    def start_requests(self):
        yield self._request(self.resolve_target_url(), 1)

    def _request(self, base_url, page):
        settings = getattr(self, "settings", {})
        return scrapy.Request(
            self._page_url(base_url, page), callback=self.parse, headers=self.headers,
            meta={"proxy": settings.get("PROXY"), "page": page, "base_url": base_url},
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url, page):
        if page <= 1:
            return url
        parts = urlsplit(url)
        path = parts.path.rstrip("/")
        if path.rsplit("/", 1)[-1].endswith("_p"):
            path = path.rsplit("/", 1)[0]
        return urlunsplit((parts.scheme, parts.netloc, f"{path}/{page}_p/", parts.query, parts.fragment))

    @staticmethod
    def _state(text, url="response"):
        lowered = text.lower()
        if any(marker in lowered for marker in ("failed to get successful response", "pardon the interruption", "px-captcha")):
            raise RuntimeError(f"Zillow challenge/proxy error at {url}")
        selector = scrapy.Selector(text=text)
        raw = selector.css("script#__NEXT_DATA__::text").get()
        if not raw:
            raise RuntimeError(f"Zillow response has no __NEXT_DATA__ at {url}")
        try:
            data = json.loads(raw)
            if data.get("props", {}).get("isBot") is True:
                raise RuntimeError(f"Zillow bot response at {url}")
            return data["props"]["pageProps"]["searchPageState"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Invalid Zillow hydration at {url}: {exc}") from exc

    def parse(self, response):
        if response.status != 200:
            raise RuntimeError(f"Zillow returned HTTP {response.status}: {response.url}")
        state = self._state(response.text, response.url)
        results = state.get("cat1", {}).get("searchResults", {}).get("listResults")
        if not isinstance(results, list):
            raise RuntimeError(f"Zillow hydration has no cat1 listResults at {response.url}")
        page = int(response.meta["page"])
        region = (state.get("regionState", {}).get("regionInfo") or [{}])[0]
        total = state.get("categoryTotals", {}).get("cat1", {}).get("totalResultCount")
        new_count = 0
        for position, product in enumerate(results, 1):
            zpid = str(product.get("zpid") or "").strip()
            if not zpid or zpid in self.seen:
                continue
            self.seen.add(zpid); new_count += 1
            home = product.get("hdpData", {}).get("homeInfo", {})
            latlong = product.get("latLong") or {}
            yield {
                "item_id": zpid, "title": product.get("address"),
                "url": urljoin("https://www.zillow.com", product.get("detailUrl") or ""),
                "image_url": product.get("imgSrc"), "price": product.get("unformattedPrice"),
                "price_display": product.get("price"), "currency": product.get("countryCurrency"),
                "address": product.get("address"), "street": product.get("addressStreet"),
                "city": product.get("addressCity"), "state": product.get("addressState"),
                "postal_code": product.get("addressZipcode"), "beds": product.get("beds"),
                "baths": product.get("baths"), "area": product.get("area"),
                "status": product.get("statusType"), "status_text": product.get("statusText"),
                "home_type": home.get("homeType"), "latitude": latlong.get("latitude"),
                "longitude": latlong.get("longitude"), "zestimate": product.get("zestimate"),
                "rent_zestimate": home.get("rentZestimate"), "broker": product.get("brokerName"),
                "days_on_zillow": home.get("daysOnZillow"), "time_on_zillow": home.get("timeOnZillow"),
                "listing_sub_type": home.get("listing_sub_type"), "has_3d_model": product.get("has3DModel"),
                "category": self.category or "custom", "region_id": region.get("regionId"),
                "region_name": region.get("displayName") or region.get("regionName"),
                "page": page, "position": position, "total_count": total,
                "source": "zillow_next_data", "raw": product,
                "timestamp": self.job_timestamp,
            }
        if page < self.max_pages and results and new_count == len(results):
            yield self._request(response.meta["base_url"], page + 1)
