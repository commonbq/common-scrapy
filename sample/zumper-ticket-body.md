## Goal

Add a `zumper_listing` spider for **Zumper** (`zumper.com`), a leading US rental marketplace. There is currently **no Zumper spider** under `common/spiders/` and **no open/closed Zumper issue** in this repository (checked the full issue list via `gh issue list --state all --search "Zumper in:title"`).

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, the sitemap index, the `AFR-cities` city sitemap and **six city listing pages** all returned HTTP 200.

Zumper has **no classic retail "category" taxonomy**. Its catalogue is organised by **city/market search pages** (`https://www.zumper.com/apartments-for-rent/<city-slug>`), each of which is a product listing ("products" = rental properties / apartment buildings). Saved-search variants exist as query params (`?bedrooms=1`, `?max_price=2000`, `?pets=1`, `?furnished=true`, ...).

## Top 20 category URLs

City slugs come from the live city sitemap `https://www.zumper.com/sitemaps/AFR-cities.xml.gz` (**10,684 city URLs** parsed at capture time). The dict below is the top 20 US rental markets, kept in a deterministic, ordered 20-entry shape (mirror `zillow_categories.py` / `apartments_categories.py`).

```python
CATEGORIES = {
    "new-york-ny":      "https://www.zumper.com/apartments-for-rent/new-york-ny",
    "los-angeles-ca":   "https://www.zumper.com/apartments-for-rent/los-angeles-ca",
    "san-francisco-ca": "https://www.zumper.com/apartments-for-rent/san-francisco-ca",
    "chicago-il":       "https://www.zumper.com/apartments-for-rent/chicago-il",
    "boston-ma":        "https://www.zumper.com/apartments-for-rent/boston-ma",
    "seattle-wa":       "https://www.zumper.com/apartments-for-rent/seattle-wa",
    "washington-dc":    "https://www.zumper.com/apartments-for-rent/washington-dc",
    "miami-fl":         "https://www.zumper.com/apartments-for-rent/miami-fl",
    "atlanta-ga":       "https://www.zumper.com/apartments-for-rent/atlanta-ga",
    "philadelphia-pa":  "https://www.zumper.com/apartments-for-rent/philadelphia-pa",
    "houston-tx":       "https://www.zumper.com/apartments-for-rent/houston-tx",
    "dallas-tx":        "https://www.zumper.com/apartments-for-rent/dallas-tx",
    "austin-tx":        "https://www.zumper.com/apartments-for-rent/austin-tx",
    "denver-co":        "https://www.zumper.com/apartments-for-rent/denver-co",
    "phoenix-az":       "https://www.zumper.com/apartments-for-rent/phoenix-az",
    "san-diego-ca":     "https://www.zumper.com/apartments-for-rent/san-diego-ca",
    "portland-or":      "https://www.zumper.com/apartments-for-rent/portland-or",
    "minneapolis-mn":   "https://www.zumper.com/apartments-for-rent/minneapolis-mn",
    "las-vegas-nv":     "https://www.zumper.com/apartments-for-rent/las-vegas-nv",
    "nashville-tn":     "https://www.zumper.com/apartments-for-rent/nashville-tn",
}
```

Verified live on 2026-10-07 (all HTTP 200, all server-rendered):

| slug | bytes | `listing-card` nodes | JSON-LD ItemList `numberOfItems` | market title |
|---|---|---|---|---|
| new-york-ny | 932,902 | 23 | 9,108 | Apartments for Rent in NYC |
| los-angeles-ca | 970,056 | 22 | 6,719 | Los Angeles, CA |
| chicago-il | 895,921 | 23 | 8,555 | Chicago, IL |
| san-francisco-ca | 874,019 | 25 | 650 | San Francisco, CA |
| miami-fl | 824,797 | 24 | 6,128 | Miami, FL |
| austin-tx | 887,609 | 21 | 3,396 | Austin, TX |
| new-york-ny page 2 | 896,985 | 25 | — | NYC - Page 2 |

> Note: distinct metadata for the *sitemap* taxonomy is at `sample/zumper-categories-all.json` (all 10,684 slugs) and `sample/zumper-top20-categories.json` (this dict).

## First-category investigation: New York, NY

```text
GET https://www.zumper.com/apartments-for-rent/new-york-ny
HTTP 200, 932,902 bytes
<title>Apartments for Rent in NYC - 10,770 Rentals Updated Daily | Zumper</title>
<link rel="canonical" href="https://www.zumper.com/apartments-for-rent/new-york-ny">
```

### How the products load — server-rendered HTML + JSON-LD + `__PRELOADED_STATE__` hydration

Evidence gathered while drafting this ticket:

