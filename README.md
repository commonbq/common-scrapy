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

Standalone spiders also honor `PROXY` (some require `-a use_proxy=1` depending on spider).

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

- Purpose-built: `common-scrapy crawl target_listing -a keyword=sneakers -a max_pages=2 -O target.jsonl`
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

- `amazon_listing` – keyword listing spider.
- `walmart_listing` – listing spider with anti-bot fallback.
- `macys_listing` – Macy’s xapi listing (may route via fallback when blocked).
- `ulta_listing` – Ulta GraphQL listing API.
- `target_search` – Target RedSky (plp_search_v2) search API.
- `target_listing` – deprecated alias for `target_search`.
- `nordstrom_listing` – currently experimental (HTML script-tag extraction; often blocked).

#### Sample output

Below are trimmed examples from recent local test runs (JSONL output, 1 item shown).

**amazon_listing**
```json
{
  "asin": "B08NF2W2V2",
  "title": "INZCOU",
  "price": 36.98,
  "url": "https://www.amazon.com/s?k=sneakers",
  "image_url": "https://m.media-amazon.com/images/I/71Akg8OEbXL._AC_UL320_.jpg"
}
```

**walmart_listing**
```json
{
  "item_id": null,
  "title": "Restored Dell Latitude 3190 | 11.6\" Touchscreen Laptop PC | Intel Core Pentium Silver N5030 (1.1 GHz) | 8GB RAM | 128GB SSD | Windows 11 Pro $178.00",
  "price": 178.0,
  "url": "https://www.walmart.com/sp/track?...",
  "image_url": "https://i5.walmartimages.com/seo/...jpeg?odnHeight=576&odnWidth=576&odnBg=FFFFFF"
}
```

**macys_listing**
```json
{
  "item_id": "25092672",
  "title": "Floral Stickers Laptop, 74 Pcs, Stickers for Water Bottles,",
  "brand": "Mr. Pen",
  "price": 6.99,
  "url": "https://www.macys.com/shop/product/floral-stickers-laptop-74-pcs-stickers-for-water-bottles?ID=25092672",
  "image_url": "7/optimized/34925717_fpx.tif"
}
```

**ulta_listing**
```json
{
  "item_id": "xlsImpprod15511061",
  "sku_id": "2580410",
  "brand": "Redken",
  "title": "All Soft Shampoo",
  "list_price": "$11.00 - $56.00",
  "sale_price": null,
  "url": "https://www.ulta.com/p/all-soft-shampoo-xlsImpprod15511061?sku=2580410",
  "image_url": "https://media.ulta.com/i/ulta/2580410"
}
```

**target_search**
```json
{
  "product_id": "94568023",
  "name": "Women&#8217;s Skyler Sneakers with Memory Foam Insole &#8211; Universal Thread&#8482; Dark Brown 8",
  "price": "$27.00",
  "url": "https://www.target.com/p/women-8217-s-skyler-sneakers-with-memory-foam-insole-8211-universal-thread-8482-dark-brown-8/-/A-94568023",
  "image": "https://target.scene7.com/is/image/Target/GUEST_462ecc94-caac-418f-9d72-920828dacadb"
}
```

**nordstrom_listing**

Currently blocked in this environment (often returns anti-bot interstitial / wrapper HTML), so sample output may be empty.

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
