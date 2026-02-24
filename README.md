# Common Scrapy Retailer Spiders

An open, well-maintained collection of Scrapy spiders for harvesting structured product data from major retailers. Spiders are purpose-built per retailer with bootstrap/API/HTML fallback logic where needed.

## Installation

```bash
pip install common-scrapy
```

## CLI usage

`pip install common-scrapy` adds a `common-scrapy` console script so you can work with the packaged spider without cloning the repo.

### Proxy configuration

This project reads `PROXY` from a local `.env` file (recommended) via `python-dotenv`.

- Create `./.env` (it’s gitignored) with:
  ```
  PROXY=http://user:pass@host:1234
  ```
- Or you can still pass it inline for one-off runs:
  ```bash
  PROXY=http://user:pass@host:1234 common-scrapy crawl kohls_listing -a category=women
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

| Spider Name | Status | Method | Description |
|---|---|---|---|
| [`amazon_search`](#amazon_search) | Active | html | Amazon keyword search spider. |
| [`amazon_listing`](#amazon_listing-category) | Active | html | Amazon category listing spider (category shortcuts). |
| [`walmart_search`](#walmart_search-keyword) | Active | api + html | Walmart keyword search spider. |
| [`walmart_listing`](#walmart_listing-category) | Active | api + html | Walmart category listing spider with anti-bot fallback. |
| [`ebay_search`](#ebay_search-keyword-bootstrapmodel-state) | Flaky | bootstrap + html | eBay keyword search via `__NEXT_DATA__` + fallback. |
| [`ebay_listing`](#ebay_listing-category-bootstrapmodel-state) | Flaky | bootstrap + html | eBay category listing via `__NEXT_DATA__` + fallback. |
| [`homedepot_search`](#homedepot_search-keyword-apollo-bootstrap) | Active | bootstrap + html | Home Depot keyword search via Apollo state. |
| [`homedepot_listing`](#homedepot_listing-category-apollo-bootstrap) | Flaky | bootstrap + html | Home Depot category listing via Apollo state. |
| [`macys_listing`](#macys_listing) | Active | api | Macy’s listing via xapi endpoint (with fallback routing). |
| [`ulta_search`](#ulta_search-keyword) | Flaky | api | Ulta keyword search via GraphQL. |
| [`ulta_listing`](#ulta_listing-category) | Active | api + html | Ulta category listing (GraphQL default, HTML fallback mode). |
| [`kohls_listing`](#kohls_listing) | Experimental | api | Kohl’s listing via `/web/catalog/...` API. |
| [`sephora_listing`](#sephora_listing) | Experimental | api | Sephora listing via `/api/v2/catalog/categories/<slug>/seo`. |
| [`stockx_listing`](#stockx_listing) | Experimental | bootstrap + html | StockX listing via `__NEXT_DATA__` bootstrap. |
| [`fashionnova_listing`](#fashionnova_listing) | Active | api + html | Fashion Nova listing via Shopify Storefront GraphQL with HTML fallback. |
| [`target_search`](#target_search) | Active | api | Target RedSky search API spider. |
| [`target_listing`](#target_search) | Active (alias) | api | Deprecated alias of `target_search`. |
| [`nordstrom_listing`](#nordstrom_listing) | Experimental | bootstrap + html | Nordstrom listing parser; often blocked/changed. |
| [`bestbuy_search`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | Best Buy search via Playwright + Apollo cache extract. |
| [`bestbuy_listing`](#bestbuy_search--bestbuy_listing) | Flaky | bootstrap + html | Best Buy listing via Playwright + Apollo cache extract. |
| [`costco_search`](#costco_search--costco_listing) | Active | bootstrap + html | Costco keyword search with state extraction + fallback. |
| [`costco_listing`](#costco_search--costco_listing) | Active | bootstrap + html | Costco category listing with state extraction + fallback. |
| [`kroger_search`](#kroger_search--kroger_listing) | Active | bootstrap + html | Kroger keyword search with state extraction + fallback. |
| [`kroger_listing`](#kroger_search--kroger_listing) | Flaky | bootstrap + html | Kroger category listing with search fallback path. |
| [`bathandbodyworks_listing`](#bathandbodyworks_listing) | Experimental | api + bootstrap + html | Bath & Body Works multi-mode listing spider. |
| [`sallybeauty_listing`](#sallybeauty_listing) | Experimental | api + bootstrap + html | Sally Beauty multi-mode listing spider. |
| [`maccosmetics_listing`](#maccosmetics_listing) | Experimental | api + bootstrap + html | MAC Cosmetics multi-mode listing spider. |
| [`elfcosmetics_listing`](#elfcosmetics_listing) | Experimental | api + bootstrap + html | e.l.f. Cosmetics multi-mode listing spider. |
| [`ae_listing`](#ae_listing) | Experimental | html | American Eagle listing spider via category-page product cards. |

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

Run example:
`common-scrapy crawl walmart_search -a q=laptop -a max_pages=1 -O walmart_search.jsonl`

### ebay_search (keyword; bootstrap/model-state)
```json
{
  "item_id": "166543210987",
  "title": "Apple iPhone 14 Pro Max 256GB - Space Black (Unlocked)",
  "url": "https://www.ebay.com/itm/166543210987",
  "price": 899.99,
  "currency": "USD",
  "seller": "top_seller_store",
  "condition": "Used"
}
```

Run example:
`common-scrapy crawl ebay_search -a q='iphone 14 pro' -a max_pages=1 -O ebay_search.jsonl`

### ebay_listing (category; bootstrap/model-state)

Run example:
`common-scrapy crawl ebay_listing -a category='laptops' -a max_pages=1 -O ebay_listing.jsonl`

### homedepot_search (keyword; Apollo bootstrap)

Run example:
`common-scrapy crawl homedepot_search -a q='screwdriver' -a max_pages=1 -O homedepot_search.jsonl`

### homedepot_listing (category; Apollo bootstrap)

Run example:
`common-scrapy crawl homedepot_listing -a category='screwdrivers' -a max_pages=1 -O homedepot_listing.jsonl`

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
  "source": "macys_xapi_discover_v1_page_via_r.jina.ai"
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
- `mode=html` is a fallback parser from rendered product cards and is useful when GraphQL responses are unstable.
- HTML mode typically returns URL/title/image/price text first; GraphQL mode gives richer normalized fields (brand/rating/reviews/sponsored).

### ulta_search (keyword)

Run example:
`common-scrapy crawl ulta_search -a q=shampoo -a max_pages=1 -O ulta_search.jsonl`

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

### nordstrom_listing

Currently blocked in this environment (often returns anti-bot interstitial / wrapper HTML), so sample output may be empty.

### bestbuy_search / bestbuy_listing

Best Buy pages currently use Apollo hydration (not `__NEXT_DATA__` on PLP/search). These spiders use Playwright to render the page, then extract normalized data from `ApolloClientSingleton.cache.extract()` (with inline bootstrap parsing fallback).

If Best Buy serves a challenge/error variant, output may still be empty; Playwright materially improves reliability versus plain HTTP fetch.

### costco_search / costco_listing

These spiders try bootstrap state extraction first (`__NEXT_DATA__` / `__APOLLO_STATE__`), then fallback to JSON-LD and direct product-link HTML parsing.

Run examples:
- `common-scrapy crawl costco_search -a q='coffee' -a max_pages=1 -O costco_search.jsonl`
- `common-scrapy crawl costco_listing -a category='coffee' -a max_pages=1 -O costco_listing.jsonl`

### kroger_search / kroger_listing

These spiders try bootstrap state extraction first (`__NEXT_DATA__` / `__APOLLO_STATE__`), then fallback to JSON-LD and direct product-link HTML parsing.

Run examples:
- `common-scrapy crawl kroger_search -a q='milk' -a max_pages=1 -O kroger_search.jsonl`
- `common-scrapy crawl kroger_listing -a category='cereal' -a max_pages=1 -O kroger_listing.jsonl`

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
  "source": "elfcosmetics_internal_api|elfcosmetics_html"
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
