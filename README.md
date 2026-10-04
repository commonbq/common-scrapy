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

All extra args are forwarded to `scrapy crawl` unchanged (feeds, settings overrides, etc.).

## Available spiders

### Standalone spiders (via `scrapy crawl <spider>`)

These live under `common/spiders/*_listing_spider.py` and are purpose-built per retailer.

Working spiders running daily in production:

| Spider Name | Status | Method | Antibot | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|---|
| [`adorama_listing`](#adorama_listing) | Active | bootstrap (Next.js `__NEXT_DATA__`) | DataDome | Adorama category listings from server-rendered Next.js hydration state. | 24 (one page; 48 across 2 pages) | 1,079 crawlable categories across 11 departments from `adorama_categories.py` | `{"category":"cameras","item_id":"KKRK0603A","title":"Kodak Charmera Millenium Edition...","price":54.94,"currency":"USD"...}` |
| [`amazon_listing`](#amazon_listing-category) | Active | html | none detected | Amazon category listing spider (category shortcuts). | 22 (ok) | electronics, fashion, beauty, home-kitchen, toys-games, sports-outdoors, grocery, books | `{"asin":"B0DKDTBBF7","title":"2 Packs Electric Candle Lighters, Windproof Flameless USB Rechargeable Plasma Arc Long Lighter for Grill Fi...` |
| [`amazon_search`](#amazon_search) | Active | html | none detected | Amazon keyword search spider. | 22 (ok) | - | `{"asin":"B0GHQRV71M","title":"16\" FHD IPS Laptop Computer - 16GB RAM 512GB SSD, Pentium N100(Beat to i3-1115G4, 4 Cores Up to 3.4GHz), B...` |
| [`bestbuy_listing`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | unknown (timeout/no verdict) | Best Buy listing via direct HTTP + Apollo bootstrap extraction. | 10 (skipped2) | laptops, tvs, headphones, monitors, cell-phones | `{"item_id":"6572184","title":"Samsung - Galaxy Book4 15.6\" FHD Laptop - Intel Core 7- 16GB Memory - 512GB SSD - Silver","url":"https://www.bestbuy.com/product/samsung-galaxy-bo...` |
| [`bestbuy_search`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | unknown (timeout/no verdict) | Best Buy search via direct HTTP + Apollo bootstrap extraction. | 4 (skipped2) | - | `{"item_id":"6613879","title":"HP - 14\" Laptop - Intel Processor N150 2025 - 4GB Memory - 128GB UFS - Willow Green","url":"https://www.bestbuy.com/product/hp-14-laptop-intel-pro...` |
| [`macys_listing`](#macys_listing) | Active | api | Akamai | Macy’s listing via xapi endpoint (with fallback routing). | 60 (ok) | laptops, shoes, dresses, fragrance, bedding | `{"item_id":"17595303","title":"5Core AC Power Cord 6Ft 3 Prong US Male to Female Extension Adapter 18AWG 10A 7A 125V","brand":"5 Core","u...` |
| [`nordstrom_listing`](#nordstrom_listing) | Active | bootstrap + html | PerimeterX / HUMAN | Nordstrom listing parser; often blocked/changed. | 0 (timeout2) | women, men, kids, beauty, home, designer, sale | `{}` |
| [`sephora_listing`](#sephora_listing) | Active | api | Akamai | Sephora listing via `/api/v2/catalog/categories/<slug>/seo`. | 60 (ok) | makeup, skincare, gifts, fragrance | `{"item_id":"P517483","title":"Pocket Blush Buildable Hydrating Cream Blush","url":"https://www.sephora.com/product/pocket-blush-P517483?s...` |
| [`ulta_listing`](#ulta_listing-category) | Active | api | Akamai | Ulta category listing with dynamic GraphQL module discovery. | 152 (2 pages, proxy) | makeup, skin-care, hair-care, fragrance, body-care | `n/a` |
| [`ulta_search`](#ulta_search-keyword) | Active | api + html | Akamai | Ulta keyword search via GraphQL (with unsorted retry + HTML fallback). | 64 (ok) | - | `{"item_id":"xlsImpprod15511061","title":"All Soft Shampoo","source":"ulta_dxl_graphql"...}` |
| [`walmart_listing`](#walmart_listing-category) | Active | api + html | Akamai (+ PerimeterX/HUMAN signals) | Walmart category listing spider (direct API+HTML flow). | 45 (ok) | electronics, home, clothing, beauty, toys, sports-and-outdoors, grocery | `{"productId":"19231301884","usItemId":"19231301884","title":"No Boundaries Women's Faux Leather Loafers","brand":"No Boundaries"...` |
| [`walmart_search`](#walmart_search-keyword) | Active | api + html | Akamai (+ PerimeterX/HUMAN signals) | Walmart keyword search spider. | 12 (ok) | - | `{"item_id":"13542163431","title":"ASUS Vivobook Go 15.6” Laptop, Intel i3-N305, 8GB, 256GB, Windows 11 Home in S mode, Cool Silver, E1504...` |
| [`ebay_listing`](#ebay_listing-category-marko-hydration-state) | Active | Marko + html | Akamai | Stable eBay category listing extraction from Marko hydration state, with HTML subcategory discovery. | 18 (Antiques fixture browse tiles) | 18 top-level groups / 209 subcategories from `ebay_categories.py` | `{"productId":"234346994063","title":"MacBook Pro 15 Inch 256GB SSD 16 GB i7 3.40Ghz Apple Retina Big Sur 3yr Warranty","price":439.0,"currency":"USD",...}` |
| [`ebay_search`](#ebay_search-keyword-marko-hydration-state) | Active | Marko | Akamai | Stable eBay keyword search extraction from Marko `ListingItemCard` hydration data. | 60 (ok) | - | `{"productId":"234346994063","title":"MacBook Pro 15 Inch 256GB SSD 16 GB i7 3.40Ghz Apple Retina Big Sur 3yr Warranty","price":439.0,"currency":"USD",...}` |

Spiders below are returning items in recent smoke runs:

| Spider Name | Status | Method | Antibot | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|---|
| [`adidas_listing`](#adidas_listing) | Experimental | Next.js hydration | Akamai (ScrapeOps 367 on plain route; `residential=true` worked) | adidas listings from server-rendered `__NEXT_DATA__` `props.pageProps.products`, paginated by `?start=`. | 96 (2 pages, proxy) | 25 sections / 196 categories from `adidas_categories.py` | `{"item_id":"KI8294","title":"ADIZERO ADIOS PRO 5 Running Shoes","brand":"Men Performance","price":275.0,"currency":"USD",...}` |
| [`ae_listing`](#ae_listing) | Experimental | FastBoot + API | Akamai (signals in headers) | American Eagle listing spider via FastBoot shoebox state and browse API pagination. | 30 (ok) | women, men, aerie | `{"item_id":"1457_2980_808","title":"AE Big Hug V-Neck Sweatshirt","url":"https://www.ae.com/us/en/p/women/hoodies-sweatshirts/crew-neck-sweatshirts/ae-big-hug-v-neck-sweatshirt/1457_2980_808","price":38.97...` |
| [`asos_listing`](#asos_listing) | Experimental | bootstrap + API | Akamai | ASOS US listings from `window.asos.plp._data`, with pagination through the hydrated search API contract. | 2 (fixture; live unverified) | complete women/men navigation inventory from `asos_categories.py` | `{"item_id":"211160390","title":"ASOS DESIGN stretch chiffon scarf detail plunge draped maxi dress in chocolate","price":69.99,"currency":"USD"...}` |
| [`bloomingdales_listing`](#bloomingdales_listing) | Experimental | html + nuxt-state | Akamai | Bloomingdale's listing spider via Nuxt SSR state contract parsing (splash->leaf aware). | 8 (ok) | new-now, women, beauty, shoes, handbags, jewelry-accessories, men, kids, home, sale, gifts, designers | `{"item_id":"5973765","title":"Tumbled Woven Verne Pants","url":"https://www.bloomingdales.com/shop/product/cinq-a-sept-tumbled-woven-vern...` |
| [`costco_listing`](#costco_search--costco_listing) | Active | React Flight + API | Akamai | Costco category listing with React Flight discovery and GRS search pagination. | 24 (ok) | 131 parent groups / 432 subcategory entries from `costco-categories.json` | `{"item_id":"100501081","title":"Starbucks Pike Place Medium Roast K-Cup","url":"https://www.costco.com/starbucks-pike-place-medium-roast-k-cup-72-count.product.100501081.html","price":...` |
| [`containerstore_listing`](#containerstore_listing) | Active | bootstrap | none detected | Container Store category listings from the server-rendered Next.js `__NEXT_DATA__` hydration. | 120 (2 pages, proxy) | 14 departments / 189 L2 / 159 L3 nodes -> 295 unique catalogue URLs from `containerstore_categories.py` | `{"category":"Kitchen > Pantry Organizers","department":"Kitchen","subcategory":"Pantry Organizers","item_id":"11017102","sku_id":"10087168","title":"Everything Organizer Shelf-Depth Pantry Bin with Divider","price":9.19,"original_price":22.99,...` |
| [`dickssportinggoods_listing`](#dickssportinggoods_listing) | Active | api | Akamai | DICK'S Sporting Goods category listings from the first-party catalog product-search API. | 48 (ok) | 1287 unique categories from 10 departments | `{"item_id":"13286436","title":"adidas FIFA World Cup Historical Mini Soccer Ball Set","brand":"adidas","price":141.52,"currency":"USD",...}` |
| [`elfcosmetics_listing`](#elfcosmetics_listing) | Experimental | api + bootstrap + html | none detected (CloudFront CDN only) | e.l.f. Cosmetics multi-mode listing spider. | 6 (ok) | face, eyes, lips | `{'item_id':'300261','title':'Soft Glam Satin Concealer','url':'https://www.elfcosmetics.com/soft-glam-satin-concealer/300262.html','price':9.0,'brand':'e.l.f. Cosmetics','source':'elfcosmetics_preloaded_state'...}` |
| [`fashionnova_listing`](#fashionnova_listing) | Active | api + html | Cloudflare | Fashion Nova listing via Shopify Storefront GraphQL with HTML fallback. | 48 (ok) | women, new, dresses, jeans, sale | `{"item_id":"175898317","title":"Classic High Waist Skinny Jeans - Dark Denim","url":"https://www.fashionnova.com/products/dark-blue-class...` |
| [`nike_listing`](#nike_listing) | Active | api | none detected (ScrapeOps proxy; keep_headers) | Nike product wall via `__NEXT_DATA__` hydration + `api.nike.com` product-wall API pagination (no HTML fallback). | 239 (page 1, proxy) | 168 unique URLs across 6 departments from `nike_categories.py` | `{"category":"mens-shoes-nik1zy7ok","item_id":"IX3952-600","title":"Nike Moon Shoe OG","price":105,"currency":"USD","source":"nike_next_data"...` |
| [`gamestop_listing`](#gamestop_listing) | Active | api | none detected (ScrapeOps proxy) | GameStop SFCC Demandware listing via the `Tile-GetProductsJSON` controller (no HTML fallback). | 139 (3 pages, proxy) | 119 URLs across 33 category groups from `gamestop_categories.py` | `{"category":"consoles-hardware","item_id":"106429","title":"Nintendo Wii Original Console with Wii Remote - Super Mario Bros. 25th Anniversary Edition Red","price":"139.99","availability":"InStock","source":"gamestop_tile_json"...` |
| [`footlocker_listing`](#footlocker_listing) | Active | api | residential proxy (ScrapeOps) | Foot Locker category listings from the ZGW search API (residential proxy required). | 48 (1 page, residential proxy) | Dynamically resolved from `header.public.json` | `{"band":"Men's","sub_category":"Shoes","category":"all-men-s-shoes","item_id":"T8013103","title":"Jordan Retro 12 - Men's","url":"https://www.footlocker.com/product/T8013103.html","image_url":"https://images.footlocker.com/is/image/EBFL2/T8013103","price":215.0,"original_price":215.0,"currency":"USD","availability":"InStock","brand":"Jordan","rating":5.0,"reviews_count":999,"page":1,"category_url":"/category/mens/shoes.html","source":"footlocker_api"...` |
| [`homedepot_listing`](#homedepot_listing-category-apollo-state) | Flaky | bootstrap | Akamai | Home Depot department listings from embedded Apollo state. | 2 (fixture) | appliances, bath, building-materials, decor-and-furniture, electrical, flooring, hardware, heating-and-cooling, kitchen, lawn-and-garden, lighting, paint, plumbing, storage, tools | `{"category":"tools","item_id":"100000001","sku":"1000000001","title":"16 oz. Fiberglass Claw Hammer","brand":"Husky","price":14.97...` |
| [`homedepot_search`](#homedepot_search-keyword-apollo-bootstrap) | Active | bootstrap + html | Akamai | Home Depot keyword search via Apollo state. | 24 (ok) | - | `{"item_id":"336787835","sku":"1014334650","brand":"Lukyamzn","title":"14 in. Dual-Core Celeron N4000 Laptop 6 GB RAM 128 GB SSD IPS Displ...` |
| [`jcpenney_listing`](#jcpenney_listing) | Active | api | Akamai (+ reCAPTCHA scripts observed) | JCPenney listing spider via search API bootstrap endpoint. | 48 (ok) | womens_tops, mens_shirts | `{"item_id":"ppr5008584232","title":"St. John's Bay Womens Boat Neck Elbow Sleeve T-Shirt","brand":"st. john's bay","url":"https://www.jcp...` |
| [`ikea_listing`](#ikea_listing) | Active | api + html | none detected | IKEA category listings from the SIK search API, with a server-rendered HTML fallback. | 46 (api, ok) / 24 (html, ok) | 221 unique targets from 23 departments | `{"category":"st004","item_id":"50561244","title":"STORKLINTA","product_type":"6-drawer dresser","price":279.99,"department":"Storage & organization",...}` |
| [`kroger_listing`](#kroger_search--kroger_listing) | Active | Redux bootstrap | unknown (timeout/no verdict) | Kroger category listings from `window.__INITIAL_STATE__` search products. | 2 (fixture) | cereal, milk, eggs, bread, coffee, snacks | `{"category":"cereal","item_id":"0001111012345","title":"Kroger Toasted Oats Cereal","brand":"Kroger","price":3.99,...}` |
| [`kroger_search`](#kroger_search--kroger_listing) | Active | bootstrap + html | unknown (timeout/no verdict) | Kroger keyword search with state extraction + fallback. | 27 (ok) | - | `{'item_id':'kroger-2-reduced-fat-milk-gallon','url':'https://www.kroger.com/p/kroger-2-reduced-fat-milk-gallon/0001111041700','source':'kroger_html_links_fallback'}` |
| [`levis_listing`](#levis_listing) | Active | bootstrap | none detected through proxy | Levi's listings from SSR `__LSCO_INITIAL_STATE__.ssrViewStoreProductList`. | 48 (2 pages, live proxy) | 5 sections / 83 PLP targets from `levi_categories.py` | `{"category":"shop-all-men-s-jeans","item_id":"005053473","title":"505™ Regular Dobby Men's Jeans","brand":"Levi's","price":64.99...` |
| [`lululemon_listing`](#lululemon_listing) | Active | bootstrap | Akamai | lululemon listing spider via Next.js `__NEXT_DATA__`. | 40 (ok) | women-shorts, women-leggings, men-shorts, bags | `{"category":"women-shorts","product_id":"prod11860112","name":"Shake It Out High-Rise Running Short 2.5\"","brand":"lululemon","price":["...` |
| [`llbean_listing`](#llbean_listing) | Active | api | none detected (ScrapeOps `country=us` route required) | L.L.Bean listing via the UDAL `product-discovery` JSON endpoint (no HTML fallback). | 96 (2 pages, proxy) | 11 departments / 500 targets from `llbean_categories.py` | `{"category":"Gift Shop","item_id":"1000316302","sku_id":"1000316302","title":"Women's The Original Double L® Sweater, Crewneck","brand":"L.L.Bean","price":49.99,"original_price":69.95,"currency":"USD","rating":4.4,"reviews_count":359,"color":"Classic Navy","size":"X-Small","availability":"IN","on_sale":true,"page":1,"position":1,"total_count":626,"source":"llbean_udal_product_discovery"...` |
| [`maccosmetics_listing`](#maccosmetics_listing) | Experimental | api + bootstrap + html | Akamai | MAC Cosmetics multi-mode listing spider. | 66 (ok) | face, lips, eyes | `{"item_id":"13854","title":"4.8/5 ( 452 ) Lustreglass Sheer-Shine Lipstick Sheer Coverage, Glossy/High-Shine Finish, Infused With Raspberry Seed/Organic Extra Virgin Olive Oils ...` |
| [`officedepot_listing`](#officedepot_listing) | Active | bootstrap | none detected (ScrapeOps proxy) | Office Depot / OfficeMax category listings from inline `window.ODSEARCHBROWSE_INITIAL_STATE` SSR hydration; taxonomy resolved from the header mega-menu JSON. | 59 (2 pages, furniture) | 388 browse PLPs from `header-menu-excel/products.json` | `{"department":"Furniture","item_id":"9003237","title":"Serta® Smart Layers™ Brinkley Ergonomic Bonded Leather High-Back Executive Office Chair, Black/Silver","price":299.99,"availability":"InStock","source":"officedepot_bootstrap"...}`
| [`poshmark_listing`](#poshmark_listing) | Experimental | bootstrap | none detected | Poshmark listing spider via `window.__INITIAL_STATE__` category grid data. | 48 (ok) | women, men, kids, home, electronics, pets | `{"category":"women","item_id":"6989d90ac4e7b4d4de556bac","title":"🔥Stunning  Farm Rio NWT Size Large Tropical Midi Dress with Sleeves – V...` |
| [`qvc_listing`](#qvc_listing) | Experimental | html + bootstrap | Akamai | QVC listing spider via server-rendered gallery cards and `utag_data` page state. | 96 (Beauty proxy capture) | fashion | `{"category":"beauty","category_id":"NAV6285","item_id":"A740517","title":"Whish 12 Days of Beauty Whishes Advent Calendar","price":59.98,...}` |
| [`zappos_listing`](#zappos_listing) | Experimental | Redux hydration | none detected through proxy | Zappos listings from `window.__INITIAL_STATE__.products.list`. | 100 (one-page proxy smoke) | 4 departments / 50 targets | `{"item_id":"8910671","title":"Kiruna Padded Parka","brand":"Fjällräven","price":300.0,...}` |
| [`saksfifthavenue_listing`](#saksfifthavenue_listing-category) | Experimental | html | DataDome | Saks Fifth Avenue listing spider via direct category HTML cards. | 24 (ok) | women, men, shoes, beauty, handbags | `{"item_id":"0400026449047","title":"Prada Washed Re Nylon Rain Jacket","url":"https://www.saksfifthavenue.com/product/prada-washed-re-nyl...` |
| [`sallybeauty_listing`](#sallybeauty_listing) | Experimental | html + AJAX | PerimeterX / HUMAN (px-captcha signals) | Sally Beauty SFCC product-grid spider with `Search-UpdateGrid` pagination. | 2 (fixture) | hair-color, hair-care, textured-curly-hair, hair-extensions, tools-brushes, nails, cosmetics-skin-care, fragrances, mens-grooming, salon-supplies, new, deals | `{"category":"hair-care","item_id":"SBS-539230","title":"Low Porosity Aloe Vera Gel Shampoo","brand":"Texture ID","price":11.99...` |
| [`stockx_listing`](#stockx_listing) | Experimental | bootstrap + html | Cloudflare | StockX listing via `__NEXT_DATA__` bootstrap. | 41 (ok) | sneakers, apparel, electronics, trading-cards, collectibles | `{"item_id":"brands","title":"Brands","url":"https://stockx.com/brands","price":null,"currency":null}` |
| [`staples_listing`](#staples_listing) | Experimental | Next.js hydration | Akamai | Staples category listings from server-rendered `__NEXT_DATA__`. | 40 (one page) | 34 roots / 208 subcategories from `staples_categories.py` | `{"item_id":"82656","title":"Staples 1\" 3-Ring View Binder...","price":10.09,"currency":"USD"...}` |
| [`target_listing`](#target_listing) | Active (alias) | api | PerimeterX / HUMAN (cookie signals) | Deprecated alias of `target_search`. | 24 (ok) | - | `{"product_id":"90600286","name":"Women&#39;s Waffle Short Robe - Auden&#8482; Light Gray M/L: Front Tie, Long Sleeve","price":"$35.00","u...` |
| [`uniqlo_listing`](#uniqlo_listing) | Experimental | api | none detected (plain ScrapeOps datacenter route) | UNIQLO US category listings from the first-party commerce BFF products API. | 36 (one page, ok) | 2741 taxonomy URLs (4 genders / 46 classes / 212 categories / 2479 subcategories) from `uniqlo-categories.json` | `{"item_id":"E424873-000-00","title":"Crew Neck T-Shirt","color":"White","price":19.9,"currency":"USD"...}` |
| [`target_search`](#target_search) | Active | api | PerimeterX / HUMAN (cookie signals) | Target RedSky search API spider. | 24 (ok) | - | `{"product_id":"90600286","name":"Women&#39;s Waffle Short Robe - Auden&#8482; Light Gray M/L: Front Tie, Long Sleeve","price":"$35.00","u...` |
| [`victoriassecret_listing`](#victoriassecret_listing) | Active | api | none detected (ScrapeOps proxy, plain datacenter route) | Victoria's Secret / PINK listings from the first-party `stacks` JSON API; page 0 reads `collectionId` from SSR `clientProps`. | 192 (2 pages, live) | 427 targets across `vs` + `pink` brands from `victoriassecret_categories.py` | `{"category":"vs-bras","brand":"vs","item_id":"11295563|7I65","name":"Signature Shine Cotton Lightly Lined Balconette Bra","price":49.95,...}` |
| [`williams_sonoma_listing`](#williams_sonoma_listing) | Active | api | Akamai (not an issue for API) | Williams-Sonoma category listings via the Constructor.io browse API (taxonomy from the runtime category-tree API). | 100 (1 page, proxy) | ~3500 group_ids from the runtime category-tree API | `{"category":"cookware-sets","item_id":"greenpan-reserve-pro-ceramic-nonstick-10-piece-cookware-set","title":"GreenPan™ Reserve Pro Ceramic Nonstick 10-Piece Cookware Set","price":399.95,"currency":"USD","image_url":"https://assets.wsimgs.com/wsimgs/rk/images/dp/wcm/202631/0164/img2c.jpg","flags":["freeShip","more_colors"],"source":"williams_sonoma_constructor_browse"...` |

#### In-progress spiders

These are still being worked on and currently returned `0` items in recent smoke runs:

| Spider Name | Status | Method | Antibot | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|---|
| [`anthropologie_listing`](#anthropologie_listing) | Experimental | api + html | PerimeterX / HUMAN | Anthropologie listing spider (API + HTML fallback). | 0 (ok) | women, dresses, sale | `n/a` |
| [`bathandbodyworks_listing`](#bathandbodyworks_listing) | Experimental | api + bootstrap + html | PerimeterX / HUMAN (px-captcha) | Bath & Body Works multi-mode listing spider. | 0 (ok) | body-care, home-fragrance, hand-soaps | `{}` |
| [`costco_search`](#costco_search--costco_listing) | Active | bootstrap + html | Akamai | Costco keyword search with state extraction + fallback. | 0 (skipped2) | - | `{}` |
| [`dillards_listing`](#dillards_listing) | Experimental | bootstrap | Akamai | Dillard's listing spider via `window.__INITIAL_STATE__`. | 0 (ok) | women, men, shoes, handbags, beauty, juniors, home | `n/a` |
| [`kohls_listing`](#kohls_listing) | Experimental | api | Akamai (Cloudflare challenge assets also observed) | Kohl’s listing via `/web/catalog/...` API. | 0 (ok) | women, men, sale | `n/a` |
| [`nordstromrack_listing`](#nordstromrack_listing) | Experimental | JSON-LD | Fastly (`x-jungle`) | Nordstrom Rack category listings from server-rendered Schema.org `ItemList` data. | 2 (fixture; live 403) | women, men, kids, shoes, bags-and-accessories, beauty, home, clearance | `{"item_id":"7788991","title":"Pleated Midi Dress","brand":"Donna Ricco","price":34.97,"currency":"USD",...}` |

*`Number of items output` reflects recent local smoke runs (typically `max_pages=1`) and can vary by location, anti-bot behavior, and site changes.*
Many listing spiders accept `-a category=<name>` shortcuts (in addition to `-a category_url=<url>`), including Amazon, Walmart, eBay, Home Depot, Best Buy, and Kroger. Costco listing uses category-only selection.

#### Sample output

Below are trimmed examples from recent local test runs (JSONL output, 1 item shown).

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
```json
{
  "item_id": "by-anthropologie-cotton-floral-cutwork-barn-jacket",
  "title": "By Anthropologie Cotton Floral Cutwork Barn Jacket",
  "url": "https://www.anthropologie.com/shop/by-anthropologie-cotton-floral-cutwork-barn-jacket?color=016&type=STANDARD",
  "price": 198.0,
  "currency": "USD",
  "brand": "Anthropologie",
  "source": "anthropologie_html",
  "category_url": "https://www.anthropologie.com/womens-clothing",
  "page": 1
}
```
Run example:
`common-scrapy crawl anthropologie_listing -a category=women -a max_pages=1 -O anthropologie_listing.jsonl`

Notes:
- Verified after connecting via NordVPN US endpoints (Seattle, Chicago, Miami) and again with NordVPN disabled.
- HTML parsing is enabled by default; API/bootstrap was not required once the spider ignored recaptcha config noise.

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
```json
{
  "item_id": "12345678",
  "title": "Body Lotion ...",
  "url": "https://www.bathandbodyworks.com/p/...",
  "price": 16.95,
  "currency": "USD",
  "brand": "Bath & Body Works",
  "source": "bathandbodyworks_internal_api|bathandbodyworks_html"
}
```
Run examples:
- `common-scrapy crawl bathandbodyworks_listing -a category='body-care' -a mode=api -a max_pages=1 -O bbw_api.jsonl`
- `common-scrapy crawl bathandbodyworks_listing -a category='body-care' -a mode=bootstrap -a max_pages=1 -O bbw_bootstrap.jsonl`
- `common-scrapy crawl bathandbodyworks_listing -a category='body-care' -a mode=html -a max_pages=1 -O bbw_html.jsonl`

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

### Project layout

- `common/spiders/` – retailer spiders (`*_listing_spider.py`, `*_search_spider.py`) and shared helpers.
- `common/settings/` – shared Scrapy configuration; reads environment variables via `.env`.
- `scrapy.cfg` – entry point for the `scrapy` CLI.

### Adding new retailer spiders

1. Investigate real browser traffic and identify internal API/bootstrap/HTML patterns.
2. Implement a purpose-built spider under `common/spiders/` with normalized output fields.
3. Add category shortcuts (`categories`) where applicable.
4. Validate with `max_pages=1` runs and update README examples/output snippets.
### Gap listing spider

`gap_listing` uses Gap's public commerce search API and exports a stable field
order through `FEED_EXPORT_FIELDS`. Choose `women`, `men`, or `girls`; each
selection expands to its maintained child listing URLs.

```bash
scrapy crawl gap_listing -a category=women -a max_pages=1 -O gap.jsonl
```

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
