## Goal

Add a `hostelworld_listing` spider for **Hostelworld** (hostelworld.com, the leading global hostel/backpacker accommodation marketplace). There is currently **no Hostelworld spider** under `common/spiders/` and **no open/closed Hostelworld issue** in this repository.

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, the destinations index, the sitemap index, and **20 city listing pages** all returned HTTP 200.

Hostelworld has **no retail "category" taxonomy**. Its catalogue is organised by **destination city pages** (`https://www.hostelworld.com/hostels/<continent>/<country>/<city>/`), each of which is a product listing ("products" = bookable hostels, i.e. properties). The site is a **Nuxt/Vue SSR** app and is **not** Next.js.

## Top 20 category URLs

City slugs come from the live sitemap index `https://www.hostelworld.com/sitemap-index.xml` → 32 gzipped `sitemap-N.xml.gz` files (≈**2,838 city category URLs**). The dict below is the top 20 global destinations, kept in a deterministic, ordered 20-entry shape.

```python
HOSTELWORLD_CATEGORIES = {
    "london": "https://www.hostelworld.com/hostels/europe/england/london/",
    "paris": "https://www.hostelworld.com/hostels/europe/france/paris/",
    "barcelona": "https://www.hostelworld.com/hostels/europe/spain/barcelona/",
    "rome": "https://www.hostelworld.com/hostels/europe/italy/rome/",
    "amsterdam": "https://www.hostelworld.com/hostels/europe/netherlands/amsterdam/",
    "berlin": "https://www.hostelworld.com/hostels/europe/germany/berlin/",
    "madrid": "https://www.hostelworld.com/hostels/europe/spain/madrid/",
    "prague": "https://www.hostelworld.com/hostels/europe/czech-republic/prague/",
    "lisbon": "https://www.hostelworld.com/hostels/europe/portugal/lisbon/",
    "dublin": "https://www.hostelworld.com/hostels/europe/ireland/dublin/",
    "vienna": "https://www.hostelworld.com/hostels/europe/austria/vienna/",
    "budapest": "https://www.hostelworld.com/hostels/europe/hungary/budapest/",
    "milan": "https://www.hostelworld.com/hostels/europe/italy/milan/",
    "venice": "https://www.hostelworld.com/hostels/europe/italy/venice/",
    "edinburgh": "https://www.hostelworld.com/hostels/europe/scotland/edinburgh/",
    "copenhagen": "https://www.hostelworld.com/hostels/europe/denmark/copenhagen/",
    "krakow": "https://www.hostelworld.com/hostels/europe/poland/krakow/",
    "athens": "https://www.hostelworld.com/hostels/europe/greece/athens/",
    "new-york": "https://www.hostelworld.com/hostels/north-america/usa/new-york/",
    "bangkok": "https://www.hostelworld.com/hostels/asia/thailand/bangkok/",
}
```

Verified live on 2026-10-07 (all HTTP 200). Each page renders **up to 30 hostels server-side**; the city's true total (`N Hostels in <City>`) is in the page headline. `city_id` is required for the paging API.

| slug | city_id | hostels total | SSR items | slug | city_id | hostels total | SSR items |
|---|---|---|---|---|---|---|---|
| london | 3 | 92 | 30 | budapest | 50 | 51 | 30 |
| paris | 14 | 102 | 30 | milan | 649 | 56 | 30 |
| barcelona | 83 | 113 | 30 | venice | 68 | 30 | 30 |
| rome | 36 | 112 | 30 | edinburgh | 22 | 27 | 27 |
| amsterdam | 15 | 80 | 30 | copenhagen | 48 | 17 | 17 |
| berlin | 26 | 54 | 30 | krakow | 285 | 47 | 30 |
| madrid | 117 | 89 | 30 | athens | 588 | 50 | 30 |
| prague | 19 | 61 | 30 | new-york | 13 | 29 | 29 |
| lisbon | 725 | 81 | 30 | bangkok | 149 | 320 | 30 |
| dublin | 5 | 18 | 18 | vienna | 38 | 25 | 25 |

## First-category investigation: New York, NY

```text
GET https://www.hostelworld.com/hostels/north-america/usa/new-york/
HTTP 200, 699,499 bytes
<title>Best Hostels in New York from US$29.75 | 2026</title>
<h1 ...>Hostels in New York</h1><span class="headline-sub-label">29 Hostels in New York, USA</span>
```

### How the products load — Nuxt SSR: `window.__NUXT__` state + JSON-LD `@graph` ItemList + server-rendered cards (page 1 needs no XHR)

