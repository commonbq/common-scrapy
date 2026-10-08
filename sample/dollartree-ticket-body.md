# Add `dollartree_listing` spider — Dollar Tree (top 20 categories, Oracle Commerce Cloud guided-search JSON)

## Goal

Add a `dollartree_listing` spider for **Dollar Tree** (`www.dollartree.com`), one of the highest-traffic US discount retailers (~$30B revenue, 16,000+ stores, tens of millions of monthly visits). Dollar Tree is **not currently represented** under `common/spiders/` and there is **no open/closed Dollar Tree issue** in this repository (verified: no `dollar*`/`dollartree*` spider files, no repo references, no matching issue).

Follow the conventions of the existing listing spiders and subclass `BaseListingSpider`.

## ⚠️ Proxy / capture note

The repository-configured **ScrapeOps proxy currently returns its credits-exhausted envelope** for every request:

```json
{"API Credits":"You have consumed all your API credits. Please upgrade to a larger plan to activate more credits."}
```

(Confirmed on 2026-10-08 for `httpbin.org`, `mercari.com`, `fivebelow.com`, and `dollartree.com`; the proxy CONNECT tunnel is established — `HTTP/1.1 200` — and ScrapeOps replies with the envelope, and its TLS cert is untrusted so `curl` needs `-k`.)

Therefore all artifacts below were captured by **direct fetch** (no proxy). `dollartree.com` served HTTP 200 for all pages/APIs without blocking. The spider itself should still route through `SCRAPEOPS_PROXY` like the other listing spiders; **re-verify through ScrapeOps once credits are restored**.

## Target site

- **Site:** https://www.dollartree.com
- **Platform:** **Oracle Commerce Cloud (OCC)** — storefront `siteUS`, JS bundles under `/file/.../storeJS/26.09/`, widget registry at `/ccstoreui/v1/registry`, catalogue via OCC "guided search" (Endeca) JSON.

## 1. Categories dict (top 20)

Full category inventory was harvested from two authoritative sources:

1. `https://www.dollartree.com/categorySitemap.xml` (index → **615 category URLs**; `staticSitemap.xml`, `productSitemap.xml` also exist).
2. The OCC collection tree via `/ccstoreui/v1/collections/rootCategory` → `category` → `department` (33 departments, each with child categories, `route` and `dimensionId`).

Each category is filtered server-side through the OCC guided-search XHR by its **Endeca `dimensionId`** (see §3). The top 20 below are ranked by **live product count** (`resultsList.totalNumRecs` for each `dimensionId`):

| # | Category | URL | `dimensionId` | Products |
|---|----------|-----|---------------|----------|
| 1 | Food, Candy & Drinks | https://www.dollartree.com/department/food-candy-drinks | 477714525 | 2146 |
| 2 | Holidays | https://www.dollartree.com/department/holidays | 2264625405 | 1541 |
| 3 | Health & Beauty Supplies | https://www.dollartree.com/department/health-beauty-supplies | 890155376 | 1300 |
| 4 | Christmas | https://www.dollartree.com/holidays/christmas | 2506507028 | 851 |
| 5 | Party Supplies | https://www.dollartree.com/department/party-supplies | 4070223595 | 838 |
| 6 | Office & School Supplies | https://www.dollartree.com/department/office-school-supplies | 1697834676 | 825 |
| 7 | Seasons & Occasions | https://www.dollartree.com/department/seasons-occasions | 3856293076 | 805 |
| 8 | Kitchen & Dining | https://www.dollartree.com/department/kitchen-dining | 2026343247 | 773 |
| 9 | Toys, Books, Puzzles & Games | https://www.dollartree.com/department/toys-books-crafts | 256284133 | 765 |
| 10 | Cleaning & Storage | https://www.dollartree.com/department/cleaning-storage | 2636629494 | 680 |
| 11 | Floral & Home Decor | https://www.dollartree.com/department/floral-home-decor | 3380301068 | 615 |
| 12 | Toys | https://www.dollartree.com/toys-books-puzzles-games/toys | 222478146 | 593 |
| 13 | Household & Pet Supplies | https://www.dollartree.com/department/household-pet-supplies | 1422104691 | 579 |
| 14 | Snacks | https://www.dollartree.com/food-candy-drinks/snacks | 922829371 | 549 |
| 15 | Food | https://www.dollartree.com/food-candy-drinks/food | 1675155572 | 516 |
| 16 | Drinks | https://www.dollartree.com/food-candy-drinks/drinks | 617538265 | 482 |
| 17 | Candy & Gum | https://www.dollartree.com/food-candy-drinks/candy-gum | 1669243216 | 477 |
| 18 | Halloween Shop | https://www.dollartree.com/holidays/halloween | 1585155482 | 448 |
| 19 | New Arrivals | https://www.dollartree.com/department/new-arrivals | 3856621262 | 390 |
| 20 | Arts & Crafts Supplies | https://www.dollartree.com/department/arts-crafts-supplies | 577154638 | 376 |

