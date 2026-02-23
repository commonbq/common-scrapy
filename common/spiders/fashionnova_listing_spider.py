from __future__ import annotations

import json
import re

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class FashionnovaListingSpider(BaseListingSpider):
    """FashionNova listing spider.

    Mode priority:
    - api (default): Shopify Storefront GraphQL
    - html: product link/card fallback parser
    """

    name = "fashionnova_listing"
    allowed_domains = ["fashionnova.com", "www.fashionnova.com"]

    categories = [
        {"category": "women", "url": "https://www.fashionnova.com/collections/women", "handle": "women"},
        {"category": "new", "url": "https://www.fashionnova.com/collections/new", "handle": "new"},
        {"category": "dresses", "url": "https://www.fashionnova.com/collections/dresses", "handle": "dresses"},
        {"category": "jeans", "url": "https://www.fashionnova.com/collections/jeans", "handle": "jeans"},
        {"category": "sale", "url": "https://www.fashionnova.com/collections/sale", "handle": "sale"},
    ]

    def start_requests(self):
        mode = (getattr(self, "mode", None) or "api").strip().lower()
        if mode == "html":
            yield scrapy.Request(self.resolve_target_url(), callback=self.parse_html, meta={"page": 1})
            return

        yield self._api_request(cursor=None, page=1)

    def _api_request(self, cursor: str | None, page: int):
        handle = self._category_handle()
        query = """
        query CollectionProducts($handle: String!, $first: Int!, $after: String) {
          collection(handle: $handle) {
            products(first: $first, after: $after) {
              pageInfo { hasNextPage endCursor }
              edges {
                node {
                  id
                  title
                  handle
                  vendor
                  onlineStoreUrl
                  featuredImage { url }
                  priceRange { minVariantPrice { amount currencyCode } }
                }
              }
            }
          }
        }
        """
        payload = {
            "query": query,
            "variables": {"handle": handle, "first": 48, "after": cursor},
        }
        return scrapy.Request(
            "https://www.fashionnova.com/api/unstable/graphql.json",
            method="POST",
            body=json.dumps(payload),
            headers={"content-type": "application/json", "accept": "application/json", "user-agent": "Mozilla/5.0"},
            callback=self.parse_api,
            meta={"page": page},
        )

    def parse_api(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        data = self._to_json(response)
        if not isinstance(data, dict):
            self.logger.warning("fashionnova api non-json status=%s", response.status)
            return

        products = (((data.get("data") or {}).get("collection") or {}).get("products") or {})
        edges = products.get("edges") or []
        for edge in edges:
            node = (edge or {}).get("node") or {}
            pr = ((node.get("priceRange") or {}).get("minVariantPrice") or {})
            gid = node.get("id")
            item_id = None
            if isinstance(gid, str):
                item_id = gid.rsplit("/", 1)[-1]

            url = node.get("onlineStoreUrl")
            if not url and node.get("handle"):
                url = f"https://www.fashionnova.com/products/{node.get('handle')}"

            yield {
                "item_id": item_id,
                "title": node.get("title"),
                "url": url,
                "price": self._to_float(pr.get("amount")),
                "currency": pr.get("currencyCode"),
                "brand": node.get("vendor"),
                "rating": None,
                "reviews_count": None,
                "image_url": (node.get("featuredImage") or {}).get("url"),
                "source": "fashionnova_storefront_graphql",
                "mode": "category",
                "category_url": self.resolve_target_url(),
                "page": page,
            }

        page_info = products.get("pageInfo") or {}
        if page >= self.max_pages:
            return
        if page_info.get("hasNextPage") and page_info.get("endCursor"):
            yield self._api_request(cursor=page_info.get("endCursor"), page=page + 1)

    def parse_html(self, response: scrapy.http.Response):
        page = int(response.meta.get("page", 1))
        seen: set[str] = set()
        for a in response.xpath('//a[contains(@href,"/products/")]'):
            href = (a.attrib.get("href") or "").strip()
            if not href:
                continue
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)
            card = a.xpath('ancestor::*[self::article or self::li or self::div][1]')
            text = " ".join(card.xpath('.//text()').getall()) if card else ""
            text = re.sub(r"\s+", " ", text).strip()
            m = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
            price = float(m.group(1)) if m else None
            img = (card.xpath('.//img/@src').get() if card else None) or (card.xpath('.//img/@data-src').get() if card else None)
            yield {
                "item_id": url.rstrip('/').split('/')[-1],
                "title": text or None,
                "url": url,
                "price": price,
                "currency": "USD" if price is not None else None,
                "brand": "Fashion Nova",
                "rating": None,
                "reviews_count": None,
                "image_url": img,
                "source": "fashionnova_html",
                "mode": "category_html",
                "category_url": self.resolve_target_url(),
                "page": page,
            }

    def _category_handle(self) -> str:
        if self.category:
            for c in self.categories:
                if c.get("category") == self.category:
                    return c.get("handle")
        url = self.resolve_target_url()
        m = re.search(r"/collections/([^/?#]+)", url)
        if m:
            return m.group(1)
        raise ValueError("Provide -a category=<name> for fashionnova_listing")

    @staticmethod
    def _to_json(response: scrapy.http.Response):
        try:
            return json.loads(response.text)
        except Exception:
            return None

    @staticmethod
    def _to_float(v):
        try:
            return float(v)
        except Exception:
            return None