- `__NEXT_DATA__` occurrences: **0** — it is **not** Next.js.
- It **is a Nuxt/Vue SSR app**: the document embeds a minified `window.__NUXT__=(function(...){...})(...)` state blob. The city/hostel cache lives under `__NUXT__.data["getCityProperties…"].data`.
- **Primary clean source (page 1):** a schema.org JSON-LD block
  `<script type="application/ld+json" data-nuxt-schema-org="true" data-hid="schema-org-graph">{"@context":...,"@graph":[…]}</script>` whose `@graph` contains an **`ItemList`** of **`LodgingBusiness`** nodes (`additionalType: "Hostel"`) — **29 entries** for New York, one per hostel, with `name`, `url`, `image[]`, `address`, `geo`, `aggregateRating{ratingValue,reviewCount,bestRating}`.
- **State fallback:** `__NUXT__.data["getCityPropertiesenhostel131030nullUSD"].data` = `{ totalPropertiesCount, numberOfPages, page, hasAvailability, properties:[…] }` with 30 rich property dicts (`id`, `name`, `urlFriendlyName`, `avgRating`, `numberReviews`, `sharedMinPrice{value,currency}`, `privateMinPrice`, `geoCoordinates`, `images[]`, `badges[]`, `averageRatings{…}`, `cityCenterDistance`, …).
- **HTML fallback:** the same hostels are **server-rendered** as `<a class="property-card-container …" href="…/hostels/p/<id>/<slug>/">` cards (property-name / rating score / review count / `From US$xx`).
- Paging, however, is **client-side**: see below. The spider therefore needs an HTML/JSON parser **and** a follow-up API call for pages ≥ 2.

Card data observed: `class="property-card-container compact horizontal featured-property-card"`, `data-v-*` scoped attrs, `href="https://www.hostelworld.com/hostels/p/<propertyId>/<slug>/"`.

### Pagination — apigee "staticpages" city-properties API (pages ≥ 2)

The listing page only ever SSRs the **first 30** hostels; the rest are fetched by the Vue app via a JSON API (no `?page=` or `/page/N/` HTML links exist — pagination is infinite-scroll/XHR). Endpoint (resolved from the runtime config + `D5nVHPVQ.js` store):

```text
GET https://prod.apigee.hostelworld.com/legacy-staticpages-service/city/hostel/{city_id}/properties/
    ?limit=30&page={n}&featured=0&origin=spapi&priorityPropertyType=hostel&currency=USD
Headers:
    api-key: <config.public.APIGEE_KEY>       # e.g. TKM51SUbyeCZl8soGScBLR9lYQdjCvTR8cIN4vfqpG6oExKT
    Accept: application/json
    Accept-Language: en                        # one of the allowed locales
```

> ⚠️ **Gotcha (verified live):** the ScrapeOps proxy rewrites/overrides the `Accept` and `Accept-Language` request headers, and the apigee gateway then answers `{"success":false,…"Unacceptable value set to the 'Accept' header…"}`. Fetch this API **directly** (it is not geo/anti-bot protected) or with a proxy that preserves headers. Example verified response below.

Verified paging for London (`city_id=3`, total 92, `numberOfPages=4`):

```text
page 1 → 30 items (ids 502, 88047, 14348, …)
page 2 → 30 items (ids 510, 55551, 93920, …)   0 overlap with page 1
page 3 → 30 items
page 4 →  2 items                              → stop
```

Response shape (`data`):

```json
{ "success": true, "data": {
  "id": 3, "name": "London", "urlFriendlyName": "london",
  "country": "England", "continent": "Europe",
  "totalPropertiesCount": 92, "numberOfPages": 4, "page": 2, "hasAvailability": true,
  "properties": [ {
      "id": 510, "name": "Generator London", "type": "HOSTEL",
      "urlFriendlyName": "generator-london",
      "address": "Compton Place", "city": "London", "country": "England", "continent": "Europe",
      "avgRating": 7, "numberReviews": 9468, "cityCenterDistance": 2.97, "hasAvailability": true,
      "image": {"small": "...", "medium": "...", "large": "..."},
      "sharedMinPrice": {"value": 23.2, "currency": "USD"},
      "privateMinPrice": { "value": 27.77, "currency": "USD" },
      "geoCoordinates": {"latitude": 51.5263103, "longitude": -0.1245209},
      "averageRatings": {"security": 7.86, "location": 8.5, "staff": 7.34, "atmosphere": 6.69, "cleanliness": 6, "valueForMoney": 6.6, "facilities": 5.96},
      "badges": [{"id":"90","badgeName":"Free WiFi","transCode":"FREEWIFI"}],
      "intro": "Generator London is a design hotel-hostel located in Russell Square …",
      "tracking": {"name":"Generator London","city":"London","country":"England","continent":"Europe"}
  } ] } }
```

### Field map (JSON-LD `LodgingBusiness` on page 1 / API `properties[]` on pages ≥ 2)

