# Add `dollargeneral_listing` spider — Dollar General (US, top 20 categories, server-rendered AEM product cards + `?page=N` pagination)

## Goal

Add a `dollargeneral_listing` spider for **Dollar General** (`www.dollargeneral.com`), one of the highest-traffic US retailers (≈19,000+ stores, one of the top US grocery/discount sites, on the order of **100M+ monthly visits**). Dollar General is **not currently represented** under `common/spiders/` and there is **no Dollar General issue** in this repository (verified: no `dollargeneral*`/`dollar_general*` spider files or repo references; the only "dollar" issue is #326 for *Dollar Tree*, a different company).

Follow the conventions of the existing listing spiders and subclass `BaseListingSpider`.

## Target site

- **Site:** https://www.dollargeneral.com
- **Platform:** Adobe Experience Manager (AEM) storefront — `data-cmp-data-layer` / `adobeDataLayer` (Launch/Adobe Analytics), components under `dollargeneral/components/...`. Product listing grids are **server-rendered HTML** (no `__NEXT_DATA__` / no required XHR for the first page).
- **Traffic:** major US discount retailer; large, evergreen grocery + household + seasonal catalogue.

## 1. Categories dict (top 20)

Full category inventory was harvested from the authoritative sitemap:

```text
GET https://www.dollargeneral.com/sitemap.xml            -> sitemapindex
GET https://www.dollargeneral.com/sitemap-main.xml       -> 33,558 URLs (store-directory + /c/ categories)
```

**1,383 `/c/...` category URLs** across **25 top-level groups** (plus store-directory and coupon/ad sitemaps, excluded). Promotion/utility nodes were dropped when ranking: `digital-shelves` (343 promo shelves e.g. `2-for-6-on-select-post-cereal`), `ds`, `collections`, `dg-brands`, `dg-autodeliver`.

The top 20 (ranked by **breadth** = number of descendant `/c/` sub-category paths):

| # | Category | URL | Subcategories |
|---|----------|-----|---------------|
| 1 | On Sale | https://www.dollargeneral.com/c/on-sale | 118 |
| 2 | Food & Beverage | https://www.dollargeneral.com/c/food-beverage | 113 |
| 3 | Seasonal | https://www.dollargeneral.com/c/seasonal | 72 |
| 4 | Christmas | https://www.dollargeneral.com/c/christmas | 61 |
| 5 | Household | https://www.dollargeneral.com/c/household | 60 |
| 6 | Personal Care | https://www.dollargeneral.com/c/personal-care | 58 |
| 7 | Toys | https://www.dollargeneral.com/c/toys | 57 |
| 8 | Home | https://www.dollargeneral.com/c/home | 50 |
| 9 | Cleaning | https://www.dollargeneral.com/c/cleaning | 46 |
| 10 | Kitchen & Dining | https://www.dollargeneral.com/c/kitchen-dining | 41 |
| 11 | Beauty | https://www.dollargeneral.com/c/beauty | 36 |
| 12 | Apparel | https://www.dollargeneral.com/c/apparel | 33 |
| 13 | Pet | https://www.dollargeneral.com/c/pet | 32 |
| 14 | Office & School Supplies | https://www.dollargeneral.com/c/office-school-supplies | 31 |
| 15 | Health | https://www.dollargeneral.com/c/health | 27 |
| 16 | Party & Occasions | https://www.dollargeneral.com/c/party-occasions | 20 |
| 17 | Electronics | https://www.dollargeneral.com/c/electronics | 15 |
| 18 | Auto & Hardware | https://www.dollargeneral.com/c/auto-hardware | 14 |
| 19 | Outdoor Living | https://www.dollargeneral.com/c/outdoor-living | 13 |
| 20 | Baby | https://www.dollargeneral.com/c/baby | 10 |

Shaped as a plain `name -> url` dict for the spider:

```python
CATEGORIES = {
    "on-sale":               "https://www.dollargeneral.com/c/on-sale",
    "food-beverage":         "https://www.dollargeneral.com/c/food-beverage",
    "seasonal":              "https://www.dollargeneral.com/c/seasonal",
    "christmas":             "https://www.dollargeneral.com/c/christmas",
    "household":             "https://www.dollargeneral.com/c/household",
    "personal-care":         "https://www.dollargeneral.com/c/personal-care",
    "toys":                  "https://www.dollargeneral.com/c/toys",
    "home":                  "https://www.dollargeneral.com/c/home",
    "cleaning":              "https://www.dollargeneral.com/c/cleaning",
    "kitchen-dining":        "https://www.dollargeneral.com/c/kitchen-dining",
    "beauty":                "https://www.dollargeneral.com/c/beauty",
    "apparel":               "https://www.dollargeneral.com/c/apparel",
    "pet":                   "https://www.dollargeneral.com/c/pet",
    "office-school-supplies":"https://www.dollargeneral.com/c/office-school-supplies",
    "health":                "https://www.dollargeneral.com/c/health",
    "party-occasions":       "https://www.dollargeneral.com/c/party-occasions",
    "electronics":           "https://www.dollargeneral.com/c/electronics",
    "auto-hardware":         "https://www.dollargeneral.com/c/auto-hardware",
    "outdoor-living":        "https://www.dollargeneral.com/c/outdoor-living",
    "baby":                  "https://www.dollargeneral.com/c/baby",
}
```

**Attached artifacts:**

- `sample/dollargeneral_category_dict.json` — full nested dict: every top-level group → `{url, subcategories:{name -> {url, subcategories{...}}}}` (1,382 nodes).
- `sample/dollargeneral_top20_categories.json` — the ranked top 20 as JSON.

## 2. Verified first product listing

First top category: **On Sale** (`/c/on-sale`).

```text
GET https://www.dollargeneral.com/c/on-sale
HTTP 200, 462,559 bytes
# 32 unique products server-rendered as HTML product cards
```

Normalized sample items (`sample/dollargeneral-on-sale-products-sample.json`):

```json
{
  "item_id": "430002404825",
  "title": "Halloween-Iridescent-Blow-Mold-Ghost-with-Bubble-Light-Décor,-2-Assorted-Styles",
  "url": "https://www.dollargeneral.com/p/Halloween-Iridescent-Blow-Mold-Ghost-with-Bubble-Light-D%C3%A9cor,-2-Assorted-Styles/430002404825",
  "price": "$8.0",
  "image": "https://s7d1.scene7.com/is/image/dolgen/dg-43891101-1"
}
```

## 3. How products are loaded (investigation)

Dollar General does **not** require an XHR to get the first page of products — the grid is **server-rendered in the HTML** and hydrated client-side afterwards. Findings:

- **No `__NEXT_DATA__`, no `self.__next_f`, no Nuxt/Redux state blob.** The page is AEM-rendered HTML; the only inline state is `window.__FEATURE_FLAGS__` and an `application/json` block, plus the Adobe data layer (`adobeDataLayer` / `data-cmp-data-layer`).
- **Product cards are plain HTML** — the canonical parse target:

```html
<div class="product-card">
  <div class="product-card__image-container">
    <img class="product--image" src="https://s7d1.scene7.com/is/image/dolgen/dg-43891101-1" .../>
    <div class="product-card__add-button-wrapper">
      <button aria-label="Add to Cart" class="product--add-button">...</button>
    </div>
  </div>
  <div class="product-card__details">
    <div class="product--info">
      <span class="product-price product-card__current-price">&dollar;8.0</span>
    </div>
    <a class="product--title" href="/p/Halloween-Iridescent-Blow-Mold-Ghost-with-Bubble-Light-D%C3%A9cor,-2-Assorted-Styles/430002404825">
      Halloween-Iridescent-Blow-Mold-Ghost-with-Bubble-Light-Décor,-2-Assorted-Styles
    </a>
    <div class="product--deal">... "Offer" ... BUY 1 ... GET 1 50% OFF ...</div>
  </div>
</div>
```

  - PDP href pattern: `/p/<slug>/<item_id>` (slug is URL-encoded). `item_id` = trailing numeric segment.
  - Price: `span.product-card__current-price` (HTML entity `&dollar;`); some cards also carry a struck-through previous price / `product--deal` offer markup.
  - Image: `img.product--image` (Adobe Scene7 `s7d1.scene7.com`).
- **The first cards are duplicated** inside a `splide` carousel (`ul.splide__list.dg-splide-carousel__splide-list`) that precedes/overlaps the main grid — a spider should **de-duplicate by `item_id`** and/or skip the `splide` carousel block, otherwise it will pick up the same products twice.
- A small carousel block also emits malformed hrefs like `href="/p//18200150470"` (missing slug); these should be ignored in favour of the canonical `/p/<slug>/<id>` links.
- **JSON-LD** on the category page is only `BreadcrumbList` (no `ItemList`/`Product` blocks), so the HTML cards are the reliable parse target — not JSON-LD.

### Pagination

Classic **server-rendered `?page=N`** (1-based) pagination via `<a href="/c/on-sale?page=N">`; server emits ~363 page links for On Sale. Verified:

| Request | HTTP | distinct `/p/.../<id>` links | overlap with p1 |
|---------|------|------------------------------|-----------------|
| `/c/on-sale` | 200 | 56 (32 unique cards) | — |
| `/c/on-sale?page=2` | 200 | 56 | 32 (carousel-only overlap) |

Stop paging when a page yields `0` new unique `item_id`s (or when the last page link is reached).

## 4. Proposed spider

- **Files:** `common/spiders/dollargeneral_listing_spider.py`, `common/spiders/dollargeneral_categories.py` (top-20 dict), `sample/` captures.
- **Mode:** `html` (server-rendered product cards). No XHR/JSON API needed for listing or pagination.
- **Parse target:** `div.product-card` → `a.product--title[href]` (item_id from trailing segment), `a.product--title` text (title), `span.product-card__current-price` (price), `img.product--image[src]` (image), plus optional `product--deal` offer text.
- **De-dup:** unique by `item_id`; drop `ul.splide__list` carousel block and malformed `/p//<id>` hrefs.
- **Normalized fields:** `item_id`, `title`, `url`, `image`, `price`, `currency` (`USD`), `deal` (optional), `category`, `source`.
- **Pagination:** `?page=2,3,...` (1-based); stop when no new unique `item_id`s.
- **Proxy:** `SCRAPEOPS_PROXY` (country `us`) — proxy required in production; the captures in `sample/` were taken through ScrapeOps.

## 5. Acceptance criteria

- [ ] Spider runs without crash.
- [ ] `dollargeneral_listing -a category=on-sale -a max_pages=1` returns non-zero items.
- [ ] Items de-duplicated by `item_id` (carousel duplicates and `/p//<id>` malformed links excluded).
- [ ] `?page=N` pagination handled; stops on no-new-ids.
- [ ] Output fields normalized (`item_id`, `title`, `url`, `image`, `price`, `currency`, etc.).
- [ ] README entry + sample output added.

## Environment
- Capture date: 2026-10-08 (Asia/Bangkok)
- Proxy: ScrapeOps (`SCRAPEOPS_PROXY`, country `us`) — HTTP 200 for all captures above
- Platform: Adobe Experience Manager (AEM) + Adobe Launch data layer; server-rendered product grid, no `__NEXT_DATA__`
