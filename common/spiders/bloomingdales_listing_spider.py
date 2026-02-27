from __future__ import annotations

import json
import re
from html import unescape
from urllib.parse import parse_qs, urljoin, urlparse

import scrapy

from common.spiders.base_listing_spider import BaseListingSpider


class BloomingdalesListingSpider(BaseListingSpider):
    """Bloomingdale's listing spider using direct site HTML."""

    name = "bloomingdales_listing"
    allowed_domains = ["bloomingdales.com", "www.bloomingdales.com"]

    categories = [
        {"category": "women", "url": "https://www.bloomingdales.com/shop/womens-apparel?id=2910"},
        {"category": "men", "url": "https://www.bloomingdales.com/shop/mens?id=3864"},
        {"category": "shoes", "url": "https://www.bloomingdales.com/shop/womens-designer-shoes?id=16961"},
        {"category": "beauty", "url": "https://www.bloomingdales.com/shop/makeup-perfume-beauty?id=2921"},
        {"category": "home", "url": "https://www.bloomingdales.com/shop/home?id=3865"},
    ]

    def start_requests(self):
        target_url = self.resolve_target_url()
        for page in range(1, self.max_pages + 1):
            page_url = self._page_url(target_url, page)
            yield scrapy.Request(
                page_url,
                callback=self.parse,
                meta={"page": page},
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                },
            )

    def parse(self, response: scrapy.http.Response):
        products = self._extract_products(response.text)
        seen: set[str] = set()

        for product in products:
            item_id = product.get("item_id")
            if item_id and item_id in seen:
                continue
            if item_id:
                seen.add(item_id)
            yield product

    def _extract_products(self, html_text: str) -> list[dict]:
        state = self._extract_nuxt_state(html_text)
        if not state:
            return self._extract_products_from_initial_state(html_text)

        products_by_id: dict[int, dict] = {}
        url_nodes: list[dict] = []

        for node in state:
            if not isinstance(node, dict):
                continue
            if "id" in node and "detail" in node:
                pid = self._resolve_ref(state, node.get("id"))
                if isinstance(pid, int):
                    products_by_id[pid] = node
            if "productUrl" in node and "productId" in node:
                url_nodes.append(node)

        out: list[dict] = []
        for node in url_nodes:
            raw_url = self._resolve_ref(state, node.get("productUrl"))
            pid = self._resolve_ref(state, node.get("productId"))
            if not isinstance(raw_url, str):
                continue

            product_node = products_by_id.get(pid) if isinstance(pid, int) else None
            detail = self._resolve_ref(state, (product_node or {}).get("detail")) if product_node else {}
            pricing = self._resolve_ref(state, (product_node or {}).get("pricing")) if product_node else {}

            title = self._resolve_ref(state, (detail or {}).get("name")) if isinstance(detail, dict) else None
            price, price_text = self._extract_price(pricing if isinstance(pricing, dict) else {})

            normalized_url = self._normalize_url(raw_url)
            parsed = urlparse(normalized_url)
            q = parse_qs(parsed.query)
            item_id = (q.get("ID") or q.get("id") or [pid if isinstance(pid, int) else None])[0]

            out.append(
                {
                    "item_id": str(item_id) if item_id is not None else None,
                    "title": self._clean_title(title or "") or None,
                    "url": normalized_url,
                    "price": price,
                    "price_text": price_text,
                    "source": "bloomingdales_direct_html",
                }
            )

        return out

    def _extract_products_from_initial_state(self, html_text: str) -> list[dict]:
        # Fallback for runtime variants that expose product data in
        # window.__INITIAL_STATE__ (JS object, not strict JSON).
        out: list[dict] = []
        seen: set[str] = set()

        pattern = re.compile(
            r'"productUrl":"(?P<url>(?:\\.|[^"])*)"'
            r'.{0,160}?"productId":(?P<pid>\d+)'
            r'.{0,1600}?"name":"(?P<name>(?:\\.|[^"])*)"'
            r'.{0,2400}?"formattedValue":"(?P<price_text>(?:\\.|[^"])*)"',
            re.S,
        )

        for m in pattern.finditer(html_text):
            raw_url = self._js_unescape(m.group("url"))
            item_id = m.group("pid")
            if item_id in seen:
                continue
            seen.add(item_id)

            title = self._clean_title(self._js_unescape(m.group("name")))
            price_text = self._js_unescape(m.group("price_text"))

            out.append(
                {
                    "item_id": item_id,
                    "title": title or None,
                    "url": self._normalize_url(raw_url),
                    "price": self._to_float(price_text),
                    "price_text": price_text or None,
                    "source": "bloomingdales_direct_html",
                }
            )

        return out

    def _extract_nuxt_state(self, html_text: str) -> list:
        # Primary path: explicit Nuxt state script.
        m = re.search(
            r'<script[^>]+data-nuxt-data="nuxt-app"[^>]*>(?P<data>.*?)</script>',
            html_text,
            re.I | re.S,
        )
        if m:
            parsed = self._parse_state_candidate(m.group("data"))
            if parsed:
                return parsed

        # Fallback 1: parse any JSON-bearing <script> block and pick the one
        # that looks like Bloomingdale's product state.
        for sm in re.finditer(r"<script[^>]*>(?P<data>.*?)</script>", html_text, re.I | re.S):
            parsed = self._parse_state_candidate(sm.group("data"))
            if parsed:
                return parsed

        # Fallback 2: handle assignment forms (e.g. window.__NUXT__=...;)
        am = re.search(r"(?:window\.)?__NUXT__\s*=\s*(?P<data>\{.*?\});", html_text, re.I | re.S)
        if am:
            try:
                obj = json.loads(am.group("data"))
                for key in ("data", "state", "payload"):
                    val = obj.get(key) if isinstance(obj, dict) else None
                    if isinstance(val, list):
                        blob = json.dumps(val)
                        if "productUrl" in blob and "productId" in blob:
                            return val
            except Exception:
                pass

        return []

    def _parse_state_candidate(self, raw: str) -> list:
        if not raw:
            return []

        candidate = raw.strip()
        if not candidate:
            return []

        # Skip executable scripts quickly.
        if not (candidate.startswith("[") or candidate.startswith("{")):
            return []

        try:
            data = json.loads(candidate)
        except Exception:
            return []

        if isinstance(data, list):
            blob = json.dumps(data)
            if "productUrl" in blob and ("productId" in blob or '"id"' in blob):
                return data

        if isinstance(data, dict):
            for key in ("data", "state", "payload"):
                val = data.get(key)
                if isinstance(val, list):
                    blob = json.dumps(val)
                    if "productUrl" in blob and ("productId" in blob or '"id"' in blob):
                        return val

        return []

    def _resolve_ref(self, state: list, value, depth: int = 0):
        if depth > 30:
            return value
        if isinstance(value, int) and 0 <= value < len(state):
            return self._resolve_ref(state, state[value], depth + 1)
        if isinstance(value, list):
            return [self._resolve_ref(state, v, depth + 1) for v in value]
        if isinstance(value, dict):
            return {k: self._resolve_ref(state, v, depth + 1) for k, v in value.items()}
        return value

    def _extract_price(self, pricing: dict) -> tuple[float | None, str | None]:
        price = pricing.get("price") if isinstance(pricing, dict) else None
        tiered = (price or {}).get("tieredPrice") if isinstance(price, dict) else None

        if isinstance(tiered, list):
            for tier in tiered:
                values = (tier or {}).get("values") or []
                if not values:
                    continue
                first = values[0] or {}
                val = self._to_float(first.get("value"))
                txt = first.get("formattedValue")
                if val is not None or txt:
                    if isinstance(txt, str):
                        txt_val = self._to_float(txt)
                        if txt_val is not None:
                            val = txt_val
                    return val, txt

        # Fallback for payload variants where price fields are shaped differently
        # (e.g. nested lists/dicts without tieredPrice at the expected path).
        fallback_val, fallback_txt = self._find_price_any(pricing if isinstance(pricing, dict) else {})
        return fallback_val, fallback_txt

    def _page_url(self, url: str, page: int) -> str:
        if page <= 1:
            return url
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}pageindex={page}"

    def _normalize_url(self, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return urljoin("https://www.bloomingdales.com", url)

    def _clean_title(self, raw: str) -> str:
        text = re.sub(r"\\u0026", "&", raw)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"^(NEW!?|New:?|Exclusive:?|Shop New:)\s*", "", text, flags=re.I)
        return unescape(text.strip())

    def _find_price_any(self, node) -> tuple[float | None, str | None]:
        if isinstance(node, dict):
            txt = node.get("formattedValue")
            val = self._to_float(node.get("value"))
            if isinstance(txt, str):
                txt_val = self._to_float(txt)
                if txt_val is not None:
                    val = txt_val
            if val is not None or isinstance(txt, str):
                return val, txt if isinstance(txt, str) else None

            for v in node.values():
                p = self._find_price_any(v)
                if p != (None, None):
                    return p

        elif isinstance(node, list):
            for v in node:
                p = self._find_price_any(v)
                if p != (None, None):
                    return p

        return None, None

    def _js_unescape(self, text: str) -> str:
        if text is None:
            return ""
        s = text
        try:
            s = bytes(s, "utf-8").decode("unicode_escape")
        except Exception:
            pass
        return unescape(s)

    def _to_float(self, value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()
        if not text:
            return None

        # Prefer currency-like tokens first to avoid picking unrelated numbers
        # from labels such as "1 of".
        currency = re.search(r"\$\s*([0-9][0-9,]*(?:\.\d+)?)", text)
        token = currency.group(1) if currency else None

        if token is None:
            # Fallback for values like "USD 49.99" or "49.99 - 79.99".
            m = re.search(r"-?\d{1,3}(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?", text)
            if not m:
                return None
            token = m.group(0)

        try:
            return float(token.replace(",", ""))
        except Exception:
            return None