| field | page-1 (JSON-LD) | pages ≥ 2 (API) |
|---|---|---|
| `item_id` | propertyId parsed from `url` `/hostels/p/<id>/` | `properties[].id` |
| `url` | `item.url` | `https://www.hostelworld.com/hostels/p/{id}/{urlFriendlyName}/` |
| `name` | `item.name` | `properties[].name` |
| `address` | `item.address.streetAddress` | `properties[].address` |
| `city` / `country` / `continent` | `address.addressLocality`/`addressCountry`(/-) | `city` / `country` / `continent` (+ `urlFriendly*`) |
| `rating` / `reviews` | `aggregateRating.ratingValue` / `.reviewCount` | `avgRating` / `numberReviews` |
| `price_shared` / `min_price` | (not in JSON-LD; parse card `From US$…`) | `sharedMinPrice.value` (+ `.currency`) |
| `price_private` | — | `privateMinPrice.value` |
| `lat` / `lng` | `geo.latitude` / `geo.longitude` | `geoCoordinates.latitude` / `.longitude` |
| `photo` | `image[0]` | `image.medium` / `images[0].medium` (prefix `https://`) |
| `distance_km` | — | `cityCenterDistance` |
| `badges` / `facilities` | — | `badges[].badgeName` |
| `property_type` | `additionalType` ("Hostel") | `type` |
| `category` | city slug (keep on every item) | city slug |
| `page` | 1 | `{n}` |
| `source` | `"hostelworld_itemlist_jsonld"` | `"hostelworld_city_properties_api"` |

### Taxonomy sources

- `https://www.hostelworld.com/sitemap-index.xml` → `sitemap-1.xml.gz` … `sitemap-32.xml.gz` (gzipped; ScrapeOps passes `.gz` through fine and `gunzip` works) — **2,838** `/hostels/<continent>/<country>/<city>/` URLs.
- Human-facing index `https://www.hostelworld.com/hostels/` (continents/countries + 8 popular cities) and the homepage (7 popular cities).
- Country pages (e.g. `/hostels/europe/italy/`, 103 cities) list cities but are **not** product listings — only city pages carry a hostel `ItemList`.

### Sample HTML / JSON

- Full New York page: `sample/hostelworld-new-york-ny.html`
- Full London page (pagination example): `sample/hostelworld-london-england.html`
- Card HTML (trimmed): `sample/hostelworld-card-sample.html`
- JSON-LD `ItemList` (29 hostels): `sample/hostelworld-itemlist-sample.json`
- Trimmed `window.__NUXT__` state: `sample/hostelworld-nuxt-state-sample.json`
- Paging API response (London page 2, trimmed to 2 items): `sample/hostelworld-api-response-sample.json`

```html
<a rel="noopener" class="property-card-container compact horizontal featured-property-card"
   href="https://www.hostelworld.com/hostels/p/1850/hi-new-york-city-hostel/" data-v-29424246>
  <div class="property-photos"><div class="carousel ..." title="HI New York City Hostel">…</div></div>
  <div class="property-info-container">
    <div class="property-name"><span>HI New York City Hostel</span></div>
    <div class="property-rating"><div class="rating ..."><span class="score">9.2</span>
        <span class="keyword" title="Superb">Superb</span><span class="num-reviews">(11433)</span></div></div>
    <div class="property-accommodations"><div class="property-accommodation-from-price">
        <span class="from-price-label">From</span><strong class="current notranslate">US$53.10</strong></div></div>
  </div>
</a>
```

```json
{ "@type": "ListItem", "position": 1, "item": {
  "@type": "LodgingBusiness", "additionalType": "Hostel",
  "name": "HI New York City Hostel",
  "url": "https://www.hostelworld.com/hostels/p/1850/hi-new-york-city-hostel/",
  "address": {"@type":"PostalAddress","streetAddress":"891 Amsterdam Avenue","addressLocality":"New York","addressCountry":"USA","addressRegion":"USA","postalCode":"N/A"},
  "geo": {"@type":"GeoCoordinates","latitude":40.798684,"longitude":-73.966653},
  "aggregateRating": {"@type":"AggregateRating","ratingValue":9.2,"reviewCount":11434,"bestRating":10} } }
```

## Implementation instructions

- Add `common/spiders/hostelworld_categories.py` with the exact 20-entry `HOSTELWORLD_CATEGORIES` dict above (slug → city URL), plus a `HostelworldCategory` note that each city also has a numeric `city_id` (see verification JSON) needed for paging.
- Add a `hostelworld_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` and support `category_url` / running all categories, consistent with the other listing spiders.
- **Page 1:** request the city URL through the configured ScrapeOps proxy (US) and parse the **JSON-LD `@graph` `ItemList`** first:
  `json.loads(response.css('script[type="application/ld+json"]::text').get())` → pick the node with `@type == "ItemList"` → `itemListElement[].item`.
  Fall back to `__NUXT__.data["getCityProperties…"].data.properties`, then to server-rendered `a.property-card-container` cards.
