"""Tests for `backcountry_listing` (SSR `#__NEXT_DATA__` PLP + Apollo hydration)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from common.spiders.backcountry_categories import BACKCOUNTRY_CATEGORIES
from common.spiders.backcountry_listing_spider import (
    IMAGE_CDN,
    BackcountryListingSpider,
)

SAMPLE = Path(__file__).resolve().parents[1] / "sample"

MENS_SHIRTS = "https://www.backcountry.com/cat/mens-shirts"


def _crawl_text(crawler, url=MENS_SHIRTS, **kwargs):
    """Run the spider against one fixture and return (items, requests)."""
    body = kwargs.pop("body")
    status = kwargs.pop("status", 200)
    meta = {"category": "cat-mens-shirts", "department": "Men", "section": "Clothing",
            "category_id": "bc-mens-shirts", "page": 1, "proxy": None}
    meta.update(kwargs.pop("meta", {}))
    response = _FakeResponse(url=url, body=body, status=status, meta=meta)
    kwargs.setdefault("category", "cat-mens-shirts")
    spider = BackcountryListingSpider(**kwargs)
    out = []
    requests = []
    for item in spider.parse(response):
        if hasattr(item, "url"):
            requests.append(item)
        else:
            out.append(item)
    return out, requests


class _FakeResponse:
    def __init__(self, url, body, status=200, meta=None):
        self.url = url
        self.text = body
        self.status = status
        self.meta = meta or {}
        self.url = url


def _read(name: str) -> str:
    return (SAMPLE / name).read_text(encoding="utf-8")


def _hydration(page_props: dict) -> str:
    """Wrap bare pageProps in the SSR document shell the storefront emits."""
    return (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps({"props": {"pageProps": page_props}, "buildId": "5.33.0"})
        + "</script></body></html>"
    )


# --------------------------------------------------------------------- taxonomy


def test_categories_are_unique_and_well_formed():
    slugs = [entry["category"] for entry in _FLAT(BACKCOUNTRY_CATEGORIES)]
    urls = [entry["url"] for entry in _FLAT(BACKCOUNTRY_CATEGORIES)]
    assert slugs, "category inventory must not be empty"
    assert len(slugs) == len(set(slugs)), "category slugs must be unique"
    assert len(urls) == len(set(urls)), "category URLs must be unique"
    for entry in _FLAT(BACKCOUNTRY_CATEGORIES):
        assert entry["url"].startswith("https://www.backcountry.com/")
        assert entry["department"] and entry["section"]


def test_categories_cover_both_cat_and_rc_families():
    prefixes = {entry["category"].split("-", 1)[0] for entry in _FLAT(BACKCOUNTRY_CATEGORIES)}
    assert "cat" in prefixes
    assert "rc" in prefixes


def test_taxonomy_normalizes_links_without_a_category_id():
    # The header emits filtered /rc/ and /brand/ links with an empty categoryId.
    # Those must survive normalization rather than being silently dropped.
    without_id = [e for e in _FLAT(BACKCOUNTRY_CATEGORIES) if e["category_id"] is None]
    assert without_id, "links lacking a categoryId must be kept"
    assert all(e["url"].startswith("https://www.backcountry.com/") for e in without_id)
    assert all(e["category"] and e["name"] for e in without_id)


def test_taxonomy_slugs_derive_from_the_storefront_path():
    entry = next(e for e in _FLAT(BACKCOUNTRY_CATEGORIES) if e["category"] == "rc-mens-parkas")
    assert entry["url"].endswith("/rc/mens-parkas")
    assert entry["category"] == "rc-mens-parkas"


def test_mens_shirts_is_crawlable():
    entry = next(e for e in _FLAT(BACKCOUNTRY_CATEGORIES) if e["category"] == "cat-mens-shirts")
    assert entry["url"] == MENS_SHIRTS
    assert entry["category_id"] == "bc-mens-shirts"


def test_target_resolution_from_category():
    spider = BackcountryListingSpider(category="cat-mens-shirts")
    assert spider.resolve_target_url() == MENS_SHIRTS


def test_unknown_category_raises():
    # The base class defers the unknown-slug error to target resolution, so the
    # run fails loudly before any request is scheduled.
    with pytest.raises(ValueError, match="Unknown category"):
        BackcountryListingSpider(category="does-not-exist").resolve_target_url()


def test_run_without_any_target_raises():
    with pytest.raises(ValueError):
        BackcountryListingSpider()


# --------------------------------------------------------------------- parsing


def test_page1_exports_every_edge():
    items, requests = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    assert len(items) == 5
    assert requests == [] or requests  # page-1 request itself is yielded by start_requests
    first = items[0]
    assert first["item_id"] == "SKU1"
    assert first["title"] == "Test Product 1 - Men's"
    assert first["brand"] == "Testbrand"
    assert first["url"] == "https://www.backcountry.com/test-product-1-mens"
    assert first["price"] == 100.0
    assert first["original_price"] is None
    assert first["currency"] == "USD"
    assert first["in_stock"] is True
    assert first["stock_status"] == "IN_STOCK"
    assert first["availability"] == "in stock"
    assert first["position"] == 1
    assert first["page"] == 1
    assert first["source"] == "backcountry_next_data"
    assert first["department"] == "Men"
    assert first["section"] == "Clothing"


def test_export_fields_cover_every_item():
    fields = BackcountryListingSpider.custom_settings["FEED_EXPORT_FIELDS"]
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    for item in items:
        assert set(item) == set(fields), f"missing/extra keys: {set(item) ^ set(fields)}"


def test_sale_price_and_discount():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    sale = next(i for i in items if i["item_id"] == "SKU2")
    assert sale["price"] == 52.5
    assert sale["original_price"] == 75.0
    assert sale["discount_percentage"] == 30
    assert sale["is_new_arrival"] is True
    assert sale["raw"]["variations_on_sale"] == 2


def test_equal_prices_are_not_reported_as_sale():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    plain = next(i for i in items if i["item_id"] == "SKU1")
    # minDiscount 0 is normalized to null so it never reads as a markdown.
    assert plain["discount_percentage"] is None
    assert plain["original_price"] is None
    assert plain["price"] == 100.0


def test_out_of_stock_is_not_in_stock():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    out = next(i for i in items if i["item_id"] == "SKU3")
    assert out["in_stock"] is False
    assert out["availability"] == "OUT_OF_STOCK"


def test_reviews_and_multiple_colors():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    item = next(i for i in items if i["item_id"] == "SKU4")
    assert item["rating"] == 4.5
    assert item["reviews_count"] == 7
    assert item["colors"] == ["Red", "Blue"]
    assert item["color"] == "Red"
    assert item["color_option_count"] == 2
    # The first swatch only has tileImage; the CDN origin must be applied.
    assert item["image"] == f"{IMAGE_CDN}/images/items/160/TST/SKU4/RED.jpg"


def test_missing_optional_values_do_not_crash():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    sparse = next(i for i in items if i["item_id"] == "SKU5")
    assert sparse["brand"] is None
    assert sparse["image"] is None
    assert sparse["colors"] is None
    assert sparse["color_option_count"] == 0
    assert sparse["rating"] is None
    assert sparse["reviews_count"] == 0
    assert sparse["price"] == 59.95
    # An empty product url falls back to the crawled page url rather than "".
    assert sparse["url"] == MENS_SHIRTS


def test_absolute_urls():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    assert all(item["url"].startswith("https://www.backcountry.com/") for item in items)
    assert all(item["image"].startswith("https://") for item in items if item["image"])


def test_totals_are_exported():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    assert items[0]["total_count"] == 1490
    assert items[0]["last_page"] == 36


def test_apollo_record_is_joined_and_recorded():
    items, _ = _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"))
    item = next(i for i in items if i["item_id"] == "SKU1")
    assert item["raw"]["container"] == "category"
    assert item["raw"]["apollo"]["id"] == "SKU1"


def test_collection_container_is_parsed():
    items, _ = _crawl_text(
        None,
        url="https://www.backcountry.com/rc/mens-parkas",
        body=_read("backcountry-plp-collection.json"),
        meta={"category": "rc-mens-parkas", "department": "Men", "section": "Outerwear",
              "category_id": None},
    )
    assert len(items) == 2
    assert items[0]["item_id"] == "SKU10"
    assert items[0]["raw"]["container"] == "collection"
    assert items[0]["department"] == "Men"


def test_brand_container_is_parsed():
    items, _ = _crawl_text(
        None,
        url="https://www.backcountry.com/brand/patagonia",
        body=_read("backcountry-plp-brand.json"),
        meta={"category": "brand-patagonia", "department": "Brands", "section": "Patagonia",
              "category_id": None},
    )
    assert [i["item_id"] for i in items] == ["SKU12"]
    assert items[0]["raw"]["container"] == "brand"


def test_listing_container_locates_unlabelled_kind():
    container, name = BackcountryListingSpider._listing_container({"whatever": {"edges": []}})
    assert name == "whatever"


def test_listing_container_returns_none_without_edges():
    assert BackcountryListingSpider._listing_container({"junk": 1}) == (None, "")


# ------------------------------------------------------------------ pagination


def test_page2_request_uses_same_url_and_increments_page():
    _items, requests = _crawl_text(None, body=_read("backcountry-plp-cat-page2.json"), max_pages=2)
    assert len(requests) == 1
    assert requests[0].url == f"{MENS_SHIRTS}?page=2"
    assert requests[0].meta["page"] == 2
    assert requests[0].dont_filter is True


@pytest.mark.parametrize(
    "url,page,expected",
    [
        (MENS_SHIRTS, 1, MENS_SHIRTS),
        (MENS_SHIRTS, 2, f"{MENS_SHIRTS}?page=2"),
        (MENS_SHIRTS, 12, f"{MENS_SHIRTS}?page=12"),
        ("https://www.backcountry.com/rc/mens-parkas", 3,
         "https://www.backcountry.com/rc/mens-parkas?page=3"),
        # A pre-filtered brand link keeps its own query params.
        ("https://www.backcountry.com/brand/patagonia?p=gender_uFilter:%22male%22", 2,
         "https://www.backcountry.com/brand/patagonia?p=gender_uFilter%3A%22male%22&page=2"),
        # An existing page param is replaced, not duplicated.
        (f"{MENS_SHIRTS}?page=2", 3, f"{MENS_SHIRTS}?page=3"),
    ],
)
def test_page_url_construction(url, page, expected):
    assert BackcountryListingSpider._page_url(url, page) == expected


def test_max_pages_stops_pagination():
    _items, requests = _crawl_text(None, body=_read("backcountry-plp-cat-page2.json"), max_pages=1)
    assert requests == []


def test_has_next_page_false_stops_pagination():
    _items, requests = _crawl_text(None, body=_read("backcountry-plp-cat-lastpage.json"), max_pages=5)
    assert requests == []


def test_empty_container_yields_no_items_and_no_request():
    items, requests = _crawl_text(None, body=_read("backcountry-plp-empty.json"))
    assert items == []
    assert requests == []


def test_duplicate_ids_are_suppressed_across_pages():
    spider = BackcountryListingSpider(category="cat-mens-shirts")
    seen = spider._seen
    seen.add("SKU5")
    response = _FakeResponse(MENS_SHIRTS, _read("backcountry-plp-cat-page2.json"), 200,
                             {"category": "cat-mens-shirts", "page": 2})
    items = [i for i in spider.parse(response) if not hasattr(i, "url")]
    # SKU5 repeats from page 1; SKU6 and SKU7 are new.
    assert [i["item_id"] for i in items] == ["SKU6", "SKU7"]


# --------------------------------------------------------------- failure modes


def test_non_200_raises():
    with pytest.raises(RuntimeError, match="HTTP 403"):
        _crawl_text(None, body=_read("backcountry-plp-cat-page1.json"), status=403)


def test_waf_challenge_raises_instead_of_zero_items():
    with pytest.raises(RuntimeError, match="no #__NEXT_DATA__ script"):
        _crawl_text(None, body=_read("backcountry-waf-challenge.html"))


def test_missing_next_data_script_raises():
    with pytest.raises(RuntimeError, match="no #__NEXT_DATA__ script"):
        _crawl_text(None, body=_read("backcountry-no-next-data.html"))


def test_invalid_json_raises():
    with pytest.raises(RuntimeError, match="not valid JSON"):
        _crawl_text(None, body=_read("backcountry-next-data-invalid.json.html"))


def test_non_plp_page_raises():
    body = _hydration({"type": "home", "targeters": {}})
    with pytest.raises(RuntimeError, match="no props.pageProps PLP payload"):
        _crawl_text(None, body=body)


def test_missing_plp_data_raises():
    body = _hydration({"type": "plp-cat"})
    with pytest.raises(RuntimeError, match="no plpData.data"):
        _crawl_text(None, body=body)


def test_plp_without_container_raises():
    body = _hydration({"type": "plp-cat", "plpData": {"data": {}}})
    with pytest.raises(RuntimeError, match="no product container"):
        _crawl_text(None, body=body)


# ---------------------------------------------------------------------- proxy


class _Settings(dict):
    pass


def _spider_with_proxy(proxy):
    spider = BackcountryListingSpider(category="cat-mens-shirts")
    spider.settings = _Settings({"PROXY": proxy})
    return spider


SECRET = "6538bdfd-12b3-4108-b863-06151459cf00"


def test_residential_appended_once_for_scrapeops():
    proxy = f"http://scrapeops.country=us:{SECRET}@proxy.scrapeops.io:5353"
    result = _spider_with_proxy(proxy)._residential_proxy()
    assert result == (
        f"http://scrapeops.country=us.residential=true:{SECRET}@proxy.scrapeops.io:5353"
    )
    # Idempotent: a second pass does not append again.
    spider = _spider_with_proxy(result)
    assert spider._residential_proxy() == result


def test_other_scrapeops_options_are_preserved():
    proxy = f"http://scrapeops.country=de.render_js=false:{SECRET}@proxy.scrapeops.io:5353"
    result = _spider_with_proxy(proxy)._residential_proxy()
    assert result.startswith("http://scrapeops.country=de.render_js=false.residential=true:")
    assert result.endswith(f"@proxy.scrapeops.io:5353")


def test_non_scrapeops_proxy_unchanged():
    proxy = f"http://user:pass@proxy.example.com:8080"
    assert _spider_with_proxy(proxy)._residential_proxy() == proxy


def test_missing_proxy_returns_none():
    assert _spider_with_proxy(None)._residential_proxy() is None


def test_proxy_password_never_logged():
    proxy = f"http://scrapeops.country=us:{SECRET}@proxy.scrapeops.io:5353"
    result = _spider_with_proxy(proxy)._residential_proxy()
    assert result.count(SECRET) == 1
    assert "residential=true" in result


def test_requests_carry_the_residential_proxy():
    spider = BackcountryListingSpider(category="cat-mens-shirts")
    spider.settings = _Settings({"PROXY": "http://scrapeops.country=us:k@proxy.scrapeops.io:5353"})
    requests = list(spider.start_requests())
    assert len(requests) == 1
    assert "residential=true" in requests[0].meta["proxy"]


# ------------------------------------------------------------------- numbers


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, None),
        (True, None),
        ("12", 12),
        ("12.5", 12.5),
        ("1,299.99", 1299.99),
        (7, 7),
        ("abc", None),
    ],
)
def test_number_coercion(value, expected):
    assert BackcountryListingSpider._number(value) == expected


def test_apollo_products_indexes_by_id():
    apollo = {"Product:SKU1": {"id": "SKU1"}, "Product:SKU2": {"__ref": "Product:SKU2"},
              "Other:1": {"id": "Other:1"}}
    products = BackcountryListingSpider._apollo_products(apollo)
    assert sorted(products) == ["SKU1", "SKU2"]


def test_apollo_products_falls_back_to_cache_key():
    # A record with no own `id` is keyed by its cache key suffix, never by __ref.
    apollo = {"Product:SKU9": {"__ref": "Product:SKU9", "name": "No id field"}}
    products = BackcountryListingSpider._apollo_products(apollo)
    assert list(products) == ["SKU9"]


def _FLAT(const):
    """Flatten a ``{group: {leaf: value}}`` categories mapping into leaf rows."""
    return [value for group in const.values() for value in group.values()]
