## Goal

Add a `tripcom_listing` spider for **Trip.com** (`trip.com` / `us.trip.com`), one of the largest global online travel agencies (Trip.com Group / Ctrip). There is currently **no Trip.com spider** under `common/spiders/` and **no open/closed Trip.com issue** in this repository.

Check performed before drafting:

```text
gh issue list --repo commonbq/common-scrapy --state all --search "trip.com in:title"  -> empty
grep -ril "trip.com" common/spiders tests        -> none (only this ticket's own sample files)
ls common/spiders | grep -i trip                 -> none
```

All live discovery below was performed on **2026-10-07** through the repository-configured ScrapeOps US proxy (`SCRAPEOPS_PROXY`, `country=us`). The homepage and **twenty city hotel-list pages** all returned HTTP 200.

Trip.com (like the other travel sites already covered — Agoda, Booking.com, Klook, GetYourGuide, Viator, Tripadvisor) has **no classic retail "category" taxonomy**. Its catalogue is organised by **destination hotel-list pages** (`https://us.trip.com/hotels/<city>-hotels-list-<cityId>/`), each of which is a product listing ("products" = hotels / stays).

## Top 20 category URLs

The taxonomy comes straight off the homepage's server-rendered SEO link block `seoLinksContent.data.tabList` → tab **`Popular Hotels`** (**21 links**). The dict below is the top 20 of those 21 (the 21st, `da-nang`, is on the `www.` host and is dropped to keep a deterministic 20-entry shape; mirror `agoda_categories.py` / `booking_categories.py`). Raw capture: `sample/trip-com-home-seolinks-popular-hotels.json`.

```python
CATEGORIES = {
    "shanghai":     "https://us.trip.com/hotels/shanghai-hotels-list-2/",
    "hong-kong":    "https://us.trip.com/hotels/hong-kong-hotels-list-58/",
    "las-vegas":    "https://us.trip.com/hotels/las-vegas-hotels-list-26282/",
    "bangkok":      "https://us.trip.com/hotels/bangkok-hotels-list-359/",
    "beijing":      "https://us.trip.com/hotels/beijing-hotels-list-1/",
    "guangzhou":    "https://us.trip.com/hotels/guangzhou-hotels-list-32/",
    "new-york":     "https://us.trip.com/hotels/new-york-hotels-list-633/",
    "singapore":    "https://us.trip.com/hotels/singapore-hotels-list-73/",
    "kuala-lumpur": "https://us.trip.com/hotels/kuala-lumpur-hotels-list-315/",
    "dubai":        "https://us.trip.com/hotels/dubai-hotels-list-220/",
    "chicago":      "https://us.trip.com/hotels/chicago-hotels-list-549/",
    "san-diego":    "https://us.trip.com/hotels/san-diego-hotels-list-698/",
    "miami":        "https://us.trip.com/hotels/miami-hotels-list-25773/",
    "new-orleans":  "https://us.trip.com/hotels/new-orleans-hotels-list-1186/",
    "nashville":    "https://us.trip.com/hotels/nashville-hotels-list-3228/",
    "boston":       "https://us.trip.com/hotels/boston-hotels-list-26848/",
    "orlando":      "https://us.trip.com/hotels/orlando-hotels-list-1187/",
    "savannah":     "https://us.trip.com/hotels/savannah-hotels-list-26631/",
    "charleston":   "https://us.trip.com/hotels/charleston-hotels-list-4188/",
    "los-angeles":  "https://us.trip.com/hotels/los-angeles-hotels-list-347/",
}
```

Verified live on 2026-10-07 — **all 20 HTTP 200**, all server-rendered, **9 cards + 9 JSON-LD items** each:

| slug | bytes | main-grid cards | JSON-LD items | unique hotel ids on page |
|---|---|---|---|---|
| shanghai | 3,772,406 | 9 | 9 | 61 |
| hong-kong | 3,299,210 | 9 | 9 | 58 |
| las-vegas | 3,092,157 | 9 | 9 | 54 |
| bangkok | 3,380,755 | 9 | 9 | 65 |
| beijing | 3,488,518 | 9 | 9 | 57 |
| guangzhou | 3,906,106 | 9 | 9 | 69 |
| new-york | 3,184,017 | 9 | 9 | 63 |
| singapore | 3,503,654 | 9 | 9 | 53 |
| kuala-lumpur | 3,276,768 | 9 | 9 | 58 |
| dubai | 3,286,767 | 9 | 9 | 68 |
| chicago | 3,086,896 | 9 | 9 | 47 |
| san-diego | 3,049,076 | 9 | 9 | 56 |
| miami | 2,794,780 | 9 | 9 | 50 |
| new-orleans | 3,003,512 | 9 | 9 | 54 |
| nashville | 3,263,001 | 9 | 9 | 47 |
| boston | 3,694,828 | 9 | 9 | 57 |
| orlando | 3,168,727 | 9 | 9 | 60 |
| savannah | 2,688,603 | 9 | 9 | 37 |
| charleston | 2,424,820 | 9 | 9 | 50 |
| los-angeles | 3,294,386 | 9 | 9 | 58 |

