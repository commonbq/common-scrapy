## Goal

Add a `movoto_listing` spider for **Movoto** (movoto.com, a Lower / Rocket-affiliated US real-estate marketplace). There is currently **no Movoto spider** under `common/spiders/` and **no open/closed Movoto issue** in this repository (checked the full issue list).

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage, the `/sitemap/` page and **20 city listing pages** all returned HTTP 200.

Movoto has **no classic retail "category" taxonomy**. Its catalogue is organised by **city/market search pages** (`https://www.movoto.com/<city-slug>/`), each of which is a product listing ("products" = active for-sale homes / property cards). Property-type variants exist as sub-paths (`/<city-slug>/condos/`, `/<city-slug>/single-family/`, `/<city-slug>/multi-family/`, `/<city-slug>/land/`, `/<city-slug>/open-houses/`, `/<city-slug>/rentals/`).

## Top 20 category URLs

City slugs come from the live `/sitemap/` page (**149 city URLs** linked at capture time) plus the sitemap index `https://www.movoto.com/ssl/sitemap.xml` → `list-city/cities_1.xml.gz`. The dict below is the top 20 US real-estate markets, kept in a deterministic, ordered 20-entry shape (mirror `apartments_categories.py` / `zillow_categories.py`).

```python
CATEGORIES = {
    "new-york-ny":       "https://www.movoto.com/new-york-ny/",
    "los-angeles-ca":    "https://www.movoto.com/los-angeles-ca/",
    "chicago-il":        "https://www.movoto.com/chicago-il/",
    "houston-tx":        "https://www.movoto.com/houston-tx/",
    "phoenix-az":        "https://www.movoto.com/phoenix-az/",
    "philadelphia-pa":   "https://www.movoto.com/philadelphia-pa/",
    "san-antonio-tx":    "https://www.movoto.com/san-antonio-tx/",
    "san-diego-ca":      "https://www.movoto.com/san-diego-ca/",
    "dallas-tx":         "https://www.movoto.com/dallas-tx/",
    "san-jose-ca":       "https://www.movoto.com/san-jose-ca/",
    "austin-tx":         "https://www.movoto.com/austin-tx/",
    "jacksonville-fl":   "https://www.movoto.com/jacksonville-fl/",
    "fort-worth-tx":     "https://www.movoto.com/fort-worth-tx/",
    "columbus-oh":       "https://www.movoto.com/columbus-oh/",
    "charlotte-nc":      "https://www.movoto.com/charlotte-nc/",
    "indianapolis-in":   "https://www.movoto.com/indianapolis-in/",
    "seattle-wa":        "https://www.movoto.com/seattle-wa/",
    "denver-co":         "https://www.movoto.com/denver-co/",
    "boston-ma":         "https://www.movoto.com/boston-ma/",
    "las-vegas-nv":      "https://www.movoto.com/las-vegas-nv/",
}
```

Verified live on 2026-10-07 (all HTTP 200, all server-rendered, 50 cards on page 1):

| slug | total listings | cards p1 | slug | total listings | cards p1 |
|---|---|---|---|---|---|
| new-york-ny | 21,716 | 50 | jacksonville-fl | 6,423 | 50 |
| los-angeles-ca | 13,416 | 50 | fort-worth-tx | 4,886 | 50 |
| chicago-il | 8,710 | 50 | columbus-oh | 3,888 | 50 |
| houston-tx | 17,419 | 50 | charlotte-nc | 5,914 | 50 |
| phoenix-az | 6,064 | 50 | indianapolis-in | 5,502 | 50 |
| philadelphia-pa | 9,882 | 50 | seattle-wa | 3,782 | 50 |
| san-antonio-tx | 14,347 | 50 | denver-co | 5,104 | 50 |
| san-diego-ca | 3,701 | 50 | boston-ma | 1,817 | 50 |
| dallas-tx | 5,736 | 50 | las-vegas-nv | 10,735 | 50 |
| san-jose-ca | 1,630 | 50 | austin-tx | 6,417 | 50 |

## First-category investigation: New York, NY

```text
GET https://www.movoto.com/new-york-ny/
HTTP 200, 317,891 bytes
<title>New York, NY Homes for Sale &amp; Real Estate - Movoto</title>
<h1>New York, NY Homes for Sale &amp; Real Estate</h1>
results banner: 1 - 50 of 21,716
```

### How the products load — Nuxt SSR: `#__INITIAL_STATE__` JSON + server-rendered cards (no XHR needed)

Evidence gathered while drafting this ticket:

