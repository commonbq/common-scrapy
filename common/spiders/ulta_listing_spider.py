from __future__ import annotations

import json
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class UltaListingSpider(BaseListingSpider):
    """Ulta category listing spider.

    Modes:
    - default/graphql: Ulta GraphQL APIs (/dxl/graphql)
    - html: direct HTML card parsing

    Examples:
    - scrapy crawl ulta_listing -a category='shampoo' -a max_pages=1
    - scrapy crawl ulta_listing -a category='shampoo' -a mode=html -a max_pages=1
    """

    name = "ulta_listing"
    allowed_domains = ["ulta.com", "www.ulta.com"]

    custom_settings = {
        "HTTPERROR_ALLOW_ALL": True,
    }

    categories = [
        {"category": "shampoo", "url": "https://www.ulta.com/shop/hair/shampoo-conditioner/shampoo"},
        {"category": "conditioner", "url": "https://www.ulta.com/shop/hair/shampoo-conditioner/conditioner"},
        {"category": "cleanser", "url": "https://www.ulta.com/shop/makeup/face/foundation/face-primer"},
        {"category": "mascara", "url": "https://www.ulta.com/shop/makeup/eyes/mascara"},
        {"category": "moisturizer", "url": "https://www.ulta.com/shop/skin-care/moisturizers"},
    ]

    module_params = {
        "gti": "4c5ae407-6d39-4bc2-8b88-c3c73b90c19c",
        "loginStatus": "anonymous",
        "retailerVisitorId": "bff8c299-5cd1-4012-ae07-2c4ce39c6e45",
        "breakpoint": "LG",
    }

    def start_requests(self):
        mode = (getattr(self, "mode", None) or "graphql").strip().lower()
        target = self.resolve_target_url()

        if mode == "html":
            first = self._with_page(target, 1)
            yield scrapy.Request(first, callback=self.parse_html_listing, meta=self.proxy_meta({"page": 1, "mode": "html", "origin": target}))
            return

        page_query = (
            'query Page($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON, $url: JSON) '
            '{ Page: Page(stagingHost: $stagingHost, previewOptions: $previewOptions, '
            'moduleParams: $moduleParams, url: $url, deliveryKey: "SDK") '
            '{ content customResponseAttributes meta __typename } }'
        )
        variables = {"moduleParams": {}, "url": {"path": target}}
        url = self._build_graphql_get_url(page_query, "Page", variables)
        yield scrapy.Request(
            url,
            callback=self.parse_page_definition,
            headers=self._headers(),
            meta=self.proxy_meta({"page": 1, "mode": "graphql"}),
        )

    def parse_page_definition(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        if not payload:
            self.logger.warning("Ulta Page query failed")
            return

        modules = payload.get("data", {}).get("Page", {}).get("content", {}).get("modules", [])

        content_id = None
        for m in modules:
            if isinstance(m, dict) and m.get("type") == "ProductListingResults":
                content_id = m.get("id")
                break

        if not content_id:
            self.logger.warning("Could not locate ProductListingResults contentId")
            return

        first_url = self._build_noncached_url(content_id=content_id, page=1)
        yield scrapy.Request(
            first_url,
            callback=self.parse_listing,
            headers=self._headers(),
            meta=self.proxy_meta({"content_id": content_id, "page": 1}),
        )

    def parse_listing(self, response: scrapy.http.Response):
        payload = self._to_json(response)
        if not payload:
            self.logger.warning("Ulta NonCachedPage query failed for page=%s", response.meta.get("page"))
            return

        content = payload.get("data", {}).get("Page", {}).get("content", {})
        items = content.get("items", []) or []

        for item in items:
            action = item.get("action") or {}
            rating_raw = item.get("rating")
            review_raw = item.get("reviewCount")

            yield {
                "item_id": item.get("productId"),
                "sku_id": item.get("skuId"),
                "brand": item.get("brandName"),
                "title": item.get("productName"),
                "url": action.get("url"),
                "image_url": self._extract_image_url(item),
                "list_price": item.get("listPrice"),
                "sale_price": item.get("salePrice"),
                "rating": self._to_float(rating_raw),
                "reviews_count": self._to_int(review_raw),
                "is_sponsored": bool(item.get("sponsored")),
                "source": "ulta_dxl_graphql",
                "mode": "category",
                "category_url": self.resolve_target_url(),
            }

        current_page = int(response.meta.get("page", 1))
        if current_page >= self.max_pages or not items:
            return

        next_page = current_page + 1
        content_id = response.meta.get("content_id")
        next_url = self._build_noncached_url(content_id=content_id, page=next_page)
        yield scrapy.Request(
            next_url,
            callback=self.parse_listing,
            headers=self._headers(),
            meta=self.proxy_meta({"content_id": content_id, "page": next_page}),
        )

    def parse_html_listing(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        seen: set[str] = set()
        yielded = 0

        anchors = response.xpath('//a[contains(@href,"/p/")]')
        for a in anchors:
            href = (a.attrib.get("href") or "").strip()
            if "/p/" not in href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)

            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            title = " ".join(card.xpath('.//text()').getall()).strip() if card else ""
            title = re.sub(r"\s+", " ", title)
            img = (card.xpath('.//img/@src').get() if card else None) or (card.xpath('.//img/@data-src').get() if card else None)

            prices = re.findall(r"\$\d+(?:\.\d{2})?(?:\s*-\s*\$\d+(?:\.\d{2})?)?", title)
            list_price = prices[0] if prices else None
            sale_price = None
            if len(prices) > 1:
                sale_price = prices[0]
                list_price = prices[1]

            sku_match = re.search(r"[?&]sku=(\d+)", url)
            item_id = sku_match.group(1) if sku_match else None

            yield {
                "item_id": item_id,
                "sku_id": item_id,
                "brand": None,
                "title": title or None,
                "url": url,
                "image_url": img,
                "list_price": list_price,
                "sale_price": sale_price,
                "rating": None,
                "reviews_count": None,
                "is_sponsored": False,
                "source": "ulta_direct_html",
                "mode": "category_html",
                "category_url": response.meta.get("origin") or self.resolve_target_url(),
                "page": page,
            }
            yielded += 1

        if yielded == 0:
            self.logger.warning("Ulta HTML mode yielded 0 items (status=%s)", response.status)

        if page >= self.max_pages:
            return
        next_page = page + 1
        origin = response.meta.get("origin") or self.resolve_target_url()
        next_url = self._with_page(origin, next_page)
        yield scrapy.Request(next_url, callback=self.parse_html_listing, meta=self.proxy_meta({"page": next_page, "mode": "html", "origin": origin}))

    def _build_noncached_url(self, content_id: str, page: int) -> str:
        base_path = self.resolve_target_url()
        path = base_path if page == 1 else f"{base_path}&page={page}"

        query = (
            'query NonCachedPage($stagingHost: String, $previewOptions: JSON, $moduleParams: JSON) '
            '{ Page: NonCachedPage(stagingHost:$stagingHost, previewOptions:$previewOptions, '
            'moduleParams:$moduleParams, url: {path: "'
            + path
            + '"}, contentId: "'
            + content_id
            + '") { content customResponseAttributes meta __typename } }'
        )

        variables = {"moduleParams": self.module_params}
        return self._build_graphql_get_url(query, "NonCachedPage", variables)

    def _build_graphql_get_url(self, query: str, operation_name: str, variables: dict) -> str:
        params = {
            "ultasite": "en-us",
            "user-agent": "gomez",
            "query": query,
            "operationName": operation_name,
            "variables": json.dumps(variables, separators=(",", ":")),
        }
        return f"https://www.ulta.com/dxl/graphql?{urlencode(params)}"

    def _headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0",
            "accept": "application/json,text/plain,*/*",
            "content-type": "application/json",
        }

    def _to_json(self, response: scrapy.http.Response) -> dict | None:
        try:
            return json.loads(response.text)
        except Exception:
            return None

    def _extract_image_url(self, item: dict) -> str | None:
        for key in ("image", "altImage"):
            img = item.get(key)
            if isinstance(img, dict):
                if img.get("imageUrl"):
                    return img.get("imageUrl")
            elif isinstance(img, str):
                return img
        return None

    @staticmethod
    def _with_page(url: str, page: int) -> str:
        parts = urlparse(url)
        qs = parse_qs(parts.query)
        if page > 1:
            qs["page"] = [str(page)]
        return urlunparse(parts._replace(query=urlencode(qs, doseq=True)))

    def _to_float(self, value):
        try:
            return float(value)
        except Exception:
            return None

    def _to_int(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        try:
            return int(value)
        except Exception:
            return None
