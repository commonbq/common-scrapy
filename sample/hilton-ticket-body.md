## Goal

Add a `hilton_listing` spider for **Hilton** (hilton.com, one of the most popular global hotel brands). There is currently **no Hilton spider** under `common/spiders/` and **no open/closed Hilton issue** in this repository (checked the full issue list — `gh issue list --limit 300 --state all`).

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, the `/en/locations/` hub and **20 US city destination pages** all returned HTTP 200.

Hilton has **no classic retail "category" taxonomy**. Its catalogue is organised by **destination ("locations") pages**: `https://www.hilton.com/en/locations/<country>/<state>/<city>/`. Each of these is a product listing where the "products" are **hotels**. Every city page also exposes **sub-category** links (by brand, by amenity, by nearby attraction) via `pageData.location.pageInterlinks`, e.g. `…/new-york/new-york/luxury/`, `…/new-york/new-york/hilton-hotels/`, `…/new-york/new-york/central-park/`.

## Top 20 category URLs

Destination slugs come from the live **`/en/locations/` hub page** (`https://www.hilton.com/en/locations/`), whose Next.js `dehydratedState` embeds **2,499 US destination URLs** (and 2,599 worldwide) as `locations/<country>/<state>/<city>/`. The authoritative full list is also available as a sitemap index: `https://www.hilton.com/sitemap.xml` → `…/sitemap/en/sitemap-en.xml` → 20 × `sitemap-en-location-0NN.xml`.

The dict below is the top 20 US real-estate/travel markets, kept in a deterministic, ordered 20-entry shape (mirror `agoda_categories.py` / `rent_categories.py`).

```python
HILTON_CATEGORIES = {
    "new-york-ny": "https://www.hilton.com/en/locations/usa/new-york/new-york/",
    "los-angeles-ca": "https://www.hilton.com/en/locations/usa/california/los-angeles/",
    "chicago-il": "https://www.hilton.com/en/locations/usa/illinois/chicago/",
    "miami-fl": "https://www.hilton.com/en/locations/usa/florida/miami/",
    "las-vegas-nv": "https://www.hilton.com/en/locations/usa/nevada/las-vegas/",
    "orlando-fl": "https://www.hilton.com/en/locations/usa/florida/orlando/",
    "san-francisco-ca": "https://www.hilton.com/en/locations/usa/california/san-francisco/",
    "washington-dc": "https://www.hilton.com/en/locations/usa/district-of-columbia/washington/",
    "boston-ma": "https://www.hilton.com/en/locations/usa/massachusetts/boston/",
    "seattle-wa": "https://www.hilton.com/en/locations/usa/washington/seattle/",
    "houston-tx": "https://www.hilton.com/en/locations/usa/texas/houston/",
    "dallas-tx": "https://www.hilton.com/en/locations/usa/texas/dallas/",
    "atlanta-ga": "https://www.hilton.com/en/locations/usa/georgia/atlanta/",
    "phoenix-az": "https://www.hilton.com/en/locations/usa/arizona/phoenix/",
    "san-diego-ca": "https://www.hilton.com/en/locations/usa/california/san-diego/",
    "denver-co": "https://www.hilton.com/en/locations/usa/colorado/denver/",
    "new-orleans-la": "https://www.hilton.com/en/locations/usa/louisiana/new-orleans/",
    "nashville-tn": "https://www.hilton.com/en/locations/usa/tennessee/nashville/",
    "austin-tx": "https://www.hilton.com/en/locations/usa/texas/austin/",
    "honolulu-hi": "https://www.hilton.com/en/locations/usa/hawaii/honolulu/",
}
```

Verified live on 2026-10-07 (all HTTP 200, all server-rendered; hotel cards on page 1):

| slug | location name | hotels p1 | first ctyhocn | slug | location name | hotels p1 | first ctyhocn |
|---|---|---|---|---|---|---|---|
| new-york-ny | New York, NY | 20 | NYCTEPO | houston-tx | Houston, TX | 20 | — |
| los-angeles-ca | Los Angeles, CA | 20 | — | dallas-tx | Dallas, TX | 20 | — |
| chicago-il | Chicago, IL | 20 | — | atlanta-ga | Atlanta, GA | 20 | — |
| miami-fl | Miami, FL | 20 | — | phoenix-az | Phoenix, AZ | 20 | — |
| las-vegas-nv | Las Vegas, NV | 20 | — | san-diego-ca | San Diego, CA | 20 | — |
| orlando-fl | Orlando, FL | 20 | — | denver-co | Denver, CO | 20 | — |
| san-francisco-ca | San Francisco, CA | 20 | — | new-orleans-la | New Orleans, LA | 20 | — |
| washington-dc | Washington, DC | 20 | — | nashville-tn | Nashville, TN | 20 | — |
| boston-ma | Boston, MA | 20 | — | austin-tx | Austin, TX | 20 | — |
| seattle-wa | Seattle, WA | 18 | — | honolulu-hi | Honolulu, HI | 15 | — |