> Per-category machine-readable verification: `sample/trip-com-category-verification.json`. The ordered dict is `sample/trip-com-top20-categories.json`.

## First-category investigation: Bangkok

```text
GET https://us.trip.com/hotels/bangkok-hotels-list-359/
HTTP 200, 3,380,755 bytes
<title>10 Best Bangkok Hotels, Thailand (from $20) | Trip.com</title>
<link rel="canonical" href="https://us.trip.com/hotels/bangkok-hotels-list-359/" />
<meta name="description" content="Discover best hotels in Bangkok, Thailand from $20. Get great hotel deals, read hotel reviews, and book cheap hotels in Bangkok now!" />
```

### How the products load — server-rendered HTML + JSON-LD `ItemList` (no XHR / no `__NEXT_DATA__` / no hydration JSON)

- `__NEXT_DATA__`: **0**, `__INITIAL_STATE__`: **0**, `__NUXT__`: **0**, `__APOLLO_STATE__`: **0** — this is a plain **server-rendered SEO page** (Trip.com's own streaming framework, no Next.js).
- The hotel list is fully present in the raw HTML — **no browser execution required**. Products are exposed **two ways**:
  1. **`<script type="application/ld+json">` → `ItemList`** (the cleanest source). 9 `itemListElement`s, each `{ "@type": "ListItem", "position", "item": { "@type": "Hotel", "name", "url", "image", "starRating": {"@type":"Rating","ratingValue":N}, "aggregateRating": {"@type":"AggregateRating","ratingValue":"8.0","bestRating":10,"worstRating":1,"reviewCount":16689} } }`. (A second ld+json block is an FAQPage — ignore it.)
  2. **Server-rendered DOM cards** in the `Best hotels in Bangkok` section: `div.Template-Grid-Hotel-Cards-hotel-card-container` → 9 × `a.Template-Grid-Hotel-Cards-hotel-card[href=".../hotels/<slug>-hotel-detail-<id>/<slug>/"]`, each with image, `rating-score`, `rating-count`, `<h3>name ★★★★`, `hotel-location` (address), `hotel-description` (a review snippet), and `hotel-price` (`1 night` + `$NN`).
- The page also contains several **secondary grids/sections** (`Where to stay in Bangkok`, `Find the perfect stay for your travel style`, `Hotels near top Bangkok landmarks`, `Real traveler reviews`, …) which together add up to **65 unique `-hotel-detail-<id>/` links** on the Bangkok page (54–69 per city). The primary, uniformly structured grid is the 9-card `Template-Grid-Hotel-Cards` block.
- **No listing XHR/GraphQL is used or required** for the SEO page. The interactive search page (`/hotels/list?city=<id>`) *does* fetch over XHR (`/restapi/soa2/34951/fetchHotelList`, `.../fetchHotelListInit`, `.../fetchHotelListSeo`) after hydration via `window.__NFES_DATA__`, but those endpoints are **`Disallow`ed in `robots.txt`** and the page ships an anti-spider script — see "Interactive (XHR) page" below.

So the spider needs **plain HTTP + an HTML/JSON parser only**: brace-extract the `ItemList` ld+json and/or parse the `Template-Grid-Hotel-Cards` DOM.

### JSON-LD sample (first `itemListElement`, from `sample/trip-com-itemlist.json`)

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "item": {
        "@type": "Hotel",
        "name": "NASA BANGKOK - Airport Rail Link Ramkhamhang",
        "url": "https://us.trip.com/hotels/bangkok-hotel-detail-996749/nasa-bangkok-airport-rail-link-ramkhamhang/",
        "image": "https://ak-d.tripcdn.com/images/1mc0t12000btgb5fd35A4.jpg?proc=resize/m_r,w_700,h_448,8688",
        "starRating": { "@type": "Rating", "ratingValue": 4 },
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "8.0",
          "bestRating": 10,
          "worstRating": 1,
          "reviewCount": 16689
        }
      }
    }
  ]
}
```

The hotel-detail `url` shape `.../hotels/<city-slug>-hotel-detail-<hotelId>/<slug>/` is stable and unique per hotel (`996749` in the example). Address, review snippet and price are **not** in the JSON-LD — take them from the DOM cards.

### Server-rendered card sample (from `sample/trip-com-card-sample.html`)

Rendered text for card 1:

```text
NASA BANGKOK - Airport Rail Link Ramkhamhang ★★★★
📍 44 Sukhumvit 71 Rd, Suan Luang, Bangkok
8.0 (16,689 reviews)
"Room is a bit old. ..."
1 night   $15
Book now
```

```html
<div class="Template-Grid-Hotel-Cards-hotel-card-container">
  <a href="https://us.trip.com/hotels/bangkok-hotel-detail-996749/nasa-bangkok-airport-rail-link-ramkhamhang/"
     class="Template-Grid-Hotel-Cards-hotel-card">
    <div class="Template-Grid-Hotel-Cards-image-wrapper">
      <img src="https://ak-d.tripcdn.com/images/1mc0t12000btgb5fd35A4.jpg?proc=…&proc=format/f_webp"
           alt="NASA BANGKOK - Airport Rail Link Ramkhamhang"
           class="Template-Grid-Hotel-Cards-hotel-card-image">
      <div class="Template-Grid-Hotel-Cards-hotel-rating">
        <span class="Template-Grid-Hotel-Cards-rating-score">8.0</span>
        <span class="Template-Grid-Hotel-Cards-rating-count">(16,689 reviews)</span>
      </div>
    </div>
    <div class="Template-Grid-Hotel-Cards-hotel-card-content">
      <h3>NASA BANGKOK - Airport Rail Link Ramkhamhang
        <span class="Template-Grid-Hotel-Cards-stars">★★★★</span></h3>
      <div class="Template-Grid-Hotel-Cards-hotel-location">📍 44 Sukhumvit 71 Rd, Suan Luang, Bangkok</div>
      <p class="Template-Grid-Hotel-Cards-hotel-description">"Room is a bit old. …"</p>
      <div class="Template-Grid-Hotel-Cards-card-footer">
        <div class="Template-Grid-Hotel-Cards-hotel-price"><span>1 night</span> $15</div>
        <span class="Template-Grid-Hotel-Cards-view-hotel-btn">Book now</span>
      </div>
    </div>
  </a>
  …
