## Goal

Add a `hobbylobby_listing` spider for **Hobby Lobby** (`hobbylobby.com`), the largest privately-owned US arts-and-crafts retailer (900+ stores, heavy e-commerce traffic).

There is currently **no Hobby Lobby spider** under `common/spiders/` and **no open or closed Hobby Lobby issue** in this repository (verified against the full issue list). Unlike the many accommodation/real-estate listings already covered, this is a large **retail product catalogue** with a clean, fully server-rendered listing mechanism.

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, the sitemap index, 26 `*_Categories` sitemaps and **22 category listing pages** all returned HTTP 200.

## Category inventory (all categories → dict)

Hobby Lobby's taxonomy lives in **per-department category sitemaps** exposed from `https://www.hobbylobby.com/sitemap.xml`:

```
https://www.hobbylobby.com/sitemap-ART_Categories.xml
https://www.hobbylobby.com/sitemap-BEADS_Categories.xml
https://www.hobbylobby.com/sitemap-CHRISTMAS_Categories.xml
... (26 `*_Categories.xml` files)
https://www.hobbylobby.com/sitemap-YARN_Categories.xml
```

Every category URL follows `https://www.hobbylobby.com/<path...>/c/<hierarchy-id>` where the id encodes depth:

- `c/8` → department (level 1)
- `c/8-168` → subcategory (level 2)
- `c/8-168-1309` → leaf category (level 3)

Aggregated across all 26 department sitemaps: **1,071 category URLs** (22 departments, 196 level-2, 853 level-3). The full `{slug: url}` map is attached as `sample/hobbylobby-categories.json`.

> **Important:** department (level-1) pages are **SEO landing pages** — they render marketing copy and subcategory tiles but **no product grid** (no Algolia payload, no `ItemList`). Product-bearing pages are the level-2 / level-3 categories. The 20 categories below are level-2 categories that were **each verified live to carry a product grid**.

## Top 20 categories

```python
HOBBY_LOBBY_CATEGORIES = {
    "art-supplies-painting-supplies":            "https://www.hobbylobby.com/art-supplies/painting-supplies/c/8-168",
    "beads-jewelry-beads":                       "https://www.hobbylobby.com/beads-jewelry/beads/c/2-100",
    "christmas-decorations-christmas-ornaments": "https://www.hobbylobby.com/christmas-decorations/christmas-ornaments/c/58-825",
    "christmas-decorations-christmas-crafts":    "https://www.hobbylobby.com/christmas-decorations/christmas-crafts/c/58-800",
    "clothes-accessories-bags-bag-accessories":  "https://www.hobbylobby.com/clothes-accessories/bags-bag-accessories/c/11-196",
    "clothes-accessories-hair-accessories":      "https://www.hobbylobby.com/clothes-accessories/hair-accessories/c/11-601",
    "crafts-hobbies-basic-crafts":               "https://www.hobbylobby.com/crafts-hobbies/basic-crafts/c/9-172",
    "crafts-hobbies-kids-crafts-activities":     "https://www.hobbylobby.com/crafts-hobbies/kids-crafts-activities/c/9-174",
    "fabric-sewing-quilting-fabrics":            "https://www.hobbylobby.com/fabric-sewing/quilting-fabrics/c/6-136",
    "floral-artificial-flowers":                 "https://www.hobbylobby.com/floral/artificial-flowers/c/4-120",
    "home-decor-frames-candles-fragrance":       "https://www.hobbylobby.com/home-decor-frames/candles-fragrance/c/3-111",
    "home-decor-frames-decor-pillows":           "https://www.hobbylobby.com/home-decor-frames/decor-pillows/c/3-110",
    "home-decor-frames-frames-framing-supplies": "https://www.hobbylobby.com/home-decor-frames/frames-framing-supplies/c/3-113",
    "kitchen-baking-bakeware-cookware":          "https://www.hobbylobby.com/kitchen-baking/bakeware-cookware/c/71-119",
    "kitchen-baking-cake-decorating-supplies":   "https://www.hobbylobby.com/kitchen-baking/cake-decorating-supplies/c/71-121",
    "party-supplies-balloons-accessories":       "https://www.hobbylobby.com/party-supplies/balloons-accessories/c/75-201",
    "party-supplies-party-tableware":            "https://www.hobbylobby.com/party-supplies/party-tableware/c/75-208",
    "scrapbook-paper-crafts-stickers-embellishments": "https://www.hobbylobby.com/scrapbook-paper-crafts/stickers-embellishments/c/7-157",
    "yarn-needle-art-crochet":                   "https://www.hobbylobby.com/yarn-needle-art/crochet/c/5-128",
    "yarn-needle-art-yarn-tools":                "https://www.hobbylobby.com/yarn-needle-art/yarn-tools/c/5-126",
}
```