> Page sizes are **capped at 20** (see caveat below); a few thin markets return fewer (Seattle 18, Honolulu 15).

## First-category investigation: New York, NY

```text
GET https://www.hilton.com/en/locations/usa/new-york/new-york/
HTTP 200, 1,141,889 bytes
<title>Hotels in New York, NY - Find Hotels - Hilton</title>
pageData.location.title: "Hotels in New York, [NY](New York)"
pageData.location.uri:   "locations/usa/new-york/new-york/"
pageData.match:          {"name":"New York, New York, USA","type":"locality", …}
```

### How the products load — Next.js SSR: `#__NEXT_DATA__` JSON + server-rendered cards (no XHR needed)

Evidence gathered while drafting this ticket:

- `__NEXT_DATA__` occurrences: **1** — it **is Next.js** (`<script id="__NEXT_DATA__" type="application/json">…</script>`). `props.page` = `/locations/[...slug]`.
- The hotel listing payload lives at **`props.pageProps.pageData.hotelSummaryOptions.hotels`** — an array of **up to 20 fully-populated hotel dicts** (`ctyhocn`, `name`, `brandCode`, `address{…}`, `localization.coordinate{latitude,longitude}`, `images.master.ratios[].url`, `leadRate.lowest.rateAmount`, `distance`, `amenityIds`, `display{open,openDate}`, `facilityOverview.homeUrlTemplate`, …). **This is the primary, cleanest data source.**
- The ordering list is duplicated at **`props.pageProps.pageData.ctyhocnList.hotelList`** (array of `{"ctyhocn": "<code>"}`, 20 entries) and the size is mirrored at **`hotelSummaryOptions._hotels.totalSize`** (= 20).
- The same hotels are also **server-rendered** as cards: `<a target="_blank" href="https://www.hilton.com/en/hotels/<ctyhocn>-<slug>/">` containing `<h3 data-testid="listViewPropertyName">…</h3>`. **Use this as the HTML fallback.**
- Page 1 of New York contains **20** hotel anchors; `hotelSummaryOptions.hotels` also has **20** entries.
- The page is SSR (`isSSR: true`); the same GraphQL response is embedded in `props.pageProps.dehydratedState` under query **`hotelSummaryOptions_geocodePage`** with variables `{"path":"locations/usa/new-york/new-york","language":"en","queryLimit":20,"currencyCode":"USD", …}`. The scraper needs **plain HTTP + an HTML/JSON parser only** — no browser execution, no separate XHR fetch.
- No bot-wall markers observed (no captcha / Akamai / PerimeterX / DataDome / Incapsula strings). Perimeter/CDN protection is nevertheless assumed present, so **the ScrapeOps proxy is required (and used for every request)**.

Card markup observed (server-rendered fallback):

```html
<a target="_blank" href="https://www.hilton.com/en/hotels/nyctepo-tempo-new-york-times-square/" class="link--base inline-block link--brand" rel="noopener noreferrer">
  <div class="underline-offset-2 inline-block">
    <h3 data-testid="listViewPropertyName" class="heading--base heading--xs w-full break-words font-semibold leading-snug pe-10">Tempo by Hilton New York Times Square</h3>
  </div><span class="sr-only">, <span>Opens new tab</span></span>
</a>
```

### ⚠️ Caveat — the destination landing page is capped at 20 hotels

The embedded GraphQL query hard-codes **`queryLimit: 20`**, and every city page returns **at most 20** hotels (New York, with 100+ properties, returns exactly 20). This 20-hotel SSR set is the intended primary source for this spider (one page → up to 20 items). The full, paginated inventory lives behind Hilton's `/search/` flow, which `robots.txt` disallows (`Disallow: /search/`) and which requires a session/token — **out of scope** for this ticket. Document the cap; do not attempt to defeat `/search/`.

### Sub-categories (optional second level)

`pageData.location.pageInterlinks` is a list of `{title, links:[{name, uri}]}` groups giving deeper city pages:
- *by amenities & features* → `locations/usa/new-york/new-york/<amenity>/` (e.g. `boutique`, `luxury`, `spa`, `pet-friendly`, `extended-stay`)
- *by brand* → `locations/usa/new-york/new-york/<brand>/` (e.g. `hilton-hotels`, `hampton-by-hilton`, `waldorf-astoria`, `conrad-hotels`)
- *near attractions* → `locations/usa/new-york/new-york/<attraction>/` (e.g. `central-park`, `bryant-park`)

Each of these is itself a valid listing page (same `__NEXT_DATA__` shape, capped at 20).

### Field map (from `pageData.hotelSummaryOptions.hotels[]`)

