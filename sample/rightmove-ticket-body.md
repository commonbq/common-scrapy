## Goal

Add a `rightmove_listing` spider for **Rightmove** (`rightmove.co.uk`), the UK's largest property portal (real estate). There is currently **no Rightmove spider** under `common/spiders/` and **no open/closed Rightmove issue** in this repository (checked with `gh issue list --state all --search "rightmove in:title"` → empty, and `ls common/spiders/ | grep -i rightmove` → empty).

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, `robots.txt`, the sitemap index, the England/London region sitemaps and **twenty-nine city listing pages** all returned HTTP 200.

Rightmove's catalogue is organised as **location "categories"**: each category is a property-for-sale search page of the form `https://www.rightmove.co.uk/property-for-sale/<Location>.html`. Each such page is a product listing ("products" = individual property adverts). Filter variants exist as sub-paths (`/houses.html`, `/flats.html`, `/2-bed-flats.html`, ...) and as query params (`?index=`, `?radius=`, `?maxPrice=`, `?sortType=`, ...); the canonical form carries the internal location id (`London-87490.html`).

## Top 20 category URLs

The dict below is the **top 20 UK locations by live `resultCount`** on the "for sale" channel, kept in a deterministic `(slug -> url)` shape (mirror `zillow_categories.py` / `rent_categories.py` / `hotpads_categories.py`).

```python
CATEGORIES = {
    "london":         "https://www.rightmove.co.uk/property-for-sale/London.html",
    "manchester":     "https://www.rightmove.co.uk/property-for-sale/Manchester.html",
    "birmingham":     "https://www.rightmove.co.uk/property-for-sale/Birmingham.html",
    "leeds":          "https://www.rightmove.co.uk/property-for-sale/Leeds.html",
    "liverpool":      "https://www.rightmove.co.uk/property-for-sale/Liverpool.html",
    "bristol":        "https://www.rightmove.co.uk/property-for-sale/Bristol.html",
    "leicester":      "https://www.rightmove.co.uk/property-for-sale/Leicester.html",
    "sheffield":      "https://www.rightmove.co.uk/property-for-sale/Sheffield.html",
    "cardiff":        "https://www.rightmove.co.uk/property-for-sale/Cardiff.html",
    "coventry":       "https://www.rightmove.co.uk/property-for-sale/Coventry.html",
    "milton-keynes":  "https://www.rightmove.co.uk/property-for-sale/Milton-Keynes.html",
    "southampton":    "https://www.rightmove.co.uk/property-for-sale/Southampton.html",
    "nottingham":     "https://www.rightmove.co.uk/property-for-sale/Nottingham.html",
    "brighton":       "https://www.rightmove.co.uk/property-for-sale/Brighton.html",
    "glasgow":        "https://www.rightmove.co.uk/property-for-sale/Glasgow.html",
    "norwich":        "https://www.rightmove.co.uk/property-for-sale/Norwich.html",
    "edinburgh":      "https://www.rightmove.co.uk/property-for-sale/Edinburgh.html",
    "portsmouth":     "https://www.rightmove.co.uk/property-for-sale/Portsmouth.html",
    "derby":          "https://www.rightmove.co.uk/property-for-sale/Derby.html",
    "plymouth":       "https://www.rightmove.co.uk/property-for-sale/Plymouth.html",
}
```

Verified live on 2026-10-07 — **all 20 HTTP 200**, all server-rendered, **exactly 25** listings on page 1 each:

| # | slug | bytes | props (p1) | total pages | `resultCount` | location display name |
|---|------|-------|-----------|-------------|---------------|-----------------------|
| 1 | london | 1,248,568 | 25 | 42 | 60,714 | London |
| 2 | manchester | 1,417,916 | 25 | 42 | 6,839 | Manchester, Greater Manchester |
| 3 | birmingham | 1,385,300 | 25 | 42 | 6,346 | Birmingham |
| 4 | leeds | 1,375,246 | 25 | 42 | 4,887 | Leeds, West Yorkshire |
| 5 | liverpool | 1,450,323 | 25 | 42 | 4,874 | Liverpool, Merseyside |
| 6 | bristol | 1,250,748 | 25 | 42 | 3,822 | Bristol |
| 7 | leicester | 1,375,329 | 25 | 42 | 3,725 | Leicester, Leicestershire |
| 8 | sheffield | 1,514,967 | 25 | 42 | 2,782 | Sheffield |
| 9 | cardiff | 1,405,976 | 25 | 42 | 2,445 | Cardiff(City) |
| 10 | coventry | 1,490,398 | 25 | 42 | 2,312 | Coventry, West Midlands |
| 11 | milton-keynes | 1,481,086 | 25 | 42 | 2,271 | Milton Keynes, Buckinghamshire |
| 12 | southampton | 1,349,217 | 25 | 42 | 2,189 | Southampton, Hampshire |
| 13 | nottingham | 1,283,748 | 25 | 42 | 2,110 | Nottingham, Nottinghamshire |
| 14 | brighton | 1,448,436 | 25 | 42 | 2,106 | Brighton, East Sussex |
| 15 | glasgow | 1,454,347 | 25 | 42 | 2,062 | Glasgow |
| 16 | norwich | 1,379,728 | 25 | 42 | 1,972 | Norwich, Norfolk |
| 17 | edinburgh | 1,350,115 | 25 | 42 | 1,944 | Edinburgh |
| 18 | portsmouth | 1,335,192 | 25 | 42 | 1,857 | Portsmouth, Hampshire |
| 19 | derby | 1,485,899 | 25 | 42 | 1,836 | Derby, Derbyshire |
| 20 | plymouth | 1,440,890 | 25 | 42 | 1,704 | Plymouth, Devon |

> `resultCount` is a **comma-formatted string** in the payload (e.g. `"60,714"`); strip commas before `int()`. Rightmove caps pagination at **42 pages / ~1,000 results** per search (`pagination.total = 42`, `pagination.last = "984"`), so stop at `min(42, ceil(resultCount/24))`.

> Per-category machine-readable verification: `sample/rightmove-category-verification.json`. Taxonomy sources: `sample/rightmove-sitemap-index.xml`, `sample/rightmove-region-sitemap-england.xml`, `sample/rightmove-region-sitemap-london.xml`. The ordered dict is `sample/rightmove-top20-categories.json`.

## First-category investigation: London

```text
GET https://www.rightmove.co.uk/property-for-sale/London.html
HTTP 200, 1,248,568 bytes
<canvas 19,672 value> resultCount = "60,714"
<meta name="description" content="Flats &amp; Houses For Sale in London - Find properties with Rightmove - the UK's largest selection of properties.">
<link rel="canonical" href="https://www.rightmove.co.uk/property-for-sale/London-87490.html">
__NEXT_DATA__.props.pageProps.searchResults.pageTitle = "Properties For Sale in London | Rightmove"
```

### How the products load — Next.js **Pages Router** hydration (`__NEXT_DATA__`) + server-rendered DOM cards

Evidence gathered while drafting this ticket:

- **`__NEXT_DATA__` count = 1**, **`self.__next_f.push` count = 0** → this is the Next.js **Pages Router** (the server-rendered flight payload of the App Router is absent). `JSON.parse` the single `<script id="__NEXT_DATA__">` block and read `props.pageProps.searchResults`.
- The page is fully **server-rendered**; all 25 products are present in the raw HTML — **no browser execution / JS challenge required**. `robots.txt` `Disallow`s `/api/*`, but no listing API is needed (and none is referenced: `fetch(` count = 0, `graphql` count = 0, only 1 stray `XMLHttpRequest` polyfill reference and 5 `typeAhead` autocomplete refs).
- **No JSON-LD** (`application/ld+json` count = 0) — unlike the US portals, Rightmove does **not** expose schema.org `ItemList`; the `__NEXT_DATA__` blob is the canonical structured source.
- Product data is available **two ways** in the raw HTML:
  1. **`props.pageProps.searchResults.properties[]`** — array of **25** property objects, each with `id`, `bedrooms`, `bathrooms`, `price {amount, currencyCode, displayPrices[]}`, `propertyUrl`, `propertySubType`, `propertyTypeFullDescription`, `displayAddress`, `summary`, `location {latitude, longitude}`, `images[]`, `propertyImages[]`, `customer {branchId, contactTelephone, branchDisplayName, brandTradingName, ...}`, `firstVisibleDate`, `addedOrReduced`, `tenure {tenureType}`, `tags[]`, `keyFeatures[]`, `displaySize`, `numberOfImages`, `numberOfFloorplans`, `numberOfVirtualTours`, `productLabel`, `heading`, etc. This is the cleanest structured source.
  2. **Server-rendered listing cards** in the DOM: `div[data-testid="propertyCard-vrt-N"]` → `a.PropertyCard_propertyCardAnchor__s2ZaP` (`<a id="prop<ID>">`) → `/properties/<ID>#/?channel=RES_BUY` → price/address/summary child nodes. Page 1 has **25** `propertyCard-vrt-*` roots matching the JSON `properties` 1:1.
- `searchResults.searchParameters` exposes the resolved query: `{"locationIdentifier":"REGION^87490","numberOfPropertiesPerPage":"24","radius":"0.0","sortType":"2","index":"0","channel":"BUY","currencyCode":"GBP", ...}` — page 1 carries index `"0"`.

So the scraper needs **plain HTTP + HTML/JSON parsing only**; brace-extract the `__NEXT_DATA__` script, `json.loads` it, and walk `props.pageProps.searchResults.properties`.

### Product sample (first `properties[]` entry, from `sample/rightmove-nextdata-sample.json`)

```json
{
  "id": 89825950,
  "bedrooms": 1,
  "bathrooms": 1,
  "numberOfImages": 12,
  "numberOfFloorplans": 1,
  "numberOfVirtualTours": 1,
  "summary": "This is a first floor one bedroom flat at Maxclif House set above popular local cafes in Tottenham Street, Fitzrovia. Reception room, separate fitted kitchen and family bathroom. Moments from Charlotte Street, Goodge Street and transport links. Walking distance to Oxford Street, Covent Garden, Soho.",
  "displayAddress": "Tottenham Street, Fitzrovia, W1",
  "countryCode": "GB",
  "location": { "latitude": 51.52055, "longitude": -0.13503 },
  "price": {
    "amount": 680000,
    "frequency": "not specified",
    "currencyCode": "GBP",
    "displayPrices": [{ "displayPrice": "£680,000", "displayPriceQualifier": "" }]
  },
  "propertyUrl": "/properties/89825950#/?channel=RES_BUY",
  "propertySubType": "Flat",
  "propertyTypeFullDescription": "1 bedroom flat for sale",
  "tenure": { "tenureType": "LEASEHOLD" },
  "displaySize": "526 sq. ft.",
  "firstVisibleDate": "2021-03-15T13:00:06Z",
  "addedOrReduced": "Added on 15/03/2021",
  "customer": {
    "branchId": 129667,
    "branchDisplayName": "Leo Newman, London Sales",
    "brandTradingName": "Leo Newman",
    "contactTelephone": "020 3910 0880"
  },
  "keyFeatures": [
    { "order": 1, "description": "1st Floor 1 Bedroom Flat" },
    { "order": 2, "description": "Central Fitzrovia Location" }
  ],
  "images": [{ "srcUrl": "https://media.rightmove.co.uk:443/dir/crop/10:9-16:9/property-photo/.../89825950/....jpeg", "url": "property-photo/.../....jpeg", "caption": null }]
}
```

`id` is stable and unique; the advert URL is `https://www.rightmove.co.uk` + `propertyUrl`. Price lives in `price.amount` (+ `price.displayPrices[0].displayPrice` for the display string).