### Live verification (all HTTP 200, all with a product payload)

| category | hits | pages | per page |
|---|---|---|---|
| art-supplies-painting-supplies | 254 | 22 | 12 |
| beads-jewelry-beads | 1460 | 122 | 12 |
| christmas-decorations-christmas-ornaments | 1298 | 109 | 12 |
| christmas-decorations-christmas-crafts | 694 | 58 | 12 |
| clothes-accessories-bags-bag-accessories | 309 | 26 | 12 |
| clothes-accessories-hair-accessories | 104 | 9 | 12 |
| crafts-hobbies-basic-crafts | 344 | 29 | 12 |
| crafts-hobbies-kids-crafts-activities | 1680 | 140 | 12 |
| fabric-sewing-quilting-fabrics | 687 | 58 | 12 |
| floral-artificial-flowers | 374 | 32 | 12 |
| home-decor-frames-candles-fragrance | 496 | 42 | 12 |
| home-decor-frames-decor-pillows | 1990 | 166 | 12 |
| home-decor-frames-frames-framing-supplies | 459 | 39 | 12 |
| kitchen-baking-bakeware-cookware | 45 | 4 | 12 |
| kitchen-baking-cake-decorating-supplies | 336 | 28 | 12 |
| party-supplies-balloons-accessories | 87 | 8 | 12 |
| party-supplies-party-tableware | 343 | 29 | 12 |
| scrapbook-paper-crafts-stickers-embellishments | 1313 | 110 | 12 |
| yarn-needle-art-crochet | 41 | 4 | 12 |
| yarn-needle-art-yarn-tools | 92 | 8 | 12 |