| field | source |
|---|---|
| `item_id` | `hotel.ctyhocn` (stable Hilton property code; == card hotel URL prefix) |
| `url` | `hotel.facilityOverview.homeUrlTemplate` (fallback: card `a[href]`) |
| `title` | `hotel.name` (card: `h3[data-testid=listViewPropertyName]`) |
| `brand_code` | `hotel.brandCode` |
| `address` / `city` / `state` / `state_name` / `postal_code` / `country` | `hotel.address.addressFmt` / `.city` / `.state` / `.stateName` / `.postalCode` / `.country` |
| `lat` / `lng` | `hotel.localization.coordinate.latitude` / `.longitude` |
| `price` / `price_fmt` / `currency` | `hotel.leadRate.lowest.rateAmount` / `.rateAmountFmt` / `hotel.localization.currencyCode` |
| `rate_plan` | `hotel.leadRate.lowest.ratePlan.ratePlanName` |
| `distance` / `distance_fmt` | `hotel.distance` / `hotel.distanceFmt` |
| `amenities` | `hotel.amenityIds` |
| `is_open` / `open_date` | `hotel.display.open` / `hotel.display.openDate` |
| `phone` | `hotel.contactInfo.phoneNumber` |
| `photo` | `hotel.images.master.ratios[].url` (prefer a stable size, e.g. `threeByTwo`) |
| `category` | city slug (keep on every item) |

## Implementation instructions

- Add `common/spiders/hilton_categories.py` with the exact 20-entry `HILTON_CATEGORIES` dict above.
- Add a `hilton_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` and support `category_url` / running all categories, consistent with the other listing spiders.
- Request each destination page through the configured ScrapeOps proxy (US) and parse the **`#__NEXT_DATA__` JSON first** — `json.loads(response.css('script#__NEXT_DATA__::text').get())` → `props.pageProps.pageData.hotelSummaryOptions.hotels`. Fall back to **server-rendered hotel anchors** (`a[href*="/en/hotels/"]` with `h3[data-testid=listViewPropertyName]`) when the state script is missing/empty.
- Emit `item_id` from `ctyhocn` (stable), plus the field map above; `source="hilton_next_data"` (or `"hilton_card_html"`).
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Deduplicate by `ctyhocn`; stop on an empty/short list or `max_pages`. There is **no page 2** on a destination page — pagination beyond 20 is intentionally out of scope (document it).
- Detect bot-wall/challenge/proxy-error payloads explicitly (captcha / 403 / "access denied" / ScrapeOps error bodies) and log a clear warning instead of silently emitting 0 items.
- Do **not** use Playwright — plain HTTP HTML/JSON parsing is sufficient.

## Acceptance criteria

- Unit fixtures/tests cover: `__NEXT_DATA__` hotel extraction, card-anchor fallback parsing, field mapping, `ctyhocn` dedup, and challenge/error detection.
- A live one-city New York run through ScrapeOps returns 20 items with unique `item_id` values.
- Document the spider, the 20-city taxonomy, the loading mechanism (Next.js `__NEXT_DATA__` + `hotelSummaryOptions.hotels` + server-rendered cards), the 20-hotel cap, and the proxy requirement in the README.

## Attached evidence

- Category dict (top 20): above; also `sample/hilton-top20-categories.py` / `sample/hilton-top20-categories.json`.
- Category verification (HTTP/hotel counts for all 20): `sample/hilton-category-verification.json`.
- Sample HTML / JSON (inline above):
  - `sample/hilton-new-york-ny.html` — New York destination page 1 (1,141,889 bytes, 20 hotels)
  - `sample/hilton-chicago-il.html` — Chicago destination page (1,196,827 bytes, 20 hotels)
  - `sample/hilton-next-data-sample.json` — trimmed `__NEXT_DATA__` (`location` + `pageInterlinks` + first 2 hotels + `ctyhocnList`)
  - `sample/hilton-hotel-sample.json` — one full hotel dict (`CYCTEPO`/Tempo)
  - `sample/hilton-hotel-card-sample.html` — server-rendered hotel card anchor
  - `sample/hilton-subcategory-links.json` — `pageInterlinks` brand/amenity/attraction sub-category URLs
- Taxonomy sources: `/en/locations/` hub `dehydratedState` (2,499 US destinations) and sitemap index `https://www.hilton.com/sitemap.xml` → `…/sitemap/en/sitemap-en.xml` → `sitemap-en-location-0NN.xml`.

## Environment

- Branch/commit: `cron-ticket-hilton`
- Capture date: 2026-10-07 (Asia/Bangkok)
- Proxy: repository `SCRAPEOPS_PROXY` (`country=us`); diagnostic curl used `-k` to trust the proxy's TLS interception
- Runtime notes: Hilton is a **Next.js** app — the destination page's hotels are in `#__NEXT_DATA__` → `props.pageProps.pageData.hotelSummaryOptions.hotels` (≤20, `queryLimit:20`) and duplicated as server-rendered `a[href*="/en/hotels/"]` cards. No historical spider and no prior Hilton issue exist in this repo.
