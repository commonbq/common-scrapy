from __future__ import annotations

"""Ace Hardware listings parsed from the server-rendered Kibo/Mozu hydration."""

import json
import re
from html import unescape
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import scrapy

from common.spiders.acehardware_categories import ACEHARDWARE_CATEGORIES, BASE_URL
from common.spiders.base_listing_spider import BaseListingSpider, group_categories


# ScrapeOps option appended to the proxy username. Ace Hardware sits behind a bot
# wall that rejects the datacenter route outright: `country=us` alone, `bypass=5`
# through `bypass=20`, and `residential=true` without a bypass level each return the
# 367-byte ScrapeOps "couldn't retrieve a successful response" envelope instead of
# the document. Only the combination below returns the real ~1.9 MB SSR page with
# its `data-mz-preload-*` hydration blocks.
RESIDENTIAL_PROXY = "residential=true"
BYPASS_PROXY = "bypass=5"

# Image sources hydrate as protocol-relative Mozu CMS paths.
IMAGE_CDN = "https://cdn-tp6.mozu.com"

# The storefront ships each hydration block as its own
# `<script type="text/json" id="data-mz-preload-<Name>">` island.
_PRELOAD_RE = r'<script type="text/json" id="data-mz-preload-%s">(.*?)</script>'

# Brand is a Kibo custom property rather than a top-level field; it is the
# `tenant~brand-name-attribute` value the PLP hydration carries per product.
_BRAND_PROPERTY = "tenant~brand-name-attribute"

# Depth guard for the recursive department -> leaf walk. Ace's deepest observed
# department nesting is 3 levels below the department page, so 6 leaves room for a
# deeper re-categorization without ever letting a cycle run away.
MAX_CATEGORY_DEPTH = 6