### Server-rendered card sample (from `sample/rightmove-card-sample.html`)

```html
<div class="PropertyCard_propertyCardContainerWrapper__mcK1Z propertyCard-details" data-testid="propertyCard-vrt-0">
  <a id="prop89825950" class="PropertyCard_propertyCardAnchor__s2ZaP"></a>
  <div class="PropertyCard_featuredBannerTopOfCard__cYuPM">
    <a data-testid="property-details-lozenge" href="/properties/89825950#/?channel=RES_BUY">…1/12…</a>
  </div>
  <div class="PropertyCard_propertyCardContainer__VSRSA PropertyCard_feature…">
    … "£680,000" … "Tottenham Street, Fitzrovia, W1" …
  </div>
</div>
```

### Pagination — query-param based, also server-rendered

Rightmove exposes an explicit pager and honours an `index` query param in steps of 24:

```text
searchResults.pagination = { "total": 42, "first": "0", "last": "984", "next": "24", "page": "1" }
GET https://www.rightmove.co.uk/property-for-sale/London.html?index=24
HTTP 200, 1,142,201 bytes
```

Verified: page 2 returned **25** `properties` with `searchParameters.index="24"`, `pagination.page="2"`, and **all ids distinct from page 1** (p1 first ids `[89825950, 760770556763601, 155320229]`, p2 first ids `[174450575, 90070020, 92974734]`, overlap = ∅). Page N is `"<base>?index={24*(N-1)}"` (page 1 is the bare slug — do **not** append `?index=0`). Iterate until `properties` is empty, ids repeat, `index > pagination.last`, or the 42-page cap is hit.

### Field map

| field | source |
|---|---|
| `item_id` | `property.id` (stable, unique) |
| `title` | `property.displayAddress` / card heading |
| `url` | `https://www.rightmove.co.uk` + `property.propertyUrl` |
| `address` | `property.displayAddress` |
| `price` / `price_display` | `property.price.amount` / `property.price.displayPrices[0].displayPrice` |
| `price_currency` | `property.price.currencyCode` |
| `bedrooms` / `bathrooms` | `property.bedrooms` / `property.bathrooms` |
| `property_type` | `property.propertySubType` / `property.propertyTypeFullDescription` |
| `tenure` | `property.tenure.tenureType` |
| `size` | `property.displaySize` |
| `latitude` / `longitude` | `property.location.latitude` / `property.location.longitude` |
| `summary` | `property.summary` |
| `key_features` | `property.keyFeatures[].description` |
| `photo` / `photos` | `property.images[].srcUrl` (json) / card `<img src>` |
| `image_count` / `floorplan_count` / `virtual_tour_count` | `property.numberOfImages` / `numberOfFloorplans` / `numberOfVirtualTours` |
| `agent` / `agent_phone` / `branch_id` | `property.customer.branchDisplayName` / `contactTelephone` / `branchId` |
| `first_visible_date` / `added_or_reduced` | `property.firstVisibleDate` / `addedOrReduced` |
| `transaction_type` | `property.transactionType` (`buy`) |
| `tags` / `product_label` | `property.tags[]` / `property.productLabel.productLabelText` |
| `result_count` | `searchResults.resultCount` (comma-stripped) |
| `total_pages` | `searchResults.pagination.total` |
| `location_id` | `searchResults.location.id` / `searchParameters.locationIdentifier` (`REGION^87490`) |
| `category` (slug) | requested category |
| `page`, `position` | pager context / array index |
| `source` | e.g. `"rightmove_next_data"` |
| `timestamp` | pipeline/constant |

### Taxonomy sources