- `__NEXT_DATA__` occurrences: **0** — it is **not** Next.js.
- The page **is** server-rendered with React "Chakra UI" markup. There is a large hydration blob: `window.__PRELOADED_STATE__ = { ... }` (a JSON object, plus `__PRELOADED_STATE__ = "{}"` placeholder for streamed chunks).
- Product data is available **three ways** in the raw HTML (no browser execution required):
  1. **`<script type="application/ld+json">` → `SearchResultsPage` → `mainEntity` (`@type: ItemList`)**. Page 1 exposes `numberOfItems` (total market count) and exactly **25** `itemListElement` entries, each `{ "@type": "RealEstateListing", "@id", "url", "name", "datePosted", "about": { ApartmentComplex ... } }`. This is the cleanest structured source.
  2. **Server-rendered listing cards** in the DOM (`23` `data-testid="listing-card"` nodes on page 1 — a couple of the ItemList rows are building-level cards rendered by a sibling component).
  3. **`window.__PRELOADED_STATE__`** hydration (`currentSearch.firstPageCount = 25`, `currentSearch.hasMoreListables = true`, `searchUI.limit/offset`, `geo.cities[...]` with `city_id`, `listing_count`, bounds, bedroom counts).
- **No public listing XHR/GraphQL is required.** The only network endpoints referenced in the HTML are analytics (`api.getblueshift.com`, `prod-main-datapipeline.zumper.com/events`). The `/api`, `/json`, `/listing-feed`, `/partials` paths are `Disallow`ed in `robots.txt` and are not needed.

So the scraper needs **plain HTTP + an HTML/JSON parser only**; the `__PRELOADED_STATE__` blob can be brace-extracted and parsed with `json.loads`.

### JSON-LD sample (first `itemListElement`, from `sample/zumper-itemlist.json`)

```json
{
  "@context": "https://schema.org",
  "@type": "ListItem",
  "position": 1,
  "item": {
    "@type": "RealEstateListing",
    "@id": "https://www.zumper.com/apartment-buildings/p203911/pearl-pine-financial-district-new-york-ny",
    "url": "https://www.zumper.com/apartment-buildings/p203911/pearl-pine-financial-district-new-york-ny",
    "name": "Pearl & Pine",
    "datePosted": "2026-10-02",
    "about": {
      "@type": "ApartmentComplex",
      "name": "Pearl & Pine",
      "telephone": "(332) 587-0974",
      "image": "https://img.zumpercdn.com/918579216/1280x960",
      "amenityFeature": [
        { "@type": "LocationFeatureSpecification", "name": "Air Conditioning", "value": true },
        { "@type": "LocationFeatureSpecification", "name": "Hardwood Floor", "value": true }
      ],
      "numberOfBedrooms": "...",
      "petsAllowed": true,
      "address": { "@type": "PostalAddress", "..." : "..." }
    }
  }
}
```

The `RealEstateListing` `@id` is stable (`/apartment-buildings/p<id>/<slug>`). Price is **not** in the JSON-LD; take it from the card / hydration (see field map).

### Server-rendered card sample (one full card, from `sample/zumper-card-sample.html`)

Card root: `div[data-testid="listing-card"]` (Chakra component, CSS-module + arbitrary-Tailwind classes).
Rendered text fields for one card:

```text
Featured · 4d ago · 9.6 Excellent · Our team has verified this company · Verified
Quick look
Parker Towers
10420 Queens Blvd, New York, NY 11375
Furnished · On-site laundry · Hardwood floor
Studio–4 beds · 1–2 baths
$2,829–$6,489
Price drop   Tour   Check availability   Call
```

```html
<div data-testid="listing-card" ...>
  <div class="ListingCardImageSection-container-box ...">
    <img alt="Parker Towers - Photo 1 of 1"
         srcSet="https://img.zumpercdn.com/434939807/1280x960?fit=crop&amp;h=208&amp;w=329&amp;..." />
  </div>
  ...
  <a href="/apartment-buildings/p456715/parker-towers-rego-park-new-york-ny"> ... </a>
  <a href="tel:5162190597"> ... </a>
  <span data-testid="list-card-badge">Featured</span>
  <svg data-testid="verified-svg"> ... </svg>
</div>
```

### Hydration sample (`sample/zumper-preloaded-state-sample.json`)

```json
{
  "currentSearch": { "firstPageCount": 25, "firstPageOffset": null, "firstPageAdditionalCount": 0,
                     "hasMoreListables": true, "countsBy": { "bedrooms": {}, "minPrice": {} } },
  "searchUI":      { "limit": 20, "offset": 0, "pageOffset": 0, "loadMoreCount": 0, "moreResult": true },
  "geo":           { "cities": [ { "city_id": 2185, "name": "New York", "state": "NY",
                                   "url": "new-york-ny", "listing_count": 10400,
                                   "box": [-74.2557, 40.496, -73.7002, 40.9176] } ] }
}
```

### Pagination — query param, also server-rendered

Zumper exposes an explicit pager (`data-testid="pagination"`) and honours `?page=N`:

```text
GET https://www.zumper.com/apartments-for-rent/new-york-ny?page=2
HTTP 200, 896,985 bytes
<title>Apartments for Rent in NYC - 10,770 Rentals Updated Daily | Zumper - Page 2</title>
```