(`hits`/`pages`/`per` are read straight from the page's embedded Algolia payload.)

## First-category investigation: `art-supplies/painting-supplies/c/8-168`

```text
GET https://www.hobbylobby.com/art-supplies/painting-supplies/c/8-168
HTTP 200, 280,657 bytes
<title>Painting Supplies | Tools, Cleaners &amp; Paints | Hobby Lobby</title>
payload: index=HLNextGenEcommIndex_prd  hits=254  pages=22  hitsPerPage=12
```

### How products load — server-rendered HTML, **no AJAX/XHR and no browser needed**

This is a **Next.js App Router** app (React Server Components streaming via `self.__next_f.push(...)`; **no `__NEXT_DATA__`** — it is not Pages Router). The listing page is fully **server-rendered**; a plain HTTP request + HTML/JSON parser is enough. There are **three redundant in-HTML sources** for the same 12 products:

1. **Primary / richest — Algolia InstantSearch bootstrap** (embedded JSON, one per page):
   ```js
   <script>window[Symbol.for("InstantSearchInitialResults")] = {"HLNextGenEcommIndex_prd":{
       "state":{"index":"HLNextGenEcommIndex_prd",
                "filters":"categoryNames:\"Art Supplies\" AND categoryNames:\"Painting Supplies\""},
       "results":[{"hits":[ ...12 full hit objects... ],
                   "nbHits":254,"page":0,"nbPages":22,"hitsPerPage":12,"queryID":"..."}],
       "requestParams":[{"filters":"categoryNames:\"Art Supplies\" AND categoryNames:\"Painting Supplies\"","hitsPerPage":12}]}}</script>
   ```
   Each hit carries `sku`, `productID`, `productKey`, `objectID`, `name`/`productName`, `variantUrl`, `pdpUrl`, `variant.price`, `product.lowestPrice`/`product.highestPrice`/`product.lowestOriginalPrice`, `isInStock`, `availability`, `onlineStatus`, `department`, `category`, `categoryNames`, `categories` (lvl0/lvl1/lvl2), `quantity`, `medium`, `color-family`, `material`, `images[]`, `ratings.average`, `ratings.count`, `details` (description HTML). This single payload gives both the items **and** the pagination contract (`nbHits`, `nbPages`, `hitsPerPage`, `page`).
   Extraction tip: locate `InstantSearchInitialResults")] = ` and use a **brace-matching JSON decode** (the JSON body contains `;` inside HTML entities, so a lazy regex up to `;` breaks).

2. **Structured fallback — JSON-LD `CollectionPage`** (clean schema.org):
   ```json
   {"@context":"https://schema.org","@type":"CollectionPage","name":"Painting Supplies",
    "mainEntity":{"@type":"ItemList","itemListElement":[
      {"@type":"ListItem","position":1,"item":{"@type":"Product","url":".../p/80968391","name":"...","image":[...],"description":"<p>...</p>","offers":{...}}},
      ... 12 items ]}}
   ```

3. **Rendered cards — server-rendered DOM** (hashed CSS classes; build-dependent):
   ```html
   <a class="card_link__Ubz3T" href="/art-supplies/painting-supplies/oil-painting/master-s-touch-oil-paint---12-piece-set/p/80968391">
     <div class="card_product__coFjZ">
       <section class="card_image__jh62R"><img src="https://cdn.media.amplience.net/s/hobbylobby/..." /></section>
       <section class="card_details__Rc81U">
         <h2 class="card_title___g5fi">Master's Touch Oil Paint - 12 Piece Set</h2>
         <section class="card_rating__ckIc0"><span role="img" aria-label="3.8571 out of 5 stars"></span></section>
         ... price / favorite button ...
   ```
   → Prefer source **(1)** (or **(2)** as fallback); use **(3)** only with prefix selectors like `a[class^="card_link__"]`, since the `__hash` suffixes change between builds.

### Pagination — static `?page=N` (server-rendered, no XHR)

```html
<ul class="ais-Pagination-list">
  ...
  <li class="ais-Pagination-item"><a class="ais-Pagination-link" href="https://www.hobbylobby.com/art-supplies/painting-supplies/c/8-168?page=2" aria-label="Page 2">2</a></li>
  <li class="ais-Pagination-item ais-Pagination-item--nextPage"><a class="ais-Pagination-link" href="https://www.hobbylobby.com/art-supplies/painting-supplies/c/8-168?page=2" aria-label="Last Page, Page 2">&gt;</a></li>
</ul>
```

Page `N` is simply `https://www.hobbylobby.com/<category-path>/c/<id>?page=N` (page 1 = bare URL). **Verified live:** `?page=2` returned HTTP 200, same `nbHits=254`, same `nbHitsPerPage=12`, and a distinct 12-item set. `hitsPerPage` is 12, so `nbPages` == ceil(nbHits/12) — drive the crawl by `nbPages` (or stop on repeated/empty page), never a fixed page count.

### Field map (per product)

| field | source |
|---|---|
| `item_id` | Algolia `objectID` (or `sku`); JSON-LD `item.url` tail `/p/<objectID>` |
| `sku` | Algolia `sku` |
| `product_key` | Algolia `productKey` (e.g. `RS52220-80968391`) |
| `title` | Algolia `name` / `productName`; JSON-LD `item.name` |
| `url` | absolute of Algolia `variantUrl` (`https://www.hobbylobby.com` + path) |
| `pdp_url` | absolute of Algolia `pdpUrl` |
| `price` | Algolia `variant.price` (also `product.lowestPrice` / `product.highestPrice`) |
| `original_price` | `product.lowestOriginalPrice` / `product.highestOriginalPrice` |
| `currency` | `USD` |
| `in_stock` | `isInStock` |
| `availability` | `availability` (`BOTH` / `ONLINE` / `STORE`) |
| `online_status` | `onlineStatus` (`ACTIVE`) |
| `department` / `category` | `department` / `category` |
| `category_names` / `categories` | `categoryNames[]` / `categories.lvl0..lvl2` |
| `quantity` | `quantity` (e.g. `12 Count`) |
| `medium` / `color_family` / `material` | `medium[]` / `color-family` / `material` |
| `rating` / `reviews_count` | `ratings.average` / `ratings.count` |
| `image` / `images` | `images[].url` |
| `description` | `details` (HTML) or JSON-LD `item.description` |
| `category` (run arg) | the spider `category` slug |
| `page` | current page number |
| `source` | `"hobbylobby_instantsearch_bootstrap"` (or `..._itemlist_jsonld`) |
| `raw` | verbatim Algolia hit (or JSON-LD item) |
| `timestamp` | per-run crawl timestamp |

## Suggested implementation

- `common/spiders/hobbylobby_categories.py` — `HOBBY_LOBBY_CATEGORIES` dict above (top 20; the full 1,071-entry map is in `sample/hobbylobby-categories.json`).
- `common/spiders/hobbylobby_listing_spider.py` — subclass the shared listing base:
  - accept `-a category=<slug>` or `-a category_url=<url>`;
  - keep `meta={"proxy": settings.get("PROXY")}` on every request (ScrapeOps; the storefront is fine over the default `country=us` proxy);
  - page 1 fetch → **brace-match** the `InstantSearchInitialResults` JSON → emit hits; fall back to JSON-LD `CollectionPage.mainEntity.ItemList`; last-resort DOM prefix selectors `[class^="card_product__"]`;
  - read `nbPages` from the payload and follow `?page=N` until the last page / repeated IDs / empty hits;
  - emit `source`, `raw` and a per-run `timestamp` and populate `FEED_EXPORT_FIELDS`.
- `common/spiders/hobbylobby_categories.py` can also be used to refresh the inventory by parsing the 26 `sitemap-*_Categories.xml` files.
- README: add a `hobbylobby_listing` section + spider table row.
- Tests: `set(FEED_EXPORT_FIELDS) == set(first_item)` and a fixture asserting a payload hit parses to `{item_id, title, url, price, in_stock}`.

## Attached evidence

Pushed on branch **`cron-ticket-hobbylobby`**:

- `sample/hobbylobby-categories.json` — full 1,071-entry `{slug: url}` taxonomy aggregated from the 26 department sitemaps
- `sample/hobbylobby-top20-categories.json` — the top-20 dict above
- `sample/hobbylobby-painting-supplies-p1.html` — full first-category page (280,657 bytes, 254 products)
- `sample/hobbylobby-painting-supplies-p2.html` — same category `?page=2` (proves `?page=N` pagination, distinct items)
- `sample/hobbylobby-art-sets-p1.html` — second verified category page (`c/8-161`, 17 products)
- `sample/hobbylobby-instantsearch-payload.json` — the parsed `InstantSearchInitialResults` payload (index `HLNextGenEcommIndex_prd`, 12 hits, `nbHits`/`nbPages`/`hitsPerPage`)
- `sample/hobbylobby-itemlist.json` — the parsed JSON-LD `CollectionPage` → `ItemList` of 12 `Product` entries
- `sample/hobbylobby-product-card-sample.html` — one server-rendered product card showing every DOM hook
- `sample/hobbylobby-sitemap-index.xml` — the sitemap index (57 sitemaps, incl. the 26 `*_Categories.xml`)

## Acceptance criteria

- [ ] New `hobbylobby_listing` spider + `hobbylobby_categories.py` (top-20 dict).
- [ ] First category crawl returns ≥1 live item with `source`, `raw`, `timestamp`.
- [ ] Payload extraction is brace-matched (no fragile regex), with JSON-LD fallback.
- [ ] Pagination via `?page=N` driven by `nbPages`; no duplicate/looping pages.
- [ ] All requests go through `PROXY` (ScrapeOps); no direct hits.
- [ ] README section + spider table row.
- [ ] Tests green (`set(FEED_EXPORT_FIELDS) == set(first_item)`).