- `__NEXT_DATA__` occurrences: **0** — it is **not** Next.js.
- It **is a Nuxt/Vue SSR app**: the document embeds a JSON state script
  `<script id="__INITIAL_STATE__" type="application/json">…</script>` which the client re-hydrates via
  `window.__INITIAL_STATE__ = JSON.parse(document.getElementById('__INITIAL_STATE__').textContent); …`.
- The listing payload lives at **`__INITIAL_STATE__.pageData.listings`** — an array of **50 fully-populated listing dicts** (`id`, `propertyId`, `listPrice`, `bed`, `bath`, `sqftTotal`, `lotSize`, `propertyType(DisplayName)`, `mlsNumber`, `mlsDbNumber`, `listingAgent`, `officeListName`, `officeListPhone`, `openHouses`, `yearBuilt`, `hoafee`, `status`, `geo{…}`, `path`, `tnImgPath`, …). **This is the primary, cleanest data source.**
- The same 50 items are also **server-rendered** as `<article class="mvt-cardproperty" data-id="<uuid>">` cards, each carrying a per-card **JSON-LD** `<script type="application/ld+json">` array with `SingleFamilyResidence` + `Product`/`Offer` nodes (name, url, address, geo, image, price). **Use this as the HTML fallback.**
- Page 1 of New York contains **50** cards → **50 unique `data-id` values**; `pageData.listings` also has **50** entries.
- The scraper therefore needs **plain HTTP + an HTML/JSON parser only**; no browser execution for the listing pages.
- PerimeterX is present (`perimeterxAppId: "PXPb7SA58F"` in the state) → **the ScrapeOps proxy is required**.

Card data attributes observed: `data-link-name`, `data-id` (stable UUID = `propertyId`), `mark-id` (`mark0_<lat>_<lng>`).

### Pagination — path-based, `/<city-slug>/p-<N>/`

Page 1 is the bare slug. Additional pages use a **dedicated `p-<N>` segment**:

```html
<section class="mvt-pagination grid xs-grid-cols-1">
  <div class="f4 text-center"><b class="text-bold">1 - 50 of 21,716</b>
      <span>Homes for sale in <b class="text-bold">New York, NY</b></span></div>
  <div class="mvt-pagination__list">
    <a class="mvt-pagination__list-item mvt-pagination__list-item--prev" href="#" disabled aria-label="Previous Page"></a>
    <a href="https://www.movoto.com/new-york-ny/"        class="mvt-pagination__list-item mvt-pagination__list-item--active">1</a>
    <a href="https://www.movoto.com/new-york-ny/p-2/"    class="mvt-pagination__list-item">2</a>
    <a href="https://www.movoto.com/new-york-ny/p-3/"    class="mvt-pagination__list-item">3</a>
    …
    <span>...</span>
    <a class="mvt-pagination__list-item" href="https://www.movoto.com/new-york-ny/p-99/">99</a>
    <a class="mvt-pagination__list-item mvt-pagination__list-item--next"
       href="https://www.movoto.com/new-york-ny/p-2/" role="button" aria-label="Next Page"></a>
  </div>
</section>
```

> ⚠️ **Gotcha (verified live):** `/<city-slug>/<N>/` is **NOT** pagination. `GET /new-york-ny/2/` returned a *search* page for the term "2" (`<title>2, New York Homes For Sale…`, "1 - 50 of 4,609", different cards). The correct page 2 URL is **`/new-york-ny/p-2/`** — verified: HTTP 200, 321,152 bytes, banner `51 - 100 of 21,716`, 50 cards, **0 overlap** with page 1.

> ⚠️ **Gotcha:** the pager only renders links up to page **99** then an ellipsis (no `last` link). New York's true page count is `ceil(21716/50) = 435`. **Always compute the last page from the `X - Y of TOTAL` banner (`ceil(TOTAL/50)`), never from the nav.**

### Field map (from `pageData.listings[]` / card JSON-LD)

