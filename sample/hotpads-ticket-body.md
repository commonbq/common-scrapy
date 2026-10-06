## Goal

Add a `hotpads_listing` spider for **HotPads** (`hotpads.com`), a leading US rental marketplace (Zillow Group). There is currently **no HotPads spider** under `common/spiders/` and **no open/closed HotPads issue** in this repository (checked with `gh issue list --state all --search "hotpads in:title"` → empty, and `grep -ril hotpads` over the repo → only this ticket's own sample files).

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, `robots.txt`, the city sitemap index, two state city sitemaps and **twenty city listing pages** all returned HTTP 200.

HotPads has **no classic retail "category" taxonomy**. Its catalogue is organised by **city/market search pages** (`https://hotpads.com/<city-slug>/apartments-for-rent`), each of which is a product listing ("products" = rental properties / apartment buildings). Filter variants exist as other paths (`/<city-slug>/houses-for-rent`, `/rooms-for-rent`, `/condos-for-rent`, `.../page/N`) and as query params (`?maxPrice=`, `?beds=`, `?pets=`, ...).

## Top 20 category URLs

City slugs come from the live city sitemap index `https://hotpads.com/sitemap-city-index.xml` (per-state sitemaps like `sitemap-city-apartments-for-rent-<ST>_0.xml.gz`; **241 `<loc>`** in the index, tens of thousands of city URLs in total). The dict below is the top 20 US rental markets, kept in a deterministic, ordered 20-entry shape (mirror `zillow_categories.py` / `rent_categories.py`).

```python
CATEGORIES = {
    "new-york-ny":      "https://hotpads.com/new-york-ny/apartments-for-rent",
    "los-angeles-ca":   "https://hotpads.com/los-angeles-ca/apartments-for-rent",
    "chicago-il":       "https://hotpads.com/chicago-il/apartments-for-rent",
    "houston-tx":       "https://hotpads.com/houston-tx/apartments-for-rent",
    "phoenix-az":       "https://hotpads.com/phoenix-az/apartments-for-rent",
    "philadelphia-pa":  "https://hotpads.com/philadelphia-pa/apartments-for-rent",
    "san-antonio-tx":   "https://hotpads.com/san-antonio-tx/apartments-for-rent",
    "san-diego-ca":     "https://hotpads.com/san-diego-ca/apartments-for-rent",
    "dallas-tx":        "https://hotpads.com/dallas-tx/apartments-for-rent",
    "san-jose-ca":      "https://hotpads.com/san-jose-ca/apartments-for-rent",
    "austin-tx":        "https://hotpads.com/austin-tx/apartments-for-rent",
    "jacksonville-fl":  "https://hotpads.com/jacksonville-fl/apartments-for-rent",
    "fort-worth-tx":    "https://hotpads.com/fort-worth-tx/apartments-for-rent",
    "columbus-oh":      "https://hotpads.com/columbus-oh/apartments-for-rent",
    "charlotte-nc":     "https://hotpads.com/charlotte-nc/apartments-for-rent",
    "indianapolis-in":  "https://hotpads.com/indianapolis-in/apartments-for-rent",
    "san-francisco-ca": "https://hotpads.com/san-francisco-ca/apartments-for-rent",
    "seattle-wa":       "https://hotpads.com/seattle-wa/apartments-for-rent",
    "denver-co":        "https://hotpads.com/denver-co/apartments-for-rent",
    "boston-ma":        "https://hotpads.com/boston-ma/apartments-for-rent",
}
```

Verified live on 2026-10-07 — **all 20 HTTP 200**, all server-rendered, **exactly 40** listings each:

| slug | bytes | cards / ItemList items | `X Rentals` total |
|---|---|---|---|
| new-york-ny | 1,082,415 | 40 / 40 | 17,672 |
| los-angeles-ca | 1,171,875 | 40 / 40 | 40,015 |
| chicago-il | 1,106,164 | 40 / 40 | 20,630 |
| houston-tx | 1,143,105 | 40 / 40 | 43,266 |
| phoenix-az | 1,148,201 | 40 / 40 | 18,492 |
| philadelphia-pa | 1,110,903 | 40 / 40 | 17,099 |
| san-antonio-tx | 1,102,295 | 40 / 40 | 22,029 |
| san-diego-ca | 1,188,754 | 40 / 40 | 14,605 |
| dallas-tx | 1,147,985 | 40 / 40 | 24,691 |
| san-jose-ca | 1,092,213 | 40 / 40 | 3,842 |
| austin-tx | 1,168,036 | 40 / 40 | 32,336 |
| jacksonville-fl | 1,118,532 | 40 / 40 | 11,669 |
| fort-worth-tx | 1,111,794 | 40 / 40 | 10,963 |
| columbus-oh | 1,079,129 | 40 / 40 | 12,777 |
| charlotte-nc | 1,172,740 | 40 / 40 | 24,338 |
| indianapolis-in | 1,062,454 | 40 / 40 | 9,964 |
| san-francisco-ca | 1,099,789 | 40 / 40 | 4,790 |
| seattle-wa | 1,159,777 | 40 / 40 | 19,399 |
| denver-co | 1,159,006 | 40 / 40 | 20,492 |
| boston-ma | 1,146,828 | 40 / 40 | 14,890 |

> Per-category machine-readable verification: `sample/hotpads-category-verification.json`. Taxonomy sources: `sample/hotpads-city-sitemap-index.xml` (index) and `sample/hotpads-city-sitemap-{ca,ny}.xml` (sample state sitemaps). The ordered dict is `sample/hotpads-top20-categories.json`.

## First-category investigation: New York, NY

```text
GET https://hotpads.com/new-york-ny/apartments-for-rent
HTTP 200, 1,082,415 bytes
<title>New York, NY Apartments for Rent - 17,672 Rentals | HotPads</title>
<link rel="canonical" href="https://hotpads.com/new-york-ny/apartments-for-rent">
<meta name="description" content="Search apartments for rent in New York, NY with the largest and most trusted rental site. ...">
```

### How the products load — server-rendered HTML + JSON-LD ItemList + Next.js App Router RSC hydration

Evidence gathered while drafting this ticket:

- `__NEXT_DATA__` occurrences: **0** and `window.__PRELOADED_STATE__`: **0** — it is the **Next.js App Router**, not Pages Router.
- The page **is** server-rendered, and carries the App Router streamed flight payload: **`self.__next_f.push` appears 71×** (`<script>self.__next_f.push([1,"..."])</script>`). Product data is present in the raw HTML — **no browser execution required**.
- Product data is available **three ways** in the raw HTML:
  1. **`<script type="application/ld+json">` → `@graph` → `SearchResultsPage` + `ItemList`**. Page 1 exposes `numberOfItems: 40` and exactly **40 `itemListElement`** entries, each `{ "@type": "ListItem", "position", "item": { "@type": "ApartmentComplex", "@id", "url", "name", "image", "address", "numberOfBedrooms", "offers": { "@type": "AggregateOffer", "lowPrice", "highPrice", "availability", "url" } } }`. This is the cleanest structured source. (A second ld+json block holds an FAQPage — ignore it.)
  2. **Server-rendered listing cards** in the DOM: `li[data-srp-listing-card="true"][data-marker-id]` → `a[data-testid="listing-card"][href="/<slug>/pad"]` → `article[data-c11n-component="PropertyCard.Root"]` with price (`$3,888+ /mo`), beds (`Studio - 3 beds`), `N units available`, `Apartment building`, badges (`New Today`) etc. Page 1 has **40** such `<li>` cards and **40** unique `/pad` links, matching the ItemList 1:1.
  3. **RSC flight payload** (`self.__next_f.push`) carries the search envelope: `"page":{"number":1,"limit":40}`, `"numUnits":17672`, `"numBuildingsAvailable":9879`, `"minPrice":1580`, `"totalPages":247`, `"searchSlug":"apartments-for-rent"`, `"area":{ resourceId/areaId/name/type/city/state }`, `"filters":{"boundingBox":{...},"areaId",...}`, and per-building objects with `title`, `tags` (`paidMultifamily`, `trusted`, ...), `unitCount`, `priceDropCount`, `contactPhone`.
- **No public listing XHR/GraphQL is required.** The only network endpoints referenced in the HTML are analytics/static (`api/static-map`, `datagrail` consent); there is no listing JSON API in the markup. `robots.txt` `Disallow`s `/api/`, `/node/api/v2/`, `/hotpads-api/`, `/ajax/`, `/mapdata/` — none of which are needed.

So the scraper needs **plain HTTP + an HTML/JSON parser only**; the ld+json `@graph` ItemList and (optionally) the RSC flight blob can be brace-extracted and `json.loads`-ed.

### JSON-LD sample (first `itemListElement`, from `sample/hotpads-itemlist.json`)

```json
{
  "@type": "ListItem",
  "position": 1,
  "item": {
    "@type": "ApartmentComplex",
    "@id": "https://hotpads.com/riverbank-new-york-ny-10036-skefej/pad#residence",
    "url": "https://hotpads.com/riverbank-new-york-ny-10036-skefej/pad",
    "name": "Riverbank",
    "image": "https://photos.zillowstatic.com/fp/927467905003e2527a1c738c39ab9845-rentals_medium_500_500.webp",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "560 W 43rd St",
      "addressLocality": "New York",
      "addressRegion": "NY",
      "postalCode": "10036",
      "addressCountry": "US"
    },
    "numberOfBedrooms": 0,
    "offers": {
      "@type": "AggregateOffer",
      "priceCurrency": "USD",
      "lowPrice": 3888,
      "highPrice": 11151,
      "availability": "https://schema.org/InStock",
      "url": "https://hotpads.com/riverbank-new-york-ny-10036-skefej/pad"
    }
  }
}
```

The `@id`/`url` shape `/…-<city>-<st>-<zip>-<markerId>/pad` is stable and unique per building; price lives in `offers.lowPrice`/`offers.highPrice` (no single "price" field — emit the range).

### Server-rendered card sample (from `sample/hotpads-card-sample.html`)

Card root: `li[data-srp-listing-card="true"]` → `article[data-c11n-component="PropertyCard.Root"]` (Zillow `c11n` design-system components).
Rendered text fields for card 1 (`data-marker-id="skefej"`):

```text
Riverbank, New York, NY 10036
$3,888+ /mo
Total price
Studio - 3 beds · 6 units available
Apartment building
Riverbank
New York, NY 10036
Listing options
New Today
Add to favorites
Share
```

```html
<li data-srp-listing-card="true" data-marker-id="skefej">
  <a data-testid="listing-card" href="/riverbank-new-york-ny-10036-skefej/pad">
    <span class="…" data-c11n-component="VisuallyHidden">Riverbank, New York, NY 10036</span>
  </a>
  <article data-c11n-component="PropertyCard.Root">
    <div data-c11n-component="PropertyCard.DataArea">
      <span>$3,888+ /mo</span>
      …
    </div>
  </article>
</li>
```

### RSC hydration sample (`sample/hotpads-rsc-state-sample.json`)

```json
{
  "page": { "number": 1, "limit": 40 },
  "search": { "numUnits": 17672, "numBuildingsAvailable": 9879, "minPrice": 1580, "totalPages": 247 },
  "initialParams": {
    "searchSlug": "apartments-for-rent",
    "area": { "resourceId": "new-york-ny", "areaId": "117776782", "name": "New York", "type": "city", "city": "New York", "state": "NY" },
    "filters": { "boundingBox": { "minLat": 40.4774, "maxLat": 40.91758, "minLon": -74.25909, "maxLon": -73.70027 }, "areaId": "117776782" },
    "page": { "number": 1, "limit": 40 }
  },
  "listing_sample": { "title": "Marquis West Side", "tags": ["active","paidMultifamily","trusted"], "unitCount": 1, "contactPhone": "1-516-689-9759" }
}
```

### Pagination — path-based, also server-rendered

HotPads exposes an explicit `<link rel="next">` and honours a `/page/N` path segment:

```text
<link rel="next" href="https://hotpads.com/new-york-ny/apartments-for-rent/page/2"/>
GET https://hotpads.com/new-york-ny/apartments-for-rent/page/2
HTTP 200, 1,035,237 bytes
```

Verified: page 2 returned **40** `li[data-srp-listing-card]` nodes, **40** `/pad` links and a JSON-LD ItemList with **40** `ListItem`s, **all distinct from page 1** (page 1 starts at `riverbank-…-skefej`, page 2 at `view-34-…-sj8403`). Page N is simply `"{base}/page/{N}"` (page 1 is the bare slug — do **not** append `/page/1`; append only for N ≥ 2). The RSC envelope reports `totalPages: 247` for `new-york-ny`. Stop when the ItemList/cards are empty, the `/pad` hrefs repeat, `numberOfItems`/`totalPages` is exhausted, an HTTP error occurs, or `max_pages` is hit.

### Field map

| field | source |
|---|---|
| `item_id` / `marker_id` | JSON-LD `item.@id` / card `data-marker-id` (stable `<city>-<st>-<zip>-<markerId>`) |
| `title` / `name` | JSON-LD `item.name` / card heading |
| `url` | JSON-LD `item.url` (absolute) |
| `address` | JSON-LD `item.address` ({streetAddress, addressLocality, addressRegion, postalCode}) |
| `beds` | JSON-LD `item.numberOfBedrooms` / card `Studio - 3 beds` |
| `baths` | card text (JSON-LD has none) |
| `price_low` / `price_high` | JSON-LD `item.offers.lowPrice` / `offers.highPrice` (AggregateOffer) |
| `price_currency` | JSON-LD `item.offers.priceCurrency` |
| `availability` | JSON-LD `item.offers.availability` |
| `photo` | JSON-LD `item.image` (`photos.zillowstatic.com`) |
| `units_available` | card `N units available` |
| `property_type` | card `Apartment building` / RSC `propertyType` |
| `badges` | card badges (`New Today`, `Total price`) |
| `phone` | RSC listing `contactPhone` |
| `tags` | RSC listing `tags` |
| `total_count` | RSC `search.numUnits` / page `X Rentals` title |
| `total_pages` | RSC `search.totalPages` |
| `area_id` / `city` / `state` | RSC `initialParams.area` |
| `category` (slug) | requested category |
| `page`, `position` | pager context / ItemList `position` |
| `source` | e.g. `"hotpads_jsonld_itemlist"` |
| `timestamp` | pipeline/constant |

### Taxonomy sources

- City taxonomy (authoritative): `https://hotpads.com/sitemap-city-index.xml` (from `robots.txt` sitemap list; **241** per-state sitemaps) → `https://hotpads.com/sitemap-city-apartments-for-rent-<ST>_0.xml.gz` (gzip works through the proxy) → city URLs of the form `https://hotpads.com/<city-slug>/apartments-for-rent`.
- Sibling taxonomies in the same index family: `sitemap-city-houses-for-rent-…`, `sitemap-hood-…` (neighborhoods), `sitemap-county-…`, `sitemap-zip-…`, `sitemap-region-…`, plus attribute variants (`-pet-friendly-`, `-luxury-`, `-under-1000-`, `-by-owner-`, ...).
- `robots.txt` lists the sitemaps; do not touch the `Disallow`ed `/api/`, `/node/api/v2/`, `/hotpads-api/`, `/ajax/`, `/mapdata/` paths.

## Implementation instructions

- Add `common/spiders/hotpads_categories.py` with the exact 20-entry `CATEGORIES` dict above (a `(slug -> url)` map, deterministic order).
- Add a `hotpads_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` plus `category_url`, and support running all categories, consistent with the other listing spiders.
- Request each city page through the configured ScrapeOps proxy (US). Parse **two sources and prefer JSON-LD**:
  1. Brace-extract and `json.loads` the ld+json block containing `@graph` → take the `ItemList.itemListElement` → emit one item per `ListItem.item` (`ApartmentComplex`).
  2. Optionally enrich from `li[data-srp-listing-card]` cards (baths, units available, badges, property type) and from the RSC flight payload (`totalPages`, `numUnits`, `area`).
- Paginate with `f"{base}/page/{n}"` for `n >= 2`, driven by the ItemList/card count and `totalPages`/`numberOfItems`, never a fixed page count. Deduplicate by `item_id` (marker id).
- Emit `item_id`, `marker_id`, `title`, absolute `url`, `address`, `beds`, `baths`, `price_low`, `price_high`, `price_currency`, `availability`, `photo`, `units_available`, `property_type`, `badges`, `phone`, `tags`, `total_count`, `total_pages`, `area_id`, `city`, `state`, `category` (slug), `page`, `position`, `source`, `timestamp`.
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Detect bot-wall / challenge / proxy-error payloads explicitly (empty body, tiny body `< 5 KB`, ScrapeOps `"Failed to get successful response"`, captcha/`Pardon the Interruption` stubs) and log a clear warning instead of silently emitting 0 items.

## Attached evidence (committed to this repo under `sample/`)

- `sample/hotpads-top20-categories.json` — the top-20 `{slug: url}` dict above.
- `sample/hotpads-city-sitemap-index.xml` — city sitemap index (241 per-state sitemaps).
- `sample/hotpads-city-sitemap-ca.xml` / `sample/hotpads-city-sitemap-ny.xml` — sample state city sitemaps.
- `sample/hotpads-category-verification.json` — per-category HTTP/bytes/items/total-rentals table.
- `sample/hotpads-new-york-ny.html` — full page-1 capture (1,082,415 bytes).
- `sample/hotpads-new-york-ny-p2.html` — full page-2 capture (`/page/2`, 1,035,237 bytes).
- `sample/hotpads-itemlist.json` — extracted JSON-LD `ItemList` (40 `ApartmentComplex` listings).
- `sample/hotpads-card-sample.html` — two full `li[data-srp-listing-card]` nodes.
- `sample/hotpads-rsc-state-sample.json` — trimmed Next.js App Router RSC flight excerpt (search envelope + one listing).
