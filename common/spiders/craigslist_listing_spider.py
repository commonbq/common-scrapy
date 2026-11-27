from __future__ import annotations

"""Craigslist NYC classifieds listing spider.

Server-rendered HTML with JSON-LD ItemList fallback.

Usage examples:
  scrapy crawl craigslist_listing -a category=antiques -a max_pages=1 \
    -s HTTPCACHE_ENABLED=False -s PROXY=http://scrapeops.country=us:***@proxy.scrapeops.io:5353
"""

from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class CraigslistListingSpider(BaseListingSpider):
    name = "craigslist_listing"
    allowed_domains = ["newyork.craigslist.org", "craigslist.org"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "id",
            "title",
            "price",
            "price_currency",
            "location",
            "image_urls",
            "category",
            "position",
            "listing_url",
            "raw",
            "timestamp",
        ],
    }

    categories = {
        "all_for_sale": "https://newyork.craigslist.org/search/sss",
        "antiques": "https://newyork.craigslist.org/search/ata",
        "appliances": "https://newyork.craigslist.org/search/ppa",
        "arts_crafts": "https://newyork.craigslist.org/search/ara",
        "atv_utv_sno": "https://newyork.craigslist.org/search/sna",
        "auto_parts": "https://newyork.craigslist.org/search/pta",
        "aviation": "https://newyork.craigslist.org/search/ava",
        "baby_kid": "https://newyork.craigslist.org/search/baa",
        "barter": "https://newyork.craigslist.org/search/bar",
        "beauty_hlth": "https://newyork.craigslist.org/search/haa",
        "bike_parts": "https://newyork.craigslist.org/search/bip",
        "bikes": "https://newyork.craigslist.org/search/bia",
        "boat_parts": "https://newyork.craigslist.org/search/bpa",
        "boats": "https://newyork.craigslist.org/search/boo",
        "books": "https://newyork.craigslist.org/search/bka",
        "business": "https://newyork.craigslist.org/search/bfa",
        "cars_trucks": "https://newyork.craigslist.org/search/cta",
        "cds_dvd_vhs": "https://newyork.craigslist.org/search/ema",
        "cell_phones": "https://newyork.craigslist.org/search/moa",
        "clothes_acc": "https://newyork.craigslist.org/search/cla",
        "collectibles": "https://newyork.craigslist.org/search/cba",
        "computer_parts": "https://newyork.craigslist.org/search/syp",
        "computers": "https://newyork.craigslist.org/search/sya",
        "electronics": "https://newyork.craigslist.org/search/ela",
        "farm_garden": "https://newyork.craigslist.org/search/gra",
        "free": "https://newyork.craigslist.org/search/zip",
        "furniture": "https://newyork.craigslist.org/search/fua",
        "garage_sale": "https://newyork.craigslist.org/search/gms",
        "general": "https://newyork.craigslist.org/search/foa",
        "heavy_equip": "https://newyork.craigslist.org/search/hva",
        "household": "https://newyork.craigslist.org/search/hsa",
        "jewelry": "https://newyork.craigslist.org/search/jwa",
        "materials": "https://newyork.craigslist.org/search/maa",
        "motorcycle_parts": "https://newyork.craigslist.org/search/mpa",
        "motorcycles": "https://newyork.craigslist.org/search/mca",
        "music_instr": "https://newyork.craigslist.org/search/msa",
        "photo_video": "https://newyork.craigslist.org/search/pha",
        "rvs_camp": "https://newyork.craigslist.org/search/rva",
        "sporting": "https://newyork.craigslist.org/search/sga",
        "tickets": "https://newyork.craigslist.org/search/tia",
        "tools": "https://newyork.craigslist.org/search/tla",
        "toys_games": "https://newyork.craigslist.org/search/taa",
        "trailers": "https://newyork.craigslist.org/search/tra",
        "video_gaming": "https://newyork.craigslist.org/search/vga",
        "wanted": "https://newyork.craigslist.org/search/waa",
        "wheels_tires": "https://newyork.craigslist.org/search/wta",
    }

    @staticmethod
    def _ensure_nosplash(url: str) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        qs["intl"] = ["nosplash"]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def start_requests(self):
        category_url = self.categories.get(self.category)
        if not category_url:
            available = ", ".join(self.categories.keys())
            raise ValueError(
                f"Unknown category '{self.category}'. Use one of: {available}"
            )
        target = self._ensure_nosplash(category_url)
        yield scrapy.Request(
            target,
            callback=self.parse_listing_page,
            meta={"page": 1},
        )

    def parse_listing_page(self, response: scrapy.http.Response):
        page_num = int(response.meta.get("page", 1))
        self.logger.info(f"Parsing page {page_num}: {response.url}")

        # Primary: extract from JSON-LD ItemList embedded in the page
        items = self._extract_from_json_ld(response)
        self.logger.info(f"Extracted {len(items)} items from JSON-LD")
        if items:
            for idx, item in enumerate(items):
                yield self._format_item(item, page_num, idx + 1)
        else:
            self.logger.warning("JSON-LD extraction returned 0 items, trying HTML cards")
            # Fallback: extract from HTML cards
            items = self._extract_from_html_cards(response)
            self.logger.info(f"Extracted {len(items)} items from HTML cards")
            for idx, item in enumerate(items):
                yield self._format_item(item, page_num, idx + 1)

        # Pagination: follow rel=next link
        next_url = self._get_next_page_url(response)
        if next_url:
            yield scrapy.Request(
                next_url,
                callback=self.parse_listing_page,
                meta={"page": page_num + 1},
            )

    def _extract_from_json_ld(self, response: scrapy.http.Response):
        """Extract items from <script type="application/ld+json" id="ld_searchpage_results">."""
        import json

        ld_script = response.css(
            'script[type="application/ld+json"]#ld_searchpage_results::text'
        ).get()
        if not ld_script:
            return []

        try:
            data = json.loads(ld_script)
        except (json.JSONDecodeError, TypeError):
            return []

        # Expected shape: {"itemListElement": [{"@type": "ListItem", "item": {"@type": "Product", ...}}, ...]}
        items_list = data.get("itemListElement", [])
        if not isinstance(items_list, list):
            return []

        results = []
        for entry in items_list:
            if not isinstance(entry, dict) or entry.get("@type") != "ListItem":
                continue
            item_data = entry.get("item", {})
            if not isinstance(item_data, dict) or item_data.get("@type") != "Product":
                continue
            item = {}
            offers = item_data.get("offers", {})
            if isinstance(offers, dict):
                item["price"] = offers.get("price")
                item["price_currency"] = offers.get("priceCurrency")
            else:
                item["price"] = None
                item["price_currency"] = None

            item["title"] = item_data.get("name")
            item["image_urls"] = item_data.get("image", []) or []
            item["id"] = item_data.get("itemId") or item_data.get("id")
            item["description"] = item_data.get("description") or ""

            # Extract location from geo coordinates if available
            geo = offers.get("availableAtOrFrom", {}).get("geo", {}) or {}
            item["location"] = (
                f"{geo.get('latitude', '')}, {geo.get('longitude', '')}"
                if geo.get("latitude") and geo.get("longitude")
                else None
            )

            results.append(item)

        return results

    def _extract_from_html_cards(self, response: scrapy.http.Response):
        """Fallback: extract from <li class="cl-static-search-result"> cards."""
        results = []
        for card in response.css("li.cl-static-search-result"):
            # Listing ID from the detail link slug
            link = card.css("a::attr(href)").get()
            listing_id = None
            if link:
                # e.g., /view/d/brooklyn-toshiba-crt-tv-19inch-screen/baw2r8BXuAQnMaZPjfyxsS
                parts = link.strip("/").split("/")
                if len(parts) >= 2:
                    listing_id = parts[-1]

            title = (
                card.css("div.title::text").get()
                or card.css("div::text").get()
                or ""
            ).strip()

            price_text = card.css("div.price::text").get()
            price = None
            if price_text:
                import re
                m = re.search(r"\$?(\d+(?:\.\d{1,2})?)", price_text)
                if m:
                    price = float(m.group(1))

            location_text = card.css("div.location::text").get()
            location = location_text.strip() if location_text else None

            image_urls = []
            img = card.css("img::attr(src)").get()
            if img:
                image_urls = [response.urljoin(img)]

            results.append(
                {
                    "id": listing_id,
                    "title": title or None,
                    "price": price,
                    "price_currency": "USD",
                    "location": location,
                    "image_urls": image_urls,
                    "listing_url": link,
                }
            )
        return results

    def _format_item(self, item: dict, page_num: int, position: int) -> dict:
        """Normalize a scraped item into the standard output format."""
        return {
            "id": item.get("id"),
            "title": item.get("title"),
            "price": item.get("price"),
            "price_currency": item.get("price_currency") or "USD",
            "location": item.get("location"),
            "image_urls": item.get("image_urls", []) or [],
            "category": self.category,
            "position": position,
            "listing_url": item.get("listing_url"),
            "raw": item,
            "timestamp": self.get_timestamp(),
            "page": page_num,
        }

    def _get_next_page_url(self, response: scrapy.http.Response):
        """Find the next page URL from rel=next or pagination offset."""
        # Try rel=next link first
        next_link = response.css('a[rel="next"]::attr(href)').get()
        if next_link:
            return response.urljoin(next_link)

        # Try to find pagination offset from the URL parameters
        # Craigslist uses ?s= offset parameter
        parsed = urlparse(response.url)
        qs = parse_qs(parsed.query)
        current_s = qs.get("s", [0])[0]
        try:
            next_s = int(current_s) + 25  # 25 items per page on Craigslist
        except (ValueError, TypeError):
            return None

        qs["s"] = [str(next_s)]
        new_query = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=new_query))