| field | source |
|---|---|
| `item_id` | `listing.propertyId` (UUID; == card `data-id`) |
| `url` | `https://www.movoto.com/` + `listing.path` (card fallback: JSON-LD `Product.offers.url` / card `a[href]`) |
| `title` / `address` | `listing.geo.formatAddress` (card: `<address>` text; JSON-LD `name`) |
| `price` / `price_raw` | `listing.listPrice` (card: `ul > li.price`) |
| `beds` | `listing.bed` (card: `li` with `abbr[title=Bedroom]`) |
| `baths` | `listing.bath` (card: `li` with `abbr[title=Bathroom]`) |
| `sqft` | `listing.sqftTotal` |
| `lot_size` | `listing.lotSize` |
| `property_type` | `listing.propertyTypeDisplayName` / `propertyType` |
| `year_built` | `listing.yearBuilt` |
| `hoa_fee` | `listing.hoafee` |
| `status` | `listing.status` / `houseRealStatus` |
| `mls_number` / `mls_db` | `listing.mlsNumber` / `listing.mlsDbNumber` |
| `listing_agent` | `listing.listingAgent` |
| `office` / `office_phone` | `listing.officeListName` / `officeListPhone` |
| `open_houses` | `listing.openHouses` (card also emits an `Event` JSON-LD for open houses) |
| `lat` / `lng` | `listing.geo.lat` / `geo.lng` |
| `city` / `state` / `county` / `zip` / `neighborhood` | `listing.geo.*` |
| `photo` | `listing.tnImgPath` (card: `img[src]`) |
| `days_on_movoto` / `list_date` | `listing.daysOnMovoto` / `listDate` |
| `category` | city slug (keep on every item) |

### Sample HTML / JSON

- Card HTML (trimmed): `sample/movoto-card-sample.html`
- Pagination HTML (trimmed): `sample/movoto-pagination-sample.html`
- One parsed listing: `sample/movoto-listing-sample.json`
- Trimmed `__INITIAL_STATE__` (with `pageData.listings[0]`): `sample/movoto-initial-state-sample.json`

```html
<article class="mvt-cardproperty style1" data-link-name="Card"
         data-id="5b834876-5af7-4556-a496-1a9f5981db0c" mark-id="mark0_40.661365_-73.957509">
  <script type="application/ld+json">[{"@context":"http://schema.org","@type":"SingleFamilyResidence",
    "name":"155 Lincoln Rd, Brooklyn, NY 11225",
    "url":"https://www.movoto.com/brooklyn-ny/155-lincoln-rd-brooklyn-ny-11225/pid_jxiur8tqjh/",
    "address":{"@type":"PostalAddress","streetAddress":"155 Lincoln Rd","addressLocality":"Brooklyn","postalCode":"11225","addressRegion":"NY"},
    "geo":{"@type":"GeoCoordinates","latitude":40.661365,"longitude":-73.957509},
    "image":"https://pi.movoto.com/p/482/1059590_0_2ViUFv_p.webp"},
   {"@context":"http://schema.org","@type":"Product","name":"155 Lincoln Rd, Brooklyn, NY 11225",
    "offers":{"@type":"Offer","priceCurrency":"USD","availability":"http://schema.org/InStock","price":2500000,
    "url":"https://www.movoto.com/brooklyn-ny/155-lincoln-rd-brooklyn-ny-11225/pid_jxiur8tqjh/"},
    "description":"155 Lincoln Rd, Brooklyn, NY 11225","image":"https://pi.movoto.com/p/482/1059590_0_2ViUFv_p.webp"}]</script>
  <div class="mvt-cardproperty-info"><div>
    <a href="https://www.movoto.com/brooklyn-ny/155-lincoln-rd-brooklyn-ny-11225/pid_jxiur8tqjh/" target="_blank" tabindex="-1">
      <address><span>155 Lincoln Rd, </span><span>Brooklyn, NY 11225</span></address></a>
  </div>
  <ul data-viewed="false"><li class="price">$2,500,000</li>
      <li>6<abbr title="Bedroom">Bd</abbr></li>
      <li>5<abbr title="Bathroom">Ba</abbr></li>
      <li>3,660 <abbr title="Sqft">Sq Ft</abbr></li></ul></div>
  <div class="tag-panel"><span class="tag tag-left custom new-tag"><span>New</span><span>47 Min</span></span></div>
</article>
```

### Taxonomy sources

- `https://www.movoto.com/sitemap/` — human-facing sitemap, **149 city links** (`https://www.movoto.com/<city>-<st>/`), captured as `sample/movoto-city-sitemap-page.html`.
- `https://www.movoto.com/robots.txt` → `Sitemap: https://www.movoto.com/ssl/sitemap.xml` (index) → `list-city/cities_1.xml.gz` (authoritative full city list, gzipped; the proxy mangles `.gz`, so prefer the `/sitemap/` page or the uncompressed city links).
- Homepage also links curated metros plus property-type roots (`/for-sale/`, `/single-family/`, `/condos/`, …).
- Property-type variant of any city: `/<city-slug>/<type>/` (e.g. `/new-york-ny/condos/`).

## Implementation instructions

