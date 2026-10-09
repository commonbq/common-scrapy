# Common Scrapy Retailer Spiders

An open, actively maintained collection of Scrapy spiders for harvesting structured product data from major retailers. Spiders are purpose-built per retailer with bootstrap/API/HTML fallback logic where needed.

> This repository is actively maintained by **OpenClaw AI Agents** (with human oversight).

## Installation

```bash
pip install common-scrapy
```

## CLI usage

`pip install common-scrapy` adds a `common-scrapy` console script so you can work with the packaged spider without cloning the repo.

### Proxy configuration

```bash
PROXY=http://user:pass@host:1234 common-scrapy crawl amazon_listing -a category=fashion
```

All spiders honor `PROXY` via project-wide middleware.

### List available spiders

```bash
common-scrapy list
```

### Run a crawl

```bash
common-scrapy crawl <identifier> [--category <category>] [additional Scrapy args]
```

> `--category` is required for listing spiders. If omitted, the CLI prints available categories for that spider.

Examples:

- `common-scrapy crawl target_search --category 5xtc0 -a max_pages=2 -O target.jsonl`
- `common-scrapy crawl kohls_listing --category women -a max_pages=1 -O kohls_listing.jsonl`
- `common-scrapy crawl sephora_listing --category makeup -a max_pages=1 -O sephora_listing.jsonl`
- `common-scrapy crawl newegg_listing --category desktop-cpu-processors -a max_pages=1 -O newegg.jsonl` (36 items, verified live on 2026-10-02; see [newegg_listing](#newegg_listing))
- `common-scrapy crawl cvs_listing --category health-medicine -a max_pages=3 -O cvs.jsonl` (60 items, verified live on 2026-10-04; see [cvs_listing](#cvs_listing))
- `common-scrapy crawl menards_listing --category halloween-animated-decorations -a max_pages=1 -O menards.jsonl`

`newegg_listing` parses the server-rendered `window.__initialState__.Products`
payload. It accepts `category`, `category_url`, or `url`; use
`all-current-categories` to refresh and crawl Newegg's live category inventory.

All extra args are forwarded to `scrapy crawl` unchanged (feeds, settings overrides, etc.).

### decathlon_listing

`decathlon_listing` reads products exclusively from Shopify's first-party
`/collections/<handle>/products.json` API. It requests up to 250 product records
per page and follows the API's numbered pages; there is no HTML-card, embedded
metadata, or JSON-LD fallback. The 20 category seeds in
`decathlon_categories.py` are the highest-inventory primary-nav collections.
Each item includes the complete API product object in `raw`, and the ordered
`FEED_EXPORT_FIELDS` contract contains 24 fields.

```bash
scrapy crawl decathlon_listing -a category=camp-hike -a max_pages=2 -s HTTPCACHE_ENABLED=False -O decathlon.jsonl
```

Verified live on 2026-10-08: the default `shop-all` crawl returned HTTP 200
and emitted 250 unique products from one API page in 6.9 seconds.

### dollartree_listing

`dollartree_listing` reads product records exclusively from Dollar Tree's
first-party Oracle Commerce Cloud guided-search API. It sends each category's
stable Endeca `dimension_id` to `/ccstoreui/v1/search` and paginates with the
API's `No` offset; there is no direct-HTML or JSON-LD fallback. The 20 category
seeds are ranked by the API's live product totals in
`dollartree_categories.py`. Each product includes the source attributes in
`raw`; the ordered `FEED_EXPORT_FIELDS` contract contains 27 fields.

```bash
scrapy crawl dollartree_listing -a category=food-candy-drinks -a max_pages=2 -s HTTPCACHE_ENABLED=False -O dollartree.jsonl
```

### tripcom_listing

`tripcom_listing` reads the server-provided `data-jsondata` state for Trip.com's
`City` template component. This is a single bootstrap direction: it does not parse
rendered hotel cards or JSON-LD. The 20 deterministic city categories come from
Trip.com's popular-hotel destination links. Each city SEO page is fetched once;
the component supplies hotel names, prices, price units, and city metadata.

Every exported item includes the verbatim `raw` City-bootstrap hotel record and a
per-run crawl `timestamp`.

```bash
scrapy crawl tripcom_listing -a category=bangkok -s HTTPCACHE_ENABLED=False -O tripcom.jsonl
```

### hobbylobby_listing

`hobbylobby_listing` reads the server-rendered Algolia InstantSearch bootstrap
embedded in Hobby Lobby category pages. This is the spider's only product-data
direction: there is no product-card HTML or JSON-LD fallback. The bootstrap
supplies full product records plus `nbHits`, `nbPages`, and `hitsPerPage`, so the
same state drives `?page=N` pagination and its stop condition.

The 20 stable level-2 category seeds in `hobbylobby_categories.py` cover art,
beads, seasonal, crafts, fabric, floral, home decor, kitchen, party, scrapbook,
and yarn departments. Custom `category_url` and `url` targets are also supported.
Every item includes the verbatim Algolia hit as `raw`, the source page, and a
per-run `timestamp`; the ordered `FEED_EXPORT_FIELDS` contract contains 60 fields.

```bash
scrapy crawl hobbylobby_listing -a category=art-supplies-painting-supplies -a max_pages=2 -s HTTPCACHE_ENABLED=False -O hobbylobby.jsonl
```

### barnesandnoble_listing

`barnesandnoble_listing` reads Barnes & Noble's rotating Shopify domain, API
version, and public Storefront token from the selected collection shell, then
uses the first-party Storefront GraphQL API exclusively for products and cursor
pagination. It exports product, price-range, image, option, and variant data in
the spider's ordered 32-field `FEED_EXPORT_FIELDS` contract. Direct connections
are used because both storefront hosts are reachable without anti-bot handling.

```bash
scrapy crawl barnesandnoble_listing -a category=fiction -a max_pages=2 -s HTTPCACHE_ENABLED=False -O barnesandnoble.jsonl
```

Verified live on 2026-10-08: 100 unique products across two API pages (50 per
page), with all three responses returning HTTP 200.

## Available spiders

### Standalone spiders (via `scrapy crawl <spider>`)

These live under `common/spiders/*_listing_spider.py` and are purpose-built per retailer.

Working spiders running daily in production:

| Spider Name | Status | Method | Antibot | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|---|
| [`decathlon_listing`](#decathlon_listing) | Active | API | none detected direct; compatible with plain ScrapeOps US proxy | Decathlon products from Shopify's first-party collection JSON API only; no HTML, embedded-metadata, or JSON-LD fallback. | Up to 250/API page | Top 20 primary-nav collections ranked by product count | `{"category":"camp-hike","item_id":"8209731190846","title":"Simond Men’s Xplore Hooded Down Jacket","price":119.0,"currency":"USD","source":"decathlon_shopify_collection_api"...}` |
| [`dollartree_listing`](#dollartree_listing) | Active | API | none detected direct | Dollar Tree products from the first-party Oracle Commerce Cloud guided-search API only; no HTML or JSON-LD fallback. | 24/page | Top 20 categories ranked by live product count | `{"category":"food-candy-drinks","item_id":"354662","title":"Lil' Dutch Maid Duplex Crème Cookies.","price":1.25,"currency":"USD","source":"dollartree_occ_guided_search_api"...}` |
| [`etsy_listing`](#etsy_listing) | Active | html | ScrapeOps US proxy | Etsy products from the server-rendered category document: the `ld+json` `ItemList` plus listing-card markup; the async Neu Spec API is not extractable anonymously (its `public` route returns an empty `output` and the client's results path is an authenticated `member` POST). | 60/page | 20 primary Etsy categories | `{"category":"jewelry","item_id":"1806011672","title":"Baguette Birthstone Necklace, Family Birthstone Necklace, Personalized Gift","price":32.8,"currency":"USD","source":"etsy_itemlist_jsonld"...}` |
| [`barnesandnoble_listing`](#barnesandnoble_listing) | Active | API | none detected | Barnes & Noble products from the first-party Shopify Storefront GraphQL API. The collection page only supplies rotating API configuration; there is no HTML-card or JSON-LD product fallback. | 50/page | 20 stable collection seeds | `{"category":"fiction","item_id":"8827283734769","ean":"9780765635969","title":"Projecting Politics: Political Messages in American Films","format":"Hardcover","price":237.61,"currency":"USD","source":"barnesandnoble_storefront_graphql_api"...}` |
| [`hobbylobby_listing`](#hobbylobby_listing) | Experimental | bootstrap | ScrapeOps US proxy | Hobby Lobby products from the server-rendered Algolia InstantSearch state only; no direct HTML-card or JSON-LD extraction. | 12/page | 20 product-bearing level-2 categories | `{"category":"art-supplies-painting-supplies","item_id":"80968391","title":"Master's Touch Oil Paint - 12 Piece Set","price":6.99,"source":"hobbylobby_instantsearch_bootstrap"...}` |
| [`tripcom_listing`](#tripcom_listing) | Experimental | bootstrap | ScrapeOps proxy | Trip.com hotels from the server-provided `City` template-component state; no direct HTML-card or JSON-LD extraction. | 9 (one city page) | 20 popular hotel destinations | `{"category":"bangkok","title":"NASA BANGKOK - Airport Rail Link Ramkhamhang","price":15,"currency":"USD","source":"tripcom_city_component_bootstrap"...}` |
| [`hostelworld_listing`](#hostelworld_listing) | Active | api | none detected; API must be direct so proxy does not rewrite `Accept` | Hostelworld properties from the first-party Apigee city-properties API only; no HTML or JSON-LD fallback. | 29 (New York, one page) | 20 popular global cities; 2,838 city URLs available from the sitemap index | `{"category":"new-york","item_id":"1850","name":"HI New York City Hostel","source":"hostelworld_city_properties_api"...}` |
| [`dell_listing`](#dell_listing) | Experimental | bootstrap | ScrapeOps proxy | Dell US listings from the authoritative `data-product-detail-info` Product Stack bootstrap; no product-card or JSON-LD fallback. | Live smoke tested below | 18 stable product/deal categories | `{"item_id":"dellplus16laptopdb16250","title":"Dell 16 Plus Laptop","price":1559.99,"currency":"USD","source":"dell_product_stack_bootstrap"...}` |
| [`dollargeneral_listing`](#dollargeneral_listing) | Active | api | ScrapeOps proxy (`keep_headers=true`) | Dollar General category listings from the first-party Omni v5 product-search API; no HTML-card or JSON-LD fallback. | 24 per API page | 20 high-coverage departments | `{"item_id":"37000853794","title":"Crest Plus Scope Whitening Toothpaste...","price":8.25,"currency":"USD","source":"dollargeneral_omni_search_api"...}` |
| [`agoda_listing`](#agoda_listing) | Experimental | api | proxy required | Agoda curated destination accommodations from the first-party Cronos geo API. | 30 (Bali, one API response) | 20 popular cities from the homepage destination payload | `{"category":"bali","item_id":"489045","title":"RIMBA by AYANA Bali","review_score":9.1,"star_rating":5.0,"source":"agoda_cronos_geo_api","timestamp":"2026-10-06 10:30:00"...}` |
| [`adorama_listing`](#adorama_listing) | Active | bootstrap (Next.js `__NEXT_DATA__`) | DataDome | Adorama category listings from server-rendered Next.js hydration state. | 24 (one page; 48 across 2 pages) | 1,079 crawlable categories across 11 departments from `adorama_categories.py` | `{"category":"cameras","item_id":"KKRK0603A","title":"Kodak Charmera Millenium Edition...","price":54.94,"currency":"USD"...}` |
| [`amazon_listing`](#amazon_listing-category) | Active | html | none detected | Amazon category listing spider (category shortcuts). | 22 (ok) | electronics, fashion, beauty, home-kitchen, toys-games, sports-outdoors, grocery, books | `{"asin":"B0DKDTBBF7","title":"2 Packs Electric Candle Lighters, Windproof Flameless USB Rechargeable Plasma Arc Long Lighter for Grill Fi...` |
| [`amazon_search`](#amazon_search) | Active | html | none detected | Amazon keyword search spider. | 22 (ok) | - | `{"asin":"B0GHQRV71M","title":"16\" FHD IPS Laptop Computer - 16GB RAM 512GB SSD, Pentium N100(Beat to i3-1115G4, 4 Cores Up to 3.4GHz), B...` |
| [`acehardware_listing`](#acehardware_listing) | Active | bootstrap | ScrapeOps residential + `bypass=5` required | Ace Hardware category listings and recursive department discovery from server-rendered Kibo/Mozu hydration. | 60 (2 pages, cordless-drills) | 20 department/category seeds from `acehardware_categories.py`; department pages recursively discover product-bearing leaves | `{"category":"cordless-drills","item_id":"2385458","title":"DeWalt 20V MAX 1/2 in. Brushed Cordless Compact Drill Kit (Battery & Charger)","brand":"DeWalt","price":179.0,"currency":"USD","source":"acehardware_mozu_hydration",...}` |
| [`backcountry_listing`](#backcountry_listing) | Active | bootstrap | AWS WAF (datacenter + `bypass=5` both return the challenge; `residential=true` required) | Backcountry.com category/collection/brand listings from the server-rendered Next.js `#__NEXT_DATA__` PLP payload joined to `__APOLLO_STATE__`. | 84 (2 pages, `cat-mens-shirts`); 52 (`rc-mens-parkas`, natural last page) | 398 unique targets across 14 top-level menus / 110 sections from `backcountry_categories.py` | `{"category":"cat-mens-shirts","department":"Men","section":"Clothing","item_id":"FJRZ133","title":"Fjallglim Regular Shirt - Men's","brand":"Fjallraven","price":124.95,"original_price":null,"currency":"USD","in_stock":true,"source":"backcountry_next_data",...}` |
| [`landwatch_listing`](#landwatch_listing) | Active | bootstrap | Akamai; ScrapeOps US residential required | LandWatch property listings from the authoritative server-rendered `#__SERVER_STATE__.searchPage.searchResults.propertyResults` payload only; no HTML-card or JSON-LD fallback. | 25/page | 20 high-inventory US state markets | `{"category":"texas","item_id":"427783557","title":"Superior Views, Better Hunting","price":769950,"acres":108.1,"source":"landwatch_server_state_bootstrap",...}` |
| [`realtor_listing`](#realtor_listing) | Active | bootstrap | residential ScrapeOps + `bypass=5` required | Realtor.com sale listings from authoritative React Router streamed SSR loader state. | 42/page | 20 major US city markets from `realtor_categories.py` | `{"item_id":"9573322873","listing_id":"2994590506","title":"11201 Chalon Rd, Los Angeles, CA 90049","price":400000000,"source":"realtor_react_router_stream",...}` |
| [`zillow_listing`](#zillow_listing) | Active | bootstrap | PerimeterX | Zillow sale listings from server-rendered Next.js `__NEXT_DATA__`, including path-based SSR pagination. | 82 (2 pages, `houston-tx`) | 20 major US city markets | `{"item_id":"55476612","title":"8323 Gentlewood Ct, Houston, TX 77095","price":375000,"beds":4,"baths":3,"area":2992,"source":"zillow_next_data"}` |
| [`loopnet_listing`](#loopnet_listing) | Experimental | api | ScrapeOps US proxy | Commercial-property records from LoopNet's first-party `/services/search` JSON service and its API-delivered placard payload, initialized from the page's search-criteria bootstrap; no listing-page or JSON-LD fallback. | Live smoke tested below | 20 sale/lease property-type searches | `{"item_id":"42148644","title":"THE GARAGE Luxury Condos","source":"loopnet_search_api"...}` |
| [`rent_listing`](#rent_listing) | Active | bootstrap | ScrapeOps US proxy | Rent.com apartment listings from authoritative server-rendered Next.js `__NEXT_DATA__`, with `/page-N` pagination and no fallback. | 30/page | 20 major US rental markets | `{"category":"los-angeles-ca","item_id":"lc6732384","title":"El Conquistador","price_min":1664,"source":"rent_next_data"...}` |
| [`apartments_listing`](#apartments_listing) | Experimental | bootstrap | ScrapeOps US proxy | Apartments.com rental map inventory from authoritative server-rendered `window.aptsState`; no HTML-card or JSON-LD fallback. | 567 unique listings in captured New York page 1 state | 20 major US rental markets | `{"category":"new-york-ny","item_id":"1j2c5h6","rent_min":5075,"latitude":40.7766,"source":"apartments_apts_state_bootstrap"...}` |
| [`hilton_listing`](#hilton_listing) | Active | bootstrap | ScrapeOps US proxy | Hilton destination hotels from authoritative server-rendered Next.js `__NEXT_DATA__`; no HTML or JSON-LD fallback. | Up to 20 | 20 major US city markets | `{"category":"new-york-ny","item_id":"NYCTEPO","title":"Tempo by Hilton New York Times Square","source":"hilton_next_data"...}` |
| [`basspro_listing`](#basspro_listing) | Active | api | Akamai on the storefront legs (403 direct); the Coveo search leg must stay unproxied | Bass Pro Shops category listings from the storefront Coveo Headless search API (`platform.cloud.coveo.com/rest/search/v2`); taxonomy from the `__NEXT_DATA__.props.megaNavHtmlV2` mega-nav. | 96 (2 pages, rod-reel-combos) | 909 nav entries (11 departments / 116 level-2 / 782 level-3) | `{"category":"Fishing/Rod & Reel Combos","item_id":"3472884","title":"Bass Pro Shops Megacast Baitcast Combo","brand":"Bass Pro Shops","url":"https://www.basspro.com/p/bass-pro-shops-megacast-baitcast-combo","price":69.99,"availability":"InStock","source":"basspro_coveo"...}` |
| [`booking_listing`](#booking_listing) | Active | bootstrap | none detected (anonymous SSR cruise) | Booking.com listings for the 20 homepage-exposed US city destinations from the anonymous server-rendered Apollo cache (`ROOT_QUERY.lxAccommodations` -> `ROOT_QUERY.searchQueries.search().results`). | 33 (2 pages, `las-vegas`) | 20 US city destinations from `booking_categories.py` | `{"category":"las-vegas","item_id":"15743439","title":"The Platinum Hotel Las Vegas","price":227.91,"currency":"EUR","rating":9.1,"reviews_count":8,"city":"Las Vegas","source":"booking_apollo_hydration"...}` |
| [`marriott_listing`](#marriott_listing) | Active | bootstrap (Next.js `__NEXT_DATA__`) | ScrapeOps US residential proxy required | Marriott destination properties from the server-rendered `processedData.hotels` hydration collection, with `?pg=N` pagination and no fallback. | 12/page (`miami`) | 20 featured city destinations from `marriott_categories.py` | `{"category":"miami","item_id":"MIAJW","title":"JW Marriott Miami","rating":3.7,"reviews_count":1715,"source":"marriott_next_data_hydration"...}` |
| [`microcenter_listing`](#microcenter_listing) | Experimental | bootstrap | Cloudflare; configured US proxy required | Store-scoped Micro Center listings from structured server-rendered product-card state. | 24/page | 513 unique targets preserving 20 departments / 118 groups / 578 navigation contexts | `{"category":"processors-cpus","item_id":"706001","sku":"974659","title":"Ryzen 7 9850X3D...","brand":"AMD","price":459.99,"source":"microcenter_card_state_bootstrap"...}` |
| [`bestbuy_listing`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | unknown (timeout/no verdict) | Best Buy listing via direct HTTP + Apollo bootstrap extraction. | 10 (skipped2) | laptops, tvs, headphones, monitors, cell-phones | `{"item_id":"6572184","title":"Samsung - Galaxy Book4 15.6\" FHD Laptop - Intel Core 7- 16GB Memory - 512GB SSD - Silver","url":"https://www.bestbuy.com/product/samsung-galaxy-bo...` |
| [`backcountry_listing`](#backcountry_listing) | Active | bootstrap (Next.js `__NEXT_DATA__`) | AWS WAF (residential proxy: `scrapeops.country=us.residential=true`) | Backcountry category, `/rc/` collection and brand listings from the server-rendered PLP hydration state; taxonomy from the header `headerNavigation` mega-nav. | 42 (1 page) / 84 (2 pages) / 42 (`/rc/`) / 42 (brand) | 469 links (14 departments / 109 sections; 398 distinct URLs) from `backcountry_categories.py` | `{"item_id":"FJRZ133","title":"Fjallglim Regular Shirt - Men's","brand":"Fjallraven","price":124.95,"original_price":124.95,"currency":"USD","url":"https://www.backcountry.com/fjallraven-fjallglim-regular-shirt-mens","availability":"IN_STOCK","in_stock":true,"page":1,"source":"backcountry_next_data"...}` |
| [`bestbuy_search`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | unknown (timeout/no verdict) | Best Buy search via direct HTTP + Apollo bootstrap extraction. | 4 (skipped2) | - | `{"item_id":"6613879","title":"HP - 14\" Laptop - Intel Processor N150 2025 - 4GB Memory - 128GB UFS - Willow Green","url":"https://www.bestbuy.com/product/hp-14-laptop-intel-pro...` |
| [`macys_listing`](#macys_listing) | Active | api | Akamai | Macy’s listing via xapi endpoint (with fallback routing). | 60 (ok) | laptops, shoes, dresses, fragrance, bedding | `{"item_id":"17595303","title":"5Core AC Power Cord 6Ft 3 Prong US Male to Female Extension Adapter 18AWG 10A 7A 125V","brand":"5 Core","u...` |
| [`nordstrom_listing`](#nordstrom_listing) | Active | bootstrap + html | PerimeterX / HUMAN | Nordstrom listing parser; often blocked/changed. | 0 (timeout2) | women, men, kids, beauty, home, designer, sale | `{}` |
| [`sephora_listing`](#sephora_listing) | Active | api | Akamai | Sephora listing via `/api/v2/catalog/categories/<slug>/seo`. | 60 (ok) | makeup, skincare, gifts, fragrance | `{"item_id":"P517483","title":"Pocket Blush Buildable Hydrating Cream Blush","url":"https://www.sephora.com/product/pocket-blush-P517483?s...` |
| [`ulta_listing`](#ulta_listing-category) | Active | api | Akamai | Ulta category listing with dynamic GraphQL module discovery. | 152 (2 pages, proxy) | makeup, skin-care, hair-care, fragrance, body-care | `n/a` |
| [`ulta_search`](#ulta_search-keyword) | Active | api + html | Akamai | Ulta keyword search via GraphQL (with unsorted retry + HTML fallback). | 64 (ok) | - | `{"item_id":"xlsImpprod15511061","title":"All Soft Shampoo","source":"ulta_dxl_graphql"...}` |
| [`walmart_listing`](#walmart_listing-category) | Active | api + html | Akamai (+ PerimeterX/HUMAN signals) | Walmart category listing spider (direct API+HTML flow). | 45 (ok) | electronics, home, clothing, beauty, toys, sports-and-outdoors, grocery | `{"productId":"19231301884","usItemId":"19231301884","title":"No Boundaries Women's Faux Leather Loafers","brand":"No Boundaries"...` |
| [`walmart_search`](#walmart_search-keyword) | Active | api + html | Akamai (+ PerimeterX/HUMAN signals) | Walmart keyword search spider. | 12 (ok) | - | `{"item_id":"13542163431","title":"ASUS Vivobook Go 15.6” Laptop, Intel i3-N305, 8GB, 256GB, Windows 11 Home in S mode, Cool Silver, E1504...` |
| [`wayfair_listing`](#wayfair_listing) | Experimental | server-rendered HTML cards | none detected | Wayfair listing cards with semantic selectors and tracking metadata. | 1 (committed sofas fixture; no live crawl run) | 15 departments / 668 menu links; 577 verified listing targets | `{"item_id":"W117645758","title":"Boneless 96\" Sectional Couches...","price":399.99,...}` |
| [`ebay_listing`](#ebay_listing-category-marko-hydration-state) | Active | Marko + html | Akamai | Stable eBay category listing extraction from Marko hydration state, with HTML subcategory discovery. | 18 (Antiques fixture browse tiles) | 18 top-level groups / 209 subcategories from `ebay_categories.py` | `{"productId":"234346994063","title":"MacBook Pro 15 Inch 256GB SSD 16 GB i7 3.40Ghz Apple Retina Big Sur 3yr Warranty","price":439.0,"currency":"USD",...}` |
| [`ebay_search`](#ebay_search-keyword-marko-hydration-state) | Active | Marko | Akamai | Stable eBay keyword search extraction from Marko `ListingItemCard` hydration data. | 60 (ok) | - | `{"productId":"234346994063","title":"MacBook Pro 15 Inch 256GB SSD 16 GB i7 3.40Ghz Apple Retina Big Sur 3yr Warranty","price":439.0,"currency":"USD",...}` |

### landwatch_listing

LandWatch state-market pages expose complete property records in the authoritative
server-rendered `#__SERVER_STATE__` search bootstrap. The spider reads only
`searchPage.searchResults.propertyResults`, follows the bootstrap's `paginationData.nextLink`,
and does not fall back to placard HTML or JSON-LD. It exports stable listing/inventory IDs,
prices, acreage, property types, address and coordinates, house attributes, seller details,
media flags, pagination metadata, and the raw bootstrap record. The 20 state seeds are in
`common/spiders/landwatch_categories.py`.

LandWatch's Akamai edge requires the configured ScrapeOps US residential route. The spider
adds `residential=true` to a configured ScrapeOps proxy automatically:

```bash
scrapy crawl landwatch_listing -a category=texas -a max_pages=1 \
  -s HTTPCACHE_ENABLED=False -O landwatch-texas.jsonl
```

Verified 2026-10-08: HTTP 200, 25 unique properties from one uncached Texas page.

Spiders below are returning items in recent smoke runs:

| Spider Name | Status | Method | Antibot | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|---|
| [`academy_listing`](#academy_listing) | Active | api | PerimeterX (`scrapeops.country=us.bypass=5` needed for the API host) | Academy Sports + Outdoors category listings from the first-party `/api/category/v3/{categoryId}` catalog API; taxonomy captured from the global header `window.ASOData` component registry. | 96 (2 pages, hot-deals) | 228 unique categories from 12 departments | `{"category":"deals-clearance-hot-deals","item_id":"27288501","title":"YETI Camino Carryall 20 Tote Bag","brand":"YETI","price":140.0,"currency":"USD","vendor_name":"YETI HOLDINGS INC YETI COOLERS LLC","valued_cost":84.0,"color_images":{...},"deal_badges":"Hot Deal, New Colors","fulfillment_mode":"01 SELL ONLINE","source":"academy_category_api",...}` |
| [`adidas_listing`](#adidas_listing) | Experimental | Next.js hydration | Akamai (ScrapeOps 367 on plain route; `residential=true` worked) | adidas listings from server-rendered `__NEXT_DATA__` `props.pageProps.products`, paginated by `?start=`. | 96 (2 pages, proxy) | 25 sections / 196 categories from `adidas_categories.py` | `{"item_id":"KI8294","title":"ADIZERO ADIOS PRO 5 Running Shoes","brand":"Men Performance","price":275.0,"currency":"USD",...}` |
| [`ae_listing`](#ae_listing) | Experimental | FastBoot + API | Akamai (signals in headers) | American Eagle listing spider via FastBoot shoebox state and browse API pagination. | 30 (ok) | women, men, aerie | `{"item_id":"1457_2980_808","title":"AE Big Hug V-Neck Sweatshirt","url":"https://www.ae.com/us/en/p/women/hoodies-sweatshirts/crew-neck-sweatshirts/ae-big-hug-v-neck-sweatshirt/1457_2980_808","price":38.97...` |
| [`anthropologie_listing`](#anthropologie_listing) | Experimental | Pinia hydration | PerimeterX / HUMAN | Anthropologie listing spider using the server-rendered Pinia product state. | 37 (ok, proxy) | womens-clothing, dresses, shoes, sale and refinements | `{"item_id":"AN-4114086690121-000","title":"By Anthropologie Goldie 100% Cashmere Sweater","price":138.0,...}` |
| [`asos_listing`](#asos_listing) | Experimental | bootstrap + API | Akamai | ASOS US listings from `window.asos.plp._data`, with pagination through the hydrated search API contract. | 2 (fixture; live unverified) | complete women/men navigation inventory from `asos_categories.py` | `{"item_id":"211160390","title":"ASOS DESIGN stretch chiffon scarf detail plunge draped maxi dress in chocolate","price":69.99,"currency":"USD"...}` |
| [`bloomingdales_listing`](#bloomingdales_listing) | Experimental | html + nuxt-state | Akamai | Bloomingdale's listing spider via Nuxt SSR state contract parsing (splash->leaf aware). | 8 (ok) | new-now, women, beauty, shoes, handbags, jewelry-accessories, men, kids, home, sale, gifts, designers | `{"item_id":"5973765","title":"Tumbled Woven Verne Pants","url":"https://www.bloomingdales.com/shop/product/cinq-a-sept-tumbled-woven-vern...` |
| [`blick_listing`](#blick_listing) | Active | api | none detected (ScrapeOps US proxy; API needs `X-blick-portal: blick`) | Blick Art Materials category listings from the first-party `api.dickblick.com` product-search API; taxonomy captured from the `/categories/` Next.js hydration. | 84 (3 pages, acrylic-paint) | 899 crawlable categories across 17 departments from `blick_categories.py` | `{"category":"paint-and-mediums/acrylic-paint","item_id":"00711","title":"Blickrylic Student Acrylic Paints and Sets","brand":"Blick","price":7.45,"currency":"USD","source":"blick_product_search_api",...}` |
| [`cvs_listing`](#cvs_listing) | Active | bootstrap | none detected (ScrapeOps `country=us` route required) | CVS.com category listings from the inline `var productIndexData = {...}` SSR hydration assignment; taxonomy captured from `initialState.allCategories`. | 60 (3 pages, health-medicine) / 39 (2 pages, multivitamins) | 715 categories / 13 departments from `cvs_categories.py` | `{"category":"health-medicine","item_id":"702568","title":"Nature's Truth Melatonin 12mg & Magnesium Gummies, Sour Grape, 60 CT","brand":"Nature's Truth","price":21.99,"currency":"USD","in_stock":true,"stock_quantity":2052,"rating":null,"page":1,"source":"cvs_product_index_hydration"}` |
| [`costco_listing`](#costco_search--costco_listing) | Active | React Flight + API | Akamai | Costco category listing with React Flight discovery and GRS search pagination. | 24 (ok) | 131 parent groups / 432 subcategory entries from `costco-categories.json` | `{"item_id":"100501081","title":"Starbucks Pike Place Medium Roast K-Cup","url":"https://www.costco.com/starbucks-pike-place-medium-roast-k-cup-72-count.product.100501081.html","price":...` |
| [`containerstore_listing`](#containerstore_listing) | Active | bootstrap | none detected | Container Store category listings from the server-rendered Next.js `__NEXT_DATA__` hydration. | 120 (2 pages, proxy) | 14 departments / 189 L2 / 159 L3 nodes -> 295 unique catalogue URLs from `containerstore_categories.py` | `{"category":"Kitchen > Pantry Organizers","department":"Kitchen","subcategory":"Pantry Organizers","item_id":"11017102","sku_id":"10087168","title":"Everything Organizer Shelf-Depth Pantry Bin with Divider","price":9.19,"original_price":22.99,...` |
| [`shopbop_listing`](#shopbop_listing) | Active | bootstrap | none detected (ScrapeOps proxy) | Shopbop category listings from the server-rendered `window.__shopbop_sca_hydrate__` React Query hydration. | 200 (2 pages, proxy) | 3 groups / 20 primary / 335 nav nodes -> 266 unique category URLs from `shopbop_categories.py` | {"category":"Women > What's New","department":"Women","subcategory":"What's New","folder_id":"13198","item_id":"1560892247","sku_id":"AKNVA30171","title":"Kyla Faux Fur Coat","brand":"AKNVAS","price":1495.0,"currency":"USD","page":1,"offset":0,"source":"shopbop_sca_hydrate_products_query",...}` |
| [`dickssportinggoods_listing`](#dickssportinggoods_listing) | Active | api | Akamai | DICK'S Sporting Goods category listings from the first-party catalog product-search API. | 48 (ok) | 1287 unique categories from 10 departments | `{"item_id":"13286436","title":"adidas FIFA World Cup Historical Mini Soccer Ball Set","brand":"adidas","price":141.52,"currency":"USD",...}` |
| [`tractorsupply_listing`](#tractorsupply_listing) | Experimental | bootstrap | Akamai | Tractor Supply products from official sitemaps and PDP `__NEXT_DATA__`. | 24/page | 4 product sitemap shards | `{"item_id":"867","sku":"100001199","title":"Gorilla-Lift Trailer Tailgate Lift Assist","brand":"Gorilla-Lift",...}` |
| [`elfcosmetics_listing`](#elfcosmetics_listing) | Experimental | api + bootstrap + html | none detected (CloudFront CDN only) | e.l.f. Cosmetics multi-mode listing spider. | 6 (ok) | face, eyes, lips | `{'item_id':'300261','title':'Soft Glam Satin Concealer','url':'https://www.elfcosmetics.com/soft-glam-satin-concealer/300262.html','price':9.0,'brand':'e.l.f. Cosmetics','source':'elfcosmetics_preloaded_state'...}` |
| [`fashionnova_listing`](#fashionnova_listing) | Active | api + html | Cloudflare | Fashion Nova listing via Shopify Storefront GraphQL with HTML fallback. | 48 (ok) | women, new, dresses, jeans, sale | `{"item_id":"175898317","title":"Classic High Waist Skinny Jeans - Dark Denim","url":"https://www.fashionnova.com/products/dark-blue-class...` |
| [`nike_listing`](#nike_listing) | Active | api | none detected (ScrapeOps proxy; keep_headers) | Nike product wall via `__NEXT_DATA__` hydration + `api.nike.com` product-wall API pagination (no HTML fallback). | 239 (page 1, proxy) | 168 unique URLs across 6 departments from `nike_categories.py` | `{"category":"mens-shoes-nik1zy7ok","item_id":"IX3952-600","title":"Nike Moon Shoe OG","price":105,"currency":"USD","source":"nike_next_data"...` |
| [`gamestop_listing`](#gamestop_listing) | Active | api | none detected (ScrapeOps proxy) | GameStop SFCC Demandware listing via the `Tile-GetProductsJSON` controller (no HTML fallback). | 139 (3 pages, proxy) | 119 URLs across 33 category groups from `gamestop_categories.py` | `{"category":"consoles-hardware","item_id":"106429","title":"Nintendo Wii Original Console with Wii Remote - Super Mario Bros. 25th Anniversary Edition Red","price":"139.99","availability":"InStock","source":"gamestop_tile_json"...` |
| [`getyourguide_listing`](#getyourguide_listing) | Active | bootstrap | none detected through ScrapeOps proxy | GetYourGuide destination activity shelves from server-rendered `window.__INITIAL_STATE__.sdui` hydration (no HTML or JSON-LD fallback). | 24 (one bounded shelf, live proxy) | 20 destination countries from `getyourguide_categories.py` | `{"category":"argentina","item_id":1220349,"title":"El Calafate: Perito Moreno Glacier Boat Tour with Guide","starting_price":50,"currency":"USD","source":"getyourguide_initial_state_sdui"...}` |
| [`autozone_listing`](#autozone_listing) | Active | bootstrap (Next.js React Query hydration) | ScrapeOps residential proxy required (`residential=true.country=us`) | AutoZone category listings from server-rendered Next.js/TanStack React Query bootstrap state (`productshelf-results` joined to `productSkuDetails` by SKU). | 24 (one page, oil-filter) | 20 stable category seeds | `{"category":"oil-filter","item_id":"1117175","title":"STP Oil Filter S45023","brand":"STP","price":5.99,"currency":"USD","source":"autozone_next_data"...}` |
| [`viator_listing`](#viator_listing) | Active | bootstrap | none detected through ScrapeOps proxy | Viator destination activity shelves from server-rendered `__PRELOADED_DATA__.pageModel.topActivities` hydration (no HTML or JSON-LD fallback). | 15 (one bounded shelf, live proxy) | 20 Popular Cities from `viator_categories.py` | `{"category":"nashville","item_id":"361513P2","title":"LUXURY 5-Star PRIVATE Nashville Party Tour w/ Panoramic Views","price":395,"currency":"USD","source":"viator_preloaded_top_activities"...}` |
| [`footlocker_listing`](#footlocker_listing) | Active | api | residential proxy (ScrapeOps) | Foot Locker category listings from the ZGW search API (residential proxy required). | 48 (1 page, residential proxy) | Dynamically resolved from `header.public.json` | `{"band":"Men's","sub_category":"Shoes","category":"all-men-s-shoes","item_id":"T8013103","title":"Jordan Retro 12 - Men's","url":"https://www.footlocker.com/product/T8013103.html","image_url":"https://images.footlocker.com/is/image/EBFL2/T8013103","price":215.0,"original_price":215.0,"currency":"USD","availability":"InStock","brand":"Jordan","rating":5.0,"reviews_count":999,"page":1,"category_url":"/category/mens/shoes.html","source":"footlocker_api"...` |
| [`homedepot_listing`](#homedepot_listing-category-apollo-state) | Flaky | bootstrap | Akamai | Home Depot department listings from embedded Apollo state. | 2 (fixture) | appliances, bath, building-materials, decor-and-furniture, electrical, flooring, hardware, heating-and-cooling, kitchen, lawn-and-garden, lighting, paint, plumbing, storage, tools | `{"category":"tools","item_id":"100000001","sku":"1000000001","title":"16 oz. Fiberglass Claw Hammer","brand":"Husky","price":14.97...` |
| [`hm_listing`](#hm_listing) | Experimental | bootstrap (Next.js `__NEXT_DATA__`) | Akamai | H&M US product listings from authoritative server-rendered PLP hydration, with hydrated pagination. | 60/page | Women, Men, Kids, Home, Beauty new arrivals | `{"category":"women-new-arrivals","item_id":"1345672001","title":"Scarf-Detail Jacket","price":59.99,"currency":"USD","source":"hm_next_data"}` |
| [`homedepot_search`](#homedepot_search-keyword-apollo-bootstrap) | Active | bootstrap + html | Akamai | Home Depot keyword search via Apollo state. | 24 (ok) | - | `{"item_id":"336787835","sku":"1014334650","brand":"Lukyamzn","title":"14 in. Dual-Core Celeron N4000 Laptop 6 GB RAM 128 GB SSD IPS Displ...` |
| [`jcpenney_listing`](#jcpenney_listing) | Active | api | Akamai (+ reCAPTCHA scripts observed) | JCPenney listing spider via search API bootstrap endpoint. | 48 (ok) | womens_tops, mens_shirts | `{"item_id":"ppr5008584232","title":"St. John's Bay Womens Boat Neck Elbow Sleeve T-Shirt","brand":"st. john's bay","url":"https://www.jcp...` |
| [`ikea_listing`](#ikea_listing) | Active | api + html | none detected | IKEA category listings from the SIK search API, with a server-rendered HTML fallback. | 46 (api, ok) / 24 (html, ok) | 221 unique targets from 23 departments | `{"category":"st004","item_id":"50561244","title":"STORKLINTA","product_type":"6-drawer dresser","price":279.99,"department":"Storage & organization",...}` |
| [`iherb_listing`](#iherb_listing) | Active | api | PerimeterX on storefront; catalog API works through ScrapeOps US proxy | iHerb category listings from the first-party catalog product API (single API direction; no HTML or JSON-LD fallback). | 100 (2 pages, magnesium) | 380 unique category URLs across 9 departments from `iherb_categories.py` | `{"category":"magnesium","item_id":"103273","title":"California Gold Nutrition, Magnesium Bisglycinate Chelate...","price":12.59,"currency":"USD","source":"iherb_catalog_api",...}` |
| [`kroger_listing`](#kroger_search--kroger_listing) | Active | Redux bootstrap | unknown (timeout/no verdict) | Kroger category listings from `window.__INITIAL_STATE__` search products. | 2 (fixture) | cereal, milk, eggs, bread, coffee, snacks | `{"category":"cereal","item_id":"0001111012345","title":"Kroger Toasted Oats Cereal","brand":"Kroger","price":3.99,...}` |
| [`klook_listing`](#klook_listing) | Active | API | none detected through ScrapeOps | Klook activities from the first-party destination recommendation API discovered in `window.__KLOOK__` hydration. | 12 (Japan, one curated response) | 20 popular country/city destinations | `{"item_id":"46604","title":"Universal Studios Japan Studio Pass","currency":"HKD","source":"klook_destination_api",...}` |
| [`kroger_search`](#kroger_search--kroger_listing) | Active | bootstrap + html | unknown (timeout/no verdict) | Kroger keyword search with state extraction + fallback. | 27 (ok) | - | `{'item_id':'kroger-2-reduced-fat-milk-gallon','url':'https://www.kroger.com/p/kroger-2-reduced-fat-milk-gallon/0001111041700','source':'kroger_html_links_fallback'}` |
| [`levis_listing`](#levis_listing) | Active | bootstrap | none detected through proxy | Levi's listings from SSR `__LSCO_INITIAL_STATE__.ssrViewStoreProductList`. | 48 (2 pages, live proxy) | 5 sections / 83 PLP targets from `levi_categories.py` | `{"category":"shop-all-men-s-jeans","item_id":"005053473","title":"505™ Regular Dobby Men's Jeans","brand":"Levi's","price":64.99...` |
| [`lululemon_listing`](#lululemon_listing) | Active | bootstrap | Akamai | lululemon listing spider via Next.js `__NEXT_DATA__`. | 40 (ok) | women-shorts, women-leggings, men-shorts, bags | `{"category":"women-shorts","product_id":"prod11860112","name":"Shake It Out High-Rise Running Short 2.5\"","brand":"lululemon","price":["...` |
| [`newegg_listing`](#newegg_listing) | Experimental | SSR hydration state | none detected | Newegg listing spider reading server-rendered `window.__initialState__.Products` with `/Page-N` pagination and live RolloverMenu inventory refresh. | 36 (ok) | desktop-cpu-processors, all-current-categories | `{"item_id":"19-113-877","title":"AMD Ryzen 7 9800X3D - Ryzen 7 9000 Series Zen 5 8-Core 5.2 GHz - Socket AM5 120W - AMD Radeon Graphics Desktop Processor - 100-100001084WOF","model":"100-100001084WOF","brand":"AMD","price":469,"currency":"USD","url":"https://www.newegg.com/amd-ryzen-7-9000-series-ryzen-7-9800x3d-granite-ridge-zen-5-socket-am5-desktop-cpu-processor/p/N82E16819113877","image":"https://c1.neweggimages.com/ProductImageOriginal/19-113-877-01.png","rating":4.8,"reviews_count":729,"page":1,"source":"newegg_initial_state"}` |
| [`redfin_listing`](#redfin_listing) | Active | api | ScrapeOps US proxy | Redfin city listings from the first-party Stingray GIS JSON API discovered in React server hydration. | 350 (one page) | 20 major US city markets | `{"category":"los-angeles-ca","item_id":"5196541","price":1399000,"source":"redfin_stingray_api"...}` |
| [`movoto_listing`](#movoto_listing) | Experimental | bootstrap | PerimeterX (ScrapeOps US proxy required) | Movoto sale listings from server-rendered Nuxt `__INITIAL_STATE__.pageData.listings` only; no HTML or JSON-LD fallback. | 50 (one page, live proxy) | 20 major US city markets | `{"category":"new-york-ny","item_id":"aca725fa-4f79-41bc-a458-6de558312a3b","title":"50 W 66th St #10C New York, NY 10023","price":10950000,"source":"movoto_initial_state"...}` |
| [`oreilly_listing`](#oreilly_listing) | Active | bootstrap (`window._ost`) | direct 403; ScrapeOps US residential required | O'Reilly Auto Parts category listings from the server-rendered product bootstrap only. | 18 (live brake rotors page) | 34 root departments from `oreilly_categories.py`; direct leaf URLs supported | `{"item_id":"BBR|3512RGS","title":"BrakeBest Select Front Brake Rotor - 3512RGS","price":89.99,"currency":"USD","source":"oreilly_ost_bootstrap"}` |
| [`rei_listing`](#rei_listing) | Active | bootstrap (`#initial-props`) | none detected | REI category listings from the server-rendered `#initial-props` bootstrap (`ProductSearch.products.searchResults.results`); follows hydration pagination and dedupes by `prodId`. | 30 (1 page, hiking-footwear) | 20 stable commerce-category shortcuts from `rei_categories.py` | `{"category":"hiking-footwear","item_id":"202126","title":"Moab 3 Hiking Shoes - Women's","brand":"Merrell","price":71.83,"currency":"USD","source":"rei_initial_props_bootstrap","timestamp":"2026-10-06 20:34:00"}` |
| [`trulia_listing`](#trulia_listing) | Experimental | bootstrap | challenge/WAF | Trulia sale listings from server-rendered Next.js `props.searchData.homes`. | 40 (live) | 20 homepage-highlighted US cities | `{"item_id":"465800506","title":"97 Marland Rd, Colorado Springs, CO 80906","price":2500000,"currency":"USD"}` |
| [`llbean_listing`](#llbean_listing) | Active | api | none detected (ScrapeOps `country=us` route required) | L.L.Bean listing via the UDAL `product-discovery` JSON endpoint (no HTML fallback). | 96 (2 pages, proxy) | 11 departments / 500 targets from `llbean_categories.py` | `{"category":"Gift Shop","item_id":"1000316302","sku_id":"1000316302","title":"Women's The Original Double L® Sweater, Crewneck","brand":"L.L.Bean","price":49.99,"original_price":69.95,"currency":"USD","rating":4.4,"reviews_count":359,"color":"Classic Navy","size":"X-Small","availability":"IN","on_sale":true,"page":1,"position":1,"total_count":626,"source":"llbean_udal_product_discovery"...` |
| [`maccosmetics_listing`](#maccosmetics_listing) | Experimental | api + bootstrap + html | Akamai | MAC Cosmetics multi-mode listing spider. | 66 (ok) | face, lips, eyes | `{"item_id":"13854","title":"4.8/5 ( 452 ) Lustreglass Sheer-Shine Lipstick Sheer Coverage, Glossy/High-Shine Finish, Infused With Raspberry Seed/Organic Extra Virgin Olive Oils ...` |
| [`officedepot_listing`](#officedepot_listing) | Active | bootstrap | none detected (ScrapeOps proxy) | Office Depot / OfficeMax category listings from inline `window.ODSEARCHBROWSE_INITIAL_STATE` SSR hydration; taxonomy resolved from the header mega-menu JSON. | 59 (2 pages, furniture) | 388 browse PLPs from `header-menu-excel/products.json` | `{"department":"Furniture","item_id":"9003237","title":"Serta® Smart Layers™ Brinkley Ergonomic Bonded Leather High-Back Executive Office Chair, Black/Silver","price":299.99,"availability":"InStock","source":"officedepot_bootstrap"...}`
| [`orientaltrading_listing`](#orientaltrading_listing) | Active | API | none detected (ScrapeOps US proxy) | Oriental Trading category products from the first-party `/web/browse/productQuickView` endpoint only; listing HTML is used solely to discover API URLs and pagination. | 5 (bounded live smoke run) | 20 stable top-level shopping categories | `{"item_id":"13913005","title":"Bulk Value Candy Assortment - 30 lb, 3000 pc","price":169.98,"currency":"USD","source":"orientaltrading_quick_view_api"...}` |
| [`petsmart_listing`](#petsmart_listing) | Active | api | none detected (Akamai sensor served, API open; no proxy needed) | PetSmart category listings from the first-party `/api/search/1/indexes/<replica>/query` endpoint the storefront's Algolia client is pinned to. | 200 (2 pages x 100, ok) | 491 category paths / 7 departments from `petsmart_categories.py` | `{"category":"dog/food/dry-food","item_id":"5252900","title":"Purina Pro Plan Sensitive Skin and Stomach Dry Dog Food Adult Salmon & Rice Formula Digestive Health","brand":"Purina Pro Plan","price":77.99,"currency":"USD","rating":4.5,"reviews_count":9118,"url":"https://www.petsmart.com/dog/food/dry-food/purina-pro-plan-...-36648.html",...}` |
| [`michaels_listing`](#michaels_listing) | Experimental | Next.js RSC hydration | none detected (Akamai fronted; no challenge observed) | Michaels listings from the server-rendered React Server Component payload (`self.__next_f` -> `initialProducts`), paginated by `?page=`. | 40 (1 page, live proxy; page 2 blocked by a local 407 on CONNECT) | 3,611 categories under 33 departments from `sitemap_MIK_category.xml` | `{"category":"home-decor-floral-arrangements","item_id":"10809872","title":"11\" Pink Peony & Cream Rose Mix Bouquet by Ashland®","brand":"Michaels","price":9.99,"rating":4.5...` |
| [`vinted_listing`](#vinted_listing) | Active | bootstrap (Next.js RSC) | none detected (ScrapeOps proxy convention) | Vinted catalog listings exclusively from server-rendered `self.__next_f` catalog state; no HTML-card or JSON-LD fallback. | 96/page | 20 high-coverage catalog seeds from `vinted_categories.py` | `{"category":"home","item_id":"10287111268","title":"Chocolate drink maker","brand":"Hersey","condition":"New without tags","price":5,"currency":"USD","source":"vinted_nextjs_rsc_catalog_items"}` |
| [`poshmark_listing`](#poshmark_listing) | Experimental | bootstrap | none detected | Poshmark listing spider via `window.__INITIAL_STATE__` category grid data. | 48 (ok) | women, men, kids, home, electronics, pets | `{"category":"women","item_id":"6989d90ac4e7b4d4de556bac","title":"🔥Stunning  Farm Rio NWT Size Large Tropical Midi Dress with Sleeves – V...` |
| [`qvc_listing`](#qvc_listing) | Experimental | html + bootstrap | Akamai | QVC listing spider via server-rendered gallery cards and `utag_data` page state. | 96 (Beauty proxy capture) | fashion | `{"category":"beauty","category_id":"NAV6285","item_id":"A740517","title":"Whish 12 Days of Beauty Whishes Advent Calendar","price":59.98,...}` |
| [`zappos_listing`](#zappos_listing) | Experimental | Redux hydration | none detected through proxy | Zappos listings from `window.__INITIAL_STATE__.products.list`. | 100 (one-page proxy smoke) | 4 departments / 50 targets | `{"item_id":"8910671","title":"Kiruna Padded Parka","brand":"Fjällräven","price":300.0,...}` |
| [`zara_listing`](#zara_listing) | Active | api | Akamai (ScrapeOps `country=us,bypass=5`) | Zara US listings from the first-party category and product JSON APIs; no HTML or JSON-LD fallback. | 637 (Dresses; one API response) | 912 live product categories across 8 menu sections | `{"category":"WOMAN > COLLECTION > DRESSES","item_id":"560058525","title":"STRIPED PUFF SLEEVE MINI DRESS","price":69.9,"currency":"USD","source":"zara_api"...}` |
| [`saksfifthavenue_listing`](#saksfifthavenue_listing-category) | Experimental | html | DataDome | Saks Fifth Avenue listing spider via direct category HTML cards. | 24 (ok) | women, men, shoes, beauty, handbags | `{"item_id":"0400026449047","title":"Prada Washed Re Nylon Rain Jacket","url":"https://www.saksfifthavenue.com/product/prada-washed-re-nyl...` |
| [`sallybeauty_listing`](#sallybeauty_listing) | Experimental | html + AJAX | PerimeterX / HUMAN (px-captcha signals) | Sally Beauty SFCC product-grid spider with `Search-UpdateGrid` pagination. | 2 (fixture) | hair-color, hair-care, textured-curly-hair, hair-extensions, tools-brushes, nails, cosmetics-skin-care, fragrances, mens-grooming, salon-supplies, new, deals | `{"category":"hair-care","item_id":"SBS-539230","title":"Low Porosity Aloe Vera Gel Shampoo","brand":"Texture ID","price":11.99...` |
| [`belk_listing`](#belk_listing) | Experimental | api | none detected (first-party JSON) | Belk listings from the `/ecom/cio/v1/web/category/{path}?v2=true` search facade. | 60 (one page, ok) | 13 departments / 427 browse categories from `belk_categories.py` | `{"item_id":"2900965MULANEYW","title":"Mulaney Flats","brand":"DV Dolce Vita","price":45.5,"original_price":65.0,"discount_percent":30.0,"currency":"USD"...}` |
| [`stockx_listing`](#stockx_listing) | Experimental | bootstrap + html | Cloudflare | StockX listing via `__NEXT_DATA__` bootstrap. | 41 (ok) | sneakers, apparel, electronics, trading-cards, collectibles | `{"item_id":"brands","title":"Brands","url":"https://stockx.com/brands","price":null,"currency":null}` |
| [`urbanoutfitters_listing`](#urbanoutfitters_listing) | Active | bootstrap | none detected through ScrapeOps proxy | Urban Outfitters listings from double-decoded Vue/Pinia SSR state (`#urbnInitialPiniaState`), with `?page=` pagination and no HTML fallback. | 144 (2 pages, live proxy) | 2,158 sitemap PLPs plus 4 navigation roots absent from the sitemap (2,162 targets total) | `{"category":"new-arrivals","item_id":"UO-106663735-000","title":"Kimchi Blue Ella Flyaway Ruffle Lace Trim Cami","brand":"Kimchi Blue","price":39,"rating":4.7308,"reviews_count":26,"color":"Maroon","source":"urbanoutfitters_pinia_ssr_tiles"...}` |
| [`staples_listing`](#staples_listing) | Experimental | Next.js hydration | Akamai | Staples category listings from server-rendered `__NEXT_DATA__`. | 40 (one page) | 34 roots / 208 subcategories from `staples_categories.py` | `{"item_id":"82656","title":"Staples 1\" 3-Ring View Binder...","price":10.09,"currency":"USD"...}` |
| [`rightmove_listing`](#rightmove_listing) | Experimental | bootstrap | none detected through ScrapeOps proxy | Rightmove properties for sale from server-rendered Next.js Pages Router `__NEXT_DATA__` hydration (no HTML or JSON-LD fallback). | 25 (one page, live proxy) | 20 high-inventory UK cities | `{"category":"london","item_id":"89825950","title":"Tottenham Street, Fitzrovia, W1","price":680000,"price_currency":"GBP","source":"rightmove_next_data"...}` |
| [`petco_listing`](#petco_listing) | Experimental | bootstrap (Next.js `__NEXT_DATA__`) | none detected | Petco category listings from the server-rendered Constructor.io search hydration. | 48 (one page) | 22 roots / 286 nodes / 264 `-a category=` entries from `petco_categories.py` | `{"item_id":"6848523","title":"Purina Cat Chow Indoor Healthy Weight and Hairball with Chicken Dry Cat Food, 15 lbs.","brand":"Purina Cat Chow","price":18.99,"original_price":19.99,"rating":4.8141,"source":"petco_next_data"...}` |
| [`target_listing`](#target_listing) | Active (alias) | api | PerimeterX / HUMAN (cookie signals) | Deprecated alias of `target_search`. | 24 (ok) | - | `{"product_id":"90600286","name":"Women&#39;s Waffle Short Robe - Auden&#8482; Light Gray M/L: Front Tie, Long Sleeve","price":"$35.00","u...` |
| [`uniqlo_listing`](#uniqlo_listing) | Experimental | api | none detected (plain ScrapeOps datacenter route) | UNIQLO US category listings from the first-party commerce BFF products API. | 36 (one page, ok) | 2741 taxonomy URLs (4 genders / 46 classes / 212 categories / 2479 subcategories) from `uniqlo-categories.json` | `{"item_id":"E424873-000-00","title":"Crew Neck T-Shirt","color":"White","price":19.9,"currency":"USD"...}` |
| [`target_search`](#target_search) | Active | api | PerimeterX / HUMAN (cookie signals) | Target RedSky search API spider. | 24 (ok) | - | `{"product_id":"90600286","name":"Women&#39;s Waffle Short Robe - Auden&#8482; Light Gray M/L: Front Tie, Long Sleeve","price":"$35.00","u...` |
| [`victoriassecret_listing`](#victoriassecret_listing) | Active | api | none detected (ScrapeOps proxy, plain datacenter route) | Victoria's Secret / PINK listings from the first-party `stacks` JSON API; page 0 reads `collectionId` from SSR `clientProps`. | 192 (2 pages, live) | 427 targets across `vs` + `pink` brands from `victoriassecret_categories.py` | `{"category":"vs-bras","brand":"vs","item_id":"11295563|7I65","name":"Signature Shine Cotton Lightly Lined Balconette Bra","price":49.95,...}` |
| [`williams_sonoma_listing`](#williams_sonoma_listing) | Active | api | Akamai (not an issue for API) | Williams-Sonoma category listings via the Constructor.io browse API (taxonomy from the runtime category-tree API). | 100 (1 page, proxy) | ~3500 group_ids from the runtime category-tree API | `{"category":"cookware-sets","item_id":"greenpan-reserve-pro-ceramic-nonstick-10-piece-cookware-set","title":"GreenPan™ Reserve Pro Ceramic Nonstick 10-Piece Cookware Set","price":399.95,"currency":"USD","image_url":"https://assets.wsimgs.com/wsimgs/rk/images/dp/wcm/202631/0164/img2c.jpg","flags":["freeShip","more_colors"],"source":"williams_sonoma_constructor_browse"...` |
| [`harborfreight_listing`](#harborfreight_listing) | Active | bootstrap (`window.__APOLLO_STATE__`) | none detected | Harbor Freight category listings from the server-rendered Apollo hydration state; 17 deterministic department aliases and Magento `?p=N` pagination. | 36 (1 page, `Automotive`) | 17 department aliases from `harborfreight_categories.py` | `{"category":"Automotive","item_id":"64784","title":"3 Ton Low-Profile Professional Floor Jack with RAPID PUMP, Green","brand":"DAYTONA","price":199.99,"currency":"USD","source":"harborfreight_apollo_bootstrap"...}` |
| [`lowes_listing`](#lowes_listing) | Active | bootstrap (`window['__PRELOADED_STATE__']`) | Akamai (ScrapeOps residential + `bypass=5` required) | Lowe's category listings from the server-rendered `__PRELOADED_STATE__` bootstrap payload only; 16 stable category shortcuts with `?page=N` pagination. | 24 (1 page, `beverage-wine-chillers`) | 16 stable category shortcuts from `lowes_categories.py` | `{"category":"beverage-wine-chillers","item_id":"5017343139","title":"23.4-in W 20-Bottles Stainless Steel Dual Zone Cooling Built-in Indoor Wine Cooler","price":...,"source":"lowes_preloaded_state"...}` |
| [`bhphotovideo_listing`](#bh-photo-video-listing-spider) | Active | bootstrap (`bh-preloaded-data` / `ListingStore`) | ScrapeOps proxy | B&H Photo Video category listings from the server-rendered MobX `ListingStore` hydration; no HTML-card or JSON-LD fallback. | 28 (1 page, `Mirrorless Lenses`) | 13 listing leaves from `bhphotovideo_categories.py` | `{"category":"Mirrorless Lenses","product_id":2000025,"sku":"SO60063GM","title":"Sony FE 600mm f/6.3 GM OSS Lens (Sony E)","price":3698,"currency":"USD","source":"bootstrap","timestamp":"2026-10-07 00:38:12"...}` |
| [`vitacost_listing`](#vitacost_listing) | Active | api | none detected | Vitacost (Shopify + Boost AI Search) category listings from the first-party `services.mybcapps.com/bc-sf-filter/filter` JSON API; taxonomy from the `Categories` mega-menu. | 96 (2 pages, `category=Supplements`, page size 48) | 92 crawl targets / 90 unique collection URLs across 8 departments from `vitacost_categories.py` | `{"category":"Supplements","handle":"supplements","collection_id":"457575104827","item_id":"10390080782651","title":"Vitacost, Root2®, Turmeric Extract Curcumin C3 Complex®, 120 Capsules","brand":"Vitacost","price":24.74,"original_price":32.99,"discount_percentage":25.0,"source":"vitacost_boost_filter_api"...}` |
| [`hotpads_listing`](#hotpads_listing) | Active | bootstrap (Next.js RSC `initialListingsData`) | ScrapeOps proxy | HotPads rental-building listings from the server-rendered Next.js App Router RSC bootstrap; no rendered-card or JSON-LD fallback. | 40 (1 page, `new-york-ny`) | 20 major US rental markets from `hotpads_categories.py` | `{"category":"new-york-ny","item_id":"24cjp0b","title":"Sky Three","price_low":3675,"price_high":5575,"city":"Brooklyn","state":"NY","source":"hotpads_rsc_bootstrap","timestamp":"2026-10-07 02:36:00"...}` |
| [`tripadvisor_listing`](#tripadvisor_listing) | Active | bootstrap (URQL SSR cache) | ScrapeOps residential proxy | Tripadvisor hotels extracted only from the server-rendered URQL GraphQL cache; no card or JSON-LD fallback. | 37 (1 page, `bali`) | 20 Travelers' Choice destinations | `{"category":"bali","item_id":"24976303","title":"Kappa Senses Ubud","price":160.0,"currency":"USD","source":"tripadvisor_urql_bootstrap"...}` |
| [`homes_listing`](#homes_listing) | Active | bootstrap (`window.gState` map data) | ScrapeOps US proxy | Homes.com property markers from its printable-ASCII encoded search bootstrap; no placard HTML or JSON-LD fallback. | 638 (`new-york-ny`, live one-response crawl) | 20 major US city markets from `homes_categories.py` | `{"category":"new-york-ny","item_id":"4b215f8nkz79f","listing_key":"lfbykfb6tllzk","price":785000.0,"latitude":40.84279,"longitude":-73.82926,"source":"homes_gstate_map_bootstrap"...}` |
| [`remax_listing`](#remax_listing) | Active | bootstrap (Next.js App Router RSC) | ScrapeOps US proxy | RE/MAX homes for sale from the server-rendered `listingResultsUnfiltered` RSC bootstrap; no rendered-card or JSON-LD fallback. | 24/page | 20 populous US states from `remax_categories.py` | `{"category":"california","item_id":"M00000079-20262083","title":"7610 N LAKE BLVD # 29, TAHOE VISTA, CA 96148","price":299000,"beds":null,"baths":1,"source":"remax_nextjs_rsc_bootstrap"...}` |
| [`worldmarket_listing`](#worldmarket_listing) | Active | api | none detected (ScrapeOps proxy) | World Market products from the first-party SFCC `Search-UpdateGrid` grid API (no direct product-card or JSON-LD fallback). | 60 (1 page, live proxy) | 13 department seeds from `worldmarket_categories.py` | `{"category":"furniture-shop-all-furniture","item_id":"SET135122","title":"Isaiah Tufted Mid Century Seating Collection","price":299.99,"currency":"USD","source":"worldmarket_sfcc_search_update_grid_api"...}` |
| [`walgreens_listing`](#walgreens_listing) | Active | bootstrap (Redux `window.getInitialState()`) | Akamai (ScrapeOps US JS rendering required) | Walgreens category listings from the server-rendered Redux `window.getInitialState()` bootstrap (`searchResult.productList[*].productInfo`); no HTML-card or JSON-LD fallback. | 24 (1 page, `Allergy & Sinus`) | 19 departments / 170 child categories from `walgreens_categories.py` | `{"category":"Allergy & Sinus","category_id":"360545","product_id":"prod6335256","title":"Walgreens Neti Pot Kit","brand":"Walgreens","price":11.99,"currency":"USD","source_url":"https://www.walgreens.com/store/c/productlist/N=360545/1/ShopAll=360545","raw":{...},"timestamp":"2026-10-07 05:40:00"...}` |
| [`chewy_listing`](#chewy_listing) | Active | bootstrap (Next.js `__NEXT_DATA__`) | ScrapeOps US residential route required | Chewy category listings from the server-rendered Next.js `__NEXT_DATA__` bootstrap (`props.pageProps.initialState.searchSlice.plpData.products`); no HTML-card or JSON-LD fallback. | 44 (1 page, `food-332`) | 172-category pet taxonomy (dogs, cats, other pets) from `chewy_categories.py` | `{"category":"food-332","item_id":"147999","title":"Instinct Original Adult Grain-Free Real Beef Recipe Wet Dog Food, 13.2-oz can, case of 6","brand":"Instinct","price":28.14,"currency":"USD","source":"chewy_next_data_bootstrap","timestamp":"2026-10-06 21:40:56"...}` |
| [`patagonia_listing`](#patagonia_listing) | Active | api | ScrapeOps residential route required | Patagonia product listings from the first-party SFCC `AsyncComponents-ProductList` API, driven by the page's `cgid` category contract; no HTML-card or JSON-LD fallback. | Live smoke tested below; 0 items on current failover shell, parser verified against documented payload | 20 stable shopping categories from `patagonia_categories.py` | `{"category":"new-arrivals","item_id":"...","title":"...","price":...,"currency":"USD","source":"patagonia_sfcc_async_components_api",...}` |
| [`zumper_listing`](#zumper_listing) | Active | bootstrap (`window.__PRELOADED_STATE__`) | ScrapeOps US proxy | Zumper rental listings from the server-rendered `window.__PRELOADED_STATE__` bootstrap (`currentSearch.listables`) with hydrated `?page=N` pagination; no HTML-card or JSON-LD fallback. | 25 (1 page, `new-york-ny`) | 20 major US rental markets from `zumper_categories.py` | `{"category":"new-york-ny","item_id":"456715","title":"Parker Towers","min_price":2829,"max_price":6489,"currency":"USD","city":"New York","state":"NY","source":"zumper_preloaded_state","timestamp":"2026-10-07 05:36:58"...}` |
| [`crateandbarrel_listing`](#crateandbarrel_listing) | Active | bootstrap (React `ProductListing` hydration) | Akamai (ScrapeOps residential proxy required) | Crate & Barrel category listings from the first-party React `ProductListing` hydration payload only; 13 product-bearing category URLs with numeric-path pagination. | 100 (1 page, `sofas`) | 13 category URLs from `crateandbarrel_categories.py` | `{"category":"sofas","item_id":"322117","title":"Lounge Sofa (62\"-105\")","brand":"Crate & Barrel","price":1529.0,"currency":"USD","source":"crateandbarrel_productlisting_bootstrap","timestamp":"2026-10-07 09:46:17"...}` |
| [`ssense_listing`](#ssense_listing) | Experimental | bootstrap | Cloudflare; configured US proxy required | SSENSE men/women category products from the server-rendered Next.js RSC (`self.__next_f`) bootstrap only; no rendered HTML-card or JSON-LD extraction. | 120/page | 20 stable men/women category shortcuts from `ssense_categories.py` | `{"category":"men-clothing","department":"men","item_id":"15856491","sku":"242232M188005","title":"Gray Porterville Stefan Cargo Pants","brand":"Rick Owens","price":1400,"currency":"USD","total_pages":97,"source":"ssense_next_rsc_bootstrap",...}` |
| [`mediamarkt_listing`](#mediamarkt_listing) | Active | bootstrap (Apollo `window.__PRELOADED_STATE__`) | ScrapeOps proxy required (direct requests hit a 403 CAPTCHA) | MediaMarkt Germany products from the server-rendered `window.__PRELOADED_STATE__` Apollo cache (`ProductListPage` + normalized product/price/media/status/badge/feature entities); no rendered-card or JSON-LD fallback. | 12 (1 page, `Computer & Büro`) | 20 electronics and appliance categories from `mediamarkt_categories.py` | `{"category":"Computer & Büro","item_id":"3037446","title":"SAMSUNG Galaxy Book4 Edge...","brand":"SAMSUNG","price":629,"original_price":1019,"currency":"EUR","rating":4.8333,"availability":"AVAILABLE","source":"mediamarkt_preloaded_apollo_bootstrap","timestamp":"2026-10-09 01:36:58"...}` |

### hostelworld_listing

`hostelworld_listing` uses one data direction: Hostelworld's first-party Apigee
`city/hostel/{city_id}/properties` JSON API for every page, including page 1.
The API yields stable property IDs, prices, ratings, coordinates, photos,
facilities and paging totals. Requests go directly to Apigee because a proxy
that rewrites `Accept` or `Accept-Language` causes the gateway to reject them;
there is no direct-HTML or JSON-LD fallback.

The spider includes 20 deterministic popular-city seeds. Hostelworld's full
continent/country/city taxonomy is published by `sitemap-index.xml` across 32
gzipped sitemap files (about 2,838 city listing URLs).

```bash
scrapy crawl hostelworld_listing -a category=new-york -a max_pages=1 -s HTTPCACHE_ENABLED=False -O hostelworld.jsonl
```

### menards_listing

`menards_listing` extracts products through one data path: Menards' first-party
`POST /main/search/category.ajx` JSON API. It first visits the selected category
to establish the proxy-backed cookie session, derives `categoryId` from the
canonical `c-<id>.htm` URL, and then paginates the API's `searchResult.items`
contract. It does not parse product cards or JSON-LD.

The spider includes 20 stable department/category seeds from Menards' Shop >
Departments navigation. Both the category page and API request use the configured
US proxy because direct API requests receive an Incapsula challenge.

```bash
scrapy crawl menards_listing -a category=halloween-animated-decorations -a max_pages=1 -s HTTPCACHE_ENABLED=False -O menards.jsonl
```

### microcenter_listing

`microcenter_listing` uses one data direction: the structured state serialized
on each server-rendered Micro Center product card. It does not use JSON-LD or
request product detail pages. The card contract provides stable product/SKU
IDs, name, brand, price, image, position, promotion, inventory text, store ID,
and product URL. Pagination follows the listing's reported total at 24 products
per page and always preserves `storeid`.

The packaged mega-menu inventory preserves 20 departments, 118 groups, and all
578 navigation contexts, deduplicated to 513 crawl targets. Inventory and
availability are store-specific. Cambridge (`121`) is the default and can be
overridden with `-a store_id=<id>`.

```bash
scrapy crawl microcenter_listing -a category=processors-cpus -a store_id=121 \
  -a max_pages=2 -s HTTPCACHE_ENABLED=False -O microcenter.jsonl
```

#### In-progress spiders

These are still being worked on and currently returned `0` items in recent smoke runs:

| Spider Name | Status | Method | Antibot | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|---|
| [`bathandbodyworks_listing`](#bathandbodyworks_listing) | Experimental | api + bootstrap + html | PerimeterX / HUMAN (px-captcha) | Bath & Body Works multi-mode listing spider. | 0 (ok) | body-care, home-fragrance, hand-soaps | `{}` |
| [`anthropologie_listing`](#anthropologie_listing) | Experimental | api + html | PerimeterX / HUMAN | Anthropologie listing spider (API + HTML fallback). | 0 (ok) | women, dresses, sale | `n/a` |
| [`bathandbodyworks_listing`](#bathandbodyworks_listing) | Active | Mobify React Query hydration | PerimeterX / HUMAN (px-captcha) | Bath & Body Works category listings from server-rendered product state. | 48 (live, one page) | 65 current navigation targets | `{"category":"body-care","item_id":"028030187","title":"Vanilla Silk Skin Replenishing Body Wash",...}` |
| [`costco_search`](#costco_search--costco_listing) | Active | bootstrap + html | Akamai | Costco keyword search with state extraction + fallback. | 0 (skipped2) | - | `{}` |
| [`dillards_listing`](#dillards_listing) | Experimental | bootstrap | Akamai | Dillard's listing spider via `window.__INITIAL_STATE__`. | 0 (ok) | women, men, shoes, handbags, beauty, juniors, home | `n/a` |
| [`kohls_listing`](#kohls_listing) | Experimental | api | Akamai (Cloudflare challenge assets also observed) | Kohl’s listing via `/web/catalog/...` API. | 0 (ok) | women, men, sale | `n/a` |
| [`nordstromrack_listing`](#nordstromrack_listing) | Experimental | JSON-LD | Fastly (`x-jungle`) | Nordstrom Rack category listings from server-rendered Schema.org `ItemList` data. | 2 (fixture; live 403) | women, men, kids, shoes, bags-and-accessories, beauty, home, clearance | `{"item_id":"7788991","title":"Pleated Midi Dress","brand":"Donna Ricco","price":34.97,"currency":"USD",...}` |
| [`menards_listing`](#menards_listing) | Active | api | Incapsula (ScrapeOps US residential route required; API leg still returns a proxy/Incapsula failure envelope) | Menards category listings from the first-party `POST /main/search/category.ajx` JSON API; session is seeded from the category page and taxonomy comes from the homepage `mcom-header` menu JSON. | 0 (live proxy unverified; fixture smoke emits items) | 20 department/category seeds from `menards_categories.py` | `{"category":"halloween-animated-decorations","item_id":"123","title":"Animated Dragon","brand":"Enchanted Forest","price":99.99,"currency":"USD","source":"menards_category_api",...}` |

*`Number of items output` reflects recent local smoke runs (typically `max_pages=1`) and can vary by location, anti-bot behavior, and site changes.*
Many listing spiders accept `-a category=<name>` shortcuts (in addition to `-a category_url=<url>`), including Amazon, Walmart, eBay, Home Depot, Best Buy, and Kroger. Costco listing uses category-only selection.

### dell_listing

`dell_listing` reads Dell's authoritative Product Stack bootstrap map from
`data-product-detail-info`. Product cards and JSON-LD are intentionally not used
as fallback data sources.

```bash
scrapy crawl dell_listing -a category=view-all-laptops -a max_pages=2 \
  -s HTTPCACHE_ENABLED=False -O dell.jsonl
```

The ordered `FEED_EXPORT_FIELDS` contract covers identifiers, title, URLs,
pricing, ratings, badges, pagination context, source metadata, the raw API
record, and timestamp.

### dollargeneral_listing

`dollargeneral_listing` covers 20 broad Dollar General departments. It obtains
the storefront's anonymous guest tokens from `/bin/dg/user`, then uses the
first-party Omni v5 product-search API as its only product-data direction. The
API supplies identifiers, prices, inventory, fulfilment flags, ratings, facets,
and pagination metadata; rendered product cards and JSON-LD are not parsed.

```bash
scrapy crawl dollargeneral_listing -a category=on-sale -a max_pages=2 \
  -s HTTPCACHE_ENABLED=False -O dollargeneral.jsonl
```

The API is store-aware and uses the guest session's automatically selected US
store. Its ordered `FEED_EXPORT_FIELDS` contract includes 36 fields covering
category context, product identity, media, pricing, inventory, fulfilment,
reviews, pagination, provenance, the raw API record, and timestamp. The API
request enables ScrapeOps `keep_headers=true` so DG's anonymous session headers
reach the Omni host unchanged.

### redfin_listing

`redfin_listing` supports 20 popular US city markets. It reads Redfin's
server-rendered React `InitialContext` only to discover the authoritative cached
`/stingray/api/gis` request, then uses that first-party JSON API as its single
listing-data direction. The API's `{}&&` anti-hijacking prefix is removed before
decoding; no HTML-card or JSON-LD fallback is used. Pagination preserves each
market's hydrated query contract and increments `page_number` and `start`.

```bash
scrapy crawl redfin_listing -a category=los-angeles-ca -a max_pages=2 \
  -s HTTPCACHE_ENABLED=False -O redfin.jsonl
```

The ordered `FEED_EXPORT_FIELDS` contract includes property/listing/MLS IDs,
address, price, beds, baths, square footage, location, property metadata,
coordinates, market flags, pagination context, source, and the raw API record.

### wayfair_listing

`wayfair_listing` reads the authoritative server-rendered cards inside Wayfair's
`Browse-Grid`; no browser or secondary product request is required. The bundled
navigation inventory preserves 15 departments and 668 menu links; entries are
classified and only verified product listings are exposed as crawl targets
(577), so magazine hubs (`/m/`), department roots, advice/help pages, and
informational pages such as `/affirm` and Design Services are never announced as
categories. Pages without a product grid fail visibly.

```bash
common-scrapy crawl wayfair_listing -a category=sofas -a max_pages=2 -O wayfair.jsonl -s HTTPCACHE_ENABLED=False
```

Fields are exported in a fixed order: category context, listing/variant IDs,
title and manufacturer, selected options, product and image URLs, current and
original USD prices, rating/review count, promotion, stock/delivery, pagination
context, source metadata, and the decoded tracking record. Pagination follows
the rendered Next link (`?curpage=N`) and deduplicates by listing ID.

#### Sample output

The item below is the real export produced by parsing the committed
`sample/wayfair-sofas-sample.html` fixture through `wayfair_listing`
(`-a category=sofas -a max_pages=1`); long values are trimmed and `raw` is
abbreviated to its key names:

```json
{
  "item_id": "W117645758",
  "variant_id": "W117645758_1924516003_1924516004",
  "title": "Boneless 96\" Sectional Couches For Living Room Modern Modular L-Shape Cloud Sofa Compression-Boneless Deep Seat Couch With Chaise",
  "brand": "Latitude Run®",
  "selected_options": "Black Corduroy, Left Hand Facing",
  "option_ids": [1924516004, 1924516003],
  "choices_text": "5 Colors",
  "url": "https://www.wayfair.com/furniture/pdp/latitude-run-boneless-96-sectional-couches-...-w117645758.html?piid=1924516003%2C1924516004",
  "image_url": "https://assets.wfcdn.com/im/75631410/resize-h400-w400^compr-r85/4574/457449932/Boneless+96\"+Sectional+Couches+...jpg",
  "image_srcset": "<5 CDN widths, 600w/500w/400w/300w/200w>",
  "price": 399.99,
  "original_price": 419.99,
  "currency": "USD",
  "rating": 4.23,
  "reviews_count": 513,
  "promotion": "Big Furniture Sale",
  "promotion_type": "MAJOR_PROMOTION",
  "availability": "672 Left in Stock",
  "delivery": "FREE Delivery",
  "is_sponsored": false,
  "category": "sofas",
  "department": "Furniture",
  "page": 1,
  "position": 1,
  "source_url": "https://www.wayfair.com/furniture/sb0/sofas-c413892.html",
  "source": "wayfair_server_rendered_listing_card",
  "raw": {"index": 1, "pageNumber": -1, "metadata": "<41 keys: displayListingId, leadPrice, averageRating, ...>"}
}
```

Note: the committed fixture contains exactly one real product card, so the
committed sample output is 1 item. The summary table's item count reflects this
fixture run, not a live crawl.

### acehardware_listing

`acehardware_listing` uses one extraction direction: Ace Hardware's
server-rendered Kibo/Mozu bootstrap state. Product shelves come from
`#data-mz-preload-PLPModel`; no HTML-card, JSON-LD, or API fallback is used.
Pagination requests the same bootstrap payload with `?startIndex=N`. Department
seeds without products are expanded recursively from the hydrated
`routeData.-categoryObject.childrenCategories` tree until product-bearing leaves
are reached.

Ace currently requires the configured ScrapeOps proxy with both
`residential=true` and `bypass=5`. The spider adds those options without exposing
credentials.

```bash
scrapy crawl acehardware_listing -a category=cordless-drills -a max_pages=2 \
  -s HTTPCACHE_ENABLED=False -O acehardware.jsonl
```

Verified live on 2026-10-05: 60 unique items across two HTTP 200 bootstrap pages.
The exported contract includes IDs (SKU, MPN, UPC), product URL and images,
brand, pricing, availability, fulfillment methods, package measurements,
category/page metadata, source, and the normalized raw hydration record.
Every exported item also includes the crawl `timestamp`.

```json
{
  "item_id": "2385458",
  "title": "DeWalt 20V MAX 1/2 in. Brushed Cordless Compact Drill Kit (Battery & Charger)",
  "brand": "DeWalt",
  "sku": "2385458",
  "mpn": "DCD771C2",
  "upc": "885911325905",
  "price": 179.0,
  "currency": "USD",
  "in_stock": true,
  "fulfillment_types": ["DirectShip", "InStorePickup", "Delivery"],
  "category": "cordless-drills",
  "page": 1,
  "position": 1,
  "total_count": 172,
  "last_page": 6,
  "source": "acehardware_mozu_hydration"
}
```

### academy_listing
`academy_listing` uses exactly one data direction: the first-party catalog API.

```text
GET https://www.academy.com/api/category/v3/{categoryId}
    ?web=true&displayFacets=true&recordsPerPage=48&pageNumber=N
```

Academy is a React SSR storefront (not Next.js). It ships one hydration
assignment per component into `window.ASOData`, keyed by a rotating
`comp-blt<...>` id, and the PLP component (`rcn: "productListingPage240"`)
only carries the **first** slice of products — `?page=N` on the browse URL is
ignored by SSR. There is **no HTML / JSON-LD fallback**: if the API stops
answering, the spider raises instead of silently yielding an empty grid.

```json
{
  "category": "deals-clearance-hot-deals",
  "department": "Deals + Clearance",
  "category_name": "Hot Deals",
  "category_id": "210952",
  "category_url": "https://www.academy.com/c/hot-deals",
  "item_id": "8061056",
  "object_id": "164716873",
  "partnumber": "124138950",
  "parent_partnumber": "124138950",
  "sku_id": "164716873",
  "sku_ids": [
    "89676605",
    "90648031",
    "87004509",
    "…"
  ],
  "title": "YETI Rambler 18 oz Chug Cap Bottle",
  "brand": "YETI",
  "vendor_name": "YETI HOLDINGS INC YETI COOLERS LLC",
  "url": "https://www.academy.com/p/yeti-rambler-18-oz-bottle-with-chug-cap/124138950",
  "image_url": "https://academy.scene7.com/is/image/academy/21719853",
  "image_alt": "YETI Rambler 18 oz Chug Cap Bottle",
  "image_count": 24,
  "color_images": {
    "Red": "https://academy.scene7.com/is/image/academy//drinkware/yeti-rambler-18-oz-chug-cap-bottle-21071504044-red/0cc5581e-e59f-4c3f-b0f0-dc62e27d3396",
    "Brown": "https://academy.scene7.com/is/image/academy//drinkware/yeti-rambler-18-oz-chug-cap-bottle-21071503521/a626e90a-1f76-4c65-95ea-c73ae2cc8bce"
  },
  "colors": "Seafoam Pattern",
  "color_count": 16,
  "price": 37.0,
  "min_price": 19.97,
  "max_price": 37.0,
  "list_price": 37.0,
  "map_price": 37.0,
  "map_price_flag": "Y",
  "sale_price": 37.0,
  "promo_price": null,
  "msrp": 30.0,
  "min_msrp": 30.0,
  "max_msrp": 30.0,
  "valued_cost": 19.2,
  "dollar_savings": 17.03,
  "percent_savings": 38.0,
  "promo_message": null,
  "promo_code": null,
  "rebate_message": null,
  "rebate_code": null,
  "rebate_end_date": null,
  "rebate_url": null,
  "deal_badges": "Hot Deal, New Colors",
  "currency": "USD",
  "rating": 4.6,
  "reviews_count": 12431,
  "order_count": 25,
  "color": "Green",
  "size": null,
  "in_stock": true,
  "fulfillment_mode": "01 SELL ONLINE",
  "special_order": false,
  "clearance_status": "M",
  "ship_to_store": true,
  "same_day_delivery": true,
  "store_availability": {
    "pick": "0",
    "sts": "1",
    "sth": "0",
    "lsi": "0"
  },
  "free_shipping": true,
  "gift_card": false,
  "primary_category": "Water Bottles",
  "primary_category_id": "198029",
  "industry_sub_group": "Green",
  "catalog_ids": [
    "10051"
  ],
  "category_ids": [
    "3074457345616908598",
    "3074457345616941639",
    "220431",
    "…"
  ],
  "page": 1,
  "position": 4,
  "total_count": 504,
  "source_url": "https://www.academy.com/api/category/v3/210952?web=true&displayFacets=true&recordsPerPage=48&pageNumber=1",
  "source": "academy_category_api"
}
```

Run examples:
- `common-scrapy crawl academy_listing -a category=deals-clearance-hot-deals -a max_pages=2 -O academy.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl academy_listing -a url=https://www.academy.com/c/hot-deals -a max_pages=1 -O academy.jsonl`
- `common-scrapy crawl academy_listing -O academy.jsonl` (crawls the whole taxonomy)

Notes:
- `pageNumber` on this endpoint is **1-based** (unlike most Algolia-backed
  endpoints), and `nbHits`/`nbPages` in the same payload drive the stop
  condition. `recordsPerPage=48` is honoured.
- The bundle `academy_categories.py` captures the header taxonomy from
  `window.ASOData['comp-<blt...>']` with `rcn: "header240"`, at
  `cms.shop.shop_navigation[0].l1_level` (recursing `l2_level` -> `l3_level`
  -> `l4_level`), as **246 id-bearing nodes across 12 departments (97 level-2,
  137 level-3)**, collapsing to **228 unique category ids**. Nodes without a
  `categoryId` cannot be requested from `/api/category/v3/`, so they are
  dropped and their id-bearing children are kept.
- Cross-listed nodes repeat the same `categoryId` under several departments
  (e.g. "Shoes + Boots" and "Men's Shoes" are both `15646`), so the spider
  dedupes on `categoryId` and keeps every referencing department. Where a
  parent department node reuses a child's id without a browse URL (e.g.
  "Deals + Clearance" == "Hot Deals" == `210952`), the URL-bearing cross-listing
  wins so `-a url=...` resolves. Category slugs are department-qualified, e.g.
  `deals-clearance-hot-deals`.
- The API host is PerimeterX-protected: the plain datacenter route returns a stub
  instead of JSON, so the spider appends `scrapeops.country=us.bypass=5` to the
  ScrapeOps proxy username for product requests only.
- `price` prefers `defaultSku.salePrice` and falls back to `minEffectivePrice` /
  `minProductPrice`; `list_price` comes from `defaultSku.listPrice`, falling back
  to `mapPrice` (the struck-through value). `brand` is the `facet_Brand` facet,
  `rating`/`reviews_count` come from `descriptiveAttributes` (falling back to
  `averageRating`/`reviewCount`), and `color`/`size` from
  `defaultSku.color` / `definingAttributes`.
- `url` is built from the bare `seoURL` slug as
  `https://www.academy.com/p/<slug>/<partNumber>`, and protocol-relative
  Scene7 images (`//academy.scene7.com/...`) are absolutized to `https://`.
- The ordered export fields are `category`, `department`, `category_name`,
  `category_id`, `category_url`, `item_id`, `object_id`, `partnumber`,
  `parent_partnumber`, `sku_id`, `sku_ids`, `title`, `brand`, `vendor_name`,
  `url`, `image_url`, `image_alt`, `image_count`, `color_images`, `colors`,
  `color_count`, `price`, `min_price`, `max_price`, `list_price`, `map_price`,
  `map_price_flag`, `sale_price`, `promo_price`, `msrp`, `min_msrp`,
  `max_msrp`, `valued_cost`, `dollar_savings`, `percent_savings`,
  `promo_message`, `promo_code`, `rebate_message`, `rebate_code`,
  `rebate_end_date`, `rebate_url`, `deal_badges`, `currency`, `rating`,
  `reviews_count`, `order_count`, `color`, `size`, `in_stock`,
  `fulfillment_mode`, `special_order`, `clearance_status`, `ship_to_store`,
  `same_day_delivery`, `store_availability`, `free_shipping`, `gift_card`,
  `primary_category`, `primary_category_id`, `industry_sub_group`,
  `catalog_ids`, `category_ids`, `page`, `position`, `total_count`,
  `source_url`, `source`, and `raw`.
- **Variant, price and fulfilment detail come out of the same single API
  response** — no extra requests, no second direction. Every field below is
  already present in the `/api/category/v3/` hit and was simply not being read:
  - `sku_ids` (every SKU in the style), `object_id` (the search-engine object id,
    distinct from `item_id`), `color_count` / `brandColorCount`, `colors`
    (`Color` facet) and `color_images` — the `{colour: image}` family map from
    `industrySubGroup_image`, absolutized. `image_count` is the gallery size
    derived from `industrySubGroup_ImageSku` (primary shot + `alternateImages`
    per swatch).
  - `min_price` / `max_price` are the `minProductPrice` / `maxProductPrice`
    **range** across the product's variants, which `price` alone cannot express
    for a multi-colour item. `msrp` / `min_msrp` / `max_msrp` come from
    `minMSRP`/`maxMSRP` (falling back to `descriptiveAttributes.udamsrp`).
  - Price telemetry lives on the swatch blocks, not on the hit root:
    `swatches_mapprice.priceInfo` is the MAP-price (member) view and carries
    `dollarSavings` / `percentSavings`; `swatches_nonmapprice.priceInfo` is the
    open price view. `valued_cost` is Academy's member valued cost, read from
    whichever block is present.
  - `rebate_*` mirror `rebatePromotion` (message, promotion code, end date, PDF
    link). `deal_badges` is `facet_Deals`, deduped — the facet repeats a value
    when several merchandising rules match the same hit
    (`["Hot Deal", "Hot Deal", "New Colors"]`).
  - Fulfilment: `fulfillment_mode` is `ecomCodeDesc`
    (`01 SELL ONLINE` / `04 DROP SHIP` / `07 SELL ONLINE AND DROPSHIP`),
    `special_order` is `SPECIALORDER == "Y"`, `clearance_status` is
    `Clearance_Status` (`Y` / `M` / `N`, deduped), and `ship_to_store` /
    `same_day_delivery` decode the single-element `["Y"]` / `["N"]` flag lists.
    `store_availability` keeps the API's own per-channel out-of-stock flags
    verbatim under short names — `pick` (pickup), `sts` (ship-to-store), `sth`
    (ship-to-home), `lsi` (large item), `stsfs` (ship-from-store) — because a
    missing key means "channel not stated" rather than "out of stock".
  - `vendor_name` is `descriptiveAttributes.vendorName` (the legal entity, e.g.
    `NIKE USA INC`) and is not the same as the `brand` facet.
- Fields that are genuinely sparse on a hot-deals grid stay `null` rather than
  being invented: `rebate_*` (~3% of hits), `dollar_savings` / `percent_savings`
  (only hits on the MAP-price view), `msrp` (~half of hits) and `color_images`
  (empty for products with no colour family). `special_order` remains a boolean
  and is true only for products explicitly marked `SPECIALORDER == "Y"`.

Verified live (`category=deals-clearance-hot-deals`, `max_pages=2`, ScrapeOps
proxy, 2026-10-04 UTC): **96 items, 96 unique `item_id`s**, 22 distinct brands,
`raw` present on 96/96, 68 exported fields per item. `category=sports-soccer`,
`max_pages=1`: **48 items**, 48 unique, `nbHits=845`.

### adidas_listing

`adidas_listing` uses one authoritative source: the server-rendered Next.js
hydration blob at `script#__NEXT_DATA__` -> `props.pageProps`. Products live in
`props.pageProps.products` (48 per window), the category taxonomy is captured in
`adidas_categories.py` (25 sitemap sections / 196 category URLs), and pagination
is a pure hydration re-render driven by the `?start=<N>` query parameter stepping
by `info.viewSize`. It supports `-a category=<name>`, `-a category_url=<url>`, or
`-a url=<url>`, and deduplicates products by `id` across pages.

Pricing uses the `sale` entry as the current price and the `original` entry as the
list price when a discount is present (adidas hangs a negative
`discountPercentage` off the `original` entry). `colorway_count` / `colorway_ids`
carry the sibling colour SKU list (`colourVariations`); the PLP hydration exposes
no human-readable colour names. `brand` is the adidas `subTitle` product line
(e.g. `Men Performance`) and `product_category` is the merch category
(e.g. `Performance`). Every item carries the full `raw` hydrated product record.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl adidas_listing -a category=mens-running-shoes -a max_pages=2 -O adidas.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"mens-running-shoes","department":"MEN'S SHOES","subcategory":"Men's Running Shoes","item_id":"KI8294","style_id":"ONN61","title":"ADIZERO ADIOS PRO 5 Running Shoes","brand":"Men Performance","product_category":"Performance","colorway_count":3,"colorway_ids":"KI8294, KJ7039, KJ7040","price":275.0,"original_price":null,"discount_percentage":null,"currency":"USD","rating":4.8001,"reviews_count":5,"on_sale":false,"sold_out":false,"badges":"New","page":1,"position":1,"total_count":241,"source":"adidas_next_data_page_props_products"}
```
### petsmart_listing

`petsmart_listing` uses one data direction: PetSmart's own Algolia proxy. The
storefront bundle pins `NEXT_PUBLIC_ALGOLIA_HOST_URL` to
`www.petsmart.com/api/search` and builds the search client with an **empty**
application id and api key, so the storefront never touches an Algolia host:

```text
POST https://www.petsmart.com/api/search/1/indexes/r-US_products_best-sellers/query
{"params": "query=&hitsPerPage=100&page=0&filters=isSKUAvailable: true AND onlineFrom < <now_ms> AND onlineTo > <now_ms> AND custom_category_names:\"Dog > Food > Dry Food\"&attributesToRetrieve=id,objectID,masterProductID,name,brand,..."}
headers: content-type: application/json, x-algolia-application-id: "", x-algolia-api-key: "", x-petm-algolia-caller: web_desktop
```

No authentication, no API key, no browser execution and no HTML/JSON-LD parsing:
products are the `hits[]` of the search envelope itself. PLPs are Next.js App
Router pages (RSC flight stream, ~1.8 MB per page, no `__NEXT_DATA__`), so the
API route is both lighter and more stable.

- **Taxonomy from the API.** `custom_category_names` is the facet the storefront
  PLPs filter on. `petsmart_categories.py` ships the 2026-10-04 capture: 7
  departments (Dog, Cat, Fish, Bird, Reptile, Small Pet, Farm Animal), 491
  category paths, each with its SKU count. Marketing overlays (`Sale`,
  `Featured Shops`, `Featured Brands`, `PA`, ...) are excluded. All 491 derived
  PLP URLs were verified; the 15 that redirect are pinned in
  `CANONICAL_URL_OVERRIDES`.
- **Three sort replicas.** `-a sort=best-sellers` (default, storefront default),
  `top-rated`, `new-arrivals`.
- **`attributesToRetrieve`.** Only the ~46 attributes the item reads are pulled,
  which keeps a 100-hit page at ~450 KB instead of ~1.9 MB (the full payload
  repeats an HTML `long_description` per hit).
- **Product URLs.** Hits carry no URL, so the canonical PDP route is rebuilt from
  the hit's browse path + name slug + `masterProductID`
  (`/dog/food/dry-food/<name-slug>-36648.html`), the same shape the PLP JSON-LD
  `offers.url` uses. Verified live (12/12 sample URLs return HTTP 200).
- **Range pricing.** `priceData.current`, else the `saleRange` floor when
  `price.displayType == "range"` (the card advertises "from $x" while
  `price.number` is the priciest variant).
- **Fail loud.** A challenge page, a non-200, a non-JSON body or an Algolia error
  envelope raises instead of yielding empty items. There is no HTML fallback.

Arguments: `-a category=<slug path>` (e.g. `dog/food/dry-food`), or
`-a category_url=<PLP url>`, `-a max_pages=N`, `-a hits_per_page=N` (default 100),
`-a sort=<replica>`, `-a available_only=0` (drop the availability window).

```bash
rm -f petsmart-out.jsonl
HTTPCACHE_ENABLED=False common-scrapy crawl petsmart_listing -a category=dog/food/dry-food -a max_pages=2 -O petsmart-out.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category": "dog/food/dry-food", "department": "Dog", "subcategory": "Food", "category_name": "Dog > Food > Dry Food", "category_url": "https://www.petsmart.com/dog/food/dry-food/", "category_item_count": 1794, "sort": "best-sellers", "index": "r-US_products_best-sellers", "item_id": "5252900", "master_product_id": 36648, "title": "Purina Pro Plan Sensitive Skin and Stomach Dry Dog Food Adult Salmon & Rice Formula Digestive Health", "brand": "Purina Pro Plan", "url": "https://www.petsmart.com/dog/food/dry-food/purina-pro-plan-sensitive-skin-and-stomach-dry-dog-food-adult-salmon-and-rice-formula-digestive-health-36648.html", "image_url": "https://s7d2.scene7.com/is/image/PetSmart/5252900?$sclp-prd-main_large$", "price": 77.99, "price_display": "$20.68-$94.99", "price_display_type": "range", "currency": "USD", "rating": 4.5, "reviews_count": 9118, "upc": "038100175526", "available": true, "autoship_eligible": true, "variation_types": "4 Sizes, 1 Flavor", "page": 1, "position": 1, "total_count": 937, "total_pages": 10, "source": "petsmart_first_party_search_api", "raw": {...}}
```

`max_order_quantity` and the food facets are department-dependent, and the spider
leaves them `null` rather than inventing values — a `Cat > Toys` capture has
`pet_types`, `max_order_quantity`, `carton_weight` and `conversion_rate` populated
while every food facet stays null.

### blick_listing

`blick_listing` uses exactly one product-data direction: the first-party
product-search API.

```text
GET https://api.dickblick.com/product-search/api/v1.0/collections/alias/{entryId}
    ?pageNumber=N&pageSize=30&includeFacets=false
Header: X-blick-portal: blick
```

Blick is a Next.js storefront. The category page server-renders the first 30
products into `__NEXT_DATA__`, but its pager emits no links -- the page-number
controls are JavaScript buttons. The category page is therefore still fetched,
for exactly one value: `props.pageProps.entryId`, the opaque collection id the
API is keyed by. Products are **never** parsed out of the HTML. API
`pageNumber=0` returns the same 30 records the HTML embeds (verified by
comparing `itemId` order), so page 1 is fetched from the API as well and the
spider has a single item source. There is **no HTML / JSON-LD fallback**: if the
API stops answering, the spider raises instead of silently yielding fewer items.

API paging is **zero-based**: `pageNumber=0` is the first page and
`pageNumber=1` is the second. The stop condition is `totalPages`, with
`pageNumber * pageSize >= totalCount` as a backstop when `totalPages` is
absent, plus the `max_pages` cap. `includeFacets=false` keeps facet payloads out
of the response; pagination never needs updated facet counts.

`X-blick-portal: blick` is required -- it is a static literal in the storefront
bundle, not a credential. Both hosts answer through the plain configured
ScrapeOps US proxy; no bypass or residential option was needed.

Taxonomy (`blick_categories.py`) is captured from the `/categories/`
hydration: `props.pageProps.data[]` holds **2,697 records**, which are the same
**899 nodes** repeated under three `contentType` values (`department`,
`categoriesLandingPages`, `subCategoriesLandingPages`). Keeping only the records
that carry both `name` and `url` collapses that to **899 unique
`/categories/.../` URLs under 17 departments** -- 16 department landing pages,
204 direct children and 679 grandchildren. Nine further group nodes are
path-derived containers with no landing page of their own (e.g.
`/categories/painting/acrylics/` exists only as a segment of its children), so
`crawlable_categories()` returns 899 rows while `flatten_categories()` returns
908. The marketing homepage's smaller `browseDepartments` array is deliberately
not used: it is a curated subset that would miss hundreds of leaf categories.

```json
{
  "category": "paint-and-mediums/acrylic-paint",
  "department": "Paint and Mediums",
  "category_name": "Acrylic Paint",
  "category_path": "Paint and Mediums > Acrylic Paint",
  "category_url": "https://www.dickblick.com/categories/painting/acrylic-paint/",
  "collection_id": "64h0nGCpZmASYWykoCaM4E",
  "item_id": "00711",
  "entry_id": "369APl7qXZbGGqHYo0wZsc",
  "sku_id": "00711",
  "title": "Blickrylic Student Acrylic Paints and Sets",
  "brand": "Blick",
  "url": "https://www.dickblick.com/products/blickrylic-student-acrylics/",
  "image_url": "https://cld-assets.dick-blick.com/image/upload/f_auto/q_auto/v1748032379/00711-Group-9-4ww.jpg",
  "image_alt": "Blickrylic Student Acrylic Paints and Sets",
  "short_description": "Blickrylic Student Acrylic Paint is a true acrylic paint, priced for the budget-minded...",
  "price": 7.45,
  "price_max": 183.4,
  "list_price": 183.4,
  "sale_price": 7.45,
  "currency": "USD",
  "savings_text": "SAVE up to 43%",
  "is_sale": true,
  "is_best_price": true,
  "rating": 4.6,
  "reviews_count": 2140,
  "sku_count": 123,
  "in_stock": true,
  "is_new": false,
  "is_overstock": false,
  "is_clearance": false,
  "is_coupon_eligible": false,
  "page": 0,
  "position": 1,
  "total_count": 168,
  "total_pages": 6,
  "source_url": "https://api.dickblick.com/product-search/api/v1.0/collections/alias/64h0nGCpZmASYWykoCaM4E?pageNumber=0&pageSize=30&includeFacets=false",
  "source": "blick_product_search_api",
  "raw": {
    "_omitted": "(full product object retained in the feed)"
  }
}
```

Run examples:
- `common-scrapy crawl blick_listing -a category=paint-and-mediums/acrylic-paint -a max_pages=3 -O blick.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl blick_listing -a category_url=https://www.dickblick.com/categories/painting/acrylic-paint/ -a max_pages=2 -O blick.jsonl`
- `common-scrapy crawl blick_listing -O blick.jsonl` (crawls all 899 categories)

Notes:
- Category slugs are a `department/group/leaf` path of the display names, e.g.
  `paint-and-mediums/acrylic-paint`. Look them up with
  `common-spiders.blick_categories.crawlable_categories()`. The homepage
  `browseDepartments` list is **not** the taxonomy.
- `entryId` is resolved from the category page's `__NEXT_DATA__`, so every
  category costs one extra HTML request before its first API page. That request
  is never mined for products.
- **Challenge detection scans only the first 8 KB** of the category page. A real
  PLP is ~370 KB and its feature-flag blob contains strings such as
  `ff-checkout-captcha-enabled`, so a whole-body substring scan rejects every
  legitimate category page. The API leg is checked against JSON markers plus
  `<html`, since that endpoint otherwise always answers with JSON.
- The API answers HTTP 200 with a bare JSON **string** (`"Collection with
  external ID '...' not found"`) for an unknown alias -- which happens for
  department landing pages that have no product collection. A non-object
  payload raises.
- Dedupe is on `itemId`, falling back to `entryId`. The API itself repeats
  items across page boundaries: a 3-page run returns 90 item slots containing
  **84 unique** `itemId`s (six products appear on two pages each), so the
  emitted count is lower than `pageSize * pages` by design.
- `price` is `pricing.priceMin` and `price_max` is `pricing.priceMax`; Blick
  lists one product record per family with a price range across its SKUs, so
  `list_price` is `pricing.skuMsrp` when present, otherwise `price_max` for
  range-priced products. `sale_price` is `priceMin` only when
  `pricing.isSkuOnSale`, and `savings_text` carries `pricing.savingStory`
  (e.g. `SAVE up to 43%`).
- `in_stock` is `true` for every listed product: the search payload has no stock
  flag, so availability is expressed through the flags it does carry
  (`is_new`, `is_overstock`, `is_clearance`, `is_coupon_eligible`).
- `page` is the zero-based API `pageNumber`, matching the endpoint's own
  numbering, and `position` is the 1-based index within that page's response.
- The ordered export fields are `category`, `department`, `category_name`,
  `category_path`, `category_url`, `collection_id`, `item_id`, `entry_id`,
  `sku_id`, `title`, `brand`, `url`, `image_url`, `image_alt`,
  `short_description`, `price`, `price_max`, `list_price`, `sale_price`,
  `currency`, `savings_text`, `is_sale`, `is_best_price`, `rating`,
  `reviews_count`, `sku_count`, `in_stock`, `is_new`, `is_overstock`,
  `is_clearance`, `is_coupon_eligible`, `page`, `position`, `total_count`,
  `total_pages`, `source_url`, `source`, and `raw`.

Verified live (`HTTPCACHE_ENABLED=False`, ScrapeOps US proxy, 2026-10-05 UTC):

| Category | `max_pages` | Items | Unique `item_id` | API pages crawled | `total_count` / `total_pages` | Distinct brands | Requests |
|---|---|---|---|---|---|---|---|
| `paint-and-mediums/acrylic-paint` | 3 | 84 | 84 | `pageNumber=0,1,2` | 168 / 6 | 37 | 4 (1 category page + 3 API) |
| `illustration-and-drawing-supplies/art-markers` | 2 | 56 | 56 | `pageNumber=0,1` | 434 / 15 | 28 | 3 (1 category page + 2 API) |

Both runs returned non-empty `item_id`, `title`, `brand`, `url`, `image_url`,
`price` and `currency` on 100% of items. The acrylic-paint run requested 90 item
slots (3 x 30) and emitted 84 after dedupe, matching the six cross-page repeats
present in the upstream API responses. Sample output items:

| # | Category | `item_id` | `title` | `brand` | `price` | `price_max` | `savings_text` | `rating` | `reviews_count` | `page` | `position` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | acrylic-paint | `00711` | Blickrylic Student Acrylic Paints and Sets | Blick | 7.45 | 183.4 | SAVE up to 43% | 4.6 | 2140 | 0 | 1 |
| 2 | acrylic-paint | `00760` | Sennelier Abstract Acrylic Paints and Sets | Sennelier | 3.6 | 33.79 | SAVE 17-53% | 4.5 | 139 | 0 | 30 |
| 3 | acrylic-paint | `00795` | Liquitex Professional Acrylic Gouache and Sets | Liquitex | 9.79 | 73.91 | SAVE 30-42% | 4.8 | 223 | 1 | 1 |
| 4 | acrylic-paint | `01633` | Da Vinci Fluid Acrylics | Da Vinci Paints | 10.45 | 49.9 | SAVE 50% | 4.5 | 51 | 1 | 30 |
| 5 | acrylic-paint | `00799` | Pebeo Mat Pub Paint | Pebeo | 12.15 | 14.42 | SAVE 31-40% | 4.8 | 5 | 2 | 30 |
| 6 | art-markers | `01660` | Posca Paint Markers and Sets | Posca | 2.37 | 94.99 | SAVE up to 65% | 4.8 | 1007 | 0 | 1 |
| 7 | art-markers | `21252` | Crayola Super Tips Washable Markers Sets | Crayola | 3.67 | 23.75 | SAVE up to 47% | 4.6 | 14 | 1 | 30 |

Rows 1-5 are the first and last item of each of the three acrylic-paint API
pages; rows 6-7 are the first and last item of the two art-markers API pages.

Tests: `tests/test_blick_listing_spider.py` (34 tests) covers the taxonomy
counts and uniqueness, the cross-listed-URL collapse, zero-based paging,
`totalPages` / empty-page / `max_pages` / `totalCount` stop conditions,
cross-page and intra-page dedupe, the portal header and endpoint shape, and the
fail-loud paths (missing `__NEXT_DATA__`, missing `entryId`, challenge bodies,
non-200, non-JSON, unknown-alias string payload). Fixtures under `sample/` are
trimmed from the live captures: each API fixture keeps the response envelope
(so paging behaves as on the untrimmed response) plus two real products.


### cvs_listing

`cvs_listing` uses exactly one data direction: the bootstrap hydration state CVS
already ships with every shop page.

```text
var initialState = {
  "allCategories": {...},        # named shop taxonomy (715 PLP URLs)
  "productIndexData": {
    "numFound": 3035, "start": 0, "limit": 20, "page": 1,
    "products": [...],           # 20 product objects
    "facets": {...}, "refinements": [...], "breadCrumbs": [...]
  }
};
```

The spider parses `var productIndexData = {...}` only. There is **no product
markup fallback and no JSON-LD fallback**: if the assignment or its expected
keys disappear, the spider raises rather than silently degrading to card
scraping. Pagination is ordinary query-string SSR (`?page=N`) and the stop
condition comes from `start`/`limit`/`numFound` in that same assignment, so the
spider never has to guess a page count.

Run examples:

```bash
common-scrapy crawl cvs_listing -a category=health-medicine -a max_pages=3 -O cvs.jsonl -s HTTPCACHE_ENABLED=False
common-scrapy crawl cvs_listing -a category=multivitamins -a max_pages=2 -O cvs.jsonl
common-scrapy crawl cvs_listing -a category_url=https://www.cvs.com/shop/vitamins/multivitamins -a max_pages=1 -O cvs.jsonl
```

Sample item (`category=health-medicine`, page 1 position 1, `raw` omitted):

```json
{
  "item_id": "702568",
  "title": "Nature's Truth Melatonin 12mg & Magnesium Gummies, Sour Grape, 60 CT",
  "brand": "Nature's Truth",
  "url": "https://www.cvs.com/shop/nature-s-truth-melatonin-12mg-magnesium-gummies-sour-grape-60-ct-prodid-702568",
  "image": "https://www.cvs.com/bizcontent/merchandising/productimages/high_res/84009312838.jpg",
  "price": 21.99,
  "original_price": null,
  "sale_price": null,
  "carepass_price": null,
  "unit_price": "36.6¢/ea.",
  "currency": "USD",
  "in_stock": true,
  "stock_quantity": 2052,
  "store_pickup": true,
  "pickup_in_stock": false,
  "same_day_in_stock": false,
  "rating": null,
  "reviews_count": null,
  "is_new": true,
  "is_featured": false,
  "is_sponsored": false,
  "hot_deals": false,
  "fsa_eligible": false,
  "promo_message": "Buy 1, Get 1 Free",
  "size": "60.00 Ct",
  "count": "60 CT",
  "category": "health-medicine",
  "category_name": "Health & Medicine",
  "category_id": "cat1",
  "department": "Health & Medicine",
  "breadcrumb": ["Health & Medicine"],
  "page": 1,
  "position": 1,
  "total_count": 3035,
  "source_url": "https://www.cvs.com/shop/health-medicine",
  "source": "cvs_product_index_hydration"
}
```

Notes:

- Each PLP is a ~3.9 MB SSR document, so `CONCURRENT_REQUESTS_PER_DOMAIN` is 1
  with a 1 s `DOWNLOAD_DELAY`.
- `cvs_categories.py` is captured from
  `initialState.allCategories.allCategories.children` (15 roots / 856 nodes /
  730 distinct browse URLs before filtering). Each node's first child repeats the
  parent as an "All &lt;department&gt;" link; those self-links are dropped. The
  `/shop/brand-directory` tree and content pages such as `/shop/content/fsa` are
  excluded because they are not product listings. That leaves **13 departments
  and 715 category URLs**, each carrying its CVS `cat*` id.
- CVS cross-lists labels (e.g. "Compression Hosiery & Stockings" appears under
  two Home Health Care branches, and "Bar Soap" under two Personal Care ones),
  so CLI slugs are department-qualified (`personal-care-bar-soap`) and fall back
  to a path-qualified slug plus counter when that still collides. All 715 slugs
  and 715 URLs are unique.
- CVS emits `"0.0"` for every optional price it does not have, so `carepass_price`
  treats 0 as absent rather than reporting a free product.
- `sale_price`/`original_price` are only populated when `salePrice < listPrice`;
  CVS otherwise mirrors `salePrice` into `listPrice` and reporting that as a
  markdown would be wrong.
- `inventoryInfo` separates `shipInv`, `pickInv` and `sddInv`, which is why
  `in_stock`, `pickup_in_stock` and `same_day_in_stock` are separate fields.
- `raw` keeps the verbatim product object plus its `variants` list, so
  variant-level size/price/availability differences that the PLP grid does not
  surface stay re-derivable downstream.
- An unknown `-a category=` slug raises at construction time rather than
  producing an empty crawl.


### containerstore_listing

`containerstore_listing` uses one authoritative source: the server-rendered Next.js
hydration blob at `script#__NEXT_DATA__` -> `props.pageProps.initialState`. No HTML
cards, no JSON-LD, no XHR fallback.

The payload is Redux-style normalized state and splits cleanly:

| Path | Contents |
|---|---|
| `initialState.products.entities` | normalized product records keyed by product id |
| `initialState.plp.entities[str(currentPage)].products` | the **ordered** ids for that one page |
| `initialState.plp.data` | `totalCount`, `currentPage`, `lastPage`, `pageSize`, `nextPageUrl`, `breadcrumbs` |
| `initialState.categories.data.eCommCategories` | the full taxonomy: `L1Categories`, `L2Categories`, `L3Categories` |

Pagination is plain SSR: the spider follows the `nextPageUrl` the payload hands it
(`/s/<cat>/<id>?p=60&ps=60`) until `lastPage`, an empty grid, or `max_pages`. Products
are deduplicated by id across pages.

Taxonomy lives in `containerstore_categories.py` -- **362 hydrated nodes** (14 L1 +
189 L2 + 159 L3) reduced to **295 unique catalogue URLs** by dropping 21
design-centre/tooling links (`/custom-spaces/...`, `/design-center/...`) and 52
duplicate URLs (the storefront repeats each `/s/<dept>/1` href as a
`Shop All <department>` L2 node; the shallower L1 entry wins). Names are
HTML-unescaped -- nine Elfa / Desktop Collection nodes ship `Decor&#43; by Elfa`
style entities.

Two things are worth knowing before picking a category:

* **`pageType` is not a reliable signal.** A leaf that hydrates as `PrismicTemplate`
  carries a full 60-item grid, while a `/12` page hydrating as `Category` may carry
  none at all. The spider keys off the presence of an ordered grid in `plp.entities`
  and ignores `pageType` entirely.
* **Department pages (`/s/<dept>/1`) have no product grid.** They hydrate as
  `EnhancedCategoryLanding` with an empty `plp.entities` and render a subcategory
  *tile* grid instead. Crawling one logs a message and yields 0 items -- that is not
  an error. Use a `/12` or `/123` leaf to get products.

Pricing needs care. The displayed `salePrice` / `retailPrice` strings are ranges
(`"$4.49 – $71.91"`) for multisku products, so they are never parsed. The numeric
`minSalePrice` / `minRetailPrice` are used instead, and `isOnSale` is frequently
`true` while the two are equal -- when the computed discount is not positive the item
falls back to `price = minRetailPrice` with a null `original_price` and
`discount_percentage` rather than reporting a 0% discount.

`color_option_count` / `color_options` come from `colorSwatcheInfo.values` (populated
for only 6 of 60 products on a representative page); `badge` is the storefront's
merchandising badge (`25off`, `Clearance`). `department` / `subcategory` / `leaf` are
taken from the spider's taxonomy, falling back to the page `breadcrumbs` so `-a url=`
still gets a full path. Every item carries the full `raw` hydrated product record.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl containerstore_listing -a category="Kitchen > Pantry Organizers" -a max_pages=2 -O containerstore.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"Kitchen > Pantry Organizers","department":"Kitchen","subcategory":"Pantry Organizers","leaf":null,"item_id":"11017102","sku_id":"10087168","title":"Everything Organizer Shelf-Depth Pantry Bin with Divider","url":"https://www.containerstore.com/s/kitchen/pantry-organizers/shelf_depth-pantry-bin-with-divider/12d?productId=11017102","image_url":"https://images.containerstore.com/catalogimages/683293/10087168_15_Inch_Modular_Pantry_Bin_.jpg?width=312&height=312","image_alt":"Shelf-Depth Pantry Bin with Divider","product_type":"single","color_option_count":null,"color_options":null,"price":9.19,"original_price":22.99,"discount_percentage":60.03,"currency":"USD","on_sale":true,"out_of_stock":false,"rating":5.0,"reviews_count":20,"badge":"Clearance","page":1,"position":1,"total_count":325,"last_page":6,"source_url":"https://www.containerstore.com/s/kitchen/pantry-organizers/12","source":"containerstore_next_data_products_entities"}
```

### shopbop_listing

`shopbop_listing` uses one authoritative source: the server-rendered hydration blob
assigned to `window.__shopbop_sca_hydrate__` inside a `DOMContentLoaded` listener. No
HTML product cards, no JSON-LD, no separate product API, no browser engine. The blob is
a megabyte of nested JSON, so it is read with a balanced `json.JSONDecoder().raw_decode`
rather than a regex.

The dehydrated React Query cache sits at a different depth depending on which slots the
page composes, so the spider searches **every** `queries` list in the tree for the entry
that hydrates a `products` array:

| Path | Contents |
|---|---|
| `...topLevelSlots["plp-main"].content.slotConfiguration.squareState.props.dehydratedState.queries[]` where `queryKey[0] == "products"` | the authoritative grid |
| `...state.data.data.products[]` | `{"colorSin": ..., "product": {...}}` entries |
| `...state.data.data.nextOffset` / `totalResults` / `folderId` / `resultsTitle` | pagination + category identity |
| `...topLevelSlots["top-nav-1"]...props.unfilteredNavigationData.navigationCategoryGroupList` | the full taxonomy (homepage only) |

Two structural traps are worth knowing:

* **`pageType` alone is not enough.** The blob also reports `Designer` (`/designers`),
  `DesignerIndex`, `MensLandingPage` (`/shop-men`) and `Homepage` -- none of which carry a
  `products` query at all. The spider looks for the grid first and only enforces
  `pageType == "PLP"` once one is found, so a non-listing page logs a message and yields
  0 items instead of raising.
* **`totalResults` drifts between pages.** `Women > What's New` reported 1097 on page 1 and
  1046 on page 2 minutes later; `Women > Sale` reported 8078 and then 7820. It is used only
  as an upper bound, never as a page count -- pagination actually follows `nextOffset`.

Pagination is ordinary `?offset=N` at a **page size of 100**
(`slotToCardConfig["plp-main"].widgetConfig.pageSize`). The offset is rewritten **in
place**, so any facet/sort state already on the URL (`?f=...&productSort=...`) survives.
`nextOffset` is `null` on the natural last page, and products are deduplicated by
`productSin` across pages.

Taxonomy lives in `shopbop_categories.py` -- **335 navigation link nodes** shipped by the
homepage (3 groups -> 20 primary categories -> 311 section/item links) reduced to **266
unique category URLs** (Women 183, Men 70, Beauty 13):

* 20 nodes carry **no `folderId`** and are dropped: 11 editorial `/ci/...` pages, the
  designer index (`/designers`, `/designers?bu=sbm`), one hand-curated `/vp/` product page,
  `/giftcard` and the `/shop-men` landing page.
* 49 nodes repeat a URL already present at a **shallower** level (34 distinct duplicates).
  The storefront repeats each primary category link as its own section link and again as an
  `All <Category>` item link, so `/whats-new/br/v=1/13198.htm` appears three times. The
  shallowest node wins and a category keeps its primary-catalog placement.
* Titles are whitespace-collapsed (several ship as `"Accessories "`), and the 27 sections
  with an empty `title` (the storefront's `imageSection` blocks) are omitted from the path
  rather than emitted as a blank segment.

Pricing needs care. `retailPrice.usdPrice` is the only **numeric** price in the payload;
`lowPrice` / `highPrice` / `colorPrice` only carry a formatted string (`"$262.50"`) plus
`onSale` / `salePercentage` flags. The strings are never parsed -- the current price is
derived as `usdPrice * (1 - salePercentage / 100)`, which matches the storefront string
exactly on all 100 products of a representative sale grid. A product with `onSale: true`
but no positive percentage, or a discount that rounds back onto the retail price, is
reported as a full-price item.

Two smaller notes:

* **Image URLs need a CDN base *and* a transform suffix.** The payload's `/prod/products/...`
  path is CDN-relative: it resolves against `https://m.media-amazon.com/images/G/01/Shopbop/p`
  (the `/p` segment is required -- without it the CDN answers `Not Found`) and the raw
  `.jpg` 404s, so the storefront's own `._QL90_UX564_.jpg` transform is appended to the
  filename stem.
* **`reviews.average` hydrates as `0` for every product** on the grids checked, so `rating`
  is only emitted when `reviews_count` is non-zero rather than reporting a misleading `0.0`.

One item is emitted per `productSin`; the colorways (`colors[]`, each with its own images,
swatch and `sizeSins`) and the size run (`sizes[]`) are retained in `raw` and summarised in
`color_options` / `size_options` / `color_option_count` / `size_option_count`. The default
PLP query sets `allowOutOfStockItems: false`, so the storefront filters sold-out products
out before hydration and `out_of_stock` is false in practice. 40 export fields.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl shopbop_listing -a category="Women > What's New" -a max_pages=2 -O shopbop.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"Women > What's New","department":"Women","subcategory":"What's New","leaf":null,"folder_id":"13198","item_id":"1560892247","sku_id":"AKNVA30171","title":"Kyla Faux Fur Coat","brand":"AKNVAS","brand_url":"https://www.shopbop.com/aknvas/br/v=1/69344.htm","url":"https://www.shopbop.com/kyla-faux-fur-coat-aknvas/vp/v=1/1560892247.htm","image_url":"https://m.media-amazon.com/images/G/01/Shopbop/p/prod/products/aknva/aknva3017128ab5/aknva3017128ab5_1789592901812_2-0._QL90_UX564_.jpg","image_url_count":7,"color":"TAN / WHITE","color_code":"28AB5","color_option_count":1,"color_options":"TAN / WHITE","size_option_count":4,"size_options":"XS, S, M, L","size_scale":"US","price":1495.0,"original_price":null,"discount_percentage":null,"currency":"USD","on_sale":false,"final_sale":false,"out_of_stock":false,"rating":null,"reviews_count":0,"product_type":"Outerwear","product_category":"APPAREL","gender":"WOMENS","attribute_icons":null,"page":1,"position":1,"total_count":1097,"offset":0,"source_url":"https://www.shopbop.com/whats-new/br/v=1/13198.htm","source":"shopbop_sca_hydrate_products_query"}
```

Fixtures: `sample/shopbop-home-navigation.html` (homepage taxonomy payload),
`sample/shopbop-listing-page1.html` / `-page2.html` (`?offset=100`), `-sale.html` (the
discount branch), `-lastpage.html` (`nextOffset: null` on an 81-item category),
`-empty.html` and `-designer-index.html` (`pageType="Designer"`, no products query).

Tests: `python -m pytest tests/test_shopbop_listing_spider.py` (40 network-free tests,
including a taxonomy rebuild from the saved homepage that asserts 335 -> 315 -> 266).

Live verification (`-s HTTPCACHE_ENABLED=False`, 2026-10-05 UTC, ScrapeOps US proxy):

| Category | max_pages | requests | HTTP | items | unique `item_id` | pages @ offsets | `total_count` | on_sale | brands |
|---|---|---|---|---|---|---|---|---|---|
| `Women > What's New` | 2 | 2 | 200 | **200** | 200 | 1/2 @ 0,100 | 1097 | 0 | 91 |
| `Women > Sale` | 2 | 2 | 200 | **200** | 200 | 1/2 @ 0,100 | 8078 | 200 | 100 |
| `Beauty > Beauty > Suncare` | 2 | 1 | 200 | **81** | 81 | 1 @ 0 | 81 | 0 | 25 |
| `Men > Shoes` | 2 | 2 | 200 | **200** | 200 | 1/2 @ 0,100 | 1200 | 0 | 29 |

A random sample of 6 emitted item URLs and 6 image URLs was re-fetched over the proxy: all
12 returned HTTP 200, and all 6 images were real JPEGs (32 KB - 164 KB).

### llbean_listing

`llbean_listing` uses one authoritative source: the first-party UDAL JSON
endpoint `/api/udal/product-discovery/search`. The PLP HTML carries no products
-- the server-rendered `window.__INITIAL_STATE__` blob only holds the page
descriptor with an empty `docs` array -- so there is no HTML path to fall back
to.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl llbean_listing --category "Gift Shop" -a max_pages=2 -O llbean.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"Gift Shop","department":"Gift Shop","item_id":"1000316302","sku_id":"1000316302","title":"Women's The Original Double L® Sweater, Crewneck","brand":"L.L.Bean","url":"https://www.llbean.com/llb/shop/20010334?page=The-Original-Double-L-Crewneck-Novely-Sweater-Womens-Petite","image_url":"https://cdni.llbean.net/is/image/wim/527356_49104_44?wid=302&hei=352","price":49.99,"original_price":69.95,"currency":"USD","rating":4.4,"reviews_count":359,"color":"Classic Navy","size":"X-Small","availability":"IN","on_sale":true,"page":1,"position":1,"total_count":626,"source_url":"https://www.llbean.com/api/udal/product-discovery/search?categoryId=509870&pageSize=48&start=0","source":"llbean_udal_product_discovery","raw":{...}}
```

500 targets across 11 departments come from the homepage
`headerReducer.navData` capture in `llbean_categories.py` (the site
`sitemap.xml` is bot-challenged). Because that capture is flattened one level,
the same leaf name recurs across departments, so `-a category=` names are
qualified with the department -- and, where that still collides, the category id:

```bash
# both forms are valid; the first is unique, the second is disambiguated
common-scrapy crawl llbean_listing --category "Gift Shop"
common-scrapy crawl llbean_listing --category "Clothing / Sweaters [611]"
```

Three behaviours worth knowing before changing the pagination:

- **`start` is the only honoured offset.** The endpoint accepts `pageOffset` /
  `pageNumber` and silently ignores them, so page 2 returns page 1. The spider
  advances `start` by `pageSize` (48) and stops at `response.numFound`.
- **`docs` are one row per SKU, not per product.** The same `itemID_s` /
  `pageID_s` recurs across sizes, so items are de-duplicated on `skuID_s` and
  `item_id` is that same SKU id.
- **A US proxy route is required.** A direct request to a category URL
  302-redirects to the international `global.llbean.com` storefront, so the
  `scrapeops.country=us` route is what returns the real US site.

`price` takes `minSalePrice_f` when present and `original_price` is only carried
when the full price differs; `size` and `rating`/`reviews_count` are `null` for
the SKUs the API omits them for (37/96 and 1/96 respectively on a two-page Gift
Shop run).
### levis_listing

`levis_listing` uses one authoritative source: the LSCO React SSR hydration
blob installed via `Object.defineProperty(window, "__LSCO_INITIAL_STATE__", {value:
{...}})` and read at `ssrViewStoreProductList`. Products are already in the HTML
— there is no `__NEXT_DATA__` and no product XHR to replay — and pagination is a
pure SSR re-render driven by the 0-indexed `?page=<N>` query string. The spider
ships the full header-navigation taxonomy (5 sections / 83 PLP targets from
`levi_categories.py`) plus direct `category_url` or `url` input, and stops on the
`pagination.totalPages` / `currentPage` window, de-duplicating on `code`.

Its ordered `FEED_EXPORT_FIELDS` contract carries the section/group context,
title/brand/url, primary gallery and swatch images, current and pre-discount
prices, discount/rating/review data, merchandising badges, colorway count,
availability flags, the PLP `category_code` and the raw hydrated product record
(`raw` is present on every item).

```bash
rm -f levis-out.csv
HTTPCACHE_ENABLED=False common-scrapy crawl levis_listing --category shop-all-men-s-jeans -a max_pages=2 -O levis-out.csv -s HTTPCACHE_ENABLED=False
```

```json
{"category":"shop-all-men-s-jeans","department":"Men","subcategory":"Men’s Jeans","item_id":"005053473","title":"505™ Regular Dobby Men's Jeans","brand":"Levi's","url":"https://www.levi.com/US/en_US/clothing/men/jeans/straight/505TM-regular-dobby-mens-jeans/p/005053473","image_url":"https://lscoglobal.scene7.com/is/image/lscoglobal/MB_00505-3473_GLO_CM_DA?$qv_desktop_full$","swatch_url":"https://lscoglobal.scene7.com/is/image/lscoglobal/MB_00505-3473_GLO_CL_SW?$swatch$","price":64.99,"original_price":74.95,"currency":"USD","discount_pct":null,"rating":3.8395,"reviews_count":4168,"on_sale":true,"merchant_badge":"Best Seller","promotional_badge":"30% off Applied at Checkout","color_count":22,"coming_soon":false,"sold_out":false,"category_code":"levi_clothing_men_jeans","page":1,"position":1,"total_count":174,"source":"levis_lsco_initial_state_products"}
```
### zappos_listing

`zappos_listing` uses one authoritative source: the server-rendered Redux state
at `window.__INITIAL_STATE__.products.list`. It supports four department
shortcuts plus every captured Department subcategory, direct `category_url` or
`url` input, and follows the HTML `rel=next` link. Its ordered
`FEED_EXPORT_FIELDS` contract includes product/style IDs, price, color, rating,
sale state, crawl context, and the raw hydrated product record.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl zappos_listing --category women -a max_pages=2 -O zappos.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"women","department":"Women","item_id":"8910671","style_id":"4036549","title":"Kiruna Padded Parka","brand":"Fjällräven","color":"Black","price":300.0,"original_price":375.0,"currency":"USD","rating":3.7,"reviews_count":38,"on_sale":true,"page":1,"source":"zappos_initial_state_products"}
```

### uniqlo_listing

`uniqlo_listing` uses one authoritative source: the first-party commerce BFF products
endpoint `https://www.uniqlo.com/us/api/commerce/v5/en/products`. UNIQLO's SSR shell
ships the full navigation taxonomy in `window.__PRELOADED_STATE__.taxonomies` but an
*empty* product grid (`search.search.productIds == []`); the React app hydrates it
client-side over XHR. This spider therefore never scrapes HTML cards or JSON-LD.

- **Taxonomy.** `sample/uniqlo-categories.json` (harvested from `__PRELOADED_STATE__`)
  is committed and flattened by `uniqlo_categories.py` into 2741 selectable URLs:
  4 genders / 46 classes / 212 categories / 2479 subcategories. Every entry keeps the
  Fast Retailing taxonomy id chain the API expects in its `path` query parameter
  (`genderId[,classId[,categoryId[,subCategoryId]]]`), so no page has to be re-resolved.
  Select with `-a category=<slug>` or `-a category_url=<url>` (any of the 2741 URLs).
- **Products.** `GET /us/api/commerce/v5/en/products?path=<ids>&limit=36&offset=<n>`,
  paged via `pagination.total` / `offset`. `max_pages` caps the number of API pages.
- **Identifiers.** `productId` alone is *not* unique: the same `E424873-000` comes back
  once per colourway with a distinct `representativeColorDisplayCode`. UNIQLO's own
  hydration state names rows `<productId>-<colorCode>`, so `item_id` joins the two
  (e.g. `E424873-000-00`) and `style_id` is the numeric style (`424873`).
- **Prices.** `prices.base` is the regular price and `prices.promo` the discounted one,
  so a sale row exports `price` = promo value, `original_price` = base value and
  `on_sale: true`. `on_sale` only fires when the row actually shows two prices
  (`isDualPrice`, or `promo.value != base.value`), so a plain `promo` block that merely
  repeats `base.value` is not treated as a sale. No discounted row appeared in the
  live payloads sampled so far, so this path is covered by unit tests rather than a
  live capture.

```json
{"category":"t-shirts-and-tank-tops","category_name":"T-Shirts and Tank Tops","department":"Women","subcategory":"T-Shirts, Sweats & Fleece","item_id":"E424873-000-00","style_id":"424873","title":"Crew Neck T-Shirt","brand":"UNIQLO","gender":"WOMEN","color":"White","color_code":"00","url":"https://www.uniqlo.com/us/en/products/E424873-000","image_url":"https://image.uniqlo.com/UQ/ST3/us/imagesgoods/424873/item/usgoods_00_424873_3x4.jpg","price":19.9,"original_price":null,"currency":"USD","on_sale":false,"rating":4.7,"reviews_count":2858,"available_sizes":["XXS","XS","S","M","L","XL","XXL"],"page":1,"position":1,"total_count":69,"items_per_page":36,"taxonomy_path":"22210,23295,23335","source":"uniqlo_commerce_bff_products"}
```

Run example:
`HTTPCACHE_ENABLED=False common-scrapy crawl uniqlo_listing -a category=t-shirts-and-tank-tops -a max_pages=2 -O uniqlo.jsonl -s HTTPCACHE_ENABLED=False`

### amazon_search
```json
{
  "asin": "B08NF2W2V2",
  "title": "INZCOU",
  "price": 36.98,
  "url": "https://www.amazon.com/s?k=sneakers",
  "image_url": "https://m.media-amazon.com/images/I/71Akg8OEbXL._AC_UL320_.jpg"
}
```

Run example:
`common-scrapy crawl amazon_search -a q=sneakers -a max_pages=1 -O amazon_search.jsonl`

### amazon_listing (category)

Supported built-in categories:
`electronics`, `fashion`, `beauty`, `home-kitchen`, `toys-games`, `sports-outdoors`, `grocery`, `books`.

Notes:
- Uses Amazon search query URLs (`/s?k=...`) for category shortcuts.
- If a page returns no cards, spider logs a warning with URL/title to help diagnose layout/response changes.

```json
{
  "asin": "B00008BFZH",
  "title": "Snap Circuits Jr. SC-100 Electronics Exploration Kit, Over 100 Projects, Full Color Project Manual, 28 Parts, STEM Educational Toy for Kids 8 +",
  "url": "https://www.amazon.com/Snap-Circuits-SC-100-Electronics-Exploration/dp/B00008BFZH/ref=sr_1_1?...",
  "image_url": "https://m.media-amazon.com/images/I/91THy3rMlCL._AC_UY218_.jpg",
  "price": 29.98,
  "rating": 4.8,
  "reviews_count": 28851,
  "is_prime": false,
  "is_sponsored": false
}
```

Run example:
`common-scrapy crawl amazon_listing -a category=electronics -a max_pages=1 -O amazon_cat.jsonl`

### asos_listing

ASOS page 1 is read from the server-rendered `window.asos.plp._data` bootstrap. Later pages use the search API and carry its query contract, including `keyStoreDataversion`, directly from that bootstrap. The handoff forwards every non-null field of the hydrated `query` object rather than a fixed allowlist, so refined categories keep their `brand`/`sizeFilter`/`priceFilter` refinements on later pages instead of widening back to the bare CID; only browser-only keys (`browsedRegion`, `deliveryCurrency`, `experiment`, …) are dropped. Structured filters are JSON-encoded in the query string, matching the hydrated contract.

The bootstrap currently nests the listing under a `search` object (`state["search"]["products"]`), with the older flat `{products, itemCount, query}` shape still supported. Product fields are normalized from both shapes, since the PLP sends a bare numeric `price` with `description`/`image` while the search API keeps a nested price object with `name`/`imageUrl`.

The `women` and `men` shortcuts target each department's "New In" listing (`cid=27108` / `cid=27110`). The department landing pages themselves (`/us/women/`, `/us/men/`) are navigation-only and serve no listing data, so they cannot be crawled directly. Every other category alias comes from the 412-CID inventory in `asos_categories.py`. Where an alias shares its URL with a department shortcut (`women-view-all` / `men-view-all` both target the same `cid=27108` / `cid=27110` listing), an explicitly supplied `category=` is resolved by its own category key, so those aliases export their own `View all` label rather than the shortcut's `New In`.

Representative output item from the committed fixture:
```json
{
  "category": "custom",
  "subcategory": null,
  "item_id": "211160390",
  "style_id": "158157966",
  "title": "ASOS DESIGN stretch chiffon scarf detail plunge draped maxi dress in chocolate",
  "brand": "ASOS DESIGN",
  "color": "Chocolate",
  "price": 69.99,
  "original_price": 99.99,
  "currency": "USD",
  "total_count": 1591,
  "source": "asos_plp_hydration",
  "raw": {"id": 211160390, "productCode": 158157966, "...": "..."}
}
```

Run example (2 items from the committed hydration fixture):
```bash
python3 -m http.server 8765 --bind 127.0.0.1 &
HTTPCACHE_ENABLED=False python3 -m common_scrapy.cli crawl asos_listing \
  -a category_url=http://127.0.0.1:8765/sample/asos-listing-sample.html \
  -a max_pages=1 -O asos.jsonl -s HTTPCACHE_ENABLED=False -s PROXY=
```

`-s PROXY=` is required for a local fixture run: the project downloader middleware otherwise
forces every request, including `127.0.0.1`, through the configured `PROXY` from `.env`, and
the fixture server answers with a gateway error instead of the sample HTML.

| item_id | title | brand | price | original_price | currency | is_selling_fast |
|---|---|---|---:|---:|---|---|
| 211160390 | ASOS DESIGN stretch chiffon scarf detail plunge draped maxi dress in chocolate | ASOS DESIGN | 69.99 | 99.99 | USD | true |
| 211160391 | Second product | ASOS DESIGN | 45.00 |  | USD | false |

Verification notes:
* The committed fixture exports 2 items and every `FEED_EXPORT_FIELDS` key is present on both, including a populated `raw` (15 keys each). Values are not all non-null: `subcategory` is `null` for a direct-URL crawl and the second item has no `original_price`. The pagination handoff is covered by deterministic contract tests rather than a live crawl.
* The API handoff drops `proxy`/`_auth_proxy` from the copied request meta. `HttpProxyMiddleware` rewrites `meta["proxy"]` to the credential-free URL and stashes the credentialed one in `_auth_proxy`, so forwarding either key would make the follow-up request look pre-authenticated, skip re-attaching `Proxy-Authorization`, and fail the API leg with HTTP 407. `tests/test_asos_listing_spider.py` asserts the follow-up re-applies proxy authentication end to end.
* Live output is currently **unverified**: a direct cache-disabled storefront attempt from this runner did not complete, so no live item count or `total_count` is claimed here. Treat `category=women` / `category=men` runs as unverified until run against the real storefront.
* In this sandbox Scrapy receives a 407 on the proxy CONNECT tunnel for the API leg specifically, while `curl` succeeds on an identical URL. The generated API URL is correct; the page-1 hydration leg is unaffected. Treat multi-page runs as unverified locally until run on a host without the TLS-intercepting middlebox.
* An Akamai access-denied/challenge page is detected before hydration extraction and fails with a targeted message rather than a generic "no valid hydration" error.

### walmart_listing (category)
```json
{
  "url": "https://www.walmart.com/ip/W-NB-HORSEBIT-LOAFER/19231301884?...",
  "page": 1,
  "position": 20,
  "productId": "19231301884",
  "usItemId": "19231301884",
  "offerId": "22830F1D3D4938EEA4A44EC7DE147CFF",
  "title": "No Boundaries Women's Faux Leather Loafers",
  "brand": "No Boundaries",
  "productType": "Casual & Dress Shoes",
  "sellerId": "F55CDC31AB754BB68FE0B39041159D63",
  "sellerName": "Walmart.com",
  "imageUrl": "https://i5.walmartimages.com/seo/W-NB-HORSEBIT-LOAFER_...jpeg",
  "currency": "USD",
  "price": 26.98,
  "currentPrice": 26.98,
  "rating": 4.6,
  "reviewsCount": 35,
  "availabilityStatus": "IN_STOCK",
  "isOutOfStock": false,
  "fulfillmentType": "STORE",
  "badgeText": "Best seller",
  "badgeKey": "BESTSELLER",
  "isSponsored": false,
  "variantCount": 0,
  "variants": []
}
```

Run example:
`common-scrapy crawl walmart_listing -a category=electronics -a max_pages=1 -O walmart.jsonl`

### walmart_search (keyword)
```json
{
  "item_id": "13542163431",
  "title": "ASUS Vivobook Go 15.6” Laptop, Intel i3-N305, 8GB, 256GB, Windows 11 Home in S mode, Cool Silver, E1504GA-WS35",
  "url": "https://www.walmart.com/sp/track?.../ip/.../13542163431",
  "image_url": "https://i5.walmartimages.com/seo/...jpeg?odnHeight=288&odnWidth=288&odnBg=FFFFFF",
  "price": 269.0,
  "rating": null,
  "reviews_count": null,
  "is_sponsored": false,
  "source": "walmart_html"
}
```

Run example:
`common-scrapy crawl walmart_search -a q=laptop -a max_pages=1 -O walmart_search.jsonl`

Notes:
- Uses the same HTML parser as `walmart_listing`.
- Walmart frequently serves a **"Robot or human?"** challenge depending on IP/proxy reputation; when blocked, no items are emitted and the spider logs a warning.
- Browser inspection on `https://www.walmart.com/search?q=laptop` confirmed product cards + price blocks are present in rendered HTML in this runtime.
- NordVPN US city checks (`max_pages=1`, `q=laptop`) returned stable output across Ashburn (`us11646`), Dallas (`us9147`), and Los Angeles (`us5381`) with 13 items each.

### ebay_search (keyword; Marko hydration state)
```json
{
  "productId": "234346994063",
  "title": "MacBook Pro 15 Inch 256GB SSD 16 GB i7 3.40Ghz Apple Retina Big Sur 3yr Warranty",
  "url": "https://www.ebay.com/itm/234346994063?...",
  "price": 439.0,
  "currency": "USD",
  "originalPrice": 878.0,
  "originalCurrency": "USD",
  "discountPercentage": 50.0,
  "imageUrl": "https://i.ebayimg.com/images/g/tLEAAOSwzOJjKIz4/s-l400.webp",
  "imageUrls": [
    "https://i.ebayimg.com/images/g/tLEAAOSwzOJjKIz4/s-l400.webp",
    "https://i.ebayimg.com/images/g/md4AAOSwGwFiJjhM/s-l400.webp",
    "https://i.ebayimg.com/images/g/SSkAAOSwYEphOWNZ/s-l400.webp",
    "https://i.ebayimg.com/images/g/WIkAAOSwTkxiJjhV/s-l400.webp"
  ],
  "condition": "Pre-Owned",
  "brand": "Apple",
  "quantityAvailable": 1,
  "quantityText": "1 remaining",
  "shippingCost": 0.0,
  "shippingCurrency": "USD",
  "shippingText": "Free shipping",
  "deliveryText": "Est. delivery Sat, Sep 19",
  "isSponsored": true,
  "position": 60,
  "mode": "keyword",
  "query": "laptop",
  "page": 1,
  "sourceUrl": "https://www.ebay.com/sch/i.html?_nkw=laptop&_ipg=60"
}
```

Run example:
`common-scrapy crawl ebay_search -a q=laptop -a max_pages=1 -O ebay_search.jsonl`

Notes:
- The example omits the large `raw` eBay `ListingItemCard` payload for readability.
- Products are extracted directly from eBay's Marko hydration data and normalized from `ListingItemCard` records.
- Non-listing Marko records and promotional cards are ignored.
- The Marko extraction path is stable and returned 60 items with `q=laptop` and `max_pages=1`.

### ebay_listing (category; Marko hydration state)

```json
{
  "productId": "234346994063",
  "title": "MacBook Pro 15 Inch 256GB SSD 16 GB i7 3.40Ghz Apple Retina Big Sur 3yr Warranty",
  "url": "https://www.ebay.com/itm/234346994063?...",
  "price": 439.0,
  "currency": "USD",
  "originalPrice": 878.0,
  "originalCurrency": "USD",
  "discountPercentage": 50.0,
  "imageUrl": "https://i.ebayimg.com/images/g/tLEAAOSwzOJjKIz4/s-l400.webp",
  "imageUrls": [
    "https://i.ebayimg.com/images/g/tLEAAOSwzOJjKIz4/s-l400.webp",
    "https://i.ebayimg.com/images/g/md4AAOSwGwFiJjhM/s-l400.webp",
    "https://i.ebayimg.com/images/g/SSkAAOSwYEphOWNZ/s-l400.webp",
    "https://i.ebayimg.com/images/g/WIkAAOSwTkxiJjhV/s-l400.webp"
  ],
  "condition": "Pre-Owned",
  "brand": "Apple",
  "quantityAvailable": 1,
  "quantityText": "1 remaining",
  "shippingCost": 0.0,
  "shippingCurrency": "USD",
  "shippingText": "Free shipping",
  "deliveryText": "Est. delivery Sat, Sep 19",
  "isSponsored": true,
  "position": 60,
  "category": "Electronics",
  "subCategory": "Apple",
  "page": 1,
  "listingUrl": "https://www.ebay.com/b/Apple-Laptops-Netbooks/175672/bn_2780164"
}
```

Run example:
`common-scrapy crawl ebay_listing -a category=Electronics -a max_pages=1 -O ebay_listing.jsonl`

Notes:
- The example omits the large `raw` eBay `ListingItemCard` payload for readability.
- Products are extracted directly from eBay's Marko hydration data and normalized from `ListingItemCard` records.
- The Marko product extraction path is stable; HTML parsing is used only to discover nested browse categories.
- A top-level category request crawls each configured subcategory in `common/spiders/ebay_categories.py`.
- Product pages emit commerce fields such as current/original price, discount, seller feedback, condition, shipping, delivery, returns, listing type, bid/sold counts, and sponsorship status when present.
- Browse pages such as the Antiques fixture contain destination tiles rather than products; these are extracted as `subCategory`/`url` pairs and followed until listing pages are reached.
- All emitted eBay field names use camelCase.

### homedepot_search (keyword; Apollo bootstrap)

```json
{
  "item_id": "204663533",
  "sku": "1000024249",
  "brand": "Husky",
  "title": "Screwdriver Set (2-Piece)",
  "model": "246340020",
  "url": "https://www.homedepot.com/p/Husky-Screwdriver-Set-2-Piece-246340020/204663533",
  "image_url": "https://images.thdstatic.com/productImages/08052130-f21b-4366-93a8-9faecad0ba34/svn/husky-screwdriver-sets-246340020-64_300.jpg",
  "price": 6.97,
  "original_price": 6.97,
  "rating": 4.63,
  "reviews_count": 227,
  "source": "homedepot_apollo_bootstrap",
  "mode": "keyword",
  "query": "screwdriver",
  "category_url": null,
  "page": 1
}
```

Run example:
`common-scrapy crawl homedepot_search -a q='screwdriver' -a max_pages=1 -O homedepot_search.jsonl`

### homedepot_listing (category; Apollo state)

Supported built-in categories:
`appliances`, `bath`, `building-materials`, `decor-and-furniture`, `electrical`, `flooring`, `hardware`, `heating-and-cooling`, `kitchen`, `lawn-and-garden`, `lighting`, `paint`, `plumbing`, `storage`, `tools`.

```json
{
  "category": "tools",
  "item_id": "100000001",
  "sku": "1000000001",
  "title": "16 oz. Fiberglass Claw Hammer",
  "brand": "Husky",
  "model": "N-G16CHD",
  "url": "https://www.homedepot.com/p/Husky-16-oz-Fiberglass-Claw-Hammer-N-G16CHD/100000001",
  "image_url": "https://images.thdstatic.com/productImages/hammer_300.jpg",
  "price": 14.97,
  "original_price": 17.97,
  "currency": "USD",
  "rating": 4.7,
  "reviews_count": 238,
  "availability": "InStock",
  "source": "homedepot_apollo_state",
  "category_url": "https://www.homedepot.com/b/Tools/N-5yc1vZc1xy",
  "page": 1
}
```

Run example:
`common-scrapy crawl homedepot_listing -a category=tools -a max_pages=1 -O homedepot_listing.jsonl`

Notes:
- Products are extracted from the PLP's embedded `window.__APOLLO_STATE__`; missing Apollo state or product references fail the crawl visibly instead of emitting a silent empty feed.
- Output uses a fixed 17-field export order: category, identifiers, product details, pricing, reviews, availability, source, category URL, and page.
- Duplicate Apollo references are removed by item ID. Additional pages use Home Depot's `Nao` offset in increments of 24.
- A direct live request returned Home Depot's 403 anti-bot response during the latest verification. The checked-in representative fixture emitted 2 products and is covered by deterministic contract tests.

### maccosmetics_listing (Shopify collection catalog)

MAC Cosmetics now exposes its current catalog through Shopify collection pages. The
spider includes all 79 collections published in the store sitemap and parses the
server-rendered Shopify analytics catalog as its authoritative product source.

```bash
scrapy crawl maccosmetics_listing -a category=face -a max_pages=1 \
  -s HTTPCACHE_ENABLED=False -O maccosmetics_listing.jsonl
```

The stable `FEED_EXPORT_FIELDS` contract exports category, Shopify product ID,
SKU, title, brand, product type, product and image URLs, USD price, page, source,
and the raw catalog object. Collection pagination is followed up to `max_pages`.

### macys_listing
```json
{
  "item_id": "25092672",
  "title": "Floral Stickers Laptop, 74 Pcs, Stickers for Water Bottles,",
  "brand": "Mr. Pen",
  "price": 6.99,
  "price_text": "$6.99",
  "url": "https://www.macys.com/shop/product/floral-stickers-laptop-74-pcs-stickers-for-water-bottles?ID=25092672",
  "image_url": "7/optimized/34925717_fpx.tif",
  "source": "macys_xapi_discover_v1_page"
}
```

### ulta_listing (category)

GraphQL-only listing: discover the current `ProductListingResults` module with
`Page`, then request its cards with `NonCachedPage`. No fixed content or visitor
IDs are required. Product requests supply the desktop breakpoint (`XL`) and
anonymous login status. Requests use JSON POST and retain the module ID while paginating
with `page=N`. An empty first page triggers one rediscovery attempt; blocked,
invalid, exhausted, or repeated results terminate without HTML fallback.

```sh
common-scrapy crawl ulta_listing -a category=makeup -a max_pages=2 -O ulta.jsonl
```

Categories are a name-to-URL dictionary: `makeup`, `skin-care`, `hair-care`,
`fragrance`, `body-care`.
Use `-a url='https://www.ulta.com/shop/makeup/eyes/mascara'` with a category
label to override the route.

The item schema and export columns remain unchanged: original Ulta card fields
plus `category`. Illustrative exported card (abbreviated):

```json
{
  "category": "makeup",
  "productId": "pimprod1",
  "skuId": "123",
  "brandName": "Brand",
  "productName": "Mascara",
  "action": {"url": "/p/mascara-pimprod1?sku=123"},
  "image": {"imageUrl": "https://media.ultainc.com/i/ulta/123"},
  "listPrice": "$20",
  "salePrice": "$15",
  "rating": "4.5",
  "reviewCount": "1,234",
  "sponsored": false
}
```

Validation (2026-09-23): terminal crawl with `category=makeup`, `max_pages=2`
returned **152 product records with 152 distinct SKUs** through the configured
proxy. All 3 requests (discovery plus 2 product pages) returned HTTP 200, and the
spider finished normally. Direct egress returned HTTP 403. All 10 Ulta regression
tests pass, including authenticated proxy handoff, unchanged item schema,
discovery, pagination, bounded rediscovery, and error termination.

Validation command (disable the development item cap to verify both pages):

```sh
pipenv run scrapy crawl ulta_listing -a category=makeup -a max_pages=2 -s HTTPCACHE_ENABLED=False -s CLOSESPIDER_ITEMCOUNT=0 -O /tmp/ulta-issue60-verified.jsonl
```

Run regression tests: `python -m unittest discover -s tests -p 'test_ulta*' -v`.

### ulta_search (keyword)

```json
{
  "item_id": "xlsImpprod15511061",
  "sku_id": "2580410",
  "brand": "Redken",
  "title": "All Soft Shampoo",
  "url": "https://www.ulta.com/p/all-soft-shampoo-xlsImpprod15511061?sku=2580410",
  "image_url": "https://media.ultainc.com/i/ulta/2580410",
  "list_price": "$11.00 - $56.00",
  "rating": 4.1,
  "reviews_count": 1601,
  "is_sponsored": false,
  "source": "ulta_dxl_graphql"
}
```

Run examples:
- GraphQL mode (recommended):
  `common-scrapy crawl ulta_search -a q=shampoo -a mode=graphql -a max_pages=1 -O ulta_search.jsonl`
- HTML fallback mode:
  `common-scrapy crawl ulta_search -a q=shampoo -a mode=html -a max_pages=1 -O ulta_search_html.jsonl`

Notes:
- `mode=graphql` is the stable path for normalized fields.
- For reliability, run via US residential egress/VPN (validated from NordVPN US Dallas).

### kohls_listing
```json
{
  "item_id": "12345678",
  "title": "Women's ...",
  "url": "https://www.kohls.com/product/prd-...",
  "price": 29.99,
  "regular_price": 39.99,
  "sale_price": 29.99,
  "brand": "SONOMA Goods for Life",
  "source": "kohls_web_catalog_api"
}
```
Run example:
`common-scrapy crawl kohls_listing -a category=women -a max_pages=1 -O kohls_listing.jsonl`

### sephora_listing
```json
{
  "item_id": "P517483",
  "title": "Pocket Blush Buildable Hydrating Cream Blush",
  "url": "https://www.sephora.com/product/pocket-blush-P517483?skuId=2895845",
  "brand": "rhode",
  "rating": 4.0598,
  "reviews_count": 1153,
  "source": "sephora_catalog_api"
}
```
Run example:
`common-scrapy crawl sephora_listing -a category=makeup -a max_pages=1 -O sephora_listing.jsonl`

### stockx_listing
```json
{
  "item_id": "9acafeb5-bc4a-4d66-bc3a-4899d2e64775",
  "title": "Jordan 4 Retro Toro Bravo (2026)",
  "brand": "Jordan",
  "price": 155,
  "highest_bid": 347,
  "last_sale_price": 153,
  "currency": "USD",
  "url": "https://stockx.com/air-jordan-4-retro-toro-bravo-2026",
  "product_category": "sneakers",
  "source": "stockx_next_data_browse"
}
```
Run example:
`common-scrapy crawl stockx_listing -a category=sneakers -a max_pages=1 -O stockx_listing.jsonl`

The spider reads the authoritative `browse.results` query from StockX's
`__NEXT_DATA__` state, follows its `pageCount`, and deduplicates products by ID.
Available categories are `sneakers`, `apparel`, `electronics`, `trading-cards`,
and `collectibles`.

### adorama_listing

Adorama listing pages are Next.js SSR routes (`/l/[[...param]]`). The spider reads a
single authoritative data path: the hydration payload in
`script#__NEXT_DATA__` -> `props.pageProps.products[]` (24 products per page).
There is no HTML-card or XHR fallback. Pagination is query-based and follows
`pageProps.nextPageUrl` (`?startAt={n}`, 24 per page); SKUs are deduplicated
across pages.

`common/spiders/adorama_categories.py` ships the normalized taxonomy
(11 departments, 1,090 `/l/` URLs), re-derived from Adorama's category sitemap
(`https://www.adorama.com/UnifySiteMaps/Category.xml`). Depth-1 department
landings (`pageInfo.pageType == "bcmsSitePage"`, no product grid) are excluded,
leaving **1,079** crawlable depth-2+ categories exposed as `-a category=<slug>`.

Adorama is DataDome-protected; live requests require the configured US proxy.

```json
{
  "category": "cameras",
  "item_id": "KKRK0603A",
  "title": "Kodak Charmera Millenium Edition 1.6MP Keychain Digital Camera, w/32GB Card",
  "brand": "Kodak",
  "url": "https://www.adorama.com/kodak-charmera-millenium-edition-keychain-camera-1-6-mp/p/kkrk0603a",
  "image_url": "https://www.adorama.com/images/product/KKRK0603A.JPG",
  "price": 54.94,
  "currency": "USD",
  "stock": "In",
  "in_stock": true,
  "is_available_for_purchase": true,
  "page": 1,
  "page_type": "listPage",
  "source": "adorama_next_data"
}
```

Run example:
`HTTPCACHE_ENABLED=False common-scrapy crawl adorama_listing -a category=cameras -a max_pages=2 -O adorama.jsonl  -s HTTPCACHE_ENABLED=False`

### staples_listing

Staples listings use one data path: `props.initialStateOrStore.searchState.productTileData`
inside the server-rendered `script#__NEXT_DATA__`. Pagination follows `link[rel=next]`.
The sitemap inventory includes 34 roots and 208 subcategories; `binders` is a verified
product-bearing leaf. Direct Staples requests may require the configured US proxy.

```json
{
  "category": "binders",
  "item_id": "82656",
  "title": "Staples 1\" 3-Ring View Binder, D-Ring, White (55406/26432)",
  "brand": "Staples",
  "model": "55406/26432",
  "price": 10.09,
  "currency": "USD",
  "rating": 4.68,
  "reviews_count": 1543,
  "in_stock": true,
  "page": 1,
  "source": "staples_next_data"
}
```

Run example:
`HTTPCACHE_ENABLED=False common-scrapy crawl staples_listing -a category=binders -a max_pages=2 -O staples.jsonl -s HTTPCACHE_ENABLED=False`

### rightmove_listing

Rightmove listings use one product-data path: `props.pageProps.searchResults.properties`
inside the server-rendered Next.js Pages Router `script#__NEXT_DATA__`. The spider maps
property, price, location, media, agent and search-context fields directly from that
hydration; it does not use HTML cards or JSON-LD as a fallback. The deterministic taxonomy
contains 20 high-inventory UK cities. Pagination follows the hydrated `pagination.next`
offset as `?index=N`, bounded by `pagination.total`, Rightmove's 42-page cap and `max_pages`.
The ordered `FEED_EXPORT_FIELDS` contract covers stable property identity, price,
location, property details, media, agent and search-context metadata, the provenance
`source=rightmove_next_data`, the authoritative raw property record (`raw`), and a
per-item `timestamp`.

```json
{
  "category": "london",
  "item_id": "89825950",
  "title": "Tottenham Street, Fitzrovia, W1",
  "price": 680000,
  "price_display": "£680,000",
  "price_currency": "GBP",
  "bedrooms": 1,
  "property_type": "1 bedroom flat for sale",
  "source": "rightmove_next_data"
}
```

Run example:
`scrapy crawl rightmove_listing -a category=london -a max_pages=1 -O rightmove.jsonl -s HTTPCACHE_ENABLED=False`

### petco_listing

Petco listings use one data path: `props.pageProps.pageData.constructorResults.response`
inside the server-rendered `script#__NEXT_DATA__`. That object carries the whole
first-party Constructor.io response used to paint the grid, so the spider needs a single
request per page and no HTML/JSON-LD fallback:

- `response.results[]` — grid rows. Each row holds a `data` block (the default/first
  variation: `itemname`, `mfName`, `rdprice`, `listprice`, `AverageRating`,
  `TotalReviewCount`, `catEntryID`, `parentCatEntryID`, `image_url`, `url`, `facets[]`,
  `group_ids[]`, `PTC_OMNI_*` flags) plus `variations[]` (the remaining size variants,
  exported as `variants_count` / `variant_ids`).
- `response.total_num_results` — category total (433 for `dry-cat-food`, 1059 for
  `dry-dog-food` at authoring time); `constructorResults.request` echoes `page`,
  `num_results_per_page` (48), `sort_by` and `sort_order`.
- `response.facets[]`, `response.groups[]`, `response.sort_options[]`, plus
  `pageData.breadcrumbs[]`, `pageData.categoryId` and `pageData.h1title`.

Pagination is plain SSR `?page=N` (the parameter is replaced, never appended), bounded by
`max_pages` and by `page * items_per_page < total_num_results`; rows are de-duplicated by
`item_id` (`catEntryID`). `in_stock` is derived from price presence — the grid only returns
priced rows and the hydration carries no stock flag.

`petco_categories.py` holds the full inventory taken from the mega-menu (22 roots / 286
nodes); `-a category=` takes the slug of the whole category path so departments never
collide (`cat-cat-food-dry-cat-food`, `dog-dog-food-dry-dog-food`). `-a url=` also accepts
any PLP URL directly.

```json
{
  "category": "cat-cat-food-dry-cat-food",
  "department": "Cat",
  "subcategory": "Dry Cat Food",
  "category_id": "10195",
  "category_name": "Dry Cat Food & Kibble",
  "breadcrumb_path": "Cat Supplies > Cat Food > Dry Cat Food & Kibble",
  "item_id": "6848523",
  "title": "Purina Cat Chow Indoor Healthy Weight and Hairball with Chicken Dry Cat Food, 15 lbs.",
  "brand": "Purina Cat Chow",
  "price": 18.99,
  "original_price": 19.99,
  "currency": "USD",
  "rating": 4.8141,
  "reviews_count": 3770,
  "in_stock": true,
  "variants_count": 2,
  "page": 1,
  "position": 1,
  "total_count": 433,
  "items_per_page": 48,
  "search_engine": "constructor.io",
  "source": "petco_next_data"
}
```

Run example:
`HTTPCACHE_ENABLED=False common-scrapy crawl petco_listing -a category=cat-cat-food-dry-cat-food -a max_pages=2 -O petco.jsonl -s HTTPCACHE_ENABLED=False`

Run example (raw page URL, e.g. to start on page 2):
`HTTPCACHE_ENABLED=False common-scrapy crawl petco_listing -a url="https://www.petco.com/shop/en/petcostore/category/cat/cat-food/dry-cat-food?page=2" -O petco.jsonl -s HTTPCACHE_ENABLED=False`
### belk_listing

Belk listings use **one** data path: the first-party search facade that the site itself calls.
The category HTML carries the Next.js App Router React Flight mega-menu but deliberately
does **not** contain product records, and there is no JSON-LD to fall back on.

```text
https://www.belk.com/ecom/cio/v1/web/category/{categoryPath}?v2=true&start={offset}&sz=60
```

`product_tiles` holds the full record for each item (brand, original/sale price ranges,
coupons, `promotions` such as `BOGO`, badge, colour swatches, rating/review count) and
`header.count` carries the category total. Pagination is offset based: the API advertises
the next offset itself in `pagination.navs[*].params` (`start=60&sz=60`), which the spider
reuses, and `max_pages` bounds the run.

`belk_categories.py` holds the inventory extracted from the homepage mega-menu
(`self.__next_f.push([1, ...])` → `categories.desktop.categories`): **13 departments, 741 nav
nodes, max depth 4, 427 unique browse categories**. Two mega-menu details are handled
explicitly — `/search/` "Shop All..." shortcuts are not categories (but their real browse
children still are), and a cross-linked path such as `/fan-gear/` is reported under its
shallowest (real) department rather than whichever department linked it first.

Note that `https://www.belk.com/sitemap_29-category.xml` advertises 8,489 category URLs but
is **stale** — it still lists paths the API no longer resolves — so it is not used as the
taxonomy source.

Two categories in the inventory are landing pages rather than PLPs (`/clearance/`,
`/brands/designer-brands/`); the API answers those with `{"metaData": {"redirectUrl": ...}}`
and the spider raises a loud error naming the redirect instead of emitting zero items.

```json
{
  "category": "shoes/womens-shoes/flats",
  "department": "Shoes",
  "subcategory": "Women's Shoes > Flats",
  "category_id": "shoes-womens-shoes-flats",
  "item_id": "2900965MULANEYW",
  "title": "Mulaney Flats",
  "brand": "DV Dolce Vita",
  "url": "https://www.belk.com/p/dv-dolce-vita-mulaney-flats/2900965MULANEYW.html",
  "price": 45.5,
  "original_price": 65.0,
  "discount_percent": 30.0,
  "currency": "USD",
  "badge": "badge-db-buys",
  "color": "IVORY",
  "swatches": ["IVORY"],
  "page": 1,
  "position": 1,
  "total_count": 1637,
  "source": "belk_cio_category_api"
}
```

Run examples:
`HTTPCACHE_ENABLED=False common-scrapy crawl belk_listing -a category=shoes/womens-shoes/flats -a max_pages=1 -O belk.jsonl -s HTTPCACHE_ENABLED=False`
`common-scrapy crawl belk_listing -a category=home/home-decor -a max_pages=3 -O belk_home.jsonl`
`common-scrapy crawl belk_listing -a category_url=https://www.belk.com/jewelry/fashion-jewelry/bracelets/ -O belk_bracelets.jsonl`

`-a category=` accepts the full browse path (`shoes/womens-shoes/flats`) or an unambiguous
trailing segment (`flats`); `-a category_url=` and `-a url=` accept a browse page URL or a
ready-made API URL.

### fashionnova_listing
```json
{
  "item_id": "123456789",
  "title": "Curve Appeal Maxi Dress - Black",
  "url": "https://www.fashionnova.com/products/curve-appeal-maxi-dress-black",
  "price": 39.99,
  "currency": "USD",
  "brand": "Fashion Nova",
  "source": "fashionnova_storefront_graphql"
}
```
Run examples:
- `common-scrapy crawl fashionnova_listing -a category=women -a max_pages=1 -O fashionnova_listing.jsonl`
- `common-scrapy crawl fashionnova_listing -a category=women -a mode=html -a max_pages=1 -O fashionnova_listing_html.jsonl`

### anthropologie_listing

Extracts one authoritative source: the `category.pages[page].wrapper.tiles` product records in the server-rendered `urbnInitialPiniaState` Pinia payload. The captured inventory contains nine US/CA category and refinement URLs in `common/spiders/anthropologie_categories.py`. Pagination uses the `page` query parameter and the hydrated `totalPages` value; duplicate product IDs are suppressed across pages. A starting `page` encoded in the selected URL is preserved (so the `womens-clothing-page-2` alias crawls page 2, not page 1), and product links keep the crawled storefront locale (`/en-ca/` URLs export `/en-ca/shop/...` links). `currency` prefers a hydrated currency code and otherwise follows the crawled storefront (`CAD` for `/en-ca/`, `USD` for the US site). Missing or malformed hydration and pages without product records fail visibly. Every exported item carries the full hydrated `raw` tile record.

Run with cache disabled:

`HTTPCACHE_ENABLED=False common-scrapy crawl anthropologie_listing -a category=womens-clothing -a max_pages=1 -O anthropologie_listing.jsonl`

Exported fields are `category`, `item_id`, `style_number`, `title`, `brand`, `url`, `image_url`, `price`, `original_price`, `currency`, `availability`, `rating`, `reviews_count`, `color`, `color_count`, `badges`, `source`, `category_url`, `page`, `position`, and `raw`.

```json
{
  "item_id": "AN-4114086690121-000",
  "style_number": "4114086690121",
  "title": "By Anthropologie Goldie 100% Cashmere Sweater",
  "brand": "By Anthropologie",
  "url": "https://www.anthropologie.com/shop/by-anthropologie-goldie-100-cashmere-sweater?color=702&type=STANDARD",
  "price": 138.0,
  "original_price": 138.0,
  "currency": "USD",
  "availability": "InStock",
  "rating": 4.5869,
  "reviews_count": 656,
  "color_count": 29,
  "source": "urbn_pinia_hydration",
  "category_url": "https://www.anthropologie.com/womens-clothing?page=1",
  "page": 1
}
```
Run example:
`common-scrapy crawl anthropologie_listing -a category=womens-clothing -a max_pages=1 -O anthropologie_listing.jsonl`

Notes:
- Direct traffic may receive HTTP 403; the 2026-09-29 live verification used the configured US proxy and exported 37 unique products from HTTP 200. A 2026-10-02 re-verification attempt returned HTTP 403 again (PerimeterX), so the 37 figure is the most recent successful live run and the current item count is unconfirmed.
- Direct `-a url=<listing-url>` and `-a category_url=<listing-url>` runs are supported; a bare run with no target fails with the available category list.
- The spider intentionally does not fall back to DOM cards or another endpoint when the hydration contract is absent.

### lululemon_listing
Run example:
`common-scrapy crawl lululemon_listing -a category=women-shorts -a max_pages=1 -O lululemon_listing.jsonl`

### jcpenney_listing
Extracts the authoritative `organicZoneInfo.products` collection from JCPenney's
search-service JSON endpoint. The stable `FEED_EXPORT_FIELDS` contract includes
category and page context, identifiers, pricing, rating, media, and the raw source
record. The endpoint is protected by Akamai and fails visibly when its expected
JSON contract is unavailable.

Run example:
`common-scrapy crawl jcpenney_listing -a category=womens_tops -a max_pages=1 -O jcpenney_listing.jsonl`

### dillards_listing
Extracts the authoritative `CatalogEntryList` from Dillard's `window.__INITIAL_STATE__` bootstrap data. The category inventory covers 10 top-level departments and 124 current child listing URLs; selecting a department crawls every child and deduplicates products by catalog entry ID. Pagination uses Dillard's `pageNumber` query parameter and is bounded by `max_pages` per child listing.

Run example:
`common-scrapy crawl dillards_listing -a category=women -a max_pages=1 -O dillards_listing.jsonl`

Current category names: `women`, `lingerie`, `juniors`, `shoes`, `handbags`, `accessories`, `men`, `kids`, `home`, `beauty`.

The site is protected by Akamai and may return an HTTP 200 access-denied page from datacenter IPs. Use the configured residential proxy; the spider deliberately stops when the authoritative bootstrap contract is absent.

### poshmark_listing
```json
{
  "category": "women",
  "item_id": "62bdd4097028ec9dd68ee867",
  "title": "Size Large solid black yoga pants by Canta Bella",
  "brand": "Canta Bella",
  "url": "https://poshmark.com/listing/Size-Large-solid-black-yoga-pants-by-Canta-Bella-62bdd4097028ec9dd68ee867",
  "price": 11.0,
  "currency": "USD",
  "source": "poshmark_bootstrap_initial_state"
}
```
Run example:
`common-scrapy crawl poshmark_listing -a category=women -a max_pages=1 -O poshmark_listing.jsonl`

Notes:
- Verified while connected to NordVPN US endpoints (Seattle and Los Angeles).
- Category pages expose `window.__INITIAL_STATE__` with listing records at `$_category.gridData.data`.

### bloomingdales_listing
```json
{
  "item_id": "1234567",
  "title": "AQUA ...",
  "url": "https://www.bloomingdales.com/shop/product/...",
  "price": 198.0,
  "price_text": "$198.00",
  "original_price": 248.0,
  "original_price_text": "$248.00",
  "image": "https://...",
  "brand": "AQUA",
  "rating": 4.6,
  "review_count": 12,
  "category": "women",
  "category_root_url": "https://www.bloomingdales.com/shop/womens-apparel?id=2910",
  "subcategory_urls": ["https://www.bloomingdales.com/shop/womens-apparel/dresses?id=21683"],
  "facet_urls": [],
  "source": "bloomingdales_nuxt_state"
}
```
Run example:
`common-scrapy crawl bloomingdales_listing -a category=women -a max_pages=1 -O bloomingdales_listing.jsonl`

Contract notes:
- Supported top-level categories are `new-now`, `women`, `beauty`, `shoes`, `handbags`, `jewelry-accessories`, `men`, `kids`, `home`, `sale`, `gifts`, and `designers`.
- The spider accepts category selection only; direct `url` and `category_url` overrides are not used.
- Uses a single authoritative parser for `<script type="application/json" data-nuxt-data="nuxt-app" data-ssr="true">...` state.
- A top-level category splash starts every discovered leaf browse URL before pagination.
- Category payload URLs are normalized into `subcategory_urls` and `facet_urls` metadata on emitted items.
- Access-denied/block pages raise a visible runtime error.

### qvc_listing

QVC renders the initial category product grid in HTML. The spider treats
`#searchResults .galleryItem[data-item-id]` as the authoritative product source;
it does not call the product-list endpoint found in QVC's JavaScript configuration
because the captured category page did not use that endpoint to populate its grid.

```json
{
  "category": "beauty",
  "category_id": "NAV6285",
  "item_id": "A740517",
  "title": "Whish 12 Days of Beauty Whishes Advent Calendar",
  "brand": null,
  "url": "https://www.qvc.com/whish-12-days-of-beauty-whishes-advent-calendar.product.A740517.html?sc=NAVLIST",
  "image_url": "https://qvc.scene7.com/is/image/QVC/a/17/a740517.001?$aemprodgallery80$",
  "price": 59.98,
  "original_price": 73.0,
  "currency": "USD",
  "rating": null,
  "reviews_count": null,
  "badge": "Today's Special Value",
  "shipping_promo": "Free Standard S&H",
  "special_price_code": "TSV",
  "installment_count": 3,
  "colors_count": 0,
  "total_products": 5326,
  "page": 1,
  "source": "qvc_server_rendered_gallery_with_utag_state"
}
```

Run example:

`common-scrapy crawl qvc_listing -a category=fashion -a max_pages=1 -O qvc_listing.jsonl`

Contract notes:

- The built-in category is `fashion`. A direct page can also be supplied with
  `-a url=<category-url>` or `-a category_url=<category-url>` while retaining a
  category label.
- The fixed 20-field export contract includes product identity, URLs, prices,
  ratings, merchandising badges, shipping promotion, installment count, color
  count, category ID, page number, and listing total.
- `utag_data` supplies `category_id` and `currentPage`; card extraction still
  works when that optional bootstrap object is absent.
- Pagination follows QVC's canonical `<link rel="next">` and stops at
  `max_pages`. Products are deduplicated by `item_id` across pages.
- If the expected gallery is missing, the spider logs
  `QVC product grid unavailable` and emits no fallback data.
- QVC is protected by Akamai. Direct requests from some networks return HTTP
  `418`; use a permitted, appropriately configured proxy route and disable the
  Scrapy HTTP cache when validating live behavior.

### poshmark_listing
Poshmark category pages expose their first 48 listing records in the server-rendered
`window.__INITIAL_STATE__` payload. The spider deliberately uses only that authoritative
bootstrap payload and exports a stable field order through `FEED_EXPORT_FIELDS`.
Each exported item also includes the complete source listing object in `raw`.

Supported categories are `women`, `men`, `kids`, `home`, `electronics`, and `pets`.

Run example:
`common-scrapy crawl poshmark_listing -a category=women -a max_pages=1 -s HTTPCACHE_ENABLED=False -O poshmark_listing.jsonl`

### saksfifthavenue_listing (category)
```json
{
  "item_id": "0400026449047",
  "title": "Prada Washed Re Nylon Rain Jacket",
  "url": "https://www.saksfifthavenue.com/product/prada-washed-re-nylon-rain-jacket-0400026449047.html?dwvar_0400026449047_color=GREY",
  "price": 6200.0,
  "price_text": "$6,200",
  "source": "saksfifthavenue_direct_html"
}
```
Run example:
`common-scrapy crawl saksfifthavenue_listing -a category=women -a max_pages=1 -O saksfifthavenue_listing.jsonl`

Notes:
- Saks is heavily anti-bot protected (DataDome). Direct HTTP requests may return `403` challenge pages from some runtimes/IPs.
- Treat this spider as **best-effort/experimental**; verify output quality in your target environment before relying on unattended runs.

### target_search
```json
{
  "product_id": "xxxxx",
  "name": "…",
  "price": "$…",
  "url": "https://www.target.com/p/...",
  "image": "https://target.scene7.com/is/image/Target/..."
}
```

Run example:
`common-scrapy crawl target_search -a category=5xtc0 -a max_pages=1 -O target.jsonl`

### target_listing

`target_listing` uses Target's RedSky `plp_search_v2` response as its
authoritative product source. A named department expands to each configured
subcategory; direct Target category IDs remain supported for focused runs.

Available departments include `grocery`, `women`, `men`, `kids`, `baby`,
`home`, `kitchen-dining`, `patio-garden`, `beauty`, `personal-care`, `health`,
`household-essentials`, `pets`, `toys`, `electronics`, `video-games`,
`sports-outdoors`, `school-office`, `movies-music-books`, `gift-cards`, and
`clearance`. The `grocery` department expands to 14 current child listings.

Sample output:
```json
{
  "product_id": "81127431",
  "name": "Women's Perfectly Cozy Jogger Pants - Stars Above™ Black M",
  "price": "$22.00",
  "url": "https://www.target.com/p/women-s-perfectly-cozy-jogger-pants-stars-above-black/-/A-81127431",
  "image": "https://target.scene7.com/is/image/Target/GUEST_9f95ecf4-59f7-4008-b854-95380a6b6f89"
}
```

Run example:
`.venv/bin/scrapy crawl target_listing -a category=5xtc0 -a max_pages=1 -O target_listing.jsonl`

Department example:
`scrapy crawl target_listing -a category=grocery -a max_pages=1 -O target_grocery.jsonl`

The feed contract is fixed with `FEED_EXPORT_FIELDS`: product ID, title, brand,
current/original price, currency, URL, image, rating/review count, category and
subcategory context, page, extraction source, and raw RedSky product data.

Validation notes (2026-03-01):
- Browser-control tool was unavailable during this run, so sorting behavior was validated via direct RedSky API probes (`sortBy`: `relevance`, `newest`, `PriceHigh`, `PriceLow`), all returning HTTP 200.
- Fixed Target key extraction to parse escaped `apiKey` from bootstrap payload and use the first 32-hex chars for `plp_search_v2`.
- Disabled proxy routing for Target spider requests (`disable_proxy`) because the configured proxy path returned RedSky 404 for this endpoint.
- Verified `target_listing` (`category=5xtc0`, `max_pages=1`) returns **24 items** with NordVPN US cities **Ashburn** and **Dallas**, and also while NordVPN is disconnected.

### nordstrom_listing

HTML-first Nordstrom listing spider that extracts products from embedded hydration data (`window.__INITIAL_CONFIG__`, with `__NEXT_DATA__`/generic JSON fallback).

Run example:
`common-scrapy crawl nordstrom_listing -a category=women -a max_pages=1 -O nordstrom_listing.jsonl`

Sample output:
```json
{
  "category": "women",
  "product_id": 3865966,
  "name": "Pure Luxe Underwire T-Shirt Bra",
  "brand": "Natori",
  "price": 29.6,
  "url": "https://www.nordstrom.com/s/natori-pure-luxe-underwire-t-shirt-bra/3865966",
  "image": "https://n.nordstrommedia.com/it/0777d4b6-d7ef-4809-84a5-36fe4da01aff.jpeg",
  "rating": 4.5,
  "reviews_count": 1715
}
```

Validation notes (2026-02-25):
- Browser check showed live product cards rendering on `https://www.nordstrom.com/browse/women`.
- Confirmed while connected to NordVPN US cities: **Ashburn**, **Seattle**, and **Dallas**.
- `nordstrom_listing` (`category=women`, `max_pages=1`) returned **81 items** in this environment.
- One run hit an initial `502 Bad Gateway` but recovered via retry and completed successfully.

### nordstromrack_listing

Direct-HTTP listing spider for Nordstrom Rack category pages. It reads the
server-rendered Schema.org `ItemList` JSON-LD, deduplicates products, and follows
the category `page` query parameter up to `max_pages`.

Run example:
`common-scrapy crawl nordstromrack_listing -a category=women -a max_pages=1 -O nordstromrack_listing.jsonl`

Available categories: `women`, `men`, `kids`, `shoes`,
`bags-and-accessories`, `beauty`, `home`, and `clearance`.

The export contract is ordered and includes `item_id`, `title`, `brand`,
`price`, `price_max`, `currency`, `availability`, `url`, `image_url`,
`category`, `page`, `position`, `source`, and the original JSON-LD product in
`raw`.

Sample output:
```json
{
  "item_id": "7788991",
  "title": "Pleated Midi Dress",
  "brand": "Donna Ricco",
  "price": 34.97,
  "price_max": 49.97,
  "currency": "USD",
  "availability": "InStock",
  "url": "https://www.nordstromrack.com/s/pleated-midi-dress/7788991",
  "image_url": "https://n.nordstrommedia.com/id/example.jpeg",
  "category": "women",
  "page": 1,
  "position": 1,
  "source": "nordstromrack_itemlist_json_ld",
  "raw": {"@type": "Product", "sku": "7788991"}
}
```

Live requests returned Fastly's `x-jungle` HTTP 403 response during the latest
validation. The checked-in representative fixture exercises the same JSON-LD
contract deterministically.

### bestbuy_search / bestbuy_listing

Best Buy pages currently use Apollo hydration (not `__NEXT_DATA__` on PLP/search). These spiders extract normalized data from the Apollo bootstrap embedded in the direct HTTP response.

If Best Buy serves a challenge/error variant, output may be empty.

Run examples:
- `common-scrapy crawl bestbuy_search -a q='laptop' -a max_pages=1 -O bestbuy_search.jsonl`
- `common-scrapy crawl bestbuy_listing -a category=laptops -a max_pages=1 -O bestbuy_listing.jsonl`

Validation notes (2026-02-25):
- Browser check confirmed live product cards rendered on `searchpage.jsp?st=laptop`.
- `bestbuy_search` (`max_pages=1`) returned items with `source=bestbuy_apollo_bootstrap` while connected to NordVPN US Dallas (`us9157`).
- Also tested browser accessibility from NordVPN US Seattle (`us8242`) and US Ashburn (`us9510`); listing pages still rendered.

`bestbuy_search` sample output:
```json
{
  "item_id": "10460842",
  "title": "HP - 14\" Laptop - Intel Processor N150 2025 - 4GB Memory - 128GB UFS - Willow Green",
  "url": "https://www.bestbuy.com/product/hp-14-laptop-intel-processor-n150-2025-4gb-memory-128gb-ufs-willow-green/JJGQJQR8CP",
  "brand": null,
  "price": 189.98,
  "currency": "USD",
  "rating": 4.6,
  "reviews_count": 1551,
  "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/90a8a03b-c474-416d-bb79-579d46bf34d5.jpg",
  "source": "bestbuy_apollo_bootstrap",
  "mode": "keyword",
  "query": "laptop",
  "page": 1,
  "source_url": "https://www.bestbuy.com/site/searchpage.jsp?st=laptop&intl=nosplash"
}
```

`bestbuy_listing` sample output:
```json
{
  "item_id": "6628354",
  "title": "Dell - Plus - Copilot+ PC - 16\" 2K Touchscreen Laptop - AMD Ryzen AI 7 350 2025 - 32GB Memory - 1TB Storage - Ice Blue",
  "url": "https://www.bestbuy.com/product/dell-plus-copilot-pc-16-2k-touchscreen-laptop-amd-ryzen-ai-7-350-2025-32gb-memory-1tb-storage-ice-blue/J3K4L63SVF/sku/6628354",
  "brand": null,
  "price": 799.99,
  "currency": "USD",
  "rating": 4.7,
  "reviews_count": 439,
  "image_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/7afd11ae-3eb7-46d2-ad3e-6690837b2fdd.jpg",
  "source": "bestbuy_apollo_bootstrap",
  "mode": "category",
  "category_url": "https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000",
  "page": 1,
  "source_url": "https://www.bestbuy.com/site/all-laptops/laptops/abcat0502000.c?id=abcat0502000&cp=1&intl=nosplash"
}
```

### costco_search / costco_listing

`costco_search` retains its existing search extraction flow. `costco_listing` uses the current category-page contract: React Flight discovers the category and GRS search configuration, then the GRS API returns paginated products.

Run examples:
- `common-scrapy crawl costco_search -a q='coffee' -a max_pages=1 -O costco_search.jsonl`
- `common-scrapy crawl costco_listing -a category='coffee' -a max_pages=1 -O costco_listing.jsonl`

`costco_search` sample output:
```json
{
  "item_id": "100617983",
  "title": null,
  "url": "https://www.costco.com/lavazza-espresso-gran-crema-whole-bean-coffee-medium-22-lbs.product.100617983.html",
  "price": null,
  "currency": null,
  "brand": null,
  "rating": null,
  "reviews_count": null,
  "image_url": null,
  "source": "costco_html_links_fallback",
  "raw": null,
  "mode": "keyword",
  "query": "coffee",
  "page": 1,
  "source_url": "https://www.costco.com/s?keyword=coffee"
}
```

`costco_listing` sample output:
```json
{
  "item_id": "100361434",
  "title": "Kirkland Signature Colombian Coffee",
  "url": "https://www.costco.com/kirkland-signature-colombian-coffee-dark-roast-3-lbs.product.100361434.html",
  "price": 14.99,
  "original_price": 19.99,
  "currency": "USD",
  "brand": "Kirkland Signature",
  "rating": 4.7,
  "reviews_count": 123,
  "image_url": "https://images.costco-static.com/100361434.jpg",
  "source": "costco_grs_search_api",
  "mode": "category",
  "category": "coffee",
  "subcategory": "ground-coffee",
  "listing_url": "https://www.costco.com/ground-coffee.html",
  "page": 1,
  "source_url": "https://www.costco.com/ground-coffee.html"
}
```

Notes:
- `costco_listing` exposes all 131 parent groups and 432 subcategory entries from `sample/costco-categories.json`.
- Selecting a parent category starts every listed child; for example, `category=coffee` starts its four inventory entries.
- The listing spider accepts category selection only; direct `url` and `category_url` overrides are not used.
- Pagination uses the discovered `pageSize`, category page ID, and GRS `offset` contract.

### kroger_search / kroger_listing

`kroger_search` tries bootstrap state extraction first (`__NEXT_DATA__` /
`__APOLLO_STATE__`), then falls back to JSON-LD and direct product-link HTML
parsing.

`kroger_search` sample output:
```json
{
  "item_id": "kroger-2-reduced-fat-milk-gallon",
  "title": null,
  "url": "https://www.kroger.com/p/kroger-2-reduced-fat-milk-gallon/0001111041700",
  "price": null,
  "currency": null,
  "brand": null,
  "rating": null,
  "reviews_count": null,
  "image_url": null,
  "source": "kroger_html_links_fallback",
  "raw": null,
  "mode": "keyword",
  "query": "milk",
  "page": 1,
  "source_url": "https://www.kroger.com/search?query=milk&searchType=default_search&sort=bestMatch"
}
```

`kroger_listing` sample output:
```json
{
  "category": "cereal",
  "item_id": "0001111012345",
  "title": "Kroger Toasted Oats Cereal",
  "brand": "Kroger",
  "url": "https://www.kroger.com/p/kroger-toasted-oats-cereal/0001111012345",
  "image_url": "https://www.kroger.com/product/images/large/front/0001111012345",
  "price": 3.99,
  "regular_price": 4.49,
  "currency": "USD",
  "availability": "InStock",
  "size": "18 oz",
  "source": "kroger_initial_state_search_products",
  "category_url": "https://www.kroger.com/pl/cereal/09002",
  "page": 1,
  "raw": {"upc": "0001111012345", "description": "Kroger Toasted Oats Cereal"}
}
```

Run examples:
- `common-scrapy crawl kroger_search -a q='milk' -a max_pages=1 -O kroger_search.jsonl`
- `common-scrapy crawl kroger_listing -a category='milk' -a max_pages=1 -O kroger_listing.jsonl`

Notes:
- Added sort variant retries (`bestMatch`, `sale`) to mitigate zero-item responses from Akamai caches; `kroger_search` now emits ~27 items via HTML link fallback even when bootstrap state is stripped.
- `kroger_listing` reads only `window.__INITIAL_STATE__.search.searchAll.response.products`; it raises a visible error when the state or product collection is absent instead of exporting partial fallback records.
- Its ordered 15-field export contract is `category`, `item_id`, `title`, `brand`, `url`, `image_url`, `price`, `regular_price`, `currency`, `availability`, `size`, `source`, `category_url`, `page`, and `raw`.
- Products are deduplicated by UPC. Pagination uses Kroger's `page` parameter, the Redux `pageSize`, and `productsInfo.totalCount`, and stops at `max_pages`.
- The six maintained category shortcuts are `cereal`, `bread`, `coffee`, `eggs`, `milk`, and `snacks`. A direct fixture or listing URL can be supplied with `-a url=<listing-url>`.
- NordVPN US egress (New York, Chicago, Los Angeles, Dallas, Miami, Seattle) continued to return 403s/timeouts during curl checks; disconnecting NordVPN and routing through the configured BRD residential proxy remains the only reliable path in this environment.

### bathandbodyworks_listing

Extracts the authoritative product `hits` from the `products` React Query inside
the server-rendered `#mobify-data` payload. There are no API/HTML fallback modes:
missing hydration or an empty product collection fails visibly. The nested
`BATHANDBODYWORKS_CATEGORIES` inventory contains 65 current navigation targets
across sale, new, gifts, body care, candles, home fragrance, soaps and sanitizers,
men's, and home care. Products are deduplicated by `productId`; additional pages
use the storefront's `start` offset and obey `max_pages`.

```json
{
  "item_id": "028005116",
  "title": "A Thousand Wishes Ultimate Hydration Body Cream",
  "url": "https://www.bathandbodyworks.com/p/a-thousand-wishes-ultimate-hydration-body-cream-028005116",
  "price": 4.95,
  "regular_price": 18.95,
  "currency": "USD",
  "availability": "InStock",
  "rating": 4.8455,
  "reviews_count": 5132,
  "source": "bathandbodyworks_mobify_react_query"
}
```

Run examples:

- `common-scrapy crawl bathandbodyworks_listing -a category=body-care -a max_pages=1 -O bbw.jsonl -s HTTPCACHE_ENABLED=False`
- Pass any of the 65 aliases, such as `3-wick-candles`, or use `-a url=<listing-url>`.

Live verification status: as of 2026-10-03, a one-page live crawl of
`https://www.bathandbodyworks.com/c/body-care` returned HTTP 200 and exported
48 items, all with a non-empty `raw` hydrated record. The committed
`sample/bathandbodyworks-listing-products.html` fixture yields 2 items for
deterministic tests.

The ordered `FEED_EXPORT_FIELDS` contract includes identifiers, name and brand,
product/media URLs, sale and regular prices, availability, rating/review data,
product type, fragrance, size, color, position, source, crawl context, and the raw
hydrated record.

### ikea_listing

Uses IKEA's SIK category-search endpoint as the single authoritative product
source. The bundled inventory is normalized from 23 product departments and
deduplicated by IKEA item number; category arguments are the final IKEA category
tokens (for example, `st004`).

Pagination uses fixed 24-**slot** windows — offsets `0, 24, 48, ...` — not
24-product windows. A window is a mixed slot budget: the storefront fills it with
`PRODUCT` entries *and* typed breakouts (`AFFORDABILITY`, `NEW_PRODUCT`, `OFFERS`),
so a full 24-slot window yields fewer than 24 products. In the live `st004` run
below, window 1 held 24 slots of which 22 were products, and window 2 held 24
products because it carried no breakouts. The crawl stops at `max_pages`, when the
window's `end` reaches `itemsPerType.PRODUCT` (or `max`), or when a window returns
no new products.

IKEA validates the SIK query version server-side and rejects an unknown value with
`{"detail":"Invalid API version"}`, which carries no `PRIMARY_AREA`. The version is
therefore pinned to the last verified value and can be rotated without a code
change via `-a sik_version=`. Both the pinned version and the failure message name
the override, so a retired version is diagnosable from the log alone.

The live response wraps the component as `{"results": [{"component":
"PRIMARY_AREA", "items": [...], "metadata": {...}}], "metadata": {...}}`, where
window counts live under the component's `metadata`. The bundled capture
(`sample/ikea-sik-sample.json`) is instead a reduced top-level `PRIMARY_AREA` with
`metadata_window`; both shapes are supported and both are fixture-tested.

Because `require_category_arg` is disabled (so `-a url=` / `-a category_url=` runs
are accepted), `BaseListingSpider` skips its own categories schema check. The
spider therefore validates its own inventory at construction: every entry must be a
dict with non-empty string `category` and `url`, and the `category` token must be
recoverable from the `url` — the same value `resolve_target_url()` feeds to SIK. A
malformed inventory entry fails immediately rather than as a confusing
`Unknown category` error at crawl time.

`-a mode=html` selects the server-rendered fallback described in issue #114: it
fetches the category PLP and parses the `.js-product-list[data-category]` container
state plus the `.plp-fragment-wrapper` cards, rejecting a hub-only URL (no
product-list container) with a clear error. It is opt-in and page 1 only — the
storefront hydrates windows 2+ through SIK, so there is no HTML equivalent of offset
windows, and a silent automatic downgrade would hide exactly the schema drift the
API path reports loudly. HTML items set `source: "ikea_plp_html"` and leave the
API-only enrichment fields (`item_no_global`, `department`, `category_path`,
`business_area`, `product_type_tag`, `variant_count`, `colors`, `quick_facts`) as
`None`, since the rendered card does not carry them.

Run examples:

- `common-scrapy crawl ikea_listing -a category=st004 -a max_pages=2 -O ikea.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl ikea_listing -a category=st004 -a max_pages=2 -a sik_version=<version> -O ikea.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl ikea_listing -a category=st004 -a mode=html -O ikea_html.jsonl -s HTTPCACHE_ENABLED=False`

The ordered export fields are `category`, `item_id`, `title`, `product_type`,
`dimensions`, `url`, `image_url`, `image_urls`, `price`, `currency`, `rating`,
`reviews_count`, `badge`, `design`, `availability`, `item_no_global`,
`product_class`, `department`, `category_path`, `business_area`,
`product_type_tag`, `variant_count`, `colors`, `quick_facts`, `image_alt`, `page`,
`category_url`, and `source`, and `raw`.

Everything after `availability` is read directly from the SIK `PRODUCT` payload —
`itemNoGlobal`, `filterClass`, `categoryPath`, `businessStructure.productAreaName`,
`optimizelyAttributes.PRODUCT_TYPE`, `gprDescription.numberOfVariants`, `colors`,
`quickFacts`, and `mainImageAlt` — rather than derived from the rendered page.
`department` and `category_path` report the product's canonical IKEA path, which
can differ from the crawled category for cross-listed entries. Optional keys
degrade to `None` (or `[]` for `colors`) when absent.

Live verification (`-s HTTPCACHE_ENABLED=False`, `category=st004`, `max_pages=2`,
2026-10-01 UTC, re-confirmed 2026-10-02 UTC) exported **46 unique items** with
`raw` present on every row: 22 products in the first 24-slot window and 24 in the
second. The API reported `itemsPerType.PRODUCT = 148` for this category, so the
crawl stopped at `max_pages` rather than exhausting the category.

The HTML path was verified live on the same category (2026-10-02 UTC,
`sample/ikea-plp-fixture.html` reduced from that capture): **24 items** exported
from the 24 server-rendered cards, all unique, `raw` present on 24/24. The reduced
fixture keeps the first 2 cards, so the fixture test asserts 2 items; the 24-item
figure is the live crawl, not the fixture.

### sallybeauty_listing

Extracts Sally Beauty product tiles from the server-rendered Salesforce Commerce
Cloud listing page. For later batches, the spider follows the exact
`Search-UpdateGrid` URL advertised by the page's Load More control. That endpoint
returns another HTML product-grid fragment rather than JSON. Reusing the supplied
URL preserves the storefront's category ID, refinements, sort order, page size,
and offset.

Run examples:

- `common-scrapy crawl sallybeauty_listing -a category='hair-care' -a max_pages=1 -O sallybeauty.jsonl`
- `common-scrapy crawl sallybeauty_listing -a category='hair-care' -a max_pages=3 -O sallybeauty.jsonl`
- `common-scrapy crawl sallybeauty_listing -a category='hair-care' -a url='https://www.sallybeauty.com/hair-care/shop-by-product/shampoo/' -a max_pages=2 -O shampoo.jsonl`

The export contract is ordered as:

`category`, `item_id`, `title`, `brand`, `url`, `image_url`, `price`,
`price_max`, `currency`, `rating`, `reviews_count`, `page`, `source`, and
`category_url`.

```json
{
  "category": "hair-care",
  "item_id": "SBS-539230",
  "title": "Low Porosity Aloe Vera Gel Shampoo",
  "brand": "Texture ID",
  "url": "https://www.sallybeauty.com/hair-care/shop-by-product/shampoo/low-porosity-aloe-vera-gel-shampoo/SBS-539230.html",
  "image_url": "https://www.sallybeauty.com/images/539230.jpg",
  "price": 11.99,
  "price_max": null,
  "currency": "USD",
  "rating": 4.6,
  "reviews_count": 29,
  "page": 1,
  "source": "sallybeauty_sfcc_product_grid",
  "category_url": "https://www.sallybeauty.com/hair-care/shop-by-product/shampoo/"
}
```

Notes:

- Page 1 uses `source=sallybeauty_sfcc_product_grid`; AJAX batches use
  `source=sallybeauty_sfcc_search_update_grid`.
- `max_pages` includes the initial listing page. Pagination stops when that
  limit is reached or the response no longer advertises a `Search-UpdateGrid`
  URL.
- The spider intentionally raises an error if a response contains no expected
  product grid, so a PerimeterX challenge cannot be mistaken for product data.
- Sally Beauty currently returns PerimeterX `PX-ABR`/captcha responses to some
  automated egress. Use an authorized proxy or network path when needed.
- Representative redacted responses are available in
  `sample/sallybeauty-listing-product.html` and
  `sample/sallybeauty-listing-product-page-2.html`.

### officedepot_listing

Office Depot / OfficeMax category listings from the inline Redux hydration state
`window.ODSEARCHBROWSE_INITIAL_STATE`. The category taxonomy is resolved at
start-up from the first-party header mega-menu JSON
(`https://ma.officedepot.com/header-menu-excel/products.json`). A plain ScrapeOps
datacenter route returned real SSR HTML for every page fetched; no residential or
`bypass` option is required.

Flow:

1. `start_requests` fetches the header mega-menu JSON and walks
   `responseObject.menuList` (department -> level-2 -> level-3). Only
   `/b/<slug>/N-<navId>` browse PLPs are crawled (388 entries); `/l/...` editorial
   landing pages are skipped. Every entry is registered under both a plain slug and a
   `<department>-<name>` qualified slug, so duplicate leaf names (for example
   "Sheet Protectors" under Office Supplies and School Supplies) can be selected
   unambiguously.
2. Each selected category PLP is fetched with `?page=N` (1-based). The server-rendered
   page embeds `window.ODSEARCHBROWSE_INITIAL_STATE` as a JS object literal that also
   contains bare `undefined` tokens (invalid strict JSON); the spider brace-matches the
   object and rewrites `undefined` -> `null` before `json.loads`.
3. Products are read from `products.products[]`; `products.total` is the authoritative
   stop and pagination continues while `current_page * page_size < total` and
   `page <= max_pages`. Items are deduplicated by `item_id` across pages.

Category slugs come from the leaf name via `_slugify` (for example `Office Chairs` ->
`office-chairs`); the resolved set is exposed through the spider's
`available_categories()` (plain and qualified slugs).

Run examples:

- `common-scrapy crawl officedepot_listing -a category='furniture' -a max_pages=2 -O officedepot.jsonl`
- `common-scrapy crawl officedepot_listing -a category='office-chairs' -a max_pages=1 -O officedepot.jsonl`
- `common-scrapy crawl officedepot_listing -a max_pages=1 -O officedepot-all.jsonl` (all 388 browse PLPs)

Export contract: `department`, `sub_category`, `category`, `item_id`, `title`, `brand`,
`url`, `image_url`, `price`, `original_price`, `list_price`, `currency`, `availability`,
`rating`, `reviews_count`, `item_number`, `description`, `catalog_labels`, `category_id`,
`page`, `category_url`, `breadcrumbs`, `source`, `raw`.

Fixtures: `sample/officedepot-header.json` (captured
`header-menu-excel/products.json`) and `sample/officedepot-category-page.html` (reduced
capture of `/b/furniture/N-917` carrying the `ODSEARCHBROWSE_INITIAL_STATE` blob).

Tests: `python -m unittest tests.test_officedepot_listing_spider` (16 network-free tests).

Live verification (`-s HTTPCACHE_ENABLED=False`, 2026-10-02 UTC):

- `category=furniture, max_pages=2` -> **59 items** (page 1: 34 products, page 2: 34
  products with 9 cross-page duplicates removed), 3 HTTP 200 requests, `finish_reason=finished`.
- `category=office-chairs, max_pages=1` -> **24 items**, 4-level breadcrumbs
  (`Home > Furniture > Chairs & Seating > Office Chairs`).

```json
{"department":"Furniture","sub_category":null,"category":"Furniture","item_id":"9003237","title":"Serta® Smart Layers™ Brinkley Ergonomic Bonded Leather High-Back Executive Office Chair, Black/Silver","brand":"Serta","url":"https://www.officedepot.com/a/products/9003237/Serta-Smart-Layers-Brinkley-Ergonomic-Bonded/","image_url":"https://media.officedepot.com/images/t_large%2Cf_auto/products/9003237/1.jpg","price":299.99,"original_price":299.99,"list_price":586.81,"currency":"USD","availability":"InStock","rating":4.5169,"reviews_count":178,"item_number":"9003237","description":"...","catalog_labels":["ecoConscious","lessHarshChemicals"],"category_id":"593061","page":1,"category_url":"https://www.officedepot.com/b/furniture/N-917?page=1","breadcrumbs":["Home","Furniture"],"source":"officedepot_bootstrap","raw":{...}}
```

### orientaltrading_listing

`orientaltrading_listing` covers 20 stable shopping categories from Oriental
Trading's main navigation. It uses one item-data direction: each category page
supplies first-party `/web/browse/productQuickView` endpoint URLs, and every
exported product is parsed exclusively from that API response. There is no
direct product-card or JSON-LD extraction fallback.

The quick-view response supplies more detail than a listing tile, including all
product images, description, rating and review count, stock status, internal
category metadata, badge, quantity/unit data, current price, and original price.
Pages follow the server-advertised `rel=next` URL and stable SKUs are deduplicated.
`max_pages` bounds pagination; `api_limit` can bound product calls per page for a
short live smoke run.

```bash
scrapy crawl orientaltrading_listing -a category=sale -a max_pages=1 -s HTTPCACHE_ENABLED=False -O orientaltrading.jsonl
```

The ordered `FEED_EXPORT_FIELDS` contract contains 27 fields: category context,
SKU identity, title and canonical URL, all images, current/original price,
quantity, availability, rating/reviews, brand and internal category details,
badge, description, page/position, discovery and API URLs, source, raw API form
values, and timestamp.

Tests: `python3 -m unittest tests.test_orientaltrading_listing_spider -v`.

### basspro_listing

Bass Pro Shops (`https://www.basspro.com`) runs on a Next.js App Router storefront
(`/c/<slug>` for departments, `/l/<slug>` for level-2 categories and subcategories).
The server HTML deliberately ships **no product records**: `__NEXT_DATA__.props.pageProps.pageValues`
carries only page metadata (page id, layout, breadcrumbs, facet configuration) and
`__NEXT_DATA__.props.megaNavHtmlV2` carries only the navigation tree. The product grid is a
client-side **Coveo Headless** search, so this spider talks to that one endpoint directly —
there is no HTML-card parser and no JSON-LD fallback.

Flow:

1. `start_requests` fetches the resolved category page through `PROXY` and reads
   `__NEXT_DATA__.props.pageProps.pageValues` for `pageId`, `pageIdentifier`, `storeId`,
   `breadcrumbs` and the `facetList` (`srchattridentifier` values arrive as `_cat.<field>`).
2. `GET /api/v1/coveo/generate-token?refresh=true` returns a short-lived search token
   (valid ~4 h, per the storefront's own `COVEO_TOKEN_VALID_TIME_HOURS`). The token is used
   in memory only — it is never written to disk or to a fixture.
3. `POST https://platform.cloud.coveo.com/rest/search/v2?organizationId=bassproshopsproductionl92epymr`
   with `Authorization: Bearer <token>`, `searchHub=basspro-searchhub` (the storefront's
   `ProductionPipeline` query pipeline) and
   `aq=NOT (@isgun==1 OR @isammo=="1" OR @isgooglerestricted=="1") AND @groupurlkeywords=="<slug>"`.
   `groupurlkeywords` is the indexed catalog-group slug, which is exactly the last path
   segment of the browse URL, so the taxonomy slug maps 1:1 onto the search filter.
   Pagination is offset based (`firstResult` / `numberOfResults`, default 48) and stops on
   a short page, on `totalCount`, or at `max_pages`. Items are deduplicated by `item_id`.

### Routing: the two legs need opposite routes

| Leg | Host | Route | Why |
|---|---|---|---|
| Category page | `www.basspro.com` | **PROXY** | Akamai returns `403 Access Denied` on a direct request |
| Search token | `www.basspro.com` | **PROXY** | same Akamai edge |
| Product search | `platform.cloud.coveo.com` | **direct** | a proxied POST comes back `HTTP 200` with the **unfiltered** `totalCount` (541813) because the proxy drops the request body — routing this leg through `PROXY` silently yields the whole index instead of the category |

Because of that the spider sets `DOWNLOADER_MIDDLEWARES` to disable the project-wide
`CommonDownloaderMiddleware` (which force-proxies every request) and routes each leg
explicitly: storefront legs get `meta["proxy"] = PROXY`, the Coveo leg gets no proxy at all.
`PROXY` is therefore required for this spider; there is no unproxied fallback for the
storefront legs.

Taxonomy (`common/spiders/basspro_categories.py`) is generated from the live `megaNavHtmlV2`
blob: **11 departments, 155 level-2 categories and 782 level-3 subcategories**. 39 level-2
tiles are pure marketing links (`Sale`, `New Arrivals`, …) with no browse URL and are skipped,
leaving **909 crawlable entries**. Every entry keeps its full navigation path
(`Fishing/Rod & Reel Combos/Baitcast Combos`), so the 119 slugs cross-linked between
departments (for example `/l/trailer-accessories` under both Boating and Outdoor Rec) stay
addressable per department; the bare slug is accepted too and resolves to the same browse URL.

Run examples:

- `common-scrapy crawl basspro_listing -a category=rod-reel-combos -a max_pages=2 -O basspro.jsonl`
- `common-scrapy crawl basspro_listing -a category='Fishing/Rod & Reel Combos/Baitcast Combos' -a max_pages=1 -O basspro.jsonl`
- `common-scrapy crawl basspro_listing -a url=https://www.basspro.com/c/marine-electronics -a max_pages=1 -O basspro.jsonl`
- optional args: `-a page_size=24`, `-a include_restricted=1` (drop the storefront's
  firearm/ammunition/restricted-SKU safety query)

Export contract (56 `FEED_EXPORT_FIELDS`): `category`, `department`, `subcategory`,
`category_id`, `page_id`, `category_url`, `category_slug`, `category_name`, `breadcrumb`,
`item_id`, `product_id`, `sku`, `part_number`, `upc`, `mpn`, `title`, `brand`, `url`,
`image_url`, `price`, `original_price`, `currency`, `discount_percent`, `savings`, `rating`,
`reviews_count`, `availability`, `quantity`, `retail_quantity`, `is_clearance`, `is_sale`,
`is_new`, `is_free_shipping`, `is_club_exclusive`, `in_store_inventory`, `collection`,
`classification`, `class_name`, `category_path`, `color`, `size`, `country_of_origin`,
`pieces`, `gear_ratio`, `line_weight`, `retrieve`, `action`, `power`, `store_id`, `page`,
`position`, `total_count`, `items_per_page`, `source_url`, `source`, `raw`.

The `raw` dict keeps the full curated `fieldsToInclude` projection (identifiers, prices,
availability flags, ratings, media, spec attributes and the composite `thecategories` /
`groupurlkeywords` catalog-group records). The unfiltered Coveo payload is ~200 fields and
~30 KB per product; the curated list cuts the page size by ~60% without dropping anything
the PLP tile renders.

Fixtures: `sample/basspro-plp.html` (reduced `/l/rod-reel-combos` capture with the real
`__NEXT_DATA__`), `sample/basspro-coveo-page1.json`, `sample/basspro-coveo-page2.json`,
`sample/basspro-coveo-lastpage.json` (short last page), `sample/basspro-token.json`
(placeholder token), `sample/basspro-coveo-error.json` and `sample/basspro-challenge.html`.

Tests: `python -m unittest tests.test_basspro_listing_spider` (41 network-free tests).

Verified live runs (`HTTPCACHE_ENABLED=False`):

- `category=rod-reel-combos, max_pages=2` -> **96 items** (96 unique `item_id`, pages 1 and 2,
  `totalCount=478`), 4 HTTP 200 requests, `finish_reason=finished`.
- `category=womens-shoes-boots, max_pages=1` -> **48 items** (48 unique `item_id`,
  `totalCount=820`, 10 of them markdown rows with `original_price` set).

```json
{"category":"Fishing/Rod & Reel Combos","department":"Fishing","subcategory":"Baitcast","category_id":"3074457345616732396","page_id":"3074457345616732396","category_url":"https://www.basspro.com/l/rod-reel-combos","category_slug":"rod-reel-combos","category_name":"Rod and Reel Combos","breadcrumb":["Fishing","Rod & Reel Combos"],"item_id":"3472884","product_id":"3074457345623307121","sku":"3472884","part_number":"101243021","upc":"900006658840","title":"Bass Pro Shops Megacast Baitcast Combo","brand":"Bass Pro Shops","url":"https://www.basspro.com/p/bass-pro-shops-megacast-baitcast-combo","price":69.99,"original_price":null,"currency":"USD","discount_percent":0.0,"savings":0.0,"rating":3.6241,"reviews_count":133,"availability":"InStock","quantity":624,"gear_ratio":"6.6:1","country_of_origin":"CHINA","page":1,"position":1,"total_count":478,"items_per_page":48,"source_url":"https://www.basspro.com/l/rod-reel-combos","source":"basspro_coveo","raw":{...}}
```

### gamestop_listing

GameStop runs on Salesforce Commerce Cloud (Demandware) behind a Constructor.io
"hybrid" browse front end. The PLP HTML does **not** contain product data: the
server renders empty tile shells that carry only a `data-pid`, and `main.js`
hydrates each tile from a first-party JSON controller:

```
/on/demandware.store/Sites-gamestop-us-Site/default/Tile-GetProductsJSON
    ?deliveryAttribute=&data=<comma-separated-pids>&useTileImage=true
```

This spider uses exactly one data direction -- that JSON controller. There is no
HTML tile scraping, no Constructor.io browse call, and no rendered-browser
fallback. If the controller stops answering correctly the spider raises instead
of silently emitting empty tile shells.

Flow:

1. Fetch the category page (or a later `Search-UpdateGrid` fragment) and read the
   `data-pid` list plus `data-cnstrc-num-results` (total).
2. Batch the pids (`TILE_BATCH_SIZE`, 20 per request) into `Tile-GetProductsJSON`.
3. Emit one item per returned product, deduplicated by `item_id`.
4. Paginate with `Search-UpdateGrid?cgid=<slug>&start=<n>&sz=<sz>` until

   `start >= total`, `max_pages` is reached, or a grid page yields no new ids.

Two details worth knowing:

- The `cgid` used for pagination is the Demandware category id (`consoles`,
  `toys-and-collectibles-funko`, ...), which is **not** the friendly URL slug
  (`consoles-hardware`, `collectibles/funko`). The spider reads it back from the
  page's own `Search-UpdateGrid` link rather than guessing.
- The friendly category URL renders the storefront's default page size (20),
  which is smaller than `PAGE_SIZE` (60), so pagination advances by the number of
  pids the grid actually served rather than `page * PAGE_SIZE`.
- `data-cnstrc-num-results` is rendered on the category page but **not** on the
  `Search-UpdateGrid` fragments, so the page-1 total is remembered and reused for
  later pages; otherwise `start >= total` could never fire and the crawl would
  run one grid past the end of the listing.
- The next-page request is decided once per grid page, after all its pid batches
  have answered. A batch that comes back with an empty `productsJSON` (retired
  pids) is skipped without cancelling pagination for the sibling batches.

Run examples:

- `common-scrapy crawl gamestop_listing -a category='consoles-hardware' -a max_pages=1 -O gamestop.jsonl`
- `common-scrapy crawl gamestop_listing -a category='consoles-hardware' -a max_pages=3 -O gamestop.jsonl`
- `common-scrapy crawl gamestop_listing -a category='collectibles-funko' -a max_pages=2 -O funko.jsonl`
- `common-scrapy crawl gamestop_listing -a category_url='https://www.gamestop.com/consoles-hardware' -a max_pages=1 -O gamestop.jsonl`

Category shortcuts come from `common/spiders/gamestop_categories.py` (the full
header-menu taxonomy, 119 URLs across 33 category groups). Category keys are the full
URL path slug, e.g. `consoles-hardware`, `video-games-nintendo-switch`,
`collectibles-funko`, because leaf slugs alone collide across departments.

The export contract is ordered as:

`category`, `department`, `item_id`, `title`, `url`, `image_url`, `image_alt`,
`price`, `list_price`, `pro_price`, `price_min`, `price_max`, `currency`,
`availability`, `is_digital_product`, `badge`, `rating`, `reviews_count`,
`market_price`, `release_date`, `product_platform`, `short_description`, `page`,
`category_url`, `source`, and `raw`.

```json
{
  "category": "consoles-hardware",
  "department": "consoles-hardware",
  "item_id": "106429",
  "title": "Nintendo Wii Original Console with Wii Remote - Super Mario Bros. 25th Anniversary Edition Red",
  "url": "https://www.gamestop.com/consoles-hardware/retro-consoles/products/nintendo-wii-original-console-with-wii-remote---super-mario-bros.-25th-anniversary-edition-red/106429.html",
  "image_url": "https://media.gamestop.com/i/gamestop/10121186?",
  "image_alt": "Nintendo Wii Original Console with Wii Remote - Super Mario Bros. 25th Anniversary Edition Red",
  "price": "139.99",
  "list_price": "139.99",
  "pro_price": "132.99",
  "price_min": null,
  "price_max": null,
  "currency": "USD",
  "availability": "InStock",
  "is_digital_product": false,
  "badge": "BUY CONSOLE, SAVE 10% PO ACC.",
  "rating": "83.85",
  "reviews_count": "654",
  "market_price": null,
  "release_date": null,
  "product_platform": null,
  "short_description": null,
  "page": 1,
  "category_url": "https://www.gamestop.com/consoles-hardware",
  "source": "gamestop_tile_json",
  "raw": { "id": "106429", "name": "...", "price": { "base": "139.99", "sale": null, "pro": "132.99" } }
}
```

Notes:

- `price` uses the sale price when GameStop provides one, otherwise the base
  price; `list_price` keeps the base price for comparison.
- `availability` is normalized to `InStock` / `PreOrder` / `OutOfStock` from the
  tile `availability` object. The explicit `preorder` flag is checked **first**,
  because a preorder item is often also flagged `available` (it can be bought
  before release) and testing `available` first would report it as in stock.
  `readyToOrder` is deliberately ignored -- it is an SFCC product-selection flag
  (the variant is selectable), not a preorder indicator, and in the captured
  payload it is `true` alongside `available: true` for ordinary in-stock
  products.
- `source` is always `gamestop_tile_json` -- every item comes from the same JSON
  controller.
- The spider fails loudly on a non-200 response, an access-denied/challenge body,
  a non-JSON tile body, a missing `productsJSON` key, a tile without an `id`, or
  a **page-1** grid with no `data-pid` tiles, so a stale category map cannot
  masquerade as an empty category. On later pages an empty grid is treated as the
  end of the listing, not an error.
- Fixtures live in `sample/gamestop-listing-grid.html`,
  `sample/gamestop-tile-products.json`, and `sample/gamestop-categories.json`.
- Tests: `.venv/bin/python -m unittest tests.test_gamestop_listing_spider`
  (29 network-free fixture tests).
### footlocker_listing

Foot Locker category listings from the ZGW search API. Residential ScrapeOps proxy is
required for the API calls (`scrapeops.country=us.residential=true`); the header and
category HTML pages go through the plain datacenter route.

Flow:

1. `start_requests` fetches `https://www.footlocker.com/api/content/en/header.public.json`.
2. `parse_header_json_for_categories` walks the `ContentBand` components, whose list items
   are `headerSection*` bands; each band holds `headerCategory` groups of
   `headerCategoryLink`s. It rebuilds a band -> sub-category -> link tree.
   - When `-a category=<slug>` is given, only the taxonomy link whose slugified text matches
     is resolved (so a scoped run resolves a single category instead of the whole menu).
3. `_resolve_category_search_params` resolves `searchParams` for each category link:
   - a link with `?query=` uses that value directly;
   - otherwise the category HTML is fetched and `searchParams` is read from
     `window.footlocker.STATE_FROM_SERVER.page.category["<path>"].searchParams`
     (`parse_search_params_from_html` / `_extract_search_params_from_html`).
   A category that cannot be resolved is recorded and skipped rather than deadlocking the
   crawl; `_start_api_crawls` fires once every category has resolved or failed.
4. `_start_api_crawls` issues `_api_request`s to the ZGW search endpoint. Without
   `-a category`, every resolved category is crawled; with it, only the matching
   `category_slug`.
5. `parse_api_products` yields one item per returned product and paginates via
   `currentPage` until `max_pages` or the last page.

Category slugs come from the header link text via `_slugify` (e.g. `All Men's Shoes` ->
`all-men-s-shoes`); the resolved set is exposed through the spider's `available_categories()`.

Run examples:

- `common-scrapy crawl footlocker_listing -a category='all-men-s-shoes' -a max_pages=1 -O footlocker.jsonl`
- `common-scrapy crawl footlocker_listing -a category='all-men-s-shoes' -a max_pages=3 -O footlocker.jsonl`
- `common-scrapy crawl footlocker_listing -a max_pages=1 -O footlocker-all.jsonl` (every resolved category)

Export contract: `band`, `sub_category`, `category`, `item_id`, `title`, `url`, `image_url`,
`price`, `original_price`, `currency`, `availability`, `brand`, `rating`, `reviews_count`,
`page`, `category_url`, `source`, `raw`.

Fixtures: `sample/footlocker-header.json` (captured `header.public.json`),
`sample/footlocker-mens-shoes.html` (captured category HTML with the `STATE_FROM_SERVER`
blob), and `sample/footlocker-mens-shoes-api-page0.json` (captured ZGW page 0).

Tests: `python -m unittest tests.test_footlocker_listing_spider` (9 network-free fixture tests).

```json
{"band":"Men's","sub_category":"Shoes","category":"all-men-s-shoes","item_id":"O2463102","title":"Jordan Air Jordan Retro 4 - Men's","url":"https://www.footlocker.com/product/O2463102.html","image_url":"https://images.footlocker.com/is/image/EBFL2/O2463102","price":220.0,"original_price":220.0,"currency":"USD","availability":"OutOfStock","brand":"Jordan","rating":5.0,"reviews_count":5,"page":1,"category_url":"/category/mens/shoes.html","source":"footlocker_api","raw":{"badges":{"isDiscountsExcluded":true,"isPromoted":false,"isNewProduct":true,"isSale":false},"baseProduct":"O2463102","name":"Jordan Air Jordan Retro 4 - Men's","price":{"value":220.0,"formattedValue":"$220.00"},"originalPrice":{"value":220.0,"formattedValue":"$220.00"},"reviewRatings":{"reviews":5,"rating":5.0},"sku":"O2463102","imageSku":"O2463102","variantsCount":1}}
```

### maccosmetics_listing
```json
{
  "item_id": "MAC-12345",
  "title": "Foundation ...",
  "url": "https://www.maccosmetics.com/...",
  "price": 42.0,
  "currency": "USD",
  "brand": "MAC Cosmetics",
  "source": "maccosmetics_internal_api_graphql|maccosmetics_html"
}
```
Run examples:
- `common-scrapy crawl maccosmetics_listing -a category='face' -a mode=api -a max_pages=1 -O mac_api.jsonl`
- `common-scrapy crawl maccosmetics_listing -a category='face' -a mode=bootstrap -a max_pages=1 -O mac_bootstrap.jsonl`
- `common-scrapy crawl maccosmetics_listing -a category='face' -a mode=html -a max_pages=1 -O mac_html.jsonl`

### elfcosmetics_listing
```json
{
  "item_id": "8696341102680",
  "variant_id": "43876616192088",
  "title": "Soft Glam Satin Foundation",
  "url": "https://www.elfcosmetics.com/products/soft-glam-satin-foundation?Color=21+Light+Neutral",
  "price": 8.0,
  "currency": "USD",
  "brand": "e.l.f. Cosmetics",
  "available_for_sale": true,
  "selected_options": [{"name": "Color", "value": "21 Light Neutral"}],
  "images": [{"altText": "...", "url": "https://cdn.shopify.com/..."}],
  "swatches": [{"availableForSale": true, "color": "#d8a47e"}],
  "category": "face",
  "page": 1,
  "source": "elfcosmetics_hydrogen_bootstrap"
}
```
The spider decodes Shopify Hydrogen's streamed React Router bootstrap data. It
exports product and variant IDs, availability, images, selected options,
swatches, pricing, and the raw product object, then follows bootstrap pagination.

Run example:
`common-scrapy crawl elfcosmetics_listing -a category=face -a max_pages=1 -O elfcosmetics_listing.jsonl`

### oreilly_listing

`oreilly_listing` reads one authoritative source: the server-rendered
`window._ost` bootstrap assignments. It does not parse product cards or JSON-LD.
The spider exports the ordered `FEED_EXPORT_FIELDS` contract, validates the
bootstrap totals, deduplicates item IDs, and supports standard query pagination.
The 34 stable root departments live in `oreilly_categories.py`; a product-bearing
leaf can also be supplied with `-a category_url=<url>`. Storefront requests need
the configured ScrapeOps US residential route and use a Googlebot user agent.

```bash
scrapy crawl oreilly_listing -a category_url=https://www.oreillyauto.com/shop/b/brakes/brake-drums---rotors/7145c118aa8d -a max_pages=1 -s HTTPCACHE_ENABLED=False -O oreilly.jsonl
```

### backcountry_listing

Backcountry listing spider backed by the server-rendered Next.js hydration
payload (`#__NEXT_DATA__`). One data direction only: the bootstrap state. There
is no HTML/JSON-LD fallback, so if the payload, the PLP data or the product
edges disappear the spider fails loudly instead of silently degrading.

- **Arguments:** `-a category=<slug>`, `-a category_url=<url>`, or `-a url=<url>`;
  plus `-a max_pages=<n>`.
- **Categories:** 469 slugs shaped `<department>/<section>/<name>`, e.g.
  `men/clothing/shirts`, `women/outerwear/rain-jackets`,
  `sale/outlet/deals-under-50`. See `backcountry_categories.py` for the full
  tree.
- **Pagination:** `?page=N` up to `max_pages` and the payload's `totalPages`.
  The page parameter is appended to the existing query verbatim, so
  brand-filtered URLs (`?p=gender_uFilter:"male"`) keep their filter.
  Products are de-duplicated by `Product.id` across pages.
- **Output:** 36 normalized fields plus `raw`, which holds the verbatim hydration
  record.

Hydration paths read:

```text
props.pageProps.type                              # plp-cat | plp-collection | plp-brand
props.pageProps.plpData.data.<category|collection|brand>.edges[]
props.pageProps.plpData.data.<...>.pageInfo       # hasNextPage / hasPreviousPage
props.pageProps.totalPages                        # e.g. 36 for mens-shirts
props.pageProps.__APOLLO_STATE__["Product:<id>"]  # normalized product record
```

The three PLP page types share one block shape, so the spider resolves the
listing block by shape rather than branching on the page-type string:

| Slug | URL shape | `type` | `plpData.data` key | Listing id field |
|---|---|---|---|---|
| `men/clothing/shirts` | `/cat/mens-shirts` | `plp-cat` | `category` | `categoryId` |
| `men/clothing/sun-protection` | `/rc/mens-upf-apparel` | `plp-collection` | `collection` | `collectionId` |
| `men/top-brands/patagonia` | `/brand/patagonia?p=...` | `plp-brand` | `brand` | `brandSlug` |

Price uses `aggregates.minSalePrice` (current) and `aggregates.minListPrice`
(list); `minDiscount` becomes `discount_percent`, and `on_sale` is true when the
sale price is below list price or any variation is on sale.

#### Proxy: residential is mandatory

Backcountry sits behind an AWS WAF. The datacenter ScrapeOps route returns a
~2.3 KB `window.awsWafCookieDomainList` challenge with HTTP 200; only the
residential pool returns the real ~1 MB category HTML. `_residential_proxy()`
appends `residential=true` to the ScrapeOps username on every request, preserving
existing username options (e.g. `country=us.bypass=7`) and the credentials. The
proxy password is never logged.

A challenge response raises an actionable error naming that remedy instead of
producing zero items. The check matches the specific `awsWaf` token rather than a
generic "captcha" marker, because the real category page embeds a
`grecaptcha-badge` style block that a loose marker would reject.

Verification — live crawls on 2026-10-05 with the HTTP cache disabled:

```bash
scrapy crawl backcountry_listing -a category=men/clothing/shirts -a max_pages=1 \
  -s HTTPCACHE_ENABLED=False -O backcountry.jsonl
```

| Run | Result |
|---|---|
| `category=men/clothing/shirts max_pages=1` | 1 request, HTTP 200, `item_scraped_count: 42` |
| `category=men/clothing/shirts max_pages=2` | 2 requests, HTTP 200 x2, `item_scraped_count: 84` (42 + 42, zero overlap) |
| `category=men/clothing/sun-protection max_pages=1` (`/rc/` collection) | 1 request, HTTP 200, `item_scraped_count: 42` |
| `category=men/top-brands/patagonia max_pages=1` (brand page) | 1 request, HTTP 200, `item_scraped_count: 42` |

Every one-page run returned 42 products with 42 distinct `item_id`s, a
non-null `brand`, `price` and `image_url`, and absolute `https://www.backcountry.com/...`
product URLs. Sample of the `mens-shirts` run (trimmed, `raw` elided):

```json
{"item_id": "FJRZ133", "title": "Fjallglim Regular Shirt - Men's", "brand": "Fjallraven", "url": "https://www.backcountry.com/fjallraven-fjallglim-regular-shirt-mens", "listing_url": "https://www.backcountry.com/cat/mens-shirts", "price": 124.95, "original_price": 124.95, "currency": "USD", "on_sale": false, "discount_percent": 0.0, "availability": "IN_STOCK", "in_stock": true, "stock_status": "IN_STOCK", "image_url": "https://www.backcountry.com/images/items/large/FJR/FJRZ133/DANACHWH.jpg", "color": "Dark Navy/Chalk White", "colors": ["Dark Navy/Chalk White", "Dark Navy/Maroon", "Wood Brown/Black Oak"], "color_count": 3, "total_variations": 10, "department": "Men", "section": "Clothing", "category_name": "Shirts", "category_slug": "men/clothing/shirts", "category_id": "bc-mens-shirts", "page": 1, "source": "backcountry_next_data"}
```

A sale-priced example from the same run, showing `aggregates.minSalePrice` /
`minListPrice` / `minDiscount` mapping:

```json
{"item_id": "BJOC0B1", "title": "Tempo T-Shirt - Men's", "brand": "Bjorn Daehlie", "price": 20.97, "original_price": 34.95, "currency": "USD", "on_sale": true, "discount_percent": 40.0, "variations_on_sale": 7, "availability": "IN_STOCK", "in_stock": true}
```

Sample of the `/rc/` collection run (`category_id` comes from the SSR payload's
`collectionId`, labels from the taxonomy):

```json
{"item_id": "BCCZ2PL", "department": "Men", "section": "Clothing", "category_name": "Sun Protection", "category_slug": "men/clothing/sun-protection", "category_id": "mens-upf-apparel", "page": 1, "source": "backcountry_next_data"}
```

Tests: `python -m unittest tests.test_backcountry_listing_spider` (54 network-free
tests: taxonomy normalization, page-1 parsing, page-2 request creation,
`max_pages` / `totalPages` / `hasNextPage` stop conditions, dedup across pages,
Apollo join, all three PLP page types, absolute URLs, prices, sale/discount,
availability, invalid and missing hydration, WAF challenge detection, and proxy
routing).

### newegg_listing

Category listing spider backed by Newegg's server-rendered hydration payload
(`window.__initialState__.Products`), parsed with a balanced JSON decoder so a
later `<script>` block cannot corrupt the match.

- **Arguments:** `-a category=<name>`, `-a category_url=<url>`, or `-a url=<url>`;
  plus `-a max_pages=<n>`.
- **Categories:** `desktop-cpu-processors` (a concrete `/SubCategory/` URL) and
  `all-current-categories` (the live `api/RolloverMenu` inventory).
- **Pagination:** follows `/Page-N` up to `max_pages` and the `TotalItemCount`
  total. The page size is taken from the first page and carried forward through
  `cb_kwargs`, so a partial final page cannot inflate the computed last page and
  schedule an out-of-range request.
- **Output:** normalized product fields plus `raw`, which holds the verbatim
  hydration entry for each item.

Verification — live crawl on 2026-10-02 with the HTTP cache disabled:

```bash
python -m common_scrapy.cli crawl newegg_listing \
  -a category=desktop-cpu-processors -a max_pages=1 \
  -s HTTPCACHE_ENABLED=False -O newegg.jsonl
```

Result: 1 request, HTTP 200, `item_scraped_count: 36`. All 36 exported items carry
a non-empty `raw` object. Sample (trimmed, `raw` elided):

```json
{"item_id": "19-113-877", "title": "AMD Ryzen 7 9800X3D - Ryzen 7 9000 Series Zen 5 8-Core 5.2 GHz - Socket AM5 120W - AMD Radeon Graphics Desktop Processor - 100-100001084WOF", "model": "100-100001084WOF", "brand": "AMD", "price": 469, "original_price": 497.49, "currency": "USD", "url": "https://www.newegg.com/amd-ryzen-7-9000-series-ryzen-7-9800x3d-granite-ridge-zen-5-socket-am5-desktop-cpu-processor/p/N82E16819113877", "image": "https://c1.neweggimages.com/ProductImageOriginal/19-113-877-01.png", "rating": 4.8, "reviews_count": 729, "seller": "Newegg", "in_stock": true, "shipping_charge": 0.01, "ships_from": "United States", "category": "CPU", "subcategory": "Desktop CPU Processor", "page": 1, "source": "newegg_initial_state", "raw": {"ProductNumber": "19-113-877", "ItemCell": {"FinalPrice": 469, "...": "..."}}}
```

The `36 (ok)` figure above is a single verified `max_pages=1` run on 2026-10-02.
Multi-page totals are **not** live-verified in this PR; Newegg's page size and
inventory vary by location and change over time.

### ae_listing
```json
{
  "item_id": "1457_2980_808",
  "title": "AE Big Hug V-Neck Sweatshirt",
  "url": "https://www.ae.com/us/en/p/women/hoodies-sweatshirts/crew-neck-sweatshirts/ae-big-hug-v-neck-sweatshirt/1457_2980_808",
  "price": 38.97,
  "original_price": 64.95,
  "currency": "USD",
  "brand": "American Eagle",
  "rating": 4.7,
  "reviews_count": 123,
  "image_url": "https://images.ae.com/is/image/aeo/1457_2980_808_of?$pdp-m-opt$",
  "category": "women",
  "subcategory": "tops",
  "listing_url": "https://www.ae.com/us/en/c/women/tops/cat10049",
  "source": "ae_fastboot_shoebox",
  "mode": "browse_api"
}
```
Run example:
- `common-scrapy crawl ae_listing -a category='women' -a max_pages=1 -O ae_listing.jsonl`

Notes:
- The spider accepts category selection only; direct `url` and `category_url` overrides are not used.
- Category pages expose the authoritative product payload in FastBoot shoebox scripts (`<script type="fastboot/shoebox">`) with IDs that base64url-decode to `/browse/v1/category/{category}`.
- Selecting a category (`women`, `men`, or `aerie`) starts every configured subcategory in that group.
- Pagination uses `/browse/v1/category/{category}?offset={offset}&rows={rows}` with `meta.offset`, `meta.rows`, and `meta.totalProducts`.
- Requests should keep browser-like headers (`accept`, `accept-language`, `referer`, `user-agent`, and `x-requested-with`).

### nike_listing

Nike runs a Next.js catch-all route (`/w/[[...slug]]`). The product wall is
hydrated into `script#__NEXT_DATA__` on page 1, and every later page is served by
the first-party product-wall API on `api.nike.com`:

```
/discover/product_wall/v1/marketplace/US/language/en/consumerChannelId/<uuid>
    ?path=/w/<slug>&attributeIds=<uuids>&queryType=PRODUCTS&anchor=<n>&count=<n>
```

This spider uses exactly one data direction -- that hydration state and the API it
points at. There is no HTML card scraping and no rendered-browser fallback. Both
legs return the same product object shape, so a single parser builds every item.

Two details are load-bearing:

- `api.nike.com` rejects requests without `nike-api-caller-id`, answering HTTP 200
  with `{"errors":[{"code":"NIKE_API_CALLER_ID_HEADER_NOT_PRESENT"}]}` -- so a
  status check alone would read a rejected request as a valid empty last page.
  The spider raises on that envelope instead.
- ScrapeOps strips custom request headers by default, so the API leg applies the
  provider's `keep_headers=true` username option (mirroring
  `costco_listing_spider._search_api_proxy`); without it the header is dropped in
  transit and Nike returns exactly that error.

The bundled inventory preserves the desktop global navigation hierarchy
(`department -> group -> subcategory -> url`), flattened to 168 unique URLs across
Men, Women, Kids, Jordan, NikeSKIMS, and Sport. Six URLs are linked from two
departments (for example `/w/sunglasses-arlyp` from both Men and Women); the
spider deduplicates by URL and keeps the first department, matching the
repository convention. Entries are keyed by the URL path slug (for example
`mens-shoes-nik1zy7ok`), which is already unique across the whole inventory.

Grouping is *not* the unit of output: a `productGroupings[]` entry holds every
colorway it collects and each has its own `productCode`, so collapsing to one item
per group would silently drop colorways. Items are deduplicated by
`(category, productCode)`.

Pagination reads the next relative path from the previous response's own
pagination field (`Wall.pageData.next` on page 1, `pages.next` afterwards) and
never hard-codes the channel/attribute UUIDs or the anchor, because Nike rotates
them. The crawl stops at `max_pages` or when the current page carries no further
`next`.

Run examples:

- `common-scrapy crawl nike_listing -a category=mens-shoes-nik1zy7ok -a max_pages=2 -O nike.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl nike_listing -a category=womens-shoes-5e1x6zy7ok -a max_pages=1 -O nike_women.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl nike_listing -a category_url='https://www.nike.com/w/mens-shoes-nik1zy7ok' -a max_pages=1 -O nike.jsonl`

The ordered export fields are `category`, `department`, `group`, `item_id`,
`title`, `subtitle`, `url`, `image_url`, `price`, `list_price`,
`discount_percent`, `employee_price`, `currency`, `color`, `color_hex`,
`color_description`, `product_type`, `availability`, `badge`, `promotion`,
`is_new_until`, `page`, `category_url`, `source`, and `raw`.

```json
{
  "category": "mens-shoes-nik1zy7ok",
  "department": "Men",
  "group": "Shoes",
  "item_id": "IX3952-600",
  "title": "Nike Moon Shoe OG",
  "subtitle": "Men's Shoes",
  "url": "https://www.nike.com/t/moon-shoe-og-mens-shoes-QjBip6mn/IX3952-600",
  "image_url": "https://static.nike.com/a/images/t_default/.../NIKE+MOON+SHOE+OG.png",
  "price": 105,
  "list_price": null,
  "discount_percent": null,
  "employee_price": 63,
  "currency": "USD",
  "color": "Red",
  "color_hex": "B40033",
  "color_description": "Tough Red/Mystic Dates/Gum Light Brown/Sail",
  "product_type": "FOOTWEAR",
  "availability": "InStock",
  "badge": "Just In",
  "promotion": null,
  "is_new_until": "2026-10-14T14:00:00.000Z",
  "page": 1,
  "category_url": "https://www.nike.com/w/mens-shoes-nik1zy7ok",
  "source": "nike_next_data",
  "raw": { "productCode": "IX3952-600", "copy": { "title": "Nike Moon Shoe OG" } }
}
```

Notes:

- `price` is `prices.currentPrice` and `list_price` is only populated when
  `discountPercentage` is non-zero, so an undiscounted item does not report the
  same value twice as if it had been marked down.
- `availability` maps Nike's `featuredAttributes`: `COMING_SOON` -> `PreOrder`,
  `RESTOCK` -> `BackInStock`, otherwise `InStock`.
- `promotion` carries the customer-facing promotion title from the first `PW`
  product-wall visibility (for example "See Price in Bag").
- `source` is `nike_next_data` for page 1 and `nike_product_wall_api` for later
  pages.
- The spider fails loudly on a non-200 response, an access-denied/challenge body,
  a missing `script#__NEXT_DATA__` block, a missing
  `props.pageProps.initialState.Wall`, a malformed JSON body, a response missing
  `productGroupings`, a product without a `productCode`, or a Nike `errors`
  envelope, so a retired category slug or a stripped caller header cannot
  masquerade as an empty listing.
- Fixtures live in `sample/nike-listing-next-data.html`,
  `sample/nike-product-wall-page.json`, and `sample/nike-categories.json`.
- Tests: `.venv/bin/python -m unittest tests.test_nike_listing_spider`
  (33 network-free fixture tests).
### williams_sonoma_listing

Williams-Sonoma (US) category listings via the Constructor.io browse API. The
category taxonomy is pulled from the first-party category-tree JSON API on every
run, so category changes on the site are reflected without spider updates;
product data comes from `https://ac.cnstrc.com/browse/group_id/{group_id}`.

No HTML parsing or rendered browser is used: category pages are JavaScript
shells that hydrate products client-side. The spider reads the Constructor.io
API key from `window.__INITIAL_STATE__` on a sample category page once per run
and then queries the browse endpoint directly; if the key cannot be read it
fails loudly rather than falling back to a hardcoded value.

Select a category by `group_id`, by URL, or crawl every category:

- `common-scrapy crawl williams_sonoma_listing -a category=cookware-sets -a max_pages=1 -O ws.jsonl`
- `common-scrapy crawl williams_sonoma_listing -a category_url='https://www.williams-sonoma.com/shop/cookware/cookware-sets/' -a max_pages=1 -O ws.jsonl`
- `common-scrapy crawl williams_sonoma_listing -a all_categories=true -a max_pages=1 -O ws-full.jsonl`

Pagination follows the `page` parameter until `page * page_size >= total_num_results`,
`max_pages` is reached, or a page returns no results. Products are deduplicated by
`item_id`. Editorial/collection hubs that exist in the taxonomy but have no
Constructor group behind them are logged and skipped instead of failing the crawl.

Export contract: `category`, `category_name`, `parent_category`, `item_id`,
`title`, `url`, `brand`, `sku`, `price`, `regular_price`, `price_min`,
`price_max`, `regular_price_min`, `regular_price_max`, `sale_price_min`,
`sale_price_max`, `discount_percent`, `price_type`, `currency`, `image_url`,
`image_alt`, `alt_images_count`, `swatches_count`, `flags`, `pip_type`,
`quick_buy`, `description`, `short_description`, `product_details`, `group_ids`,
`page`, `category_url`, `source`, and `raw`.

Fixtures: `sample/williams-sonoma-category-tree.json`,
`sample/williams-sonoma-browse-items.json`, and
`sample/williams-sonoma-context.html`. Tests:
`python -m unittest tests.test_williams_sonoma_listing_spider` (29 network-free
fixture tests).

```json
{"category":"cookware-sets","category_name":"Cookware Sets","parent_category":"Cookware","item_id":"greenpan-reserve-pro-ceramic-nonstick-10-piece-cookware-set","title":"GreenPan™ Reserve Pro Ceramic Nonstick 10-Piece Cookware Set","url":"https://www.williams-sonoma.com/products/greenpan-reserve-pro-ceramic-nonstick-10-piece-cookware-set/","brand":null,"sku":10486629,"price":399.95,"regular_price":580,"price_min":399.95,"price_max":399.95,"discount_percent":31,"price_type":"Discount","currency":"USD","image_url":"https://assets.wsimgs.com/wsimgs/rk/images/dp/wcm/202631/0164/img2c.jpg","flags":["freeShip","more_colors","newcore","organic"],"pip_type":"simple-buy","quick_buy":true,"page":1,"category_url":"https://www.williams-sonoma.com/shop/cookware/cookware-sets/","source":"williams_sonoma_constructor_browse"}
```

Verified live (`category=cookware-sets`, `max_pages=1`, ScrapeOps proxy,
2026-10-02 UTC): **100 items, 100 unique `item_id`s**, with `raw` present on
100/100.
### vitacost_listing

`vitacost_listing` uses one authoritative source: the first-party Boost AI Search
& Discovery filter API that the storefront itself calls for every grid refresh.
No product HTML is parsed, no JSON-LD.

```http
GET https://services.mybcapps.com/bc-sf-filter/filter
    ?_=pf&shop=icost.myshopify.com&collection_scope=457575104827&page=1&limit=48
    &pg=collection_page&event_type=init&build_filter_tree=true&sort=best-selling
Referer: https://www.vitacost.com/collections/supplements
```

The response is a normalized Shopify product feed, which carries much more than the
rendered cards expose:

| Path | Contents |
|---|---|
| `products[]` | full product records: `id`, `handle`, `title`, `vendor`, `price_min`, `compare_at_price_min`, `percent_sale_min`, `variants[]` (SKU, barcode, stock), `images_info[]`, `tags[]`, `collections[]`, `metafields[]` |
| `total_product` | category size, used as the pagination stop condition |
| `filter.options[]` | the `multi_level_tag` "Category" facet tree (parent -> child -> `doc_count`) |
| `meta` | `currency`, `money_format` |

Two request details matter:

* **`collection_scope` must be the numeric Shopify collection id.** Passing a handle
  silently returns the whole 55,327-product shop, and dropping the parameter does the
  same. The spider therefore fetches the collection page once per run and reads
  `generalSettings.collection_id` out of the Boost boot payload
  (`function readPayload(){return {generalSettings:{page: "collection", collection_id: 458194583867, ...}}}`);
  every product field still comes from the API. Shopify also stamps the id into its
  `collection_viewed` analytics payload, which is a usable fallback for the same value.
* **`limit` is capped server-side.** `limit=48` returns 48 products, `limit=100`
  returns 20, so the spider defaults to 48 and clamps any `-a limit=` to 50.

The storefront request goes through `settings.PROXY`; the Boost request must **not**,
because the configured ScrapeOps tunnel refuses to CONNECT to `services.mybcapps.com`
(`407 Proxy Authentication Required`). `VitacostProxyMiddleware` replaces
`CommonDownloaderMiddleware` for this spider and proxies only `www.vitacost.com`.

Field notes:

* `original_price` uses `compare_at_price_min`, which Shopify fills with the current
  price on non-reduced products, so equal prices collapse to `null` with
  `on_sale=false`. `discount_percentage` prefers the API's `percent_sale_min` and falls
  back to computing it from the two prices.
* `rating` / `reviews_count` come from the Judge.me metafields (`rating`,
  `rating_count`) -- the API's own `review_count` is always `0`. `badges` is the
  `Clearance` / `OnSale` metafields with the literal `Full Price` values dropped.
* `package_quantity`, `form` and `strength` are merchant metafields
  (`PackageQuantity`, `Form`, `Strength`).
* `options` / `option_count` cover real variants only; single-variant products ship a
  `Default Title` option that is filtered out.
* `raw` is the API record minus `body_html`, which is the full page copy and dwarfs
  every other field. The first 400 characters are exposed as `description`.

Taxonomy lives in `vitacost_categories.py`: the 8-department `Categories` mega-menu
extracted on 2026-10-04, flattened to **92 category entries** (**90 unique collection
URLs** -- `Sunscreen` and `Essential Oils & Aromatherapy` each exist under two
departments, so `category` is qualified as `Department > Label`).

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl vitacost_listing -a category="Supplements" -a max_pages=2 -O vitacost.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category": "Supplements", "department": "Supplements", "subcategory": null, "handle": "supplements", "collection_id": "457575104827", "item_id": "10390080782651", "title": "Vitacost, Root2®, Turmeric Extract Curcumin C3 Complex®, 120 Capsules", "url": "https://www.vitacost.com/products/vitacost-root2-turmeric-extract-curcumin-c3-complex-120-capsules-158591/", "brand": "Vitacost", "product_type": "[Vitacost Brands][SuperDeal]", "tags": "Antioxidants, Supplements, Turmeric & Curcumin, ...", "price": 24.74, "original_price": 32.99, "discount_percentage": 25.0, "currency": "USD", "on_sale": true, "out_of_stock": false, "in_stock_quantity": 3508, "image_url": "https://cdn.shopify.com/s/files/1/0804/8974/2651/files/10_da6689c1-38d5-4f54-8e85-b694eb0f26d1.jpg?v=1781816097", "image_alt": "Vitacost, Root2®, Turmeric Extract Curcumin C3 Complex®, 120 Capsules", "image_count": 2, "sku": "158591", "barcode": "835003004423", "package_quantity": "120 - 179 count", "form": "Capsule", "strength": "1000 - 4999 mg", "badges": "Clearance, On Sale", "description": "Description 1,160 mg Per Serving Featuring BioPerine® ...", "rating": 4.72, "reviews_count": 484, "published_at": "2026-05-18T23:03:16Z", "page": 1, "position": 1, "total_count": 25399, "scraped_timestamp": "2026-10-04 11:21:40", "source_url": "https://services.mybcapps.com/bc-sf-filter/filter?_=pf&shop=icost.myshopify.com&collection_scope=457575104827&page=1&limit=48", "source": "vitacost_boost_filter_api", "raw": {"skus": ["158591"], "available": true, ...}}
```

Fixtures: `sample/vitacost-collection-page.html`,
`sample/vitacost-boost-filter-supplements-page1.json`,
`sample/vitacost-boost-filter-supplements-page2.json`,
`sample/vitacost-boost-filter-empty.json`. Tests:
`python -m unittest tests.test_vitacost_listing_spider` (29 network-free
fixture tests).

Verified live (`category=Supplements`, `max_pages=2`, page size 48, ScrapeOps proxy
for the storefront leg, 2026-10-04 UTC): **96 items** (48 + 48), 96 unique
`item_id`s, `total_count=25399`, 3 requests all HTTP 200. Same for
`category="Supplements > Vitamins"`: **96 items**, `total_count=4079`,
`collection_id=458194583867`.

### dickssportinggoods_listing
```json
{
  "category": "soccer-gear-equipment",
  "department": "Sports",
  "category_name": "Soccer",
  "category_id": 201847,
  "category_url": "https://www.dickssportinggoods.com/c/soccer-gear-equipment",
  "category_page_type": "c",
  "item_id": "13286436",
  "partnumber": "26968873",
  "parent_partnumber": "25ADIUSOCCWC26HSTMFAA",
  "title": "adidas FIFA World Cup Historical Mini Soccer Ball Set",
  "brand": "adidas",
  "url": "https://www.dickssportinggoods.com/p/adidas-fifa-world-cup-historical-mini-soccer-ball-set-25adiusoccwc26hstmfaa/25adiusoccwc26hstmfaa",
  "image_url": "https://dks.scene7.com/is/image/dkscdn/25ADIUSOCCWC26HSTMFAA_White?$DSG_ProductCard$",
  "price": 141.52,
  "list_price": 250.0,
  "map_price": null,
  "discount_percent": 43.39,
  "currency": "USD",
  "rating": 4.72,
  "reviews_count": 125,
  "is_coming_soon": false,
  "is_color_pinned": false,
  "primary_category": "SoccerBalls-253295",
  "page": 1,
  "position": 1,
  "total_count": 5577,
  "source": "dickssportinggoods_search_api"
}
```
Run examples:
- `common-scrapy crawl dickssportinggoods_listing -a category=soccer-gear-equipment -a max_pages=2 -O dickssportinggoods.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl dickssportinggoods_listing -a url=https://www.dickssportinggoods.com/c/soccer-gear-equipment -a max_pages=1 -O dickssportinggoods.jsonl`
- `common-scrapy crawl dickssportinggoods_listing -O dickssportinggoods.jsonl` (crawls the whole taxonomy)

Notes:
- Uses exactly one data direction: the first-party catalog product-search API,
  `GET https://prod-catalog-product-api.dickssportinggoods.com/v2/search?searchVO=<json>`,
  with `selectedCategory="12301_<catgroupId>"`, `storeId=15108`, and
  `pageSize=48`. The PLP HTML carries no product cards (only a
  `dcsg-ngx-plp-server-state` blob), so there is no HTML fallback; a bot wall
  raises a clear error instead of silently yielding empty tile shells.
- The bundle `dickssportinggoods_categories.py` captures the SEO category tree
  (`GET api-search.dickssportinggoods.com/seo-category/v1/categories`) as
  **1685 nodes across 10 departments (153 level-2, 1522 level-3)**, which
  collapse to **1287 unique category URLs** (cross-listed nodes repeat with the
  same `catgroupId`). Every request's `selectedCategory` is `12301_<catgroupId>`,
  so a target must match the bundled inventory; `category`, `category_url`, and
  `url` all resolve against it.
- The catalog host is Akamai-protected: the plain datacenter ScrapeOps route is
  rejected, so the spider appends `scrapeops.country=us.bypass=5` to the proxy
  username for product requests only. The SEO category host needs no bypass.
- `price` is the `offerprice` facet whose `[start,end]` window contains "now"
  (the payload carries several historical/upcoming windows), falling back to
  `listprice`. `list_price`, `map_price`, and `discount_percent` come from the
  same `floatFacets`/`dsgPriceIndicators` block. `product_attributes` is the
  parsed `attributes` JSON (e.g. `X_BRAND`, `PRIMARY_CATEGORY_DSG`).
- The ordered export fields are `category`, `department`, `category_name`,
  `category_id`, `category_url`, `category_page_type`, `item_id`, `partnumber`,
  `parent_partnumber`, `title`, `brand`, `url`, `image_url`, `image_alt`, `price`,
  `list_price`, `map_price`, `discount_percent`, `currency`, `rating`,
  `reviews_count`, `is_coming_soon`, `is_color_pinned`, `product_attributes`,
  `primary_category`, `page`, `position`, `total_count`, `source_url`, `source`,
  and `raw`.
- Live verification (`-s HTTPCACHE_ENABLED=False`, `category=soccer-gear-equipment`,
  `max_pages=1`, 2026-10-02 UTC) exported **48 unique items** with `raw` present
  on all 48. The API reported `totalCount=5577` for the category, so the run was
  bounded by `max_pages`. A first attempt returned a transient ScrapeOps error
  page and no items; the retry succeeded with zero errors.

### tractorsupply_listing

`tractorsupply_listing` uses one data direction: official product sitemaps
discover PDP URLs, and each PDP's structured Next.js `__NEXT_DATA__` bootstrap
supplies the product record. There is no HTML-card or JSON-LD fallback. Each
`max_pages` unit processes 24 product URLs.
For a small smoke test, `-a max_items=3` caps each selected sitemap explicitly.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl tractorsupply_listing \
  -a category=products-1 -a max_pages=1 -O tractorsupply.jsonl \
  -s HTTPCACHE_ENABLED=False
```

The four bundled targets correspond to the official product sitemap shards. The
ordered export contract is `category`, `department`, `category_name`,
`item_id`, `sku`, `title`, `brand`, `url`, `image_url`, `price`,
`list_price`, `currency`, `availability`, `rating`, `reviews_count`,
`primary_category`, `source_url`, `source`, and `raw`.

Product fields come only from `props.pageProps.pageProps.pdpData.productDetails`
inside `__NEXT_DATA__`; missing bootstrap state fails visibly.

## Contributing

### fashionnova_listing

```bash
scrapy crawl fashionnova_listing -a category=dresses -a max_pages=1 \
  -s HTTPCACHE_ENABLED=False -O fashionnova.jsonl
```

The category map mirrors the current Fashion Nova women's navigation, including
the current dress occasion subcategories. Product data comes from the
server-rendered Schema.org `CollectionPage` / `ItemList` JSON-LD; pagination uses
the collection `page` query parameter. The spider intentionally does not parse
Hydrogen's internal serialized React stream.

Each item uses the stable `FEED_EXPORT_FIELDS` order defined by the spider and
includes SKU, prices, availability, canonical URL, image, category context,
page, extraction source, and the original JSON-LD product object.

Issues and pull requests that add or improve retailer spiders, pagination logic, or extraction helpers are welcome.

### michaels_listing

`michaels_listing` uses one authoritative source: the Next.js App Router
**React Server Component** payload. Michaels has no `__NEXT_DATA__` blob -- the
server streams its flight payload through `self.__next_f.push([1, "<json>"])`.
Concatenating those chunks gives one text buffer in which the whole product
grid is already present as `initialProducts` (40 rows per window), next to
`initialTotal` (the true category size) and `initialFilters` (facets with
counts). Nothing has to be re-requested client-side and nothing is scraped out
of rendered DOM, so there is no HTML fallback path.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl michaels_listing --category home-decor-floral-arrangements -a max_pages=2 -O michaels.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"home-decor-floral-arrangements","department":"home-decor","subcategory":"floral-arrangements","item_id":"10809872","sku":"10809872","master_sku":null,"title":"11\" Pink Peony & Cream Rose Mix Bouquet by Ashland®","brand":"Michaels","product_category":"Fall Stem Bundles","taxonomy_path":"Fall Stem Bundles","url":"https://www.michaels.com/product/11-pink-peony-cream-rose-mix-bouquet-by-ashland-10809872","image_url":"https://imgs.michaels.com/7903ee7b-1298-4ad2-9244-56224c0f6033.jpg?fit=inside|540:540","image_count":3,"price":9.99,"original_price":null,"currency":"USD","on_sale":false,"rating":4.5,"reviews_count":16,"badges":"Same Day Delivery|Free Store Pickup","store_pickup":false,"same_day_delivery":true,"available_to_ship":true,"page":1,"position":1,"total_count":3319,"source":"michaels_nextjs_rsc_initial_products"}
```

Pagination is ordinary SSR: `?page=<N>` re-renders the route and hydrates the
next window, and a page past the end comes back as a valid document with
`initialProducts: []` and `initialTotal: 0`, so the crawl ends there instead of
erroring. Items are deduplicated by `skuNumber`.

Categories come from the sitemap the site advertises in `robots.txt`
(`sitemap_MIK_category.xml`), which is parsed at crawl time rather than
committed as a 3,611-entry literal -- 3,611 categories under 33 departments, up
to five levels deep. That is the only other request the spider makes, and it
exists solely to resolve `-a category=` to a PLP URL and to label items with
their department. **Leaf slugs repeat across departments** (the live sitemap has
five different `floral-arrangements` pages), so a repeated leaf is qualified
with its department: `home-decor-floral-arrangements`, `floral-floral-arrangements`.
`-a category_url=/shop/home-decor/floral-arrangements/` also works and needs no
slug lookup.

Field notes:

- `raw` is the full hydrated product record. The RSC protocol serialises absent
  values as the literal string `"$undefined"`; those are normalised to `null`
  rather than shipped into every exported row.
- `badges` is the boolean badge map flattened into labels (`Sale`, `Clearance`,
  `New`, `Great Buy`, `Everyday Value`, `Doorbuster`, `Coming Soon`,
  `Michaels Exclusive`, `Free Shipping`, `Same Day Delivery`, `Store Only`, ...).
- `availability` (`store_pickup`, `available_to_ship`, `same_day_delivery`,
  `in_stock`) reflects the fulfilment flags the PLP renders for the store the
  request was geo-routed to, so it is per-run state rather than a catalogue fact.
- `color_count` / `variant_count` come from `colorSwatches` / `variantCount`
  (`"Color:3"`); most listings rows carry none.

Tests: `python -m unittest tests.test_michaels_listing_spider` (22 tests, all
offline against the fixtures in `sample/`).

### urbanoutfitters_listing

`urbanoutfitters_listing` uses one product-data direction: the Vue/Pinia SSR
bootstrap state in `#urbnInitialPiniaState`. The script body is a JSON string
containing JSON, so it is decoded twice; products then come exclusively from
`category.pages[<currentPage>].wrapper.tiles`. The spider intentionally has no
rendered-card or JSON-LD fallback.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl urbanoutfitters_listing --category new-arrivals -a max_pages=2 -O urbanoutfitters.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"new-arrivals","item_id":"UO-106663735-000","style_id":"106663735","sku_id":"106663735_000","title":"Kimchi Blue Ella Flyaway Ruffle Lace Trim Cami","brand":"Kimchi Blue","url":"https://www.urbanoutfitters.com/shop/kimchi-blue-ella-flyaway-ruffle-lace-trim-cami","image_url":"https://images.urbndata.com/is/image/UrbanOutfitters/106663735_000_b3?wid=640","price":39,"currency":"USD","rating":4.7308,"reviews_count":26,"color":"Maroon","color_code":"000","in_stock":true,"page":1,"position":1,"total_count":1241,"total_pages":18,"source":"urbanoutfitters_pinia_ssr_tiles"}
```

Pagination requests the same SSR route with `?page=N`; the served bootstrap
contains only `pages["N"]`. Existing refinement parameters are preserved. The
live two-page validation on 2026-10-04 returned 144 unique products (72 per
page), including 18 markdowns, with no overlap between pages.

Categories are parsed at crawl time from `categories_sitemap.xml`, the
authoritative inventory linked by the site's sitemap index. The captured
sitemap had 2,158 unique PLP URLs, including 1,380 filtered variants; four of
the 12 curated navigation roots were absent and are added as stable aliases,
for 2,162 targets total. Filter aliases include every key/value pair, for
example `dresses-length-mini-sleeve-long-sleeve`. `-a category_url=` accepts
absolute or relative URLs and preserves their query string.

Price fields are colour-range aware: `price` / `price_high` reflect the live
sale range, while `sale_price`, `list_price`, and `discount_percentage` are set
only when `hasMarkdown` is true and the sale price is genuinely lower. `raw`
keeps the complete hydrated tile, including `product`, `skuInfo`, reviews, and
face-out colour context.

Tests: `python3 -m unittest tests.test_urbanoutfitters_listing_spider` (8 tests,
offline against committed sitemap and Pinia fixtures).

### Project layout

- `common/spiders/` – retailer spiders (`*_listing_spider.py`, `*_search_spider.py`) and shared helpers.
- `common/settings/` – shared Scrapy configuration; reads environment variables via `.env`.
- `scrapy.cfg` – entry point for the `scrapy` CLI.

### Adding new retailer spiders

1. Investigate real browser traffic and identify internal API/bootstrap/HTML patterns.
2. Implement a purpose-built spider under `common/spiders/` with normalized output fields.
3. Add category shortcuts (`categories`) where applicable.
4. Validate with `max_pages=1` runs and update README examples/output snippets.
### trulia_listing

Trulia sale-market listings are read exclusively from the page's Next.js
`__NEXT_DATA__` bootstrap state (`props.searchData.homes`); there is no HTML-card,
JSON-LD, or API fallback. The spider exposes the 20 `Homes For Sale` cities
highlighted on Trulia's homepage, including `colorado-springs-co`, `sacramento-ca`,
`los-angeles-ca`, `miami-fl`, `new-york-ny`, and `chicago-il`. Use
`scrapy crawl trulia_listing -a category=colorado-springs-co -a max_pages=2`.

Pagination follows canonical `/2_p/` links and deduplicates normalized ZPIDs.
The configured ScrapeOps proxy is amended idempotently with `residential=true`
and `bypass=5`; production use should be authorized against current site terms.
The ordered `FEED_EXPORT_FIELDS` contract includes property ID, address, URL,
price/currency, beds, baths, floor space, property type, coordinates, image,
provider/status, result count, page/position, source, and raw hydration record.
Every exported item also includes the crawl `timestamp`.

### Gap listing spider

`gap_listing` uses Gap's public commerce search API and exports a stable field
order through `FEED_EXPORT_FIELDS`. Choose `women`, `men`, or `girls`; each
selection expands to its maintained child listing URLs.

```bash
scrapy crawl gap_listing -a category=women -a max_pages=1 -O gap.jsonl
```

### klook_listing

`klook_listing` reads `window.__KLOOK__` only to discover the destination's
`ttd_acts` URL, then extracts products exclusively from that first-party JSON
API. It does not parse activity cards or JSON-LD. Klook's endpoint currently
returns 12 curated recommendations and advertises the larger catalogue through
`corner_button_deep_link`; `has_more`, `more_url`, and `total_count` are
exported rather than pretending those recommendations are full pagination.
Currency comes from the returned price text and is never inferred from locale.

```bash
scrapy crawl klook_listing -a category=japan -s HTTPCACHE_ENABLED=False -O klook.jsonl
```

### iherb_listing

`iherb_listing` uses one data direction: the first-party iHerb catalog JSON API.
It sends `POST https://catalog.app.iherb.com/category/<urlName>/products` with
`page` and `pageSize` (capped at 50). The response supplies richer product data
than the storefront cards, including part number, brand, current/list price,
promotions, rating counts, availability flags, product form, package quantity,
and recent-sales activity. There is no HTML-card, JSON-LD, or browser fallback.

The taxonomy in `common/spiders/iherb_categories.py` contains 380 normalized,
unique category URLs across nine departments. Category slugs are stable and
duplicate labels are department-qualified when necessary.

Run examples:

- `scrapy crawl iherb_listing -a category=magnesium -a max_pages=2 -O iherb.jsonl -s HTTPCACHE_ENABLED=False`
- `scrapy crawl iherb_listing -a category=supplements -a max_pages=1 -O supplements.jsonl -s HTTPCACHE_ENABLED=False`
- `scrapy crawl iherb_listing -a category_url=https://www.iherb.com/c/probiotics -a max_pages=1 -O probiotics.jsonl -s HTTPCACHE_ENABLED=False`

Pagination stops at `max_pages`, the API's `totalSize`, an empty page, or a
repeated product page. Non-JSON, empty-body, and missing-contract responses fail
loudly so bot challenges cannot masquerade as successful empty categories.

The ordered export contract is:

`category`, `department`, `subcategory`, `category_url_name`, `item_id`,
`part_number`, `title`, `product_name`, `brand`, `brand_code`, `url`,
`image_url`, `price`, `list_price`, `currency`, `currency_symbol`,
`discount_percent`, `promo_code`, `promo_message`, `rating`, `reviews_count`,
`in_stock`, `availability`, `back_in_stock_date`, `recent_activity`, `is_new`,
`is_shipping_saver`, `is_featured_brand`, `is_iherb_pick`,
`is_express_delivery`, `is_autoship`, `product_form`, `potency`,
`package_quantity`, `price_per_serving`, `product_status`, `group_id`, `page`,
`position`, `total_count`, `items_per_page`, `source_url`, `source`, and `raw`.

### victoriassecret_listing

`victoriassecret_listing` covers the Victoria's Secret and PINK US storefronts
via a **single data direction**: the first-party `stacks` JSON API. The category
SSR page is fetched only to discover the `collectionId` (plus the brand and the
`isBrasOrPanties` flag) from the embedded `<script id="clientProps">` block;
every product then comes from `api.victoriassecret.com`. There is no HTML card
scraping, no `__NEXT_DATA__` parsing, and no browser fallback.

Flow:

1. Fetch the category PLP and read `clientProps.reactQueryState.queries[]` for
   the entry whose `queryKey[0] == "collectionStacks"` -> `collectionId`,
   `brand`, `isBrasOrPanties` (`clientProps.brand` is the authoritative brand).
2. Page 0: `GET https://api.victoriassecret.com/stacks/v46/` with the full query
   (`activeCountry`, `collectionId`, `orderBy`, `limit`, `isDomestic`,
   `isBrasOrPanties`, `brand`, `maxSwatches`, `isPersonalized`,
   `isWishlistEnabled`, `recCues`) -> `stacks[0].list` plus `TotalItems`.
3. Pages 1..N: `GET .../stacks/v46/stack?...&offset=<n>`, advancing by the number
   of items the API actually served until `offset >= TotalItems`, `max_pages` is
   reached, or a page returns no products.

Two details worth knowing:

- **The trailing slash matters.** Page 0 is `.../stacks/v46/?...`; dropping the
  slash makes the gateway answer a flat `404 page not found` (HTTP 200 body).
  Load-more uses `.../stacks/v46/stack?...`.
- **A minimal query 400s.** `collectionId` + `brand` alone returns
  `{"error":"bad-request"}`; the full parameter set above is required.
- **Images need a rendition prefix.** The API returns extension-less paths
  (`png/zz/26/08/28/01/112955637I65_OM_F`); only the `380x507` rendition under
  `/p/<w>x<h>/<path>.jpg` resolved in testing.

Category shortcuts come from `common/spiders/victoriassecret_categories.py` (the
full `vs` + `pink` mega-menu, flattened to 427 targets). Slugs are
brand-prefixed (`vs-bras`, `vs-bras-push-up`) because leaf labels collide across
departments. Run the module directly to list or resolve them:

```bash
python -m common.spiders.victoriassecret_categories
python -m common.spiders.victoriassecret_categories --category vs-bras
```

Run examples:

- `common-scrapy crawl victoriassecret_listing --category vs-bras -a max_pages=3 -O vs.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl victoriassecret_listing --category pink-panties -a max_pages=1 -O pink.jsonl -s HTTPCACHE_ENABLED=False`
- `common-scrapy crawl victoriassecret_listing --category vs-bras-push-up -a max_pages=1 -O pushup.jsonl -s HTTPCACHE_ENABLED=False`

The export contract is ordered as:

`category`, `brand`, `top_category`, `sub_category`, `item_id`,
`master_style_id`, `name`, `family`, `color`, `url`, `image_url`, `price`,
`list_price`, `sale_price`, `alt_prices`, `currency`, `rating`, `reviews_count`,
`swatch_count`, `is_new`, `is_clearance`, `is_gift_card`, `page`, `category_url`,
`source`, and `raw`.

```json
{
  "category": "vs-bras",
  "brand": "vs",
  "top_category": "BRAS",
  "sub_category": null,
  "item_id": "11295563|7I65",
  "master_style_id": "5000010932",
  "name": "Signature Shine Cotton Lightly Lined Balconette Bra",
  "family": "The T-shirt",
  "color": "Print",
  "url": "https://www.victoriassecret.com/us/vs/bras-catalog/5000010932?brand=vs&collectionId=e88ab444-c093-4a29-a7c9-ef78f2a3e557",
  "image_url": "https://www.victoriassecret.com/p/380x507/png/zz/26/08/28/01/112955637I65_OM_F.jpg",
  "price": 49.95,
  "list_price": null,
  "sale_price": null,
  "alt_prices": ["or Buy 2, Get 1 Free VS Bras"],
  "currency": "USD",
  "rating": 4.52,
  "reviews_count": 269,
  "swatch_count": 16,
  "is_new": false,
  "is_clearance": false,
  "is_gift_card": false,
  "page": 1,
  "category_url": "https://www.victoriassecret.com/us/vs/bras",
  "source": "victoriassecret_listing"
}
```

Verified on 2026-10-03 UTC through the plain ScrapeOps datacenter route
(`scrapeops.country=us`, no `residential`/`bypass`), `HTTPCACHE_ENABLED=False`:

- `vs-bras`, `max_pages=2`: **192 items** (96 per page), all unique, `raw` present
  on 192/192, `image_url` present on 192/192.
- `pink-panties`, `max_pages=1`: **96 items**, `brand: pink` (brand read from
  `clientProps`, not the slug).
- `vs-bras-push-up`, `max_pages=1`: **96 items**, `sub_category: "Push-Up"`.

No HTML-card or `__NEXT_DATA__` path exists in this spider, so a gateway change
surfaces as a logged non-JSON response rather than silent empty results.

### zara_listing

`zara_listing` uses one data direction: Zara's first-party JSON APIs. It first
hydrates the current menu from `GET https://www.zara.com/us/en/categories`, then
requests the selected category from
`GET /us/en/category/<category_id>/products?ajax=true`. The products endpoint
returns the complete category in one response, so `max_pages` is accepted for
CLI consistency but values above one do not create duplicate requests.

The runtime taxonomy currently resolves **912 unique product URLs** across
WOMAN, MAN, KIDS, ZARA HOME, MASSIMO DUTTI, BEAUTY, PRE-OWNED, and one root
entry. Only `layout == "products-category-view"`, non-irrelevant nodes with a
complete SEO URL are crawlable. Repeated labels are disambiguated with their
full navigation path. Product extraction reads every
`productGroups[].elements[].commercialComponents[]`, keeps real
`type == "Product"` components, and filters editorial/outfit bundles. Product
IDs are deduplicated across merchandising blocks.

```bash
common-scrapy crawl zara_listing \
  --category 'WOMAN > COLLECTION > DRESSES' \
  -a max_pages=1 -O zara.jsonl -s HTTPCACHE_ENABLED=False
```

The ordered export contract (`FEED_EXPORT_FIELDS`) is:

`category`, `section`, `category_name`, `category_id`, `category_url`,
`item_id`, `partnumber`, `display_reference`, `title`, `kind`, `url`,
`image_url`, `image_alt`, `colors`, `color_count`, `price`, `original_price`,
`currency`, `discount_percent`, `availability`, `coming_soon`, `in_stock`,
`brand`, `family_name`, `subfamily_name`, `grid_position`, `page`, `position`,
`total_count`, `source_url`, `source`, and `raw`.

```json
{
  "category": "WOMAN > COLLECTION > DRESSES",
  "section": "WOMAN",
  "category_id": 2420895,
  "item_id": "560058525",
  "title": "STRIPED PUFF SLEEVE MINI DRESS",
  "price": 69.9,
  "currency": "USD",
  "availability": "in_stock",
  "source": "zara_api"
}
```

Verified live on 2026-10-04 through ScrapeOps US `bypass=5` with
`HTTPCACHE_ENABLED=False`: the taxonomy returned 912 unique product categories,
and `WOMAN > COLLECTION > DRESSES` returned **637 unique items** from one product
JSON response. There is no HTML-card, browser, bootstrap, or JSON-LD fallback;
changed API contracts raise explicit errors instead of returning a silent empty
feed.


### marriott_listing

`marriott_listing` crawls 20 featured Marriott city destinations and extracts
properties through one data direction only: the server-rendered Next.js
`__NEXT_DATA__` payload. The spider locates the page model's unique
`processedData.hotels` collection and emits stable property and brand IDs,
canonical property and review URLs, descriptions, all hydrated images, ratings,
review counts, distance, live rate/availability details, pagination context,
the raw bootstrap record, and a crawl timestamp.

Pagination follows Marriott's SSR `?pg=N` contract and stops on an empty page,
the advertised `totalProperties`, the configured `max_pages`, or a page with no
new property IDs. Every request uses the configured `PROXY`, amended
idempotently with `residential=true.country=us` for ScrapeOps. Missing or
ambiguous hydration fails explicitly; direct property-card HTML and JSON-LD are
not parsed as fallbacks.

```bash
scrapy crawl marriott_listing -a category=miami -a max_pages=2 \
  -O marriott.jsonl -s HTTPCACHE_ENABLED=False
```

The ordered output contract is defined in the spider's `FEED_EXPORT_FIELDS`.

### booking_listing

`booking_listing` crawls the first 20 US city destinations exposed by the
Booking.com homepage. It uses one extraction direction only: the anonymous
server-rendered Apollo cache in `<script type="application/json">`. The city
payload's `ROOT_QUERY.lxAccommodations(...)` supplies the destination ID and
`seeAllUrl`; each exhaustive search page then comes from
`ROOT_QUERY.searchQueries.search(...).results`. No HTML-card or JSON-LD parser
is used, and missing or ambiguous Apollo state raises an error.

Search pagination uses Booking's SSR `rows=25&offset=N` contract. Items are
deduplicated by property ID and include numeric price, ratings, review count,
coordinates, location, property type, canonical hotel URL, image URL. The
ordered `FEED_EXPORT_FIELDS` contract is defined on the spider and every exported
item also carries the crawl `timestamp` alongside the normalized `raw` record.

```bash
common-scrapy crawl booking_listing -a category=las-vegas -a max_pages=2 \
  -O booking.jsonl -s HTTPCACHE_ENABLED=False
```

Live verification on 2026-10-06 with the HTTP cache disabled returned three
HTTP 200 responses (one city handoff plus two search pages) and 33 unique
properties: 25 on page one and 8 on page two. Every exported item had a title,
canonical URL, image, numeric price/currency, rating, and review count. Booking's
live advertised total varied between the two undated SSR requests, so the spider
uses each response's own pagination metadata and property-ID deduplication.

### backcountry_listing

`backcountry_listing` uses one authoritative source: the server-rendered Next.js
hydration blob at `script#__NEXT_DATA__` -> `props.pageProps`, joined to the Apollo
cache the same payload carries. No HTML card scraping, no JSON-LD, no separate
product API call, no browser engine.

| Path | Contents |
|---|---|
| `props.pageProps.plpData.data.<container>.edges[].node` | the **ordered** products for that page (42/page) |
| `props.pageProps.__APOLLO_STATE__["Product:<id>"]` | the normalized product record for the same ids |
| `props.pageProps.plpData.data.<container>.pageInfo` | `hasNextPage`, `hasPreviousPage`, page cursors |
| `props.pageProps.totalCount` / `totalPages` | storefront-wide totals for the target |
| `props.pageProps.targeters.headerNavigation` | the full taxonomy, present in every SSR response |
| `props.pageProps.type` | `plp-cat` / `plp-collection` / `plp-brand` |

Pagination is plain SSR: the storefront honours the ordinary `?page=N` query
(`/cat/mens-shirts?page=2` returns 42 different edges with `hasPreviousPage=true`
and echoes `query.page` back in `__NEXT_DATA__`). The spider follows it until
`max_pages`, `totalPages`, or `pageInfo.hasNextPage === false`, and deduplicates by
product id across pages.

**The container key follows the PLP kind, not `pageProps.type`**, so the spider
locates it by shape -- the ordered `edges` array -- rather than by name. That keeps
all three target families working:

| Target family | URL | `type` | container key | Live result |
|---|---|---|---|---|
| Category | `/cat/mens-shirts` | `plp-cat` | `category` | 1490 products / 36 pages; 84 items over 2 pages |
| Collection (filtered) | `/rc/mens-parkas` | `plp-collection` | `collection` | 52 products / 2 pages; 42 + 10 items (natural last page) |
| Brand | `/brand/patagonia` | `plp-brand` | `brand` | 959 products / 23 pages |

Pricing comes from the numeric aggregates, never from display strings:
`aggregates.minSalePrice` is `price`, `aggregates.minListPrice` is `original_price`,
and `aggregates.minDiscount` is `discount_percentage`. A product is only reported as
on sale when `minDiscount > 0` *and* `minSalePrice < minListPrice`; otherwise the
item falls back to `price = minSalePrice` with a null `original_price`, so an
unreduced product never claims a 0% markdown. Availability is the storefront's own
`stockStatus` enum -- only `IN_STOCK` sets `in_stock = true`.

Color swatches hydrate as storefront-relative paths
(`/images/items/160/FJR/FJRZ133/DANACHWH.jpg`) and are resolved against
`https://content.backcountry.com`, the same CDN host the SSR `<img>` tags use.

**Proxy note.** Backcountry sits behind an AWS WAF. The plain datacenter route and
every `bypass` level return a 2.4 KB `window.awsWafCookieDomainList` interstitial
instead of the page, and the challenge never resolves server-side. Only the
residential route returns the real ~1 MB SSR document, so the spider appends
`residential=true` to the ScrapeOps username on its own requests
(`scrapeops.country=us.residential=true:<key>@proxy.scrapeops.io:5353`). Existing
ScrapeOps options are preserved, the flag is applied at most once, non-ScrapeOps
proxies pass through untouched, and the API key is never logged. Because the
interstitial contains no `#__NEXT_DATA__` script, a blocked run raises instead of
reporting a successful zero-item crawl.

The taxonomy in `backcountry_categories.py` is **398 unique crawlable URLs** reduced
from the 470 link entries the homepage header emits (14 top-level menus, 110
sections): 71 entries repeat a URL already seen under another menu and the first
(menu-alphabetical) label wins. Each `category` slug is derived from the storefront
path itself (`/cat/mens-shirts` -> `cat-mens-shirts`), so slugs are unique by
construction and survive label changes. The header emits an empty `categoryId` for
filtered `/rc/` and `/brand/` links; those are kept rather than dropped, and every
item carries its `department` / `section` from the header.

```bash
HTTPCACHE_ENABLED=False common-scrapy crawl backcountry_listing -a category=cat-mens-shirts -a max_pages=2 -O backcountry.jsonl -s HTTPCACHE_ENABLED=False
```

```json
{"category":"cat-mens-shirts","department":"Men","section":"Clothing","item_id":"FJRZ133","title":"Fjallglim Regular Shirt - Men's","brand":"Fjallraven","product_type":"Product","url":"https://www.backcountry.com/fjallraven-fjallglim-regular-shirt-mens","image":"https://content.backcountry.com/images/items/160/FJR/FJRZ133/DANACHWH.jpg","image_alt":"Fjallglim Regular Shirt - Men's","color":"Dark Navy/Chalk White","colors":["Dark Navy/Chalk White","Dark Navy/Maroon","Wood Brown/Black Oak"],"color_option_count":3,"price":124.95,"original_price":null,"discount_percentage":null,"currency":"USD","in_stock":true,"stock_status":"IN_STOCK","availability":"in stock","rating":null,"reviews_count":0,"is_new_arrival":false,"is_exclusive":false,"is_past_season":true,"is_gearhead_pick":false,"past_season_colors":["DANACHWH","DARNAVMAR","WOBRBLOA"],"category_id":"bc-mens-shirts","page":1,"position":1,"total_count":1490,"last_page":36,"source":"backcountry_next_data","raw":{"node":{...},"apollo":{...},"container":"category","variations_on_sale":0,"total_variations":11}}
```
### hm_listing

`hm_listing` reads H&M US products exclusively from the server-rendered Next.js
`#__NEXT_DATA__` PLP state. It does not parse HTML product cards or JSON-LD.
Hydrated `pagination` metadata drives `?page=N` requests, while an article-code
deduplication guard stops repeated pages. The curated taxonomy contains stable,
product-bearing new-arrival leaves for Women, Men, Kids, Home, and Beauty; H&M's
hydrated `siteStructure` is the source to use when refreshing that inventory.

The ordered `FEED_EXPORT_FIELDS` contract covers IDs, department/category,
canonical product and image URLs, current and regular prices, color, size/stock,
availability, page/source metadata, and the authoritative raw product record.
The storefront may require the configured ScrapeOps US proxy when Akamai blocks a
direct request.

```bash
scrapy crawl hm_listing -a category=women-new-arrivals -a max_pages=2 -s HTTPCACHE_ENABLED=False -O hm.jsonl
```

### getyourguide_listing

`getyourguide_listing` exports the fixed activity shelf on GetYourGuide country
landing pages. Choose one of 20 verified destination slugs, for example:

```bash
scrapy crawl getyourguide_listing -a category=argentina -s HTTPCACHE_ENABLED=False -O getyourguide.jsonl
```

The spider uses one product-data direction: the server-rendered
`window.__INITIAL_STATE__.sdui` bootstrap state. It recursively selects objects
with the stable activity contract and deduplicates tracking copies by numeric
activity ID. It does not parse presentation cards or JSON-LD and fails visibly
when the hydration contract is missing, malformed, or empty.

These destination pages expose a bounded recommendation shelf (24 activities
for Argentina in the verified live response), not an exhaustive paginated
catalogue. Consequently `max_pages` does not invent pagination. The ordered
`FEED_EXPORT_FIELDS` contract includes activity/tour IDs, title and description,
canonical URL, images, activity type, numeric prices and currency, full-precision
rating and review count, attributes, availability, page metadata, source, and
the crawl timestamp, and the raw authoritative record.

### viator_listing

`viator_listing` exports Viator's fixed top-activities shelf for 20 Popular Cities.
Choose a verified destination slug such as `nashville`:

```bash
scrapy crawl viator_listing -a category=nashville -s HTTPCACHE_ENABLED=False -O viator.jsonl
```

The spider uses one product-data direction: the server-rendered
`script[type="mime/invalid"]` JSON payload at
`__PRELOADED_DATA__.pageModel.topActivities`. It does not parse HTML cards,
JSON-LD, or replay GraphQL as a fallback. Missing, malformed, or empty hydration
raises an explicit error instead of reporting a successful zero-item crawl.

The destination contract is a bounded recommendation shelf (15 Nashville
activities in the verified live response), not an exhaustive paginated result
set, so `max_pages` does not invent pagination. The ordered `FEED_EXPORT_FIELDS`
contract includes destination context, activity ID, title and description,
canonical URL and images, category and location, exact hydrated prices and
discount state, rating and review count, language and duration metadata, flags,
badges, coordinates, provenance, timestamp, and the raw authoritative record.

### realtor_listing

`realtor_listing` uses one data direction: the server-rendered React Router stream
in `window.__reactRouterContext.streamController.enqueue(...)`. It JSON-decodes the
JavaScript strings, applies the `P<n>:` streamed patches to the indexed data table,
and resolves `loaderData.srp.search.properties`. The tiny `__NEXT_DATA__` geo object,
HTML property cards, and JSON-LD are not used as fallbacks; missing or malformed SRP
state raises an explicit error.

The bounded taxonomy contains 20 major US cities. Pagination uses canonical
`/pg-N` routes, stops at `max_pages` or an empty authoritative result set, and
deduplicates `property_id` across pages. Items retain listing/property IDs, status,
address, price/range, beds, baths, floor and lot area, property type, coordinates,
primary photo, broker/builder, flags, page position, and the raw structured record.
The ordered export contract also includes the crawl `timestamp` and `raw` payload.

Realtor.com's legal notice says automated scraping requires authorization. Confirm
permission and applicable terms before production use. The real SSR response also
requires the ScrapeOps residential route with bypass 5; the spider adds
`residential=true` and `bypass=5` idempotently while preserving existing proxy
options.

```bash
scrapy crawl realtor_listing -a category=los-angeles-ca -a max_pages=2 -s HTTPCACHE_ENABLED=False -O realtor.jsonl
```

### apartments_listing

`apartments_listing` reads one product-data source only: Apartments.com's
server-rendered `window.aptsState` bootstrap. Its `as.p` collection is the map
inventory for the selected market and is substantially larger than the 40
rendered placards (567 unique records in the captured New York page-one state).
The spider never parses product cards or JSON-LD and has no fallback direction.

The 20 deterministic city seeds come from Apartments.com's city-search sitemap.
Every item includes the stable listing key, coordinates, rent range, opaque
listing-type and feature codes, related listing IDs, market/geography metadata,
hydrated inventory totals, pagination state, the raw bootstrap record, and the
crawl timestamp. `window.aptsState.as.pg.nextUrl` drives path pagination up to
`max_pages`, while listing keys are deduplicated across pages. A configured
ScrapeOps US proxy is required; proxy-account and bot-wall payloads fail loudly.

```bash
scrapy crawl apartments_listing -a category=new-york-ny -a max_pages=1 -s HTTPCACHE_ENABLED=False -O apartments.jsonl
```

### zillow_listing

`zillow_listing` exports homes from one source only: Zillow's server-rendered
Next.js `__NEXT_DATA__` bootstrap state. It supports 20 major US sale markets and
uses Zillow's server-rendered `/<N>_p/` pages for pagination; there is no HTML-card,
JSON-LD, GraphQL, or browser fallback. Stable IDs come from `zpid`, and the ordered
`FEED_EXPORT_FIELDS` include price, address, property facts, coordinates, estimates,
broker, region, pagination metadata, and the authoritative raw record.
Every exported item also includes the crawl `timestamp`.

```bash
scrapy crawl zillow_listing -a category=houston-tx -a max_pages=2 -s HTTPCACHE_ENABLED=False -O zillow.jsonl
```

### agoda_listing

`agoda_listing` uses one product-data direction: Agoda's first-party Cronos geo
JSON API. The destination page is requested only to decode its escaped
`geoPageParams` configuration and discover the destination-specific `pageTypeId`,
`objectId`, and `accommodationTypeId`; product HTML and JSON-LD are never parsed.
The API returns a curated recommendation carousel, not exhaustive
city search results, and the spider fails visibly on malformed hydration,
challenges, proxy errors, or empty API output.

The ordered taxonomy contains 20 homepage destinations, from Bali through Johor
Bahru. The ordered `FEED_EXPORT_FIELDS` contract includes the stable hotel ID,
names, normalized hotel and image URLs, ratings and review details, any available
price fields, discovered geo identifiers, source metadata, and the raw API card.
Every exported item also includes the crawl `timestamp`.
A working configured proxy is required for the destination and API requests.

```bash
scrapy crawl agoda_listing -a category=bali -s HTTPCACHE_ENABLED=False -O agoda.jsonl
```

### autozone_listing

`autozone_listing` exposes 20 stable AutoZone category seeds and accepts
`-a category=<name>`. It reads products exclusively from the server-rendered
Next.js/TanStack React Query bootstrap state: `productshelf-results` supplies
the shelf records and `productSkuDetails` supplies authoritative price and
stock data. Those records are joined by SKU; missing queries, details, and
prices fail loudly. Pagination requests the next PLP page and stops at the
hydrated total or `max_pages`.

All AutoZone requests require the configured ScrapeOps proxy. The spider adds
`residential=true.country=us` to that proxy username without embedding
credentials. Its ordered `FEED_EXPORT_FIELDS` include category, identifiers,
product facts, canonical URL, image, price/availability, sponsorship, page and
position metadata, source, the joined raw hydration records, and the crawl
timestamp.
An uncached live check on 2026-10-06 exported 24/24 unique oil-filter SKUs;
sample: `1117175`, “STP Oil Filter S45023”, `$5.99`, in stock.

```bash
scrapy crawl autozone_listing -a category=oil-filter -a max_pages=1 -s HTTPCACHE_ENABLED=False
```

### rent_listing

`rent_listing` extracts the complete property list from Rent.com's server-rendered
Next.js `props.pageProps.pageData.location.listingSearch` hydration state. It follows
canonical `/page-N` pages and has no rendered-HTML or JSON-LD fallback.

```bash
scrapy crawl rent_listing -a category=los-angeles-ca -a max_pages=1 -s HTTPCACHE_ENABLED=False -O rent.jsonl
```

The spider exposes 20 major US rental markets from `rent_categories.py`. Its ordered
`FEED_EXPORT_FIELDS` cover property identity, location, price and bed ranges,
floor-plan bath and square-footage ranges, availability, ratings, amenities, photo
IDs, contact details, pagination metadata, and the authoritative raw record.

### hotpads_listing

`hotpads_listing` extracts rental buildings exclusively from HotPads' server-rendered
Next.js App Router RSC `initialListingsData` bootstrap. It does not use rendered
cards or JSON-LD as product-data fallbacks. Run one of 20 major US city categories,
a custom `category_url`, or omit all targets to crawl every configured city.

```bash
scrapy crawl hotpads_listing -a category=new-york-ny -a max_pages=1 -s HTTPCACHE_ENABLED=False -O hotpads.jsonl
```

Pagination follows the server-rendered `/page/N` path and hydrated `totalPages`.
The ordered `FEED_EXPORT_FIELDS` contract covers stable lot/marker identity,
location, bed/bath/square-foot ranges, pricing, availability, photos, contact and
tag metadata, coordinates, city/page totals, the authoritative raw record, and
`source=hotpads_rsc_bootstrap`.

### tripadvisor_listing

`tripadvisor_listing` reads Tripadvisor's server-rendered `$WP` bootstrap data URI and
decodes the `urqlSsrData.results` GraphQL cache. Hotel products come exclusively from
the cached `list.results` payload; rendered cards and JSON-LD are deliberately not used.
The spider maps stable location IDs, canonical URLs, ratings, live lowest prices,
addresses, coordinates, contact details, photos, amenities, and merchandising labels.
Pagination uses Tripadvisor's 30-result `-oa<N>-` path contract.

```bash
scrapy crawl tripadvisor_listing -a category=bali -a max_pages=1 -s HTTPCACHE_ENABLED=False -O tripadvisor.jsonl
```

Twenty destination shortcuts are defined in `tripadvisor_categories.py`. The site
requires the configured ScrapeOps residential route for reliable live responses.

### homes_listing

`homes_listing` uses one product-data direction: the server-embedded
`window.gState` search bootstrap. Homes.com encodes that JSON with a printable
ASCII Caesar shift; the spider decodes its `as.p` map inventory and emits stable
property/listing keys, normalized prices, coordinates, grouped-listing metadata,
and search totals. A live New York response exposed 638 unique property markers,
versus the 40 placards rendered in the page HTML. The spider deliberately does
not parse those placards or JSON-LD as a fallback.

The ordered 17-field `FEED_EXPORT_FIELDS` contract includes `source`, the raw
marker record, and a per-run timestamp. Choose one of 20 major-city seeds:

```bash
scrapy crawl homes_listing -a category=new-york-ny -s HTTPCACHE_ENABLED=False -O homes.jsonl
```

### remax_listing

`remax_listing` uses one listing-data direction: the authoritative
`listingResultsUnfiltered` object embedded in RE/MAX's server-rendered Next.js App
Router RSC (`self.__next_f`) stream. It does not parse rendered listing cards or
JSON-LD. The hydrated records include stable property, listing, and MLS identifiers;
address and property facts; price; photos; agent and office contacts; badges; and
open-house data. The ordered `FEED_EXPORT_FIELDS` contract also includes page and
position metadata, the raw structured record, and a crawl timestamp.

The spider provides 20 populous US state categories. Pagination updates the site's
JSON-encoded `searchQuery` parameter with `pageNumber`, stops at `max_pages`, and
deduplicates the hydrated `uniqueListingId` values across pages. RE/MAX requires the
configured ScrapeOps US proxy; direct requests can return an empty challenge response.

```bash
scrapy crawl remax_listing -a category=california -a max_pages=2 -s HTTPCACHE_ENABLED=False -O remax.jsonl
```
### worldmarket_listing

`worldmarket_listing` uses one product-data direction: World Market's first-party
Salesforce Commerce Cloud `Search-UpdateGrid` endpoint. The category landing page
is used only to resolve its `cgid`; products are requested from the endpoint from
offset zero onward, without product-card or JSON-LD fallbacks. Pagination follows
the API-provided result count in 60-item offsets and deduplicates stable product or
collection IDs.

The ordered `FEED_EXPORT_FIELDS` contract includes category context, product and
SKU identifiers, title, canonical URL, image, current/original USD prices,
availability, ratings, sale flags, position, total count, source URL, the raw
SFCC data attributes, and a per-run export `timestamp`. Thirteen stable department seeds are defined in
`worldmarket_categories.py`; custom category URLs remain supported.

```bash
scrapy crawl worldmarket_listing -a category=furniture-shop-all-furniture -a max_pages=2 -s HTTPCACHE_ENABLED=False -O worldmarket.jsonl
### movoto_listing

Movoto sale listings use one data path: the server-rendered Nuxt JSON in
`script#__INITIAL_STATE__`, specifically `pageData.listings`. Each item includes the
stable `propertyId`, price, property facts, MLS and broker metadata, location, and image.
There is deliberately no direct card-HTML or JSON-LD extraction fallback.

The spider provides 20 deterministic major-city categories sourced from Movoto's
`/sitemap/` city inventory. Pagination uses `/<city>/p-<N>/` (not the search route
`/<city>/<N>/`) and is bounded by `pageData.totalCount`, `max_pages`, short/empty pages,
and repeated IDs. Movoto is PerimeterX-protected, so use the configured ScrapeOps US
proxy.

The ordered `FEED_EXPORT_FIELDS` contract covers stable property identity, price and
property facts, MLS and broker metadata, location, media, pagination and search-context
metadata, the provenance `source=movoto_initial_state`, the authoritative raw listing
record (`raw`), and a per-item `timestamp`.

```bash
scrapy crawl movoto_listing -a category=new-york-ny -a max_pages=1 -O movoto.jsonl -s HTTPCACHE_ENABLED=False
```

### harborfreight_listing

`harborfreight_listing` reads products exclusively from the server-rendered
`window.__APOLLO_STATE__` bootstrap. It resolves each `ROOT_QUERY.products(...)`
reference to its normalized `SimpleProduct:<id>` entity; it does not parse HTML
cards or JSON-LD. The 17 deterministic department aliases point to stable,
product-bearing subcategories from Harbor Freight's public department navigation.

Pagination uses Magento's `?p=N` URL and the hydrated `page_info.total_pages`.
Items are deduplicated by SKU, and missing hydration, HTTP failures, and bot/proxy
challenges fail visibly. The ordered `FEED_EXPORT_FIELDS` contract includes
department context, IDs, title, brand, canonical URL, image, final/regular prices,
page totals, the authoritative raw entity, and `source=harborfreight_apollo_bootstrap`.

```bash
scrapy crawl harborfreight_listing -a category=Automotive -a max_pages=2 -s HTTPCACHE_ENABLED=False -O harborfreight.jsonl
```

### lowes_listing

`lowes_listing` reads products exclusively from Lowe's server-rendered
`window['__PRELOADED_STATE__']` bootstrap payload. It does not fall back to HTML
cards or JSON-LD. Stable category shortcuts, `category_url`, and `url` are
supported; `?page=N` pagination is bounded by `max_pages`. Lowe's requires the
configured ScrapeOps proxy and challenge responses fail loudly.

```bash
scrapy crawl lowes_listing -a category=beverage-wine-chillers -a max_pages=1 -s HTTPCACHE_ENABLED=False -O lowes.jsonl
```

### zumper_listing

`zumper_listing` extracts rentals exclusively from the server-rendered
`window.__PRELOADED_STATE__` bootstrap at `currentSearch.listables`; it has no
HTML-card or JSON-LD fallback. Twenty major US rental-market categories are
provided, and `?page=N` pagination follows hydrated `hasMoreListables` while
respecting `max_pages`. The ordered `FEED_EXPORT_FIELDS` contract covers stable
listing/building IDs, location, price and property ranges, amenities, photos,
contact details, market totals, pagination context, provenance, and raw records.

```bash
scrapy crawl zumper_listing -a category=new-york-ny -a max_pages=1 -s HTTPCACHE_ENABLED=False -O zumper.jsonl
```

### loopnet_listing

`loopnet_listing` uses one product-data direction: LoopNet's first-party
`POST /services/search` JSON service. The initial category response is used only
to hydrate the service's exact `viewdata.criteria` request contract. Items are
read from the service's structured listing arrays or its `Placards.HTML` response
field, with coordinates joined from the accompanying event model. There is no
listing-page or JSON-LD fallback.

Twenty deterministic sale and lease category searches mirror LoopNet's primary
property-type navigation. API pagination updates `criteria.PageNumber`, respects
`max_pages`, and deduplicates stable listing IDs. The ordered
`FEED_EXPORT_FIELDS` contract covers property identity, title and URL, address,
type, transaction, price, size, coordinates, image, paging context, raw API data,
provenance, and a crawl timestamp.

```bash
scrapy crawl loopnet_listing -a category=commercial-real-estate-for-sale -a max_pages=1 -s HTTPCACHE_ENABLED=False -O loopnet.jsonl
```

### B&H Photo Video listing spider

`bhphotovideo_listing` reads products from B&H's server-rendered
`bh-preloaded-data` / `ListingStore` bootstrap state. It deliberately has no
HTML-card or JSON-LD fallback. Choose a leaf with `-a category='Mirrorless Lenses'`
and bound path-based pagination with `-a max_pages=2`; `url` and `category_url`
retain the standard listing-spider precedence. Its ordered `FEED_EXPORT_FIELDS`
cover category context, product and manufacturer identifiers, pricing, rating,
availability, paging metadata, provenance, the raw bootstrap record, and the
crawl `timestamp`.
### rei_listing

`rei_listing` reads products exclusively from REI's server-rendered
`#initial-props` JSON bootstrap at
`ProductSearch.products.searchResults.results`. It follows the bootstrap's
`pagination.nextPage.queryString`, deduplicates by `prodId`, and fails visibly
when REI returns a challenge, malformed state, or an empty product page. It does
not parse rendered product cards or JSON-LD.

The spider exposes 20 stable commerce-category shortcuts. Its ordered
`FEED_EXPORT_FIELDS` contract includes product/style identity, brand and title,
canonical URL and image, current/range/original prices, sale and availability
flags, ratings, pagination metadata, the authoritative raw record, the crawl
`timestamp`, and `source=rei_initial_props_bootstrap`.

```bash
scrapy crawl rei_listing -a category=hiking-footwear -a max_pages=1 -s HTTPCACHE_ENABLED=False -O rei.jsonl
### walgreens_listing

`walgreens_listing` reads products exclusively from Walgreens' rendered Redux
bootstrap (`window.getInitialState()` → `searchResult.productList[*].productInfo`).
It does not parse product cards or JSON-LD. The ScrapeOps request enables US JS
rendering so the hydrated state is present, while pagination follows Walgreens'
`/productlist/N={id}/{page}/ShopAll={id}` route and stops on hydrated totals,
empty output, repeated product IDs, or `max_pages`.

The ordered `FEED_EXPORT_FIELDS` contract covers category context, Walgreens
product/SKU/article/UPC identifiers, title and brand, normalized URLs, prices,
ratings, inventory, pagination metadata, the authoritative raw bootstrap record,
and a crawl `timestamp`.

```bash
scrapy crawl walgreens_listing -a category='Allergy & Sinus' -a max_pages=1 -s HTTPCACHE_ENABLED=False -O walgreens.jsonl
### chewy_listing

`chewy_listing` reads one authoritative source: the product array in Chewy's
server-rendered Next.js `__NEXT_DATA__` bootstrap state. It does not parse HTML
product cards or JSON-LD. Its complete verified navigation taxonomy covers dogs,
cats, and other pets; custom listing URLs are also supported. Pagination uses
`?page=N` and stops at `recordSetTotal`, `max_pages`, an empty product page, or a
page with no new product IDs.

The ordered `FEED_EXPORT_FIELDS` include product identity, brand, canonical URL
(including sponsored-link redirect normalization), image, displayed/current/list
and Autoship prices, ratings, ad state, pagination metadata, provenance, raw
hydration record, and timestamp. Missing or malformed hydration and non-200
responses fail visibly. A working configured ScrapeOps proxy is expected.

```bash
scrapy crawl chewy_listing -a category=food-332 -a max_pages=1 -s HTTPCACHE_ENABLED=False -O chewy.jsonl
```

### crateandbarrel_listing

`crateandbarrel_listing` extracts the first-party `ProductListing` React bootstrap
state used to hydrate Crate & Barrel product-listing pages. It does not scrape
product cards or use JSON-LD. The category inventory contains 13 stable,
product-bearing URLs discovered from the site index; pagination changes the
terminal `/1` segment to `/2`, `/3`, and so on. Crate & Barrel's Akamai route
requires the configured ScrapeOps residential proxy.

```bash
scrapy crawl crateandbarrel_listing -a category=sofas -a max_pages=1 \
  -O crateandbarrel-sofas.jsonl -s HTTPCACHE_ENABLED=False
```

The ordered `FEED_EXPORT_FIELDS` cover category context, identifiers, title,
canonical URL, image, normalized prices, currency, ratings, product flags,
colors, page/position metadata, provenance, the raw first-party product object,
and the crawl timestamp.
### hilton_listing

`hilton_listing` extracts hotel records exclusively from the destination page's
server-rendered Next.js bootstrap at
`props.pageProps.pageData.hotelSummaryOptions.hotels`. Its ordered
`FEED_EXPORT_FIELDS` contract includes the stable Hilton property code, location,
coordinates, lead rate, amenities, availability, contact and image fields.

The taxonomy contains 20 major US city destinations. Run one with
`scrapy crawl hilton_listing -a category=new-york-ny`. Hilton caps destination
landing pages at 20 hotels; the session-backed `/search/` inventory is out of
scope. Requests use the configured US proxy, and missing/challenge bootstrap
responses fail visibly. There is no direct-HTML or JSON-LD extraction path.

### vinted_listing

`vinted_listing` reads one authoritative product source: the structured catalog
state streamed in Vinted's server-rendered Next.js React Server Component
(`self.__next_f`) payload. It does not parse the rendered grid cards or JSON-LD.
Each hydrated page supplies 96 records and pagination metadata; the spider
follows `?page=N`, deduplicates stable item IDs, and stops at the hydrated
`total_pages` or `-a max_pages` bound.

The 32-field `FEED_EXPORT_FIELDS` contract covers category context, item and
seller identifiers, title, brand, condition, size, canonical URL, images,
price/fee/total amounts, favorites and promotion state, search provenance,
pagination, the raw hydration record, and timestamp. The category inventory is
the 20 highest-coverage nodes captured from Vinted's hydrated `catalogTree`.
Requests use the project's configured proxy middleware and a realistic browser
user agent.

```bash
scrapy crawl vinted_listing -a category=home -a max_pages=1 \
  -s HTTPCACHE_ENABLED=False -O vinted-home.jsonl
### ssense_listing

`ssense_listing` extracts products exclusively from SSENSE's server-rendered
Next.js React Server Component (`self.__next_f`) bootstrap. It reads the
authoritative product-list analytics state and associated card component state;
it does not parse rendered product HTML or JSON-LD and has no fallback data
direction. Twenty stable men/women category shortcuts are included, and
`?page=N` pagination follows hydrated `paginationInfo.totalPages` while respecting
`max_pages` and deduplicating product IDs.

The ordered 22-field `FEED_EXPORT_FIELDS` contract includes category context,
product/SKU and brand identifiers, canonical URL and image, current/original
prices, availability, pagination metadata, raw bootstrap data, and timestamp.

```bash
scrapy crawl ssense_listing -a category=men-clothing -a max_pages=1 -s HTTPCACHE_ENABLED=False -O ssense.jsonl
```

### patagonia_listing

`patagonia_listing` extracts products through one authoritative data direction:
Patagonia's first-party Salesforce Commerce Cloud `AsyncComponents-ProductList`
API. It exposes 20 stable shopping categories, supports custom listing URLs, and
uses the API's offset parameters for bounded pagination. It does not parse the
listing page's direct HTML or JSON-LD as a product-data fallback.

```bash
scrapy crawl patagonia_listing -a category=new-arrivals -a max_pages=1 -s HTTPCACHE_ENABLED=False -O patagonia.jsonl
```

### etsy_listing

`etsy_listing` reads the 20 stable category seeds that mirror the marketplace's
primary departments from the server-rendered category document. Each page
embeds an `application/ld+json` `ItemList` with the organic products (name,
image, canonical listing URL, brand, offers), and the accompanying
`[data-listing-id]` listing-card markup supplies shop IDs, ratings, review
counts, ad and free-shipping flags. Pagination follows the server-rendered
`?ref=pagination&page=N` links.

Etsy's asynchronous Neu Spec search API is not an extractable alternative:
the anonymous `/bespoke/public/` endpoint answers every request shape
(SSR-exact args, page 2, `initial`, `search_results` route, `log_performance_metrics`)
with an empty `output` list, and the client's real results path is an
authenticated `/bespoke/member/` POST gated by a CSRF nonce and login session
(verified live against Etsy's own `chunk-b-etsylibs` client contract).

The ordered `FEED_EXPORT_FIELDS` contract covers listing and shop IDs, title,
shop, canonical URL, image, current/original prices, currency, rating/reviews,
ad and shipping flags, category/page/position, source, and the raw identity
record. Requests go through the configured ScrapeOps US proxy.

```bash
scrapy crawl etsy_listing -a category=jewelry -a max_pages=1 -s HTTPCACHE_ENABLED=False -O etsy.jsonl
```

### mediamarkt_listing

`mediamarkt_listing` extracts products exclusively from MediaMarkt Germany's
server-rendered `window.__PRELOADED_STATE__` bootstrap. The Apollo cache's
`ProductListPage` supplies the ordered 12-product grid, while its normalized
product, price, media, availability, badge, and feature entities provide the
listing fields. It does not parse rendered product cards or JSON-LD, and it
follows the bootstrap's bounded `?page=N` pagination.

The spider exposes 20 electronics and appliance categories. Its ordered
`FEED_EXPORT_FIELDS` contract includes product/EAN identity, URLs, imagery,
current and strike-through prices, discount, ratings, availability,
marketplace seller data, taxonomy, highlighted features, pagination totals,
provenance, and the contributing hydrated entities.

```bash
scrapy crawl mediamarkt_listing -a category='Computer & Büro' -a max_pages=1 -s HTTPCACHE_ENABLED=False -O mediamarkt.jsonl
```
