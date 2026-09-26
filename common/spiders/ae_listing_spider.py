from __future__ import annotations

import base64
import binascii
import json
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class AeListingSpider(BaseListingSpider):
    """American Eagle listing spider."""

    name = "ae_listing"
    allowed_domains = ["ae.com", "www.ae.com"]

    AE_CATEGORIES = {
        "women": {
            "all": "https://www.ae.com/us/en/c/women/womens",
            "jeans": "https://www.ae.com/us/en/c/women/bottoms/jeans/cat6430042",
            "tops": "https://www.ae.com/us/en/c/women/tops/cat10049",
            "bottoms": "https://www.ae.com/us/en/c/women/bottoms/cat10051",
            "pants-sweatpants": "https://www.ae.com/us/en/c/women/bottoms/pants-sweatpants/cat90034",
            "t-shirts": "https://www.ae.com/us/en/c/women/tops/t-shirts/cat90030",
            "hoodies-sweatshirts": "https://www.ae.com/us/en/c/women/tops/hoodies-sweatshirts/cat90048",
            "sweaters-cardigans": "https://www.ae.com/us/en/c/women/tops/sweaters-cardigans/cat1410002",
            "dresses-jumpsuits": "https://www.ae.com/us/en/c/women/dresses/cat1320034",
            "loungewear-pjs": "https://www.ae.com/us/en/c/women/loungewear-pjs/cat730011",
            "jackets-vests": "https://www.ae.com/us/en/c/women/tops/jackets-vests/cat4260032",
            "accessories-socks": "https://www.ae.com/us/en/c/women/accessories-socks/cat4840018",
            "shoes": "https://www.ae.com/us/en/c/women/shoes/cat4840020",
            "clearance": "https://www.ae.com/us/en/c/women/clearance/clrwomens",
        },
        "men": {
            "all": "https://www.ae.com/us/en/c/men/mens",
            "jeans": "https://www.ae.com/us/en/c/men/bottoms/jeans/cat6430041",
            "tops": "https://www.ae.com/us/en/c/men/tops/cat10025",
            "bottoms": "https://www.ae.com/us/en/c/men/bottoms/cat10027",
            "hoodies-sweatshirts": "https://www.ae.com/us/en/c/men/tops/hoodies-sweatshirts/cat90020",
            "t-shirts": "https://www.ae.com/us/en/c/men/tops/t-shirts/cat90012",
            "shirts-flannels": "https://www.ae.com/us/en/c/men/tops/shirts-flannels/cat40005",
            "underwear": "https://www.ae.com/us/en/c/men/underwear/cat10032",
            "activewear": "https://www.ae.com/us/en/c/men/activewear/cat1100008",
            "loungewear-pjs": "https://www.ae.com/us/en/c/men/loungewear-pjs/cat130005",
            "jackets": "https://www.ae.com/us/en/c/men/tops/jackets/cat380145",
            "accessories-socks": "https://www.ae.com/us/en/c/men/accessories-socks/cat4840022",
            "shoes": "https://www.ae.com/us/en/c/men/shoes/cat4840024",
            "clearance": "https://www.ae.com/us/en/c/men/clearance/clrmens",
        },
        "aerie": {
            "all": "https://www.ae.com/us/en/c/aerie/clothing-accessories/cat870009",
        },
    }

    categories = {
        f"{section}-{name}": url
        for section, values in AE_CATEGORIES.items()
        for name, url in values.items()
    }

    custom_settings = {"HTTPERROR_ALLOW_ALL": True, "DOWNLOAD_DELAY": 1}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._seen_products: set[str] = set()

    def available_categories(self) -> list[str]:
        return sorted(self.categories)

    def resolve_target_url(self) -> str:
        if self.url or self.category_url:
            return self.url or self.category_url
        if self.category in self.categories:
            return self.categories[self.category]
        available = ", ".join(self.available_categories())
        raise ValueError(
            f"Unknown category '{self.category}'. Available categories: {available}"
        )

    def start_requests(self):
        target = self.resolve_target_url()
        yield scrapy.Request(
            target,
            callback=self.parse_html,
            headers=self._headers(referer=target, wants_json=False),
            meta={"page": 1, "category": self.category, "category_url": target},
        )

    def parse_html(self, response: scrapy.http.Response):
        browse_path, payload = self._extract_shoebox_payload(response)
        if not browse_path or not payload:
            self.logger.warning(
                "AE shoebox payload unavailable (status=%s url=%s)",
                response.status,
                response.url,
            )
            return
        yield from self._yield_products(
            payload,
            page=int(response.meta.get("page", 1)),
            category=response.meta.get("category"),
            category_url=response.meta.get("category_url") or response.url,
        )
        next_request = self._build_next_request(
            payload=payload,
            page=int(response.meta.get("page", 1)),
            browse_path=browse_path,
            category=response.meta.get("category"),
            category_url=response.meta.get("category_url") or response.url,
            reference_url=response.url,
        )
        if next_request:
            yield next_request

    def parse_browse(self, response: scrapy.http.Response):
        payload = self._json_obj(response.text)
        if not payload:
            self.logger.warning(
                "AE browse payload invalid (status=%s url=%s)",
                response.status,
                response.url,
            )
            return
        page = int(response.meta.get("page", 1))
        yield from self._yield_products(
            payload,
            page=page,
            category=response.meta.get("category"),
            category_url=response.meta.get("category_url") or response.url,
        )
        next_request = self._build_next_request(
            payload=payload,
            page=page,
            browse_path=response.meta.get("browse_path"),
            category=response.meta.get("category"),
            category_url=response.meta.get("category_url") or response.url,
            reference_url=response.meta.get("category_url") or response.url,
        )
        if next_request:
            yield next_request

    @classmethod
    def _extract_shoebox_payload(
        cls, response: scrapy.http.Response
    ) -> tuple[str | None, dict | None]:
        for script in response.xpath('//script[@type="fastboot/shoebox"]'):
            encoded = (script.attrib.get("id") or "").strip()
            path = cls._decode_shoebox_id(encoded)
            if not path.startswith("/browse/v1/category/"):
                continue
            payload = cls._json_obj(script.xpath("text()").get())
            if payload:
                return path, payload
        return None, None

    @staticmethod
    def _decode_shoebox_id(encoded: str) -> str:
        if not encoded:
            return ""
        padded = encoded + ("=" * ((4 - len(encoded) % 4) % 4))
        try:
            return base64.urlsafe_b64decode(padded.encode()).decode("utf-8")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            return ""

    @staticmethod
    def _json_obj(raw: str | None) -> dict | None:
        if not raw:
            return None
        try:
            payload = json.loads(raw)
        except (TypeError, ValueError):
            return None
        return payload if isinstance(payload, dict) else None

    def _yield_products(
        self, payload: dict, *, page: int, category: str | None, category_url: str
    ):
        for entry in payload.get("included") or []:
            if not isinstance(entry, dict) or entry.get("type") != "product":
                continue
            attrs = entry.get("attributes")
            if not isinstance(attrs, dict):
                continue
            url = attrs.get("url")
            if not isinstance(url, str) or not url:
                continue
            canonical_url = category_url if url == "/" else urljoin(category_url, url)
            item_id = self._item_id(entry, attrs, canonical_url)
            if item_id in self._seen_products:
                continue
            self._seen_products.add(item_id)
            yield {
                "item_id": item_id,
                "title": attrs.get("displayName"),
                "url": canonical_url,
                "price": self._to_float(attrs.get("salePrice")),
                "original_price": self._to_float(attrs.get("listPrice")),
                "currency": "USD",
                "brand": attrs.get("brand") or "American Eagle",
                "rating": self._to_float(attrs.get("rating")),
                "reviews_count": self._to_int(attrs.get("reviewCount")),
                "image_url": self._image_url(attrs, category_url),
                "category": category,
                "category_url": category_url,
                "page": page,
                "source": "ae_fastboot_shoebox",
                "mode": "browse_api",
                "raw": None,
            }

    @staticmethod
    def _item_id(entry: dict, attrs: dict, canonical_url: str) -> str:
        for value in (
            attrs.get("id"),
            entry.get("id"),
            attrs.get("productCode"),
            canonical_url.rstrip("/").split("/")[-1],
        ):
            if isinstance(value, str) and value:
                return value
        return canonical_url

    @staticmethod
    def _to_float(value):
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            cleaned = value.strip().replace("$", "").replace(",", "")
            if cleaned:
                try:
                    return float(cleaned)
                except ValueError:
                    return None
        return None

    @staticmethod
    def _to_int(value):
        if isinstance(value, bool):
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            cleaned = value.strip().replace(",", "")
            if cleaned.isdigit():
                return int(cleaned)
        return None

    @classmethod
    def _image_url(cls, attrs: dict, category_url: str) -> str | None:
        plp_images = attrs.get("plpImages")
        if isinstance(plp_images, list):
            for image in plp_images:
                if not isinstance(image, dict):
                    continue
                for key in ("url", "imageUrl", "src"):
                    value = image.get(key)
                    if isinstance(value, str) and value:
                        return urljoin(category_url, value)
        return None

    def _build_next_request(
        self,
        *,
        payload: dict,
        page: int,
        browse_path: str | None,
        category: str | None,
        category_url: str,
        reference_url: str,
    ) -> scrapy.Request | None:
        if page >= self.max_pages or not browse_path:
            return None
        meta = payload.get("meta")
        if not isinstance(meta, dict):
            return None
        rows = self._to_int(meta.get("rows")) or 0
        total = self._to_int(meta.get("totalProducts"))
        offset = self._to_int(meta.get("offset")) or 0
        if rows <= 0:
            return None
        next_offset = offset + rows
        if total is not None and next_offset >= total:
            return None
        next_url = self._with_offset_rows(
            urljoin(reference_url, browse_path),
            offset=next_offset,
            rows=rows,
        )
        return scrapy.Request(
            next_url,
            callback=self.parse_browse,
            headers=self._headers(referer=category_url, wants_json=True),
            meta={
                "page": page + 1,
                "category": category,
                "category_url": category_url,
                "browse_path": browse_path,
            },
        )

    @staticmethod
    def _with_offset_rows(url: str, *, offset: int, rows: int) -> str:
        parts = urlparse(url)
        query = parse_qs(parts.query, keep_blank_values=True)
        query["offset"] = [str(max(offset, 0))]
        query["rows"] = [str(max(rows, 1))]
        return urlunparse(parts._replace(query=urlencode(query, doseq=True)))

    @staticmethod
    def _headers(*, referer: str, wants_json: bool) -> dict[str, str]:
        return {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "accept": "application/json,text/plain,*/*"
            if wants_json
            else "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "referer": referer,
            "x-requested-with": "XMLHttpRequest" if wants_json else "fetch",
        }
