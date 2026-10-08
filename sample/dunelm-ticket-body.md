# Add `dunelm_listing` spider — Dunelm (UK, top 20 categories, server-rendered SSR state)

## Goal

Add a `dunelm_listing` spider for **Dunelm** (`www.dunelm.com`), one of the highest-traffic UK home & furniture retailers (FTSE-250, ~200 stores, high tens of millions of monthly visits). Dunelm is **not currently represented** under `common/spiders/` and there is **no open/closed Dunelm issue** in this repository (verified: no `dunelm*` spider files, no repo references, no matching issue).

Follow the conventions of the existing listing spiders and subclass `BaseListingSpider`.

## ⚠️ Proxy / capture note

The repository-configured **ScrapeOps proxy currently returns its credits-exhausted envelope** for every request:

```json
{"API Credits":"You have consumed all your API credits. Please upgrade to a larger plan to activate more credits."}
```

Confirmed on 2026-10-08: `proxy.scrapeops.io/v1/account` reports `plan_api_credits=50000`, `used_api_credits=50016`. The CONNECT tunnel is established (`HTTP/1.1 200`) and ScrapeOps replies with the envelope; its TLS cert is untrusted for `curl` (needs `-k`). The alternate proxies in `.env` were also unusable: Bright Data returns `407 ip_forbidden` (this host IP `171.225.248.209` is not whitelisted), ScraperAPI returns `401` (invalid key).

Therefore all artifacts below were captured by **direct fetch** (no proxy). `dunelm.com` served HTTP 200 for the homepage, sitemap and PLPs without blocking. The spider itself should still route through `SCRAPEOPS_PROXY` like the other listing spiders; **re-verify through ScrapeOps once credits are restored**.

## Target site

- **Site:** https://www.dunelm.com
- **Platform:** React/Remix-style SSR storefront with **two server-rendered state containers** (see §3). Search/listing backend is **Algolia** (`search.dunelm.com`, app id `FY8PLEBN34`, index `search_prod`, public search key shipped in `reduxState.config.algolia`).
- **Traffic:** major UK retailer; seasonal + evergreen home/furniture catalogue.

## 1. Categories dict (top 20)

Full category inventory was harvested from the authoritative sitemap:

```text
GET https://www.dunelm.com/sitemap.xml          -> sitemapindex
GET https://www.dunelm.com/sitemap/category-sitemap.xml -> 670 /category/ URLs
GET https://www.dunelm.com/sitemap/product-1-sitemap.xml -> 5.1 MB product URLs
```

670 `/category/...` paths across **46 top-level departments**. Each category page is a server-rendered PLP (see §2/§3).

The top 20 below are ranked by **breadth** (number of descendant sub-category paths) after dropping non-catalogue utility nodes (`press-show`, `campaigns`, `inspiration`, `home-delivery`, `price-guarantee`):

| # | Category | URL | Subcategories |
|---|----------|-----|---------------|
| 1 | Home & Furniture | https://www.dunelm.com/category/home-and-furniture | 239 |
| 2 | Brands | https://www.dunelm.com/category/brands | 110 |
| 3 | Home Decor | https://www.dunelm.com/category/home-decor | 33 |
| 4 | Made To Measure | https://www.dunelm.com/category/made-to-measure | 18 |
| 5 | Electricals | https://www.dunelm.com/category/electricals | 18 |
| 6 | Kids | https://www.dunelm.com/category/kids | 17 |
| 7 | Garden | https://www.dunelm.com/category/garden | 17 |
| 8 | Rugs | https://www.dunelm.com/category/rugs | 16 |
| 9 | Christmas | https://www.dunelm.com/category/christmas | 16 |
| 10 | Lighting | https://www.dunelm.com/category/lighting | 14 |
| 11 | Gifts | https://www.dunelm.com/category/gifts | 14 |
| 12 | Seasonal | https://www.dunelm.com/category/seasonal | 12 |
| 13 | DIY & Decorating | https://www.dunelm.com/category/diy-and-decorating | 12 |
| 14 | Cleaning & Laundry | https://www.dunelm.com/category/cleaning-and-laundry | 11 |
| 15 | Nursery | https://www.dunelm.com/category/nursery | 8 |
| 16 | Fabric & Haberdashery | https://www.dunelm.com/category/fabric-and-haberdashery | 7 |
| 17 | Pets | https://www.dunelm.com/category/pets | 5 |
| 18 | Holiday | https://www.dunelm.com/category/holiday | 3 |
| 19 | Health & Wellbeing | https://www.dunelm.com/category/health-and-wellbeing | 1 |
| 20 | Sale | https://www.dunelm.com/category/sale | 0 |

