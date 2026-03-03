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

| Spider Name | Status | Method | Description | Number of items output | Spider Categories | Sample output |
|---|---|---|---|---|---|---|
| [`ae_listing`](#ae_listing) | Experimental | html | American Eagle listing spider via category-page product cards. | 30 (ok) | women-tops, women-jeans, men-tops | `{"item_id":"1457_2980_808","title":null,"url":"https://www.ae.com/us/en/p/women/hoodies-sweatshirts/crew-neck-sweatshirts/ae-big-hug-v-neck-sweatshirt/1457_2980_808","price":nul...` |
| [`amazon_listing`](#amazon_listing-category) | Active | html | Amazon category listing spider (category shortcuts). | 22 (ok) | electronics, fashion, beauty, home-kitchen, toys-games, sports-outdoors, grocery, books | `{"asin":"B0DKDTBBF7","title":"2 Packs Electric Candle Lighters, Windproof Flameless USB Rechargeable Plasma Arc Long Lighter for Grill Fi...` |
| [`amazon_search`](#amazon_search) | Active | html | Amazon keyword search spider. | 22 (ok) | - | `{"asin":"B0GHQRV71M","title":"16\" FHD IPS Laptop Computer - 16GB RAM 512GB SSD, Pentium N100(Beat to i3-1115G4, 4 Cores Up to 3.4GHz), B...` |
| [`anthropologie_listing`](#anthropologie_listing) | Experimental | api + html | Anthropologie listing spider (API + HTML fallback). | 0 (ok) | women, dresses, sale | `n/a` |
| [`bathandbodyworks_listing`](#bathandbodyworks_listing) | Experimental | api + bootstrap + html | Bath & Body Works multi-mode listing spider. | 0 (ok) | body-care, home-fragrance, hand-soaps | `{}` |
| [`bestbuy_listing`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | Best Buy listing via Playwright + Apollo cache extract. | 10 (skipped2) | laptops, tvs, headphones, monitors, cell-phones | `{"item_id":"6572184","title":"Samsung - Galaxy Book4 15.6\" FHD Laptop - Intel Core 7- 16GB Memory - 512GB SSD - Silver","url":"https://www.bestbuy.com/product/samsung-galaxy-bo...` |
| [`bestbuy_search`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | Best Buy search via Playwright + Apollo cache extract. | 4 (skipped2) | - | `{"item_id":"6613879","title":"HP - 14\" Laptop - Intel Processor N150 2025 - 4GB Memory - 128GB UFS - Willow Green","url":"https://www.bestbuy.com/product/hp-14-laptop-intel-pro...` |
| [`bloomingdales_listing`](#bloomingdales_listing) | Experimental | html + nuxt-state | Bloomingdale's listing spider via direct HTML/state extraction (resilient parser). | 8 (ok) | women, men, shoes, beauty, home | `{"item_id":"5973765","title":"Tumbled Woven Verne Pants","url":"https://www.bloomingdales.com/shop/product/cinq-a-sept-tumbled-woven-vern...` |
| [`costco_listing`](#costco_search--costco_listing) | Active | bootstrap + html | Costco category listing with state extraction + fallback. | 24 (ok) | coffee, water, snacks, vitamins, laundry, paper-products | `{"item_id":"100501081","title":null,"url":"https://www.costco.com/starbucks-pike-place-medium-roast-k-cup-72-count.product.100501081.html","price":null,"currency":null,"brand":n...` |
| [`costco_search`](#costco_search--costco_listing) | Active | bootstrap + html | Costco keyword search with state extraction + fallback. | 0 (skipped2) | - | `{}` |
| [`dillards_listing`](#dillards_listing) | Experimental | bootstrap | Dillard's listing spider via `window.__INITIAL_STATE__`. | 0 (ok) | women, men, shoes, handbags, beauty, juniors, home | `n/a` |
| [`ebay_listing`](#ebay_listing-category-bootstrapmodel-state) | Flaky | bootstrap + html | eBay category listing via `__NEXT_DATA__` + fallback. | 4 (ok) | laptops, cell-phones, headphones, watches, video-games | `{"item_id":null,"title":"Apple MacBook Air 13.3'' (256GB SSD, Apple M1, 8GB RAM) Laptop - Space Gray - MGN63LL/A (2020)","url":"https://w...` |
| [`ebay_search`](#ebay_search-keyword-bootstrapmodel-state) | Flaky | bootstrap + html | eBay keyword search via `__NEXT_DATA__` + JSON-LD + HTML fallback (filters promo/non-item cards). | 60 (ok, VPN-dependent) | - | `{'item_id':'286393092388','title':'Dell Latitude Laptop Computer PC Intel i5 Up To 32GB RAM 1TB SSD Windows 11',...}` |
| [`elfcosmetics_listing`](#elfcosmetics_listing) | Experimental | api + bootstrap + html | e.l.f. Cosmetics multi-mode listing spider. | 6 (ok) | face, eyes, lips | `{'item_id':'300261','title':'Soft Glam Satin Concealer','url':'https://www.elfcosmetics.com/soft-glam-satin-concealer/300262.html','price':9.0,'brand':'e.l.f. Cosmetics','source':'elfcosmetics_preloaded_state'...}` |
| [`fashionnova_listing`](#fashionnova_listing) | Active | api + html | Fashion Nova listing via Shopify Storefront GraphQL with HTML fallback. | 48 (ok) | women, new, dresses, jeans, sale | `{"item_id":"175898317","title":"Classic High Waist Skinny Jeans - Dark Denim","url":"https://www.fashionnova.com/products/dark-blue-class...` |
| [`homedepot_listing`](#homedepot_listing-category-apollo-bootstrap) | Flaky | bootstrap + html | Home Depot category listing via Apollo state. | 0 (ok) | screwdrivers, drills, paint, light-bulbs, lumber | `n/a` |
| [`homedepot_search`](#homedepot_search-keyword-apollo-bootstrap) | Active | bootstrap + html | Home Depot keyword search via Apollo state. | 24 (ok) | - | `{"item_id":"336787835","sku":"1014334650","brand":"Lukyamzn","title":"14 in. Dual-Core Celeron N4000 Laptop 6 GB RAM 128 GB SSD IPS Displ...` |
| [`jcpenney_listing`](#jcpenney_listing) | Active | api | JCPenney listing spider via search API bootstrap endpoint. | 48 (ok) | womens_tops, mens_shirts | `{"item_id":"ppr5008584232","title":"St. John's Bay Womens Boat Neck Elbow Sleeve T-Shirt","brand":"st. john's bay","url":"https://www.jcp...` |
| [`kohls_listing`](#kohls_listing) | Experimental | api | Kohl’s listing via `/web/catalog/...` API. | 0 (ok) | women, men, sale | `n/a` |
| [`kroger_listing`](#kroger_search--kroger_listing) | Active | bootstrap + html | Kroger category listing with search fallback path. | 31 (ok) | cereal, milk, eggs, bread, coffee, snacks | `{'item_id':'kroger-vitamin-d-whole-milk-gallon','url':'https://www.kroger.com/p/kroger-vitamin-d-whole-milk-gallon/0001111040101','source':'kroger_html_links_fallback'}` |
| [`kroger_search`](#kroger_search--kroger_listing) | Active | bootstrap + html | Kroger keyword search with state extraction + fallback. | 27 (ok) | - | `{'item_id':'kroger-2-reduced-fat-milk-gallon','url':'https://www.kroger.com/p/kroger-2-reduced-fat-milk-gallon/0001111041700','source':'kroger_html_links_fallback'}` |
| [`lululemon_listing`](#lululemon_listing) | Active | bootstrap | lululemon listing spider via Next.js `__NEXT_DATA__`. | 40 (ok) | women-shorts, women-leggings, men-shorts, bags | `{"category":"women-shorts","product_id":"prod11860112","name":"Shake It Out High-Rise Running Short 2.5\"","brand":"lululemon","price":["...` |
| [`maccosmetics_listing`](#maccosmetics_listing) | Experimental | api + bootstrap + html | MAC Cosmetics multi-mode listing spider. | 66 (ok) | face, lips, eyes | `{"item_id":"13854","title":"4.8/5 ( 452 ) Lustreglass Sheer-Shine Lipstick Sheer Coverage, Glossy/High-Shine Finish, Infused With Raspberry Seed/Organic Extra Virgin Olive Oils ...` |
| [`macys_listing`](#macys_listing) | Active | api | Macy’s listing via xapi endpoint (with fallback routing). | 60 (ok) | laptops, shoes, dresses, fragrance, bedding | `{"item_id":"17595303","title":"5Core AC Power Cord 6Ft 3 Prong US Male to Female Extension Adapter 18AWG 10A 7A 125V","brand":"5 Core","u...` |
| [`nordstrom_listing`](#nordstrom_listing) | Experimental | bootstrap + html | Nordstrom listing parser; often blocked/changed. | 0 (timeout2) | women, men, kids, beauty, home, designer, sale | `{}` |
| [`nordstromrack_listing`](#nordstromrack_listing) | Experimental | playwright + html | Nordstrom Rack listing spider via rendered category pages. | 0 (skipped2) | dresses, women, men, shoes | `{}` |
| [`poshmark_listing`](#poshmark_listing) | Experimental | bootstrap | Poshmark listing spider via `window.__INITIAL_STATE__` category grid data. | 48 (ok) | women, men, kids, home, electronics, pets | `{"category":"women","item_id":"6989d90ac4e7b4d4de556bac","title":"🔥Stunning  Farm Rio NWT Size Large Tropical Midi Dress with Sleeves – V...` |
| [`qvc_listing`](#qvc_listing) | Experimental | html | QVC listing spider via direct category HTML parsing. | 102 (ok) | beauty, fashion, home, kitchen | `{"item_id":"A711188","title":"lwya by kim gravel balm bae center core lip balm quad","url":"https://www.qvc.com/lwya-by-kim-gravel-balm-b...` |
| [`saksfifthavenue_listing`](#saksfifthavenue_listing-category) | Experimental | html | Saks Fifth Avenue listing spider via direct category HTML cards. | 24 (ok) | women, men, shoes, beauty, handbags | `{"item_id":"0400026449047","title":"Prada Washed Re Nylon Rain Jacket","url":"https://www.saksfifthavenue.com/product/prada-washed-re-nyl...` |
| [`sallybeauty_listing`](#sallybeauty_listing) | Experimental | api + bootstrap + html | Sally Beauty multi-mode listing spider. | 1 (ok) | hair-color, hair-care, nails | `{"item_id":null,"title":"What's the issue? We’re dedicated to keeping SallyBeauty.com safe from bots and other malicious software. Sometimes a technical issue with your internet...` |
| [`sephora_listing`](#sephora_listing) | Experimental | api | Sephora listing via `/api/v2/catalog/categories/<slug>/seo`. | 60 (ok) | makeup, skincare, gifts, fragrance | `{"item_id":"P517483","title":"Pocket Blush Buildable Hydrating Cream Blush","url":"https://www.sephora.com/product/pocket-blush-P517483?s...` |
| [`stockx_listing`](#stockx_listing) | Experimental | bootstrap + html | StockX listing via `__NEXT_DATA__` bootstrap. | 41 (ok) | sneakers, apparel, electronics, trading-cards, collectibles | `{"item_id":"brands","title":"Brands","url":"https://stockx.com/brands","price":null,"currency":null}` |
| [`target_listing`](#target_listing) | Active (alias) | api | Deprecated alias of `target_search`. | 24 (ok) | - | `{"product_id":"90600286","name":"Women&#39;s Waffle Short Robe - Auden&#8482; Light Gray M/L: Front Tie, Long Sleeve","price":"$35.00","u...` |
| [`target_search`](#target_search) | Active | api | Target RedSky search API spider. | 24 (ok) | - | `{"product_id":"90600286","name":"Women&#39;s Waffle Short Robe - Auden&#8482; Light Gray M/L: Front Tie, Long Sleeve","price":"$35.00","u...` |
| [`ulta_listing`](#ulta_listing-category) | Active | api + html | Ulta category listing (GraphQL default, HTML fallback mode). | 0 (ok) | shampoo, conditioner, cleanser, mascara, moisturizer | `n/a` |
| [`ulta_search`](#ulta_search-keyword) | Active | api + html | Ulta keyword search via GraphQL (with unsorted retry + HTML fallback). | 64 (ok) | - | `{"item_id":"xlsImpprod15511061","title":"All Soft Shampoo","source":"ulta_dxl_graphql"...}` |
| [`walmart_listing`](#walmart_listing-category) | Active | api + html | Walmart category listing spider (direct API+HTML flow). | 45 (ok) | electronics, home, clothing, beauty, toys, sports-and-outdoors, grocery | `{"item_id":"375041225","title":"Restaurado Apple iPhone 12 Restaurado - Desbloqueado para Cualquier Operador - 64GB Negro (Reacondicionad...` |
| [`walmart_search`](#walmart_search-keyword) | Active | api + html | Walmart keyword search spider. | 12 (ok) | - | `{"item_id":"13542163431","title":"ASUS Vivobook Go 15.6” Laptop, Intel i3-N305, 8GB, 256GB, Windows 11 Home in S mode, Cool Silver, E1504...` |

*`Number of items output` reflects recent local smoke runs (typically `max_pages=1`) and can vary by location, anti-bot behavior, and site changes.*

Many listing spiders accept `-a category=<name>` shortcuts (in addition to `-a category_url=<url>`), including Amazon, Walmart, eBay, Home Depot, Best Buy, Costco, and Kroger.

#### Sample output

Below are trimmed examples from recent local test runs (JSONL output, 1 item shown).

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

### walmart_listing (category)
```json
{
  "item_id": null,
  "title": "Restored Dell Latitude 3190 | 11.6\" Touchscreen Laptop PC | Intel Core Pentium Silver N5030 (1.1 GHz) | 8GB RAM | 128GB SSD | Windows 11 Pro $178.00",
  "price": 178.0,
  "url": "https://www.walmart.com/sp/track?...",
  "image_url": "https://i5.walmartimages.com/seo/...jpeg?odnHeight=576&odnWidth=576&odnBg=FFFFFF"
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

### ebay_search (keyword; bootstrap/model-state)
```json
{
  "item_id": "286393092388",
  "title": "Dell Latitude Laptop Computer PC Intel i5 Up To 32GB RAM 1TB SSD Windows 11",
  "url": "https://www.ebay.com/itm/286393092388?...",
  "price": 237.36,
  "currency": "USD",
  "seller": "discountcomputerdepot 99.2% positive (153.3K)",
  "source": "ebay_html_cards_fallback"
}
```

Run example:
`common-scrapy crawl ebay_search -a q=laptop -a max_pages=1 -O ebay_search.jsonl`

Notes:
- Added filtering for non-listing promo cards (e.g. "Shop on eBay") so fallback HTML parsing only yields real `/itm/<id>` products.
- US NordVPN city test (Chicago `us11915`) returned 60 items with `max_pages=1`.
- No-VPN run in this environment often returns 0 items (HTTP 500/anti-bot), so eBay spiders remain marked **Flaky**.

### ebay_listing (category; bootstrap/model-state)

```json
{
  "item_id": null,
  "title": "Apple MacBook Air 13.3'' (256GB SSD, Apple M1, 8GB RAM) Laptop - Space Gray - MGN63LL/A (2020)",
  "url": "https://www.ebay.com/p/9055828714",
  "price": null,
  "currency": null,
  "image_url": "https://i.ebayimg.com/images/g/vtYAAOSwA3tnk8aQ/s-l400.webp",
  "source": "ebay_jsonld_fallback",
  "mode": "category",
  "category_url": "https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276",
  "page": 1,
  "source_url": "https://www.ebay.com/b/Laptops-Netbooks/175672/bn_1648276?_ipg=60&_pgn=1"
}
```

Run example:
`common-scrapy crawl ebay_listing -a category='laptops' -a max_pages=1 -O ebay_listing.jsonl`

Notes:
- Proxy-rendered category HTML may omit `__NEXT_DATA__` and serve unquoted `type=application/ld+json` blocks.
- Spider now parses `ItemList`/`Product` JSON-LD fallback in that HTML mode.

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

### homedepot_listing (category; Apollo/bootstrap + HTML fallback)

Sample output (2026-03-01, no VPN):
```json
[]
```

Run example:
`common-scrapy crawl homedepot_listing -a category='screwdrivers' -a max_pages=1 -O homedepot_listing.jsonl`

Observed logs:
- `HomeDepot listing fallback found 0 items (status=403)`
- feed written with `0 items`

Notes:
- Category and search/listing pages are currently blocked in this environment with Home Depot anti-bot (`403`, `Oops/Error Page`, or `Access Denied`) across multiple US NordVPN cities and sort orders.
- Current fallback paths (`__APOLLO_STATE__`, JSON-LD, and HTML product links) cannot extract items when the origin serves only error/deny responses.
- If this target is business-critical, use a dedicated unblocker/browser-rendering pipeline or provide an approved alternative data source.

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
```json
{
  "item_id": "2565096",
  "sku_id": "2565096",
  "brand": null,
  "title": "3 sizes Hydrate Shampoo for Dry Hair $12.00 - $90.00 Add to bag",
  "list_price": "$12.00 - $90.00",
  "sale_price": null,
  "url": "https://www.ulta.com/p/hydrate-shampoo-dry-hair-pimprod2017791?sku=2565096",
  "image_url": "https://media.ultainc.com/i/ulta/2565096?w=200&$ProductCardNeutralBGLight$&h=200&fmt=auto",
  "source": "ulta_direct_html",
  "mode": "category_html"
}
```

Run examples:
- GraphQL mode (default):
  `common-scrapy crawl ulta_listing -a category='shampoo' -a max_pages=1 -O ulta.jsonl`
- HTML mode:
  `common-scrapy crawl ulta_listing -a category='shampoo' -a mode=html -a max_pages=1 -O ulta_html.jsonl`

Notes:
- GraphQL mode now retries once without `sort` when Ulta blocks sorted requests (e.g. `sort=new`, `sort=price_low`) before falling back to HTML.
- `mode=html` is a fallback parser from rendered product cards and is useful when GraphQL responses are unstable.
- HTML mode typically returns URL/title/image/price text first; GraphQL mode gives richer normalized fields (brand/rating/reviews/sponsored).
- Validation (2026-03-01): GraphQL mode returned `64` items across NordVPN US cities (Dallas, Atlanta, Chicago) for `q=shampoo`, `max_pages=1`; with NordVPN disconnected Ulta returned `403` and `0` items (including HTML fallback).

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
  "item_id": "air-jordan-1-retro-high-og-chicago-lost-and-found",
  "title": "Air Jordan 1 Retro High OG Chicago Lost and Found",
  "url": "https://stockx.com/air-jordan-1-retro-high-og-chicago-lost-and-found",
  "price": null,
  "source": "stockx_next_data|stockx_html_links_fallback"
}
```
Run example:
`common-scrapy crawl stockx_listing -a category=sneakers -a max_pages=1 -O stockx_listing.jsonl`

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
Run example:
`common-scrapy crawl jcpenney_listing -a category=womens_tops -a max_pages=1 -O jcpenney_listing.jsonl`

### dillards_listing
Run example:
`common-scrapy crawl dillards_listing -a category=women -a max_pages=1 -O dillards_listing.jsonl`

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
  "source": "bloomingdales_direct_html"
}
```
Run example:
`common-scrapy crawl bloomingdales_listing -a category=women -a max_pages=1 -O bloomingdales_listing.jsonl`

### qvc_listing
```json
{
  "item_id": "A711188",
  "title": "lwya by kim gravel balm bae center core lip balm quad",
  "url": "https://www.qvc.com/lwya-by-kim-gravel-balm-bae-center-core-lip-balm-quad.product.A711188.html?sc=PRODFEED",
  "price": 29.98,
  "source": "qvc_direct_html"
}
```
Run example:
`common-scrapy crawl qvc_listing -a category=beauty -a max_pages=1 -O qvc_listing.jsonl`

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

`target_listing` is a backwards-compatible alias of `target_search`.

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

Playwright-rendered listing spider for Nordstrom Rack category pages.

Run example:
`common-scrapy crawl nordstromrack_listing -a category=dresses -a max_pages=1 -O nordstromrack_listing.jsonl`

Sample output:
```json
{
  "category": "dresses",
  "product_id": "8210770",
  "name": "One-Shoulder Front Twist A-Line Gown",
  "url": "https://www.nordstromrack.com/s/marina-one-shoulder-front-twist-a-line-gown/8210770?origin=category-personalizedsort&breadcrumb=Home%2FWomen%2FClothing%2FDresses",
  "image": "https://n.nordstrommedia.com/it/b91a2122-b716-4559-b990-4fc031eed7ca.jpeg?h=368&w=240&dpr=2",
  "source_url": "https://www.nordstromrack.com/shop/women/clothing/dresses?page=1",
  "page": 1,
  "mode": "listing"
}
```

### bestbuy_search / bestbuy_listing

Best Buy pages currently use Apollo hydration (not `__NEXT_DATA__` on PLP/search). These spiders use Playwright to render the page, then extract normalized data from `ApolloClientSingleton.cache.extract()` (with inline bootstrap parsing fallback).

If Best Buy serves a challenge/error variant, output may still be empty; Playwright materially improves reliability versus plain HTTP fetch.

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

These spiders try bootstrap state extraction first (`__NEXT_DATA__` / `__APOLLO_STATE__`), then fallback to JSON-LD and direct product-link HTML parsing.

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
  "title": null,
  "url": "https://www.costco.com/kirkland-signature-colombian-coffee-dark-roast-3-lbs.product.100361434.html",
  "price": null,
  "currency": null,
  "brand": null,
  "rating": null,
  "reviews_count": null,
  "image_url": null,
  "source": "costco_html_links_fallback",
  "raw": null,
  "mode": "category",
  "category_url": "https://www.costco.com/coffee.html",
  "page": 1,
  "source_url": "https://www.costco.com/coffee.html"
}
```

Notes:
- Browser HTML inspection confirms Costco search results render product links for `keyword=coffee` in this runtime.
- NordVPN US city variance observed while testing `costco_search` (`max_pages=1`): Ashburn (`us9512`) → 24 items, Los Angeles (`us5864`) → 24 items, Dallas (`us8104`) → 0 items. HTML links fallback remains the most reliable extraction path.

### kroger_search / kroger_listing

These spiders try bootstrap state extraction first (`__NEXT_DATA__` / `__APOLLO_STATE__`), then fallback to JSON-LD and direct product-link HTML parsing.

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
  "item_id": "kroger-vitamin-d-whole-milk-gallon",
  "title": null,
  "url": "https://www.kroger.com/p/kroger-vitamin-d-whole-milk-gallon/0001111040101",
  "price": null,
  "currency": null,
  "brand": null,
  "rating": null,
  "reviews_count": null,
  "image_url": null,
  "source": "kroger_html_links_fallback",
  "mode": "category",
  "category_url": "https://www.kroger.com/pl/milk/02001",
  "page": 1,
  "source_url": "https://www.kroger.com/pl/milk/02001"
}
```

Run examples:
- `common-scrapy crawl kroger_search -a q='milk' -a max_pages=1 -O kroger_search.jsonl`
- `common-scrapy crawl kroger_listing -a category='milk' -a max_pages=1 -O kroger_listing.jsonl`

Notes:
- Added sort variant retries (`bestMatch`, `sale`) to mitigate zero-item responses from Akamai caches; `kroger_search` now emits ~27 items via HTML link fallback even when bootstrap state is stripped.
- Listing spider now captures escaped `/p/slug` references that Kroger injects inside serialized props, so categories like `milk` return ~31 URLs before the search fallback is considered.
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

### sallybeauty_listing
```json
{
  "item_id": null,
  "title": "Gift Cards",
  "url": "https://www.sallybeauty.com/giftCards.html",
  "price": null,
  "currency": null,
  "brand": "Sally Beauty",
  "source": "sallybeauty_html",
  "mode": "category_html",
  "category_url": "https://www.sallybeauty.com/hair-care/"
}
```
Run examples:
- `common-scrapy crawl sallybeauty_listing -a category='hair-care' -a mode=api -a max_pages=1 -O sally_api.jsonl`
- `common-scrapy crawl sallybeauty_listing -a category='hair-care' -a mode=bootstrap -a max_pages=1 -O sally_bootstrap.jsonl`
- `common-scrapy crawl sallybeauty_listing -a category='hair-care' -a mode=html -a max_pages=1 -O sally_html.jsonl`

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
  "item_id": "ELF-12345",
  "title": "Primer ...",
  "url": "https://www.elfcosmetics.com/products/...",
  "price": 10.0,
  "currency": "USD",
  "brand": "e.l.f. Cosmetics",
  "source": "elfcosmetics_internal_api|elfcosmetics_preloaded_state|elfcosmetics_html"
}
```
Run examples:
- `common-scrapy crawl elfcosmetics_listing -a category='face' -a mode=api -a max_pages=1 -O elf_api.jsonl`
- `common-scrapy crawl elfcosmetics_listing -a category='face' -a mode=bootstrap -a max_pages=1 -O elf_bootstrap.jsonl`
- `common-scrapy crawl elfcosmetics_listing -a category='face' -a mode=html -a max_pages=1 -O elf_html.jsonl`

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
  "source": "ae_html",
  "mode": "category_html"
}
```
Run example:
- `common-scrapy crawl ae_listing -a category='women-tops' -a max_pages=1 -O ae_listing.jsonl`

Notes:
- Verified in browser and direct HTTP while connected to NordVPN US (Dallas + Seattle).
- In this environment, HTML category pages contain stable product cards/links (`/us/en/p/...`) suitable for listing extraction.

## Contributing

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