- City taxonomy (authoritative): `https://www.rightmove.co.uk/sitemap.xml` (from `robots.txt`; **188** `sitemap-outcodes-*.xml`, **187** `sitemap-properties-*.xml`, ~300 `sitemap-regions-*.xml`) → `https://www.rightmove.co.uk/sitemap-regions-England.xml` (sub-regions like `East-Midlands`, `North-West`, …) and `…/sitemap-regions-London.xml` (`South-London`, `Central-London`, …). Region entries are of the form `https://www.rightmove.co.uk/property-for-sale/<Location>.html` plus sub-path filter variants (`/houses.html`, `/2-bed-flats.html`, `/flats.html`, …).
- The human-readable slug URLs (`/property-for-sale/Birmingham.html`) resolve directly; the canonical form appends the internal id (`Birmingham-<id>.html`). Both work; use the slug form in the dict.
- `robots.txt` lists the sitemaps; it `Disallow`s `/api/*`, `/draw-a-search.html?*`, map-view/fullscreen/photo paths — none of which are needed for the listing scrape.

## Implementation instructions

- Add `common/spiders/rightmove_categories.py` with the exact 20-entry `CATEGORIES` dict above (a `(slug -> url)` map, deterministic order).
- Add a `rightmove_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` plus `category_url`, and support running all categories, consistent with the other listing spiders.
- Request each city page through the configured ScrapeOps proxy (US). Brace-extract the single `<script id="__NEXT_DATA__">` block, `json.loads` it, and read `props.pageProps.searchResults`:
  1. Emit one item per `searchResults.properties[]` entry (primary source).
  2. Optionally enrich from `div[data-testid^="propertyCard-vrt-"]` DOM cards (rendered `£` price string, address, summary) — the JSON is a superset, so the DOM is a fallback/verification source.
- Paginate with `?index={24*(n-1)}` for `n >= 2`, driven by `pagination.total` / `pagination.last` / present property count, never a fixed page count. Deduplicate by `item_id`. Respect the 42-page cap.
- Emit `item_id`, `title`, absolute `url`, `address`, `price`, `price_display`, `price_currency`, `bedrooms`, `bathrooms`, `property_type`, `tenure`, `size`, `latitude`, `longitude`, `summary`, `key_features`, `photo`, `photos`, `image_count`, `floorplan_count`, `virtual_tour_count`, `agent`, `agent_phone`, `branch_id`, `first_visible_date`, `added_or_reduced`, `transaction_type`, `tags`, `product_label`, `result_count`, `total_pages`, `location_id`, `category` (slug), `page`, `position`, `source`, `timestamp`.
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Note `resultCount` and `pagination.*` values are **strings** (some comma-formatted) — normalise before arithmetic.
- Detect bot-wall / challenge / proxy-error payloads explicitly (empty body, tiny body `< 5 KB`, ScrapeOps `"Failed to get successful response"`, captcha/`Pardon the Interruption` stubs) and log a clear warning instead of silently emitting 0 items.

## Attached evidence (committed to this repo under `sample/`)

- `sample/rightmove-top20-categories.json` — the top-20 `{slug: url}` dict above.
- `sample/rightmove-top20-categories.py` — same dict as a ready-to-paste `CATEGORIES` literal.
- `sample/rightmove-category-verification.json` — per-category HTTP/bytes/props/pages/resultCount table.
- `sample/rightmove-london.html` — full page-1 capture (1,248,568 bytes).
- `sample/rightmove-london-p2.html` — full page-2 capture (`?index=24`, 1,142,201 bytes).
- `sample/rightmove-nextdata-sample.json` — trimmed `__NEXT_DATA__.props.pageProps.searchResults` (envelope + 2 full properties).
- `sample/rightmove-properties-page1.json` — the complete 25-property `properties` array from page 1.
- `sample/rightmove-card-sample.html` — one full server-rendered `propertyCard-vrt-0` DOM node.
- `sample/rightmove-sitemap-index.xml` / `sample/rightmove-region-sitemap-england.xml` / `sample/rightmove-region-sitemap-london.xml` — taxonomy sources.
- `sample/rightmove-robots.txt` — crawl policy (sitemaps + disallows).