- **Pages ≥ 2:** read `totalPropertiesCount`/`numberOfPages` (from the state, or parse the headline `N Hostels in <City>`), then loop
  `https://prod.apigee.hostelworld.com/legacy-staticpages-service/city/hostel/{city_id}/properties/?limit=30&page={n}&featured=0&origin=spapi&priorityPropertyType=hostel&currency=USD`
  with headers `api-key: <APIGEE_KEY>, Accept: application/json, Accept-Language: en`. Fetch this endpoint **directly** (do not route it through a header-rewriting proxy — the gateway rejects the rewritten `Accept` header).
- Parse the JSON-LD block with `data-hid="schema-org-graph"` (the graph holds WebSite/WebPage/BreadcrumbList/ItemList/FAQ pages).
- Emit `item_id` (stable property id), `url`, `name`, `address`, `city`/`country`/`continent`, `rating`, `reviews`, `price_shared`/`price_private` (`min_price` from shared), `lat`/`lng`, `photo`, `distance_km`, `badges`, `property_type`, `category` (city slug), `page`, `source`.
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Deduplicate by property id; stop on an empty page, a short page (< 30), a repeated page (same first id as previous), `page > numberOfPages`, a nonzero error, or `max_pages`.
- Detect bot-wall / proxy-error payloads explicitly (`{"success":false,…}`, apigee "Unacceptable value set to the 'Accept' header", PerimeterX/captcha bodies) and log a clear warning instead of silently emitting 0 items.
- Do **not** use Playwright — plain HTTP HTML/JSON parsing plus the JSON API is sufficient.

## Acceptance criteria

- Unit fixtures/tests cover: JSON-LD `ItemList` extraction, `__NUXT__` state + card fallback parsing, field mapping, property-id dedup, the apigee paging call (`page=2` distinct from page 1, 0 overlap), `numberOfPages`-derived stop, and challenge/error detection.
- A live one-page New York run through ScrapeOps returns 29 items with unique `item_id` values.
- A live London run proves page 2 (`page=2` of the apigee API) is distinct (ids differ, 0 overlap) and respects `numberOfPages`/`max_pages`.
- Document the spider, the 20-city taxonomy, the loading mechanism (Nuxt `__INITIAL_STATE__`/`__NUXT__` + JSON-LD `ItemList` + server-rendered cards + apigee `city/hostel/{id}/properties` paging), the proxy/header gotcha, and the sitemap source in the README.

## Attached evidence

- Category dict (top 20) + taxonomy sources: above; also `sample/hostelworld-top20-categories.py` / `.json`.
- Live verification of all 20 categories: `sample/hostelworld-category-verification.json` (city_id, total, SSR items, HTTP status).
- Sample card HTML, JSON-LD `ItemList`, trimmed `__NUXT__` state and apigee API response: inline above and under `sample/` (see list).
- Local capture artifacts used while drafting this ticket:
  - `sample/hostelworld-new-york-ny.html` — New York listing page 1 (699,499 bytes, `29 Hostels`, 29 `ItemList` entries)
  - `sample/hostelworld-london-england.html` — London listing page 1 (764,755 bytes, `92 Hostels`, 30 SSR items → pagination)
  - `sample/hostelworld-card-sample.html`, `sample/hostelworld-itemlist-sample.json`
  - `sample/hostelworld-nuxt-state-sample.json` — city + `getCityProperties` cache
  - `sample/hostelworld-api-response-sample.json` — apigee `city/hostel/3/properties/?page=2`
  - `sample/hostelworld-top20-categories.py`, `sample/hostelworld-top20-categories.json`

## Environment

- Branch/commit: `cron-ticket-hostelworld`
- Capture date: 2026-10-07 (Asia/Bangkok)
- Proxy: repository `SCRAPEOPS_PROXY` (`country=us`) for HTML pages; the apigee JSON API was fetched directly (proxy rewrites `Accept`/`Accept-Language`).
- Runtime notes: Hostelworld is a **Nuxt/Vue SSR** app. Page 1 = JSON-LD `@graph` `ItemList` (`LodgingBusiness`) + `window.__NUXT__` state + server-rendered `property-card` HTML. Pages ≥ 2 = apigee `legacy-staticpages-service/city/hostel/{city_id}/properties` (`api-key`, `page`, `limit=30`), direct. City taxonomy = `/hostels/<continent>/<country>/<city>/` (2,838 cities from the sitemap index). 30 hostels per page.