- Add `common/spiders/movoto_categories.py` with the exact 20-entry `CATEGORIES` dict above (a `(slug -> url)` map, deterministic order).
- Add a `movoto_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` and support `category_url` / running all categories, consistent with the other listing spiders.
- Request each city page through the configured ScrapeOps proxy (US) and parse the **`#__INITIAL_STATE__` JSON first** — `json.loads(response.css('script#__INITIAL_STATE__::text').get())` → `pageData["listings"]`. Fall back to **server-rendered `article.mvt-cardproperty`** cards (and their per-card JSON-LD) when the state script is missing/empty.
- Paginate by building `f"{base}p-{N}/"` from the paging nav / banner, up to `ceil(total / 50)` where `total` comes from the `X - Y of TOTAL` banner. **Do not** use `/<slug>/<N>/` (that is a search-term URL) and **do not** cap at the nav's page-99 ellipsis.
- Emit `item_id` from `propertyId` (stable), plus `url`, `address`/`title`, `price`/`price_raw`, `beds`, `baths`, `sqft`, `lot_size`, `property_type`, `year_built`, `hoa_fee`, `status`, `mls_number`, `listing_agent`, `office`, `office_phone`, `open_houses`, `lat`/`lng`, `city`/`state`/`county`/`zip`/`neighborhood`, `photo`, `category` (slug), `page`, `source="movoto_initial_state"` (or `"movoto_card_html"`).
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Deduplicate by `propertyId`; stop on an empty page, a short page (< 50), a repeated page (same first id as previous), a nonzero error, missing listings, or `max_pages`.
- Detect bot-wall/challenge/proxy-error payloads explicitly (PerimeterX challenge pages, `"Failed to get successful response"`/captcha bodies) and log a clear warning instead of silently emitting 0 items.
- Do **not** use Playwright — plain HTTP HTML/JSON parsing is sufficient for both page 1 and pagination.

## Acceptance criteria

- Unit fixtures/tests cover: `__INITIAL_STATE__` listing extraction, card/JSON-LD fallback parsing, field mapping, `propertyId` dedup, pagination (`/<slug>/p-2/` distinct from page 1 and from the `/2/` search-page trap), banner-derived last-page, challenge/error detection, and stop conditions.
- A live one-page New York run through ScrapeOps returns 50 items with unique `item_id` values.
- A live two-page run proves page 2 (`/new-york-ny/p-2/`) is distinct (IDs differ, 0 overlap) and respects `max_pages`.
- Document the spider, the 20-city taxonomy, the loading mechanism (Nuxt `__INITIAL_STATE__` + server-rendered cards + `p-<N>` pagination), the proxy requirement, and the sitemap source in the README.

## Attached evidence

- Category dict (top 20) + taxonomy sources: above; also `sample/movoto-top20-categories.py` / `.json`.
- Sample card HTML, pagination HTML and `__INITIAL_STATE__` JSON: inline above.
- Local capture artifacts used while drafting this ticket:
  - `sample/movoto-new-york-ny.html` — New York listing page 1 (317,891 bytes, 50 cards, `1 - 50 of 21,716`)
  - `sample/movoto-new-york-ny-p-2.html` — New York page 2 (`/p-2/`, 321,152 bytes, `51 - 100 of 21,716`, distinct ids)
  - `sample/movoto-los-angeles-ca.html`, `movoto-chicago-il.html`, `movoto-houston-tx.html`, `movoto-phoenix-az.html` — four more verified city pages
  - `sample/movoto-city-sitemap-page.html` — `/sitemap/` page with 149 city links
  - `sample/movoto-category-verification.json` — live HTTP/status/card/total for all 20 categories
  - `sample/movoto-initial-state-sample.json`, `sample/movoto-listing-sample.json`, `sample/movoto-card-sample.html`, `sample/movoto-pagination-sample.html`
  - `sample/movoto-top20-categories.py`, `sample/movoto-top20-categories.json`

## Environment

- Branch/commit: `cron-ticket-movoto`
- Capture date: 2026-10-07 (Asia/Bangkok)
- Proxy: repository `SCRAPEOPS_PROXY` (`country=us`); diagnostic curl used `-k` to trust the proxy's TLS interception
- Runtime notes: Movoto is a **Nuxt/Vue SSR** app — data is in `#__INITIAL_STATE__` (`pageData.listings`, 50/page) and duplicated as server-rendered `article.mvt-cardproperty` cards with per-card JSON-LD. Pagination is `/<slug>/p-<N>/` (the `/2/` form is a search URL). Pager display caps at page 99; derive the last page from the results banner. 50 results per page.
