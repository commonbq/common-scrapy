"""Tests for `acehardware_listing` (SSR Kibo/Mozu `data-mz-preload-PLPModel` hydration)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from common.spiders.acehardware_categories import ACEHARDWARE_CATEGORIES
from common.spiders.acehardware_listing_spider import (
    BASE_URL,
    BYPASS_PROXY,
    RESIDENTIAL_PROXY,
    AceHardwareListingSpider,
)

SAMPLE = Path(__file__).resolve().parents[1] / "sample"

CORDLESS = "https://www.acehardware.com/departments/tools/power-tools/cordless-drills"
TOOLS = "https://www.acehardware.com/departments/tools"


class _FakeResponse:
    def __init__(self, url, body, status=200, meta=None):
        self.url = url
        self.text = body
        self.status = status
        self.meta = meta or {}


def _read(name: str) -> str:
    return (SAMPLE / name).read_text(encoding="utf-8")


def _crawl(body, url=CORDLESS, status=200, meta=None, spider=None, **kwargs):
    """Run the spider against one fixture and return (items, requests)."""
    base_meta = {
        "category": "cordless-drills",
        "department": "Tools",
        "section": "Power Tools",
        "category_id": "3002",
        "category_name": "Cordless Drills",
        "category_path": ["departments", "tools", "power-tools", "cordless-drills"],
        "page": 1,
        "start_index": 0,
        "depth": 0,
        "proxy": None,
    }
    base_meta.update(meta or {})
    response = _FakeResponse(url=url, body=body, status=status, meta=base_meta)
    kwargs.setdefault("category", "cordless-drills")
    if spider is None:
        spider = AceHardwareListingSpider(**kwargs)
    items, requests = [], []
    for out in spider.parse(response):
        (requests if hasattr(out, "url") else items).append(out)
    return items, requests


# --------------------------------------------------------------------- taxonomy


def test_categories_are_well_formed_and_unique():
    assert ACEHARDWARE_CATEGORIES
    slugs = [entry["category"] for entry in ACEHARDWARE_CATEGORIES]
    assert len(slugs) == len(set(slugs)), "category slugs must be unique"
    for entry in ACEHARDWARE_CATEGORIES:
        assert entry["url"].startswith(BASE_URL)
        assert entry["url"].count("?") == 0


def test_spider_requires_a_target():
    with pytest.raises(ValueError, match="Provide -a category"):
        AceHardwareListingSpider()


# --------------------------------------------------------------------- PLP items


def test_plp_hydration_yields_one_item_per_product():
    items, requests = _crawl(_read("acehardware_cordless_drills.html"), max_pages=2)
    assert len(items) == 3
    first = items[0]
    assert first["item_id"] == "2385458"
    assert first["sku"] == "2385458"
    assert first["title"].startswith("DeWalt 20V MAX")
    assert first["brand"] == "DeWalt"
    assert first["mpn"] == "DCD771C2"
    assert first["upc"] == "885911325905"
    assert first["price"] == 179.0
    assert first["currency"] == "USD"
    assert first["on_sale"] is False
    assert first["original_price"] is None
    assert first["in_stock"] is True
    assert first["stock_status"] == "IN_STOCK"
    assert first["is_purchasable"] is True
    assert first["fulfillment_types"] == ["DirectShip", "InStorePickup", "Delivery"]
    assert first["source"] == "acehardware_mozu_hydration"
    assert first["total_count"] == 172
    assert first["last_page"] == 6
    assert first["page"] == 1
    assert first["position"] == 1
    assert first["url"].startswith(f"{BASE_URL}/dewalt-20v-max")
    assert first["image"].startswith("https://cdn-tp6.mozu.com/")
    assert not first["image"].startswith("//")
    assert len(first["images"]) == 8
    assert first["package_weight"] == "5.9 lbs"
    assert first["package_dimensions"]["height"] == "9.8 in"
    assert first["short_description"] == "20V CMPT DRILL 1/2 2BAT"
    assert first["product_type"] == "016013301004-Cordless Drills"
    assert len(requests) == 1, "page 1 of 6 should request page 2 when max_pages allows"


def test_positions_increment_and_paging_uses_start_index():
    items, requests = _crawl(_read("acehardware_cordless_drills.html"), max_pages=2)
    assert [item["position"] for item in items] == [1, 2, 3]
    assert len(requests) == 1
    # Ace ignores ?page=N, so paging must go through the startIndex contract.
    assert "startIndex=30" in requests[0].url
    assert "page=2" not in requests[0].url


def test_max_pages_caps_the_walk():
    _, requests = _crawl(_read("acehardware_cordless_drills.html"), max_pages=1)
    assert requests == []


def test_duplicate_products_are_dropped_across_pages():
    """The same shelf replayed as page 2 must not re-export the same SKUs."""
    spider = AceHardwareListingSpider(category="cordless-drills", max_pages=2)
    body = _read("acehardware_cordless_drills.html")
    meta = {"page": 1, "start_index": 0, "category_path": [], "category_id": None,
            "department": None, "section": None, "category_name": "Cordless Drills",
            "depth": 0}
    first_items, first_requests = _crawl(body, meta=meta, spider=spider)
    assert len(first_items) == 3 and len(first_requests) == 1
    meta_page2 = dict(meta, page=2, start_index=30)
    second_items, _ = _crawl(body, url=CORDLESS + "?startIndex=30", meta=meta_page2,
                             spider=spider)
    assert second_items == [], "the same three products must not be exported twice"


# --------------------------------------------------------------- department walk


def test_department_page_follows_children_instead_of_emitting_nothing():
    items, requests = _crawl(
        _read("acehardware_tools_department.html"),
        url=TOOLS,
        meta={"category": "tools", "category_id": "28", "category_path": ["departments"],
              "department": "Tools", "section": "Tools", "category_name": "Tools"},
    )
    assert items == []
    assert len(requests) == 17, "the Tools department hydrates 17 visible children"
    urls = {request.url for request in requests}
    assert f"{BASE_URL}/departments/tools/power-tools" in urls
    assert f"{BASE_URL}/departments/tools/hand-tools" in urls
    assert all(request.meta["depth"] == 1 for request in requests)
    assert all(request.meta["proxy"] is None for request in requests)


def test_hidden_children_are_skipped():
    """Hidden housekeeping nodes must not be crawled."""
    spider = AceHardwareListingSpider(category="tools")
    items, requests = _crawl(
        _read("acehardware_tools_department.html"),
        url=TOOLS,
        spider=spider,
        meta={"category": "tools", "category_id": "28", "category_path": ["departments"],
              "department": "Tools", "section": "Tools", "category_name": "Tools"},
    )
    assert len(requests) == 17
    assert all("isHidden" not in r.url for r in requests)


def test_depth_guard_stops_recursion():
    items, requests = _crawl(
        _read("acehardware_tools_department.html"),
        url=TOOLS,
        meta={"category": "tools", "category_id": "28", "category_path": ["departments"],
              "department": "Tools", "section": "Tools", "category_name": "Tools",
              "depth": 99},
    )
    assert items == [] and requests == []


# ------------------------------------------------------------------- proxy route


def test_scrapeops_proxy_gains_residential_and_bypass_options():
    spider = AceHardwareListingSpider(category="cordless-drills")
    spider.settings = {
        "PROXY": "http://scrapeops.country=us:apikey@proxy.scrapeops.io:5353"
    }
    url = spider._proxy_url()
    assert url == "http://scrapeops.country=us.residential=true.bypass=5:apikey@proxy.scrapeops.io:5353"


def test_proxy_options_are_not_duplicated():
    spider = AceHardwareListingSpider(category="cordless-drills")
    spider.settings = {
        "PROXY": "http://scrapeops.country=us.residential=true.bypass=5:k@proxy.scrapeops.io:5353"
    }
    url = spider._proxy_url()
    username = url.split("://", 1)[1].split(":", 1)[0]
    assert username == "scrapeops.country=us.residential=true.bypass=5"


def test_non_scrapeops_proxy_is_untouched():
    spider = AceHardwareListingSpider(category="cordless-drills")
    spider.settings = {"PROXY": "http://user:pass@brd.superproxy.io:33335"}
    assert spider._proxy_url() == "http://user:pass@brd.superproxy.io:33335"


def test_missing_proxy_returns_none():
    spider = AceHardwareListingSpider(category="cordless-drills")
    spider.settings = {}
    assert spider._proxy_url() is None


# ------------------------------------------------------------------ page guards


def test_non_200_status_is_an_explicit_error():
    with pytest.raises(RuntimeError, match="HTTP 429"):
        _crawl(_read("acehardware_cordless_drills.html"), status=429)


def test_proxy_failure_envelope_is_not_silently_zero_items():
    envelope = json.dumps(
        {"status": "We couldn't retrieve a successful response for this request."}
    )
    with pytest.raises(RuntimeError, match="failure envelope"):
        _crawl(envelope)


def test_missing_hydration_raises_rather_than_returning_nothing():
    with pytest.raises(RuntimeError, match="neither a PLPModel nor routeData"):
        _crawl("<html><body><div>blocked</div></body></html>")


def test_page_url_drops_page_and_sets_start_index():
    build = AceHardwareListingSpider._page_url
    assert build(CORDLESS, 0) == CORDLESS
    assert build(CORDLESS, 30) == f"{CORDLESS}?startIndex=30"
    # A stale ?page= must be dropped, because Ace silently re-renders page 1.
    assert "page=2" not in build(f"{CORDLESS}?page=2", 30)
    assert build(f"{CORDLESS}?page=2", 30).endswith("startIndex=30")


def test_alt_text_has_html_entities_decoded():
    """Kibo hydrates CMS copy that still carries entities; they must be unescaped."""
    items, _ = _crawl(_read("acehardware_cordless_drills.html"))
    first = items[0]
    assert first["image_alt"] == first["title"]
    assert "&amp;" not in first["image_alt"]
    assert "Battery & Charger" in first["image_alt"]


def test_category_path_is_reported_when_walking_from_a_department():
    spider = AceHardwareListingSpider(category="tools")
    meta = {"category": "tools", "category_id": "28", "category_path": ["departments"],
            "department": "Tools", "section": "Tools", "category_name": "Tools", "depth": 0}
    body = _read("acehardware_tools_department.html")
    requests = _crawl(body, url=TOOLS, meta=meta, spider=spider)[1]
    leaf = [r for r in requests if r.url.endswith("/power-tools")][0]
    # The child's path is its parent's chain; its own slug is appended only if that
    # page also turns out to be a department index.
    assert leaf.meta["category_path"] == ["departments", "tools"]
    assert leaf.meta["depth"] == 1


def test_feed_export_fields_match_the_emitted_item():
    fields = AceHardwareListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
    assert "item_id" in fields and "title" in fields and "price" in fields
    assert len(fields) == len(set(fields)), "FEED_EXPORT_FIELDS must not repeat a field"