Shaped as a plain `name -> url` dict for the spider:

```python
CATEGORIES = {
    "home-and-furniture":    "https://www.dunelm.com/category/home-and-furniture",
    "brands":                "https://www.dunelm.com/category/brands",
    "home-decor":            "https://www.dunelm.com/category/home-decor",
    "made-to-measure":       "https://www.dunelm.com/category/made-to-measure",
    "electricals":           "https://www.dunelm.com/category/electricals",
    "kids":                  "https://www.dunelm.com/category/kids",
    "garden":                "https://www.dunelm.com/category/garden",
    "rugs":                  "https://www.dunelm.com/category/rugs",
    "christmas":             "https://www.dunelm.com/category/christmas",
    "lighting":              "https://www.dunelm.com/category/lighting",
    "gifts":                 "https://www.dunelm.com/category/gifts",
    "seasonal":              "https://www.dunelm.com/category/seasonal",
    "diy-and-decorating":    "https://www.dunelm.com/category/diy-and-decorating",
    "cleaning-and-laundry":  "https://www.dunelm.com/category/cleaning-and-laundry",
    "nursery":               "https://www.dunelm.com/category/nursery",
    "fabric-and-haberdashery":"https://www.dunelm.com/category/fabric-and-haberdashery",
    "pets":                  "https://www.dunelm.com/category/pets",
    "holiday":               "https://www.dunelm.com/category/holiday",
    "health-and-wellbeing":  "https://www.dunelm.com/category/health-and-wellbeing",
    "sale":                  "https://www.dunelm.com/category/sale",
}
```

**Attached artifacts:**

- `sample/dunelm_category_dict.json` — full nested dict: every top-level category → `{url, subcategories:{name -> {url, subcategories{...}}}}` (670 paths).
- `sample/dunelm_top20_categories.json` — the ranked top 20 as JSON.

## 2. Verified first product listing

First top category: **Home & Furniture** (`/category/home-and-furniture`).

```text
GET https://www.dunelm.com/category/home-and-furniture
HTTP 200, 581,528 bytes
# 60 products server-rendered as Schema.org JSON-LD (CollectionPage -> ItemList)
```

Sample item (`sample/dunelm-department-itemlist.json`):

```json
{
  "@type": "ListItem",
  "position": 1,
  "item": {
    "@type": "Product",
    "name": "Pure Cotton Fitted Sheet",
    "url": "https://www.dunelm.com/product/pure-cotton-fitted-sheet-1000194189?defaultSkuId=30750006",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": 5195},
    "offers": {"@type": "AggregateOffer", "lowPrice": "9", "highPrice": "37", "priceCurrency": "GBP"}
  }
}
```

A **leaf PLP** (e.g. `/category/home-and-furniture/bedding`) additionally carries a richer Redux state (see §3) with 60 fully-populated products.

## 3. How products are loaded (investigation)

Dunelm does **not** require a separate XHR for the first page — the product grid is **server-rendered** inside an embedded JSON state script. There are two page shells:

### A. Leaf PLP — Redux SSR state (`#ssr-state-data`)

`GET https://www.dunelm.com/category/home-and-furniture/bedding` → HTTP 200, 1,430,997 bytes

```html
<script type="application/json" id="ssr-state-data">{ ... 1.09 MB JSON ... }</script>
```

Key path:

```text
reduxState.searchProduct.results[0].searchParam
  -> {"filterValues":{"hierarchicalCategories.lvl1":["home and furniture > bedding"]},
      "query":"","page":0,"orderBy":"ranking_desc"}

reduxState.product.partialProductById   -> 60 products (page 0)
reduxState.product.productById          -> {} (empty on PLP)
reduxState.config.algolia               -> {id:"FY8PLEBN34", key:"ae9bc9ca475f6c3d7579016da0305a33",
                                            indexes:{ranking_desc:"search_prod", ...}}
reduxState.config.enrichedProductApi    -> {"url":"https://enriched-product-api.dunelm.com"}
```

