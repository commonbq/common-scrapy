# Common Scrapy Templates

An open, well-maintained collection of Scrapy templates for harvesting structured product data from major retailers. Each template encodes the HTTP request, pagination strategy, and response extraction rules needed for a specific storefront so you can stay focused on downstream data processing.

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
  PROXY=http://user:pass@host:1234 common-scrapy crawl kohls_products
  ```

Standalone spiders also honor `PROXY`.

### List available templates

```bash
common-scrapy list
```

### Run a crawl

```bash
common-scrapy crawl <identifier> [additional Scrapy args]
```

`<identifier>` resolution:

- If `<identifier>` matches a purpose-built spider name (e.g. `target_listing`), it runs that spider.
- Otherwise, it treats `<identifier>` as a template name and runs the parameterized `common` spider with `-a name=<identifier>`.

Examples:

- Purpose-built: `common-scrapy crawl target_search -a category=5xtc0 -a max_pages=2 -O target.jsonl`
- Template: `common-scrapy crawl kohls_products -s LOG_LEVEL=INFO`
- Template: `common-scrapy crawl sephora_products -o sephora.csv`

All extra args are forwarded to `scrapy crawl` unchanged (feeds, settings overrides, etc.).

## Available spiders / templates

### Template-driven (via `common-scrapy crawl <template>`)

(Templates are only used when there is no purpose-built spider with the same name.)

- `kohls_products` – product listing crawl for Kohl's seasonal catalog endpoints.
- `sephora_products` – product listing crawl for Sephora category APIs.

#### Sample output

**sephora_products** (1 item, trimmed)
```json
{
  "brandName": "rhode",
  "displayName": "Pocket Blush Buildable Hydrating Cream Blush",
  "productId": "P517483",
  "targetUrl": "/product/pocket-blush-P517483?skuId=2895845",
  "heroImage": "https://www.sephora.com/productimages/sku/s2895845-main-zoom.jpg?imwidth=270&pb=clean-at-sephora",
  "rating": "4.0598",
  "reviews": "1153"
}
```

**kohls_products**

Kohl’s `/web/catalog/...` endpoint is currently **blocked from this environment** (returns Access Denied / non-JSON), so we can’t produce a live crawl sample right now. The repository includes a captured sample payload at:
`common/templates/kohls_products/sample_response.json`

### Standalone spiders (via `scrapy crawl <spider>`)

These live under `common/spiders/*_listing_spider.py` and are purpose-built per retailer.

- `amazon_listing` – category listing spider (requires category).
- `amazon_search` – keyword search spider.
- `walmart_listing` – category listing spider with anti-bot fallback.
- `walmart_search` – keyword search spider.
- `ebay_listing` – eBay category listing spider using bootstrap/model-state (`__NEXT_DATA__`) extraction with JSON-LD fallback.
- `ebay_search` – eBay keyword search spider using bootstrap/model-state (`__NEXT_DATA__`) extraction with JSON-LD fallback.
- `homedepot_listing` – Home Depot category listing spider using Apollo bootstrap state (`__APOLLO_STATE__`).
- `homedepot_search` – Home Depot keyword search spider using Apollo bootstrap state (`__APOLLO_STATE__`).
- `macys_listing` – Macy’s xapi listing (may route via fallback when blocked).
- `ulta_listing` – Ulta category listing with two modes: GraphQL (`/dxl/graphql`, default) and direct HTML card parsing (`-a mode=html`).
- `ulta_search` – Ulta keyword search (GraphQL).
- `target_search` – Target RedSky (plp_search_v2) search API.
- `target_listing` – deprecated alias for `target_search`.
- `nordstrom_listing` – currently experimental (HTML script-tag extraction; often blocked).
- `bestbuy_search` – Best Buy keyword search using Playwright + Apollo state extraction (`ApolloClientSingleton.cache.extract()`).
- `bestbuy_listing` – Best Buy category/listing crawl using Playwright + Apollo state extraction (`ApolloClientSingleton.cache.extract()`).
- `costco_search` – Costco keyword search spider with bootstrap (`__NEXT_DATA__`/`__APOLLO_STATE__`) + HTML fallback extraction.
- `costco_listing` – Costco category listing spider with bootstrap (`__NEXT_DATA__`/`__APOLLO_STATE__`) + HTML fallback extraction.
- `kroger_search` – Kroger keyword search spider with bootstrap (`__NEXT_DATA__`/`__APOLLO_STATE__`) + HTML fallback extraction.
- `kroger_listing` – Kroger category listing spider with bootstrap (`__NEXT_DATA__`/`__APOLLO_STATE__`) + HTML fallback extraction.
- `bathandbodyworks_listing` – Bath & Body Works listing spider with mode priority: internal API (`mode=api`), bootstrap (`mode=bootstrap`), HTML (`mode=html`).
- `sallybeauty_listing` – Sally Beauty listing spider with mode priority: internal API (`mode=api`), bootstrap (`mode=bootstrap`), HTML (`mode=html`).
- `maccosmetics_listing` – MAC Cosmetics listing spider with mode priority: internal API (`mode=api`, GraphQL endpoint), bootstrap (`mode=bootstrap`), HTML (`mode=html`).
- `elfcosmetics_listing` – e.l.f. Cosmetics listing spider with mode priority: internal API (`mode=api`), bootstrap (`mode=bootstrap`), HTML (`mode=html`).

Many listing spiders accept `-a category=<name>` shortcuts (in addition to `-a category_url=<url>`), including Amazon, Walmart, eBay, Home Depot, Best Buy, Costco, and Kroger.

#### Sample output

Below are trimmed examples from recent local test runs (JSONL output, 1 item shown).

**amazon_search**
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

**amazon_listing** (category)

Supported built-in categories:
`electronics`, `fashion`, `beauty`, `home-kitchen`, `toys-games`, `sports-outdoors`, `grocery`, `books`.

Notes:
- Uses Amazon search query URLs (`/s?k=...`) for category shortcuts.
- If a page returns no cards, spider logs a warning with URL/title to help diagnose layout/response changes.

Run example:
`common-scrapy crawl amazon_listing -a category=electronics -a max_pages=1 -O amazon_cat.jsonl`

**walmart_listing** (category)
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

**walmart_search** (keyword)

Run example:
`common-scrapy crawl walmart_search -a q=laptop -a max_pages=1 -O walmart_search.jsonl`

**ebay_search** (keyword; bootstrap/model-state)
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

**ebay_listing** (category; bootstrap/model-state)

Run example:
`common-scrapy crawl ebay_listing -a category='laptops' -a max_pages=1 -O ebay_listing.jsonl`

**homedepot_search** (keyword; Apollo bootstrap)

Run example:
`common-scrapy crawl homedepot_search -a q='screwdriver' -a max_pages=1 -O homedepot_search.jsonl`

**homedepot_listing** (category; Apollo bootstrap)

Run example:
`common-scrapy crawl homedepot_listing -a category='screwdrivers' -a max_pages=1 -O homedepot_listing.jsonl`

**macys_listing**
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

**ulta_listing** (category)
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

**ulta_search** (keyword)

Run example:
`common-scrapy crawl ulta_search -a q=shampoo -a max_pages=1 -O ulta_search.jsonl`

**target_search**
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

**nordstrom_listing**

Currently blocked in this environment (often returns anti-bot interstitial / wrapper HTML), so sample output may be empty.

**bestbuy_search / bestbuy_listing**

Best Buy pages currently use Apollo hydration (not `__NEXT_DATA__` on PLP/search). These spiders use Playwright to render the page, then extract normalized data from `ApolloClientSingleton.cache.extract()` (with inline bootstrap parsing fallback).

If Best Buy serves a challenge/error variant, output may still be empty; Playwright materially improves reliability versus plain HTTP fetch.

**costco_search / costco_listing**

These spiders try bootstrap state extraction first (`__NEXT_DATA__` / `__APOLLO_STATE__`), then fallback to JSON-LD and direct product-link HTML parsing.

Run examples:
- `common-scrapy crawl costco_search -a q='coffee' -a max_pages=1 -O costco_search.jsonl`
- `common-scrapy crawl costco_listing -a category='coffee' -a max_pages=1 -O costco_listing.jsonl`

**kroger_search / kroger_listing**

These spiders try bootstrap state extraction first (`__NEXT_DATA__` / `__APOLLO_STATE__`), then fallback to JSON-LD and direct product-link HTML parsing.

Run examples:
- `common-scrapy crawl kroger_search -a q='milk' -a max_pages=1 -O kroger_search.jsonl`
- `common-scrapy crawl kroger_listing -a category='cereal' -a max_pages=1 -O kroger_listing.jsonl`

**bathandbodyworks_listing**
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

**sallybeauty_listing**
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

**maccosmetics_listing**
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

**elfcosmetics_listing**
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

## Contributing

Issues and pull requests that add or improve retailer templates, pagination logic, or extraction helpers are welcome. Please keep templates well-commented, anonymize sensitive identifiers, and include notes on any authentication or proxy requirements to keep the collection healthy for the community.

### Project layout

- `common/spiders/common_spider.py` – single parameterized spider that loads retailer-specific templates and converts API responses into normalized items.
- `common/templates/` – each retailer lives in its own folder (for example, `common/templates/<retailer>/`) with three files:
  - `request.json` – captured HTTP request, headers, query/body params, and pagination strategy.
  - `sample.json` – a trimmed API response saved from the network inspector so you can reason about the payload without re-running the crawl.
  - `extract.json` – schema describing what to copy out of the payload (see “Iterating on extraction”).
- `common/settings/` – shared Scrapy configuration; reads environment variables via `.env`.
- `scrapy.cfg` – entry point for the `scrapy` CLI.

### Iterating on extraction

- Reference `sample.json` to understand the payload shape without replaying the crawl.
- Update `extract.json` to control which fields land in the final item. Set `$list` to the array that contains products, `$include` for top-level metadata to copy onto every record, and `$item` for nested lookups inside each product.
- Save the file and re-run the spider to confirm you get the expected output.

### Adding new retailer templates

1. Capture a representative network request (e.g., via DevTools) and save the HAR snippet into `common/templates/<retailer>/request.json`.
2. Grab a sample JSON response (copy/paste the network preview) and drop it into `common/templates/<retailer>/sample.json`. Update it as the API evolves.
3. Populate `extract.json` with `$list`, `$include`, and `$item` sections so the spider knows which fields to emit.
4. Run the spider with `scrapy crawl common -a name=<retailer>` to verify it paginates and emits data.