Shaped as a plain `name -> url` dict for the spider:

```python
CATEGORIES = {
    "food-candy-drinks":        "https://www.dollartree.com/department/food-candy-drinks",
    "holidays":                 "https://www.dollartree.com/department/holidays",
    "health-beauty-supplies":   "https://www.dollartree.com/department/health-beauty-supplies",
    "christmas":                "https://www.dollartree.com/holidays/christmas",
    "party-supplies":           "https://www.dollartree.com/department/party-supplies",
    "office-school-supplies":   "https://www.dollartree.com/department/office-school-supplies",
    "seasons-occasions":        "https://www.dollartree.com/department/seasons-occasions",
    "kitchen-dining":           "https://www.dollartree.com/department/kitchen-dining",
    "toys-books-crafts":        "https://www.dollartree.com/department/toys-books-crafts",
    "cleaning-storage":         "https://www.dollartree.com/department/cleaning-storage",
    "floral-home-decor":        "https://www.dollartree.com/department/floral-home-decor",
    "toys-books-puzzles-games/toys": "https://www.dollartree.com/toys-books-puzzles-games/toys",
    "household-pet-supplies":   "https://www.dollartree.com/department/household-pet-supplies",
    "food-candy-drinks/snacks": "https://www.dollartree.com/food-candy-drinks/snacks",
    "food-candy-drinks/food":   "https://www.dollartree.com/food-candy-drinks/food",
    "food-candy-drinks/drinks": "https://www.dollartree.com/food-candy-drinks/drinks",
    "food-candy-drinks/candy-gum": "https://www.dollartree.com/food-candy-drinks/candy-gum",
    "holidays/halloween":       "https://www.dollartree.com/holidays/halloween",
    "new-arrivals":             "https://www.dollartree.com/department/new-arrivals",
    "arts-crafts-supplies":     "https://www.dollartree.com/department/arts-crafts-supplies",
}
```

**Attached artifacts:**

- `sample/dollartree_category_dict.json` — full dict: each department → `{url, dimensionId, productCount, subcategoryCount, subcategories:[...]}` plus a `_sitemap_only_categories` list of the 447 additional sitemap URLs.
- `sample/dollartree_top20_categories.json` — the ranked top 20 as JSON.

## 2. Verified first product listing

First top category: **Food, Candy & Drinks** (`/department/food-candy-drinks`, `dimensionId=477714525`).

```text
GET https://www.dollartree.com/department/food-candy-drinks
HTTP 200, 16,694 bytes
# server-rendered shell only — NO products in the HTML
```

The HTML shell contains the breadcrumb/nav state but **no product cards** (`grep -c 'product.repositoryId'` = **0**). The real product grid is fetched client-side:

```text
GET https://www.dollartree.com/ccstoreui/v1/search?N=477714525&Nrpp=6&No=0
Headers: X-CCProfileType: storefrontUI, Accept: application/json
HTTP 200, 220,753 bytes
resultsList.totalNumRecs = 2146      # full category product count
resultsList.recsPerPage  = 6
```

Products are real and complete: each result is a grouped SKU record whose nested `records[0].attributes` carries `product.id`, `product.displayName`, `product.route`, `sku.activePrice`, `product.primaryImageAltText`, `product.primaryFullImageURL`, `product.longDescription`, dimensions, ratings, etc.

Example (first record):