</div>
```

### Interactive (XHR) page — documented for completeness, NOT the recommended source

```text
GET https://us.trip.com/hotels/list?city=359
HTTP 200, 755,178 bytes
```

- Hydration `window.__NFES_DATA__` is present but its `props.pageProps` is a near-empty shell (`{"pathname":"/list","asPath":"/hotels/search/list?city=359"}`) — the hotel rows are fetched **after load** by XHR.
- XHR endpoints seen in the markup / SSR call log: `/restapi/soa2/34951/fetchHotelList`, `/restapi/soa2/34951/fetchHotelListInit`, `/restapi/soa2/34951/fetchHotelListSeo`, `/restapi/soa2/34951/getHotelCommonFilter`, plus `/htls/restapi/*`.
- `robots.txt` explicitly disallows these: `Disallow: /restapi/soa2/*`, `Disallow: /htls/restapi/*`, and the page ships an anti-spider script (`hotel-spider-defence-new`).
- Full evidence: `sample/trip-com-hotel-list-xhr-sample.json`.

⇒ **Use the static SEO city pages.** They are robots-allowed, require no JS/cookies, and carry the same hotels in HTML + JSON-LD.

### Pagination

The SEO city page is a **single fixed page** — it is a "10 Best …" landing page, not a paged result set:

- `https://us.trip.com/hotels/bangkok-hotels-list-359/` → 9 cards.
- `https://us.trip.com/hotels/bangkok-hotels-list-359/2/` → HTTP 200 but a **2,545-byte stub, 0 cards**.
- `https://us.trip.com/hotels/bangkok-hotels-list-359/?page=2` → identical to page 1 (param ignored).
- No `<link rel="next">` / `<link rel="prev">`.

So the spider needs **no pager**: fetch each category URL once. Deduplicate hotels by `hotel_id` across categories (some hotels appear in landmark/areas sub-grids of the same page). If deeper inventory is ever needed, it must come from the robots-disallowed XHR — out of scope here and explicitly discouraged.

### Field map

| field | source |
|---|---|
| `item_id` / `hotel_id` | JSON-LD `item.url` / card href → `-hotel-detail-<id>-` (e.g. `996749`) |
| `title` | JSON-LD `item.name` / card `<h3>` text (minus stars) |
| `url` | JSON-LD `item.url` (absolute) |
| `image_url` | JSON-LD `item.image` / card `<img src>` |
| `star_rating` | JSON-LD `item.starRating.ratingValue` / card `.…-stars` count |
| `review_score` | JSON-LD `item.aggregateRating.ratingValue` / card `.rating-score` |
| `review_score_best` / `_worst` | JSON-LD `bestRating` / `worstRating` |
| `reviews_count` | JSON-LD `item.aggregateRating.reviewCount` / card `.rating-count` |
| `address` | card `.…-hotel-location` (strip the 📍 prefix) |
| `review_snippet` | card `.…-hotel-description` |
| `price` / `currency` | card `.…-hotel-price` (`$15`; currency from symbol) |
| `price_unit` | card `.…-hotel-price` (`1 night`) |
| `city` / `category` (slug) | requested category |
| `city_id` | trailing number of the category URL (e.g. `359`) |
| `position` | JSON-LD `position` / 0-based card index |
| `source_url` | the fetched category URL |
| `source` | e.g. `"tripcom_seo_jsonld_itemlist"` |
| `timestamp` | pipeline/constant |

### Taxonomy sources

- Homepage `https://us.trip.com/` → `seoLinksContent.data.tabList` (server-rendered) → tab `Popular Hotels` (21 destination links). Other tabs (`Popular flights`, `Hot car rental spots`, `Popular activities`, `Popular airlines`, `Popular trips`, …) are **not** hotel product listings.
- No usable sitemap: `robots.txt` lists **no `Sitemap:` entries**; the only human-facing index is the SEO links block. Additional destination slugs can be discovered from the "nearby / other cities" links and the landmark sub-grids inside any city page (all follow `/hotels/<city>-hotels-list-<id>/`).
- `robots.txt` `Disallow`s to respect: `/restapi/soa2/*`, `/htls/restapi/*`, `/htls/getHotDestination`, `/webapp/`, `/m/`, `/account/`, `/passport/`, `/maintain/`, `/*/getSeoTdk*`, `/*/getHotelSDTSource*`.

## Implementation instructions

- Add `common/spiders/tripcom_categories.py` with the exact 20-entry `CATEGORIES` dict above (a `(slug -> url)` map, deterministic order).
- Add a `tripcom_listing` spider subclassing `BaseListingSpider`; accept `-a category=<slug>` plus `category_url`, and support running all categories, consistent with the other listing spiders.
- Request each city page through the configured ScrapeOps proxy (US). Parse **two sources and prefer JSON-LD**:
  1. Brace-extract and `json.loads` the `application/ld+json` block whose `@type` is `ItemList` → emit one item per `ListItem.item` (`Hotel`).
  2. Enrich from the `Template-Grid-Hotel-Cards-hotel-card` cards in the `Best hotels in <city>` section (address, review snippet, price, price unit, star string). Optionally also harvest the other `-hotel-detail-<id>/` links on the page for extra coverage, de-duplicated by `hotel_id`.
- **No pagination** — one request per category. Stop logic: if JSON-LD/cards are empty, log and move on.
- Deduplicate by `hotel_id` (the numeric id in the detail URL).
- Emit `item_id`, `hotel_id`, `title`, absolute `url`, `image_url`, `star_rating`, `review_score`, `review_score_best`, `review_score_worst`, `reviews_count`, `address`, `review_snippet`, `price`, `currency`, `price_unit`, `city`/`category` (slug), `city_id`, `position`, `source_url`, `source`, `timestamp`.
- Keep the city slug (`category`) on every item so downstream partitioning works.
- Detect bot-wall / challenge / proxy-error payloads explicitly (empty body, tiny body `< 5 KB`, ScrapeOps `"Failed to get successful response"`, captcha stubs, the 2,545-byte `/2/` stub) and log a clear warning instead of silently emitting 0 items.

## Attached evidence (committed to this repo under `sample/`)

- `sample/trip-com-top20-categories.json` — the top-20 `{slug: url}` dict above.
- `sample/trip-com-home-seolinks-popular-hotels.json` — raw homepage `seoLinksContent` "Popular Hotels" tab (21 links) proving the taxonomy source.
- `sample/trip-com-category-verification.json` — per-category HTTP/bytes/cards/JSON-LD/unique-id table.
- `sample/trip-com-bangkok-hotels-list-359.html` — full Bangkok city-page capture (3,380,755 bytes).
- `sample/trip-com-itemlist.json` — extracted JSON-LD `ItemList` (9 `Hotel` entries).
- `sample/trip-com-card-sample.html` — the 9-card `Template-Grid-Hotel-Cards` container.
- `sample/trip-com-hotel-list-xhr-sample.json` — interactive `/hotels/list?city=359` XHR/`__NFES_DATA__` evidence + robots disallows.