Verified: page 2 returned **25** `listing-card` nodes and a JSON-LD ItemList with **27** `ListItem` / **25** `RealEstateListing` entries (all distinct from page 1), while `hasMoreListables` stayed `true`. Page N is simply `"{base}?page={N}"` (page 1 is the bare slug — do **not** send `?page=1`, append only for N≥2). Stop when the ItemList is empty / cards repeat / `numberOfItems`/`listing_count` is exhausted / non-zero error / `max_pages`.

### Field map

| field | source |
|---|---|
| `item_id` | JSON-LD `item.@id` (stable `/apartment-buildings/p<id>/<slug>`); fallback card `a[href*="/apartment-buildings/"]` |
| `title` / `name` | JSON-LD `item.name` / card heading |
| `url` | JSON-LD `item.url` (absolute) |
| `address` | JSON-LD `about.address` / card street line |
| `beds` | card `Studio–4 beds` / hydration `listing_counts` keys |
| `baths` | card `1–2 baths` |
| `price` / `price_raw` | card price range `$2,829–$6,489` (JSON-LD has none) |
| `amenities` | JSON-LD `about.amenityFeature[].name`; card amenity chips |
| `rating` / `reviews` | card `9.6 · Excellent` |
| `verified` / `badges` | card `data-testid="verified-svg"` / `list-card-badge` |
| `phone` | card `a[href^="tel:"]` / JSON-LD `about.telephone` |
| `photo` | card `img[srcSet]` → `img.zumpercdn.com/<id>/1280x960` / JSON-LD `about.image` |
| `date_posted` | JSON-LD `item.datePosted` |
| `city_id` / `city` / `state` | hydration `geo.cities[0]` |
| `category` (slug) | requested category |
| `page`, `position`, `total_count` | pager context / ItemList `numberOfItems` |
| `source` | e.g. `"zumper_jsonld_itemlist"` |

### Taxonomy sources

- City taxonomy (authoritative): `https://www.zumper.com/sitemap.xml.gz` (sitemap index, gzip works through the proxy) → `https://www.zumper.com/sitemaps/AFR-cities.xml.gz` (**10,684 `<loc>`** city pages, "apartments for rent"). Sibling indexes exist: `AFR-neighborhoods.xml.gz`, `RFR-cities.xml.gz`, `HFR-cities.xml.gz`, plus price/pet/furnished variants (`AFR-cities-cheap.xml.gz`, `-pet-friendly`, `-luxury`, ...).
- `robots.txt` → `Sitemap: https://www.zumper.com/sitemap.xml.gz`; do not touch the `Disallow`ed `/api`, `/json`, `/listing-feed`, `/partials`, `/map` paths.
- Homepage links are client-rendered, so **use the sitemap**, not the homepage, for taxonomy.

## Implementation instructions

- Add `common/spiders/zumper_categories.py` with the exact 20-entry `CATEGORIES` dict above (a `(slug -> url)` map, deterministic order).
- Add a `zumper_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` plus `category_url`, and support running all categories, consistent with the other listing spiders.
- Request each city page through the configured ScrapeOps proxy (US). Parse **two sources and prefer JSON-LD**:
  1. Brace-extract and `json.loads` the `SearchResultsPage.mainEntity` ItemList from `script[type="application/ld+json"]` → emit one item per `RealEstateListing`.
  2. Optionally enrich from the server-rendered `div[data-testid="listing-card"]` nodes (price range, rating, badges, phone) and from `window.__PRELOADED_STATE__` (`currentSearch.firstPageCount`, `geo.cities[0]`).
- Paginate with `f"{base}?page={n}"` for `n >= 2`, driven by the ItemList/card count and `hasMoreListables`/`numberOfItems`, never a fixed page count. Deduplicate by `item_id`.
- Emit `item_id`, `title`, absolute `url`, `address`, `beds`, `baths`, `price`/`price_raw`, `amenities`, `rating`, `reviews`, `verified`, `badges`, `phone`, `photo`, `date_posted`, `city_id`, `city`, `state`, `category` (slug), `page`, `position`, `total_count`, `source`, `timestamp`.
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Detect bot-wall / challenge / proxy-error payloads explicitly (empty body, tiny body `< 5 KB`, ScrapeOps `"Failed to get successful response"`, captcha/`Pardon the Interruption` stubs) and log a clear warning instead of silently emitting 0 items.

## Attached evidence (committed to this repo under `sample/`)

- `sample/zumper-categories-all.json` — full `{slug: url}` map of all **10,684** city categories from the live sitemap.
- `sample/zumper-top20-categories.json` — the top-20 dict above.
- `sample/zumper-new-york-ny.html` — full page-1 capture (932,902 bytes).
- `sample/zumper-new-york-ny-p2.html` — full page-2 capture (`?page=2`, 896,985 bytes).
- `sample/zumper-itemlist.json` — extracted JSON-LD `SearchResultsPage.mainEntity` ItemList (25 listings).
- `sample/zumper-card-sample.html` — one full `data-testid="listing-card"` node.
- `sample/zumper-preloaded-state-sample.json` — trimmed `window.__PRELOADED_STATE__` hydration excerpt.