class AceHardwareListingSpider(BaseListingSpider):
    """acehardware.com listings from the SSR `#data-mz-preload-PLPModel` hydration.

    One direction only: every field is read out of the server-rendered Kibo/Mozu
    hydration (`<script type="text/json" id="data-mz-preload-PLPModel">`), which
    carries the full normalized product record for each shelf. There is no HTML-card
    fallback, no JSON-LD, and no separate product API call.

    Paging stays on that same direction. The storefront honors `?startIndex=N` and
    re-renders `PLPModel` for the requested offset, so page N is another SSR
    hydration read rather than a second extraction strategy.
    """

    name = "acehardware_listing"
    allowed_domains = ["acehardware.com", "www.acehardware.com"]
    categories = group_categories(ACEHARDWARE_CATEGORIES, "department")
    # Direct url=/category_url= runs are supported, so opt out of the base class
    # category-only gate; resolve_target_url() still rejects a run with no target.
    require_category_arg = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.5,
        # Let the explicit status checks in parse() run so a bot-wall envelope or an
        # error status surfaces the documented actionable error instead of a
        # successful zero-item crawl.
        "HTTPERROR_ALLOW_ALL": True,
        "FEED_EXPORT_FIELDS": [
            "item_id",
            "title",
            "brand",
            "sku",
            "mpn",
            "upc",
            "product_type",
            "url",
            "image",
            "image_alt",
            "images",
            "short_description",
            "price",
            "original_price",
            "discount_percentage",
            "currency",
            "on_sale",
            "in_stock",
            "stock_status",
            "availability",
            "is_purchasable",
            "fulfillment_types",
            "package_weight",
            "package_dimensions",
            "category",
            "department",
            "section",
            "category_name",
            "category_id",
            "category_path",
            "page",
            "position",
            "total_count",
            "last_page",
            "source",
            "raw",
            "timestamp",
        ],
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.category or self.category_url or self.url):
            raise ValueError(
                "Provide -a category=<name>, category_url=<url>, or url=<url>. "
                f"Available categories: {', '.join(self.available_categories())}"
            )
        self._seen: set[str] = set()
        self._visited_categories: set[str] = set()

    # ---------------------------------------------------------------- requests

    def start_requests(self) -> Iterable[scrapy.Request]:
        self._seen.clear()
        self._visited_categories.clear()
        target = self.resolve_target_url()
        selected = next((entry for entry in self.iter_categories() if entry.get("url") == target), {})
        yield self._page_request(target, page=1, start_index=0, selected=selected)

    def _page_request(
        self,
        url: str,
        *,
        page: int,
        start_index: int,
        selected: dict[str, Any],
    ) -> scrapy.Request:
        return scrapy.Request(
            self._page_url(url, start_index),
            callback=self.parse,
            headers=self.headers,
            meta={
                "proxy": self._proxy_url(),
                "page": page,
                "start_index": start_index,
                "category": self.category or selected.get("category") or "custom",
                "department": selected.get("department"),
                "section": selected.get("section"),
                "category_id": selected.get("category_id") or None,
                "category_name": selected.get("name"),
                "category_path": [],
                "depth": 0,
            },
            dont_filter=True,
        )

    def _child_request(
        self,
        url: str,
        *,
        parent: dict[str, Any],
        category_path: list[str],
    ) -> scrapy.Request:
        """Request a child category discovered from a department page's hydration."""
        return scrapy.Request(
            url,
            callback=self.parse,
            headers=self.headers,
            meta={
                "proxy": self._proxy_url(),
                "page": 1,
                "start_index": 0,
                "category": parent.get("category") or "custom",
                "department": parent.get("department"),
                "section": parent.get("section"),
                "category_id": None,
                "category_name": category_path[-1] if category_path else parent.get("category_name"),
                "category_path": category_path,
                "depth": parent.get("depth", 0) + 1,
            },
            dont_filter=True,
        )

    @staticmethod
    def _page_url(url: str, start_index: int) -> str:
        """Return ``url`` with the storefront's ``?startIndex=N`` contract applied.

        The PLP is server-rendered per offset (``/cat?startIndex=30`` returns
        ``currentPage`` 2), and the number is echoed back as
        ``PLPModel.startIndex``. Offset 0 is left bare so the canonical category URL
        stays the first request, and any existing query string is preserved.

        ``?page=N`` is deliberately not used: Ace ignores it and silently re-renders
        page 1, which would loop the crawler on a single shelf.
        """
        if start_index <= 0:
            return url
        parts = urlsplit(url)
        query = [
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k not in ("startIndex", "page")
        ]
        query.append(("startIndex", str(start_index)))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def _proxy_url(self) -> str | None:
        """Return the configured proxy with the residential + bypass options enabled.

        ScrapeOps credentials are carried as ``<options>:<api_key>@host:port``, so
        the options belong on the username side and the password is preserved
        verbatim. A non-ScrapeOps proxy, or one that already carries the options, is
        returned untouched.
        """
        proxy = getattr(self, "settings", {}).get("PROXY")
        if not isinstance(proxy, str) or not proxy:
            return None
        if "scrapeops" not in proxy.lower():
            return proxy
        parts = urlsplit(proxy)
        if parts.password is None or not parts.hostname:
            return proxy
        username = parts.username or ""
        if BYPASS_PROXY.split("=")[-1] in username:
            return proxy
        if RESIDENTIAL_PROXY.split("=")[-1] not in username:
            username = f"{username}.{RESIDENTIAL_PROXY}"
        username = f"{username}.{BYPASS_PROXY}"
        return urlunsplit(
            (
                parts.scheme,
                f"{username}:{parts.password}@{parts.hostname}:{parts.port}",
                parts.path,
                parts.query,
                parts.fragment,
            )
        )

    # ------------------------------------------------------------------ parse

    def parse(self, response: scrapy.http.Response):
        if response.status != 200:
            raise RuntimeError(
                f"acehardware listing returned HTTP {response.status}: {response.url}"
            )
        body = self._body(response)
        plp_model = self._preload(body, "PLPModel", response.url)

        if plp_model is None:
            # A department index page (e.g. /departments/tools) hydrates routeData
            # with its recursive children but no product shelf. Following the
            # children down to the leaves is the same hydration direction, not a
            # second extraction strategy.
            yield from self._follow_department(response, body)
            return

        items = plp_model.get("items")
        items = items if isinstance(items, list) else []
        if not items:
            self.logger.warning(
                "acehardware %s hydrated an empty PLPModel (totalCount=%s)",
                response.url, plp_model.get("totalCount"),
            )
            return

        current_page = int(response.meta.get("page") or 1)
        total_count = self._number(plp_model.get("totalCount"))
        last_page = self._number(plp_model.get("pageCount"))

        for position, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                continue
            item_id = str(item.get("productCode") or "").strip()
            if not item_id or item_id in self._seen:
                continue
            self._seen.add(item_id)
            yield self._item(item, response=response, page=current_page, position=position,
                             total_count=total_count, last_page=last_page)

        yield from self._next_page(response, plp_model, current_page, last_page)

    def _next_page(
        self,
        response: scrapy.http.Response,
        plp_model: dict[str, Any],
        current_page: int,
        last_page: int | None,
    ):
        if current_page >= self.max_pages:
            return
        if plp_model.get("hasNextPage") is False:
            return
        page_size = self._number(plp_model.get("pageSize")) or 0
        if not page_size:
            return
        start_index = self._number(response.meta.get("start_index")) or 0
        # `pageCount` is the storefront's own count and is present on every PLP, so
        # it bounds the walk even when `hasNextPage` is absent.
        if last_page is not None and current_page >= last_page:
            return
        selected = next((entry for entry in self.iter_categories() if entry.get("url") == response.url), {})
        yield self._page_request(
            self._base_url(response.url),
            page=current_page + 1,
            start_index=start_index + page_size,
            selected=selected,
        )

    # ------------------------------------------------------- department walking

    def _follow_department(self, response: scrapy.http.Response, body: str):
        """Emit requests for the product-bearing leaves under a department page."""
        route_data = self._preload(body, "routeData", response.url)
        if not isinstance(route_data, dict):
            raise RuntimeError(
                f"acehardware {response.url} hydrated neither a PLPModel nor routeData; "
                "the response is a bot-wall challenge or an unsupported page type"
            )

        meta = response.meta
        depth = int(meta.get("depth") or 0)
        if depth >= MAX_CATEGORY_DEPTH:
            return

        category_object = route_data.get("-categoryObject")
        category_object = category_object if isinstance(category_object, dict) else {}
        children = category_object.get("childrenCategories")
        children = children if isinstance(children, list) else []
        children = [
            child for child in children
            if isinstance(child, dict) and not self._is_hidden(child)
        ]
        if not children:
            self.logger.warning(
                "acehardware %s is a leaf with no product shelf and no crawlable "
                "children (categoryId=%s)", response.url, route_data.get("categoryId"),
            )
            return

        path = list(meta.get("category_path") or [])
        slug = str(route_data.get("categorySlug") or "").strip()
        if slug:
            path.append(slug)

        for child in children:
            url = self._child_url(child, path)
            if not url or url in self._visited_categories:
                continue
            self._visited_categories.add(url)
            yield self._child_request(url, parent=meta, category_path=path)

    def _child_url(self, child: dict[str, Any], parent_path: list[str]) -> str | None:
        """Resolve the crawlable PLP URL for a child category node.

        The hydration gives both a ``/slug/c/<id>`` canonical path and a ``slug``
        field. Ace's crawlable department URL is the breadcrumb path
        (``/departments/tools/power-tools/cordless-drills``), which is what the
        site itself links to, so the slug chain from the parent route is rebuilt
        rather than using the ``/c/<id>`` form.
        """
        content = child.get("content")
        content = content if isinstance(content, dict) else {}
        slug = str(content.get("slug") or "").strip()
        if not slug:
            url = str(child.get("url") or "").strip()
            match = re.match(r"^/([^/]+)/c/\d+", url)
            slug = match.group(1) if match else ""
        if not slug:
            return None
        path = [part for part in parent_path if part != "departments"]
        segments = [part for part in (["departments"] + path + [slug]) if part]
        return urljoin(BASE_URL + "/", "/".join(segments))

    @staticmethod
    def _is_hidden(node: dict[str, Any]) -> bool:
        """Return True when a nav child is a hidden/system node.

        Ace's department trees carry a large set of `isHidden` housekeeping nodes
        (test categories, seasonal placeholders) that are not linked from the
        storefront navigation.
        """
        return bool(node.get("isHidden")) or bool(node.get("isSystemNode"))

    @staticmethod
    def _base_url(url: str) -> str:
        """Strip paging params so the next page re-applies `startIndex` cleanly."""
        parts = urlsplit(url)
        query = [
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k not in ("startIndex", "page")
        ]
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    # ------------------------------------------------------------- extraction

    @staticmethod
    def _preload(body: str, name: str, url: str) -> dict[str, Any] | None:
        """Return one `data-mz-preload-<name>` hydration block, or None if absent.

        A missing block is not an error on its own: department pages ship no
        PLPModel. Callers decide what the absence means for the page type.
        """
        match = re.search(_PRELOAD_RE % re.escape(name), body or "", re.S)
        if not match:
            return None
        raw = match.group(1).strip()
        if not raw:
            return None
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"acehardware data-mz-preload-{name} at {url} is not valid JSON"
            ) from exc
        return payload if isinstance(payload, dict) else None

    def _body(self, response: scrapy.http.Response) -> str:
        """Return the response text, rejecting the known bot-wall envelope."""
        text = response.text or ""
        # A blocked upstream fetch is answered with HTTP 200 and a tiny JSON
        # envelope rather than an error status, so status checking alone turns a
        # blocked run into a green, zero-item crawl. The envelope is the only
        # response small enough to be meaningless as a storefront document.
        if len(text) < 2048 and "retrieve a successful response" in text:
            raise RuntimeError(
                f"acehardware {response.url} returned the proxy's failure envelope "
                f"({len(text)} bytes) instead of the storefront page; the proxy route "
                "is being blocked"
            )
        return text

    def _item(
        self,
        product: dict[str, Any],
        *,
        response: scrapy.http.Response,
        page: int,
        position: int,
        total_count: int | None,
        last_page: int | None,
    ) -> dict[str, Any]:
        content = product.get("content")
        content = content if isinstance(content, dict) else {}
        price_block = product.get("price")
        price_block = price_block if isinstance(price_block, dict) else {}
        inventory = product.get("inventoryInfo")
        inventory = inventory if isinstance(inventory, dict) else {}
        purchasable = product.get("purchasableState")
        purchasable = purchasable if isinstance(purchasable, dict) else {}

        price = self._number(price_block.get("price"))
        original_price = self._number(price_block.get("msrp"))
        on_sale = bool(price_block.get("onSale")) and (
            original_price is None or price is None or price < original_price
        )
        discount_percentage = None
        if on_sale and original_price and price and original_price > 0:
            discount_percentage = round((original_price - price) / original_price * 100, 2)

        # `isPurchasable` is the storefront's own sellability decision and already
        # folds in publishState/isActive, so it is the stock signal; the inventory
        # counters break ties and give a readable reason when it is False.
        is_purchasable = bool(purchasable.get("isPurchasable"))
        online_stock = self._number(inventory.get("onlineStockAvailable"))
        in_stock = is_purchasable and bool(online_stock)
        if in_stock:
            stock_status = "IN_STOCK"
        elif not is_purchasable:
            stock_status = "NOT_PURCHASABLE"
        elif online_stock == 0:
            stock_status = "OUT_OF_STOCK"
        else:
            stock_status = "UNKNOWN"

        title = self._clean_text(content.get("productName"))
        relative_url = str(product.get("url") or "").strip()
        url = urljoin(BASE_URL + "/", relative_url.lstrip("/")) if relative_url else response.url
        item_id = str(product.get("productCode") or "").strip()
        category_path = [p for p in (response.meta.get("category_path") or []) if p]
        categories = product.get("categories")
        categories = categories if isinstance(categories, list) else []
        primary_category = categories[0] if categories and isinstance(categories[0], dict) else {}
        primary_content = (
            primary_category.get("content") if isinstance(primary_category.get("content"), dict) else {}
        )

        measurements = product.get("measurements")
        measurements = measurements if isinstance(measurements, dict) else {}
        item: dict[str, Any] = {
            "item_id": item_id,
            "title": title,
            "brand": self._brand(product),
            "sku": item_id or None,
            "mpn": str(product.get("mfgPartNumber") or "").strip() or None,
            "upc": str(product.get("upc") or "").strip() or None,
            "product_type": product.get("productType"),
            "url": url,
            "image": self._main_image(product),
            "image_alt": self._clean_text((product.get("mainImage") or {}).get("altText")),
            "images": self._images(content),
            "short_description": self._clean_text(content.get("productShortDescription")),
            "price": price,
            "original_price": original_price if on_sale else None,
            "discount_percentage": discount_percentage,
            "currency": "USD",
            "on_sale": on_sale,
            "in_stock": in_stock,
            "stock_status": stock_status,
            "availability": "in stock" if in_stock else stock_status.lower().replace("_", " "),
            "is_purchasable": is_purchasable,
            "fulfillment_types": product.get("fulfillmentTypesSupported") or None,
            "package_weight": self._measurement(measurements.get("packageWeight")),
            "package_dimensions": {
                key: self._measurement(measurements.get(f"package{key.capitalize()}"))
                for key in ("height", "width", "length")
            }
            or None,
            "category": response.meta.get("category"),
            "department": response.meta.get("department"),
            "section": response.meta.get("section"),
            "category_name": response.meta.get("category_name"),
            "category_id": str(primary_category.get("categoryId") or "")
            or response.meta.get("category_id"),
            "category_path": category_path or None,
            "page": page,
            "position": position,
            "total_count": total_count,
            "last_page": last_page,
            "source": "acehardware_mozu_hydration",
            "raw": {
                "product": product,
                "primary_category_name": primary_content.get("name"),
                "upcs": product.get("upCs") or None,
                "days_available_in_catalog": product.get("daysAvailableInCatalog"),
                "product_type_id": product.get("productTypeId"),
            },
            "timestamp": self.job_timestamp,
        }
        return item

    @staticmethod
    def _clean_text(value: Any) -> str | None:
        """Normalize a hydrated string.

        Kibo carries storefront-authored copy that still has HTML entities from the
        CMS (``Battery &amp; Charger``), so the value is unescaped rather than
        emitted raw. Embedded tags are dropped: this is text, not markup.
        """
        if not isinstance(value, str):
            return None
        text = unescape(value).strip()
        text = re.sub(r"<[^>]+>", "", text).strip()
        return text or None

    @classmethod
    def _brand(cls, product: dict[str, Any]) -> str | None:
        """Return the brand from the `tenant~brand-name-attribute` property.

        Ace carries brand as a Kibo custom property. `values` is a list because the
        property is declared multi-value, and each entry repeats the value in
        `value`/`stringValue`, so the first populated entry wins.
        """
        for prop in product.get("properties") or []:
            if not isinstance(prop, dict) or prop.get("attributeFQN") != _BRAND_PROPERTY:
                continue
            for entry in prop.get("values") or []:
                if not isinstance(entry, dict):
                    continue
                brand = entry.get("value") or entry.get("stringValue")
                if brand and cls._clean_text(brand):
                    return cls._clean_text(brand)
        return None

    @classmethod
    def _main_image(cls, product: dict[str, Any]) -> str | None:
        main = product.get("mainImage")
        main = main if isinstance(main, dict) else {}
        for key in ("src", "imageUrl"):
            value = main.get(key)
            if value:
                return cls._absolute_image(str(value))
        return None

    @classmethod
    def _images(cls, content: dict[str, Any]) -> list[str] | None:
        urls: list[str] = []
        for image in content.get("productImages") or []:
            if not isinstance(image, dict):
                continue
            value = image.get("src") or image.get("imageUrl")
            if value:
                url = cls._absolute_image(str(value))
                if url and url not in urls:
                    urls.append(url)
        return urls or None

    @staticmethod
    def _absolute_image(value: str) -> str:
        """Resolve a protocol-relative Mozu CDN path against the CDN origin."""
        if value.startswith("//"):
            return f"https:{value}"
        if value.startswith(("http://", "https://")):
            return value
        return urljoin(IMAGE_CDN + "/", value.lstrip("/"))

    @staticmethod
    def _measurement(value: Any) -> str | None:
        """Render a Kibo measurement object as `<value> <unit>`."""
        if not isinstance(value, dict):
            return None
        amount = value.get("value")
        unit = value.get("unit")
        if amount is None or not unit:
            return None
        return f"{amount} {unit}"

    @staticmethod
    def _number(value: Any) -> int | float | None:
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, (int, float)):
            return value
        try:
            text = str(value).strip().replace(",", "")
            return float(text) if "." in text else int(text)
        except (TypeError, ValueError):
            return None