Each product in `partialProductById` carries `id`, `productUrl`, `name`, `brand`, `colors`, `priceRange{min,max}`, `rating`, `category[]`, and nested `skus[]` with `price{current,previous,history}`, `media.image[]`, `clickAndCollectEligible`, etc.

```json
{
  "id": "1000000601",
  "productUrl": "non-iron-plain-fitted-sheet-1000000601",
  "name": "Non Iron Plain Fitted Sheet",
  "brand": "Dunelm",
  "colors": ["Ivory","White","Silver","Navy"],
  "priceRange": {"wasMin": null, "wasMax": null, "min": 6, "max": 20},
  "rating": 3,
  "category": [{"key":"Home-and-Furniture","label":"Home and Furniture"},
               {"key":"Bedding","label":"Bedding"},{"key":"All-Bedding","label":"All Bedding"}],
  "skus": [{"id":"30145683","productId":"1000000601",
            "price":{"previous":[],"current":12,"history":[]},
            "media":{"image":["30145683.jpg","30145683_alt01.jpg"]}}]
}
```

(Full trimmed capture: `sample/dunelm-plp-ssr-state-bedding.json`; single product: `sample/dunelm-product-sample.json`.)

### B. Department landing — React-Query shell (`#shell-ssr-data`) + JSON-LD

`GET https://www.dunelm.com/category/home-and-furniture` → HTTP 200, `#shell-ssr-data` holds the dehydrated React-Query state + site config; products are emitted as Schema.org JSON-LD `CollectionPage`/`ItemList` (60 items) — the most robust parse target for every category page.

### C. Pagination

Query-string pagination via `?page=N` (1-based externally; reflected 0-based in `searchParam.page`):

| Request | HTTP | `searchParam.page` | products | distinct from p1 |
|---------|------|--------------------|----------|------------------|
| `/category/home-and-furniture/bedding` | 200 | 0 | 60 | — |
| `...?page=2` | 404* | 1 | 60 | yes (0 overlap) |
| `...?page=3` | 404* | 2 | 60 | yes |

\* Dunelm returns an **HTTP 404 status while still server-rendering the requested page's listing**. A spider must **not** treat `?page>=2` 404s as a fetch failure — parse the body (or ignore status for paginated PLP) and keep paging until `< 60` products.

The richer backend is **Algolia** (`search.dunelm.com`, index `search_prod`, filter `hierarchicalCategories.lvl1:"<lvl0> > <lvl1>"`, `page` 0-based). The `-dsn.algolia.net` host is not publicly resolvable; the key above is the storefront search key — verify whether it can drive the public `search.dunelm.com` proxy before relying on the API path.

## 4. Proposed spider

- **Files:** `common/spiders/dunelm_listing_spider.py`, `common/spiders/dunelm_categories.py` (top-20 dict), `sample/` captures.
- **Mode:** `bootstrap` (SSR JSON) + `html` (JSON-LD fallback).
- **Preferred parse order:**
  1. `#ssr-state-data` → `reduxState.product.partialProductById` (rich fields) when present;
  2. else JSON-LD `CollectionPage` → `itemListElement[].item` (name, url, rating, offers.lowPrice/highPrice/priceCurrency).
- **Normalized fields:** `item_id` (product id), `title`, `brand`, `url`, `image`, `price`/`price_min`/`price_max`, `currency` (`GBP`), `rating`, `reviews_count`, `category`, `source`.
- **Pagination:** `?page=2,3,...` (accept HTTP 404 with body), stop when item count `< 60`.
- **Proxy:** `SCRAPEOPS_PROXY` (country `gb`/`us`); re-verify once credits restored.

## 5. Acceptance criteria

- [ ] Spider runs without crash.
- [ ] `dunelm_listing -a category=home-and-furniture -a max_pages=1` returns non-zero items.
- [ ] Both parse paths exercised (department JSON-LD + leaf `#ssr-state-data`).
- [ ] `?page=N` pagination handled incl. the 404-with-body quirk.
- [ ] Output fields normalized (`item_id`, `title`, `url`, price fields, `currency`, etc.).
- [ ] README entry + sample output added.

## Environment
- Capture date: 2026-10-08 (Asia/Bangkok)
- ScrapeOps: credits exhausted (50016/50000) → direct fetch used
- Bright Data: 407 ip_forbidden; ScraperAPI: 401 invalid key