```json
{
  "product.id": "354662",
  "product.displayName": "Lil' Dutch Maid Duplex Crème Cookies.",
  "product.route": "/lil-dutch-maid-duplex-crme-cookies/354662",
  "sku.activePrice": "1.250000",
  "product.primaryImageAltText": "Lil Dutch Maid Duplex Crème Cookies, 16-oz.",
  "product.primaryFullImageURL": "/ccstore/v1/images/?source=/file/v4476752558428568044/products/354662.jpg"
}
```

## 3. How the products load — AJAX XHR (OCC guided search)

Dollar Tree is **not** Next.js and has **no `__NEXT_DATA__` / hydration state**. It is **Oracle Commerce Cloud** where the PLP is assembled by an **AJAX XHR against the OCC guided-search service**:

- Category page HTML embeds `ccNavState` including `"pageid":"category"` and `"pageContext":"<id>"` (e.g. `"pageContext":"1149"` for Food, Candy & Drinks).
- The **`pageContext` id is the OCC collection id**; the collection object (`/ccstoreui/v1/collections/<id>`) exposes the **Endeca `dimensionId`** used to filter the catalogue, e.g. Dinnerware → `dimensionId: 4080624943`.
- The grid XHR is:
  ```text
  GET /ccstoreui/v1/search?N=<dimensionId>&Nrpp=<pageSize>&No=<offset>
  ```
  `N` = Endeca dimension value, `Nrpp` = records per page, `No` = zero-based offset. Verified: `N=4080624943` (Dinnerware) → `totalNumRecs=166`; `N=477714525` (Food, Candy & Drinks) → `totalNumRecs=2146`.
- Pagination is offset-based via `No` (pagingActionTemplate: `?No={offset}&Nrpp={recordsPerPage}&categoryId=<id>`); there are **no numbered page URLs**.
- Supporting endpoints: `/ccstoreui/v1/registry` (endpoint map), `/ccstoreui/v1/collections/{id}` (category → `dimensionId` + children), `/ccstoreui/v1/products?categoryId=<id>` (category meta; returns 0 direct products — the grid always comes from `/ccstoreui/v1/search`).

**Attached artifacts:**

- `sample/dollartree-category-shell-food-candy-drinks.html` — the 16,694-byte category page shell (shows `ccNavState.pageContext`, no products).
- `sample/dollartree-search-xhr-food-candy-drinks.json` — trimmed sample of the `…/search?N=477714525…` XHR (request URL/headers + first 3 products + pagination metadata).
- `sample/dollartree-collection-dinnerware.json` — collection object showing `id`/`route`/`dimensionId` mapping.

## 4. Implementation guidance

Create `common/spiders/dollartree_listing_spider.py` (+ `dollartree_categories.py`), subclassing `BaseListingSpider`:

1. For each category URL in `CATEGORIES`, resolve the **collection id** and **`dimensionId`** once (either hard-code the `dimensionId`s from `sample/dollartree_top20_categories.json`, or fetch `/ccstoreui/v1/collections/{id}` and read `dimensionId` — the id comes from `ccNavState.pageContext` in the category HTML).
2. Request the guided-search XHR directly, sending `X-CCProfileType: storefrontUI` and `Accept: application/json`:
   ```
   /ccstoreui/v1/search?N=<dimensionId>&Nrpp=24&No=<offset>
   ```
   Page until `firstRecNum + recsPerPage > totalNumRecs`.
3. Parse records from `resultsList.records[]`; each product's fields live in the nested `records[0].attributes`. Map:
   - `product.id` → item id; `product.displayName` / `product.primaryImageAltText` → title
   - `sku.activePrice` (and `sku.maxActivePrice`/`sku.minActivePrice`) → price
   - `product.route` → product URL (`https://www.dollartree.com` + route)
   - `product.primaryFullImageURL` → image; `product.longDescription` → description; `product.category` → category
4. Honour the repo's ScrapeOps proxy middleware (`SCRAPEOPS_PROXY`) for both the HTML shell and the JSON XHR; keep a realistic `User-Agent`. Retry/backoff on 429/403.
5. Add a `tests/test_dollartree_listing_spider.py` fixture based on the attached XHR sample (the response shape is stable OCC/Endeca JSON).

_Discovery + captures performed 2026-10-08._
